"""
Paper Trading Dashboard (SIMULATION ONLY)
==========================================
Real live market prices are pulled from Binance's PUBLIC market-data API
(no API key / no login needed, no real funds ever touched).

All "trades" placed in this app are simulated in-memory. NOTHING is ever
sent to a real exchange. There is no self-learning AI here — this is a
transparent rule-based paper-trading simulator so you can practice and
track a strategy's performance honestly, with real numbers.

Run with:
    pip install streamlit requests pandas --break-system-packages
    streamlit run paper_trading_dashboard.py
"""

import time
import requests
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Paper Trading Dashboard (Simulation)", page_icon="📈", layout="wide")

BINANCE_TICKER_URL = "https://api.binance.com/api/v3/ticker/24hr"
BINANCE_PRICE_URL = "https://api.binance.com/api/v3/ticker/price"

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
st.caption("⚠️ This is a paper-trading simulator for practice and tracking only. "
           "It does not connect to any real exchange account, does not use real funds, "
           "and does not place real orders. Nothing here is financial advice.")
