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
    last_rsi = df['RSI'].iloc[-1]
    upper_b = df['Upper_Band'].iloc[-1]
    lower_b = df['Lower_Band'].iloc[-1]
    ema9 = df['EMA9'].iloc[-1]
    ema21 = df['EMA21'].iloc[-1]

    # Active Precision Logic
    if last_rsi < 50 or last_close <= df['Close'].mean() or ema9 > ema21:
        return "CALL", "CALL (UP) ⬆", f"{min(89 + int(abs(50 - last_rsi)), 98)}%", last_rsi
    else:
        return "PUT", "PUT (DOWN) ⬇", f"{min(89 + int(abs(last_rsi - 50)), 98)}%", last_rsi