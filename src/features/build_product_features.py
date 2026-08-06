"""
Feature Engineering Script for H&M Product & Time Features

This script processes cleaned transaction and article catalog data from:
    - data/processed/cleaned_transactions.parquet
    - data/processed/cleaned_articles.parquet

It calculates Product-level behavioral, velocity, and seasonality features, including:
    - First & Last Sale Dates & Active Selling Lifecycle (days)
    - Total Revenue & Total Sales Count
    - Unique Customers Count
    - Sales Velocity in First 30 Days (from product launch/first transaction date)
    - Seasonal Breakdown (Spring: Mar-May, Summer: Jun-Aug, Autumn: Sep-Nov, Winter: Dec-Feb)
    - Peak Season Classification

Output:
    - data/marts/product_features.parquet
"""

from pathlib import Path
import time
import duckdb


def build_product_features(
    transactions_parquet_path: Path,
    articles_parquet_path: Path,
    output_parquet_path: Path
) -> None:
    """
    Calculates Product & Time/Seasonality features using DuckDB for high performance,
    validates output integrity, and exports to Parquet format.

    Args:
        transactions_parquet_path (Path): Path to cleaned_transactions.parquet.
        articles_parquet_path (Path): Path to cleaned_articles.parquet.
        output_parquet_path (Path): Path to save product_features.parquet.
    """
    start_time = time.time()
    print("=" * 70)
    print("Starting Product & Time Feature Engineering Pipeline")
    print("=" * 70)

    con = duckdb.connect()

    # Step 1: Input Data Verification
    print(f"\n[Step 1] Reading input files:")
    print(f" -> Articles Catalog: {articles_parquet_path}")
    print(f" -> Transactions: {transactions_parquet_path}")

    tx_parquet_str = transactions_parquet_path.as_posix()
    art_parquet_str = articles_parquet_path.as_posix()

    total_articles = con.execute(
        f"SELECT COUNT(*) FROM read_parquet('{art_parquet_str}')"
    ).fetchone()[0]

    print(f" -> Total Articles in Catalog: {total_articles:,}")

    # Step 2: Compute Product Aggregation, Velocity, & Seasonality
    print("\n[Step 2] Calculating Product Aggregations, 30-Day Velocity & Seasonality...")

    query = f"""
    CREATE OR REPLACE TABLE product_features AS
    WITH min_dates AS (
        SELECT 
            article_id,
            MIN(t_dat) AS min_t_dat,
            MAX(t_dat) AS max_t_dat
        FROM read_parquet('{tx_parquet_str}')
        GROUP BY article_id
    ),
    tx_with_min AS (
        SELECT 
            t.article_id,
            t.customer_id,
            t.t_dat,
            t.price,
            m.min_t_dat,
            m.max_t_dat,
            EXTRACT(MONTH FROM t.t_dat) AS sale_month
        FROM read_parquet('{tx_parquet_str}') t
        JOIN min_dates m ON t.article_id = m.article_id
    ),
    tx_agg AS (
        SELECT 
            article_id,
            MIN(min_t_dat) AS first_sale_date,
            MAX(max_t_dat) AS last_sale_date,
            CAST(DATEDIFF('day', MIN(min_t_dat), MAX(max_t_dat)) AS INTEGER) AS selling_lifecycle_days,
            CAST(SUM(price) AS DOUBLE) AS total_revenue,
            CAST(COUNT(*) AS INTEGER) AS total_sales_count,
            CAST(COUNT(DISTINCT customer_id) AS INTEGER) AS unique_customers,
            CAST(AVG(price) AS DOUBLE) AS avg_price,
            CAST(SUM(CASE WHEN DATEDIFF('day', min_t_dat, t_dat) < 30 THEN 1 ELSE 0 END) AS INTEGER) AS sales_velocity_30d,
            CAST(SUM(CASE WHEN sale_month IN (3, 4, 5) THEN 1 ELSE 0 END) AS INTEGER) AS spring_sales_count,
            CAST(SUM(CASE WHEN sale_month IN (6, 7, 8) THEN 1 ELSE 0 END) AS INTEGER) AS summer_sales_count,
            CAST(SUM(CASE WHEN sale_month IN (9, 10, 11) THEN 1 ELSE 0 END) AS INTEGER) AS autumn_sales_count,
            CAST(SUM(CASE WHEN sale_month IN (12, 1, 2) THEN 1 ELSE 0 END) AS INTEGER) AS winter_sales_count,
            CAST(SUM(CASE WHEN sale_month IN (3, 4, 5) THEN price ELSE 0 END) AS DOUBLE) AS spring_revenue,
            CAST(SUM(CASE WHEN sale_month IN (6, 7, 8) THEN price ELSE 0 END) AS DOUBLE) AS summer_revenue,
            CAST(SUM(CASE WHEN sale_month IN (9, 10, 11) THEN price ELSE 0 END) AS DOUBLE) AS autumn_revenue,
            CAST(SUM(CASE WHEN sale_month IN (12, 1, 2) THEN price ELSE 0 END) AS DOUBLE) AS winter_revenue
        FROM tx_with_min
        GROUP BY article_id
    )
    SELECT 
        a.article_id,
        a.product_code,
        a.prod_name,
        a.product_type_no,
        a.product_type_name,
        a.product_group_name,
        a.graphical_appearance_no,
        a.graphical_appearance_name,
        a.colour_group_code,
        a.colour_group_name,
        a.perceived_colour_value_id,
        a.perceived_colour_value_name,
        a.perceived_colour_master_id,
        a.perceived_colour_master_name,
        a.department_no,
        a.department_name,
        a.index_code,
        a.index_name,
        a.index_group_no,
        a.index_group_name,
        a.section_no,
        a.section_name,
        a.garment_group_no,
        a.garment_group_name,
        a.detail_desc,
        (t.article_id IS NOT NULL) AS has_transactions,
        t.first_sale_date,
        t.last_sale_date,
        COALESCE(t.selling_lifecycle_days, 0) AS selling_lifecycle_days,
        COALESCE(t.total_revenue, 0.0) AS total_revenue,
        COALESCE(t.total_sales_count, 0) AS total_sales_count,
        COALESCE(t.unique_customers, 0) AS unique_customers,
        COALESCE(t.avg_price, 0.0) AS avg_price,
        COALESCE(t.sales_velocity_30d, 0) AS sales_velocity_30d,
        COALESCE(t.spring_sales_count, 0) AS spring_sales_count,
        COALESCE(t.summer_sales_count, 0) AS summer_sales_count,
        COALESCE(t.autumn_sales_count, 0) AS autumn_sales_count,
        COALESCE(t.winter_sales_count, 0) AS winter_sales_count,
        COALESCE(t.spring_revenue, 0.0) AS spring_revenue,
        COALESCE(t.summer_revenue, 0.0) AS summer_revenue,
        COALESCE(t.autumn_revenue, 0.0) AS autumn_revenue,
        COALESCE(t.winter_revenue, 0.0) AS winter_revenue,
        CASE 
            WHEN COALESCE(t.spring_sales_count, 0) >= GREATEST(COALESCE(t.summer_sales_count, 0), COALESCE(t.autumn_sales_count, 0), COALESCE(t.winter_sales_count, 0)) AND COALESCE(t.spring_sales_count, 0) > 0 THEN 'Spring'
            WHEN COALESCE(t.summer_sales_count, 0) >= GREATEST(COALESCE(t.spring_sales_count, 0), COALESCE(t.autumn_sales_count, 0), COALESCE(t.winter_sales_count, 0)) AND COALESCE(t.summer_sales_count, 0) > 0 THEN 'Summer'
            WHEN COALESCE(t.autumn_sales_count, 0) >= GREATEST(COALESCE(t.spring_sales_count, 0), COALESCE(t.summer_sales_count, 0), COALESCE(t.winter_sales_count, 0)) AND COALESCE(t.autumn_sales_count, 0) > 0 THEN 'Autumn'
            WHEN COALESCE(t.winter_sales_count, 0) >= GREATEST(COALESCE(t.spring_sales_count, 0), COALESCE(t.summer_sales_count, 0), COALESCE(t.autumn_sales_count, 0)) AND COALESCE(t.winter_sales_count, 0) > 0 THEN 'Winter'
            ELSE 'None'
        END AS peak_season
    FROM read_parquet('{art_parquet_str}') a
    LEFT JOIN tx_agg t ON a.article_id = t.article_id
    """
    con.execute(query)

    # Step 3: Run Data Integrity & Validation Checks
    print("\n[Step 3] Running Automated Data Integrity Checks...")

    output_count = con.execute("SELECT COUNT(*) FROM product_features").fetchone()[0]
    print(f" -> Output total product count: {output_count:,}")
    assert output_count == total_articles, f"Row count mismatch! Expected {total_articles}, got {output_count}"

    transacting_articles = con.execute("SELECT COUNT(*) FROM product_features WHERE has_transactions = TRUE").fetchone()[0]
    print(f" -> Transacting articles count: {transacting_articles:,}")

    null_article_ids = con.execute("SELECT COUNT(*) FROM product_features WHERE article_id IS NULL").fetchone()[0]
    assert null_article_ids == 0, "Found NULL article_id in product_features!"

    negative_values = con.execute(
        "SELECT COUNT(*) FROM product_features WHERE total_revenue < 0 OR total_sales_count < 0 OR sales_velocity_30d < 0"
    ).fetchone()[0]
    assert negative_values == 0, "Found negative values in metrics!"

    print(" -> Data Validation Passed: 100% complete, no orphan IDs, no negative metrics.")

    # Step 4: Console Summary Printouts
    print("\n" + "=" * 70)
    print("TOP 10 PRODUCTS BY TOTAL REVENUE")
    print("=" * 70)
    top_revenue_df = con.execute("""
        SELECT 
            article_id,
            prod_name,
            product_group_name,
            ROUND(total_revenue, 4) AS total_revenue,
            total_sales_count,
            unique_customers,
            sales_velocity_30d,
            peak_season
        FROM product_features
        ORDER BY total_revenue DESC
        LIMIT 10
    """).df()
    print(top_revenue_df.to_string(index=False))

    print("\n" + "=" * 70)
    print("TOP 10 PRODUCTS BY SALES VELOCITY (FIRST 30 DAYS)")
    print("=" * 70)
    top_velocity_df = con.execute("""
        SELECT 
            article_id,
            prod_name,
            product_group_name,
            sales_velocity_30d,
            total_sales_count,
            ROUND(total_revenue, 4) AS total_revenue,
            first_sale_date,
            peak_season
        FROM product_features
        ORDER BY sales_velocity_30d DESC
        LIMIT 10
    """).df()
    print(top_velocity_df.to_string(index=False))
    print("=" * 70)

    # Step 5: Export to Parquet Format
    print(f"\n[Step 4] Exporting results to Parquet format...")
    output_parquet_path.parent.mkdir(parents=True, exist_ok=True)
    con.execute(f"COPY product_features TO '{output_parquet_path.as_posix()}' (FORMAT PARQUET, COMPRESSION ZSTD)")

    file_size_mb = output_parquet_path.stat().st_size / (1024 * 1024)
    elapsed = time.time() - start_time
    print(f" -> Output File: {output_parquet_path}")
    print(f" -> File Size: {file_size_mb:.2f} MB")
    print(f" -> Execution Time: {elapsed:.2f} seconds")
    print("\nFeature Engineering Phase 3 Part 2 Completed Successfully!")


if __name__ == "__main__":
    project_root = Path(__file__).resolve().parents[2]

    transactions_path = project_root / "data" / "processed" / "cleaned_transactions.parquet"
    articles_path = project_root / "data" / "processed" / "cleaned_articles.parquet"
    output_path = project_root / "data" / "marts" / "product_features.parquet"

    build_product_features(
        transactions_parquet_path=transactions_path,
        articles_parquet_path=articles_path,
        output_parquet_path=output_path
    )
