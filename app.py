import streamlit as st
import os
from datetime import datetime, timedelta

# --- KONFIGURACIJA ---
st.set_page_config(page_title="Zalihe", layout="centered")

# --- CSS ZA STROGO FIKSNI RASPODRED ---
st.markdown("""
    <style>
    /* Spuštanje sadržaja za oko 1.5 cm - da se vidi heder na PC i mob */
    .block-container {
        padding-top: 60px !important;
        max-width: 400px !important;
        margin: auto;
    }

    /* SILA: Horizontalni red sa 3 kolone na svim ekranima */
    [data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        justify-content: center !important;
        gap: 2px !important; /* Minimalni razmak */
    }

    /* Fiksna širina kolona da bi razmak bio mali (oko 1cm između teksta) */
    [data-testid="column"] {
        width: 110px !important; 
        flex: none !important;
    }

    /* Heder - 5 kolona, puni nazivi, zbijeno */
    .header-btns [data-testid="column"] {
        width: 75px !important;
    }

    div.stButton > button {
        border: none !important;
        background: none !important;
        padding: 2px !important;
        font-weight: bold !important;
        font-size: 13px !important;
        white-space: nowrap !important;
    }

    div.stButton > button:contains("Izlaz") { color: red !important; }

    .stImage > img { margin: 0 auto; display: block; }
    </style>
    """, unsafe_allow_html=True)

# --- INICIJALIZACIJA ---
if 'korak' not in st.session_state: st.session_state.korak = "jezik"
if 'izbor' not in st.session_state: st.session_state.izbor = {}

# --- PODACI (Hijerarhija 4 nivoa) ---
podaci = {
    "Belo meso": {
        "Piletina": ["Gril pile", "Batak", "Karabatak", "Krila", "Belo meso"],
        "Guščije": ["Guščiji batak", "Guščije grudi"],
        "Pačije": ["Pačiji file", "Bataci"]
    },
    "Crveno meso": {
        "Svinjetina": ["But", "Vrat", "Krmenadla"],
        "Junetina": ["Biftek", "But"]
    }
}

jezici_lista = [
    ("Srpski", "Srpski"), ("Engleski", "English"), ("Nemacki", "Deutsch"),
    ("Ruski", "Русский"), ("Ukrajinski", "Українська"), ("Madjarski", "Magyar"),
    ("Spanski", "Español"), ("Portugalski", "Português"), ("Mandarinski", "中文"),
    ("Francuski", "Français")
]

# --- FUNKCIJA ZA HEDER ---
def prikazi_heder():
    st.markdown('<div class="header-btns">', unsafe_allow_html=True)
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
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Zastava
    if 'izabrani_jezik_kod' in st.session_state:
        jezik = st.session_state.izabrani_jezik_kod
        if os.path.exists(f"icons/{jezik}.png"):
            st.image(f"icons/{jezik}.png", width=40)
    st.markdown("<hr style='margin:2px 0'>", unsafe_allow_html=True)

# --- LOGIKA EKRANA ---
if st.session_state.korak == "jezik":
    # Na prvom ekranu (izbor jezika) ne prikazujemo heder da ne bi bilo gužve
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
else:
    prikazi_heder()
    
    if st.session_state.korak == "kategorije":
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
        st.write(f"**{st.session_state.izbor['deo']}**")
        with st.form("form_u"):
            c1, c2 = st.columns(2)
            kom = c1.number_input("Komada:", min_value=1, step=1)
            kol = c2.number_input("Težina/Lit:")
            jed = c2.selectbox("", ["g", "kg", "lit", "kom"], label_visibility="collapsed")
            rok = st.number_input("Meseci trajanja:", value=6)
            if st.form_submit_button("SAČUVAJ"):
                st.success("Uspešno dodato!")
                st.session_state.korak = "kategorije"
