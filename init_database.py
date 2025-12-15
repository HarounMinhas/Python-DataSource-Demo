"""Database Initialisatie Script

Dit script creëert de SQLite database en vult deze met sample data.
Voer dit script één keer uit na het klonen van de repository.

Usage:
    python init_database.py
"""

import sqlite3
import os

DATABASE_PATH = 'data/products.db'

# Sample product data
SAMPLE_PRODUCTS = [
    (1, 'Laptop Dell XPS 13', 'Krachtige ultrabook met 13 inch scherm, Intel i7 processor en 16GB RAM', 1299.99, 15, 'laptop.png'),
    (2, 'Draadloze Muis Logitech MX Master 3', 'Ergonomische draadloze muis met precisie tracking en oplaadbare batterij', 99.99, 42, 'mouse.png'),
    (3, 'Mechanisch Toetsenbord Keychron K2', 'Compact 75% mechanisch toetsenbord met RGB verlichting en hot-swappable switches', 89.99, 28, 'keyboard.png'),
    (4, 'Monitor LG UltraWide 34"', 'Ultrawide QHD monitor (3440x1440) met IPS panel en 75Hz refresh rate', 449.99, 8, 'monitor.png'),
    (5, 'USB-C Hub Anker 7-in-1', '7-poorts USB-C hub met HDMI, USB 3.0, SD kaartlezer en 100W Power Delivery', 54.99, 67, 'usb-hub.png'),
]


def create_database():
    """
    Creëert de database en de products tabel.
    
    De tabel structuur:
    - id: Primary key
    - name: Product naam (TEXT, NOT NULL)
    - description: Product beschrijving (TEXT)
    - price: Prijs in euro (REAL, NOT NULL)
    - stock: Voorraad aantal (INTEGER, NOT NULL)
    - image_path: Pad naar afbeelding (TEXT)
    """
    # Zorg dat de data directory bestaat
    os.makedirs('data', exist_ok=True)
    
    # Verwijder oude database als deze bestaat
    if os.path.exists(DATABASE_PATH):
        os.remove(DATABASE_PATH)
    
    # Maak verbinding en creëert database
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()
    
    # Creëert products tabel
    cursor.execute('''
        CREATE TABLE products (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT,
            price REAL NOT NULL,
            stock INTEGER NOT NULL,
            image_path TEXT
        )
    ''')
    
    # Voeg sample data toe
    cursor.executemany('''
        INSERT INTO products (id, name, description, price, stock, image_path)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', SAMPLE_PRODUCTS)
    
    # Commit en sluit
    connection.commit()
    connection.close()
    
    print(f"Database aangemaakt: {DATABASE_PATH}")
    print(f"{len(SAMPLE_PRODUCTS)} producten toegevoegd aan de database.")


if __name__ == '__main__':
    create_database()
    print("\nDatabase initialisatie voltooid!")
    print("Je kunt nu de applicatie starten met: python app.py")
