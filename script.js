// ============================================
// PUNI SCRIPT ZA APLIKACIJU - HIJERARHIJSKI NAZAD
// ============================================
console.log('✅ Script.js je učitan!');

// ===== TRENUTNO STANJE =====
let currentLang = 'en';
let currentCategory = '';
let currentSubcategory = '';
let currentProductPart = '';
let currentScreenState = 'languages';
let newlyAddedIds = new Set(); // id-jevi stavki dodatih/ažuriranih u ovoj sesiji (za plavo isticanje)

// ===== 0. EXIT FUNKCIJA =====
function exitApp() {
    console.log("🚪 Exit dugme kliknuto!");
    
    const loginScreen = document.getElementById('loginScreen');
    const languageScreen = document.getElementById('languageScreen');
    
    const isLoginVisible = loginScreen && window.getComputedStyle(loginScreen).display === 'flex';
    const isLanguageVisible = languageScreen && window.getComputedStyle(languageScreen).display === 'flex';
    
    let poruka;
    if (isLoginVisible || isLanguageVisible) {
        poruka = "Thanks for using this app! 👋";
    } else {
        poruka = translations[currentLang]?.exit_poruka || "Thanks for using this app! 👋";
    }
    
    document.body.innerHTML = '';
    document.body.style.background = '#1a237e';
    document.body.style.margin = '0';
    document.body.style.padding = '0';
    document.body.style.width = '100%';
    document.body.style.height = '100vh';
    document.body.style.display = 'flex';
    document.body.style.justifyContent = 'center';
    document.body.style.alignItems = 'center';
    document.body.style.flexDirection = 'column';
    document.body.style.fontFamily = 'Arial, sans-serif';
    
    document.body.innerHTML = `
        <div style="text-align: center; color: #FFD700;">
            <div style="font-size: 80px; margin-bottom: 20px;">👋</div>
            <div style="font-size: 32px; font-weight: bold;">${poruka}</div>
            <div style="font-size: 16px; color: #888; margin-top: 30px;">© Supplies App</div>
            <button onclick="location.reload()" style="margin-top:30px; padding:12px 30px; background:#FFD700; color:#1a237e; border:none; border-radius:8px; font-size:18px; cursor:pointer; font-weight:bold;">
                🔄 Restart App
            </button>
        </div>
    `;
}

// ===== MODERNI ALERT =====
function showModernAlert(title, message, icon = '📢') {
    const alertDiv = document.getElementById('modernAlert');
    if (!alertDiv) {
        alert(message);
        return;
    }
    document.getElementById('alertIcon').textContent = icon;
    document.getElementById('alertTitle').textContent = title;
    document.getElementById('alertMessage').textContent = message;
    alertDiv.style.display = 'flex';
    alertDiv.classList.add('active');
    setTimeout(() => { closeModernAlert(); }, 2000);
}

function closeModernAlert() {
    const alertDiv = document.getElementById('modernAlert');
    if (alertDiv) {
        alertDiv.classList.remove('active');
        alertDiv.style.display = 'none';
    }
}

// ===== MODERNI CONFIRM (DODAJ OVO OVDE) =====
let confirmCallback = null;

function showModernConfirm(title, message, icon = '⚠️', onYes, onNo) {
    // Proveri da li modernConfirm postoji u HTML-u
    const confirmDiv = document.getElementById('modernConfirm');
    if (!confirmDiv) {
        // Ako nema, koristi običan confirm
        if (confirm(message)) {
            onYes();
        } else {
            onNo();
        }
        return;
    }
    
    document.getElementById('confirmIcon').textContent = icon;
    document.getElementById('confirmTitle').textContent = title;
    document.getElementById('confirmMessage').textContent = message;
    document.getElementById('modernConfirm').style.display = 'flex';
    document.getElementById('modernConfirm').classList.add('active');
    
    confirmCallback = {
        onYes: onYes || function() {},
        onNo: onNo || function() {}
    };
}

function closeModernConfirm() {
    const confirmDiv = document.getElementById('modernConfirm');
    if (confirmDiv) {
        confirmDiv.classList.remove('active');
        confirmDiv.style.display = 'none';
    }
    confirmCallback = null;
}

// Poveži dugmad (ako postoje) - OVO DODAJ U DOMContentLoaded
// ===== SUPPORT FUNKCIJE =====
function openSupportDialog() {
    const dialog = document.getElementById('supportDialog');
    if (dialog) {
        dialog.style.display = 'flex';
        dialog.classList.add('active');
    }
}

function closeSupportDialog() {
    const dialog = document.getElementById('supportDialog');
    if (dialog) {
        dialog.style.display = 'none';
        dialog.classList.remove('active');
    }
}
// ===== 1. JEZICI =====
const languages = {
    sr: { name: 'Srpski', flag: 'icons/jezici/srpski.png' },
    en: { name: 'English', flag: 'icons/jezici/engleski.png' },
    de: { name: 'Deutsch', flag: 'icons/jezici/nemacki.png' },
    hu: { name: 'Magyar', flag: 'icons/jezici/madjarski.png' },
    uk: { name: 'Українська', flag: 'icons/jezici/ukrajinski.png' },
    ru: { name: 'Русский', flag: 'icons/jezici/ruski.png' },
    zh: { name: '中文', flag: 'icons/jezici/mandarinski.png' },
    es: { name: 'Español', flag: 'icons/jezici/spanski.png' },
    pt: { name: 'Português', flag: 'icons/jezici/portugalski.png' },
    fr: { name: 'Français', flag: 'icons/jezici/francuski.png' }
};

// ===== 2. PREVODI =====
const translations = {
    sr: {
        nazad: "Nazad", stanje: "Zalihe", spisak: "Spisak",
        naziv_proizvoda: "Proizvod:", opis: "Opis:",
        komad: "Komada:", kolicina: "Količina:", jedinica_mere: "Jed. mere:",
        datum_unosa: "Datum unosa:", rok_trajanja: "Rok (meseci):",
        automatski_rok: "Rok ističe:", mesto_skladistenja: "Skladište:",
        unesi: "Unesi", odustani: "Odustani", pretrazi: "Pretraži",
        glavne_kategorije: "Glavne kategorije", podkategorije: "Podkategorije",
        delovi_proizvoda: "Delovi proizvoda", unos_podataka: "Unos podataka",
        pregled_unosa: "Pregled unosa", nema_proizvoda: "Nema proizvoda",
        spisak_potreba: "Spisak potreba", azuriraj: "Ažuriraj", obrisi: "Obriši",
        oznaci_sve: "Označi sve", kopiraj: "Kopiraj", obrisi_oznaceno: "Obriši označeno",
        exit_poruka: "Hvala na korišćenju! 👋",
        zamrzivac_1: "Zamrzivač 1", zamrzivac_2: "Zamrzivač 2", zamrzivac_3: "Zamrzivač 3",
        frizider: "Frižider", ostava: "Ostava", Ostalo: "Ostalo",
        kg: "kg", g: "g", kom: "kom", l: "l", ml: "ml", pak: "pak", kutija: "kutija",
        error: "Greška",
        invalid_input: "Neispravan unos",
        please_enter_phone: "Unesite validan broj telefona (9+ cifara)!",
        success: "Uspešno",
        product_saved: "Proizvod sačuvan!",
        product_updated: "Proizvod ažuriran!",
        no_selection: "Nema odabira",
        no_items_selected: "Niste označili nijednu stavku!",
        missing_info: "Nedostaju podaci",
        enter_product_name: "Unesite naziv proizvoda!",
        enter_quantity: "Unesite količinu!",
        shopping_moved: "Proizvod prebačen u spisak potreba (količina 0)!",
        copied: "Lista je kopirana!",
        copy_error: "Greška pri kopiranju.",
        delete_from_shopping: "Obrišite stavku sa spiska?",
        delete_confirm: "Da li ste sigurni da želite da obrišete {count} stavku/ke?",
        delete_confirm_title: "Potvrda brisanja",
        list_empty: "Spisak je prazan"
    },
    en: {
        nazad: "Back", stanje: "Inventory", spisak: "Shopping List",
        naziv_proizvoda: "Product:", opis: "Description:",
        komad: "Piece:", kolicina: "Quantity:", jedinica_mere: "Unit:",
        datum_unosa: "Entry Date:", rok_trajanja: "Shelf Life (months):",
        automatski_rok: "Auto Expiry:", mesto_skladistenja: "Storage:",
        unesi: "Enter", odustani: "Cancel", pretrazi: "Search",
        glavne_kategorije: "Main Categories", podkategorije: "Subcategories",
        delovi_proizvoda: "Product Parts", unos_podataka: "Data Entry",
        pregled_unosa: "Entry Review", nema_proizvoda: "No products",
        spisak_potreba: "Shopping List", azuriraj: "Update", obrisi: "Delete",
        oznaci_sve: "Select all", kopiraj: "Copy", obrisi_oznaceno: "Delete selected",
        exit_poruka: "Thanks for using this app! 👋",
        zamrzivac_1: "Freezer 1", zamrzivac_2: "Freezer 2", zamrzivac_3: "Freezer 3",
        frizider: "Refrigerator", ostava: "Pantry", Ostalo: "Other",
        kg: "kg", g: "g", kom: "pcs", l: "l", ml: "ml", pak: "pck", kutija: "box",
        error: "Error",
        invalid_input: "Invalid Input",
        please_enter_phone: "Please enter a valid phone number (9+ digits)!",
        success: "Success",
        product_saved: "Product saved!",
        product_updated: "Product updated!",
        no_selection: "No Selection",
        no_items_selected: "You have not selected any items!",
        missing_info: "Missing Information",
        enter_product_name: "Please enter a product name!",
        enter_quantity: "Please enter a valid quantity!",
        shopping_moved: "Product moved to shopping list (quantity 0)!",
        copied: "List copied to clipboard!",
        copy_error: "Failed to copy list!",
        delete_from_shopping: "Delete item from shopping list?",
        delete_confirm: "Are you sure you want to delete {count} item(s)?",
        delete_confirm_title: "Delete Confirmation",
        list_empty: "Shopping list is empty"
    },
    de: {
        nazad: "Zurück", stanje: "Bestand", spisak: "Einkaufsliste",
        naziv_proizvoda: "Produkt:", opis: "Beschreibung:",
        komad: "Stück:", kolicina: "Menge:", jedinica_mere: "Einheit:",
        datum_unosa: "Eingangsdatum:", rok_trajanja: "Haltbarkeit (Monate):",
        automatski_rok: "Auto Ablauf:", mesto_skladistenja: "Lager:",
        unesi: "Eingeben", odustani: "Abbrechen", pretrazi: "Suchen",
        glavne_kategorije: "Hauptkategorien", podkategorije: "Unterkategorien",
        delovi_proizvoda: "Produktteile", unos_podataka: "Dateneingabe",
        pregled_unosa: "Eingabeübersicht", nema_proizvoda: "Keine Produkte",
        spisak_potreba: "Einkaufsliste", azuriraj: "Aktualisieren", obrisi: "Löschen",
        oznaci_sve: "Alle auswählen", kopiraj: "Kopieren", obrisi_oznaceno: "Ausgewählte löschen",
        exit_poruka: "Danke für die Nutzung! 👋",
        zamrzivac_1: "Gefrierschrank 1", zamrzivac_2: "Gefrierschrank 2", zamrzivac_3: "Gefrierschrank 3",
        frizider: "Kühlschrank", ostava: "Vorratskammer", Ostalo: "Andere",
        kg: "kg", g: "g", kom: "Stk", l: "l", ml: "ml", pak: "Pck", kutija: "Karton",
        error: "Fehler",
        invalid_input: "Ungültige Eingabe",
        please_enter_phone: "Bitte geben Sie eine gültige Telefonnummer ein (9+ Ziffern)!",
        success: "Erfolg",
        product_saved: "Produkt gespeichert!",
        product_updated: "Produkt aktualisiert!",
        no_selection: "Keine Auswahl",
        no_items_selected: "Sie haben keine Elemente ausgewählt!",
        missing_info: "Fehlende Informationen",
        enter_product_name: "Bitte geben Sie einen Produktnamen ein!",
        enter_quantity: "Bitte geben Sie eine gültige Menge ein!",
        shopping_moved: "Produkt wurde zur Einkaufsliste verschoben (Menge 0)!",
        copied: "Liste kopiert!",
        copy_error: "Fehler beim Kopieren!",
        delete_from_shopping: "Element aus der Einkaufsliste löschen?",
        delete_confirm: "Sind Sie sicher, dass Sie {count} Element(e) löschen möchten?",
        delete_confirm_title: "Löschbestätigung",
        list_empty: "Einkaufsliste ist leer"
    },
    hu: {
        nazad: "Vissza", stanje: "Készlet", spisak: "Bevásárlólista",
        naziv_proizvoda: "Termék:", opis: "Leírás:",
        komad: "Darab:", kolicina: "Mennyiség:", jedinica_mere: "Mértékegység:",
        datum_unosa: "Beírás dátuma:", rok_trajanja: "Szavatosság (hónap):",
        automatski_rok: "Automatikus lejárat:", mesto_skladistenja: "Raktár:",
        unesi: "Bevitel", odustani: "Mégsem", pretrazi: "Keresés",
        glavne_kategorije: "Fő kategóriák", podkategorije: "Alkategóriák",
        delovi_proizvoda: "Termék részei", unos_podataka: "Adatbevitel",
        pregled_unosa: "Bevitel áttekintése", nema_proizvoda: "Nincsenek termékek",
        spisak_potreba: "Bevásárlólista", azuriraj: "Frissítés", obrisi: "Törlés",
        oznaci_sve: "Mindet kijelöl", kopiraj: "Másolás", obrisi_oznaceno: "Kijelöltek törlése",
        exit_poruka: "Köszönjük a használatot! 👋",
        zamrzivac_1: "Mélyhűtő 1", zamrzivac_2: "Mélyhűtő 2", zamrzivac_3: "Mélyhűtő 3",
        frizider: "Hűtőszekrény", ostava: "Spájz", Ostalo: "Egyéb",
        kg: "kg", g: "g", kom: "db", l: "l", ml: "ml", pak: "csom", kutija: "doboz",
        error: "Hiba",
        invalid_input: "Érvénytelen bevitel",
        please_enter_phone: "Kérem, adjon meg egy érvényes telefonszámot (9+ számjegy)!",
        success: "Siker",
        product_saved: "Termék elmentve!",
        product_updated: "Termék frissítve!",
        no_selection: "Nincs kijelölés",
        no_items_selected: "Nem jelölt ki egyetlen elemet sem!",
        missing_info: "Hiányzó információk",
        enter_product_name: "Kérem, adja meg a termék nevét!",
        enter_quantity: "Kérem, adjon meg érvényes mennyiséget!",
        shopping_moved: "Termék áthelyezve a bevásárlólistába (mennyiség 0)!",
        copied: "Lista másolva!",
        copy_error: "Hiba a másolás során!",
        delete_from_shopping: "Törli az elemet a bevásárlólistából?",
        delete_confirm: "Biztosan törölni szeretné {count} elemet?",
        delete_confirm_title: "Törlés megerősítése",
        list_empty: "A bevásárlólista üres"
    },
    uk: {
        nazad: "Назад", stanje: "Запаси", spisak: "Список",
        naziv_proizvoda: "Продукт:", opis: "Опис:",
        komad: "Штука:", kolicina: "Кількість:", jedinica_mere: "Од. виміру:",
        datum_unosa: "Дата внесення:", rok_trajanja: "Термін (місяці):",
        automatski_rok: "Авто термін:", mesto_skladistenja: "Сховище:",
        unesi: "Внести", odustani: "Скасувати", pretrazi: "Пошук",
        glavne_kategorije: "Основні категорії", podkategorije: "Підкатегорії",
        delovi_proizvoda: "Частини продукту", unos_podataka: "Введення даних",
        pregled_unosa: "Огляд введення", nema_proizvoda: "Немає продуктів",
        spisak_potreba: "Список потреб", azuriraj: "Оновити", obrisi: "Видалити",
        oznaci_sve: "Вибрати все", kopiraj: "Копіювати", obrisi_oznaceno: "Видалити вибране",
        exit_poruka: "Дякуємо за використання! 👋",
        zamrzivac_1: "Морозилка 1", zamrzivac_2: "Морозилка 2", zamrzivac_3: "Морозилка 3",
        frizider: "Холодильник", ostava: "Комора", Ostalo: "Інше",
        kg: "кг", g: "г", kom: "шт", l: "л", ml: "мл", pak: "уп", kutija: "кор",
        error: "Помилка",
        invalid_input: "Невірне введення",
        please_enter_phone: "Будь ласка, введіть дійсний номер телефону (9+ цифр)!",
        success: "Успішно",
        product_saved: "Продукт збережено!",
        product_updated: "Продукт оновлено!",
        no_selection: "Немає вибору",
        no_items_selected: "Ви не вибрали жодного елемента!",
        missing_info: "Відсутня інформація",
        enter_product_name: "Будь ласка, введіть назву продукту!",
        enter_quantity: "Будь ласка, введіть дійсну кількість!",
        shopping_moved: "Продукт перенесено до списку потреб (кількість 0)!",
        copied: "Список скопійовано!",
        copy_error: "Помилка копіювання!",
        delete_from_shopping: "Видалити елемент зі списку потреб?",
        delete_confirm: "Ви впевнені, що хочете видалити {count} елемент(ів)?",
        delete_confirm_title: "Підтвердження видалення",
        list_empty: "Список потреб порожній"
    },
    ru: {
        nazad: "Назад", stanje: "Запасы", spisak: "Список",
        naziv_proizvoda: "Продукт:", opis: "Описание:",
        komad: "Штука:", kolicina: "Количество:", jedinica_mere: "Ед. изм.:",
        datum_unosa: "Дата внесения:", rok_trajanja: "Срок (месяцы):",
        automatski_rok: "Авто срок:", mesto_skladistenja: "Склад:",
        unesi: "Внести", odustani: "Отмена", pretrazi: "Поиск",
        glavne_kategorije: "Основные категории", podkategorije: "Подкатегории",
        delovi_proizvoda: "Части продукта", unos_podataka: "Ввод данных",
        pregled_unosa: "Обзор ввода", nema_proizvoda: "Нет продуктов",
        spisak_potreba: "Список потребностей", azuriraj: "Обновить", obrisi: "Удалить",
        oznaci_sve: "Выбрать все", kopiraj: "Копировать", obrisi_oznaceno: "Удалить выбранное",
        exit_poruka: "Спасибо за использование! 👋",
        zamrzivac_1: "Морозилка 1", zamrzivac_2: "Морозилка 2", zamrzivac_3: "Морозилка 3",
        frizider: "Холодильник", ostava: "Кладовая", Ostalo: "Другое",
        kg: "кг", g: "г", kom: "шт", l: "л", ml: "мл", pak: "уп", kutija: "кор",
        error: "Ошибка",
        invalid_input: "Неверный ввод",
        please_enter_phone: "Пожалуйста, введите действительный номер телефона (9+ цифр)!",
        success: "Успешно",
        product_saved: "Продукт сохранён!",
        product_updated: "Продукт обновлён!",
        no_selection: "Нет выбора",
        no_items_selected: "Вы не выбрали ни одного элемента!",
        missing_info: "Отсутствует информация",
        enter_product_name: "Пожалуйста, введите название продукта!",
        enter_quantity: "Пожалуйста, введите действительное количество!",
        shopping_moved: "Продукт перемещён в список потребностей (количество 0)!",
        copied: "Список скопирован!",
        copy_error: "Ошибка копирования!",
        delete_from_shopping: "Удалить элемент из списка потребностей?",
        delete_confirm: "Вы уверены, что хотите удалить {count} элемент(ов)?",
        delete_confirm_title: "Подтверждение удаления",
        list_empty: "Список потребностей пуст"
    },
    zh: {
        nazad: "返回", stanje: "库存", spisak: "购物清单",
        naziv_proizvoda: "产品:", opis: "描述:",
        komad: "件:", kolicina: "数量:", jedinica_mere: "单位:",
        datum_unosa: "录入日期:", rok_trajanja: "保质期(月):",
        automatski_rok: "自动到期:", mesto_skladistenja: "存储:",
        unesi: "输入", odustani: "取消", pretrazi: "搜索",
        glavne_kategorije: "主要类别", podkategorije: "子类别",
        delovi_proizvoda: "产品部件", unos_podataka: "数据输入",
        pregled_unosa: "输入记录查看", nema_proizvoda: "没有产品",
        spisak_potreba: "购物清单", azuriraj: "更新", obrisi: "删除",
        oznaci_sve: "全选", kopiraj: "复制", obrisi_oznaceno: "删除选中",
        exit_poruka: "感谢使用！👋",
        zamrzivac_1: "冷冻柜 1", zamrzivac_2: "冷冻柜 2", zamrzivac_3: "冷冻柜 3",
        frizider: "冰箱", ostava: "储藏室", Ostalo: "其他",
        kg: "公斤", g: "克", kom: "件", l: "升", ml: "毫升", pak: "包", kutija: "盒",
        error: "错误",
        invalid_input: "无效输入",
        please_enter_phone: "请输入有效的电话号码（9位以上）！",
        success: "成功",
        product_saved: "产品已保存！",
        product_updated: "产品已更新！",
        no_selection: "未选择",
        no_items_selected: "您未选择任何项目！",
        missing_info: "信息缺失",
        enter_product_name: "请输入产品名称！",
        enter_quantity: "请输入有效数量！",
        shopping_moved: "产品已移至购物清单（数量0）！",
        copied: "列表已复制！",
        copy_error: "复制失败！",
        delete_from_shopping: "从购物清单中删除此项目？",
        delete_confirm: "您确定要删除 {count} 个项目吗？",
        delete_confirm_title: "删除确认",
        list_empty: "购物清单为空"
    },
    es: {
        nazad: "Atrás", stanje: "Inventario", spisak: "Lista de Compras",
        naziv_proizvoda: "Producto:", opis: "Descripción:",
        komad: "Pieza:", kolicina: "Cantidad:", jedinica_mere: "Unidad:",
        datum_unosa: "Fecha de Entrada:", rok_trajanja: "Caducidad (meses):",
        automatski_rok: "Vencimiento Auto:", mesto_skladistenja: "Almacenamiento:",
        unesi: "Ingresar", odustani: "Cancelar", pretrazi: "Buscar",
        glavne_kategorije: "Categorías Principales", podkategorije: "Subcategorías",
        delovi_proizvoda: "Partes del Producto", unos_podataka: "Entrada de Datos",
        pregled_unosa: "Revisión de entrada", nema_proizvoda: "No hay productos",
        spisak_potreba: "Lista de Compras", azuriraj: "Actualizar", obrisi: "Eliminar",
        oznaci_sve: "Seleccionar todo", kopiraj: "Copiar", obrisi_oznaceno: "Eliminar seleccionados",
        exit_poruka: "¡Gracias por usar! 👋",
        zamrzivac_1: "Congelador 1", zamrzivac_2: "Congelador 2", zamrzivac_3: "Congelador 3",
        frizider: "Refrigerador", ostava: "Despensa", Ostalo: "Otro",
        kg: "kg", g: "g", kom: "pz", l: "l", ml: "ml", pak: "pq", kutija: "caja",
        error: "Error",
        invalid_input: "Entrada inválida",
        please_enter_phone: "¡Por favor, introduzca un número de teléfono válido (9+ dígitos)!",
        success: "Éxito",
        product_saved: "¡Producto guardado!",
        product_updated: "¡Producto actualizado!",
        no_selection: "Sin selección",
        no_items_selected: "¡No ha seleccionado ningún elemento!",
        missing_info: "Información faltante",
        enter_product_name: "¡Por favor, introduzca el nombre del producto!",
        enter_quantity: "¡Por favor, introduzca una cantidad válida!",
        shopping_moved: "¡Producto movido a la lista de compras (cantidad 0)!",
        copied: "¡Lista copiada!",
        copy_error: "¡Error al copiar!",
        delete_from_shopping: "¿Eliminar elemento de la lista de compras?",
        delete_confirm: "¿Está seguro de que desea eliminar {count} elemento(s)?",
        delete_confirm_title: "Confirmación de eliminación",
        list_empty: "La lista de compras está vacía"
    },
    pt: {
        nazad: "Voltar", stanje: "Estoque", spisak: "Lista de Compras",
        naziv_proizvoda: "Produto:", opis: "Descrição:",
        komad: "Peça:", kolicina: "Quantidade:", jedinica_mere: "Unidade:",
        datum_unosa: "Data de Entrada:", rok_trajanja: "Validade (meses):",
        automatski_rok: "Validade Auto:", mesto_skladistenja: "Armazenamento:",
        unesi: "Inserir", odustani: "Cancelar", pretrazi: "Pesquisar",
        glavne_kategorije: "Categorias Principais", podkategorije: "Subcategorias",
        delovi_proizvoda: "Partes do Produto", unos_podataka: "Entrada de Dados",
        pregled_unosa: "Revisão de entrada", nema_proizvoda: "Nenhum produto",
        spisak_potreba: "Lista de Compras", azuriraj: "Atualizar", obrisi: "Excluir",
        oznaci_sve: "Selecionar tudo", kopiraj: "Copiar", obrisi_oznaceno: "Excluir selecionados",
        exit_poruka: "Obrigado por usar! 👋",
        zamrzivac_1: "Congelador 1", zamrzivac_2: "Congelador 2", zamrzivac_3: "Congelador 3",
        frizider: "Geladeira", ostava: "Despensa", Ostalo: "Outro",
        kg: "kg", g: "g", kom: "pç", l: "l", ml: "ml", pak: "pc", kutija: "cx",
        error: "Erro",
        invalid_input: "Entrada inválida",
        please_enter_phone: "Por favor, insira um número de telefone válido (9+ dígitos)!",
        success: "Sucesso",
        product_saved: "Produto guardado!",
        product_updated: "Produto atualizado!",
        no_selection: "Sem seleção",
        no_items_selected: "Não selecionou nenhum item!",
        missing_info: "Informação em falta",
        enter_product_name: "Por favor, insira o nome do produto!",
        enter_quantity: "Por favor, insira uma quantidade válida!",
        shopping_moved: "Produto movido para a lista de compras (quantidade 0)!",
        copied: "Lista copiada!",
        copy_error: "Erro ao copiar!",
        delete_from_shopping: "Eliminar item da lista de compras?",
        delete_confirm: "Tem a certeza que deseja eliminar {count} item(ns)?",
        delete_confirm_title: "Confirmação de exclusão",
        list_empty: "A lista de compras está vazia"
    },
    fr: {
        nazad: "Retour", stanje: "Stock", spisak: "Liste de Courses",
        naziv_proizvoda: "Produit:", opis: "Description:",
        komad: "Pièce:", kolicina: "Quantité:", jedinica_mere: "Unité:",
        datum_unosa: "Date d'entrée:", rok_trajanja: "Durée (mois):",
        automatski_rok: "Expiration Auto:", mesto_skladistenja: "Stockage:",
        unesi: "Entrer", odustani: "Annuler", pretrazi: "Rechercher",
        glavne_kategorije: "Catégories Principales", podkategorije: "Sous-catégories",
        delovi_proizvoda: "Pièces du Produit", unos_podataka: "Saisie de Données",
        pregled_unosa: "Aperçu des saisies", nema_proizvoda: "Aucun produit",
        spisak_potreba: "Liste de Courses", azuriraj: "Mettre à jour", obrisi: "Supprimer",
        oznaci_sve: "Tout sélectionner", kopiraj: "Copier", obrisi_oznaceno: "Supprimer sélectionnés",
        exit_poruka: "Merci d'utiliser! 👋",
        zamrzivac_1: "Congélateur 1", zamrzivac_2: "Congélateur 2", zamrzivac_3: "Congélateur 3",
        frizider: "Réfrigérateur", ostava: "Garde-manger", Ostalo: "Autre",
        kg: "kg", g: "g", kom: "pc", l: "l", ml: "ml", pak: "paq", kutija: "boîte",
        error: "Erreur",
        invalid_input: "Saisie invalide",
        please_enter_phone: "Veuillez entrer un numéro de téléphone valide (9+ chiffres)!",
        success: "Succès",
        product_saved: "Produit enregistré!",
        product_updated: "Produit mis à jour!",
        no_selection: "Aucune sélection",
        no_items_selected: "Vous n'avez sélectionné aucun élément!",
        missing_info: "Informations manquantes",
        enter_product_name: "Veuillez entrer le nom du produit!",
        enter_quantity: "Veuillez entrer une quantité valide!",
        shopping_moved: "Produit déplacé vers la liste de courses (quantité 0)!",
        copied: "Liste copiée!",
        copy_error: "Erreur lors de la copie!",
        delete_from_shopping: "Supprimer l'élément de la liste de courses?",
        delete_confirm: "Êtes-vous sûr de vouloir supprimer {count} élément(s)?",
        delete_confirm_title: "Confirmation de suppression",
        list_empty: "La liste de courses est vide"
    }
};
// ===== POMOĆNA FUNKCIJA ZA PREVODE =====
function t(key) {
    return translations[currentLang]?.[key] || key;
}

// ===== 3. BOJE =====
const categoryColors = {
    "Belo meso": "#FFE295", "Crveno meso": "#F1624B",
    "Sitna divljač": "#F59AA6", "Krupna divljač": "#E19E94",
    "Riba": "#00BBF1", "Mlečni proizvodi": "#ACE1F9",
    "Povrće": "#8FC74A", "Zimnica i kompoti": "#CC98C4",
    "Testo i Slatkiši": "#FFECAB", "Pića": "#F8E06D",
    "Hemija i higijena": "#98D6D2", "Ostalo": "#F58634"
};

const subcategoryColors = {
    "Belo meso": ["#FFEDB5", "#F2D382"],
    "Crveno meso": ["#FABFA9", "#F9AA75"],
    "Sitna divljač": ["#F6C5A4", "#E8A97B"],
    "Krupna divljač": ["#FBCEC8", "#F6998C"],
    "Riba": ["#91D8F7", "#D5EFFC"],
    "Mlečni proizvodi": ["#ACE1F9", "#D5EFFC"],
    "Povrće": ["#8FC74A", "#A0D29E"],
    "Zimnica i kompoti": ["#F3B6D1", "#E894B0"],
    "Testo i Slatkiši": ["#FEE5CB", "#FFECAB"],
    "Pića": ["#FFD76E", "#EEB832"],
    "Hemija i higijena": ["#AADBD2", "#6FC7B8"],
    "Ostalo": ["#D9D9D9", "#BFBFBF"]
};

// ===== 4. GLAVNE KATEGORIJE =====
const mainCategories = {
    sr: ["Belo meso", "Crveno meso", "Sitna divljač", "Krupna divljač", "Riba", "Mlečni proizvodi", "Povrće", "Zimnica i kompoti", "Testo i Slatkiši", "Pića", "Hemija i higijena", "Ostalo"],
    en: ["White meat", "Red meat", "Small game", "Big game", "Fish", "Dairy products", "Vegetables", "Preserves and compotes", "Dough and Sweets", "Beverages", "Chemicals and hygiene", "Other"],
    de: ["Weißes Fleisch", "Rotes Fleisch", "Kleinwild", "Großwild", "Fisch", "Milchprodukte", "Gemüse", "Konserven und Kompotte", "Teig und Süßigkeiten", "Getränke", "Chemie und Hygiene", "Andere"],
    hu: ["Fehér hús", "Vörös hús", "Apróvad", "Nagyvad", "Hal", "Tejtermékek", "Zöldség", "Befőttek és kompótok", "Tészta és Édességek", "Italok", "Kémia és higiénia", "Egyéb"],
    uk: ["Біле м'ясо", "Червоне м'ясо", "Дрібна дичина", "Велика дичина", "Риба", "Молочні продукти", "Овочі", "Консервація та компоти", "Тісто та Солодощі", "Напої", "Хімія та гігієна", "Інше"],
    ru: ["Белое мясо", "Красное мясо", "Мелкая дичь", "Крупная дичь", "Рыба", "Молочные продукты", "Овощи", "Консервация и компоты", "Тесто и Сладости", "Напитки", "Химия и гигиена", "Другое"],
    zh: ["白肉", "红肉", "小型野味", "大型野味", "鱼", "乳制品", "蔬菜", "蜜饯", "面团和糖果", "饮料", "化学品和卫生", "其他"],
    es: ["Carne blanca", "Carne roja", "Caza menor", "Caza mayor", "Pescado", "Productos lácteos", "Verduras", "Conservas y compotas", "Masa y Dulces", "Bebidas", "Química e higiene", "Otro"],
    pt: ["Carne branca", "Carne vermelha", "Caça pequena", "Caça grossa", "Peixe", "Laticínios", "Vegetais", "Conservas e compotas", "Massa e Doces", "Bebidas", "Química e higiene", "Outro"],
    fr: ["Viande blanche", "Viande rouge", "Petit gibier", "Gros gibier", "Poisson", "Produits laitiers", "Légumes", "Conserves et compotes", "Pâte et Sucreries", "Boissons", "Chimie et hygiène", "Autre"]
};

// ===== 5. PODKATEGORIJE =====
const subcategories = {
    sr: {
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
    en: {
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
    de: {
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
    hu: {
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
    uk: {
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
    ru: {
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
    zh: {
        "白肉": ["鸡", "火鸡", "鹅", "鸭", "其他"],
        "红肉": ["猪肉", "羊肉", "羊", "小牛肉", "牛肉", "公牛", "马肉", "兔肉", "其他"],
        "小型野味": ["鹌鹑", "野鸡", "鹧鸪", "野鸭", "野鹅", "野兔", "鸽子", "其他"],
        "大型野味": ["鹿", "狍子", "野山羊", "驼鹿", "驯鹿", "野猪", "野牛", "骆驼", "羊驼", "袋鼠", "鳄鱼", "蜥蜴", "蛇", "其他"],
        "鱼": ["海鱼", "淡水鱼", "海鲜", "其他"],
        "乳制品": ["牛奶", "乳制品加工", "其他"],
        "蔬菜": ["新鲜", "热处理", "冷冻", "其他"],
        "蜜饯": ["水果", "蔬菜", "其他"],
        "面团和糖果": ["面团", "糖果", "其他"],
        "饮料": ["水", "葡萄酒", "果汁", "烈酒", "啤酒", "其他"],
        "化学品和卫生": ["卫生", "个人卫生", "设备", "其他"],
        "其他": ["其他"]
    },
    es: {
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
    pt: {
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
    fr: {
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
};
// ===== 7. POMOĆNE FUNKCIJE =====
function t(key) {
    return translations[currentLang]?.[key] || key;
}

function showScreen(screenId) {
    document.querySelectorAll('.screen').forEach(s => s.style.display = 'none');
    const screen = document.getElementById(screenId);
    if (screen) screen.style.display = 'flex';
}

function updateHeaderTexts() {
    const backText = document.getElementById('backText');
    const invText = document.getElementById('invText');
    const shopText = document.getElementById('shopText');
    if (backText) backText.textContent = t('nazad');
    if (invText) invText.textContent = t('stanje');
    if (shopText) shopText.textContent = t('spisak');
    
    // Ažuriraj placeholder za pretragu ako postoji
    const searchInput = document.getElementById('inventorySearchInput');
    if (searchInput) {
        searchInput.placeholder = `${t('pretrazi')}...`;
    }
}

function getMainCategories() {
    return mainCategories[currentLang] || mainCategories.sr;
}

function getSubcategories(category) {
    const sub = subcategories[currentLang] || subcategories.sr || {};
    return sub[category] || ['Ostalo'];
}

function getProductParts(subcategory) {
    if (typeof productParts !== 'undefined' && productParts[currentLang] && productParts[currentLang][subcategory]) {
        return productParts[currentLang][subcategory];
    }
    if (typeof productParts !== 'undefined' && productParts.sr && productParts.sr[subcategory]) {
        return productParts.sr[subcategory];
    }
    return ["Ostalo"];
}

function getCategoryColor(category) {
    const srList = mainCategories.sr;
    for (let i = 0; i < srList.length; i++) {
        if (category === mainCategories[currentLang]?.[i] || category === srList[i]) {
            return categoryColors[srList[i]] || '#cccccc';
        }
    }
    return '#cccccc';
}

function getSubcategoryColors(category) {
    const srList = mainCategories.sr;
    for (let i = 0; i < srList.length; i++) {
        if (category === mainCategories[currentLang]?.[i] || category === srList[i]) {
            return subcategoryColors[srList[i]] || ['#FFEDB5', '#F2D382'];
        }
    }
    return ['#FFEDB5', '#F2D382'];
}

function isOtherButton(text) {
    const ostaloVariants = ["Ostalo", "Other", "Andere", "Egyéb", "Інше", "Другое", "其他", "Otro", "Outro", "Autre"];
    return ostaloVariants.includes(text);
}

// ===== 8. RENDER FUNKCIJE =====
function renderLanguages() {
    if (!currentLang || currentLang === '') {
        currentLang = 'en';
    }
    currentScreenState = 'languages';
    const grid = document.getElementById('languageGrid');
    if (!grid) return;
    grid.innerHTML = '';
    Object.keys(languages).forEach(code => {
        const lang = languages[code];
        const btn = document.createElement('button');
        btn.className = 'lang-btn-main';
        btn.innerHTML = `
            <img src="${lang.flag}?v=3" alt="${lang.name}" onerror="this.style.display='none'">
            <span class="lang-name">${lang.name}</span>
        `;
        btn.onclick = () => selectLanguage(code);
        grid.appendChild(btn);
    });
    console.log('✅ Jezici prikazani');
}

function selectLanguage(langCode) {
    currentLang = langCode;
    showScreen('mainScreen');
    updateHeaderTexts();
    renderCategories();
}

function renderCategories() {
    currentScreenState = 'categories';
    const content = document.getElementById('mainContent');
    if (!content) return;
    const catList = getMainCategories();
    let html = `<div class="title">${t('glavne_kategorije')}</div>`;
    html += `<div class="categories-grid">`;
    catList.forEach(cat => {
        const color = getCategoryColor(cat);
        if (isOtherButton(cat)) {
            html += `<button class="category-btn" style="background:${color};" onclick="renderDataEntry('')">${cat} ➜</button>`;
        } else {
            html += `<button class="category-btn" style="background:${color};" onclick="renderSubcategories('${cat.replace(/'/g, "\\'")}')">${cat}</button>`;
        }
    });
    html += `</div>`;
    content.innerHTML = html;
}

function renderSubcategories(category) {
    currentScreenState = 'subcategories';
    currentCategory = category;
    const content = document.getElementById('mainContent');
    if (!content) return;

    const langSubs = subcategories[currentLang] || subcategories.sr || {};
    const subData = langSubs[category] || [];
    const colors = getSubcategoryColors(category);
    
    let html = `<div class="title">${t('podkategorije')}</div>`;
    html += `<div class="categories-grid">`;
    
    if (Array.isArray(subData) && subData.length > 0) {
        let displayData = [...subData];
        const hasOstalo = displayData.some(item => isOtherButton(item));
        if (!hasOstalo) {
            displayData.push(t('Ostalo') || "Ostalo");
        }
        
        displayData.forEach((item, idx) => {
            const color = colors[idx % colors.length];
            const safeItem = item.toString().replace(/'/g, "\\'");
            const hasParts = typeof productParts !== 'undefined' && ((productParts[currentLang] && productParts[currentLang][item]) || (productParts.sr && productParts.sr[item]));
            
            if (isOtherButton(item)) {
                html += `<button class="category-btn" style="background:${color};" onclick="renderDataEntry('')">${item} ➜</button>`;
            } else if (hasParts) {
                html += `<button class="category-btn" style="background:${color};" onclick="renderProductParts('${safeItem}')">${item}</button>`;
            } else {
                html += `<button class="category-btn" style="background:${color};" onclick="renderDataEntry('${safeItem}')">${item}</button>`;
            }
        });
    } else if (subData && typeof subData === 'object') {
        const keys = Object.keys(subData);
        let displayKeys = [...keys];
        const hasOstalo = displayKeys.some(key => isOtherButton(key));
        if (!hasOstalo) {
            displayKeys.push(t('Ostalo') || "Ostalo");
        }
        displayKeys.forEach((groupName, idx) => {
            const color = colors[idx % colors.length];
            const safeGroup = groupName.toString().replace(/'/g, "\\'");
            if (isOtherButton(groupName)) {
                html += `<button class="category-btn" style="background:${color};" onclick="renderDataEntry('')">${groupName} ➜</button>`;
            } else {
                html += `<button class="category-btn" style="background:${color};" onclick="renderSubcategoryGroup('${category.replace(/'/g, "\\'")}', '${safeGroup}')">${groupName}</button>`;
            }
        });
    } else {
        html += `<button class="category-btn" style="background:#ddd;" onclick="renderDataEntry('')">${t('Ostalo') || "Ostalo"} ➜</button>`;
    }
    
    html += `</div>`;
    content.innerHTML = html;
}

function renderSubcategoryGroup(category, groupName) {
    currentScreenState = 'subcategories';
    const content = document.getElementById('mainContent');
    const sub = subcategories[currentLang] || subcategories.sr || {};
    let items = sub[category] ? sub[category][groupName] : [];
    const colors = getSubcategoryColors(category);
    
    let html = `<div class="title">${groupName}</div>`;
    html += `<div class="categories-grid">`;
    if (Array.isArray(items) && items.length > 0) {
        let displayItems = [...items];
        const hasOstalo = displayItems.some(item => isOtherButton(item));
        if (!hasOstalo) {
            displayItems.push(t('Ostalo') || "Ostalo");
        }
        displayItems.forEach((item, idx) => {
            const color = colors[idx % colors.length];
            const safeItem = item.toString().replace(/'/g, "\\'");
            const hasParts = typeof productParts !== 'undefined' && ((productParts[currentLang] && productParts[currentLang][item]) || (productParts.sr && productParts.sr[item]));
            
            if (isOtherButton(item)) {
                html += `<button class="category-btn" style="background:${color};" onclick="renderDataEntry('')">${item} ➜</button>`;
            } else if (hasParts) {
                html += `<button class="category-btn" style="background:${color};" onclick="renderProductParts('${safeItem}')">${item}</button>`;
            } else {
                html += `<button class="category-btn" style="background:${color};" onclick="renderDataEntry('${safeItem}')">${item}</button>`;
            }
        });
    } else {
        html += `<button class="category-btn" style="background:#ddd;" onclick="renderDataEntry('')">${t('Ostalo') || "Ostalo"} ➜</button>`;
    }
    html += `</div>`;
    content.innerHTML = html;
}

function renderProductParts(subcategory) {
    currentScreenState = 'productParts';
    currentSubcategory = subcategory;
    const content = document.getElementById('mainContent');
    let parts = getProductParts(subcategory);
    const colors = getSubcategoryColors(currentCategory);
    
    let html = `<div class="title">${subcategory}</div>`;
    html += `<div style="margin-bottom:15px;text-align:center;font-size:20px;color:#666;">${t('delovi_proizvoda')}</div>`;
    html += `<div class="categories-grid">`;
    if (parts && parts.length > 0) {
        let displayParts = [...parts];
        const hasOstalo = displayParts.some(part => isOtherButton(part));
        if (!hasOstalo) {
            displayParts.push(t('Ostalo') || "Ostalo");
        }
        displayParts.forEach((part, idx) => {
            const color = colors[idx % colors.length];
            const safePart = part.toString().replace(/'/g, "\\'");
            if (isOtherButton(part)) {
                html += `<button class="category-btn" style="background:${color};" onclick="renderDataEntry('')">${part} ➜</button>`;
            } else {
                html += `<button class="category-btn" style="background:${color};" onclick="renderDataEntry('${safePart}')">${part}</button>`;
            }
        });
    } else {
        html += `<button class="category-btn" style="background:#ddd;" onclick="renderDataEntry('')">${t('Ostalo') || "Ostalo"} ➜</button>`;
    }
    html += `</div>`;
    content.innerHTML = html;
}

function renderDataEntry(productName) {
    currentScreenState = 'dataEntry';
    currentProductPart = productName;
    const content = document.getElementById('mainContent');
    if (!content) return;
    const today = new Date().toISOString().split('T')[0];
    content.innerHTML = `
        <div class="title">${t('unos_podataka')}</div>
        <div class="row"><label>${t('naziv_proizvoda')}</label><input type="text" id="productInput" value="${productName || ''}"></div>
        <div class="row"><label>${t('opis')}</label><input type="text" id="descriptionInput"></div>
        <div class="row">
            <label>${t('komad')} <span style="color:red;">*</span></label>
            <div class="inline-group">
                <input type="text" id="pieceInput">
                <label>${t('kolicina')} <span style="color:red;">*</span></label>
                <input type="number" id="quantityInput" step="0.1">
                <label>${t('jedinica_mere')}</label>
                <select id="unitSelect">
                    <option value="kg">${t('kg')}</option>
                    <option value="g">${t('g')}</option>
                    <option value="kom">${t('kom')}</option>
                    <option value="l">${t('l')}</option>
                    <option value="ml">${t('ml')}</option>
                    <option value="pak">${t('pak')}</option>
                    <option value="kutija">${t('kutija')}</option>
                </select>
            </div>
        </div>
        <div class="row">
            <label>${t('datum_unosa')}</label>
            <div class="inline-group">
                <input type="date" id="dateInput" value="${today}">
                <label>${t('rok_trajanja')} <span style="color:red;">*</span></label>
                <input type="number" id="shelfLifeInput">
                <span style="font-size:18px;">mes</span>
            </div>
        </div>
        <div class="row">
            <label>${t('automatski_rok')}</label>
            <div class="inline-group"><span id="expiryDisplay">-</span></div>
        </div>
        <div class="row">
            <label>${t('mesto_skladistenja')}</label>
            <select id="storageSelect">
                <option value="${t('zamrzivac_1')}">❄️ ${t('zamrzivac_1')}</option>
                <option value="${t('zamrzivac_2')}">❄️ ${t('zamrzivac_2')}</option>
                <option value="${t('zamrzivac_3')}">❄️ ${t('zamrzivac_3')}</option>
                <option value="${t('frizider')}">🧊 ${t('frizider')}</option>
                <option value="${t('ostava')}">🏠 ${t('ostava')}</option>
                <option value="${t('Ostalo')}">📦 ${t('Ostalo')}</option>
            </select>
        </div>
        <div class="btn-group">
            <button class="btn-save" onclick="saveProduct()">✅ ${t('unesi')}</button>
            <button class="btn-cancel" onclick="handleBackAction()">✖ ${t('odustani')}</button>
        </div>
        <div class="table-container">
            <div class="table-title">📊 ${t('pregled_unosa')}</div>
            <div id="entriesContainer"></div>
        </div>
    `;
    document.getElementById('dateInput')?.addEventListener('change', updateExpiryDate);
    document.getElementById('dateInput')?.addEventListener('input', updateExpiryDate);
    document.getElementById('shelfLifeInput')?.addEventListener('change', updateExpiryDate);
    document.getElementById('shelfLifeInput')?.addEventListener('input', updateExpiryDate);
    document.getElementById('productInput')?.focus();
    updateExpiryDate();
    prikaziSveUnose();
}
function prikaziSveUnose() {
    const container = document.getElementById('entriesContainer');
    if (!container) return;
    const zalihe = JSON.parse(localStorage.getItem('zalihe') || '[]');
    container.innerHTML = `
        <div class="table-row header-row">
            <div class="cell">${t('komad')}</div>
            <div class="cell">${t('kolicina')}</div>
            <div class="cell">${t('jedinica_mere')}</div>
            <div class="cell">${t('rok_trajanja')}</div>
            <div class="cell">${t('mesto_skladistenja')}</div>
        </div>
    `;
    const aktivni = zalihe.filter(p => p.quantity > 0);
    if (aktivni.length === 0) {
        const row = document.createElement('div');
        row.className = 'table-row';
        row.innerHTML = `<div class="cell" style="grid-column:span 5;padding:20px;color:#999;text-align:center;">${t('nema_proizvoda')}</div>`;
        container.appendChild(row);
        return;
    }
    aktivni.forEach(p => {
        const expiry = new Date(p.entry_date);
        expiry.setMonth(expiry.getMonth() + p.shelf_life_months);
        const expiryDisplay = expiry.toLocaleDateString('sr-RS', { month: '2-digit', year: '2-digit' });
        const row = document.createElement('div');
        row.className = 'table-row';
        row.innerHTML = `
            <div class="cell">${p.piece || '-'}</div>
            <div class="cell">${p.quantity}</div>
            <div class="cell">${p.unit}</div>
            <div class="cell">${expiryDisplay}</div>
            <div class="cell">${p.storage_location}</div>
        `;
        container.appendChild(row);
    });
}

function updateExpiryDate() {
    const dateInput = document.getElementById('dateInput');
    const shelfLifeInput = document.getElementById('shelfLifeInput');
    const expiryDisplay = document.getElementById('expiryDisplay');
    if (!dateInput || !shelfLifeInput || !expiryDisplay) return;
    const date = dateInput.value;
    const months = parseInt(shelfLifeInput.value) || 0;
    if (date && months > 0) {
        const expiry = new Date(date);
        expiry.setMonth(expiry.getMonth() + months);
        expiryDisplay.textContent = expiry.toLocaleDateString('sr-RS', { day: '2-digit', month: '2-digit', year: 'numeric' });
    } else {
        expiryDisplay.textContent = '-';
    }
}

function saveProduct() {
    const product = document.getElementById('productInput')?.value.trim();
    const piece = document.getElementById('pieceInput')?.value.trim();
    const quantity = document.getElementById('quantityInput')?.value.trim();
    const shelfLife = document.getElementById('shelfLifeInput')?.value.trim();
    
    // Provera obaveznih polja - OVE PORUKE OSTAJU (validacija je bitna)
    if (!product) {
        showModernAlert(t('missing_info'), t('enter_product_name'), '📝');
        document.getElementById('productInput')?.focus();
        return;
    }
    if (!piece) {
        showModernAlert(t('missing_info'), 'Unesite komad!', '📝');
        document.getElementById('pieceInput')?.focus();
        return;
    }
    if (!quantity || isNaN(parseFloat(quantity))) {
        showModernAlert(t('missing_info'), t('enter_quantity'), '📝');
        document.getElementById('quantityInput')?.focus();
        return;
    }
    if (!shelfLife || isNaN(parseInt(shelfLife))) {
        showModernAlert(t('missing_info'), 'Unesite rok trajanja (meseci)!', '📝');
        document.getElementById('shelfLifeInput')?.focus();
        return;
    }
    
    const novaKolicina = parseFloat(quantity);
    const noviUnit = document.getElementById('unitSelect')?.value || 'kg';
    const noviDatum = document.getElementById('dateInput')?.value || new Date().toISOString().split('T')[0];
    const noviRok = parseInt(shelfLife);
    const novoSkladiste = document.getElementById('storageSelect')?.value || 'Ostalo';
    const novOpis = document.getElementById('descriptionInput')?.value.trim() || '';

    let zalihe = JSON.parse(localStorage.getItem('zalihe') || '[]');

    const postojeci = zalihe.find(p =>
        p.quantity > 0 &&
        p.product_name.trim().toLowerCase() === product.trim().toLowerCase() &&
        p.storage_location === novoSkladiste &&
        p.unit === noviUnit
    );

    if (postojeci) {
        postojeci.quantity = parseFloat((postojeci.quantity + novaKolicina).toFixed(3));
        postojeci.piece = piece;
        postojeci.description = novOpis;
        postojeci.entry_date = noviDatum;
        postojeci.shelf_life_months = noviRok;
        newlyAddedIds.add(postojeci.id);
    } else {
        const productData = {
            id: Date.now(),
            product_name: product,
            description: novOpis,
            piece: piece,
            quantity: novaKolicina,
            unit: noviUnit,
            entry_date: noviDatum,
            shelf_life_months: noviRok,
            storage_location: novoSkladiste
        };
        zalihe.push(productData);
        newlyAddedIds.add(productData.id);
    }

    localStorage.setItem('zalihe', JSON.stringify(zalihe));
    prikaziSveUnose();
    
    // Resetuj polja
    document.getElementById('pieceInput').value = '';
    document.getElementById('quantityInput').value = '';
    document.getElementById('shelfLifeInput').value = '';
    document.getElementById('descriptionInput').value = '';
    document.getElementById('productInput').focus();
    document.getElementById('productInput').select();
    
    // ❌ UKLONJEN POPUP: showModernAlert(t('success'), t('product_saved'), '✅');
    // Umesto toga - samo vizuelna potvrda bez prekida rada
    console.log('✅ Proizvod sačuvan bez popup-a');
}
function renderInventory() {
    currentScreenState = 'inventory';
    const content = document.getElementById('mainContent');
    if (!content) return;
    const zalihe = JSON.parse(localStorage.getItem('zalihe') || '[]');
    const aktivneZalihe = zalihe.filter(p => p.quantity > 0);
    
    let html = `<div class="title">${t('stanje')}</div>`;
    html += `<div style="display:flex; gap:10px; margin-bottom:15px; flex-wrap:wrap; align-items:center;">`;
    html += `<button onclick="azurirajZalihe()" style="background:#4CAF50; color:white; border:none; padding:10px 20px; border-radius:8px; font-size:16px; cursor:pointer;">✅ ${t('azuriraj')}</button>`;
    html += `<button onclick="obrisiZalihe()" style="background:#666; color:white; border:none; padding:10px 20px; border-radius:8px; font-size:16px; cursor:pointer;">🗑️ ${t('obrisi')}</button>`;
    html += `<button onclick="renderCategories()" style="background:#f44336; color:white; border:none; padding:10px 20px; border-radius:8px; font-size:16px; cursor:pointer;">✖ ${t('odustani')}</button>`;
    
    // ===== NOVO: POLJE ZA PRETRAGU =====
    html += `<div style="position:relative; flex:1; min-width:200px;">`;
    html += `<input type="text" id="inventorySearchInput" 
                placeholder="${t('pretrazi')}..." 
                autocomplete="off"
                style="width:100%; padding:10px 15px; border:2px solid #1a237e; border-radius:8px; font-size:16px; box-sizing:border-box;"
                oninput="handleInventorySearchInput(this.value)"
                onkeydown="handleInventorySearchKeydown(event)">`;
    html += `<div id="inventorySuggestions" style="position:absolute; top:100%; left:0; right:0; background:white; border:1px solid #ccc; border-top:none; border-radius:0 0 8px 8px; max-height:200px; overflow-y:auto; z-index:1000; display:none; box-shadow:0 4px 8px rgba(0,0,0,0.1);"></div>`;
    html += `</div>`;
    html += `</div>`;
    
    html += `<div class="table-container" style="max-height:400px; overflow-y:auto;">`;
    html += `<div class="table-title">📦 ${t('stanje')}</div>`;
    html += `<div id="inventoryTable">`;
    html += `<div class="table-row header-row" style="display:grid; grid-template-columns:40px 1.2fr 1.2fr 0.8fr 0.8fr 0.8fr 0.8fr 1fr; gap:2px; background:#f0f0f0; font-weight:bold; border-bottom:2px solid #ccc; padding:5px 0;">`;
    html += `<div class="cell" style="text-align:center;"><input type="checkbox" id="selectAll" onchange="toggleAllCheckboxes()"></div>`;
    html += `<div class="cell">${t('naziv_proizvoda')}</div>`;
    html += `<div class="cell">${t('opis')}</div>`;
    html += `<div class="cell">${t('komad')}</div>`;
    html += `<div class="cell">${t('kolicina')}</div>`;
    html += `<div class="cell">${t('jedinica_mere')}</div>`;
    html += `<div class="cell">${t('rok_trajanja')}</div>`;
    html += `<div class="cell">${t('mesto_skladistenja')}</div>`;
    html += `</div>`;
    
    if (aktivneZalihe.length === 0) {
        html += `<div class="table-row"><div class="cell" style="grid-column:span 8;padding:30px;color:#999;text-align:center;">${t('nema_proizvoda')}</div></div>`;
    } else {
        aktivneZalihe.forEach((p, idx) => {
            const originalIndex = zalihe.indexOf(p);
            const expiry = new Date(p.entry_date);
            expiry.setMonth(expiry.getMonth() + p.shelf_life_months);
            const expiryDisplay = expiry.toLocaleDateString('sr-RS', { month: '2-digit', year: '2-digit' });
            const isLow = (p.unit === 'g' && p.quantity <= 1000) || (p.unit === 'kg' && p.quantity <= 1) || ((p.unit === 'kom' || p.unit === 'pcs') && p.quantity <= 2);
            const isNew = newlyAddedIds.has(p.id);

            let bgColor = '';
            let textColor = '';
            if (isLow) {
                bgColor = '#f44336';
                textColor = 'white';
            } else if (isNew) {
                bgColor = '#BBDEFB';
            }
            
            // ===== NOVO: data-search-row atribut za lakše pronalaženje =====
            const rowStyle = `display:grid; grid-template-columns:40px 1.2fr 1.2fr 0.8fr 0.8fr 0.8fr 0.8fr 1fr; gap:2px; border-bottom:1px solid #eee; padding:5px 0; background:${bgColor}; color:${textColor};`;
            const searchKey = (p.product_name || '').toLowerCase();
            
            html += `<div class="table-row" data-search-row="${searchKey}" data-original-index="${originalIndex}" style="${rowStyle}">`;
            html += `<div class="cell" style="text-align:center;"><input type="checkbox" class="row-checkbox" data-index="${originalIndex}"></div>`;
            html += `<div class="cell">${p.product_name}</div>`;
            html += `<div class="cell">${p.description || ''}</div>`;
            html += `<div class="cell">${p.piece || '-'}</div>`;
            html += `<div class="cell">${p.quantity}</div>`;
            html += `<div class="cell">${p.unit}</div>`;
            html += `<div class="cell">${expiryDisplay}</div>`;
            html += `<div class="cell">${p.storage_location}</div>`;
            html += `</div>`;
        });
    }
    html += `</div></div>`;
    content.innerHTML = html;
}
// ===== PRETRAGA U INVENTARU =====
let inventorySearchTimeout = null;

function handleInventorySearchInput(value) {
    const suggestions = document.getElementById('inventorySuggestions');
    if (!suggestions) return;
    
    clearTimeout(inventorySearchTimeout);
    const query = value.trim().toLowerCase();
    
    if (query.length === 0) {
        suggestions.style.display = 'none';
        suggestions.innerHTML = '';
        return;
    }
    
    inventorySearchTimeout = setTimeout(() => {
        const zalihe = JSON.parse(localStorage.getItem('zalihe') || '[]');
        const aktivne = zalihe.filter(p => p.quantity > 0);
        
        // Pronađi sve koji počinju sa upisanim slovima
        const matches = aktivne.filter(p => 
            (p.product_name || '').toLowerCase().startsWith(query)
        );
        
        // Jedinstveni nazivi
        const uniqueNames = [...new Set(matches.map(p => p.product_name))];
        
        if (uniqueNames.length === 0) {
            suggestions.style.display = 'none';
            suggestions.innerHTML = '';
            return;
        }
        
        // Ako ima SAMO JEDAN pogodak - automatski dopuni polje (autocomplete)
        if (uniqueNames.length === 1) {
            const input = document.getElementById('inventorySearchInput');
            if (input && input.value.toLowerCase() !== uniqueNames[0].toLowerCase()) {
                input.value = uniqueNames[0];
                // Postavi kursor na kraj
                input.setSelectionRange(input.value.length, input.value.length);
                // Odmah izvrši pretragu
                performInventorySearch(uniqueNames[0]);
            }
            suggestions.style.display = 'none';
            suggestions.innerHTML = '';
            return;
        }
        
        // Prikaži listu predloga
        suggestions.innerHTML = '';
        uniqueNames.slice(0, 10).forEach(name => {
            const div = document.createElement('div');
            div.textContent = name;
            div.style.padding = '10px 15px';
            div.style.cursor = 'pointer';
            div.style.borderBottom = '1px solid #eee';
            div.style.fontSize = '15px';
            div.onmouseover = () => { div.style.background = '#e3f2fd'; };
            div.onmouseout = () => { div.style.background = 'white'; };
            div.onclick = () => {
                const input = document.getElementById('inventorySearchInput');
                input.value = name;
                suggestions.style.display = 'none';
                suggestions.innerHTML = '';
                performInventorySearch(name);
            };
            suggestions.appendChild(div);
        });
        suggestions.style.display = 'block';
    }, 150);
}

function handleInventorySearchKeydown(event) {
    if (event.key === 'Enter') {
        event.preventDefault();
        const input = document.getElementById('inventorySearchInput');
        const suggestions = document.getElementById('inventorySuggestions');
        if (suggestions) {
            suggestions.style.display = 'none';
            suggestions.innerHTML = '';
        }
        if (input && input.value.trim()) {
            performInventorySearch(input.value.trim());
        }
    } else if (event.key === 'Escape') {
        const suggestions = document.getElementById('inventorySuggestions');
        if (suggestions) {
            suggestions.style.display = 'none';
            suggestions.innerHTML = '';
        }
    }
}

function performInventorySearch(searchTerm) {
    const query = searchTerm.trim().toLowerCase();
    if (!query) return;
    
    const rows = document.querySelectorAll('[data-search-row]');
    let foundRow = null;
    let matchCount = 0;
    
    rows.forEach(row => {
        const rowKey = row.getAttribute('data-search-row');
        // Resetuj prethodno isticanje
        row.style.background = '';
        row.style.color = '';
        row.style.outline = '';
        
        // Vrati originalnu boju
        const originalIndex = parseInt(row.getAttribute('data-original-index'));
        const zalihe = JSON.parse(localStorage.getItem('zalihe') || '[]');
        const p = zalihe[originalIndex];
        if (p) {
            const isLow = (p.unit === 'g' && p.quantity <= 1000) || (p.unit === 'kg' && p.quantity <= 1) || ((p.unit === 'kom' || p.unit === 'pcs') && p.quantity <= 2);
            const isNew = newlyAddedIds.has(p.id);
            if (isLow) {
                row.style.background = '#f44336';
                row.style.color = 'white';
            } else if (isNew) {
                row.style.background = '#BBDEFB';
            }
        }
        
        // Traži poklapanje
        if (rowKey === query || rowKey.includes(query)) {
            matchCount++;
            if (!foundRow) foundRow = row;
        }
    });
    
    if (foundRow) {
        // Označi pronađeni red - ROYAL PLAVA pozadina sa ŽUTIM slovima
        foundRow.style.background = '#1a237e'; // Royal blue
        foundRow.style.color = '#FFD700';       // Gold/žuto
        foundRow.style.fontWeight = 'bold';
        foundRow.style.outline = '2px solid #FFD700';
        foundRow.style.outlineOffset = '-2px';
        
        // Skroluj do reda
        foundRow.scrollIntoView({ behavior: 'smooth', block: 'center' });
        
        // Označi checkbox u tom redu
        const checkbox = foundRow.querySelector('.row-checkbox');
        if (checkbox) {
            checkbox.checked = true;
        }
    } else {
        showModernAlert(t('nema_proizvoda'), `"${searchTerm}" - ${t('nema_proizvoda')}`, '🔍');
    }
}
function toggleAllCheckboxes() {
    const selectAll = document.getElementById('selectAll');
    const checkboxes = document.querySelectorAll('.row-checkbox');
    checkboxes.forEach(cb => cb.checked = selectAll.checked);
}

function obrisiZalihe() {
    const selected = document.querySelectorAll('.row-checkbox:checked');
    if (selected.length === 0) {
        showModernAlert(t('no_selection'), t('no_items_selected'), '⚠️');
        return;
    }
    
    // ❌ UKLONJEN confirm() - briše odmah bez pitanja
    const zalihe = JSON.parse(localStorage.getItem('zalihe') || '[]');
    const indices = Array.from(selected).map(cb => parseInt(cb.dataset.index));
    indices.sort((a, b) => b - a);
    indices.forEach(i => zalihe.splice(i, 1));
    localStorage.setItem('zalihe', JSON.stringify(zalihe));
    renderInventory();
}

function azurirajZalihe() {
    const selected = document.querySelectorAll('.row-checkbox:checked');
    if (selected.length === 0) {
        showModernAlert(t('no_selection'), t('no_items_selected'), '⚠️');
        return;
    }
    if (selected.length > 1) {
        showModernAlert(t('error'), 'Možete ažurirati samo jedan red odjednom!', '❌');
        return;
    }
    const index = parseInt(selected[0].dataset.index);
    const zalihe = JSON.parse(localStorage.getItem('zalihe') || '[]');
    renderUpdateEntry(zalihe[index], index);
}

function renderUpdateEntry(proizvod, index) {
    currentScreenState = 'dataEntry';
    const content = document.getElementById('mainContent');
    if (!content) return;
    const today = proizvod.entry_date || new Date().toISOString().split('T')[0];
    
    content.innerHTML = `
        <div class="title">✏️ Ažuriraj - ${proizvod.product_name}</div>
        <div class="row"><label>${t('naziv_proizvoda')}</label><input type="text" id="updateProductInput" value="${proizvod.product_name || ''}"></div>
        <div class="row"><label>${t('opis')}</label><input type="text" id="updateDescriptionInput" value="${proizvod.description || ''}"></div>
        <div class="row">
            <label>${t('komad')}</label>
            <div class="inline-group">
                <input type="text" id="updatePieceInput" value="${proizvod.piece || ''}">
                <label>${t('kolicina')}</label>
                <input type="number" id="updateQuantityInput" value="${proizvod.quantity || 1}" step="0.1">
                <label>${t('jedinica_mere')}</label>
                <select id="updateUnitSelect">
                    <option value="kg" ${proizvod.unit === 'kg' ? 'selected' : ''}>${t('kg')}</option>
                    <option value="g" ${proizvod.unit === 'g' ? 'selected' : ''}>${t('g')}</option>
                    <option value="kom" ${proizvod.unit === 'kom' ? 'selected' : ''}>${t('kom')}</option>
                    <option value="l" ${proizvod.unit === 'l' ? 'selected' : ''}>${t('l')}</option>
                    <option value="ml" ${proizvod.unit === 'ml' ? 'selected' : ''}>${t('ml')}</option>
                    <option value="pak" ${proizvod.unit === 'pak' ? 'selected' : ''}>${t('pak')}</option>
                    <option value="kutija" ${proizvod.unit === 'kutija' ? 'selected' : ''}>${t('kutija')}</option>
                </select>
            </div>
        </div>
        <div class="row">
            <label>${t('datum_unosa')}</label>
            <div class="inline-group">
                <input type="date" id="updateDateInput" value="${today}">
                <label>${t('rok_trajanja')}</label>
                <input type="number" id="updateShelfLifeInput" value="${proizvod.shelf_life_months || 12}">
                <span style="font-size:18px;">mes</span>
            </div>
        </div>
        <div class="row">
            <label>${t('automatski_rok')}</label>
            <div class="inline-group"><span id="updateExpiryDisplay">-</span></div>
        </div>
        <div class="row">
            <label>${t('mesto_skladistenja')}</label>
            <select id="updateStorageSelect">
                <option value="${t('zamrzivac_1')}" ${proizvod.storage_location === t('zamrzivac_1') ? 'selected' : ''}>❄️ ${t('zamrzivac_1')}</option>
                <option value="${t('zamrzivac_2')}" ${proizvod.storage_location === t('zamrzivac_2') ? 'selected' : ''}>❄️ ${t('zamrzivac_2')}</option>
                <option value="${t('zamrzivac_3')}" ${proizvod.storage_location === t('zamrzivac_3') ? 'selected' : ''}>❄️ ${t('zamrzivac_3')}</option>
                <option value="${t('frizider')}" ${proizvod.storage_location === t('frizider') ? 'selected' : ''}>🧊 ${t('frizider')}</option>
                <option value="${t('ostava')}" ${proizvod.storage_location === t('ostava') ? 'selected' : ''}>🏠 ${t('ostava')}</option>
                <option value="${t('Ostalo')}" ${proizvod.storage_location === t('Ostalo') ? 'selected' : ''}>📦 ${t('Ostalo')}</option>
            </select>
        </div>
        <div class="btn-group">
            <button class="btn-save" onclick="sacuvajAzuriranje(${index})">✅ Sačuvaj</button>
            <button class="btn-cancel" onclick="renderInventory()">✖ Odustani</button>
        </div>
    `;
    document.getElementById('updateDateInput')?.addEventListener('change', updateUpdateExpiryDate);
    document.getElementById('updateDateInput')?.addEventListener('input', updateUpdateExpiryDate);
    document.getElementById('updateShelfLifeInput')?.addEventListener('change', updateUpdateExpiryDate);
    document.getElementById('updateShelfLifeInput')?.addEventListener('input', updateUpdateExpiryDate);
    updateUpdateExpiryDate();
}

function updateUpdateExpiryDate() {
    const dateInput = document.getElementById('updateDateInput');
    const shelfLifeInput = document.getElementById('updateShelfLifeInput');
    const expiryDisplay = document.getElementById('updateExpiryDisplay');
    if (!dateInput || !shelfLifeInput || !expiryDisplay) return;
    const date = dateInput.value;
    const months = parseInt(shelfLifeInput.value) || 0;
    if (date && months > 0) {
        const expiry = new Date(date);
        expiry.setMonth(expiry.getMonth() + months);
        expiryDisplay.textContent = expiry.toLocaleDateString('sr-RS', { day: '2-digit', month: '2-digit', year: 'numeric' });
    } else {
        expiryDisplay.textContent = '-';
    }
}

function sacuvajAzuriranje(index) {
    const product = document.getElementById('updateProductInput')?.value.trim();
    const quantity = document.getElementById('updateQuantityInput')?.value.trim();
    
    if (!product) {
        showModernAlert(t('missing_info'), t('enter_product_name'), '📝');
        return;
    }
    if (!quantity || isNaN(parseFloat(quantity))) {
        showModernAlert(t('missing_info'), t('enter_quantity'), '📝');
        return;
    }
    
    const novaKolicina = parseFloat(quantity);
    let zalihe = JSON.parse(localStorage.getItem('zalihe') || '[]');
    let shopping = JSON.parse(localStorage.getItem('shoppingList') || '[]');
    
    // Ako je količina 0, prebaci u spisak potreba BEZ POPUP-a
    if (novaKolicina === 0) {
        const proizvod = zalihe[index];
        if (proizvod) {
            shopping.push({
                product_name: proizvod.product_name,
                description: proizvod.description || '',
                quantity: 0,
                unit: proizvod.unit || 'kom'
            });
            localStorage.setItem('shoppingList', JSON.stringify(shopping));
            zalihe.splice(index, 1);
            localStorage.setItem('zalihe', JSON.stringify(zalihe));
            // ❌ UKLONJEN POPUP
            renderInventory();
            return;
        }
    }
    
    // Ažuriraj BEZ POPUP-a
    zalihe[index] = {
        product_name: product,
        description: document.getElementById('updateDescriptionInput')?.value.trim() || '',
        piece: document.getElementById('updatePieceInput')?.value.trim() || '-',
        quantity: novaKolicina,
        unit: document.getElementById('updateUnitSelect')?.value || 'kg',
        entry_date: document.getElementById('updateDateInput')?.value || new Date().toISOString().split('T')[0],
        shelf_life_months: parseInt(document.getElementById('updateShelfLifeInput')?.value) || 12,
        storage_location: document.getElementById('updateStorageSelect')?.value || 'Ostalo'
    };
    
    localStorage.setItem('zalihe', JSON.stringify(zalihe));
    // ❌ UKLONJEN POPUP
    renderInventory();
}
 
function renderShoppingList() {
    currentScreenState = 'shopping';
    const content = document.getElementById('mainContent');
    if (!content) return;
    const shopping = JSON.parse(localStorage.getItem('shoppingList') || '[]');
    
    let html = `<div class="title">${t('spisak_potreba')}</div>`;
    html += `<div style="display:flex; gap:10px; margin-bottom:15px; flex-wrap:wrap;">`;
    html += `<button onclick="oznaciSveShopping()" style="background:#2196F3; color:white; border:none; padding:10px 20px; border-radius:8px; font-size:16px; cursor:pointer;">☑️ ${t('oznaci_sve')}</button>`;
    html += `<button onclick="kopirajShopping()" style="background:#4CAF50; color:white; border:none; padding:10px 20px; border-radius:8px; font-size:16px; cursor:pointer;">📋 ${t('kopiraj')}</button>`;
    html += `<button onclick="obrisiOznacenoShopping()" style="background:#f44336; color:white; border:none; padding:10px 20px; border-radius:8px; font-size:16px; cursor:pointer;">🗑️ ${t('obrisi_oznaceno')}</button>`;
    html += `<button onclick="renderCategories()" style="background:#666; color:white; border:none; padding:10px 20px; border-radius:8px; font-size:16px; cursor:pointer;">✖ ${t('odustani')}</button>`;
    html += `</div>`;
    
    html += `<div class="table-container" style="max-height:400px; overflow-y:auto;">`;
    html += `<div class="table-title">🛒 ${t('spisak_potreba')}</div>`;
    html += `<div id="shoppingTable">`;
    // UKLONJENA kolona Akcija - sada samo 3 kolone
    html += `<div class="table-row header-row" style="display:grid; grid-template-columns:40px 1.5fr 1.5fr; gap:2px; background:#f0f0f0; font-weight:bold; border-bottom:2px solid #ccc; padding:5px 0;">`;
    html += `<div class="cell" style="text-align:center;"><input type="checkbox" id="selectAllShopping" onchange="toggleAllShopping()"></div>`;
    html += `<div class="cell">${t('naziv_proizvoda')}</div>`;
    html += `<div class="cell">${t('opis')}</div>`;
    html += `</div>`;
    
    if (shopping.length === 0) {
        html += `<div class="table-row"><div class="cell" style="grid-column:span 3;padding:30px;color:#999;text-align:center;">${t('nema_proizvoda')}</div></div>`;
    } else {
        shopping.forEach((p, index) => {
            html += `<div class="table-row" style="display:grid; grid-template-columns:40px 1.5fr 1.5fr; gap:2px; border-bottom:1px solid #eee; padding:5px 0;">`;
            html += `<div class="cell" style="text-align:center;"><input type="checkbox" class="shopping-checkbox" data-index="${index}"></div>`;
            html += `<div class="cell">${p.product_name}</div>`;
            html += `<div class="cell">${p.description || ''}</div>`;
            html += `</div>`;
        });
    }
    html += `</div></div>`;
    content.innerHTML = html;
}


function oznaciSveShopping() {
    const checkboxes = document.querySelectorAll('.shopping-checkbox');
    const selectAll = document.getElementById('selectAllShopping');
    if (checkboxes.length === 0) return;
    const sviOznaceni = Array.from(checkboxes).every(cb => cb.checked);
    checkboxes.forEach(cb => cb.checked = !sviOznaceni);
    if (selectAll) selectAll.checked = !sviOznaceni;
}

function toggleAllShopping() {
    const selectAll = document.getElementById('selectAllShopping');
    const checkboxes = document.querySelectorAll('.shopping-checkbox');
    checkboxes.forEach(cb => cb.checked = selectAll.checked);
}

function kopirajShopping() {
    const shopping = JSON.parse(localStorage.getItem('shoppingList') || '[]');
    if (shopping.length === 0) {
        showModernAlert(t('list_empty'), t('no_items_selected'), '🛒');
        return;
    }
    let tekst = `${t('spisak_potreba')}\n${'='.repeat(30)}\n\n`;
    shopping.forEach((p, index) => {
        tekst += `${index + 1}. ${p.product_name}`;
        if (p.description) tekst += ` - ${p.description}`;
        tekst += `\n`;
    });
    if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(tekst).then(() => {
            showModernAlert(t('success'), t('copied'), '✅');
        }).catch(() => kopirajFallback(tekst));
    } else {
        kopirajFallback(tekst);
    }
}

function kopirajFallback(tekst) {
    const textarea = document.createElement('textarea');
    textarea.value = tekst;
    textarea.style.position = 'fixed';
    textarea.style.opacity = '0';
    document.body.appendChild(textarea);
    textarea.select();
    try { 
        document.execCommand('copy'); 
        showModernAlert(t('success'), t('copied'), '✅');
    } catch (err) { 
        showModernAlert(t('error'), t('copy_error'), '❌');
    }
    document.body.removeChild(textarea);
}

function obrisiOznacenoShopping() {
    const selected = document.querySelectorAll('.shopping-checkbox:checked');
    if (selected.length === 0) {
        showModernAlert(t('no_selection'), t('no_items_selected'), '⚠️');
        return;
    }
    // ❌ UKLONJEN confirm() - briše odmah
    let shopping = JSON.parse(localStorage.getItem('shoppingList') || '[]');
    const indices = Array.from(selected).map(cb => parseInt(cb.dataset.index));
    indices.sort((a, b) => b - a);
    indices.forEach(i => shopping.splice(i, 1));
    localStorage.setItem('shoppingList', JSON.stringify(shopping));
    renderShoppingList();
}

function obrisiSaSpiska(index) {
    // ❌ UKLONJEN confirm()
    let shopping = JSON.parse(localStorage.getItem('shoppingList') || '[]');
    shopping.splice(index, 1);
    localStorage.setItem('shoppingList', JSON.stringify(shopping));
    renderShoppingList();
    // ❌ UKLONJEN showModernAlert posle brisanja
}
// ===== GLAVNA FUNKCIJA ZA NAZAD / ODUSTANI =====
function handleBackAction() {
    console.log('⬅️ Trenutni ekran stanje:', currentScreenState);
    if (currentScreenState === 'dataEntry') {
        if (currentSubcategory) {
            renderProductParts(currentSubcategory);
        } else if (currentCategory) {
            renderSubcategories(currentCategory);
        } else {
            renderCategories();
        }
    } else if (currentScreenState === 'productParts') {
        if (currentCategory) {
            renderSubcategories(currentCategory);
        } else {
            renderCategories();
        }
    } else if (currentScreenState === 'subcategories') {
        renderCategories();
    } else if (currentScreenState === 'categories') {
        showScreen('languageScreen');
        renderLanguages();
    } else if (currentScreenState === 'inventory' || currentScreenState === 'shopping') {
        renderCategories();
    } else {
        showScreen('mainScreen');
        renderCategories();
    }
}

// ============================================
// GLOBALNA FUNKCIJA ZA LOGIN
// ============================================
function triggerLogin() {
    console.log("🔐 triggerLogin pozvan!");
    const phoneInput = document.getElementById('phoneInput');
    if (!phoneInput) {
        showModernAlert(t('error'), 'Phone input not found!', '❌');
        return;
    }
    const phone = phoneInput.value.trim();
    console.log("📱 Unet broj:", phone);
    if (phone.length >= 9) {
        console.log("✅ Login uspešan");
        showScreen('languageScreen');
        renderLanguages();
    } else {
        showModernAlert(t('invalid_input'), t('please_enter_phone'), '📱');
    }
}

// ===== GLAVNI DOGAĐAJI (Delegirani pristup) =====
document.addEventListener('DOMContentLoaded', function() {
    console.log('✅ DOM je spreman!');

    // Slušamo sve klikove na nivou celog dokumenta
    document.addEventListener('click', function(e) {
        // ===== LOGIN DUGME (ENTER) =====
        if (e.target && (e.target.id === 'loginBtn' || e.target.closest('#loginBtn'))) {
            e.preventDefault();
            console.log('🖱️ Klik na ENTER dugme');
            triggerLogin();
        }

        // ===== EXIT DUGMAD =====
        if (e.target && (e.target.id === 'exitLoginBtn' || e.target.closest('#exitLoginBtn') ||
                         e.target.id === 'exitLangBtn'  || e.target.closest('#exitLangBtn')  ||
                         e.target.id === 'exitMainBtn'  || e.target.closest('#exitMainBtn'))) {
            console.log('🚪 Exit dugme kliknuto putem delegiranja');
            exitApp();
        }

        // ===== BACK DUGME =====
        if (e.target && (e.target.id === 'backBtn' || e.target.closest('#backBtn'))) {
            handleBackAction();
        }

        // ===== INVENTORY DUGME =====
        if (e.target && (e.target.id === 'invBtn' || e.target.closest('#invBtn'))) {
            console.log('📦 Inventory klik');
            renderInventory();
        }

        // ===== SHOPPING DUGME =====
        if (e.target && (e.target.id === 'shopBtn' || e.target.closest('#shopBtn'))) {
            console.log('🛒 Shopping klik');
            renderShoppingList();
        }

        // ===== SUPPORT DUGMAD =====
        if (e.target && (e.target.id === 'supportBtn' || e.target.closest('#supportBtn'))) {
            openSupportDialog();
        }
        if (e.target && (e.target.id === 'closeSupportBtn' || e.target.closest('#closeSupportBtn') ||
                         e.target.id === 'closeSupportBtn2' || e.target.closest('#closeSupportBtn2'))) {
            closeSupportDialog();
        }
    });

    // ===== ENTER TASTER NA INPUT POLJU =====
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Enter') {
            const activeElement = document.activeElement;
            if (activeElement && activeElement.id === 'phoneInput') {
                e.preventDefault();
                console.log('⌨️ Enter taster pritisnut na phoneInput-u');
                triggerLogin();
            }
        }
        if (e.key === 'Escape') {
            closeSupportDialog();
            closeModernConfirm(); // DODATO - zatvara i Confirm na ESC
        }
    });

    // ===== MODERNI CONFIRM DUGMAD =====
    const yesBtn = document.getElementById('confirmYesBtn');
    const noBtn = document.getElementById('confirmNoBtn');
    
    if (yesBtn) {
        yesBtn.addEventListener('click', function() {
            if (confirmCallback && confirmCallback.onYes) {
                confirmCallback.onYes();
            }
            closeModernConfirm();
        });
        console.log('✅ Confirm Yes dugme povezano');
    }
    
    if (noBtn) {
        noBtn.addEventListener('click', function() {
            if (confirmCallback && confirmCallback.onNo) {
                confirmCallback.onNo();
            }
            closeModernConfirm();
        });
        console.log('✅ Confirm No dugme povezano');
    }

    console.log('✅ Svi događaji uspešno povezani preko delegiranja!');
});
