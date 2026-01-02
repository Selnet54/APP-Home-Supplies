import streamlit as st
import os
from datetime import datetime, timedelta

# --- KONFIGURACIJA ---
st.set_page_config(page_title="Zalihe", layout="centered")

# --- CSS ZA STROGO ZBIJANJE (PORTRET MOBILNI) ---
st.markdown("""
    <style>
    /* 1. Podizanje svega nagore i maksimalno sužavanje aplikacije */
    .block-container {
        padding-top: 10px !important;
        max-width: 320px !important; 
        margin: auto;
    }

    /* 2. Horizontalni redovi (Heder i Grid) */
    [data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        justify-content: center !important;
        gap: 0px !important;
    }

    /* 3. Kolone hedera (Home, Kategorija...) */
    .header-col {
        width: 60px !important;
        flex: none !important;
    }

    /* 4. Stil dugmadi (Tekstualni) */
    div.stButton > button {
        border: none !important;
        background: none !important;
        padding: 2px !important;
        font-weight: bold !important;
        font-size: 11px !important;
        color: black !important;
        white-space: nowrap !important;
    }
    
    /* Pomeranje Kategorije ulevo (specifično dugme) */
    div.stButton > button[key="h_kat"] {
        margin-left: -15px !important;
    }

    div.stButton > button:contains("Izlaz") { color: red !important; }

    /* 5. Zastava i tekst u istom redu */
    .flag-row {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 10px;
        margin-top: 5px;
        margin-bottom: 5px;
    }
    .flag-row img { width: 30px; height: auto; }
    .flag-row span { font-weight: bold; font-size: 14px; }
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

# --- FUNKCIJA ZA HEDER ---
def prikazi_heder():
    # Home | Kategorija | Zalihe | Spisak | Izlaz
    # Koristimo 5 kolona fiksne širine
    c1, c2, c3, c4, c5 = st.columns([1, 1.2, 1, 1, 0.8])
    with c1: st.button("Home", key="h_home")
    with c2: st.button("Kategorija", key="h_kat")
    with c3: st.button("Zalihe", key="h_zal")
    with c4: st.button("Spisak", key="h_spis")
    with c5: 
        if st.button("Izlaz", key="h_izl"):
            st.session_state.korak = "jezik"
            st.rerun()
    
    # Zastava i tekst u istom redu
    if 'izabrani_jezik_kod' in st.session_state:
        kod = st.session_state.izabrani_jezik_kod
        naziv = st.session_state.izabrani_jezik_naziv
        path = f"icons/{kod}.png"
        if os.path.exists(path):
            st.markdown(f"""
                <div class="flag-row">
                    <img src="data:image/png;base64,{st.image_to_base64(path) if hasattr(st, 'image_to_base64') else ''}" /> 
                    <span>{naziv}</span>
                </div>
            """, unsafe_allow_html=True)
            # Alternativa ako gornje ne radi u Streamlitu:
            col_f1, col_f2 = st.columns([1, 2])
            with col_f1: st.image(path, width=30)
            with col_f2: st.markdown(f"**{naziv}**")
            
    st.markdown("<hr style='margin:2px 0'>", unsafe_allow_html=True)

# --- EKRANI ---
prikazi_heder()

if st.session_state.korak == "jezik":
    for i in range(0, len(jezici_lista), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(jezici_lista):
                fajl, ime = jezici_lista[i + j]
                with cols[j]:
                    if os.path.exists(f"icons/{fajl}.png"): 
                        st.image(f"icons/{fajl}.png", width=40)
                    if st.button(ime, key=f"L_{fajl}"):
                        st.session_state.izabrani_jezik_kod = fajl
                        st.session_state.izabrani_jezik_naziv = ime
                        st.session_state.korak = "kategorije"
                        st.rerun()

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

# ... Ostatak koda za podkategorije i delove ostaje isti ...
