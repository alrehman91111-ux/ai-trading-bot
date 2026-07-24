er trading dashboard · PY
"""
Paper Trading Dashboard (SIMULATION ONLY)
==========================================
Real live market prices are pulled from Binance's PUBLIC market-data API
(no API key / no login needed, no real funds ever touched).
 
Optionally, you can also check your REAL Binance account balance using a
genuine HMAC-signed, read-only API call — this requires a "read only"
API key (no trading/withdrawal permission) and never places any order.
 
All "trades" placed in this app are simulated in-memory. NOTHING is ever
sent to a real exchange, no matter what is shown in the balance checker.
There is no self-learning AI here — this is a transparent rule-based
paper-trading simulator so you can practice and track a strategy's
performance honestly, with real numbers.
 
Run with:
    pip install streamlit requests pandas --break-system-packages
    streamlit run paper_trading_dashboard.py
"""
 
import time
import hmac
import hashlib
import urllib.parse
import requests
import pandas as pd
import streamlit as st
 
st.set_page_config(page_title="Paper Trading Dashboard (Simulation)", page_icon="📈", layout="wide")
 
BINANCE_TICKER_URL = "https://api.binance.com/api/v3/ticker/24hr"
BINANCE_PRICE_URL = "https://api.binance.com/api/v3/ticker/price"
BINANCE_ACCOUNT_URL = "https://api.binance.com/api/v3/account"
 
DEFAULT_PAIRS = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "XRPUSDT", "BNBUSDT"]
 
# ---------------------------------------------------------------------
# SESSION STATE (in-memory only — resets when the app restarts)
# ---------------------------------------------------------------------
if "paper_balance" not in st.session_state:
    st.session_state.paper_balance = 1000.0  # starting fake balance, user-editable
if "paper_positions" not in st.session_state:
    st.session_state.paper_positions = {}  # symbol -> {"qty": float, "avg_price": float}
if "trade_log" not in st.session_state:
    st.session_state.trade_log = []
if "real_balances" not in st.session_state:
    st.session_state.real_balances = None  # only populated after a genuine, successful API call
if "real_balance_error" not in st.session_state:
    st.session_state.real_balance_error = None
 
 
# ---------------------------------------------------------------------
# REAL ACCOUNT BALANCE (read-only) — genuine HMAC-signed Binance call.
# This section makes NO trades and requires only "Enable Reading"
# permission on the API key. It never uses withdrawal permissions.
# ---------------------------------------------------------------------
def fetch_real_binance_balances(api_key: str, api_secret: str):
    """
    Calls Binance's authenticated /api/v3/account endpoint (read-only data)
    using a proper HMAC-SHA256 signature, exactly as Binance requires.
    Returns (balances_list, error_message). Only non-zero balances are kept.
    """
    try:
        timestamp = int(time.time() * 1000)
        query_string = f"timestamp={timestamp}&recvWindow=5000"
        signature = hmac.new(
            api_secret.encode("utf-8"),
            query_string.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
        url = f"{BINANCE_ACCOUNT_URL}?{query_string}&signature={signature}"
        headers = {"X-MBX-APIKEY": api_key}
 
        resp = requests.get(url, headers=headers, timeout=8)
        if resp.status_code != 200:
            try:
                msg = resp.json().get("msg", resp.text)
            except Exception:
                msg = resp.text
            return None, f"Binance rejected the request (HTTP {resp.status_code}): {msg}"
 
        data = resp.json()
        balances = [
            {"Asset": b["asset"], "Free": float(b["free"]), "Locked": float(b["locked"])}
            for b in data.get("balances", [])
            if float(b["free"]) > 0 or float(b["locked"]) > 0
        ]
        return balances, None
    except requests.exceptions.RequestException as e:
        return None, f"Network error contacting Binance: {e}"
    except Exception as e:
        return None, f"Unexpected error: {e}"
 
 
# ---------------------------------------------------------------------
# DATA FETCHING (real market data, read-only, public endpoint)
# ---------------------------------------------------------------------
@st.cache_data(ttl=10)
def fetch_prices(symbols):
    """Fetch real live prices + 24h stats from Binance's public API."""
    try:
        resp = requests.get(BINANCE_TICKER_URL, timeout=5)
        resp.raise_for_status()
        data = {row["symbol"]: row for row in resp.json()}
        rows = []
        for s in symbols:
            if s in data:
                rows.append({
                    "Symbol": s,
                    "Price": float(data[s]["lastPrice"]),
                    "24h Change %": float(data[s]["priceChangePercent"]),
                    "24h High": float(data[s]["highPrice"]),
                    "24h Low": float(data[s]["lowPrice"]),
                    "24h Volume": float(data[s]["volume"]),
                })
        return pd.DataFrame(rows)
    except Exception as e:
        st.error(f"Could not fetch live prices from Binance: {e}")
        return pd.DataFrame()
 
 
def get_single_price(symbol):
    try:
        resp = requests.get(BINANCE_PRICE_URL, params={"symbol": symbol}, timeout=5)
        resp.raise_for_status()
        return float(resp.json()["price"])
    except Exception as e:
        st.error(f"Price fetch failed: {e}")
        return None
 
 
# ---------------------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------------------
with st.sidebar:
    st.title("📈 Paper Trading")
    st.caption("SIMULATION MODE — no real money, no exchange account is ever touched.")
    st.divider()
    st.metric("Simulated Cash Balance", f"${st.session_state.paper_balance:,.2f}")
    if st.button("Reset Simulation"):
        st.session_state.paper_balance = 1000.0
        st.session_state.paper_positions = {}
        st.session_state.trade_log = []
        st.rerun()
    st.divider()
    st.caption("Prices are real, live data from Binance's public market API. "
               "Everything else on this page is a simulation for practice/tracking only.")
 
st.title("Paper Trading Dashboard")
st.markdown("Practice a strategy against **real live prices** with **fake money**, and keep an honest record of how it performs.")
 
# ---------------------------------------------------------------------
# REAL BALANCE CHECKER (read-only, optional)
# ---------------------------------------------------------------------
with st.expander("🔐 Check My Real Binance Balance (read-only, optional)"):
    st.markdown(
        "This only **reads** your account balances — it never places, modifies, or cancels "
        "any real order, and it never touches withdrawals.\n\n"
        "**Before using this:** on Binance, create an API key with **only** the "
        "\"Enable Reading\" permission turned on, and leave \"Enable Spot & Margin Trading\" "
        "and \"Enable Withdrawals\" **off**. That way, even if something went wrong, this key "
        "physically cannot move your funds."
    )
    rb_col1, rb_col2 = st.columns(2)
    with rb_col1:
        real_api_key = st.text_input("Binance API Key", type="password", key="real_api_key")
    with rb_col2:
        real_api_secret = st.text_input("Binance API Secret", type="password", key="real_api_secret")
 
    st.caption("Keys are kept only in this browser session's memory — they are not written to disk, "
               "logged, or sent anywhere except directly to Binance's own API.")
 
    if st.button("Fetch My Real Balance"):
        if not real_api_key or not real_api_secret:
            st.warning("Please enter both the API key and secret.")
        else:
            with st.spinner("Contacting Binance..."):
                balances, error = fetch_real_binance_balances(real_api_key, real_api_secret)
            if error:
                st.session_state.real_balances = None
                st.session_state.real_balance_error = error
            else:
                st.session_state.real_balances = balances
                st.session_state.real_balance_error = None
 
    if st.session_state.real_balance_error:
        st.error(st.session_state.real_balance_error)
 
    if st.session_state.real_balances is not None:
        if st.session_state.real_balances:
            st.success("Real balances fetched directly from your Binance account:")
            st.dataframe(pd.DataFrame(st.session_state.real_balances).style.format(
                {"Free": "{:,.8f}", "Locked": "{:,.8f}"}
            ), use_container_width=True)
        else:
            st.info("Connected successfully, but no non-zero balances were found on this account.")
 
# ---------------------------------------------------------------------
# LIVE MARKET TABLE
# ---------------------------------------------------------------------
st.subheader("Live Market Prices (real data, read-only)")
price_df = fetch_prices(DEFAULT_PAIRS)
if not price_df.empty:
    st.dataframe(price_df.style.format({
        "Price": "${:,.2f}", "24h Change %": "{:+.2f}%",
        "24h High": "${:,.2f}", "24h Low": "${:,.2f}", "24h Volume": "{:,.0f}"
    }), use_container_width=True)
else:
    st.warning("No live data available right now.")
 
st.divider()
 
# ---------------------------------------------------------------------
# SIMULATED ORDER FORM
# ---------------------------------------------------------------------
st.subheader("Place a Simulated Order")
col1, col2, col3, col4 = st.columns(4)
with col1:
    symbol = st.selectbox("Pair", DEFAULT_PAIRS)
with col2:
    side = st.selectbox("Side", ["BUY", "SELL"])
with col3:
    usd_amount = st.number_input("Amount (USD, simulated)", min_value=1.0, value=50.0, step=10.0)
with col4:
    st.write("")
    st.write("")
    place = st.button("Execute Simulated Order")
 
if place:
    live_price = get_single_price(symbol)
    if live_price is None:
        st.error("Could not get a live price — order not placed.")
    else:
        qty = usd_amount / live_price
        pos = st.session_state.paper_positions.get(symbol, {"qty": 0.0, "avg_price": 0.0})
 
        if side == "BUY":
            if usd_amount > st.session_state.paper_balance:
                st.error("Insufficient simulated balance for this order.")
            else:
                new_qty = pos["qty"] + qty
                pos["avg_price"] = ((pos["qty"] * pos["avg_price"]) + (qty * live_price)) / new_qty if new_qty else live_price
                pos["qty"] = new_qty
                st.session_state.paper_positions[symbol] = pos
                st.session_state.paper_balance -= usd_amount
                st.session_state.trade_log.insert(0, {
                    "Time": time.strftime("%H:%M:%S"), "Pair": symbol, "Side": "BUY",
                    "Price": live_price, "Qty": qty, "USD": usd_amount
                })
                st.success(f"Simulated BUY: {qty:.6f} {symbol} at ${live_price:,.2f}")
 
        else:  # SELL
            if pos["qty"] * live_price < usd_amount - 1e-9 or pos["qty"] <= 0:
                st.error("Not enough simulated position in this pair to sell that amount.")
            else:
                pos["qty"] -= qty
                st.session_state.paper_positions[symbol] = pos
                st.session_state.paper_balance += usd_amount
                st.session_state.trade_log.insert(0, {
                    "Time": time.strftime("%H:%M:%S"), "Pair": symbol, "Side": "SELL",
                    "Price": live_price, "Qty": qty, "USD": usd_amount
                })
                st.success(f"Simulated SELL: {qty:.6f} {symbol} at ${live_price:,.2f}")
 
st.divider()
 
# ---------------------------------------------------------------------
# POSITIONS & PERFORMANCE (honest, calculated — not decorative)
# ---------------------------------------------------------------------
st.subheader("Open Simulated Positions")
positions_rows = []
total_position_value = 0.0
for sym, pos in st.session_state.paper_positions.items():
    if pos["qty"] > 1e-9:
        cur_price = get_single_price(sym) or pos["avg_price"]
        value = pos["qty"] * cur_price
        pnl = value - (pos["qty"] * pos["avg_price"])
        total_position_value += value
        positions_rows.append({
            "Pair": sym, "Qty": pos["qty"], "Avg Entry": pos["avg_price"],
            "Current Price": cur_price, "Value": value, "Unrealized P/L": pnl
        })
 
if positions_rows:
    st.dataframe(pd.DataFrame(positions_rows).style.format({
        "Qty": "{:.6f}", "Avg Entry": "${:,.2f}", "Current Price": "${:,.2f}",
        "Value": "${:,.2f}", "Unrealized P/L": "{:+,.2f}"
    }), use_container_width=True)
else:
    st.info("No open simulated positions yet.")
 
total_equity = st.session_state.paper_balance + total_position_value
c1, c2, c3 = st.columns(3)
c1.metric("Cash", f"${st.session_state.paper_balance:,.2f}")
c2.metric("Position Value", f"${total_position_value:,.2f}")
c3.metric("Total Simulated Equity", f"${total_equity:,.2f}", delta=f"{total_equity - 1000.0:+,.2f}")
 
st.divider()
 
# ---------------------------------------------------------------------
# TRADE HISTORY
# ---------------------------------------------------------------------
st.subheader("Simulated Trade History")
if st.session_state.trade_log:
    hist_df = pd.DataFrame(st.session_state.trade_log)
    st.dataframe(hist_df.style.format({"Price": "${:,.2f}", "Qty": "{:.6f}", "USD": "${:,.2f}"}),
                 use_container_width=True)
else:
    st.info("No simulated trades placed yet.")
 
st.markdown("---")
st.caption("⚠️ Trading on this page is simulated for practice and tracking only — it does not "
           "place real orders. The optional balance checker above makes a genuine read-only call "
           "to your real Binance account if you choose to use it, but still cannot trade or "
           "withdraw funds. Nothing here is financial advice.")
