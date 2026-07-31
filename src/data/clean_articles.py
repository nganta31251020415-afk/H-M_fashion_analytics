"""
Data Cleaning and Validation Script for H&M Articles Table

This script processes raw product metadata from data/raw/articles.csv,
applies string standardization, handles missing values in product descriptions,
validates data integrity constraints, and exports the clean dataset to Parquet format.

Output:
    - data/processed/cleaned_articles.parquet
"""

from pathlib import Path
import duckdb


def clean_articles_data(raw_csv_path: Path, output_parquet_path: Path) -> None:
    """
    Cleans raw articles CSV data using DuckDB and exports to Parquet.
    
    Args:
        raw_csv_path (Path): Path to the input raw articles.csv file.
        output_parquet_path (Path): Path to the output clean Parquet file.
    """
    print("=" * 60)
    print("Starting Articles Table Cleaning & Validation Pipeline")
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

    # Step 2 & Step 3: Transformation Query
    # - Formats article_id to 10-digit string with leading zeros
    # - Formats product_code to 7-digit string with leading zeros
    # - Applies TRIM to string columns
    # - Imputes NULLs in detail_desc with 'No description available'
    print("\n[Step 2 & 3] Applying transformations & handling missing values...")
    clean_query = f"""
    CREATE OR REPLACE TABLE cleaned_articles AS
    SELECT 
        LPAD(TRIM(article_id), 10, '0') AS article_id,
        LPAD(TRIM(product_code), 7, '0') AS product_code,
        TRIM(prod_name) AS prod_name,
        CAST(product_type_no AS BIGINT) AS product_type_no,
        TRIM(product_type_name) AS product_type_name,
        TRIM(product_group_name) AS product_group_name,
        CAST(graphical_appearance_no AS BIGINT) AS graphical_appearance_no,
        TRIM(graphical_appearance_name) AS graphical_appearance_name,
        TRIM(colour_group_code) AS colour_group_code,
        TRIM(colour_group_name) AS colour_group_name,
        CAST(perceived_colour_value_id AS BIGINT) AS perceived_colour_value_id,
        TRIM(perceived_colour_value_name) AS perceived_colour_value_name,
        CAST(perceived_colour_master_id AS BIGINT) AS perceived_colour_master_id,
        TRIM(perceived_colour_master_name) AS perceived_colour_master_name,
        CAST(department_no AS BIGINT) AS department_no,
        TRIM(department_name) AS department_name,
        TRIM(index_code) AS index_code,
        TRIM(index_name) AS index_name,
        CAST(index_group_no AS BIGINT) AS index_group_no,
        TRIM(index_group_name) AS index_group_name,
        CAST(section_no AS BIGINT) AS section_no,
        TRIM(section_name) AS section_name,
        CAST(garment_group_no AS BIGINT) AS garment_group_no,
        TRIM(garment_group_name) AS garment_group_name,
        COALESCE(TRIM(detail_desc), 'No description available') AS detail_desc
    FROM read_csv_auto('{raw_csv_path.as_posix()}', all_varchar=True)
    """
    con.execute(clean_query)

    # Step 4: Data Validation Checks
    print("\n[Step 4] Running Automated Data Validation Checks...")
    
    # Check 1: Row count check
    clean_count = con.execute("SELECT COUNT(*) FROM cleaned_articles").fetchone()[0]
    print(f"-> Clean total rows: {clean_count:,}")
    assert clean_count == raw_count, f"Row count mismatch! Raw: {raw_count}, Clean: {clean_count}"

    # Check 2: Primary Key uniqueness
    distinct_articles = con.execute("SELECT COUNT(DISTINCT article_id) FROM cleaned_articles").fetchone()[0]
    print(f"-> Distinct article_id count: {distinct_articles:,}")
    assert distinct_articles == clean_count, "Primary Key (article_id) contains duplicates!"

    # Check 3: Zero padded article_id length check
    invalid_length_count = con.execute("SELECT COUNT(*) FROM cleaned_articles WHERE LENGTH(article_id) != 10").fetchone()[0]
    print(f"-> Articles with invalid article_id length (!= 10): {invalid_length_count}")
    assert invalid_length_count == 0, "Found article_id entries with length != 10!"

    # Check 4: Null count verification in detail_desc
    null_desc_count = con.execute("SELECT COUNT(*) FROM cleaned_articles WHERE detail_desc IS NULL").fetchone()[0]
    print(f"-> Remaining NULLs in detail_desc: {null_desc_count}")
    assert null_desc_count == 0, "Found unexpected NULLs in detail_desc after imputation!"

    # Check 5: Total NULL count across all columns
    total_nulls = sum([
        con.execute(f"SELECT COUNT(*) FROM cleaned_articles WHERE {col} IS NULL").fetchone()[0]
        for col in [
            "article_id", "product_code", "prod_name", "product_type_no", "product_type_name",
            "product_group_name", "graphical_appearance_no", "graphical_appearance_name",
            "colour_group_code", "colour_group_name", "perceived_colour_value_id",
            "perceived_colour_value_name", "perceived_colour_master_id",
            "perceived_colour_master_name", "department_no", "department_name", "index_code",
            "index_name", "index_group_no", "index_group_name", "section_no", "section_name",
            "garment_group_no", "garment_group_name", "detail_desc"
        ]
    ])
    print(f"-> Total NULL values across all 25 columns: {total_nulls}")
    assert total_nulls == 0, "Found remaining NULL values in clean dataset!"

    # Step 5: Export to Parquet
    print(f"\n[Step 5] Exporting clean dataset to Parquet: {output_parquet_path}")
    con.execute(f"COPY cleaned_articles TO '{output_parquet_path.as_posix()}' (FORMAT PARQUET, COMPRESSION SNAPPY)")
    
    parquet_size_mb = output_parquet_path.stat().st_size / (1024 * 1024)
    print(f"-> Successfully exported Parquet file! Size: {parquet_size_mb:.2f} MB")
    print("=" * 60)
    print("Articles Data Cleaning Pipeline Completed Successfully!")
    print("=" * 60)


if __name__ == "__main__":
    project_root = Path(__file__).resolve().parents[2]
    raw_path = project_root / "data" / "raw" / "articles.csv"
    output_path = project_root / "data" / "processed" / "cleaned_articles.parquet"

    clean_articles_data(raw_path, output_path)
