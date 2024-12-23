import pandas as pd
import numpy as np
import mplfinance as mpf

# Read the data from the Excel file
df = pd.read_excel(r'nifty_50_1day_1min.xlsx')

# Convert date column to datetime format and set as index
df['date'] = pd.to_datetime(df['date'])
df.set_index('date', inplace=True)

# Define a function to calculate trading signals
def apply_strategy(df, stop_loss=10, risk_reward_ratios=[1, 2, 3]):
    df['ema_9'] = df['close'].ewm(span=9, adjust=False).mean()
    total_trades = 0
    winning_trades = 0
    losing_trades = 0
    trade_results = []

    for i in range(1, len(df)):
        if df['close'].iloc[i] < df['ema_9'].iloc[i]:
            if df['low'].iloc[i] < df['low'].iloc[i-1]:
                entry_price = df['close'].iloc[i]
                stop_loss_price = entry_price - stop_loss
                
                for j in range(i + 1, len(df)):
                    if df['low'].iloc[j] <= stop_loss_price:
                        losing_trades += 1
                        trade_results.append(('loss', df.index[i], entry_price, df['close'].iloc[j]))
                        break
                    
                    for rr in range(len(risk_reward_ratios)):
                        if df['high'].iloc[j] >= entry_price + stop_loss * risk_reward_ratios[rr]:
                            winning_trades += 1
                            trade_results.append(('win', df.index[i], entry_price, df['close'].iloc[j]))
                            break
                    if j == len(df) - 1:
                        trade_results.append(('no_exit', df.index[i], entry_price, df['close'].iloc[j]))
    
    total_trades = winning_trades + losing_trades
    return total_trades, winning_trades, losing_trades, trade_results

# Resampling Function
def resample_data(df, freq):
    return df.resample(freq).agg({'open': 'first', 'high': 'max', 'low': 'min', 'close': 'last', 'volume': 'sum'})

# Specify the date and time frames to analyze
specific_date = '2015-01-09'  # Make sure this date exists in your dataset
time_frames = ['1T', '5T', '15T', '1D']  # 1 minute, 5 minutes, 15 minutes, 1 Day

# Analyze and plot results for the specific day at different time frames
for tf in time_frames:
    # Resample the data
    resampled_df = resample_data(df, tf)
    
    # Filter for specific date, keeping only full days in DataFrame
    resampled_df = resampled_df[resampled_df.index.date == pd.to_datetime(specific_date).date()]

    # Apply the trading strategy if the DataFrame is not empty
    if not resampled_df.empty:
        total_trades, winning_trades, losing_trades, trade_results = apply_strategy(resampled_df)
        
        # Prepare for plotting
        # Initialize series for markers
        win_series = pd.Series(index=resampled_df.index, data=np.nan)
        loss_series = pd.Series(index=resampled_df.index, data=np.nan)

        for result in trade_results:
            index_time = result[1]  # Trade time
            if result[0] == 'win' and index_time in resampled_df.index:
                win_series.loc[index_time] = resampled_df['close'].loc[index_time]  # Set winning close price
            elif result[0] == 'loss' and index_time in resampled_df.index:
                loss_series.loc[index_time] = resampled_df['close'].loc[index_time]  # Set losing close price

        # Check that there are markers to plot
        if not win_series.dropna().empty or not loss_series.dropna().empty:
            # Generate a candlestick chart with markers
            apds = []
            if not win_series.dropna().empty:
                apds.append(mpf.make_addplot(win_series, type='scatter', markersize=150, marker='^', color='green', label='Win'))
            if not loss_series.dropna().empty:
                apds.append(mpf.make_addplot(loss_series, type='scatter', markersize=150, marker='v', color='red', label='Loss'))

            # Plot the candlestick chart with trade signals
            mpf.plot(resampled_df, type='candle', addplot=apds, 
                     title=f'Trading Strategy Results on {specific_date} at {tf} Time Frame', volume=False,
                     style='yahoo', figsize=(10, 6))
        else:
            print(f"No trades available to plot for {specific_date} at {tf} time frame.")
    else:
        print(f"No data available for {specific_date} at {tf} time frame.")
