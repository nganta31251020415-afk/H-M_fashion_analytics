"""
Data Cleaning and Validation Script for H&M Transactions Table

This script processes raw transactions data from data/raw/transactions_train.csv
using DuckDB for memory-efficient and high-performance processing of ~31.8 million records.
It formats data types, validates foreign key constraints against cleaned customers and articles,
verifies price integrity, and exports the clean dataset to Parquet format.

Output:
    - data/processed/cleaned_transactions.parquet
"""

from pathlib import Path
import duckdb


def clean_transactions_data(
    raw_csv_path: Path,
    customers_parquet_path: Path,
    articles_parquet_path: Path,
    output_parquet_path: Path
) -> None:
    """
    Cleans raw transactions CSV data using DuckDB, validates integrity, and exports to Parquet.

    Args:
        raw_csv_path (Path): Path to input raw transactions_train.csv file.
        customers_parquet_path (Path): Path to cleaned_customers.parquet for FK validation.
        articles_parquet_path (Path): Path to cleaned_articles.parquet for FK validation.
        output_parquet_path (Path): Path to output clean Parquet file.
    """
    print("=" * 60)
    print("Starting Transactions Table Cleaning & Validation Pipeline")
    print("=" * 60)

    # Initialize DuckDB connection
    con = duckdb.connect()

    # Step 1: Load raw data & inspect schema
    print(f"\n[Step 1] Reading raw data from: {raw_csv_path}")
    raw_count = con.execute(
        f"SELECT COUNT(*) FROM read_csv_auto('{raw_csv_path.as_posix()}', all_varchar=True)"
    ).fetchone()[0]
    print(f"-> Raw total rows: {raw_count:,}")

    # Ensure output directory exists
    output_parquet_path.parent.mkdir(parents=True, exist_ok=True)

    # Step 2: Create Cleaned Transactions Table
    # - Formats t_dat to DATE
    # - Formats customer_id with TRIM
    # - Formats article_id with LPAD to 10-digit string
    # - Casts price to DOUBLE
    # - Casts sales_channel_id to TINYINT
    print("\n[Step 2] Applying data type standardization & key formatting...")
    clean_query = f"""
    CREATE OR REPLACE TABLE cleaned_transactions AS
    SELECT 
        CAST(t_dat AS DATE) AS t_dat,
        TRIM(customer_id) AS customer_id,
        LPAD(TRIM(article_id), 10, '0') AS article_id,
        CAST(price AS DOUBLE) AS price,
        CAST(sales_channel_id AS TINYINT) AS sales_channel_id
    FROM read_csv_auto('{raw_csv_path.as_posix()}', all_varchar=True)
    """
    con.execute(clean_query)

    # Step 3: Data Validation Checks
    print("\n[Step 3] Running Automated Data Validation Checks...")

    # Check 1: Row count preservation (31,788,324 rows)
    clean_count = con.execute("SELECT COUNT(*) FROM cleaned_transactions").fetchone()[0]
    print(f"-> Clean total rows: {clean_count:,}")
    assert clean_count == raw_count, f"Row count mismatch! Raw: {raw_count}, Clean: {clean_count}"

    # Check 2: Null count verification across all 5 columns
    total_nulls = sum([
        con.execute(f"SELECT COUNT(*) FROM cleaned_transactions WHERE {col} IS NULL").fetchone()[0]
        for col in ["t_dat", "customer_id", "article_id", "price", "sales_channel_id"]
    ])
    print(f"-> Total NULL values across all 5 columns: {total_nulls}")
    assert total_nulls == 0, "Found unexpected NULL values in transactions!"

    # Check 3: Date range check (2018-09-20 to 2020-09-22)
    min_date, max_date = con.execute("SELECT MIN(t_dat), MAX(t_dat) FROM cleaned_transactions").fetchone()
    print(f"-> Transaction Date Range: {min_date} to {max_date}")
    assert str(min_date) == "2018-09-20", f"Unexpected min date: {min_date}"
    assert str(max_date) == "2020-09-22", f"Unexpected max date: {max_date}"

    # Check 4: Price integrity check (price > 0)
    invalid_price_count = con.execute("SELECT COUNT(*) FROM cleaned_transactions WHERE price <= 0").fetchone()[0]
    min_price, avg_price, max_price = con.execute("SELECT MIN(price), AVG(price), MAX(price) FROM cleaned_transactions").fetchone()
    print(f"-> Price range: Min={min_price:.6f}, Avg={avg_price:.6f}, Max={max_price:.6f}")
    print(f"-> Invalid (<= 0) price count: {invalid_price_count}")
    assert invalid_price_count == 0, f"Found {invalid_price_count} transactions with price <= 0!"

    # Check 5: Referential Integrity Check - Customer ID
    print("\n[Step 4] Checking Referential Integrity (Foreign Keys)...")
    orphan_cust_count = con.execute(f"""
        SELECT COUNT(DISTINCT t.customer_id)
        FROM cleaned_transactions t
        LEFT JOIN '{customers_parquet_path.as_posix()}' c ON t.customer_id = c.customer_id
        WHERE c.customer_id IS NULL
    """).fetchone()[0]
    print(f"-> Orphan customer_id count (not in customers dimension): {orphan_cust_count}")
    assert orphan_cust_count == 0, f"Found {orphan_cust_count} orphan customer_ids in transactions!"

    # Check 6: Referential Integrity Check - Article ID
    orphan_art_count = con.execute(f"""
        SELECT COUNT(DISTINCT t.article_id)
        FROM cleaned_transactions t
        LEFT JOIN '{articles_parquet_path.as_posix()}' a ON t.article_id = a.article_id
        WHERE a.article_id IS NULL
    """).fetchone()[0]
    print(f"-> Orphan article_id count (not in articles dimension): {orphan_art_count}")
    assert orphan_art_count == 0, f"Found {orphan_art_count} orphan article_ids in transactions!"

    # Step 5: Export to Parquet
    print(f"\n[Step 5] Exporting clean dataset to Parquet: {output_parquet_path}")
    con.execute(f"COPY cleaned_transactions TO '{output_parquet_path.as_posix()}' (FORMAT PARQUET, COMPRESSION SNAPPY)")

    parquet_size_mb = output_parquet_path.stat().st_size / (1024 * 1024)
    print(f"-> Successfully exported Parquet file! Size: {parquet_size_mb:.2f} MB")
    print("=" * 60)
    print("Transactions Data Cleaning Pipeline Completed Successfully!")
    print("=" * 60)


if __name__ == "__main__":
    project_root = Path(__file__).resolve().parents[2]
    raw_path = project_root / "data" / "raw" / "transactions_train.csv"
    cust_parquet = project_root / "data" / "processed" / "cleaned_customers.parquet"
    art_parquet = project_root / "data" / "processed" / "cleaned_articles.parquet"
    output_path = project_root / "data" / "processed" / "cleaned_transactions.parquet"

    clean_transactions_data(raw_path, cust_parquet, art_parquet, output_path)
