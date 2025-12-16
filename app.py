"""Main Application

Dit bestand bevat de Flask webapplicatie die de gebruikersinterface biedt
voor het ophalen van productgegevens uit verschillende databronnen.

Flask werd gekozen omdat het eenvoudig en lichtgewicht is, ideaal voor
demo-doeleinden.
"""

from flask import Flask, render_template, request, jsonify
from typing import Dict, Any, List
from data_sources.database_source import DatabaseSource
from data_sources.csv_source import CSVSource
from data_sources.base_source import BaseDataSource
from models.product import Product
import os
import sys

app = Flask(__name__)

# Configuratie
DATABASE_PATH: str = 'data/products.db'
CSV_PATH: str = 'data/products.csv'


def create_data_source(source_type: str) -> BaseDataSource:
    """
    Factory functie voor het creëren van databronnen.
    
    Dit is een implementatie van het Factory Pattern: de juiste databron
    wordt geïnstantieerd op basis van de source_type parameter.
    
    Args:
        source_type: Type databron ('database' of 'csv')
    
    Returns:
        BaseDataSource: Concrete databron implementatie
    
    Raises:
        ValueError: Als source_type ongeldig is
    """
    source_type = source_type.lower().strip()
    
    if source_type == 'csv':
        return CSVSource(CSV_PATH)
    elif source_type == 'database':
        return DatabaseSource(DATABASE_PATH)
    else:
        raise ValueError(
            f"Ongeldige databron type: '{source_type}'. "
            "Gebruik 'database' of 'csv'."
        )


@app.route('/')
def index() -> str:
    """Render de hoofdpagina met de gebruikersinterface."""
    return render_template('index.html')


@app.route('/api/products', methods=['GET'])
def get_products() -> tuple[Dict[str, Any], int]:
    """
    API endpoint voor het ophalen van producten.
    
    Query parameters:
        source (str): 'database' of 'csv' - kiest de databron
    
    Returns:
        JSON response met lijst van producten en HTTP status code
    """
    source_type: str = request.args.get('source', 'database')
    
    try:
        # Factory Pattern: selecteer de juiste databron gebaseerd op input
        data_source: BaseDataSource = create_data_source(source_type)
        
        try:
            # Haal producten op via de gekozen bron
            products: List[Product] = data_source.get_all_products()
            
            # Converteer Product objecten naar dictionaries voor JSON
            products_data: List[Dict[str, Any]] = [
                product.to_dict() for product in products
            ]
            
            return jsonify({
                'success': True,
                'source': source_type,
                'count': len(products_data),
                'products': products_data
            }), 200
        
        finally:
            # Zorg ervoor dat bronnen altijd worden vrijgegeven
            data_source.close()
    
    except ValueError as e:
        # Client fouten (ongeldige input)
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
    
    except FileNotFoundError as e:
        # Bestand niet gevonden
        return jsonify({
            'success': False,
            'error': str(e)
        }), 404
    
    except Exception as e:
        # Server fouten
        print(f"Onverwachte fout: {str(e)}", file=sys.stderr)
        return jsonify({
            'success': False,
            'error': 'Er is een onverwachte fout opgetreden'
        }), 500


@app.route('/api/health', methods=['GET'])
def health_check() -> tuple[Dict[str, Any], int]:
    """
    Health check endpoint voor monitoring.
    
    Returns:
        JSON response met status informatie
    """
    status: Dict[str, Any] = {
        'status': 'healthy',
        'database_exists': os.path.exists(DATABASE_PATH),
        'csv_exists': os.path.exists(CSV_PATH)
    }
    
    return jsonify(status), 200


@app.errorhandler(404)
def not_found(error) -> tuple[Dict[str, str], int]:
    """Handler voor 404 fouten."""
    return jsonify({
        'success': False,
        'error': 'Endpoint niet gevonden'
    }), 404


@app.errorhandler(500)
def internal_error(error) -> tuple[Dict[str, str], int]:
    """Handler voor 500 fouten."""
    return jsonify({
        'success': False,
        'error': 'Interne server fout'
    }), 500


if __name__ == '__main__':
    # Zorg dat de data directory bestaat
    os.makedirs('data', exist_ok=True)
    
    # Controleer of database geïnitialiseerd is
    if not os.path.exists(DATABASE_PATH):
        print(
            "WAARSCHUWING: Database niet gevonden.\n"
            "Voer 'python init_database.py' uit om de database te initialiseren.",
            file=sys.stderr
        )
    
    # Controleer of CSV bestaat
    if not os.path.exists(CSV_PATH):
        print(
            "WAARSCHUWING: CSV bestand niet gevonden.",
            file=sys.stderr
        )
    
    # Start de applicatie
    app.run(debug=True, port=5000, host='127.0.0.1')
