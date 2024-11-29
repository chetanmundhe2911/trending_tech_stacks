import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

# Define the ticker and timeframe
ticker = "^NSEI"  # NIFTY 50 symbol
interval = "5m"   # 5-minute interval
end_date = datetime.now()  # Current date and time
start_date = end_date - timedelta(days=60)  # 60 days ago

# Download the data
data = yf.download(ticker, start=start_date, end=end_date, interval=interval)

# Calculate the 9 EMA and 21 EMA
data['9 EMA'] = data['Close'].ewm(span=9, adjust=False).mean()
data['21 EMA'] = data['Close'].ewm(span=21, adjust=False).mean()

# Add day and date columns
data['Day'] = data.index.day_name()
data['Date'] = data.index.date

# Reorder columns for better readability
data = data[['Date', 'Day', 'Open', 'High', 'Low', 'Close', 'Volume', '9 EMA', '21 EMA']]

# Save the data to a CSV file
data.to_csv("nifty_50_5min_last_60_days_with_ema.csv")

print("Data download completed and saved to 'nifty_50_5min_last_60_days_with_ema.csv'")
