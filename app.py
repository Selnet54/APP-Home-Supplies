import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os

# --- KONFIGURACIJA ---
st.set_page_config(page_title="Zalihe", layout="centered")

# --- CSS ZA FIKSNI HEDER I ZBIJANJE ---
st.markdown("""
    <style>
    /* Smanjenje širine sadržaja da kolone budu bliže (oko 2cm razmaka) */
    .block-container {
        max-width: 450px !important;
        padding-top: 20px !important;
    }
    
    /* Heder: fiksiran, bez okvira, jedan red */
    .fixed-header {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        background-color: white;
        z-index: 999;
        border-bottom: 1px solid #ddd;
        padding: 10px 0;
        display: flex;
        justify-content: center;
        gap: 5px;
    }

    /* Stil za dugmad u hederu (tekstualni) */
    div.stButton > button {
        border: none !important;
        background: none !important;
        padding: 0px 5px !important;
        font-weight: bold !important;
        font-size: 14px !important;
    }
    
    /* Crveni Izlaz */
    div.stButton > button:contains("Izlaz") { color: red !important; }

    /* Centriranje zastave ispod hedera */
    .flag-sub-header {
        text-align: center;
        margin-top: 50px; /* Da ne bi bilo ispod fiksnog hedera */
        margin-bottom: 10px;
    }

    /* Poravnanje teksta i slike u gridu */
    [data-testid="column"] {
        text-align: center !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- INICIJALIZACIJA ---
if 'korak' not in st.session_state: st.session_state.korak = "jezik"
if 'izbor' not in st.session_state: st.session_state.izbor = {}

# --- PODACI (Hijerarhija iz tvog fajla) ---
jezici_lista = [
    ("Srpski", "Srpski"), ("Engleski", "English"), ("Nemacki", "Deutsch"),
    ("Ruski", "Русский"), ("Ukrajinski", "Українська"), ("Madjarski", "Magyar"),
    ("Spanski", "Español"), ("Portugalski", "Português"), ("Mandarinski", "中文"),
    ("Francuski", "Français")
]

podaci = {
    "Belo meso": {
        "Piletina": ["Gril pile", "Batak", "Karabatak", "Belo meso", "Krila"],
        "Ćuretina": ["Ćureći file", "Ćureći batak"]
    },
    "Crveno meso": {
        "Svinjetina": ["Krmenadla", "Vrat", "But"],
        "Junetina": ["Biftek", "But"]
    }
}

# --- FUNKCIJA ZA HEDER ---
def prikazi_heder():
    # Pošto Streamlit ne podržava lako fiksne headere sa interaktivnim dugmićima, 
    # koristimo standardne kolone ali sa "zbijenim" CSS-om.
    c1, s1, c2, s2, c3, s3, c4, s4, c5 = st.columns([1, 0.1, 1, 0.1, 1.2, 0.1, 1.2, 0.1, 1])
    with c1: 
        if st.button("Home", key="nav_home"): st.session_state.korak = "home"
    s1.write("|")
    with c2: 
        if st.button("Kat.", key="nav_kat"): st.session_state.korak = "kategorije"
    s2.write("|")
    with c3: 
        if st.button("Zalihe", key="nav_zal"): st.session_state.korak = "spisak"
    s3.write("|")
    with c4: 
        if st.button("Potrebe", key="nav_pot"): st.session_state.korak = "potrebe"
    s4.write("|")
    with c5: 
        if st.button("Izlaz", key="nav_ex"): 
            st.session_state.korak = "jezik"
            st.rerun()
    
    # Zastava odmah ispod
    jezik = st.session_state.get('izabrani_jezik_kod', 'Srpski')
    st.markdown('<div class="flag-sub-header">', unsafe_allow_html=True)
    if os.path.exists(f"icons/{jezik}.png"):
        st.image(f"icons/{jezik}.png", width=40)
    st.markdown('</div><hr style="margin:0">', unsafe_allow_html=True)

# --- EKRAN 1: JEZICI (3 kolone x 4 reda) ---
if st.session_state.korak == "jezik":
    st.write("") # Razmak od vrha
    for i in range(0, len(jezici_lista), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(jezici_lista):
                ime_fajla, naziv_ekran = jezici_lista[i + j]
                with cols[j]:
                    if os.path.exists(f"icons/{ime_fajla}.png"):
                        st.image(f"icons/{ime_fajla}.png", width=45)
                    if st.button(naziv_ekran, key=f"lang_{ime_fajla}"):
                        st.session_state.izabrani_jezik_kod = ime_fajla
                        st.session_state.korak = "kategorije"
                        st.rerun()

# --- EKRAN 2: KATEGORIJE ---
elif st.session_state.korak == "kategorije":
    prikazi_heder()
    kategorije = list(podaci.keys())
    for i in range(0, len(kategorije), 3):
        cols = st.columns(3)
        for j in range(3):
            if i+j < len(kategorije):
                kat = kategorije[i+j]
                with cols[j]:
                    if st.button(kat, key=f"k_{kat}"):
                        st.session_state.izbor['kat'] = kat
                        st.session_state.korak = "podkategorije"
                        st.rerun()

# --- EKRAN 3: PODKATEGORIJE ---
elif st.session_state.korak == "podkategorije":
    prikazi_heder()
    podkat_lista = list(podaci[st.session_state.izbor['kat']].keys())
    for i in range(0, len(podkat_lista), 3):
        cols = st.columns(3)
        for j in range(3):
            if i+j < len(podkat_lista):
                pk = podkat_lista[i+j]
                with cols[j]:
                    if st.button(pk, key=f"pk_{pk}"):
                        st.session_state.izbor['podkat'] = pk
                        st.session_state.korak = "delovi"
                        st.rerun()

# --- EKRAN 4: DELOVI ---
elif st.session_state.korak == "delovi":
    prikazi_heder()
    delovi = podaci[st.session_state.izbor['kat']][st.session_state.izbor['podkat']]
    for i in range(0, len(delovi), 3):
        cols = st.columns(3)
        for j in range(3):
            if i+j < len(delovi):
                d = delovi[i+j]
                with cols[j]:
                    if st.button(d, key=f"d_{d}"):
                        st.session_state.izbor['deo'] = d
                        st.session_state.korak = "unos"
                        st.rerun()

# --- EKRAN 5: UNOS ---
elif st.session_state.korak == "unos":
    prikazi_heder()
    st.write(f"**{st.session_state.izbor['deo']}**")
    with st.form("f_unos"):
        c1, c2 = st.columns(2)
        kom = c1.number_input("Komada:", min_value=1, step=1)
        kol = c2.number_input("Težina/Količina:")
        jed = c2.selectbox("", ["g", "kg", "lit"], label_visibility="collapsed")
        rok = st.number_input("Rok (meseci):", value=6)
        if st.form_submit_button("SAČUVAJ"):
            st.success("Dodato!")
            st.session_state.korak = "kategorije"
