import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os

# --- KONFIGURACIJA ---
st.set_page_config(page_title="Zalihe", layout="centered")

# --- CSS ZA ZBIJANJE I HEDER ---
st.markdown("""
    <style>
    /* Smanjenje širine stranice da kolone budu bliže sredini */
    .block-container {
        max-width: 500px !important;
        padding-top: 5px !important;
    }
    
    /* Heder: Jedan red, bez okvira, fiksiran na vrhu */
    .nav-bar {
        display: flex;
        justify-content: space-around;
        align-items: center;
        border-bottom: 1px solid #ddd;
        padding-bottom: 5px;
        margin-bottom: 5px;
    }
    
    /* Dugmad u hederu */
    div.stButton > button {
        border: none !important;
        background: none !important;
        padding: 0px 5px !important;
        font-weight: bold !important;
        font-size: 14px !important;
        color: black !important;
    }
    
    /* Razmak između kolona (oko 2cm na ekranu) */
    [data-testid="stHorizontalBlock"] {
        gap: 30px !important; 
        justify-content: center !important;
    }

    /* Crveni izlaz */
    div.stButton > button:contains("Izlaz") { color: red !important; }

    /* Centriranje zastave */
    .flag-container { text-align: center; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- INICIJALIZACIJA ---
if 'korak' not in st.session_state: st.session_state.korak = "jezik"
if 'izbor' not in st.session_state: st.session_state.izbor = {}

# --- TVOJI PODACI (Primjer hijerarhije) ---
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

# --- FUNKCIJA ZA HEDER I ZASTAVU ---
def zaglavlje():
    # Heder u jednom redu (bez okvira)
    c1, s1, c2, s2, c3, s3, c4, s4, c5 = st.columns([1, 0.1, 1, 0.1, 1.2, 0.1, 1.2, 0.1, 1])
    with c1: 
        if st.button("Home"): st.session_state.korak = "home"
    s1.write("|")
    with c2: 
        if st.button("Kat."): st.session_state.korak = "kategorije"
    s2.write("|")
    with c3: 
        if st.button("Zalihe"): st.session_state.korak = "spisak"
    s3.write("|")
    with c4: 
        if st.button("Potrebe"): st.session_state.korak = "potrebe"
    s4.write("|")
    with c5: 
        if st.button("Izlaz"): 
            st.session_state.korak = "jezik"
            st.rerun()
    
    # Zastava odmah ispod hedera
    jezik = st.session_state.get('izabrani_jezik', 'Srpski')
    st.markdown(f'<div class="flag-container">', unsafe_allow_html=True)
    if os.path.exists(f"icons/{jezik}.png"):
        st.image(f"icons/{jezik}.png", width=40)
    st.markdown('</div>', unsafe_allow_html=True)

# --- EKRANI ---

# 1. JEZIK (Grid 3 kolone)
if st.session_state.korak == "jezik":
    jezici = ["Srpski", "Engleski", "Nemacki", "Francuski", "Ruski", "Ukrajinski", "Madjarski", "Spanski", "Portugalski", "Mandarinski"]
    for i in range(0, len(jezici), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(jezici):
                l = jezici[i + j]
                with cols[j]:
                    if os.path.exists(f"icons/{l}.png"): st.image(f"icons/{l}.png", width=40)
                    if st.button(l, key=l):
                        st.session_state.izabrani_jezik = l
                        st.session_state.korak = "kategorije"
                        st.rerun()

# 2. KATEGORIJE (npr. Belo meso, Crveno meso)
elif st.session_state.korak == "kategorije":
    zaglavlje()
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

# 3. PODKATEGORIJE (npr. Piletina)
elif st.session_state.korak == "podkategorije":
    zaglavlje()
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

# 4. DIJELOVI PROIZVODA (npr. Gril pile, Batak...)
elif st.session_state.korak == "delovi":
    zaglavlje()
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

# 5. UNOS PODATAKA
elif st.session_state.korak == "unos":
    zaglavlje()
    st.write(f"**{st.session_state.izbor['deo']}**")
    with st.form("form"):
        c1, c2 = st.columns(2)
        kom = c1.number_input("Komada:", min_value=1, step=1)
        kol = c2.number_input("Težina/Količina:")
        jed = c2.selectbox("", ["g", "kg", "lit"], label_visibility="collapsed")
        rok = st.number_input("Rok trajanja (meseci):", value=6)
        if st.form_submit_button("SNIMI"):
            st.success("Dodano!")
            st.session_state.korak = "kategorije"
