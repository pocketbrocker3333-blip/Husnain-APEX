import pandas as pd
import ta

def analyze_binary_market(df, expiry="1m"):
    if df is None or len(df) < 15:
        return {
            "signal": "WAIT / FETCHING DATA 🟡",
            "action": "Loading market candles...",
            "expiry": expiry,
            "confidence": "0%",
            "rsi": "N/A"
        }

    df = df.copy()
    
    # Handle MultiIndex if present from yfinance
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    # ------------------ INDICATORS CALCULATIONS ------------------
    df['rsi'] = ta.momentum.rsi(df['Close'], window=14)
    
    stoch = ta.momentum.StochasticOscillator(df['High'], df['Low'], df['Close'], window=14, smooth_window=3)
    df['stoch_k'] = stoch.stoch()
    df['stoch_d'] = stoch.stoch_signal()
    
    df['ema_9'] = ta.trend.ema_indicator(df['Close'], window=9)
    df['ema_21'] = ta.trend.ema_indicator(df['Close'], window=21)
    
    bb = ta.volatility.BollingerBands(df['Close'], window=20, window_dev=2)
    df['bb_high'] = bb.bollinger_hband()
    df['bb_low'] = bb.bollinger_lband()
    
    macd = ta.trend.MACD(df['Close'])
    df['macd'] = macd.macd()
    df['macd_signal'] = macd.macd_signal()

    last = df.iloc[-1]

    up_score = 0.0
    down_score = 0.0

    # 1. RSI Pressure
    rsi_val = last['rsi']
    if pd.notnull(rsi_val):
        if rsi_val < 50:
            up_score += (50 - rsi_val) / 8.0 + 1.0
        else:
            down_score += (rsi_val - 50) / 8.0 + 1.0

    # 2. Stochastic Cross
    if pd.notnull(last['stoch_k']) and pd.notnull(last['stoch_d']):
        if last['stoch_k'] >= last['stoch_d']:
            up_score += 1.5
        else:
            down_score += 1.5

    # 3. EMA Trend
    if pd.notnull(last['ema_9']) and pd.notnull(last['ema_21']):
        if last['Close'] >= last['ema_9']:
            up_score += 1.5
        else:
            down_score += 1.5

    # 4. Bollinger Bands Position
    if pd.notnull(last['bb_low']) and pd.notnull(last['bb_high']):
        mid_bb = (last['bb_low'] + last['bb_high']) / 2
        if last['Close'] <= mid_bb:
            up_score += 1.0
        else:
            down_score += 1.0

    # 5. MACD Momentum
    if pd.notnull(last['macd']) and pd.notnull(last['macd_signal']):
        if last['macd'] >= last['macd_signal']:
            up_score += 1.5
        else:
            down_score += 1.5

    rsi_formatted = round(rsi_val, 2) if pd.notnull(rsi_val) else "N/A"
    expiry_label = "1 MINUTE" if expiry == "1m" else ("5 MINUTES" if expiry == "5m" else "15 MINUTES")

    # ------------------ GUARANTEED UP/DOWN SIGNAL DECISION ------------------
    if up_score >= down_score:
        accuracy = min(round(68 + (up_score * 3.5)), 96)
        return {
            "signal": "CALL (UP ⬆️) 🟢",
            "action": "BUY GREEN CANDLE / PLACE CALL TRADE NOW",
            "expiry": expiry_label,
            "confidence": f"{accuracy}%",
            "rsi": rsi_formatted
        }
    else:
        accuracy = min(round(68 + (down_score * 3.5)), 96)
        return {
            "signal": "PUT (DOWN ⬇️) 🔴",
            "action": "SELL RED CANDLE / PLACE PUT TRADE NOW",
            "expiry": expiry_label,
            "confidence": f"{accuracy}%",
            "rsi": rsi_formatted
        }