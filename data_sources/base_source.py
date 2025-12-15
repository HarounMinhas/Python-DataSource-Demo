"""Base Data Source

Dit bestand definieert de abstracte basisklasse voor databronnen.

In traditionele OOP talen zoals Java zou dit een Interface zijn.
In Python gebruiken we de Abstract Base Class (abc) module voor
vergelijkbare functionaliteit.

Voorbeeld vergelijking:

Java:
    public interface IDataSource {
        List<Product> getAllProducts();
    }

Python (deze implementatie):
    class BaseDataSource(ABC):
        @abstractmethod
        def get_all_products(self): pass

Voordelen van Python's benadering:
- Minder boilerplate code
- Duck typing: als een object de juiste methodes heeft, werkt het
- Flexibeler: je kunt ook mixins en multiple inheritance gebruiken
"""

from abc import ABC, abstractmethod
from typing import List
from models.product import Product


class BaseDataSource(ABC):
    """
    Abstracte basisklasse voor alle databronnen.
    
    Deze klasse volgt het Interface Segregation Principle (SOLID):
    clients worden niet gedwongen om afhankelijk te zijn van methodes
    die ze niet gebruiken.
    
    Het Dependency Inversion Principle (SOLID) wordt ook toegepast:
    high-level modules (app.py) zijn afhankelijk van deze abstractie,
    niet van concrete implementaties.
    """
    
    @abstractmethod
    def get_all_products(self) -> List[Product]:
        """
        Haal alle producten op uit de databron.
        
        Returns:
            List[Product]: Lijst van Product objecten
        """
        pass
    
    @abstractmethod
    def close(self):
        """
        Sluit de verbinding met de databron.
        
        Deze methode volgt het principe van proper resource management.
        """
        pass
