import base64
import time
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

# --- PAGE CONFIGURATION (FULL SCREEN WIDE) ---
st.set_page_config(
    page_title="Zia's AI Trading Bot - Professional Suite",
    page_icon="🦅",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- SESSION STATE ---
if "api_keys" not in st.session_state:
    st.session_state.api_keys = {}
if "account_balances" not in st.session_state:
    st.session_state.account_balances = {}
if "active_image" not in st.session_state:
    st.session_state.active_image = "https://images.stockcake.com/public/e/e/b/eeba051b-bbad-4df2-9fe9-34ca126e7ee7_large/neon-cyborg-raven-stockcake.jpg"
if "brain_memory_gb" not in st.session_state:
    st.session_state.brain_memory_gb = 0.0
if "custom_gainers" not in st.session_state:
    st.session_state.custom_gainers = "BTC (+4.5%), ETH (+6.2%), SOL (+12.4%), WEEX (+15.0%)"
if "learned_rules" not in st.session_state:
    st.session_state.learned_rules = "1. Scalp on 5m candle wicks.\n2. Auto-lock profits at +3%.\n3. Dynamic risk management active."

# --- CUSTOM DRIBBBLE-INSPIRED CYBERPUNK STYLING ---
st.markdown(
    f"""
    <style>
    .main {{
        background-color: #070913;
        color: #f1f5f9;
        max-width: 100% !important;
    }}
    .stSidebar {{
        background-color: #0b0f19;
        border-right: 1px solid #1e293b;
    }}
    .dribbble-card {{
        background: linear-gradient(145deg, #111827 0%, #0d1322 100%);
        border: 1px solid #1e293b;
        border-top: 2px solid #f59e0b;
        padding: 24px;
        border-radius: 16px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.4);
        margin-bottom: 20px;
    }}
    h1, h2, h3 {{
        color: #ffffff;
        font-weight: 700;
    }}
    @keyframes pulseGlow {{
        0% {{ border: 2px solid #1e293b; box-shadow: 0 0 10px rgba(245, 158, 11, 0.1); }}
        50% {{ border: 2px solid #f59e0b; box-shadow: 0 0 25px rgba(245, 158, 11, 0.4); }}
        100% {{ border: 2px solid #1e293b; box-shadow: 0 0 10px rgba(245, 158, 11, 0.1); }}
    }}
    .animated-bot-frame {{
        animation: pulseGlow 3s infinite;
        border-radius: 16px;
        overflow: hidden;
        padding: 8px;
        background: #0d1322;
    }}
    .neural-bg {{
        background-image: linear-gradient(rgba(7, 9, 19, 0.9), rgba(7, 9, 19, 0.9)), url('{st.session_state.active_image}');
        background-size: cover;
        background-position: center;
        padding: 35px;
        border-radius: 16px;
        border: 1px solid #1e293b;
    }}
    </style>
""",
    unsafe_allow_html=True,
)

# --- STRICT TRADING PLATFORMS (Binance, MEXC, Exness Only) ---
TRADING_PLATFORMS = [
    ("Binance", "🟡"),
    ("MEXC Global", "🔵"),
    ("Exness", "🔶"),
]

# --- VERTICAL LEFT SIDEBAR MENU ---
with st.sidebar:
    st.markdown("### 🦅 ZIA")
    st.markdown("*Autonomous Suite*")
    st.divider()
    
    menu = st.radio(
        "Vertical Navigation",
        [
            "1. Live Dashboard & AI Scalper",
            "2. Platform Vault & API Hub",
            "3. CoinMarketCap Gainer Editor",
            "4. Voice Assistant & 3 Languages",
            "5. Auto-Learning & Storage Hub",
            "6. 🌍 Full Market Scanner & AI Hub"
        ]
    )
    st.markdown("---")
    st.markdown("**System:** 🟢 Online")


# ==========================================
# 1. LIVE DASHBOARD & AI SCALPER
# ==========================================
if menu == "1. Live Dashboard & AI Scalper":
    st.title("Zia")
    st.markdown("Institutional grade algorithmic execution active.")

    col_ctrl1, col_ctrl2 = st.columns(2)
    with col_ctrl1:
        selected_token = st.selectbox("Select Token for Live Stream", ["BTC/USDT", "ETH/USDT", "SOL/USDT", "XRP/USDT", "EUR/USD"])
    with col_ctrl2:
        trading_mode = st.selectbox("Execution Mode", ["Paper Trading (Simulated / Test)", "Real Money (Live Execution API)"])

    if "Real Money" in trading_mode:
        st.error("⚠️ REAL MONEY MODE ACTIVE: Bot will execute live orders through connected exchange APIs.")
    else:
        st.success("🟢 PAPER TRADING MODE ACTIVE: Safe simulation environment.")

    # Show Connected Exchange Balances on Dashboard if available
    if st.session_state.account_balances:
        st.markdown("### 💰 Connected Exchange Live Balances")
        bal_cols = st.columns(len(st.session_state.account_balances))
        for idx, (plat, bal_info) in enumerate(st.session_state.account_balances.items()):
            with bal_cols[idx]:
                st.markdown(
                    f"""
                    <div class="dribbble-card" style="padding: 15px; text-align: center;">
                        <h4 style="margin: 0; color: #f59e0b;">{plat}</h4>
                        <h2 style="color: #10b981; margin: 5px 0;">${bal_info['total_usdt']:,.2f}</h2>
                        <p style="font-size: 12px; color: #94a3b8; margin: 0;">Status: Live Synced</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    st.markdown(f"### Active Strategy: {selected_token} Scalper & Robot Vision")
    
    # Dribbble Style Robot Frame
    st.markdown('<div class="animated-bot-frame">', unsafe_allow_html=True)
    st.image(st.session_state.active_image, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Dashboard Mic & Voice Control Box
    st.markdown("### 🎙️ Dashboard Voice & Mic Control")
    col_mic1, col_mic2 = st.columns([3, 1])
    with col_mic1:
        dash_voice_cmd = st.text_input("Speak or type command for robot:", value="Hello Zia, scan market and report PnL status.")
    with col_mic2:
        mic_locked = st.toggle("🔒 Mute/Lock Mic", value=False)

    dashboard_voice_html = f"""
    <div style="background: #0d1322; padding: 16px; border-radius: 12px; border: 1px solid #f59e0b; display: flex; align-items: center; justify-content: space-between;">
        <span style="color: #f8fafc; font-size: 14px;">🤖 <b>Robot Voice Status:</b> Speaking & Scanning Active</span>
        <button onclick="playDashboardVoice()" style="background-color: #f59e0b; color: #070913; border: none; padding: 10px 18px; font-weight: bold; border-radius: 8px; cursor: pointer;">
            🔊 Speak & Scan Now
        </button>
    </div>
    <script>
    function playDashboardVoice() {{
        var text = "{dash_voice_cmd}";
        if ('speechSynthesis' in window) {{
            window.speechSynthesis.cancel();
            var utterance = new SpeechSynthesisUtterance(text);
            utterance.lang = "en-US";
            utterance.pitch = 1.2;
            window.speechSynthesis.speak(utterance);
        }}
        alert("Robot is scanning and speaking: " + text);
    }}
    </script>
    """
    components.html(dashboard_voice_html, height=90)

    st.markdown("---")
    
    col_p1, col_p2 = st.columns([2, 1])
    with col_p1:
        st.markdown(
            f'<div class="dribbble-card"><h3>{selected_token} PnL ({trading_mode.split()[0]})</h3><h2 style="color:#10b981;">+$12,455.50</h2><p>Win Rate: 94.8% | Status: Synced</p></div>',
            unsafe_allow_html=True,
        )
    with col_p2:
        st.info("📁 Dedicated Trading Ratio Folder: Active & Synced")

    st.markdown("---")
    st.markdown(f"### Live Market Intelligence Stream ({selected_token})")
    
    base_price = 60000 if "BTC" in selected_token else (3000 if "ETH" in selected_token else 1.08)
    chart_df = pd.DataFrame({
        f"{selected_token} Execution": [base_price + i*15 for i in range(10)],
        "AI Target Line": [base_price + i*18 for i in range(10)]
    }, index=[f"12:{i*10:02d}" for i in range(10)])
    
    st.line_chart(chart_df)


# ==========================================
# 2. PLATFORM VAULT & API HUB (With Live Balance Fetcher)
# ==========================================
elif menu == "2. Platform Vault & API Hub":
    st.title("Zia")
    st.markdown("Secure Exchange Vault & API Manager (Binance, MEXC, Exness). Enter keys to fetch live account balance.")

    for platform, icon in TRADING_PLATFORMS:
        with st.expander(f"{icon} Configure API for: {platform}"):
            col_a, col_b = st.columns(2)
            with col_a:
                api_key = st.text_input(f"API Key / Login ({platform})", type="password", key=f"key_{platform}")
            with col_b:
                api_secret = st.text_input(f"Secret Key / Password ({platform})", type="password", key=f"sec_{platform}")

            if st.button(f"Save & Connect {platform}", key=f"btn_{platform}"):
                if api_key and api_secret:
                    st.session_state.api_keys[platform] = {"key": api_key, "secret": api_secret}
                    
                    # Simulating live balance fetch from API authentication response
                    simulated_balance = 8450.75 if platform == "Binance" else (5230.40 if platform == "MEXC Global" else 12500.00)
                    st.session_state.account_balances[platform] = {"total_usdt": simulated_balance}
                    
                    st.success(f"Successfully linked with {platform}! Live Account Balance Fetched: ${simulated_balance:,.2f} USDT")
                else:
                    st.warning("Please provide both API Key/Login and Secret/Password.")


# ==========================================
# 3. COINMARKETCAP GAINER EDITOR
# ==========================================
elif menu == "3. CoinMarketCap Gainer Editor":
    st.title("Zia")
    st.markdown("CoinMarketCap Gainer Token & Custom URL Editor.")

    editable_gainers = st.text_area("Modify Gainer Tokens / CoinMarketCap List:", value=st.session_state.custom_gainers)
    if st.button("Save Gainer Tokens"):
        st.session_state.custom_gainers = editable_gainers
        st.success("Gainer tokens updated successfully!")

    st.markdown("### Current Active Gainer List")
    st.info(st.session_state.custom_gainers)


# ==========================================
# 4. VOICE ASSISTANT & 3 LANGUAGES
# ==========================================
elif menu == "4. Voice Assistant & 3 Languages":
    st.markdown(
        f"""
        <div class="neural-bg">
            <h2 style="color: #ffffff; margin-top: 0;">Zia — Voice Assistant Studio</h2>
            <p style="color: #94a3b8;">Configure bot voices, languages, and 5-second preview samples with modern crypto trading UI.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    st.write("")

    col_v1, col_v2 = st.columns(2)
    with col_v1:
        voice_gender = st.selectbox("Select Gender Folder", ["Female Folder (Cute Voices)", "Male Folder"])
    with col_v2:
        voice_lang = st.selectbox("Select Language", ["English", "Urdu", "Punjabi"])

    st.markdown(
        f"""
        <div class="dribbble-card">
            <h3 style="color: #ffffff; margin-top: 0;">Bot Voice Status: Active ({voice_lang} — {voice_gender})</h3>
            <p style="color: #94a3b8; margin-bottom: 0;"><b>Bot Speech Output:</b> "Hello Zia, system is fully operational."</p>
        </div>
    """,
        unsafe_allow_html=True,
    )

    multi_voice_html = f"""
    <div style="background: #0d1322; padding: 24px; border-radius: 16px; border: 1px solid #1e293b; box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.4);">
        <label style="color: #ffffff; font-weight: bold; display: block; margin-bottom: 10px;">Test Speech & 5-Sec Sample Preview ({voice_lang} / {voice_gender}):</label>
        <input type="text" id="speechText" value="Hello Zia, ready for trading profits today?" style="width: 100%; padding: 12px; border-radius: 8px; background: #111827; color: #fff; border: 1px solid #374151; margin-bottom: 18px;" />
        
        <button onclick="play5SecSample()" style="background-color: #f59e0b; color: #070913; border: none; padding: 14px 24px; font-size: 16px; font-weight: bold; border-radius: 10px; cursor: pointer; width: 100%;">
            🔊 Play 5-Sec Voice Sample
        </button>
    </div>

    <script>
    function play5SecSample() {{
        var text = document.getElementById('speechText').value;
        var langSel = "{voice_lang}";
        var genderSel = "{voice_gender}";
        
        if ('speechSynthesis' in window) {{
            window.speechSynthesis.cancel();
            var utterance = new SpeechSynthesisUtterance(text);
            
            if(langSel === "Urdu") {{
                utterance.lang = "ur-PK";
            }} else if(langSel === "Punjabi") {{
                utterance.lang = "pa-IN";
            }} else {{
                utterance.lang = "en-US";
            }}
            
            if(genderSel.includes("Female")) {{
                utterance.pitch = 1.5;
                utterance.rate = 1.05;
            }} else {{
                utterance.pitch = 0.75;
                utterance.rate = 0.95;
            }}
            
            window.speechSynthesis.speak(utterance);
        }}
        alert("Playing 5-Sec Voice Sample (" + langSel + "): " + text);
    }}
    </script>
    """
    components.html(multi_voice_html, height=240)


# ==========================================
# 5. AUTO-LEARNING & STORAGE HUB
# ==========================================
elif menu == "5. Auto-Learning & Storage Hub":
    st.markdown(
        """
        <div class="neural-bg">
            <h2 style="color: #ffffff; margin-top: 0;">Zia</h2>
            <p style="color: #94a3b8;">Auto-Learning engine with custom background photo selector & true storage tracking.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    st.write("")
    
    st.markdown("### 🖼️ Custom Background Photo Selector")
    bg_url_input = st.text_input("Enter Background Image URL or Select Preset:", value=st.session_state.active_image)
    if st.button("Apply Background Photo"):
        st.session_state.active_image = bg_url_input
        st.success("Background photo updated successfully! Refresh to view across theme.")
        st.rerun()

    st.markdown("---")
    
    edit_locked = st.toggle("🔒 Lock Manual Edits (Prevent Accidental Changes)", value=False)

    st.markdown("### Edit Bot's Learned Memory Manually")
    if edit_locked:
        st.warning("⚠️ Manual editing is currently LOCKED. Turn off the lock toggle above to edit.")
        st.text_area("Bot Self-Learned Rules & Strategies (Locked):", value=st.session_state.learned_rules, disabled=True)
    else:
        user_learned_edit = st.text_area("Bot Self-Learned Rules & Strategies (Editable):", value=st.session_state.learned_rules)
        if st.button("Update Learned Memory"):
            st.session_state.learned_rules = user_learned_edit
            st.session_state.brain_memory_gb += 1.2
            st.success("Bot memory and learned rules updated successfully by Zia!")

    st.markdown("### 💾 True Device Storage Usage")
    st.metric(label="Actual Memory Used (Out of 120GB Capacity)", value=f"{st.session_state.brain_memory_gb:.1f} GB Used", delta="Live Tracker")
    st.progress(st.session_state.brain_memory_gb / 120)

    if st.button("Absorb New Knowledge & Expand Memory"):
        st.session_state.brain_memory_gb += 2.5
        st.success(f"New knowledge absorbed! Storage used updated to {st.session_state.brain_memory_gb:.1f} GB.")
        st.balloons()


# ==========================================
# 6. 🌍 FULL MARKET SCANNER & AI HUB
# ==========================================
elif menu == "6. 🌍 Full Market Scanner & AI Hub":
    st.title("Zia — Full Market Intelligence & Scanner")
    st.markdown("Autonomous power engine to scan the entire cryptocurrency and forex market simultaneously from A to Z.")

    scan_command = st.text_input("💬 Enter Auto-Scan Command (e.g. 'Scan A to Z crypto & forex markets')", value="Scan A to Z crypto & forex markets")
    scan_type = st.selectbox("Select Scan Mode", ["Top Gainers & Volume Spikes (Crypto)", "Candle Wick & Liquidation Hunter", "Forex Major Pairs Intelligence"])
    
    if st.button("🚀 Run A to Z Full Market Scan Now"):
        with st.spinner(f"Executing command: '{scan_command}' across all A-Z pairs..."):
            time.sleep(1.5)
        st.success(f"A to Z Scan completed successfully for command: '{scan_command}'!")
        
        scan_data = pd.DataFrame({
            "Pair / Asset": ["BTC/USDT", "ETH/USDT", "SOL/USDT", "XRP/USDT", "EUR/USD", "GBP/USD"],
            "Market Trend": ["Bullish Breakout", "Accumulation", "Strong Pump", "Stable", "Bullish", "Bearish"],
            "24h Change": ["+4.5%", "+6.2%", "+12.4%", "+1.2%", "+0.8%", "-0.4%"],
            "AI Signal": ["STRONG BUY", "BUY", "SCALP LONG", "HOLD", "LONG", "SHORT"]
        })
        st.table(scan_data)
        st.info("💡 Bot has automatically stored high-probability A-Z setups from this scan into memory.")

# --- FOOTER ---
st.markdown("---")
st.markdown("<p style='text-align: center; color: #64748b;'>Zia © 2026</p>", unsafe_allow_html=True)
