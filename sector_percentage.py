import pandas as pd
import psycopg2

# -----------------------------
# PostgreSQL Connection Details
# -----------------------------
DB_HOST = "localhost"
DB_NAME = "stock_project"
DB_USER = "postgres"
DB_PASSWORD = "12345"
DB_PORT = "5432"

# -----------------------------
# Connect to PostgreSQL
# -----------------------------
try:
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT
    )

    # -----------------------------
    # Query Data
    # -----------------------------
    query = """
    SELECT 
        sector,
        average
    FROM sector_average
    ORDER BY average DESC
    """

    df = pd.read_sql(query, conn)

    # Close connection
    conn.close()

    # -----------------------------
    # Convert Decimal to Percentage
    # -----------------------------
    df['average_percentage'] = (df['average'] * 100).round(2)

    # Example:
    # 0.00309 -> 0.31

    # -----------------------------
    # Save as CSV
    # -----------------------------
    output_file = "sector_average_percentage.csv"

    df.to_csv(output_file, index=False)

    print(f"CSV file created successfully: {output_file}")

    # Display Data
    print(df)

except Exception as e:
    print(f"Database Connection Error: {e}")