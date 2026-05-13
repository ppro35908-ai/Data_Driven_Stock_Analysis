import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine

# =====================================================
# PAGE CONFIGURATION
# =====================================================
st.set_page_config(
    page_title="Stock Market Dashboard",
    layout="wide"
)

st.title("📊 Stock Market Analysis Dashboard")

# =====================================================
# DATABASE CONNECTION
# =====================================================
DB_URL = "postgresql+psycopg2://postgres:12345@localhost:5432/stock_project"

engine = create_engine(DB_URL)

# =====================================================
# SIDEBAR MENU
# =====================================================
st.sidebar.title("📌 Navigation")

option = st.sidebar.selectbox(
    "Select Analysis",
    [
        "Volatility Analysis",
        "Cumulative Returns",
        "Sector Average",
        "Stock Price Correlation",
        "Top 5 Gainers and Losers"
    ]
)

# =====================================================
# 1. VOLATILITY ANALYSIS
# =====================================================
if option == "Volatility Analysis":

    st.header("📊 Volatility Analysis")

    analysis_type = st.sidebar.radio(
        "Select View",
        [
            "Top 10 High Volatility Stocks",
            "Top 10 Low Volatility Stocks"
        ]
    )

    # -----------------------------------
    # Dynamic Query
    # -----------------------------------
    if analysis_type == "Top 10 High Volatility Stocks":

        order_direction = "DESC"
        chart_title = "Top 10 Highest Volatility Stocks"
        bar_color = "#00CC96"

    else:

        order_direction = "ASC"
        chart_title = "Top 10 Lowest Volatility Stocks"
        bar_color = "#EF553B"

    query = f"""
        SELECT
            ticker,
            AVG(standard_deviation) AS avg_volatility
        FROM stock_volatility
        GROUP BY ticker
        ORDER BY avg_volatility {order_direction}
        LIMIT 10
    """

    try:

        df = pd.read_sql(query, engine)

        if not df.empty:

            fig = px.bar(
                df,
                x='ticker',
                y='avg_volatility',
                text_auto='.4f',
                title=chart_title,
                color_discrete_sequence=[bar_color]
            )

            fig.update_layout(
                xaxis_title="Stock Symbol",
                yaxis_title="Volatility",
                xaxis_tickangle=-45,
                template="plotly_white",
                height=600
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

            with st.expander(
                "📋 View Data"
            ):
                st.dataframe(
                    df,
                    use_container_width=True
                )

        else:

            st.warning(
                "No data available."
            )

    except Exception as e:

        st.error(f"Database Error: {e}")

# =====================================================
# 2. CUMULATIVE RETURNS
# =====================================================
elif option == "Cumulative Returns":

    st.header("📈 Cumulative Returns")

    # -----------------------------------
    # Date Filters
    # -----------------------------------
    start_dt = st.sidebar.date_input(
        "Start Date",
        value=pd.to_datetime("2023-11-01")
    )

    end_dt = st.sidebar.date_input(
        "End Date",
        value=pd.to_datetime("2024-11-22")
    )

    # -----------------------------------
    # SQL Query
    # -----------------------------------
    query = f"""
        SELECT
            ticker,
            date,
            return
        FROM cumulative_return
        WHERE date BETWEEN '{start_dt}' AND '{end_dt}'
        ORDER BY date ASC
    """

    try:

        df = pd.read_sql(
            query,
            engine
        )

        if not df.empty:

            # -----------------------------------
            # Convert Date
            # -----------------------------------
            df['date'] = pd.to_datetime(
                df['date']
            )

            # -----------------------------------
            # Calculate Cumulative Return
            # -----------------------------------
            df['cum_return'] = df.groupby(
                'ticker'
            )['return'].transform(
                lambda x: (1 + x.fillna(0)).cumprod() - 1
            )

            # -----------------------------------
            # Top 5 Stocks
            # -----------------------------------
            last_values = df.groupby(
                'ticker'
            ).last()[['cum_return']].sort_values(
                by='cum_return',
                ascending=False
            )

            top_5 = last_values.head(5).index.tolist()

            top_df = df[
                df['ticker'].isin(top_5)
            ]

            # -----------------------------------
            # Line Chart
            # -----------------------------------
            fig = px.line(
                top_df,
                x='date',
                y='cum_return',
                color='ticker',
                title="Top 5 Performing Stocks"
            )

            fig.update_layout(
                template="plotly_white",
                height=600
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

            with st.expander(
                "📋 Final Cumulative Returns"
            ):
                st.dataframe(
                    last_values.head(5),
                    use_container_width=True
                )

        else:

            st.warning(
                "No data found."
            )

    except Exception as e:

        st.error(f"Database Error: {e}")

# =====================================================
# 3. SECTOR AVERAGE
# =====================================================
elif option == "Sector Average":

    st.header("🏭 Average Yearly Return by Sector")

    query = """
        SELECT
            sector,
            average
        FROM sector_average
        ORDER BY average DESC
    """

    try:

        df = pd.read_sql(
            query,
            engine
        )

        if not df.empty:

            # -----------------------------------
            # Metrics
            # -----------------------------------
            best_sector = df.loc[
                df['average'].idxmax()
            ]

            low_sector = df.loc[
                df['average'].idxmin()
            ]

            overall_avg = df['average'].mean()

            df['difference'] = abs(
                df['average'] - overall_avg
            )

            stable_sector = df.loc[
                df['difference'].idxmin()
            ]

            # -----------------------------------
            # KPI Cards
            # -----------------------------------
            col1, col2, col3 = st.columns(3)

            with col1:
                st.success(
                    f"""
                    Best Sector

                    {best_sector['sector']}

                    {best_sector['average']:.4f}%
                    """
                )

            with col2:
                st.error(
                    f"""
                    Lowest Sector

                    {low_sector['sector']}

                    {low_sector['average']:.4f}%
                    """
                )

            with col3:
                st.info(
                    f"""
                    Stable Sector

                    {stable_sector['sector']}

                    {stable_sector['average']:.4f}%
                    """
                )

            # -----------------------------------
            # Bar Chart
            # -----------------------------------
            fig = px.bar(
                df,
                x="sector",
                y="average",
                text="average",
                color="average",
                title="Average Yearly Return by Sector"
            )

            fig.update_traces(
                texttemplate='%{text:.4f}',
                textposition='outside'
            )

            fig.update_layout(
                xaxis_title="Sector",
                yaxis_title="Average Return",
                template="plotly_white",
                height=600
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        else:

            st.warning(
                "No data available."
            )

    except Exception as e:

        st.error(f"Database Error: {e}")

# =====================================================
# 4. STOCK PRICE CORRELATION
# =====================================================
elif option == "Stock Price Correlation":

    st.header("📈 Stock Correlation Heatmap")

    query = """
        SELECT
            stock_1,
            stock_2,
            correlation
        FROM correlate_stocks
    """

    try:

        df = pd.read_sql(
            query,
            engine
        )

        if not df.empty:

            # -----------------------------------
            # Pivot Table
            # -----------------------------------
            heatmap_data = df.pivot(
                index='stock_1',
                columns='stock_2',
                values='correlation'
            )

            # -----------------------------------
            # Heatmap
            # -----------------------------------
            fig = px.imshow(
                heatmap_data,
                text_auto=True,
                color_continuous_scale='RdBu_r',
                aspect='auto',
                title='Stock Correlation Heatmap'
            )

            fig.update_layout(
                height=900
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

            # -----------------------------------
            # Positive Correlation
            # -----------------------------------
            st.subheader(
                "📈 Top Positive Correlations"
            )

            top_positive = df.sort_values(
                by='correlation',
                ascending=False
            ).head(10)

            st.dataframe(
                top_positive,
                use_container_width=True
            )

            # -----------------------------------
            # Negative Correlation
            # -----------------------------------
            st.subheader(
                "📉 Top Negative Correlations"
            )

            top_negative = df.sort_values(
                by='correlation',
                ascending=True
            ).head(10)

            st.dataframe(
                top_negative,
                use_container_width=True
            )

        else:

            st.warning(
                "No data available."
            )

    except Exception as e:

        st.error(f"Database Error: {e}")

# =====================================================
# 5. TOP 5 GAINERS & LOSERS
# =====================================================
elif option == "Top 5 Gainers and Losers":

    st.header("📈 Monthly Top 5 Gainers & Losers")

    try:

        df = pd.read_sql(
            "SELECT * FROM monthly_top_gainer_top_loser",
            engine
        )

        for i in range(len(df)):

            row = df.iloc[i]

            month = row["Month"]

            stock = []
            value = []
            category = []

            # -----------------------------------
            # Top 5 Gainers
            # -----------------------------------
            for j in range(1, 6):

                stock.append(
                    row[f"Gainer_{j}"]
                )

                value.append(
                    row[f"Gainer_{j}_Return_%"]
                )

                category.append(
                    "Gainer"
                )

            # -----------------------------------
            # Top 5 Losers
            # -----------------------------------
            for j in range(1, 6):

                stock.append(
                    row[f"Loser_{j}"]
                )

                value.append(
                    row[f"Loser_{j}_Return_%"]
                )

                category.append(
                    "Loser"
                )

            # -----------------------------------
            # Create DataFrame
            # -----------------------------------
            chart_df = pd.DataFrame({

                "Stock": stock,
                "Return %": value,
                "Category": category

            })

            # -----------------------------------
            # Bar Chart
            # -----------------------------------
            fig = px.bar(
                chart_df,
                x="Return %",
                y="Stock",
                color="Category",
                orientation="h",
                text="Return %",
                title=f"{month} - Top 5 Gainers & Losers",
                color_discrete_map={
                    "Gainer": "green",
                    "Loser": "red"
                }
            )

            fig.update_traces(
                textposition="outside"
            )

            fig.update_layout(
                height=500,
                template="plotly_white",
                yaxis={
                    'categoryorder': 'total ascending'
                }
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

            with st.expander(
                f"📋 {month} Data"
            ):
                st.dataframe(
                    chart_df,
                    use_container_width=True
                )

    except Exception as e:

        st.error(f"Database Error: {e}")