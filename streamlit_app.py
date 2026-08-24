import streamlit as st

st.set_page_config(page_title="Torneo A Vite", page_icon="🏆", layout="centered")

# --- INIZIALIZZAZIONE DELLO STATO ---
if "players" not in st.session_state:
    st.session_state.players = []

if "tournament_started" not in st.session_state:
    st.session_state.tournament_started = False

# --- BARRA LATERALE PER IL LOGIN AMMINISTRATORE ---
st.sidebar.title("🔐 Accesso")
admin_code = st.sidebar.text_input("Codice Amministratore", type="password", placeholder="Inserisci 0000")

is_admin = (admin_code == "0000")

if is_admin:
    st.sidebar.success("Modo Amministratore Attivo 🔓")
else:
    st.sidebar.info("Modalità Spettatore (Sola lettura)")

# --- INTERFACCIA PRINCIPALE ---
st.title("🏆 Torneo A Vite")

# Sezione Amministratore: Gestione e aggiunta giocatori
if is_admin:
    st.subheader("⚙️ Pannello Amministratore")
    
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

    # Pulsanti di controllo del torneo
    if len(st.session_state.players) >= 2:
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if not st.session_state.tournament_started:
                if st.button("🚀 Inizia Torneo", type="primary"):
                    st.session_state.tournament_started = True
                    st.rerun()
            else:
                if st.button("🛑 Termina/Sblocca Torneo", type="secondary"):
                    st.session_state.tournament_started = False
                    st.rerun()

    st.divider()

# --- VISUALIZZAZIONE GARA (Per tutti: Admin e Ospiti) ---
st.subheader("📊 Stato della Gara e Partecipanti")
st.write(f"**Partecipanti totali:** {len(st.session_state.players)}")

if not st.session_state.players:
    st.info("Nessun giocatore iscritto al torneo.")
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
            # Solo l'admin può modificare le vite o rimuovere i giocatori
            if is_admin:
                # Pulsante di rimozione (solo se il torneo non è iniziato)
                if not st.session_state.tournament_started:
                    if st.button("✖", key=f"remove_{p['id']}"):
                        st.session_state.players = [pl for pl in st.session_state.players if pl["id"] != p["id"]]
                        st.rerun()
                else:
                    # A torneo iniziato, l'admin può gestire i punti/vite in modo rapido
                    if not p["eliminated"]:
                        if st.button("➖ Vita", key=f"minus_{p['id']}"):
                            p["lives"] -= 1
                            if p["lives"] <= 0:
                                p["lives"] = 0
                                p["eliminated"] = True
                            st.rerun()
