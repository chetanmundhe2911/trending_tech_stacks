import pandas as pd
import numpy as np

# Load the CSV file (adjust the path as per your system)
file_path = r'C:\Users\cheta\OneDrive\Chetan\Destiny\archive\NIFTY 50_minute.csv'
df = pd.read_csv(file_path)

# Convert the 'date' column to datetime with the correct format
df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d %H:%M:%S')

# Set 'date' as the index
df.set_index('date', inplace=True)

# Function to calculate Exponential Moving Average (EMA) using numpy
def calculate_ema(prices, period):
    alpha = 2 / (period + 1)
    ema = [prices[0]]  # Start with the first value as the first EMA
    for price in prices[1:]:
        ema.append((price * alpha) + (ema[-1] * (1 - alpha)))
    return np.array(ema)

# Function to calculate 9x21 EMA Crossover
def ema_crossover(df, short_period=9, long_period=21):
    # Calculate EMAs using the custom numpy function
    df['EMA9'] = calculate_ema(df['close'].values, short_period)
    df['EMA21'] = calculate_ema(df['close'].values, long_period)
    
    # Generate signals (1 for buy, -1 for sell, 0 for no signal) using .loc to avoid SettingWithCopyWarning
    df['Signal'] = 0
    df.loc[df['EMA9'] > df['EMA21'], 'Signal'] = 1   # Bullish crossover (Buy signal)
    df.loc[df['EMA9'] < df['EMA21'], 'Signal'] = -1  # Bearish crossover (Sell signal)
    
    return df

# Function to calculate backtest performance metrics
def backtest(df):
    # Create a column for strategy returns (Signal-based)
    # Use fill_method=None in pct_change to avoid FutureWarning
    df['Strategy Returns'] = df['Signal'].shift(1) * df['close'].pct_change(fill_method=None)

    # Drop NaN values
    df.dropna(subset=['Strategy Returns'], inplace=True)

    # Performance Metrics
    win_rate = len(df[df['Strategy Returns'] > 0]) / len(df)
    
    # Add a check to avoid division by zero
    positive_returns = df[df['Strategy Returns'] > 0]['Strategy Returns'].sum()
    negative_returns = abs(df[df['Strategy Returns'] < 0]['Strategy Returns'].sum())
    
    if negative_returns == 0:
        profit_factor = np.nan  # Handle edge case gracefully
    else:
        profit_factor = positive_returns / negative_returns
    
    total_return = df['Strategy Returns'].sum()
    max_drawdown = (df['close'] / df['close'].cummax() - 1).min()
    
    return win_rate, profit_factor, total_return, max_drawdown

# Apply the crossover function
df = ema_crossover(df)

# Perform backtest on the original timeframe
win_rate, profit_factor, total_return, max_drawdown = backtest(df)

# Print results for the original timeframe
print(f"Original Timeframe (Minute-level): Win Rate = {win_rate:.2f}, Profit Factor = {profit_factor:.2f}, Total Return = {total_return:.2f}, Max Drawdown = {max_drawdown:.2f}")

# Resample to 5-minute data (if your data is more granular)
df_5min = df.resample('5T').agg({'open': 'first', 'high': 'max', 'low': 'min', 'close': 'last', 'volume': 'sum'})
df_5min = ema_crossover(df_5min)

# Backtest on the 5-minute data
win_rate_5min, profit_factor_5min, total_return_5min, max_drawdown_5min = backtest(df_5min)
print(f"5-Minute Timeframe: Win Rate = {win_rate_5min:.2f}, Profit Factor = {profit_factor_5min:.2f}, Total Return = {total_return_5min:.2f}, Max Drawdown = {max_drawdown_5min:.2f}")

# Resample to 15-minute data
df_15min = df.resample('15T').agg({'open': 'first', 'high': 'max', 'low': 'min', 'close': 'last', 'volume': 'sum'})
df_15min = ema_crossover(df_15min)

# Backtest on the 15-minute data
win_rate_15min, profit_factor_15min, total_return_15min, max_drawdown_15min = backtest(df_15min)
print(f"15-Minute Timeframe: Win Rate = {win_rate_15min:.2f}, Profit Factor = {profit_factor_15min:.2f}, Total Return = {total_return_15min:.2f}, Max Drawdown = {max_drawdown_15min:.2f}")

# Resample to 1-day data
df_daily = df.resample('D').agg({'open': 'first', 'high': 'max', 'low': 'min', 'close': 'last', 'volume': 'sum'})
df_daily = ema_crossover(df_daily)

# Backtest on the 1-day data
win_rate_daily, profit_factor_daily, total_return_daily, max_drawdown_daily = backtest(df_daily)
print(f"1-Day Timeframe: Win Rate = {win_rate_daily:.2f}, Profit Factor = {profit_factor_daily:.2f}, Total Return = {total_return_daily:.2f}, Max Drawdown = {max_drawdown_daily:.2f}")
