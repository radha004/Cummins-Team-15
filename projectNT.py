import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import glob
import requests
import numpy as np
import matplotlib.pyplot as plt
import os

# App Title 
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>Currency Exchange Rate Analysis Dashboard</h1>", unsafe_allow_html=True)

# Description 
st.markdown("<p style='text-align: center; color: #6A5ACD;'>Analyze historical exchange rates between the U.S. dollar (USD) and other currencies.<br>Visualize trends across different frequencies: Annual, Monthly, Weekly, Quarterly.</p>", unsafe_allow_html=True)

# Layout Two columns for frequency and year selection
col1, col2 = st.columns(2)

# Dropdown for frequency (Annual, Monthly, Weekly, Quarterly)
with col1:
    frequency = st.selectbox("Select Frequency", ['Annual', 'Monthly', 'Weekly', 'Quarterly'])

# Dropdown for Year, disabled if Annual is selected
with col2:
    years = list(range(2012, 2025))  # From 2012 to 2024
    selected_year = st.selectbox("Select Year", years, disabled=(frequency == 'Annual'))

# All annual CSV files into single DataFrame
def read_annual_data():
    files = glob.glob("C:/Users/Piyu/currency_dashboard/Currency Conversion Rate Data From 2012/Exchange_Rate_Report_*.csv")
    dataframes = []
    for file in files:
        if '2023' in file or '2024' in file:
            df = pd.read_csv(file, parse_dates=['Date'], dayfirst=True, date_parser=lambda x: pd.to_datetime(x, format='%d-%m-%Y', errors='coerce'))
        else:
            df = pd.read_csv(file, parse_dates=['Date'], dayfirst=True)
        dataframes.append(df)
    return pd.concat(dataframes, ignore_index=True)

def read_selected_year_data(year):
    file_path = f"C:/Users/Piyu/currency_dashboard/Currency Conversion Rate Data From 2012/Exchange_Rate_Report_{year}.csv"
    if year in [2023, 2024]:
        return pd.read_csv(file_path, parse_dates=['Date'], dayfirst=True, date_parser=lambda x: pd.to_datetime(x, format='%d-%m-%Y', errors='coerce'))
    else:
        return pd.read_csv(file_path, parse_dates=['Date'], dayfirst=True)

def process_data(data, frequency):
    data['Date'] = pd.to_datetime(data['Date'])
    processed_data = pd.DataFrame()

    if frequency == 'Annual':
        processed_data = data.groupby(data['Date'].dt.year).mean()
    elif frequency == 'Monthly':
        processed_data = data.groupby(data['Date'].dt.to_period("M")).mean()
        processed_data.index = processed_data.index.to_timestamp()
    elif frequency == 'Weekly':
        processed_data = data.resample('W-Mon', on='Date').mean()
    elif frequency == 'Quarterly':
        processed_data = data.resample('Q', on='Date').mean()

    return processed_data

processed_data = pd.DataFrame()

if frequency == 'Annual':
    data = read_annual_data()
    processed_data = process_data(data, frequency)
else:
    data = read_selected_year_data(selected_year)
    processed_data = process_data(data, frequency)

# Display processed data and metrics
if not processed_data.empty:
    currency1 =  'U.S. dollar   (USD)                     ' # Base Currency
    currency1 = st.selectbox("Currency 1 (Base Currency)                    ",  currency1)
    currency_columns = processed_data.columns[1:].tolist()  # Exclude 'Date' column
    currency2 = st.selectbox("Select Currency 2", currency_columns)

    if currency2 in processed_data.columns:
        peak_rate = processed_data[currency2].max()
        peak_row = processed_data[processed_data[currency2] == peak_rate].iloc[0]
        peak_date = peak_row.name.strftime('%Y-%m-%d') if isinstance(peak_row.name, pd.Timestamp) else str(peak_row)

        lowest_rate = processed_data[currency2].min()
        lowest_row = processed_data[processed_data[currency2] == lowest_rate].iloc[0]
        lowest_date = lowest_row.name.strftime('%Y-%m-%d') if isinstance(lowest_row.name, pd.Timestamp) else str(lowest_row)

        col3, col4 = st.columns(2)
        with col3:
            st.metric("Peak Rate", f"{peak_rate:.2f}", delta=None, help=f"Peak Date: {peak_date}", delta_color="normal")
        with col4:
            st.metric("Lowest Rate", f"{lowest_rate:.2f}", delta=None, help=f"Lowest Date: {lowest_date}", delta_color="inverse")

        # Create Plotly chart
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=processed_data.index, y=processed_data[currency2],
                                 mode='lines+markers',
                                 name=currency2,
                                 marker=dict(color='#FF6347'),
                                 fill='tozeroy',
                                 hoverinfo='text',
                                 hovertext=processed_data[currency2].apply(lambda x: f'Rate: {x:.2f}')))

        # Update layout
        fig.update_layout(title=f'{frequency} Exchange Rate of {currency2} (2012-2022)',
                          xaxis_title='Date',
                          yaxis_title=f'Exchange Rate ({currency2})',
                          template='plotly_white')

        # Plot in Streamlit
        st.plotly_chart(fig)

        # Calculate and display volatility
        rolling_volatility = processed_data[currency2].rolling(window=5).std()  # Rolling 5-day volatility
        processed_data['Volatility'] = rolling_volatility

        # Plot volatility
        plt.figure(figsize=(10, 5))
        plt.plot(processed_data.index, rolling_volatility, label='Volatility', color='blue')
        plt.axhline(y=rolling_volatility.mean(), color='orange', linestyle='--', label='Mean Volatility')
        plt.fill_between(processed_data.index, rolling_volatility, rolling_volatility.mean(),
                         where=(rolling_volatility > rolling_volatility.mean()),
                         color='red', alpha=0.3, label='High Risk')
        plt.fill_between(processed_data.index, rolling_volatility, rolling_volatility.mean(),
                         where=(rolling_volatility <= rolling_volatility.mean()),
                         color='green', alpha=0.3, label='Low Risk')
        plt.title(f'Volatility of {currency2} Exchange Rate (Rolling 5-Day)')
        plt.xlabel('Date')
        plt.ylabel('Volatility')
        plt.legend()
        plt.grid()
        st.pyplot(plt)

    else:
        st.error(f"Currency '{currency2}' not found in the data.")
else:
    st.error("No data available for the selected frequency.")

# Custom Currency Basket Feature with colored text
st.markdown("<h2 style='text-align: left; color: #FF4500;'>Custom Currency Basket</h2>", unsafe_allow_html=True)

base_currency = st.selectbox("Select Base Currency", 'USD')

# User Input for Custom Currency Basket
num_currencies = st.number_input("Number of Currencies in Basket", min_value=1, max_value=10, value=3)

# List of available currencies for selection
available_currencies = [
    'DZD', 'AUD', 'BHD', 'VEF', 'BWP', 'BRL', 'BND', 'CAD', 'CLP', 
    'CNY', 'COP', 'CZK', 'DKK', 'EUR', 'HUF', 'ISK', 'INR', 'IDR', 
    'IRR', 'ILS', 'JPY', 'KZT', 'KRW', 'KWD', 'LYD', 'MYR', 'MUR', 
    'MXN', 'NPR', 'NZD', 'NOK', 'OMR', 'PKR', 'PEN', 'PHP', 'PLN', 
    'QAR', 'RUB', 'SAR', 'SGD', 'ZAR', 'LKR', 'SEK', 'CHF', 'THB', 
    'TTD', 'TND', 'AED', 'GBP', 'USD', 'UYU'
]
selected_currencies = []
weights = []

# Dropdown for each currency selection and corresponding weight input
for i in range(num_currencies):
    selected_currency = st.selectbox(f"Select Currency {i + 1}", available_currencies, key=f"currency_{i}")
    weight = st.number_input(f"Enter Weight for {selected_currency} (%)", min_value=0.0, max_value=100.0, key=f"weight_{i}")
    selected_currencies.append(selected_currency)
    weights.append(weight)

# Function to fetch exchange rates for the custom basket calculation
def fetch_exchange_rates(base_currency):
    url = f"https://api.exchangerate-api.com/v4/latest/{base_currency}"
    response = requests.get(url)
    return response.json()['rates']

# Calculate the weighted average for the custom basket
if st.button("Calculate Basket Rate"):
    try:
        exchange_rates = fetch_exchange_rates(base_currency)
        total_weight = sum(weights)
        basket_rate = sum(exchange_rates[currency] * (weight / 100) for currency, weight in zip(selected_currencies, weights))
        weighted_average = basket_rate / total_weight if total_weight > 0 else 0

        st.success(f"The weighted average exchange rate for your custom basket is: {weighted_average:.2f}")
    except Exception as e:
        st.error(f"Error fetching exchange rates: {e}")

# Function to fetch current exchange rates
def fetch_current_exchange_rates():
    url = "https://api.exchangerate-api.com/v4/latest/USD" 
    response = requests.get(url)
    return response.json()['rates']

# Add feature to display current exchange rates
st.markdown("<h2 style='text-align: left; color: #FF4500;'>Current Exchange Rates</h2>", unsafe_allow_html=True)

current_rates = fetch_current_exchange_rates()
currency_selection = st.selectbox("Select Currency", list(current_rates.keys()))

if currency_selection:
    current_rate = current_rates[currency_selection]
    st.write(f"Current exchange rate for {currency_selection} is: {current_rate:.2f}")
