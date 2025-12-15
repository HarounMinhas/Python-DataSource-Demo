"""Database Data Source

Dit bestand implementeert toegang tot een SQLite database.

SQLite werd gekozen omdat:
- Het geen aparte server vereist (self-contained)
- Perfect voor demo en kleine applicaties
- Standaard beschikbaar in Python

Voor productie-omgevingen zou je PostgreSQL, MySQL of een andere
volwaardige database gebruiken, maar de principes blijven hetzelfde.
"""

import sqlite3
from typing import List
from models.product import Product
from .base_source import BaseDataSource


class DatabaseSource(BaseDataSource):
    """
    Implementatie voor SQLite database toegang.
    
    Deze klasse demonstreert:
    - Single Responsibility Principle: alleen database operaties
    - Open/Closed Principle: uitbreidbaar via overerving
    - Information Expert (GRASP): deze klasse kent de database structuur
    """
    
    def __init__(self, database_path: str):
        """
        Initialiseer de database connectie.
        
        Args:
            database_path (str): Pad naar het SQLite database bestand
        """
        self.database_path = database_path
        self.connection = None
        self._connect()
    
    def _connect(self):
        """
        Maak verbinding met de database.
        
        Private methode (conventie: _ prefix) voor interne operaties.
        Dit volgt het principe van Low Coupling (GRASP).
        """
        try:
            self.connection = sqlite3.connect(self.database_path)
            self.connection.row_factory = sqlite3.Row  # Voor dict-achtige toegang
        except sqlite3.Error as e:
            raise Exception(f"Database verbinding mislukt: {e}")
    
    def get_all_products(self) -> List[Product]:
        """
        Haal alle producten op uit de database.
        
        Returns:
            List[Product]: Lijst van Product objecten
        """
        if not self.connection:
            self._connect()
        
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT id, name, description, price, stock, image_path
            FROM products
            ORDER BY id
        """)
        
        products = []
        for row in cursor.fetchall():
            # Creator Pattern (GRASP): DatabaseSource creëert Product objecten
            product = Product(
                id=row['id'],
                name=row['name'],
                description=row['description'],
                price=row['price'],
                stock=row['stock'],
                image_path=row['image_path']
            )
            products.append(product)
        
        return products
    
    def close(self):
        """Sluit de database verbinding."""
        if self.connection:
            self.connection.close()
            self.connection = None
    
    def __enter__(self):
        """Context manager support (met 'with' statement)."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager cleanup."""
        self.close()
