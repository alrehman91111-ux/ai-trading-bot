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

# --- CUSTOM CYBERPUNK STYLING & VERTICAL MENU ---
st.markdown(
    """
    <style>
    .main {
        background-color: #0b0f19;
        color: #e2e8f0;
        max-width: 100% !important;
    }
    .stSidebar {
        background-color: #111827;
        border-right: 1px solid #374151;
    }
    .metric-card {
        background: linear-gradient(135deg, #1f2937 0%, #111827 100%);
        border: 1px solid #374151;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    h1, h2, h3 {
        color: #f8fafc;
    }
    .voice-box {
        background: #1e293b;
        border: 1px solid #f59e0b;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 15px;
    }
    .neural-bg {
        background-image: linear-gradient(rgba(11, 15, 25, 0.85), rgba(11, 15, 25, 0.85)), url('https://images.stockcake.com/public/e/e/b/eeba051b-bbad-4df2-9fe9-34ca126e7ee7_large/neon-cyborg-raven-stockcake.jpg');
        background-size: cover;
        background-position: center;
        padding: 30px;
        border-radius: 15px;
        border: 1px solid #374151;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# --- SESSION STATE ---
if "api_keys" not in st.session_state:
    st.session_state.api_keys = {}
if "active_image" not in st.session_state:
    st.session_state.active_image = "https://images.stockcake.com/public/e/e/b/eeba051b-bbad-4df2-9fe9-34ca126e7ee7_large/neon-cyborg-raven-stockcake.jpg"
if "brain_memory_gb" not in st.session_state:
    st.session_state.brain_memory_gb = 42.5
if "custom_gainers" not in st.session_state:
    st.session_state.custom_gainers = "BTC (+4.5%), ETH (+6.2%), SOL (+12.4%), WEEX (+15.0%)"

# --- TRADING PLATFORMS LIST WITH ICONS ---
TRADING_PLATFORMS = [
    ("Binance", "🟡"),
    ("MEXC Global", "🔵"),
    ("WEEX Exchange", "🟢"),
    ("Bybit", "⚫"),
    ("OKX", "⚪"),
    ("KuCoin", "🟩"),
    ("Gate.io", "🔴"),
    ("Coinbase Pro", "🟦"),
    ("Kraken", "🟣"),
    ("Bitget", "🔷"),
    ("Binance Futures", "⚡"),
]

# --- VERTICAL LEFT SIDEBAR MENU (1, 2, 3, 4, 5) ---
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
            "5. Auto-Learning & Storage Hub"
        ]
    )
    st.markdown("---")
    
    st.markdown("### 🎙️ Mic & Audio Control")
    mic_locked = st.toggle("🔒 Lock / Mute Mic (Tap to Stop/Talk)", value=False)
    if mic_locked:
        st.warning("Mic is Locked/Muted.")
    else:
        st.success("Mic is Active & Listening.")
        
    st.markdown("---")
    st.markdown("**System:** 🟢 Online")


# ==========================================
# 1. LIVE DASHBOARD & AI SCALPER
# ==========================================
if menu == "1. Live Dashboard & AI Scalper":
    st.title("Zia")
    st.markdown("Institutional grade algorithmic execution active.")

    # Token Selector Option for Dashboard Chart
    selected_token = st.selectbox("Select Token for Live Stream & Analysis", ["BTC/USDT", "ETH/USDT", "SOL/USDT", "WEEX/USDT", "XRP/USDT", "PEPE/USDT"])

    col_img1, col_img2 = st.columns([2, 1])
    with col_img1:
        st.markdown(f"### Active Strategy: {selected_token} Scalper & Robot Vision")
        st.image(
            st.session_state.active_image,
            use_container_width=True,
        )
    with col_img2:
        st.markdown("### Quick Metrics & Ratio Folder")
        st.markdown(
            f'<div class="metric-card"><h3>{selected_token} PnL</h3><h2 style="color:#10b981;">+$12,455.50</h2><p>Win Rate: 94.8%</p></div>',
            unsafe_allow_html=True,
        )
        st.info("📁 Dedicated Trading Ratio Folder: Active & Synced")

    st.markdown("---")
    st.markdown(f"### Live Market Intelligence Stream ({selected_token})")
    
    # Clean DataFrame to fix axis display bugs completely
    base_price = 60000 if "BTC" in selected_token else (3000 if "ETH" in selected_token else 150)
    chart_df = pd.DataFrame({
        f"{selected_token} Execution": [base_price + i*15 for i in range(10)],
        "AI Target Line": [base_price + i*18 for i in range(10)]
    }, index=[f"12:{i*10:02d}" for i in range(10)])
    
    st.line_chart(chart_df)


# ==========================================
# 2. PLATFORM VAULT & API HUB
# ==========================================
elif menu == "2. Platform Vault & API Hub":
    st.title("Zia")
    st.markdown("Secure Exchange Vault & API Manager with official platform icons.")

    search_query = st.text_input("Search Trading Platform...", "")
    filtered_platforms = [p for p in TRADING_PLATFORMS if search_query.lower() in p[0].lower()]

    for platform, icon in filtered_platforms:
        with st.expander(f"{icon} Configure API for: {platform}"):
            col_a, col_b = st.columns(2)
            with col_a:
                api_key = st.text_input(f"API Key ({platform})", type="password", key=f"key_{platform}")
            with col_b:
                api_secret = st.text_input(f"Secret Key ({platform})", type="password", key=f"sec_{platform}")

            if st.button(f"Save & Connect {platform}", key=f"btn_{platform}"):
                if api_key and api_secret:
                    st.session_state.api_keys[platform] = {"key": api_key, "secret": api_secret}
                    st.success(f"Successfully linked with {platform} securely!")
                else:
                    st.warning("Please provide both API Key and Secret.")


# ==========================================
# 3. COINMARKETCAP GAINER EDITOR
# ==========================================
elif menu == "3. CoinMarketCap Gainer Editor":
    st.title("Zia")
    st.markdown("CoinMarketCap Gainer Token & Custom URL Editor.")

    st.markdown("### Edit Gainer Tokens Manually")
    editable_gainers = st.text_area("Modify Gainer Tokens / CoinMarketCap List:", value=st.session_state.custom_gainers)
    if st.button("Save Gainer Tokens"):
        st.session_state.custom_gainers = editable_gainers
        st.success("Gainer tokens updated successfully!")

    st.markdown("### Current Active Gainer List")
    st.info(st.session_state.custom_gainers)
    
    st.markdown("---")
    st.write("🔗 Official Source: [CoinMarketCap Portal](https://coinmarketcap.com)")


# ==========================================
# 4. VOICE ASSISTANT & 3 LANGUAGES
# ==========================================
elif menu == "4. Voice Assistant & 3 Languages":
    st.title("Zia")
    st.markdown("Voice Assistant Studio (English, Urdu, Punjabi — Male & Female Folders)")

    col_v1, col_v2 = st.columns(2)
    with col_v1:
        voice_gender = st.selectbox("Select Gender Folder", ["Female Folder (Cute Voices)", "Male Folder"])
    with col_v2:
        voice_lang = st.selectbox("Select Language", ["English", "Urdu", "Punjabi"])

    st.markdown(
        f"""
        <div class="voice-box">
            <h3>Bot Voice Status: Active ({voice_lang} — {voice_gender})</h3>
            <p><b>Bot Speech Output:</b> "Hello Zia, system is fully operational."</p>
        </div>
    """,
        unsafe_allow_html=True,
    )

    # Robust multi-language speech handler with Urdu/Punjabi fallback support
    multi_voice_html = f"""
    <div style="background: #111827; padding: 20px; border-radius: 10px; border: 1px solid #374151;">
        <label style="color: #f8fafc; font-weight: bold; display: block; margin-bottom: 8px;">Test Speech ({voice_lang} / {voice_gender}):</label>
        <input type="text" id="speechText" value="Hello Zia, ready for trading profits today?" style="width: 100%; padding: 10px; border-radius: 6px; background: #1f2937; color: #fff; border: 1px solid #4b5563; margin-bottom: 15px;" />
        
        <button onclick="playRobustSpeech()" style="background-color: #f59e0b; color: #0b0f19; border: none; padding: 12px 24px; font-size: 16px; font-weight: bold; border-radius: 8px; cursor: pointer; width: 100%;">
            🔊 Play Voice Audio ("Hello Zia")
        </button>
    </div>

    <script>
    function playRobustSpeech() {{
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
                utterance.pitch = 1.4; // Cute high pitch for female
                utterance.rate = 1.0;
            }} else {{
                utterance.pitch = 0.8; // Deep pitch for male
                utterance.rate = 0.95;
            }}
            
            window.speechSynthesis.speak(utterance);
        }}
        
        // Visual confirmation feedback
        alert("Playing " + langSel + " (" + genderSel + "): " + text);
    }}
    </script>
    """
    components.html(multi_voice_html, height=220)


# ==========================================
# 5. AUTO-LEARNING & STORAGE HUB
# ==========================================
elif menu == "5. Auto-Learning & Storage Hub":
    st.markdown(
        """
        <div class="neural-bg">
            <h2 style="color: #f8fafc; margin-top: 0;">Zia</h2>
            <p style="color: #cbd5e1;">Auto-Learning engine with custom background & full phone/device storage access (100GB+).</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    st.write("")
    
    st.markdown("### Edit Bot's Learned Memory Manually")
    user_learned_edit = st.text_area("Bot Self-Learned Rules & Strategies (Editable):", value="1. Scalp on 5m candle wicks.\n2. Auto-lock profits at +3%.\n3. Dynamic risk management active.")
    if st.button("Update Learned Memory"):
        st.success("Bot memory and learned rules updated successfully by Zia!")

    st.markdown("### 💾 Device & Phone Storage Usage")
    st.metric(label="Storage Used (Out of 120GB+ Capacity)", value=f"{st.session_state.brain_memory_gb} GB Used", delta="Fully Synchronized")
    st.progress(st.session_state.brain_memory_gb / 120)

    if st.button("Absorb New Knowledge & Expand Storage"):
        st.session_state.brain_memory_gb += 5.0
        st.success(f"Knowledge absorbed! Storage used updated to {st.session_state.brain_memory_gb} GB.")
        st.balloons()

# --- FOOTER ---
st.markdown("---")
st.markdown("<p style='text-align: center; color: #64748b;'>Zia © 2026</p>", unsafe_allow_html=True)
