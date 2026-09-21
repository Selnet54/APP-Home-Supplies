// ============================================
// APP-HOME-SUPPLIES - script.js
// PRERAĐENA VERZIJA - usklađena sa index.html i productParts.js
// ============================================
console.log('✅ Script.js je učitan!');

// ===== Globalna stanja =====
let currentLanguage = localStorage.getItem('appLanguage') || null;
let currentCategory = '';
let currentItem = '';
let editingId = null; // id stavke koja se trenutno menja (null = nova stavka)
let screenStack = ['inventory']; // istorija ekrana unutar glavnog dela aplikacije

// ===== Podaci o jezicima (nazivi kategorija dolaze iz productParts.js) =====
const LANG_INFO = {
    sr: { flag: '🇷🇸', name: 'Srpski' },
    en: { flag: '🇬🇧', name: 'English' },
    de: { flag: '🇩🇪', name: 'Deutsch' },
    hu: { flag: '🇭🇺', name: 'Magyar' },
    uk: { flag: '🇺🇦', name: 'Українська' },
    ru: { flag: '🇷🇺', name: 'Русский' },
    zh: { flag: '🇨🇳', name: '中文' },
    es: { flag: '🇪🇸', name: 'Español' },
    pt: { flag: '🇵🇹', name: 'Português' },
    fr: { flag: '🇫🇷', name: 'Français' }
};
const CATEGORY_COLORS = ['#e3f2fd', '#f1f8e9', '#fff3e0', '#fce4ec', '#ede7f6', '#e0f7fa', '#fffde7', '#efebe9'];

// ===== Inicijalizacija aplikacije =====
document.addEventListener('DOMContentLoaded', () => {
    initApp();
    setupEventListeners();
});

function initApp() {
    renderLanguages();

    const savedLang = localStorage.getItem('appLanguage');
    const savedPhone = localStorage.getItem('userPhone');

    // Ako korisnik već ima sačuvan broj telefona i jezik, preskoči login i izbor jezika
    if (savedLang && savedPhone) {
        currentLanguage = savedLang;
        document.getElementById('loginScreen').style.display = 'none';
        document.getElementById('languageScreen').style.display = 'none';
        document.getElementById('mainScreen').style.display = 'flex';
        showInventory();
    }
}

// ===== LOGIN =====
function handleLogin() {
    const phoneInput = document.getElementById('phoneInput');
    const phone = phoneInput ? phoneInput.value.trim() : '';

    if (!phone) {
        showModernAlert('Upozorenje', 'Unesite broj telefona.', '⚠️');
        return;
    }

    localStorage.setItem('userPhone', phone);

    document.getElementById('loginScreen').style.display = 'none';
    document.getElementById('languageScreen').style.display = 'flex';
}

// ===== IZBOR JEZIKA =====
function renderLanguages() {
    const grid = document.getElementById('languageGrid');
    if (!grid) return;

    grid.innerHTML = '';
    Object.keys(LANG_INFO).forEach(code => {
        const info = LANG_INFO[code];
        const card = document.createElement('div');
        card.className = 'lang-btn-main';
        card.innerHTML = `
            <span style="font-size:44px;line-height:1;">${info.flag}</span>
            <span class="lang-name">${info.name}</span>
        `;
        card.onclick = () => selectLanguage(code);
        grid.appendChild(card);
    });
}

function selectLanguage(langCode) {
    if (!productParts[langCode]) return;

    currentLanguage = langCode;
    localStorage.setItem('appLanguage', langCode);

    document.getElementById('languageScreen').style.display = 'none';
    document.getElementById('mainScreen').style.display = 'flex';

    screenStack = ['inventory'];
    showInventory();
}

// ===== NAVIGACIJA NAZAD =====
function goBack() {
    if (screenStack.length <= 1) return; // već smo na početnom ekranu
    screenStack.pop();
    const prev = screenStack[screenStack.length - 1];
    renderScreen(prev);
}

function renderScreen(name) {
    switch (name) {
        case 'shopping': renderShoppingScreen(); break;
        case 'categories': renderCategoriesScreen(); break;
        case 'items': renderItemsScreen(); break;
        case 'dataEntry': renderDataEntryScreen(); break;
        default: renderInventoryScreen();
    }
}

// ===== GLAVNI EKRAN: ZALIHE (početni ekran) =====
function showInventory() {
    screenStack = ['inventory'];
    renderInventoryScreen();
}

function renderInventoryScreen() {
    const container = document.getElementById('mainContent');
    container.innerHTML = `
        <div class="title">📦 Vaše zalihe</div>
        <div style="text-align:center;margin-bottom:25px;">
            <button class="btn btn-green" id="addItemBtn" style="width:auto;padding:14px 40px;">➕ Dodaj stavku</button>
        </div>
        <div id="inventoryListContainer"></div>
    `;
    document.getElementById('addItemBtn').onclick = () => showCategories();
    renderInventoryList();
}

function renderInventoryList() {
    const container = document.getElementById('inventoryListContainer');
    if (!container) return;

    const zalihe = JSON.parse(localStorage.getItem('zalihe') || '[]');

    if (zalihe.length === 0) {
        container.innerHTML = `<p style="text-align:center;color:#888;font-size:20px;padding:30px;">Nema stavki na zalihama.</p>`;
        return;
    }

    let html = `
        <div class="table-container">
            <div class="table-row header-row">
                <div class="cell">Kategorija</div>
                <div class="cell">Stavka</div>
                <div class="cell">Količina</div>
                <div class="cell">Rok ističe</div>
                <div class="cell">Akcije</div>
            </div>
    `;

    zalihe.forEach(item => {
        let isLow = false;
        if ((item.unit === 'g' && item.quantity < 400) ||
            (item.unit === 'kg' && item.quantity < 0.4) ||
            (item.unit === 'kom' && item.quantity <= 2)) {
            isLow = true;
        }
        html += `
            <div class="table-row" style="${isLow ? 'background:#ffebee;' : ''}">
                <div class="cell">${item.category}</div>
                <div class="cell">${item.item}</div>
                <div class="cell">${item.quantity} ${item.unit}</div>
                <div class="cell">${item.expiryDate || '-'}</div>
                <div class="cell">
                    <button onclick="urediZalihe(${item.id})" style="border:none;background:none;font-size:20px;cursor:pointer;">✏️</button>
                    <button onclick="obrisiZalihe(${item.id})" style="border:none;background:none;font-size:20px;cursor:pointer;">🗑️</button>
                </div>
            </div>
        `;
    });

    html += `</div>`;
    container.innerHTML = html;
}

function obrisiZalihe(id) {
    showModernConfirm(
        'Brisanje',
        'Da li ste sigurni da želite da obrišete ovu stavku?',
        '🗑️',
        function onYes() {
            let zalihe = JSON.parse(localStorage.getItem('zalihe') || '[]');
            zalihe = zalihe.filter(item => item.id !== id);
            localStorage.setItem('zalihe', JSON.stringify(zalihe));
            renderInventoryList();
        }
    );
}

function urediZalihe(id) {
    const zalihe = JSON.parse(localStorage.getItem('zalihe') || '[]');
    const item = zalihe.find(z => z.id === id);
    if (!item) return;

    currentCategory = item.category;
    currentItem = item.item;
    editingId = id;

    screenStack.push('dataEntry');
    renderDataEntryScreen(item);
}

// ===== KATEGORIJE =====
function showCategories() {
    screenStack.push('categories');
    renderCategoriesScreen();
}

function renderCategoriesScreen() {
    const container = document.getElementById('mainContent');
    const data = productParts[currentLanguage] || {};
    const cats = Object.keys(data);

    let html = `<div class="title">Izaberite kategoriju</div><div class="categories-grid">`;
    cats.forEach((cat, i) => {
        const color = CATEGORY_COLORS[i % CATEGORY_COLORS.length];
        html += `<button class="category-btn" style="background:${color};" data-cat="${cat}">${cat}</button>`;
    });
    html += `</div>`;
    container.innerHTML = html;

    container.querySelectorAll('.category-btn').forEach(btn => {
        btn.onclick = () => selectCategory(btn.getAttribute('data-cat'));
    });
}

function selectCategory(catName) {
    currentCategory = catName;
    screenStack.push('items');
    renderItemsScreen();
}

// ===== STAVKE U OKVIRU KATEGORIJE =====
function renderItemsScreen() {
    const container = document.getElementById('mainContent');
    const items = (productParts[currentLanguage] && productParts[currentLanguage][currentCategory]) || [];

    let html = `<div class="title">${currentCategory}</div><div class="categories-grid">`;
    items.forEach(item => {
        html += `<button class="category-btn" style="background:#f5f5f5;" data-item="${item}">${item}</button>`;
    });
    html += `</div>`;
    container.innerHTML = html;

    container.querySelectorAll('.category-btn').forEach(btn => {
        btn.onclick = () => {
            currentItem = btn.getAttribute('data-item');
            editingId = null;
            screenStack.push('dataEntry');
            renderDataEntryScreen();
        };
    });
}

// ===== UNOS PODATAKA =====
function renderDataEntryScreen(existingItem) {
    const container = document.getElementById('mainContent');
    const today = new Date().toISOString().split('T')[0];

    const qty = existingItem ? existingItem.quantity : '';
    const unit = existingItem ? existingItem.unit : 'kom';
    const entryDate = existingItem ? existingItem.entryDate : today;
    const expiryMonths = existingItem ? existingItem.expiryMonths : 0;

    container.innerHTML = `
        <div class="title">${currentCategory} — ${currentItem}</div>

        <div class="row">
            <label>Količina:</label>
            <div class="inline-group">
                <input type="number" id="itemQuantity" min="0" step="0.1" value="${qty}" placeholder="npr. 1.5">
                <select id="itemUnit">
                    <option value="kom" ${unit === 'kom' ? 'selected' : ''}>kom</option>
                    <option value="g" ${unit === 'g' ? 'selected' : ''}>g</option>
                    <option value="kg" ${unit === 'kg' ? 'selected' : ''}>kg</option>
                    <option value="ml" ${unit === 'ml' ? 'selected' : ''}>ml</option>
                    <option value="l" ${unit === 'l' ? 'selected' : ''}>l</option>
                </select>
            </div>
        </div>

        <div class="row">
            <label>Datum unosa:</label>
            <input type="date" id="entryDate" value="${entryDate}">
        </div>

        <div class="row">
            <label>Rok trajanja (meseci):</label>
            <input type="number" id="expiryMonths" min="0" value="${expiryMonths}">
            <div id="expiryDisplay">-</div>
        </div>

        <div class="btn-group">
            <button class="btn-save" id="btnSaveData">💾 Sačuvaj</button>
            <button class="btn-cancel" id="btnCancelData">✖ Otkaži</button>
        </div>
    `;

    document.getElementById('entryDate').addEventListener('change', updateExpiryDate);
    document.getElementById('expiryMonths').addEventListener('input', updateExpiryDate);
    document.getElementById('btnSaveData').addEventListener('click', sacuvajZalihe);
    document.getElementById('btnCancelData').addEventListener('click', goBack);

    updateExpiryDate();
}

function updateExpiryDate() {
    const entryDateVal = document.getElementById('entryDate')?.value;
    const monthsVal = parseInt(document.getElementById('expiryMonths')?.value || '0', 10);
    const expiryDisplay = document.getElementById('expiryDisplay');

    if (!entryDateVal || isNaN(monthsVal) || !expiryDisplay) return;

    const d = new Date(entryDateVal);
    d.setMonth(d.getMonth() + monthsVal);

    expiryDisplay.textContent = d.toISOString().split('T')[0];
}

function sacuvajZalihe() {
    const quantity = document.getElementById('itemQuantity')?.value;
    const unit = document.getElementById('itemUnit')?.value;
    const entryDate = document.getElementById('entryDate')?.value;
    const expiryMonths = document.getElementById('expiryMonths')?.value;
    const expiryDate = document.getElementById('expiryDisplay')?.textContent;

    if (!quantity || quantity <= 0) {
        showModernAlert('Upozorenje', 'Unesite ispravnu količinu.', '⚠️');
        return;
    }

    let zalihe = JSON.parse(localStorage.getItem('zalihe') || '[]');

    if (editingId) {
        zalihe = zalihe.map(item => item.id === editingId ? {
            ...item,
            category: currentCategory,
            item: currentItem,
            quantity: parseFloat(quantity),
            unit, entryDate,
            expiryMonths: parseInt(expiryMonths, 10),
            expiryDate
        } : item);
    } else {
        zalihe.push({
            id: Date.now(),
            category: currentCategory,
            item: currentItem,
            quantity: parseFloat(quantity),
            unit, entryDate,
            expiryMonths: parseInt(expiryMonths, 10),
            expiryDate
        });
    }

    localStorage.setItem('zalihe', JSON.stringify(zalihe));
    editingId = null;

    showModernAlert('Uspešno', 'Stavka je sačuvana.', '✅');
    showInventory();
}

// ===== SPISAK ZA KUPOVINU =====
function showShoppingList() {
    screenStack = ['inventory', 'shopping'];
    renderShoppingScreen();
}

function renderShoppingScreen() {
    const container = document.getElementById('mainContent');
    container.innerHTML = `
        <div class="title">🛒 Spisak za kupovinu</div>

        <div class="row">
            <input type="text" id="shopName" placeholder="Naziv stavke" style="flex:2;">
            <input type="number" id="shopQty" placeholder="Kol." min="0" step="0.1" style="flex:1;">
            <select id="shopUnit" style="flex:1;">
                <option value="kom">kom</option>
                <option value="g">g</option>
                <option value="kg">kg</option>
                <option value="l">l</option>
            </select>
            <button class="btn btn-green" id="addShopBtn" style="width:auto;padding:16px 25px;">➕</button>
        </div>

        <button class="btn btn-orange" id="clearCheckedBtn" style="margin:15px 0;">🧹 Obriši označeno</button>

        <div id="shoppingListContainer"></div>
    `;

    document.getElementById('addShopBtn').onclick = dodajNaSpisak;
    document.getElementById('clearCheckedBtn').onclick = obrisiOznacenoShopping;

    renderShoppingList();
}

function dodajNaSpisak() {
    const name = document.getElementById('shopName')?.value.trim();
    const quantity = document.getElementById('shopQty')?.value;
    const unit = document.getElementById('shopUnit')?.value;

    if (!name) {
        showModernAlert('Upozorenje', 'Unesite naziv stavke.', '⚠️');
        return;
    }

    let list = JSON.parse(localStorage.getItem('shoppingList') || '[]');
    list.push({ name, quantity: quantity || '', unit, checked: false });
    localStorage.setItem('shoppingList', JSON.stringify(list));
    renderShoppingList();

    document.getElementById('shopName').value = '';
    document.getElementById('shopQty').value = '';
}

function renderShoppingList() {
    const container = document.getElementById('shoppingListContainer');
    if (!container) return;

    const shoppingList = JSON.parse(localStorage.getItem('shoppingList') || '[]');
    container.innerHTML = '';

    if (shoppingList.length === 0) {
        container.innerHTML = `<p style="text-align:center;color:#888;font-size:20px;padding:30px;">Spisak je prazan.</p>`;
        return;
    }

    shoppingList.forEach((item, index) => {
        const div = document.createElement('div');
        div.className = 'row';
        div.style.background = '#f5f5f5';
        div.style.borderRadius = '10px';
        div.style.padding = '12px 15px';
        div.innerHTML = `
            <input type="checkbox" id="shop_${index}" ${item.checked ? 'checked' : ''} style="width:auto;flex:none;transform:scale(1.4);">
            <label for="shop_${index}" style="flex:1;text-align:left;font-size:20px;text-decoration:${item.checked ? 'line-through' : 'none'};color:${item.checked ? '#999' : '#333'};">${item.name} ${item.quantity ? '- ' + item.quantity + ' ' + item.unit : ''}</label>
            <button data-idx="${index}" class="delShopBtn" style="border:none;background:none;font-size:20px;cursor:pointer;">❌</button>
        `;
        container.appendChild(div);
    });

    container.querySelectorAll('input[type="checkbox"]').forEach((cb, index) => {
        cb.onchange = () => toggleShoppingItem(index);
    });
    container.querySelectorAll('.delShopBtn').forEach(btn => {
        btn.onclick = () => obrisiSaSpiska(parseInt(btn.getAttribute('data-idx'), 10));
    });
}

function toggleShoppingItem(index) {
    let list = JSON.parse(localStorage.getItem('shoppingList') || '[]');
    if (list[index]) {
        list[index].checked = !list[index].checked;
        localStorage.setItem('shoppingList', JSON.stringify(list));
        renderShoppingList();
    }
}

function obrisiSaSpiska(index) {
    showModernConfirm(
        'Brisanje',
        'Da li želite da uklonite stavku sa spiska?',
        '❌',
        function onYes() {
            let list = JSON.parse(localStorage.getItem('shoppingList') || '[]');
            list.splice(index, 1);
            localStorage.setItem('shoppingList', JSON.stringify(list));
            renderShoppingList();
        }
    );
}

function obrisiOznacenoShopping() {
    showModernConfirm(
        'Čišćenje spiska',
        'Da li želite da obrišete sve označene stavke?',
        '🧹',
        function onYes() {
            let list = JSON.parse(localStorage.getItem('shoppingList') || '[]');
            list = list.filter(item => !item.checked);
            localStorage.setItem('shoppingList', JSON.stringify(list));
            renderShoppingList();
        }
    );
}

// ===== IZLAZ =====
function handleExit() {
    showModernConfirm(
        'Izlaz',
        'Da li želite da se izlogujete?',
        '🚪',
        function onYes() {
            localStorage.removeItem('userPhone');
            document.getElementById('mainScreen').style.display = 'none';
            document.getElementById('languageScreen').style.display = 'none';
            document.getElementById('loginScreen').style.display = 'flex';
        }
    );
}

// ===== Događaji / Event Listeners =====
function setupEventListeners() {
    // Login: klik na dugme ENTER
    const loginBtn = document.getElementById('loginBtn');
    if (loginBtn) loginBtn.addEventListener('click', handleLogin);

    // Login: submit forme (Enter u polju za broj telefona)
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', (event) => {
            event.preventDefault();
            handleLogin();
        });
    }

    const phoneInput = document.getElementById('phoneInput');
    if (phoneInput) {
        phoneInput.addEventListener('keydown', (event) => {
            if (event.key === 'Enter') {
                event.preventDefault();
                handleLogin();
            }
        });
    }

    // Support dijalog
    document.getElementById('supportBtn')?.addEventListener('click', () => {
        document.getElementById('supportDialog').classList.add('active');
    });
    document.getElementById('closeSupportBtn')?.addEventListener('click', () => {
        document.getElementById('supportDialog').classList.remove('active');
    });
    document.getElementById('closeSupportBtn2')?.addEventListener('click', () => {
        document.getElementById('supportDialog').classList.remove('active');
    });

    // Izlaz sa login ekrana
    document.getElementById('exitLoginBtn')?.addEventListener('click', () => {
        showModernConfirm('Izlaz', 'Da li želite da zatvorite aplikaciju?', '🚪', () => window.close());
    });

    // Izlaz sa ekrana za jezike
    document.getElementById('exitLangBtn')?.addEventListener('click', () => {
        document.getElementById('languageScreen').style.display = 'none';
        document.getElementById('loginScreen').style.display = 'flex';
    });

    // Glavni header
    document.getElementById('backBtn')?.addEventListener('click', goBack);
    document.getElementById('invBtn')?.addEventListener('click', showInventory);
    document.getElementById('shopBtn')?.addEventListener('click', showShoppingList);
    document.getElementById('exitMainBtn')?.addEventListener('click', handleExit);
}

// ===== Modern Modal Dialog Helpers =====
function showModernAlert(title, message, icon = 'ℹ️') {
    const alertModal = document.getElementById('modernAlert');
    if (!alertModal) {
        alert(message);
        return;
    }
    document.getElementById('alertIcon').textContent = icon;
    document.getElementById('alertTitle').textContent = title;
    document.getElementById('alertMessage').textContent = message;
    alertModal.style.display = 'flex';
}

function closeModernAlert() {
    const alertModal = document.getElementById('modernAlert');
    if (alertModal) alertModal.style.display = 'none';
}

function showModernConfirm(title, message, icon = '❓', onYesCallback) {
    const confirmModal = document.getElementById('modernConfirm');
    if (!confirmModal) {
        if (confirm(message)) onYesCallback();
        return;
    }
    document.getElementById('confirmIcon').textContent = icon;
    document.getElementById('confirmTitle').textContent = title;
    document.getElementById('confirmMessage').textContent = message;

    const btnYes = document.getElementById('confirmYesBtn');
    const btnNo = document.getElementById('confirmNoBtn');

    const closeConfirm = () => {
        confirmModal.style.display = 'none';
        document.removeEventListener('keydown', handleModalEnter);
    };

    btnYes.onclick = () => {
        closeConfirm();
        if (onYesCallback) onYesCallback();
    };
    btnNo.onclick = () => closeConfirm();

    const handleModalEnter = (e) => {
        if (e.key === 'Enter' && confirmModal.style.display !== 'none') {
            e.preventDefault();
            btnYes.click();
        }
    };
    document.addEventListener('keydown', handleModalEnter);

    confirmModal.style.display = 'flex';
    btnYes.focus();
}
