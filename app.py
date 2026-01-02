import streamlit as st
import os
from datetime import datetime, timedelta

# --- KONFIGURACIJA ---
st.set_page_config(page_title="Zalihe", layout="centered")

# --- CSS: FORSIRANJE HORIZONTALNOG RASPOREDA NA MOBILNOM ---
st.markdown("""
    <style>
    /* 1. Pomeranje celog sadržaja naniže da se vidi vrh na PC */
    .block-container {
        padding-top: 50px !important;
        max-width: 500px !important;
    }

    /* 2. SILA: Kolone moraju ostati jedna pored druge (horizontalno) */
    [data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        align-items: center !important;
        justify-content: center !important;
        gap: 5px !important;
    }

    /* 3. Širina kolona u hederu i gridu */
    [data-testid="column"] {
        flex: 1 1 auto !important;
        min-width: 0px !important;
        text-align: center !important;
    }

    /* 4. Heder dugmad (bez okvira) */
    div.stButton > button {
        border: none !important;
        background: none !important;
        padding: 5px !important;
        font-weight: bold !important;
        font-size: 14px !important;
        width: 100% !important;
    }

    /* 5. Izlaz dugme crveno */
    div.stButton > button:contains("Izlaz") { color: red !important; }

    /* Smanjenje razmaka između slika i teksta */
    .stImage { margin-bottom: -10px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- INICIJALIZACIJA ---
if 'korak' not in st.session_state: st.session_state.korak = "jezik"
if 'izbor' not in st.session_state: st.session_state.izbor = {}

# --- PODACI (Jezici) ---
jezici_data = [
    ("Srpski", "Srpski"), ("Engleski", "English"), ("Nemacki", "Deutsch"),
    ("Ruski", "Русский"), ("Ukrajinski", "Українська"), ("Madjarski", "Magyar"),
    ("Spanski", "Español"), ("Portugalski", "Português"), ("Mandarinski", "中文"),
    ("Francuski", "Français")
]

# --- FUNKCIJA ZA HEDER (Sada forsira horizontalu) ---
def prikazi_heder():
    # Heder u jednom redu: Home | Kat. | Zalihe | Potrebe | Izlaz
    c1, s1, c2, s2, c3, s3, c4, s4, c5 = st.columns([1, 0.1, 1, 0.1, 1, 0.1, 1, 0.1, 1])
    with c1: 
        if st.button("Home"): st.session_state.korak = "home"
    s1.write("|")
    with c2: 
        if st.button("Kat."): st.session_state.korak = "kategorije"
    s2.write("|")
    with c3: 
        if st.button("Zal."): st.session_state.korak = "spisak"
    s3.write("|")
    with c4: 
        if st.button("Pot."): st.session_state.korak = "potrebe"
    s4.write("|")
    with c5: 
        if st.button("Izlaz"): 
            st.session_state.korak = "jezik"
            st.rerun()
    
    # Zastava ispod hedera
    jezik = st.session_state.get('izabrani_jezik_kod', 'Srpski')
    if os.path.exists(f"icons/{jezik}.png"):
        st.image(f"icons/{jezik}.png", width=40)
    st.markdown("<hr style='margin:2px 0'>", unsafe_allow_html=True)

# --- EKRAN 1: JEZICI (3 u redu, horizontalno i na mobilnom) ---
if st.session_state.korak == "jezik":
    # Grupišemo jezike po 3 za prikaz u redovima
    for i in range(0, len(jezici_data), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(jezici_data):
                fajl, ime = jezici_data[i + j]
                with cols[j]:
                    if os.path.exists(f"icons/{fajl}.png"):
                        st.image(f"icons/{fajl}.png", width=45)
                    if st.button(ime, key=f"L_{fajl}"):
                        st.session_state.izabrani_jezik_kod = fajl
                        st.session_state.korak = "kategorije"
                        st.rerun()

# --- EKRAN 2: KATEGORIJE (Horizontalni grid) ---
elif st.session_state.korak == "kategorije":
    prikazi_heder()
    # Primer kategorija iz tvog koda
    kats = ["Belo meso", "Crveno meso", "Divljač", "Higijena", "Alat", "Ostalo"]
    for i in range(0, len(kats), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(kats):
                naziv = kats[i + j]
                with cols[j]:
                    if st.button(naziv, key=f"K_{naziv}"):
                        st.session_state.izbor['kat'] = naziv
                        st.session_state.korak = "podkat"
                        st.rerun()

# --- EKRAN 3: UNOS (Primer forme) ---
elif st.session_state.korak == "unos":
    prikazi_heder()
    st.write(f"**Unos: {st.session_state.izbor.get('kat', '')}**")
    with st.form("form_unos"):
        c1, c2 = st.columns(2)
        kom = c1.number_input("Kom:", min_value=1)
        kol = c2.number_input("Težina:")
        jed = c2.selectbox("", ["g", "kg", "lit"], label_visibility="collapsed")
        if st.form_submit_button("SNIMI"):
            st.success("OK")
