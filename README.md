# Data_Driven_Stock_Analysis
In this project, we created streamlit dashboard and power bi dashboard by using Language:python, Database:postgresql, Visualisation tool :Streamlit and Power bi and the Libraries: Pandas, datetime, psycopg2. In this dashboard  helps Investors, analysts, and enthusiasts make informed decisions based on the stock performance trends.
1st step
 Yaml to master_market_data_2023_2024.csv
2nd step 
Cleaning  ‘Sector.csv’ into clean_sector.csv and ‘stock_market_data_2023_2024.csv’ into clean_stock_market.csv
3rd step 
Both csv merged and created Merged_Sector_Stock_market.csv
4th step
Merged_Sector_Stock_market.csv   created into separate Ticker File Folder which contains different csv’s based on Ticker
5th step 
Created volatility_output folder which contains csv’s with topics Tickers , date , standard deviation
Visualization 0f volatility Analysis:
In volatility.ipynb- By using a Ticker_Files folder created volatility_output folder which contains volatility of different stocks
Visualisation of Cumulative return:
In cumulative_return.py- By using a Ticker_Files folder, found return of stocks and created as a cumulative_return folder which contains returns of stocks as csv files
Visualisation of Sector performance:
In sector.py file- By using Clean_Sector_data.csv and Clean_Stock_Market_data.csv found average of stocks and merged both files by using common column Ticker and created final_sector_average.csv file which has columns like sector and average 
Visualisation of stock price correlation: 
In correlate_stock.py file – By using Merge_Sector_Stock.csv correlated stocks by date and company name and value used here is positive correlated >0.3 and Negative correlated <0.3,  created Correlation_result.csv file which has four columns Stock_1, Stock_2, Correlation, Type.
Visualisation of top gainers and top losers:
In Monthwise_gainer_loser.py – By using Merge_Sector_Stock_Market.csv created top 5 gainers and losers as Monthly_gainers_losers_report.csv 
These five different csv's imported in postgresql in database stock_project and the tables stock_volatilit,cumulative_return, correlate_stocks, sector_average, monthly_top_gainer_top_loser
Finally, in Final_Visualization.py file created a code to connect with postgresql tables and visualized it in streamlit.
And 
we create same dashboard in powerbi by using csv files
