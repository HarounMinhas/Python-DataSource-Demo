# Python DataSource Demo

Een educatieve demo-applicatie die laat zien hoe je in Python met verschillende databronnen werkt (SQLite database en CSV bestanden) via een webinterface.

## Doel van deze Demo

Deze applicatie is ontworpen als leermiddel om de volgende concepten te demonstreren:

- Werken met verschillende databronnen in Python
- Toepassen van software ontwikkelprincipes (SOLID, GRASP, KISS, DRY)
- Verschil tussen Python's benadering en traditionele Object-Georiënteerde programmeertalen
- Design patterns in de praktijk
- Opzetten van een eenvoudige webapplicatie met Flask

## Waarom Python anders is dan Traditionele OOP

In traditionele Object-Georiënteerde talen zoals Java of C# is de structuur vaak rigide met interfaces, abstracte klassen, en strikte type-systemen. Python hanteert een andere filosofie:

### Duck Typing

Python gebruikt "duck typing": als een object eruitziet als een eend en kwaakt als een eend, dan is het een eend. Je hoeft niet expliciet te declareren dat een klasse een interface implementeert.

**Java voorbeeld:**
```java
public interface DataSource {
    List<Product> getAllProducts();
}

public class DatabaseSource implements DataSource {
    public List<Product> getAllProducts() { ... }
}
```

**Python equivalent:**
```python
class DatabaseSource:
    def get_all_products(self):
        ...
```

Python controleert pas tijdens uitvoering of een methode bestaat, niet tijdens compilatie.

### Protocol-Oriented in plaats van Interface-Oriented

Python focust op wat een object kan doen (zijn protocol) in plaats van wat het is (zijn type). In deze demo zie je dat via de Abstract Base Class (abc module), maar zelfs die is optioneel.

### Flexibiliteit en Eenvoud

Python code is vaak korter en leesbaarder omdat:
- Geen expliciete type declaraties nodig (hoewel type hints mogelijk zijn)
- Minder boilerplate code
- Dynamische eigenschappen: je kunt attributen en methodes tijdens runtime toevoegen
- Ingebouwde features zoals list comprehensions, decorators, context managers

### Wanneer gebruik je wel OOP in Python?

Python ondersteunt volledige OOP, maar gebruik het selectief:
- Gebruik klassen voor logisch gegroepeerde functionaliteit
- Gebruik overerving spaarzaam (compositie heeft vaak de voorkeur)
- Gebruik abstracte basisklassen voor expliciete contracten
- Simpele functies zijn vaak beter dan klassen met één methode

## Software Ontwikkelprincipes

### SOLID Principes

SOLID is een acroniem voor vijf ontwerpprincipes die code onderhoudbaar en uitbreidbaar maken:

**S - Single Responsibility Principle**
Elke klasse heeft één verantwoordelijkheid. In deze demo:
- `Product`: representeert alleen productgegevens
- `DatabaseSource`: handelt alleen database operaties af
- `CSVSource`: handelt alleen CSV operaties af

**O - Open/Closed Principle**
Klassen zijn open voor uitbreiding, maar gesloten voor modificatie. Je kunt nieuwe databronnen toevoegen zonder bestaande code te wijzigen.

**L - Liskov Substitution Principle**
Afgeleide klassen moeten vervangbaar zijn voor hun basisklassen. Zowel `DatabaseSource` als `CSVSource` kunnen gebruikt worden waar `BaseDataSource` verwacht wordt.

**I - Interface Segregation Principle**
Clients moeten niet afhankelijk zijn van interfaces die ze niet gebruiken. `BaseDataSource` bevat alleen de minimaal nodige methodes.

**D - Dependency Inversion Principle**
Hang af van abstracties, niet van concrete implementaties. `app.py` gebruikt `BaseDataSource`, niet direct `DatabaseSource` of `CSVSource`.

### GRASP Principes

GRASP (General Responsibility Assignment Software Patterns) helpt bij het toewijzen van verantwoordelijkheden:

**Information Expert**
Ken verantwoordelijkheid toe aan de klasse die de meeste informatie heeft. `DatabaseSource` kent de databasestructuur, dus handelt database queries af.

**Creator**
Klasse A creëert objecten van klasse B als A deze bevat of gebruikt. `DatabaseSource` creëert `Product` objecten uit database rows.

**Low Coupling**
Minimaliseer afhankelijkheden tussen klassen. Databronnen zijn onafhankelijk van elkaar.

**High Cohesion**
Houd gerelateerde functionaliteit bij elkaar. Alle database operaties zitten in `DatabaseSource`.

**Controller**
`app.py` fungeert als controller: handelt requests af en coördineert tussen componenten.

### KISS (Keep It Simple, Stupid)

Hou code simpel en begrijpelijk. In deze demo:
- Geen overbodige abstracties
- Duidelijke naamgeving
- Eenvoudige datastructuren
- Minimale externe dependencies

### DRY (Don't Repeat Yourself)

Vermijd code duplicatie. In deze demo:
- `Product.to_dict()`: conversie logica op één plek
- `BaseDataSource`: gedeelde interface definitie
- Herbruikbare componenten in aparte modules

### Design Patterns

**Strategy Pattern**
De applicatie gebruikt verschillende strategieën (database, CSV) die tijdens runtime uitgewisseld kunnen worden. Dit zie je in `app.py` waar de databron gekozen wordt op basis van gebruikersinput.

**Factory Pattern**
In `app.py` wordt de juiste databron geïnstantieerd op basis van de `source_type` parameter. Dit is een lichtgewicht factory pattern.

**Template Method Pattern**
`BaseDataSource` definieert het template (interface) dat alle concrete implementaties moeten volgen.

## Project Structuur

```
Python-DataSource-Demo/
├── app.py                      # Hoofd Flask applicatie
├── requirements.txt            # Python dependencies
├── README.md                   # Deze documentatie
├── SETUP.md                    # Installatie instructies
├── PRINCIPLES.md               # Uitgebreide uitleg principes
├── init_database.py            # Database initialisatie script
├── models/
│   ├── __init__.py
│   └── product.py              # Product datamodel
├── data_sources/
│   ├── __init__.py
│   ├── base_source.py          # Abstracte basisklasse
│   ├── database_source.py      # SQLite implementatie
│   └── csv_source.py           # CSV implementatie
├── data/
│   ├── products.db             # SQLite database (wordt gegenereerd)
│   └── products.csv            # CSV bestand met productdata
├── templates/
│   └── index.html              # HTML template
└── static/
    ├── css/
    │   └── style.css           # Stylesheet
    ├── js/
    │   └── app.js              # Frontend JavaScript
    └── images/
        └── placeholder.png     # Placeholder afbeelding
```

## Installatie en Gebruik

Zie [SETUP.md](SETUP.md) voor gedetailleerde installatie-instructies.

## Functionaliteit

### Databron Selectie

De gebruiker kan kiezen tussen twee databronnen:
- **Database**: SQLite database met gestructureerde data
- **CSV**: Tekstbestand met komma-gescheiden waardes

Beide bronnen bevatten dezelfde productgegevens en worden via dezelfde interface aangesproken.

### Product Weergave

De applicatie toont:
- Product ID
- Naam
- Beschrijving
- Prijs in euro
- Voorraad
- Afbeelding (of placeholder als deze niet bestaat)

### Afbeeldingen

Productafbeeldingen worden als placeholder getoond. In de database en CSV staat een bestandsnaam (bijvoorbeeld `laptop.png`), maar als dit bestand niet bestaat wordt automatisch een placeholder icoon gebruikt. Dit voorkomt dat binaire bestanden in de Git repository opgeslagen moeten worden.

## Leertraject

Voor studenten wordt aanbevolen om de code in deze volgorde te bestuderen:

1. **README.md** (dit bestand): Krijg overzicht van het project
2. **SETUP.md**: Installeer en start de applicatie
3. **PRINCIPLES.md**: Bestudeer de principes in detail
4. **models/product.py**: Begin met de simpelste component
5. **data_sources/base_source.py**: Begrijp de abstracte interface
6. **data_sources/database_source.py**: Zie concrete implementatie
7. **data_sources/csv_source.py**: Vergelijk met alternatieve implementatie
8. **app.py**: Begrijp hoe alles samenkomt
9. **templates/index.html** en **static/**: Frontend implementatie

## Uitbreidingsmogelijkheden

Deze demo kan uitgebreid worden met:
- Zoek- en filterfunctionaliteit
- CRUD operaties (Create, Read, Update, Delete)
- Authenticatie en autorisatie
- RESTful API met meerdere endpoints
- Andere databronnen (JSON, XML, externe API's)
- Unit tests en integration tests
- Error handling en logging
- Caching mechanismen

## Licentie

Deze demo is vrij beschikbaar voor educatieve doeleinden.
