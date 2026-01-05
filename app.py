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
        "azuriranje_proизvoda": "Обновление продукта", "stanje_zaliha": "Состояние запасов",
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
        "naziv_proизvoda": "产品:", "opis": "描述:", "komad": "件:", 
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
    },
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
},

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
    "hungary": {
        "Fehér hús": ["Csirke", "Pulyka", "Libacomb", "Kacsa", "Egyéb"],
        "Vörös hús": ["Sertéshús", "Bárányhús", "Juhhús", "Borjúhús", "Marhahús", "Bikahús", "Lóhús", "Nyúlhús", "Egyéb"],
        "Apróvad": ["Fürj", "Fácán", "Fogoly", "Vadkacsa", "Vadliba", "Vadnyúl", "Galamb", "Egyéb"],
        "Nagyvad": ["Szarvac", "Őz", "Vadkecske", "Jávorszarvas", "Rénszarvas", "Vadkan", "Bölény", "Teve", "Láma", "Alpaka", "Kenguru", "Krokodil/Alligátor", "Gyík", "Kígyó", "Egyéb"],
        "Hal": ["Tengeri", "Édesvízi", "Tenger gyümölcsei", "Egyéb"],
        "Tejtermékek": ["Tej", "Tejfeldolgozások", "Egyéb"],
        "Zöldség": ["Friss", "Hőkezelt", "Fagyasztott", "Egyéb"],
        "Befőttek és kompótok": ["Gyümölcs", "Zöldség", "Egyéb"],
        "Tészta és Édességek": ["Tészta", "Édességek", "Egyéb"],
        "Italok": ["Víz", "Bor", "Lé", "Tömény italok", "Sör", "Egyéb"],
        "Kémia és higiénia": ["WC", "Személyes higiénia", "Felszerelés", "Egyéb"],
        "Egyéb": ["Egyéb"]
    },
    "ukrajinski": {
        "Біле м'ясо": ["Курятина", "Індичка", "Гуска", "Качка", "Інше"],
        "Червоне м'ясо": ["Свинина", "Ягнятина", "Баранина", "Телятина", "Яловичина", "Бичатина", "Конина", "Кролик", "Інше"],
        "Дрібна дичина": ["Перепілка", "Фазан", "Куріпка", "Дика качка", "Дика гуска", "Заєць", "Голуб", "Інше"],
        "Велика дичина": ["Олень", "Косуля", "Козуль", "Лось", "Північний олень", "Дикий кабан", "Бізон", "Верблюд", "Лама", "Альпака", "Кенгуру", "Крокодил/Алігатор", "Ящірка", "Змія", "Інше"],
        "Риба": ["Морська", "Прісноводна", "Морепродукти", "Інше"],
        "Молочні продукти": ["Молоко", "Молочні переробки", "Інше"],
        "Овочі": ["Свіжі", "Термічно оброблені", "Заморожені", "Інше"],
        "Консервація та компоти": ["Фрукти", "Овочі", "Інше"],
        "Тісто та Солодощі": ["Тісто", "Солодощі", "Інше"],
        "Напої": ["Вода", "Вино", "Сік", "Міцні напої", "Пиво", "Інше"],
        "Хімія та гігієна": ["Санітарія", "Особиста гігієна", "Приладдя", "Інше"],
        "Інше": ["Інше"]
    },
    "ruski": {
        "Белое мясо": ["Курица", "Индейка", "Гусь", "Утка", "Другое"],
        "Красное мясо": ["Свинина", "Баранина", "Овца", "Телятина", "Говядина", "Бык", "Конина", "Кролик", "Другое"],
        "Мелкая дичь": ["Перепел", "Фазан", "Куропатка", "Дикая утка", "Дикий гусь", "Заяц", "Голубь", "Другое"],
        "Крупная дичь": ["Олень", "Косуля", "Дикая коза", "Лось", "Северный олень", "Кабан", "Бизон", "Верблюд", "Лама", "Альпака", "Кенгуру", "Крокодил/Аллигатор", "Ящерица", "Змея", "Другое"],
        "Рыба": ["Морская", "Пресноводная", "Морепродукты", "Другое"],
        "Молочные продукты": ["Молоко", "Молочные переработки", "Другое"],
        "Овощи": ["Свежие", "Термически обработанные", "Замороженные", "Другое"],
        "Консервация и компоты": ["Фрукты", "Овощи", "Другое"],
        "Тесто и Сладости": ["Тесто", "Сладости", "Другое"],
        "Напитки": ["Вода", "Вино", "Сок", "Крепкие напитки", "Пиво", "Другое"],
        "Химия и гигиена": ["Сантехника", "Личная гигиена", "Оборудование", "Другое"],
        "Другое": ["Другое"]
    },
    "english": {
        "White meat": ["Chicken", "Turkey", "Goose", "Duck", "Other"],
        "Red meat": ["Pork", "Lamb", "Sheep", "Veal", "Beef", "Bull", "Horse", "Rabbit", "Other"],
        "Small game": ["Quail", "Pheasant", "Partridge", "Wild duck", "Wild goose", "Hare", "Pigeon", "Other"],
        "Big game": ["Deer", "Roe deer", "Wild goat", "Moose", "Reindeer", "Wild boar", "Bison", "Camel", "Llama", "Alpaca", "Kangaroo", "Crocodile/Alligator", "Lizard", "Snake", "Other"],
        "Fish": ["Sea", "Freshwater", "Seafood", "Other"],
        "Dairy products": ["Milk", "Dairy processing", "Other"],
        "Vegetables": ["Fresh", "Heat treated", "Frozen", "Other"],
        "Preserves and compotes": ["Fruits", "Vegetables", "Other"],
        "Dough and Sweets": ["Dough", "Sweets", "Other"],
        "Beverages": ["Water", "Wine", "Juice", "Spirits", "Beer", "Other"],
        "Chemicals and hygiene": ["Sanitary", "Personal hygiene", "Equipment", "Other"],
        "Other": ["Other"]
    },
    "deutsch": {
        "Weißes Fleisch": ["Huhn", "Truthahn", "Gans", "Ente", "Andere"],
        "Rotes Fleisch": ["Schwein", "Lamm", "Schaf", "Kalb", "Rind", "Bulle", "Pferd", "Kaninchen", "Andere"],
        "Kleinwild": ["Wachtel", "Fasan", "Rebhuhn", "Wildente", "Wildgans", "Hase", "Taube", "Andere"],
        "Großwild": ["Hirsch", "Reh", "Wildziege", "Elch", "Rentier", "Wildschwein", "Bison", "Kamel", "Lama", "Alpaka", "Känguru", "Krokodil/Alligator", "Eidechse", "Schlange", "Andere"],
        "Fisch": ["Meer", "Süßwasser", "Meeresfrüchte", "Andere"],
        "Milchprodukte": ["Milch", "Milchverarbeitung", "Andere"],
        "Gemüse": ["Frisch", "Wärmebehandelt", "Gefroren", "Andere"],
        "Konserven und Kompotte": ["Früchte", "Gemüse", "Andere"],
        "Teig und Süßigkeiten": ["Teig", "Süßigkeiten", "Andere"],
        "Getränke": ["Wasser", "Wein", "Saft", "Spirituosen", "Bier", "Andere"],
        "Chemie und Hygiene": ["Sanitär", "Persönliche Hygiene", "Ausrüstung", "Andere"],
        "Andere": ["Andere"]
    },
    "mandarinski": {
        "白肉": ["鸡", "火鸡", "鹅", "鸭", "其他"],
        "红肉": ["猪肉", "羊肉", "羊", "小牛肉", "牛肉", "公牛", "马肉", "兔肉", "其他"],
        "小型野味": ["鹌鹑", "野鸡", "鹧鸪", "野鸭", "野鹅", "野兔", "鸽子", "其他"],
        "大型野味": ["鹿", "狍子", "野山羊", "驼鹿", "驯鹿", "野猪", "野牛", "骆驼", "羊驼", "袋鼠", "鳄鱼", "蜥蜴", "蛇", "其他"],
        "鱼": ["海鱼", "淡水鱼", "海鲜", "其他"],
        "乳制品": ["牛奶", "乳制品加工", "其他"],
        "蔬菜": ["新鲜", "热处理", "冷冻", "其他"],
        "蜜饯和蜜饯": ["水果", "蔬菜", "其他"],
        "面团和糖果": ["面团", "糖果", "其他"],
        "饮料": ["水", "葡萄酒", "果汁", "烈酒", "啤酒", "其他"],
        "化学品和卫生": ["卫生", "个人卫生", "设备", "其他"],
        "其他": ["其他"]
    },
    "espanol": {
        "Carne blanca": ["Pollo", "Pavo", "Ganso", "Pato", "Otro"],
        "Carne roja": ["Cerdo", "Cordero", "Oveja", "Ternera", "Res", "Toro", "Caballo", "Conejo", "Otro"],
        "Caza menor": ["Codorniz", "Faisán", "Perdiz", "Pato salvaje", "Ganso salvaje", "Liebre", "Paloma", "Otro"],
        "Caza mayor": ["Ciervo", "Corzo", "Cabra salvaje", "Alce", "Reno", "Jabalí", "Bisonte", "Camello", "Llama", "Alpaca", "Canguro", "Cocodrilo/Caimán", "Lagarto", "Serpiente", "Otro"],
        "Pescado": ["Mar", "Agua dulce", "Mariscos", "Otro"],
        "Productos lácteos": ["Leche", "Procesamiento lácteo", "Otro"],
        "Verduras": ["Frescas", "Tratadas térmicamente", "Congeladas", "Otro"],
        "Conservas y compotas": ["Frutas", "Verduras", "Otro"],
        "Masa y Dulces": ["Masa", "Dulces", "Otro"],
        "Bebidas": ["Agua", "Vino", "Jugo", "Licores", "Cerveza", "Otro"],
        "Química e higiene": ["Sanitario", "Higiene personal", "Equipo", "Otro"],
        "Otro": ["Otro"]
	},
	"portugalski": {
		"Carne branca": ["Frango", "Peru", "Ganso", "Pato", "Outro"],
		"Carne vermelha": ["Porco", "Cordeiro", "Ovelha", "Vitela", "Boi", "Touro", "Cavalo", "Coelho", "Outro"],
		"Caça pequena": ["Codorna", "Faisão", "Perdiz", "Pato selvagem", "Ganso selvagem", "Lebre", "Pombo", "Outro"],
		"Caça grossa": ["Cervo", "Corça", "Cabra selvagem", "Alce", "Rena", "Javali", "Bisão", "Camelo", "Lhama", "Alpaca", "Canguru", "Crocodilo/Jacaré", "Lagarto", "Cobra", "Outro"],
		"Peixe": ["Mar", "Água doce", "Frutos do mar", "Outro"],
		"Laticínios": ["Leite", "Processamento de leite", "Outro"],
		"Vegetais": ["Fresco", "Tratado termicamente", "Congelado", "Outro"],
		"Conservas e compotas": ["Frutas", "Vegetais", "Outro"],
		"Massa e Doces": ["Massa", "Doces", "Outro"],
		"Bebidas": ["Água", "Vinho", "Suco", "Bebidas destiladas", "Cerveja", "Outro"],
		"Química e higiene": ["Sanitário", "Higiene pessoal", "Equipamento", "Outro"],
		"Outro": ["Outro"]
	},
    "francais": {
        "Viande blanche": ["Poulet", "Dinde", "Oie", "Canard", "Autre"],
        "Viande rouge": ["Porc", "Agneau", "Mouton", "Veau", "Bœuf", "Taureau", "Cheval", "Lapin", "Autre"],
        "Petit gibier": ["Caille", "Faisan", "Perdrix", "Canard sauvage", "Oie sauvage", "Lièvre", "Pigeon", "Autre"],
        "Gros gibier": ["Cerf", "Chevreuil", "Chèvre sauvage", "Élan", "Renne", "Sanglier", "Bison", "Chameau", "Lama", "Alpaga", "Kangourou", "Crocodile/Alligator", "Lézard", "Serpent", "Autre"],
        "Poisson": ["Mer", "Eau douce", "Fruits de mer", "Autre"],
        "Produits laitiers": ["Lait", "Transformation laitière", "Autre"],
        "Légumes": ["Frais", "Traité thermiquement", "Congelé", "Autre"],
        "Conserves et compotes": ["Fruits", "Légumes", "Autre"],
        "Pâte et Sucreries": ["Pâte", "Sucreries", "Autre"],
        "Boissons": ["Eau", "Vin", "Jus", "Spiritueux", "Bière", "Autre"],
        "Chimie et hygiène": ["Sanitaire", "Hygiène personnelle", "Équipement", "Autre"],
        "Autre": ["Autre"]
    }
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
    "hungary": {
        # --- Fehér hús ---
        "Csirke": ["Grillcsirke", "Egész csirke", "Egész comb", "Comb filé", "Alsó comb", "Fehér hús (mell)", "Filé", "Hát", "Szárny", "Medál", "Nugget", "Rántott szelet", "Darált", "Leveshez", "Egyéb"],
        "Pulyka": ["Egész comb", "Comb filé", "Alsó comb", "Tekercs comb", "Comb szeletek", "Fehér hús (mell)", "Szárny", "Hát", "Szárnyak", "Leveshez", "Darált", "Egyéb"],
        "Libacomb": ["Fehér hús (mell)", "Egész comb", "Comb filé", "Alsó comb", "Szárny", "Hát", "Nyak", "Májas pástétom", "Libazsír", "Darált", "Leveshez", "Egyéb"],
        "Kacsa": ["Fehér hús (mell)", "Egész comb", "Comb filé", "Alsó comb", "Szárny", "Hát", "Nyak", "Kacsazsír", "Darált", "Máj", "Leveshez", "Egyéb"],

        # --- Vörös hús ---
        "Sertéshús": ["Szelet", "Karfiol", "Nyak", "Comb", "Szűzérme", "Borda", "Mell", "Lapocka", "Karakas", "Csülök", "Darált", "Apróra vágott", "Leveshez", "Egyéb"],
        "Bárányhús": ["Fej", "Nyak", "Lapocka", "Gerinc", "Mell", "Vese", "Comb", "Csülök", "Egyéb"],
        "Juhhús": ["Fej", "Nyak", "Lapocka", "Gerinc", "Mell", "Vese", "Comb", "Csülök", "Egyéb"],
        "Borjúhús": ["Bifsztek", "Nyak - tarja", "Mell", "Lapocka", "Csülök", "Borda", "Has", "T-bone steak", "Rump steak", "Rib-Eye", "Farok", "Egyéb"],
        "Marhahús": ["Roston sült", "Bifsztek", "Nyak", "Karakas", "Mell", "Csülök", "Borda", "Gerinc", "Hát", "Has", "Comb", "Egyéb"],
        "Bikahús": ["Comb", "Lapocka", "Szűzérme (hát)", "Mell és borda", "Lapocka", "Nyak", "Ágyék", "Farok", "Egyéb"],
        "Lóhús": ["Comb", "Lapocka", "Szűzérme (hát)", "Nyak", "Mell és borda", "Bifsztek", "Rump steak", "Darált hús", "Egyéb"],
        "Nyúlhús": ["Hátsó comb", "Elülső comb", "Filé (hát)", "Borda", "Egyéb"],

        # --- Apróvad ---
        "Fürj": ["Egész hús", "Mell (filék)", "Combok", "Máj", "Egyéb"],
        "Fácán": ["Egész hús", "Mell (filék)", "Combok", "Máj", "Egyéb"],
        "Fogoly": ["Egész hús", "Mell (filék)", "Combok", "Máj", "Egyéb"],
        "Galamb": ["Egész hús", "Mell (filék)", "Combok", "Máj", "Egyéb"],
        "Vadnyúl": ["Hátsó comb", "Elülső comb", "Filé (hát)", "Borda", "Egyéb"],
        "Vadkacsa": ["Egész hús", "Mell (filék)", "Combok", "Máj", "Egyéb"],
        "Vadliba": ["Egész hús", "Mell (filék)", "Combok", "Máj", "Egyéb"],

        # --- Nagy vad ---
        "Szarvac": ["Comb", "Filé (hát)", "Bifsztek", "Borda", "Mell", "Lapocka", "Csülök", "Apróra vágott", "Egyéb"],
        "Őz": ["Comb", "Filé (hát)", "Bifsztek", "Borda", "Mell", "Lapocka", "Csülök", "Apróra vágott", "Egyéb"],
        "Vadkecske": ["Comb", "Filé (hát)", "Bifsztek", "Borda", "Mell", "Lapocka", "Csülök", "Apróra vágott", "Egyéb"],
        "Jávorszarvas": ["Comb", "Filé (hát)", "Bifsztek", "Borda", "Mell", "Lapocka", "Csülök", "Apróra vágott", "Egyéb"],
        "Rénszarvas": ["Comb", "Filé (hát)", "Bifsztek", "Borda", "Mell", "Lapocka", "Csülök", "Apróra vágott", "Egyéb"],
        "Vadkan": ["Comb", "Lapocka", "Borda", "Szalonna", "Csülök", "Nyak", "Fej", "Egyéb"],
        "Bölény": ["Comb", "Lapocka", "Bifsztek", "Rump steak", "Borda", "Ágyék", "Nyak", "Csülök", "Egyéb"],
        "Teve": ["Comb", "Lapocka", "Filé (ágyék)", "Filé (hát)", "Borda", "Mell", "Nyak", "Púp", "Egyéb"],
        "Láma": ["Comb", "Lapocka", "Filé (hát és ágyék)", "Borda", "Nyak", "Egyéb"],
        "Alpaka": ["Comb", "Lapocka", "Filé (hát és ágyék)", "Borda", "Nyak", "Egyéb"],
        "Kenguru": ["Comb", "Lapocka", "Filé (hát és ágyék)", "Borda", "Farok", "Egyéb"],
        "Krokodil/Alligátor": ["Farok", "Filé (hát)", "Combok", "Egyéb"],
        "Gyík": ["Farok", "Hát", "Combok", "Egyéb"],
        "Kígyó": ["Törzs (gyűrűk)", "Egyéb"],

        # --- Hal ---
        "Tengeri": ["Lazac", "Tonhal", "Szardínia", "Tőkehal", "Tőkehal", "Makréla", "Fogas", "Aranysügér", "Laposhal", "Herring", "Szardella", "Tőkehal", "Egyéb"],
        "Édesvízi": ["Ponty", "Pisztráng", "Harcsa", "Kárász", "Sügér", "Tilápia", "Pangász", "Tok", "Csuka", "Fehér amur", "Arapaima", "Egyéb"],
        "Tenger gyümölcsei": ["Garnéla", "Tintahal", "Kagyló", "Kagyló", "Kagyló", "Kagyló", "Kagyló", "Rák", "Polip", "Lília", "Tengeri sün", "Tengeri uborka", "Abalone", "Egyéb"],

        # --- Tejtermékek ---
        "Tej": ["Tej", "Kefir", "Tejföl", "Tejszín", "Főzőtejszín", "Egyéb"],
        "Tejfeldolgozások": ["Túró", "Friss sajt", "Krémsajt", "Gouda", "Edami", "Trappista", "Kaskavál", "Parmezán", "Gorgonzola", "Roquefort", "Halloumi", "Egyéb"],

        # --- Zöldség ---
        "Friss": ["Borsó", "Zöldbab", "Karfiol", "Brokkoli", "Tök", "Paradicsom", "Uborka", "Paprika", "Egyéb"],
        "Hőkezelt": ["Borsó", "Zöldbab", "Kukorica", "Karfiol", "Brokkoli", "Paprika", "Cukkini", "Spenót", "Egyéb"],
        "Fagyasztott": ["Borsó", "Zöldbab", "Kukorica", "Karfiol", "Brokkoli", "Paprika", "Cukkini", "Spenót", "Egyéb"],

        # --- Befőttek és kompótok ---
        "Gyümölcs": ["Sárgabarack", "Körte", "Cseresznye", "Epres lekvár", "Szilvalekvár", "Cseresznye", "Málnalekvár", "Birsalma", "Ananász", "Mangó lekvár", "Egyéb"],
        "Zöldség": ["Savanyú uborka", "Savanyú paprika", "Paradicsompüré", "Cékla", "Ajvár", "Savanyúság", "Savanyú káposzta", "Egyéb"],

        # --- Tészta és Édességek ---
        "Tészta": ["Kenyér", "Rozskenyér", "Ciabatta", "Kukoricalepény", "Baguette", "Búzaliszt", "Teljes kiőrlésű liszt", "Hajdinaliszt", "Rizsliszt", "Fűszerek", "Egyéb"],
        "Édességek": ["Sütemények", "Torták", "Pékáru", "Fagylalt", "Csokoládé", "Cukorkák", "Egyéb"],

        # --- Italok ---
        "Víz": ["Ásványvíz", "Szénsavmentes", "Szénsavas", "Egyéb"],
        "Bor": ["Vörös", "Fehér", "Rozé", "Egyéb"],
        "Lé": ["Gyümölcslé", "Zöldséglé", "Egyéb"],
        "Tömény italok": ["Pálinka", "Vodka", "Whisky", "Egyéb"],
        "Sör": ["Barna", "Világos", "Egyéb"],

        # --- Kémia és higiénia ---
        "WC": ["Ablaktisztító", "Mosogatószer", "Padlótisztító", "Fürdőszobai tisztítószer", "Egyéb"],
        "Személyes higiénia": ["Dezodor", "Borotva", "Smink", "Szappan", "Sampon", "Krém", "Egyéb"],
        "Felszerelés": ["Vödör", "Vödör", "Poroló", "Seprű", "Egyéb"],

        # --- Egyéb ---
        "Egyéb": ["Megjegyzés: Írja be a termék nevét"]
    },
    "ukrajinski": {
        # --- Біле м'ясо ---
        "Курятина": ["Ціла курка", "Грудка", "Стегно", "Гомілка", "Крило", "Філе", "Спина", "Медальйони", "Нагетси", "Панірований шніцель", "Фарш", "Для супу", "Інше"],
        "Індичка": ["Ціла індичка", "Грудка", "Стегно", "Крило", "Філе", "Спина", "Медальйони", "Для супу", "Фарш", "Інше"],
        "Гуска": ["Ціла гуска", "Грудка", "Стегно", "Крило", "Спина", "Шия", "Печінка", "Гусячий жир", "Фарш", "Для супу", "Інше"],
        "Качка": ["Ціла качка", "Грудка", "Стегно", "Крило", "Спина", "Шия", "Качиний жир", "Печінка", "Фарш", "Для супу", "Інше"],
        
        # --- Червоне м'ясо ---
        "Свинина": ["Філе", "Котлета", "Окост", "Шия", "Лопатка", "Грудинка", "Ребра", "Голяшка", "Шинка", "Фарш", "Для супу", "Інше"],
        "Ягнятина": ["Філе", "Котлета", "Окост", "Шия", "Лопатка", "Грудинка", "Ребра", "Голяшка", "Фарш", "Для супу", "Інше"],
        "Яловичина": ["Філей", "Стейк", "Окост", "Шия", "Лопатка", "Грудинка", "Ребра", "Голяшка", "Фарш", "Для супу", "Інше"],
        "Телятина": ["Філе", "Котлета", "Окост", "Шия", "Лопатка", "Грудинка", "Ребра", "Голяшка", "Фарш", "Для супу", "Інше"],
        "Кролик": ["Задні лапи", "Передні лапи", "Спинка", "Ребра", "Для супу", "Інше"],
        
        # --- Дрібна дичина ---
        "Перепілка": ["Ціла", "Грудка", "Гомілки", "Крила", "Печінка", "Інше"],
        "Фазан": ["Цілий", "Грудка", "Гомілки", "Крила", "Печінка", "Інше"],
        "Куріпка": ["Ціла", "Грудка", "Гомілки", "Крила", "Печінка", "Інше"],
        "Голуб": ["Цілий", "Грудка", "Гомілки", "Крила", "Печінка", "Інше"],
        "Заєць": ["Задні лапи", "Передні лапи", "Спинка", "Ребра", "Інше"],
        "Дика качка": ["Ціла", "Грудка", "Гомілки", "Крила", "Печінка", "Інше"],
        "Дика гуска": ["Ціла", "Грудка", "Гомілки", "Крила", "Печінка", "Інше"],
        
        # --- Велика дичина ---
        "Олень": ["Філе", "Котлета", "Окост", "Шия", "Лопатка", "Грудинка", "Ребра", "Голяшка", "Фарш", "Для супу", "Інше"],
        "Косуля": ["Філе", "Котлета", "Окост", "Шия", "Лопатка", "Грудинка", "Ребра", "Голяшка", "Фарш", "Для супу", "Інше"],
        "Дикий кабан": ["Філе", "Котлета", "Окост", "Шия", "Лопатка", "Грудинка", "Ребра", "Голяшка", "Фарш", "Для супу", "Інше"],
        "Лось": ["Філе", "Котлета", "Окост", "Шия", "Лопатка", "Грудинка", "Ребра", "Голяшка", "Фарш", "Для супу", "Інше"],
        "Північний олень": ["Філе", "Котлета", "Окост", "Шия", "Лопатка", "Грудинка", "Ребра", "Голяшка", "Фарш", "Для супу", "Інше"],
        "Бізон": ["Філе", "Стейк", "Окост", "Шия", "Лопатка", "Грудинка", "Ребра", "Голяшка", "Фарш", "Для супу", "Інше"],
        "Верблюд": ["Філе", "Котлета", "Окост", "Шия", "Лопатка", "Горб", "Ребра", "Фарш", "Для супу", "Інше"],
        "Лама": ["Філе", "Котлета", "Окост", "Шия", "Лопатка", "Ребра", "Фарш", "Для супу", "Інше"],
        "Альпака": ["Філе", "Котлета", "Окост", "Шия", "Лопатка", "Ребра", "Фарш", "Для супу", "Інше"],
        "Кенгуру": ["Філе", "Стейк", "Окост", "Шия", "Лопатка", "Хвіст", "Фарш", "Для супу", "Інше"],
        "Крокодил/Алігатор": ["Хвіст", "Філе", "Гомілки", "Інше"],
        "Ящірка": ["Хвіст", "Спина", "Гомілки", "Інше"],
        "Змія": ["Кільця", "Інше"],
        
        # --- Риба ---
        "Морська": ["Філе", "Стейк", "Ціла риба", "Філе зі шкірою", "Філе без шкіри", "Шматки", "Для супу", "Інше"],
        "Прісноводна": ["Філе", "Стейк", "Ціла риба", "Філе зі шкірою", "Філе без шкіри", "Шматки", "Для супу", "Інше"],
        "Морепродукти": ["Креветки", "Кальмар", "Мідії", "Устриці", "Гребінці", "Краби", "Восьминіг", "Каракатиця", "Інше"],
        
        # --- Молочні продукти ---
        "Молоко": ["Цільне", "Знежирене", "Пастеризоване", "Стерилізоване", "Кип'ячене", "Згущене", "Сухе", "Інше"],
        "Молочні переробки": ["Сир", "Сир домашній", "Сметана", "Йогурт", "Кефір", "Масло", "Сирний крем", "Інше"],
        
        # --- Овочі ---
        "Свіжі": ["Цілі", "Нарізані", "Виміті", "Очищені", "Терті", "Інше"],
        "Термічно оброблені": ["Варені", "Тушковані", "Смажені", "Запечені", "Приготовані на пару", "Інше"],
        "Заморожені": ["Цілі", "Нарізані", "Суміш", "Пюре", "Інше"],
        
        # --- Фрукти ---
        "Фрукти": ["Цілі", "Нарізані", "Очищені", "Без кісточок", "Консервовані", "Сушені", "Інше"],
        
        # --- Тісто та Солодощі ---
        "Тісто": ["Дріжджове", "Пісочне", "Листкове", "Для млинців", "Для піци", "Для макарон", "Інше"],
        "Солодощі": ["Шоколад", "Цукерки", "Печиво", "Торти", "Випічка", "Морозиво", "Вафлі", "Інше"],
        
        # --- Напої ---
        "Вода": ["Газована", "Негазована", "Мінеральна", "Ароматизована", "Інше"],
        "Вино": ["Червоне", "Біле", "Рожеве", "Ігристe", "Солодке", "Сухе", "Напівсухе", "Інше"],
        "Сік": ["Яблучний", "Апельсиновий", "Виноградний", "Томатний", "Мультифрукт", "З м'якоттю", "Без м'якоті", "Інше"],
        "Міцні напої": ["Горілка", "Віскі", "Коньяк", "Ром", "Джин", "Текіла", "Лікер", "Інше"],
        "Пиво": ["Світле", "Темне", "Пшеничне", "Крафтове", "Безалкогольне", "Інше"],
        
        # --- Хімія та гігієна ---
        "Санітарія": ["Для ванної", "Для туалету", "Для умивальника", "Універсальний", "Антибактеріальний", "Інше"],
        "Особиста гігієна": ["Мило", "Шампунь", "Гель для душу", "Дезодорант", "Зубна паста", "Бритва", "Крем", "Інше"],
        "Приладдя": ["Відро", "Швабра", "Ганчірка", "Губка", "Щітка", "Рукавиці", "Інше"],
        
        "Інше": ["Примітка: введіть назву продукту"]
    },

    "ruski": {
        # --- Белое мясо ---
        "Курица": ["Целая курица", "Грудка", "Бедро", "Голень", "Крыло", "Филе", "Спина", "Медальоны", "Наггетсы", "Панированное", "Фарш", "Для супа", "Другое"],
        "Индейка": ["Целая индейка", "Грудка", "Бедро", "Голень", "Крыло", "Филе", "Спина", "Медальоны", "Для супа", "Фарш", "Другое"],
        "Гусь": ["Целая гусь", "Грудка", "Бедро", "Голень", "Крыло", "Спина", "Шея", "Печень", "Гусиный жир", "Фарш", "Для супа", "Другое"],
        "Утка": ["Целая утка", "Грудка", "Бедро", "Голень", "Крыло", "Спина", "Шея", "Утиный жир", "Печень", "Фарш", "Для супа", "Другое"],
        
        # --- Красное мясо ---
        "Свинина": ["Вырезка", "Корейка", "Окорок", "Шея", "Лопатка", "Грудинка", "Ребра", "Рулька", "Подплечный край", "Фарш", "Для супа", "Другое"],
        "Баранина": ["Вырезка", "Корейка", "Окорок", "Шея", "Лопатка", "Грудинка", "Ребра", "Рулька", "Фарш", "Для супа", "Другое"],
        "Телятина": ["Вырезка", "Корейка", "Окорок", "Шея", "Лопатка", "Грудинка", "Ребра", "Рулька", "Фарш", "Для супа", "Другое"],
        "Говядина": ["Вырезка", "Корейка", "Окорок", "Шея", "Лопатка", "Грудинка", "Ребра", "Рулька", "Фарш", "Для супа", "Другое"],
        "Кролик": ["Задние лапы", "Передние лапы", "Спинка", "Ребра", "Для супа", "Другое"],
        
        # --- Мелкая дичь ---
        "Перепел": ["Целая тушка", "Грудка", "Бедра", "Крылья", "Печень", "Другое"],
        "Фазан": ["Целая тушка", "Грудка", "Бедра", "Крылья", "Печень", "Другое"],
        "Куропатка": ["Целая тушка", "Грудка", "Бедра", "Крылья", "Печень", "Другое"],
        "Голубь": ["Целая тушка", "Грудка", "Бедра", "Крылья", "Печень", "Другое"],
        "Заяц": ["Задние лапы", "Передние лапы", "Спинка", "Ребра", "Другое"],
        "Дикая утка": ["Целая тушка", "Грудка", "Бедра", "Крылья", "Печень", "Другое"],
        "Дикий гусь": ["Целая тушка", "Грудка", "Бедра", "Крылья", "Печень", "Другое"],
        
        # --- Крупная дичь ---
        "Олень": ["Вырезка", "Корейка", "Окорок", "Шея", "Лопатка", "Грудинка", "Ребра", "Рулька", "Фарш", "Для супа", "Другое"],
        "Косуля": ["Вырезка", "Корейка", "Окорок", "Шея", "Лопатка", "Грудинка", "Ребра", "Рулька", "Фарш", "Для супа", "Другое"],
        "Кабан": ["Вырезка", "Корейка", "Окорок", "Шея", "Лопатка", "Грудинка", "Ребра", "Рулька", "Фарш", "Для супа", "Другое"],
        "Лось": ["Вырезка", "Корейка", "Окорок", "Шея", "Лопатка", "Грудинка", "Ребра", "Рулька", "Фарш", "Для супа", "Другое"],
        
        # --- Рыба ---
        "Морская": ["Филе", "Стейк", "Целая рыба", "Филе с кожей", "Филе без кожи", "Филе на коже", "Куски", "Для супа", "Другое"],
        "Пресноводная": ["Филе", "Стейк", "Целая рыба", "Филе с кожей", "Филе без кожи", "Филе на коже", "Куски", "Для супа", "Другое"],
        "Морепродукты": ["Креветки", "Кальмары", "Мидии", "Устрицы", "Гребешки", "Крабы", "Осьминоги", "Каракатицы", "Другое"],
        
        # --- Молочные продукты ---
        "Молоко": ["Цельное", "Обезжиренное", "Пастеризованное", "Стерилизованное", "Топленое", "Сгущенное", "Сухое", "Другое"],
        "Молочные переработки": ["Сыр", "Творог", "Сметана", "Йогурт", "Кефир", "Ряженка", "Сливочное масло", "Творожный сыр", "Другое"],
        
        # --- Овощи ---
        "Свежие": ["Целые", "Нарезанные", "Вымытые", "Чищенные", "Натертые", "Другое"],
        "Термически обработанные": ["Вареные", "Тушеные", "Жареные", "Запеченные", "Приготовленные на пару", "Другое"],
        "Замороженные": ["Целые", "Нарезанные", "Смесь", "Пюре", "Другое"],
        
        # --- Фрукты ---
        "Фрукты": ["Целые", "Нарезанные", "Очищенные", "Без косточек", "Консервированные", "Сушеные", "Другое"],
        
        # --- Тесто и сладости ---
        "Тесто": ["Дрожжевое", "Песочное", "Слоеное", "Блинное", "Для пиццы", "Для пасты", "Другое"],
        "Сладости": ["Шоколад", "Конфеты", "Печенье", "Торты", "Пирожные", "Мороженое", "Вафли", "Другое"],
        
        # --- Напитки ---
        "Вода": ["Газированная", "Негазированная", "Минеральная", "Ароматизированная", "Другое"],
        "Вино": ["Красное", "Белое", "Розовое", "Игристое", "Сладкое", "Сухое", "Полусухое", "Другое"],
        "Сок": ["Яблочный", "Апельсиновый", "Виноградный", "Томатный", "Мультифрукт", "С мякотью", "Без мякоти", "Другое"],
        "Крепкие напитки": ["Водка", "Виски", "Коньяк", "Ром", "Джин", "Текила", "Ликер", "Другое"],
        "Пиво": ["Светлое", "Темное", "Пшеничное", "Крафтовое", "Безалкогольное", "Другое"],
        
        # --- Химия и гигиена ---
        "Сантехника": ["Для ванной", "Для туалета", "Для раковины", "Универсальное", "Антибактериальное", "Другое"],
        "Личная гигиена": ["Мыло", "Шампунь", "Гель для душа", "Дезодорант", "Зубная паста", "Бритва", "Крем", "Другое"],
        "Оборудование": ["Ведро", "Швабра", "Тряпка", "Губка", "Щетка", "Перчатки", "Другое"],
        
        "Другое": ["Примечание: введите название продукта"]
    },

    "english": {
        # --- White meat ---
        "Chicken": ["Whole chicken", "Breast", "Thigh", "Drumstick", "Wing", "Filet", "Back", "Medallions", "Nuggets", "Breaded cutlet", "Minced meat", "For soup", "Other"],
        "Turkey": ["Whole turkey", "Breast", "Thigh", "Wing", "Filet", "Back", "Medallions", "For soup", "Minced meat", "Other"],
        "Goose": ["Whole goose", "Breast", "Thigh", "Wing", "Back", "Neck", "Liver", "Goose fat", "Minced meat", "For soup", "Other"],
        "Duck": ["Whole duck", "Breast", "Thigh", "Wing", "Back", "Neck", "Duck fat", "Liver", "Minced meat", "For soup", "Other"],
        
        # --- Red meat ---
        "Pork": ["Loin", "Chop", "Leg", "Neck", "Shoulder", "Belly", "Ribs", "Hock", "Ham", "Minced meat", "For soup", "Other"],
        "Lamb": ["Loin", "Chop", "Leg", "Neck", "Shoulder", "Belly", "Ribs", "Hock", "Minced meat", "For soup", "Other"],
        "Beef": ["Sirloin", "Steak", "Leg", "Neck", "Shoulder", "Brisket", "Ribs", "Shank", "Minced meat", "For soup", "Other"],
        "Veal": ["Loin", "Chop", "Leg", "Neck", "Shoulder", "Belly", "Ribs", "Hock", "Minced meat", "For soup", "Other"],
        "Rabbit": ["Hind legs", "Front legs", "Saddle", "Ribs", "For soup", "Other"],
        
        # --- Small game ---
        "Quail": ["Whole", "Breast", "Legs", "Wings", "Liver", "Other"],
        "Pheasant": ["Whole", "Breast", "Legs", "Wings", "Liver", "Other"],
        "Partridge": ["Whole", "Breast", "Legs", "Wings", "Liver", "Other"],
        "Pigeon": ["Whole", "Breast", "Legs", "Wings", "Liver", "Other"],
        "Hare": ["Hind legs", "Front legs", "Saddle", "Ribs", "Other"],
        "Wild duck": ["Whole", "Breast", "Legs", "Wings", "Liver", "Other"],
        "Wild goose": ["Whole", "Breast", "Legs", "Wings", "Liver", "Other"],
        
        # --- Big game ---
        "Deer": ["Loin", "Chop", "Leg", "Neck", "Shoulder", "Brisket", "Ribs", "Shank", "Minced meat", "For soup", "Other"],
        "Roe deer": ["Loin", "Chop", "Leg", "Neck", "Shoulder", "Brisket", "Ribs", "Shank", "Minced meat", "For soup", "Other"],
        "Wild boar": ["Loin", "Chop", "Leg", "Neck", "Shoulder", "Belly", "Ribs", "Hock", "Minced meat", "For soup", "Other"],
        "Moose": ["Loin", "Chop", "Leg", "Neck", "Shoulder", "Brisket", "Ribs", "Shank", "Minced meat", "For soup", "Other"],
        "Reindeer": ["Loin", "Chop", "Leg", "Neck", "Shoulder", "Brisket", "Ribs", "Shank", "Minced meat", "For soup", "Other"],
        "Bison": ["Loin", "Steak", "Leg", "Neck", "Shoulder", "Brisket", "Ribs", "Shank", "Minced meat", "For soup", "Other"],
        "Camel": ["Loin", "Chop", "Leg", "Neck", "Shoulder", "Brisket", "Ribs", "Hump", "Minced meat", "For soup", "Other"],
        "Llama": ["Loin", "Chop", "Leg", "Neck", "Shoulder", "Brisket", "Ribs", "Minced meat", "For soup", "Other"],
        "Alpaca": ["Loin", "Chop", "Leg", "Neck", "Shoulder", "Brisket", "Ribs", "Minced meat", "For soup", "Other"],
        "Kangaroo": ["Loin", "Steak", "Leg", "Neck", "Shoulder", "Tail", "Minced meat", "For soup", "Other"],
        "Crocodile/Alligator": ["Tail", "Filet", "Legs", "Other"],
        "Lizard": ["Tail", "Back", "Legs", "Other"],
        "Snake": ["Body rings", "Other"],
        
        # --- Fish ---
        "Sea": ["Fillet", "Steak", "Whole fish", "Skin-on fillet", "Skinless fillet", "Pieces", "For soup", "Other"],
        "Freshwater": ["Fillet", "Steak", "Whole fish", "Skin-on fillet", "Skinless fillet", "Pieces", "For soup", "Other"],
        "Seafood": ["Shrimp", "Squid", "Mussels", "Oysters", "Scallops", "Crabs", "Octopus", "Cuttlefish", "Other"],
        
        # --- Dairy products ---
        "Milk": ["Whole", "Skimmed", "Pasteurized", "Sterilized", "Boiled", "Condensed", "Powder", "Other"],
        "Dairy processing": ["Cheese", "Cottage cheese", "Sour cream", "Yogurt", "Kefir", "Butter", "Cream cheese", "Other"],
        
        # --- Vegetables ---
        "Fresh": ["Whole", "Chopped", "Washed", "Peeled", "Grated", "Other"],
        "Heat treated": ["Boiled", "Stewed", "Fried", "Baked", "Steamed", "Other"],
        "Frozen": ["Whole", "Chopped", "Mixed", "Puree", "Other"],
        
        # --- Fruits ---
        "Fruits": ["Whole", "Sliced", "Peeled", "Seedless", "Canned", "Dried", "Other"],
        
        # --- Dough and Sweets ---
        "Dough": ["Yeast dough", "Shortcrust", "Puff pastry", "Pancake batter", "Pizza dough", "Pasta dough", "Other"],
        "Sweets": ["Chocolate", "Candy", "Cookies", "Cakes", "Pastries", "Ice cream", "Wafers", "Other"],
        
        # --- Beverages ---
        "Water": ["Sparkling", "Still", "Mineral", "Flavored", "Other"],
        "Wine": ["Red", "White", "Rosé", "Sparkling", "Sweet", "Dry", "Semi-dry", "Other"],
        "Juice": ["Apple", "Orange", "Grape", "Tomato", "Multifruit", "With pulp", "Without pulp", "Other"],
        "Spirits": ["Vodka", "Whisky", "Cognac", "Rum", "Gin", "Tequila", "Liqueur", "Other"],
        "Beer": ["Light", "Dark", "Wheat", "Craft", "Non-alcoholic", "Other"],
        
        # --- Chemicals and hygiene ---
        "Sanitary": ["For bathroom", "For toilet", "For sink", "Universal", "Antibacterial", "Other"],
        "Personal hygiene": ["Soap", "Shampoo", "Shower gel", "Deodorant", "Toothpaste", "Razor", "Cream", "Other"],
        "Equipment": ["Bucket", "Mop", "Cloth", "Sponge", "Brush", "Gloves", "Other"],
        
        "Other": ["Note: Enter product name"]
    },

    "deutsch": {
        # --- Weißes Fleisch ---
        "Huhn": ["Ganzes Huhn", "Brust", "Keule", "Flügel", "Filet", "Rücken", "Medaillons", "Nuggets", "Panierte Schnitzel", "Hackfleisch", "Für Suppe", "Andere"],
        "Truthahn": ["Ganzes Truthahn", "Brust", "Keule", "Flügel", "Filet", "Rücken", "Medaillons", "Für Suppe", "Hackfleisch", "Andere"],
        "Gans": ["Ganze Gans", "Brust", "Keule", "Flügel", "Rücken", "Hals", "Leber", "Gänseschmalz", "Hackfleisch", "Für Suppe", "Andere"],
        "Ente": ["Ganze Ente", "Brust", "Keule", "Flügel", "Rücken", "Hals", "Entenschmalz", "Leber", "Hackfleisch", "Für Suppe", "Andere"],
        
        # --- Rotes Fleisch ---
        "Schwein": ["Filet", "Kotelett", "Keule", "Hals", "Schulter", "Brust", "Rippen", "Haxe", "Schinken", "Hackfleisch", "Für Suppe", "Andere"],
        "Lamm": ["Filet", "Kotelett", "Keule", "Hals", "Schulter", "Brust", "Rippen", "Haxe", "Hackfleisch", "Für Suppe", "Andere"],
        "Rind": ["Filet", "Kotelett", "Keule", "Hals", "Schulter", "Brust", "Rippen", "Haxe", "Hackfleisch", "Für Suppe", "Andere"],
        "Kalbfleisch": ["Filet", "Kotelett", "Keule", "Hals", "Schulter", "Brust", "Rippen", "Haxe", "Hackfleisch", "Für Suppe", "Andere"],
        "Kaninchen": ["Hinterläufe", "Vorderläufe", "Rücken", "Rippen", "Für Suppe", "Andere"],
        
        # --- Kleinwild ---
        "Wachtel": ["Ganzes Tier", "Brust", "Keulen", "Flügel", "Leber", "Andere"],
        "Fasan": ["Ganzes Tier", "Brust", "Keulen", "Flügel", "Leber", "Andere"],
        "Rebhuhn": ["Ganzes Tier", "Brust", "Keulen", "Flügel", "Leber", "Andere"],
        "Taube": ["Ganzes Tier", "Brust", "Keulen", "Flügel", "Leber", "Andere"],
        "Hase": ["Hinterläufe", "Vorderläufe", "Rücken", "Rippen", "Andere"],
        "Wildente": ["Ganzes Tier", "Brust", "Keulen", "Flügel", "Leber", "Andere"],
        "Wildgans": ["Ganzes Tier", "Brust", "Keulen", "Flügel", "Leber", "Andere"],
        
        # --- Großwild ---
        "Hirsch": ["Filet", "Kotelett", "Keule", "Hals", "Schulter", "Brust", "Rippen", "Haxe", "Hackfleisch", "Für Suppe", "Andere"],
        "Reh": ["Filet", "Kotelett", "Keule", "Hals", "Schulter", "Brust", "Rippen", "Haxe", "Hackfleisch", "Für Suppe", "Andere"],
        "Wildschwein": ["Filet", "Kotelett", "Keule", "Hals", "Schulter", "Brust", "Rippen", "Haxe", "Hackfleisch", "Für Suppe", "Andere"],
        "Elch": ["Filet", "Kotelett", "Keule", "Hals", "Schulter", "Brust", "Rippen", "Haxe", "Hackfleisch", "Für Suppe", "Andere"],
        
        # --- Fisch ---
        "Meer": ["Filet", "Steak", "Ganzer Fisch", "Filet mit Haut", "Filet ohne Haut", "Stücke", "Für Suppe", "Andere"],
        "Süßwasser": ["Filet", "Steak", "Ganzer Fisch", "Filet mit Haut", "Filet ohne Haut", "Stücke", "Für Suppe", "Andere"],
        "Meeresfrüchte": ["Garnelen", "Tintenfisch", "Muscheln", "Austern", "Jakobsmuscheln", "Krabben", "Tintenfisch", "Sepia", "Andere"],
        
        # --- Milchprodukte ---
        "Milch": ["Vollmilch", "Fettarme", "Pasteurisiert", "Sterilisiert", "Gekocht", "Kondensmilch", "Pulver", "Andere"],
        "Milchverarbeitung": ["Käse", "Hüttenkäse", "Sauerrahm", "Joghurt", "Kefir", "Butter", "Frischkäse", "Andere"],
        
        # --- Gemüse ---
        "Frisch": ["Ganz", "Geschnitten", "Gewaschen", "Geschält", "Geraspelt", "Andere"],
        "Erhitzt": ["Gekocht", "Gedünstet", "Gebraten", "Gebacken", "Gedämpft", "Andere"],
        "Gefroren": ["Ganz", "Geschnitten", "Mischung", "Püree", "Andere"],
        
        # --- Obst ---
        "Früchte": ["Ganz", "Geschnitten", "Geschält", "Kernlos", "Konserviert", "Getrocknet", "Andere"],
        
        # --- Teig und Süßigkeiten ---
        "Teig": ["Hefeteig", "Mürbeteig", "Blätterteig", "Pfannkuchenteig", "Pizzateig", "Pastateig", "Andere"],
        "Süßigkeiten": ["Schokolade", "Bonbons", "Kekse", "Kuchen", "Torten", "Eis", "Waffeln", "Andere"],
        
        # --- Getränke ---
        "Wasser": ["Sprudel", "Still", "Mineral", "Aromatisiert", "Andere"],
        "Wein": ["Rot", "Weiß", "Rosé", "Sekt", "Süß", "Trocken", "Halbtrocken", "Andere"],
        "Saft": ["Apfel", "Orange", "Traube", "Tomate", "Multifrucht", "Mit Fruchtfleisch", "Ohne Fruchtfleisch", "Andere"],
        "Spirituosen": ["Wodka", "Whisky", "Cognac", "Rum", "Gin", "Tequila", "Likör", "Andere"],
        "Bier": ["Hell", "Dunkel", "Weizen", "Craft", "Alkoholfrei", "Andere"],
        
        # --- Chemie und Hygiene ---
        "Sanitär": ["Für Bad", "Für Toilette", "Für Waschbecken", "Universal", "Antibakteriell", "Andere"],
        "Persönliche Hygiene": ["Seife", "Shampoo", "Duschgel", "Deodorant", "Zahnpasta", "Rasierer", "Creme", "Andere"],
        "Ausrüstung": ["Eimer", "Mop", "Tuch", "Schwamm", "Bürste", "Handschuhe", "Andere"],
        
        "Andere": ["Hinweis: Produktname eingeben"]
    },

    "mandarinski": {
        # --- 白肉 ---
        "鸡": ["整鸡", "鸡胸", "鸡腿", "鸡翅", "鸡柳", "鸡背", "鸡块", "鸡米花", "炸鸡排", "鸡绞肉", "汤用", "其他"],
        "火鸡": ["整火鸡", "火鸡胸", "火鸡腿", "火鸡翅", "火鸡柳", "火鸡背", "火鸡块", "汤用", "火鸡绞肉", "其他"],
        "鹅": ["整鹅", "鹅胸", "鹅腿", "鹅翅", "鹅背", "鹅颈", "鹅肝", "鹅油", "鹅绞肉", "汤用", "其他"],
        "鸭": ["整鸭", "鸭胸", "鸭腿", "鸭翅", "鸭背", "鸭颈", "鸭油", "鸭肝", "鸭绞肉", "汤用", "其他"],
        
        # --- 红肉 ---
        "猪肉": ["里脊", "排骨", "猪腿", "猪颈", "猪肩", "猪胸", "猪肋", "猪蹄", "猪绞肉", "汤用", "其他"],
        "羊肉": ["里脊", "排骨", "羊腿", "羊颈", "羊肩", "羊胸", "羊肋", "羊蹄", "羊绞肉", "汤用", "其他"],
        "牛肉": ["里脊", "牛排", "牛腿", "牛颈", "牛肩", "牛胸", "牛肋", "牛蹄", "牛绞肉", "汤用", "其他"],
        "兔肉": ["后腿", "前腿", "兔背", "兔肋", "汤用", "其他"],
        
        # --- 小型野味 ---
        "鹌鹑": ["整只", "鹌鹑胸", "鹌鹑腿", "鹌鹑翅", "鹌鹑肝", "其他"],
        "野鸡": ["整只", "野鸡胸", "野鸡腿", "野鸡翅", "野鸡肝", "其他"],
        "鹧鸪": ["整只", "鹧鸪胸", "鹧鸪腿", "鹧鸪翅", "鹧鸪肝", "其他"],
        "鸽子": ["整只", "鸽子胸", "鸽子腿", "鸽子翅", "鸽子肝", "其他"],
        "野兔": ["后腿", "前腿", "兔背", "兔肋", "其他"],
        "野鸭": ["整只", "野鸭胸", "野鸭腿", "野鸭翅", "野鸭肝", "其他"],
        "野鹅": ["整只", "野鹅胸", "野鹅腿", "野鹅翅", "野鹅肝", "其他"],
        
        # --- 大型野味 ---
        "鹿": ["里脊", "鹿排", "鹿腿", "鹿颈", "鹿肩", "鹿胸", "鹿肋", "鹿蹄", "鹿绞肉", "汤用", "其他"],
        "狍子": ["里脊", "狍子排", "狍子腿", "狍子颈", "狍子肩", "狍子胸", "狍子肋", "狍子蹄", "狍子绞肉", "汤用", "其他"],
        "野猪": ["里脊", "野猪排", "野猪腿", "野猪颈", "野猪肩", "野猪胸", "野猪肋", "野猪蹄", "野猪绞肉", "汤用", "其他"],
        "驼鹿": ["里脊", "驼鹿排", "驼鹿腿", "驼鹿颈", "驼鹿肩", "驼鹿胸", "驼鹿肋", "驼鹿蹄", "驼鹿绞肉", "汤用", "其他"],
        
        # --- 鱼 ---
        "海鱼": ["鱼片", "鱼排", "整鱼", "带皮鱼片", "去皮鱼片", "鱼块", "汤用", "其他"],
        "淡水鱼": ["鱼片", "鱼排", "整鱼", "带皮鱼片", "去皮鱼片", "鱼块", "汤用", "其他"],
        "海鲜": ["虾", "鱿鱼", "蛤蜊", "牡蛎", "扇贝", "螃蟹", "章鱼", "墨鱼", "其他"],
        
        # --- 乳制品 ---
        "牛奶": ["全脂", "脱脂", "巴氏杀菌", "灭菌", "煮沸", "炼乳", "奶粉", "其他"],
        "乳制品加工": ["奶酪", "干酪", "酸奶油", "酸奶", "开菲尔", "黄油", "奶油奶酪", "其他"],
        
        # --- 蔬菜 ---
        "新鲜": ["整颗", "切片", "洗净", "去皮", "擦丝", "其他"],
        "热处理": ["煮熟", "炖煮", "油炸", "烘烤", "蒸煮", "其他"],
        "冷冻": ["整颗", "切片", "混合", "泥状", "其他"],
        
        # --- 水果 ---
        "水果": ["整颗", "切片", "去皮", "去核", "罐头", "干果", "其他"],
        
        # --- 面团和糖果 ---
        "面团": ["酵母面团", "酥皮面团", "千层酥皮", "煎饼面糊", "披萨面团", "意大利面团", "其他"],
        "糖果": ["巧克力", "糖果", "饼干", "蛋糕", "糕点", "冰淇淋", "华夫饼", "其他"],
        
        # --- 饮料 ---
        "水": ["气泡水", "静水", "矿泉水", "调味水", "其他"],
        "酒": ["红酒", "白酒", "桃红", "起泡酒", "甜酒", "干酒", "半干", "其他"],
        "果汁": ["苹果汁", "橙汁", "葡萄汁", "番茄汁", "混合果汁", "带果肉", "无果肉", "其他"],
        "烈酒": ["伏特加", "威士忌", "干邑", "朗姆酒", "金酒", "龙舌兰", "利口酒", "其他"],
        "啤酒": ["淡啤", "黑啤", "小麦啤", "精酿", "无酒精", "其他"],
        
        # --- 化学品和卫生 ---
        "卫生": ["浴室用", "厕所用", "洗手池用", "通用", "抗菌", "其他"],
        "个人卫生": ["肥皂", "洗发水", "沐浴露", "除臭剂", "牙膏", "剃须刀", "面霜", "其他"],
        "设备": ["桶", "拖把", "布", "海绵", "刷子", "手套", "其他"],
        
        "其他": ["注：输入产品名称"]
    },

    "espanol": {
        # --- Carne blanca ---
        "Pollo": ["Pollo entero", "Pechuga", "Muslo", "Ala", "Filete", "Espalda", "Medallones", "Nuggets", "Milanesa", "Carne molida", "Para sopa", "Otro"],
        "Pavo": ["Pavo entero", "Pechuga", "Muslo", "Ala", "Filete", "Espalda", "Medallones", "Para sopa", "Carne molida", "Otro"],
        "Ganso": ["Ganso entero", "Pechuga", "Muslo", "Ala", "Espalda", "Cuello", "Hígado", "Grasa de ganso", "Carne molida", "Para sopa", "Otro"],
        "Pato": ["Pato entero", "Pechuga", "Muslo", "Ala", "Espalda", "Cuello", "Grasa de pato", "Hígado", "Carne molida", "Para sopa", "Otro"],
        
        # --- Carne roja ---
        "Cerdo": ["Lomo", "Chuleta", "Pierna", "Cuello", "Paleta", "Pecho", "Costilla", "Codillo", "Jamón", "Carne molida", "Para sopa", "Otro"],
        "Cordero": ["Lomo", "Chuleta", "Pierna", "Cuello", "Paleta", "Pecho", "Costilla", "Codillo", "Carne molida", "Para sopa", "Otro"],
        "Res": ["Lomo", "Bistec", "Pierna", "Cuello", "Paleta", "Pecho", "Costilla", "Codillo", "Carne molida", "Para sopa", "Otro"],
        "Ternera": ["Lomo", "Chuleta", "Pierna", "Cuello", "Paleta", "Pecho", "Costilla", "Codillo", "Carne molida", "Para sopa", "Otro"],
        "Conejo": ["Patas traseras", "Patas delanteras", "Lomo", "Costillas", "Para sopa", "Otro"],
        
        # --- Caza menor ---
        "Codorniz": ["Entera", "Pechuga", "Muslos", "Alas", "Hígado", "Otro"],
        "Faisán": ["Entera", "Pechuga", "Muslos", "Alas", "Hígado", "Otro"],
        "Perdiz": ["Entera", "Pechuga", "Muslos", "Alas", "Hígado", "Otro"],
        "Paloma": ["Entera", "Pechuga", "Muslos", "Alas", "Hígado", "Otro"],
        "Liebre": ["Patas traseras", "Patas delanteras", "Lomo", "Costillas", "Otro"],
        "Pato salvaje": ["Entera", "Pechuga", "Muslos", "Alas", "Hígado", "Otro"],
        "Ganso salvaje": ["Entera", "Pechuga", "Muslos", "Alas", "Hígado", "Otro"],
        
        # --- Caza mayor ---
        "Ciervo": ["Lomo", "Chuleta", "Pierna", "Cuello", "Paleta", "Pecho", "Costilla", "Codillo", "Carne molida", "Para sopa", "Otro"],
        "Corzo": ["Lomo", "Chuleta", "Pierna", "Cuello", "Paleta", "Pecho", "Costilla", "Codillo", "Carne molida", "Para sopa", "Otro"],
        "Jabalí": ["Lomo", "Chuleta", "Pierna", "Cuello", "Paleta", "Pecho", "Costilla", "Codillo", "Carne molida", "Para sopa", "Otro"],
        "Alce": ["Lomo", "Chuleta", "Pierna", "Cuello", "Paleta", "Pecho", "Costilla", "Codillo", "Carne molida", "Para sopa", "Otro"],
        
        # --- Pescado ---
        "Mar": ["Filete", "Filete con piel", "Filete sin piel", "Entero", "Trozos", "Para sopa", "Otro"],
        "Agua dulce": ["Filete", "Filete con piel", "Filete sin piel", "Entero", "Trozos", "Para sopa", "Otro"],
        "Mariscos": ["Camarones", "Calamar", "Mejillones", "Ostras", "Vieiras", "Cangrejos", "Pulpo", "Sepia", "Otro"],
        
        # --- Productos lácteos ---
        "Leche": ["Entera", "Descremada", "Pasteurizada", "Esterilizada", "Hervida", "Condensada", "En polvo", "Otro"],
        "Procesamiento lácteo": ["Queso", "Requesón", "Crema agria", "Yogur", "Kéfir", "Mantequilla", "Queso crema", "Otro"],
        
        # --- Verduras ---
        "Frescas": ["Enteras", "Cortadas", "Lavadas", "Peladas", "Ralladas", "Otro"],
        "Tratadas térmicamente": ["Cocidas", "Estofadas", "Fritas", "Horneadas", "Al vapor", "Otro"],
        "Congeladas": ["Enteras", "Cortadas", "Mezcla", "Puré", "Otro"],
        
        # --- Frutas ---
        "Frutas": ["Enteras", "Cortadas", "Peladas", "Sin semillas", "Enlatadas", "Secas", "Otro"],
        
        # --- Masa y dulces ---
        "Masa": ["Levadura", "Quebrada", "Hojaldre", "Para panqueques", "Para pizza", "Para pasta", "Otro"],
        "Dulces": ["Chocolate", "Caramelos", "Galletas", "Pasteles", "Tortas", "Helado", "Wafles", "Otro"],
        
        # --- Bebidas ---
        "Agua": ["Con gas", "Sin gas", "Mineral", "Saborizada", "Otro"],
        "Vino": ["Tinto", "Blanco", "Rosado", "Espumoso", "Dulce", "Seco", "Semiseco", "Otro"],
        "Jugo": ["Manzana", "Naranja", "Uva", "Tomate", "Multifruta", "Con pulpa", "Sin pulpa", "Otro"],
        "Licores": ["Vodka", "Whisky", "Coñac", "Ron", "Ginebra", "Tequila", "Licor", "Otro"],
        "Cerveza": ["Clara", "Oscura", "Trigo", "Artesanal", "Sin alcohol", "Otro"],
        
        # --- Química e higiene ---
        "Sanitario": ["Para baño", "Para inodoro", "Para lavabo", "Universal", "Antibacterial", "Otro"],
        "Higiene personal": ["Jabón", "Champú", "Gel de baño", "Desodorante", "Pasta dental", "Maquinilla", "Crema", "Otro"],
        "Equipo": ["Cubo", "Trapeador", "Paño", "Esponja", "Cepillo", "Guantes", "Otro"],
        
        "Otro": ["Nota: Ingrese el nombre del producto"]
    },

	"portugalski": {
		"Frango": ["Frango grelhado", "Frango inteiro", "Coxa inteira", "Sobrecoxa", "Coxinha", "Peito", "Filé", "Costas", "Asas", "Medalhões", "Nuggets", "Bife empanado", "Moído", "Para sopa", "Outro"],
		"Peru": ["Coxa inteira", "Sobrecoxa", "Coxinha", "Coxa enrolada", "Bifes de coxa", "Peito", "Asas", "Costas", "Pontas de asa", "Para sopa", "Moído", "Outro"],
		"Ganso": ["Peito", "Sobrecoxa", "Coxinha", "Asas", "Costas", "Pescoço", "Fígado (foie gras)", "Banha de ganso", "Moído", "Para sopa", "Outro"],
		"Pato": ["Peito", "Sobrecoxa", "Coxinha", "Asas", "Costas", "Pescoço", "Banha de pato", "Moído", "Fígado", "Para sopa", "Outro"],
		"Porco": ["Bife", "Costeleta", "Pescoço", "Pernil", "Lombo", "Costelas", "Barriga", "Paleta", "Espádua", "Jarret", "Moído", "Picado", "Para sopa", "Outro"],
		"Cordeiro": ["Cabeça", "Pescoço", "Paleta", "Lombo", "Peito", "Rim", "Pernil", "Jarret", "Outro"],
		"Boi": ["Bife", "Pescoço", "Peito", "Paleta", "Jarret", "Costelas", "Fralda", "T-bone", "Alcatra", "Rib-eye", "Rabo", "Outro"],
		"Coelho": ["Perna traseira", "Perna dianteira", "Filé do lombo", "Costelas", "Outro"],
		# --- Sitna divljač ---
		"Codorna": ["Carne inteira", "Peito (filés)", "Coxas", "Fígado", "Outro"],
		"Faisão": ["Carne inteira", "Peito (filés)", "Coxas", "Fígado", "Outro"],
		"Perdiz": ["Carne inteira", "Peito (filés)", "Coxas", "Fígado", "Outro"],
		"Pato selvagem": ["Carne inteira", "Peito (filés)", "Coxas", "Fígado", "Outro"],
		"Ganso selvagem": ["Carne inteira", "Peito (filés)", "Coxas", "Fígado", "Outro"],
		"Lebre": ["Perna traseira", "Perna dianteira", "Filé do lombo", "Costelas", "Outro"],
		"Pombo": ["Carne inteira", "Peito (filés)", "Coxas", "Fígado", "Outro"],
		# --- Krupna divljač ---
		"Cervo": ["Perna", "Filé (lombo)", "Bife", "Costelas", "Peito", "Paleta", "Jarrete", "Picado", "Outro"],
		"Corça": ["Perna", "Filé (lombo)", "Bife", "Costelas", "Peito", "Paleta", "Jarrete", "Picado", "Outro"],
		"Cabra selvagem": ["Perna", "Filé (lombo)", "Bife", "Costelas", "Peito", "Paleta", "Jarrete", "Picado", "Outro"],
		"Alce": ["Perna", "Filé (lombo)", "Bife", "Costelas", "Peito", "Paleta", "Jarrete", "Picado", "Outro"],
		"Rena": ["Perna", "Filé (lombo)", "Bife", "Costelas", "Peito", "Paleta", "Jarrete", "Picado", "Outro"],
		"Javali": ["Perna", "Paleta", "Costelas", "Bacon", "Jarrete", "Pescoço", "Cabeça", "Outro"],
		"Bisão": ["Perna", "Paleta", "Bife", "Alcatra", "Costelas", "Lombo", "Pescoço", "Jarrete", "Outro"],
		"Camelo": ["Perna", "Paleta", "Filé (lombo)", "Filé (dorso)", "Costelas", "Peito", "Pescoço", "Corcova", "Outro"],
		"Lhama": ["Perna", "Paleta", "Filé (dorso e lombo)", "Costelas", "Pescoço", "Outro"],
		"Alpaca": ["Perna", "Paleta", "Filé (dorso e lombo)", "Costelas", "Pescoço", "Outro"],
		"Canguru": ["Perna", "Paleta", "Filé (dorso e lombo)", "Costelas", "Rabo", "Outro"],
		"Crocodilo/Jacaré": ["Rabo", "Filé (dorso)", "Coxas", "Outro"],
		"Lagarto": ["Rabo", "Dorso", "Coxas", "Outro"],
		"Cobra": ["Tronco (anéis)", "Outro"],
		"Mar": ["Salmão", "Atum", "Sardinha", "Bacalhau", "Pescada", "Cavala", "Robalo", "Dourada", "Linguado", "Arenque", "Anchova", "Outro"],
		"Água doce": ["Carpa", "Truta", "Bagre", "Percha", "Sander", "Tilápia", "Panga", "Esturjão", "Lúcio", "Carpa capim", "Pirarucu", "Outro"],
		"Frutos do mar": ["Camarão", "Lula", "Vieiras", "Amêijoas", "Mexilhões", "Ostras", "Caranguejo", "Polvo", "Ouriço", "Pepino do mar", "Abalone", "Outro"],
		"Leite": ["Leite", "Kefir", "Creme azedo", "Creme", "Creme de cozinha", "Outro"],
		"Processamento de leite": ["Queijo fresco", "Queijo jovem", "Queijo cremoso", "Gouda", "Edam", "Trappista", "Kashkaval", "Parmesão", "Gorgonzola", "Roquefort", "Halloumi", "Outro"],
		"Fresco": ["Ervilhas", "Feijão verde", "Couve-flor", "Brócolis", "Abóbora", "Tomate", "Pepino", "Pimentão", "Outro"],
		"Tratado termicamente": ["Ervilhas", "Feijão verde", "Milho", "Couve-flor", "Brócolis", "Pimentão", "Abobrinha", "Espinafre", "Outro"],
		"Congelado": ["Ervilhas", "Feijão verde", "Milho", "Couve-flor", "Brócolis", "Pimentão", "Abobrinha", "Espinafre", "Outro"],
		"Frutas": ["Damasco", "Pera", "Cereja", "Geleia de morango", "Geleia de ameixa", "Cereja doce", "Geleia de framboesa", "Marmelo", "Abacaxi", "Geleia de manga", "Outro"],
		"Vegetais": ["Picles", "Pimentão em conserva", "Purê de tomate", "Beterraba", "Ajvar", "Conservas", "Chucrute", "Outro"],
		"Massa": ["Pão", "Pão de centeio", "Ciabatta", "Pão de milho", "Baguete", "Farinha de trigo", "Farinha integral", "Farinha de trigo sarraceno", "Farinha de arroz", "Temperos", "Outro"],
		"Doces": ["Bolos", "Tortas", "Padaria", "Sorvete", "Chocolate", "Doces", "Outro"],
		"Água": ["Mineral", "Sem gás", "Com gás", "Outro"],
		"Vinho": ["Tinto", "Branco", "Rosé", "Outro"],
		"Suco": ["Fruta", "Vegetal", "Outro"],
		"Bebidas destiladas": ["Conhaque", "Vodka", "Uísque", "Outro"],
		"Cerveja": ["Escura", "Clara", "Outro"],
		"Sanitário": ["Limpa-vidros", "Detergente", "Limpa-pisos", "Limpa-banheiro", "Outro"],
		"Higiene pessoal": ["Desodorante", "Lâmina", "Maquiagem", "Sabão", "Xampu", "Creme", "Outro"],
		"Equipamento": ["Balde", "Pano", "Espanador", "Vassoura", "Outro"],
		"Outro": ["Nota: Digite o nome do produto"]
	},

    "francais": {
        # --- Viande blanche ---
        "Poulet": ["Poulet entier", "Poitrine", "Cuisse", "Aile", "Filet", "Dos", "Médaillons", "Nuggets", "Escalope panée", "Viande hachée", "Pour soupe", "Autre"],
        "Dinde": ["Dinde entière", "Poitrine", "Cuisse", "Aile", "Filet", "Dos", "Médaillons", "Pour soupe", "Viande hachée", "Autre"],
        "Oie": ["Oie entière", "Poitrine", "Cuisse", "Aile", "Dos", "Cou", "Foie", "Graisse d'oie", "Viande hachée", "Pour soupe", "Autre"],
        "Canard": ["Canard entier", "Magret", "Cuisse", "Aile", "Dos", "Cou", "Graisse de canard", "Foie", "Viande hachée", "Pour soupe", "Autre"],
        
        # --- Viande rouge ---
        "Porc": ["Filet", "Côtelette", "Jambon", "Échine", "Épaule", "Poitrine", "Côtes", "Jarret", "Viande hachée", "Pour soupe", "Autre"],
        "Agneau": ["Filet", "Côtelette", "Gigot", "Collet", "Épaule", "Poitrine", "Côtes", "Souris", "Viande hachée", "Pour soupe", "Autre"],
        "Bœuf": ["Filet", "Entrecôte", "Rumsteck", "Collier", "Paleron", "Poitrine", "Côtes", "Jarret", "Viande hachée", "Pour soupe", "Autre"],
        "Veau": ["Filet", "Côtelette", "Rognonnade", "Collet", "Épaule", "Poitrine", "Côtes", "Osso buco", "Viande hachée", "Pour soupe", "Autre"],
        "Lapin": ["Cuisses arrière", "Cuisses avant", "Râble", "Côtes", "Pour soupe", "Autre"],
        
        # --- Petit gibier ---
        "Caille": ["Entière", "Poitrine", "Cuisses", "Ailes", "Foie", "Autre"],
        "Faisan": ["Entier", "Poitrine", "Cuisses", "Ailes", "Foie", "Autre"],
        "Perdrix": ["Entière", "Poitrine", "Cuisses", "Ailes", "Foie", "Autre"],
        "Pigeon": ["Entier", "Poitrine", "Cuisses", "Ailes", "Foie", "Autre"],
        "Lièvre": ["Cuisses arrière", "Cuisses avant", "Râble", "Côtes", "Autre"],
        "Canard sauvage": ["Entier", "Poitrine", "Cuisses", "Ailes", "Foie", "Autre"],
        "Oie sauvage": ["Entière", "Poitrine", "Cuisses", "Ailes", "Foie", "Autre"],
        
        # --- Gros gibier ---
        "Cerf": ["Filet", "Côtelette", "Cuissot", "Collet", "Épaule", "Poitrine", "Côtes", "Jarret", "Viande hachée", "Pour soupe", "Autre"],
        "Chevreuil": ["Filet", "Côtelette", "Cuissot", "Collet", "Épaule", "Poitrine", "Côtes", "Jarret", "Viande hachée", "Pour soupe", "Autre"],
        "Sanglier": ["Filet", "Côtelette", "Cuissot", "Collet", "Épaule", "Poitrine", "Côtes", "Jarret", "Viande hachée", "Pour soupe", "Autre"],
        "Élan": ["Filet", "Côtelette", "Cuissot", "Collet", "Épaule", "Poitrine", "Côtes", "Jarret", "Viande hachée", "Pour soupe", "Autre"],
        "Renne": ["Filet", "Côtelette", "Cuissot", "Collet", "Épaule", "Poitrine", "Côtes", "Jarret", "Viande hachée", "Pour soupe", "Autre"],
        "Bison": ["Filet", "Entrecôte", "Cuissot", "Collet", "Épaule", "Poitrine", "Côtes", "Jarret", "Viande hachée", "Pour soupe", "Autre"],
        "Chameau": ["Filet", "Côtelette", "Cuissot", "Collet", "Épaule", "Bosse", "Côtes", "Viande hachée", "Pour soupe", "Autre"],
        "Lama": ["Filet", "Côtelette", "Cuissot", "Collet", "Épaule", "Côtes", "Viande hachée", "Pour soupe", "Autre"],
        "Alpaga": ["Filet", "Côtelette", "Cuissot", "Collet", "Épaule", "Côtes", "Viande hachée", "Pour soupe", "Autre"],
        "Kangourou": ["Filet", "Steak", "Cuissot", "Collet", "Épaule", "Queue", "Viande hachée", "Pour soupe", "Autre"],
        "Crocodile/Alligator": ["Queue", "Filet", "Cuisses", "Autre"],
        "Lézard": ["Queue", "Dos", "Cuisses", "Autre"],
        "Serpent": ["Anneaux", "Autre"],
        
        # --- Poisson ---
        "Mer": ["Filet", "Darnes", "Poisson entier", "Filet avec peau", "Filet sans peau", "Morceaux", "Pour soupe", "Autre"],
        "Eau douce": ["Filet", "Darnes", "Poisson entier", "Filet avec peau", "Filet sans peau", "Morceaux", "Pour soupe", "Autre"],
        "Fruits de mer": ["Crevettes", "Calmar", "Moules", "Huîtres", "Coquilles Saint-Jacques", "Crabes", "Poulpe", "Seiche", "Autre"],
        
        # --- Produits laitiers ---
        "Lait": ["Entier", "Écrémé", "Pasteurisé", "Stérilisé", "Bouilli", "Condensé", "En poudre", "Autre"],
        "Transformation laitière": ["Fromage", "Fromage blanc", "Crème fraîche", "Yaourt", "Kéfir", "Beurre", "Fromage à tartiner", "Autre"],
        
        # --- Légumes ---
        "Frais": ["Entiers", "Coupés", "Lavés", "Pelés", "Râpés", "Autre"],
        "Traité thermiquement": ["Cuits", "Étuvés", "Frits", "Rôtis", "Vapeur", "Autre"],
        "Congelé": ["Entiers", "Coupés", "Mélange", "Purée", "Autre"],
        
        # --- Fruits ---
        "Fruits": ["Entiers", "Tranchés", "Pelés", "Sans pépins", "En conserve", "Séchés", "Autre"],
        
        # --- Pâte et Sucreries ---
        "Pâte": ["Pâte à levure", "Pâte brisée", "Pâte feuilletée", "Pâte à crêpes", "Pâte à pizza", "Pâte à pâtes", "Autre"],
        "Sucreries": ["Chocolat", "Bonbons", "Biscuits", "Gâteaux", "Pâtisseries", "Glace", "Gaufres", "Autre"],
        
        # --- Boissons ---
        "Eau": ["Pétillante", "Plate", "Minérale", "Aromatisée", "Autre"],
        "Vin": ["Rouge", "Blanc", "Rosé", "Mousseux", "Doux", "Sec", "Demi-sec", "Autre"],
        "Jus": ["Pomme", "Orange", "Raisin", "Tomate", "Multifruits", "Avec pulpe", "Sans pulpe", "Autre"],
        "Spiritueux": ["Vodka", "Whisky", "Cognac", "Rhum", "Gin", "Tequila", "Liqueur", "Autre"],
        "Bière": ["Blonde", "Brune", "Blanche", "Artisanale", "Sans alcool", "Autre"],
        
        # --- Chimie et hygiène ---
        "Sanitaire": ["Pour salle de bain", "Pour toilettes", "Pour lavabo", "Universel", "Antibactérien", "Autre"],
        "Hygiène personnelle": ["Savon", "Shampooing", "Gel douche", "Déodorant", "Dentifrice", "Rasoir", "Crème", "Autre"],
        "Équipement": ["Seau", "Balai", "Chiffon", "Éponge", "Brosse", "Gants", "Autre"],
        
        "Autre": ["Note : Saisir le nom du produit"]
    },
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
            font-size: 14px !important; 
            height: 45px !important;
            margin: 1px !important;
            padding: 2px 5px !important;
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
            height: 35px !important;
            margin: 1px !important;
            padding: 2px 3px !important;
        } /* Manji font za mobilni */
    }

    /* Heder - kompaktniji razmak */
    [data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        align-items: center !important;
        justify-content: space-between !important;
        gap: 1px !important; /* SMANJEN razmak */
        margin: 0 !important;
        padding: 0 !important;
    }

    /* Dugmad bez okvira - kompaktnija */
    div.stButton > button {
        border: none !important;
        background: none !important;
        padding: 3px 5px !important; /* SMANJEN padding */
        font-weight: bold !important;
        color: black !important;
        white-space: nowrap !important;
        margin: 1px !important; /* SMANJEN margin */
        font-size: 12px !important;
        min-width: 60px !important;
    }

    div.stButton > button:contains("Izlaz") { 
        color: red !important; 
        background-color: #ffcccc !important;
    }
    
    /* Linija separatora */
    hr { 
        margin: 5px 0 !important; /* SMANJEN margin */
        border-color: #ccc !important;
    }
    
    /* Kategorija dugmad sa bojama - kompaktnija */
    .category-button {
        border-radius: 8px !important;
        margin: 2px !important; /* SMANJEN margin */
        border: 1px solid #ddd !important;
        font-size: 13px !important;
        padding: 8px 5px !important;
    }
    
    /* Stil za jezik dugmad - KOMPAKTNIJE */
    .language-button-container {
        display: flex;
        flex-direction: column;
        align-items: flex-start; /* TEKST U LEVO */
        justify-content: flex-start;
        margin: 5px 0 !important; /* SMANJEN margin */
        padding: 3px !important; /* SMANJEN padding */
        min-height: 100px;
    }
    
    .language-button-container img {
        width: 70px !important; /* SMANJENA veličina */
        height: 45px !important; /* SMANJENA visina */
        object-fit: contain;
        margin-bottom: 3px !important; /* SMANJEN razmak */
        border-radius: 3px;
        box-shadow: 0 1px 2px rgba(0,0,0,0.1);
    }
    
    .language-text {
        font-weight: bold;
        font-size: 12px !important; /* SMANJEN font */
        text-align: left; /* TEKST U LEVO */
        margin-left: 0 !important;
        padding-left: 0 !important;
        width: 100%;
    }
    
    /* Dugmad za jezike - manja i bez teksta */
    .language-select-button {
        width: 70px !important;
        height: 25px !important;
        font-size: 10px !important;
        margin-top: 2px !important;
        padding: 2px !important;
    }
    
    /* Kategorije - mnogo bliže */
    .category-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 3px !important; /* VEOMA MALI razmak */
        margin: 5px 0 !important;
    }
    
    .category-item {
        margin: 1px !important;
        padding: 0 !important;
    }
    
    /* Kompaktniji spacing za sve */
    .stButton > button {
        margin: 1px !important;
        padding: 4px 6px !important;
    }
    
    /* Kompaktniji form elementi */
    .stTextInput, .stTextArea, .stNumberInput, .stSelectbox, .stDateInput {
        margin-bottom: 5px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- DINAMIČKI HEDER ---
def prikazi_heder():
    # CSS za podizanje hedera
    st.markdown("""
        <style>
        .main .block-container {
            padding-top: 0.2rem !important; /* SMANJENO */
        }
        </style>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5 = st.columns([1, 1.5, 1, 1, 1])
    
    # ⭐⭐ KORISTI PAGE_NAME U KEY ZA UNIQUE ⭐⭐
    page_name = st.session_state.get('korak', 'unknown')
    
    with col1: 
        if st.button("🏠", key=f"h_home_{page_name}", help="Početna"):  # SAMO IKONA
            st.session_state.korak = "kategorije"
            st.rerun()
    
    with col2: 
        if st.button("📂", key=f"h_kat_{page_name}", help="Kategorije"):  # SAMO IKONA
            st.session_state.korak = "kategorije"
            st.rerun()
    
    with col3: 
        if st.button("📦", key=f"h_zal_{page_name}", help="Zalihe"):  # SAMO IKONA
            st.session_state.korak = "zalihe"
            st.rerun()
    
    with col4: 
        if st.button("🛒", key=f"h_spis_{page_name}", help="Spisak"):  # SAMO IKONA
            st.session_state.korak = "spisak"
            st.rerun()
    
    with col5: 
        if st.button("🚪", key=f"h_izl_{page_name}", help="Izlaz"):  # SAMO IKONA
            st.session_state.korak = "jezik"
            st.rerun()
    
    st.markdown("<hr>", unsafe_allow_html=True)

# --- STRANICE APLIKACIJE ---

def stranica_jezik():
    """Stranica za odabir jezika - kompaktnija verzija"""
    
    # Dodaj malo prostora na vrhu
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    
    # PRVI RED (3 jezika)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="language-button-container">', unsafe_allow_html=True)
        st.image("icons/Srpski.png", width=70)
        st.markdown('<div class="language-text">Srpski</div>', unsafe_allow_html=True)
        if st.button("✓", key="lang_sr_1", use_container_width=True, type="primary"):
            st.session_state.izabrani_jezik_kod = "Srpski"
            st.session_state.izabrani_jezik_naziv = "Srpski"
            st.session_state.jezik_kljuc = "srpski"
            st.session_state.korak = "kategorije"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="language-button-container">', unsafe_allow_html=True)
        sst.image("icons/English.png", width=70) 
        st.markdown('<div class="language-text">English</div>', unsafe_allow_html=True)
        if st.button("✓", key="lang_en_2", use_container_width=True, type="primary"):
            st.session_state.izabrani_jezik_kod = "Engleski"
            st.session_state.izabrani_jezik_naziv = "English"
            st.session_state.jezik_kljuc = "english"
            st.session_state.korak = "kategorije"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="language-button-container">', unsafe_allow_html=True)
        st.image("icons/Deutsch.png", width=70)
        st.markdown('<div class="language-text">Deutsch</div>', unsafe_allow_html=True)
        if st.button("✓", key="lang_de_3", use_container_width=True, type="primary"):
            st.session_state.izabrani_jezik_kod = "Nemacki"
            st.session_state.izabrani_jezik_naziv = "Deutsch"
            st.session_state.jezik_kljuc = "deutsch"
            st.session_state.korak = "kategorije"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    # DRUGI RED (3 jezika)
    col4, col5, col6 = st.columns(3)
    
    with col4:
        st.markdown('<div class="language-button-container">', unsafe_allow_html=True)
        sst.image("icons/Русский.png", width=70)
        st.markdown('<div class="language-text">Русский</div>', unsafe_allow_html=True)
        if st.button("✓", key="lang_ru_4", use_container_width=True, type="primary"):
            st.session_state.izabrani_jezik_kod = "Ruski"
            st.session_state.izabrani_jezik_naziv = "Русский"
            st.session_state.jezik_kljuc = "ruski"
            st.session_state.korak = "kategorije"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col5:
        st.markdown('<div class="language-button-container">', unsafe_allow_html=True)
        st.image("icons/Українська.png", width=70)
        st.markdown('<div class="language-text">Українська</div>', unsafe_allow_html=True)
        if st.button("✓", key="lang_uk_5", use_container_width=True, type="primary"):
            st.session_state.izabrani_jezik_kod = "Ukrajinski"
            st.session_state.izabrani_jezik_naziv = "Українська"
            st.session_state.jezik_kljuc = "ukrajinski"
            st.session_state.korak = "kategorije"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col6:
        st.markdown('<div class="language-button-container">', unsafe_allow_html=True)
        st.image("icons/Magyar.png", width=70)
        st.markdown('<div class="language-text">Magyar</div>', unsafe_allow_html=True)
        if st.button("✓", key="lang_hu_6", use_container_width=True, type="primary"):
            st.session_state.izabrani_jezik_kod = "Madjarski"
            st.session_state.izabrani_jezik_naziv = "Magyar"
            st.session_state.jezik_kljuc = "hungary"
            st.session_state.korak = "kategorije"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    # TREĆI RED (3 jezika)
    col7, col8, col9 = st.columns(3)
    
    with col7:
        st.markdown('<div class="language-button-container">', unsafe_allow_html=True)
        st.image("icons/Español.png", width=70)
        st.markdown('<div class="language-text">Español</div>', unsafe_allow_html=True)
        if st.button("✓", key="lang_es_7", use_container_width=True, type="primary"):
            st.session_state.izabrani_jezik_kod = "Spanski"
            st.session_state.izabrani_jezik_naziv = "Español"
            st.session_state.jezik_kljuc = "espanol"
            st.session_state.korak = "kategorije"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col8:
        st.markdown('<div class="language-button-container">', unsafe_allow_html=True)
        st.image("icons/Português.png", width=70)
        st.markdown('<div class="language-text">Português</div>', unsafe_allow_html=True)
        if st.button("✓", key="lang_pt_8", use_container_width=True, type="primary"):
            st.session_state.izabrani_jezik_kod = "Portugalski"
            st.session_state.izabrani_jezik_naziv = "Português"
            st.session_state.jezik_kljuc = "portugalski"
            st.session_state.korak = "kategorije"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
	with col9:
		st.markdown('<div class="language-button-container">', unsafe_allow_html=True)
		st.image("icons/Chinese.png", width=70)
		st.markdown('<div class="language-text">中文</div>', unsafe_allow_html=True)
		if st.button("✓", key="lang_zh_9", use_container_width=True, type="primary"):
			st.session_state.izabrani_jezik_kod = "Mandarinski"
			st.session_state.izabrani_jezik_naziv = "中文"
			st.session_state.jezik_kljuc = "mandarinski"
			st.session_state.korak = "kategorije"
			st.rerun()
		st.markdown('</div>', unsafe_allow_html=True)
    
    # ČETVRTI RED (samo francuski centriran)
    col10, col11, col12 = st.columns([1, 2, 1])
    
    with col11:
        st.markdown('<div class="language-button-container">', unsafe_allow_html=True)
        st.image("icons/Français.png", width=70)
        st.markdown('<div class="language-text">Français</div>', unsafe_allow_html=True)
        if st.button("✓", key="lang_fr_10", use_container_width=True, type="primary"):
            st.session_state.izabrani_jezik_kod = "Francuski"
            st.session_state.izabrani_jezik_naziv = "Français"
            st.session_state.jezik_kljuc = "francais"
            st.session_state.korak = "kategorije"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

def stranica_kategorije():
    """Stranica glavnih kategorija - KOMPAKTNIJE"""
    
    # Prikazi heder
    prikazi_heder()
    
    # Naslov na trenutnom jeziku
    st.markdown(f"<h4 style='text-align: center; margin: 5px 0;'>{t('glavne_kategorije')}</h4>", unsafe_allow_html=True)
    
    # Uzmi kategorije na trenutnom jeziku
    jezik = st.session_state.jezik_kljuc
    kategorije = main_categories_translations.get(jezik, main_categories_translations["srpski"])
    
    # KOMPAKTNIJI prikaz kategorija u gridu 2x2 sa minimalnim razmakom
    for i in range(0, len(kategorije), 2):
        col1, col2 = st.columns(2)
        
        # Prva kolona u redu - KOMPAKTNIJE
        if i < len(kategorije):
            kat1 = kategorije[i]
            with col1:
                if st.button(kat1, key=f"kat_{i}", use_container_width=True, type="primary"):
                    st.session_state.trenutna_kategorija = kat1
                    st.session_state.korak = "podkategorije"
                    st.rerun()
        
        # Druga kolona u redu - KOMPAKTNIJE
        if i + 1 < len(kategorije):
            kat2 = kategorije[i + 1]
            with col2:
                if st.button(kat2, key=f"kat_{i+1}", use_container_width=True, type="primary"):
                    st.session_state.trenutna_kategorija = kat2
                    st.session_state.korak = "podkategorije"
                    st.rerun()
    
    # Dugme za nazad - KOMPAKTNIJE
    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button(f"⬅️", use_container_width=True, help=t('nazad')):
            st.session_state.korak = "jezik"
            st.rerun()

def stranica_podkategorije():
    """Stranica podkategorija - KOMPAKTNIJE"""
    
    # Prikazi heder
    prikazi_heder()
    
    # Naslov
    st.markdown(f"<h4 style='text-align: center; margin: 5px 0;'>{t('podkategorije')} {st.session_state.trenutna_kategorija}</h4>", unsafe_allow_html=True)
    
    # Uzmi podkategorije na trenutnom jeziku
    jezik = st.session_state.jezik_kljuc
    trenutna_kategorija = st.session_state.trenutna_kategorija
    
    # Pronađi podkategorije za ovu kategoriju
    podkategorije = subcategories_translations.get("srpski", {}).get(trenutna_kategorija, ["Nema podkategorija"])
    
    # KOMPAKTNIJI prikaz podkategorija
    for i, podkat in enumerate(podkategorije):
        if st.button(podkat, key=f"podkat_{i}", use_container_width=True):
            st.session_state.trenutna_podkategorija = podkat
            st.session_state.korak = "delovi_proizvoda"
            st.rerun()
    
    # Dugmad za navigaciju - KOMPAKTNIJE
    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button(f"⬅️", use_container_width=True, help=t('nazad')):
            st.session_state.korak = "kategorije"
            st.rerun()
    with col2:
        if st.button("🏠", use_container_width=True, help="Početna"):
            st.session_state.korak = "kategorije"
            st.rerun()

def stranica_delovi_proizvoda():
    """Stranica delova proizvoda - KOMPAKTNIJE"""
    
    # Prikazi heder
    prikazi_heder()
    
    # Naslov
    st.markdown(f"<h4 style='text-align: center; margin: 5px 0;'>{t('delovi_proizvoda')} {st.session_state.trenutna_podkategorija}</h4>", unsafe_allow_html=True)
    
    # Uzmi delove proizvoda na trenutnom jeziku
    jezik = st.session_state.jezik_kljuc
    trenutna_podkategorija = st.session_state.trenutna_podkategorija
    
    # Pronađi delove proizvoda za ovu podkategoriju
    delovi = product_parts_translations.get("srpski", {}).get(trenutna_podkategorija, ["Nema delova"])
    
    # KOMPAKTNIJI prikaz delova proizvoda
    for i, deo in enumerate(delovi):
        if st.button(deo, key=f"deo_{i}", use_container_width=True):
            st.session_state.trenutni_deo_proizvoda = deo
            st.session_state.korak = "unos"
            st.rerun()
    
    # Dugmad za navigaciju - KOMPAKTNIJE
    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button(f"⬅️", use_container_width=True, help=t('nazad')):
            st.session_state.korak = "podkategorije"
            st.rerun()
    with col2:
        if st.button("🏠", use_container_width=True, help="Početna"):
            st.session_state.korak = "kategorije"
            st.rerun()

def stranica_unos():
    """Stranica za unos podataka - KOMPAKTNIJE"""
    
    # Prikazi heder
    prikazi_heder()
    
    # Naslov
    st.markdown(f"<h4 style='text-align: center; margin: 5px 0;'>{t('unos_podataka')}</h4>", unsafe_allow_html=True)
    
    # KOMPAKTNIJI prikaz trenutne selekcije
    st.info(f"{st.session_state.trenutna_kategorija} > "
            f"{st.session_state.trenutna_podkategorija} > "
            f"{st.session_state.trenutni_deo_proizvoda}")
    
    # KOMPAKTNIJA forma za unos
    with st.form("unos_forma"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"**{t('naziv_proizvoda')}**")
            naziv = st.text_input("", value=st.session_state.trenutni_deo_proizvoda, label_visibility="collapsed")
            
            st.markdown(f"**{t('opis')}**")
            opis = st.text_area("", height=60, label_visibility="collapsed")
            
            st.markdown(f"**{t('komad')}**")
            komad = st.text_input("", label_visibility="collapsed")
            
            st.markdown(f"**{t('kolicina')}**")
            kolicina = st.number_input("", min_value=0.0, value=1.0, step=0.5, label_visibility="collapsed")
        
        with col2:
            st.markdown(f"**{t('jedinica_mere')}**")
            jedinica = st.selectbox("", ["kg", "g", "l", "ml", "kom"], label_visibility="collapsed")
            
            st.markdown(f"**{t('datum_unosa')}**")
            datum_unosa = st.date_input("", value=datetime.now(), label_visibility="collapsed")
            
            st.markdown(f"**{t('rok_trajanja')}**")
            rok_meseci = st.number_input("", min_value=0, max_value=60, value=12, label_visibility="collapsed")
            
            st.markdown(f"**{t('mesto_skladistenja')}**")
            mesto = st.selectbox("", [
                t('zamrzivac_1'), t('zamrzivac_2'), t('zamrzivac_3'),
                t('frizider'), t('ostava'), "Ostalo"
            ], label_visibility="collapsed")
        
        # Dugme za unos - KOMPAKTNIJE
        submitted = st.form_submit_button(f"✅ {t('unesi')}", use_container_width=True)
            
        if submitted:
            # Izračunaj datum isteka
            datum_isteka = datum_unosa + timedelta(days=rok_meseci * 30)
            
            # Sačuvaj u bazu
            sacuvaj_u_bazu(
                naziv, opis, komad, kolicina, jedinica,
                datum_unosa.strftime("%Y-%m-%d"), rok_meseci,
                datum_isteka.strftime("%Y-%m-%d"), mesto
            )
            
            st.success(f"Proizvod '{naziv}' unet!")
    
    # Dugmad za navigaciju - KOMPAKTNIJE
    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button(f"⬅️", use_container_width=True, help=t('nazad')):
            st.session_state.korak = "delovi_proizvoda"
            st.rerun()
    with col2:
        if st.button("🏠", use_container_width=True, help="Početna"):
            st.session_state.korak = "kategorije"
            st.rerun()

def stranica_zalihe():
    """Stranica za prikaz zaliha - KOMPAKTNIJE"""
    
    # Prikazi heder
    prikazi_heder()
    
    # Naslov
    st.markdown(f"<h4 style='text-align: center; margin: 5px 0;'>{t('stanje_zaliha')}</h4>", unsafe_allow_html=True)
    
    # Učitaj podatke iz baze
    conn = sqlite3.connect('inventory.db')
    df = pd.read_sql_query("SELECT * FROM products", conn)
    conn.close()
    
    if len(df) > 0:
        # KOMPAKTNIJI prikaz tabele
        st.dataframe(df, use_container_width=True, height=300)
        
        # KOMPAKTNIJE opcije
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button(f"🔄", use_container_width=True, help=t('azuriraj')):
                st.session_state.korak = "azuriranje"
                st.rerun()
        with col2:
            if st.button(f"🗑️", use_container_width=True, help=t('obrisi')):
                st.warning("Brisanje - u izradi")
        with col3:
            if st.button(f"🖨️", use_container_width=True, help=t('stampaj')):
                st.info("Štampanje - u izradi")
    else:
        st.info(t('nema_proizvoda'))
    
    # Dugme za nazad - KOMPAKTNIJE
    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    if st.button(f"⬅️", use_container_width=True, help=t('nazad')):
        st.session_state.korak = "kategorije"
        st.rerun()

def stranica_spisak():
    """Stranica za spisak potreba - KOMPAKTNIJE"""
    
    # Prikazi heder
    prikazi_heder()
    
    # Naslov
    st.markdown(f"<h4 style='text-align: center; margin: 5px 0;'>{t('spisak_potreba')}</h4>", unsafe_allow_html=True)
    
    # Učitaj podatke iz baze
    conn = sqlite3.connect('inventory.db')
    df = pd.read_sql_query("SELECT * FROM shopping_list", conn)
    conn.close()
    
    if len(df) > 0:
        # KOMPAKTNIJI prikaz tabele
        st.dataframe(df, use_container_width=True, height=250)
        
        # KOMPAKTNIJE opcije
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button(f"📧", use_container_width=True, help=t('posalji_email')):
                st.session_state.korak = "email"
                st.rerun()
        with col2:
            if st.button(f"📱", use_container_width=True, help=t('posalji_messenger')):
                st.info("Messenger - u izradi")
        with col3:
            if st.button(f"📋", use_container_width=True, help=t('kopiraj')):
                st.info("Kopiranje - u izradi")
    else:
        st.info("Spisak je prazan")
    
    # Dugme za nazad - KOMPAKTNIJE
    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    if st.button(f"⬅️", use_container_width=True, help=t('nazad')):
        st.session_state.korak = "kategorije"
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
    stranica_podkategorije()
elif st.session_state.korak == "delovi_proizvoda":
    stranica_delovi_proizvoda()
elif st.session_state.korak == "unos":
    stranica_unos()
elif st.session_state.korak == "zalihe":
    stranica_zalihe()
elif st.session_state.korak == "spisak":
    stranica_spisak()
elif st.session_state.korak == "email":
    # Prikazi heder i na email stranici
    prikazi_heder()
    st.markdown(f"<h4 style='text-align: center; margin: 5px 0;'>📧 {t('posalji_email')}</h4>", unsafe_allow_html=True)
    st.info("Email funkcionalnost - u izradi")
    if st.button(f"⬅️", help=t('nazad')):
        st.session_state.korak = "spisak"
        st.rerun()
else:
    # Fallback ako korak nije prepoznat
    st.session_state.korak = "jezik"
    st.rerun()
