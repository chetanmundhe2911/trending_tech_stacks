import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Step 1: Load the CSV data
data = pd.read_csv(r'NIFTY 50_minute.csv')

# Step 2: Convert the 'date' column to datetime format
data['date'] = pd.to_datetime(data['date'])

# Step 3: Set the 'date' column as the index
data.set_index('date', inplace=True)

# Step 4: Resample the data to 15-minute intervals
data_resampled = data.resample('15T').agg({'high': 'max', 'low': 'min', 'close': 'last'})

# Step 5: Calculate the returns for each 15-minute period (percentage change in close price)
data_resampled['return'] = data_resampled['close'].pct_change()

# Step 6: Calculate the standard deviation of returns (volatility) for each 15-minute period
data_resampled['volatility'] = data_resampled['return'].rolling(window=2).std()

# Step 7: Drop any rows with NaN values in volatility (which may be at the start due to rolling window)
data_resampled.dropna(subset=['volatility'], inplace=True)

# Step 8: Plot the volatility as a line chart
plt.figure(figsize=(12, 6))
plt.plot(data_resampled.index, data_resampled['volatility'], label='Volatility (Standard Deviation)', color='tab:blue')
plt.title('15-Minute Volatility (Standard Deviation of Returns)')
plt.xlabel('Time')
plt.ylabel('Volatility')
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.legend()
plt.show()
