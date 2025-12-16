"""CSV Data Source

Dit bestand implementeert toegang tot een CSV bestand.

CSV (Comma-Separated Values) is een eenvoudig tekstformaat voor
tabellaire data. Het wordt vaak gebruikt voor data-uitwisseling
tussen verschillende systemen.
"""

import csv
import os
from typing import List, Optional
from models.product import Product
from .base_source import BaseDataSource


class CSVSource(BaseDataSource):
    """
    Implementatie voor CSV bestand toegang.
    
    Deze klasse demonstreert hetzelfde patroon als DatabaseSource,
    maar met een andere databron. Dit toont het Strategy Pattern
    in actie: verschillende implementaties van dezelfde interface.
    """
    
    def __init__(self, csv_path: str) -> None:
        """
        Initialiseer de CSV bron.
        
        Args:
            csv_path (str): Pad naar het CSV bestand
        
        Raises:
            ValueError: Als het pad leeg is
        """
        if not csv_path:
            raise ValueError("CSV pad mag niet leeg zijn")
        
        self.csv_path: str = csv_path
        self._validate_file_exists()
    
    def _validate_file_exists(self) -> None:
        """
        Controleer of het CSV bestand bestaat.
        
        Raises:
            FileNotFoundError: Als het bestand niet bestaat
        """
        if not os.path.exists(self.csv_path):
            raise FileNotFoundError(
                f"CSV bestand niet gevonden: {self.csv_path}"
            )
    
    def _parse_product_row(self, row: dict, row_number: int) -> Optional[Product]:
        """
        Parse een CSV rij naar een Product object.
        
        Args:
            row: Dictionary met product data
            row_number: Rijnummer voor error reporting
        
        Returns:
            Product object of None bij fouten
        
        Raises:
            ValueError: Bij ongeldige data
        """
        try:
            # Valideer vereiste velden
            required_fields = ['id', 'name', 'description', 'price', 'stock', 'image_path']
            missing_fields = [field for field in required_fields if field not in row]
            
            if missing_fields:
                raise KeyError(
                    f"Ontbrekende kolommen in rij {row_number}: {', '.join(missing_fields)}"
                )
            
            # Converteer en valideer types
            product_id = int(row['id'])
            name = row['name'].strip()
            description = row['description'].strip()
            price = float(row['price'])
            stock = int(row['stock'])
            image_path = row['image_path'].strip()
            
            # Valideer waardes
            if product_id <= 0:
                raise ValueError(f"Product ID moet positief zijn (rij {row_number})")
            
            if not name:
                raise ValueError(f"Product naam mag niet leeg zijn (rij {row_number})")
            
            if price < 0:
                raise ValueError(f"Prijs mag niet negatief zijn (rij {row_number})")
            
            if stock < 0:
                raise ValueError(f"Voorraad mag niet negatief zijn (rij {row_number})")
            
            return Product(
                id=product_id,
                name=name,
                description=description,
                price=price,
                stock=stock,
                image_path=image_path
            )
        
        except (ValueError, KeyError) as e:
            raise ValueError(
                f"Fout bij verwerken van rij {row_number}: {str(e)}"
            ) from e
    
    def get_all_products(self) -> List[Product]:
        """
        Lees alle producten uit het CSV bestand.
        
        Returns:
            List[Product]: Lijst van Product objecten
        
        Raises:
            FileNotFoundError: Als het bestand niet bestaat
            ValueError: Bij ongeldige data in het CSV bestand
            Exception: Bij andere fouten
        """
        products: List[Product] = []
        
        try:
            with open(self.csv_path, 'r', encoding='utf-8') as file:
                # DictReader parse CSV en geeft elke rij als dictionary
                # quoting=csv.QUOTE_MINIMAL zorgt voor correcte afhandeling van quotes
                reader = csv.DictReader(
                    file,
                    quoting=csv.QUOTE_MINIMAL,
                    skipinitialspace=True
                )
                
                # Controleer of CSV headers aanwezig zijn
                if not reader.fieldnames:
                    raise ValueError(
                        "CSV bestand heeft geen headers of is leeg"
                    )
                
                # Verwerk elke rij
                for row_number, row in enumerate(reader, start=2):  # Start bij 2 (na header)
                    product = self._parse_product_row(row, row_number)
                    if product:
                        products.append(product)
            
            if not products:
                raise ValueError(
                    "Geen geldige producten gevonden in CSV bestand"
                )
            
            return products
        
        except FileNotFoundError as e:
            raise FileNotFoundError(
                f"CSV bestand niet gevonden: {self.csv_path}"
            ) from e
        
        except csv.Error as e:
            raise ValueError(
                f"Fout bij lezen van CSV bestand: {str(e)}"
            ) from e
        
        except Exception as e:
            raise Exception(
                f"Onverwachte fout bij lezen van CSV: {str(e)}"
            ) from e
    
    def close(self) -> None:
        """
        Sluit de bron.
        
        Voor CSV is er geen actieve verbinding, maar de methode wordt
        geïmplementeerd voor consistentie met de interface.
        """
        pass  # Geen actieve verbinding om te sluiten
    
    def __enter__(self) -> 'CSVSource':
        """Context manager support."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Context manager cleanup."""
        self.close()
    
    def __repr__(self) -> str:
        """String representatie voor debugging."""
        return f"CSVSource(csv_path='{self.csv_path}')"
