import streamlit as st
import os
from datetime import datetime, timedelta

# --- KONFIGURACIJA ---
st.set_page_config(page_title="Zalihe", layout="centered")

# --- AGRESIVNI CSS ZA MOBILNI RASPODRED ---
st.markdown("""
    <style>
    /* Smanjen padding na vrhu da se vrati sve gore za oko 2cm */
    .block-container {
        padding-top: 40px !important;
        max-width: 450px !important;
        margin: auto;
    }

    /* FORSIRANJE HORIZONTALNOG REDA - Bez obzira na uređaj */
    [data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        justify-content: center !important;
        align-items: center !important;
        gap: 10px !important; /* Razmak između kolona */
    }

    /* Fiksna širina kolona da ne bi bežale van ekrana */
    [data-testid="column"] {
        width: 120px !important; 
        flex: none !important;
    }

    /* Heder dugmad - Puni nazivi, bez okvira */
    div.stButton > button {
        border: none !important;
        background: none !important;
        padding: 5px 2px !important;
        font-weight: bold !important;
        font-size: 14px !important;
        white-space: nowrap !important; /* Sprečava prelamanje teksta */
    }

    /* Crveni Izlaz */
    div.stButton > button:contains("Izlaz") { color: red !important; }

    /* Centriranje zastava i slika */
    .stImage > img { margin: 0 auto; display: block; }
    </style>
    """, unsafe_allow_html=True)

# --- INICIJALIZACIJA ---
if 'korak' not in st.session_state: st.session_state.korak = "jezik"
if 'izbor' not in st.session_state: st.session_state.izbor = {}

# --- PODACI ---
jezici_lista = [
    ("Srpski", "Srpski"), ("Engleski", "English"), ("Nemacki", "Deutsch"),
    ("Ruski", "Русский"), ("Ukrajinski", "Українська"), ("Madjarski", "Magyar"),
    ("Spanski", "Español"), ("Portugalski", "Português"), ("Mandarinski", "中文"),
    ("Francuski", "Français")
]

podaci = {
    "Belo meso": {
        "Piletina": ["Gril pile", "Batak", "Karabatak", "Krila", "Belo meso"],
        "Guščije": ["Guščiji batak", "Guščije grudi"],
        "Pačije": ["Pačiji file", "Bataci"]
    }
}

# --- FUNKCIJA ZA HEDER (Sada se vidi svuda) ---
def prikazi_heder():
    # Puni nazivi bez vertikalnih linija radi uštede prostora
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1: 
        if st.button("Home"): st.session_state.korak = "home"
    with c2: 
        if st.button("Kategorija"): st.session_state.korak = "kategorije"
    with c3: 
        if st.button("Zalihe"): st.session_state.korak = "spisak"
    with c4: 
        if st.button("Spisak"): st.session_state.korak = "potrebe"
    with c5: 
        if st.button("Izlaz"): 
            st.session_state.korak = "jezik"
            st.rerun()
    
    # Prikaz zastave ako je jezik izabran
    if 'izabrani_jezik_kod' in st.session_state:
        jezik = st.session_state.izabrani_jezik_kod
        if os.path.exists(f"icons/{jezik}.png"):
            st.image(f"icons/{jezik}.png", width=40)
    st.markdown("<hr style='margin:5px 0'>", unsafe_allow_html=True)

# --- LOGIKA EKRANA ---

# 1. EKRAN: JEZICI (Prikazujemo heder i ovde ako želiš, ili samo mrežu)
if st.session_state.korak == "jezik":
    # Ako želiš heder i na prvom ekranu, otkomentariši donju liniju:
    # prikazi_heder() 
    
    st.write(" ") # Mali razmak od vrha
    for i in range(0, len(jezici_lista), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(jezici_lista):
                fajl, naziv = jezici_lista[i + j]
                with cols[j]:
                    if os.path.exists(f"icons/{fajl}.png"): 
                        st.image(f"icons/{fajl}.png", width=45)
                    if st.button(naziv, key=f"L_{fajl}"):
                        st.session_state.izabrani_jezik_kod = fajl
                        st.session_state.korak = "kategorije"
                        st.rerun()

# 2. EKRAN: KATEGORIJE
elif st.session_state.korak == "kategorije":
    prikazi_heder()
    kats = list(podaci.keys())
    for i in range(0, len(kats), 3):
        cols = st.columns(3)
        for j in range(3):
            if i+j < len(kats):
                k = kats[i+j]
                with cols[j]:
                    if st.button(k, key=f"K_{k}"):
                        st.session_state.izbor['kat'] = k
                        st.session_state.korak = "podkategorije"
                        st.rerun()

# 3. EKRAN: PODKATEGORIJE
elif st.session_state.korak == "podkategorije":
    prikazi_heder()
    pk_lista = list(podaci[st.session_state.izbor['kat']].keys())
    for i in range(0, len(pk_lista), 3):
        cols = st.columns(3)
        for j in range(3):
            if i+j < len(pk_lista):
                pk = pk_lista[i+j]
                with cols[j]:
                    if st.button(pk, key=f"PK_{pk}"):
                        st.session_state.izbor['podkat'] = pk
                        st.session_state.korak = "delovi"
                        st.rerun()

# 4. EKRAN: DELOVI
elif st.session_state.korak == "delovi":
    prikazi_heder()
    delovi = podaci[st.session_state.izbor['kat']][st.session_state.izbor['podkat']]
    for i in range(0, len(delovi), 3):
        cols = st.columns(3)
        for j in range(3):
            if i+j < len(delovi):
                d = delovi[i+j]
                with cols[j]:
                    if st.button(d, key=f"D_{d}"):
                        st.session_state.izbor['deo'] = d
                        st.session_state.korak = "unos"
                        st.rerun()
