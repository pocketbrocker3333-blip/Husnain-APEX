import streamlit as st
from config import APP_NAME, QUOTEX_LIVE_PAIRS, QUOTEX_OTC_PAIRS, EXPIRY_TIMES
from data_engine import fetch_market_data
from strategies import analyze_binary_market

# Page Setup
st.set_page_config(page_title=APP_NAME, page_icon="🎯", layout="wide")

# Custom Quotex Dark Theme CSS
st.markdown("""
    <style>
    .main { background-color: #0d1117; color: #ffffff; }
    .stMetric { background-color: #161b22; padding: 15px; border-radius: 10px; border: 1px solid #30363d; }
    .stButton>button { width: 100%; background: linear-gradient(90deg, #00c853, #00e676); color: black; font-weight: bold; border-radius: 8px; height: 50px; font-size: 18px; border: none; }
    </style>
""", unsafe_allow_html=True)

st.title("🎯 Husnain APEX - Quotex Binary Signal Bot")
st.caption("BOT BY HUSNAIN NASEER | Optimized for Quotex 1-Min & 5-Min Fixed Time Binary Option Trades")

# Sidebar
st.sidebar.header("⚙️ Quotex Market Selector")
market_mode = st.sidebar.radio("Market Category", ["Quotex OTC Market (24/7)", "Quotex Live Market"])

pairs_dict = QUOTEX_OTC_PAIRS if market_mode == "Quotex OTC Market (24/7)" else QUOTEX_LIVE_PAIRS

selected_pair = st.sidebar.selectbox("Select Asset Pair", list(pairs_dict.keys()))
selected_expiry = st.sidebar.selectbox("Select Expiration Time", list(EXPIRY_TIMES.keys()))

symbol = pairs_dict[selected_pair]
tf = EXPIRY_TIMES[selected_expiry]

st.sidebar.markdown("---")
st.sidebar.button("⚡ SCAN QUOTEX SIGNAL")

# Main Display
st.subheader(f"📊 Market Analysis: {selected_pair}")

with st.spinner("Analyzing Quotex Candle Data..."):
    df = fetch_market_data(symbol, interval=tf)

if df is not None and not df.empty:
    result = analyze_binary_market(df, expiry=tf)
    
    col1, col2, col3, col4 = st.columns(4)
    
    latest_price = round(float(df['Close'].iloc[-1]), 5)
    col1.metric("Current Price", f"${latest_price}")
    col2.metric("RSI Level", result.get("rsi", "N/A"))
    col3.metric("Trade Expiry", result.get("expiry", "1 MIN"))
    col4.metric("Signal Accuracy", result.get("confidence", "0%"))
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Quotex Binary Signal Output Box
    sig = result.get("signal", "")
    action = result.get("action", "")
    
    if "CALL" in sig:
        st.success(f"### 🟢 QUOTEX SIGNAL: {sig}\n**Recommendation:** {action} | **Expiry:** {result.get('expiry')}")
    elif "PUT" in sig:
        st.error(f"### 🔴 QUOTEX SIGNAL: {sig}\n**Recommendation:** {action} | **Expiry:** {result.get('expiry')}")
    else:
        st.warning(f"### 🟡 MARKET STATUS: {sig}\n**Recommendation:** {action} - Wait for Next Candle")

    st.markdown("---")
    st.subheader("📈 Live Candle Data")
    st.dataframe(df[['Open', 'High', 'Low', 'Close']].tail(8), use_container_width=True)
else:
    st.error("Market data fetch نہیں ہو سکا۔ برائے مہربانی Pair تبدیل کر کے دوبارہ کوشش کریں۔")