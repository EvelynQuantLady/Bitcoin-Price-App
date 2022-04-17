# This app is for educational purpose only. Insights gained is not financial advice. Use at your own risk!
import streamlit as st
from PIL import Image
import pandas as pd
import base64
from plotly import graph_objs as go
from bs4 import BeautifulSoup
import requests
import json
import time

# ---------------------------------#
# New feature (make sure to upgrade your streamlit library)
# pip install --upgrade streamlit

# ---------------------------------#
# Page layout
# Page expands to full width
st.set_page_config(layout="wide")
# ---------------------------------#
# Title

st.title("Bitcoin Prices")
st.markdown(
    """
This app retrieves bitcoin prices for the selected days from the **Coingecko**!

"""
)
# ---------------------------------#
# About
expander_bar = st.expander("About")
expander_bar.markdown(
    """
* **Python libraries:** base64, pandas, streamlit, numpy, plotly, requests
* **Data source:** [Coingecko](https://www.coingecko.com/.
"""
)


# ---------------------------------#
# Page layout (continued)
# Divide page to 3 columns (col1 = sidebar, col2 and col3 = page contents)
col1 = st.sidebar
col2, col3 = st.columns((2, 1))

# ---------------------------------#
# Sidebar + Main panel
col1.header("Input Options")

# Sidebar - Currency price unit
currency_price_unit = col1.radio("Select currency for price", ("USD", "CAD", "INR"))
no_of_days = col1.slider("No. of Days", 1, 365, 1)
#vs_currency=cad
#days=90
#interva%20l=daily

# data loading
def load_data():
    API_URL = 'https://api.coingecko.com/api/v3/coins/bitcoin/market_chart'
    payload = {'days': no_of_days, 'vs_currency': currency_price_unit, 'interva%20l': 'daily'}
    req = requests.get(API_URL, payload)
    if req.status_code == 200:
        data = req.json()
    #data
    #raw_data = data['market_caps']
    raw_data2 = data['prices']
    #raw_data
    df = pd.DataFrame(data=raw_data2)
    df.columns =['Date', 'Price']
    df['Date'] = pd.to_datetime(df['Date'], unit='ms')
    
    df.head()
    #df2.head()
    #raw_data = data['dataset']['data']
    #raw_data = data['market_caps']['prices']['total_volumes']
    #df = pd.DataFrame(data=raw_data, columns=data['dataset']['column_names'])
    #df.plot.line(x='Date', y='Close')  
    return df

# Plot raw data
def plot_raw_data():
	fig = go.Figure()
	fig.add_trace(go.Scatter(x=df['Date'], y=df['Price'], name="stock_open"))
	fig.layout.update(title_text='Time Series data with Rangeslider', xaxis_rangeslider_visible=True)
	st.plotly_chart(fig)

df = load_data()

# ---------------------------------#
# Preparing data for Bar plot of Price change
col2.subheader("Bar Plot of Price for the selected days")
plot_raw_data()

#Average Value
col3.header("Insights")
col3.subheader("Average Price during this time was "+ str(df["Price"].mean())+ " "+ currency_price_unit)
