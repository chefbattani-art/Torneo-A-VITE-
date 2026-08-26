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

# --- STILE GRAFICO PRO ESPORTS (BLU NEON, ORO, VIOLETTO) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;900&family=Rajdhani:wght@600;700&display=swap');

    /* Sfondo Arena Pro */
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

    /* Banner Turno - Neon Blu Elettrico */
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
        box-shadow: 0 0 25px rgba(0, 243, 255, 0.15), inset 0 0 15px rgba(0, 243, 255, 0.1);
    }

    /* Box Biliardino - Stile Tavolo da Gara */
    .pro-match-card {
        background: rgba(10, 15, 30, 0.7);
        border: 1px solid rgba(0, 243, 255, 0.2);
        border-radius: 10px;
        padding: 18px;
        margin-bottom: 20px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.8);
    }

    .biliardino-tag {
        background: linear-gradient(90deg, #ffd700, #ffaa00);
        color: #02040a;
        text-align: center;
        font-family: 'Orbitron', sans-serif;
        font-weight: 900;
        font-size: 0.8em;
        text-transform: uppercase;
        letter-spacing: 2px;
        padding: 6px;
        border-radius: 4px;
        margin-bottom: 14px;
        box-shadow: 0 0 12px rgba(255, 215, 0, 0.4);
    }

    /* Box Squadre */
    .pro-team-box {
        background: #060c18;
        border: 1px solid #1e293b;
        border-radius: 6px;
        padding: 12px;
        text-align: center;
    }

    .pro-player-names {
        font-family: 'Orbitron', sans-serif;
        font-size: 1em;
        font-weight: 700;
        text-transform: uppercase;
        color: #ffd700 !important;
        letter-spacing: 1.5px;
        text-shadow: 0 0 8px rgba(255, 215, 0, 0.3);
    }

    /* Separatore VS */
    .pro-vs {
        text-align: center;
        font-family: 'Orbitron', sans-serif;
        font-weight: 900;
        color: #b026ff;
        font-size: 1.1em;
        margin: 10px 0;
        letter-spacing: 3px;
        text-shadow: 0 0 10px rgba(176, 38, 255, 0.5);
    }

    /* Pulsanti Vittoria - Gradiente Blu/Azzurro Neon */
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
        transition: all 0.2s ease;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #007bff, #00bfff) !important;
        border-color: #ffffff !important;
        box-shadow: 0 0 20px rgba(0, 243, 255, 0.6);
        transform: translateY(-1px);
    }

    /* Pannelli Classifiche */
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
        text-shadow: 0 0 8px rgba(0, 243, 255, 0.4);
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

    /* Podio e Hall of Fame */
    .pro-podium-card {
        background: linear-gradient(145deg, #100824, #060a14);
        border: 2px solid #b026ff;
        border-radius: 10px;
        padding: 18px;
        margin-bottom: 20px;
        box-shadow: 0 0 25px rgba(176, 38, 255, 0.3);
    }
    .pro-podium-title {
        text-align: center;
        font-family: 'Orbitron', sans-serif;
        font-size: 1.2em;
        font-weight: 900;
        color: #e2e8f0;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 16px;
        border-bottom: 1px solid #b026ff;
        padding-bottom: 8px;
        text-shadow: 0 0 10px rgba(176, 38, 255, 0.5);
    }
    .pro-podium-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: #0b1326;
        padding: 10px 14px;
        border-radius: 6px;
        margin-bottom: 8px;
        border: 1px solid #1e293b;
    }
    .pos-1 { border-left: 4px solid #ffd700; box-shadow: 0 0 10px rgba(255, 215, 0, 0.2); }
    .pos-2 { border-left: 4px solid #94a3b8; box-shadow: 0 0 10px rgba(148, 163, 184, 0.2); }
    .pos-3 { border-left: 4px solid #d97706; box-shadow: 0 0 10px rgba(217, 119, 6, 0.2); }
    .pos-4 { border-left: 4px solid #00f3ff; box-shadow: 0 0 10px rgba(0, 243, 255, 0.2); }
    
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
    normal_style = styles['Normal']
    
    elements.append(Paragraph("PRO ESPORTS ARENA // REPORT UFFICIALE", title_style))
    elements.append(Paragraph("Storico Partite e Risultati del Torneo", ParagraphStyle('Sub', parent=normal_style, alignment=1, textColor=colors.HexColor("#94a3b8"))))
    elements.append(Spacer(1, 15))
    
    if st.session_state.match_history:
        for item in st.session_state.match_history:
            turno_num = item["turno"]
            elements.append(Paragraph(f"Turno N° {turno_num}", subtitle_style))
            
            table_data = [["Biliardino", "Squadra A", "Squadra B", "Esito"]]
            for idx, m in enumerate(item["partite"]):
                tA = f"⚽️ {m['tA_att']} & 🥅 {m['tA_port']}"
                tB = f"⚽️ {m['tB_att']} & 🥅 {m['tB_port']}"
                vincitore = m.get('vincitore', 'Completata')
                table_data.append([str(idx+1), tA, tB, vincitore])
                
            t = Table(table_data, colWidths=[65, 200, 200, 85])
            t.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#060a14")),
                ('TEXTCOLOR', (0,0), (-1,0), colors.HexColor("#00f3ff")),
                ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0,0), (-1,0), 6),
                ('BACKGROUND', (0,1), (-1,-1), colors.HexColor("#0b1326")),
                ('TEXTCOLOR', (0,1), (-1,-1), colors.HexColor("#e2e8f0")),
                ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#1e293b")),
                ('FONTSIZE', (0,0), (-1,-1), 8.5),
            ]))
            elements.append(t)
            elements.append(Spacer(1, 10))
    else:
        elements.append(Paragraph("Nessuna partita registrata nello storico.", normal_style))
        
    doc.build(elements)
    buffer.seek(0)
    return buffer.getvalue()

st.sidebar.title("🔐 SECURITY & ADMIN")
admin_code = st.sidebar.text_input("Codice Amministratore", type="password", placeholder="Inserisci 0000")
is_admin = (admin_code == "0000")

if is_admin:
    st.sidebar.success("ADMIN MODE ACTIVE 🔓")
else:
    st.sidebar.info("Player / Viewer Mode ⚡")

nomi_giocatori = sorted(list(set([p["name"] for p in st.session_state.players]))) if st.session_state.players else []

if st.session_state.giocatore_selezionato is None:
    st.title("PRO TOURNAMENT ARENA")
    st.markdown("""
        <div style="background: rgba(0, 243, 255, 0.05); border: 1px solid #00f3ff; border-radius: 6px; padding: 15px; text-align: center; font-size: 1em; color: #e2e8f0; margin-bottom: 20px;">
            🎮 <b>PLAYER AUTH:</b> Seleziona il tuo profilo dalla lista per accedere all'interfaccia di gara.
        </div>
    """, unsafe_allow_html=True)

    if nomi_giocatori:
        with st.container(border=True):
            st.markdown("### 👤 SELEZIONA UTENTE:")
            nome_scelto_temp = st.selectbox("Iscritti:", nomi_giocatori, label_visibility="collapsed")
            
            col_b1, col_b2, col_b3 = st.columns([1, 2, 1])
            with col_b2:
                if st.button("ACCEDI ALLA COMPETIZIONE", type="primary", use_container_width=True):
                    st.session_state.giocatore_selezionato = nome_scelto_temp
                    st.rerun()
    else:
        st.warning("⚠️ Nessun partecipante caricato. Inserisci i dati dal pannello Admin.")
        
    if is_admin:
        with st.expander("⚙️ Pannello Configurazione & Gestione (Admin)", expanded=True):
            col_conf1, col_conf2 = st.columns(2)
            with col_conf1:
                st.session_state.initial_lives = st.number_input("Vite iniziali", min_value=1, max_value=10, value=st.session_state.initial_lives)
            with col_conf2:
                st.session_state.num_biliardini = st.number_input("Numero Biliardini", min_value=1, max_value=10, value=st.session_state.num_biliardini)
            
            st.markdown("---")
            lista_input_testo = st.text_area("Incolla partecipanti (es: 1 ⚽️ Nome, 2 🥅 Nome):", height=80)
            
            if st.button("📥 Importa e Registra Giocatori", type="primary"):
                righe = lista_input_testo.split("\n")
                count_aggiunti = 0
                for riga in righe:
                    riga_pulita = riga.strip()
                    if not riga_pulita: continue
                    role = None
                    if "🥅" in riga_pulita: role = "portiere"
                    elif "⚽️" in riga_pulita or "⚽" in riga_pulita: role = "attaccante"
                    
                    if role:
                        nome = riga_pulita.replace("🥅", "").replace("⚽️", "").replace("⚽", "")
                        nome = re.sub(r'^\d+[\.\-\s]*', '', nome).strip()
                        if nome and not any(p["name"].lower() == nome.lower() and p["role"] == role for p in st.session_state.players):
                            st.session_state.players.append({
                                "id": len(st.session_state.players) + 1,
                                "name": nome, "role": role,
                                "lives": st.session_state.initial_lives,
                                "max_lives": st.session_state.initial_lives,
                                "eliminated": False, "last_result": None
                            })
                            count_aggiunti += 1
                salva_stato()
                st.success(f"Importati {count_aggiunti} giocatori.")
                st.rerun()

            attaccanti = [p for p in st.session_state.players if p["role"] == "attaccante"]
            portieri = [p for p in st.session_state.players if p["role"] == "portiere"]
            st.info(f"📊 Registrati: ⚽️ {len(attaccanti)} Attaccanti | 🥅 {len(portieri)} Portieri")

            if len(st.session_state.players) >= 2:
                if not st.session_state.tournament_started:
                    if st.button("🚀 Avvia Torneo", type="primary"):
                        st.session_state.tournament_started = True
                        st.session_state.round_number = 1
                        st.session_state.history = []
                        st.session_state.match_history = []
                        st.session_state.current_round_matches = genera_abbinamenti()
                        salva_stato()
                        st.rerun()
                if st.button("🛑 Reset Torneo"):
                    st.session_state.tournament_started = False
                    st.session_state.current_round_matches = []
                    st.session_state.round_number = 0
                    st.session_state.players = []
                    st.session_state.history = []
                    st.session_state.match_history = []
                    if os.path.exists(STATE_FILE):
                        os.remove(STATE_FILE)
                    st.rerun()

    st.stop()

st.title("PRO ESPORTS ARENA")

col_u1, col_u2 = st.columns([3, 1])
with col_u1:
    giocatore_selezionato = st.session_state.giocatore_selezionato
    st.info(f"⚡ Operatore Connesso: **{giocatore_selezionato.upper()}**")
with col_u2:
    if st.button("🔄 Logout", use_container_width=True):
        st.session_state.giocatore_selezionato = None
        st.session_state.vista_personale_attiva = False
        st.rerun()

etichetta_occhio = "👁️ Disattiva Filtro Personale" if st.session_state.vista_personale_attiva else "👁️ Vista Personale (Mostra solo i miei match)"
if st.button(etichetta_occhio, use_container_width=True):
    st.session_state.vista_personale_attiva = not st.session_state.vista_personale_attiva
    st.rerun()

if is_admin:
    with st.expander("⚙️ Pannello Configurazione & Gestione", expanded=not st.session_state.tournament_started):
        if not st.session_state.tournament_started:
            col_conf1, col_conf2 = st.columns(2)
            with col_conf1:
                st.session_state.initial_lives = st.number_input("Vite iniziali", min_value=1, max_value=10, value=st.session_state.initial_lives)
            with col_conf2:
                st.session_state.num_biliardini = st.number_input("Numero Biliardini", min_value=1, max_value=10, value=st.session_state.num_biliardini)
            
            st.markdown("---")
            lista_input_testo = st.text_area("Incolla partecipanti (es: 1 ⚽️ Nome, 2 🥅 Nome):", height=80)
            
            if st.button("📥 Importa e Registra Giocatori", type="primary"):
                righe = lista_input_testo.split("\n")
                count_aggiunti = 0
                for riga in righe:
                    riga_pulita = riga.strip()
                    if not riga_pulita: continue
                    role = None
                    if "🥅" in riga_pulita: role = "portiere"
                    elif "⚽️" in riga_pulita or "⚽" in riga_pulita: role = "attaccante"
                    
                    if role:
                        nome = riga_pulita.replace("🥅", "").replace("⚽️", "").replace("⚽", "")
                        nome = re.sub(r'^\d+[\.\-\s]*', '', nome).strip()
                        if nome and not any(p["name"].lower() == nome.lower() and p["role"] == role for p in st.session_state.players):
                            st.session_state.players.append({
                                "id": len(st.session_state.players) + 1,
                                "name": nome, "role": role,
                                "lives": st.session_state.initial_lives,
                                "max_lives": st.session_state.initial_lives,
                                "eliminated": False, "last_result": None
                            })
                            count_aggiunti += 1
                salva_stato()
                st.success(f"Importati {count_aggiunti} giocatori.")
                st.rerun()

        attaccanti = [p for p in st.session_state.players if p["role"] == "attaccante"]
        portieri = [p for p in st.session_state.players if p["role"] == "portiere"]
        st.info(f"📊 Registrati: ⚽️ {len(attaccanti)} Attaccanti | 🥅 {len(portieri)} Portieri")

        if len(st.session_state.players) >= 2:
            col_act1, col_act2 = st.columns(2)
            with col_act1:
                if not st.session_state.tournament_started:
                    if st.button("🚀 Avvia Torneo", type="primary"):
                        st.session_state.tournament_started = True
                        st.session_state.round_number = 1
                        st.session_state.history = []
                        st.session_state.match_history = []
                        st.session_state.current_round_matches = genera_abbinamenti()
                        salva_stato()
                        st.rerun()
            with col_act2:
                if st.button("🛑 Reset Torneo"):
                    st.session_state.tournament_started = False
                    st.session_state.current_round_matches = []
                    st.session_state.round_number = 0
                    st.session_state.players = []
                    st.session_state.history = []
                    st.session_state.match_history = []
                    if os.path.exists(STATE_FILE):
                        os.remove(STATE_FILE)
                    st.rerun()

if st.session_state.tournament_started:
    pdf_data = genera_pdf_report()
    st.sidebar.markdown("---")
    st.sidebar.download_button(
        label="📥 Download Report PDF",
        data=pdf_data,
        file_name="report_torneo_pro.pdf",
        mime="application/pdf",
        use_container_width=True
    )

st.markdown("---")

attivi_att = [p for p in st.session_state.players if p["role"] == "attaccante" and not p["eliminated"]]
attivi_port = [p for p in st.session_state.players if p["role"] == "portiere" and not p["eliminated"]]
torneo_finito = st.session_state.tournament_started and (len(attivi_att) < 2 or len(attivi_port) < 2)

if st.session_state.tournament_started:
    if torneo_finito:
        st.markdown("""
            <div style="text-align: center; font-family: 'Orbitron', sans-serif; font-size: 1.8em; font-weight: 900; color: #ffd700; text-transform: uppercase; margin-bottom: 25px; letter-spacing: 3px; text-shadow: 0 0 15px rgba(255, 215, 0, 0.5);">
                🏆 HALL OF FAME // PODIO UFFICIALE 🏆
            </div>
        """, unsafe_allow_html=True)
        
        atts_sorted = sorted([p for p in st.session_state.players if p["role"] == "attaccante"], key=lambda x: (x["lives"], not x["eliminated"]), reverse=True)
        ports_sorted = sorted([p for p in st.session_state.players if p["role"] == "portiere"], key=lambda x: (x["lives"], not x["eliminated"]), reverse=True)
        
        col_pod1, col_pod2 = st.columns(2)
        with col_pod1:
            st.markdown("""
                <div class="pro-podium-card">
                    <div class="pro-podium-title">⚽️ Top Attaccanti</div>
            """, unsafe_allow_html=True)
            for rank, p in enumerate(atts_sorted[:4]):
                cuori = "❤️ " * p["lives"]
                bare = "⚰️ " * (p["max_lives"] - p["lives"])
                pos_class = f"pos-{rank+1}"
                st.markdown(f"""
                    <div class="pro-podium-row {pos_class}">
                        <span style="font-family: 'Orbitron', sans-serif; font-weight: 900; color: #f8fafc;">{rank+1}°</span>
                        <span style="font-family: 'Orbitron', sans-serif; font-weight: 700; color: #ffd700; text-transform: uppercase;">{p['name']}</span>
                        <span style="font-size: 0.8em;">{cuori}{bare}</span>
                    </div>
                """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
        with col_pod2:
            st.markdown("""
                <div class="pro-podium-card">
                    <div class="pro-podium-title">🥅 Top Portieri</div>
            """, unsafe_allow_html=True)
            for rank, p in enumerate(ports_sorted[:4]):
                cuori = "❤️ " * p["lives"]
                bare = "⚰️ " * (p["max_lives"] - p["lives"])
                pos_class = f"pos-{rank+1}"
                st.markdown(f"""
                    <div class="pro-podium-row {pos_class}">
                        <span style="font-family: 'Orbitron', sans-serif; font-weight: 900; color: #f8fafc;">{rank+1}°</span>
                        <span style="font-family: 'Orbitron', sans-serif; font-weight: 700; color: #ffd700; text-transform: uppercase;">{p['name']}</span>
                        <span style="font-size: 0.8em;">{cuori}{bare}</span>
                    </div>
                """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
        st.download_button(
            label="📄 Scarica Report Finale PDF",
            data=pdf_data,
            file_name="report_finale_pro.pdf",
            mime="application/pdf",
            use_container_width=True
        )
    else:
        data_turno = st.session_state.current_round_matches
        
        if data_turno and not data_turno.get("partite"):
            st.session_state.round_number += 1
            st.session_state.current_round_matches = genera_abbinamenti()
            salva_stato()
            st.rerun()

        if is_admin and len(st.session_state.history) > 0:
            if st.button("↩️ Annulla Ultima Azione (Undo)", type="secondary", use_container_width=True):
                last_state = st.session_state.history.pop()
                st.session_state.players = last_state.get("players", st.session_state.players)
                st.session_state.current_round_matches = last_state.get("current_round_matches", {})
                st.session_state.round_number = last_state.get("round_number", 1)
                st.session_state.match_history = last_state.get("match_history", [])
                salva_stato()
                st.rerun()

        st.markdown(f"""
            <div class="pro-turn-banner">
                ⚔️ TURNO DI GARA N° {st.session_state.round_number}
            </div>
        """, unsafe_allow_html=True)
        
        if data_turno and data_turno.get("pass"):
            pass_names = ", ".join([f"{p['name'].upper()}" for p in data_turno["pass"]])
            st.info(f"🛡️ **Riposo / Turno di Pass:** {pass_names}")

        partite = data_turno.get("partite", []) if data_turno else []
        
        if partite:
            num_biliardini = st.session_state.num_biliardini
            partite_in_corso = partite[:num_biliardini]
            partite_in_coda = partite[num_biliardini:]
            
            is_vista_personale = st.session_state.vista_personale_attiva

            if is_vista_personale:
                partite_filtrate = []
                for idx, match in enumerate(partite_in_corso):
                    tA_att, tA_port = match["teamA"]
                    tB_att, tB_port = match["teamB"]
                    nomi_partita = [tA_att['name'], tA_port['name'], tB_att['name'], tB_port['name']]
                    if any(n.lower() == giocatore_selezionato.lower() for n in nomi_partita):
                        partite_filtrate.append((idx, match))
                
                if not partite_filtrate:
                    st.info(f"☕️ Al momento {giocatore_selezionato.upper()} non ha match attivi in questo turno.")
                else:
                    st.markdown(f"#### 🎯 Match attivo per: {giocatore_selezionato.upper()}")
                
                iter_partite = partite_filtrate
            else:
                st.markdown("#### 🏟️ TAVOLI ATTIVI IN ARENA")
                iter_partite = [(idx, match) for idx, match in enumerate(partite_in_corso)]

            for idx, match in iter_partite:
                biliardino_num = idx + 1
                tA_att, tA_port = match["teamA"]
                tB_att, tB_port = match["teamB"]
                
                giocatore_nella_squadra_a = any(n.lower() == giocatore_selezionato.lower() for n in [tA_att['name'], tA_port['name']])
                giocatore_nella_squadra_b = any(n.lower() == giocatore_selezionato.lower() for n in [tB_att['name'], tB_port['name']])

                st.markdown(f"""
                    <div class="pro-match-card">
                        <div class="biliardino-tag">📍 BILIARDINO N. {biliardino_num}</div>
                """, unsafe_allow_html=True)
                
                st.markdown(f"""
                    <div class="pro-team-box">
                        <div class="pro-player-names">⚽️ {tA_att['name'].upper()} &nbsp;|&nbsp; 🥅 {tA_port['name'].upper()}</div>
                    </div>
                """, unsafe_allow_html=True)
                
                mostra_tasto_A = is_admin or is_vista_personale or giocatore_nella_squadra_a
                
                if mostra_tasto_A:
                    if st.button("⚡ REGISTRA VITTORIA SQUADRA A", key=f"win_A_{st.session_state.round_number}_{idx}", use_container_width=True):
                        salva_snapshot()
                        
                        match_record = {
                            "turno": st.session_state.round_number,
                            "partite": [{
                                "tA_att": tA_att['name'].upper(), "tA_port": tA_port['name'].upper(),
                                "tB_att": tB_att['name'].upper(), "tB_port": tB_port['name'].upper(),
                                "vincitore": f"Vittoria Squadra A (⚽️ {tA_att['name'].upper()} & 🥅 {tA_port['name'].upper()})"
                            }]
                        }
                        found_h = next((h for h in st.session_state.match_history if h["turno"] == st.session_state.round_number), None)
                        if found_h:
                            found_h["partite"].append(match_record["partite"][0])
                        else:
                            st.session_state.match_history.append(match_record)

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
                
                st.markdown("<div class='pro-vs'>VS</div>", unsafe_allow_html=True)
                
                st.markdown(f"""
                    <div class="pro-team-box">
                        <div class="pro-player-names">⚽️ {tB_att['name'].upper()} &nbsp;|&nbsp; 🥅 {tB_port['name'].upper()}</div>
                    </div>
                """, unsafe_allow_html=True)
                
                mostra_tasto_B = is_admin or is_vista_personale or giocatore_nella_squadra_b

                if mostra_tasto_B:
                    if st.button("⚡ REGISTRA VITTORIA SQUADRA B", key=f"win_B_{st.session_state.round_number}_{idx}", use_container_width=True):
                        salva_snapshot()
                        
                        match_record = {
                            "turno": st.session_state.round_number,
                            "partite": [{
                                "tA_att": tA_att['name'].upper(), "tA_port": tA_port['name'].upper(),
                                "tB_att": tB_att['name'].upper(), "tB_port": tB_port['name'].upper(),
                                "vincitore": f"Vittoria Squadra B (⚽️ {tB_att['name'].upper()} & 🥅 {tB_port['name'].upper()})"
                            }]
                        }
                        found_h = next((h for h in st.session_state.match_history if h["turno"] == st.session_state.round_number), None)
                        if found_h:
                            found_h["partite"].append(match_record["partite"][0])
                        else:
                            st.session_state.match_history.append(match_record)

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
                
                st.markdown("</div>", unsafe_allow_html=True)
                
            if partite_in_coda and not is_vista_personale:
                st.markdown("#### ⏳ MATCH IN CODA")
                for q_idx, q_match in enumerate(partite_in_coda):
                    qa, qp = q_match["teamA"]
                    qb, qpp = q_match["teamB"]
                    st.info(f"Coda #{q_idx+1}: [⚽️ {qa['name'].upper()} & 🥅 {qp['name'].upper()}] vs [⚽️ {qb['name'].upper()} & 🥅 {qpp['name'].upper()}]")

st.markdown("---")

# --- CLASSIFICA E VITE ---
if st.session_state.players:
    st.markdown("### 📊 STATISTICHE & VITE GIOCATORI")
    col_c1, col_c2 = st.columns(2)
    
    with col_c1:
        st.markdown("""
            <div class="pro-rank-container">
                <div class="pro-rank-header">⚽️ ATTACCANTI</div>
        """, unsafe_allow_html=True)
        for p in [x for x in st.session_state.players if x["role"] == "attaccante"]:
            cuori = "❤️ " * p["lives"]
            bare = "⚰️ " * (p["max_lives"] - p["lives"])
            vite_display = cuori + bare
            
            css_class = "pro-player-row pro-player-row-eliminated" if p["eliminated"] else "pro-player-row"
            name_class = "pro-rank-name-eliminated" if p["eliminated"] else "pro-rank-name"
            
            st.markdown(f"""
                <div class="{css_class}">
                    <span class="{name_class}">{p['name']}</span>
                    <span>{vite_display}</span>
                </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col_c2:
        st.markdown("""
            <div class="pro-rank-container">
                <div class="pro-rank-header">🥅 PORTIERI</div>
        """, unsafe_allow_html=True)
        for p in [x for x in st.session_state.players if x["role"] == "portiere"]:
            cuori = "❤️ " * p["lives"]
            bare = "⚰️ " * (p["max_lives"] - p["lives"])
            vite_display = cuori + bare
            
            css_class = "pro-player-row pro-player-row-eliminated" if p["eliminated"] else "pro-player-row"
            name_class = "pro-rank-name-eliminated" if p["eliminated"] else "pro-rank-name"
            
            st.markdown(f"""
                <div class="{css_class}">
                    <span class="{name_class}">{p['name']}</span>
                    <span>{vite_display}</span>
                </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
