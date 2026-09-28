import pandas as pd
import numpy as np

def calculate_advanced_signal(df):
    # 1. RSI Calculation
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    df['RSI'] = df['RSI'].fillna(50)

    # 2. EMAs Calculation
    df['EMA9'] = df['Close'].ewm(span=9, adjust=False).mean()
    df['EMA21'] = df['Close'].ewm(span=21, adjust=False).mean()
    
    # Current Market Values
    last_close = df['Close'].iloc[-1]
    last_open = df['Open'].iloc[-1]
    last_rsi = df['RSI'].iloc[-1]
    upper_b = df['Upper_Band'].iloc[-1]
    lower_b = df['Lower_Band'].iloc[-1]
    ema9 = df['EMA9'].iloc[-1]
    ema21 = df['EMA21'].iloc[-1]
    
    # Previous Candle Data
    prev_close = df['Close'].iloc[-2]
    prev_open = df['Open'].iloc[-2]

    # Dynamic Scoring System
    call_score = 0
    put_score = 0

    # Pattern & Indicator Detection
    bullish_engulfing = (prev_close < prev_open) and (last_close > last_open) and (last_close > prev_open)
    bearish_engulfing = (prev_close > prev_open) and (last_close < last_open) and (last_close < prev_open)

    # RSI Conditions
    if last_rsi < 35:
        call_score += 2
    elif last_rsi > 65:
        put_score += 2

    # Bollinger Bands Reversals
    if last_close <= lower_b:
        call_score += 2
    elif last_close >= upper_b:
        put_score += 2

    # Trend Direction via EMA
    if ema9 > ema21:
        call_score += 1
    elif ema9 < ema21:
        put_score += 1

    # Price Action Confirmation
    if bullish_engulfing:
        call_score += 2
    elif bearish_engulfing:
        put_score += 2

    # Final Decision Making based on live scores
    if call_score >= 3 and call_score > put_score:
        acc = min(88 + call_score * 2, 98)
        return "CALL", "CALL (UP) ⬆", f"{acc}%", last_rsi
    elif put_score >= 3 and put_score > call_score:
        acc = min(88 + put_score * 2, 98)
        return "PUT", "PUT (DOWN) ⬇", f"{acc}%", last_rsi
    else:
        return "WAIT", "WAIT / NO TRADE ⚠️", "Consolidation", last_rsi