"""Database Initialisatie Script

Dit script creëert de SQLite database en vult deze met sample data.
Voer dit script één keer uit na het klonen van de repository.

Usage:
    python init_database.py
"""

import sqlite3
import os
import sys
from typing import List, Tuple

DATABASE_PATH: str = 'data/products.db'

# Sample product data
# Format: (id, name, description, price, stock, image_path)
SAMPLE_PRODUCTS: List[Tuple[int, str, str, float, int, str]] = [
    (
        1,
        'Laptop Dell XPS 13',
        'Krachtige ultrabook met 13 inch scherm, Intel i7 processor en 16GB RAM',
        1299.99,
        15,
        'laptop.png'
    ),
    (
        2,
        'Draadloze Muis Logitech MX Master 3',
        'Ergonomische draadloze muis met precisie tracking en oplaadbare batterij',
        99.99,
        42,
        'mouse.png'
    ),
    (
        3,
        'Mechanisch Toetsenbord Keychron K2',
        'Compact 75% mechanisch toetsenbord met RGB verlichting en hot-swappable switches',
        89.99,
        28,
        'keyboard.png'
    ),
    (
        4,
        'Monitor LG UltraWide 34 inch',
        'Ultrawide QHD monitor (3440x1440) met IPS panel en 75Hz refresh rate',
        449.99,
        8,
        'monitor.png'
    ),
    (
        5,
        'USB-C Hub Anker 7-in-1',
        '7-poorts USB-C hub met HDMI, USB 3.0, SD kaartlezer en 100W Power Delivery',
        54.99,
        67,
        'usb-hub.png'
    ),
]


def create_database() -> None:
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
    try:
        # Zorg dat de data directory bestaat
        os.makedirs('data', exist_ok=True)
        
        # Verwijder oude database als deze bestaat
        if os.path.exists(DATABASE_PATH):
            print(f"Verwijder bestaande database: {DATABASE_PATH}")
            os.remove(DATABASE_PATH)
        
        # Maak verbinding en creëert database
        print(f"Creëren van nieuwe database: {DATABASE_PATH}")
        connection = sqlite3.connect(DATABASE_PATH)
        cursor = connection.cursor()
        
        # Creëert products tabel
        cursor.execute('''
            CREATE TABLE products (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT,
                price REAL NOT NULL CHECK(price >= 0),
                stock INTEGER NOT NULL CHECK(stock >= 0),
                image_path TEXT
            )
        ''')
        print("Products tabel aangemaakt")
        
        # Voeg sample data toe
        cursor.executemany('''
            INSERT INTO products (id, name, description, price, stock, image_path)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', SAMPLE_PRODUCTS)
        print(f"{len(SAMPLE_PRODUCTS)} producten toegevoegd")
        
        # Commit en sluit
        connection.commit()
        connection.close()
        
        print(f"\nDatabase succesvol aangemaakt: {DATABASE_PATH}")
        print(f"Totaal aantal producten: {len(SAMPLE_PRODUCTS)}")
    
    except sqlite3.Error as e:
        print(f"FOUT bij database operatie: {str(e)}", file=sys.stderr)
        sys.exit(1)
    
    except Exception as e:
        print(f"Onverwachte fout: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    print("=" * 50)
    print("Database Initialisatie")
    print("=" * 50)
    
    create_database()
    
    print("\n" + "=" * 50)
    print("Voltooid!")
    print("=" * 50)
    print("\nJe kunt nu de applicatie starten met:")
    print("  python app.py")
    print()
