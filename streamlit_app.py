
import streamlit as st
import random
import re
import json
import os

st.set_page_config(page_title="CHAMPIONS BILIARDINO LIVE // BY BATTANI", page_icon="🏆", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@700;900&family=Orbitron:wght@700;900&display=swap');
.stApp { background: #020a1a; background-image: radial-gradient(ellipse at top, rgba(0,82,180,0.45) 0%, transparent 60%), radial-gradient(ellipse at bottom, rgba(255,215,0,0.1) 0%, transparent 60%); }
.hero-champions { text-align: center; padding: 22px 10px; background: linear-gradient(180deg, #0a1931 0%, #020a1a 100%); border: 2px solid #c9a86a; border-radius: 18px; margin-bottom: 18px; box-shadow: 0 0 35px rgba(201,168,106,0.25); }
.hero-title { font-family: 'Orbitron'; font-size: 2.1em; font-weight: 900; background: linear-gradient(135deg, #fff 10%, #c9a86a 90%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; letter-spacing: 3px; text-transform: uppercase; }
.hero-sub { color: #6ea8ff; font-family: 'Montserrat'; letter-spacing: 4px; font-size: 0.85em; font-weight: 700; }
.omini-row { font-size: 26px; letter-spacing: 10px; }
.champions-card { background: linear-gradient(160deg, #0a1931 0%, #061024 100%); border: 1px solid rgba(201,168,106,0.35); border-left: 4px solid #0052b4; border-radius: 12px; padding: 14px; margin-bottom: 12px; box-shadow: 0 5px 18px rgba(0,0,0,0.5); }
.champions-card-live { border: 2px solid #c9a86a; box-shadow: 0 0 22px rgba(201,168,106,0.35), 0 0 12px rgba(0,82,180,0.4); background: linear-gradient(160deg, #12326b 0%, #0a1931 100%); }
.biliardino-badge { background: #020a1a; border: 1px solid #c9a86a; color: #c9a86a; padding: 2px 9px; border-radius: 20px; font-family: 'Orbitron'; font-size: 0.68em; font-weight: 800; }
.vs-badge { background: #0052b4; color: #fff; font-weight: 900; font-family: 'Orbitron'; width: 32px; height: 32px; border-radius: 50%; display: flex; align-items: center; justify-content: center; }
.vs-badge-live { background: #c9a86a; color: #020a1a; animation: pulse 1.5s infinite; }
@keyframes pulse { 0%{transform:scale(1)} 50%{transform:scale(1.15)} 100%{transform:scale(1)} }
.team-name { font-family: 'Montserrat'; font-weight: 800; text-transform: uppercase; color: #eaf2ff; font-size: 0.92em; }
.classifica-row { display: flex; justify-content: space-between; align-items: center; background: rgba(2,10,26,0.9); padding: 7px 11px; border-radius: 6px; margin-bottom: 4px; border-left: 3px solid transparent; }
.classifica-row.top8 { border-left-color: #00d1ff; background: rgba(0,82,180,0.28); }
.classifica-row.playoff { border-left-color: #c9a86a; }
.classifica-row.europa { border-left-color: #ff6b35; opacity: 0.8; }
.ko-stage-title { font-family: 'Orbitron'; color: #c9a86a; font-size: 1.15em; font-weight: 900; letter-spacing: 2px; margin: 18px 0 8px 0; border-bottom: 1px solid rgba(201,168,106,0.3); padding-bottom: 6px; }
.ko-match { background: linear-gradient(135deg, #0a1931, #07152f); border: 1px solid #1e3a6b; border-radius: 10px; padding: 10px; margin-bottom: 8px; }
.ko-match-winner { border-color: #c9a86a; background: linear-gradient(135deg, #1e3a5f, #0a1931); }
.live-dot { width: 8px; height: 8px; background: #ff3b3b; border-radius: 50%; display: inline-block; margin-right: 6px; box-shadow: 0 0 8px #ff3b3b; animation: blink 1s infinite; }
@keyframes blink { 0%{opacity:1} 50%{opacity:0.2} 100%{opacity:1} }
</style>
""", unsafe_allow_html=True)

STATE_FILE = "torneo_champions_state.json"

def salva():
    data = {k: st.session_state[k] for k in ["teams","config","league_matches","ko_champions","ko_europa","phase"]}
    with open(STATE_FILE, "w") as f:
        json.dump(data, f, indent=2)

def carica():
    if not os.path.exists(STATE_FILE): return False
    try:
        with open(STATE_FILE, "r") as f:
            d=json.load(f)
        for k in d: st.session_state[k]=d[k]
        return True
    except: return False

def punti(gf,gs):
    diff=gf-gs
    if diff>=2: return 3,0
    if diff==1: return 2,1
    if diff==-1: return 1,2
    return 0,3

def genera_league(teams, n_per_team):
    poss=[]
    for i in range(len(teams)):
        for j in range(i+1,len(teams)): poss.append((teams[i]["id"],teams[j]["id"]))
    random.shuffle(poss)
    cnt={t["id"]:0 for t in teams}
    cal=[]
    for a,b in poss:
        if cnt[a]<n_per_team and cnt[b]<n_per_team:
            cal.append({"id":len(cal)+1,"teamA_id":a,"teamB_id":b,"golA":None,"golB":None,"giocata":False,"biliardino":None})
            cnt[a]+=1; cnt[b]+=1
    for tid in list(cnt.keys()):
        while cnt[tid]<n_per_team:
            cand=[t for t in teams if t["id"]!=tid]
            av=random.choice(cand)
            cal.append({"id":len(cal)+1,"teamA_id":tid,"teamB_id":av["id"],"golA":None,"golB":None,"giocata":False,"biliardino":None})
            cnt[tid]+=1; cnt[av["id"]]+=1
    random.shuffle(cal)
    return cal

def get_team(tid):
    for t in st.session_state.teams:
        if t["id"]==tid: return t
    return None

def classifica_calc():
    for t in st.session_state.teams:
        t["punti"]=0; t["gf"]=0; t["gs"]=0; t["giocate"]=0; t["diff"]=0
    for m in st.session_state.league_matches:
        if not m["giocata"]: continue
        ta=get_team(m["teamA_id"]); tb=get_team(m["teamB_id"])
        if not ta or not tb: continue
        pA,pB=punti(m["golA"],m["golB"])
        ta["punti"]+=pA; tb["punti"]+=pB
        ta["gf"]+=m["golA"]; ta["gs"]+=m["golB"]; tb["gf"]+=m["golB"]; tb["gs"]+=m["golA"]
        ta["giocate"]+=1; tb["giocate"]+=1
    for t in st.session_state.teams: t["diff"]=t["gf"]-t["gs"]
    return sorted(st.session_state.teams, key=lambda x:(x["punti"],x["diff"],x["gf"]), reverse=True)

def crea_ko_iniziale(teams_qual):
    """teams_qual già ordinate"""
    if len(teams_qual)<=8:
        return {"top8":teams_qual,"playoff":[],"ottavi":[],"quarti":[],"semi":[],"finale":None,"vincitore":None,"fase_attuale":"OTTAVI"}
    top8=teams_qual[:8]
    playoff_teams=teams_qual[8:]
    playoff=[]
    l=len(playoff_teams)
    for i in range(l//2):
        playoff.append({"id":f"PL{i+1}","teamA":playoff_teams[i],"teamB":playoff_teams[l-1-i],"golA":None,"golB":None,"giocata":False,"vincitore":None,"biliardino":None})
    return {"top8":top8,"playoff":playoff,"ottavi":[],"quarti":[],"semi":[],"finale":None,"vincitore":None,"fase_attuale":"PLAYOFF"}

def avanza_ko(ko):
    # Se playoff finiti -> crea ottavi
    if ko["fase_attuale"]=="PLAYOFF" and ko["playoff"]:
        if all(m["giocata"] for m in ko["playoff"]):
            vincitori=[m["vincitore"] for m in ko["playoff"]]
            # accoppia top8 vs vincitori: 1° vs peggior vincitore, ecc. Semplice: shuffle
            # Ordina top8 per classifica, vincitori per punti originali
            ottavi=[]
            # Top8 già in ordine, vincitori in ordine di arrivo
            pool = ko["top8"] + vincitori
            random.shuffle(pool)
            for i in range(0,len(pool)-1,2):
                ottavi.append({"id":f"OT{i//2+1}","teamA":pool[i],"teamB":pool[i+1],"golA":None,"golB":None,"giocata":False,"vincitore":None,"biliardino":None})
            ko["ottavi"]=ottavi
            ko["fase_attuale"]="OTTAVI"
            return ko

    # Se ottavi finiti -> quarti
    if ko["fase_attuale"]=="OTTAVI" and ko["ottavi"]:
        if all(m["giocata"] for m in ko["ottavi"]):
            vinc=[m["vincitore"] for m in ko["ottavi"]]
            quarti=[]
            for i in range(0,len(vinc)-1,2):
                quarti.append({"id":f"QU{i//2+1}","teamA":vinc[i],"teamB":vinc[i+1],"golA":None,"golB":None,"giocata":False,"vincitore":None,"biliardino":None})
            ko["quarti"]=quarti
            ko["fase_attuale"]="QUARTI"
            return ko

    if ko["fase_attuale"]=="QUARTI" and ko["quarti"]:
        if all(m["giocata"] for m in ko["quarti"]):
            vinc=[m["vincitore"] for m in ko["quarti"]]
            semi=[]
            for i in range(0,len(vinc)-1,2):
                semi.append({"id":f"SE{i//2+1}","teamA":vinc[i],"teamB":vinc[i+1],"golA":None,"golB":None,"giocata":False,"vincitore":None,"biliardino":None})
            ko["semi"]=semi
            ko["fase_attuale"]="SEMI"
            return ko

    if ko["fase_attuale"]=="SEMI" and ko["semi"]:
        if all(m["giocata"] for m in ko["semi"]):
            vinc=[m["vincitore"] for m in ko["semi"]]
            if len(vinc)>=2:
                ko["finale"]={"id":"FIN","teamA":vinc[0],"teamB":vinc[1],"golA":None,"golB":None,"giocata":False,"vincitore":None,"biliardino":None}
                ko["fase_attuale"]="FINALE"
            return ko

    if ko["fase_attuale"]=="FINALE" and ko["finale"]:
        if ko["finale"]["giocata"]:
            ko["vincitore"]=ko["finale"]["vincitore"]
            ko["fase_attuale"]="FINITO"
            return ko
    return ko

def assegna_biliardini_ko(ko, num_biliardini, partite_gia_in_corso_count):
    # Ritorna lista partite live per questo tabellone
    fase = ko["fase_attuale"]
    lista=[]
    if fase=="PLAYOFF": lista=ko["playoff"]
    elif fase=="OTTAVI": lista=ko["ottavi"]
    elif fase=="QUARTI": lista=ko["quarti"]
    elif fase=="SEMI": lista=ko["semi"]
    elif fase=="FINALE": lista=[ko["finale"]] if ko["finale"] else []
    else: lista=[]
    # solo non giocate
    non_giocate=[m for m in lista if not m["giocata"]]
    return non_giocate

# INIT
if "initialized" not in st.session_state:
    st.session_state.initialized=True
    st.session_state.teams=[]
    st.session_state.config={"num_biliardini":4,"partite_per_coppia":6,"num_fascia_A":16,"nome_torneo":"CHAMPIONS BILIARDINO LIVE"}
    st.session_state.league_matches=[]
    st.session_state.ko_champions=None
    st.session_state.ko_europa=None
    st.session_state.phase="setup"
    carica()

# ADMIN
st.sidebar.title("🔐 ACCESSO")
admin_code=st.sidebar.text_input("Codice Admin", type="password", placeholder="0000")
is_admin=admin_code=="0000"
if is_admin:
    st.sidebar.success("ADMIN 0000 ATTIVO")
    if st.sidebar.button("Accedi ADMIN"):
        st.session_state.giocatore="ADMIN"
        st.query_params["user"]="ADMIN"
        st.rerun()

if "giocatore" not in st.session_state:
    st.session_state.giocatore=st.query_params.get("user",None)

st.markdown(f"""
<div class="hero-champions">
    <div class="omini-row">🧍‍♂️ 🧍‍♂️ 🧍‍♂️ ⚽ 🧍‍♂️ 🧍‍♂️ 🧍‍♂️</div>
    <div class="hero-title">{st.session_state.config['nome_torneo']}</div>
    <div class="hero-sub">★ CHAMPIONS LEAGUE LIVE • FOOSBALL EDITION • BY BATTANI ★</div>
    <div class="omini-row">🧍‍♂️ 🧍‍♂️ 🧍‍♂️ ⚽ 🧍‍♂️ 🧍‍♂️ 🧍‍♂️</div>
</div>
""", unsafe_allow_html=True)

if not st.session_state.giocatore:
    st.markdown("### 👤 SELEZIONA LA TUA COPPIA")
    if st.session_state.teams:
        nomi=[t["nome"] for t in st.session_state.teams]
        scelta=st.selectbox("Coppie:", nomi)
        if st.button("ENTRA NEL TORNEO LIVE", type="primary", use_container_width=True):
            st.session_state.giocatore=scelta
            st.query_params["user"]=scelta
            st.rerun()
    else:
        st.info("Nessuna coppia registrata - chiedi all'admin di creare il torneo")
    if is_admin:
        with st.expander("⚙️ SETUP TORNEO CHAMPIONS LIVE - ADMIN", expanded=True):
            c1,c2,c3=st.columns(3)
            num_bil=c1.number_input("N° Biliardini",1,10,st.session_state.config["num_biliardini"])
            partite_pc=c2.selectbox("Partite per coppia",[6,7,8], index=[6,7,8].index(st.session_state.config["partite_per_coppia"]))
            num_A=c3.number_input("Coppie in Fascia A",8,32,st.session_state.config["num_fascia_A"])
            nome_torneo=st.text_input("Nome Torneo", st.session_state.config["nome_torneo"])
            lista=st.text_area("Lista coppie (una per riga: Rossi / Bianchi)", height=220, placeholder="Battani / Fiore\nRossi / Verdi\nSpaccaTutto Team")
            if st.button("💾 CREA CALENDARIO CHAMPIONS LIVE", type="primary", use_container_width=True):
                teams=[]
                for idx,riga in enumerate(lista.split("\n")):
                    riga=riga.strip()
                    if not riga: continue
                    nome=re.sub(r'^\d+[\.\-\)\s]*','',riga).strip()
                    teams.append({"id":idx+1,"nome":nome,"punti":0,"gf":0,"gs":0,"diff":0,"giocate":0})
                if len(teams)<4:
                    st.error("Minimo 4 coppie")
                else:
                    st.session_state.config={"num_biliardini":num_bil,"partite_per_coppia":partite_pc,"num_fascia_A":num_A,"nome_torneo":nome_torneo}
                    st.session_state.teams=teams
                    st.session_state.league_matches=genera_league(teams, partite_pc)
                    st.session_state.phase="league"
                    st.session_state.ko_champions=None
                    st.session_state.ko_europa=None
                    salva()
                    st.success(f"Torneo LIVE creato! {len(teams)} coppie, {len(st.session_state.league_matches)} partite")
                    st.rerun()
    st.stop()

# LOGGATO
c1,c2=st.columns([3,1])
with c1: st.info(f"🎮 Coppia: **{st.session_state.giocatore}** | Fase: **{st.session_state.phase.upper()}** | Biliardini: {st.session_state.config['num_biliardini']}")
with c2:
    if st.button("Logout"):
        st.session_state.giocatore=None
        st.query_params.clear()
        st.rerun()

if is_admin and st.sidebar.button("🔄 RESET TOTALE"):
    if os.path.exists(STATE_FILE): os.remove(STATE_FILE)
    for k in list(st.session_state.keys()): del st.session_state[k]
    st.rerun()

# ========== FUNZIONE GENERICA PER SEGNALARE RISULTATO KO ==========
def ui_segna_ko(match, prefix):
    ta=match["teamA"]; tb=match["teamB"]
    st.markdown(f"""
    <div class="champions-card champions-card-live">
        <div style="display:flex; justify-content:space-between;"><span class="biliardino-badge">🏟️ {match.get('biliardino','?')} • {match.get('id','')} • LIVE</span><span class="live-dot"></span><span class="biliardino-badge">{prefix}</span></div>
        <div style="display:flex; justify-content:space-between; align-items:center; margin-top:10px; text-align:center;">
            <div style="flex:1;"><div class="team-name">{ta['nome']}</div></div><div class="vs-badge vs-badge-live">VS</div><div style="flex:1;"><div class="team-name">{tb['nome']}</div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    keyA=f"golA_{prefix}_{match['id']}"
    keyB=f"golB_{prefix}_{match['id']}"
    if keyA not in st.session_state: st.session_state[keyA]=0
    if keyB not in st.session_state: st.session_state[keyB]=0
    ca,_,cb=st.columns([4,1,4])
    with ca:
        st.write(f"**{ta['nome']}**")
        cols=st.columns(8)
        for i in range(8):
            if cols[i].button(str(i), key=f"{prefix}_ga_{match['id']}_{i}", use_container_width=True): st.session_state[keyA]=i
        st.metric("Gol", st.session_state[keyA])
    with cb:
        st.write(f"**{tb['nome']}**")
        cols=st.columns(8)
        for i in range(8):
            if cols[i].button(str(i), key=f"{prefix}_gb_{match['id']}_{i}", use_container_width=True): st.session_state[keyB]=i
        st.metric("Gol", st.session_state[keyB])
    if st.button(f"✅ CONFERMA {prefix} - {ta['nome']} {st.session_state[keyA]}-{st.session_state[keyB]} {tb['nome']}", key=f"conf_{prefix}_{match['id']}", type="primary", use_container_width=True):
        if st.session_state[keyA]==st.session_state[keyB]:
            st.error("Pareggio non ammesso in eliminazione diretta! Segnate fino a 7, deve esserci un vincitore")
        else:
            match["golA"]=st.session_state[keyA]; match["golB"]=st.session_state[keyB]; match["giocata"]=True
            match["vincitore"]=ta if st.session_state[keyA]>st.session_state[keyB] else tb
            st.session_state[keyA]=0; st.session_state[keyB]=0
            salva(); st.success(f"Vince {match['vincitore']['nome']}!"); st.rerun()
    if is_admin and st.button(f"❌ Annulla {match['id']}", key=f"ann_{prefix}_{match['id']}"):
        match["giocata"]=False; match["golA"]=None; match["golB"]=None; match["vincitore"]=None; salva(); st.rerun()

# ===================== FASE LEAGUE LIVE =====================
if st.session_state.phase=="league":
    classif=classifica_calc()
    non_giocate=[m for m in st.session_state.league_matches if not m["giocata"]]
    for i,m in enumerate(non_giocate[:st.session_state.config["num_biliardini"]]): m["biliardino"]=i+1
    for m in non_giocate[st.session_state.config["num_biliardini"]:]: m["biliardino"]=None

    mio_team=next((t for t in st.session_state.teams if t["nome"]==st.session_state.giocatore), None)
    mie = non_giocate if st.session_state.giocatore=="ADMIN" else [m for m in non_giocate if mio_team and (m["teamA_id"]==mio_team["id"] or m["teamB_id"]==mio_team["id"])]

    if mie:
        st.markdown("### ⭐ LA TUA PARTITA LIVE - SEGNALAZIONE")
        m=mie[0]
        ta=get_team(m["teamA_id"]); tb=get_team(m["teamB_id"])
        st.markdown(f"""
        <div class="champions-card champions-card-live">
            <div style="display:flex; justify-content:space-between;"><span class="biliardino-badge">🏟️ BILIARDINO {m['biliardino'] if m['biliardino'] else 'IN CODA'} • LIVE</span><span class="live-dot"></span><span class="biliardino-badge">ID {m['id']} • LEAGUE</span></div>
            <div style="display:flex; justify-content:space-between; align-items:center; margin-top:10px; text-align:center;">
                <div style="flex:1;"><div class="team-name">{ta['nome']}</div></div><div class="vs-badge vs-badge-live">VS</div><div style="flex:1;"><div class="team-name">{tb['nome']}</div></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if "golA_temp" not in st.session_state: st.session_state.golA_temp=0
        if "golB_temp" not in st.session_state: st.session_state.golB_temp=0
        ca,_,cb=st.columns([4,1,4])
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
        pA,pB=punti(st.session_state.golA_temp, st.session_state.golB_temp)
        st.info(f"Anteprima: {ta['nome']} {pA}pt - {tb['nome']} {pB}pt | Diff {st.session_state.golA_temp-st.session_state.golB_temp:+d}")
        if st.button("✅ CONFERMA RISULTATO LEAGUE", type="primary", use_container_width=True):
            m["golA"]=st.session_state.golA_temp; m["golB"]=st.session_state.golB_temp; m["giocata"]=True
            st.session_state.golA_temp=0; st.session_state.golB_temp=0; salva(); st.rerun()
        if is_admin and st.button("❌ Annulla (admin)"):
            m["giocata"]=False; m["golA"]=None; m["golB"]=None; salva(); st.rerun()

    st.divider()
    col_campo,col_class=st.columns([2,1])
    with col_campo:
        st.markdown(f"### 🏟️ LIVE - IN CORSO ({len(non_giocate[:st.session_state.config['num_biliardini']])}/{st.session_state.config['num_biliardini']} biliardini occupati)")
        for m in non_giocate[:st.session_state.config["num_biliardini"]]:
            ta=get_team(m["teamA_id"]); tb=get_team(m["teamB_id"])
            evidenzia=mio_team and (m["teamA_id"]==mio_team["id"] or m["teamB_id"]==mio_team["id"])
            st.markdown(f"""<div class="champions-card {'champions-card-live' if evidenzia else ''}"><div style="display:flex; justify-content:space-between;"><span class="biliardino-badge">TAVOLO {m['biliardino']}</span><span class="live-dot"></span><span style="font-size:0.7em; color:#6ea8ff;">ID {m['id']}</span></div><div style="display:flex; justify-content:space-between; margin-top:8px;"><span class="team-name">{ta['nome']}</span><span class="vs-badge">VS</span><span class="team-name">{tb['nome']}</span></div></div>""", unsafe_allow_html=True)
        st.markdown(f"### ⏳ CODA ({len(non_giocate[st.session_state.config['num_biliardini']:])} partite)")
        for m in non_giocate[st.session_state.config["num_biliardini"]:][:10]:
            ta=get_team(m["teamA_id"]); tb=get_team(m["teamB_id"])
            st.markdown(f"""<div class="champions-card" style="opacity:0.7; padding:9px;"><div style="display:flex; justify-content:space-between; font-size:0.84em;"><span>{ta['nome']}</span><span style="color:#c9a86a;">VS</span><span>{tb['nome']}</span></div></div>""", unsafe_allow_html=True)
        if len(non_giocate)==0 and is_admin:
            if st.button("🏁 CHIUDI FASE LEAGUE E GENERA TABELLONE LIVE", type="primary", use_container_width=True):
                classif_finale=classifica_calc()
                num_A=st.session_state.config["num_fascia_A"]
                champ=classif_finale[:num_A]
                europa=classif_finale[num_A:]
                st.session_state.ko_champions=crea_ko_iniziale(champ)
                st.session_state.ko_europa=crea_ko_iniziale(europa)
                st.session_state.phase="knockout"
                salva(); st.rerun()
    with col_class:
        st.markdown("### 📊 CLASSIFICA LIVE")
        for idx,t in enumerate(classif):
            if idx<8: fascia="top8"; label="🔵 DIRETTA OTTAVI"
            elif idx<st.session_state.config["num_fascia_A"]: fascia="playoff"; label="🟡 PLAYOFF"
            else: fascia="europa"; label="🟠 EUROPA"
            star="⭐" if mio_team and t["id"]==mio_team["id"] else ""
            st.markdown(f"""<div class="classifica-row {fascia}"><div><span style="font-family:Orbitron; font-weight:800; color:#c9a86a; margin-right:5px;">{idx+1}</span><span style="font-weight:800; font-size:0.84em;">{star} {t['nome']}</span><div style="font-size:0.62em; color:#6ea8ff;">{label} • {t['giocate']}/{st.session_state.config['partite_per_coppia']} • {t['punti']} PT</div></div><div style="text-align:right; font-size:0.78em;"><div>GF {t['gf']} GS {t['gs']}</div><div style="color:{'#00ff88' if t['diff']>=0 else '#ff4444'};">Diff {t['diff']:+d}</div></div></div>""", unsafe_allow_html=True)

# ===================== FASE KNOCKOUT LIVE =====================
if st.session_state.phase=="knockout":
    st.markdown("## 🏆 TABELLONE LIVE - CHAMPIONS & EUROPA")
    # Avanza automaticamente se una fase è finita
    if st.session_state.ko_champions:
        st.session_state.ko_champions=avanza_ko(st.session_state.ko_champions)
    if st.session_state.ko_europa:
        st.session_state.ko_europa=avanza_ko(st.session_state.ko_europa)
    salva()

    tabC, tabE = st.tabs(["⭐ CHAMPIONS LEAGUE LIVE - FASCIA A", "🟠 EUROPA LEAGUE LIVE - FASCIA B"])

    with tabC:
        ko=st.session_state.ko_champions
        if not ko:
            st.warning("Nessun tabellone Champions")
        else:
            st.markdown(f"### 🔴 LIVE: Fase attuale: **{ko['fase_attuale']}**")
            # Mostra partite live della fase attuale con biliardini
            live_now = assegna_biliardini_ko(ko, st.session_state.config["num_biliardini"], 0)
            # Assegna biliardino numeri
            for i,m in enumerate([mm for mm in live_now if not mm["giocata"]][:st.session_state.config["num_biliardini"]]): m["biliardino"]=f"TAV {i+1}"
            for m in [mm for mm in live_now if not mm["giocata"]][st.session_state.config["num_biliardini"]:]: m["biliardino"]="CODA"

            # La mia partita knockout
            mio_nome=st.session_state.giocatore
            if live_now:
                # Filtra per me
                if mio_nome!="ADMIN":
                    mie_ko=[m for m in live_now if not m["giocata"] and (m["teamA"]["nome"]==mio_nome or m["teamB"]["nome"]==mio_nome)]
                else:
                    mie_ko=[m for m in live_now if not m["giocata"]][:1]
                if mie_ko:
                    st.markdown("### ⭐ LA TUA PARTITA KNOCKOUT LIVE")
                    ui_segna_ko(mie_ko[0], f"CHAMPIONS {ko['fase_attuale']}")

            st.divider()
            # Visualizzazione bracket completo live
            for stage in ["PLAYOFF","OTTAVI","QUARTI","SEMI","FINALE"]:
                matches=[]
                if stage=="PLAYOFF": matches=ko["playoff"]
                elif stage=="OTTAVI": matches=ko["ottavi"]
                elif stage=="QUARTI": matches=ko["quarti"]
                elif stage=="SEMI": matches=ko["semi"]
                elif stage=="FINALE": matches=[ko["finale"]] if ko["finale"] else []
                if not matches: continue
                st.markdown(f"<div class='ko-stage-title'>{stage} {'🔴 LIVE' if ko['fase_attuale']==stage else '✅' if all(m['giocata'] for m in matches) else '⏳'}</div>", unsafe_allow_html=True)
                cols=st.columns(2)
                for i,m in enumerate(matches):
                    vinc = m.get("vincitore")
                    stato = f"✅ {vinc['nome']} vince {m['golA']}-{m['golB']}" if m["giocata"] else f"🔴 LIVE TAV {m.get('biliardino','?')}" if m.get("biliardino") and "TAV" in str(m.get("biliardino")) else "⏳ IN CODA" if not m["giocata"] else ""
                    cols[i%2].markdown(f"""
                    <div class="ko-match {'ko-match-winner' if m['giocata'] else ''}">
                        <div style="display:flex; justify-content:space-between; font-size:0.7em; color:#c9a86a;"><span>{m['id']}</span><span>{stato}</span></div>
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-top:6px;">
                            <span class="team-name" style="color:{'#00ff88' if vinc and vinc['nome']==m['teamA']['nome'] else '#eaf2ff'};">{m['teamA']['nome']}</span>
                            <span style="font-family:Orbitron; font-weight:900; color:#fff;">{f"{m['golA']}-{m['golB']}" if m['giocata'] else "vs"}</span>
                            <span class="team-name" style="color:{'#00ff88' if vinc and vinc['nome']==m['teamB']['nome'] else '#eaf2ff'};">{m['teamB']['nome']}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            if ko.get("vincitore"):
                st.balloons()
                st.markdown(f"<div class='hero-champions' style='border-color:#00ff88;'><div class='hero-title'>🏆 CAMPIONE CHAMPIONS: {ko['vincitore']['nome']} 🏆</div></div>", unsafe_allow_html=True)

    with tabE:
        ko=st.session_state.ko_europa
        if not ko or (not ko["playoff"] and not ko["ottavi"]):
            st.info("Nessuna squadra in Europa League - aumenta le coppie o riduci Fascia A")
        else:
            st.markdown(f"### 🔴 LIVE EUROPA: {ko['fase_attuale']}")
            live_now = assegna_biliardini_ko(ko, st.session_state.config["num_biliardini"], 0)
            for i,m in enumerate([mm for mm in live_now if not mm["giocata"]][:st.session_state.config["num_biliardini"]]): m["biliardino"]=f"TAV {i+1}"
            mio_nome=st.session_state.giocatore
            if live_now:
                if mio_nome!="ADMIN":
                    mie_ko=[m for m in live_now if not m["giocata"] and (m["teamA"]["nome"]==mio_nome or m["teamB"]["nome"]==mio_nome)]
                else:
                    mie_ko=[m for m in live_now if not m["giocata"]][:1]
                if mie_ko:
                    st.markdown("### ⭐ LA TUA PARTITA EUROPA LEAGUE LIVE")
                    ui_segna_ko(mie_ko[0], f"EUROPA {ko['fase_attuale']}")
            for stage in ["PLAYOFF","OTTAVI","QUARTI","SEMI","FINALE"]:
                matches=[]
                if stage=="PLAYOFF": matches=ko["playoff"]
                elif stage=="OTTAVI": matches=ko["ottavi"]
                elif stage=="QUARTI": matches=ko["quarti"]
                elif stage=="SEMI": matches=ko["semi"]
                elif stage=="FINALE": matches=[ko["finale"]] if ko["finale"] else []
                if not matches: continue
                st.markdown(f"<div class='ko-stage-title'>{stage} EUROPA {'🔴 LIVE' if ko['fase_attuale']==stage else ''}</div>", unsafe_allow_html=True)
                cols=st.columns(2)
                for i,m in enumerate(matches):
                    vinc=m.get("vincitore")
                    stato=f"✅ {vinc['nome']}" if m["giocata"] else "🔴 LIVE" if m.get("biliardino") else "⏳"
                    cols[i%2].markdown(f"<div class='ko-match {'ko-match-winner' if m['giocata'] else ''}'><div style='font-size:0.7em; color:#ff8c42;'>{m['id']} {stato}</div><div style='display:flex; justify-content:space-between;'><span class='team-name'>{m['teamA']['nome']}</span><span>{f"{m['golA']}-{m['golB']}" if m['giocata'] else 'vs'}</span><span class='team-name'>{m['teamB']['nome']}</span></div></div>", unsafe_allow_html=True)
            if ko.get("vincitore"):
                st.balloons()
                st.markdown(f"<div class='hero-champions' style='border-color:#ff8c42;'><div class='hero-title'>🏆 CAMPIONE EUROPA LEAGUE: {ko['vincitore']['nome']} 🏆</div></div>", unsafe_allow_html=True)
