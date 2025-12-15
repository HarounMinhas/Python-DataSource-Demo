# Installatie Instructies

Deze handleiding begeleidt je stap voor stap bij het installeren en opstarten van de Python DataSource Demo applicatie.

## Vereisten

- Python 3.8 of hoger geïnstalleerd op je systeem
- Git (om de repository te klonen)
- Een teksteditor of IDE (bijvoorbeeld VS Code, PyCharm, of Sublime Text)
- Terminal/Command Prompt/PowerShell toegang

### Python Versie Controleren

Open een terminal en voer uit:

```bash
python --version
```

of op sommige systemen:

```bash
python3 --version
```

Je zou iets moeten zien zoals `Python 3.8.x` of hoger.

## Stap 1: Repository Klonen

Open een terminal en navigeer naar de map waar je het project wilt plaatsen:

```bash
cd pad/naar/gewenste/map
```

Kloon de repository:

```bash
git clone https://github.com/HarounMinhas/Python-DataSource-Demo.git
```

Ga naar de project directory:

```bash
cd Python-DataSource-Demo
```

## Stap 2: Virtual Environment Aanmaken

Een virtual environment isoleert de project dependencies van je systeem Python installatie.

### Windows

```bash
python -m venv venv
```

### macOS/Linux

```bash
python3 -m venv venv
```

## Stap 3: Virtual Environment Activeren

### Windows (Command Prompt)

```bash
venv\Scripts\activate
```

### Windows (PowerShell)

```bash
venv\Scripts\Activate.ps1
```

Als je een foutmelding krijgt over execution policy:

```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Probeer daarna opnieuw.

### macOS/Linux

```bash
source venv/bin/activate
```

### Verificatie

Als de virtual environment actief is, zie je `(venv)` voor je command prompt:

```
(venv) C:\Users\YourName\Python-DataSource-Demo>
```

## Stap 4: Dependencies Installeren

Installeer de benodigde Python packages:

```bash
pip install -r requirements.txt
```

Dit installeert:
- Flask: het web framework
- Werkzeug: utilities voor Flask

## Stap 5: Database Initialiseren

Maak de SQLite database aan en vul deze met sample data:

```bash
python init_database.py
```

Je zou moeten zien:

```
Database aangemaakt: data/products.db
5 producten toegevoegd aan de database.
```

## Stap 6: Applicatie Starten

Start de Flask development server:

```bash
python app.py
```

Je zou output moeten zien zoals:

```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
```

## Stap 7: Applicatie Openen

Open je webbrowser en ga naar:

```
http://localhost:5000
```

of

```
http://127.0.0.1:5000
```

Je zou nu de webinterface moeten zien met de optie om tussen Database en CSV te wisselen.

## Applicatie Stoppen

Druk in de terminal op `Ctrl+C` om de server te stoppen.

## Virtual Environment Deactiveren

Wanneer je klaar bent:

```bash
deactivate
```

## Problemen Oplossen

### Port 5000 al in gebruik

Als je de foutmelding krijgt dat port 5000 al in gebruik is, kun je een andere port gebruiken:

```bash
python app.py
```

En wijzig in `app.py` de laatste regel naar:

```python
app.run(debug=True, port=5001)
```

### Module niet gevonden

Als je een "ModuleNotFoundError" krijgt:

1. Controleer of je virtual environment actief is (zie `(venv)` in prompt)
2. Installeer dependencies opnieuw: `pip install -r requirements.txt`

### Database niet aangemaakt

Als de database niet bestaat:

1. Controleer of de `data` directory bestaat
2. Voer `python init_database.py` opnieuw uit
3. Controleer of je schrijfrechten hebt in de project directory

### CSV bestand niet gevonden

Controleer of `data/products.csv` bestaat. Dit bestand zou automatisch aanwezig moeten zijn na het klonen van de repository.

## Project Structuur Verifiëren

Na installatie zou je directory er zo uit moeten zien:

```
Python-DataSource-Demo/
├── venv/                    # Virtual environment (niet in Git)
├── data/
│   ├── products.db          # Gegenereerde database
│   └── products.csv         # Sample CSV data
├── models/
├── data_sources/
├── templates/
├── static/
├── app.py
├── init_database.py
├── requirements.txt
└── README.md
```

## Volgende Stappen

Nu de applicatie draait:

1. Experimenteer met het wisselen tussen Database en CSV bronnen
2. Bekijk de code in de verschillende modules
3. Lees [PRINCIPLES.md](PRINCIPLES.md) voor diepgaande uitleg
4. Probeer zelf wijzigingen aan te brengen

## Development Workflow

Voor verder ontwikkelen:

1. Activeer virtual environment
2. Maak wijzigingen in de code
3. Flask herlaadt automatisch (debug mode)
4. Test je wijzigingen in de browser
5. Commit je wijzigingen naar Git

```bash
git add .
git commit -m "Beschrijving van wijzigingen"
git push
```
