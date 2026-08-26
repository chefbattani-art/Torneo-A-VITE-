        num_biliardini = st.session_state.num_biliardini
        partite_in_corso = partite[:num_biliardini]
        partite_in_coda = partite[num_biliardini:]
        
        is_personale = st.session_state.vista_personale_attiva
        target_user = st.session_state.giocatore_selezionato.lower()

        if is_personale:
            st.markdown(f"### 🔥 LE PARTITE DI {st.session_state.giocatore_selezionato.upper()}:")
        else:
            st.markdown("### 🔥 PARTITE IN CORSO (Sui biliardini):")

        total_partite_corso = len(partite_in_corso)

        for idx, match in enumerate(partite_in_corso):
            tA_att, tA_port = match["teamA"]
            tB_att, tB_port = match["teamB"]
            nomi_match = [tA_att['name'].lower(), tA_port['name'].lower(), tB_att['name'].lower(), tB_port['name'].lower()]
            
            if is_personale and target_user not in nomi_match:
                continue

            biliardino_num = idx + 1
            # L'ultima partita è ora l'ultima TRA QUELLI ATTIVI SUI BILIARDINI, a patto che non ci siano match in coda. 
            # Se ci sono match in coda, i biliardini sono tutti pieni e nessuno di essi è l'ultimo assoluto del turno.
            is_ultima = (idx == total_partite_corso - 1) and (len(partite_in_coda) == 0)

            if is_ultima and not is_personale:
                st.markdown(f"""<div class="pro-last-match-banner">⚠️ ULTIMA PARTITA TURNO N° {st.session_state.round_number}</div>""", unsafe_allow_html=True)
                st.markdown(f"""
                    <div class="pro-match-card-last">
                        <div class="match-header-row">
                            <span class="biliardino-title" style="color: #ef4444;">🏟️ BILIARDINO {biliardino_num} (ULTIMO MATCH)</span>
                            <span class="turno-badge" style="border-color: #ef4444; color: #ef4444;">TURNO {st.session_state.round_number}</span>
                        </div>
                        <div class="match-teams-row" style="background: #180505; border-color: #7f1d1d;">
                            <div class="team-box">🥅 {tA_port['name'].upper()} / ⚽️ {tA_att['name'].upper()}</div>
                            <div class="vs-badge" style="color: #ef4444;">VS</div>
                            <div class="team-box">🥅 {tB_port['name'].upper()} / ⚽️ {tB_att['name'].upper()}</div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            else:
                card_style_class = "pro-match-card-last" if (is_ultima and is_personale) else "pro-match-card"
                if is_ultima and is_personale:
                    st.markdown(f"""<div class="pro-last-match-banner">⚠️ ULTIMA PARTITA TURNO N° {st.session_state.round_number}</div>""", unsafe_allow_html=True)
                
                st.markdown(f"""
                    <div class="{card_style_class}">
                        <div class="match-header-row">
                            <span class="biliardino-title">🏟️ BILIARDINO {biliardino_num}</span>
                            <span class="turno-badge">TURNO {st.session_state.round_number}</span>
                        </div>
                        <div class="match-teams-row">
                            <div class="team-box">🥅 {tA_port['name'].upper()} / ⚽️ {tA_att['name'].upper()}</div>
                            <div class="vs-badge">VS</div>
                            <div class="team-box">🥅 {tB_port['name'].upper()} / ⚽️ {tB_att['name'].upper()}</div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            
            nome_coppia_a = f"{tA_port['name'].upper()} & {tA_att['name'].upper()}"
            nome_coppia_b = f"{tB_port['name'].upper()} & {tB_att['name'].upper()}"

            c1, c2 = st.columns(2)
            with c1:
                if st.button(f"⚡ VITTORIA: {nome_coppia_a}", key=f"wa_{st.session_state.round_number}_{idx}", use_container_width=True):
                    salva_snapshot()
                    perdenti_turno = [tB_att, tB_port]
                    for v in [tA_att, tA_port]: v["last_result"] = 'W'
                    for per in perdenti_turno:
                        per["last_result"] = 'L'
                        per["lives"] = max(0, per["lives"] - 1)
                        if per["lives"] == 0: per["eliminated"] = True
                    
                    periti_nomi = [p['name'] for p in perdenti_turno if p['lives'] == 0]
                    perdita_vite_nomi = [p['name'] for p in perdenti_turno]
                    
                    if "turno_report_log" not in st.session_state or st.session_state.turno_report_log["turno"] != st.session_state.round_number:
                        st.session_state.turno_report_log = {"turno": st.session_state.round_number, "vite_perse": [], "eliminati": []}
                    
                    st.session_state.turno_report_log["vite_perse"].extend(perdita_vite_nomi)
                    st.session_state.turno_report_log["eliminati"].extend(periti_nomi)

                    st.session_state.current_round_matches["partite"].pop(idx)
                    if not st.session_state.current_round_matches["partite"]:
                        st.session_state.round_number += 1
                        st.session_state.current_round_matches = genera_abbinamenti()
                        st.session_state.turno_report_log = {"turno": st.session_state.round_number, "vite_perse": [], "eliminati": []}
                    salva_stato()
                    st.rerun()

            with c2:
                if st.button(f"⚡ VITTORIA: {nome_coppia_b}", key=f"wb_{st.session_state.round_number}_{idx}", use_container_width=True):
                    salva_snapshot()
                    perdenti_turno = [tA_att, tA_port]
                    for v in [tB_att, tB_port]: v["last_result"] = 'W'
                    for per in perdenti_turno:
                        per["last_result"] = 'L'
                        per["lives"] = max(0, per["lives"] - 1)
                        if per["lives"] == 0: per["eliminated"] = True
                    
                    periti_nomi = [p['name'] for p in perdenti_turno if p['lives'] == 0]
                    perdita_vite_nomi = [p['name'] for p in perdenti_turno]
                    
                    if "turno_report_log" not in st.session_state or st.session_state.turno_report_log["turno"] != st.session_state.round_number:
                        st.session_state.turno_report_log = {"turno": st.session_state.round_number, "vite_perse": [], "eliminati": []}
                    
                    st.session_state.turno_report_log["vite_perse"].extend(perdita_vite_nomi)
                    st.session_state.turno_report_log["eliminati"].extend(periti_nomi)

                    st.session_state.current_round_matches["partite"].pop(idx)
                    if not st.session_state.current_round_matches["partite"]:
                        st.session_state.round_number += 1
                        st.session_state.current_round_matches = genera_abbinamenti()
                        st.session_state.turno_report_log = {"turno": st.session_state.round_number, "vite_perse": [], "eliminati": []}
                    salva_stato()
                    st.rerun()

        if "turno_report_log" in st.session_state and st.session_state.turno_report_log["turno"] == st.session_state.round_number:
            log_data = st.session_state.turno_report_log
            if log_data["vite_perse"]:
                nomi_vite = ", ".join(set(log_data["vite_perse"]))
                st.markdown(f"""<div class="pro-report-box">📉 <b>Persone che hanno perso una vita in questo Turno ({st.session_state.round_number}):</b> {nomi_vite}</div>""", unsafe_allow_html=True)
            if log_data["eliminati"]:
                nomi_elim = ", ".join(set(log_data["eliminati"]))
                st.markdown(f"""<div class="pro-eliminated-box">💀 <b>GIOCATORI ELIMINATI DEFINITIVAMENTE NEL TURNO {st.session_state.round_number}:</b> {nomi_elim}</div>""", unsafe_allow_html=True)

        if partite_in_coda and not is_personale:
            st.markdown("### 📢 PROSSIMI IN CODA:")
            for q_idx, q_match in enumerate(partite_in_coda):
                qa, qp = q_match["teamA"]
                qb, qpp = q_match["teamB"]
                st.markdown(f"""
                    <div class="pro-queue-card">
                        <div class="match-header-row">
                            <span class="biliardino-title" style="color: #34d399;">⏳ IN CODA</span>
                            <span class="turno-badge" style="border-color: #34d399; color: #34d399;">TURNO {st.session_state.round_number}</span>
                        </div>
                        <div class="match-teams-row" style="background: #06120e;">
                            <div class="team-box">🥅 {qp['name'].upper()} / ⚽️ {qa['name'].upper()}</div>
                            <div class="vs-badge" style="color: #34d399;">VS</div>
                            <div class="team-box">🥅 {qpp['name'].upper()} / ⚽️ {qb['name'].upper()}</div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
