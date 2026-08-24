import streamlit as st
import random
import re
import json
import os

st.set_page_config(page_title="Torneo A Vite - Calcio Balilla", page_icon="⚽️", layout="centered")

# --- STILE GRAFICO CSS PERSONALIZZATO ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stButton>button { width: 100%; border-radius: 6px; font-weight: bold; background-color: #0284c7; color: white; border: none; padding: 8px; font-size: 0.9em; }
    .stButton>button:hover { background-color: #0369a1; color: white; }
    
    /* Contenitore match compatto */
    .match-card { background-color: #161b22; padding: 10px 14px; border-radius: 12px; margin-bottom: 15px; border: 1px solid #30363d; }
    
    /* Intestazione Biliardino Giallo/Dorato Marcato */
    .biliardino-box { background: linear-gradient(135deg, #f59e0b, #d97706); color: #111827; text-align: center; font-size: 1.15em; font-weight: 900; padding: 6px; border-radius: 8px; margin-bottom: 10px; text-transform: uppercase; letter-spacing: 1px; box-shadow: 0 2px 4px rgba(0,0,0,0.2); }
    
    /* Box Coppia Verde Scuro Marcato */
    .team-box { background-color: #064e3b; padding: 10px; border-radius: 8px; border: 1px solid #047857; text-align: center; color: #f3f4f6; }
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

st.title("⚽️ Torneo a Vite: Attaccanti & Portieri 🥅")

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
            st.markdown("### 📝 Incolla la lista dei giocatori")
            lista_input_testo = st.text_area("Incolla partecipanti (es: 1 ⚽️ Nome, 2 🥅 Nome):", height=120)
            
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
                    if st.button("🚀 Avvia Torneo e 1° Turno", type="primary"):
                        st.session_state.tournament_started = True
                        st.session_state.round_number = 1
                        st.session_state.show_podium = False
                        st.session_state.current_round_matches = genera_abbinamenti()
                        salva_stato()
                        st.rerun()
                else:
                    if st.button("🔄 Genera Turno Successivo"):
                        st.session_state.round_number += 1
                        st.session_state.current_round_matches = genera_abbinamenti()
                        salva_stato()
                        st.rerun()
            with col_act2:
                if st.button("🛑 Ricomincia da Zero (Reset)"):
                    st.session_state.tournament_started = False
                    st.session_state.current_round_matches = []
                    st.session_state.round_number = 0
                    st.session_state.show_podium = False
                    st.session_state.players = []
                    if os.path.exists(STATE_FILE):
                        os.remove(STATE_FILE)
                    st.rerun()

st.divider()

# --- VISUALIZZAZIONE PARTITE ---
if st.session_state.tournament_started:
    st.subheader(f"⚔️ Turno N° {st.session_state.round_number}")
    
    data_turno = st.session_state.current_round_matches
    if data_turno and data_turno.get("pass"):
        for p in data_turno["pass"]:
            icona = "⚽️" if p["role"] == "attaccante" else "🥅"
            st.info(f"💚 **{icona} {p['name']}** riposa in questo turno (Pass automatico 💚)")

    partite = data_turno.get("partite", []) if data_turno else []
    
    if not partite:
        st.success("🎉 Turno completato! Clicca su 'Genera Turno Successivo' nel pannello admin.")
        if is_admin and not st.session_state.show_podium:
            if st.button("🏆 Mostra Podio Finale"):
                st.session_state.show_podium = True
                salva_stato()
                st.rerun()
    else:
        num_biliardini = st.session_state.num_biliardini
        partite_in_corso = partite[:num_biliardini]
        partite_in_coda = partite[num_biliardini:]
        
        st.markdown("### 🏟️ Partite nei Biliardini")
        for idx, match in enumerate(partite_in_corso):
            biliardino_num = idx + 1
            tA_att, tA_port = match["teamA"]
            tB_att, tB_port = match["teamB"]
            
            # Card singola di ogni partita
            st.markdown(f"""
                <div class="match-card">
                    <div class="biliardino-box">BILIARDINO {biliardino_num}</div>
            """, unsafe_allow_html=True)
            
            col_m1, col_mvs, col_m2 = st.columns([5, 1, 5])
            
            with col_m1:
                st.markdown(f"""
                    <div class="team-box">
                        <div style="font-size: 0.95em; margin-bottom: 4px;">⚽️ <b>{tA_att['name']}</b></div>
                        <div style="font-size: 0.95em;">🥅 <b>{tA_port['name']}</b></div>
                    </div>
                """, unsafe_allow_html=True)
                if is_admin:
                    if st.button("🏆 Segna Vittoria", key=f"win_A_{st.session_state.round_number}_{idx}"):
                        for v in [tA_att, tA_port]: v["last_result"] = 'W'
                        for per in [tB_att, tB_port]:
                            per["last_result"] = 'L'
                            per["lives"] = max(0, per["lives"] - 1)
                            if per["lives"] == 0: per["eliminated"] = True
                        st.session_state.current_round_matches["partite"].pop(idx)
                        salva_stato()
                        st.rerun()

            with col_mvs:
                st.markdown("<h4 style='text-align: center; color: #f59e0b; margin-top: 18px;'>VS</h4>", unsafe_allow_html=True)
                
            with col_m2:
                st.markdown(f"""
                    <div class="team-box">
                        <div style="font-size: 0.95em; margin-bottom: 4px;">⚽️ <b>{tB_att['name']}</b></div>
                        <div style="font-size: 0.95em;">🥅 <b>{tB_port['name']}</b></div>
                    </div>
                """, unsafe_allow_html=True)
                if is_admin:
                    if st.button("🏆 Segna Vittoria", key=f"win_B_{st.session_state.round_number}_{idx}"):
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
            st.markdown("### ⏳ In Coda")
            for q_idx, q_match in enumerate(partite_in_coda):
                qa, qp = q_match["teamA"]
                qb, qpp = q_match["teamB"]
                st.warning(f"Coda #{q_idx+1}: [⚽️ {qa['name']} & 🥅 {qp['name']}] vs [⚽️ {qb['name']} & 🥅 {qpp['name']}]")

# --- CLASSIFICA ---
st.subheader("📋 Classifica Generale e Vite")
if st.session_state.players:
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        st.markdown("### ⚽️ Attaccanti")
        for p in [x for x in st.session_state.players if x["role"] == "attaccante"]:
            cuori = "❤️ " * p["lives"] + "🖤 " * (p["max_lives"] - p["lives"])
            stato = "💀 ELIMINATO" if p["eliminated"] else cuori
            st.markdown(f"**{p['name']}** — {stato}")
    with col_c2:
        st.markdown("### 🥅 Portieri")
        for p in [x for x in st.session_state.players if x["role"] == "portiere"]:
            cuori = "❤️ " * p["lives"] + "🖤 " * (p["max_lives"] - p["lives"])
            stato = "💀 ELIMINATO" if p["eliminated"] else cuori
            st.markdown(f"**{p['name']}** — {stato}")

# --- PODIO FINALE ---
if st.session_state.show_podium:
    st.divider()
    st.subheader("🏆 Podio Ufficiale Finale")
    atts_sorted = sorted([p for p in st.session_state.players if p["role"] == "attaccante"], key=lambda x: (x["lives"], not x["eliminated"]), reverse=True)
    ports_sorted = sorted([p for p in st.session_state.players if p["role"] == "portiere"], key=lambda x: (x["lives"], not x["eliminated"]), reverse=True)
    
    col_pod1, col_pod2 = st.columns(2)
    with col_pod1:
        st.markdown("### ⚽️ Top 4 Attaccanti")
        for rank, p in enumerate(atts_sorted[:4]):
            st.markdown(f"**{rank+1}°** {p['name']} — {'❤️ ' * p['lives']}")
    with col_pod2:
        st.markdown("### 🥅 Top 4 Portieri")
        for rank, p in enumerate(ports_sorted[:4]):
            st.markdown(f"**{rank+1}°** {p['name']} — {'❤️ ' * p['lives']}")
