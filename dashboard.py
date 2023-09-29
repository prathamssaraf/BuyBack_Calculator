# Import necessary libraries
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from annual_report_downloader import process_annual_report
from data_extractor import convert_images_to_csv
from current_price import get_last_closing_price,get_buyback_price,get_buyback_size
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import locale

#
#
#
#
#
#
# Set the locale to the Indian system
locale.setlocale(locale.LC_NUMERIC, 'en_IN')
#
#
#
#
#
#
url = st.text_input("Enter Chitorgarh URL")
#
#
#
#
#
# Creating DataFrames
years_to_process = ["2020", "2021", "2022","2023"]
company_symbol = st.text_input("Enter the Symbol of the Company")
for year in years_to_process:
    csv_file = f"{company_symbol}_{year}_Shareholding.csv"
    df_name = f"df_{year}"
    globals()[df_name] = pd.read_csv(csv_file)
#
#
#
#
#
#
# Set the title of the dashboard
st.title("My BuyBack Dashboard")
#
#
#
#
#
#
# Create two columns with equal width
col1, col2, col3 = st.columns([1, 1, 2])

# Add content to the first column
with col1:
    # Get the last closing stock price
    last_closing_price = get_last_closing_price(company_symbol)

    # Format the stock price with the Indian comma system
    formatted_stock_price = locale.format_string("%.2f", last_closing_price, grouping=True)

    # Create a box surrounding the KPI component for stock price with styling
    st.markdown(
        f"""
        <div style='border: 2px solid #007BFF; padding: 10px; border-radius: 5px;'>
            <p style='font-weight: bold; font-size: 22px; margin-bottom: 5px;'>Stock Price</p>
            <p style='font-size: 16;'>Rs. <span style='font-weight: bold;font-size: 40px;'>{formatted_stock_price}</span></p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:

    buyback_price = get_buyback_price(url)
    
    last_closing_price = get_last_closing_price(company_symbol)

    # Format the stock price with the Indian comma system
    formatted_stock_price = locale.format_string("%.2f", last_closing_price, grouping=True)

    # Create a box surrounding the KPI component for stock price with styling
    st.markdown(
        f"""
        <div style='border: 2px solid #007BFF; padding: 10px; border-radius: 5px;'>
            <p style='font-weight: bold; font-size: 22px; margin-bottom: 5px;'>BuyBack Price</p>
            <p style='font-size: 16px;'>Rs. <span style='font-weight: bold;font-size: 40px;'>{buyback_price}</span></p>
        </div>
        """,
        unsafe_allow_html=True
    )

# Add content to the second column
with col3:
    # Calculate the average holding in rupees for 2023 based on row 0
    last_closing_price = get_last_closing_price("SIYSIL")
    holding_2023_row_0 = df_2023.iloc[0]['Holding']
    shareholders_2023_row_0 = df_2023.iloc[0]['No of Holders']
    average_holding_in_rupees = (holding_2023_row_0 / shareholders_2023_row_0) * last_closing_price

    # Format the average holding with Indian comma system
    formatted_average_holding = locale.format_string("%.2f", average_holding_in_rupees, grouping=True)

    # Create a box surrounding the KPI component with styling
    st.markdown(
        f"""
        <div style='border: 2px solid #007BFF; padding: 10px; border-radius: 5px;'>
            <p style='font-weight: bold; font-size: 21px; margin-bottom: 5px;'>Average Holding in Rupees (2023)</p>
            <p style='font-size: 24px;'>Rs. <span style='font-weight: bold;font-size: 40px;'>{formatted_average_holding}</span></p>
        </div>
        """,
        unsafe_allow_html=True
    )
#
#
#
#
#
#
#
#
st.markdown("\n\n")
#
#
#
#
#
#
#
col1, col2 = st.columns(2)

with col1:
    
    buyback_size = int((get_buyback_size(url))*0.15)
    # Format the stock price with the Indian comma system
    buyback_size = locale.format_string("%.0f", buyback_size, grouping=True)


        # Create a box surrounding the KPI component for stock price with styling
    st.markdown(
            f"""
            <div style='border: 2px solid #007BFF; padding: 10px; border-radius: 5px;'>
                <p style='font-weight: bold; font-size: 22px; margin-bottom: 5px;'>BuyBack Size - Retail Quota</p>
                <p style='font-size: 16px;'><span style='font-weight: bold;font-size: 40px;'>{buyback_size} Shares</span></p>
            </div>
            """,
            unsafe_allow_html=True
        )
with col2:
    shares_held_by_retailers = df_2023.iloc[0]['Holding']
    
    
    # Format the stock price with the Indian comma system
    shares_held_by_retailers = locale.format_string("%.0f", shares_held_by_retailers, grouping=True)


        # Create a box surrounding the KPI component for stock price with styling
    st.markdown(
            f"""
            <div style='border: 2px solid #007BFF; padding: 10px; border-radius: 5px;'>
                <p style='font-weight: bold; font-size: 22px; margin-bottom: 5px;'>No. of Shares held By Retailers</p>
                <p style='font-size: 16px;'><span style='font-weight: bold;font-size: 40px;'>{shares_held_by_retailers} Shares</span></p>
            </div>
            """,
            unsafe_allow_html=True
        )
#
#
#
#
#
#
#
st.markdown("\n\n")
#
#
#
#
#
#
#
shares_held_by_retailers = float(df_2023.iloc[0]['Holding'])
buyback_size = float((get_buyback_size(url))*0.15)
number = float(buyback_size/shares_held_by_retailers*100)
# Format the stock price with the Indian comma system
number = locale.format_string("%.2f", number, grouping=True)


        # Create a box surrounding the KPI component for stock price with styling
st.markdown(
            f"""
            <div style='border: 2px solid #007BFF; padding: 10px; border-radius: 5px;'>
                <p style='font-weight: bold; font-size: 22px; margin-bottom: 5px;'>Expected Minimum Entitlement Ratio of Buyback</p>
                <p style='font-size: 16px;'><span style='font-weight: bold;font-size: 40px;'>{number} %</span></p>
            </div>
            """,
            unsafe_allow_html=True
        )
#
#
#
#
#
#
#
st.markdown("\n\n")
#
#
#
#
#
#
#




# Now, integrate your existing graph into the dashboard
dfs = [df_2020, df_2021, df_2022, df_2023]
# Extract the first row values from each DataFrame
first_row_values = [df.iloc[0]['Holding'] for df in dfs]
# Create a list of years for the x-axis (assuming the first year is 2020)
years = list(range(2020, 2024))
# Create a line graph with adjusted positioning
fig2, ax2 = plt.subplots(figsize=(10, 6))
ax2.plot(years, first_row_values, marker='o', linestyle='-', color='royalblue')
ax2.set_xlabel('Year')
# Create a custom formatter to display values in lakhs
def lakhs_formatter(x, pos):
    """Format y-axis values in lakhs."""
    return f'{x/100000:.0f} Lacs'
ax2.yaxis.set_major_formatter(ticker.FuncFormatter(lakhs_formatter))
ax2.set_title('Percentage Increase in Holding Over Time')
ax2.set_xticks(years)
ax2.grid(True)
# Adjust the positioning of the graph to top left
fig2.subplots_adjust(top=0.9, left=0.1)
# Display the Matplotlib figure in Streamlit
st.pyplot(fig2)






