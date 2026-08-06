import os
import duckdb
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def main():
    print("Starting EDA...")
    os.makedirs('reports/figures', exist_ok=True)
    
    # 1. Load data using duckdb
    print("Loading data...")
    con = duckdb.connect()
    
    # We use DuckDB to load data efficiently into Pandas for Seaborn/Matplotlib
    customers_df = con.query("SELECT * FROM 'data/marts/customer_features.parquet'").df()
    transactions_df = con.query("SELECT * FROM 'data/processed/cleaned_transactions.parquet'").df()
    
    # 2. Univariate Visualization
    print("Generating Univariate Visualizations...")
    
    # Age distribution
    plt.figure(figsize=(10, 6))
    sns.histplot(customers_df['age'].dropna(), bins=30, kde=True, color='skyblue')
    plt.title('Distribution of Customer Age')
    plt.xlabel('Age')
    plt.ylabel('Count')
    plt.savefig('reports/figures/age_distribution.png', bbox_inches='tight')
    plt.close()
    
    print(f"Age Stats: Min={customers_df['age'].min()}, Max={customers_df['age'].max()}, Mean={customers_df['age'].mean()}")
    
    # Price distribution
    # Filter out extreme outliers for better visualization, like top 1%
    price_99th = transactions_df['price'].quantile(0.99)
    plt.figure(figsize=(10, 6))
    sns.histplot(transactions_df[transactions_df['price'] <= price_99th]['price'], bins=50, kde=True, color='salmon')
    plt.title('Distribution of Transaction Price (99th percentile)')
    plt.xlabel('Price')
    plt.ylabel('Count')
    plt.savefig('reports/figures/price_distribution.png', bbox_inches='tight')
    plt.close()
    
    print(f"Price Stats: Min={transactions_df['price'].min()}, Max={transactions_df['price'].max()}, Mean={transactions_df['price'].mean()}")
    
    # 3. Bivariate & Temporal Visualization
    print("Generating Bivariate & Temporal Visualizations...")
    
    # Revenue trend over time (monthly)
    transactions_df['t_dat'] = pd.to_datetime(transactions_df['t_dat'])
    monthly_revenue = transactions_df.set_index('t_dat').resample('ME')['price'].sum().reset_index()
    
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=monthly_revenue, x='t_dat', y='price', marker='o', color='green')
    plt.title('Monthly Revenue Trend')
    plt.xlabel('Date')
    plt.ylabel('Total Revenue')
    plt.grid(True)
    plt.savefig('reports/figures/revenue_trend.png', bbox_inches='tight')
    plt.close()
    
    print(f"Revenue Trend: Peak month = {monthly_revenue.loc[monthly_revenue['price'].idxmax(), 't_dat']}, Peak Revenue = {monthly_revenue['price'].max()}")
    
    # Revenue comparison by sales_channel_id
    channel_revenue = transactions_df.groupby('sales_channel_id')['price'].sum().reset_index()
    channel_revenue['sales_channel_id'] = channel_revenue['sales_channel_id'].astype(str)
    
    plt.figure(figsize=(8, 6))
    sns.barplot(data=channel_revenue, x='sales_channel_id', y='price', hue='sales_channel_id', palette='Set2')
    plt.title('Total Revenue by Sales Channel')
    plt.xlabel('Sales Channel ID')
    plt.ylabel('Total Revenue')
    plt.savefig('reports/figures/sales_channel_comparison.png', bbox_inches='tight')
    plt.close()
    
    print(f"Sales Channel 1 Revenue: {channel_revenue[channel_revenue['sales_channel_id'] == '1']['price'].values[0] if '1' in channel_revenue['sales_channel_id'].values else 0}")
    print(f"Sales Channel 2 Revenue: {channel_revenue[channel_revenue['sales_channel_id'] == '2']['price'].values[0] if '2' in channel_revenue['sales_channel_id'].values else 0}")
    
    # 4. Multivariate & Correlation
    print("Generating Multivariate & Correlation Visualizations...")
    
    # Heatmap of correlation matrix for numeric customer features
    cols = ['recency', 'frequency', 'monetary', 'tenure', 'age', 'category_diversity']
    # Check which columns exist in the DataFrame
    available_cols = [c for c in cols if c in customers_df.columns]
    
    corr_matrix = customers_df[available_cols].corr()
    
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1, center=0, fmt='.2f', square=True)
    plt.title('Correlation Heatmap of Customer Features')
    plt.savefig('reports/figures/correlation_heatmap.png', bbox_inches='tight')
    plt.close()
    
    print("Correlation matrix created.")
    print("EDA completed successfully. Figures saved to reports/figures/")

if __name__ == '__main__':
    main()
