//@version=5
strategy("Enhanced 9 & 21 EMA Strategy with Single Entry", overlay=true,
     commission_type=strategy.commission.percent,
     commission_value=0.1,
     slippage=0)

// === Input Parameters ===
// Start and End Dates
start_date = input.time(timestamp("2018-01-01 00:00 +0000"), title="Start Date")
end_date   = input.time(timestamp("2069-12-31 23:59 +0000"), title="End Date")

// EMAs Periods
shortEmaPeriod = input.int(9, title="Short EMA Period", minval=1)
longEmaPeriod  = input.int(21, title="Long EMA Period", minval=1)

// Minimum Bars Between Trades
minBarsBetweenTrades = input.int(5, title="Minimum Bars Between Trades", minval=1)

// === Risk-Reward Parameters ===
// Risk-Reward Ratio: 1:2 (1 point SL, 2 points TP)
riskPoints   = input.int(2, title="Risk (Stop-Loss) in Points", minval=1)
rewardPoints = input.int(4, title="Reward (Take-Profit) in Points", minval=1) // 1:2 ratio

// === Calculate EMAs ===
emaShort = ta.ema(close, shortEmaPeriod)
emaLong  = ta.ema(close, longEmaPeriod)

// Plot EMAs
plot(emaShort, color=color.blue, title="Short EMA")
plot(emaLong, color=color.orange, title="21 EMA")

// === Trade Filters ===
// Cooldown: Ensure minimum bars have passed since the last trade
var int lastTradeBar = na
isCooldown = na(lastTradeBar) or (bar_index - lastTradeBar > minBarsBetweenTrades)

// === Initialize Trade State Variables ===
var bool pendingLong  = false
var bool pendingShort = false

// === Entry Conditions ===
// Long Entry: 9 EMA crosses above 21 EMA
if (ta.crossover(emaShort, emaLong) and
    (time >= start_date and time <= end_date) and
    isCooldown and
    (strategy.position_size == 0))
    pendingLong  := true
    pendingShort := false  // Reset short pending if any

// Short Entry: 9 EMA crosses below 21 EMA
if (ta.crossunder(emaShort, emaLong) and
    (time >= start_date and time <= end_date) and
    isCooldown and
    (strategy.position_size == 0))
    pendingShort := true
    pendingLong  := false  // Reset long pending if any

// === Detect Price Touching the 21 EMA ===
// For Long Entries
if (pendingLong and (low <= emaLong and high >= emaLong))
    // Execute Long Entry
    strategy.entry("Long", strategy.long)
    
    // Calculate Stop-Loss and Take-Profit Prices
    stopLossPriceLong   = close - riskPoints
    takeProfitPriceLong = close + rewardPoints
    
    // Set Exit Orders
    strategy.exit("Exit Long TP/SL", "Long",
                  stop=stopLossPriceLong,
                  limit=takeProfitPriceLong)
    
    // Update Last Trade Bar for Cooldown
    lastTradeBar := bar_index
    
    // Reset Pending Flags
    pendingLong  := false

// For Short Entries
if (pendingShort and (low <= emaLong and high >= emaLong))
    // Execute Short Entry
    strategy.entry("Short", strategy.short)
    
    // Calculate Stop-Loss and Take-Profit Prices
    stopLossPriceShort   = close + riskPoints
    takeProfitPriceShort = close - rewardPoints
    
    // Set Exit Orders
    strategy.exit("Exit Short TP/SL", "Short",
                  stop=stopLossPriceShort,
                  limit=takeProfitPriceShort)
    
    // Update Last Trade Bar for Cooldown
    lastTradeBar := bar_index
    
    // Reset Pending Flags
    pendingShort := false

// === Optional: Plot Trade Signals ===

// Buy (Long) Signal
plotshape(series=pendingLong, 
          location=location.belowbar, 
          color=color.green, 
          style=shape.labelup, 
          title="Buy Signal", 
          text="BUY")

// Sell (Short) Signal
plotshape(series=pendingShort, 
          location=location.abovebar, 
          color=color.red, 
          style=shape.labeldown, 
          title="Sell Signal", 
          text="SELL")

// Take Profit for Long Positions
plotshape(series=(strategy.position_size > 0 and close >= (strategy.position_avg_price + rewardPoints)), 
          location=location.abovebar, 
          color=color.blue, 
          style=shape.labelup, 
          title="Take Profit Long", 
          text="TP")

// Stop Loss for Long Positions
plotshape(series=(strategy.position_size > 0 and close <= (strategy.position_avg_price - riskPoints)), 
          location=location.abovebar, 
          color=color.red, 
          style=shape.labeldown, 
          title="Stop Loss Long", 
          text="SL")

// Take Profit for Short Positions
plotshape(series=(strategy.position_size < 0 and close <= (strategy.position_avg_price - rewardPoints)), 
          location=location.belowbar, 
          color=color.blue, 
          style=shape.labeldown, 
          title="Take Profit Short", 
          text="TP")

// Stop Loss for Short Positions
plotshape(series=(strategy.position_size < 0 and close >= (strategy.position_avg_price + riskPoints)), 
          location=location.belowbar, 
          color=color.red, 
          style=shape.labelup, 
          title="Stop Loss Short", 
          text="SL")
