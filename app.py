import streamlit as st
from PIL import Image
import os
import pandas as pd

# --- KONFIGURACIJA STRANICE ---
icon_path = "icons/512.png"
if os.path.exists(icon_path):
    st.set_page_config(page_title="Zalihe", page_icon=Image.open(icon_path), layout="wide")
else:
    st.set_page_config(page_title="Zalihe", page_icon="📦", layout="wide")

# --- REČNIK PREVODA (10 JEZIKA) ---
prevodi = {
    "Srpski": {"naslov": "Upravljanje zalihama", "art": "Artikl", "kol": "Količina", "dodaj": "Dodaj", "lista": "Stanje", "brisi": "Obriši"},
    "Madjarski": {"naslov": "Készletkezelés", "art": "Termék", "kol": "Mennyiség", "dodaj": "Hozzáad", "lista": "Készlet", "brisi": "Törlés"},
    "Ukrajinski": {"naslov": "Управління запасами", "art": "Товар", "kol": "Кількість", "dodaj": "Додати", "lista": "Запаси", "brisi": "Видалити"},
    "Ruski": {"naslov": "Управление запасами", "art": "Товар", "kol": "Количество", "dodaj": "Добавить", "lista": "Запасы", "brisi": "Удалить"},
    "Engleski": {"naslov": "Inventory Management", "art": "Item", "kol": "Quantity", "dodaj": "Add", "lista": "Stock", "brisi": "Delete"},
    "Nemacki": {"naslov": "Lagerverwaltung", "art": "Artikel", "kol": "Menge", "dodaj": "Hinzufügen", "lista": "Bestand", "brisi": "Löschen"},
    "Mandarinski": {"naslov": "库存管理", "art": "产品", "kol": "数量", "dodaj": "添加", "lista": "库存", "brisi": "删除"},
    "Spanski": {"naslov": "Gestión de inventario", "art": "Artículo", "kol": "Cantidad", "dodaj": "Agregar", "lista": "Stock", "brisi": "Eliminar"},
    "Portugalski": {"naslov": "Gestão de Inventário", "art": "Item", "kol": "Quantidade", "dodaj": "Adicionar", "lista": "Estoque", "brisi": "Excluir"},
    "Francuski": {"naslov": "Gestion des Stocks", "art": "Article", "kol": "Quantité", "dodaj": "Ajouter", "lista": "Stocks", "brisi": "Supprimer"}
}

# --- BAZA PODATAKA (U MEMORIJI ZA POČETAK) ---
if 'zalihe' not in st.session_state:
    st.session_state.zalihe = []

# --- SIDEBAR ---
with st.sidebar:
    if os.path.exists(icon_path):
        st.image(icon_path, width=100)
    
    izbor = st.selectbox("Izaberi jezik / Language", list(prevodi.keys()))
    t = prevodi[izbor]
    
    # Putanja do zastave (Mora biti npr. icons/Srpski.png)
    flag_path = f"icons/{izbor}.png"
    if os.path.exists(flag_path):
        st.image(flag_path, width=80)
    else:
        st.info(f"Fali slika: {flag_path}")

# --- GLAVNI SADRŽAJ ---
st.title(f"📦 {t['naslov']}")

# Unos nove robe
col1, col2, col3 = st.columns([2, 1, 1])
with col1:
    artikl = st.text_input(t['art'])
with col2:
    kolicina = st.number_input(t['kol'], min_value=0, step=1)
with col3:
    st.write(" ") # Razmak
    if st.button(t['dodaj']):
        if artikl:
            st.session_state.zalihe.append({"Artikl": artikl, "Količina": kolicina})
            st.rerun()

st.divider()

# Tabela zaliha
st.subheader(t['lista'])
if st.session_state.zalihe:
    for i, stavka in enumerate(st.session_state.zalihe):
        c1, c2, c3 = st.columns([3, 1, 1])
        c1.write(f"**{stavka['Artikl']}**")
        c2.write(f"{stavka['Količina']}")
        if c3.button(t['brisi'], key=f"del_{i}"):
            st.session_state.zalihe.pop(i)
            st.rerun()
else:
    st.write("Lista je prazna.")
