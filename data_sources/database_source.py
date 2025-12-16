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
import os
from typing import List, Optional
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
    
    def __init__(self, database_path: str) -> None:
        """
        Initialiseer de database connectie.
        
        Args:
            database_path (str): Pad naar het SQLite database bestand
        
        Raises:
            ValueError: Als het pad leeg is
            Exception: Bij database connectie fouten
        """
        if not database_path:
            raise ValueError("Database pad mag niet leeg zijn")
        
        self.database_path: str = database_path
        self.connection: Optional[sqlite3.Connection] = None
        self._connect()
    
    def _connect(self) -> None:
        """
        Maak verbinding met de database.
        
        Private methode (conventie: _ prefix) voor interne operaties.
        Dit volgt het principe van Low Coupling (GRASP).
        
        Raises:
            Exception: Bij database connectie fouten
        """
        try:
            if not os.path.exists(self.database_path):
                raise FileNotFoundError(
                    f"Database bestand niet gevonden: {self.database_path}"
                )
            
            self.connection = sqlite3.connect(self.database_path)
            self.connection.row_factory = sqlite3.Row  # Voor dict-achtige toegang
            
            # Test de verbinding
            cursor = self.connection.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            
            if not any(table['name'] == 'products' for table in tables):
                raise ValueError(
                    "Database bevat geen 'products' tabel. "
                    "Voer 'python init_database.py' uit."
                )
        
        except sqlite3.Error as e:
            raise Exception(f"Database verbinding mislukt: {str(e)}") from e
    
    def _create_product_from_row(self, row: sqlite3.Row) -> Product:
        """
        Creëert een Product object uit een database rij.
        
        Args:
            row: SQLite Row object
        
        Returns:
            Product object
        
        Raises:
            ValueError: Bij ongeldige data
        """
        try:
            return Product(
                id=int(row['id']),
                name=str(row['name']),
                description=str(row['description'] or ''),
                price=float(row['price']),
                stock=int(row['stock']),
                image_path=str(row['image_path'] or '')
            )
        except (KeyError, ValueError, TypeError) as e:
            raise ValueError(
                f"Ongeldige product data in database: {str(e)}"
            ) from e
    
    def get_all_products(self) -> List[Product]:
        """
        Haal alle producten op uit de database.
        
        Returns:
            List[Product]: Lijst van Product objecten
        
        Raises:
            Exception: Bij database fouten
        """
        if not self.connection:
            self._connect()
        
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                SELECT id, name, description, price, stock, image_path
                FROM products
                ORDER BY id
            """)
            
            products: List[Product] = []
            for row in cursor.fetchall():
                try:
                    # Creator Pattern (GRASP): DatabaseSource creëert Product objecten
                    product = self._create_product_from_row(row)
                    products.append(product)
                except ValueError as e:
                    # Log maar skip ongeldige producten
                    print(f"Waarschuwing: {str(e)}")
                    continue
            
            if not products:
                raise ValueError(
                    "Geen geldige producten gevonden in database"
                )
            
            return products
        
        except sqlite3.Error as e:
            raise Exception(
                f"Fout bij ophalen van producten: {str(e)}"
            ) from e
    
    def close(self) -> None:
        """Sluit de database verbinding."""
        if self.connection:
            try:
                self.connection.close()
            except sqlite3.Error:
                pass  # Negeer fouten bij sluiten
            finally:
                self.connection = None
    
    def __enter__(self) -> 'DatabaseSource':
        """Context manager support (met 'with' statement)."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Context manager cleanup."""
        self.close()
    
    def __repr__(self) -> str:
        """String representatie voor debugging."""
        return f"DatabaseSource(database_path='{self.database_path}')"
    
    def __del__(self) -> None:
        """Destructor om verbinding te sluiten bij garbage collection."""
        self.close()
