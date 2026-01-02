import streamlit as st
import os
from datetime import datetime, timedelta

# --- KONFIGURACIJA ---
st.set_page_config(page_title="Zalihe", layout="centered")

# --- CSS ZA RUČNO POZICIONIRANJE DUGMADI ---
st.markdown("""
    <style>
    /* Maksimalno podizanje i sužavanje */
    .block-container {
        padding-top: 0px !important;
        margin-top: -20px !important;
        max-width: 350px !important; 
        margin: auto;
    }

    /* Forsiranje horizontala */
    [data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        gap: 0px !important;
    }

    /* Stil svih dugmadi u hederu */
    div.stButton > button {
        border: none !important;
        background: none !important;
        padding: 0px !important;
        font-weight: bold !important;
        font-size: 11px !important;
        color: black !important;
        white-space: nowrap !important;
    }

    /* PRECIZNO POMERANJE SVAKOG DUGMETA POJEDINAČNO */
    
    /* Home ostaje levo */
    div.stButton > button[key="h_home"] {
        text-align: left !important;
    }

    /* KATEGORIJA - Pomeranje ulevo (negativna margina) */
    div.stButton > button[key="h_kat"] {
        margin-left: -40px !important; 
    }

    /* ZALIHE - Pomeranje udesno (pozitivna margina) da se odlepi od Kategorije */
    div.stButton > button[key="h_zal"] {
        margin-left: 20px !important;
    }

    /* SPISAK - Malo udesno */
    div.stButton > button[key="h_spis"] {
        margin-left: 15px !important;
    }

    /* IZLAZ - Skroz desno */
    div.stButton > button[key="h_izl"] {
        color: red !important;
        text-align: right !important;
    }

    /* Red za zastavu i tekst */
    .flag-container-row {
        display: flex;
        align-items: center;
        justify-content: flex-start;
        gap: 8px;
        margin: 0px 0px 5px 5px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- INICIJALIZACIJA ---
if 'korak' not in st.session_state: st.session_state.korak = "jezik"
if 'izbor' not in st.session_state: st.session_state.izbor = {}

# --- FUNKCIJA ZA HEDER ---
def prikazi_heder():
    # Definišemo kolone
    c1, c2, c3, c4, c5 = st.columns([0.7, 1.5, 1, 1, 0.7])
    
    with c1: st.button("Home", key="h_home")
    with c2: st.button("Kategorija", key="h_kat")
    with c3: st.button("Zalihe", key="h_zal")
    with c4: st.button("Spisak", key="h_spis")
    with c5: 
        if st.button("Izlaz", key="h_izl"):
            st.session_state.korak = "jezik"
            st.rerun()
    
    # Zastava i tekst (Zbijeno u jedan red bez kolona)
    if 'izabrani_jezik_kod' in st.session_state:
        kod = st.session_state.izabrani_jezik_kod
        naziv = st.session_state.izabrani_jezik_naziv
        path = f"icons/{kod}.png"
        if os.path.exists(path):
            # Koristimo HTML za fiksni red zastave i teksta
            st.markdown(f"""
                <div class="flag-container-row">
                    <img src="https://raw.githubusercontent.com/tvoj-user/tvoj-repo/main/icons/{kod}.png" width="25" style="vertical-align: middle;">
                    <span style="font-weight:bold; font-size:14px; vertical-align: middle;">{naziv}</span>
                </div>
            """, unsafe_allow_html=True)
            # Ako gornji link ne radi (jer je lokalan), koristi običan Streamlit red:
            # col_a, col_b = st.columns([1, 8])
            # with col_a: st.image(path, width=25)
            # with col_b: st.markdown(f"**{naziv}**")
            
    st.markdown("<hr style='margin:2px 0'>", unsafe_allow_html=True)

# --- LOGIKA EKRANA ---
prikazi_heder()

# (Ovde ide ostatak tvog koda za izbor jezika, kategorija itd.)
if st.session_state.korak == "jezik":
    jezici_lista = [("Srpski", "Srpski"), ("Engleski", "English"), ("Nemacki", "Deutsch"), ("Francuski", "Français")] # primer
    for i in range(0, len(jezici_lista), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(jezici_lista):
                fajl, ime = jezici_lista[i + j]
                with cols[j]:
                    if st.button(ime, key=f"L_{fajl}"):
                        st.session_state.izabrani_jezik_kod = fajl
                        st.session_state.izabrani_jezik_naziv = ime
                        st.session_state.korak = "kategorije"
                        st.rerun()
