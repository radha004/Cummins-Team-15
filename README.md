This dashboard is designed for analyzing historical exchange rates between the U.S. dollar (USD) and other currencies from 2012 onwards. It provides features such as frequency-based trend analysis, custom currency basket creation, risk indicators, and future exchange rate predictions using ARIMA. The dashboard is built using Streamlit for the frontend, Pandas for data handling, and Plotly for visualizations.

Features:

Currency Exchange Rate Visualization:

Annual, Monthly, Weekly, and Quarterly Data Views: The user can choose from different time frequencies and a specific year to analyze exchange rate trends.
Interactive Plotly Graph: Visualizes the exchange rate trends with dynamic tooltips and a filled line chart.
Custom Currency Basket:

Allows users to select multiple currencies and assign custom weights to each. The dashboard calculates a weighted average exchange rate for the basket in comparison to a base currency.
Currency Weighting: The user can define the weight of each currency in the basket and calculate the basket rate based on current exchange rates.
Risk Indicator (Volatility Analysis):

Users can select two currencies to compare their historical volatility. The dashboard computes standard deviation and classifies volatility into low, medium, or high.
Visual Representation: Displays a bar chart comparing the volatilities of the selected currencies.
ARIMA-based Exchange Rate Prediction:

Historical data from 2012-2022 is used to predict exchange rates for 2023 using an ARIMA (AutoRegressive Integrated Moving Average) model.
Dummy Data Creation for 2023: Generates dummy data for the entire year of 2023 based on predictions, saved as a CSV file.
Current Exchange Rates:

Fetches real-time exchange rates using an API and allows users to view the latest rates for a selected currency.
