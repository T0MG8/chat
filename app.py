import streamlit as st
import pandas as pd
import datetime

# Initialiseer session state
if "tracking" not in st.session_state:
    st.session_state.tracking = False
if "locations" not in st.session_state:
    st.session_state.locations = []

st.title("📍 Live Locatie Tracker")

# HTML & JavaScript: vraag locatie op
get_location = st.button("📡 Vraag locatie op")

if get_location:
    st.components.v1.html(
        """
        <script>
        navigator.geolocation.getCurrentPosition(
            (position) => {
                const latitude = position.coords.latitude;
                const longitude = position.coords.longitude;
                const accuracy = position.coords.accuracy;

                const event = new CustomEvent("streamlit:location", {
                    detail: {latitude: latitude, longitude: longitude, accuracy: accuracy}
                });
                window.parent.document.dispatchEvent(event);
            },
            (error) => {
                console.error(error);
                alert("Locatie ophalen mislukt: " + error.message);
            }
        );
        </script>
        """,
        height=0,
    )

# Event listener om locatie op te vangen
location_event = st.experimental_get_query_params().get("location", None)

# Start en stop tracking
col1, col2 = st.columns(2)
if col1.button("▶️ Start tracking"):
    st.session_state.tracking = True
if col2.button("⏹️ Stop tracking"):
    st.session_state.tracking = False

# Continu locatie ophalen
if st.session_state.tracking:
    st.write("Tracking actief... haal elke 5 seconden locatie op")
    st.experimental_rerun()

# Simuleer ontvangst van locatie (in plaats van event listener)
# Hier normaal gesproken de code om inkomende browser events af te vangen

# Handmatig toegevoegde test (voor demonstratie)
if get_location:
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Fake locatie als test: Amsterdam centrum
    lat, lon = 52.3702, 4.8952
    st.session_state.locations.append({"timestamp": now, "latitude": lat, "longitude": lon})

# Toon verzamelde locaties
if st.session_state.locations:
    df = pd.DataFrame(st.session_state.locations)
    st.subheader("📋 Gearchiveerde Locaties")
    st.dataframe(df)

    st.subheader("🗺️ Kaart")
    st.map(df.rename(columns={"latitude": "lat", "longitude": "lon"}))

