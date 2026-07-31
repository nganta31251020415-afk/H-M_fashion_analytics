"""
Data Cleaning and Validation Script for H&M Customers Table

This script processes raw customer demographics from data/raw/customers.csv,
applies binary flag conversion (FN, Active), imputes categorical status values,
applies distribution-based random sampling imputation for missing age values,
validates data integrity constraints, and exports the clean dataset to Parquet format.

Output:
    - data/processed/cleaned_customers.parquet
"""

from pathlib import Path
import duckdb
import numpy as np
import pandas as pd


def clean_customers_data(raw_csv_path: Path, output_parquet_path: Path) -> None:
    """
    Cleans raw customers CSV data using DuckDB & NumPy, then exports to Parquet.
    
    Args:
        raw_csv_path (Path): Path to input raw customers.csv file.
        output_parquet_path (Path): Path to output clean Parquet file.
    """
    print("=" * 60)
    print("Starting Customers Table Cleaning & Validation Pipeline")
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

    # Step 2: Binary flags, categorical normalization, and initial string cleanup
    print("\n[Step 2] Applying binary flag conversion and categorical normalization...")
    df = con.execute(f"""
        SELECT 
            TRIM(customer_id) AS customer_id,
            COALESCE(CAST(FN AS TINYINT), 0) AS FN,
            COALESCE(CAST(Active AS TINYINT), 0) AS Active,
            COALESCE(NULLIF(UPPER(TRIM(club_member_status)), ''), 'NONE') AS club_member_status,
            CASE 
                WHEN fashion_news_frequency IS NULL OR UPPER(TRIM(fashion_news_frequency)) IN ('NONE', '') THEN 'NONE'
                WHEN UPPER(TRIM(fashion_news_frequency)) = 'REGULARLY' THEN 'Regularly'
                WHEN UPPER(TRIM(fashion_news_frequency)) = 'MONTHLY' THEN 'Monthly'
                ELSE TRIM(fashion_news_frequency)
            END AS fashion_news_frequency,
            CAST(age AS DOUBLE) AS age,
            TRIM(postal_code) AS postal_code
        FROM read_csv_auto('{raw_csv_path.as_posix()}', all_varchar=True)
    """).df()

    # Calculate pre-imputation age stats for verification
    age_pre_stats = df['age'].agg(['count', 'mean', 'std', 'min', 'max'])
    age_pre_p25 = df['age'].quantile(0.25)
    age_pre_p50 = df['age'].quantile(0.50)
    age_pre_p75 = df['age'].quantile(0.75)

    print("\nPre-imputation Age Statistics:")
    print(f"  Count: {int(age_pre_stats['count']):,}, Mean: {age_pre_stats['mean']:.4f}, Std: {age_pre_stats['std']:.4f}")
    print(f"  Min: {age_pre_stats['min']}, P25: {age_pre_p25}, Median: {age_pre_p50}, P75: {age_pre_p75}, Max: {age_pre_stats['max']}")

    # Step 3: Distribution-based Random Sampling Imputation for 'age'
    print("\n[Step 3] Performing Distribution-based Random Sampling Imputation for missing ages...")
    np.random.seed(42)  # Fixed random seed for 100% reproducibility
    non_null_ages = df['age'].dropna().values
    null_age_mask = df['age'].isna()
    null_age_count = null_age_mask.sum()

    print(f"-> Missing age count to impute: {null_age_count:,} ({null_age_count / raw_count * 100:.4f}%)")

    # Draw random samples directly from empirical non-null age distribution
    sampled_ages = np.random.choice(non_null_ages, size=null_age_count, replace=True)
    df.loc[null_age_mask, 'age'] = sampled_ages

    # Convert age column to integer
    df['age'] = df['age'].astype('int64')

    # Calculate post-imputation age stats
    age_post_stats = df['age'].agg(['count', 'mean', 'std', 'min', 'max'])
    age_post_p25 = df['age'].quantile(0.25)
    age_post_p50 = df['age'].quantile(0.50)
    age_post_p75 = df['age'].quantile(0.75)

    print("\nPost-imputation Age Statistics:")
    print(f"  Count: {int(age_post_stats['count']):,}, Mean: {age_post_stats['mean']:.4f}, Std: {age_post_stats['std']:.4f}")
    print(f"  Min: {age_post_stats['min']}, P25: {age_post_p25}, Median: {age_post_p50}, P75: {age_post_p75}, Max: {age_post_stats['max']}")

    # Step 4: Data Validation Checks
    print("\n[Step 4] Running Automated Data Validation Checks...")

    # Check 1: Row count preservation
    clean_count = len(df)
    print(f"-> Clean total rows: {clean_count:,}")
    assert clean_count == raw_count, f"Row count mismatch! Raw: {raw_count}, Clean: {clean_count}"

    # Check 2: Primary Key uniqueness
    distinct_customers = df['customer_id'].nunique()
    print(f"-> Distinct customer_id count: {distinct_customers:,}")
    assert distinct_customers == clean_count, "Primary Key (customer_id) contains duplicates!"

    # Check 3: Customer ID string length check (64 hex characters)
    invalid_cust_id_len = (df['customer_id'].str.len() != 64).sum()
    print(f"-> Customer IDs with length != 64: {invalid_cust_id_len}")
    assert invalid_cust_id_len == 0, "Found customer_id entries with length != 64!"

    # Check 4: Zero NULL values across all 7 columns
    null_counts = df.isna().sum()
    total_nulls = null_counts.sum()
    print(f"-> Total NULL values across all 7 columns: {total_nulls}")
    assert total_nulls == 0, f"Found remaining NULL values in clean dataset:\n{null_counts}"

    # Check 5: Age mean & std deviation shift check (< 0.05 difference)
    mean_diff = abs(age_pre_stats['mean'] - age_post_stats['mean'])
    std_diff = abs(age_pre_stats['std'] - age_post_stats['std'])
    print(f"-> Age distribution mean shift: {mean_diff:.6f}, std shift: {std_diff:.6f}")
    assert mean_diff < 0.05, f"Age mean shifted significantly after imputation: {mean_diff}"
    assert std_diff < 0.05, f"Age std shifted significantly after imputation: {std_diff}"

    # Step 5: Register DataFrame into DuckDB & Export to Parquet
    print(f"\n[Step 5] Exporting clean dataset to Parquet: {output_parquet_path}")
    con.register("cleaned_customers_df", df)
    con.execute(f"COPY cleaned_customers_df TO '{output_parquet_path.as_posix()}' (FORMAT PARQUET, COMPRESSION SNAPPY)")

    parquet_size_mb = output_parquet_path.stat().st_size / (1024 * 1024)
    print(f"-> Successfully exported Parquet file! Size: {parquet_size_mb:.2f} MB")
    print("=" * 60)
    print("Customers Data Cleaning Pipeline Completed Successfully!")
    print("=" * 60)


if __name__ == "__main__":
    project_root = Path(__file__).resolve().parents[2]
    raw_path = project_root / "data" / "raw" / "customers.csv"
    output_path = project_root / "data" / "processed" / "cleaned_customers.parquet"

    clean_customers_data(raw_path, output_path)
