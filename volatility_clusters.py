import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Step 1: Load the CSV data
data = pd.read_csv(r'C:\Users\cheta\OneDrive\Chetan\Destiny\archive\NIFTY 50_minute.csv')

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

# Step 8: Define a threshold for high volatility based on the mean and standard deviation of volatility
mean_volatility = data_resampled['volatility'].mean()
std_volatility = data_resampled['volatility'].std()

# High volatility is defined as when the volatility is greater than the mean + 1 standard deviation
high_volatility_threshold = mean_volatility + std_volatility

# Step 9: Detect volatility clusters (periods of high volatility)
data_resampled['high_volatility'] = data_resampled['volatility'] > high_volatility_threshold

# Step 10: Identify clusters of high volatility
data_resampled['volatility_cluster'] = (data_resampled['high_volatility'] != data_resampled['high_volatility'].shift()).cumsum()

# Step 11: Filter and display the periods where volatility clusters occurred
volatility_clusters = data_resampled[data_resampled['high_volatility']].groupby('volatility_cluster').agg({'volatility': 'mean', 'high_volatility': 'sum'})

# Step 12: Print the clusters
print(volatility_clusters)

# Step 13: Plot the volatility and the high volatility periods to visualize the clusters
plt.figure(figsize=(12, 6))
plt.plot(data_resampled.index, data_resampled['volatility'], label='Volatility', color='tab:blue')
plt.fill_between(data_resampled.index, 0, data_resampled['volatility'], where=data_resampled['high_volatility'], color='tab:red', alpha=0.3, label='High Volatility Cluster')
plt.title('Volatility with Detected High Volatility Clusters')
plt.xlabel('Time')
plt.ylabel('Volatility')
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.legend()
plt.show()
