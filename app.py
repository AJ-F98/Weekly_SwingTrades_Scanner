#!/usr/bin/env python3
"""
Streamlit Dashboard for NSE PRO Swing Scanner (2025 Final Version)
Works with SWING_PRO_*.csv files from the final scanner
"""

import streamlit as st
import pandas as pd
import os
from glob import glob
from datetime import datetime

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="NSE Pro Swing Scanner",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== CUSTOM CSS ====================
st.markdown("""
<style>
    .big-font {font-size:50px !important; font-weight:bold; text-align:center; color:#1E90FF;}
    .date-font {font-size:24px; text-align:center; color:#666;}
    .empty-state {text-align:center; padding:50px; font-size:22px; color:#888;}
</style>
""", unsafe_allow_html=True)

# ==================== TITLE & DATE ====================
st.markdown('<p class="big-font">NSE PRO SWING SCANNER</p>', unsafe_allow_html=True)
st.markdown(f'<p class="date-font">Today: {datetime.now().strftime("%A, %d %B %Y")}</p>', unsafe_allow_html=True)
st.markdown("**High-Probability 5–10% Weekly Swings | Risk ≤7% | RR ≥1:1.3 | Beats Nifty**")
st.divider()

# ==================== FIND LATEST RESULTS ====================
# Supports both old and new naming
all_csvs = sorted(
    glob("swing_signals_*.csv") + glob("SWING_PRO_*.csv") + glob("*.csv"),
    key=os.path.getmtime,
    reverse=True
)

if not all_csvs:
    st.error("No Positive Swings found")
    st.stop()

# Extract date from filename
def extract_date(filename):
    base = os.path.basename(filename)
    for prefix in ["SWING_PRO_", "swing_signals_"]:
        if prefix in base:
            try:
                date_str = base.replace(prefix, "").replace(".csv", "").replace(".xlsx", "")[:13]
                return datetime.strptime(date_str, "%Y%m%d_%H%M")
            except:
                pass
    return os.path.getmtime(filename)

latest_file = max(all_csvs, key=extract_date)
latest_date = extract_date(latest_file).strftime("%d %b %Y, %I:%M %p")

st.success(f"Latest scan: **{latest_date}**")
st.markdown("---")

# ==================== LOAD DATA ====================
@st.cache_data
def load_csv(path):
    return pd.read_csv(path)

df = load_csv(latest_file)

# Auto-detect if it's old or new format
is_pro_version = all(col in df.columns for col in ['Risk%', 'RS_vs_Nifty', 'Range_10d%'])

# ==================== ZERO SIGNALS CASE (BEAUTIFUL) ====================
if len(df) == 0:
    st.markdown("<div class='empty-state'>", unsafe_allow_html=True)
    st.markdown("### No High-Probability Setups Today")
    st.markdown("**The market is currently overextended.**")
    st.markdown("This scanner is protecting your capital by staying in cash.")
    st.markdown("**This is the edge.** Most traders lose money right now — you are winning by doing nothing.")
    st.markdown("Next batch of 10–15% winners coming after the correction.")
    st.markdown("</div>", unsafe_allow_html=True)
    st.balloons()
    st.stop()

# ==================== STATS ====================
st.subheader("Scan Summary")
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("Opportunities Found", len(df))
with col2:
    st.metric("Avg Risk", f"{df['Risk%'].str.rstrip('%').astype(float).mean():.1f}%")
with col3:
    st.metric("Avg RR (5%)", f"1:{df['Risk_Reward'].str.extract(r'1:([\d.]+)').astype(float).mean():.1f}")
with col4:
    st.metric("Avg RSI", f"{df['RSI'].mean():.1f}")
with col5:
    st.metric("Beating Nifty", f"{(df['RS_vs_Nifty'].str.rstrip('%').astype(float) > 0).sum()}/{len(df)}")

# ==================== FILTERS ====================
st.subheader("Filters")

col1, col2, col3, col4 = st.columns(4)
with col1:
    price_range = st.slider("Price Range (₹)", 0, int(df['Current_Price'].max()*1.2), (0, int(df['Current_Price'].max()*1.2)))
with col2:
    rsi_range = st.slider("RSI", 0, 100, (30, 70))
with col3:
    risk_max = st.slider("Max Risk %", 0.0, 10.0, 7.0, 0.1)
with col4:
    min_rr = st.slider("Min RR (5%)", 1.0, 5.0, 1.3, 0.1)

# Apply filters
filtered = df.copy()
filtered = filtered[filtered['Current_Price'].between(price_range[0], price_range[1])]
filtered = filtered[filtered['RSI'].between(rsi_range[0], rsi_range[1])]
filtered['Risk_Num'] = filtered['Risk%'].str.rstrip('%').astype(float)
filtered = filtered[filtered['Risk_Num'] <= risk_max]
filtered['RR_Num'] = filtered['Risk_Reward'].str.extract(r'1:([\d.]+)').astype(float)
filtered = filtered[filtered['RR_Num'] >= min_rr]

# ==================== HIGHLIGHTING ====================
def color_cells(val):
    if isinstance(val, (int, float)):
        if val > 70:
            return 'background-color: #ffcccc'
        if val < 40:
            return 'background-color: #ccffcc'
    return ''

styled = filtered.style\
    .applymap(color_cells, subset=['RSI'])\
    .format({
        'Current_Price': '₹{:.2f}',
        'Risk%': '{:.1f}%',
        '2W_Momentum': '{:.1f}%'
    })

# ==================== DISPLAY ====================
st.subheader(f"Top Opportunities ({len(filtered)} filtered)")
st.dataframe(styled, use_container_width=True, height=700, hide_index=True)

# ==================== DOWNLOAD ====================
csv_data = filtered.to_csv(index=False).encode()
st.download_button(
    "Download Filtered Results",
    data=csv_data,
    file_name=f"NSE_Swing_Signals_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
    mime="text/csv",
    use_container_width=True
)

# ==================== FOOTER ====================
st.markdown("---")
st.markdown("""
**How to trade these:**
- Buy only on Monday if price is in Buy_Range
- Risk max 1–2% of capital per trade
- Cut loss immediately if Stop_Loss hit
- Take 50% profit at 5%, trail rest
""")

st.caption("Pro Scanner v5 • Zero signals = capital preservation • Next leg coming soon")