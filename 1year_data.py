import pandas as pd

# -----------------------------------
# Load Dataset
# -----------------------------------
df = pd.read_csv(
    r"C:\Users\welcome\Desktop\stock_project\Merged_Sector_Stock_market.csv"
)

# -----------------------------------
# Convert Date Column
# -----------------------------------
df['date'] = pd.to_datetime(df['date'])

# -----------------------------------
# Create Month Column
# -----------------------------------
df['Month'] = df['date'].dt.to_period('M').astype(str)

# -----------------------------------
# Sort Properly
# -----------------------------------
df = df.sort_values(by=['Company', 'date'])

# -----------------------------------
# Calculate Monthly Returns
# -----------------------------------
monthly_returns = []

# Group by Company and Month
grouped = df.groupby(['Company', 'Month'])

for (company, month), group in grouped:

    # Sort dates inside each month
    group = group.sort_values(by='date')

    # First and Last Closing Price
    start_price = group.iloc[0]['close']
    end_price = group.iloc[-1]['close']

    # Avoid division by zero
    if start_price == 0:
        continue

    # Monthly Return %
    monthly_return = (
        (end_price - start_price)
        / start_price
    ) * 100

    monthly_returns.append({
        'Month': month,
        'Company': company,
        'Monthly Return %': round(monthly_return, 2)
    })

# -----------------------------------
# Create Monthly Returns DataFrame
# -----------------------------------
monthly_returns_df = pd.DataFrame(monthly_returns)

# -----------------------------------
# Create Output Folder (Optional)
# -----------------------------------
import os

output_folder = "Monthly_Gainers_Losers"

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# -----------------------------------
# Generate Month-wise CSV Files
# -----------------------------------
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

    top_gainers['Type'] = 'Gainer'

    # -----------------------------------
    # Top 5 Losers
    # -----------------------------------
    top_losers = temp.sort_values(
        by='Monthly Return %',
        ascending=True
    ).head(5)

    top_losers['Type'] = 'Loser'

    # -----------------------------------
    # Combine Both
    # -----------------------------------
    final_month_df = pd.concat(
        [top_gainers, top_losers],
        ignore_index=True
    )

    # -----------------------------------
    # Reorder Columns
    # -----------------------------------
    final_month_df = final_month_df[
        ['Month', 'Type', 'Company', 'Monthly Return %']
    ]

    # -----------------------------------
    # Save CSV
    # -----------------------------------
    file_name = f"{output_folder}/{month}_Top5_Gainers_Losers.csv"

    final_month_df.to_csv(
        file_name,
        index=False
    )

    print(f"Saved: {file_name}")

print("\nAll Monthly CSV Files Generated Successfully!")