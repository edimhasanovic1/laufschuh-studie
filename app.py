import random
import time
from urllib.parse import urlencode

import streamlit as st

st.set_page_config(
    page_title="Nika – Laufschuh-Beratung",
    page_icon="👟",
    layout="centered",
)

# =====================================================
# FARBEN / THEMES
# =====================================================
DEFAULT_PRIMARY = "#1D3557"    # Start-Blau/Lila
DEFAULT_SECONDARY = "#0b2545"

CLUB_THEMES = {
    "FC Augsburg": ["#BA3733", "#46714D"],
    "1. FC Union Berlin": ["#EB1923", "#FDDC02"],
    "SV Werder Bremen": ["#1D9053", "#FFFFFF"],
    "Borussia Dortmund": ["#FDE100", "#000000"],
    "Eintracht Frankfurt": ["#E1000F", "#000000"],
    "SC Freiburg": ["#000000", "#FFFFFF"],
    "1. FC Köln": ["#C8102E", "#FFFFFF"],
    "FC Bayern München": ["#A5001E", "#FFFFFF"],
    "Hamburger SV": ["#0A3F86", "#FFFFFF"],
    "1. FC Heidenheim": ["#003B79", "#E2001A"],
    "TSG 1899 Hoffenheim": ["#1961B5", "#FFFFFF"],
    "RB Leipzig": ["#DD013F", "#0C2043"],
    "Bayer 04 Leverkusen": ["#E32221", "#000000"],
    "1. FSV Mainz 05": ["#C3141E", "#918F90"],
    "Borussia Mönchengladbach": ["#000000", "#5F9B50"],
    "FC St. Pauli": ["#624839", "#E30613"],
    "VfB Stuttgart": ["#E32219", "#FFFFFF"],
    "VfL Wolfsburg": ["#65B32E", "#FFFFFF"],
}

CLUB_INSIDER = {
    "FC Augsburg": "Auf geht’s, FCA!",
    "1. FC Union Berlin": "Eisern Union!",
    "SV Werder Bremen": "Lebenslang Grün-Weiß!",
    "Borussia Dortmund": "Echte Liebe.",
    "Eintracht Frankfurt": "Nur die SGE!",
    "SC Freiburg": "SC! SC! SC!",
    "Hamburger SV": "Nur der HSV!",
    "1. FC Heidenheim": "Auf geht’s, Heidenheim!",
    "TSG 1899 Hoffenheim": "TSG! TSG!",
    "1. FC Köln": "Mer stonn zo dir, FC Kölle!",
    "RB Leipzig": "Auf geht’s, RB!",
    "Bayer 04 Leverkusen": "Werkself!",
    "1. FSV Mainz 05": "Nur der FSV!",
    "Borussia Mönchengladbach": "Die Elf vom Niederrhein!",
    "FC Bayern München": "Mia san mia.",
    "FC St. Pauli": "You’ll Never Walk Alone.",
    "VfB Stuttgart": "VfB! VfB!",
    "VfL Wolfsburg": "Auf geht’s, Wölfe!",
}

TRAITS = ["Innovativ", "Komfort", "Leicht", "Atmungsaktiv", "Dämpfung", "Stabilität"]

# =====================================================
# THEME / CSS
# =====================================================
def apply_theme(primary: str, secondary: str):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: linear-gradient(135deg, {primary} 0%, {secondary} 100%) !important;
        }}
        div[data-testid="stAppViewContainer"] > .main {{
            background: rgba(255,255,255,0.18);
        }}

        h1, h2, h3 {{
            color: rgba(255,255,255,0.96) !important;
        }}
        .stCaption {{
            color: rgba(255,255,255,0.9) !important;
        }}
        .stMarkdown, .stMarkdown p, .stMarkdown li, label {{
            color: rgba(255,255,255,0.96) !important;
        }}

        div[data-testid="stAlert"] * {{
            color: rgba(255,255,255,0.96) !important;
        }}
        div[data-testid="stAlert"] {{
            background: rgba(255,255,255,0.14) !important;
            border: 1px solid rgba(255,255,255,0.35) !important;
        }}

        .nika-card {{
            border: 2px solid rgba(255,255,255,0.55);
            border-radius: 14px;
            padding: 14px;
            margin: 10px 0;
            background: rgba(255,255,255,0.92);
            color: #111111 !important;
        }}
        .nika-card * {{
            color: #111111 !important;
        }}
        .nika-accent {{
            color: #111111 !important;
            font-weight: 700;
            font-size: 1.05rem;
        }}

        /* Button-Schrift überall einheitlich "dünn" */
        div[data-testid="stButton"] > button,
        div[data-testid="stButton"] button,
        button[data-testid^="baseButton"] {{
            border-radius: 12px !important;
            border: 2px solid rgba(255,255,255,0.75) !important;
            background: rgba(255,255,255,0.92) !important;
            color: {DEFAULT_PRIMARY} !important;
            font-weight: 400 !important;
            -webkit-font-smoothing: antialiased;
        }}
        div[data-testid="stButton"] > button *,
        div[data-testid="stButton"] button *,
        button[data-testid^="baseButton"] * {{
            font-weight: 400 !important;
        }}
        div[data-testid="stButton"] > button:hover,
        div[data-testid="stButton"] button:hover,
        button[data-testid^="baseButton"]:hover {{
            border: 2px solid rgba(0,0,0,0.25) !important;
        }}

        div[data-baseweb="input"] > div {{
            background: rgba(255,255,255,0.92) !important;
            border: 2px solid rgba(255,255,255,0.75) !important;
            border-radius: 12px !important;
        }}
        div[data-baseweb="input"] * {{
            color: {DEFAULT_PRIMARY} !important;
            font-weight: 600 !important;
        }}

        div[data-testid="stLinkButton"] a,
        a[data-testid="stLinkButton"] {{
            display: inline-block !important;
            border-radius: 12px !important;
            border: 2px solid rgba(255,255,255,0.75) !important;
            background: rgba(255,255,255,0.92) !important;
            color: {DEFAULT_PRIMARY} !important;
            font-weight: 600 !important;
            text-decoration: none !important;
            padding: 0.45rem 0.9rem !important;
        }}

        div[data-testid="stChatMessage"] {{
            background: rgba(255,255,255,0.10);
            border: 1px solid rgba(255,255,255,0.25);
            border-radius: 14px;
            padding: 10px 12px;
            margin-bottom: 8px;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

# =====================================================
# URL PARAMETER (rid Pflicht)
# =====================================================
params = st.query_params
rid = params.get("rid")
if isinstance(rid, list):
    rid = rid[0]
if rid is None:
    st.error("Fehlender Parameter 'rid'. Bitte starte die Studie über den LimeSurvey-Link.")
    st.stop()

# =====================================================
# A/B RANDOMISIERUNG (Session-stabil)
# =====================================================
if "group" not in st.session_state:
    st.session_state.group = random.choice(["A", "B"])
group = st.session_state.group

# =====================================================
# STATE
# =====================================================
st.session_state.setdefault("step", "club")
st.session_state.setdefault("club", None)
st.session_state.setdefault("traits", [])  # exakt 3
st.session_state.setdefault("prefs", {"typ": None, "tech": None, "weite": None, "preis": None})
st.session_state.setdefault("recs", None)
st.session_state.setdefault("selected_shoe", None)

st.session_state.setdefault("club_intro_done", False)
st.session_state.setdefault("prefs_intro_done", False)
st.session_state.setdefault("thinking_intro_done", False)

# =====================================================
# THEME-LOGIK
# =====================================================
if group == "B" and st.session_state.club in CLUB_THEMES:
    primary, secondary = CLUB_THEMES[st.session_state.club][:2]
    apply_theme(primary, secondary)
else:
    apply_theme(DEFAULT_PRIMARY, DEFAULT_SECONDARY)

# =====================================================
# UI HEADER
# =====================================================
st.title("👟 Nika – Laufschuh-Beratung")
# st.caption(f"Teilnahme-ID: {rid} | Gruppe: {group}")  # <-- ausgeblendet (intern weiterhin vorhanden)

# =====================================================
# HELPERS
# =====================================================
def render_typing_then_messages(messages: list[str], delay: float = 3.0):
    with st.chat_message("assistant", avatar="👟"):
        ph = st.empty()
        ph.markdown("✍️ *Nika schreibt …*")
        time.sleep(delay)
        ph.markdown(messages[0])

    for msg in messages[1:]:
        with st.chat_message("assistant", avatar="👟"):
            st.markdown(msg)

def render_typing_then_block(messages: list[str], delay: float = 3.0):
    block = "<br/><br/>".join(messages)
    with st.chat_message("assistant", avatar="👟"):
        ph = st.empty()
        ph.markdown("✍️ *Nika schreibt …*")
        time.sleep(delay)
        ph.markdown(block, unsafe_allow_html=True)

def render_toggle_row_single(title: str, options: list[str], state_key: str):
    st.write(f"**{title}**")
    cols = st.columns(len(options))
    current = st.session_state.prefs.get(state_key)

    for i, opt in enumerate(options):
        label = f"✅ {opt}" if current == opt else opt
        with cols[i]:
            if st.button(label, use_container_width=True, key=f"{state_key}_{i}"):
                st.session_state.prefs[state_key] = opt
                st.rerun()

def render_toggle_grid_multi(title: str, options: list[str], state_key: str, max_select: int = 3, cols_n: int = 3):
    st.write(f"**{title}**")
    selected: list[str] = list(st.session_state.get(state_key, []))

    rows = [options[i:i + cols_n] for i in range(0, len(options), cols_n)]
    for r, row in enumerate(rows):
        cols = st.columns(len(row))
        for c, opt in enumerate(row):
            is_on = opt in selected
            label = f"✅ {opt}" if is_on else opt

            with cols[c]:
                if st.button(label, use_container_width=True, key=f"{state_key}_btn_{r}_{c}"):
                    if opt in selected:
                        selected.remove(opt)
                    else:
                        if len(selected) >= max_select:
                            st.warning(f"Bitte wähle genau {max_select} Eigenschaften.")
                        else:
                            selected.append(opt)

                    st.session_state[state_key] = selected
                    st.rerun()

    if len(selected) != max_select:
        st.info(f"Bitte wähle genau {max_select} Eigenschaften. Aktuell: {len(selected)}")
    else:
        st.success("Perfekt – genau 3 Eigenschaften ausgewählt.")

def build_lime_redirect_url(base_url: str) -> str:
    traits = list(st.session_state.traits or [])
    while len(traits) < 3:
        traits.append("")

    payload = {
        "rid": rid,
        "group": group,
        "club": st.session_state.club or "",
        "traits_1": traits[0],
        "traits_2": traits[1],
        "traits_3": traits[2],
        "traits_csv": "|".join([t for t in traits if t]),
        "typ": st.session_state.prefs.get("typ") or "",
        "tech": st.session_state.prefs.get("tech") or "",
        "weite": st.session_state.prefs.get("weite") or "",
        "preis": st.session_state.prefs.get("preis") or "",
        "rec": st.session_state.selected_shoe or "",
    }
    return f"{base_url}&{urlencode(payload)}"

def fixed_prices_from_user_budget(user_price: int) -> tuple[int, int, int]:
    base = int(user_price)

    cheap = max(100, min(300, base - 30))
    mid = max(100, min(300, base - 5))
    expensive = max(100, min(300, base + 25))

    if not (cheap < mid < expensive):
        cheap = max(100, min(300, base - 20))
        mid = max(100, min(300, base))
        expensive = max(100, min(300, base + 20))

    if not (cheap < mid < expensive):
        cheap, mid, expensive = 130, 160, 190

    return cheap, mid, expensive

# =====================================================
# PAGE SLOT (harte Seite, alte Inhalte sofort weg)
# =====================================================
page_slot = st.empty()
page_slot.empty()

with page_slot.container():

    if st.session_state.step == "club":

        if not st.session_state.club_intro_done:
            render_typing_then_messages(
                [
                    "Hallo! 👋 Ich bin **Nika** – dein **Laufschuh**-Assistent.",
                    "Ich stelle dir ein paar kurze Fragen und suche dann passende Modelle für dich raus.",
                    "Zum Einstieg: Mit welchem der **18 Bundesliga-Clubs** identifizierst du dich am meisten?",
                ],
                delay=3.0,
            )
            st.session_state.club_intro_done = True
        else:
            with st.chat_message("assistant", avatar="👟"):
                st.markdown("Hallo! 👋 Ich bin **Nika** – dein **Laufschuh**-Assistent.")
            with st.chat_message("assistant", avatar="👟"):
                st.markdown("Ich stelle dir ein paar kurze Fragen und suche dann passende Modelle für dich raus.")
            with st.chat_message("assistant", avatar="👟"):
                st.markdown("Zum Einstieg: Mit welchem der **18 Bundesliga-Clubs** identifizierst du dich am meisten?")

        clubs = list(CLUB_THEMES.keys())
        cols = st.columns(3)
        for i, club in enumerate(clubs):
            with cols[i % 3]:
                if st.button(club, use_container_width=True, key=f"club_{club}"):
                    st.session_state.club = club
                    st.session_state.step = "traits"
                    st.rerun()

    elif st.session_state.step == "traits":
        st.success(f"Exzellente Wahl – {CLUB_INSIDER.get(st.session_state.club)}")
        st.info("Als Nächstes: Welche **drei Eigenschaften** sollen deine neuen Laufschuhe unbedingt haben?")

        render_toggle_grid_multi(
            "Bitte genau drei auswählen:",
            TRAITS,
            state_key="traits",
            max_select=3,
            cols_n=3,
        )

        if len(st.session_state.traits) == 3:
            if st.button("Auswahl speichern & weiter", type="primary"):
                st.session_state.prefs_intro_done = False
                st.session_state.step = "prefs"
                st.rerun()

    elif st.session_state.step == "prefs":

        if not st.session_state.prefs_intro_done:
            render_typing_then_messages(
                [
                    "Danke. Die Auswahl wurde gespeichert. Bitte gib nun deine konkreten Wünsche für die Sportschuhe ein. Sie werden für die Auswahl benötigt.",
                ],
                delay=3.0,
            )
            st.session_state.prefs_intro_done = True
        else:
            st.success(
                "Danke. Die Auswahl wurde gespeichert. "
                "Bitte gib nun deine konkreten Wünsche für die Sportschuhe ein. "
                "Sie werden für die Auswahl benötigt."
            )

        render_toggle_row_single(
            "Schuhtyp/Einsatzbereich:",
            ["Training (Straße)", "Gelände (Trail)", "Wettkampf (Racing)"],
            "typ",
        )

        render_toggle_row_single(
            "Technologie:",
            ["Keine", "Nylon", "Carbon"],
            "tech",
        )

        render_toggle_row_single(
            "Passform:",
            ["Schmal", "Normal", "Weit"],
            "weite",
        )

        st.write("**Preis (100–300 €):**")

        price_value = st.session_state.prefs["preis"]
        if price_value is None:
            price_value = 100

        price = st.number_input(
            "Bitte ganze Zahl eingeben:",
            min_value=100,
            max_value=300,
            step=1,
            value=int(price_value),
            key="preis_input",
        )
        st.session_state.prefs["preis"] = int(price)

        errors = []
        if not st.session_state.prefs.get("typ"):
            errors.append("Bitte wähle einen **Schuhtyp/Einsatzbereich**.")
        if not st.session_state.prefs.get("tech"):
            errors.append("Bitte wähle eine **Technologie**.")
        if not st.session_state.prefs.get("weite"):
            errors.append("Bitte wähle eine **Passform**.")
        if len(st.session_state.traits) != 3:
            errors.append("Bitte bestätige **genau drei Eigenschaften**.")
        p = st.session_state.prefs.get("preis")
        if not isinstance(p, int) or p < 100 or p > 300:
            errors.append("**Preis**: Bitte eine ganze Zahl zwischen **100 und 300** eingeben.")

        if errors:
            st.info("Sobald alles ausgefüllt ist, kannst du die Empfehlung generieren.")
            st.error("❌ " + "\n❌ ".join(errors))

        if st.button("Empfehlung generieren", type="primary"):
            if errors:
                st.rerun()

            cheap, mid, expensive = fixed_prices_from_user_budget(int(st.session_state.prefs["preis"]))

            st.session_state.recs = [
                {"name": "Striden X2", "preis": mid, "rating": 4.7},
                {"name": "Aerli TempoOne", "preis": expensive, "rating": 4.6},
                {"name": "FleetRunner Basic", "preis": cheap, "rating": 4.3},
            ]

            st.session_state.thinking_intro_done = False
            st.session_state.step = "thinking"
            st.rerun()

    elif st.session_state.step == "thinking":
        traits_text = ", ".join(st.session_state.traits)

        thinking_msgs = [
            "Super, danke für deine Angaben!",
            f"Ich suche jetzt ein Modell, das **{traits_text}** bietet – und berücksichtige dabei auch deine weiteren Präferenzen.",
            "Einen Moment – ich vergleiche passende Modelle…",
        ]

        if not st.session_state.thinking_intro_done:
            render_typing_then_block(thinking_msgs, delay=3.0)
            st.session_state.thinking_intro_done = True
            st.rerun()
        else:
            with st.chat_message("assistant", avatar="👟"):
                st.markdown("<br/><br/>".join(thinking_msgs), unsafe_allow_html=True)

            if st.button("Ergebnis anzeigen", type="primary"):
                st.session_state.step = "recs"
                st.rerun()

    elif st.session_state.step == "recs":
        st.success(
            "Hier ist dein Ergebnis:\n\n"
            "Als nächsten Schritt klicke bitte auf den Laufschuh, für den du dich am ehesten entscheiden würdest."
        )

        cols = st.columns(3)
        for i, item in enumerate(st.session_state.recs or []):
            with cols[i]:
                st.markdown(
                    f"""
                    <div class="nika-card">
                        <div class="nika-accent">{item["name"]}</div>
                        Preis: {item["preis"]} €<br/>
                        Bewertung: {item["rating"]:.1f} / 5
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                if st.button(item["name"], type="primary", use_container_width=True, key=f"pick_{i}"):
                    st.session_state.selected_shoe = item["name"]
                    st.session_state.step = "done"
                    st.rerun()

    elif st.session_state.step == "done":
        st.success(f"Auswahl gespeichert: **{st.session_state.selected_shoe}**")

        LIME2_URL = "https://umfragen.tu-dortmund.de/index.php/197954?lang=de"
        redirect_url = build_lime_redirect_url(LIME2_URL)

        st.link_button("Weiter zu Teil 2", redirect_url)



