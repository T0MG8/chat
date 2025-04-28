import time
import streamlit as st
import pandas as pd
from streamlit_js_eval import get_geolocation
from streamlit_autorefresh import st_autorefresh

# --- Initialiseer session state ---
if 'tracking' not in st.session_state:
    st.session_state.tracking = False
if 'df' not in st.session_state:
    st.session_state.df = pd.DataFrame(columns=['timestamp', 'latitude', 'longitude'])
if 'location_permission' not in st.session_state:
    st.session_state.location_permission = False

# --- Header ---
st.title("🌍 Live locatie‐tracker")

# --- Probeer locatie te verkrijgen ---
loc = get_geolocation()

# --- Controleer of locatie beschikbaar is ---
if loc and 'lat' in loc and 'lon' in loc:
    st.session_state.location_permission = True

# --- Als nog geen toestemming is gegeven ---
if not st.session_state.location_permission:
    st.warning("⚠️ Geef eerst toestemming voor locatietoegang bovenin je browser!")
    st.stop()

# --- Buttons om tracking te starten / te stoppen ---
col1, col2 = st.columns(2)
if col1.button("▶️ Start tracking"):
    st.session_state.tracking = True
if col2.button("⏹️ Stop tracking"):
    st.session_state.tracking = False

# --- Als we tracken: refresh elke 5 seconden ---
if st.session_state.tracking:
    st_autorefresh(interval=5000, limit=None, key="auto")

    # Opnieuw ophalen na autorefresh
    loc = get_geolocation()
    if loc and 'lat' in loc and 'lon' in loc:
        ts = time.strftime('%Y-%m-%d %H:%M:%S')
        new_row = {
            'timestamp': ts,
            'latitude': loc['lat'],
            'longitude': loc['lon']
        }
        st.session_state.df = pd.concat(
            [st.session_state.df, pd.DataFrame([new_row])],
            ignore_index=True
        )
    st.success(f"✅ Tracking actief — laatste update: {time.strftime('%H:%M:%S')}")

# --- Toon DataFrame met alle punten ---
st.subheader("📋 Gearchiveerde locaties")
st.dataframe(st.session_state.df)

# --- Kaart weergave ---
if not st.session_state.df.empty:
    st
