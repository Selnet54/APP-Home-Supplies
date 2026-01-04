import streamlit as st
import os
import sqlite3
from datetime import datetime, timedelta
import pandas as pd
import csv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import webbrowser
from PIL import Image  # Za rad sa slikama

# --- KONFIGURACIJA ---
st.set_page_config(
    page_title="Zalihe - Upravljanje",
    page_icon="📦",
    layout="wide"
)

# --- SESSION STATE INICIJALIZACIJA ---
if 'jezik_kljuc' not in st.session_state: 
    st.session_state.jezik_kljuc = "srpski"
if 'korak' not in st.session_state: 
    st.session_state.korak = "jezik"
if 'izabrani_jezik_kod' not in st.session_state: 
    st.session_state.izabrani_jezik_kod = "Srpski"
if 'izabrani_jezik_naziv' not in st.session_state: 
    st.session_state.izabrani_jezik_naziv = "Srpski"
if 'trenutna_kategorija' not in st.session_state:
    st.session_state.trenutna_kategorija = ""
if 'trenutna_podkategorija' not in st.session_state:
    st.session_state.trenutna_podkategorija = ""
if 'trenutni_deo_proizvoda' not in st.session_state:
    st.session_state.trenutni_deo_proizvoda = ""

# --- MASTER STRINGS - DODAJ OVDE SVE TVOJE PREVODE ---
master_strings = {
    "srpski": {
        "nazad": "Nazad", "stanje": "Zalihe", "izlaz": "Izlaz", "spisak": "Spisak", 
        # ... ostatak vašeg koda ...
        "nazad": "Nazad", "stanje": "Zalihe", "izlaz": "Izlaz", "spisak": "Spisak", 
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
        "Ostalo": "Ostalo",
		"azuriraj_proizvod": "Ažuriraj proizvod",
        "snimi_izmene": "Snimi izmene",
        "proizvod_azuriran": "Proizvod je uspešno ažuriran",
        "selektuj_proizvod": "Selektuj proizvod za ažuriranje",
        "trenutne_vrednosti": "Trenutne vrednosti:",
        "nove_vrednosti": "Nove vrednosti:",
        "potvrda_azuriranja": "Potvrda ažuriranja",
        "potvrdi_izmenu": "Potvrdi izmenu?",
        "nema_proizvoda": "Nema proizvoda za prikaz",
        "pogresan_izbor": "Pogrešan izbor",
        "pogresan_unos": "Pogrešan unos",
		"enter_nastavak": "Pritisni Enter za nastavak...",
        "izbor": "Izbor",
        		
		"popunite_polja": "Popunite sva obavezna polja",
        "kolicina_mora_broj": "Količina mora biti broj",
        "pregled_unosa": "Pregled unosa za",
        "zamrzivac_1": "Zamrzivač 1",
        "zamrzivac_2": "Zamrzivač 2",
        "zamrzivac_3": "Zamrzivač 3",
        "frizider": "Frižider",
        "ostava": "Ostava",

        "zaglavlja_zaliha": {
            "naziv": "Proizvod",
            "opis": "Opis",
            "komada": "Kom.",
            "jedinica": "Jed.",
            "kolicina": "Kol.",
            "rok_trajanja": "Rok",
            "mesto_skladistenja": "Sklad."
        },
        "zaglavlja_spisak": {
            "proizvod": "Proizvod",
            "opis": "Opis",
            "datum_unosa": "Datum unosa"
        }
    },

    "hungary": {
        "nazad": "Vissza", "stanje": "Készlet", "izlaz": "Kilépés", "spisak": "Bevásárlólista", 
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
        "Ostalo": "Egyéb", 
		"azuriraj_proizvod": "Termék frissítése",
        "snimi_izmene": "Változtatások mentése",
        "proizvod_azuriran": "Termék sikeresen frissítve",
        "selektuj_proizvod": "Válasszon terméket frissítéshez",
        "trenutne_vrednosti": "Jelenlegi értékek:",
        "nove_vrednosti": "Új értékek:",
        "potvrda_azuriranja": "Frissítés megerősítése",
        "potvrdi_izmenu": "Megerősíti a változtatásokat?",
        "nema_proizvoda": "Nincsenek megjeleníthető termékek",
        "pogresan_izbor": "Hibás választás",
        "pogresan_unos": "Hibás bevitel",
        "enter_nastavak": "Nyomja meg az Entert a folytatáshoz...",
        "izbor": "Választás",		
        
        "popunite_polja": "Töltse ki az összes kötelező mezőt",
        "kolicina_mora_broj": "A mennyiségnek számnak kell lennie",
        "pregled_unosa": "Bevitel áttekintése",
        "zamrzivac_1": "Mélyhűtő 1",
        "zamrzivac_2": "Mélyhűtő 2",
        "zamrzivac_3": "Mélyhűtő 3",
        "frizider": "Hűtőszekrény",
        "ostava": "Spájz",

        "zaglavlja_zaliha": {
            "naziv": "Termék",
            "opis": "Leírás",
            "komada": "Db.",
            "jedinica": "Egys.",
            "kolicina": "Menny.",
            "rok_trajanja": "Lejárat",
            "mesto_skladistenja": "Tárolás"
        },
        "zaglavlja_spisak": {
            "proizvod": "Termék",
            "opis": "Leírás",
            "datum_unosa": "Beviteli dátum"
        }
    },

    "ukrajinski": {
        "nazad": "Назад", "stanje": "Запаси", "izlaz": "Вихід", "spisak": "Список", 
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
        "Ostalo": "Інше",
		"azuriraj_proizvod": "Оновити продукт",
        "snimi_izmene": "Зберегти зміни",
        "proizvod_azuriran": "Продукт успішно оновлено",
        "selektuj_proizvod": "Виберіть продукт для оновлення",
        "trenutne_vrednosti": "Поточні значення:",
        "nove_vrednosti": "Нові значення:",
        "potvrda_azuriranja": "Підтвердження оновлення",
        "potvrdi_izmenu": "Підтвердити зміни?",
        "nema_proizvoda": "Немає продуктів для відображення",
        "pogresan_izbor": "Неправильний вибір",
        "pogresan_unos": "Неправильне введення",
        "enter_nastavak": "Натисніть Enter для продовження...",
        "izbor": "Вибір",
		
		"popunite_polja": "Заповніть всі обов'язкові поля",
        "kolicina_mora_broj": "Кількість повинна бути числом",
        "pregled_unosa": "Огляд введення для",
        "zamrzivac_1": "Морозилка 1",
        "zamrzivac_2": "Морозилка 2",
        "zamrzivac_3": "Морозилка 3",
        "frizider": "Холодильник",
        "ostava": "Комора",

        "zaglavlja_zaliha": {
            "naziv": "Продукт",
            "opis": "Опис",
            "komada": "Шт.",
            "jedinica": "Од.",
            "kolicina": "Кільк.",
            "rok_trajanja": "Термін",
            "mesto_skladistenja": "Склад"
        },
        "zaglavlja_spisak": {
            "proizvod": "Продукт",
            "opis": "Опис",
            "datum_unosa": "Дата внесення"
        }
    },

    "ruski": {
        "nazad": "Назад", "stanje": "Запасы", "izlaz": "Выход", "spisak": "Список", 
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
        "Ostalo": "Другое",
		"azuriraj_proizvod": "Обновить продукт",
        "snimi_izmene": "Сохранить изменения",
        "proizvod_azuriran": "Продукт успешно обновлен",
        "selektuj_proizvod": "Выберите продукт для обновления",
        "trenutne_vrednosti": "Текущие значения:",
        "nove_vrednosti": "Новые значения:",
        "potvrda_azuriranja": "Подтверждение обновления",
        "potvrdi_izmenu": "Подтвердить изменения?",
        "nema_proizvoda": "Нет продуктов для отображения",
        "pogresan_izbor": "Неверный выбор",
        "pogresan_unos": "Неверный ввод",
        "enter_nastavak": "Нажмите Enter для продолжения...",
        "izbor": "Выбор",
		
		"popunite_polja": "Заполните все обязательные поля",
        "kolicina_mora_broj": "Количество должно быть числом",
        "pregled_unosa": "Обзор ввода для",
        "zamrzivac_1": "Морозилка 1",
        "zamrzivac_2": "Морозилка 2",
        "zamrzivac_3": "Морозилка 3",
        "frizider": "Холодильник",
        "ostava": "Кладовая",
		
        "zaglavlja_zaliha": {
            "naziv": "Продукт",
            "opis": "Описание",
            "komada": "Шт.",
            "jedinica": "Ед.",
            "kolicina": "Кол-во",
            "rok_trajanja": "Срок",
            "mesto_skladistenja": "Склад"
        },
        "zaglavlja_spisak": {
            "proizvod": "Продукт",
            "opis": "Описание",
            "datum_unosa": "Дата добавления"
        }
    },

    "english": {
        "nazad": "Back", "stanje": "Inventory", "izlaz": "Exit", "spisak": "Shopping List", 
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
        "Ostalo": "Other",
		"azuriraj_proizvod": "Update product",
        "snimi_izmene": "Save changes", 
        "proizvod_azuriran": "Product successfully updated",
        "selektuj_proizvod": "Select product for update",
        "trenutne_vrednosti": "Current values:",
        "nove_vrednosti": "New values:",
        "potvrda_azuriranja": "Update confirmation",
        "potvrdi_izmenu": "Confirm changes?",
        "nema_proizvoda": "No products to display",
        "pogresan_izbor": "Wrong choice",
        "pogresan_unos": "Wrong input",
        "enter_nastavak": "Press Enter to continue...",
        "izbor": "Choice",
		
		"popunite_polja": "Fill in all required fields",
        "kolicina_mora_broj": "Quantity must be a number",
        "pregled_unosa": "Entry review for",
        "zamrzivac_1": "Freezer 1",
        "zamrzivac_2": "Freezer 2",
        "zamrzivac_3": "Freezer 3",
        "frizider": "Refrigerator",
        "ostava": "Pantry",

        "zaglavlja_zaliha": {
            "naziv": "Product", 
            "opis": "Desc.",
            "komada": "Pcs.",
            "jedinica": "Unit",
            "kolicina": "Qty.",
            "rok_trajanja": "Expiry",
            "mesto_skladistenja": "Storage"
        },
        "zaglavlja_spisak": {
            "proizvod": "Product",
            "opis": "Description",
            "datum_unosa": "Entry Date"
        }
    },

    "deutsch": {
        "nazad": "Zurück", "stanje": "Bestand", "izlaz": "Beenden", "spisak": "Einkaufsliste", 
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
        "Ostalo": "Andere",
		"azuriraj_proizvod": "Produkt aktualisieren",
        "snimi_izmene": "Änderungen speichern",
        "proizvod_azuriran": "Produkt erfolgreich aktualisiert",
        "selektuj_proizvod": "Produkt zur Aktualisierung auswählen",
        "trenutne_vrednosti": "Aktuelle Werte:",
        "nove_vrednosti": "Neue Werte:",
        "potvrda_azuriranja": "Aktualisierungsbestätigung",
        "potvrdi_izmenu": "Änderungen bestätigen?",
        "nema_proizvoda": "Keine Produkte zum Anzeigen",
        "pogresan_izbor": "Falsche Auswahl",
        "pogresan_unos": "Falsche Eingabe",
        "enter_nastavak": "Enter drücken zum Fortsetzen...",
        "izbor": "Auswahl",
		
		"popunite_polja": "Füllen Sie alle Pflichtfelder aus",
        "kolicina_mora_broj": "Menge muss eine Zahl sein",
        "pregled_unosa": "Eingabeübersicht für",
        "zamrzivac_1": "Gefrierschrank 1",
        "zamrzivac_2": "Gefrierschrank 2",
        "zamrzivac_3": "Gefrierschrank 3",
        "frizider": "Kühlschrank",
        "ostava": "Vorratskammer",
		
        "zaglavlja_zaliha": {
            "naziv": "Produkt",  
            "opis": "Beschr.",
            "komada": "Stk.",
            "jedinica": "Einheit",
            "kolicina": "Menge",
            "rok_trajanja": "Ablauf",
            "mesto_skladistenja": "Lager" 
        },
        "zaglavlja_spisak": {
            "proizvod": "Produkt",
            "opis": "Beschreibung",
            "datum_unosa": "Eintragsdatum"
        }
    },

    "mandarinski": {
        "nazad": "返回", "stanje": "库存", "izlaz": "退出", "spisak": "购物清单", 
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
        "Ostalo": "其他",
		"azuriraj_proizvod": "更新产品",
        "snimi_izmene": "保存更改",
        "proizvod_azuriran": "产品更新成功",
        "selektuj_proizvod": "选择要更新的产品",
        "trenutne_vrednosti": "当前值:",
        "nove_vrednosti": "新值:",
        "potvrda_azuriranja": "更新确认",
        "potvrdi_izmenu": "确认更改?",
        "nema_proizvoda": "没有产品可显示",
        "pogresan_izbor": "选择错误",
        "pogresan_unos": "输入错误",
        "enter_nastavak": "按Enter键继续...",
        "izbor": "选择",
		
		"popunite_polja": "请填写所有必填字段",
        "kolicina_mora_broj": "数量必须是数字",
        "pregled_unosa": "输入记录查看",
        "zamrzivac_1": "冷冻柜 1",
        "zamrzivac_2": "冷冻柜 2",
        "zamrzivac_3": "冷冻柜 3",
        "frizider": "冰箱",
        "ostava": "储藏室",

        "zaglavlja_zaliha": {
            "naziv": "产品",
            "opis": "描述",
            "komada": "件",
            "jedinica": "单位",
            "kolicina": "数量",
            "rok_trajanja": "有效期",
            "mesto_skladistenja": "存储"
        },
        "zaglavlja_spisak": {
            "proizvod": "产品",
            "opis": "描述",
            "datum_unosa": "录入日期"
        }
    },

    "espanol": {
        "nazad": "Atrás", "stanje": "Inventario", "izlaz": "Salir", "spisak": "Lista de Compras", 
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
        "Ostalo": "Otro",
		"azuriraj_proizvod": "Actualizar producto",
        "snimi_izmene": "Guardar cambios",
        "proizvod_azuriran": "Producto actualizado con éxito",
        "selektuj_proizvod": "Seleccione producto para actualizar",
        "trenutne_vrednosti": "Valores actuales:",
        "nove_vrednosti": "Nuevos valores:",
        "potvrda_azuriranja": "Confirmación de actualización",
        "potvrdi_izmenu": "¿Confirmar cambios?",
        "nema_proizvoda": "No hay productos para mostrar",
        "pogresan_izbor": "Elección incorrecta",
        "pogresan_unos": "Entrada incorrecta",
        "enter_nastavak": "Presione Enter para continuar...",
        "izbor": "Elección",
		
		"popunite_polja": "Complete todos los campos obligatorios",
        "kolicina_mora_broj": "La cantidad debe ser un número",
        "pregled_unosa": "Revisión de entrada para",
        "zamrzivac_1": "Congelador 1",
        "zamrzivac_2": "Congelador 2",
        "zamrzivac_3": "Congelador 3",
        "frizider": "Refrigerador",
        "ostava": "Despensa",

        "zaglavlja_zaliha": {
            "naziv": "Producto",
            "opis": "Descripción",
            "komada": "Unid.",
            "jedinica": "Unidad",
            "kolicina": "Cant.",
            "rok_trajanja": "Vencimiento",
            "mesto_skladistenja": "Almacén"
        },
        "zaglavlja_spisak": {
            "proizvod": "Producto",
            "opis": "Descripción",
            "datum_unosa": "Fecha de ingreso"
        }
    },

    # dodajte ovo u dictionary master_strings, posle "francais" bloka:

	"portugalski": {
		"nazad": "Voltar", "stanje": "Estoque", "izlaz": "Sair", "spisak": "Lista de Compras", 
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
		"Ostalo": "Outro",
		"azuriraj_proizvod": "Atualizar produto",
		"snimi_izmene": "Salvar alterações",
		"proizvod_azuriran": "Produto atualizado com sucesso",
		"selektuj_proizvod": "Selecione produto para atualizar",
		"trenutne_vrednosti": "Valores atuais:",
		"nove_vrednosti": "Novos valores:",
		"potvrda_azuriranja": "Confirmação de atualização",
		"potvrdi_izmenu": "Confirmar alterações?",
		"nema_proizvoda": "Nenhum produto para exibir",
		"pogresan_izbor": "Escolha incorreta",
		"pogresan_unos": "Entrada incorreta",
		"enter_nastavak": "Pressione Enter para continuar...",
		"izbor": "Escolha",
		"popunite_polja": "Preencha todos os campos obrigatórios",
		"kolicina_mora_broj": "A quantidade deve ser um número",
		"pregled_unosa": "Revisão de entrada para",
		"zamrzivac_1": "Congelador 1",
		"zamrzivac_2": "Congelador 2",
		"zamrzivac_3": "Congelador 3",
		"frizider": "Geladeira",
		"ostava": "Despensa",
    
		"zaglavlja_zaliha": {
			"naziv": "Produto",
			"opis": "Descrição",
			"komada": "Pçs.",
			"jedinica": "Unid.",
			"kolicina": "Qtd.",
			"rok_trajanja": "Validade",
			"mesto_skladistenja": "Armaz."
		},
		"zaglavlja_spisak": {
			"proizvod": "Produto",
			"opis": "Descrição",
			"datum_unosa": "Data de entrada"
		}
	},
	"francais": {
        "nazad": "Retour", "stanje": "Stock", "izlaz": "Quitter", "spisak": "Liste de Courses", 
        "naziv_proizvoda": "Produit:", "opis": "Description:", "komad": "Pièce:", 
        "kolicina": "Quantité:", "jedinica_mere": "Unité:", "datum_unosa": "Date d'entrée:", 
        "rok_trajanja": "Durée (mois):", "automatski_rok": "Expiration Auto:", 
        "mesto_skladistenja": "Stockage:", "unesi": "Entrer", "pretrazi": "Rechercher:",
        "azuriraj": "Mettre à jour", "obrisi": "Supprimer", "stampaj": "Imprimer", "posalji": "Envoyer",
        "izbor_jezika": "Choisir la langue", "pocetak": "Début", "jezik": "Langue",
        "glavne_kategorije": "Catégories Principales:", "podkategorije": "Sous-catégories -",
        "delovi_proizvoda": "Pièces du Produit -", "unos_podataka": "Saisie de Données",
        "azuriranje_proizvoda": "Mettre à jour Produit", "stanje_zалиha": "État du Stock",
        "spisak_potreba": "Liste de Courses", "posalji_spisak": "Envoyer Liste",
        "oznaci_sve": "Tout sélectionner", "kopiraj": "Copier", "posalji_email": "Envoyer Email",
        "posalji_messenger": "Envoyer Messenger", "pomoc_app_password": "Aide - Mot de passe App",
        "Ostalo": "Autre",
		"azuriraj_proizvod": "Mettre à jour le produit",
        "snimi_izmene": "Enregistrer les modifications",
        "proizvod_azuriran": "Produit mis à jour avec succès",
        "selektuj_proizvod": "Sélectionnez un produit à mettre à jour",
        "trenutne_vrednosti": "Valeurs actuelles:",
        "nove_vrednosti": "Nouvelles valeurs:",
        "potvrda_azuriranja": "Confirmation de mise à jour",
        "potvrdi_izmenu": "Confirmer les modifications?",
        "nema_proizvoda": "Aucun produit à afficher",
        "pogresan_izbor": "Choix incorrect",
        "pogresan_unos": "Entrée incorrecte",
        "enter_nastavak": "Appuyez sur Entrée pour continuer...",
        "izbor": "Choix",
		
		"popunite_polja": "Remplissez tous les champs obligatoires",
        "kolicina_mora_broj": "La quantité doit être un nombre",
        "pregled_unosa": "Aperçu des saisies pour",
        "zamrzivac_1": "Congélateur 1",
        "zamrzivac_2": "Congélateur 2",
        "zamrzivac_3": "Congélateur 3",
        "frizider": "Réfrigérateur",
        "ostava": "Garde-manger",

        "zaglavlja_zaliha": {
            "naziv": "Produit",
            "opis": "Description",
            "komada": "Pièce",
            "jedinica": "Unité",
            "kolicina": "Qté",
            "rok_trajanja": "Expiration",
            "mesto_skladistenja": "Stockage"
        },
        "zaglavlja_spisak": {
            "proizvod": "Produit",
            "opis": "Description",
            "datum_unosa": "Date d'entrée"
        }
    }
}

# --- KATEGORIJE, PODKATEGORIJE, DELOVI PROIZVODA ---

main_categories_translations = {
    "srpski": [
        "Belo meso", "Crveno meso", "Sitna divljač", "Krupna divljač",
        "Riba", "Mlečni proizvodi", "Povrće", "Zimnica i kompoti",
        "Testo i Slatkiši", "Pića", "Hemija i higijena", "Ostalo"
    ],
    "hungary": [
        "Fehér hús", "Vörös hús", "Apróvad", "Nagyvad",
        "Hal", "Tejtermékek", "Zöldség", "Befőttek és kompótok",
        "Tészta és Édességek", "Italok", "Kémia és higiénia", "Egyéb"
    ],
    "ukrajinski": [
        "Біле м'ясо", "Червоне м'ясо", "Дрібна дичина", "Велика дичина",
        "Риба", "Молочні продукти", "Овочі", "Консервація та компоти",
        "Тісто та Солодощі", "Напої", "Хімія та гігієна", "Інше"
    ],
    "ruski": [
        "Белое мясо", "Красное мясо", "Мелкая дичь", "Крупная дичь",
        "Рыба", "Молочные продукты", "Овощи", "Консервация и компоты",
        "Тесто и Сладости", "Напитки", "Химия и гигиена", "Другое"
    ],
    "english": [
        "White meat", "Red meat", "Small game", "Big game",
        "Fish", "Dairy products", "Vegetables", "Preserves and compotes",
        "Dough and Sweets", "Beverages", "Chemicals and hygiene", "Other"
    ],
    "deutsch": [
        "Weißes Fleisch", "Rotes Fleisch", "Kleinwild", "Großwild",
        "Fisch", "Milchprodukte", "Gemüse", "Konserven und Kompotte",
        "Teig und Süßigkeiten", "Getränke", "Chemie und Hygiene", "Andere"
    ],
    "mandarinski": [
        "白肉", "红肉", "小型野味", "大型野味",
        "鱼", "乳制品", "蔬菜", "蜜饯和蜜饯",
        "面团和糖果", "饮料", "化学品和卫生", "其他"
    ],
    "espanol": [
        "Carne blanca", "Carne roja", "Caza menor", "Caza mayor",
        "Pescado", "Productos lácteos", "Verduras", "Conservas y compotas",
        "Masa y Dulces", "Bebidas", "Química e higiene", "Otro"
	],
	"portugalski": [
		"Carne branca", "Carne vermelha", "Caça pequena", "Caça grossa",
		"Peixe", "Laticínios", "Vegetais", "Conservas e compotas",
		"Massa e Doces", "Bebidas", "Química e higiene", "Outro"
	],
    "francais": [
        "Viande blanche", "Viande rouge", "Petit gibier", "Gros gibier",
        "Poisson", "Produits laitiers", "Légumes", "Conserves et compotes",
        "Pâte et Sucreries", "Boissons", "Chimie et hygiène", "Autre"
    ]
}

subcategories_translations = {
    "srpski": {
        "Belo meso": ["Pileće", "Ćureće", "Guska", "Patka", "Ostalo"],
        "Crveno meso": ["Svinjsko", "Jagnjeće", "Ovčije", "Juneće", "Govedina", "Od bika", "Konjsko", "Zečije", "Ostalo"],
        "Sitna divljač": ["Prepelica", "Fazan", "Jarebica", "Divlja patka", "Divlja guska", "Divlji zec", "Golub", "Ostalo"],
        "Krupna divljač": ["Jelen", "Srna", "Divokoza", "Los", "Irvas", "Divlja svinja", "Bizon", "Kamila", "Lama", "Alpaka", "Kengur", "Krokodil/Aligator", "Gušter", "Zmija", "Ostalo"],
        "Riba": ["Morska", "Slatkovodna", "Plodovi mora", "Ostalo"],
        "Mlečni proizvodi": ["Mleko", "Mlečne prerađevine", "Ostalo"],
        "Povrće": ["Sveže", "Termički obrađeno", "Zamrznuto", "Ostalo"],
        "Zimnica i kompoti": ["Voće", "Povrće", "Ostalo"],
        "Testo i Slatkiši": ["Testo", "Slatkiši", "Ostalo"],
        "Pića": ["Voda", "Vino", "Sok", "Žestoka pića", "Pivo", "Ostalo"],
        "Hemija i higijena": ["Sanitar", "Lična higijena", "Pribor", "Ostalo"],
        "Ostalo": ["Ostalo"]
    },
    # ... (ostali jezici)
}

product_parts_translations = {
    "srpski": {
        # --- Belo meso ---
        "Pileće": ["Gril pile", "Pile celo", "Ceo batak", "Karabatak", "Donji batak", "Belo (grudi)", "File", "Leđa", "Krilca", "Medaljoni", "Nugati", "Panirani odrezak", "Mleveno", "Za supu", "Ostalo"],
        "Ćureće": ["Ceo batak", "Karabatak", "Donji batak", "Rolovani batak", "Odresci od bataka", "Belo (grudi)", "Krilca", "Leđa", "Krila", "Za supu", "Mleveno", "Ostalo"],
        "Guska": ["Belo (grudi)", "Ceo batak", "Karabatak", "Donji batak", "Krilca", "Leđa", "Vrat", "Jetra (foie gras)", "Gušćja mast", "Mleveno", "Za supu", "Ostalo"],
        "Patka": ["Belo (grudi)", "Ceo batak", "Karabatak", "Donji batak", "Krilca", "Leđa", "Vrat", "Pačija mast", "Mleveno", "Jetra", "Za supu", "Ostalo"],

        # --- Crveno meso ---
        "Svinjsko": ["Šnicla", "Karmenadla", "Vrat", "But", "Kare", "Rebra", "Grudi", "Plećka", "Podplećka", "Kolenica", "Mleveno", "Usitnjen", "Za supu", "Ostalo"],
        "Jagnjeće": ["Glava", "Vrat", "Plećka", "Slabine", "Grudi", "Bubrežnjak", "But", "Kolenica", "Ostalo"],
        "Ovčije": ["Glava", "Vrat", "Plećka", "Slabine", "Grudi", "Bubrežnjak", "But", "Kolenica", "Ostalo"],
        "Juneće": ["Biftek", "Vrat - zaplecak", "Prsa", "Lopatica", "Kolenica", "Rebra", "Potrbušina", "T-bone steak", "Ramstek", "Rib-Eye", "Rep", "Ostalo"],
        "Govedina": ["Karmedla", "Biftek", "Vrat", "Podplećka", "Grudi", "Kolenica", "Rebra", "Slabine", "Leđa", "Trbušina", "But", "Ostalo"],
        "Od bika": ["But", "Plećka", "Kare (leđa)", "Prsa i rebra", "Lopatica", "Vrat", "Slabina", "Rep", "Ostalo"],
        "Konjsko": ["But", "Plećka", "Kare (leđa)", "Vrat", "Prsa i rebra", "Biftek", "Ramstek", "Mleveno meso", "Ostalo"],
        "Zečije": ["Zadnji but", "Prednji but", "File (leđa)", "Rebra", "Ostalo"],

        # --- Sitna divljač ---
        "Prepelica": ["Celo meso", "Grudi (fileti)", "Bataci", "Jetra", "Ostalo"],
        "Fazan": ["Celo meso", "Grudi (fileti)", "Bataci", "Jetra", "Ostalo"],
        "Jarebica": ["Celo meso", "Grudi (fileti)", "Bataci", "Jetra", "Ostalo"],
        "Golub": ["Celo meso", "Grudi (fileti)", "Bataci", "Jetra", "Ostalo"],
        "Divlji zec": ["Zadnji but", "Prednji but", "File (leđa)", "Rebra", "Ostalo"],
        "Divlja patka": ["Celo meso", "Grudi (fileti)", "Bataci", "Jetra", "Ostalo"],
        "Divlja guska": ["Celo meso", "Grudi (fileti)", "Bataci", "Jetra", "Ostalo"],

        # --- Krupna divljač ---
        "Jelen": ["But", "File (leđa)", "Biftek", "Rebra", "Grudi", "Plećka", "Kolenica", "Usitnjeno", "Ostalo"],
        "Srna": ["But", "File (leđa)", "Biftek", "Rebra", "Grudi", "Plećka", "Kolenica", "Usitnjeno", "Ostalo"],
        "Divokoza": ["But", "File (leđa)", "Biftek", "Rebra", "Grudi", "Plećka", "Kolenica", "Usitnjeno", "Ostalo"],
        "Irvas": ["But", "File (leđa)", "Biftek", "Rebra", "Grudi", "Plećka", "Kolenica", "Usitnjeno", "Ostalo"],
        "Los": ["But", "File (leđa)", "Biftek", "Rebra", "Grudi", "Plećka", "Kolenica", "Usitnjeno", "Ostalo"],
        "Divlja svinja": ["But", "Plećka", "Rebra", "Slanina", "Kolenica", "Vrat", "Glava", "Ostalo"],
        "Bizon": ["But", "Plećka", "Biftek", "Ramstek", "Rebra", "Slabina", "Vrat", "Kolenica", "Ostalo"],
        "Kamila": ["But", "Plećka", "File (slabine)", "File (leđa)", "Rebra", "Grudi", "Vrat", "Grba", "Ostalo"],
        "Lama": ["But", "Plećka", "File (leđa i slabine)", "Rebra", "Vrat", "Ostalo"],
        "Alpaka": ["But", "Plećka", "File (leđa i slabine)", "Rebra", "Vrat", "Ostalo"],
        "Kengur": ["But", "Plećka", "File (leđa i slabine)", "Rebra", "Rep", "Ostalo"],
        "Krokodil/Aligator": ["Rep", "File (leđa)", "Butine", "Ostalo"],
        "Zmija": ["Trup (prstenovi)", "Ostalo"],
        "Gušter": ["Rep", "Leđa", "Butine", "Ostalo"],

        # --- Riba ---
        "Morska": ["Losos", "Tuna", "Sardina", "Bakalar", "Oslić", "Skuša", "Brancin", "Orada", "Halibut", "Haringa", "Inćuni", "Kirnja", "Ostalo"],
        "Slatkovodna": ["Šaran", "Pastrmka", "Som", "Grgeč", "Smuđ", "Tilapija", "Pangasijus", "Jesetra", "Štuka", "Beli amur", "Pirarukus", "Ostalo"],
        "Plodovi mora": ["Škampi", "Sipa", "Jakobove kapice", "Venerina školjka", "Dagnje", "Kamenice", "Školjke", "Rak", "Hobotnica", "Lignja", "Morski ježevi", "Morski krastavci", "Abalone", "Ostalo"],

        # --- Mlečni proizvodi ---
        "Mleko": ["Mleko", "Kefir", "Kisela pavlaka", "Slatka pavlaka", "Pavlaka za kuvanje", "Ostalo"],
        "Mlečne prerađevine": ["Urda", "Mladi sir", "Krem sir", "Gouda", "Edamer", "Trapist", "Kačkavalj", "Parmezan", "Gorgonzola", "Rokfor", "Halloumi", "Ostalo"],

        # --- Povrće ---
        "Sveže": ["Grašak", "Boranija", "Karfiol", "Brokoli", "Bundeva", "Paradajz", "Krastavac", "Paprika", "Ostalo"],
        "Termički obrađeno": ["Grašak", "Boranija", "Kukuruz", "Karfiol", "Brokoli", "Paprika", "Tikvice", "Spanać", "Ostalo"],
        "Zamrznuto": ["Grašak", "Boranija", "Kukuruz", "Karfiol", "Brokoli", "Paprika", "Tikvice", "Spanać", "Ostalo"],

        # --- Zimnica i kompoti ---
        "Voće": ["Kajsija", "Kruška", "Višnja", "Pekmez od jagoda", "Šljivov pekmez", "Trešnja", "Pekmez od malina", "Dunja", "Ananas", "Pekmez od manga", "Ostalo"],
        "Povrće": ["Kiseli krastavci", "Kisela paprika", "Paradajz pire", "Cvekla", "Ajvar", "Turšija", "Kiseli kupus", "Ostalo"],

        # --- Testo i Slatkiši ---
        "Testo": ["Hleb", "Raženi hleb", "Čabata", "Kukuruzni hleb", "Baguette", "Pšenično brašno", "Integralno brašno", "Heljdino brašno", "Pirinčano brašno", "Začini", "Ostalo"],
        "Slatkiši": ["Kolači", "Torte", "Peciva", "Sladoled", "Čokolada", "Bombone", "Ostalo"],

        # --- Pića ---
        "Voda": ["Mineralna", "Negazirana", "Gazirana", "Ostalo"],
        "Vino": ["Crno", "Belo", "Roze", "Ostalo"],
        "Sok": ["Voćni", "Povrtni", "Ostalo"],
        "Žestoka pića": ["Rakija", "Votka", "Viski", "Ostalo"],
        "Pivo": ["Tamno", "Svetlo", "Ostalo"],

        # --- Hemija i higijena ---
        "Sanitar": ["Pranje prozora", "Pranje posuđa", "Pranje podova", "Sredstvo za kupatilo", "Ostalo"],
        "Lična higijena": ["Dezodorans", "Brijač", "Šminka", "Sapun", "Šampon", "Krema", "Ostalo"],
        "Pribor": ["Kantica", "Kofa", "Krpa za prašinu", "Metla", "Ostalo"],
        
        # --- Ostalo ---
        "Ostalo": ["Napomena: Unesite naziv proizvoda"]
    },
    # ... (ostali jezici)
}

# --- POMOĆNE FUNKCIJE ZA JEZIKE ---
def jezik_mapa(ime_fajla):
    mape = {
        "Srpski": "srpski", 
        "Engleski": "english", 
        "Nemacki": "deutsch",
        "Ruski": "ruski", 
        "Ukrajinski": "ukrajinski", 
        "Madjarski": "hungary",
        "Spanski": "espanol", 
        "Portugalski": "portugalski", 
        "Mandarinski": "mandarinski",
        "Francuski": "francais"
    }
    return mape.get(ime_fajla, "srpski")

def t(key):
    """Funkcija za prevod na trenutni jezik"""
    try:
        return master_strings[st.session_state.jezik_kljuc].get(key, key)
    except:
        return key

# --- BAZA PODATAKA ---
def init_db():
    """Kreira tabele ako ne postoje"""
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS products
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  product_name TEXT,
                  description TEXT,
                  piece TEXT,
                  quantity REAL,
                  unit TEXT,
                  entry_date TEXT,
                  shelf_life_months INTEGER,
                  expiry_date TEXT,
                  storage_location TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS shopping_list
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  product_name TEXT,
                  description TEXT,
                  date_added TEXT)''')
    conn.commit()
    conn.close()

# --- RESPONZIVNI CSS ---
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
        div.stButton > button { 
            font-size: 16px !important; 
            height: 50px !important;
        } /* Veći font za PC */
    }

    /* Prilagođavanje za Mobilni */
    @media (max-width: 767px) {
        .block-container {
            max-width: 100% !important;
            padding-left: 5px !important;
            padding-right: 5px !important;
        }
        div.stButton > button { 
            font-size: 11px !important; 
            height: 40px !important;
        } /* Manji font za mobilni */
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

    /* Dugmad bez okvira */
    div.stButton > button {
        border: none !important;
        background: none !important;
        padding: 5px !important;
        font-weight: bold !important;
        color: black !important;
        white-space: nowrap !important;
        margin: 2px !important;
    }

    div.stButton > button:contains("Izlaz") { 
        color: red !important; 
        background-color: #ffcccc !important;
    }
    
    /* Linija separatora */
    hr { 
        margin: 10px 0 !important; 
        border-color: #ccc !important;
    }
    
    /* Kategorija dugmad sa bojama */
    .category-button {
        border-radius: 10px !important;
        margin: 5px !important;
        border: 1px solid #ddd !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- DINAMIČKI HEDER ---
def prikazi_heder():
    # CSS za podizanje hedera
    st.markdown("""
        <style>
        .main .block-container {
            padding-top: 0.5rem !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5 = st.columns([1, 1.5, 1, 1, 1])
    
    # ⭐⭐ KORISTI PAGE_NAME U KEY ZA UNIQUE ⭐⭐
    page_name = st.session_state.get('korak', 'unknown')
    
    with col1: 
        if st.button("Home", key=f"h_home_{page_name}"):  # SAMO TEKST
            st.session_state.korak = "kategorije"
            st.rerun()
    
    with col2: 
        if st.button("Kategorije", key=f"h_kat_{page_name}"):  # SAMO TEKST
            st.session_state.korak = "kategorije"
            st.rerun()
    
    with col3: 
        if st.button("Zalihe", key=f"h_zal_{page_name}"):  # SAMO TEKST
            st.session_state.korak = "zalihe"
            st.rerun()
    
    with col4: 
        if st.button("Spisak", key=f"h_spis_{page_name}"):  # SAMO TEKST
            st.session_state.korak = "spisak"
            st.rerun()
    
    with col5: 
        if st.button("Izlaz", key=f"h_izl_{page_name}"):  # SAMO TEKST
            st.session_state.korak = "jezik"
            st.rerun()
    
    st.markdown("<hr>", unsafe_allow_html=True)

# --- STRANICE APLIKACIJE ---

def stranica_jezik():
    """Stranica za odabir jezika - samo zastave i tekst jedan ispod drugog"""
    
    # Ukloni heder sa stranice za jezik
    # ne pozivaj prikazi_heder() ovde
    
    # Ukloni i naslov "Izaberite jezik"
    # st.markdown("<h2 style='text-align: center; margin-bottom: 20px;'>Izaberite jezik</h2>", unsafe_allow_html=True)
    
    # Dodaj malo prostora na vrhu
    st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)
    
    # CSS za vertikalno poravnanje
    st.markdown("""
        <style>
        .language-item {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            margin: 15px 0;
            text-align: center;
        }
        
        .language-flag {
            margin-bottom: 8px;
        }
        
        .language-button {
            width: 100%;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # PRVI RED (3 jezika)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="language-item">', unsafe_allow_html=True)
        st.markdown('<div class="language-flag">', unsafe_allow_html=True)
        st.image("icons/Srpski.png", width=45)
        st.markdown('</div>', unsafe_allow_html=True)
        if st.button("Srpski", key="lang_sr_1", use_container_width=True, type="secondary"):
            st.session_state.izabrani_jezik_kod = "Srpski"
            st.session_state.izabrani_jezik_naziv = "Srpski"
            st.session_state.jezik_kljuc = "srpski"
            st.session_state.korak = "kategorije"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="language-item">', unsafe_allow_html=True)
        st.markdown('<div class="language-flag">', unsafe_allow_html=True)
        st.image("icons/Engleski.png", width=45)
        st.markdown('</div>', unsafe_allow_html=True)
        if st.button("English", key="lang_en_2", use_container_width=True, type="secondary"):
            st.session_state.izabrani_jezik_kod = "Engleski"
            st.session_state.izabrani_jezik_naziv = "English"
            st.session_state.jezik_kljuc = "english"
            st.session_state.korak = "kategorije"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="language-item">', unsafe_allow_html=True)
        st.markdown('<div class="language-flag">', unsafe_allow_html=True)
        st.image("icons/Nemacki.png", width=45)
        st.markdown('</div>', unsafe_allow_html=True)
        if st.button("Deutsch", key="lang_de_3", use_container_width=True, type="secondary"):
            st.session_state.izabrani_jezik_kod = "Nemacki"
            st.session_state.izabrani_jezik_naziv = "Deutsch"
            st.session_state.jezik_kljuc = "deutsch"
            st.session_state.korak = "kategorije"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    # DRUGI RED (3 jezika)
    col4, col5, col6 = st.columns(3)
    
    with col4:
        st.markdown('<div class="language-item">', unsafe_allow_html=True)
        st.markdown('<div class="language-flag">', unsafe_allow_html=True)
        st.image("icons/Ruski.png", width=45)
        st.markdown('</div>', unsafe_allow_html=True)
        if st.button("Русский", key="lang_ru_4", use_container_width=True, type="secondary"):
            st.session_state.izabrani_jezik_kod = "Ruski"
            st.session_state.izabrani_jezik_naziv = "Русский"
            st.session_state.jezik_kljuc = "ruski"
            st.session_state.korak = "kategorije"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col5:
        st.markdown('<div class="language-item">', unsafe_allow_html=True)
        st.markdown('<div class="language-flag">', unsafe_allow_html=True)
        st.image("icons/Ukrajinski.png", width=45)
        st.markdown('</div>', unsafe_allow_html=True)
        if st.button("Українська", key="lang_uk_5", use_container_width=True, type="secondary"):
            st.session_state.izabrani_jezik_kod = "Ukrajinski"
            st.session_state.izabrani_jezik_naziv = "Українська"
            st.session_state.jezik_kljuc = "ukrajinski"
            st.session_state.korak = "kategorije"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col6:
        st.markdown('<div class="language-item">', unsafe_allow_html=True)
        st.markdown('<div class="language-flag">', unsafe_allow_html=True)
        st.image("icons/Madjarski.png", width=45)
        st.markdown('</div>', unsafe_allow_html=True)
        if st.button("Magyar", key="lang_hu_6", use_container_width=True, type="secondary"):
            st.session_state.izabrani_jezik_kod = "Madjarski"
            st.session_state.izabrani_jezik_naziv = "Magyar"
            st.session_state.jezik_kljuc = "hungary"
            st.session_state.korak = "kategorije"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    # TREĆI RED (3 jezika)
    col7, col8, col9 = st.columns(3)
    
    with col7:
        st.markdown('<div class="language-item">', unsafe_allow_html=True)
        st.markdown('<div class="language-flag">', unsafe_allow_html=True)
        st.image("icons/Spanski.png", width=45)
        st.markdown('</div>', unsafe_allow_html=True)
        if st.button("Español", key="lang_es_7", use_container_width=True, type="secondary"):
            st.session_state.izabrani_jezik_kod = "Spanski"
            st.session_state.izabrani_jezik_naziv = "Español"
            st.session_state.jezik_kljuc = "espanol"
            st.session_state.korak = "kategorije"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col8:
        st.markdown('<div class="language-item">', unsafe_allow_html=True)
        st.markdown('<div class="language-flag">', unsafe_allow_html=True)
        st.image("icons/Portugalski.png", width=45)
        st.markdown('</div>', unsafe_allow_html=True)
        if st.button("Português", key="lang_pt_8", use_container_width=True, type="secondary"):
            st.session_state.izabrani_jezik_kod = "Portugalski"
            st.session_state.izabrani_jezik_naziv = "Português"
            st.session_state.jezik_kljuc = "portugalski"
            st.session_state.korak = "kategorije"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col9:
        st.markdown('<div class="language-item">', unsafe_allow_html=True)
        st.markdown('<div class="language-flag">', unsafe_allow_html=True)
        st.image("icons/Mandarinski.png", width=45)
        st.markdown('</div>', unsafe_allow_html=True)
        if st.button("中文", key="lang_zh_9", use_container_width=True, type="secondary"):
            st.session_state.izabrani_jezik_kod = "Mandarinski"
            st.session_state.izabrani_jezik_naziv = "中文"
            st.session_state.jezik_kljuc = "mandarinski"
            st.session_state.korak = "kategorije"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    # ČETVRTI RED (samo francuski centriran)
    col10, col11, col12 = st.columns([1, 2, 1])
    
    with col11:
        st.markdown('<div class="language-item">', unsafe_allow_html=True)
        st.markdown('<div class="language-flag">', unsafe_allow_html=True)
        st.image("icons/Francuski.png", width=45)
        st.markdown('</div>', unsafe_allow_html=True)
        if st.button("Français", key="lang_fr_10", use_container_width=True, type="secondary"):
            st.session_state.izabrani_jezik_kod = "Francuski"
            st.session_state.izabrani_jezik_naziv = "Français"
            st.session_state.jezik_kljuc = "francais"
            st.session_state.korak = "kategorije"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
def stranica_kategorije():
    """Stranica glavnih kategorija"""
    
    # Prikazi heder
    prikazi_heder()
    
    # Naslov
    st.markdown("<h3 style='text-align: center;'>Kategorije</h3>", unsafe_allow_html=True)
    
    # DODAJ OVDE SVOJE KATEGORIJE
    # Primer:
    kategorije = [
        "Belo meso", "Crveno meso", "Sitna divljač", 
        "Krupna divljač", "Riba", "Mlečni proizvodi",
        "Povrće", "Zimnica i kompoti", "Testo i Slatkiši",
        "Pića", "Hemija i higijena", "Ostalo"
    ]
    
    # Prikaz kategorija u gridu 2x2
    for i in range(0, len(kategorije), 2):
        col1, col2 = st.columns(2)
        
        # Prva kolona u redu
        if i < len(kategorije):
            kat1 = kategorije[i]
            with col1:
                if st.button(kat1, key=f"kat_{i}", use_container_width=True):
                    st.session_state.trenutna_kategorija = kat1
                    st.session_state.korak = "podkategorije"  # ili "delovi_proizvoda"
                    st.rerun()
        
        # Druga kolona u redu
        if i + 1 < len(kategorije):
            kat2 = kategorije[i + 1]
            with col2:
                if st.button(kat2, key=f"kat_{i+1}", use_container_width=True):
                    st.session_state.trenutna_kategorija = kat2
                    st.session_state.korak = "podkategorije"  # ili "delovi_proizvoda"
                    st.rerun()
    
    # Dugme za nazad
    if st.button("⬅️ Nazad na jezike"):
        st.session_state.korak = "jezik"
        st.rerun()

# --- POMOĆNE FUNKCIJE ZA BAZU ---

def sacuvaj_u_bazu(naziv, opis, komad, kolicina, jedinica, datum_unosa, rok_meseci, datum_isteka, mesto):
    """Čuva proizvod u bazu"""
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    c.execute('''INSERT INTO products 
                 (product_name, description, piece, quantity, unit, 
                  entry_date, shelf_life_months, expiry_date, storage_location)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
              (naziv, opis, komad, kolicina, jedinica, 
               datum_unosa, rok_meseci, datum_isteka, mesto))
    conn.commit()
    conn.close()

def update_product_in_db(product_id, name, description, piece, quantity, unit):
    """Ažurira proizvod u bazi"""
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    c.execute('''UPDATE products 
                 SET product_name = ?, description = ?, piece = ?, 
                     quantity = ?, unit = ?
                 WHERE id = ?''',
              (name, description, piece, quantity, unit, product_id))
    conn.commit()
    conn.close()

def delete_product_from_db(product_id):
    """Briše proizvod iz baze"""
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    c.execute("DELETE FROM products WHERE id = ?", (product_id,))
    conn.commit()
    conn.close()

def add_to_shopping_list(product_name, description=""):
    """Dodaje proizvod u spisak potreba"""
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    
    # Proveri da li već postoji
    c.execute("SELECT * FROM shopping_list WHERE product_name = ?", (product_name,))
    if not c.fetchone():
        c.execute('''INSERT INTO shopping_list (product_name, description, date_added)
                     VALUES (?, ?, ?)''',
                 (product_name, description, datetime.now().strftime("%Y-%m-%d")))
    
    conn.commit()
    conn.close()

# --- GLAVNI TOK APLIKACIJE ---

# Inicijalizacija baze
init_db()

# Ruter za stranice
if st.session_state.korak == "jezik":
    stranica_jezik()
elif st.session_state.korak == "kategorije":
    stranica_kategorije()
elif st.session_state.korak == "podkategorije":
    # OVDE DODAJ SVOJU FUNKCIJU stranica_podkategorije()
    pass
elif st.session_state.korak == "delovi_proizvoda":
    # OVDE DODAJ SVOJU FUNKCIJU stranica_delovi_proizvoda()
    pass
elif st.session_state.korak == "unos":
    # OVDE DODAJ SVOJU FUNKCIJU stranica_unos()
    pass
elif st.session_state.korak == "zalihe":
    # OVDE DODAJ SVOJU FUNKCIJU stranica_zalihe()
    pass
elif st.session_state.korak == "spisak":
    # OVDE DODAJ SVOJU FUNKCIJU stranica_spisak()
    pass
elif st.session_state.korak == "email":
    st.title(f"📧 {t('posalji_email')}")
    st.info(f"{t('email_funkcionalnost')}")
    if st.button(f"⬅️ {t('nazad')}"):
        st.session_state.korak = "spisak"
        st.rerun()
else:
    # Fallback ako korak nije prepoznat
    st.session_state.korak = "jezik"
    st.rerun()
