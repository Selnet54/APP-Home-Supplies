import streamlit as st
import os
from datetime import datetime, timedelta

# --- KONFIGURACIJA ---
st.set_page_config(page_title="Zalihe", layout="centered")

# --- CSS ZA STROGU KONTROLU IZGLEDA ---
st.markdown("""
    <style>
    /* 1. Spuštanje sadržaja za oko 1.5 cm da se sve vidi */
    .block-container {
        padding-top: 40px !important;
        max-width: 400px !important;
        margin: auto;
    }

    /* 2. FORSIRANJE HORIZONTALNOG REDA - UKIDANJE RESPONSIVE SLOJA */
    [data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        justify-content: center !important;
        align-items: center !important;
        gap: 2px !important;
    }

    /* Fiksna širina kolona da sve stane u vertikalni ekran telefona */
    [data-testid="column"] {
        width: 75px !important; /* Dovoljno usko da 5 kolona stane u red */
        flex: none !important;
    }

    /* Posebna širina za grid jezika (3 kolone) */
    .lang-grid [data-testid="column"] {
        width: 120px !important;
    }

    /* Dugmad - tekstualni stil, bez okvira */
    div.stButton > button {
        border: none !important;
        background: none !important;
        padding: 2px !important;
        font-weight: bold !important;
        font-size: 12px !important;
        color: black !important;
        white-space: nowrap !important;
    }

    /* Crvena boja za Izlaz */
    div.stButton > button:contains("Izlaz") { color: red !important; }

    /* Centriranje zastava */
    .stImage > img { margin: 0 auto; display: block; }
    
    .flag-text {
        text-align: center;
        font-weight: bold;
        font-size: 16px;
        margin-top: -5px;
    }
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

# --- FUNKCIJA ZA HEDER (Sada se vidi i kod jezika) ---
def prikazi_heder():
    # Raspored: Home | Kategorija | Zalihe | Spisak | Izlaz
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
    
    # Prikaz zastave i teksta ako je jezik izabran
    if 'izabrani_jezik_kod' in st.session_state:
        kod = st.session_state.izabrani_jezik_kod
        naziv = st.session_state.izabrani_jezik_naziv
        if os.path.exists(f"icons/{kod}.png"):
            st.image(f"icons/{kod}.png", width=40)
            st.markdown(f'<div class="flag-text">{naziv}</div>', unsafe_allow_html=True)
    st.markdown("<hr style='margin:5px 0'>", unsafe_allow_html=True)

# --- EKRANI ---

# Heder se prikazuje na svim ekranima
prikazi_heder()

if st.session_state.korak == "jezik":
    st.markdown('<div class="lang-grid">', unsafe_allow_html=True)
    for i in range(0, len(jezici_lista), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(jezici_lista):
                fajl, ime = jezici_lista[i + j]
                with cols[j]:
                    if os.path.exists(f"icons/{fajl}.png"): 
                        st.image(f"icons/{fajl}.png", width=45)
                    if st.button(ime, key=f"L_{fajl}"):
                        st.session_state.izabrani_jezik_kod = fajl
                        st.session_state.izabrani_jezik_naziv = ime
                        st.session_state.korak = "kategorije"
                        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.korak == "kategorije":
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

elif st.session_state.korak == "podkategorije":
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

elif st.session_state.korak == "delovi":
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

elif st.session_state.korak == "unos":
    st.write(f"**Unos: {st.session_state.izbor['deo']}**")
    with st.form("f_unos"):
        c1, c2 = st.columns(2)
        kom = c1.number_input("Kom:", min_value=1, step=1)
        kol = c2.number_input("Težina:")
        jed = c2.selectbox("", ["g", "kg", "kom"], label_visibility="collapsed")
        rok = st.number_input("Mjeseci:", value=6)
        if st.form_submit_button("SAČUVAJ"):
            st.success("Dodano!")
            st.session_state.korak = "kategorije"
