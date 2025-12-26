import random
import time
import streamlit as st

st.set_page_config(page_title="Laufschuh-Chatbot Studie", page_icon="👟")

# URL-Parameter lesen
params = st.query_params
rid = params.get("rid", None)

if rid is None:
    st.error("Fehlender Parameter 'rid'. Bitte starte die Studie über den LimeSurvey-Link.")
    st.stop()

# A/B Randomisierung (einmal pro Session)
if "group" not in st.session_state:
    st.session_state.group = random.choice(["A", "B"])
group = st.session_state.group

st.title("👟 Laufschuh-Beratung (Test)")
st.caption(f"Teilnahme-ID (rid): {rid} | (intern) Gruppe: {group}")

st.write("Das ist ein Dummy-Flow. Deinen echten Chatbot integrieren wir gleich danach.")

if "done" not in st.session_state:
    st.session_state.done = False

if not st.session_state.done:
    if st.button("Interaktion starten (Dummy)"):
        with st.spinner("Chatbot läuft..."):
            time.sleep(2)
        st.success("Fertig! Dummy-Empfehlung: Modell X")
        st.session_state.recommendation = "Modell X"
        st.session_state.done = True

if st.session_state.done:
    st.divider()
    st.subheader("Weiter zur Nachbefragung")

    # TODO: Hier später deine LimeSurvey-URL eintragen
    LIME_URL = "https://DEINNAME.limesurvey.net/123456"

    redirect_url = f"{LIME_URL}?rid={rid}&group={group}&rec={st.session_state.recommendation}"
    st.link_button("Weiter zu Teil 2", redirect_url)

