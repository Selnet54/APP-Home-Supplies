const languages = [
    { code: 'sr', name: 'Srpski', flag: 'icons/rs.png' },
    { code: 'en', name: 'English', flag: 'icons/en.png' }
];

const translations = {
    sr: { glavne_kategorije: 'Glavne Kategorije', unesi: 'Sačuvaj', nazad: 'Nazad' },
    en: { glavne_kategorije: 'Main Categories', unesi: 'Save', nazad: 'Back' }
};

const categories = { sr: ['Hrana', 'Piće', 'Hemija'], en: ['Food', 'Drinks', 'Chemicals'] };
const subcategories = { sr: { 'Hrana': ['Mlečno', 'Meso', 'Voće'] }, en: { 'Food': ['Dairy', 'Meat', 'Fruits'] } };
const productParts = { sr: { 'Mlečno': ['Mleko', 'Jogurt', 'Sir'] }, en: { 'Dairy': ['Milk', 'Yogurt', 'Cheese'] } };

let currentLang = 'sr';

function showScreen(screenId) {
    document.querySelectorAll('.screen').forEach(s => s.style.display = 'none');
    document.getElementById(screenId).style.display = 'flex';
}

function renderCategories() {
    const content = document.getElementById('mainContent');
    content.innerHTML = `<div class="title">${translations[currentLang].glavne_kategorije}</div><div class="categories-grid" id="catGrid"></div>`;
    const grid = document.getElementById('catGrid');
    
    categories[currentLang].forEach(cat => {
        const btn = document.createElement('button');
        btn.className = 'category-btn';
        btn.textContent = cat;
        btn.onclick = () => {
            if (subcategories[currentLang] && subcategories[currentLang][cat]) {
                renderSubcategories(cat);
            } else {
                renderDataEntry(cat);
            }
        };
        grid.appendChild(btn);
    });
}

function renderSubcategories(cat) {
    const content = document.getElementById('mainContent');
    content.innerHTML = `<div class="title">${cat}</div><div class="categories-grid" id="subGrid"></div>`;
    const grid = document.getElementById('subGrid');
    
    subcategories[currentLang][cat].forEach(sub => {
        const btn = document.createElement('button');
        btn.className = 'category-btn';
        btn.textContent = sub;
        btn.onclick = () => {
            if (productParts[currentLang] && productParts[currentLang][sub]) {
                renderProductParts(sub);
            } else {
                renderDataEntry(sub);
            }
        };
        grid.appendChild(btn);
    });
}

function renderProductParts(sub) {
    const content = document.getElementById('mainContent');
    content.innerHTML = `<div class="title">${sub}</div><div class="categories-grid" id="partGrid"></div>`;
    const grid = document.getElementById('partGrid');
    
    productParts[currentLang][sub].forEach(part => {
        const btn = document.createElement('button');
        btn.className = 'category-btn';
        btn.textContent = part;
        btn.onclick = () => renderDataEntry(part);
        grid.appendChild(btn);
    });
}

function renderDataEntry(name) {
    const content = document.getElementById('mainContent');
    content.innerHTML = `
        <div class="title">Unos: ${name}</div>
        <input type="text" id="prodName" value="${name}">
        <button class="btn-save" onclick="alert('Sačuvano!')">${translations[currentLang].unesi}</button>
        <button class="btn-cancel" onclick="renderCategories()">${translations[currentLang].nazad}</button>
    `;
}

document.addEventListener('DOMContentLoaded', () => {
    // Ovde dodaj inicijalizaciju tvojih dugmadi (login, itd.)
});
