import pandas as pd

# -----------------------------------
# Load dataset
# -----------------------------------
df = pd.read_csv(
    r"C:\Users\welcome\Desktop\stock_project\Merged_Sector_Stock_market.csv"
)

# -----------------------------------
# Convert date column
# -----------------------------------
df['date'] = pd.to_datetime(df['date'])

# -----------------------------------
# Create Month column
# -----------------------------------
df['Month'] = df['date'].dt.strftime('%Y-%m')

# -----------------------------------
# Sort data
# -----------------------------------
df = df.sort_values(by=['Company', 'date'])

# -----------------------------------
# Calculate Monthly Returns
# -----------------------------------
monthly_data = []

for company in df['Company'].unique():

    company_df = df[df['Company'] == company]

    for month in company_df['Month'].unique():

        month_df = company_df[
            company_df['Month'] == month
        ]

        if len(month_df) == 0:
            continue

        # Start and End Price
        start_price = month_df.iloc[0]['close']
        end_price = month_df.iloc[-1]['close']

        # Monthly Return %
        monthly_return = (
            (end_price - start_price)
            / start_price
        ) * 100

        monthly_data.append({
            'Month': month,
            'Company': company,
            'Monthly Return %': round(monthly_return, 2)
        })

# -----------------------------------
# Create DataFrame
# -----------------------------------
monthly_returns_df = pd.DataFrame(monthly_data)

# -----------------------------------
# Final Report
# -----------------------------------
final_rows = []

for month in monthly_returns_df['Month'].unique():

    temp = monthly_returns_df[
        monthly_returns_df['Month'] == month
    ]

    # -----------------------------------
    # Top 5 Gainers
    # -----------------------------------
    top_gainers = temp.sort_values(
        by='Monthly Return %',
        ascending=False
    ).head(5)

    # -----------------------------------
    # Top 5 Losers
    # -----------------------------------
    top_losers = temp.sort_values(
        by='Monthly Return %',
        ascending=True
    ).head(5)

    # -----------------------------------
    # Create Row
    # -----------------------------------
    row = {
        'Month': month
    }

    # -----------------------------------
    # Add Gainers
    # -----------------------------------
    for i, (_, r) in enumerate(
        top_gainers.iterrows(), 1
    ):

        row[f'Gainer_{i}'] = r['Company']
        row[f'Gainer_{i}_Return_%'] = (
            r['Monthly Return %']
        )

    # -----------------------------------
    # Add Losers
    # -----------------------------------
    for i, (_, r) in enumerate(
        top_losers.iterrows(), 1
    ):

        row[f'Loser_{i}'] = r['Company']
        row[f'Loser_{i}_Return_%'] = (
            r['Monthly Return %']
        )

    final_rows.append(row)

# -----------------------------------
# Final DataFrame
# -----------------------------------
final_df = pd.DataFrame(final_rows)

# -----------------------------------
# Save CSV
# -----------------------------------
final_df.to_csv(
    "monthly_top5_gainers_losers.csv",
    index=False
)

print("Saved: monthly_top5_gainers_losers.csv")