import streamlit as st
import random

st.set_page_config(page_title="Torneo A Vite - Calcio Balilla", page_icon="⚽️", layout="centered")

# --- INIZIALIZZAZIONE DELLO STATO ---
if "players" not in st.session_state:
    st.session_state.players = []

if "tournament_started" not in st.session_state:
    st.session_state.tournament_started = False

if "initial_lives" not in st.session_state:
    st.session_state.initial_lives = 3

if "num_biliardini" not in st.session_state:
    st.session_state.num_biliardini = 1

if "current_round_matches" not in st.session_state:
    st.session_state.current_round_matches = []

if "round_number" not in st.session_state:
    st.session_state.round_number = 0

# --- BARRA LATERALE ADMIN ---
st.sidebar.title("🔐 Accesso")
admin_code = st.sidebar.text_input("Codice Amministratore", type="password", placeholder="Inserisci 0000")
is_admin = (admin_code == "0000")

if is_admin:
    st.sidebar.success("Modo Amministratore Attivo 🔓")
else:
    st.sidebar.info("Modalità Spettatore (Sola lettura)")

st.title("⚽️ Torneo a Vite: Attaccanti & Portieri 🥅")

# --- PANNELLO ADMIN: CONFIGURAZIONE & GIOCATORI ---
if is_admin:
    st.subheader("⚙️ Configurazione Amministratore")
    
    if not st.session_state.tournament_started:
        st.session_state.initial_lives = st.sidebar.number_input("Vite iniziali per persona", min_value=1, max_value=10, value=3)
        st.session_state.num_biliardini = st.sidebar.number_input("Quanti biliardini avete a disposizione?", min_value=1, max_value=10, value=2)
        
        with st.form("add_player_form", clear_on_submit=True):
            st.markdown("Usa **⚽️** prima del nome per gli attaccanti e **🥅** per i portieri.")
            raw_input_name = st.text_input("Giocatore (es. ⚽️ Mario o 🥅 Luigi)", placeholder="⚽️ Nome Attaccante o 🥅 Nome Portiere")
            submitted = st.form_submit_button("Aggiungi Partecipante")
            
            if submitted and raw_input_name.strip():
                text = raw_input_name.strip()
                role = None
                if text.startswith("⚽️"):
                    role = "attaccante"
                    clean_name = text.replace("⚽️", "").strip()
                elif text.startswith("🥅"):
                    role = "portiere"
                    clean_name = text.replace("🥅", "").strip()
                else:
                    st.error("Devi mettere ⚽️ davanti agli attaccanti o 🥅 davanti ai portieri!")
                    clean_name = ""
                
                if clean_name and role:
                    player_obj = {
                        "id": len(st.session_state.players) + 1,
                        "name": clean_name,
                        "role": role,
                        "lives": st.session_state.initial_lives,
                        "max_lives": st.session_state.initial_lives,
                        "eliminated": False,
                        "last_result": None
                    }
                    st.session_state.players.append(player_obj)
                    st.success(f"Aggiunto {role.capitalize()}: {clean_name}")

    attaccanti_count = len([p for p in st.session_state.players if p["role"] == "attaccante"])
    portieri_count = len([p for p in st.session_state.players if p["role"] == "portiere"])
    
    st.write(f"📊 **Attaccanti attivi:** {attaccanti_count} | **Portieri attivi:** {portieri_count} | **Biliardini:** {st.session_state.num_biliardini}")

    if len(st.session_state.players) >= 2:
        if not st.session_state.tournament_started:
            if st.button("🚀 Inizia Torneo e Genera 1° Turno", type="primary"):
                st.session_state.tournament_started = True
                st.session_state.round_number = 1
                st.session_state.current_round_matches = genera_abbinamenti()
                st.rerun()
        else:
            col_r1, col_r2 = st.columns(2)
            with col_r1:
                if st.button("🔄 Genera Turno Successivo"):
                    st.session_state.round_number += 1
                    st.session_state.current_round_matches = genera_abbinamenti()
                    st.rerun()
            with col_r2:
                if st.button("🛑 Reset / Sblocca Torneo"):
                    st.session_state.tournament_started = False
                    st.session_state.current_round_matches = []
                    st.session_state.round_number = 0
                    for p in st.session_state.players:
                        p["lives"] = st.session_state.initial_lives
                        p["eliminated"] = False
                        p["last_result"] = None
                    st.rerun()

    st.divider()

# --- FUNZIONE DI ABBINAMENTO INTELLIGENTE ---
def genera_abbinamenti():
    attivi = [p for p in st.session_state.players if not p["eliminated"]]
    attaccanti = [p for p in attivi if p["role"] == "attaccante"]
    portieri = [p for p in attivi if p["role"] == "portiere"]
    
    random.shuffle(attaccanti)
    random.shuffle(portieri)
    
    min_len = min(len(attaccanti), len(portieri))
    coppie = []
    for i in range(min_len):
        coppie.append({"att": attaccanti[i], "port": portieri[i]})
        
    avanzi_att = attaccanti[min_len:]
    avanzi_port = portieri[min_len:]
    avanzi = avanzi_att + avanzi_port
    
    if st.session_state.round_number == 1:
        random.shuffle(coppie)
    else:
        coppie.sort(key=lambda x: (x["att"]["last_result"] == 'W' or x["port"]["last_result"] == 'W'), reverse=True)
        
    partite = []
    i = 0
    while i < len(coppie) - 1:
        partite.append({
            "teamA": (coppie[i]["att"], coppie[i]["port"]),
            "teamB": (coppie[i+1]["att"], coppie[i+1]["port"]),
            "concluso": False
        })
        i += 2
        
    return {"partite": partite, "pass": avanzi}

# --- VISUALIZZAZIONE PARTITE E BILIARDINI ---
if st.session_state.tournament_started:
    st.subheader(f"⚔️ Turno N° {st.session_state.round_number} - Gestione Biliardini")
    
    data_turno = st.session_state.current_round_matches
    
    if data_turno and data_turno.get("pass"):
        for p in data_turno["pass"]:
            icona_ruolo = "⚽️" if p["role"] == "attaccante" else "🥅"
            st.info(f"💚 **{icona_ruolo} {p['name']}** riposa in questo turno e ottiene il **Pass 💚** automatico!")

    partite = data_turno.get("partite", []) if data_turno else []
    
    if not partite:
        st.success("Tutte le partite di questo turno sono state completate! Puoi generare il turno successivo.")
    else:
        num_biliardini = st.session_state.num_biliardini
        
        # Dividiamo tra partite in corso (assegnate ai biliardini) e partite in coda
        partite_in_corso = partite[:num_biliardini]
        partite_in_coda = partite[num_biliardini:]
        
        st.markdown("### 🏟️ Partite in Corso sui Biliardini")
        for idx, match in enumerate(partite_in_corso):
            biliardino_num = idx + 1
            tA_att, tA_port = match["teamA"]
            tB_att, tB_port = match["teamB"]
            
            st.markdown(f"**📍 Biliardino {biliardino_num}**")
            col_m1, col_mvs, col_m2 = st.columns([5, 1, 5])
            
            with col_m1:
                st.markdown(f"🔴 **Team A**\n* ⚽️ {tA_att['name']}\n* 🥅 {tA_port['name']}")
            with col_mvs:
                st.markdown("<h3 style='text-align: center;'>VS</h3>", unsafe_allow_html=True)
            with col_m2:
                st.markdown(f"🔵 **Team B**\n* ⚽️ {tB_att['name']}\n* 🥅 {tB_port['name']}")
                
            if is_admin:
                vincitore_scelto = st.selectbox(f"Vincitore Biliardino {biliardino_num}:", ["Seleziona...", "Team A (Rosso)", "Team B (Blu)"], key=f"match_res_{st.session_state.round_number}_{idx}")
                
                if vincitore_scelto != "Seleziona...":
                    if st.button(f"Conferma Risultato Biliardino {biliardino_num}", key=f"conf_match_{st.session_state.round_number}_{idx}"):
                        if vincitore_scelto == "Team A (Rosso)":
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
                                
                        # Rimuoviamo la partita completata in modo che scorra la coda
                        st.session_state.current_round_matches["partite"].pop(idx)
                        st.success("Risultato salvato! Le vite sono state aggiornate.")
                        st.rerun()
            st.divider()
            
        if partite_in_coda:
            st.markdown("### ⏳ Partite in Coda (In attesa che si liberi un biliardino)")
            for q_idx, q_match in enumerate(partite_in_coda):
                qtA_att, qtA_port = q_match["teamA"]
                qtB_att, qtB_port = q_match["teamB"]
                st.info(f"Coda #{q_idx+1}: [⚽️ {qtA_att['name']} & 🥅 {qtA_port['name']}] vs [⚽️ {qtB_att['name']} & 🥅 {qtB_port['name']}]")

# --- CLASSIFICA E PODIO FINALE ---
st.divider()
st.subheader("🏆 Classifica e Podio Finale")

if not st.session_state.players:
    st.info("Nessun giocatore inserito.")
else:
    # Separiamo attaccanti e portieri ordinandoli per vite rimanenti (dal punteggio più alto a zero)
    attaccanti_list = sorted([p for p in st.session_state.players if p["role"] == "attaccante"], key=lambda x: (x["lives"], not x["eliminated"]), reverse=True)
    portieri_list = sorted([p for p in st.session_state.players if p["role"] == "portiere"], key=lambda x: (x["lives"], not x["eliminated"]), reverse=True)
    
    col_pod1, col_pod2 = st.columns(2)
    
    with col_pod1:
        st.markdown("### ⚽️ Migliori Attaccanti")
        for rank, p in enumerate(attaccanti_list[:4]): # Primi 4
            cuori_vivi = "❤️ " * p["lives"]
            cuori_persi = "🖤 " * (p["max_lives"] - p["lives"])
            status = "💀 ELIMINATO" if p["eliminated"] else f"{cuori_vivi}{cuori_persi}"
            st.markdown(f"**{rank+1}°** {p['name']} — {status}")
            
    with col_pod2:
        st.markdown("### 🥅 Migliori Portieri")
        for rank, p in enumerate(portieri_list[:4]): # Primi 4
            cuori_vivi = "❤️ " * p["lives"]
            cuori_persi = "🖤 " * (p["max_lives"] - p["lives"])
            status = "💀 ELIMINATO" if p["eliminated"] else f"{cuori_vivi}{cuori_persi}"
            st.markdown(f"**{rank+1}°** {p['name']} — {status}")
