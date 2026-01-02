import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os

# --- KONFIGURACIJA ---
st.set_page_config(page_title="Zalihe", layout="wide")

# --- MODERAN HEDER I STILIZACIJA ---
st.markdown("""
    <style>
    /* Stil za dugmad u hederu da izgledaju kao linkovi */
    div.stButton > button {
        border: none;
        background: none;
        padding: 0px 10px;
        font-weight: bold;
        color: #31333F;
    }
    div.stButton > button:hover {
        color: #ff4b4b;
    }
    /* Horizontalna linija */
    .header-line {
        border-bottom: 1px solid #ddd;
        margin-bottom: 20px;
    }
    /* Specifično crveno dugme za Izlaz */
    [data-testid="stBaseButton-secondary"] p:contains("Izlaz") {
        color: red !important;
    }
    /* Stil za kvadratnu dugmad u kategorijama */
    .cat-button > button {
        width: 100%;
        height: 80px !important;
        border: 2px solid #f0f2f6 !important;
        border-radius: 10px !important;
        background-color: #f8f9fa !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- INICIJALIZACIJA STANJA ---
if 'korak' not in st.session_state: st.session_state.korak = "jezik"
if 'izbor' not in st.session_state: st.session_state.izbor = {}
if 'baza' not in st.session_state: st.session_state.baza = []

# --- PODACI IZ TVOG PROGRAMA (Skraćeno za primer) ---
meni = {
    "Hrana": {
        "Pileće meso": ["Gril pile", "Batak ceo", "Karabatak", "Krila"],
        "Svinjsko meso": ["Krmenadla", "Vrat", "But"]
    },
    "Higijena": {
        "Kuhinja": ["Sjaj", "Tablete", "Deterdžent"],
        "Kupatilo": ["Sapun", "Šampon"]
    }
}

# --- FUNKCIJA ZA HEDER ---
def prikazi_heder():
    cols = st.columns([1, 1, 1, 1, 1.2, 1], gap="small")
    # Tekstualni meni sa separatorima (linijama)
    if cols[0].button("Home"): st.session_state.korak = "home"
    cols[0].write("|")
    
    if cols[1].button("Kategorije"): st.session_state.korak = "kategorije"
    cols[1].write("|")
    
    if cols[2].button("Spisak zaliha"): st.session_state.korak = "spisak"
    cols[2].write("|")
    
    if cols[3].button("Spisak potreba"): st.session_state.korak = "potrebe"
    cols[3].write("|")
    
    # Crveno dugme Izlaz
    if cols[4].button("Izlaz"):
        st.session_state.korak = "jezik"
        st.rerun()
    
    st.markdown('<div class="header-line"></div>', unsafe_allow_html=True)

# --- LOGIKA EKRANA ---

# EKRAN 1: IZBOR JEZIKA (Početni)
if st.session_state.korak == "jezik":
    st.title("Izaberite jezik")
    jezici = ["Srpski", "Engleski", "Nemacki", "Francuski", "Ruski", "Ukrajinski", "Madjarski", "Spanski", "Portugalski", "Mandarinski"]
    cols = st.columns(3)
    for i, j in enumerate(jezici):
        if cols[i % 3].button(j, key=f"lang_{j}"):
            st.session_state.izabrani_jezik = j
            st.session_state.korak = "home" # Ide na Home nakon jezika
            st.rerun()

# EKRANI NAKON JEZIKA
else:
    prikazi_heder()

    # EKRAN: HOME
    if st.session_state.korak == "home":
        st.subheader("Dobrodošli u sistem za zalihe")
        st.write("Izaberite opciju iz menija iznad.")

    # EKRAN: IZBOR KATEGORIJA (Kvadratna dugmad)
    elif st.session_state.korak == "kategorije":
        st.subheader("Glavne kategorije")
        cols = st.columns(2)
        for i, kat in enumerate(meni.keys()):
            if cols[i % 2].button(kat, key=f"cat_{kat}"):
                st.session_state.izbor['kat'] = kat
                st.session_state.korak = "podkategorije"
                st.rerun()

    # EKRAN: PODKATEGORIJE
    elif st.session_state.korak == "podkategorije":
        st.subheader(f"Podkategorije: {st.session_state.izbor['kat']}")
        cols = st.columns(2)
        for i, podkat in enumerate(meni[st.session_state.izbor['kat']].keys()):
            if cols[i % 2].button(podkat, key=f"pkat_{podkat}"):
                st.session_state.izbor['podkat'] = podkat
                st.session_state.korak = "detalji"
                st.rerun()

    # EKRAN: DELOVI (DETALJI)
    elif st.session_state.korak == "detalji":
        st.subheader(f"Delovi: {st.session_state.izbor['podkat']}")
        delovi = meni[st.session_state.izbor['kat']][st.session_state.izbor['podkat']]
        cols = st.columns(2)
        for i, deo in enumerate(delovi):
            if cols[i % 2].button(deo, key=f"deo_{deo}"):
                st.session_state.izbor['deo'] = deo
                st.session_state.korak = "unos"
                st.rerun()

    # EKRAN: FINALNI UNOS
    elif st.session_state.korak == "unos":
        st.subheader("Unos proizvoda")
        with st.form("unos_form"):
            st.write(f"**{st.session_state.izbor['kat']} / {st.session_state.izbor['podkat']} / {st.session_state.izbor['deo']}**")
            
            c1, c2 = st.columns(2)
            komada = c1.number_input("Broj komada", min_value=1, step=1)
            kolicina = c2.number_input("Količina")
            jedinica = c2.selectbox("Jedinica", ["kg", "g", "lit", "kom"])
            
            datum_unosa = st.date_input("Datum unosa", datetime.now())
            rok_meseci = st.number_input("Rok trajanja (meseci)", min_value=1, value=6)
            
            # Izračunavanje roka
            rok_trajanja = (datum_unosa + timedelta(days=rok_meseci*30.44)).strftime('%d.%m.%Y')
            st.write(f"Rok trajanja ističe: **{rok_trajanja}**")
            
            if st.form_submit_button("SAČUVAJ U ZALIHE"):
                # Ovde ide logika za bazu
                st.success("Uspešno snimljeno!")
                st.session_state.korak = "kategorije"
