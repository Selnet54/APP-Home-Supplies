import streamlit as st
import os
from datetime import datetime, timedelta

# --- KONFIGURACIJA ---
st.set_page_config(page_title="Zalihe", layout="centered")

# --- CSS ZA FIKSIRANJE POLOŽAJA ---
st.markdown("""
    <style>
    /* Podizanje svega na vrh */
    .block-container {
        padding-top: 0px !important;
        max-width: 350px !important; 
        margin: auto;
    }

    /* Forsiranje horizontala za mobilni */
    [data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        justify-content: center !important;
        gap: 0px !important;
    }

    /* Stil dugmadi u hederu */
    div.stButton > button {
        border: none !important;
        background: none !important;
        padding: 0px !important;
        font-weight: bold !important;
        font-size: 11px !important;
        color: black !important;
        white-space: nowrap !important;
    }

    div.stButton > button:contains("Izlaz") { color: red !important; }

    /* Centriranje slika u gridu */
    .stImage > img { margin: 0 auto; display: block; }
    
    /* Smanjenje razmaka kod linije */
    hr { margin: 2px 0 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- INICIJALIZACIJA ---
if 'korak' not in st.session_state: st.session_state.korak = "jezik"
if 'izbor' not in st.session_state: st.session_state.izbor = {}

# --- PODACI (Skraćena lista za test) ---
jezici_lista = [
    ("Srpski", "Srpski"), ("Engleski", "English"), ("Nemacki", "Deutsch"),
    ("Ruski", "Русский"), ("Ukrajinski", "Ukrainska"), ("Madjarski", "Magyar"),
    ("Spanski", "Espanol"), ("Portugalski", "Portugues"), ("Mandarinski", "中文"),
    ("Francuski", "Francais")
]

# --- FUNKCIJA ZA HEDER ---
def prikazi_heder():
    # Podešavamo širine kolona: 
    # Kolona 2 (Kategorija) je namerno široka, a kolona 1 (Home) uska da pogura Kategoriju ulevo
    c1, c2, c3, c4, c5 = st.columns([0.6, 1.4, 0.9, 0.9, 0.7])
    
    with c1: st.button("Home", key="h_home")
    with c2: st.button("Kategorija", key="h_kat")
    with c3: st.button("Zalihe", key="h_zal")
    with c4: st.button("Spisak", key="h_spis")
    with c5: 
        if st.button("Izlaz", key="h_izl"):
            st.session_state.korak = "jezik"
            st.rerun()
    
    # ZASTAVA I TEKST U ISTOM REDU (Siguran metod)
    if 'izabrani_jezik_kod' in st.session_state:
        kod = st.session_state.izabrani_jezik_kod
        naziv = st.session_state.izabrani_jezik_naziv
        path = f"icons/{kod}.png"
        
        # Pravimo 2 kolone samo za zastavu i tekst
        f_col1, f_col2 = st.columns([1, 5])
        with f_col1:
            if os.path.exists(path):
                st.image(path, width=25)
        with f_col2:
            st.markdown(f"**{naziv}**")
            
    st.markdown("<hr>", unsafe_allow_html=True)

# --- LOGIKA EKRANA ---
prikazi_heder()

if st.session_state.korak == "jezik":
    # 3 kolone po redu
    for i in range(0, len(jezici_lista), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(jezici_lista):
                fajl, ime = jezici_lista[i + j]
                with cols[j]:
                    path = f"icons/{fajl}.png"
                    if os.path.exists(path):
                        st.image(path, width=35)
                    # Tekst ispod zastave
                    if st.button(ime, key=f"L_{fajl}"):
                        st.session_state.izabrani_jezik_kod = fajl
                        st.session_state.izabrani_jezik_naziv = ime
                        st.session_state.korak = "kategorije"
                        st.rerun()

elif st.session_state.korak == "kategorije":
    st.write("Izaberite kategoriju:")
    # Ovde dodaj svoje kategorije (Belo meso itd.)
    if st.button("Belo meso"):
        st.session_state.korak = "podkategorije"
        st.rerun()
