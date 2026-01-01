import streamlit as st
from PIL import Image
import os
import pandas as pd

# --- 1. OSNOVNA PODEŠAVANJA I DIZAJN ---
st.set_page_config(page_title="Moje Zalihe", layout="wide")

# Putanja do ikona
icon_path = "icons/512.png"

# --- 2. LOGIKA ZA JEZIKE ---
jezici = ["Srpski", "Engleski", "Nemacki", "Francuski", "Ruski", "Ukrajinski", "Madjarski", "Spanski", "Portugalski", "Mandarinski"]

with st.sidebar:
    if os.path.exists(icon_path):
        st.image(icon_path, width=120)
    
    izbor_jezika = st.selectbox("Jezik / Language", jezici)
    
    putanja_zastave = f"icons/{izbor_jezika}.png"
    if os.path.exists(putanja_zastave):
        st.image(putanja_zastave, width=80)

# --- 3. DEFINISANJE KATEGORIJA I PODKATEGORIJA ---
# Ovde možeš dodati svoje kategorije
meni = {
    "Hrana": ["Mlečni proizvodi", "Meso", "Voće i povrće", "Ostalo"],
    "Higijena": ["Kućna hemija", "Lična higijena"],
    "Alati": ["Ručni alat", "Električni alat"],
    "Ostalo": ["Razno"]
}

# --- 4. BAZA PODATAKA (Čuvanje dok je aplikacija pokrenuta) ---
if 'baza_zaliha' not in st.session_state:
    st.session_state.baza_zaliha = pd.DataFrame(columns=["Kategorija", "Podkategorija", "Proizvod", "Količina"])

# --- 5. GLAVNI EKRAN: UNOS PROIZVODA ---
st.header(f"Sistem za zalihe - {izbor_jezika}")

with st.expander("➕ Unesi novi proizvod", expanded=True):
    col1, col2 = st.columns(2)
    
    with col1:
        kat = st.selectbox("Izaberi kategoriju:", list(meni.keys()))
        podkat = st.selectbox("Izaberi podkategoriju:", meni[kat])
    
    with col2:
        proizvod = st.text_input("Naziv proizvoda:")
        kolicina = st.number_input("Količina:", min_value=0, step=1)

    if st.button("Snimi u listu"):
        novo_stanje = pd.DataFrame([[kat, podkat, proizvod, kolicina]], 
                                   columns=["Kategorija", "Podkategorija", "Proizvod", "Količina"])
        st.session_state.baza_zaliha = pd.concat([st.session_state.baza_zaliha, novo_stanje], ignore_index=True)
        st.success("Proizvod je uspešno dodat!")

# --- 6. PRIKAZ I AŽURIRANJE LISTE ---
st.subheader("📋 Trenutno stanje zaliha")

if not st.session_state.baza_zaliha.empty:
    # Omogućava ti da menjaš tabelu direktno (Ažuriranje)
    editovano_stanje = st.data_editor(st.session_state.baza_zaliha, num_rows="dynamic")
    st.session_state.baza_zaliha = editovano_stanje
    
    if st.button("Obriši sve"):
        st.session_state.baza_zaliha = pd.DataFrame(columns=["Kategorija", "Podkategorija", "Proizvod", "Količina"])
        st.rerun()
else:
    st.info("Lista je trenutno prazna. Unesite prvi proizvod iznad.")
