import streamlit as st
from PIL import Image
import os
import pandas as pd

# --- 1. PODEŠAVANJA ---
st.set_page_config(page_title="Zalihe", layout="wide")

# --- 2. REČNIK PREVODA ZA SVE JEZIKE ---
# Ovde definišemo šta se ispisuje za svaki jezik
prevodi = {
    "Srpski": {"naslov": "Sistem za zalihe", "kat": "Kategorija", "podkat": "Podkategorija", "proizvod": "Naziv proizvoda", "kol": "Količina", "dodaj": "Snimi", "lista": "Stanje zaliha", "brisi": "Obriši"},
    "Engleski": {"naslov": "Inventory System", "kat": "Category", "podkat": "Subcategory", "proizvod": "Product Name", "kol": "Quantity", "dodaj": "Save", "lista": "Stock List", "brisi": "Delete"},
    "Nemacki": {"naslov": "Lagersystem", "kat": "Kategorie", "podkat": "Unterkategorie", "proizvod": "Produktname", "kol": "Menge", "dodaj": "Speichern", "lista": "Lagerliste", "brisi": "Löschen"},
    "Ruski": {"naslov": "Система запасов", "kat": "Категория", "podkat": "Подкатегория", "proizvod": "Название товара", "kol": "Количество", "dodaj": "Сохранить", "lista": "Список запасов", "brisi": "Удалить"},
    "Ukrajinski": {"naslov": "Система запасів", "kat": "Категорія", "podkat": "Підкатегорія", "proizvod": "Назва товару", "kol": "Кількість", "dodaj": "Зберегти", "lista": "Список запасів", "brisi": "Видалити"},
    "Madjarski": {"naslov": "Készletrendszer", "kat": "Kategória", "podkat": "Alkategória", "proizvod": "Termék neve", "kol": "Mennyiség", "dodaj": "Mentés", "lista": "Készletlista", "brisi": "Törlés"},
    "Francuski": {"naslov": "Système de stock", "kat": "Catégorie", "podkat": "Sous-catégorie", "proizvod": "Nom du produit", "kol": "Quantité", "dodaj": "Enregistrer", "lista": "Liste de stock", "brisi": "Supprimer"},
    "Spanski": {"naslov": "Sistema de inventario", "kat": "Categoría", "podkat": "Subcategoría", "proizvod": "Nombre del producto", "kol": "Cantidad", "dodaj": "Guardar", "lista": "Lista de stock", "brisi": "Eliminar"},
    "Portugalski": {"naslov": "Sistema de inventário", "kat": "Categoria", "podkat": "Subcategoria", "proizvod": "Nome do produto", "kol": "Quantidade", "dodaj": "Salvar", "lista": "Lista de estoque", "brisi": "Excluir"},
    "Mandarinski": {"naslov": "库存系统", "kat": "类别", "podkat": "子类别", "proizvod": "产品名称", "kol": "数量", "dodaj": "保存", "lista": "库存 list", "brisi": "删除"}
}

# --- 3. SIDEBAR (IZBOR JEZIKA) ---
with st.sidebar:
    if os.path.exists("icons/512.png"):
        st.image("icons/512.png", width=120)
    
    # Korisnik bira jezik
    izabrani_jezik = st.selectbox("Language / Jezik", list(prevodi.keys()))
    
    # Uzimamo prevode za taj izabrani jezik
    txt = prevodi[izabrani_jezik]
    
    # Zastava
    if os.path.exists(f"icons/{izabrani_jezik}.png"):
        st.image(f"icons/{izabrani_jezik}.png", width=80)

# --- 4. DIZAJN DUGMADI (BOJE) ---
st.markdown(f"""
    <style>
    div.stButton > button {{
        background-color: #28a745; /* Zelena za snimanje */
        color: white;
        border-radius: 8px;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 5. GLAVNI EKRAN ---
st.header(f"📦 {txt['naslov']}")

# Kategorije (One ostaju na tvom jeziku jer su to tvoji podaci)
meni = {
    "Hrana": ["Špajz", "Zamrzivač", "Frižider"],
    "Higijena": ["Kupatilo", "Kuhinja"],
    "Alat": ["Garaža", "Podrum"]
}

if 'baza' not in st.session_state:
    st.session_state.baza = pd.DataFrame(columns=["Kat", "Podkat", "Ime", "Kol"])

with st.container():
    c1, c2 = st.columns(2)
    with c1:
        kategorija = st.selectbox(txt['kat'], list(meni.keys()))
        podkategorija = st.selectbox(txt['podkat'], meni[kategorija])
    with c2:
        ime_proizvoda = st.text_input(txt['proizvod'])
        kolicina_proizvoda = st.number_input(txt['kol'], min_value=0)

    if st.button(txt['dodaj']):
        nova_red = pd.DataFrame([[kategorija, podkategorija, ime_proizvoda, kolicina_proizvoda]], 
                                columns=["Kat", "Podkat", "Ime", "Kol"])
        st.session_state.baza = pd.concat([st.session_state.baza, nova_red], ignore_index=True)
        st.success("OK!")

st.divider()
st.subheader(txt['lista'])
st.table(st.session_state.baza)
