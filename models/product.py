"""Product Model

Dit bestand definieert het Product datamodel.

In Python wordt vaak een functionele benadering gebruikt in plaats van
zware OOP-structuren. Dit model is een eenvoudige dataklasse die de
productgegevens representeert.

Verschil met traditionele OOP talen (zoals Java/C#):
- Python gebruikt duck typing: als een object de juiste methodes heeft,
  werkt het, ongeacht de klasse-hierarchie
- Geen expliciete interfaces nodig (hoewel mogelijk via abc module)
- Properties en methodes kunnen dynamisch toegevoegd worden
- Focus op eenvoud en leesbaarheid boven strikte encapsulatie
"""

import os
from typing import Optional, Dict, Any


class Product:
    """
    Representeert een product uit de webwinkel.
    
    Deze klasse volgt het Single Responsibility Principle (SOLID):
    de klasse heeft slechts één verantwoordelijkheid - het representeren
    van productgegevens.
    
    Attributes:
        id (int): Uniek product ID
        name (str): Productnaam
        description (str): Productbeschrijving
        price (float): Prijs in euro
        stock (int): Aantal op voorraad
        image_path (str): Pad naar productafbeelding
    """
    
    def __init__(
        self,
        id: int,
        name: str,
        description: str,
        price: float,
        stock: int,
        image_path: str
    ) -> None:
        """
        Initialiseer een Product.
        
        Args:
            id: Uniek product ID (moet positief zijn)
            name: Productnaam (mag niet leeg zijn)
            description: Productbeschrijving
            price: Prijs in euro (mag niet negatief zijn)
            stock: Voorraad aantal (mag niet negatief zijn)
            image_path: Pad naar productafbeelding
        
        Raises:
            ValueError: Bij ongeldige input waardes
        """
        # Validatie
        if not isinstance(id, int) or id <= 0:
            raise ValueError(f"Product ID moet een positief getal zijn, kreeg: {id}")
        
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Product naam mag niet leeg zijn")
        
        if not isinstance(price, (int, float)) or price < 0:
            raise ValueError(f"Prijs mag niet negatief zijn, kreeg: {price}")
        
        if not isinstance(stock, int) or stock < 0:
            raise ValueError(f"Voorraad mag niet negatief zijn, kreeg: {stock}")
        
        # Assignments
        self.id: int = id
        self.name: str = name.strip()
        self.description: str = description.strip() if description else ''
        self.price: float = float(price)
        self.stock: int = stock
        self.image_path: str = image_path.strip() if image_path else ''
    
    def get_display_image(self) -> str:
        """
        Geeft het te tonen afbeeldingspad terug.
        
        Als de opgegeven afbeelding niet bestaat, wordt een placeholder
        icoon teruggegeven. Dit voorkomt dat binaire afbeeldingen in de
        repository moeten worden opgeslagen.
        
        Returns:
            str: Pad naar de afbeelding of placeholder
        """
        if self.image_path:
            full_path = os.path.join('static', 'images', self.image_path)
            if os.path.exists(full_path):
                return self.image_path
        
        return 'placeholder.png'
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Converteer het Product object naar een dictionary.
        
        Deze methode maakt JSON serialisatie mogelijk (DRY principle:
        herbruikbare conversie logica op één plek).
        
        Returns:
            dict: Dictionary representatie van het product
        """
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'stock': self.stock,
            'image': self.get_display_image()
        }
    
    @property
    def is_low_stock(self) -> bool:
        """
        Controleer of het product een lage voorraad heeft.
        
        Returns:
            bool: True als voorraad minder dan 10 is
        """
        return self.stock < 10
    
    @property
    def formatted_price(self) -> str:
        """
        Geeft de prijs terug in geformatteerde string.
        
        Returns:
            str: Prijs met euro symbool
        """
        return f"€{self.price:.2f}"
    
    def __repr__(self) -> str:
        """String representatie voor debugging."""
        return (
            f"Product(id={self.id}, name='{self.name}', "
            f"price={self.price}, stock={self.stock})"
        )
    
    def __eq__(self, other: object) -> bool:
        """Vergelijk twee Product objecten op basis van ID."""
        if not isinstance(other, Product):
            return NotImplemented
        return self.id == other.id
    
    def __hash__(self) -> int:
        """Hash functie voor gebruik in sets en dictionaries."""
        return hash(self.id)
