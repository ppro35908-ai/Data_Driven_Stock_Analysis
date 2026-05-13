# stock_correlation.py

import pandas as pd

# ---------------------------------
# Read CSV File
# ---------------------------------
df = pd.read_csv(
    r"C:\Users\welcome\Desktop\stock_project\Merged_Sector_Stock_market.csv"
)

# ---------------------------------
# Display Column Names
# ---------------------------------
print("Columns in CSV:")
print(df.columns)

# ---------------------------------
# Convert Date Column
# ---------------------------------
df['date'] = pd.to_datetime(df['date'])

# ---------------------------------
# Create Pivot Table
# ---------------------------------
pivot_df = df.pivot_table(
    index='date',
    columns='Company',
    values='close'
)

# ---------------------------------
# Calculate Correlation Matrix
# ---------------------------------
correlation_matrix = pivot_df.corr()

# ---------------------------------
# Convert Correlation Matrix
# into Row Format
# ---------------------------------
corr_pairs = correlation_matrix.unstack()

corr_pairs = corr_pairs.to_frame('Correlation')

corr_pairs.index.names = [
    'Stock_1',
    'Stock_2'
]

corr_pairs = corr_pairs.reset_index()

# ---------------------------------
# Remove Same Stock Comparison
# ---------------------------------
corr_pairs = corr_pairs[
    corr_pairs['Stock_1'] != corr_pairs['Stock_2']
]

# ---------------------------------
# Remove Duplicate Pairs
# ---------------------------------
corr_pairs['Pair'] = corr_pairs.apply(
    lambda x: '-'.join(
        sorted([x['Stock_1'], x['Stock_2']])
    ),
    axis=1
)

corr_pairs = corr_pairs.drop_duplicates(
    subset='Pair'
)

# ---------------------------------
# Positive Correlated Stocks
# ---------------------------------
# ---------------------------------
# Filter Strong Correlations
# ---------------------------------

filtered_corr = corr_pairs[
    (corr_pairs['Correlation'] > 0.3) |
    (corr_pairs['Correlation'] < -0.3)
].copy()

# ---------------------------------
# Add Correlation Type
# ---------------------------------

filtered_corr['Type'] = filtered_corr[
    'Correlation'
].apply(
    lambda x: 'Positive'
    if x > 0 else 'Negative'
)

# ---------------------------------
# Keep Required Columns
# ---------------------------------

final_df = filtered_corr[
    ['Stock_1', 'Stock_2', 'Correlation', 'Type']
]

# ---------------------------------
# Save CSV
# ---------------------------------

final_df.to_csv(
    r"C:\Users\welcome\Desktop\stock_project\Correlation_result.csv",
    index=False
)

# ---------------------------------
# Display Output
# ---------------------------------

print("\nFinal Correlation Data:")
print(final_df)

print("\nCSV file created successfully!")