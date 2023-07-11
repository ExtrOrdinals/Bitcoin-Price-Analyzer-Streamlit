import openai
import requests
import json
import datetime
import streamlit as st
import matplotlib.pyplot as plt

openai.api_key = st.secrets["OPENAI_API_KEY"]
def get_bitcoin_data():
    url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=usd&days=7"
    response = requests.get(url)
    data = response.json()

    # Convert prices, market_caps, and total_volumes to integers
    for field in ['prices', 'market_caps', 'total_volumes']:
        for i in range(len(data[field])):
            data[field][i][1] = int(data[field][i][1])

    return data

def analyze_bitcoin_data(data):
    prompt = f"""
    You are an expert crypto trader with more than 10 years of experience. Here is the Bitcoin data for the last 7 days: 
    {data} 
    Please provide a detailed technical analysis of Bitcoin based on this data. Include information on price overview, moving averages, relative strength index (RSI), moving average convergence divergence (MACD), and advice and suggestions. Even if you don't have enough info for the anser, get as close as possible. Should we buy or sell? Please explain in a way that a beginner can understand.
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message['content']

def plot_bitcoin_data(data):
    # Separate timestamps and prices
    timestamps = [item[0] for item in data['prices']]
    prices = [item[1] for item in data['prices']]

    # Convert timestamps to datetime objects
    dates = [datetime.datetime.fromtimestamp(ts / 1000) for ts in timestamps]

    fig, ax = plt.subplots(figsize=(10,5))
    ax.plot(dates, prices, label='Price')  # Use dates for x values and prices for y values
    ax.legend()
    ax.set_title('Bitcoin Data for the Last 7 Days')
    ax.set_xlabel('Time')
    ax.set_ylabel('Price')
    ax.grid(True)
    st.pyplot(fig)


st.title('Bitcoin Price Analyzer')
st.write('This app uses AI to analyze Bitcoin prices and other metrics.')


if st.button('Analyze'):
    with st.spinner('Getting Bitcoin data...'):
        data = get_bitcoin_data()
        st.success('Done!')
        #st.write('Raw Data: ' + json.dumps(data))
    with st.spinner('Analyzing Bitcoin data...'):
        analysis = analyze_bitcoin_data(data)
        st.text_area('Analysis', analysis, height=500)
        st.success('Done!')
    with st.spinner('Plotting Bitcoin data...'):
        plot_bitcoin_data(data)
        st.success('Done!')
