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

st.set_page_config(page_title="TORNEO A VITE // ESPORTS ARENA", page_icon="⚡", layout="centered")

# --- STILE GRAFICO GAMING ELETTRICO & NEON ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;800;900&family=Rajdhani:wght@500;700&display=swap');

    /* Sfondo Generale Cyberpunk / Elettrico */
    .main { 
        background-color: #030712; 
        background-image: 
            radial-gradient(circle at 10% 20%, rgba(59, 130, 246, 0.08) 0%, transparent 40%),
            radial-gradient(circle at 90% 80%, rgba(168, 85, 247, 0.08) 0%, transparent 40%),
            linear-gradient(rgba(255, 255, 255, 0.02) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255, 255, 255, 0.02) 1px, transparent 1px);
        background-size: 100% 100%, 100% 100%, 30px 30px, 30px 30px;
        font-family: 'Rajdhani', sans-serif;
    }

    h1, h2, h3, h4, .stMarkdown {
        font-family: 'Orbitron', sans-serif !important;
    }

    /* Banner Turno In Evidenza - Neon Blu/Viola Elettrico */
    .turn-banner {
        background: linear-gradient(135deg, #1e1b4b, #312e81);
        border: 2px solid #818cf8;
        border-radius: 12px;
        padding: 14px 20px;
        text-align: center;
        color: #e0e7ff;
        font-family: 'Orbitron', sans-serif;
        font-size: 1.3em;
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: 3px;
        margin-bottom: 20px;
        box-shadow: 0 0 20px rgba(129, 140, 248, 0.4), inset 0 0 15px rgba(59, 130, 246, 0.3);
    }

    /* Avviso Informativo Rosso / Pericolo Neon */
    .info-red-box {
        background: linear-gradient(135deg, #450a0a, #7f1d1d);
        border: 2px solid #f87171;
        border-radius: 12px;
        padding: 14px 18px;
        color: #fee2e2;
        font-weight: 700;
        font-size: 0.95em;
        margin-bottom: 20px;
        box-shadow: 0 0 15px rgba(248, 113, 113, 0.4);
    }

    /* Avviso Ultima Partita - Arancio Elettrico */
    .last-match-warning {
        background: linear-gradient(135deg, #431407, #7c2d12);
        border: 2px dashed #fb923c;
        border-radius: 10px;
        padding: 12px;
        text-align: center;
        color: #ffedd5;
        font-family: 'Orbitron', sans-serif;
        font-weight: 800;
        font-size: 0.9em;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-bottom: 15px;
        box-shadow: 0 0 20px rgba(251, 146, 60, 0.5);
    }

    /* Intestazione Biliardino - Neon Oro/Ambra */
    .biliardino-header {
        background: linear-gradient(90deg, #d97706, #fbbf24, #d97706);
        color: #030712;
        text-align: center;
        font-family: 'Orbitron', sans-serif;
        font-weight: 900;
        font-size: 0.9em;
        text-transform: uppercase;
        letter-spacing: 2px;
        padding: 8px;
        border-radius: 8px;
        margin-bottom: 12px;
        box-shadow: 0 0 15px rgba(251, 191, 36, 0.5);
    }

    /* Box Squadra / Coppia - Neon Verde Elettrico */
    .team-box {
        background: linear-gradient(145deg, #022c22, #064e3b);
        border: 1px solid #34d399;
        border-radius: 10px;
        padding: 12px;
        text-align: center;
        color: #ecfdf5;
        box-shadow: 0 0 12px rgba(52, 211, 153, 0.25);
    }

    .player-names {
        font-family: 'Orbitron', sans-serif;
        font-size: 1.1em;
        font-weight: 900;
        line-height: 1.4;
        text-transform: uppercase;
        color: #fde047 !important;
        letter-spacing: 1px;
        text-shadow: 0 0 8px rgba(253, 224, 71, 0.4);
    }

    /* Scritta VS centrale stile Neon Azzurro */
    .vs-text {
        text-align: center;
        font-family: 'Orbitron', sans-serif;
        font-weight: 900;
        color: #38bdf8;
        font-size: 1.2em;
        margin: 10px 0;
        letter-spacing: 4px;
        text-shadow: 0 0 10px rgba(56, 189, 248, 0.6);
    }

    /* Stile Pulsanti Vittoria - Gradiente Azzurro/Blu Elettrico con Glow */
    .stButton > button {
        width: 100% !important;
        background: linear-gradient(135deg, #0284c7, #2563eb) !important;
        color: #ffffff !important;
        font-family: 'Orbitron', sans-serif !important;
        font-weight: 800 !important;
        border: 1px solid #38bdf8 !important;
        border-radius: 8px !important;
        padding: 8px 0px !important;
        font-size: 0.85em !important;
        letter-spacing: 1px !important;
        box-shadow: 0 0 15px rgba(2, 132, 199, 0.4);
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #0369a1, #1d4ed8) !important;
        border-color: #7dd3fc !important;
        box-shadow: 0 0 25px rgba(56, 189, 248, 0.8);
        transform: translateY(-2px);
    }

    /* Box Classifiche - Cyber Panel */
    .rank-container {
        background: linear-gradient(145deg, #0f172a, #020617);
        border: 1px solid #334155;
        border-radius: 14px;
        padding: 16px;
        margin-bottom: 16px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.6), inset 0 0 15px rgba(30, 41, 59, 0.5);
    }
    
    .rank-header {
        font-family: 'Orbitron', sans-serif;
        font-size: 1.15em;
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 14px;
        padding-bottom: 8px;
        border-bottom: 2px solid #38bdf8;
        color: #38bdf8;
        text-align: center;
        text-shadow: 0 0 10px rgba(56, 189, 248, 0.4);
    }

    .player-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: #1e293b;
        padding: 10px 14px;
        border-radius: 8px;
        margin-bottom: 8px;
        font-size: 0.95em;
        border: 1px solid #334155;
    }
    
    .player-row-eliminated {
        background: #090d16;
        opacity: 0.7;
        border: 1px solid #1f2937;
    }
    
    .rank-name {
        font-family: 'Orbitron', sans-serif;
        font-weight: 800;
        text-transform: uppercase;
        color: #facc15;
    }

    .rank-name-eliminated {
        font-family: 'Orbitron', sans-serif;
        font-weight: 800;
        text-transform: uppercase;
        color: #ef4444;
        text-decoration: line-through;
    }

    /* Stile Podio - Neon Dorato & Viola */
    .podium-card {
        background: linear-gradient(145deg, #2e1065, #0f172a);
        border: 2px solid #a855f7;
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 0 30px rgba(168, 85, 247, 0.4);
    }
    .podium-title {
        text-align: center;
        font-family: 'Orbitron', sans-serif;
        font-size: 1.3em;
        font-weight: 900;
        color: #f3e8ff;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 20px;
        border-bottom: 2px solid #7e22ce;
        padding-bottom: 10px;
        text-shadow: 0 0 10px rgba(168, 85, 247, 0.6);
    }
    .podium-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: rgba(15, 23, 42, 0.8);
        padding: 12px 16px;
        border-radius: 10px;
        margin-bottom: 10px;
        border: 1px solid #475569;
    }
    .podium-pos-1 { border-left: 6px solid #fbbf24; box-shadow: 0 0 12px rgba(251, 191, 36, 0.3); }
    .podium-pos-2 { border-left: 6px solid #cbd5e1; box-shadow: 0 0 12px rgba(203, 213, 225, 0.3); }
    .podium-pos-3 { border-left: 6px solid #d97706; box-shadow: 0 0 12px rgba(217, 119, 6, 0.3); }
    .podium-pos-4 { border-left: 6px solid #38bdf8; box-shadow: 0 0 12px rgba(56, 189, 248, 0.3); }
    
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
    title_style = ParagraphStyle('TitleStyle', parent=styles['Heading1'], fontSize=20, textColor=colors.HexColor("#38bdf8"), alignment=1, spaceAfter=15)
    subtitle_style = ParagraphStyle('SubTitleStyle', parent=styles['Heading2'], fontSize=14, textColor=colors.HexColor("#a855f7"), spaceBefore=15, spaceAfter=8)
    normal_style = styles['Normal']
    
    elements.append(Paragraph("⚡ ESPORTS ARENA - REPORT TORNEO A VITE", title_style))
    elements.append(Paragraph("Storico Partite e Risultati Ufficiali", ParagraphStyle('Sub', parent=normal_style, alignment=1, textColor=colors.HexColor("#64748b"))))
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
                ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1e1b4b")),
                ('TEXTCOLOR', (0,0), (-1,0), colors.white),
                ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0,0), (-1,0), 6),
                ('BACKGROUND', (0,1), (-1,-1), colors.HexColor("#0f172a")),
                ('TEXTCOLOR', (0,1), (-1,-1), colors.HexColor("#e2e8f0")),
                ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#334155")),
                ('FONTSIZE', (0,0), (-1,-1), 9),
            ]))
            elements.append(t)
            elements.append(Spacer(1, 10))
    else:
        elements.append(Paragraph("Nessuna partita registrata nello storico.", normal_style))
        
    elements.append(Spacer(1, 15))
    elements.append(Paragraph("Classifica Finale / Podio", subtitle_style))
    atts_sorted = sorted([p for p in st.session_state.players if p["role"] == "attaccante"], key=lambda x: (x["lives"], not x["eliminated"]), reverse=True)
    ports_sorted = sorted([p for p in st.session_state.players if p["role"] == "portiere"], key=lambda x: (x["lives"], not x["eliminated"]), reverse=True)
    
    podio_data = [["Posizione", "Attaccanti Top", "Vite", "Portieri Top", "Vite"]]
    for i in range(max(len(atts_sorted[:4]), len(ports_sorted[:4]))):
        pos = f"{i+1}°"
        att_name = atts_sorted[i]["name"].upper() if i < len(atts_sorted) else "-"
        att_lives = f"{atts_sorted[i]['lives']} ❤️" if i < len(atts_sorted) else "-"
        port_name = ports_sorted[i]["name"].upper() if i < len(ports_sorted) else "-"
        port_lives = f"{ports_sorted[i]['lives']} ❤️" if i < len(ports_sorted) else "-"
        podio_data.append([pos, att_name, att_lives, port_name, port_lives])
        
    t_podio = Table(podio_data, colWidths=[65, 175, 60, 175, 65])
    t_podio.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#2e1065")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#475569")),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor("#0f172a")),
        ('TEXTCOLOR', (0,1), (-1,-1), colors.HexColor("#e2e8f0")),
    ]))
    elements.append(t_podio)
    
    doc.build(elements)
    buffer.seek(0)
    return buffer.getvalue()

st.sidebar.title("🔐 SECURITY & ADMIN")
admin_code = st.sidebar.text_input("Codice Amministratore", type="password", placeholder="Inserisci 0000")
is_admin = (admin_code == "0000")

if is_admin:
    st.sidebar.success("MODALITÀ ADMIN ATTIVA 🔓")
else:
    st.sidebar.info("Modalità Player / Viewer ⚡")

# --- PAGINA INIZIALE DI ACCESSO OBBLIGATO SE NON SELEZIONATO ---
nomi_giocatori = sorted(list(set([p["name"] for p in st.session_state.players]))) if st.session_state.players else []

if st.session_state.giocatore_selezionato is None:
    st.title("⚡ TORNEO A VITE // ARENA")
    st.markdown("""
        <div class="info-red-box" style="text-align: center; font-size: 1.1em;">
            🎮 <b>PLAYER LOGIN:</b> Seleziona il tuo nickname dalla lista sottostante e premi <b>ACCEDI ALL'ARENA</b> per entrare nel match.
        </div>
    """, unsafe_allow_html=True)

    if nomi_giocatori:
        with st.container(border=True):
            st.markdown("### 👤 SELEZIONA IL TUO PROFILO:")
            nome_scelto_temp = st.selectbox("Iscritti:", nomi_giocatori, label_visibility="collapsed")
            
            col_b1, col_b2, col_b3 = st.columns([1, 2, 1])
            with col_b2:
                if st.button("🚀 ACCEDI ALL'ARENA", type="primary", use_container_width=True):
                    st.session_state.giocatore_selezionato = nome_scelto_temp
                    st.rerun()
    else:
        st.warning("⚠️ Nessun giocatore registrato nel sistema. Chiedi all'admin di importare i partecipanti.")
        
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
                st.success(f"Importati {count_aggiunti} giocatori!")
                st.rerun()

            attaccanti = [p for p in st.session_state.players if p["role"] == "attaccante"]
            portieri = [p for p in st.session_state.players if p["role"] == "portiere"]
            st.info(f"📊 Iscritti: ⚽️ {len(attaccanti)} Attaccanti | 🥅 {len(portieri)} Portieri")

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
                if st.button("🛑 Reset Totale"):
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

# --- TITOLO PRINCIPALE TORNEO ---
st.title("⚡ TORNEO A VITE // BATTLE ARENA")

col_u1, col_u2 = st.columns([3, 1])
with col_u1:
    giocatore_selezionato = st.session_state.giocatore_selezionato
    st.info(f"🎮 Operatore attivo: **{giocatore_selezionato.upper()}**")
with col_u2:
    if st.button("🔄 Cambia Utente", use_container_width=True):
        st.session_state.giocatore_selezionato = None
        st.session_state.vista_personale_attiva = False
        st.rerun()

etichetta_occhio = "👁️ Disattiva Vista Personale" if st.session_state.vista_personale_attiva else "👁️ Vista Personale (Solo la mia partita)"
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
                st.success(f"Importati {count_aggiunti} giocatori!")
                st.rerun()

        attaccanti = [p for p in st.session_state.players if p["role"] == "attaccante"]
        portieri = [p for p in st.session_state.players if p["role"] == "portiere"]
        st.info(f"📊 Iscritti: ⚽️ {len(attaccanti)} Attaccanti | 🥅 {len(portieri)} Portieri")

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
                if st.button("🛑 Reset Totale"):
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
        label="📥 Scarica Report PDF Partite",
        data=pdf_data,
        file_name="report_torneo_esports.pdf",
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
            <div style="text-align: center; font-family: 'Orbitron', sans-serif; font-size: 2em; font-weight: 900; color: #fbbf24; text-transform: uppercase; margin-bottom: 20px; letter-spacing: 3px; text-shadow: 0 0 15px rgba(251, 191, 36, 0.6);">
                🏆 HALL OF FAME // PODIO FINALE 🏆
            </div>
        """, unsafe_allow_html=True)
        
        atts_sorted = sorted([p for p in st.session_state.players if p["role"] == "attaccante"], key=lambda x: (x["lives"], not x["eliminated"]), reverse=True)
        ports_sorted = sorted([p for p in st.session_state.players if p["role"] == "portiere"], key=lambda x: (x["lives"], not x["eliminated"]), reverse=True)
        
        col_pod1, col_pod2 = st.columns(2)
        with col_pod1:
            st.markdown("""
                <div class="podium-card">
                    <div class="podium-title">⚽️ Top Attaccanti</div>
            """, unsafe_allow_html=True)
            for rank, p in enumerate(atts_sorted[:4]):
                cuori = "❤️ " * p["lives"]
                bare = "⚰️ " * (p["max_lives"] - p["lives"])
                pos_class = f"podium-pos-{rank+1}"
                st.markdown(f"""
                    <div class="podium-row {pos_class}">
                        <span style="font-family: 'Orbitron', sans-serif; font-weight: 900; color: #f8fafc;">{rank+1}°</span>
                        <span style="font-family: 'Orbitron', sans-serif; font-weight: 800; color: #facc15; text-transform: uppercase;">{p['name']}</span>
                        <span style="font-size: 0.85em;">{cuori}{bare}</span>
                    </div>
                """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
        with col_pod2:
            st.markdown("""
                <div class="podium-card">
                    <div class="podium-title">🥅 Top Portieri</div>
            """, unsafe_allow_html=True)
            for rank, p in enumerate(ports_sorted[:4]):
                cuori = "❤️ " * p["lives"]
                bare = "⚰️ " * (p["max_lives"] - p["lives"])
                pos_class = f"podium-pos-{rank+1}"
                st.markdown(f"""
                    <div class="podium-row {pos_class}">
                        <span style="font-family: 'Orbitron', sans-serif; font-weight: 900; color: #f8fafc;">{rank+1}°</span>
                        <span style="font-family: 'Orbitron', sans-serif; font-weight: 800; color: #facc15; text-transform: uppercase;">{p['name']}</span>
                        <span style="font-size: 0.85em;">{cuori}{bare}</span>
                    </div>
                """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
        st.download_button(
            label="📄 Scarica Report Finale in PDF",
            data=pdf_data,
            file_name="report_finale_esports.pdf",
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
            if st.button("↩️ Annulla Ultimo Risultato (Undo)", type="secondary", use_container_width=True):
                last_state = st.session_state.history.pop()
                st.session_state.players = last_state.get("players", st.session_state.players)
                st.session_state.current_round_matches = last_state.get("current_round_matches", {})
                st.session_state.round_number = last_state.get("round_number", 1)
                st.session_state.match_history = last_state.get("match_history", [])
                salva_stato()
                st.rerun()

        st.markdown("""
            <div style="background: linear-gradient(135deg, #78350f, #b45309); border: 2px solid #fbbf24; border-radius: 12px; padding: 12px 18px; color: #fef3c7; font-weight: 700; font-size: 0.95em; text-align: center; margin-bottom: 20px; box-shadow: 0 0 15px rgba(251, 191, 36, 0.4);">
                ⚡ <b>REGOLA MATCH:</b> Assegna la vittoria cliccando sul pulsante della squadra vincente!
            </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
            <div class="turn-banner">
                ⚔️ TURNO N° {st.session_state.round_number}
            </div>
        """, unsafe_allow_html=True)
        
        if data_turno and data_turno.get("pass"):
            pass_names = ", ".join([f"{p['name'].upper()}" for p in data_turno["pass"]])
            st.info(f"💚 **In Attesa / Ripposo (Pass):** {pass_names}")

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
                    st.info(f"☕️ Al momento {giocatore_selezionato.upper()} non è impegnato in questo turno.")
                else:
                    st.markdown(f"#### 🎯 Match attivo per: {giocatore_selezionato.upper()} (Vista Personale)")
                
                iter_partite = partite_filtrate
            else:
                is_last_match_of_round = (len(partite_in_corso) == 1 and len(partite_in_coda) == 0)
                if is_last_match_of_round:
                    st.markdown("""
                        <div class="last-match-warning">
                            ⚠️ ULTIMO MATCH DEL TURNO! Assegnando la vittoria si passerà direttamente al turno successivo.
                        </div>
                    """, unsafe_allow_html=True)
                st.markdown("#### 🏟️ ARENA MATCH IN CORSO")
                iter_partite = [(idx, match) for idx, match in enumerate(partite_in_corso)]

            for idx, match in iter_partite:
                biliardino_num = idx + 1
                tA_att, tA_port = match["teamA"]
                tB_att, tB_port = match["teamB"]
                
                giocatore_nella_squadra_a = any(n.lower() == giocatore_selezionato.lower() for n in [tA_att['name'], tA_port['name']])
                giocatore_nella_squadra_b = any(n.lower() == giocatore_selezionato.lower() for n in [tB_att['name'], tB_port['name']])

                with st.container(border=True):
                    st.markdown(f"""
                        <div class="biliardino-header">📍 BILIARDINO N. {biliardino_num}</div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown(f"""
                        <div class="team-box">
                            <div class="player-names">⚽️ {tA_att['name'].upper()} &nbsp;|&nbsp; 🥅 {tA_port['name'].upper()}</div>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    mostra_tasto_A = is_admin or is_vista_personale or giocatore_nella_squadra_a
                    
                    if mostra_tasto_A:
                        if st.button("⚡ VITTORIA SQUADRA A", key=f"win_A_{st.session_state.round_number}_{idx}", use_container_width=True):
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
                    
                    st.markdown("<div class='vs-text'>VS</div>", unsafe_allow_html=True)
                    
                    st.markdown(f"""
                        <div class="team-box">
                            <div class="player-names">⚽️ {tB_att['name'].upper()} &nbsp;|&nbsp; 🥅 {tB_port['name'].upper()}</div>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    mostra_tasto_B = is_admin or is_vista_personale or giocatore_nella_squadra_b

                    if mostra_tasto_B:
                        if st.button("⚡ VITTORIA SQUADRA B", key=f"win_B_{st.session_state.round_number}_{idx}", use_container_width=True):
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
                
            if partite_in_coda and not is_vista_personale:
                st.markdown("#### ⏳ MATCH IN CODA D'ATTESA")
                for q_idx, q_match in enumerate(partite_in_coda):
                    qa, qp = q_match["teamA"]
                    qb, qpp = q_match["teamB"]
                    st.warning(f"Coda #{q_idx+1}: [⚽️ {qa['name'].upper()} & 🥅 {qp['name'].upper()}] vs [⚽️ {qb['name'].upper()} & 🥅 {qpp['name'].upper()}]")

st.markdown("---")

# --- CLASSIFICA & VITE AGGIORNATA ---
if st.session_state.players:
    st.markdown("### 📊 STATS & VITE GIOCATORI")
    col_c1, col_c2 = st.columns(2)
    
    with col_c1:
        st.markdown("""
            <div class="rank-container">
                <div class="rank-header">⚽️ ATTACCANTI STATS</div>
        """, unsafe_allow_html=True)
        for p in [x for x in st.session_state.players if x["role"] == "attaccante"]:
            cuori = "❤️ " * p["lives"]
            bare = "⚰️ " * (p["max_lives"] - p["lives"])
            vite_display = cuori + bare
            
            css_class = "player-row player-row-eliminated" if p["eliminated"] else "player-row"
            name_class = "rank-name-eliminated" if p["eliminated"] else "rank-name"
            
            st.markdown(f"""
                <div class="{css_class}">
                    <span class="{name_class}">{p['name']}</span>
                    <span>{vite_display}</span>
                </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col_c2:
        st.markdown("""
            <div class="rank-container">
                <div class="rank-header">🥅 PORTIERI STATS</div>
        """, unsafe_allow_html=True)
        for p in [x for x in st.session_state.players if x["role"] == "portiere"]:
            cuori = "❤️ " * p["lives"]
            bare = "⚰️ " * (p["max_lives"] - p["lives"])
            vite_display = cuori + bare
            
            css_class = "player-row player-row-eliminated" if p["eliminated"] else "player-row"
            name_class = "rank-name-eliminated" if p["eliminated"] else "rank-name"
            
            st.markdown(f"""
                <div class="{css_class}">
                    <span class="{name_class}">{p['name']}</span>
                    <span>{vite_display}</span>
                </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
