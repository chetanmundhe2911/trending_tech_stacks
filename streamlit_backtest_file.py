import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import numpy as np

# Load CSV data
def load_data(file):
    df = pd.read_csv(file)
    # Ensure the 'timestamp' column exists and convert it to datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.set_index('timestamp')
    return df

# Function to resample data to desired timeframe
def resample_data(df, timeframe):
    if timeframe == '5min':
        return df.resample('5T').agg({'open': 'first', 'high': 'max', 'low': 'min', 'close': 'last', 'volume': 'sum'})
    return df

# Create Candlestick Chart
def plot_candlestick(df):
    fig = go.Figure(data=[go.Candlestick(x=df.index,
                                        open=df['open'], high=df['high'],
                                        low=df['low'], close=df['close'],
                                        name='OHLC')])
    fig.update_layout(title="Nifty50 Candlestick Chart",
                      xaxis_rangeslider_visible=False,
                      xaxis_title="Time",
                      yaxis_title="Price",
                      template="plotly_dark")
    return fig

# Trade logic for buy/sell actions
def trade_action(df, action, stoploss, entry_price, trade_history):
    trade = {}
    trade['action'] = action
    trade['entry_price'] = entry_price
    trade['stoploss'] = stoploss
    trade['timestamp'] = df.index[-1]
    trade['exit_price'] = None
    trade['exit_timestamp'] = None
    trade_history.append(trade)
    return trade_history

# Record trade history
def display_trade_history(trade_history):
    if trade_history:
        history_df = pd.DataFrame(trade_history)
        st.write("Trade History", history_df)
    else:
        st.write("No trades executed yet.")

# Streamlit App UI
def main():
    st.title('Nifty50 Backtesting App')

    # File Upload
    uploaded_file = st.file_uploader("Upload OHLCV CSV Data", type=["csv"])
    
    if uploaded_file is not None:
        df = load_data(uploaded_file)

        # Display Data Table
        st.subheader('OHLCV Data')
        st.dataframe(df)

        # Select Timeframe
        timeframe = st.selectbox("Select Timeframe", ['1min', '5min'])
        resampled_df = resample_data(df, timeframe)
        
        # Plot Candlestick Chart
        st.subheader(f'Candlestick Chart ({timeframe})')
        fig = plot_candlestick(resampled_df)
        st.plotly_chart(fig)

        # Trading Actions
        st.subheader('Simulate Trades')

        # Trade History
        trade_history = []

        # Buy and Sell Buttons
        buy_button = st.button('Buy')
        if buy_button:
            entry_price = resampled_df['close'][-1]  # last close price
            stoploss = st.number_input('Enter Stoploss (%)', min_value=0.0, max_value=10.0, value=1.0)
            trade_history = trade_action(resampled_df, 'Buy', stoploss, entry_price, trade_history)
            st.success(f'Bought at {entry_price} with stoploss at {entry_price * (1 - stoploss / 100)}')

        sell_button = st.button('Sell')
        if sell_button:
            entry_price = resampled_df['close'][-1]
            stoploss = st.number_input('Enter Stoploss (%)', min_value=0.0, max_value=10.0, value=1.0)
            trade_history = trade_action(resampled_df, 'Sell', stoploss, entry_price, trade_history)
            st.success(f'Sold at {entry_price} with stoploss at {entry_price * (1 + stoploss / 100)}')

        # Display Trade History
        display_trade_history(trade_history)

if __name__ == '__main__':
    main()
