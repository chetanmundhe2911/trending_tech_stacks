
#pip install mplfinance

### This on this

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load Data
data = pd.read_csv(r"C:\Users\cheta\OneDrive\Chetan\Destiny\archive\NIFTY 50_minute.csv")
data['date'] = pd.to_datetime(data['date'])  # Ensure 'date' is in datetime format
data.set_index('date', inplace=True)

# Calculate EMA
data['9EMA'] = data['close'].ewm(span=9, adjust=False).mean()
data['21EMA'] = data['close'].ewm(span=21, adjust=False).mean()

# Parameters
rr_ratios = [1, 2]  # Risk-reward ratios to test
threshold_9ema = 0.10  # Threshold for 9 EMA re-entry
threshold_21ema = 0.10  # Threshold for 21 EMA re-entry
max_trades_per_day = 3

results = []

# Strategy Function
def strategy(data, rr, threshold_9, threshold_21):
    data = data.copy()
    data['signal'] = 0  # Signal column: 1 for buy, -1 for sell
    data['target'] = 0  # Target price for trade
    data['stop_loss'] = 0  # Stop loss for trade

    trades = []
    daily_trade_count = {}

    for i in range(1, len(data)):
        today = data.index[i].date()

        # Limit trades per day
        if daily_trade_count.get(today, 0) >= max_trades_per_day:
            continue

        # Crossover signal
        if data['9EMA'].iloc[i] > data['21EMA'].iloc[i] and data['9EMA'].iloc[i - 1] <= data['21EMA'].iloc[i - 1]:
            sl = data['low'].iloc[i - 1]
            entry = data['close'].iloc[i]
            target = entry + rr * (entry - sl)

            data.loc[data.index[i], 'signal'] = 1
            data.loc[data.index[i], 'stop_loss'] = sl
            data.loc[data.index[i], 'target'] = target

        elif data['9EMA'].iloc[i] < data['21EMA'].iloc[i] and data['9EMA'].iloc[i - 1] >= data['21EMA'].iloc[i - 1]:
            sl = data['high'].iloc[i - 1]
            entry = data['close'].iloc[i]
            target = entry - rr * (sl - entry)

            data.loc[data.index[i], 'signal'] = -1
            data.loc[data.index[i], 'stop_loss'] = sl
            data.loc[data.index[i], 'target'] = target

        # Re-entry conditions
        if data['signal'].iloc[i] == 0:
            price = data['close'].iloc[i]
            
            if abs(price - data['21EMA'].iloc[i]) / data['21EMA'].iloc[i] <= threshold_21:
                data.loc[data.index[i], 'signal'] = data['signal'].iloc[i - 1]

            elif abs(price - data['9EMA'].iloc[i]) / data['9EMA'].iloc[i] <= threshold_9:
                data.loc[data.index[i], 'signal'] = data['signal'].iloc[i - 1]

        if data['signal'].iloc[i] != 0:
            daily_trade_count[today] = daily_trade_count.get(today, 0) + 1

            trades.append({
                'entry_time': data.index[i],
                'entry_price': data['close'].iloc[i],
                'stop_loss': data['stop_loss'].iloc[i],
                'target': data['target'].iloc[i],
                'signal': data['signal'].iloc[i]
            })

    return data, trades



for rr in rr_ratios:
    for tf in ["1T", "5T", "15T", "1H", "1D"]:  # Different timeframes
        resampled_data = data.resample(tf).agg({
            'open': 'first',
            'high': 'max',
            'low': 'min',
            'close': 'last'
        }).dropna()
        
        # Recalculate EMAs for the resampled data
        resampled_data['9EMA'] = resampled_data['close'].ewm(span=9, adjust=False).mean()
        resampled_data['21EMA'] = resampled_data['close'].ewm(span=21, adjust=False).mean()

        analyzed_data, trades = strategy(resampled_data, rr, threshold_9ema, threshold_21ema)

        # Descriptive Stats
        total_trades = len(trades)
        winning_trades = sum(1 for t in trades if (t['signal'] == 1 and t['target'] <= t['entry_price']) or \
                                                  (t['signal'] == -1 and t['target'] >= t['entry_price']))
        losing_trades = total_trades - winning_trades

        results.append({
            'timeframe': tf,
            'rr_ratio': rr,
            'total_trades': total_trades,
            'winning_trades': winning_trades,
            'losing_trades': losing_trades
        })

        print(f"Timeframe: {tf}, RR: {rr}")
        print(f"Total Trades: {total_trades}, Wins: {winning_trades}, Losses: {losing_trades}\\n")


# Export Results
results_df = pd.DataFrame(results)
results_df.to_csv("strategy_analysis_results.csv", index=False)
print("Results exported to strategy_analysis_results.csv")
