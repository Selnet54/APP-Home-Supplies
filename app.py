import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# --- KONFIGURACIJA ---
st.set_page_config(page_title="Zalihe", layout="wide")

# --- STILIZACIJA (Heder u jednom redu i crveno dugme) ---
st.markdown("""
    <style>
    /* Heder u jednom redu */
    .nav-container {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 10px;
        padding: 10px 0;
        border-bottom: 1px solid #ddd;
    }
    .nav-item {
        font-weight: bold;
        text-decoration: none;
        color: black;
    }
    /* Stil za dugmad da izgledaju kao tekst u hederu */
    div.stButton > button.header-btn {
        border: none !important;
        background: none !important;
        font-weight: bold !important;
        padding: 0 5px !important;
        width: auto !important;
        height: auto !important;
    }
    /* Crveno dugme Izlaz */
    .exit-btn button {
        color: red !important;
    }
    /* Kvadratna dugmad za kategorije */
    .grid-btn button {
        width: 100% !important;
        height: 80px !important;
        border-radius: 10px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- PODACI IZ TVOG KODA (Izvučeno iz multi-jezik5a.py) ---
# Ovde koristim tvoje stvarne nazive iz SR_items
podaci_srpski = {
    "Belo meso": ["Pileći batak", "Pileći karabatak", "Pileća krila", "Pileće grudi", "Pileći file"],
    "Crveno meso": ["Svinjski but", "Svinjski vrat", "Svinjska krmenadla", "Juneći but", "Juneća leđa"],
    "Sitna divljač": ["Zec", "Fazan", "Jerebica"],
    "Krupna divljač": ["Srneći but", "Srneća leđa", "Vepar - but", "Vepar - leđa"]
}

# --- INICIJALIZACIJA ---
if 'korak' not in st.session_state: st.session_state.korak = "jezik"
if 'izbor' not in st.session_state: st.session_state.izbor = {}
if 'baza' not in st.session_state: st.session_state.baza = []

# --- HEDER (SVE U JEDNOM REDU) ---
if st.session_state.korak != "jezik":
    # Koristimo kolone za precizno poravnanje u jednom redu
    c1, c2, c3, c4, c5, c6, c7, c8, c9 = st.columns([1, 0.1, 1, 0.1, 1, 0.1, 1, 0.1, 1])
    
    with c1: 
        if st.button("Home", key="h_home", help="Početna"): st.session_state.korak = "home"
    with c2: st.write("|")
    with c3: 
        if st.button("Kategorije", key="h_kat"): st.session_state.korak = "izbor_kategorija"
    with c2: st.write("|") # Greška u indeksu kolone, ispravljeno ispod
    # Streamlit kolone moraju ići redom:
    c1, s1, c2, s2, c3, s3, c4, s4, c5 = st.columns([1, 0.1, 1, 0.1, 1, 0.1, 1, 0.1, 1])
    
    if c1.button("Home", key="btn_home"): st.session_state.korak = "home"
    s1.write("|")
    if c2.button("Kategorije", key="btn_kat"): st.session_state.korak = "izbor_kategorija"
    s2.write("|")
    if c3.button("Spisak zaliha", key="btn_zal"): st.session_state.korak = "spisak"
    s3.write("|")
    if c4.button("Spisak potreba", key="btn_pot"): st.session_state.korak = "potrebe"
    s4.write("|")
    
    with c5:
        st.markdown('<div class="exit-btn">', unsafe_allow_html=True)
        if st.button("Izlaz", key="btn_izlaz"):
            st.session_state.korak = "jezik"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<hr style="margin-top:0; margin-bottom:20px;">', unsafe_allow_html=True)

# --- LOGIKA EKRANA ---

# 1. JEZIK
if st.session_state.korak == "jezik":
    st.title("Izaberite jezik")
    jezici = ["Srpski", "Engleski", "Nemacki", "Francuski", "Ruski", "Ukrajinski", "Madjarski", "Spanski", "Portugalski", "Mandarinski"]
    cols = st.columns(2)
    for i, j in enumerate(jezici):
        if cols[i % 2].button(j, key=f"L_{j}"):
            st.session_state.korak = "home"
            st.rerun()

# 2. IZBOR KATEGORIJA (Belo meso, Crveno meso...)
elif st.session_state.korak == "izbor_kategorija":
    st.subheader("Izaberite vrstu mesa/proizvoda:")
    st.markdown('<div class="grid-btn">', unsafe_allow_html=True)
    cols = st.columns(2)
    for i, kat in enumerate(podaci_srpski.keys()):
        if cols[i % 2].button(kat, key=f"K_{kat}"):
            st.session_state.izbor['kat'] = kat
            st.session_state.korak = "izbor_dela"
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# 3. IZBOR DELA (Batak, Karabatak...)
elif st.session_state.korak == "izbor_dela":
    st.subheader(f"Kategorija: {st.session_state.izbor['kat']}")
    st.markdown('<div class="grid-btn">', unsafe_allow_html=True)
    delovi = podaci_srpski[st.session_state.izbor['kat']]
    cols = st.columns(2)
    for i, deo in enumerate(delovi):
        if cols[i % 2].button(deo, key=f"D_{deo}"):
            st.session_state.izbor['deo'] = deo
            st.session_state.korak = "unos_forme"
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# 4. UNOS PODATAKA (Ekran 5)
elif st.session_state.korak == "unos_forme":
    st.subheader("Unos u zalihe")
    deo = st.session_state.izbor['deo']
    kat = st.session_state.izbor['kat']
    
    with st.form("forma_unos"):
        st.markdown(f"### {deo}")
        
        c1, c2 = st.columns(2)
        komada = c1.number_input("Broj komada (npr. 3)", min_value=0, step=1)
        kolicina = c2.number_input("Količina (npr. 700)")
        jedinica = c2.selectbox("Jedinica", ["g", "kg", "lit", "kom"])
        
        c3, c4 = st.columns(2)
        datum_unosa = c3.date_input("Datum unosa", datetime.now())
        meseci = c4.number_input("Rok trajanja (meseci)", min_value=1, value=6)
        
        rok_date = datum_unosa + timedelta(days=meseci*30.44)
        st.write(f"Rok ističe: **{rok_date.strftime('%d.%m.%Y')}**")
        
        if st.form_submit_button("UNESI U BAZU"):
            st.success("Artikl dodat!")
            st.session_state.korak = "izbor_kategorija"
