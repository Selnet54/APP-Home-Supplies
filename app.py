import streamlit as st
import os
from datetime import datetime, timedelta

# --- KONFIGURACIJA ---
st.set_page_config(page_title="Zalihe", layout="centered")

# --- CSS ZA FIKSNI RASPODRED I RAZMAKE ---
st.markdown("""
    <style>
    /* Spuštanje sadržaja i centriranje aplikacije */
    .block-container {
        padding-top: 120px !important;
        max-width: 400px !important;
        margin: auto;
    }

    /* FORSIRANJE HORIZONTALNOG REDA (3 kolone) - RADI I NA MOBILNOM */
    [data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        gap: 10px !important;
        justify-content: center !important;
    }

    /* Širina svake kolone da bi razmak bio oko 1cm */
    [data-testid="column"] {
        width: 30% !important;
        flex: none !important;
        text-align: center !important;
    }

    /* Heder dugmad (čist tekst) */
    div.stButton > button {
        border: none !important;
        background: none !important;
        padding: 2px !important;
        font-weight: bold !important;
        font-size: 13px !important;
    }

    /* Boja za Izlaz */
    div.stButton > button:contains("Izlaz") { color: red !important; }

    /* Centriranje slika */
    .stImage > img { margin: 0 auto; display: block; }
    </style>
    """, unsafe_allow_html=True)

# --- INICIJALIZACIJA ---
if 'korak' not in st.session_state: st.session_state.korak = "jezik"
if 'izbor' not in st.session_state: st.session_state.izbor = {}

# --- STRUKTURA PODATAKA (Kategorija -> Podkategorija -> Delovi) ---
podaci = {
    "Belo meso": {
        "Piletina": ["Gril pile", "Batak", "Karabatak", "Krila", "Belo meso"],
        "Guščije": ["Guščiji batak", "Guščije grudi", "Jetra"],
        "Pačije": ["Pačiji file", "Bataci"]
    },
    "Crveno meso": {
        "Svinjetina": ["But", "Vrat", "Krmenadla"],
        "Junetina": ["Biftek", "Ribić"]
    }
}

jezici_lista = [
    ("Srpski", "Srpski"), ("Engleski", "English"), ("Nemacki", "Deutsch"),
    ("Ruski", "Русский"), ("Ukrajinski", "Українська"), ("Madjarski", "Magyar"),
    ("Spanski", "Español"), ("Portugalski", "Português"), ("Mandarinski", "中文"),
    ("Francuski", "Français")
]

# --- HEDER FUNKCIJA ---
def prikazi_heder():
    c1, s1, c2, s2, c3, s3, c4, s4, c5 = st.columns([1, 0.1, 1, 0.1, 1, 0.1, 1, 0.1, 1])
    with c1: 
        if st.button("Home", key="h_home"): st.session_state.korak = "home"
    s1.write("|")
    with c2: 
        if st.button("Kat.", key="h_kat"): st.session_state.korak = "kategorije"
    s2.write("|")
    with c3: 
        if st.button("Zal.", key="h_zal"): st.session_state.korak = "spisak"
    s3.write("|")
    with c4: 
        if st.button("Pot.", key="h_pot"): st.session_state.korak = "potrebe"
    s4.write("|")
    with c5: 
        if st.button("Izlaz", key="h_exit"): 
            st.session_state.korak = "jezik"
            st.rerun()
    
    izabrani = st.session_state.get('izabrani_jezik_kod', 'Srpski')
    if os.path.exists(f"icons/{izabrani}.png"):
        st.image(f"icons/{izabrani}.png", width=40)
    st.markdown("<hr style='margin:2px 0'>", unsafe_allow_html=True)

# --- LOGIKA EKRANA ---

# 1. JEZIK (3x4 Grid)
if st.session_state.korak == "jezik":
    for i in range(0, len(jezici_lista), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(jezici_lista):
                fajl, naziv = jezici_lista[i + j]
                with cols[j]:
                    if os.path.exists(f"icons/{fajl}.png"): st.image(f"icons/{fajl}.png", width=45)
                    if st.button(naziv, key=f"L_{fajl}"):
                        st.session_state.izabrani_jezik_kod = fajl
                        st.session_state.korak = "kategorije"
                        st.rerun()

# 2. KATEGORIJE
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

# 3. PODKATEGORIJE (Piletina, Guščije...)
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

# 4. DIJELOVI (Batak, Gril pile...)
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

# 5. UNOS
elif st.session_state.korak == "unos":
    prikazi_heder()
    st.write(f"**{st.session_state.izbor['deo']}**")
    with st.form("form_u"):
        c1, c2 = st.columns(2)
        kom = c1.number_input("Kom:", min_value=1, step=1)
        kol = c2.number_input("Težina:")
        jed = c2.selectbox("", ["g", "kg", "lit"], label_visibility="collapsed")
        rok = st.number_input("Meseci:", value=6)
        if st.form_submit_button("SAČUVAJ"):
            st.success("OK!")
            st.session_state.korak = "kategorije"
