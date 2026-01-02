import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os

# --- KONFIGURACIJA ---
st.set_page_config(page_title="Zalihe App", layout="wide")

# CSS za Heder i Dugmad (Tvoj dizajn)
st.markdown("""
    <style>
    .header-nav { display: flex; justify-content: space-around; background-color: #333; padding: 10px; border-radius: 10px; margin-bottom: 20px; }
    .header-nav button { background: none; border: none; color: white; font-weight: bold; cursor: pointer; }
    .stButton > button { width: 100%; height: 60px; border-radius: 10px; font-size: 16px; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- INICIJALIZACIJA STANJA (Session State) ---
if 'korak' not in st.session_state: st.session_state.korak = "jezik"
if 'izabrani_jezik' not in st.session_state: st.session_state.izabrani_jezik = None
if 'izbor' not in st.session_state: st.session_state.izbor = {}
if 'baza_zaliha' not in st.session_state: st.session_state.baza_zaliha = []

# --- PODACI (Primer tvoje hijerarhije) ---
podaci = {
    "Hrana": {
        "Pileće meso": ["Gril pile", "Batak ceo", "Karabatak", "Krila"],
        "Svinjsko meso": ["Krmenadla", "Vrat", "But"]
    },
    "Higijena": {
        "Kuhinja": ["Sjaj", "Tablete za sudove", "Deterdžent"],
        "Kupatilo": ["Sapun", "Šampon"]
    }
}

# --- HEDER (Navigacija) ---
if st.session_state.korak != "jezik":
    col1, col2, col3, col4, col5 = st.columns(5)
    if col1.button("🏠 Home"): st.session_state.korak = "kategorije"
    if col2.button("📂 Kategorije"): st.session_state.korak = "kategorije"
    if col3.button("📋 Spisak zaliha"): st.session_state.korak = "spisak"
    if col4.button("⚠️ Potrebe"): st.session_state.korak = "potrebe"
    if col5.button("❌ Izlaz"): st.session_state.korak = "jezik"

# --- LOGIKA EKRANA ---

# 1. EKRAN: IZBOR JEZIKA
if st.session_state.korak == "jezik":
    st.title("Izaberite jezik / Select Language")
    jezici = ["Srpski", "Engleski", "Nemacki", "Francuski", "Ruski", "Ukrajinski", "Madjarski", "Spanski", "Portugalski", "Mandarinski"]
    cols = st.columns(3)
    for i, j in enumerate(jezici):
        if cols[i % 3].button(j):
            st.session_state.izabrani_jezik = j
            st.session_state.korak = "kategorije"
            st.rerun()

# 2. EKRAN: KATEGORIJE
elif st.session_state.korak == "kategorije":
    st.header("Izaberi kategoriju")
    cols = st.columns(2)
    for i, kat in enumerate(podaci.keys()):
        if cols[i % 2].button(kat):
            st.session_state.izbor['kat'] = kat
            st.session_state.korak = "podkategorije"
            st.rerun()

# 3. EKRAN: PODKATEGORIJE
elif st.session_state.korak == "podkategorije":
    st.header(f"📂 {st.session_state.izbor['kat']}")
    cols = st.columns(2)
    for i, podkat in enumerate(podaci[st.session_state.izbor['kat']].keys()):
        if cols[i % 2].button(podkat):
            st.session_state.izbor['podkat'] = podkat
            st.session_state.korak = "detalji"
            st.rerun()

# 4. EKRAN: DELOVI PROIZVODA
elif st.session_state.korak == "detalji":
    st.header(f"📍 {st.session_state.izbor['podkat']}")
    delovi = podaci[st.session_state.izbor['kat']][st.session_state.izbor['podkat']]
    cols = st.columns(2)
    for i, deo in enumerate(delovi):
        if cols[i % 2].button(deo):
            st.session_state.izbor['deo'] = deo
            st.session_state.korak = "unos"
            st.rerun()

# 5. EKRAN: FINALNI UNOS
elif st.session_state.korak == "unos":
    st.header("Unos podataka")
    kat = st.session_state.izbor['kat']
    podkat = st.session_state.izbor['podkat']
    deo = st.session_state.izbor['deo']
    
    st.info(f"Proizvod: {kat} - {podkat} - {deo}")
    
    with st.form("forma"):
        c1, c2 = st.columns(2)
        komada = c1.number_input("Komada:", min_value=1)
        kol = c2.number_input("Količina:")
        jedinica = c2.selectbox("Jedinica:", ["kg", "g", "lit", "kom"])
        
        datum_unosa = st.date_input("Datum unosa:", datetime.now())
        meseci_trajanja = st.number_input("Rok trajanja (meseci):", min_value=1, value=6)
        
        rok_trajanja = datum_unosa + timedelta(days=meseci_trajanja*30)
        st.write(f"Izračunati rok trajanja: **{rok_trajanja.strftime('%d.%m.%Y')}**")
        
        if st.form_submit_button("✅ SNIMI U BAZU"):
            nova_stavka = {
                "Naziv": f"{kat} {podkat} {deo}",
                "Kom": komada,
                "Količina": f"{kol} {jedinica}",
                "Unos": datum_unosa,
                "Rok": rok_trajanja
            }
            st.session_state.baza_zaliha.append(nova_stavka)
            st.success("Podaci snimljeni!")
            st.session_state.korak = "kategorije"

# EKRAN: SPISAK ZALIHA
elif st.session_state.korak == "spisak":
    st.header("📋 Trenutno stanje")
    if st.session_state.baza_zaliha:
        st.table(pd.DataFrame(st.session_state.baza_zaliha))
    else:
        st.write("Baza je prazna.")

# EKRAN: POTREBE (Logika za rok i količinu)
elif st.session_state.korak == "potrebe":
    st.header("⚠️ Potrebno nabaviti / Ističe rok")
    if st.session_state.baza_zaliha:
        df = pd.DataFrame(st.session_state.baza_zaliha)
        # Filtriranje: manje od 2 komada ili rok ističe za 7 dana
        danas = datetime.now().date()
        hitno = df[(df['Kom'] < 2) | (df['Rok'] <= danas + timedelta(days=7))]
        st.table(hitno)
