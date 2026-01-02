import streamlit as st
import os

# --- KONFIGURACIJA ---
st.set_page_config(page_title="Zalihe", layout="wide") # Promenjeno na wide za PC/Tablet

# --- TVOJ MASTER STRINGS (Skraćeno ovde, koristi svoj puni rečnik) ---
if 'jezik_kljuc' not in st.session_state: st.session_state.jezik_kljuc = "srpski"

# --- NAPREDNI RESPONZIVNI CSS ---
st.markdown("""
    <style>
    /* Kontejner koji se prilagođava uređaju */
    .block-container {
        padding-top: 5px !important;
        max-width: 95% !important; /* Na mobilnom zauzima skoro sve */
    }

    /* Prilagođavanje za PC i Tablet (širi ekrani) */
    @media (min-width: 768px) {
        .block-container {
            max-width: 800px !important; /* Na PC-u i Tabletu nije preširoko ali je dovoljno veliko */
            margin: auto;
        }
        div.stButton > button { font-size: 16px !important; } /* Veći font za PC */
    }

    /* Prilagođavanje za Mobilni */
    @media (max-width: 767px) {
        .block-container {
            max-width: 100% !important;
            padding-left: 5px !important;
            padding-right: 5px !important;
        }
        div.stButton > button { font-size: 11px !important; } /* Manji font za mobilni */
    }

    /* Heder fiksiran u jednom redu bez prelamanja */
    [data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        align-items: center !important;
        justify-content: space-between !important;
        gap: 2px !important;
    }

    /* PRECIZNO POZICIONIRANJE KATEGORIJE */
    div.stButton > button[key="h_kat"] {
        margin-left: 5px !important; /* Pomereno udesno da ne guši Home */
    }

    /* Dugmad bez okvira */
    div.stButton > button {
        border: none !important;
        background: none !important;
        padding: 5px !important;
        font-weight: bold !important;
        color: black !important;
        white-space: nowrap !important;
    }

    div.stButton > button:contains("Izlaz") { color: red !important; }
    
    /* Linija separatora */
    hr { margin: 10px 0 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- POMOĆNE FUNKCIJE ---
def jezik_mapa(ime_fajla):
    mape = {
        "Srpski": "srpski", "Engleski": "english", "Nemacki": "deutsch",
        "Ruski": "ruski", "Ukrajinski": "ukrajinski", "Madjarski": "hungary",
        "Spanski": "espanol", "Portugalski": "portugalski", "Mandarinski": "mandarinski",
        "Francuski": "francais"
    }
    return mape.get(ime_fajla, "srpski")

# --- DINAMIČKI HEDER ---
def prikazi_heder():
    # Koristimo fleksibilne kolone koje se šire na PC-u
    c1, c2, c3, c4, c5 = st.columns([1, 1.5, 1, 1, 1])
    
    # Ovde koristiš prevode iz svog master_strings rečnika
    # Primer: master_strings[st.session_state.jezik_kljuc]["home"]
    with c1: st.button("Home", key="h_home")
    with c2: st.button("Kategorija", key="h_kat")
    with c3: st.button("Zalihe", key="h_zal")
    with c4: st.button("Spisak", key="h_spis")
    with c5: 
        if st.button("Izlaz", key="h_izl"):
            st.session_state.korak = "jezik"
            st.rerun()

    # ZASTAVA I TEKST U ISTOM REDU
    if 'izabrani_jezik_kod' in st.session_state:
        kod = st.session_state.izabrani_jezik_kod
        naziv = st.session_state.izabrani_jezik_naziv
        path = f"icons/{kod}.png"
        
        # Red za zastavu: fiksna širina za sliku, ostalo za tekst
        f1, f2 = st.columns([0.15, 0.85]) 
        with f1:
            if os.path.exists(path): st.image(path, width=30)
        with f2:
            st.markdown(f"<p style='margin-top:5px; font-weight:bold;'>{naziv}</p>", unsafe_allow_html=True)
    
    st.markdown("<hr>", unsafe_allow_html=True)

# --- LOGIKA APLIKACIJE ---
prikazi_heder()

if 'korak' not in st.session_state: st.session_state.korak = "jezik"

if st.session_state.korak == "jezik":
    # Grid za jezike: 3 kolone na mobilnom, ali na PC-u će biti šire
    jezici_lista = [
        ("Srpski", "Srpski"), ("Engleski", "English"), ("Nemacki", "Deutsch"),
        ("Ruski", "Ruski"), ("Ukrajinski", "Ukrajinski"), ("Madjarski", "Madjarski"),
        ("Spanski", "Spanski"), ("Portugalski", "Portugalski"), ("Mandarinski", "Mandarinski"),
        ("Francuski", "Francuski")
    ]
    
    # Prikazivanje u redovima po 3
    for i in range(0, len(jezici_lista), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(jezici_lista):
                fajl, ime = jezici_lista[i + j]
                with cols[j]:
                    path = f"icons/{fajl}.png"
                    if os.path.exists(path): st.image(path, width=50)
                    if st.button(ime, key=f"L_{fajl}"):
                        st.session_state.izabrani_jezik_kod = fajl
                        st.session_state.izabrani_jezik_naziv = ime
                        st.session_state.jezik_kljuc = jezik_mapa(fajl)
                        st.session_state.korak = "kategorije"
                        st.rerun()
