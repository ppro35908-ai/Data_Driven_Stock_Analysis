import pandas as pd
import psycopg2

# -----------------------------
# PostgreSQL Connection Details
# -----------------------------
DB_NAME = "stock_project"
DB_USER = "postgres"
DB_PASSWORD = "12345"
DB_HOST = "localhost"
DB_PORT = "5432"

# -----------------------------
# Database Connection
# -----------------------------
def get_connection():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )

# -----------------------------
# Fetch Stock Data
# -----------------------------
def fetch_stock_data(start_date, end_date):

    conn = get_connection()

    query = f"""
    SELECT 
        ticker,
        date,
        return
    FROM cumulative_return
    WHERE date BETWEEN '{start_date}' AND '{end_date}'
    ORDER BY ticker, date;
    """

    df = pd.read_sql(query, conn)

    conn.close()

    return df

# -----------------------------
# Main Program
# -----------------------------
try:

    # Define Year Range
    start_date = "2023-11-01"
    end_date = "2024-11-22"

    # Load Data
    df = fetch_stock_data(start_date, end_date)

    if not df.empty:

        # Convert date column
        df['date'] = pd.to_datetime(df['date'])

        # Rename return column
        df.rename(columns={'return': 'daily_return'}, inplace=True)

        # -----------------------------
        # Calculate Cumulative Return
        # -----------------------------
        df['cumulative_return'] = df.groupby('ticker')['daily_return'].transform(
            lambda x: (1 + x.fillna(0)).cumprod() - 1
        )

        # -----------------------------
        # Find Top 5 Performing Stocks
        # -----------------------------
        top_5 = (
            df.groupby('ticker')
            .last()[['cumulative_return']]
            .sort_values(by='cumulative_return', ascending=False)
            .head(5)
            .reset_index()
        )

        # -----------------------------
        # Merge Top 5 with Full Data
        # -----------------------------
        top_5_tickers = top_5['ticker'].tolist()

        top_5_data = df[df['ticker'].isin(top_5_tickers)]

        # Keep Required Columns
        top_5_data = top_5_data[
            ['ticker', 'date', 'daily_return', 'cumulative_return']
        ]

        # Sort Properly
        top_5_data = top_5_data.sort_values(
            by=['ticker', 'date']
        )

        # -----------------------------
        # Save CSV
        # -----------------------------
        output_file = "top_5_performing_stocks_of_year.csv"

        top_5_data.to_csv(output_file, index=False)

        print(f"\nCSV File Created Successfully: {output_file}")

        print("\nTop 5 Performing Stocks:\n")
        print(top_5)

    else:
        print("No data found for the selected year.")

except Exception as e:
    print(f"Error: {e}")