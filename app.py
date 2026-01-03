def stranica_jezik():
    """Stranica za odabir jezika - vertikalno poravnano slike iznad teksta"""
    
    # CSS za vertikalno poravnanje i manje zastave
    st.markdown("""
        <style>
        /* STILOVI ZA STRANICU JEZIKA */
        .language-column {
            display: flex !important;
            flex-direction: column !important;
            align-items: center !important;
            justify-content: flex-start !important;
            margin: 0 2px !important;
            padding: 8px 2px !important;
        }
        
        .language-image-container {
            display: flex !important;
            justify-content: center !important;
            align-items: center !important;
            height: 60px !important;
            margin-bottom: 8px !important;
            width: 100% !important;
        }
        
        .language-image {
            max-width: 50px !important;
            max-height: 35px !important;
            object-fit: contain !important;
        }
        
        .language-button {
            width: 100% !important;
            text-align: center !important;
            margin-top: 0 !important;
            font-size: 12px !important;
            padding: 5px 2px !important;
            height: auto !important;
            min-height: 35px !important;
        }
        
        /* Povećaj razmak između redova */
        .stHorizontalBlock {
            margin-bottom: 10px !important;
        }
        
        /* Smanji padding unutar kolona */
        div[data-testid="column"] {
            padding: 0 2px !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Naslov
    st.markdown("<h3 style='text-align: center; margin-bottom: 20px;'>🌍 Izaberite jezik / Choose language</h3>", unsafe_allow_html=True)
    
    # PRVI RED (3 jezika)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="language-column">', unsafe_allow_html=True)
        st.markdown('<div class="language-image-container">', unsafe_allow_html=True)
        st.image("icons/Srpski.png", width=45, use_column_width='auto')
        st.markdown('</div>', unsafe_allow_html=True)
        if st.button("Srpski", key="jezik_srpski", use_container_width=True):
            st.session_state.izabrani_jezik_kod = "Srpski"
            st.session_state.izabrani_jezik_naziv = "Srpski"
            st.session_state.jezik_kljuc = "srpski"
            st.session_state.korak = "kategorije"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="language-column">', unsafe_allow_html=True)
        st.markdown('<div class="language-image-container">', unsafe_allow_html=True)
        st.image("icons/Engleski.png", width=45, use_column_width='auto')
        st.markdown('</div>', unsafe_allow_html=True)
        if st.button("English", key="jezik_english", use_container_width=True):
            st.session_state.izabrani_jezik_kod = "Engleski"
            st.session_state.izabrani_jezik_naziv = "English"
            st.session_state.jezik_kljuc = "english"
            st.session_state.korak = "kategorije"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="language-column">', unsafe_allow_html=True)
        st.markdown('<div class="language-image-container">', unsafe_allow_html=True)
        st.image("icons/Nemacki.png", width=45, use_column_width='auto')
        st.markdown('</div>', unsafe_allow_html=True)
        if st.button("Deutsch", key="jezik_deutsch", use_container_width=True):
            st.session_state.izabrani_jezik_kod = "Nemacki"
            st.session_state.izabrani_jezik_naziv = "Deutsch"
            st.session_state.jezik_kljuc = "deutsch"
            st.session_state.korak = "kategorije"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    # DRUGI RED (3 jezika)
    col4, col5, col6 = st.columns(3)
    
    with col4:
        st.markdown('<div class="language-column">', unsafe_allow_html=True)
        st.markdown('<div class="language-image-container">', unsafe_allow_html=True)
        st.image("icons/Ruski.png", width=45, use_column_width='auto')
        st.markdown('</div>', unsafe_allow_html=True)
        if st.button("Русский", key="jezik_ruski", use_container_width=True):
            st.session_state.izabrani_jezik_kod = "Ruski"
            st.session_state.izabrani_jezik_naziv = "Русский"
            st.session_state.jezik_kljuc = "ruski"
            st.session_state.korak = "kategorije"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col5:
        st.markdown('<div class="language-column">', unsafe_allow_html=True)
        st.markdown('<div class="language-image-container">', unsafe_allow_html=True)
        st.image("icons/Ukrajinski.png", width=45, use_column_width='auto')
        st.markdown('</div>', unsafe_allow_html=True)
        if st.button("Українська", key="jezik_ukrajinski", use_container_width=True):
            st.session_state.izabrani_jezik_kod = "Ukrajinski"
            st.session_state.izabrani_jezik_naziv = "Українська"
            st.session_state.jezik_kljuc = "ukrajinski"
            st.session_state.korak = "kategorije"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col6:
        st.markdown('<div class="language-column">', unsafe_allow_html=True)
        st.markdown('<div class="language-image-container">', unsafe_allow_html=True)
        st.image("icons/Madjarski.png", width=45, use_column_width='auto')
        st.markdown('</div>', unsafe_allow_html=True)
        if st.button("Magyar", key="jezik_magyar", use_container_width=True):
            st.session_state.izabrani_jezik_kod = "Madjarski"
            st.session_state.izabrani_jezik_naziv = "Magyar"
            st.session_state.jezik_kljuc = "hungary"
            st.session_state.korak = "kategorije"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    # TREĆI RED (3 jezika)
    col7, col8, col9 = st.columns(3)
    
    with col7:
        st.markdown('<div class="language-column">', unsafe_allow_html=True)
        st.markdown('<div class="language-image-container">', unsafe_allow_html=True)
        st.image("icons/Spanski.png", width=45, use_column_width='auto')
        st.markdown('</div>', unsafe_allow_html=True)
        if st.button("Español", key="jezik_espanol", use_container_width=True):
            st.session_state.izabrani_jezik_kod = "Spanski"
            st.session_state.izabrani_jezik_naziv = "Español"
            st.session_state.jezik_kljuc = "espanol"
            st.session_state.korak = "kategorije"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col8:
        st.markdown('<div class="language-column">', unsafe_allow_html=True)
        st.markdown('<div class="language-image-container">', unsafe_allow_html=True)
        st.image("icons/Portugalski.png", width=45, use_column_width='auto')
        st.markdown('</div>', unsafe_allow_html=True)
        if st.button("Português", key="jezik_portugalski", use_container_width=True):
            st.session_state.izabrani_jezik_kod = "Portugalski"
            st.session_state.izabrani_jezik_naziv = "Português"
            st.session_state.jezik_kljuc = "portugalski"
            st.session_state.korak = "kategorije"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col9:
        st.markdown('<div class="language-column">', unsafe_allow_html=True)
        st.markdown('<div class="language-image-container">', unsafe_allow_html=True)
        st.image("icons/Mandarinski.png", width=45, use_column_width='auto')
        st.markdown('</div>', unsafe_allow_html=True)
        if st.button("中文", key="jezik_mandarinski", use_container_width=True):
            st.session_state.izabrani_jezik_kod = "Mandarinski"
            st.session_state.izabrani_jezik_naziv = "中文"
            st.session_state.jezik_kljuc = "mandarinski"
            st.session_state.korak = "kategorije"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    # ČETVRTI RED (samo francuski centriran)
    col10, col11, col12 = st.columns([1, 1, 1])
    
    with col11:
        st.markdown('<div class="language-column">', unsafe_allow_html=True)
        st.markdown('<div class="language-image-container">', unsafe_allow_html=True)
        st.image("icons/Francuski.png", width=45, use_column_width='auto')
        st.markdown('</div>', unsafe_allow_html=True)
        if st.button("Français", key="jezik_francais", use_container_width=True):
            st.session_state.izabrani_jezik_kod = "Francuski"
            st.session_state.izabrani_jezik_naziv = "Français"
            st.session_state.jezik_kljuc = "francais"
            st.session_state.korak = "kategorije"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
