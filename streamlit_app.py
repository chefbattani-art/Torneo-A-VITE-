import streamlit as st
import random
import re
import json
import os
import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

st.set_page_config(page_title="PRO TOURNAMENT // ESPORTS ARENA", page_icon="🏆", layout="centered")

# --- STILE GRAFICO PRO ESPORTS DEFINITIVO ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;900&family=Rajdhani:wght@600;700&display=swap');

    .main { 
        background-color: #02040a; 
        background-image: 
            radial-gradient(circle at 50% 0%, rgba(0, 243, 255, 0.07) 0%, transparent 50%),
            radial-gradient(circle at 50% 100%, rgba(176, 38, 255, 0.07) 0%, transparent 50%),
            linear-gradient(rgba(255, 255, 255, 0.015) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255, 255, 255, 0.015) 1px, transparent 1px);
        background-size: 100% 100%, 100% 100%, 40px 40px, 40px 40px;
        font-family: 'Rajdhani', sans-serif;
        color: #f8fafc;
    }

    h1, h2, h3, h4, .stMarkdown {
        font-family: 'Orbitron', sans-serif !important;
    }

    /* Banner Turno */
    .pro-turn-banner {
        background: linear-gradient(135deg, #050b14, #0b192c);
        border-left: 5px solid #00f3ff;
        border-right: 5px solid #00f3ff;
        border-top: 1px solid rgba(0, 243, 255, 0.3);
        border-bottom: 1px solid rgba(0, 243, 255, 0.3);
        border-radius: 6px;
        padding: 16px;
        text-align: center;
        color: #00f3ff;
        font-family: 'Orbitron', sans-serif;
        font-size: 1.3em;
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: 4px;
        margin-bottom: 25px;
        box-shadow: 0 0 25px rgba(0, 243, 255, 0.15);
    }

    /* Card Tavolo Attivo */
    .pro-match-card {
        background: linear-gradient(160deg, #070d1d, #03070f);
        border: 2px solid rgba(0, 243, 255, 0.4);
        border-radius: 12px;
        padding: 18px;
        margin-bottom: 20px;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.8), 0 0 15px rgba(0, 243, 255, 0.1);
    }

    /* Card Coda */
    .pro-queue-card {
        background: linear-gradient(160deg, #051610, #020705);
        border: 2px solid rgba(16, 185, 129, 0.4);
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 15px;
        box-shadow: 0 5px 20px rgba(0, 0, 0, 0.6);
    }

    .match-header-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 12px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        padding-bottom: 8px;
    }

    .biliardino-title {
        font-family: 'Orbitron', sans-serif;
        font-weight: 900;
        color: #ffd700;
        font-size: 1em;
        letter-spacing: 1.5px;
    }

    .turno-badge {
        background: #0f172a;
        border: 1px solid #38bdf8;
        color: #38bdf8;
        padding: 3px 10px;
        border-radius: 4px;
        font-family: 'Orbitron', sans-serif;
        font-size: 0.75em;
        font-weight: 700;
        letter-spacing: 1px;
    }

    .match-teams-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: #0b1326;
        border: 1px solid #1e293b;
        border-radius: 8px;
        padding: 12px;
        text-align: center;
    }

    .team-box {
        flex: 1;
        font-family: 'Orbitron', sans-serif;
        font-size: 0.9em;
        font-weight: 700;
        color: #f8fafc;
        text-transform: uppercase;
    }

    .vs-badge {
        font-family: 'Orbitron', sans-serif;
        font-weight: 900;
        color: #b026ff;
        font-size: 1.1em;
        padding: 0 15px;
        text-shadow: 0 0 8px rgba(176, 38, 255, 0.5);
    }

    /* Pulsanti Vittoria Personalizzati */
    .stButton > button {
        width: 100% !important;
        background: linear-gradient(135deg, #0056b3, #0099ff) !important;
        color: #ffffff !important;
        font-family: 'Orbitron', sans-serif !important;
        font-weight: 700 !important;
        border: 1px solid #00f3ff !important;
        border-radius: 6px !important;
        padding: 8px 0px !important;
        font-size: 0.8em !important;
        letter-spacing: 1.5px !important;
        box-shadow: 0 0 12px rgba(0, 243, 255, 0.25);
        margin-top: 10px;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #007bff, #00bfff) !important;
        border-color: #ffffff !important;
        box-shadow: 0 0 20px rgba(0, 243, 255, 0.6);
    }

    /* Tabelle Classifiche */
    .pro-rank-container {
        background: #060a14;
        border: 1px solid #1e293b;
        border-top: 3px solid #b026ff;
        border-radius: 8px;
        padding: 16px;
        margin-bottom: 16px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.5);
    }
    .pro-rank-header {
        font-family: 'Orbitron', sans-serif;
        font-size: 1.1em;
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 12px;
        padding-bottom: 6px;
        border-bottom: 1px solid #1e293b;
        color: #00f3ff;
    }
    .pro-player-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: #0b1326;
        padding: 8px 12px;
        border-radius: 4px;
        margin-bottom: 6px;
        font-size: 0.9em;
        border: 1px solid #13223f;
    }
    .pro-player-row-eliminated {
        background: #03050a;
        opacity: 0.5;
        border: 1px solid #0f1523;
    }
    .pro-rank-name {
        font-family: 'Orbitron', sans-serif;
        font-weight: 700;
        text-transform: uppercase;
        color: #ffd700;
    }
    .pro-rank-name-eliminated {
        font-family: 'Orbitron', sans-serif;
        font-weight: 700;
        text-transform: uppercase;
        color: #ef4444;
        text-decoration: line-through;
    }

    div.block-container {
        padding-top: 1.5rem;
        padding-bottom: 3rem;
    }
    </style>
""", unsafe_allow_html=True)

STATE_FILE = "torneo_state.json"

def salva_stato():
    data = {
        "players": st.session_state.players,
        "tournament_started": st.session_state.tournament_started,
        "initial_lives": st.session_state.initial_lives,
        "num_biliardini": st.session_state.num_biliardini,
        "current_round_matches": st.session_state.current_round_matches,
        "round_number": st.session_state.round_number,
        "history": st.session_state.history,
        "match_history": st.session_state.match_history
    }
    with open(STATE_FILE, "w") as f:
        json.dump(data, f)

def carica_stato():
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r") as f:
                data = json.load(f)
                st.session_state.players = data.get("players", [])
                st.session_state.tournament_started = data.get("tournament_started", False)
                st.session_state.initial_lives = data.get("initial_lives", 5)
                st.session_state.num_biliardini = data.get("num_biliardini", 4)
                st.session_state.current_round_matches = data.get("current_round_matches", [])
                st.session_state.round_number = data.get("round_number", 0)
                st.session_state.history = data.get("history", [])
                st.session_state.match_history = data.get("match_history", [])
                return True
        except:
            return False
    return False

if "initialized" not in st.session_state:
    st.session_state.initialized = True
    st.session_state.history = []
    st.session_state.match_history = []
    if not carica_stato():
        st.session_state.players = []
        st.session_state.tournament_started = False
        st.session_state.initial_lives = 5
        st.session_state.num_biliardini = 4
        st.session_state.current_round_matches = []
        st.session_state.round_number = 0

if "giocatore_selezionato" not in st.session_state:
    st.session_state.giocatore_selezionato = None

if "vista_personale_attiva" not in st.session_state:
    st.session_state.vista_personale_attiva = False

def salva_snapshot():
    snapshot = {
        "players": json.loads(json.dumps(st.session_state.players)),
        "current_round_matches": json.loads(json.dumps(st.session_state.current_round_matches)),
        "round_number": st.session_state.round_number,
        "match_history": json.loads(json.dumps(st.session_state.match_history))
    }
    st.session_state.history.append(snapshot)

def genera_abbinamenti():
    attivi = [p for p in st.session_state.players if not p["eliminated"]]
    
    if st.session_state.round_number == 1:
        atts = [p for p in attivi if p["role"] == "attaccante"]
        ports = [p for p in attivi if p["role"] == "portiere"]
        random.shuffle(atts)
        random.shuffle(ports)
        
        min_len = min(len(atts), len(ports))
        coppie = []
        for i in range(min_len):
            coppie.append({"att": atts[i], "port": ports[i]})
        avanzi = atts[min_len:] + ports[min_len:]
        random.shuffle(coppie)
    else:
        atts_w = [p for p in attivi if p["role"] == "attaccante" and p.get("last_result") == 'W']
        atts_l = [p for p in attivi if p["role"] == "attaccante" and p.get("last_result") != 'W']
        ports_w = [p for p in attivi if p["role"] == "portiere" and p.get("last_result") == 'W']
        ports_l = [p for p in attivi if p["role"] == "portiere" and p.get("last_result") != 'W']
        
        random.shuffle(atts_w)
        random.shuffle(atts_l)
        random.shuffle(ports_w)
        random.shuffle(ports_l)
        
        coppie = []
        while atts_w and ports_l:
            coppie.append({"att": atts_w.pop(0), "port": ports_l.pop(0)})
        while atts_l and ports_w:
            coppie.append({"att": atts_l.pop(0), "port": ports_w.pop(0)})
        while atts_w and ports_w:
            coppie.append({"att": atts_w.pop(0), "port": ports_w.pop(0)})
        while atts_l and ports_l:
            coppie.append({"att": atts_l.pop(0), "port": ports_l.pop(0)})
            
        avanzi = atts_w + atts_l + ports_w + ports_l
        random.shuffle(coppie)

    partite = []
    i = 0
    while i < len(coppie) - 1:
        partite.append({
            "teamA": (coppie[i]["att"], coppie[i]["port"]),
            "teamB": (coppie[i+1]["att"], coppie[i+1]["port"])
        })
        i += 2
        
    return {"partite": partite, "pass": avanzi}

def genera_pdf_report():
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
    elements = []
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('TitleStyle', parent=styles['Heading1'], fontSize=18, textColor=colors.HexColor("#00f3ff"), alignment=1, spaceAfter=15)
    subtitle_style = ParagraphStyle('SubTitleStyle', parent=styles['Heading2'], fontSize=12, textColor=colors.HexColor("#b026ff"), spaceBefore=12, spaceAfter=6)
    
    elements.append(Paragraph("PRO ESPORTS ARENA // REPORT UFFICIALE", title_style))
    elements.append(Spacer(1, 15))
    
    if st.session_state.match_history:
        for item in st.session_state.match_history:
            elements.append(Paragraph(f"Turno N° {item['turno']}", subtitle_style))
            table_data = [["Biliardino", "Squadra A", "Squadra B", "Esito"]]
            for idx, m in enumerate(item["partite"]):
                tA = f"🥅 {m['tA_port']} / ⚽️ {m['tA_att']}"
                tB = f"🥅 {m['tB_port']} / ⚽️ {m['tB_att']}"
                table_data.append([str(idx+1), tA, tB, m.get('vincitore', 'Completata')])
            t = Table(table_data, colWidths=[65, 200, 200, 85])
            t.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#060a14")),
                ('TEXTCOLOR', (0,0), (-1,0), colors.HexColor("#00f3ff")),
                ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#1e293b")),
                ('FONTSIZE', (0,0), (-1,-1), 8.5),
            ]))
            elements.append(t)
            elements.append(Spacer(1, 10))
    doc.build(elements)
    buffer.seek(0)
    return buffer.getvalue()

st.sidebar.title("🔐 SECURITY & ADMIN")
admin_code = st.sidebar.text_input("Codice Amministratore", type="password", placeholder="Inserisci 0000")
is_admin = (admin_code == "0000")

nomi_giocatori = sorted(list(set([p["name"] for p in st.session_state.players]))) if st.session_state.players else []

if st.session_state.giocatore_selezionato is None:
    st.title("PRO TOURNAMENT ARENA")
    if nomi_giocatori:
        with st.container(border=True):
            st.markdown("### 👤 SELEZIONA UTENTE:")
            nome_scelto_temp = st.selectbox("Iscritti:", nomi_giocatori, label_visibility="collapsed")
            if st.button("ACCEDI ALLA COMPETIZIONE", type="primary", use_container_width=True):
                st.session_state.giocatore_selezionato = nome_scelto_temp
                st.rerun()
    else:
        st.warning("⚠️ Nessun partecipante caricato. Inserisci i dati dal pannello Admin.")
        
    if is_admin:
        with st.expander("⚙️ Pannello Configurazione & Gestione (Admin)", expanded=True):
            st.session_state.initial_lives = st.number_input("Vite iniziali", 1, 10, st.session_state.initial_lives)
            st.session_state.num_biliardini = st.number_input("Numero Biliardini", 1, 10, st.session_state.num_biliardini)
            lista_input_testo = st.text_area("Incolla partecipanti (es: 1 ⚽️ Nome, 2 🥅 Nome):", height=80)
            if st.button("📥 Importa e Registra Giocatori", type="primary"):
                for riga in lista_input_testo.split("\n"):
                    riga_pulita = riga.strip()
                    if not riga_pulita: continue
                    role = "portiere" if "🥅" in riga_pulita else ("attaccante" if "⚽" in riga_pulita else None)
                    if role:
                        nome = re.sub(r'^\d+[\.\-\s]*', '', riga_pulita.replace("🥅", "").replace("⚽️", "").replace("⚽", "")).strip()
                        if nome and not any(p["name"].lower() == nome.lower() and p["role"] == role for p in st.session_state.players):
                            st.session_state.players.append({"id": len(st.session_state.players)+1, "name": nome, "role": role, "lives": st.session_state.initial_lives, "max_lives": st.session_state.initial_lives, "eliminated": False, "last_result": None})
                salva_stato()
                st.rerun()
            if len(st.session_state.players) >= 2 and not st.session_state.tournament_started:
                if st.button("🚀 Avvia Torneo", type="primary"):
                    st.session_state.tournament_started = True
                    st.session_state.round_number = 1
                    st.session_state.current_round_matches = genera_abbinamenti()
                    salva_stato()
                    st.rerun()
    st.stop()

st.title("PRO ESPORTS ARENA")
col_u1, col_u2 = st.columns([3, 1])
with col_u1:
    st.info(f"⚡ Operatore Connesso: **{st.session_state.giocatore_selezionato.upper()}**")
with col_u2:
    if st.button("🔄 Logout", use_container_width=True):
        st.session_state.giocatore_selezionato = None
        st.session_state.vista_personale_attiva = False
        st.rerun()

etichetta_occhio = "👁️ Mostra Tutti i Match" if st.session_state.vista_personale_attiva else f"🔥 Le Partite di {st.session_state.giocatore_selezionato}"
if st.button(etichetta_occhio, use_container_width=True):
    st.session_state.vista_personale_attiva = not st.session_state.vista_personale_attiva
    st.rerun()

if is_admin:
    with st.expander("⚙️ Pannello Configurazione & Gestione"):
        if st.button("🛑 Reset Torneo"):
            st.session_state.tournament_started = False
            st.session_state.current_round_matches = []
            st.session_state.round_number = 0
            st.session_state.players = []
            if os.path.exists(STATE_FILE): os.remove(STATE_FILE)
            st.rerun()

if st.session_state.tournament_started:
    pdf_data = genera_pdf_report()
    st.sidebar.markdown("---")
    st.sidebar.download_button("📥 Download Report PDF", pdf_data, "report_torneo_pro.pdf", "application/pdf", use_container_width=True)

st.markdown("---")

if st.session_state.tournament_started:
    data_turno = st.session_state.current_round_matches
    if data_turno and not data_turno.get("partite"):
        st.session_state.round_number += 1
        st.session_state.current_round_matches = genera_abbinamenti()
        salva_stato()
        st.rerun()

    st.markdown(f"""<div class="pro-turn-banner">⚔️ TURNO DI GARA N° {st.session_state.round_number}</div>""", unsafe_allow_html=True)

    partite = data_turno.get("partite", []) if data_turno else []
    if partite:
        num_biliardini = st.session_state.num_biliardini
        partite_in_corso = partite[:num_biliardini]
        partite_in_coda = partite[num_biliardini:]
        
        is_personale = st.session_state.vista_personale_attiva
        target_user = st.session_state.giocatore_selezionato.lower()

        if is_personale:
            st.markdown(f"### 🔥 LE PARTITE DI {st.session_state.giocatore_selezionato.upper()}:")
        else:
            st.markdown("### 🔥 PARTITE IN CORSO (Sui biliardini):")

        for idx, match in enumerate(partite_in_corso):
            tA_att, tA_port = match["teamA"]
            tB_att, tB_port = match["teamB"]
            nomi_match = [tA_att['name'].lower(), tA_port['name'].lower(), tB_att['name'].lower(), tB_port['name'].lower()]
            
            if is_personale and target_user not in nomi_match:
                continue

            biliardino_num = idx + 1
            
            st.markdown(f"""
                <div class="pro-match-card">
                    <div class="match-header-row">
                        <span class="biliardino-title">🏟️ BILIARDINO {biliardino_num}</span>
                        <span class="turno-badge">TURNO {st.session_state.round_number}</span>
                    </div>
                    <div class="match-teams-row">
                        <div class="team-box">🥅 {tA_port['name'].upper()} / ⚽️ {tA_att['name'].upper()}</div>
                        <div class="vs-badge">VS</div>
                        <div class="team-box">🥅 {tB_port['name'].upper()} / ⚽️ {tB_att['name'].upper()}</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            c1, c2 = st.columns(2)
            with c1:
                if st.button("⚡ VITTORIA SQUADRA A", key=f"wa_{st.session_state.round_number}_{idx}", use_container_width=True):
                    salva_snapshot()
                    for v in [tA_att, tA_port]: v["last_result"] = 'W'
                    for per in [tB_att, tB_port]:
                        per["last_result"] = 'L'
                        per["lives"] = max(0, per["lives"] - 1)
                        if per["lives"] == 0: per["eliminated"] = True
                    st.session_state.current_round_matches["partite"].pop(idx)
                    if not st.session_state.current_round_matches["partite"]:
                        st.session_state.round_number += 1
                        st.session_state.current_round_matches = genera_abbinamenti()
                    salva_stato()
                    st.rerun()
            with c2:
                if st.button("⚡ VITTORIA SQUADRA B", key=f"wb_{st.session_state.round_number}_{idx}", use_container_width=True):
                    salva_snapshot()
                    for v in [tB_att, tB_port]: v["last_result"] = 'W'
                    for per in [tA_att, tA_port]:
                        per["last_result"] = 'L'
                        per["lives"] = max(0, per["lives"] - 1)
                        if per["lives"] == 0: per["eliminated"] = True
                    st.session_state.current_round_matches["partite"].pop(idx)
                    if not st.session_state.current_round_matches["partite"]:
                        st.session_state.round_number += 1
                        st.session_state.current_round_matches = genera_abbinamenti()
                    salva_stato()
                    st.rerun()

        if partite_in_coda and not is_personale:
            st.markdown("### 📢 PROSSIMI IN CODA:")
            for q_idx, q_match in enumerate(partite_in_coda):
                qa, qp = q_match["teamA"]
                qb, qpp = q_match["teamB"]
                st.markdown(f"""
                    <div class="pro-queue-card">
                        <div class="match-header-row">
                            <span class="biliardino-title" style="color: #34d399;">⏳ IN CODA</span>
                            <span class="turno-badge" style="border-color: #34d399; color: #34d399;">TURNO {st.session_state.round_number}</span>
                        </div>
                        <div class="match-teams-row" style="background: #06120e;">
                            <div class="team-box">🥅 {qp['name'].upper()} / ⚽️ {qa['name'].upper()}</div>
                            <div class="vs-badge" style="color: #34d399;">VS</div>
                            <div class="team-box">🥅 {qpp['name'].upper()} / ⚽️ {qb['name'].upper()}</div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

st.markdown("---")

if st.session_state.players:
    st.markdown("### 📊 CLASSIFICHE IN TEMPO REALE")
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        st.markdown("""<div class="pro-rank-container"><div class="pro-rank-header">🥅 CLASSIFICA PORTIERI</div>""", unsafe_allow_html=True)
        for p in [x for x in st.session_state.players if x["role"] == "portiere"]:
            css = "pro-player-row pro-player-row-eliminated" if p["eliminated"] else "pro-player-row"
            n_css = "pro-rank-name-eliminated" if p["eliminated"] else "pro-rank-name"
            # Pallini verdi per le vite attive, rossi per quelle perse
            vite_attive = "🟢 " * p["lives"]
            vite_perse = "🔴 " * (p["max_lives"] - p["lives"])
             pallini_str = vite_attive + vite_perse
            st.markdown(f"""<div class="{css}"><span class="{n_css}">{p['name']}</span><span>{pallini_str}</span></div>""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with col_c2:
        st.markdown("""<div class="pro-rank-container"><div class="pro-rank-header">⚽️ CLASSIFICA ATTACCANTI</div>""", unsafe_allow_html=True)
        for p in [x for x in st.session_state.players if x["role"] == "attaccante"]:
            css = "pro-player-row pro-player-row-eliminated" if p["eliminated"] else "pro-player-row"
            n_css = "pro-rank-name-eliminated" if p["eliminated"] else "pro-rank-name"
            # Pallini verdi per le vite attive, rossi per quelle perse
            vite_attive = "🟢 " * p["lives"]
            vite_perse = "🔴 " * (p["max_lives"] - p["lives"])
            pallini_str = vite_attive + vite_perse
            st.markdown(f"""<div class="{css}"><span class="{n_css}">{p['name']}</span><span>{pallini_str}</span></div>""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
