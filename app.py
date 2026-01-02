import streamlit as st
import pandas as pd
import os

# --- 1. PODEŠAVANJA ---
st.set_page_config(page_title="Zalihe Navigacija", layout="centered")

# CSS za kvadratnu dugmad (Temu stil)
st.markdown("""
    <style>
    .stButton > button {
        width: 100%;
        height: 80px;
        border-radius: 12px;
        font-size: 18px;
        background-color: #ffffff;
        border: 2px solid #f0f2f6;
        margin-bottom: 10px;
    }
    .stButton > button:hover {
        border-color: #ff4b4b;
        color: #ff4b4b;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. TVOJA STRUKTURA PODATAKA ---
# Dodaj ovde svoje stvarne delove proizvoda
podaci = {
    "Hrana": {
        "Mlečni proizvodi": ["Mleko", "Jogurt", "Sirevi"],
        "Meso": ["Sveže meso", "Suvomesnato", "Zamrznuto"]
    },
    "Higijena": {
        "Kućna hemija": ["Deterdženti", "Sapun", "Površine"],
        "Lična nega": ["Šamponi", "Paste za zube"]
    }
}

# --- 3. LOGIKA NAVIGACIJE (Session State) ---
if 'nivo' not in st.session_state:
    st.session_state.nivo = "kategorije"
if 'izabrana_kat' not in st.session_state:
    st.session_state.izabrana_kat = None
if 'izabrana_podkat' not in st.session_state:
    st.session_state.izabrana_podkat = None
if 'baza' not in st.session_state:
    st.session_state.baza = []

# --- 4. FUNKCIJE ZA NAVIGACIJU ---
def idi_na_podkat(kat):
    st.session_state.izabrana_kat = kat
    st.session_state.nivo = "podkategorije"

def idi_na_delove(podkat):
    st.session_state.izabrana_podkat = podkat
    st.session_state.nivo = "delovi"

def nazad():
    if st.session_state.nivo == "delovi":
        st.session_state.nivo = "podkategorije"
    elif st.session_state.nivo == "podkategorije":
        st.session_state.nivo = "kategorije"

# --- 5. EKRANI ---

# --- EKRAN 1: GLAVNE KATEGORIJE ---
if st.session_state.nivo == "kategorije":
    st.header("Izaberi kategoriju")
    cols = st.columns(2)
    for i, kat in enumerate(podaci.keys()):
        with cols[i % 2]:
            st.button(kat, on_click=idi_na_podkat, args=(kat,))

# --- EKRAN 2: PODKATEGORIJE ---
elif st.session_state.nivo == "podkategorije":
    st.button("⬅️ Nazad", on_click=nazad)
    st.header(f"📂 {st.session_state.izabrana_kat}")
    cols = st.columns(2)
    for i, podkat in enumerate(podaci[st.session_state.izabrana_kat].keys()):
        with cols[i % 2]:
            st.button(podkat, on_click=idi_na_delove, args=(podkat,))

# --- EKRAN 3: DELOVI PROIZVODA I UNOS ---
elif st.session_state.nivo == "delovi":
    st.button("⬅️ Nazad", on_click=nazad)
    st.header(f"📍 {st.session_state.izabrana_podkat}")
    
    # Dugmad za konkretne delove/grupe
    delovi = podaci[st.session_state.izabrana_kat][st.session_state.izabrana_podkat]
    izabrani_deo = st.radio("Izaberi deo proizvoda:", delovi)
    
    st.divider()
    
    # FORMA ZA UNOS
    with st.container():
        st.subheader("Unos u zalihe")
        naziv = st.text_input("Ime artikla:", value=izabrani_deo)
        kol = st.number_input("Količina:", min_value=1, step=1)
        
        if st.button("✅ SNIMI U SPISAK"):
            st.session_state.baza.append({
                "Kategorija": st.session_state.izabrana_kat,
                "Podkategorija": st.session_state.izabrana_podkat,
                "Artikl": naziv,
                "Količina": kol
            })
            st.success("Dodato u spisak!")
            st.balloons()

# --- PRIKAZ SPISKA (UVEK VIDLJIV NA DNU) ---
if st.session_state.baza:
    st.divider()
    st.subheader("📋 Vaš spisak zaliha")
    st.table(pd.DataFrame(st.session_state.baza))
