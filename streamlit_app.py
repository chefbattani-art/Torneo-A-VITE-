import streamlit as st
import random
import re
import json
import os

st.set_page_config(
    page_title="Torneo A Vite - Calcio Balilla",
    page_icon="⚽️",
    layout="centered"
)

# ============================================================
# CSS - GRAFICA PROFESSIONALE TORNEO SPORTIVO
# ============================================================

st.markdown("""
<style>

/* ============================================================
   GLOBAL
   ============================================================ */

.stApp {
    background:
        radial-gradient(circle at 50% -10%, rgba(245,158,11,0.12), transparent 35%),
        linear-gradient(180deg, #080b10 0%, #0d1117 45%, #080b10 100%);
    color: #f8fafc;
}

.main .block-container {
    max-width: 1050px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}

/* Nasconde elementi Streamlit poco utili */
#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

/* ============================================================
   TITOLO PRINCIPALE
   ============================================================ */

h1 {
    font-size: 2.4rem !important;
    font-weight: 900 !important;
    letter-spacing: -1px;
    text-align: center;
    margin-bottom: 0.2rem !important;
    color: #f8fafc;
    text-shadow: 0 3px 20px rgba(0,0,0,0.5);
}

h2 {
    font-weight: 900 !important;
    color: #f8fafc !important;
}

h3 {
    font-weight: 800 !important;
    color: #e5e7eb !important;
}

/* Linea decorativa sotto i titoli */

h1::after {
    content: "";
    display: block;
    width: 110px;
    height: 4px;
    margin: 12px auto 22px auto;
    border-radius: 10px;
    background: linear-gradient(90deg, #d97706, #fbbf24, #d97706);
    box-shadow: 0 0 18px rgba(245,158,11,0.35);
}

/* ============================================================
   SIDEBAR
   ============================================================ */

[data-testid="stSidebar"] {
    background:
        linear-gradient(180deg, #0b0f14 0%, #111827 100%);
    border-right: 1px solid #252c36;
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #fbbf24 !important;
}

/* ============================================================
   ADMIN PANEL
   ============================================================ */

[data-testid="stExpander"] {
    background: linear-gradient(145deg, #111827, #0b1017);
    border: 1px solid #2d3744;
    border-radius: 14px;
    box-shadow: 0 12px 35px rgba(0,0,0,0.25);
}

[data-testid="stExpander"] summary {
    font-weight: 800;
}

/* ============================================================
   INPUT
   ============================================================ */

.stTextInput input,
.stTextArea textarea,
.stNumberInput input {
    background-color: #0b1118 !important;
    color: #f8fafc !important;
    border: 1px solid #374151 !important;
    border-radius: 8px !important;
}

.stTextInput input:focus,
.stTextArea textarea:focus,
.stNumberInput input:focus {
    border-color: #f59e0b !important;
    box-shadow: 0 0 0 1px #f59e0b !important;
}

/* ============================================================
   BOTTONI
   ============================================================ */

.stButton > button {
    width: 100%;
    min-height: 44px;

    background: linear-gradient(
        135deg,
        #0369a1 0%,
        #0284c7 50%,
        #0369a1 100%
    ) !important;

    color: white !important;
    font-weight: 800 !important;
    border: 1px solid #38bdf8 !important;
    border-radius: 8px !important;

    transition:
        transform 0.15s ease,
        box-shadow 0.15s ease,
        background 0.15s ease;

    box-shadow:
        0 5px 15px rgba(2,132,199,0.18);
}

.stButton > button:hover {
    transform: translateY(-2px);
    background: linear-gradient(
        135deg,
        #0284c7,
        #0ea5e9
    ) !important;

    box-shadow:
        0 8px 22px rgba(14,165,233,0.28);
}

.stButton > button:active {
    transform: translateY(0);
}

/* ============================================================
   BOTTONI PRIMARY
   ============================================================ */

.stButton > button[kind="primary"] {
    background:
        linear-gradient(
            135deg,
            #b45309,
            #f59e0b,
            #d97706
        ) !important;

    color: #111827 !important;
    border: 1px solid #fbbf24 !important;

    box-shadow:
        0 6px 20px rgba(245,158,11,0.22);
}

.stButton > button[kind="primary"]:hover {
    background:
        linear-gradient(
            135deg,
            #d97706,
            #fbbf24,
            #f59e0b
        ) !important;

    box-shadow:
        0 10px 28px rgba(245,158,11,0.32);
}

/* ============================================================
   DIVIDER
   ============================================================ */

hr {
    border: none !important;
    height: 1px !important;
    background: linear-gradient(
        90deg,
        transparent,
        #374151,
        #f59e0b,
        #374151,
        transparent
    ) !important;
    margin: 28px 0 !important;
}

/* ============================================================
   HEADER TURNO
   ============================================================ */

.round-header {
    position: relative;
    overflow: hidden;

    background:
        linear-gradient(
            135deg,
            #111827 0%,
            #161f2d 50%,
            #0b1118 100%
        );

    border: 1px solid #374151;
    border-radius: 16px;

    padding: 18px 22px;
    margin: 10px 0 24px 0;

    text-align: center;

    box-shadow:
        0 15px 40px rgba(0,0,0,0.3);
}

.round-header::before {
    content: "";
    position: absolute;
    left: 0;
    top: 0;
    bottom: 0;
    width: 5px;
    background: linear-gradient(
        180deg,
        #fbbf24,
        #d97706
    );
}

.round-label {
    color: #9ca3af;
    font-size: 0.75rem;
    font-weight: 800;
    letter-spacing: 3px;
    text-transform: uppercase;
}

.round-number {
    color: #fbbf24;
    font-size: 2rem;
    font-weight: 900;
    line-height: 1.1;
    margin-top: 3px;
}

/* ============================================================
   BILIARDINO / MATCH CARD
   ============================================================ */

.match-card {
    position: relative;
    overflow: hidden;

    background:
        linear-gradient(
            145deg,
            #121821 0%,
            #0d131b 100%
        );

    padding: 0;
    border-radius: 16px;

    margin-bottom: 24px;

    border: 1px solid #303946;

    box-shadow:
        0 12px 35px rgba(0,0,0,0.35),
        inset 0 1px 0 rgba(255,255,255,0.025);
}

.match-card::after {
    content: "";
    position: absolute;
    left: 0;
    right: 0;
    bottom: 0;
    height: 2px;

    background:
        linear-gradient(
            90deg,
            transparent,
            #d97706,
            #fbbf24,
            #d97706,
            transparent
        );

    opacity: 0.8;
}

/* ============================================================
   HEADER BILIARDINO
   ============================================================ */

.biliardino-box {
    background:
        linear-gradient(
            135deg,
            #92400e,
            #d97706 45%,
            #f59e0b 100%
        );

    color: #111827;

    text-align: center;

    font-size: 0.82rem;
    font-weight: 950;

    padding: 10px 8px;

    text-transform: uppercase;
    letter-spacing: 2px;

    border-bottom: 1px solid #fbbf24;

    text-shadow: 0 1px rgba(255,255,255,0.2);
}

/* ============================================================
   TEAM BOX
   ============================================================ */

.team-box {
    background:
        linear-gradient(
            145deg,
            #065f46 0%,
            #047857 50%,
            #064e3b 100%
        );

    padding: 13px 8px;

    border-radius: 10px;

    border: 1px solid #34d399;

    color: #f3f4f6;

    font-size: 0.92em;
    font-weight: 700;

    min-height: 72px;

    display: flex;
    flex-direction: column;
    justify-content: center;

    text-align: center;

    margin-bottom: 9px;

    box-shadow:
        inset 0 1px rgba(255,255,255,0.06),
        0 5px 15px rgba(0,0,0,0.2);
}

.team-box div {
    margin: 3px 0;
}

.team-box b {
    color: #ffffff;
}

/* ============================================================
   VS
   ============================================================ */

.vs-badge {
    text-align: center;

    color: #fbbf24;

    font-weight: 950;

    padding-top: 29px;

    font-size: 0.9rem;

    letter-spacing: 1px;

    text-shadow:
        0 0 12px rgba(251,191,36,0.25);
}

/* ============================================================
   MATCH STATUS / CODA
   ============================================================ */

.queue-card {
    background:
        linear-gradient(
            135deg,
            #172033,
            #101722
        );

    border: 1px solid #374151;

    border-left: 4px solid #f59e0b;

    border-radius: 10px;

    padding: 12px 15px;

    margin-bottom: 9px;

    color: #d1d5db;

    font-size: 0.9rem;
}

/* ============================================================
   PASS
   ============================================================ */

.pass-card {
    background:
        linear-gradient(
            135deg,
            rgba(6,95,70,0.45),
            rgba(4,120,87,0.18)
        );

    border: 1px solid #166534;

    border-left: 4px solid #22c55e;

    border-radius: 10px;

    padding: 10px 14px;

    margin-bottom: 8px;

    color: #d1fae5;
}

/* ============================================================
   CLASSIFICA
   ============================================================ */

.leaderboard-section {
    background:
        linear-gradient(
            145deg,
            #111827,
            #0d131b
        );

    border: 1px solid #303946;

    border-radius: 14px;

    padding: 16px;

    margin-bottom: 12px;

    box-shadow:
        0 10px 25px rgba(0,0,0,0.22);
}

.leaderboard-title {
    font-size: 0.95rem;
    font-weight: 900;

    text-transform: uppercase;
    letter-spacing: 1px;

    color: #fbbf24;

    border-bottom: 1px solid #303946;

    padding-bottom: 10px;
    margin-bottom: 12px;
}

.player-row {
    display: flex;
    justify-content: space-between;
    align-items: center;

    background: #0b1118;

    border: 1px solid #202833;

    border-radius: 8px;

    padding: 8px 10px;

    margin-bottom: 7px;
}

.player-name {
    color: #f3f4f6;
    font-weight: 700;
}

.player-lives {
    white-space: nowrap;
    font-size: 0.85rem;
}

/* ============================================================
   PODIO
   ============================================================ */

.podium-card {
    background:
        linear-gradient(
            145deg,
            #151b25,
            #0c1118
        );

    border: 1px solid #3b4350;

    border-radius: 14px;

    padding: 16px;

    box-shadow:
        0 12px 35px rgba(0,0,0,0.3);
}

.podium-title {
    color: #fbbf24;

    font-weight: 900;

    text-transform: uppercase;

    letter-spacing: 1px;

    text-align: center;

    border-bottom: 1px solid #303946;

    padding-bottom: 10px;

    margin-bottom: 12px;
}

.podium-player {
    background: #0b1118;

    border: 1px solid #29313d;

    border-radius: 8px;

    padding: 9px 11px;

    margin-bottom: 7px;

    font-weight: 700;
}

/* ============================================================
   INFO / SUCCESS / WARNING
   ============================================================ */

[data-testid="stAlert"] {
    border-radius: 10px !important;
}

/* ============================================================
   MOBILE
   ============================================================ */

@media (max-width: 700px) {

    .main .block-container {
        padding-left: 0.7rem;
        padding-right: 0.7rem;
        padding-top: 1rem;
    }

    h1 {
        font-size: 1.65rem !important;
        line-height: 1.15 !important;
    }

    .round-number {
        font-size: 1.6rem;
    }

    .team-box {
        min-height: 68px;
        font-size: 0.78rem;
        padding: 9px 3px;
    }

    .vs-badge {
        font-size: 0.75rem;
        padding-top: 27px;
    }

    .biliardino-box {
        font-size: 0.72rem;
        padding: 9px 5px;
        letter-spacing: 1.5px;
    }

    .match-card {
        border-radius: 12px;
    }

    .leaderboard-section {
        padding: 12px;
    }

    .player-row {
        padding: 8px;
    }
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# FILE STATO
# ============================================================

STATE_FILE = "torneo_state.json"


def salva_stato():
    data = {
        "players": st.session_state.players,
        "tournament_started": st.session_state.tournament_started,
        "initial_lives": st.session_state.initial_lives,
        "num_biliardini": st.session_state.num_biliardini,
        "current_round_matches": st.session_state.current_round_matches,
        "round_number": st.session_state.round_number,
        "show_podium": st.session_state.show_podium
    }

    with open(STATE_FILE, "w") as f:
        json.dump(data, f)


def carica_stato():
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r") as f:
                data = json.load(f)

                st.session_state.players = data.get("players", [])
                st.session_state.tournament_started = data.get(
                    "tournament_started",
                    False
                )
                st.session_state.initial_lives = data.get(
                    "initial_lives",
                    5
                )
                st.session_state.num_biliardini = data.get(
                    "num_biliardini",
                    4
                )
                st.session_state.current_round_matches = data.get(
                    "current_round_matches",
                    []
                )
                st.session_state.round_number = data.get(
                    "round_number",
                    0
                )
                st.session_state.show_podium = data.get(
                    "show_podium",
                    False
                )

                return True

        except:
            return False

    return False


# ============================================================
# INIZIALIZZAZIONE STATO
# ============================================================

if "initialized" not in st.session_state:

    st.session_state.initialized = True

    if not carica_stato():

        st.session_state.players = []
        st.session_state.tournament_started = False
        st.session_state.initial_lives = 5
        st.session_state.num_biliardini = 4
        st.session_state.current_round_matches = []
        st.session_state.round_number = 0
        st.session_state.show_podium = False


# ============================================================
# FUNZIONE ABBINAMENTI
# ============================================================

def genera_abbinamenti():

    attivi = [
        p for p in st.session_state.players
        if not p["eliminated"]
    ]

    if st.session_state.round_number == 1:

        atts = [
            p for p in attivi
            if p["role"] == "attaccante"
        ]

        ports = [
            p for p in attivi
            if p["role"] == "portiere"
        ]

        random.shuffle(atts)
        random.shuffle(ports)

        min_len = min(len(atts), len(ports))

        coppie = []

        for i in range(min_len):
            coppie.append({
                "att": atts[i],
                "port": ports[i]
            })

        avanzi = atts[min_len:] + ports[min_len:]

        random.shuffle(coppie)

    else:

        atts_w = [
            p for p in attivi
            if p["role"] == "attaccante"
            and p.get("last_result") == 'W'
        ]

        atts_l = [
            p for p in attivi
            if p["role"] == "attaccante"
            and p.get("last_result") != 'W'
        ]

        ports_w = [
            p for p in attivi
            if p["role"] == "portiere"
            and p.get("last_result") == 'W'
        ]

        ports_l = [
            p for p in attivi
            if p["role"] == "portiere"
            and p.get("last_result") != 'W'
        ]

        random.shuffle(atts_w)
        random.shuffle(atts_l)
        random.shuffle(ports_w)
        random.shuffle(ports_l)

        coppie = []

        while atts_w and ports_l:
            coppie.append({
                "att": atts_w.pop(0),
                "port": ports_l.pop(0)
            })

        while atts_l and ports_w:
            coppie.append({
                "att": atts_l.pop(0),
                "port": ports_w.pop(0)
            })

        while atts_w and ports_w:
            coppie.append({
                "att": atts_w.pop(0),
                "port": ports_w.pop(0)
            })

        while atts_l and ports_l:
            coppie.append({
                "att": atts_l.pop(0),
                "port": ports_l.pop(0)
            })

        avanzi = (
            atts_w +
            atts_l +
            ports_w +
            ports_l
        )

        random.shuffle(coppie)

    partite = []

    i = 0

    while i < len(coppie) - 1:

        partite.append({
            "teamA": (
                coppie[i]["att"],
                coppie[i]["port"]
            ),

            "teamB": (
                coppie[i + 1]["att"],
                coppie[i + 1]["port"]
            )
        })

        i += 2

    res = {
        "partite": partite,
        "pass": avanzi
    }

    return res


# ============================================================
# SIDEBAR ADMIN
# ============================================================

st.sidebar.title("🔐 ACCESSO ADMIN")

admin_code = st.sidebar.text_input(
    "Codice Amministratore",
    type="password",
    placeholder="Inserisci 0000"
)

is_admin = admin_code == "0000"

if is_admin:
    st.sidebar.success("🔓 Amministratore attivo")
else:
    st.sidebar.info("👁️ Modalità spettatore")


# ============================================================
# HEADER PRINCIPALE
# ============================================================

st.markdown("""
<div style="
    text-align:center;
    color:#9ca3af;
    font-size:0.72rem;
    font-weight:800;
    letter-spacing:3px;
    text-transform:uppercase;
    margin-bottom:4px;
">
    CAMPIONATO • CALCIO BALILLA
</div>
""", unsafe_allow_html=True)

st.title("⚽️ TORNEO A VITE")

st.markdown("""
<div style="
    text-align:center;
    color:#6b7280;
    font-size:0.85rem;
    margin-top:-14px;
    margin-bottom:22px;
">
    Attaccanti & Portieri
</div>
""", unsafe_allow_html=True)


# ============================================================
# PANNELLO CONFIGURAZIONE
# ============================================================

if is_admin:

    with st.expander(
        "⚙️ PANNELLO CONFIGURAZIONE & GESTIONE",
        expanded=not st.session_state.tournament_started
    ):

        if not st.session_state.tournament_started:

            col_conf1, col_conf2 = st.columns(2)

            with col_conf1:

                st.session_state.initial_lives = st.number_input(
                    "❤️ Vite iniziali",
                    min_value=1,
                    max_value=10,
                    value=st.session_state.initial_lives
                )

            with col_conf2:

                st.session_state.num_biliardini = st.number_input(
                    "🏟️ Numero Biliardini",
                    min_value=1,
                    max_value=10,
                    value=st.session_state.num_biliardini
                )

            st.markdown("---")

            st.markdown("### 📝 REGISTRAZIONE GIOCATORI")

            lista_input_testo = st.text_area(
                "Incolla partecipanti",
                placeholder="Esempio:\n1 ⚽️ Mario Rossi\n2 🥅 Luca Bianchi",
                height=120
            )

            if st.button(
                "📥 IMPORTA E REGISTRA GIOCATORI",
                type="primary"
            ):

                righe = lista_input_testo.split("\n")

                count_aggiunti = 0

                for riga in righe:

                    riga_pulita = riga.strip()

                    if not riga_pulita:
                        continue

                    role = None

                    if "🥅" in riga_pulita:
                        role = "portiere"

                    elif (
                        "⚽️" in riga_pulita
                        or "⚽" in riga_pulita
                    ):
                        role = "attaccante"

                    if role:

                        nome = (
                            riga_pulita
                            .replace("🥅", "")
                            .replace("⚽️", "")
                            .replace("⚽", "")
                        )

                        nome = re.sub(
                            r'^\d+[\.\-\s]*',
                            '',
                            nome
                        ).strip()

                        if nome and not any(
                            p["name"].lower() == nome.lower()
                            and p["role"] == role
                            for p in st.session_state.players
                        ):

                            st.session_state.players.append({

                                "id":
                                    len(st.session_state.players) + 1,

                                "name": nome,

                                "role": role,

                                "lives":
                                    st.session_state.initial_lives,

                                "max_lives":
                                    st.session_state.initial_lives,

                                "eliminated": False,

                                "last_result": None
                            })

                            count_aggiunti += 1

                salva_stato()

                st.success(
                    f"Importati {count_aggiunti} giocatori!"
                )

                st.rerun()

        # ====================================================
        # CONTATORI ISCRITTI
        # ====================================================

        attaccanti = [
            p for p in st.session_state.players
            if p["role"] == "attaccante"
        ]

        portieri = [
            p for p in st.session_state.players
            if p["role"] == "portiere"
        ]

        st.markdown(
            f"""
            <div style="
                display:flex;
                gap:10px;
                margin:15px 0;
            ">

                <div style="
                    flex:1;
                    background:#111827;
                    border:1px solid #374151;
                    border-radius:10px;
                    padding:12px;
                    text-align:center;
                ">
                    <div style="
                        color:#9ca3af;
                        font-size:0.7rem;
                        font-weight:800;
                    ">
                        ATTACCANTI
                    </div>
                    <div style="
                        color:#fbbf24;
                        font-size:1.5rem;
                        font-weight:900;
                    ">
                        {len(attaccanti)}
                    </div>
                </div>

                <div style="
                    flex:1;
                    background:#111827;
                    border:1px solid #374151;
                    border-radius:10px;
                    padding:12px;
                    text-align:center;
                ">
                    <div style="
                        color:#9ca3af;
                        font-size:0.7rem;
                        font-weight:800;
                    ">
                        PORTIERI
                    </div>
                    <div style="
                        color:#34d399;
                        font-size:1.5rem;
                        font-weight:900;
                    ">
                        {len(portieri)}
                    </div>
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

        if len(st.session_state.players) >= 2:

            col_act1, col_act2 = st.columns(2)

            with col_act1:

                if not st.session_state.tournament_started:

                    if st.button(
                        "🚀 AVVIA TORNEO • 1° TURNO",
                        type="primary"
                    ):

                        st.session_state.tournament_started = True
                        st.session_state.round_number = 1
                        st.session_state.show_podium = False

                        st.session_state.current_round_matches = (
                            genera_abbinamenti()
                        )

                        salva_stato()

                        st.rerun()

                else:

                    if st.button(
                        "🔄 GENERA TURNO SUCCESSIVO"
                    ):

                        st.session_state.round_number += 1

                        st.session_state.current_round_matches = (
                            genera_abbinamenti()
                        )

                        salva_stato()

                        st.rerun()

            with col_act2:

                if st.button(
                    "🛑 RICOMINCIA DA ZERO"
                ):

                    st.session_state.tournament_started = False
                    st.session_state.current_round_matches = []
                    st.session_state.round_number = 0
                    st.session_state.show_podium = False
                    st.session_state.players = []

                    if os.path.exists(STATE_FILE):
                        os.remove(STATE_FILE)

                    st.rerun()


st.divider()


# ============================================================
# VISUALIZZAZIONE TORNEO
# ============================================================

if st.session_state.tournament_started:

    st.markdown(
        f"""
        <div class="round-header">

            <div class="round-label">
                CAMPIONATO • TURNO
            </div>

            <div class="round-number">
                TURNO N° {st.session_state.round_number}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    data_turno = st.session_state.current_round_matches

    # ========================================================
    # PASS AUTOMATICI
    # ========================================================

    if data_turno and data_turno.get("pass"):

        st.markdown(
            "### 💚 PASS AUTOMATICI"
        )

        for p in data_turno["pass"]:

            icona = (
                "⚽️"
                if p["role"] == "attaccante"
                else "🥅"
            )

            st.markdown(
                f"""
                <div class="pass-card">
                    <b>{icona} {p['name']}</b>
                    <span style="color:#9ca3af;">
                        &nbsp;•&nbsp; riposa in questo turno
                    </span>
                    <span style="color:#4ade80;">
                        &nbsp;PASS
                    </span>
                </div>
                """,
                unsafe_allow_html=True
            )

    partite = (
        data_turno.get("partite", [])
        if data_turno
        else []
    )

    # ========================================================
    # NESSUNA PARTITA
    # ========================================================

    if not partite:

        st.success(
            "🎉 Turno completato! "
            "Genera il turno successivo dal pannello Admin."
        )

        if (
            is_admin
            and not st.session_state.show_podium
        ):

            if st.button(
                "🏆 MOSTRA PODIO FINALE",
                type="primary"
            ):

                st.session_state.show_podium = True

                salva_stato()

                st.rerun()

    else:

        num_biliardini = st.session_state.num_biliardini

        partite_in_corso = partite[:num_biliardini]

        partite_in_coda = partite[num_biliardini:]

        st.markdown(
            "### 🏟️ BILIARDINI IN GIOCO"
        )

        # ====================================================
        # MATCH
        # ====================================================

        for idx, match in enumerate(partite_in_corso):

            biliardino_num = idx + 1

            tA_att, tA_port = match["teamA"]

            tB_att, tB_port = match["teamB"]

            # Apertura card
            st.markdown(
                f"""
                <div class="match-card">

                    <div class="biliardino-box">
                        🏟️ BILIARDINO {biliardino_num}
                    </div>
                """,
                unsafe_allow_html=True
            )

            col_teamA, col_vs, col_teamB = st.columns(
                [5, 1, 5]
            )

            # =================================================
            # TEAM A
            # =================================================

            with col_teamA:

                st.markdown(
                    f"""
                    <div class="team-box">

                        <div>
                            ⚽️
                            <b>{tA_att['name']}</b>
                        </div>

                        <div>
                            🥅
                            <b>{tA_port['name']}</b>
                        </div>

                    </div>
                    """,
                    unsafe_allow_html=True
                )

                if is_admin:

                    if st.button(
                        "🏆 VITTORIA",
                        key=(
                            f"win_A_"
                            f"{st.session_state.round_number}_"
                            f"{idx}"
                        )
                    ):

                        for v in [tA_att, tA_port]:
                            v["last_result"] = 'W'

                        for per in [tB_att, tB_port]:

                            per["last_result"] = 'L'

                            per["lives"] = max(
                                0,
                                per["lives"] - 1
                            )

                            if per["lives"] == 0:
                                per["eliminated"] = True

                        st.session_state.current_round_matches[
                            "partite"
                        ].pop(idx)

                        salva_stato()

                        st.rerun()

            # =================================================
            # VS
            # =================================================

            with col_vs:

                st.markdown(
                    """
                    <div class="vs-badge">
                        VS
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            # =================================================
            # TEAM B
            # =================================================

            with col_teamB:

                st.markdown(
                    f"""
                    <div class="team-box">

                        <div>
                            ⚽️
                            <b>{tB_att['name']}</b>
                        </div>

                        <div>
                            🥅
                            <b>{tB_port['name']}</b>
                        </div>

                    </div>
                    """,
                    unsafe_allow_html=True
                )

                if is_admin:

                    if st.button(
                        "🏆 VITTORIA",
                        key=(
                            f"win_B_"
                            f"{st.session_state.round_number}_"
                            f"{idx}"
                        )
                    ):

                        for v in [tB_att, tB_port]:
                            v["last_result"] = 'W'

                        for per in [tA_att, tA_port]:

                            per["last_result"] = 'L'

                            per["lives"] = max(
                                0,
                                per["lives"] - 1
                            )

                            if per["lives"] == 0:
                                per["eliminated"] = True

                        st.session_state.current_round_matches[
                            "partite"
                        ].pop(idx)

                        salva_stato()

                        st.rerun()

            st.markdown(
                "</div>",
                unsafe_allow_html=True
            )

        # ====================================================
        # CODA
        # ====================================================

        if partite_in_coda:

            st.markdown("### ⏳ IN CODA")

            for q_idx, q_match in enumerate(
                partite_in_coda
            ):

                qa, qp = q_match["teamA"]

                qb, qpp = q_match["teamB"]

                st.markdown(
                    f"""
                    <div class="queue-card">

                        <b>CODA #{q_idx + 1}</b>

                        <span style="color:#6b7280;">
                            &nbsp;•&nbsp;
                        </span>

                        ⚽️ {qa['name']}
                        &nbsp;&
                        🥅 {qp['name']}

                        <span style="
                            color:#f59e0b;
                            font-weight:900;
                        ">
                            &nbsp; VS &nbsp;
                        </span>

                        ⚽️ {qb['name']}
                        &nbsp;&
                        🥅 {qpp['name']}

                    </div>
                    """,
                    unsafe_allow_html=True
                )


# ============================================================
# CLASSIFICA
# ============================================================

st.divider()

st.markdown(
    """
    <div style="
        text-align:center;
        margin-bottom:18px;
    ">

        <div style="
            color:#9ca3af;
            font-size:0.72rem;
            font-weight:800;
            letter-spacing:2px;
            text-transform:uppercase;
        ">
            STANDING UFFICIALE
        </div>

        <div style="
            color:#fbbf24;
            font-size:1.65rem;
            font-weight:900;
        ">
            📋 CLASSIFICA & VITE
        </div>

    </div>
    """,
    unsafe_allow_html=True
)

if st.session_state.players:

    col_c1, col_c2 = st.columns(2)

    # ========================================================
    # ATTACCANTI
    # ========================================================

    with col_c1:

        st.markdown(
            """
            <div class="leaderboard-section">

                <div class="leaderboard-title">
                    ⚽️ ATTACCANTI
                </div>
            """,
            unsafe_allow_html=True
        )

        for p in [
            x for x in st.session_state.players
            if x["role"] == "attaccante"
        ]:

            cuori = (
                "❤️ " * p["lives"]
                +
                "🖤 " * (
                    p["max_lives"] - p["lives"]
                )
            )

            if p["eliminated"]:

                stato = "💀 ELIMINATO"

            else:

                stato = cuori

            st.markdown(
                f"""
                <div class="player-row">

                    <div class="player-name">
                        {p['name']}
                    </div>

                    <div class="player-lives">
                        {stato}
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown("</div>", unsafe_allow_html=True)

    # ========================================================
    # PORTIERI
    # ========================================================

    with col_c2:

        st.markdown(
            """
            <div class="leaderboard-section">

                <div class="leaderboard-title">
                    🥅 PORTIERI
                </div>
            """,
            unsafe_allow_html=True
        )

        for p in [
            x for x in st.session_state.players
            if x["role"] == "portiere"
        ]:

            cuori = (
                "❤️ " * p["lives"]
                +
                "🖤 " * (
                    p["max_lives"] - p["lives"]
                )
            )

            if p["eliminated"]:

                stato = "💀 ELIMINATO"

            else:

                stato = cuori

            st.markdown(
                f"""
                <div class="player-row">

                    <div class="player-name">
                        {p['name']}
                    </div>

                    <div class="player-lives">
                        {stato}
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# PODIO FINALE
# ============================================================

if st.session_state.show_podium:

    st.divider()

    st.markdown(
        """
        <div style="
            text-align:center;
            margin-bottom:22px;
        ">

            <div style="
                font-size:2.2rem;
            ">
                🏆
            </div>

            <div style="
                color:#fbbf24;
                font-size:1.7rem;
                font-weight:900;
                letter-spacing:1px;
            ">
                PODIO UFFICIALE
            </div>

            <div style="
                color:#9ca3af;
                font-size:0.75rem;
                letter-spacing:2px;
                text-transform:uppercase;
            ">
                Classifica finale del torneo
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    atts_sorted = sorted(
        [
            p for p in st.session_state.players
            if p["role"] == "attaccante"
        ],
        key=lambda x: (
            x["lives"],
            not x["eliminated"]
        ),
        reverse=True
    )

    ports_sorted = sorted(
        [
            p for p in st.session_state.players
            if p["role"] == "portiere"
        ],
        key=lambda x: (
            x["lives"],
            not x["eliminated"]
        ),
        reverse=True
    )

    col_pod1, col_pod2 = st.columns(2)

    # ========================================================
    # TOP 4 ATTACCANTI
    # ========================================================

    with col_pod1:

        st.markdown(
            """
            <div class="podium-card">

                <div class="podium-title">
                    ⚽️ TOP 4 ATTACCANTI
                </div>
            """,
            unsafe_allow_html=True
        )

        for rank, p in enumerate(
            atts_sorted[:4]
        ):

            medaglia = ["🥇", "🥈", "🥉", "🏅"][rank]

            st.markdown(
                f"""
                <div class="podium-player">

                    {medaglia}
                    <span style="
                        color:#fbbf24;
                        margin-right:6px;
                    ">
                        {rank + 1}°
                    </span>

                    {p['name']}

                    <span style="
                        float:right;
                    ">
                        {'❤️ ' * p['lives']}
                    </span>

                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown("</div>", unsafe_allow_html=True)

    # ========================================================
    # TOP 4 PORTIERI
    # ========================================================

    with col_pod2:

        st.markdown(
            """
            <div class="podium-card">

                <div class="podium-title">
                    🥅 TOP 4 PORTIERI
                </div>
            """,
            unsafe_allow_html=True
        )

        for rank, p in enumerate(
            ports_sorted[:4]
        ):

            medaglia = ["🥇", "🥈", "🥉", "🏅"][rank]

            st.markdown(
                f"""
                <div class="podium-player">

                    {medaglia}
                    <span style="
                        color:#fbbf24;
                        margin-right:6px;
                    ">
                        {rank + 1}°
                    </span>

                    {p['name']}

                    <span style="
                        float:right;
                    ">
                        {'❤️ ' * p['lives']}
                    </span>

                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown("</div>", unsafe_allow_html=True)
