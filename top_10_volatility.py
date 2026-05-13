import pandas as pd
from sqlalchemy import create_engine

# DATABASE CONNECTION
DB_URL = 'postgresql://postgres:12345@localhost:5432/stock_project'
engine = create_engine(DB_URL)

# -----------------------------
# TOP 10 HIGH VOLATILITY
# -----------------------------
high_query = """
SELECT 
    ticker,
    AVG(standard_deviation) AS avg_volatility
FROM stock_volatility
GROUP BY ticker
ORDER BY avg_volatility DESC
LIMIT 10;
"""

# -----------------------------
# TOP 10 LOW VOLATILITY
# -----------------------------
low_query = """
SELECT 
    ticker,
    AVG(standard_deviation) AS avg_volatility
FROM stock_volatility
GROUP BY ticker
ORDER BY avg_volatility ASC
LIMIT 10;
"""

try:
    # Read data
    high_df = pd.read_sql(high_query, engine)
    low_df = pd.read_sql(low_query, engine)

    # Rename columns
    high_df.columns = ['Top 10 High Volatility Stocks', 'High Volatility Value']
    low_df.columns = ['Top 10 Low Volatility Stocks', 'Low Volatility Value']

    # Combine into single DataFrame
    final_df = pd.concat([high_df, low_df], axis=1)

    # Export single CSV
    final_df.to_csv("top_10_volatility_report.csv", index=False)

    print("Single CSV file created successfully!")
    print(final_df)

except Exception as e:
    print("Database Error:", e)