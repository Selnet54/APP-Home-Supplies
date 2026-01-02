import streamlit as st
import os

# --- KONFIGURACIJA ---
st.set_page_config(page_title="Zalihe", layout="centered")

# --- CSS ZA STROGO FIKSIRANJE (MOBILNI PORTRET) ---
st.markdown("""
    <style>
    /* 1. Podizanje na sam vrh */
    .block-container {
        padding-top: 0px !important;
        max-width: 360px !important; 
        margin: auto;
    }

    /* 2. UKLANJANJE KOLONA - Pravimo fiksni horizontalni kontejner */
    .custom-header {
        display: flex;
        flex-direction: row;
        flex-wrap: nowrap;
        justify-content: space-between;
        align-items: center;
        width: 100%;
        padding: 5px 0;
    }

    /* 3. Stil za linkove/dugmadi u hederu */
    .header-item {
        font-weight: bold;
        font-size: 11px;
        text-decoration: none;
        color: black;
        white-space: nowrap;
        cursor: pointer;
    }

    /* SPECIFIČNO POMERANJE KATEGORIJE UDESNO */
    .kat-item {
        margin-left: 15px !important; /* Pomereno za oko 2 karaktera udesno */
    }

    .exit-item { color: red !important; }

    /* 4. Zastava i tekst u istom redu */
    .flag-info {
        display: flex;
        align-items: center;
        gap: 8px;
        margin-top: 2px;
        border-top: 1px solid #ddd;
        padding-top: 5px;
    }
    .flag-info img { width: 25px; height: auto; }
    .flag-info span { font-weight: bold; font-size: 13px; }

    /* Centriranje jezika u gridu */
    .stImage > img { margin: 0 auto; display: block; }
    </style>
    """, unsafe_allow_html=True)

# --- INICIJALIZACIJA ---
if 'korak' not in st.session_state: st.session_state.korak = "jezik"

# --- PODACI ---
jezici_lista = [
    ("Srpski", "Srpski"), ("Engleski", "English"), ("Nemacki", "Deutsch"),
    ("Ruski", "Русский"), ("Ukrajinski", "Ukrajinski"), ("Madjarski", "Magyar"),
    ("Spanski", "Espanol"), ("Portugalski", "Portugues"), ("Mandarinski", "中文"),
    ("Francuski", "Francais")
]

# --- FUNKCIJA ZA RUČNI HEDER ---
def prikazi_heder_rucno():
    # Pošto Streamlit dugmad uvek prave nove redove u HTML-u, 
    # koristimo 5 veoma uskih kolona ali sa fiksiranim marginama
    c1, c2, c3, c4, c5 = st.columns([0.8, 1.4, 1, 1, 0.8])
    
    with c1: 
        if st.button("Home", key="h_home"): st.session_state.korak = "home"
    with c2: 
        # DODATA MARGINA U CSS-u iznad pomera ovo dugme
        if st.button("Kategorija", key="h_kat"): st.session_state.korak = "kategorije"
    with c3: 
        if st.button("Zalihe", key="h_zal"): st.session_state.korak = "spisak"
    with c4: 
        if st.button("Spisak", key="h_spis"): st.session_state.korak = "potrebe"
    with c5: 
        if st.button("Izlaz", key="h_izl"):
            st.session_state.korak = "jezik"
            st.rerun()

    # Zastava i tekst (Ispravljen prikaz u istom redu)
    if 'izabrani_jezik_kod' in st.session_state:
        kod = st.session_state.izabrani_jezik_kod
        naziv = st.session_state.izabrani_jezik_naziv
        path = f"icons/{kod}.png"
        
        # Koristimo kolone za zastavu i tekst da osiguramo jedan red
        f_col1, f_col2 = st.columns([1, 6])
        with f_col1:
            if os.path.exists(path): st.image(path, width=25)
        with f_col2:
            st.markdown(f"<div style='line-height:25px; font-weight:bold;'>{naziv}</div>", unsafe_allow_html=True)
    
    st.markdown("<hr style='margin:0'>", unsafe_allow_html=True)

# --- EKRANI ---
prikazi_heder_rucno()

if st.session_state.korak == "jezik":
    for i in range(0, len(jezici_lista), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(jezici_lista):
                fajl, ime = jezici_lista[i + j]
                with cols[j]:
                    path = f"icons/{fajl}.png"
                    if os.path.exists(path): st.image(path, width=35)
                    if st.button(ime, key=f"L_{fajl}"):
                        st.session_state.izabrani_jezik_kod = fajl
                        st.session_state.izabrani_jezik_naziv = ime
                        st.session_state.korak = "kategorije"
                        st.rerun()

elif st.session_state.korak == "kategorije":
    st.subheader("Kategorije")
    # Tvoj dalji kod...
