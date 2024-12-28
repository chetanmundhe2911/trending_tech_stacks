//@version=5
strategy("Enhanced 9 & 21 EMA Strategy with Trade Filters and 1:2 Risk-Reward", overlay=true,
     commission_type=strategy.commission.percent, commission_value=0.1, slippage=0)

// === Input Parameters ===
// Start and End Dates
start_date = input.time(timestamp("2018-01-01 00:00 +0000"), title="Start Date")
end_date = input.time(timestamp("2069-12-31 23:59 +0000"), title="End Date")

// EMAs Periods
shortEmaPeriod = input.int(9, title="Short EMA Period")
longEmaPeriod  = input.int(21, title="Long EMA Period")

// Minimum Bars Between Trades
minBarsBetweenTrades = input.int(5, title="Minimum Bars Between Trades", minval=1)

// === Risk-Reward Parameters ===
// Risk-Reward Ratio: 1:2 (1 point SL, 2 points TP)
riskPoints = input.int(2, title="Risk (Stop-Loss) in Points", minval=1)
rewardPoints = input.int(2, title="Reward (Take-Profit) in Points", minval=1)

// === Calculate EMAs ===
emaShort = ta.ema(close, shortEmaPeriod)
emaLong  = ta.ema(close, longEmaPeriod)

// Plot EMAs with Fixed Titles
plot(emaShort, color=color.blue, title="Short EMA")
plot(emaLong, color=color.orange, title="Long EMA")

// === Trade Filters ===
// Cooldown: Check if the minimum number of bars have passed since the last trade
var int lastTradeBar = na
cooldown = na(lastTradeBar) or (bar_index - lastTradeBar > minBarsBetweenTrades)

// === Initialize Take-Profit and Stop-Loss Prices ===
// For Long Positions
var float takeProfitPriceLong = na
var float stopLossPriceLong = na

// For Short Positions
var float takeProfitPriceShort = na
var float stopLossPriceShort = na

// === Initialize Flags for Crossover and Touch Events ===
var bool longCrossoverActive = false
var bool longTouchActive = false
var bool shortCrossoverActive = false
var bool shortTouchActive = false

// === Entry Conditions ===

// Long Entry: 9 EMA crosses above 21 EMA
if ta.crossover(emaShort, emaLong) and (time >= start_date and time <= end_date) and cooldown
    longCrossoverActive := true

// Short Entry: 9 EMA crosses below 21 EMA
if ta.crossunder(emaShort, emaLong) and (time >= start_date and time <= end_date) and cooldown
    shortCrossoverActive := true

// === Detect Price Touching the 21 EMA ===

// For Long Entries
if longCrossoverActive and (low <= emaLong and high >= emaLong)
    longTouchActive := true
    longCrossoverActive := false

// For Short Entries
if shortCrossoverActive and (low <= emaLong and high >= emaLong)
    shortTouchActive := true
    shortCrossoverActive := false

// === Execute Entries After Conditions are Met ===

// Execute Long Entry
if longTouchActive and close > close[1]
    // Calculate Stop-Loss and Take-Profit Prices
    stopLossPriceLong := close - riskPoints
    takeProfitPriceLong := close + rewardPoints
    
    // Enter Long Position
    strategy.entry("Long", strategy.long)
    
    // Set Exit Orders
    strategy.exit("Exit Long TP/SL", "Long", stop=stopLossPriceLong, limit=takeProfitPriceLong)
    
    // Update Last Trade Bar for Cooldown
    lastTradeBar := bar_index
    
    // Reset Flags
    longTouchActive := false

// Execute Short Entry
if shortTouchActive and close < close[1]
    // Calculate Stop-Loss and Take-Profit Prices
    stopLossPriceShort := close + riskPoints
    takeProfitPriceShort := close - rewardPoints
    
    // Enter Short Position
    strategy.entry("Short", strategy.short)
    
    // Set Exit Orders
    strategy.exit("Exit Short TP/SL", "Short", stop=stopLossPriceShort, limit=takeProfitPriceShort)
    
    // Update Last Trade Bar for Cooldown
    lastTradeBar := bar_index
    
    // Reset Flags
    shortTouchActive := false

// === Reset Take-Profit and Stop-Loss Prices When No Relevant Position ===
if (strategy.position_size == 0)
    // Reset Long Positions
    takeProfitPriceLong := na
    stopLossPriceLong := na
    
    // Reset Short Positions
    takeProfitPriceShort := na
    stopLossPriceShort := na

// === Optional: Plot Trade Signals ===

// Buy (Long) Signal
plotshape(series=longCrossoverActive, 
          location=location.belowbar, 
          color=color.green, 
          style=shape.labelup, 
          title="Buy Signal", 
          text="BUY")

// Sell (Short) Signal
plotshape(series=shortCrossoverActive, 
          location=location.abovebar, 
          color=color.red, 
          style=shape.labeldown, 
          title="Sell Signal", 
          text="SELL")

// Take Profit for Long Positions
plotshape(series=(strategy.position_size > 0 and close >= takeProfitPriceLong), 
          location=location.abovebar, 
          color=color.blue, 
          style=shape.labelup, 
          title="Take Profit Long", 
          text="TP")

// Stop Loss for Long Positions
plotshape(series=(strategy.position_size > 0 and close <= stopLossPriceLong), 
          location=location.abovebar, 
          color=color.red, 
          style=shape.labeldown, 
          title="Stop Loss Long", 
          text="SL")

// Take Profit for Short Positions
plotshape(series=(strategy.position_size < 0 and close <= takeProfitPriceShort), 
          location=location.belowbar, 
          color=color.blue, 
          style=shape.labeldown, 
          title="Take Profit Short", 
          text="TP")

// Stop Loss for Short Positions
plotshape(series=(strategy.position_size < 0 and close >= stopLossPriceShort), 
          location=location.belowbar, 
          color=color.red, 
          style=shape.labelup, 
          title="Stop Loss Short", 
          text="SL")
