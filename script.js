// ============================================
// APP-HOME-SUPPLIES - script.js
// OČIŠĆENA VERZIJA - 
// ============================================
console.log('✅ Script.js je učitan!');

// Globalna stanja
let currentLanguage = localStorage.getItem('appLanguage') || 'sr_lat';
let currentCategory = '';
let currentSubcategory = '';
let currentPart = '';
let currentScreenState = 'languages'; // Pristutna stanja: 'languages', 'categories', 'subcategories', 'productParts', 'dataEntry'

// Pomocna funkcija za prevode
function t(key) {
    if (typeof translations !== 'undefined' && translations[currentLanguage] && translations[currentLanguage][key]) {
        return translations[currentLanguage][key];
    }
    return key;
}

// Inicijalizacija aplikacije
document.addEventListener('DOMContentLoaded', () => {
    initApp();
    setupEventListeners();
});

function initApp() {
    renderLanguages();
    updateUIStaticTexts();
    
    // Ako već postoji zapamćen jezik, automatski učitaj kategorije
    const savedLang = localStorage.getItem('appLanguage');
    if (savedLang) {
        selectLanguage(savedLang, false);
    }
}

function updateUIStaticTexts() {
    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        el.textContent = t(key);
    });
}

// OVDJE DODAJETE LOGIKU ZA ENTER:
// Stvarna login funkcija - proverava broj telefona i prelazi na ekran za izbor jezika
function handleLogin() {
    const phoneInput = document.getElementById('phoneInput');
    const phone = phoneInput ? phoneInput.value.trim() : '';

    if (!phone) {
        showModernAlert(t('warning') || 'Upozorenje', t('enter_phone_number') || 'Unesite broj telefona.', '⚠️');
        return;
    }

    localStorage.setItem('userPhone', phone);

    document.getElementById('loginScreen').style.display = 'none';
    document.getElementById('languageScreen').style.display = 'flex';
}

// Generisanje jezika
function renderLanguages() {
    const grid = document.getElementById('languageGrid');
    if (!grid || typeof languages === 'undefined') return;
    
    grid.innerHTML = '';
    languages.forEach(lang => {
        const card = document.createElement('div');
        card.className = `language-card ${lang.id === currentLanguage ? 'active' : ''}`;
        card.onclick = () => selectLanguage(lang.id);
        card.innerHTML = `
            <span class="flag-icon">${lang.flag}</span>
            <span class="lang-name">${lang.name}</span>
        `;
        grid.appendChild(card);
    });
}

function selectLanguage(langId, switchScreen = true) {
    currentLanguage = langId;
    localStorage.setItem('appLanguage', langId);
    
    renderLanguages();
    updateUIStaticTexts();
    
    if (switchScreen) {
        showCategories();
    }
}

// Prikaz Kategorija
function showCategories() {
    currentScreenState = 'categories';
    hideAllScreens();
    
    const screen = document.getElementById('categoriesScreen');
    const container = document.getElementById('categoriesList');
    if (!screen || !container || typeof categories === 'undefined') return;
    
    container.innerHTML = '';
    categories.forEach(cat => {
        const btn = document.createElement('button');
        btn.className = 'category-btn';
        btn.innerHTML = `<span class="icon">${cat.icon}</span> <span>${t(cat.key)}</span>`;
        btn.onclick = () => selectCategory(cat.key);
        container.appendChild(btn);
    });
    
    screen.classList.remove('hidden');
}

function selectCategory(catKey) {
    currentCategory = catKey;
    showSubcategories(catKey);
}

// Prikaz Podkategorija
function showSubcategories(catKey) {
    currentScreenState = 'subcategories';
    hideAllScreens();
    
    const screen = document.getElementById('subcategoriesScreen');
    const container = document.getElementById('subcategoriesList');
    if (!screen || !container || typeof subcategories === 'undefined') return;
    
    const list = subcategories[catKey] || [];
    container.innerHTML = '';
    
    list.forEach(sub => {
        const btn = document.createElement('button');
        btn.className = 'subcategory-btn';
        btn.innerHTML = `<span class="icon">${sub.icon}</span> <span>${t(sub.key)}</span>`;
        btn.onclick = () => selectSubcategory(sub.key);
        container.appendChild(btn);
    });
    
    screen.classList.remove('hidden');
}

function selectSubcategory(subKey) {
    currentSubcategory = subKey;
    showProductParts(subKey);
}

// Prikaz Delova Proizvoda
function showProductParts(subKey) {
    currentScreenState = 'productParts';
    hideAllScreens();
    
    const screen = document.getElementById('productPartsScreen');
    const container = document.getElementById('productPartsList');
    if (!screen || !container || typeof productParts === 'undefined') return;
    
    const parts = productParts[subKey] || [];
    container.innerHTML = '';
    
    parts.forEach(part => {
        const btn = document.createElement('button');
        btn.className = 'product-part-btn';
        btn.innerHTML = `<span class="icon">${part.icon}</span> <span>${t(part.key)}</span>`;
        btn.onclick = () => selectProductPart(part.key);
        container.appendChild(btn);
    });
    
    screen.classList.remove('hidden');
}

function selectProductPart(partKey) {
    currentPart = partKey;
    showDataEntryScreen();
}

// Unos podataka
function showDataEntryScreen() {
    currentScreenState = 'dataEntry';
    hideAllScreens();
    
    const screen = document.getElementById('dataEntryScreen');
    if (!screen) return;
    
    // Postavljanje podrazumevanog datuma na današnji
    const today = new Date().toISOString().split('T')[0];
    const dateInput = document.getElementById('entryDate');
    if (dateInput) dateInput.value = today;
    
    updateExpiryDate();
    screen.classList.remove('hidden');
}

// Automatsko izračunavanje roka trajanja
function updateExpiryDate() {
    const entryDateVal = document.getElementById('entryDate')?.value;
    const monthsVal = parseInt(document.getElementById('expiryMonths')?.value || '0', 10);
    const expiryDisplay = document.getElementById('calculatedExpiry');
    
    if (!entryDateVal || isNaN(monthsVal) || !expiryDisplay) return;
    
    const d = new Date(entryDateVal);
    d.setMonth(d.getMonth() + monthsVal);
    
    const formattedDate = d.toISOString().split('T')[0];
    expiryDisplay.textContent = formattedDate;
}

// Skladištenje i Upravljanje Zalihama
function sacuvajZalihe() {
    const quantity = document.getElementById('itemQuantity')?.value;
    const unit = document.getElementById('itemUnit')?.value;
    const entryDate = document.getElementById('entryDate')?.value;
    const expiryMonths = document.getElementById('expiryMonths')?.value;
    const calculatedExpiry = document.getElementById('calculatedExpiry')?.textContent;
    
    if (!quantity || quantity <= 0) {
        showModernAlert(t('warning'), t('enter_valid_quantity'), '⚠️');
        return;
    }
    
    const newItem = {
        id: Date.now(),
        category: currentCategory,
        subcategory: currentSubcategory,
        part: currentPart,
        quantity: parseFloat(quantity),
        unit: unit,
        entryDate: entryDate,
        expiryMonths: parseInt(expiryMonths, 10),
        expiryDate: calculatedExpiry
    };
    
    let zalihe = JSON.parse(localStorage.getItem('zalihe') || '[]');
    zalihe.push(newItem);
    localStorage.setItem('zalihe', JSON.stringify(zalihe));
    
    showModernAlert(t('success'), t('item_saved_success'), '✅');
    showCategories();
}

// Prikaz Liste Zaliha
function renderInventory() {
    const container = document.getElementById('inventoryListContainer');
    if (!container) return;
    
    const zalihe = JSON.parse(localStorage.getItem('zalihe') || '[]');
    container.innerHTML = '';
    
    if (zalihe.length === 0) {
        container.innerHTML = `<p class="empty-msg">${t('no_items_in_stock') || 'Nema stavki na zalihama.'}</p>`;
        return;
    }
    
    zalihe.forEach(item => {
        const card = document.createElement('div');
        
        let isLow = false;
        if ((item.unit === 'g' && item.quantity < 400) || 
            (item.unit === 'kg' && item.quantity < 0.4) || 
            (item.unit === 'kom' && item.quantity <= 2)) {
            isLow = true;
        }
        
        card.className = `inventory-card ${isLow ? 'low-stock' : ''}`;
        card.innerHTML = `
            <div class="inv-info">
                <strong>${t(item.part) || item.part}</strong>
                <span>${item.quantity} ${item.unit}</span>
                <small>${t('expires') || 'Ističe'}: ${item.expiryDate}</small>
            </div>
            <div class="inv-actions">
                <button onclick="urediZalihe(${item.id})">✏️</button>
                <button onclick="obrisiZalihe(${item.id})">🗑️</button>
            </div>
        `;
        container.appendChild(card);
    });
}
function obrisiZalihe(id) {
    showModernConfirm(
        t('delete_confirm_title') || 'Brisanje',
        t('delete_confirm_msg') || 'Da li ste sigurni da želite da obrišete ovu stavku?',
        '🗑️',
        function onYes() {
            let zalihe = JSON.parse(localStorage.getItem('zalihe') || '[]');
            zalihe = zalihe.filter(item => item.id !== id);
            localStorage.setItem('zalihe', JSON.stringify(zalihe));
            renderInventory();
        }
    );
}

// Spisak Za Kupovinu (Shopping List)
function renderShoppingList() {
    const container = document.getElementById('shoppingListContainer');
    if (!container) return;
    
    const shoppingList = JSON.parse(localStorage.getItem('shoppingList') || '[]');
    container.innerHTML = '';
    
    if (shoppingList.length === 0) {
        container.innerHTML = `<p class="empty-msg">${t('shopping_list_empty')}</p>`;
        return;
    }
    
    shoppingList.forEach((item, index) => {
        const div = document.createElement('div');
        div.className = 'shopping-item';
        div.innerHTML = `
            <input type="checkbox" id="shop_${index}" ${item.checked ? 'checked' : ''} onchange="toggleShoppingItem(${index})">
            <label for="shop_${index}">${t(item.name) || item.name} - ${item.quantity} ${item.unit}</label>
            <button onclick="obrisiSaSpiska(${index})">❌</button>
        `;
        container.appendChild(div);
    });
}

function toggleShoppingItem(index) {
    let list = JSON.parse(localStorage.getItem('shoppingList') || '[]');
    if (list[index]) {
        list[index].checked = !list[index].checked;
        localStorage.setItem('shoppingList', JSON.stringify(list));
    }
}

function obrisiSaSpiska(index) {
    showModernConfirm(
        t('delete_confirm_title') || 'Brisanje',
        t('delete_confirm_msg') || 'Da li želite da uklonite stavku sa spiska?',
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
        t('delete_confirm_title') || 'Čišćenje spiska',
        t('delete_selected_msg') || 'Da li želite da obrišete sve označene stavke?',
        '🧹',
        function onYes() {
            let list = JSON.parse(localStorage.getItem('shoppingList') || '[]');
            list = list.filter(item => !item.checked);
            localStorage.setItem('shoppingList', JSON.stringify(list));
            renderShoppingList();
        }
    );
}

// Navigacija Unazad (Back Action)
function handleBackAction() {
    switch (currentScreenState) {
        case 'dataEntry':
            showProductParts(currentSubcategory);
            break;
        case 'productParts':
            showSubcategories(currentCategory);
            break;
        case 'subcategories':
            showCategories();
            break;
        case 'categories':
            hideAllScreens();
            document.getElementById('languagesScreen')?.classList.remove('hidden');
            currentScreenState = 'languages';
            break;
        default:
            break;
    }
}

// Pomoćna funkcija za sakrivanje svih ekrana
function hideAllScreens() {
    const screens = document.querySelectorAll('.screen-container');
    screens.forEach(s => s.classList.add('hidden'));
}

// Događaji / Event Listeners
function setupEventListeners() {
    // Login: klik na dugme ENTER
    const loginBtn = document.getElementById('loginBtn');
    if (loginBtn) {
        loginBtn.addEventListener('click', handleLogin);
    }

    // Login: taster Enter na formi (sprečava reload i zove istu login funkciju)
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', (event) => {
            event.preventDefault();
            handleLogin();
        });
    }

    // Login: taster Enter direktno u polju za broj telefona (dodatna sigurnost)
    const phoneInput = document.getElementById('phoneInput');
    if (phoneInput) {
        phoneInput.addEventListener('keydown', (event) => {
            if (event.key === 'Enter') {
                event.preventDefault();
                handleLogin();
            }
        });
    }

    document.getElementById('btnBack')?.addEventListener('click', handleBackAction);
    document.getElementById('entryDate')?.addEventListener('change', updateExpiryDate);
    document.getElementById('expiryMonths')?.addEventListener('input', updateExpiryDate);
    document.getElementById('btnSaveData')?.addEventListener('click', sacuvajZalihe);
}

// Modern Modal Dialog Helpers
function showModernAlert(title, message, icon = 'ℹ️') {
    const alertModal = document.getElementById('customAlertModal');
    if (!alertModal) {
        alert(message);
        return;
    }
    document.getElementById('alertIcon').textContent = icon;
    document.getElementById('alertTitle').textContent = title;
    document.getElementById('alertMessage').textContent = message;
    alertModal.classList.remove('hidden');
}

function showModernConfirm(title, message, icon = '❓', onYesCallback) {
    const confirmModal = document.getElementById('customConfirmModal');
    if (!confirmModal) {
        if (confirm(message)) onYesCallback();
        return;
    }
    document.getElementById('confirmIcon').textContent = icon;
    document.getElementById('confirmTitle').textContent = title;
    document.getElementById('confirmMessage').textContent = message;
    
    const btnYes = document.getElementById('confirmBtnYes');
    const btnNo = document.getElementById('confirmBtnNo');
    
    const closeConfirm = () => {
        confirmModal.classList.add('hidden');
        document.removeEventListener('keydown', handleModalEnter); // Uklanja slušalac nakon zatvaranja
    };
    
    btnYes.onclick = () => {
        closeConfirm();
        if (onYesCallback) onYesCallback();
    };
    btnNo.onclick = () => closeConfirm();
    
    // Omogućava pritisak na Enter za potvrdu modala (čak i ako fokus nije na inputu)
    const handleModalEnter = (e) => {
        if (e.key === 'Enter' && !confirmModal.classList.contains('hidden')) {
            e.preventDefault();
            btnYes.click();
        }
    };
    document.addEventListener('keydown', handleModalEnter);

    confirmModal.classList.remove('hidden');
    btnYes.focus(); // Stavlja fokus na "DA" dugme
}

// Omogućava rad tipke Enter za login i sve ostale unose
document.addEventListener('keydown', function(event) {
    if (event.key === 'Enter') {
        const aktivniElement = document.activeElement;
        
        // Provjera da li je fokus na bilo kom unosu (input ili select)
        if (aktivniElement && (aktivniElement.tagName === 'INPUT' || aktivniElement.tagName === 'SELECT')) {
            
            // Provjera za custom confirm modal
            const confirmModal = document.getElementById('customConfirmModal');
            if (confirmModal && !confirmModal.classList.contains('hidden')) {
                return;
            }

            event.preventDefault(); // Sprečava osvežavanje stranice

            // 1. Potraga za dugmetom unutar iste forme ili bloka
            const roditelj = aktivniElement.closest('form, .login-card, .login-container, .modal, div');
            
            let potvrdnoDugme = null;
            if (roditelj) {
                potvrdnoDugme = roditelj.querySelector('button[type="submit"], #btnLogin, .btn-login, #loginBtn, .btn-primary, .btn-save');
            }

            // 2. Ako nije nađeno u roditelju, traži globalno login dugme na stranici
            if (!potvrdnoDugme) {
                potvrdnoDugme = document.getElementById('btnLogin') || 
                                document.getElementById('loginBtn') || 
                                document.querySelector('.btn-login') || 
                                document.querySelector('button[type="submit"]');
            }

            // Ako je dugme pronađeno i vidljivo je na ekranu — klikni ga
            if (potvrdnoDugme && potvrdnoDugme.offsetParent !== null) {
                potvrdnoDugme.click();
            }
        }
    }
});
