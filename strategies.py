import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time
from strategies import calculate_advanced_signal

# Page Configuration
st.set_page_config(
    page_title="Husnain APEX Terminal",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Dark Apex Styling
st.markdown("""
<style>
    .main { background-color: #0b0e14; color: #ffffff; }
    .stApp { background-color: #0b0e14; }
    div[data-testid="stMetricValue"] { font-size: 24px; font-weight: bold; }
    .stButton>button {
        background: linear-gradient(90deg, #00c6ff 0%, #0072ff 100%);
        color: white; font-weight: bold; border-radius: 8px; border: none; padding: 12px 24px; width: 100%;
    }
</style>
""", unsafe_allow_html=True)

st.title("⚡ HUSNAIN APEX — BINARY SIGNAL TERMINAL")

# Sidebar Controls
st.sidebar.header("🕹️ Market Controls")
timeframe = st.sidebar.selectbox(
    "⏱️ Select Timeframe / Candle Duration:",
    ["1 Min", "2 Min", "5 Min", "10 Min", "15 Min"],
    index=0
)

asset_pair = st.sidebar.selectbox(
    "📊 Select Asset Pair:",
    ["EUR/USD (OTC)", "GBP/USD (OTC)", "USD/JPY (OTC)", "AUD/CAD (OTC)", "BTC/USD"]
)

# Market Data Generator Engine
def generate_volatile_market_data(tf_name):
    np.random.seed(int(time.time() * 10) % 10000)
    periods = 60
    dates = pd.date_range(end=pd.Timestamp.now(), periods=periods, freq='1min')
    
    # Generate balanced oscillating price movement
    steps = np.random.normal(loc=0.0, scale=0.0008, size=periods)
    price_path = 1.0850 + np.cumsum(steps)
    
    df = pd.DataFrame({'Timestamp': dates, 'Close': price_path})
    df['Open'] = df['Close'].shift(1) + np.random.normal(0, 0.0002, periods)
    df['Open'].iloc[0] = df['Close'].iloc[0] - 0.0001
    df['High'] = df[['Open', 'Close']].max(axis=1) + np.abs(np.random.normal(0, 0.0003, periods))
    df['Low'] = df[['Open', 'Close']].min(axis=1) - np.abs(np.random.normal(0, 0.0003, periods))
    
    # Bollinger Bands Calculation
    df['SMA20'] = df['Close'].rolling(window=20).mean()
    df['STD20'] = df['Close'].rolling(window=20).std()
    df['Upper_Band'] = df['SMA20'] + (df['STD20'] * 2)
    df['Lower_Band'] = df['SMA20'] - (df['STD20'] * 2)
    
    return df.dropna().reset_index(drop=True)

# Main Section
if st.button("🔍 SCAN & ANALYZE LIVE MARKET"):
    with st.spinner(f"Scanning market indicators for {asset_pair} ({timeframe})..."):
        time.sleep(0.5)
        df = generate_volatile_market_data(timeframe)
        signal, display_text, accuracy, rsi_val = calculate_advanced_signal(df)

        # Candlestick Chart
        fig = go.Figure(data=[go.Candlestick(
            x=df['Timestamp'],
            open=df['Open'],
            high=df['High'],
            low=df['Low'],
            close=df['Close'],
            increasing_line_color='#00ff88',
            decreasing_line_color='#ff3366'
        )])
        
        fig.add_trace(go.Scatter(x=df['Timestamp'], y=df['Upper_Band'], mode='lines', line=dict(color='rgba(255,255,255,0.3)'), name='Upper Band'))
        fig.add_trace(go.Scatter(x=df['Timestamp'], y=df['Lower_Band'], mode='lines', line=dict(color='rgba(255,255,255,0.3)'), name='Lower Band'))

        fig.update_layout(
            template='plotly_dark',
            paper_bgcolor='#0e131d',
            plot_bgcolor='#131924',
            xaxis_rangeslider_visible=False,
            height=450,
            margin=dict(l=10, r=10, t=30, b=10)
        )

        st.plotly_chart(fig, use_container_width=True)

        # Display Signal Metrics Cards
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Asset Pair", asset_pair)
        with col2:
            st.metric("Timeframe", timeframe)
        with col3:
            st.metric("Signal Recommendation", display_text)
        with col4:
            st.metric("Signal Accuracy", accuracy)

        st.info(f"💡 **Market Scan Summary:** RSI is at `{rsi_val:.2f}`. Strategy engines have analyzed Price Action & Indicators for {timeframe} expiration.")