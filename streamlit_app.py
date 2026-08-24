import streamlit as st
import random
import re
import json
import os

st.set_page_config(page_title="Torneo A Vite - Calcio Balilla", page_icon="⚽️", layout="centered")

# --- STILE GRAFICO CSS ULTRASCOMPATTO ---
st.markdown("""
    <style>
    .main { background-color: #0b0f19; }
    
    /* Contenitore match ridotto al minimo */
    .match-card { 
        background: linear-gradient(145deg, #131b2e, #0d1322); 
        padding: 8px 10px; 
        border-radius: 10px; 
        margin-bottom: 8px; 
        border: 1px solid #1e293b;
    }
    
    /* Header Biliardino Sottile */
    .biliardino-box { 
        background: linear-gradient(90deg, #f59e0b, #d97706); 
        color: #0f172a; 
        text-align: center; 
        font-size: 0.78em; 
        font-weight: 800; 
        padding: 2px; 
        border-radius: 4px; 
        margin-bottom: 6px; 
        text-transform: uppercase; 
        letter-spacing: 1px; 
    }

    /* Box Squadra Compatto */
    .team-box { 
        background-color: #064e3b; 
        padding: 6px 4px; 
        border-radius: 6px; 
        border: 1px solid #059669; 
        color: #ecfdf5; 
        font-size: 0.8em; 
        text-align: center; 
        margin-bottom: 4px; 
    }
    
    .player-name {
        font-weight: 600;
        line-height: 1.2;
    }

    /* Pulsante Vittoria Centrato e Ottimizzato */
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #0284c7, #0369a1) !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        border: 1px solid #38bdf8 !important;
        border-radius: 5px !important;
        padding: 2px 0px !important;
        font-size: 0.75em !important;
        margin-top: 0px !important;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #0369a1, #075985) !important;
        border-color: #7dd3fc !important;
    }
    
    /* Riduzione generale spaziatura Streamlit */
    div.block-container {
        padding-top: 1rem;
        padding-bottom: 1.5rem;
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
                st.session_state.tournament_started = data.get("tournament_started", False)
                st.session_state.initial_lives = data.get("initial_lives", 5)
                st.session_state.num_biliardini = data.get("num_biliardini", 4)
                st.session_state.current_round_matches = data.get("current_round_matches", [])
                st.session_state.round_number = data.get("round_number", 0)
                st.session_state.show_podium = data.get("show_podium", False)
                return True
        except:
            return False
    return False

# --- INIZIALIZZAZIONE STATO PERSISTENTE ---
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

# --- FUNZIONE ABBINAMENTI ---
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

# --- BARRA LATERALE ADMIN ---
st.sidebar.title("🔐 Accesso Admin")
admin_code = st.sidebar.text_input("Codice Amministratore", type="password", placeholder="Inserisci 0000")
is_admin = (admin_code == "0000")

if is_admin:
    st.sidebar.success("Modo Amministratore Attivo 🔓")
else:
    st.sidebar.info("Modalità Spettatore (Sola lettura)")

st.title("⚽️ Torneo a Vite")

# --- PANNELLO CONFIGURAZIONE ---
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
                        st.session_state.show_podium = False
                        st.session_state.current_round_matches = genera_abbinamenti()
                        salva_stato()
                        st.rerun()
                else:
                    if st.button("🔄 Turno Successivo"):
                        st.session_state.round_number += 1
                        st.session_state.current_round_matches = genera_abbinamenti()
                        salva_stato()
                        st.rerun()
            with col_act2:
                if st.button("🛑 Reset Totale"):
                    st.session_state.tournament_started = False
                    st.session_state.current_round_matches = []
                    st.session_state.round_number = 0
                    st.session_state.show_podium = False
                    st.session_state.players = []
                    if os.path.exists(STATE_FILE):
                        os.remove(STATE_FILE)
                    st.rerun()

st.markdown("---")

# --- VISUALIZZAZIONE PARTITE ---
if st.session_state.tournament_started:
    st.markdown(f"### ⚔️ Turno N° {st.session_state.round_number}")
    
    data_turno = st.session_state.current_round_matches
    if data_turno and data_turno.get("pass"):
        pass_text = ", ".join([f"{'⚽️' if p['role']=='attaccante' else '🥅'} {p['name']}" for p in data_turno["pass"]])
        st.info(f"💚 **Riposano (Pass):** {pass_text}")

    partite = data_turno.get("partite", []) if data_turno else []
    
    if not partite:
        st.success("🎉 Turno completato!")
        if is_admin and not st.session_state.show_podium:
            if st.button("🏆 Mostra Podio Finale"):
                st.session_state.show_podium = True
                salva_stato()
                st.rerun()
    else:
        num_biliardini = st.session_state.num_biliardini
        partite_in_corso = partite[:num_biliardini]
        partite_in_coda = partite[num_biliardini:]
        
        st.markdown("#### 🏟️ Partite in Corso")
        for idx, match in enumerate(partite_in_corso):
            biliardino_num = idx + 1
            tA_att, tA_port = match["teamA"]
            tB_att, tB_port = match["teamB"]
            
            # Card contenitore match ridotta
            st.markdown(f"""
                <div class="match-card">
                    <div class="biliardino-box">BILIARDINO {biliardino_num}</div>
            """, unsafe_allow_html=True)
            
            col_teamA, col_vs, col_teamB = st.columns([5, 1, 5])
            
            with col_teamA:
                st.markdown(f"""
                    <div class="team-box">
                        <div class="player-name">⚽️ {tA_att['name']}</div>
                        <div class="player-name">🥅 {tA_port['name']}</div>
                    </div>
                """, unsafe_allow_html=True)
                
                if is_admin:
                    if st.button("🏆 Vinta A", key=f"win_A_{st.session_state.round_number}_{idx}"):
                        for v in [tA_att, tA_port]: v["last_result"] = 'W'
                        for per in [tB_att, tB_port]:
                            per["last_result"] = 'L'
                            per["lives"] = max(0, per["lives"] - 1)
                            if per["lives"] == 0: per["eliminated"] = True
                        st.session_state.current_round_matches["partite"].pop(idx)
                        salva_stato()
                        st.rerun()
                        
            with col_vs:
                st.markdown("<div style='text-align: center; font-weight: 800; color: #f59e0b; padding-top: 15px; font-size: 0.85em;'>VS</div>", unsafe_allow_html=True)
                
            with col_teamB:
                st.markdown(f"""
                    <div class="team-box">
                        <div class="player-name">⚽️ {tB_att['name']}</div>
                        <div class="player-name">🥅 {tB_port['name']}</div>
                    </div>
                """, unsafe_allow_html=True)
                
                if is_admin:
                    if st.button("🏆 Vinta B", key=f"win_B_{st.session_state.round_number}_{idx}"):
                        for v in [tB_att, tB_port]: v["last_result"] = 'W'
                        for per in [tA_att, tA_port]:
                            per["last_result"] = 'L'
                            per["lives"] = max(0, per["lives"] - 1)
                            if per["lives"] == 0: per["eliminated"] = True
                        st.session_state.current_round_matches["partite"].pop(idx)
                        salva_stato()
                        st.rerun()
                        
            st.markdown("</div>", unsafe_allow_html=True)
            
        if partite_in_coda:
            st.markdown("#### ⏳ In Coda")
            for q_idx, q_match in enumerate(partite_in_coda):
                qa, qp = q_match["teamA"]
                qb, qpp = q_match["teamB"]
                st.warning(f"Coda #{q_idx+1}: [⚽️ {qa['name']} & 🥅 {qp['name']}] vs [⚽️ {qb['name']} & 🥅 {qpp['name']}]")

st.markdown("---")

# --- CLASSIFICA ---
st.markdown("### 📋 Classifica & Vite")
if st.session_state.players:
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        st.markdown("#### ⚽️ Attaccanti")
        for p in [x for x in st.session_state.players if x["role"] == "attaccante"]:
            cuori = "❤️ " * p["lives"] + "🖤 " * (p["max_lives"] - p["lives"])
            stato = "💀 ELIMINATO" if p["eliminated"] else cuori
            st.markdown(f"**{p['name']}** — {stato}")
    with col_c2:
        st.markdown("#### 🥅 Portieri")
        for p in [x for x in st.session_state.players if x["role"] == "portiere"]:
            cuori = "❤️ " * p["lives"] + "🖤 " * (p["max_lives"] - p["lives"])
            stato = "💀 ELIMINATO" if p["eliminated"] else cuori
            st.markdown(f"**{p['name']}** — {stato}")

# --- PODIO FINALE ---
if st.session_state.show_podium:
    st.markdown("---")
    st.markdown("### 🏆 Podio Ufficiale Finale")
    atts_sorted = sorted([p for p in st.session_state.players if p["role"] == "attaccante"], key=lambda x: (x["lives"], not x["eliminated"]), reverse=True)
    ports_sorted = sorted([p for p in st.session_state.players if p["role"] == "portiere"], key=lambda x: (x["lives"], not x["eliminated"]), reverse=True)
    
    col_pod1, col_pod2 = st.columns(2)
    with col_pod1:
        st.markdown("#### ⚽️ Top 4 Attaccanti")
        for rank, p in enumerate(atts_sorted[:4]):
            st.markdown(f"**{rank+1}°** {p['name']} — {'❤️ ' * p['lives']}")
    with col_pod2:
        st.markdown("#### 🥅 Top 4 Portieri")
        for rank, p in enumerate(ports_sorted[:4]):
            st.markdown(f"**{rank+1}°** {p['name']} — {'❤️ ' * p['lives']}")
