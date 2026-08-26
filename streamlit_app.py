        for idx, match in partite_in_corso:
            tA_att, tA_port = match["teamA"]
            tB_att, tB_port = match["teamB"]
            nomi_match = [tA_att['name'].lower(), tA_port['name'].lower(), tB_att['name'].lower(), tB_port['name'].lower()]
            
            if is_personale and target_user not in nomi_match:
                continue

            biliardino_num = idx + 1
            
            st.markdown(f"""
                <div class="pro-match-card">
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
            
            c1, c2 = st.columns(2)
            with c1:
                if st.button("⚡ VITTORIA SQUADRA A", key=f"wa_{st.session_state.round_number}_{idx}", use_container_width=True):
                    salva_snapshot()
                    for v in [tA_att, tA_port]: v["last_result"] = 'W'
                    for per in [tB_att, tB_port]:
                        per["last_result"] = 'L'
                        per["lives"] = max(0, per["lives"] - 1)
                        if per["lives"] == 0: per["eliminated"] = True
                    st.session_state.current_round_matches["partite"].pop(idx)
                    if not st.session_state.current_round_matches["partite"]:
                        st.session_state.round_number += 1
                        st.session_state.current_round_matches = genera_abbinamenti()
                    salva_stato()
                    st.rerun()
            with c2:
                if st.button("⚡ VITTORIA SQUADRA B", key=f"wb_{st.session_state.round_number}_{idx}", use_container_width=True):
                    salva_snapshot()
                    for v in [tB_att, tB_port]: v["last_result"] = 'W'
                    for per in [tA_att, tA_port]:
                        per["last_result"] = 'L'
                        per["lives"] = max(0, per["lives"] - 1)
                        if per["lives"] == 0: per["eliminated"] = True
                    st.session_state.current_round_matches["partite"].pop(idx)
                    if not st.session_state.current_round_matches["partite"]:
                        st.session_state.round_number += 1
                        st.session_state.current_round_matches = genera_abbinamenti()
                    salva_stato()
                    st.rerun()
