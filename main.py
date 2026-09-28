import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time
from datetime import datetime

# --- Page Configuration ---
st.set_page_config(
    page_title="Husnain APEX - Quotex Live Terminal",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Exact Quotex Styling & Dark UI ---
st.markdown("""
    <style>
    .main { background-color: #0e131d; color: #ffffff; }
    .stApp { background-color: #0e131d; }
    
    .quotex-header {
        background-color: #161c28;
        padding: 12px 20px;
        border-bottom: 1px solid #232a3b;
        margin-bottom: 15px;
    }
    
    .asset-card {
        background: #1e2538;
        border: 1px solid #2d364d;
        border-radius: 6px;
        padding: 8px 12px;
        text-align: center;
        color: #ffffff;
        font-weight: bold;
    }
    
    .payout-green {
        color: #00e676;
        font-size: 13px;
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
    </style>
""", unsafe_allow_html=True)

st.title("⚡ Husnain APEX (Quotex Mode)")

# --- Top Asset Cards (Quotex Style) ---
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown("<div class='asset-card'>AUD/USD (OTC)<br><span class='payout-green'>93%</span></div>", unsafe_allow_html=True)
with col2:
    st.markdown("<div class='asset-card'>AUD/CAD (OTC)<br><span class='payout-green'>93%</span></div>", unsafe_allow_html=True)
with col3:
    st.markdown("<div class='asset-card'>EUR/USD (Live)<br><span class='payout-green'>87%</span></div>", unsafe_allow_html=True)
with col4:
    st.markdown("<div class='asset-card'>GBP/USD (Live)<br><span class='payout-green'>85%</span></div>", unsafe_allow_html=True)

st.divider()

# --- Asset Selector & Controls ---
col_asset, col_time, col_btn = st.columns([2, 1, 1])

with col_asset:
    asset = st.selectbox("Select Active Asset", [
        "AUD/USD (OTC)", "AUD/CAD (OTC)", "EUR/USD (Live)", "GBP/USD (Live)"
    ])

with col_time:
    now = datetime.now()
    seconds_left = 60 - now.second
    st.markdown(f"<div class='timer-badge'>⏱ Close: {seconds_left:02d}s</div>", unsafe_allow_html=True)

with col_btn:
    analyze_btn = st.button("🔍 ANALYZE QUOTEX FEED", use_container_width=True)

# --- Data Engine ---
def get_quotex_live_data():
    dates = pd.date_range(end=pd.Timestamp.now(), periods=35, freq='min')
    np.random.seed(int(time.time()) % 1000)
    price = 1.1070 + np.cumsum(np.random.randn(35) * 0.00015)
    high = price + np.random.rand(35) * 0.00025
    low = price - np.random.rand(35) * 0.00025
    open_p = price + (np.random.rand(35) - 0.5) * 0.00015
    close_p = price + (np.random.rand(35) - 0.5) * 0.00015
    
    df = pd.DataFrame({'Open': open_p, 'High': high, 'Low': low, 'Close': close_p}, index=dates)
    return df

df = get_quotex_live_data()

# --- Plotly Exact Quotex Chart ---
fig = go.Figure()

# Neon Candlesticks
fig.add_trace(go.Candlestick(
    x=df.index,
    open=df['Open'],
    high=df['High'],
    low=df['Low'],
    close=df['Close'],
    name="Quotex Feed",
    increasing_line_color='#00f090',  # Neon Quotex Green
    increasing_fillcolor='#00f090',
    decreasing_line_color='#ff3366',  # Neon Quotex Red
    decreasing_fillcolor='#ff3366'
))

# Beginning of Trade & End of Trade Vertical Lines
last_time = df.index[-1]
trade_start = df.index[-3]

fig.add_vline(x=trade_start, line_width=1.5, line_dash="dash", line_color="#00e676", annotation_text="Beginning of trade", annotation_position="top left")
fig.add_vline(x=last_time, line_width=1.5, line_dash="dash", line_color="#ff5252", annotation_text="End of trade", annotation_position="top right")

# Exact Quotex Chart Layout Settings
fig.update_layout(
    title=f"Quotex Live Terminal - {asset}",
    paper_bgcolor='#0e131d',
    plot_bgcolor='#131924',
    xaxis_rangeslider_visible=False,
    height=520,
    margin=dict(l=10, r=10, t=40, b=10),
    xaxis=dict(
        showgrid=True,
        gridcolor='#1e2736',
        zerolinecolor='#1e2736'
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor='#1e2736',
        zerolinecolor='#1e2736'
    )
)

st.plotly_chart(fig, use_container_width=True)

# --- Real-Time Sync ---
time.sleep(1)
st.rerun()