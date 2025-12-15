# Software Ontwikkelprincipes - Uitgebreide Uitleg

Dit document biedt een diepgaande uitleg van de software ontwikkelprincipes die in deze demo worden toegepast.

## SOLID Principes

### Single Responsibility Principle (SRP)

**Definitie**: Een klasse moet precies één reden hebben om te veranderen. Met andere woorden, elke klasse moet één duidelijke verantwoordelijkheid hebben.

**Waarom belangrijk?**
- Makkelijker te begrijpen en te onderhouden
- Wijzigingen hebben minder impact
- Herbruikbaarheid neemt toe
- Testing wordt eenvoudiger

**In deze demo:**

```python
# GOED: Product heeft alleen verantwoordelijkheid voor productdata
class Product:
    def __init__(self, id, name, price):
        self.id = id
        self.name = name
        self.price = price
    
    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'price': self.price}

# FOUT: Product doet te veel
class Product:
    def __init__(self, id, name, price):
        self.id = id
        self.name = name
        self.price = price
    
    def save_to_database(self):  # Database logica hoort hier niet
        pass
    
    def send_email_notification(self):  # Email logica hoort hier niet
        pass
```

### Open/Closed Principle (OCP)

**Definitie**: Software entiteiten moeten open zijn voor uitbreiding, maar gesloten voor modificatie.

**Waarom belangrijk?**
- Voorkomt het breken van bestaande functionaliteit
- Nieuwe features toevoegen zonder risico
- Stabielere codebase

**In deze demo:**

```python
# GOED: Voeg nieuwe databron toe zonder bestaande code te wijzigen
class XMLSource(BaseDataSource):
    def get_all_products(self):
        # Nieuwe implementatie
        pass

# De rest van de applicatie werkt zonder wijzigingen
```

### Liskov Substitution Principle (LSP)

**Definitie**: Objecten van een afgeleide klasse moeten vervangbaar zijn voor objecten van de basisklasse zonder dat het programma kapot gaat.

**Waarom belangrijk?**
- Garandeert juist gebruik van overerving
- Voorkomt verrassend gedrag
- Maakt polymorfisme betrouwbaar

**In deze demo:**

```python
# Beide implementaties kunnen gebruikt worden waar BaseDataSource verwacht wordt
def process_products(source: BaseDataSource):
    products = source.get_all_products()
    # Werkt met DatabaseSource, CSVSource, of elke andere implementatie
```

### Interface Segregation Principle (ISP)

**Definitie**: Clients moeten niet gedwongen worden om te dependeren van interfaces die ze niet gebruiken.

**Waarom belangrijk?**
- Voorkomt onnodig grote interfaces
- Verhoogt flexibiliteit
- Vermindert coupling

**In deze demo:**

```python
# GOED: Minimale interface
class BaseDataSource(ABC):
    @abstractmethod
    def get_all_products(self): pass
    
    @abstractmethod
    def close(self): pass

# FOUT: Te veel methodes die niet altijd nodig zijn
class BaseDataSource(ABC):
    @abstractmethod
    def get_all_products(self): pass
    
    @abstractmethod
    def get_product_by_id(self): pass
    
    @abstractmethod
    def update_product(self): pass
    
    @abstractmethod
    def delete_product(self): pass
    # ... etc
```

### Dependency Inversion Principle (DIP)

**Definitie**: High-level modules mogen niet afhangen van low-level modules. Beiden moeten afhangen van abstracties.

**Waarom belangrijk?**
- Vermindert coupling
- Maakt code flexibeler
- Vergemakkelijkt testing (mocking)

**In deze demo:**

```python
# GOED: app.py hangt af van abstractie (BaseDataSource)
if source_type == 'csv':
    data_source = CSVSource(CSV_PATH)
else:
    data_source = DatabaseSource(DATABASE_PATH)

products = data_source.get_all_products()  # Polymorfisme

# FOUT: Directe afhankelijkheid van concrete implementatie
db = sqlite3.connect('products.db')
cursor = db.cursor()
# ... direct database operaties in app.py
```

## GRASP Principes

### Information Expert

**Definitie**: Ken verantwoordelijkheid toe aan de klasse die de meeste informatie heeft om deze te vervullen.

**Toepassing:**

```python
# DatabaseSource is de expert voor database operaties
class DatabaseSource:
    def get_all_products(self):
        # Deze klasse kent de database structuur
        cursor.execute("SELECT * FROM products")
        # ...
```

### Creator

**Definitie**: Klasse A moet objecten van type B creëren als:
- A bevat B
- A registreert B
- A gebruikt B intensief
- A heeft de initialisatie data voor B

**Toepassing:**

```python
# DatabaseSource creëert Product objecten omdat het de data heeft
class DatabaseSource:
    def get_all_products(self):
        products = []
        for row in cursor.fetchall():
            product = Product(...)  # Creator
            products.append(product)
        return products
```

### Low Coupling

**Definitie**: Minimaliseer afhankelijkheden tussen klassen.

**Voordelen:**
- Wijzigingen in één klasse beïnvloeden andere klassen minder
- Hergebruik is eenvoudiger
- Testing is simpeler

**Toepassing:**

```python
# DatabaseSource en CSVSource zijn onafhankelijk van elkaar
# Ze delen alleen de BaseDataSource interface
```

### High Cohesion

**Definitie**: Houd gerelateerde functionaliteit bij elkaar in één klasse.

**Toepassing:**

```python
# Alle database operaties zitten in DatabaseSource
class DatabaseSource:
    def _connect(self): pass
    def get_all_products(self): pass
    def close(self): pass
    # Alle methodes zijn gerelateerd aan database toegang
```

### Controller

**Definitie**: Wijs de verantwoordelijkheid voor het afhandelen van system events toe aan een controller klasse.

**Toepassing:**

```python
# app.py functioneert als controller
@app.route('/api/products')
def get_products():
    # Coördineert tussen request, databron en response
    source_type = request.args.get('source')
    data_source = # ... kies databron
    products = data_source.get_all_products()
    return jsonify(products)
```

## KISS (Keep It Simple, Stupid)

**Definitie**: Houd oplossingen zo simpel mogelijk. Voeg geen onnodige complexiteit toe.

**Principes:**
- Gebruik duidelijke namen
- Vermijd over-engineering
- Kies de eenvoudigste oplossing die werkt
- Voeg alleen functionaliteit toe die nodig is

**Voorbeelden:**

```python
# GOED: Simpel en duidelijk
def get_display_image(self):
    if self.image_path and os.path.exists(self.image_path):
        return self.image_path
    return 'placeholder.png'

# FOUT: Onnodig complex
def get_display_image(self):
    image_validator = ImageValidator()
    image_factory = ImageFactory()
    image_strategy = ImageSelectionStrategy()
    # ... 20 regels code voor een simpele check
```

## DRY (Don't Repeat Yourself)

**Definitie**: Elke kenniseenheid moet een enkele, ondubbelzinnige representatie hebben binnen een systeem.

**Waarom belangrijk?**
- Wijzigingen hoef je maar op één plek door te voeren
- Vermindert kans op bugs
- Makkelijker onderhoud

**Voorbeelden:**

```python
# GOED: Conversie logica op één plek
class Product:
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price
        }

# Gebruik overal
products_data = [product.to_dict() for product in products]

# FOUT: Herhaling
# In file1.py
data = {'id': product.id, 'name': product.name, 'price': product.price}

# In file2.py
data = {'id': product.id, 'name': product.name, 'price': product.price}

# In file3.py
data = {'id': product.id, 'name': product.name, 'price': product.price}
```

## Design Patterns

### Strategy Pattern

**Doel**: Definieer een familie van algoritmen, encapsuleer ze, en maak ze uitwisselbaar.

**Toepassing in demo:**

```python
# Verschillende strategieën voor data ophalen
if source_type == 'csv':
    strategy = CSVSource(CSV_PATH)
else:
    strategy = DatabaseSource(DATABASE_PATH)

# Gebruik de gekozen strategie
products = strategy.get_all_products()
```

**Voordelen:**
- Runtime keuze tussen algoritmen
- Makkelijk nieuwe strategieën toevoegen
- Vermindert conditionals in client code

### Factory Pattern

**Doel**: Definieer een interface voor het creëren van objecten, maar laat subklassen beslissen welke klasse te instantiëren.

**Toepassing in demo:**

```python
# Lichtgewicht factory in app.py
def create_data_source(source_type):
    if source_type == 'csv':
        return CSVSource(CSV_PATH)
    elif source_type == 'database':
        return DatabaseSource(DATABASE_PATH)
    else:
        raise ValueError(f"Unknown source type: {source_type}")
```

### Template Method Pattern

**Doel**: Definieer het skelet van een algoritme in een basisklasse, maar laat subklassen specifieke stappen overschrijven.

**Toepassing in demo:**

```python
# BaseDataSource definieert het template
class BaseDataSource(ABC):
    @abstractmethod
    def get_all_products(self):
        pass

# Concrete implementaties vullen de details in
class DatabaseSource(BaseDataSource):
    def get_all_products(self):
        # Database specifieke implementatie
        pass

class CSVSource(BaseDataSource):
    def get_all_products(self):
        # CSV specifieke implementatie
        pass
```

## Python Specifieke Concepten

### Duck Typing

```python
# Python controleert niet het type, alleen het gedrag
def process_source(source):
    # Zolang 'source' een get_all_products() methode heeft, werkt het
    products = source.get_all_products()
    return products

# Werkt met elke klasse die get_all_products() implementeert
```

### Context Managers

```python
# Automatische resource cleanup met 'with' statement
with DatabaseSource(DB_PATH) as source:
    products = source.get_all_products()
# source.close() wordt automatisch aangeroepen
```

### List Comprehensions

```python
# Pythonische manier om lijsten te transformeren
products_data = [product.to_dict() for product in products]

# In plaats van
products_data = []
for product in products:
    products_data.append(product.to_dict())
```

## Conclusie

Deze principes werken samen om code te creëren die:
- **Maintainable** is: makkelijk te begrijpen en aan te passen
- **Extensible** is: nieuwe functionaliteit toevoegen zonder bestaande code te breken
- **Testable** is: componenten kunnen geïsoleerd getest worden
- **Reusable** is: componenten kunnen in verschillende contexten gebruikt worden

Het belangrijkste is om deze principes pragmatisch toe te passen. Niet elk principe is in elke situatie even belangrijk. Gebruik je eigen oordeel en pas toe wat zinvol is voor jouw specifieke situatie.
