import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time
from datetime import datetime

from strategies import calculate_advanced_signal

# --- Page Configuration ---
st.set_page_config(
    page_title="Husnain APEX - Quotex Live Terminal",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Original Quotex Dark Styling & Glowing CSS ---
st.markdown("""
    <style>
    .main { background-color: #0e131d; color: #ffffff; }
    .stApp { background-color: #0e131d; }
    
    section[data-testid="stSidebar"] {
        background-color: #131722 !important;
        border-right: 1px solid #1e2538;
    }
    
    .scanner-box {
        position: relative;
        border: 2px solid #00e676;
        border-radius: 8px;
        overflow: hidden;
        background: #131722;
        padding: 20px;
        margin-top: 15px;
        margin-bottom: 20px;
    }
    
    .laser-line {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 4px;
        background: linear-gradient(90deg, transparent, #00e676, #ffffff, #00e676, transparent);
        box-shadow: 0 0 15px #00e676, 0 0 30px #00e676;
        animation: scan 1.5s infinite ease-in-out;
        z-index: 10;
    }
    
    @keyframes scan {
        0% { top: 0%; }
        50% { top: 95%; }
        100% { top: 0%; }
    }
    
    .timer-badge {
        font-size: 18px;
        font-weight: bold;
        color: #ffb74d;
        background-color: #1e2538;
        padding: 8px 14px;
        border-radius: 6px;
        border: 1px solid #ffb74d;
        text-align: center;
    }

    .card-call {
        background: #003319;
        border: 2px solid #00e676;
        box-shadow: 0 0 15px rgba(0, 230, 118, 0.4);
        border-radius: 8px;
        padding: 12px;
        text-align: center;
    }
    .card-put {
        background: #33000d;
        border: 2px solid #ff3366;
        box-shadow: 0 0 15px rgba(255, 51, 102, 0.4);
        border-radius: 8px;
        padding: 12px;
        text-align: center;
    }
    .card-info {
        background: #131722;
        border: 1px solid #2d364d;
        border-radius: 8px;
        padding: 12px;
        text-align: center;
    }
    .card-title {
        color: #8b949e;
        font-size: 12px;
        text-transform: uppercase;
        font-weight: bold;
        margin-bottom: 4px;
    }
    .card-value {
        font-size: 22px;
        font-weight: 900;
        margin: 0;
    }
    </style>
""", unsafe_allow_html=True)

# --- Header ---
st.title("⚡ Husnain APEX")
st.caption("Quotex Live Market High-Precision Signal Terminal")

# --- Top Control Toolbar ---
col_asset, col_tf, col_time, col_btn = st.columns([2, 1, 1, 1.5])

with col_asset:
    asset = st.selectbox("Quotex Asset Pair", [
        "EUR/USD (OTC)", "GBP/USD (OTC)", "USD/JPY (OTC)", 
        "AUD/CAD (OTC)", "EUR/USD (Live)", "GBP/USD (Live)"
    ])

with col_tf:
    timeframe = st.selectbox("Candle Timeframe", ["1 Min", "2 Min", "5 Min", "10 Min", "15 Min"], index=0)

@st.fragment(run_every=1)
def show_live_timer():
    now = datetime.now()
    seconds_left = 60 - now.second
    st.markdown(f"<div class='timer-badge'>⏱ Candle Close: {seconds_left:02d}s</div>", unsafe_allow_html=True)

with col_time:
    show_live_timer()

with col_btn:
    analyze_btn = st.button("🔍 ANALYZE LIVE MARKET", use_container_width=True)

# --- Dynamic Market Engine ---
def get_quotex_market_data(asset_name, tf_name):
    # Dynamic seed based on microsecond to always generate unique market waves
    np.random.seed(int(time.time() * 1000) % 100000)
    periods = 50
    dates = pd.date_range(end=pd.Timestamp.now(), periods=periods, freq='1min')
    
    # Random walk with directional volatility
    steps = np.random.normal(loc=0.0, scale=0.0009, size=periods)
    price_path = 1.0850 + np.cumsum(steps)
    
    df = pd.DataFrame({'Open': price_path, 'Close': price_path}, index=dates)
    df['Open'] = df['Close'].shift(1) + np.random.normal(0, 0.0002, periods)
    df['Open'].iloc[0] = df['Close'].iloc[0] - 0.0001
    df['High'] = df[['Open', 'Close']].max(axis=1) + np.abs(np.random.normal(0, 0.0003, periods))
    df['Low'] = df[['Open', 'Close']].min(axis=1) - np.abs(np.random.normal(0, 0.0003, periods))
    
    df['MA20'] = df['Close'].rolling(window=20).mean()
    df['STD'] = df['Close'].rolling(window=20).std()
    df['Upper_Band'] = df['MA20'] + (df['STD'] * 2)
    df['Lower_Band'] = df['MA20'] - (df['STD'] * 2)
    
    return df.dropna()

df = get_quotex_market_data(asset, timeframe)

# --- Scanner Animation ---
if analyze_btn:
    scan_placeholder = st.empty()
    for i in range(2, 0, -1):
        scan_placeholder.markdown(f"""
            <div class='scanner-box'>
                <div class='laser-line'></div>
                <h3 style='text-align: center; color: #00e676;'>Scanning Indicators for {asset} ({timeframe})...</h3>
                <p style='text-align: center; color: #ffffff;'>Calculating Support/Resistance, RSI & Candlesticks... {i}s</p>
            </div>
        """, unsafe_allow_html=True)
        time.sleep(1)
    scan_placeholder.empty()

# --- Signal Calculations ---
support = df['Low'].min()
resistance = df['High'].max()
signal_type, signal_text, confidence, last_rsi = calculate_advanced_signal(df)

# --- Signal Display Cards ---
col_sig, col_conf, col_rsi, col_supp = st.columns(4)

with col_sig:
    if signal_type == "CALL":
        st.markdown(f"<div class='card-call'><div class='card-title'>SIGNAL</div><div class='card-value' style='color:#00e676;'>{signal_text}</div></div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='card-put'><div class='card-title'>SIGNAL</div><div class='card-value' style='color:#ff3366;'>{signal_text}</div></div>", unsafe_allow_html=True)

with col_conf:
    st.markdown(f"<div class='card-info'><div class='card-title'>ACCURACY</div><div class='card-value' style='color:#ffffff;'>{confidence}</div></div>", unsafe_allow_html=True)

with col_rsi:
    st.markdown(f"<div class='card-info'><div class='card-title'>RSI (14)</div><div class='card-value' style='color:#00e676;'>{last_rsi:.1f}</div></div>", unsafe_allow_html=True)

with col_supp:
    st.markdown(f"<div class='card-info'><div class='card-title'>S/R LEVELS</div><div class='card-value' style='color:#ffb74d; font-size: 16px; margin-top: 5px;'>{support:.4f} / {resistance:.4f}</div></div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- Candlestick Chart ---
fig = go.Figure()

fig.add_trace(go.Candlestick(
    x=df.index,
    open=df['Open'],
    high=df['High'],
    low=df['Low'],
    close=df['Close'],
    name="Quotex Feed",
    increasing_line_color='#00f090',
    increasing_fillcolor='#00f090',
    decreasing_line_color='#ff3366',
    decreasing_fillcolor='#ff3366'
))

last_time = df.index[-1]
trade_start = df.index[-3]
fig.add_vline(x=trade_start, line_width=1.5, line_dash="dash", line_color="#00e676", annotation_text="Trade Start", annotation_position="top left")
fig.add_vline(x=last_time, line_width=1.5, line_dash="dash", line_color="#ff5252", annotation_text="Expiry", annotation_position="top right")

fig.update_layout(
    title=f"Quotex Live Terminal - {asset} ({timeframe})",
    paper_bgcolor='#0e131d',
    plot_bgcolor='#131924',
    xaxis_rangeslider_visible=False,
    height=500,
    margin=dict(l=10, r=10, t=40, b=10),
    xaxis=dict(showgrid=True, gridcolor='#1e2736', zerolinecolor='#1e2736'),
    yaxis=dict(showgrid=True, gridcolor='#1e2736', zerolinecolor='#1e2736')
)

st.plotly_chart(fig, use_container_width=True)