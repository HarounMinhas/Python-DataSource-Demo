/**
 * Frontend JavaScript voor Python DataSource Demo
 * 
 * Dit bestand handelt de gebruikersinteractie af en communiceert
 * met de backend API.
 */

// Globale state
let currentSource = 'database';

// DOM elementen
const btnDatabase = document.getElementById('btn-database');
const btnCSV = document.getElementById('btn-csv');
const btnLoad = document.getElementById('btn-load');
const infoMessage = document.getElementById('info-message');
const productsContainer = document.getElementById('products-container');

/**
 * Initialisatie bij laden van de pagina
 */
document.addEventListener('DOMContentLoaded', function() {
    // Event listeners voor databron selectie
    btnDatabase.addEventListener('click', () => selectSource('database'));
    btnCSV.addEventListener('click', () => selectSource('csv'));
    
    // Event listener voor laad knop
    btnLoad.addEventListener('click', loadProducts);
});

/**
 * Selecteer databron en update UI
 */
function selectSource(source) {
    currentSource = source;
    
    // Update button states
    btnDatabase.classList.toggle('active', source === 'database');
    btnCSV.classList.toggle('active', source === 'csv');
    
    // Update info message
    const sourceName = source === 'database' ? 'Database (SQLite)' : 'CSV Bestand';
    showInfo(`Databron geselecteerd: ${sourceName}`, 'info');
}

/**
 * Laad producten van de geselecteerde databron
 */
async function loadProducts() {
    try {
        // Toon loading state
        showInfo('Producten laden...', 'info');
        productsContainer.innerHTML = '<div class="loading">Laden...</div>';
        
        // API request
        const response = await fetch(`/api/products?source=${currentSource}`);
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Er is een fout opgetreden');
        }
        
        // Toon success message
        const sourceName = data.source === 'database' ? 'Database' : 'CSV';
        showInfo(
            `${data.products.length} producten geladen uit ${sourceName}`,
            'success'
        );
        
        // Render producten
        renderProducts(data.products);
        
    } catch (error) {
        console.error('Error loading products:', error);
        showInfo(`Fout bij laden: ${error.message}`, 'error');
        productsContainer.innerHTML = '<div class="empty-state">Geen producten geladen</div>';
    }
}

/**
 * Render producten in de grid
 */
function renderProducts(products) {
    if (products.length === 0) {
        productsContainer.innerHTML = '<div class="empty-state">Geen producten gevonden</div>';
        return;
    }
    
    productsContainer.innerHTML = products.map(product => `
        <div class="product-card">
            <div class="product-id">ID: ${product.id}</div>
            <img 
                src="/static/images/${product.image}" 
                alt="${product.name}"
                class="product-image"
                onerror="this.src='/static/images/placeholder.png'"
            >
            <h3 class="product-name">${escapeHtml(product.name)}</h3>
            <p class="product-description">${escapeHtml(product.description)}</p>
            <div class="product-details">
                <span class="product-price">&euro;${product.price.toFixed(2)}</span>
                <span class="product-stock ${product.stock < 10 ? 'low' : ''}">
                    Voorraad: ${product.stock}
                </span>
            </div>
        </div>
    `).join('');
}

/**
 * Toon info bericht
 */
function showInfo(message, type = 'info') {
    infoMessage.textContent = message;
    infoMessage.className = `info-box ${type}`;
}

/**
 * Escape HTML om XSS te voorkomen
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
