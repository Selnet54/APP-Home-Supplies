import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os

# --- KONFIGURACIJA ---
st.set_page_config(page_title="Zalihe", layout="centered")

# --- STIL ZA MOBILNI (Zbijeno i bez okvira) ---
st.markdown("""
    <style>
    /* Heder u jednom redu bez okvira */
    .nav-col { text-align: center; font-size: 14px; font-weight: bold; }
    
    /* Dugmad kao čist tekst */
    div.stButton > button {
        border: none !important;
        background: none !important;
        padding: 5px 2px !important;
        color: black !important;
        font-weight: bold !important;
        width: auto !important;
    }
    
    /* Crveni Izlaz */
    div.stButton > button:contains("Izlaz") { color: red !important; }

    /* Mreža za kategorije i jezike (3 kolone) */
    [data-testid="column"] {
        padding: 0px 5px !important;
        text-align: center;
    }

    /* Slike u mrežama */
    .stImage { margin-bottom: -10px; }
    
    /* Smanjenje razmaka između elemenata */
    .block-container { padding-top: 10px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- INICIJALIZACIJA ---
if 'korak' not in st.session_state: st.session_state.korak = "jezik"
if 'izbor' not in st.session_state: st.session_state.izbor = {}

# --- PODACI (Tvoja struktura iz koda) ---
jezici = ["Srpski", "Engleski", "Nemacki", "Francuski", "Ruski", "Ukrajinski", "Madjarski", "Spanski", "Portugalski", "Mandarinski"]

podaci_sr = {
    "Belo meso": ["Pileći batak", "Pileći karabatak", "Pileća krila", "Pileće grudi"],
    "Crveno meso": ["Svinjski but", "Svinjski vrat", "Svinjska krmenadla"],
    "Sitna divljač": ["Zec", "Fazan"],
    "Krupna divljač": ["Srna", "Vepar"]
}

# --- FUNKCIJA ZA HEDER (Jedan red) ---
def prikazi_heder():
    c1, s1, c2, s2, c3, s3, c4, s4, c5 = st.columns([1, 0.1, 1, 0.1, 1.2, 0.1, 1.2, 0.1, 0.8])
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
    st.markdown("<hr style='margin:2px 0'>", unsafe_allow_html=True)

# --- EKRAN 1: JEZICI (4 reda po 3 jezika) ---
if st.session_state.korak == "jezik":
    cols = st.columns(3)
    for i, j in enumerate(jezici):
        with cols[i % 3]:
            # Prikaz zastave iz foldera
            if os.path.exists(f"icons/{j}.png"):
                st.image(f"icons/{j}.png", width=50)
            if st.button(j, key=f"L_{j}"):
                st.session_state.korak = "kategorije"
                st.rerun()

# --- EKRAN 2: KATEGORIJE (3 kolone) ---
elif st.session_state.korak == "kategorije":
    prikazi_heder()
    cols = st.columns(3)
    for i, kat in enumerate(podaci_sr.keys()):
        with cols[i % 3]:
            # Ovde bi išla ikonica za kategoriju ako je imaš
            if st.button(kat, key=f"K_{kat}"):
                st.session_state.izbor['kat'] = kat
                st.session_state.korak = "podkat"
                st.rerun()

# --- EKRAN 3: PODKATEGORIJE (3 kolone) ---
elif st.session_state.korak == "podkat":
    prikazi_heder()
    stavke = podaci_sr[st.session_state.izbor['kat']]
    cols = st.columns(3)
    for i, stavka in enumerate(stavke):
        with cols[i % 3]:
            if st.button(stavka, key=f"S_{stavka}"):
                st.session_state.izbor['deo'] = stavka
                st.session_state.korak = "unos"
                st.rerun()

# --- EKRAN 4: UNOS ---
elif st.session_state.korak == "unos":
    prikazi_heder()
    st.write(f"**{st.session_state.izbor['deo']}**")
    
    with st.container():
        c1, c2 = st.columns(2)
        kom = c1.number_input("Kom:", min_value=1, step=1)
        kol = c2.number_input("Kol:")
        jed = c2.selectbox("", ["g", "kg", "lit", "kom"], label_visibility="collapsed")
        
        dat = st.date_input("Unos:", datetime.now())
        rok = st.number_input("Meseci:", min_value=1, value=6)
        
        final_rok = dat + timedelta(days=rok*30.44)
        st.write(f"Ističe: {final_rok.strftime('%d.%m.%Y')}")
        
        if st.button("✅ UNESI"):
            st.success("Snimljeno!")
            st.session_state.korak = "kategorije"
