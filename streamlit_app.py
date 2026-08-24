import streamlit as st

st.set_page_config(page_title="Torneo A Vite", page_icon="🏆", layout="centered")

st.title("🏆 Torneo A Vite")

# Inizializzazione dello stato della sessione in Streamlit
if "players" not in st.session_state:
    st.session_state.players = []

if "tournament_started" not in st.session_state:
    st.session_state.tournament_started = False

# Sezione per aggiungere giocatori (disabilitata se il torneo è iniziato)
st.subheader("Gestione Partecipanti")

with st.form("add_player_form", clear_on_submit=True):
    new_player_name = st.text_input("Nome del giocatore", placeholder="Inserisci il nome...")
    submitted = st.form_submit_button("Aggiungi Giocatore")
    
    if submitted and new_player_name.strip():
        if st.session_state.tournament_started:
            st.error("Non puoi aggiungere giocatori a torneo iniziato!")
        else:
            player_obj = {
                "id": len(st.session_state.players) + 1,
                "name": new_player_name.strip(),
                "lives": 3,
                "eliminated": False,
                "lastResult": None
            }
            st.session_state.players.append(player_obj)
            st.success(f"Giocatore '{new_player_name.strip()}' aggiunto!")

st.write(f"**Partecipanti totali:** {len(st.session_state.players)}")

# Pulsante per avviare o bloccare il torneo
if len(st.session_state.players) >= 2:
    if not st.session_state.tournament_started:
        if st.button("🚀 Inizia Torneo", type="primary"):
            st.session_state.tournament_started = True
            st.rerun()
    else:
        if st.button("🛑 Sblocca / Modifica Torneo", type="secondary"):
            st.session_state.tournament_started = False
            st.rerun()

st.divider()

# Visualizzazione della lista dei giocatori
st.subheader("Lista Giocatori")

if not st.session_state.players:
    st.info("Nessun giocatore inserito. Aggiungi qualcuno per iniziare.")
else:
    for p in st.session_state.players:
        col1, col2, col3 = st.columns([3, 2, 1])
        
        with col1:
            if p["eliminated"]:
                st.markdown(f"~~**{p['name']}**~~ 💀 *ELIMINATO*")
            else:
                st.markdown(f"**{p['name']}**")
                
        with col2:
            if not p["eliminated"]:
                lives_display = "❌ " * p["lives"]
                st.write(lives_display.strip())
            else:
                st.write("-")
                
        with col3:
            # Pulsante rimuovi visibile solo se il torneo NON è iniziato
            if not st.session_state.tournament_started:
                if st.button("✖", key=f"remove_{p['id']}"):
                    st.session_state.players = [pl for pl in st.session_state.players if pl["id"] != p["id"]]
                    st.rerun()
