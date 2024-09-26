# Currency Exchange Rate Analysis Dashboard

## Overview
The **Currency Exchange Rate Analysis Dashboard** is a web application built with Streamlit that allows users to analyze historical exchange rates between the U.S. dollar (USD) and other currencies. Users can visualize trends across different frequencies (Annual, Monthly, Weekly, Quarterly) and calculate a custom currency basket based on selected currencies and their weights.

## Features
- **Frequency Selection**: Choose between different frequency options for exchange rate data (Annual, Monthly, Weekly, Quarterly).
- **Year Selection**: Select a specific year for analysis (disabled for Annual frequency).
- **Data Visualization**: Interactive charts using Plotly to visualize exchange rates and volatility.
- **Custom Currency Basket**: Create a weighted average exchange rate for a basket of selected currencies.
- **Current Exchange Rates**: Display the latest exchange rates for various currencies.

##Data Handling
Null Values in csv files are replaced by appropriate measure.

## Installation

### Prerequisites
Make sure you have the following installed:
- Python 3.6 or later
- Streamlit
- Pandas
- Plotly
- Requests
- Matplotlib

### Installation Steps
1. Clone this repository or download the code files.
2. Navigate to the project directory in your terminal.
3. Install the required packages:
   ```bash
   pip install streamlit pandas plotly requests matplotlib
   ```

## Usage
1. Place your CSV files containing exchange rate data in the specified directory:
   ```
   C:/Users/Piyu/currency_dashboard/Currency Conversion Rate Data From 2012/
   ```
   Ensure that the filenames follow the format `Exchange_Rate_Report_<year>.csv`.

2. Run the Streamlit app:
   ```bash
   streamlit run projectNT.py

3. Access the dashboard in your web browser at `http://localhost:8501`.

## User Instructions
- Select the frequency and year of the exchange rates you wish to analyze.
- Choose a base currency and a secondary currency to compare.
- View the peak and lowest rates along with an interactive line chart of the selected currency.
- Use the **Custom Currency Basket** feature to select multiple currencies and enter their corresponding weights. Click the "Calculate Basket Rate" button to compute the weighted average exchange rate.
- Check the latest exchange rates for selected currencies.

## Code Explanation
- The app is divided into several sections:
  - **Header and Description**: Displays the title and a brief description of the app.
  - **Data Reading Functions**: Functions to read annual and specific year data from CSV files.
  - **Data Processing Functions**: Functions to process the data according to the selected frequency.
  - **Metrics and Visualization**: Displays key metrics and generates plots for the selected currency.
  - **Custom Currency Basket**: Allows users to input selected currencies and their weights, fetching the current exchange rates for calculations.
  - **Current Exchange Rates**: Fetches and displays the current exchange rates for various currencies.

## Known Issues
- Ensure the CSV files contain the required currency data; otherwise, the app may not function as intended.
- Error handling is included for network requests, but users may encounter issues if the API is down or unresponsive.
