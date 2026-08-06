import nbformat as nbf

def create_segmentation_notebook():
    nb = nbf.v4.new_notebook()
    
    # Cell 1: Markdown Header
    header_md = """# ML #1: Customer Segmentation
## Objective: 
Using K-Means Clustering on RFM features to segment customers and identify potential churn risks."""
    
    # Cell 2: Imports
    imports_code = """# Ensure required libraries are installed (especially parquet engines)
try:
    import fastparquet
except ImportError:
    !pip install fastparquet -q
try:
    import duckdb
except ImportError:
    !pip install duckdb -q

# Import necessary libraries
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
import warnings
warnings.filterwarnings('ignore')"""
    
    # Cell 3: Load Data
    load_code = """# Resolve file path gracefully whether running from root or notebooks/ dir
if os.path.exists('data/marts/customer_features.parquet'):
    customer_features_path = 'data/marts/customer_features.parquet'
elif os.path.exists('../data/marts/customer_features.parquet'):
    customer_features_path = '../data/marts/customer_features.parquet'
else:
    raise FileNotFoundError("Could not find data/marts/customer_features.parquet")

# Load the customer data
try:
    df = pd.read_parquet(customer_features_path)
    print(f"Data loaded successfully with pandas. Shape: {df.shape}")
except Exception as e:
    print(f"Pandas read_parquet failed ({e}), falling back to DuckDB...")
    import duckdb
    df = duckdb.query(f"SELECT * FROM '{customer_features_path}'").df()
    print(f"Data loaded via DuckDB. Shape: {df.shape}")

df.head()"""
    
    # Cell 4: Preprocess
    preprocess_code = """# Preprocess the data: Select RFM columns
rfm_cols = ['recency', 'frequency', 'monetary']
rfm_df = df[rfm_cols].copy()

# Handle missing values
print(f"Missing values before:\\n{rfm_df.isnull().sum()}")
rfm_df = rfm_df.dropna()
print(f"Shape after dropping NA: {rfm_df.shape}")

# Handle extreme outliers (e.g., top 1% monetary and frequency)
for col in ['frequency', 'monetary']:
    upper_limit = rfm_df[col].quantile(0.99)
    rfm_df = rfm_df[rfm_df[col] <= upper_limit]

print(f"Shape after removing top 1% outliers: {rfm_df.shape}")

# For clustering, we might want to log transform recency, frequency, monetary if they are heavily skewed
# But we'll just use StandardScaler as requested.
scaler = StandardScaler()
rfm_scaled = scaler.fit_transform(rfm_df)
rfm_scaled_df = pd.DataFrame(rfm_scaled, columns=rfm_cols, index=rfm_df.index)

rfm_scaled_df.describe()"""
    
    # Cell 5: Optimal K
    optimal_k_code = """# Determine the optimal number of clusters (k) using Elbow Method and Silhouette Score
# For performance reasons on large datasets, we'll sample the data if it's too large for silhouette
sample_size = min(20000, rfm_scaled_df.shape[0])
sample_scaled = rfm_scaled_df.sample(n=sample_size, random_state=42)

sse = []
silhouette_scores = []
k_range = range(2, 9)

print("Calculating SSE and Silhouette Scores...")
for k in k_range:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(sample_scaled)
    sse.append(kmeans.inertia_)
    score = silhouette_score(sample_scaled, kmeans.labels_)
    silhouette_scores.append(score)
    print(f"k={k}, SSE={kmeans.inertia_:.2f}, Silhouette={score:.4f}")"""
    
    # Cell 6: Plot K
    plot_k_code = """# Plot Elbow and Silhouette
fig, ax1 = plt.subplots(figsize=(10, 5))

color = 'tab:blue'
ax1.set_xlabel('Number of clusters (k)')
ax1.set_ylabel('Sum of Squared Errors (SSE)', color=color)
ax1.plot(k_range, sse, marker='o', color=color)
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()
color = 'tab:red'
ax2.set_ylabel('Silhouette Score', color=color)
ax2.plot(k_range, silhouette_scores, marker='s', color=color)
ax2.tick_params(axis='y', labelcolor=color)

plt.title('Elbow Method and Silhouette Score for Optimal k')
fig.tight_layout()
plt.show()"""
    
    # Cell 7: Apply K-Means
    apply_kmeans_code = """# Based on the plots and common RFM segmentation
optimal_k = 5  # Set to 5 as likely optimal

print(f"Applying K-Means with k={optimal_k} to full dataset...")
kmeans = KMeans(n_clusters=optimal_k, random_state=42, n_init=10)
kmeans.fit(rfm_scaled_df)

# Assign cluster labels back
rfm_df['cluster'] = kmeans.labels_

# Add back to the main DataFrame for the remaining rows
df_clustered = df.loc[rfm_df.index].copy()
df_clustered['cluster'] = kmeans.labels_

# Summary table showing average R, F, M for each cluster
cluster_summary = rfm_df.groupby('cluster').agg({
    'recency': ['mean', 'median'],
    'frequency': ['mean', 'median'],
    'monetary': ['mean', 'median', 'count']
}).round(2)

cluster_summary"""
    
    # Cell 8: Business Interpretation Markdown
    interpretation_md = """## Business Interpretation
- Analyze the `cluster_summary` above to label each cluster (e.g., Champions, Loyal Customers, At Risk, Hibernating, New Customers).
- The clusters with high recency and low frequency/monetary are potential churn risks.
- The clusters with low recency, high frequency and monetary are our Champions."""

    nb['cells'] = [
        nbf.v4.new_markdown_cell(header_md),
        nbf.v4.new_code_cell(imports_code),
        nbf.v4.new_code_cell(load_code),
        nbf.v4.new_code_cell(preprocess_code),
        nbf.v4.new_code_cell(optimal_k_code),
        nbf.v4.new_code_cell(plot_k_code),
        nbf.v4.new_code_cell(apply_kmeans_code),
        nbf.v4.new_markdown_cell(interpretation_md)
    ]
    
    with open('notebooks/02_ml_1_segmentation.ipynb', 'w', encoding='utf-8') as f:
        nbf.write(nb, f)
        print("Successfully created and updated notebooks/02_ml_1_segmentation.ipynb")

if __name__ == '__main__':
    create_segmentation_notebook()
