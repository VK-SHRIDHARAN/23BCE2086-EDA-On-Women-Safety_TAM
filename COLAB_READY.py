"""
GOOGLE COLAB READY CODE
=======================

This code works in Google Colab without needing to upload files!
Data is loaded directly from GitHub.

Instructions for Google Colab:
1. Go to https://colab.research.google.com
2. Create a new notebook
3. In the first cell, run:

!pip install pandas numpy matplotlib seaborn scikit-learn

4. In the second cell, paste ALL of the code below and run it!

No file uploads needed - everything is automatic!

"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA
import warnings
warnings.filterwarnings('ignore')

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 8)
plt.rcParams['font.size'] = 10

# Load data from GitHub (no file uploads needed!)
github_url = "https://raw.githubusercontent.com/VK-SHRIDHARAN/23BCE2086-EDA-On-Women-Safety_TAM/main/"
df = pd.read_csv(github_url + 'CrimesOnWomenData.csv', index_col=0)
description = pd.read_csv(github_url + 'description.csv', index_col=0)

print("="*80)
print("EXPLORATORY DATA ANALYSIS: CRIMES AGAINST WOMEN IN INDIA")
print("="*80)
print(f"\nDataset Shape: {df.shape}")
print(f"Time Period: {df['Year'].min()}-{df['Year'].max()}")
print(f"Number of States/UTs: {df['State'].nunique()}")

# Crime columns
crime_columns = ['Rape', 'K&A', 'DD', 'AoW', 'AoM', 'DV', 'WT']
crime_labels = {
    'Rape': 'Rape Cases',
    'K&A': 'Kidnapping & Assault',
    'DD': 'Dowry Deaths',
    'AoW': 'Assault on Women',
    'AoM': 'Assault on Modesty',
    'DV': 'Domestic Violence',
    'WT': 'Women Trafficking'
}

# Data cleaning
df = df.fillna(0)

# ============================================================================
# TASK 1: IDENTIFY STATES WITH HIGHEST CRIME
# ============================================================================

print("\n" + "="*80)
print("TASK 1: STATES WITH HIGHEST CRIME AGAINST WOMEN")
print("="*80)

state_crime_totals = df.groupby('State')[crime_columns].sum().sum(axis=1).sort_values(ascending=False)

print("\n🔴 TOP 15 STATES (Total Cases):")
for rank, (state, count) in enumerate(state_crime_totals.head(15).items(), 1):
    bar = '█' * (count // 1000)
    print(f"{rank:2}. {state:25} {bar} {int(count):,}")

# Visualization
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

state_crime_totals.head(15).plot(kind='bar', ax=axes[0], color='crimson', alpha=0.8)
axes[0].set_title('Top 15 States with Highest Total Crimes Against Women', fontsize=14, fontweight='bold')
axes[0].set_ylabel('Total Crime Cases')
axes[0].tick_params(axis='x', rotation=45)
axes[0].grid(axis='y', alpha=0.3)

state_avg_crimes = df.groupby('State')[crime_columns].sum().sum(axis=1) / df.groupby('State').size()
state_avg_crimes.head(15).plot(kind='bar', ax=axes[1], color='darkred', alpha=0.8)
axes[1].set_title('Top 15 States with Highest Average Crimes per Year', fontsize=14, fontweight='bold')
axes[1].set_ylabel('Average Crime Cases per Year')
axes[1].tick_params(axis='x', rotation=45)
axes[1].grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.show()

# ============================================================================
# TASK 2: CLUSTERING ANALYSIS
# ============================================================================

print("\n" + "="*80)
print("TASK 2: CLUSTER STATES BASED ON CRIME DATA")
print("="*80)

state_aggregated = df.groupby('State')[crime_columns].sum()
scaler = StandardScaler()
state_scaled = scaler.fit_transform(state_aggregated)

# Find optimal clusters
inertias = []
silhouette_scores = []
K_range = range(2, 11)

for k in K_range:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(state_scaled)
    inertias.append(kmeans.inertia_)
    silhouette_scores.append(silhouette_score(state_scaled, kmeans.labels_))

# Plot elbow curve
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

axes[0].plot(K_range, inertias, 'bo-', linewidth=2, markersize=8)
axes[0].set_xlabel('Number of Clusters (k)')
axes[0].set_ylabel('Inertia')
axes[0].set_title('Elbow Method for Optimal k')
axes[0].grid(True, alpha=0.3)

axes[1].plot(K_range, silhouette_scores, 'ro-', linewidth=2, markersize=8)
axes[1].set_xlabel('Number of Clusters (k)')
axes[1].set_ylabel('Silhouette Score')
axes[1].set_title('Silhouette Score for Different k')
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# Perform clustering with k=4
optimal_k = 4
kmeans = KMeans(n_clusters=optimal_k, random_state=42, n_init=10)
clusters = kmeans.fit_predict(state_scaled)
state_aggregated['Cluster'] = clusters

print(f"\n🎯 OPTIMAL CLUSTERS: {optimal_k}")
for cluster_id in range(optimal_k):
    states_in_cluster = state_aggregated[state_aggregated['Cluster'] == cluster_id].index.tolist()
    total_crimes = state_aggregated[state_aggregated['Cluster'] == cluster_id][crime_columns].sum().sum()
    print(f"\nCluster {cluster_id}: {len(states_in_cluster)} states | {int(total_crimes):,} total crimes")
    print(f"  {', '.join(states_in_cluster[:5])}{'...' if len(states_in_cluster) > 5 else ''}")

# Visualize with PCA
pca = PCA(n_components=2)
state_pca = pca.fit_transform(state_scaled)

plt.figure(figsize=(12, 8))
scatter = plt.scatter(state_pca[:, 0], state_pca[:, 1], c=clusters, cmap='viridis', s=200, alpha=0.7, edgecolors='black', linewidth=1.5)

for i, state in enumerate(state_aggregated.index):
    plt.annotate(state, (state_pca[i, 0], state_pca[i, 1]), fontsize=8, ha='center', va='center', fontweight='bold')

plt.xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.1%})')
plt.ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.1%})')
plt.title('State Clusters (K-Means + PCA)', fontsize=14, fontweight='bold')
plt.colorbar(scatter, label='Cluster')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# ============================================================================
# TASK 3: CRIME TYPE DISTRIBUTION
# ============================================================================

print("\n" + "="*80)
print("TASK 3: CRIME TYPE DISTRIBUTION BY STATE")
print("="*80)

crime_type_analysis = df.groupby('State')[crime_columns].sum()

print("\n📊 TOP STATE BY CRIME TYPE:")
for crime in crime_columns:
    top_state = crime_type_analysis[crime].idxmax()
    count = crime_type_analysis[crime].max()
    print(f"  {crime_labels.get(crime, crime):25} → {top_state:25} ({int(count):,})")

# Heatmap
fig, ax = plt.subplots(figsize=(14, 10))

top_states = state_aggregated[crime_columns].sum(axis=1).nlargest(15).index
heatmap_data = crime_type_analysis.loc[top_states, crime_columns]

sns.heatmap(heatmap_data, annot=True, fmt='d', cmap='YlOrRd', cbar_kws={'label': 'Cases'}, ax=ax, linewidths=0.5)
ax.set_title('Crime Distribution Heatmap: Top 15 States', fontsize=14, fontweight='bold')
ax.set_xlabel('Crime Type')
ax.set_ylabel('State')
plt.tight_layout()
plt.show()

# Crime type bar charts
fig, axes = plt.subplots(2, 4, figsize=(18, 10))
axes = axes.flatten()

for idx, crime in enumerate(crime_columns):
    top_10 = crime_type_analysis[crime].nlargest(10)
    top_10.plot(kind='barh', ax=axes[idx], color=plt.cm.Set3(idx), alpha=0.8)
    axes[idx].set_title(f'Top 10: {crime_labels[crime]}', fontsize=11, fontweight='bold')
    axes[idx].set_xlabel('Cases')
    axes[idx].grid(axis='x', alpha=0.3)

axes[-1].remove()
plt.tight_layout()
plt.show()

# ============================================================================
# TEMPORAL TRENDS
# ============================================================================

print("\n" + "="*80)
print("TEMPORAL TRENDS (2001-2012)")
print("="*80)

yearly_crimes = df.groupby('Year')[crime_columns].sum()

fig, axes = plt.subplots(2, 1, figsize=(14, 10))

total_by_year = yearly_crimes.sum(axis=1)
axes[0].plot(yearly_crimes.index, total_by_year, marker='o', linewidth=2.5, markersize=8, color='darkred')
axes[0].fill_between(yearly_crimes.index, total_by_year, alpha=0.3, color='red')
axes[0].set_title('Total Crimes Against Women Over Years', fontsize=14, fontweight='bold')
axes[0].set_ylabel('Total Cases')
axes[0].grid(True, alpha=0.3)

for crime in crime_columns:
    axes[1].plot(yearly_crimes.index, yearly_crimes[crime], marker='o', label=crime_labels.get(crime, crime), linewidth=2)

axes[1].set_title('Crime Types Trends', fontsize=14, fontweight='bold')
axes[1].set_xlabel('Year')
axes[1].set_ylabel('Cases')
axes[1].legend(loc='best', fontsize=10)
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# ============================================================================
# SUMMARY INSIGHTS
# ============================================================================

print("\n" + "="*80)
print("KEY INSIGHTS & STATISTICS")
print("="*80)

total_crimes = df[crime_columns].sum().sum()
print(f"\n📈 TOTAL CRIMES (2001-2012): {int(total_crimes):,}")

print("\n💔 CRIME DISTRIBUTION:")
total_by_crime = df[crime_columns].sum().sort_values(ascending=False)
for crime, count in total_by_crime.items():
    pct = (count / total_crimes) * 100
    bar = '█' * int(pct / 2)
    print(f"  {crime_labels.get(crime, crime):25} {bar} {pct:5.1f}% ({int(count):,} cases)")

print("\n📍 TOP 5 HIGH-CRIME STATES:")
for rank, (state, count) in enumerate(state_crime_totals.head(5).items(), 1):
    pct = (count / total_crimes) * 100
    print(f"  {rank}. {state:25} {int(count):,} cases ({pct:.1f}%)")

# Temporal analysis
first_year = df['Year'].min()
last_year = df['Year'].max()
crimes_first = df[df['Year'] == first_year][crime_columns].sum().sum()
crimes_last = df[df['Year'] == last_year][crime_columns].sum().sum()
growth = ((crimes_last - crimes_first) / crimes_first) * 100

print(f"\n📊 TEMPORAL ANALYSIS:")
print(f"  Year {first_year}: {int(crimes_first):,} cases")
print(f"  Year {last_year}: {int(crimes_last):,} cases")
print(f"  Growth: {growth:+.1f}% over {last_year - first_year} years")

print("\n" + "="*80)
print("✅ ANALYSIS COMPLETE!")
print("="*80)
