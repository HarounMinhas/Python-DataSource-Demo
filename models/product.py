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
    
    def __init__(self, id, name, description, price, stock, image_path):
        self.id = id
        self.name = name
        self.description = description
        self.price = price
        self.stock = stock
        self.image_path = image_path
    
    def get_display_image(self):
        """
        Geeft het te tonen afbeeldingspad terug.
        
        Als de opgegeven afbeelding niet bestaat, wordt een placeholder
        icoon teruggegeven. Dit voorkomt dat binaire afbeeldingen in de
        repository moeten worden opgeslagen.
        
        Returns:
            str: Pad naar de afbeelding of placeholder
        """
        if self.image_path and os.path.exists(os.path.join('static/images', self.image_path)):
            return self.image_path
        return 'placeholder.png'
    
    def to_dict(self):
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
    
    def __repr__(self):
        """String representatie voor debugging."""
        return f"Product(id={self.id}, name='{self.name}', price={self.price})"
