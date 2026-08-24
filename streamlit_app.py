import streamlit as st
import random
import re

st.set_page_config(page_title="Torneo A Vite - Calcio Balilla", page_icon="⚽️", layout="centered")

# --- STILE GRAFICO ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# --- INIZIALIZZAZIONE STATO ---
if "players" not in st.session_state:
    st.session_state.players = []
if "tournament_started" not in st.session_state:
    st.session_state.tournament_started = False
if "initial_lives" not in st.session_state:
    st.session_state.initial_lives = 5
if "num_biliardini" not in st.session_state:
    st.session_state.num_biliardini = 4
if "current_round_matches" not in st.session_state:
    st.session_state.current_round_matches = []
if "round_number" not in st.session_state:
    st.session_state.round_number = 0
if "show_podium" not in st.session_state:
    st.session_state.show_podium = False

# --- FUNZIONE DI ABBINAMENTO (Vincitore + Perdente) ---
def genera_abbinamenti():
    attivi = [p for p in st.session_state.players if not p["eliminated"]]
    
    # Al primo turno facciamo tutto puramente casuale
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
        # Turni successivi: Dividiamo per ruolo e per esito precedente (W vs L)
        atts_w = [p for p in attivi if p["role"] == "attaccante" and p.get("last_result") == 'W']
        atts_l = [p for p in attivi if p["role"] == "attaccante" and p.get("last_result") != 'W']
        
        ports_w = [p for p in attivi if p["role"] == "portiere" and p.get("last_result") == 'W']
        ports_l = [p for p in attivi if p["role"] == "portiere" and p.get("last_result") != 'W']
        
        random.shuffle(atts_w)
        random.shuffle(atts_l)
        random.shuffle(ports_w)
        random.shuffle(ports_l)
        
        coppie = []
        # Creiamo coppie unendo un attaccante vincente con un portiere perdente (o viceversa)
        # per formare squadre miste equilibrate W + L
        
        # Coppia tipo 1: Attaccante Vincitore + Portiere Perdente
        while atts_w and ports_l:
            coppie.append({"att": atts_w.pop(0), "port": ports_l.pop(0)})
            
        # Coppia tipo 2: Attaccante Perdente + Portiere Vincitore
        while atts_l and ports_w:
            coppie.append({"att": atts_l.pop(0), "port": ports_w.pop(0)})
            
        # Se avanzano altri giocatori dello stesso esito, li accoppiamo tra loro per esaurire la lista
        while atts_w and ports_w:
            coppie.append({"att": atts_w.pop(0), "port": ports_w.pop(0)})
        while atts_l and ports_l:
            coppie.append({"att": atts_l.pop(0), "port": ports_l.pop(0)})
            
        avanzi = atts_w + atts_l + ports_w + ports_l
        random.shuffle(coppie)

    # Formiamo le partite accoppiando le squadre
    partite = []
    i = 0
    while i < len(coppie) - 1:
        partite.append({
            "teamA": (coppie[i]["att"], coppie[i]["port"]),
            "teamB": (coppie[i+1]["att"], coppie[i+1]["port"])
        })
        i += 2
        
    return {"partite": partite, "pass": avanzi}

# --- BARRA LATERALE ADMIN ---
st.sidebar.title("🔐 Accesso Admin")
admin_code = st.sidebar.text_input("Codice Amministratore", type="password", placeholder="Inserisci 0000")
is_admin = (admin_code == "0000")

if is_admin:
    st.sidebar.success("Modo Amministratore Attivo 🔓")
else:
    st.sidebar.info("Modalità Spettatore (Sola lettura)")

st.title("⚽️ Torneo a Vite: Attaccanti & Portieri 🥅")

# --- PANNELLO CONFIGURAZIONE E LISTA MASSIVA ---
if is_admin:
    with st.expander("⚙️ Pannello Configurazione & Inserimento Giocatori", expanded=not st.session_state.tournament_started):
        
        if not st.session_state.tournament_started:
            col_conf1, col_conf2 = st.columns(2)
            with col_conf1:
                st.session_state.initial_lives = st.number_input("Vite iniziali", min_value=1, max_value=10, value=5)
            with col_conf2:
                st.session_state.num_biliardini = st.number_input("Numero Biliardini", min_value=1, max_value=10, value=4)
            
            st.markdown("---")
            st.markdown("### 📝 Incolla la lista dei giocatori")
            st.markdown("Incolla qui sotto la tua lista completa. Il sistema riconoscerà in automatico **🥅** per i portieri e **⚽️** per gli attaccanti, ignorando i numeri.")
            
            lista_input_testo = st.text_area("Incolla la lista completa dei partecipanti:", height=150, placeholder="1 🥅 Davide\n2 🥅 Francesco\n...\n1 ⚽ Luigi I.")
            
            if st.button("📥 Importa e Registra Giocatori", type="primary"):
                righe = lista_input_testo.split("\n")
                count_aggiunti = 0
                
                for riga in righe:
                    riga_pulita = riga.strip()
                    if not riga_pulita:
                        continue
                    
                    role = None
                    if "🥅" in riga_pulita:
                        role = "portiere"
                    elif "⚽️" in riga_pulita or "⚽" in riga_pulita:
                        role = "attaccante"
                        
                    if role:
                        nome = riga_pulita.replace("🥅", "").replace("⚽️", "").replace("⚽", "")
                        nome = re.sub(r'^\d+[\.\-\s]*', '', nome).strip()
                        
                        if nome:
                            if not any(p["name"].lower() == nome.lower() and p["role"] == role for p in st.session_state.players):
                                player_obj = {
                                    "id": len(st.session_state.players) + 1,
                                    "name": nome,
                                    "role": role,
                                    "lives": st.session_state.initial_lives,
                                    "max_lives": st.session_state.initial_lives,
                                    "eliminated": False,
                                    "last_result": None
                                }
                                st.session_state.players.append(player_obj)
                                count_aggiunti += 1
                                
                st.success(f"Importati con successo {count_aggiunti} giocatori!")
                st.rerun()

    attaccanti = [p for p in st.session_state.players if p["role"] == "attaccante"]
    portieri = [p for p in st.session_state.players if p["role"] == "portiere"]
    
    st.info(f"📊 **Stato Iscrizioni:** ⚽️ Attaccanti: **{len(attaccanti)}** | 🥅 Portieri: **{len(portieri)}** | 🏟️ Biliardini: **{st.session_state.num_biliardini}** | ❤️ Vite: **{st.session_state.initial_lives}**")

    if len(st.session_state.players) >= 2:
        col_start1, col_start2 = st.columns(2)
        with col_start1:
            if not st.session_state.tournament_started:
                if st.button("🚀 Avvia Torneo e Genera 1° Turno", type="primary"):
                    st.session_state.tournament_started = True
                    st.session_state.round_number = 1
                    st.session_state.show_podium = False
                    st.session_state.current_round_matches = genera_abbinamenti()
                    st.rerun()
            else:
                if st.button("🔄 Genera Turno Successivo"):
                    st.session_state.round_number += 1
                    st.session_state.current_round_matches = genera_abbinamenti()
                    st.rerun()
        with col_start2:
            if st.button("🛑 Reset Totale Torneo"):
                st.session_state.tournament_started = False
                st.session_state.current_round_matches = []
                st.session_state.round_number = 0
                st.session_state.show_podium = False
                for p in st.session_state.players:
                    p["lives"] = st.session_state.initial_lives
                    p["eliminated"] = False
                    p["last_result"] = None
                st.rerun()

st.divider()

# --- VISUALIZZAZIONE PARTITE E BILIARDINI ---
if st.session_state.tournament_started:
    st.subheader(f"⚔️ Turno N° {st.session_state.round_number} - Gestione Biliardini")
    
    data_turno = st.session_state.current_round_matches
    
    if data_turno and data_turno.get("pass"):
        for p in data_turno["pass"]:
            icona = "⚽️" if p["role"] == "attaccante" else "🥅"
            st.info(f"💚 **{icona} {p['name']}** riposa in questo turno e ottiene il **Pass 💚** automatico!")

    partite = data_turno.get("partite", []) if data_turno else []
    
    if not partite:
        st.success("🎉 Tutte le partite di questo turno sono state completate! Clicca su 'Genera Turno Successivo' dal pannello admin.")
        if is_admin and not st.session_state.show_podium:
            if st.button("🏆 Mostra Podio Finale"):
                st.session_state.show_podium = True
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
            
            with st.container():
                st.markdown(f"**📍 Biliardino {biliardino_num}**")
                col_m1, col_mvs, col_m2 = st.columns([5, 1, 5])
                with col_m1:
                    st.markdown(f"🔴 **Team Rosso**\n* ⚽️ {tA_att['name']}\n* 🥅 {tA_port['name']}")
                with col_mvs:
                    st.markdown("<h3 style='text-align: center; color: #f59e0b;'>VS</h3>", unsafe_allow_html=True)
                with col_m2:
                    st.markdown(f"🔵 **Team Blu**\n* ⚽️ {tB_att['name']}\n* 🥅 {tB_port['name']}")
                
                if is_admin:
                    vincitore_scelto = st.selectbox(f"Seleziona chi ha vinto sul Biliardino {biliardino_num}:", ["Seleziona vincitore...", "Team Rosso (Vince)", "Team Blu (Vince)"], key=f"match_res_{st.session_state.round_number}_{idx}")
                    
                    if vincitore_scelto != "Seleziona vincitore...":
                        if st.button(f"Conferma Risultato Biliardino {biliardino_num}", key=f"conf_match_{st.session_state.round_number}_{idx}"):
                            if vincitore_scelto == "Team Rosso (Vince)":
                                vincenti = [tA_att, tA_port]
                                perdenti = [tB_att, tB_port]
                            else:
                                vincenti = [tB_att, tB_port]
                                perdenti = [tA_att, tA_port]
                                
                            for v in vincenti:
                                v["last_result"] = 'W'
                            for per in perdenti:
                                per["last_result"] = 'L'
                                per["lives"] -= 1
                                if per["lives"] <= 0:
                                    per["lives"] = 0
                                    per["eliminated"] = True
                                    
                            st.session_state.current_round_matches["partite"].pop(idx)
                            st.success("Risultato registrato! I perdenti perdono 1 vita 🖤.")
                            st.rerun()
                st.markdown("---")
            
        if partite_in_coda:
            st.markdown("### ⏳ Partite in Coda (In attesa che si liberi un biliardino)")
            for q_idx, q_match in enumerate(partite_in_coda):
                qtA_att, qtA_port = q_match["teamA"]
                qtB_att, qtB_port = q_match["teamB"]
                st.warning(f"In coda #{q_idx+1} ➔ [⚽️ {qtA_att['name']} & 🥅 {qtA_port['name']}] vs [⚽️ {qtB_att['name']} & 🥅 {qtB_port['name']}]")

# --- CLASSIFICA GENERALE DI TUTTI I GIOCATORI ---
st.subheader("📋 Classifica Generale e Vite")

if not st.session_state.players:
    st.info("Nessun giocatore registrato.")
else:
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

# --- PODIO FINALE (Visibile solo a fine torneo o quando richiesto) ---
if st.session_state.show_podium:
    st.divider()
    st.subheader("🏆 Podio Ufficiale Finale")
    
    atts_sorted = sorted([p for p in st.session_state.players if p["role"] == "attaccante"], key=lambda x: (x["lives"], not x["eliminated"]), reverse=True)
    ports_sorted = sorted([p for p in st.session_state.players if p["role"] == "portiere"], key=lambda x: (x["lives"], not x["eliminated"]), reverse=True)
    
    col_pod1, col_pod2 = st.columns(2)
    with col_pod1:
        st.markdown("### ⚽️ Top 4 Attaccanti")
        for rank, p in enumerate(atts_sorted[:4]):
            cuori = "❤️ " * p["lives"]
            st.markdown(f"**{rank+1}°** {p['name']} — {cuori}")
            
    with col_pod2:
        st.markdown("### 🥅 Top 4 Portieri")
        for rank, p in enumerate(ports_sorted[:4]):
            cuori = "❤️ " * p["lives"]
            st.markdown(f"**{rank+1}°** {p['name']} — {cuori}")
