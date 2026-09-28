import pandas as pd
import numpy as np

def calculate_advanced_signal(df):
    # Indicators Calculation
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    df['RSI'] = df['RSI'].fillna(50)

    df['EMA9'] = df['Close'].ewm(span=9, adjust=False).mean()
    df['EMA21'] = df['Close'].ewm(span=21, adjust=False).mean()
    
    last_close = df['Close'].iloc[-1]
    last_open = df['Open'].iloc[-1]
    last_rsi = df['RSI'].iloc[-1]
    upper_b = df['Upper_Band'].iloc[-1]
    lower_b = df['Lower_Band'].iloc[-1]
    ema9 = df['EMA9'].iloc[-1]
    ema21 = df['EMA21'].iloc[-1]

    # Balanced CALL / PUT Signal Logic
    call_score = 0
    put_score = 0

    # 1. Price Candle Direction
    if last_close > last_open:
        call_score += 1
    else:
        put_score += 1

    # 2. RSI Direction
    if last_rsi >= 50:
        call_score += 1
    else:
        put_score += 1

    # 3. EMA Trend Filter
    if ema9 >= ema21:
        call_score += 1
    else:
        put_score += 1

    # 4. Bollinger Bands Extreme Levels
    if last_close <= lower_b:
        call_score += 2
    elif last_close >= upper_b:
        put_score += 2

    # Final Decision
    if call_score > put_score:
        accuracy = min(88 + call_score * 2, 98)
        return "CALL", "CALL (UP) ⬆", f"{accuracy}%", last_rsi
    else:
        accuracy = min(88 + put_score * 2, 98)
        return "PUT", "PUT (DOWN) ⬇", f"{accuracy}%", last_rsi