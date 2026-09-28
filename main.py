import pandas as pd
import numpy as np

def calculate_advanced_signal(df):
    # RSI Calculation
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    df['RSI'] = df['RSI'].fillna(50)

    # EMA Calculation
    df['EMA9'] = df['Close'].ewm(span=9, adjust=False).mean()
    df['EMA21'] = df['Close'].ewm(span=21, adjust=False).mean()
    
    last_close = df['Close'].iloc[-1]
    last_rsi = df['RSI'].iloc[-1]
    upper_b = df['Upper_Band'].iloc[-1]
    lower_b = df['Lower_Band'].iloc[-1]
    ema9 = df['EMA9'].iloc[-1]
    ema21 = df['EMA21'].iloc[-1]
    
    prev_open = df['Open'].iloc[-2]
    prev_close = df['Close'].iloc[-2]
    curr_open = df['Open'].iloc[-1]
    curr_close = df['Close'].iloc[-1]

    # Candlestick Patterns
    bullish_engulfing = (prev_close < prev_open) and (curr_close > curr_open) and (curr_close > prev_open)
    bearish_engulfing = (prev_close > prev_open) and (curr_close < curr_open) and (curr_close < prev_open)

    # Strategy Scoring
    call_score = 0
    put_score = 0

    # 1. RSI Rules (More Flexible Boundaries)
    if last_rsi < 45:
        call_score += 2
    elif last_rsi > 55:
        put_score += 2

    # 2. Bollinger Bands
    if last_close <= lower_b:
        call_score += 2
    elif last_close >= upper_b:
        put_score += 2

    # 3. EMA Trend
    if ema9 > ema21:
        call_score += 1
    elif ema9 < ema21:
        put_score += 1

    # 4. Candlestick Action
    if bullish_engulfing:
        call_score += 2
    elif bearish_engulfing:
        put_score += 2

    # Adjusted Threshold (Triggering Signals Smoother)
    if call_score >= 2:
        return "CALL", "CALL (UP) ⬆", f"{min(87 + call_score * 2, 98)}%", last_rsi
    elif put_score >= 2:
        return "PUT", "PUT (DOWN) ⬇", f"{min(87 + put_score * 2, 98)}%", last_rsi
    else:
        return "WAIT", "WAIT / NO TRADE ⚠️", "Consolidation", last_rsi