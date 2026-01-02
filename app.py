import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os

# --- KONFIGURACIJA ---
st.set_page_config(page_title="Zalihe", layout="centered")

# --- NAPREDNI CSS ZA MOBILNI HORIZONTALNI RASPODRED ---
st.markdown("""
    <style>
    /* Smanjenje margina celog ekrana */
    .block-container { padding: 10px 5px !important; }
    
    /* Heder: Sve u jedan red, fiksno */
    .nav-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid #ddd;
        padding-bottom: 5px;
        margin-bottom: 10px;
    }

    /* SILA HORIZONTALNOG RASPODREDA ZA MOBILNI (3 kolone) */
    [data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        align-items: flex-start !important;
        gap: 5px !important;
    }
    
    [data-testid="column"] {
        flex: 1 1 0% !important;
        min-width: 0 !important;
    }

    /* Dugmad: bez okvira, tekstualna */
    div.stButton > button {
        border: none !important;
        background: none !important;
        padding: 2px !important;
        font-weight: bold !important;
        font-size: 14px !important;
        width: 100% !important;
    }
    
    /* Crveni Izlaz */
    .exit-btn button { color: red !important; }
    
    /* Centriranje slika zastava */
    .stImage > img { margin: 0 auto; display: block; }
    </style>
    """, unsafe_allow_html=True)

# --- INICIJALIZACIJA ---
if 'korak' not in st.session_state: st.session_state.korak = "jezik"
if 'izbor' not in st.session_state: st.session_state.izbor = {}

# --- PODACI ---
jezici = ["Srpski", "Engleski", "Nemacki", "Francuski", "Ruski", "Ukrajinski", "Madjarski", "Spanski", "Portugalski", "Mandarinski"]
# Ovde ubaci ostatak rečnika iz tvog fajla
podaci_sr = {
    "Belo meso": ["Pileći batak", "Pileći karabatak", "Pileća krila", "Pileće grudi"],
    "Crveno meso": ["Svinjski but", "Svinjski vrat", "Svinjska krmenadla"],
    "Divljač": ["Zec", "Srna", "Fazan"]
}

# --- FUNKCIJA ZA HEDER I ZASTAVU ---
def prikazi_zaglavlje():
    # Heder red
    c1, c2, c3, c4, c5 = st.columns([1, 1, 1.2, 1.2, 0.8])
    with c1: 
        if st.button("Home"): st.session_state.korak = "home"
    with c2:
        if st.button("Kat."): st.session_state.korak = "kategorije"
    with c3:
        if st.button("Zalihe"): st.session_state.korak = "spisak"
    with c4:
        if st.button("Potrebe"): st.session_state.korak = "potrebe"
    with c5:
        if st.button("Izlaz", key="ex"): 
            st.session_state.korak = "jezik"
            st.rerun()
    
    # Zastava izabranog jezika ispod hedera
    izabrani = st.session_state.get('izabrani_jezik', 'Srpski')
    if os.path.exists(f"icons/{izabrani}.png"):
        st.image(f"icons/{izabrani}.png", width=40)
    st.markdown("<hr style='margin:2px 0'>", unsafe_allow_html=True)

# --- LOGIKA EKRANA ---

# 1. EKRAN: JEZICI (Grid 3 kolone)
if st.session_state.korak == "jezik":
    for i in range(0, len(jezici), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(jezici):
                lang = jezici[i + j]
                with cols[j]:
                    if os.path.exists(f"icons/{lang}.png"):
                        st.image(f"icons/{lang}.png", width=40)
                    if st.button(lang, key=f"L_{lang}"):
                        st.session_state.izabrani_jezik = lang
                        st.session_state.korak = "kategorije"
                        st.rerun()

# 2. EKRAN: KATEGORIJE (Grid 3 kolone)
elif st.session_state.korak == "kategorije":
    prikazi_zaglavlje()
    kategorije = list(podaci_sr.keys())
    for i in range(0, len(kategorije), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(kategorije):
                kat = kategorije[i + j]
                with cols[j]:
                    # Ovde možeš staviti ikonice za meso, higijenu itd.
                    if st.button(kat, key=f"K_{kat}"):
                        st.session_state.izbor['kat'] = kat
                        st.session_state.korak = "podkat"
                        st.rerun()

# 3. EKRAN: PODKATEGORIJE
elif st.session_state.korak == "podkat":
    prikazi_zaglavlje()
    stavke = podaci_sr[st.session_state.izbor['kat']]
    for i in range(0, len(stavke), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(stavke):
                s = stavke[i + j]
                with cols[j]:
                    if st.button(s, key=f"S_{s}"):
                        st.session_state.izbor['deo'] = s
                        st.session_state.korak = "unos"
                        st.rerun()

# 4. EKRAN: UNOS
elif st.session_state.korak == "unos":
    prikazi_zaglavlje()
    st.write(f"**{st.session_state.izbor['deo']}**")
    
    with st.form("form_u"):
        c1, c2 = st.columns(2)
        kom = c1.number_input("Kom:", min_value=1, step=1)
        kol = c2.number_input("Kol:")
        jed = c2.selectbox("", ["g", "kg", "lit", "kom"], label_visibility="collapsed")
        
        dat = st.date_input("Unos:", datetime.now())
        rok = st.number_input("Meseci:", min_value=1, value=6)
        
        if st.form_submit_button("SAČUVAJ"):
            st.success("Dodato!")
            st.session_state.korak = "kategorije"
