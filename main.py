# --- Real-Time Auto Refresh Timer ---
with col_time:
    now = datetime.now()
    seconds_left = 60 - now.second
    st.markdown(
        f"<div class='timer-badge'>⏱ Candle Close: {seconds_left:02d}s</div>",
        unsafe_allow_html=True,
    )

# 1 سیکنڈ بعد پیج کو آٹو اپ ڈیٹ کرنے کے لیے
time.sleep(1)
st.rerun()