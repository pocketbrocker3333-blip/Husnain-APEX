import streamlit as st
import plotly.graph_objects as go
from streamlit_autorefresh import st_autorefresh
from config import APP_NAME, QUOTEX_LIVE_PAIRS, QUOTEX_OTC_PAIRS, EXPIRY_AND_TIMEFRAME
from data_engine import fetch_market_data
from strategies import analyze_binary_market

# Page Setup
st.set_page_config(page_title=APP_NAME, page_icon="🎯", layout="wide")

# Live Auto Refresh Every 5 Seconds (Quotex Live Feel)
st_autorefresh(interval=5000, key="quotex_live_feed")

# Custom Dark HD Theme Styling
st.markdown("""
    <style>
    .main { background-color: #0B0E14; color: #FFFFFF; }
    .stMetric { background-color: #131722; padding: 15px; border-radius: 10px; border: 1px solid #2A2E39; }
    .stButton>button { width: 100%; background: linear-gradient(90deg, #00E676, #00C853); color: black; font-weight: bold; border-radius: 8px; height: 50px; font-size: 18px; border: none; }
    a.quotex-btn { display: block; text-align: center; background: #2962FF; color: white; padding: 12px; border-radius: 8px; text-decoration: none; font-weight: bold; font-size: 16px; margin-top: 10px; }
    a.quotex-btn:hover { background: #1E4BD8; color: white; }
    </style>
""", unsafe_allow_html=True)

st.title("🎯 Husnain APEX - Quotex Signal Bot")
st.caption("BOT BY HUSNAIN NASEER | Live HD Candlestick Chart & Auto-Refresh Signals")

# Sidebar Setup
st.sidebar.header("⚙️ Quotex Market Settings")
market_category = st.sidebar.radio("Select Category", ["OTC Markets (24/7)", "Live Markets"])

if market_category == "OTC Markets (24/7)":
    selected_dict = QUOTEX_OTC_PAIRS
else:
    selected_dict = QUOTEX_LIVE_PAIRS

selected_pair = st.sidebar.selectbox("Select Asset Pair", list(selected_dict.keys()))
selected_expiry_label = st.sidebar.selectbox("Select Trade Expiry & Candle Frame", list(EXPIRY_AND_TIMEFRAME.keys()))

symbol = selected_dict[selected_pair]
tf = EXPIRY_AND_TIMEFRAME[selected_expiry_label]

st.sidebar.markdown("---")
st.sidebar.button("⚡ SCAN QUOTEX SIGNAL")

# Quotex Direct Link
st.sidebar.markdown("---")
st.sidebar.markdown('<a href="https://qxbroker.com/en/trade" target="_blank" class="quotex-btn">🌐 Open Quotex Terminal</a>', unsafe_allow_html=True)

# Main Dashboard
st.subheader(f"📊 Live Market Analysis: {selected_pair}")

df = fetch_market_data(symbol, interval=tf)

if df is not None and not df.empty:
    result = analyze_binary_market(df, expiry=tf)
    
    c1, c2, c3, c4 = st.columns(4)
    
    latest_price = round(float(df['Close'].iloc[-1]), 5)
    c1.metric("Current Price", f"${latest_price}")
    c2.metric("RSI Level", result.get("rsi", "N/A"))
    c3.metric("Candle / Expiry", result.get("expiry", "1 MIN"))
    c4.metric("Signal Accuracy", result.get("confidence", "0%"))
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    sig = result.get("signal", "")
    action = result.get("action", "")
    
    if "CALL" in sig:
        st.success(f"### 🟢 QUOTEX SIGNAL: {sig}\n**Action:** {action} | **Frame:** {result.get('expiry')}")
    elif "PUT" in sig:
        st.error(f"### 🔴 QUOTEX SIGNAL: {sig}\n**Action:** {action} | **Frame:** {result.get('expiry')}")
    else:
        st.warning(f"### 🟡 MARKET STATUS: {sig}\n**Action:** {action} - Wait for Clear Setup")

    # --- HD QUOTEX-STYLE CANDLESTICK CHART ---
    st.markdown("---")
    st.subheader(f"🕯️ Quotex Live HD Chart ({selected_pair} - {tf} Frame)")
    
    # Take last 35 candles for bold & clear HD view
    df_hd = df.tail(35)
    
    fig = go.Figure(data=[go.Candlestick(
        x=df_hd.index,
        open=df_hd['Open'],
        high=df_hd['High'],
        low=df_hd['Low'],
        close=df_hd['Close'],
        increasing_line_color='#00E676', 
        increasing_fillcolor='#00E676',
        decreasing_line_color='#FF1744', 
        decreasing_fillcolor='#FF1744'
    )])
    
    fig.update_layout(
        template="plotly_dark",
        xaxis_rangeslider_visible=False,
        height=500,
        margin=dict(l=10, r=50, t=20, b=20),
        paper_bgcolor="#0B0E14",
        plot_bgcolor="#131722",
        yaxis=dict(
            side="right",
            gridcolor="#1F2937",
            showgrid=True,
            zeroline=False
        ),
        xaxis=dict(
            gridcolor="#1F2937",
            showgrid=True
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)

    st.subheader(f"📈 Recent Candle OHLC Values ({tf} Frame)")
    st.dataframe(df[['Open', 'High', 'Low', 'Close']].tail(6), use_container_width=True)
else:
    st.error("Market Data Fetch نہیں ہو سکا۔ Weekend پر OTC Markets استعمال کریں۔")