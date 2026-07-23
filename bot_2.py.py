import streamlit as st
import pandas as pd
import numpy as np

# Page Configuration for Dark Professional Look
st.set_page_config(
    page_title="AIBots - Professional Trading Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Dark Dribbble/Trading UI Look
st.markdown("""
    <style>
    .main {
        background-color: #0d1117;
        color: #ffffff;
    }
    .stMetric {
        background-color: #161b22;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #30363d;
    }
    .card {
        background-color: #161b22;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #30363d;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# Top Navigation Bar Simulation
st.markdown("### 🤖 AIBots - Advanced AI Trading & Voice Assistant")
st.markdown("---")

# Sidebar for Navigation & Settings
st.sidebar.header("⚙️ Control Panel")
menu = st.sidebar.selectbox("Navigation", ["Dashboard", "Arbitrage AI Bots", "My Exchanges", "Settings & API Keys"])

# Main Dashboard View
if menu == "Dashboard":
    st.subheader("My Dashboard Overview")
    
    # Top Row Metrics (Overview, P&L, Active Bots)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.metric(label="Total Balance (USDT)", value="$1,458.78", delta="+12.4%")
        st.markdown("BTC: 0.0282237 ($763.51) <br> ETH: 0.38632853 ($677.52)", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.metric(label="Profit and Loss (P&L)", value="+$327.64", delta="+8.2%")
        # Simulated chart line
        chart_data = pd.DataFrame(np.random.randn(20, 1), columns=['P&L'])
        st.line_chart(chart_data, height=100)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col3:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Active Bots (1)")
        st.success("🟢 Accumulator Bot Active (+14.9%)")
        st.info("🟢 BTC Scalper Running")
        st.markdown('</div>', unsafe_allow_html=True)

    # Second Row: AI Voice & Screen Analysis Section
    st.markdown("### 🎙️ AI Voice & Screen Assistant")
    chat_col, screen_col = st.columns([2, 1])
    
    with chat_col:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.write("💬 **AI Chat / Voice Interaction**")
        user_input = st.text_input("Ask your AI bot anything (e.g., 'Analyze market trend for BTC'):")
        if st.button("Send Command"):
            if user_input:
                st.success(f"AI Bot: Executing command '{user_input}' using live market data...")
        st.markdown('</div>', unsafe_allow_html=True)
        
    with screen_col:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.write("📷 **Screen Share / Analysis**")
        st.write("Allow bot to view your screen/charts to give real-time trading signals.")
        if st.button("Capture & Analyze Screen"):
            st.warning("Screen captured successfully! AI is evaluating indicators...")
        st.markdown('</div>', unsafe_allow_html=True)

elif menu == "Settings & API Keys":
    st.subheader("🔑 API Configuration & Settings")
    st.text_input("Binance / MEXC API Key", type="password")
    st.text_input("API Secret Key", type="password")
    st.text_input("OpenAI / Gemini API Key for Voice & Logic", type="password")
    if st.button("Save Securely"):
        st.success("API Keys saved successfully!")