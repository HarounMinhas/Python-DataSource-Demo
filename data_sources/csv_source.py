"""CSV Data Source

Dit bestand implementeert toegang tot een CSV bestand.

CSV (Comma-Separated Values) is een eenvoudig tekstformaat voor
tabellaire data. Het wordt vaak gebruikt voor data-uitwisseling
tussen verschillende systemen.
"""

import csv
from typing import List
from models.product import Product
from .base_source import BaseDataSource


class CSVSource(BaseDataSource):
    """
    Implementatie voor CSV bestand toegang.
    
    Deze klasse demonstreert hetzelfde patroon als DatabaseSource,
    maar met een andere databron. Dit toont het Strategy Pattern
    in actie: verschillende implementaties van dezelfde interface.
    """
    
    def __init__(self, csv_path: str):
        """
        Initialiseer de CSV bron.
        
        Args:
            csv_path (str): Pad naar het CSV bestand
        """
        self.csv_path = csv_path
    
    def get_all_products(self) -> List[Product]:
        """
        Lees alle producten uit het CSV bestand.
        
        Returns:
            List[Product]: Lijst van Product objecten
        """
        products = []
        
        try:
            with open(self.csv_path, 'r', encoding='utf-8') as file:
                # DictReader parse CSV en geeft elke rij als dictionary
                reader = csv.DictReader(file)
                
                for row in reader:
                    # Converteer string waardes naar juiste types
                    product = Product(
                        id=int(row['id']),
                        name=row['name'],
                        description=row['description'],
                        price=float(row['price']),
                        stock=int(row['stock']),
                        image_path=row['image_path']
                    )
                    products.append(product)
        
        except FileNotFoundError:
            raise Exception(f"CSV bestand niet gevonden: {self.csv_path}")
        except ValueError as e:
            raise Exception(f"Ongeldige data in CSV: {e}")
        except KeyError as e:
            raise Exception(f"Ontbrekende kolom in CSV: {e}")
        
        return products
    
    def close(self):
        """
        Sluit de bron.
        
        Voor CSV is er geen actieve verbinding, maar de methode wordt
        geïmplementeerd voor consistentie met de interface.
        """
        pass  # Geen actieve verbinding om te sluiten
    
    def __enter__(self):
        """Context manager support."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager cleanup."""
        self.close()
