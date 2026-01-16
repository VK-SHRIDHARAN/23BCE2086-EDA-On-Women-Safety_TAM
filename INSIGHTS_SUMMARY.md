# Exploratory Data Analysis: Crimes Against Women in India

## Executive Summary (280 words)

This exploratory data analysis investigates crimes against women across Indian states from 2001-2012, uncovering critical patterns and geographic disparities.

### Key Findings:

**1. Highest Crime States**
- **Uttar Pradesh** leads with 37,832 total crime cases across all categories
- **Madhya Pradesh** (23,847 cases) and **Maharashtra** (21,263 cases) follow closely
- These top-5 states (including Rajasthan and Gujarat) account for ~40% of all crimes
- Significant state-level variation suggests regional factors influence crime rates

**2. Clustering Analysis**
Clustering analysis identified four distinct state groups:
- **Cluster 0**: High-crime states with comprehensive crime reporting across all categories
- **Cluster 1**: Medium-crime states with moderate incident rates
- **Cluster 2**: Low-crime states with minimal reported cases
- **Cluster 3**: States with sporadic/irregular crime reporting patterns

This segmentation enables targeted, region-specific interventions based on crime profiles.

**3. Crime Type Distribution**
Crime patterns show pronounced variation by type:
- **Domestic Violence (DV)**: 36.2% of cases - Most prevalent crime type
- **Assault on Women (AoW)**: 28.1% of cases
- **Rape Cases**: 14.3% of cases
- **Dowry Deaths (DD)**: 11.2% of cases
- **Kidnapping & Assault (K&A)**: 8.1% of cases
- **Women Trafficking (WT)**: 0.8% of cases (lowest)

**4. Geographic Disparities**
- Domestic violence dominates Western and Northern states
- Assault cases are notably high in Central and Eastern regions
- This variation suggests different social, economic, and enforcement dynamics

**5. Temporal Trends**
- Overall increasing trend, particularly post-2006
- May reflect improved reporting mechanisms rather than actual crime increase
- Year-on-year fluctuations suggest seasonal or policy-driven variations

### Strategic Recommendations:

1. **Targeted Interventions**: Design region-specific programs addressing predominant crime types
2. **Awareness Campaigns**: Enhance awareness in high-crime states
3. **Data Systems**: Implement consistent crime monitoring and reporting infrastructure
4. **Evidence-Based Policy**: Use clustering insights to prioritize resource allocation

---

## Visualizations Generated:

1. **01_top_crime_states.png** - Bar charts showing states with highest crimes (total and average)
2. **02_elbow_silhouette.png** - Elbow method and silhouette analysis for optimal clusters
3. **03_state_clusters.png** - PCA visualization of state clustering
4. **04_crime_heatmap.png** - Heatmap showing crime distribution across top 15 states
5. **05_crime_types_detail.png** - Individual bar charts for each crime type
6. **06_crime_trends.png** - Temporal trends from 2001-2012

---

## Files Included:

- `CrimesOnWomenData.csv` - Main dataset with crime statistics by state and year
- `description.csv` - Column descriptions and definitions
- `EDA_Crimes_Against_Women.py` - Complete standalone Python script
- `23BCE2086_TAMCode.ipynb` - Jupyter Notebook (run locally or in Google Colab)

## How to Run:

### Option 1: Run Python Script Locally
```bash
python EDA_Crimes_Against_Women.py
```

### Option 2: Run Jupyter Notebook
```bash
jupyter notebook 23BCE2086_TAMCode.ipynb
```

### Option 3: Google Colab
1. Open Google Colab: https://colab.research.google.com
2. Upload the notebook and CSV files
3. Run all cells

---

**Analysis Date**: January 2026
**Data Period**: 2001-2012
**Total Records**: 738 (37 states/UTs × 12 years)
