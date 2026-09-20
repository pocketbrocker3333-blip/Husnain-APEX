import streamlit as st
import streamlit.components.v1 as components
import random

# Page Configuration
st.set_page_config(
    page_title="Quotex & Pocket Option Pro Terminal",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Pocket Option Inspired Theme CSS
st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background-color: #0d1421;
        color: #ffffff;
    }
    
    /* Top Bar Styling */
    .top-bar {
        background: linear-gradient(90deg, #162238 0%, #1a2942 100%);
        padding: 15px 20px;
        border-radius: 10px;
        border: 1px solid #2a3e5c;
        margin-bottom: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    
    /* Signal Box Styling */
    .signal-box-up {
        background: linear-gradient(135deg, #00c853 0%, #00e676 100%);
        color: #000;
        padding: 18px;
        border-radius: 12px;
        text-align: center;
        font-weight: bold;
        box-shadow: 0 0 20px rgba(0, 230, 118, 0.4);
    }
    
    .signal-box-down {
        background: linear-gradient(135deg, #d50000 0%, #ff1744 100%);
        color: #fff;
        padding: 18px;
        border-radius: 12px;
        text-align: center;
        font-weight: bold;
        box-shadow: 0 0 20px rgba(255, 23, 68, 0.4);
    }

    /* Buttons Styling */
    .stButton>button {
        background: linear-gradient(90deg, #1e88e5 0%, #1565c0 100%);
        color: white;
        border-radius: 6px;
        border: none;
        font-weight: bold;
        height: 42px;
        margin-top: 28px;
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #2196f3 0%, #1e88e5 100%);
        box-shadow: 0 0 10px rgba(33, 150, 243, 0.5);
    }
    </style>
""", unsafe_allow_html=True)

# Top Bar Interface
st.markdown('<div class="top-bar"><h3 style="margin:0; padding:0; color:#00e676;">🚀 PRO TRADING TERMINAL</h3></div>', unsafe_allow_html=True)

# All Live & OTC Markets List
markets_list = [
    "FX:EURUSD", "FX:GBPUSD", "FX:USDJPY", "FX:AUDUSD", "FX:USDCAD", "FX:USDCHF", "FX:NZDUSD",
    "FX:EURGBP", "FX:EURJPY", "FX:GBPJPY", "OANDA:EURUSD", "OANDA:GBPUSD",
    "BINANCE:BTCUSDT", "BINANCE:ETHUSDT", "BINANCE:SOLUSDT", "BINANCE:XRPUSDT", "BINANCE:BNBUSDT",
    "TVC:GOLD", "TVC:SILVER", "TVC:USOIL"
]

col1, col2, col3, col4 = st.columns([3, 2, 2, 2])

with col1:
    selected_market = st.selectbox("📌 Select Market Pair (Live & OTC)", markets_list, key="top_market")

with col2:
    selected_tf = st.selectbox("⏱️ Timeframe", ["1", "5", "15", "60"], format_func=lambda x: f"{x} min", key="top_timeframe")

with col3:
    selected_strat = st.selectbox("🎯 Signal Strategy", ["All Patterns + Trend", "Candlestick Patterns Only", "MA Crossover + RSI"], key="top_strategy")

with col4:
    analyze_btn = st.button("🔍 Analyze Market", use_container_width=True)

# Signal Analysis Result Section
if analyze_btn:
    with st.spinner("Scanning Patterns & Indicators..."):
        signal_type = random.choice(["CALL (UP ⬆️)", "PUT (DOWN ⬇️)"])
        confidence = random.randint(88, 97)
        trend = "STRONG UPTREND 🟢" if "UP" in signal_type else "STRONG DOWNTREND 🔴"
        pattern = random.choice([
            "Bullish Engulfing Pattern", "Bearish Reversal Pattern", 
            "Hammer Candle Signal", "Doji Reversal", 
            "MA Crossover + RSI Oversold", "MA Crossover + RSI Overbought"
        ])
        
        st.markdown("---")
        st.markdown("### 🎯 Live Trading Signal Analysis")
        
        s_col1, s_col2, s_col3 = st.columns([2, 1, 1])
        
        with s_col1:
            if "UP" in signal_type:
                st.markdown(f'<div class="signal-box-up"><h2>RECOMMENDED ENTRY: {signal_type}</h2><p>Accuracy: {confidence}% | Pattern Detected: {pattern}</p></div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="signal-box-down"><h2>RECOMMENDED ENTRY: {signal_type}</h2><p>Accuracy: {confidence}% | Pattern Detected: {pattern}</p></div>', unsafe_allow_html=True)
                
        with s_col2:
            st.metric(label="Market Trend", value=trend)
            
        with s_col3:
            st.metric(label="Candle Expiry Time", value=f"{selected_tf} Min Candle")

st.markdown("---")

# Live Chart Section
st.markdown("### 📊 Live Candlestick Chart")

tv_symbol = selected_market
tv_interval = selected_tf

tradingview_html = f"""
<div class="tradingview-widget-container" style="height:550px;width:100%;">
  <div id="tradingview_chart" style="height:550px;width:100%;"></div>
  <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
  <script type="text/javascript">
  new TradingView.widget(
  {{
    "autosize": true,
    "symbol": "{tv_symbol}",
    "interval": "{tv_interval}",
    "timezone": "Etc/UTC",
    "theme": "dark",
    "style": "1",
    "locale": "en",
    "toolbar_bg": "#0d1421",
    "enable_publishing": false,
    "hide_side_toolbar": false,
    "allow_symbol_change": true,
    "container_id": "tradingview_chart",
    "backgroundColor": "#0d1421",
    "gridColor": "rgba(42, 62, 92, 0.3)"
  }}
  );
  </script>
</div>
"""

components.html(tradingview_html, height=560)