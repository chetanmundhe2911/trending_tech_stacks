import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# Load the data
file_path = r'C:\Users\cheta\Downloads\options_data\nifty_data\nifty_options\2024\10\nifty_options_03_10_2024.csv'

# Extract the date from the filename and derive the day of the week
file_name = file_path.split('\\')[-1]  # Get the file name
date_str = file_name.split('_')[2:5]  # Extract date parts from the file name
date_str = '_'.join(date_str).replace('.csv', '')
file_date = datetime.strptime(date_str, '%d_%m_%Y')
day_of_week = file_date.strftime('%A')  # Get day of the week (Monday, Tuesday, etc.)

# Load and process data
df = pd.read_csv(file_path)

# Convert 'date' and 'time' columns into a datetime object
df['datetime'] = pd.to_datetime(df['date'] + ' ' + df['time'], format='%Y-%m-%d %H:%M:%S')

# Set 'datetime' as the index
df.set_index('datetime', inplace=True)

# Calculate 9-period EMA and 21-period EMA for the 'close' column
df['9ema'] = df['close'].ewm(span=9, adjust=False).mean()
df['21ema'] = df['close'].ewm(span=21, adjust=False).mean()

# Resample the data to 5-minute intervals
resampled = df.resample('5T').agg({'close': 'last', '9ema': 'last', '21ema': 'last'})

# Create 'below' and 'above' columns for 9EMA
resampled['below_9ema'] = np.where(resampled['close'] < resampled['9ema'], 1, 0)
resampled['above_9ema'] = np.where(resampled['close'] > resampled['9ema'], 1, 0)

# Calculate the percentage of time the close was below or above the 9 EMA
below_percentage = resampled['below_9ema'].mean() * 100
above_percentage = resampled['above_9ema'].mean() * 100

# Calculate total time price was below and above 9EMA (in minutes)
time_below_9ema = (resampled['below_9ema']).sum() * 5  # Multiply by 5 because of 5-minute intervals
time_above_9ema = (resampled['above_9ema']).sum() * 5  # Multiply by 5 because of 5-minute intervals

# Calculate metrics (Highest, Lowest, and Average Close Price)
highest_close = resampled['close'].max()
lowest_close = resampled['close'].min()
average_close = resampled['close'].mean()

# ---------------- Average Standard Deviation Calculation ----------------
# Above 9 EMA
above_9ema_std = resampled[resampled['above_9ema'] == 1]['close'].std()

# Below 9 EMA
below_9ema_std = resampled[resampled['below_9ema'] == 1]['close'].std()

# Above 21 EMA
above_21ema_std = resampled[resampled['close'] > resampled['21ema']]['close'].std()

# Below 21 EMA
below_21ema_std = resampled[resampled['close'] < resampled['21ema']]['close'].std()

# Print the results
print(f"Date: {file_date.strftime('%d-%m-%Y')} ({day_of_week})")
print(f"Average Standard Deviation (Above 9 EMA): {above_9ema_std:.2f}")
print(f"Average Standard Deviation (Below 9 EMA): {below_9ema_std:.2f}")
print(f"Average Standard Deviation (Above 21 EMA): {above_21ema_std:.2f}")
print(f"Average Standard Deviation (Below 21 EMA): {below_21ema_std:.2f}")

# ---------------- Create Line Plot ----------------
plt.figure(figsize=(14, 7))

# Plot close price (Black)
# plt.plot(resampled.index, resampled['close'], label='Close Price', color='black', linewidth=1.5)

# Plot 9 EMA (Green)
plt.plot(resampled.index, resampled['9ema'], label='9 EMA', color='green', linestyle='--', linewidth=1.5)

# Plot 21 EMA (Blue)
plt.plot(resampled.index, resampled['21ema'], label='21 EMA', color='blue', linestyle='--', linewidth=1.5)

# Add shading for bullish and bearish regions
plt.fill_between(resampled.index,
                 resampled['close'],
                 resampled['9ema'],
                 where=(resampled['9ema'] > resampled['21ema']),
                 color='green',
                 alpha=0.1,
                 label='Bullish Region (9EMA > 21EMA)')
plt.fill_between(resampled.index,
                 resampled['close'],
                 resampled['9ema'],
                 where=(resampled['9ema'] < resampled['21ema']),
                 color='red',
                 alpha=0.1,
                 label='Bearish Region (9EMA < 21EMA)')

# Add labels, legend, and title
plt.xlabel('Time', fontsize=12)
plt.ylabel('Price', fontsize=12)
plt.title(f"Price with 9 EMA and 21 EMA\n{file_date.strftime('%d-%m-%Y')} ({day_of_week})", fontsize=14)
plt.legend(loc='best', fontsize=11)
plt.grid(True)

# Add percentage, time, and standard deviation information as text on the plot
summary_text = (f"Date: {file_date.strftime('%d-%m-%Y')} ({day_of_week})\n"
                f"Avg Std Dev (Above 9 EMA): {above_9ema_std:.2f}\n"
                f"Avg Std Dev (Below 9 EMA): {below_9ema_std:.2f}\n"
                f"Avg Std Dev (Above 21 EMA): {above_21ema_std:.2f}\n"
                f"Avg Std Dev (Below 21 EMA): {below_21ema_std:.2f}\n"
                f"Highest Close Price: {highest_close:.2f}\n"
                f"Lowest Close Price: {lowest_close:.2f}\n"
                f"Average Close Price: {average_close:.2f}\n"
                f"Percentage Below 9 EMA: {below_percentage:.2f}%\n"
                f"Percentage Above 9 EMA: {above_percentage:.2f}%")

plt.text(
    x=resampled.index[0],  # Place text at the start of the plot
    y=max(resampled['close']),  # Position at the top, based on max close price
    s=summary_text,
    fontsize=12,
    color='black',
    bbox=dict(facecolor='white', alpha=0.8, edgecolor='black')  # Background box for visibility
)

# Show the plot
plt.tight_layout()
plt.show()
