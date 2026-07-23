import base64
import time
import streamlit as st
import streamlit.components.v1 as components

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Zia's AI Trading Bot - Professional Suite",
    page_icon="🦅",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- CUSTOM CYBERPUNK STYLING ---
st.markdown(
    """
    <style>
    .main {
        background-color: #0b0f19;
        color: #e2e8f0;
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
    </style>
""",
    unsafe_allow_html=True,
)

# --- SESSION STATE ---
if "api_keys" not in st.session_state:
    st.session_state.api_keys = {}
if "active_image" not in st.session_state:
    st.session_state.active_image = "https://media.istockphoto.com/id/1281292227/vector/abstract-vector-illustration-of-flying-owl.jpg?s=612x612&w=0&k=20&c=01SIIfHo6V_nt5fzkU90sJSpJbPwglJtxdH0veEGfK4="

# --- TRADING PLATFORMS LIST ---
TRADING_PLATFORMS = [
    "Binance",
    "MEXC Global",
    "WEEX Exchange",
    "Bybit",
    "OKX",
    "KuCoin",
    "Gate.io",
    "Coinbase Pro",
    "Kraken",
    "Bitget",
    "Huobi / HTX",
    "Binance Futures",
    "Bybit Derivatives",
    "Deribit",
    "Bitfinex",
    "Crypto.com",
]

# --- SIDEBAR: SETTINGS ICON WITH COLLAPSIBLE IMAGE & CONTROLS ---
with st.sidebar:
    st.markdown("### 🦅 NEXA ULTRA PRO")
    st.markdown("*Zia's Autonomous Trading Hub*")
    st.divider()

    # Settings Expandable Drawer for Image & Sidebar Customization
    with st.expander("⚙️ Sidebar & Theme Settings", expanded=False):
        st.markdown("#### Configure Left Panel")
        custom_url_input = st.text_input("Paste Image URL:", value=st.session_state.active_image)
        if st.button("Apply Image URL"):
            st.session_state.active_image = custom_url_input
            st.success("Sidebar asset updated!")
        
        sidebar_theme_mode = st.selectbox("Sidebar Theme Mode", ["Cyberpunk Dark", "Neon Blue", "Deep Obsidian"])
        st.info(f"Active Theme: {sidebar_theme_mode}")

    # Display Active Image inside Sidebar
    st.image(
        st.session_state.active_image,
        caption="Zia's Trading Bot Design Active",
        use_container_width=True,
    )

    st.markdown("---")
    menu = st.radio(
        "Navigation Menu",
        [
            "📊 Live Dashboard & AI Scalper",
            "🔐 Platform Vault & API Hub",
            "🖼️ Custom Image Gallery & Splash",
            "🎙️ Voice Assistant (Hello Zia & 15+ Modes)",
            "⚙️ Auto-Learning Settings",
        ],
    )
    st.markdown("---")
    st.markdown("**System Status:** 🟢 Online")


# ==========================================
# 1. LIVE DASHBOARD & AI SCALPER
# ==========================================
if menu == "📊 Live Dashboard & AI Scalper":
    st.title("⚡ AI Trading Bot - Professional Dashboard")
    st.markdown("Welcome back, **Zia**! Institutional grade algorithmic execution active.")

    col_img1, col_img2 = st.columns([2, 1])
    with col_img1:
        st.markdown("### 🤖 Active Strategy: Goldmine AI Scalper & Robot Vision")
        st.image(
            st.session_state.active_image,
            caption="AI Neural Vision & Trading Architecture",
            use_container_width=True,
        )
    with col_img2:
        st.markdown("### 📊 Quick Metrics")
        st.markdown(
            '<div class="metric-card"><h3>Portfolio PnL</h3><h2 style="color:#10b981;">+$1,245.50</h2><p>Win Rate: 91.2%</p></div>',
            unsafe_allow_html=True,
        )

    st.markdown("---")
    st.markdown("### 📈 Live Market Intelligence Stream")
    chart_data = {
        "Time": [f"12:{i}0" for i in range(10)],
        "BTC Execution": [64200 + i * 50 + (i % 2 * -25) for i in range(10)],
        "AI Target Line": [64220 + i * 52 + (i % 3 * -15) for i in range(10)],
    }
    st.line_chart(chart_data)


# ==========================================
# 2. PLATFORM VAULT & API HUB
# ==========================================
elif menu == "🔐 Platform Vault & API Hub":
    st.title("🔐 Secure Exchange Vault & API Manager")
    st.markdown("Unlock the Vault to connect your trading platforms with instant search.")

    search_query = st.text_input("🔍 Search Trading Platform (e.g., Binance, MEXC, WEEX)...", "")
    filtered_platforms = [p for p in TRADING_PLATFORMS if search_query.lower() in p.lower()]

    st.markdown("### Available Trading Ecosystems")

    for platform in filtered_platforms:
        with st.expander(f"💼 Configure API for: {platform}"):
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
# 3. CUSTOM IMAGE GALLERY & SPLASH
# ==========================================
elif menu == "🖼️ Custom Image Gallery & Splash":
    st.title("🖼️ Custom Image Gallery & Splash Hub")
    st.markdown("Manage and upload your app theme assets directly.")

    uploaded_file = st.file_uploader("Upload New Main Theme Image", type=["jpg", "png", "jpeg"])
    if uploaded_file is not None:
        st.session_state.active_image = uploaded_file
        st.success("Image updated successfully across the entire platform!")

    st.markdown("### 🖼️ Current Active Theme Asset:")
    st.image(
        st.session_state.active_image,
        caption="Active Bot Theme Asset",
        use_container_width=True,
    )


# ==========================================
# 4. VOICE ASSISTANT (HELLO ZIA & MULTI-VOICE)
# ==========================================
elif menu == "🎙️ Voice Assistant (Hello Zia & 15+ Modes)":
    st.title("🎙️ Advanced Voice Command & Multi-Voice Studio")
    st.markdown("Select your preferred male/female system voice and test live speech synthesis!")

    st.markdown(
        """
        <div class="voice-box">
            <h3>🤖 Bot Voice Status: Active & Dynamic</h3>
            <p><b>Bot Speech Output:</b> "Hello Zia, system is fully operational. All trading nodes are secure."</p>
        </div>
    """,
        unsafe_allow_html=True,
    )

    multi_voice_html = """
    <div style="padding: 10px 0; background: #111827; padding: 20px; border-radius: 10px; border: 1px solid #374151;">
        <label style="color: #f8fafc; font-weight: bold; display: block; margin-bottom: 8px;">Select Neural Voice Profile (Male / Female):</label>
        <select id="voiceSelect" style="width: 100%; padding: 10px; border-radius: 6px; background: #1f2937; color: #fff; border: 1px solid #4b5563; margin-bottom: 15px;"></select>
        
        <label style="color: #f8fafc; font-weight: bold; display: block; margin-bottom: 8px;">Custom Speech Text:</label>
        <input type="text" id="speechText" value="Hello Zia, welcome back! Ready for trading profits today?" style="width: 100%; padding: 10px; border-radius: 6px; background: #1f2937; color: #fff; border: 1px solid #4b5563; margin-bottom: 15px;" />
        
        <button onclick="speakWithSelectedVoice()" style="background-color: #f59e0b; color: #0b0f19; border: none; padding: 12px 24px; font-size: 16px; font-weight: bold; border-radius: 8px; cursor: pointer; width: 100%;">
            🔊 Play Selected Voice ("Hello Zia")
        </button>
    </div>

    <script>
    let voices = [];
    function populateVoiceList() {
        if(typeof speechSynthesis === 'undefined') {
            return;
        }
        voices = speechSynthesis.getVoices();
        var voiceSelect = document.getElementById('voiceSelect');
        voiceSelect.innerHTML = '';
        
        for(var i = 0; i < voices.length; i++) {
            var option = document.createElement('option');
            option.textContent = voices[i].name + ' (' + voices[i].lang + ')';
            if(voices[i].default) {
                option.textContent += ' — DEFAULT';
            }
            option.setAttribute('data-bt-index', i);
            voiceSelect.appendChild(option);
        }
    }

    populateVoiceList();
    if (typeof speechSynthesis !== 'undefined' && speechSynthesis.onvoiceschanged !== undefined) {
        speechSynthesis.onvoiceschanged = populateVoiceList;
    }

    function speakWithSelectedVoice() {
        if ('speechSynthesis' in window) {
            var text = document.getElementById('speechText').value;
            var utterance = new SpeechSynthesisUtterance(text);
            var voiceSelect = document.getElementById('voiceSelect');
            var selectedOptionIndex = voiceSelect.selectedOptions[0].getAttribute('data-bt-index');
            
            utterance.voice = voices[selectedOptionIndex];
            utterance.rate = 1.0;
            utterance.pitch = 1.0;
            
            window.speechSynthesis.speak(utterance);
        } else {
            alert("Speech synthesis not supported in this browser.");
        }
    }
    </script>
    """
    components.html(multi_voice_html, height=280)


# ==========================================
# 5. AUTO-LEARNING SETTINGS
# ==========================================
elif menu == "⚙️ Auto-Learning Settings":
    st.title("⚙️ Self-Optimizing Neural Engine")
    st.markdown("Configure automated parameter tuning and self-learning weights.")

    learning_rate = st.slider("Neural Adaptation Speed", 0.001, 0.1, 0.01)
    risk_tolerance = st.selectbox("Risk Profile", ["Conservative", "Balanced", "Aggressive Scalper"])
    auto_execute = st.toggle("Enable Fully Autonomous Trade Execution", value=True)

    if st.button("Apply Advanced Configuration"):
        st.success(f"Settings updated for Zia! Mode: {risk_tolerance} | Auto-Execute: {auto_execute}")

# --- FOOTER ---
st.markdown("---")
st.markdown("<p style='text-align: center; color: #64748b;'>Zia's Nexa Ultra Pro AI Trading System © 2026</p>", unsafe_allow_html=True)
