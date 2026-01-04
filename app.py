import streamlit as st
import os

# --- KONFIGURACIJA ---
st.set_page_config(page_title="Zalihe", layout="wide")

# --- MASTER STRINGS (Tvoj rečnik sa svim jezicima) ---
master_strings = {
    "srpski": {
        "nazad": "Nazad", "stanje": "Zalihe", "izlaz": "Izlaz", "spisak": "Spisak", "home": "Home", "kategorija": "Kategorija",
        "naziv_proizvoda": "Proizvod:", "opis": "Opis:", "komad": "Komad:", 
        "kolicina": "Količina:", "jedinica_mere": "Jed. mere:", "datum_unosa": "Datum unosa:", 
        "rok_trajanja": "Rok (meseci):", "automatski_rok": "Automatski rok:", 
        "mesto_skladistenja": "Skladište:", "unesi": "Unesi", "pretrazi": "Pretraži:",
        "azuriraj": "Ažuriraj", "obrisi": "Obriši", "stampaj": "Štampaj", "posalji": "Pošalji",
        "izbor_jezika": "Izaberite jezik", "pocetak": "Početak", "jezik": "Jezik",
        "glavne_kategorije": "Glavne kategorije:", "podkategorije": "Podkategorije -",
        "delovi_proizvoda": "Delovi proizvoda -", "unos_podataka": "Unos podataka",
        "azuriranje_proizvoda": "Ažuriranje proizvoda", "stanje_zaliha": "Stanje zaliha",
        "spisak_potreba": "Spisak potreba", "posalji_spisak": "Pošalji spisak",
        "oznaci_sve": "Označi sve", "kopiraj": "Kopiraj", "posalji_email": "Pošalji Email",
        "posalji_messenger": "Pošalji Messenger", "pomoc_app_password": "Pomoć - App Password",
        "Ostalo": "Ostalo"
    },
    "hungary": {
        "nazad": "Vissza", "stanje": "Készlet", "izlaz": "Kilépés", "spisak": "Bevásárlólista", "home": "Főoldal", "kategorija": "Kategória",
        "naziv_proizvoda": "Termék:", "opis": "Leírás:", "komad": "Darab:", 
        "kolicina": "Mennyiség:", "jedinica_mere": "Mértékegység:", "datum_unosa": "Beírás dátuma:", 
        "rok_trajanja": "Szavatosság (hónap):", "automatski_rok": "Automatikus lejárat:", 
        "mesto_skladistenja": "Raktár:", "unesi": "Bevitel", "pretrazi": "Keresés:",
        "azuriraj": "Frissítés", "obrisi": "Törlés", "stampaj": "Nyomtatás", "posalji": "Küldés",
        "izbor_jezika": "Válasszon nyelvet", "pocetak": "Kezdés", "jezik": "Nyelv",
        "glavne_kategorije": "Fő kategóriák:", "podkategorije": "Alkategóriák -",
        "delovi_proizvoda": "Termék részei -", "unos_podataka": "Adatbevitel",
        "azuriranje_proizvoda": "Termék frissítése", "stanje_zaliha": "Készlet állapota",
        "spisak_potreba": "Bevásárlólista", "posalji_spisak": "Lista küldése",
        "oznaci_sve": "Összes kijelölése", "kopiraj": "Másolás", "posalji_email": "Email küldése",
        "posalji_messenger": "Messenger küldése", "pomoc_app_password": "Súgó - App Jelszó",
        "Ostalo": "Egyéb"
    },
    "ukrajinski": {
        "nazad": "Назад", "stanje": "Запаси", "izlaz": "Вихід", "spisak": "Список", "home": "Головна", "kategorija": "Категорія",
        "naziv_proizvoda": "Продукт:", "opis": "Опис:", "komad": "Штука:", 
        "kolicina": "Кількість:", "jedinica_mere": "Од. виміру:", "datum_unosa": "Дата внесення:", 
        "rok_trajanja": "Термін (місяці):", "automatski_rok": "Авто термін:", 
        "mesto_skladistenja": "Сховище:", "unesi": "Внести", "pretrazi": "Пошук:",
        "azuriraj": "Оновити", "obrisi": "Видалити", "stampaj": "Друк", "posalji": "Надіслати",
        "izbor_jezika": "Виберіть мову", "pocetak": "Початок", "jezik": "Мова",
        "glavne_kategorije": "Основні категорії:", "podkategorije": "Підкатегорії -",
        "delovi_proizvoda": "Частини продукту -", "unos_podataka": "Введення даних",
        "azuriranje_proizvoda": "Оновлення продукту", "stanje_zaliha": "Стан запасів",
        "spisak_potreba": "Список потреб", "posalji_spisak": "Надіслати список",
        "oznaci_sve": "Вибрати все", "kopiraj": "Копіювати", "posalji_email": "Надіслати Email",
        "posalji_messenger": "Надіслати Messenger", "pomoc_app_password": "Допомога - App Пароль",
        "Ostalo": "Інше"
    },
    "ruski": {
        "nazad": "Назад", "stanje": "Запасы", "izlaz": "Выход", "spisak": "Список", "home": "Главная", "kategorija": "Категория",
        "naziv_proizvoda": "Продукт:", "opis": "Описание:", "komad": "Штука:", 
        "kolicina": "Количество:", "jedinica_mere": "Ед. изм.:", "datum_unosa": "Дата внесения:", 
        "rok_trajanja": "Срок (месяцы):", "automatski_rok": "Авто срок:", 
        "mesto_skladistenja": "Склад:", "unesi": "Внести", "pretrazi": "Поиск:",
        "azuriraj": "Обновить", "obrisi": "Удалить", "stampaj": "Печать", "posalji": "Отправить",
        "izbor_jezika": "Выберите язык", "pocetak": "Начало", "jezik": "Язык",
        "glavne_kategorije": "Основные категории:", "podkategorije": "Подкатегории -",
        "delovi_proizvoda": "Части продукта -", "unos_podataka": "Ввод данных",
        "azuriranje_proizvoda": "Обновление продукта", "stanje_zaliha": "Состояние запасов",
        "spisak_potreba": "Список потребностей", "posalji_spisak": "Отправить список",
        "oznaci_sve": "Выбрать все", "kopiraj": "Копировать", "posalji_email": "Отправить Email",
        "posalji_messenger": "Отправить Messenger", "pomoc_app_password": "Помощь - App Пароль",
        "Ostalo": "Другое"
    },
    "english": {
        "nazad": "Back", "stanje": "Inventory", "izlaz": "Exit", "spisak": "Shopping List", "home": "Home", "kategorija": "Category",
        "naziv_proizvoda": "Product:", "opis": "Description:", "komad": "Piece:", 
        "kolicina": "Quantity:", "jedinica_mere": "Unit:", "datum_unosa": "Entry Date:", 
        "rok_trajanja": "Shelf Life (months):", "automatski_rok": "Auto Expiry:", 
        "mesto_skladistenja": "Storage:", "unesi": "Enter", "pretrazi": "Search:",
        "azuriraj": "Update", "obrisi": "Delete", "stampaj": "Print", "posalji": "Send",
        "izbor_jezika": "Choose Language", "pocetak": "Start", "jezik": "Language",
        "glavne_kategorije": "Main Categories:", "podkategorije": "Subcategories -",
        "delovi_proizvoda": "Product Parts -", "unos_podataka": "Data Entry",
        "azuriranje_proizvoda": "Update Product", "stanje_zaliha": "Inventory Status",
        "spisak_potreba": "Shopping List", "posalji_spisak": "Send List",
        "oznaci_sve": "Select All", "kopiraj": "Copy", "posalji_email": "Send Email",
        "posalji_messenger": "Send Messenger", "pomoc_app_password": "Help - App Password",
        "Ostalo": "Other"
    },
    "deutsch": {
        "nazad": "Zurück", "stanje": "Bestand", "izlaz": "Beenden", "spisak": "Einkaufsliste", "home": "Start", "kategorija": "Kategorie",
        "naziv_proizvoda": "Produkt:", "opis": "Beschreibung:", "komad": "Stück:", 
        "kolicina": "Menge:", "jedinica_mere": "Einheit:", "datum_unosa": "Eingangsdatum:", 
        "rok_trajanja": "Haltbarkeit (Monate):", "automatski_rok": "Auto Ablauf:", 
        "mesto_skladistenja": "Lager:", "unesi": "Eingeben", "pretrazi": "Suchen:",
        "azuriraj": "Aktualisieren", "obrisi": "Löschen", "stampaj": "Drucken", "posalji": "Senden",
        "izbor_jezika": "Sprache auswählen", "pocetak": "Start", "jezik": "Sprache",
        "glavne_kategorije": "Hauptkategorien:", "podkategorije": "Unterkategorien -",
        "delovi_proizvoda": "Produktteile -", "unos_podataka": "Dateneingabe",
        "azuriranje_proizvoda": "Produkt aktualisieren", "stanje_zaliha": "Bestandsstatus",
        "spisak_potreba": "Einkaufsliste", "posalji_spisak": "Liste senden",
        "oznaci_sve": "Alle auswählen", "kopiraj": "Kopieren", "posalji_email": "Email senden",
        "posalji_messenger": "Messenger senden", "pomoc_app_password": "Hilfe - App Passwort",
        "Ostalo": "Andere"
    },
    "mandarinski": {
        "nazad": "返回", "stanje": "库存", "izlaz": "退出", "spisak": "购物清单", "home": "首页", "kategorija": "类别",
        "naziv_proizvoda": "产品:", "opis": "描述:", "komad": "件:", 
        "kolicina": "数量:", "jedinica_mere": "单位:", "datum_unosa": "录入日期:", 
        "rok_trajanja": "保质期(月):", "automatski_rok": "自动到期:", 
        "mesto_skladistenja": "存储:", "unesi": "输入", "pretrazi": "搜索:",
        "azuriraj": "更新", "obrisi": "删除", "stampaj": "打印", "posalji": "发送",
        "izbor_jezika": "选择语言", "pocetak": "开始", "jezik": "语言",
        "glavne_kategorije": "主要类别:", "podkategorije": "子类别 -",
        "delovi_proizvoda": "产品部件 -", "unos_podataka": "数据输入",
        "azuriranje_proizvoda": "更新产品", "stanje_zaliha": "库存状态",
        "spisak_potreba": "购物清单", "posalji_spisak": "发送列表",
        "oznaci_sve": "全选", "kopiraj": "复制", "posalji_email": "发送邮件",
        "posalji_messenger": "发送Messenger", "pomoc_app_password": "帮助 - 应用密码",
        "Ostalo": "其他"
    },
    "espanol": {
        "nazad": "Atrás", "stanje": "Inventario", "izlaz": "Salir", "spisak": "Lista de Compras", "home": "Inicio", "kategorija": "Categoría",
        "naziv_proizvoda": "Producto:", "opis": "Descripción:", "komad": "Pieza:", 
        "kolicina": "Cantidad:", "jedinica_mere": "Unidad:", "datum_unosa": "Fecha de Entrada:", 
        "rok_trajanja": "Caducidad (meses):", "automatski_rok": "Vencimiento Auto:", 
        "mesto_skladistenja": "Almacenamiento:", "unesi": "Ingresar", "pretrazi": "Buscar:",
        "azuriraj": "Actualizar", "obrisi": "Eliminar", "stampaj": "Imprimir", "posalji": "Enviar",
        "izbor_jezika": "Elija idioma", "pocetak": "Inicio", "jezik": "Idioma",
        "glavne_kategorije": "Categorías Principales:", "podkategorije": "Subcategorías -",
        "delovi_proizvoda": "Partes del Producto -", "unos_podataka": "Entrada de Datos",
        "azuriranje_proizvoda": "Actualizar Producto", "stanje_zaliha": "Estado del Inventario",
        "spisak_potreba": "Lista de Compras", "posalji_spisak": "Enviar Lista",
        "oznaci_sve": "Seleccionar Todo", "kopiraj": "Copiar", "posalji_email": "Enviar Email",
        "posalji_messenger": "Enviar Messenger", "pomoc_app_password": "Ayuda - Contraseña App",
        "Ostalo": "Otro"
    },
    "portugalski": {
        "nazad": "Voltar", "stanje": "Estoque", "izlaz": "Sair", "spisak": "Lista", "home": "Início", "kategorija": "Categoria",
        "naziv_proizvoda": "Produto:", "opis": "Descrição:", "komad": "Peça:", 
        "kolicina": "Quantidade:", "jedinica_mere": "Unidade:", "datum_unosa": "Data de Entrada:", 
        "rok_trajanja": "Validade (meses):", "automatski_rok": "Validade Auto:", 
        "mesto_skladistenja": "Armazenamento:", "unesi": "Inserir", "pretrazi": "Pesquisar:",
        "azuriraj": "Atualizar", "obrisi": "Excluir", "stampaj": "Imprimir", "posalji": "Enviar",
        "izbor_jezika": "Escolha o idioma", "pocetak": "Início", "jezik": "Idioma",
        "glavne_kategorije": "Categorias Principais:", "podkategorije": "Subcategorias -",
        "delovi_proizvoda": "Partes do Produto -", "unos_podataka": "Entrada de Dados",
        "azuriranje_proizvoda": "Atualizar Produto", "stanje_zaliha": "Status do Estoque",
        "spisak_potreba": "Lista de Compras", "posalji_spisak": "Enviar Lista",
        "oznaci_sve": "Selecionar Tudo", "kopiraj": "Copiar", "posalji_email": "Enviar Email",
        "posalji_messenger": "Enviar Messenger", "pomoc_app_password": "Ajuda - Senha App",
        "Ostalo": "Outro"
    },
    "francais": {
        "nazad": "Retour", "stanje": "Stock", "izlaz": "Quitter", "spisak": "Liste", "home": "Accueil", "kategorija": "Catégorie",
        "naziv_proizvoda": "Produit:", "opis": "Description:", "komad": "Pièce:", 
        "kolicina": "Quantité:", "jedinica_mere": "Unité:", "datum_unosa": "Date d'entrée:", 
        "rok_trajanja": "Durée (mois):", "automatski_rok": "Expiration Auto:", 
        "mesto_skladistenja": "Stockage:", "unesi": "Entrer", "pretrazi": "Rechercher:",
        "azuriraj": "Mettre à jour", "obrisi": "Supprimer", "stampaj": "Imprimir", "posalji": "Envoyer",
        "izbor_jezika": "Choisir la langue", "pocetak": "Début", "jezik": "Langue",
        "glavne_kategorije": "Catégories Principales:", "podkategorije": "Sous-catégories -",
        "delovi_proizvoda": "Pièces du Produit -", "unos_podataka": "Saisie de Données",
        "azuriranje_proizvoda": "Mettre à jour Produit", "stanje_zaliha": "État du Stock",
        "spisak_potreba": "Liste de Courses", "posalji_spisak": "Envoyer Liste",
        "oznaci_sve": "Tout sélectionner", "kopiraj": "Copier", "posalji_email": "Envoyer Email",
        "posalji_messenger": "Envoyer Messenger", "pomoc_app_password": "Aide - Mot de passe App",
        "Ostalo": "Autre"
    }
}

# --- POMOĆNA MAPA ZA JEZIKE ---
jezik_mapa = {
    "Srpski": "srpski", "Engleski": "english", "Nemacki": "deutsch",
    "Ruski": "ruski", "Ukrajinski": "ukrajinski", "Madjarski": "hungary",
    "Spanski": "espanol", "Portugalski": "portugalski", "Mandarinski": "mandarinski",
    "Francuski": "francais"
}

# --- CSS ZA RESPONZIVNI DIZAJN ---
st.markdown("""
    <style>
    .block-container { padding-top: 5px !important; }
    
    @media (min-width: 768px) {
        .block-container { max-width: 850px !important; margin: auto; }
        div.stButton > button { font-size: 16px !important; }
    }
    
    @media (max-width: 767px) {
        .block-container { max-width: 100% !important; padding: 0 5px !important; }
        div.stButton > button { font-size: 11px !important; }
    }

    [data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        justify-content: space-between !important;
        gap: 2px !important;
    }

    div.stButton > button {
        border: none !important; background: none !important; padding: 5px 2px !important;
        font-weight: bold !important; color: black !important; white-space: nowrap !important;
    }

    /* KATEGORIJA POMERENA UDESNO */
    div.stButton > button[key="h_kat"] {
        margin-left: 10px !important;
    }

    div.stButton > button:contains("Izlaz") { color: red !important; }
    hr { margin: 5px 0 !important; border: 0.5px solid #ddd !important; }
    </style>
    """, unsafe_allow_html=True)

# --- INICIJALIZACIJA ---
if 'korak' not in st.session_state: st.session_state.korak = "jezik"
if 'jezik_kljuc' not in st.session_state: st.session_state.jezik_kljuc = "srpski"

# --- FUNKCIJA ZA HEDER ---
def prikazi_heder():
    txt = master_strings.get(st.session_state.jezik_kljuc, master_strings["srpski"])
    
    c1, c2, c3, c4, c5 = st.columns([1, 1.6, 1, 1, 0.9])
    with c1: st.button(txt["home"], key="h_home")
    with c2: st.button(txt["kategorija"], key="h_kat")
    with c3: st.button(txt["stanje"], key="h_zal")
    with c4: st.button(txt["spisak"], key="h_spis")
    with c5: 
        if st.button(txt["izlaz"], key="h_izl"):
            st.session_state.korak = "jezik"
            st.rerun()

    if 'izabrani_jezik_kod' in st.session_state:
        kod = st.session_state.izabrani_jezik_kod
        naziv = st.session_state.izabrani_jezik_naziv
        path = f"icons/{kod}.png"
        f1, f2 = st.columns([0.15, 0.85])
        with f1:
            if os.path.exists(path): st.image(path, width=28)
        with f2:
            st.markdown(f"<div style='line-height:28px; font-weight:bold; font-size:14px;'>{naziv}</div>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)

# --- PROGRAM ---
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
                    if os.path.exists(path): st.image(path, width=45)
                    if st.button(ime, key=f"L_{fajl}"):
                        st.session_state.izabrani_jezik_kod = fajl
                        st.session_state.izabrani_jezik_naziv = ime
                        st.session_state.jezik_kljuc = jezik_mapa.get(fajl, "srpski")
                        st.session_state.korak = "kategorije"
                        st.rerun()

elif st.session_state.korak == "kategorije":
    st.write(master_strings[st.session_state.jezik_kljuc]["glavne_kategorije"])
    # Ovde dalje ide tvoj kod za bazu i unos...
