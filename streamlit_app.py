
import streamlit as st
import random
import re
import json
import os

st.set_page_config(page_title="CHAMPIONS BILIARDINO // BY BATTANI", page_icon="🏆", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@600;800;900&family=Orbitron:wght@700;900&display=swap');
.stApp { background-color: #020a1a; background-image: radial-gradient(ellipse at top, rgba(0,82,180,0.4) 0%, transparent 60%), radial-gradient(ellipse at bottom, rgba(255,215,0,0.08) 0%, transparent 60%); }
.hero-champions { text-align: center; padding: 25px 10px 15px 10px; background: linear-gradient(180deg, #0a1931 0%, #020a1a 100%); border: 2px solid #c9a86a; border-radius: 18px; margin-bottom: 20px; box-shadow: 0 0 40px rgba(201,168,106,0.25); }
.hero-title { font-family: 'Orbitron'; font-size: 2.1em; font-weight: 900; background: linear-gradient(135deg, #ffffff 20%, #c9a86a 80%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; letter-spacing: 3px; text-transform: uppercase; }
.hero-sub { color: #6ea8ff; font-family: 'Montserrat'; letter-spacing: 5px; font-size: 0.9em; font-weight: 600; }
.omini-row { font-size: 28px; letter-spacing: 12px; margin: 8px 0; }
.champions-card { background: linear-gradient(160deg, #0a1931 0%, #061024 100%); border: 1px solid rgba(201,168,106,0.4); border-left: 4px solid #0052b4; border-radius: 12px; padding: 16px; margin-bottom: 14px; }
.champions-card-live { border: 2px solid #c9a86a; box-shadow: 0 0 25px rgba(201,168,106,0.3); }
.biliardino-badge { background: #020a1a; border: 1px solid #c9a86a; color: #c9a86a; padding: 3px 10px; border-radius: 20px; font-family: 'Orbitron'; font-size: 0.7em; font-weight: 800; }
.vs-badge { color: #ffffff; font-weight: 900; font-family: 'Orbitron'; background: #0052b4; width: 34px; height: 34px; border-radius: 50%; display: flex; align-items: center; justify-content: center; }
.team-name { font-family: 'Montserrat'; font-weight: 800; text-transform: uppercase; color: #eaf2ff; font-size: 0.95em; }
.classifica-container { background: rgba(10,25,49,0.8); border: 1px solid rgba(201,168,106,0.3); border-top: 3px solid #c9a86a; border-radius: 10px; padding: 14px; }
.classifica-row { display: flex; justify-content: space-between; align-items: center; background: rgba(2,10,26,0.9); padding: 8px 12px; border-radius: 6px; margin-bottom: 5px; border-left: 3px solid transparent; }
.classifica-row.top8 { border-left-color: #00d1ff; background: rgba(0,82,180,0.25); }
.classifica-row.playoff { border-left-color: #c9a86a; }
.classifica-row.europa { border-left-color: #ff6b35; opacity: 0.8; }
.knockout-box { background: linear-gradient(135deg, #0a1931, #020a1a); border: 2px solid #0052b4; border-radius: 12px; padding: 12px; text-align: center; min-height: 80px; display: flex; flex-direction: column; justify-content: center; }
</style>
""", unsafe_allow_html=True)

STATE_FILE = "torneo_champions_state.json"

def salva():
    data = {k: st.session_state[k] for k in ["teams","config","league_matches","knockout_champions","knockout_europa","phase","round_number"]}
    with open(STATE_FILE, "w") as f:
        json.dump(data, f, indent=2)

def carica():
    if not os.path.exists(STATE_FILE):
        return False
    try:
        with open(STATE_FILE, "r") as f:
            d = json.load(f)
        for k in d:
            st.session_state[k] = d[k]
        return True
    except:
        return False

def calcola_punti(gf, gs):
    diff = gf - gs
    if diff >= 2: return 3, 0
    elif diff == 1: return 2, 1
    elif diff == -1: return 1, 2
    else: return 0, 3

def genera_calendario(teams, partite_per_coppia):
    n = len(teams)
    possibili = []
    for i in range(n):
        for j in range(i+1, n):
            possibili.append((teams[i]["id"], teams[j]["id"]))
    random.shuffle(possibili)
    conteggio = {t["id"]:0 for t in teams}
    calendario = []
    for idA, idB in possibili:
        if conteggio[idA] < partite_per_coppia and conteggio[idB] < partite_per_coppia:
            calendario.append({"id": len(calendario)+1, "teamA_id": idA, "teamB_id": idB, "golA": None, "golB": None, "giocata": False, "biliardino": None})
            conteggio[idA]+=1; conteggio[idB]+=1
    # ripeti se mancano partite
    for tid in list(conteggio.keys()):
        while conteggio[tid] < partite_per_coppia:
            candidati = [t for t in teams if t["id"] != tid]
            avv = random.choice(candidati)
            calendario.append({"id": len(calendario)+1, "teamA_id": tid, "teamB_id": avv["id"], "golA": None, "golB": None, "giocata": False, "biliardino": None})
            conteggio[tid]+=1; conteggio[avv["id"]]+=1
    random.shuffle(calendario)
    return calendario

def get_team(tid):
    for t in st.session_state.teams:
        if t["id"] == tid:
            return t
    return None

def classifica():
    for t in st.session_state.teams:
        t["punti"]=0; t["gf"]=0; t["gs"]=0; t["diff"]=0; t["giocate"]=0; t["v"]=0
    for m in st.session_state.league_matches:
        if not m["giocata"]: continue
        ta = get_team(m["teamA_id"]); tb = get_team(m["teamB_id"])
        if not ta or not tb: continue
        pA,pB = calcola_punti(m["golA"], m["golB"])
        ta["punti"]+=pA; tb["punti"]+=pB
        ta["gf"]+=m["golA"]; ta["gs"]+=m["golB"]
        tb["gf"]+=m["golB"]; tb["gs"]+=m["golA"]
        ta["giocate"]+=1; tb["giocate"]+=1
        ta["diff"]=ta["gf"]-ta["gs"]; tb["diff"]=tb["gf"]-tb["gs"]
        if pA>pB: ta["v"]+=1
        elif pB>pA: tb["v"]+=1
    return sorted(st.session_state.teams, key=lambda x: (x["punti"], x["diff"], x["gf"]), reverse=True)

def genera_ko(teams_qual):
    if len(teams_qual) <= 8:
        ottavi=[]
        for i in range(0, len(teams_qual)-1, 2):
            ottavi.append({"teamA": teams_qual[i], "teamB": teams_qual[i+1], "golA":None,"golB":None,"giocata":False,"turno":"OTTAVI"})
        return {"top8":[], "playoff":[], "ottavi":ottavi}
    top8 = teams_qual[:8]
    playoff_teams = teams_qual[8:]
    l=len(playoff_teams)
    playoff=[]
    for i in range(l//2):
        playoff.append({"teamA": playoff_teams[i], "teamB": playoff_teams[l-1-i], "golA":None,"golB":None,"giocata":False,"turno":"PLAYOFF"})
    return {"top8": top8, "playoff": playoff, "ottavi": []}

# INIT
if "initialized" not in st.session_state:
    st.session_state.initialized=True
    st.session_state.teams=[]
    st.session_state.config={"num_biliardini":4, "partite_per_coppia":6, "num_fascia_A":16, "nome_torneo":"CHAMPIONS BILIARDINO"}
    st.session_state.league_matches=[]
    st.session_state.knockout_champions=None
    st.session_state.knockout_europa=None
    st.session_state.phase="setup"
    st.session_state.round_number=1
    carica()

# ADMIN
st.sidebar.title("🔐 ACCESSO")
admin_code = st.sidebar.text_input("Codice Admin", type="password", placeholder="0000")
is_admin = admin_code == "0000"
if is_admin:
    st.sidebar.success("ADMIN ATTIVO")
    if st.sidebar.button("Accedi come ADMIN"):
        st.session_state.giocatore="ADMIN"
        st.query_params["user"]="ADMIN"
        st.rerun()

if "giocatore" not in st.session_state:
    st.session_state.giocatore = st.query_params.get("user", None)

st.markdown(f"""
<div class="hero-champions">
    <div class="omini-row">🧍‍♂️ 🧍‍♂️ 🧍‍♂️ ⚽ 🧍‍♂️ 🧍‍♂️ 🧍‍♂️</div>
    <div class="hero-title">{st.session_state.config['nome_torneo']}</div>
    <div class="hero-sub">CHAMPIONS LEAGUE • FOOSBALL EDITION • BY BATTANI</div>
    <div class="omini-row">🧍‍♂️ 🧍‍♂️ 🧍‍♂️ ⚽ 🧍‍♂️ 🧍‍♂️ 🧍‍♂️</div>
</div>
""", unsafe_allow_html=True)

if not st.session_state.giocatore:
    st.markdown("### 👤 SELEZIONA LA TUA COPPIA")
    if st.session_state.teams:
        nomi=[t["nome"] for t in st.session_state.teams]
        scelta=st.selectbox("Coppie:", nomi)
        if st.button("ENTRA", type="primary", use_container_width=True):
            st.session_state.giocatore=scelta
            st.query_params["user"]=scelta
            st.rerun()
    else:
        st.info("Nessuna coppia registrata - chiedi all'admin")

    if is_admin:
        with st.expander("⚙️ CONFIGURAZIONE - ADMIN (Registrazione Coppie)", expanded=True):
            st.markdown("#### 📥 Registrazione Coppie (Fase Iniziale)")
            g1 = st.text_input("Giocatore 1 (opzionale, aggiunta singola)")
            g2 = st.text_input("Giocatore 2 (opzionale)")
            st.markdown("📋 **Oppure incolla lista da WhatsApp:**")
            st.caption("Formato: * Alberto / Socio (con * va bene, lo pulisco io)")
            lista = st.text_area("Lista WhatsApp:", height=200, placeholder="* Alberto / Socio\n* Francesco / Donato\n* Laura / Lucia\n* Styvens / Nick\n* Michele / Fabio", label_visibility="collapsed")

            c1,c2,c3 = st.columns(3)
            num_bil = c1.number_input("N° Biliardini",1,10,st.session_state.config["num_biliardini"])
            partite_pc = c2.selectbox("Partite per coppia nella League Phase:",[6,7,8], index=[6,7,8].index(st.session_state.config["partite_per_coppia"]))
            num_A = c3.number_input("Coppie in Fascia A",8,32,st.session_state.config["num_fascia_A"])
            nome_torneo = st.text_input("Nome Torneo", st.session_state.config["nome_torneo"])

            if st.button("🚀 Aggiungi Coppie", type="primary", use_container_width=True):
                teams=[]
                idx=1
                # 1) Se c'è Giocatore1+2 singoli
                if g1 and g2:
                    nome = f"{g1.strip()} / {g2.strip()}"
                    teams.append({"id": idx, "nome": nome, "punti":0,"gf":0,"gs":0,"diff":0,"giocate":0,"v":0})
                    idx+=1
                # 2) Lista WhatsApp
                for riga in lista.split("\n"):
                    riga=riga.strip()
                    if not riga: continue
                    # Pulisci * - • numeri
                    riga_pulita = re.sub(r'^[\*\-•\d\.\s]+\s*', '', riga).strip()
                    # rimuovi * residui
                    riga_pulita = riga_pulita.replace("*","").strip()
                    if not riga_pulita: continue
                    # Evita duplicati
                    if any(t["nome"].lower()==riga_pulita.lower() for t in teams): continue
                    teams.append({"id": idx, "nome": riga_pulita, "punti":0,"gf":0,"gs":0,"diff":0,"giocate":0,"v":0})
                    idx+=1

                # Se c'erano già teams salvati, aggiungi
                if st.session_state.teams:
                    for t in teams:
                        if not any(existing["nome"].lower()==t["nome"].lower() for existing in st.session_state.teams):
                            t["id"]=len(st.session_state.teams)+1
                            st.session_state.teams.append(t)
                    teams = st.session_state.teams

                if len(teams)<4:
                    st.error(f"Minimo 4 coppie, ora ne hai {len(teams)}. Incolla tutta la lista.")
                else:
                    st.session_state.config={"num_biliardini":num_bil,"partite_per_coppia":partite_pc,"num_fascia_A":num_A,"nome_torneo":nome_torneo}
                    st.session_state.teams=teams
                    st.session_state.league_matches=genera_calendario(teams, partite_pc)
                    st.session_state.phase="league"
                    st.session_state.knockout_champions=None
                    st.session_state.knockout_europa=None
                    st.session_state.giocatore="ADMIN"
                    st.query_params["user"]="ADMIN"
                    salva()
                    st.success(f"✅ Fatto! {len(teams)} coppie, {len(st.session_state.league_matches)} partite generate. Entro come ADMIN...")
                    st.rerun()
    else:
        st.warning("🔒 Inserisci codice Admin 0000 nella sidebar per creare il torneo")

    st.stop()

# LOGGATO
c1,c2=st.columns([3,1])
with c1: st.info(f"🎮 Coppia: **{st.session_state.giocatore}** | Fase: **{st.session_state.phase.upper()}**")
with c2:
    if st.button("Logout"):
        st.session_state.giocatore=None
        st.query_params.clear()
        st.rerun()

if is_admin and st.sidebar.button("🔄 RESET TOTALE"):
    if os.path.exists(STATE_FILE): os.remove(STATE_FILE)
    for k in list(st.session_state.keys()): del st.session_state[k]
    st.rerun()

if st.session_state.phase=="league":
    classif = classifica()
    non_giocate = [m for m in st.session_state.league_matches if not m["giocata"]]
    # assegna biliardini
    for i,m in enumerate(non_giocate[:st.session_state.config["num_biliardini"]]): m["biliardino"]=i+1
    for m in non_giocate[st.session_state.config["num_biliardini"]:]: m["biliardino"]=None

    mio_team = next((t for t in st.session_state.teams if t["nome"]==st.session_state.giocatore), None)
    if st.session_state.giocatore=="ADMIN": mie = non_giocate
    else: mie = [m for m in non_giocate if mio_team and (m["teamA_id"]==mio_team["id"] or m["teamB_id"]==mio_team["id"])]

    if mie:
        st.markdown("### ⭐ LA TUA PARTITA - INSERISCI RISULTATO")
        m=mie[0]
        ta=get_team(m["teamA_id"]); tb=get_team(m["teamB_id"])
        st.markdown(f"""
        <div class="champions-card champions-card-live">
            <div style="display:flex; justify-content:space-between;"><span class="biliardino-badge">🏟️ BILIARDINO {m['biliardino'] if m['biliardino'] else 'IN CODA'}</span><span class="biliardino-badge">ID {m['id']}</span></div>
            <div style="display:flex; justify-content:space-between; align-items:center; margin-top:10px; text-align:center;">
                <div style="flex:1;"><div class="team-name">{ta['nome']}</div></div><div class="vs-badge">VS</div><div style="flex:1;"><div class="team-name">{tb['nome']}</div></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if "golA_temp" not in st.session_state: st.session_state.golA_temp=0
        if "golB_temp" not in st.session_state: st.session_state.golB_temp=0

        ca,_,cb = st.columns([4,1,4])
        with ca:
            st.write(f"**{ta['nome']}**")
            cols=st.columns(8)
            for i in range(8):
                if cols[i].button(str(i), key=f"ga_{m['id']}_{i}", use_container_width=True): st.session_state.golA_temp=i
            st.metric("Gol", st.session_state.golA_temp)
        with cb:
            st.write(f"**{tb['nome']}**")
            cols=st.columns(8)
            for i in range(8):
                if cols[i].button(str(i), key=f"gb_{m['id']}_{i}", use_container_width=True): st.session_state.golB_temp=i
            st.metric("Gol", st.session_state.golB_temp)

        pA,pB=calcola_punti(st.session_state.golA_temp, st.session_state.golB_temp)
        st.info(f"Punti: {ta['nome']} {pA}pt - {tb['nome']} {pB}pt | Diff {st.session_state.golA_temp-st.session_state.golB_temp:+d}")

        if st.button("✅ CONFERMA RISULTATO", type="primary", use_container_width=True):
            m["golA"]=st.session_state.golA_temp; m["golB"]=st.session_state.golB_temp; m["giocata"]=True
            st.session_state.golA_temp=0; st.session_state.golB_temp=0
            salva(); st.success("Salvato!"); st.rerun()

        if is_admin and st.button("❌ Annulla risultato (admin)"):
            m["giocata"]=False; m["golA"]=None; m["golB"]=None; salva(); st.rerun()

    st.divider()
    col_campo, col_class = st.columns([2,1])

    with col_campo:
        st.markdown(f"### 🏟️ IN CORSO ({st.session_state.config['num_biliardini']} biliardini)")
        for m in non_giocate[:st.session_state.config["num_biliardini"]]:
            ta=get_team(m["teamA_id"]); tb=get_team(m["teamB_id"])
            evidenzia = mio_team and (m["teamA_id"]==mio_team["id"] or m["teamB_id"]==mio_team["id"])
            st.markdown(f"""<div class="champions-card {'champions-card-live' if evidenzia else ''}"><div style="display:flex; justify-content:space-between;"><span class="biliardino-badge">TAVOLO {m['biliardino']}</span><span style="font-size:0.7em; color:#6ea8ff;">ID {m['id']}</span></div><div style="display:flex; justify-content:space-between; margin-top:8px;"><span class="team-name">{ta['nome']}</span><span class="vs-badge">VS</span><span class="team-name">{tb['nome']}</span></div></div>""", unsafe_allow_html=True)

        st.markdown(f"### ⏳ CODA ({len(non_giocate[st.session_state.config['num_biliardini']:])} partite)")
        for m in non_giocate[st.session_state.config["num_biliardini"]:][:12]:
            ta=get_team(m["teamA_id"]); tb=get_team(m["teamB_id"])
            st.markdown(f"""<div class="champions-card" style="opacity:0.7; padding:10px;"><div style="display:flex; justify-content:space-between; font-size:0.85em;"><span>{ta['nome']}</span><span style="color:#c9a86a;">VS</span><span>{tb['nome']}</span></div></div>""", unsafe_allow_html=True)

        if len(non_giocate)==0 and is_admin:
            if st.button("🏁 CHIUDI LEAGUE E CREA TABELLONE", type="primary", use_container_width=True):
                classif_finale = classifica()
                num_A = st.session_state.config["num_fascia_A"]
                champ = classif_finale[:num_A]
                europa = classif_finale[num_A:]
                st.session_state.knockout_champions = genera_ko(champ)
                st.session_state.knockout_europa = genera_ko(europa)
                st.session_state.phase="knockout"
                salva(); st.rerun()

    with col_class:
        st.markdown("### 📊 CLASSIFICA UNICA")
        st.caption(f"{st.session_state.config['partite_per_coppia']} partite per coppia | Diff reti + scontri")
        for idx,t in enumerate(classif):
            if idx<8: fascia="top8"; label="🔵 DIRETTA OTTAVI"
            elif idx<st.session_state.config["num_fascia_A"]: fascia="playoff"; label="🟡 PLAYOFF"
            else: fascia="europa"; label="🟠 EUROPA"
            star="⭐" if mio_team and t["id"]==mio_team["id"] else ""
            st.markdown(f"""<div class="classifica-row {fascia}"><div><span style="font-family:Orbitron; font-weight:800; color:#c9a86a; margin-right:6px;">{idx+1}</span><span style="font-weight:800; font-size:0.85em;">{star} {t['nome']}</span><div style="font-size:0.65em; color:#6ea8ff;">{label} • {t['giocate']}/{st.session_state.config['partite_per_coppia']} • {t['punti']} PT</div></div><div style="text-align:right; font-size:0.8em;"><div>GF {t['gf']} GS {t['gs']}</div><div style="color:{'#00ff88' if t['diff']>=0 else '#ff4444'};">Diff {t['diff']:+d}</div></div></div>""", unsafe_allow_html=True)

if st.session_state.phase=="knockout":
    st.markdown("## 🏆 FASE FINALE - CHAMPIONS & EUROPA LEAGUE")
    tab1, tab2 = st.tabs(["⭐ CHAMPIONS - FASCIA A", "🟠 EUROPA LEAGUE - FASCIA B"])
    with tab1:
        ko=st.session_state.knockout_champions
        if ko:
            if ko["top8"]:
                st.markdown("### 🔵 Top 8 - Dirette agli Ottavi (saltano turno)")
                cols=st.columns(4)
                for i,t in enumerate(ko["top8"]): cols[i%4].markdown(f"<div class='knockout-box' style='border-color:#c9a86a;'><b>{t['nome']}</b><br><span style='color:#00d1ff; font-size:0.8em;'>OTTAVI</span><br><span style='font-size:0.7em;'>{t['punti']} pt Diff {t['diff']:+d}</span></div>", unsafe_allow_html=True)
            if ko["playoff"]:
                st.markdown("### 🟡 Playoff Champions (9° vs 24°, 10° vs 23°...)")
                for m in ko["playoff"]:
                    st.markdown(f"<div class='knockout-box'>{m['teamA']['nome']} ({m['teamA']['punti']}pt) VS {m['teamB']['nome']} ({m['teamB']['punti']}pt) - {m['turno']}</div>", unsafe_allow_html=True)
    with tab2:
        ko=st.session_state.knockout_europa
        if ko:
            st.markdown("### Europa League")
            for m in ko.get("ottavi",[])+ko.get("playoff",[]):
                st.markdown(f"<div class='knockout-box'>{m['teamA']['nome']} VS {m['teamB']['nome']}</div>", unsafe_allow_html=True)
            if not ko.get("ottavi") and not ko.get("playoff"):
                st.info("Nessuna squadra in Europa League (tutte in Champions) - abbassa il numero di Fascia A se vuoi l'Europa")
