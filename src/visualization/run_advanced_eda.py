import os
import duckdb
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def main():
    print("Starting Advanced EDA...")
    os.makedirs('reports/figures', exist_ok=True)
    
    con = duckdb.connect()
    
    print("Loading data...")
    # 1. Revenue by Age Group
    print("Generating Revenue by Age Group...")
    revenue_age_df = con.query("""
        SELECT 
            c.age,
            t.price
        FROM 'data/processed/cleaned_transactions.parquet' t
        JOIN 'data/processed/cleaned_customers.parquet' c ON t.customer_id = c.customer_id
    """).df()
    
    # Bin ages
    bins = [0, 20, 30, 40, 50, 100]
    labels = ['<20', '21-30', '31-40', '41-50', '>50']
    revenue_age_df['age_group'] = pd.cut(revenue_age_df['age'], bins=bins, labels=labels, right=False)
    
    # Aggregate revenue
    age_group_revenue = revenue_age_df.groupby('age_group')['price'].sum().reset_index()
    
    plt.figure(figsize=(10, 6))
    sns.barplot(data=age_group_revenue, x='age_group', y='price', palette='viridis')
    plt.title('Total Revenue by Age Group')
    plt.xlabel('Age Group')
    plt.ylabel('Total Revenue')
    plt.savefig('reports/figures/revenue_by_age.png', bbox_inches='tight')
    plt.close()
    print("Saved revenue_by_age.png")
    
    del revenue_age_df # Free memory
    
    # 2. Top 10 Product Categories by Revenue
    print("Generating Top 10 Product Categories by Revenue...")
    revenue_category_df = con.query("""
        SELECT 
            a.product_group_name,
            SUM(t.price) as total_revenue
        FROM 'data/processed/cleaned_transactions.parquet' t
        JOIN 'data/processed/cleaned_articles.parquet' a ON t.article_id = a.article_id
        GROUP BY a.product_group_name
        ORDER BY total_revenue DESC
        LIMIT 10
    """).df()
    
    plt.figure(figsize=(10, 8))
    sns.barplot(data=revenue_category_df, x='total_revenue', y='product_group_name', palette='magma')
    plt.title('Top 10 Product Categories by Revenue')
    plt.xlabel('Total Revenue')
    plt.ylabel('Product Group Name')
    plt.savefig('reports/figures/top_categories_revenue.png', bbox_inches='tight')
    plt.close()
    print("Saved top_categories_revenue.png")
    
    # 3. Revenue Trend by Sales Channel over Time
    print("Generating Revenue Trend by Sales Channel over Time...")
    channel_trend_df = con.query("""
        SELECT 
            t_dat,
            sales_channel_id,
            SUM(price) as daily_revenue
        FROM 'data/processed/cleaned_transactions.parquet'
        GROUP BY t_dat, sales_channel_id
    """).df()
    
    channel_trend_df['t_dat'] = pd.to_datetime(channel_trend_df['t_dat'])
    
    # We will resample by month or week for a cleaner plot. Let's do weekly to capture early 2020 well.
    weekly_trend = channel_trend_df.set_index('t_dat').groupby('sales_channel_id').resample('W')['daily_revenue'].sum().reset_index()
    weekly_trend['sales_channel_name'] = weekly_trend['sales_channel_id'].map({1: 'Offline (Store)', 2: 'Online'})
    
    plt.figure(figsize=(14, 7))
    sns.lineplot(data=weekly_trend, x='t_dat', y='daily_revenue', hue='sales_channel_name', palette=['#1f77b4', '#ff7f0e'])
    plt.title('Revenue Trend by Sales Channel over Time')
    plt.xlabel('Date')
    plt.ylabel('Weekly Revenue')
    # Highlight early 2020 COVID period
    plt.axvspan(pd.to_datetime('2020-02-01'), pd.to_datetime('2020-05-31'), color='red', alpha=0.1, label='COVID-19 Impact (Early 2020)')
    plt.legend()
    plt.grid(True)
    plt.savefig('reports/figures/channel_trend_over_time.png', bbox_inches='tight')
    plt.close()
    print("Saved channel_trend_over_time.png")
    
    print("Advanced EDA completed successfully.")

if __name__ == '__main__':
    main()
