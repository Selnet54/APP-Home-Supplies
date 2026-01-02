import streamlit as st
import os

# --- KONFIGURACIJA ---
st.set_page_config(page_title="Zalihe", layout="centered")

# --- MASTER STRINGS REČNIK (Integrisan) ---
master_strings = {
    "srpski": {
        "nazad": "Nazad", "stanje": "Zalihe", "izlaz": "Izlaz", "spisak": "Spisak", "home": "Home", "kategorija": "Kategorija",
        "izbor_jezika": "Izaberite jezik", "Ostalo": "Ostalo"
        # ... (ostatak vaših stringova ovde)
    },
    "hungary": {
        "nazad": "Vissza", "stanje": "Készlet", "izlaz": "Kilépés", "spisak": "Bevásárlólista", "home": "Főoldal", "kategorija": "Kategória",
        "izbor_jezika": "Válasszon nyelvet"
    },
    "ukrajinski": {
        "nazad": "Назад", "stanje": "Запаси", "izlaz": "Вихід", "spisak": "Список", "home": "Головна", "kategorija": "Категорія"
    },
    "ruski": {
        "nazad": "Назад", "stanje": "Запасы", "izlaz": "Выход", "spisak": "Список", "home": "Главная", "kategorija": "Категория"
    },
    "english": {
        "nazad": "Back", "stanje": "Inventory", "izlaz": "Exit", "spisak": "Shopping List", "home": "Home", "kategorija": "Category"
    },
    "deutsch": {
        "nazad": "Zurück", "stanje": "Bestand", "izlaz": "Beenden", "spisak": "Einkaufsliste", "home": "Start", "kategorija": "Kategorie"
    },
    "mandarinski": {
        "nazad": "返回", "stanje": "库存", "izlaz": "退出", "spisak": "购物清单", "home": "首页", "kategorija": "类别"
    },
    "espanol": {
        "nazad": "Atrás", "stanje": "Inventario", "izlaz": "Salir", "spisak": "Lista", "home": "Inicio", "kategorija": "Categoría"
    },
    "portugalski": {
        "nazad": "Voltar", "stanje": "Estoque", "izlaz": "Sair", "spisak": "Lista", "home": "Início", "kategorija": "Categoria"
    },
    "francais": {
        "nazad": "Retour", "stanje": "Stock", "izlaz": "Quitter", "spisak": "Liste", "home": "Accueil", "kategorija": "Catégorie"
    }
}

# Pomoćna mapa za povezivanje naziva ikona sa ključevima rečnika
jezik_mapa = {
    "Srpski": "srpski", "Engleski": "english", "Nemacki": "deutsch",
    "Ruski": "ruski", "Ukrajinski": "ukrajinski", "Madjarski": "hungary",
    "Spanski": "espanol", "Portugalski": "portugueks", "Mandarinski": "mandarinski",
    "Francuski": "francais"
}

# --- CSS ZA POZICIONIRANJE I PODIZANJE ---
st.markdown("""
    <style>
    .block-container { padding-top: 0px !important; max-width: 360px !important; margin: auto; }
    [data-testid="stHorizontalBlock"] { display: flex !important; flex-direction: row !important; flex-wrap: nowrap !important; gap: 0px !important; }
    
    div.stButton > button {
        border: none !important; background: none !important; padding: 0px !important;
        font-weight: bold !important; font-size: 11px !important; color: black !important;
    }

    /* POMERANJE KATEGORIJE UDESNO ZA 2 KARAKTERA */
    div.stButton > button[key="h_kat"] {
        margin-left: -15px !important; /* Smanjeno sa -25 na -15 da bi otišlo udesno */
    }

    div.stButton > button:contains("Izlaz") { color: red !important; }
    hr { margin: 5px 0 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- INICIJALIZACIJA ---
if 'korak' not in st.session_state: st.session_state.korak = "jezik"
if 'jezik_kljuc' not in st.session_state: st.session_state.jezik_kljuc = "srpski"

# --- FUNKCIJA ZA DINAMIČKI HEDER ---
def prikazi_heder():
    # Uzimamo prevode za trenutno izabrani jezik
    txt = master_strings[st.session_state.jezik_kljuc]
    
    c1, c2, c3, c4, c5 = st.columns([0.8, 1.4, 1, 1, 0.8])
    with c1: 
        if st.button(txt.get("home", "Home"), key="h_home"): st.session_state.korak = "home"
    with c2: 
        if st.button(txt.get("kategorija", "Kategorija"), key="h_kat"): st.session_state.korak = "kategorije"
    with c3: 
        if st.button(txt.get("stanje", "Zalihe"), key="h_zal"): st.session_state.korak = "spisak"
    with c4: 
        if st.button(txt.get("spisak", "Spisak"), key="h_spis"): st.session_state.korak = "potrebe"
    with c5: 
        if st.button(txt.get("izlaz", "Izlaz"), key="h_izl"):
            st.session_state.korak = "jezik"
            st.rerun()
    
    # Zastava i tekst jezika u istom redu
    if 'izabrani_jezik_kod' in st.session_state:
        kod = st.session_state.izabrani_jezik_kod
        naziv = st.session_state.izabrani_jezik_naziv
        path = f"icons/{kod}.png"
        f1, f2 = st.columns([1, 6])
        with f1: 
            if os.path.exists(path): st.image(path, width=25)
        with f2: 
            st.markdown(f"<div style='line-height:25px; font-weight:bold;'>{naziv}</div>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)

# --- LOGIKA EKRANA ---
prikazi_heder()

if st.session_state.korak == "jezik":
    jezici_lista = [
        ("Srpski", "Srpski"), ("Engleski", "English"), ("Nemacki", "Deutsch"),
        ("Ruski", "Русский"), ("Ukrajinski", "Українська"), ("Madjarski", "Magyar"),
        ("Spanski", "Español"), ("Portugalski", "Português"), ("Mandarinski", "中文"),
        ("Francuski", "Français")
    ]
    for i in range(0, len(jezici_lista), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(jezici_lista):
                fajl, ime = jezici_lista[i + j]
                with cols[j]:
                    path = f"icons/{fajl}.png"
                    if os.path.exists(path): st.image(path, width=35)
                    if st.button(ime, key=f"L_{fajl}"):
                        st.session_state.izabrani_jezik_kod = fajl
                        st.session_state.izabrani_jezik_naziv = ime
                        # Postavljanje ključa za master_strings
                        st.session_state.jezik_kljuc = jezik_mapa.get(fajl, "srpski")
                        st.session_state.korak = "kategorije"
                        st.rerun()
