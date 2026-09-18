import pandas as pd
import ta

def analyze_binary_market(df, expiry="1m"):
    if df is None or len(df) < 30:
        return {
            "signal": "WAIT / NO TRADE 🟡",
            "action": "SKIP CANDLE",
            "expiry": expiry,
            "confidence": "0%",
            "rsi": "N/A"
        }

    # Indicators Calculation for Binary Options
    df['rsi'] = ta.momentum.rsi(df['Close'], window=14)
    macd = ta.trend.MACD(df['Close'])
    df['macd'] = macd.macd()
    df['macd_signal'] = macd.macd_signal()
    df['ema_20'] = ta.trend.ema_indicator(df['Close'], window=20)
    df['ema_50'] = ta.trend.ema_indicator(df['Close'], window=50)
    
    bb = ta.volatility.BollingerBands(df['Close'], window=20, window_dev=2)
    df['bb_high'] = bb.bollinger_hband()
    df['bb_low'] = bb.bollinger_lband()

    last = df.iloc[-1]
    prev = df.iloc[-2]

    up_score = 0
    down_score = 0

    # 1. RSI Extreme Levels
    if last['rsi'] <= 30:
        up_score += 3
    elif last['rsi'] >= 70:
        down_score += 3

    # 2. MACD Crossover Confirmation
    if last['macd'] > last['macd_signal'] and prev['macd'] <= prev['macd_signal']:
        up_score += 2
    elif last['macd'] < last['macd_signal'] and prev['macd'] >= prev['macd_signal']:
        down_score += 2

    # 3. EMA Trend Direction
    if last['Close'] > last['ema_20'] > last['ema_50']:
        up_score += 2
    elif last['Close'] < last['ema_20'] < last['ema_50']:
        down_score += 2

    # 4. Bollinger Band Reversal
    if last['Close'] <= last['bb_low']:
        up_score += 3
    elif last['Close'] >= last['bb_high']:
        down_score += 3

    rsi_val = round(last['rsi'], 2) if pd.notnull(last['rsi']) else "N/A"
    expiry_label = "1 MINUTE" if expiry == "1m" else "5 MINUTES"

    # Quotex Binary Signal Decision
    if up_score >= 5 and up_score > down_score:
        confidence = min(72 + (up_score * 3), 95)
        return {
            "signal": "CALL (UP ⬆️) 🟢",
            "action": "TRADE HIGHER / BUY GREEN CANDLE",
            "expiry": expiry_label,
            "confidence": f"{confidence}%",
            "rsi": rsi_val
        }
    elif down_score >= 5 and down_score > up_score:
        confidence = min(72 + (down_score * 3), 95)
        return {
            "signal": "PUT (DOWN ⬇️) 🔴",
            "action": "TRADE LOWER / SELL RED CANDLE",
            "expiry": expiry_label,
            "confidence": f"{confidence}%",
            "rsi": rsi_val
        }
    else:
        return {
            "signal": "WAIT / NO SIGNAL 🟡",
            "action": "DO NOT TRADE THIS CANDLE",
            "expiry": "N/A",
            "confidence": "50% (Risky Market)",
            "rsi": rsi_val
        }