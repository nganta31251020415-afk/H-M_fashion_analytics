"""
Feature Engineering Script for H&M Customer & RFM Features

This script processes cleaned transaction and customer data from:
    - data/processed/cleaned_transactions.parquet
    - data/processed/cleaned_customers.parquet

It calculates Customer-level behavioral and demographic features, including:
    - Recency (days since last transaction relative to overall max dataset date)
    - Frequency (number of distinct transaction dates)
    - Monetary (total spend)
    - Tenure (days between first and last purchase)
    - Category Diversity (number of distinct article_ids purchased)
    - RFM Quintile Scores (1 to 5 for R, F, M)
    - RFM_Score string (e.g. '555')
    - RFM_Segment (Champions, Loyal, New Customers, At Risk, Lost, Others)

Output:
    - data/marts/customer_features.parquet
"""

from pathlib import Path
import time
import duckdb


def build_customer_features(
    transactions_parquet_path: Path,
    customers_parquet_path: Path,
    output_parquet_path: Path
) -> None:
    """
    Calculates Customer & RFM features using DuckDB for memory efficiency,
    scores RFM quintiles, segments customers, validates output, and exports to Parquet.

    Args:
        transactions_parquet_path (Path): Path to cleaned_transactions.parquet.
        customers_parquet_path (Path): Path to cleaned_customers.parquet.
        output_parquet_path (Path): Path to save customer_features.parquet.
    """
    start_time = time.time()
    print("=" * 70)
    print("Starting Customer & RFM Feature Engineering Pipeline")
    print("=" * 70)

    con = duckdb.connect()

    # Step 1: Input Data Verification & Max Date Determination
    print(f"\n[Step 1] Reading input files:")
    print(f" -> Customers: {customers_parquet_path}")
    print(f" -> Transactions: {transactions_parquet_path}")

    tx_parquet_str = transactions_parquet_path.as_posix()
    cust_parquet_str = customers_parquet_path.as_posix()

    total_customers = con.execute(
        f"SELECT COUNT(*) FROM read_parquet('{cust_parquet_str}')"
    ).fetchone()[0]
    
    max_date = con.execute(
        f"SELECT MAX(t_dat) FROM read_parquet('{tx_parquet_str}')"
    ).fetchone()[0]

    print(f" -> Total Customers in Database: {total_customers:,}")
    print(f" -> Overall Max Transaction Date (Reference Date): {max_date}")

    # Step 2: Compute Aggregated Customer Features & Join Demographics
    print("\n[Step 2] Aggregating transaction history & calculating customer features...")
    
    query = f"""
    CREATE OR REPLACE TABLE customer_features_raw AS
    WITH tx_agg AS (
        SELECT 
            customer_id,
            MIN(t_dat) AS first_purchase_date,
            MAX(t_dat) AS last_purchase_date,
            DATEDIFF('day', MAX(t_dat), DATE '{max_date}') AS recency,
            CAST(COUNT(DISTINCT t_dat) AS INTEGER) AS frequency,
            CAST(SUM(price) AS DOUBLE) AS monetary,
            CAST(DATEDIFF('day', MIN(t_dat), MAX(t_dat)) AS INTEGER) AS tenure,
            CAST(COUNT(DISTINCT article_id) AS INTEGER) AS category_diversity
        FROM read_parquet('{tx_parquet_str}')
        GROUP BY customer_id
    )
    SELECT 
        c.customer_id,
        c.FN,
        c.Active,
        c.club_member_status,
        c.fashion_news_frequency,
        c.age,
        c.postal_code,
        a.first_purchase_date,
        a.last_purchase_date,
        COALESCE(a.recency, DATEDIFF('day', DATE '2018-09-20', DATE '{max_date}')) AS recency,
        COALESCE(a.frequency, 0) AS frequency,
        COALESCE(a.monetary, 0.0) AS monetary,
        COALESCE(a.tenure, 0) AS tenure,
        COALESCE(a.category_diversity, 0) AS category_diversity,
        (a.customer_id IS NOT NULL) AS has_transactions
    FROM read_parquet('{cust_parquet_str}') c
    LEFT JOIN tx_agg a ON c.customer_id = a.customer_id
    """
    con.execute(query)

    # Step 3: Compute RFM Quintiles & Apply Segment Business Rules
    print("\n[Step 3] Computing RFM Quintiles & Segment Classification...")

    scoring_query = """
    CREATE OR REPLACE TABLE customer_features AS
    WITH rfm_scoring AS (
        SELECT 
            *,
            CAST(NTILE(5) OVER (ORDER BY recency DESC) AS TINYINT) AS r_score,
            CAST(NTILE(5) OVER (ORDER BY frequency ASC) AS TINYINT) AS f_score,
            CAST(NTILE(5) OVER (ORDER BY monetary ASC) AS TINYINT) AS m_score
        FROM customer_features_raw
    )
    SELECT 
        customer_id,
        FN,
        Active,
        club_member_status,
        fashion_news_frequency,
        age,
        postal_code,
        first_purchase_date,
        last_purchase_date,
        recency,
        frequency,
        monetary,
        tenure,
        category_diversity,
        has_transactions,
        r_score,
        f_score,
        m_score,
        (r_score || f_score || m_score) AS rfm_score,
        CASE 
            WHEN r_score >= 4 AND f_score >= 4 AND m_score >= 4 THEN 'Champions'
            WHEN f_score >= 4 THEN 'Loyal'
            WHEN r_score >= 4 AND f_score = 1 THEN 'New Customers'
            WHEN r_score <= 2 AND f_score >= 3 THEN 'At Risk'
            WHEN r_score <= 2 AND f_score <= 2 THEN 'Lost'
            ELSE 'Others'
        END AS rfm_segment
    FROM rfm_scoring
    """
    con.execute(scoring_query)

    # Step 4: Run Data Validation Checks
    print("\n[Step 4] Running Data Integrity & Validation Checks...")
    
    output_count = con.execute("SELECT COUNT(*) FROM customer_features").fetchone()[0]
    print(f" -> Output total customer count: {output_count:,}")
    assert output_count == total_customers, f"Row count mismatch! Expected {total_customers}, got {output_count}"

    transacting_count = con.execute("SELECT COUNT(*) FROM customer_features WHERE has_transactions = TRUE").fetchone()[0]
    print(f" -> Transacting customer count: {transacting_count:,}")

    null_cust_ids = con.execute("SELECT COUNT(*) FROM customer_features WHERE customer_id IS NULL").fetchone()[0]
    assert null_cust_ids == 0, "Found NULL customer_id in customer_features!"

    rfm_nulls = con.execute(
        "SELECT COUNT(*) FROM customer_features WHERE r_score IS NULL OR f_score IS NULL OR m_score IS NULL"
    ).fetchone()[0]
    assert rfm_nulls == 0, "Found NULL RFM scores in customer_features!"

    invalid_scores = con.execute(
        "SELECT COUNT(*) FROM customer_features WHERE r_score NOT BETWEEN 1 AND 5 OR f_score NOT BETWEEN 1 AND 5 OR m_score NOT BETWEEN 1 AND 5"
    ).fetchone()[0]
    assert invalid_scores == 0, "Found RFM scores outside range [1, 5]!"

    print(" -> Data Validation Passed: 100% complete, no orphan IDs, no invalid RFM scores.")

    # Step 5: Segment Distribution Summary
    print("\n" + "=" * 70)
    print("CUSTOMER RFM SEGMENT DISTRIBUTION SUMMARY")
    print("=" * 70)
    segment_df = con.execute("""
        SELECT 
            rfm_segment,
            COUNT(*) AS customer_count,
            ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS percentage,
            ROUND(AVG(recency), 1) AS avg_recency_days,
            ROUND(AVG(frequency), 1) AS avg_frequency,
            ROUND(AVG(monetary), 4) AS avg_monetary,
            ROUND(AVG(category_diversity), 1) AS avg_diversity
        FROM customer_features
        GROUP BY rfm_segment
        ORDER BY customer_count DESC
    """).df()

    print(segment_df.to_string(index=False))
    print("=" * 70)

    # Step 6: Export Output to Parquet
    print(f"\n[Step 5] Exporting results to Parquet format...")
    output_parquet_path.parent.mkdir(parents=True, exist_ok=True)
    con.execute(f"COPY customer_features TO '{output_parquet_path.as_posix()}' (FORMAT PARQUET, COMPRESSION ZSTD)")
    
    file_size_mb = output_parquet_path.stat().st_size / (1024 * 1024)
    elapsed = time.time() - start_time
    print(f" -> Output File: {output_parquet_path}")
    print(f" -> File Size: {file_size_mb:.2f} MB")
    print(f" -> Execution Time: {elapsed:.2f} seconds")
    print("\nFeature Engineering Phase 3 Part 1 Completed Successfully!")


if __name__ == "__main__":
    project_root = Path(__file__).resolve().parents[2]
    
    transactions_path = project_root / "data" / "processed" / "cleaned_transactions.parquet"
    customers_path = project_root / "data" / "processed" / "cleaned_customers.parquet"
    output_path = project_root / "data" / "marts" / "customer_features.parquet"

    build_customer_features(
        transactions_parquet_path=transactions_path,
        customers_parquet_path=customers_path,
        output_parquet_path=output_path
    )
