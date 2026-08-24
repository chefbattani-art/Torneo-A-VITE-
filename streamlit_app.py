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

st.set_page_config(page_title="Torneo A Vite - Calcio Balilla", page_icon="⚽️", layout="centered")

# --- STILE GRAFICO PROFESSIONALE (DASHBOARD SPORTIVA) ---
st.markdown("""
    <style>
    .main { background-color: #0b0f19; }
    
    /* Banner Turno In Evidenza */
    .turn-banner {
        background: linear-gradient(135deg, #1e3a8a, #3b82f6);
        border: 1px solid #60a5fa;
        border-radius: 12px;
        padding: 12px 20px;
        text-align: center;
        color: #ffffff;
        font-size: 1.2em;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 20px;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
    }

    /* Avviso Ultima Partita */
    .last-match-warning {
        background: linear-gradient(135deg, #7c2d12, #c2410c);
        border: 2px dashed #fb923c;
        border-radius: 10px;
        padding: 10px;
        text-align: center;
        color: #ffedd5;
        font-weight: 800;
        font-size: 0.95em;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 15px;
        box-shadow: 0 0 15px rgba(234, 88, 12, 0.4);
    }

    /* Stile per l'intestazione del biliardino dentro il box */
    .biliardino-header {
        background: linear-gradient(90deg, #f59e0b, #d97706);
        color: #0f172a;
        text-align: center;
        font-weight: 800;
        font-size: 0.85em;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        padding: 6px;
        border-radius: 8px;
        margin-bottom: 12px;
    }

    /* Box Squadra / Coppia */
    .team-box {
        background: linear-gradient(145deg, #064e3b, #022c22);
        border: 1px solid #059669;
        border-radius: 10px;
        padding: 10px;
        text-align: center;
        color: #ecfdf5;
        box-shadow: 0 4px 6px rgba(0,0,0,0.2);
    }

    .player-names {
        font-size: 1.05em;
        font-weight: 800;
        line-height: 1.4;
        text-transform: uppercase;
        color: #facc15 !important;
        letter-spacing: 0.5px;
    }

    /* Scritta VS centrale */
    .vs-text {
        text-align: center;
        font-weight: 900;
        color: #f59e0b;
        font-size: 1.1em;
        margin: 8px 0;
        letter-spacing: 2px;
    }

    /* Stile Pulsanti Vittoria */
    .stButton > button {
        width: 100% !important;
        background: linear-gradient(135deg, #0284c7, #0369a1) !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        border: 1px solid #38bdf8 !important;
        border-radius: 8px !important;
        padding: 6px 0px !important;
        font-size: 0.8em !important;
        box-shadow: 0 4px 6px rgba(2, 132, 199, 0.2);
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #0369a1, #075985) !important;
        border-color: #7dd3fc !important;
    }

    /* Box Classifiche */
    .rank-container {
        background: linear-gradient(145deg, #131b2e, #0d1322);
        border: 1px solid #1e293b;
        border-radius: 14px;
        padding: 16px;
        margin-bottom: 16px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
    }
    
    .rank-header {
        font-size: 1.15em;
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-bottom: 14px;
        padding-bottom: 8px;
        border-bottom: 3px solid #334155;
        color: #38bdf8;
        text-align: center;
    }

    .player-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: #1e293b;
        padding: 8px 12px;
        border-radius: 8px;
        margin-bottom: 8px;
        font-size: 0.95em;
        border: 1px solid #334155;
    }
    
    .player-row-eliminated {
        background: #111827;
        opacity: 0.8;
        border: 1px solid #374151;
    }
    
    .rank-name {
        font-weight: 800;
        text-transform: uppercase;
        color: #facc15;
    }

    .rank-name-eliminated {
        font-weight: 800;
        text-transform: uppercase;
        color: #ef4444;
        text-decoration: line-through;
    }

    /* Stile Podio Professionale */
    .podium-card {
        background: linear-gradient(145deg, #1e1b4b, #0f172a);
        border: 2px solid #6366f1;
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 8px 25px rgba(99, 102, 241, 0.3);
    }
    .podium-title {
        text-align: center;
        font-size: 1.4em;
        font-weight: 900;
        color: #f8fafc;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 20px;
        border-bottom: 2px solid #312e81;
        padding-bottom: 10px;
    }
    .podium-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: rgba(30, 41, 59, 0.7);
        padding: 10px 14px;
        border-radius: 10px;
        margin-bottom: 10px;
        border: 1px solid #334155;
    }
    .podium-pos-1 { border-left: 6px solid #fbbf24; }
    .podium-pos-2 { border-left: 6px solid #94a3b8; }
    .podium-pos-3 { border-left: 6px solid #b45309; }
    .podium-pos-4 { border-left: 6px solid #38bdf8; }
    
    div.block-container {
        padding-top: 1rem;
        padding-bottom: 2rem;
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

def salva_snapshot():
    # Salva una copia profonda dello stato attuale per permettere il ripristino (undo)
    snapshot = {
        "players": json.loads(json.dumps(st.session_state.players)),
        "current_round_matches": json.loads(json.dumps(st.session_state.current_round_matches)),
        "round_number": st.session_state.round_number
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
        
    res = {"partite": partite, "pass": avanzi}
    return res

def genera_pdf_report():
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
    elements = []
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontSize=20,
        textColor=colors.HexColor("#1e3a8a"),
        alignment=1,
        spaceAfter=15
    )
    subtitle_style = ParagraphStyle(
        'SubTitleStyle',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor("#334155"),
        spaceBefore=15,
        spaceAfter=8
    )
    normal_style = styles['Normal']
    
    elements.append(Paragraph("⚽️ REPORT UFFICIALE - TORNEO A VITE", title_style))
    elements.append(Paragraph("Storico Partite e Risultati", ParagraphStyle('Sub', parent=normal_style, alignment=1, textColor=colors.HexColor("#64748b"))))
    elements.append(Spacer(1, 15))
    
    if st.session_state.match_history:
        for item in st.session_state.match_history:
            turno_num = item["turno"]
            elements.append(Paragraph(f"Turno N° {turno_num}", subtitle_style))
            
            table_data = [["Biliardino", "Squadra A (Vincitrice/Perdente)", "Squadra B (Vincitrice/Perdente)", "Risultato/Esito"]]
            for idx, m in enumerate(item["partite"]):
                tA = f"⚽️ {m['tA_att']} & 🥅 {m['tA_port']}"
                tB = f"⚽️ {m['tB_att']} & 🥅 {m['tB_port']}"
                vincitore = m.get('vincitore', 'Completata')
                table_data.append([str(idx+1), tA, tB, vincitore])
                
            t = Table(table_data, colWidths=[65, 200, 200, 85])
            t.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#3b82f6")),
                ('TEXTCOLOR', (0,0), (-1,0), colors.white),
                ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0,0), (-1,0), 6),
                ('BACKGROUND', (0,1), (-1,-1), colors.HexColor("#f8fafc")),
                ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
                ('FONTSIZE', (0,0), (-1,-1), 9),
            ]))
            elements.append(t)
            elements.append(Spacer(1, 10))
    else:
        elements.append(Paragraph("Nessuna partita registrata nello storico.", normal_style))
        
    # Aggiungi Podio Finale se disponibile
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
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1e293b")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('FONTSIZE', (0,0), (-1,-1), 9),
    ]))
    elements.append(t_podio)
    
    doc.build(elements)
    buffer.seek(0)
    return buffer.getvalue()

st.sidebar.title("🔐 Accesso Admin")
admin_code = st.sidebar.text_input("Codice Amministratore", type="password", placeholder="Inserisci 0000")
is_admin = (admin_code == "0000")

if is_admin:
    st.sidebar.success("Modo Amministratore Attivo 🔓")
else:
    st.sidebar.info("Modalità Spettatore")

st.title("⚽️ Torneo a Vite")

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

# Download PDF Button in Sidebar or Main if tournament started
if st.session_state.tournament_started:
    pdf_data = genera_pdf_report()
    st.sidebar.markdown("---")
    st.sidebar.download_button(
        label="📥 Scarica Report PDF Partite",
        data=pdf_data,
        file_name="report_torneo_calcio_balilla.pdf",
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
            <div style="text-align: center; font-size: 2em; font-weight: 900; color: #f59e0b; text-transform: uppercase; margin-bottom: 20px; letter-spacing: 2px;">
                🏆 Podio Ufficiale Finale 🏆
            </div>
        """, unsafe_allow_html=True)
        
        atts_sorted = sorted([p for p in st.session_state.players if p["role"] == "attaccante"], key=lambda x: (x["lives"], not x["eliminated"]), reverse=True)
        ports_sorted = sorted([p for p in st.session_state.players if p["role"] == "portiere"], key=lambda x: (x["lives"], not x["eliminated"]), reverse=True)
        
        col_pod1, col_pod2 = st.columns(2)
        
        with col_pod1:
            st.markdown("""
                <div class="podium-card">
                    <div class="podium-title">⚽️ Attaccanti Top 4</div>
            """, unsafe_allow_html=True)
            for rank, p in enumerate(atts_sorted[:4]):
                cuori = "❤️ " * p["lives"]
                bare = "⚰️ " * (p["max_lives"] - p["lives"])
                pos_class = f"podium-pos-{rank+1}"
                st.markdown(f"""
                    <div class="podium-row {pos_class}">
                        <span style="font-weight: 900; color: #f8fafc;">{rank+1}° Posto</span>
                        <span style="font-weight: 800; color: #facc15; text-transform: uppercase;">{p['name']}</span>
                        <span style="font-size: 0.85em;">{cuori}{bare}</span>
                    </div>
                """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
        with col_pod2:
            st.markdown("""
                <div class="podium-card">
                    <div class="podium-title">🥅 Portieri Top 4</div>
            """, unsafe_allow_html=True)
            for rank, p in enumerate(ports_sorted[:4]):
                cuori = "❤️ " * p["lives"]
                bare = "⚰️ " * (p["max_lives"] - p["lives"])
                pos_class = f"podium-pos-{rank+1}"
                st.markdown(f"""
                    <div class="podium-row {pos_class}">
                        <span style="font-weight: 900; color: #f8fafc;">{rank+1}° Posto</span>
                        <span style="font-weight: 800; color: #facc15; text-transform: uppercase;">{p['name']}</span>
                        <span style="font-size: 0.85em;">{cuori}{bare}</span>
                    </div>
                """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
        # Pulsante download PDF anche al termine
        st.download_button(
            label="📄 Scarica il Report Completo in PDF (Risultati & Podio)",
            data=pdf_data,
            file_name="report_finale_torneo.pdf",
            mime="application/pdf",
            use_container_width=True
        )
    else:
        # Tendina di navigazione turni e tasto per tornare indietro
        max_turno_registrato = st.session_state.round_number
        turni_disponibili = list(range(1, max_turno_registrato + 1))
        
        col_nav1, col_nav2 = st.columns([2, 1])
        with col_nav1:
            selected_turno = st.selectbox(
                "📂 Seleziona Turno da Visualizzare / Verificare:",
                options=turni_disponibili,
                index=len(turni_disponibili)-1,
                key="turno_selezionato_selectbox"
            )
        with col_nav2:
            st.markdown("<div style='margin-top: 28px;'></div>", unsafe_allow_html=True)
            if is_admin and len(st.session_state.history) > 0:
                if st.button("↩️ Annulla / Turno Indietro", type="secondary"):
                    last_state = st.session_state.history.pop()
                    st.session_state.players = last_state["players"]
                    st.session_state.current_round_matches = last_state["current_round_matches"]
                    st.session_state.round_number = last_state["round_number"]
                    # Rimuovi l'ultimo record dallo storico match se necessario
                    if st.session_state.match_history:
                        st.session_state.match_history.pop()
                    salva_stato()
                    st.rerun()

        # Visualizzazione del turno selezionato dalla tendina
        if selected_turno < st.session_state.round_number:
            st.info(f"Stai visualizzando lo storico del **Turno N° {selected_turno}** (Consultazione).")
            # Cerca nel match_history se esiste
            match_storico_trovato = next((item for item in st.session_state.match_history if item["turno"] == selected_turno), None)
            if match_storico_trovato:
                for idx, m in enumerate(match_storico_trovato["partite"]):
                    with st.container(border=True):
                        st.markdown(f"<div class='biliardino-header'>📍 Biliardino N. {idx+1} (Concluso)</div>", unsafe_allow_html=True)
                        st.markdown(f"<div class='team-box'><div class='player-names'>⚽️ {m['tA_att']} &nbsp;|&nbsp; 🥅 {m['tA_port']}</div></div>", unsafe_allow_html=True)
                        st.markdown("<div class='vs-text'>VS</div>", unsafe_allow_html=True)
                        st.markdown(f"<div class='team-box'><div class='player-names'>⚽️ {m['tB_att']} &nbsp;|&nbsp; 🥅 {m['tB_port']}</div></div>", unsafe_allow_html=True)
                        st.success(f"🏆 Esito: {m.get('vincitore', 'Completata')}")
            else:
                st.warning("Nessun dettaglio salvato per questo turno passato.")
        else:
            # Turno corrente attivo
            st.markdown(f"""
                <div class="turn-banner">
                    ⚔️ Turno N° {st.session_state.round_number}
                </div>
            """, unsafe_allow_html=True)
            
            data_turno = st.session_state.current_round_matches
            
            if data_turno and not data_turno.get("partite"):
                st.session_state.round_number += 1
                st.session_state.current_round_matches = genera_abbinamenti()
                salva_stato()
                st.rerun()
                
            if data_turno and data_turno.get("pass"):
                pass_names = ", ".join([f"{p['name'].upper()}" for p in data_turno["pass"]])
                st.info(f"💚 **Riposano (Pass):** {pass_names}")

            partite = data_turno.get("partite", []) if data_turno else []
            
            if partite:
                num_biliardini = st.session_state.num_biliardini
                partite_in_corso = partite[:num_biliardini]
                partite_in_coda = partite[num_biliardini:]
                
                is_last_match_of_round = (len(partite_in_corso) == 1 and len(partite_in_coda) == 0)
                
                if is_last_match_of_round:
                    st.markdown("""
                        <div class="last-match-warning">
                            ⚠️ ULTIMA PARTITA DI QUESTO TURNO! Subito dopo si passerà automaticamente ai turni successivi.
                        </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("#### 🏟️ Partite in Corso")
                for idx, match in enumerate(partite_in_corso):
                    biliardino_num = idx + 1
                    tA_att, tA_port = match["teamA"]
                    tB_att, tB_port = match["teamB"]
                    
                    with st.container(border=True):
                        st.markdown(f"""
                            <div class="biliardino-header">📍 Biliardino N. {biliardino_num}</div>
                        """, unsafe_allow_html=True)
                        
                        st.markdown(f"""
                            <div class="team-box">
                                <div class="player-names">⚽️ {tA_att['name'].upper()} &nbsp;|&nbsp; 🥅 {tA_port['name'].upper()}</div>
                            </div>
                        """, unsafe_allow_html=True)
                        
                        if is_admin:
                            if st.button("🏆 Assegna Vittoria", key=f"win_A_{st.session_state.round_number}_{idx}", use_container_width=True):
                                # Salva snapshot prima di modificare per permettere l'undo
                                salva_snapshot()
                                
                                # Registra nel match history
                                match_record = {
                                    "turno": st.session_state.round_number,
                                    "partite": [{
                                        "tA_att": tA_att['name'].upper(), "tA_port": tA_port['name'].upper(),
                                        "tB_att": tB_att['name'].upper(), "tB_port": tB_port['name'].upper(),
                                        "vincitore": f"Vittoria Squadra A (⚽️ {tA_att['name'].upper()} & 🥅 {tA_port['name'].upper()})"
                                    }]
                                }
                                # Accoda o aggiorna nello storico match del turno corrente
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
                                salva_stato()
                                st.rerun()
                        
                        st.markdown("<div class='vs-text'>VS</div>", unsafe_allow_html=True)
                        
                        st.markdown(f"""
                            <div class="team-box">
                                <div class="player-names">⚽️ {tB_att['name'].upper()} &nbsp;|&nbsp; 🥅 {tB_port['name'].upper()}</div>
                            </div>
                        """, unsafe_allow_html=True)
                        
                        if is_admin:
                            if st.button("🏆 Assegna Vittoria", key=f"win_B_{st.session_state.round_number}_{idx}", use_container_width=True):
                                # Salva snapshot prima di modificare per permettere l'undo
                                salva_snapshot()
                                
                                # Registra nel match history
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
                                salva_stato()
                                st.rerun()
                    
                if partite_in_coda:
                    st.markdown("#### ⏳ In Coda")
                    for q_idx, q_match in enumerate(partite_in_coda):
                        qa, qp = q_match["teamA"]
                        qb, qpp = q_match["teamB"]
                        st.warning(f"Coda #{q_idx+1}: [⚽️ {qa['name'].upper()} & 🥅 {qp['name'].upper()}] vs [⚽️ {qb['name'].upper()} & 🥅 {qpp['name'].upper()}]")

st.markdown("---")

# --- CLASSIFICA & VITE AGGIORNATA ---
if st.session_state.players:
    col_c1, col_c2 = st.columns(2)
    
    with col_c1:
        st.markdown("""
            <div class="rank-container">
                <div class="rank-header">⚽️⚽️⚽️ VITE RIMASTE ATTACCANTI ⚽️⚽️⚽️</div>
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
                <div class="rank-header">🥅🥅🥅 VITE RIMASTE PORTIERI 🥅🥅🥅</div>
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
