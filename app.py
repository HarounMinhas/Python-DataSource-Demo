"""Main Application

Dit bestand bevat de Flask webapplicatie die de gebruikersinterface biedt
voor het ophalen van productgegevens uit verschillende databronnen.

Flask werd gekozen omdat het eenvoudig en lichtgewicht is, ideaal voor
demo-doeleinden.
"""

from flask import Flask, render_template, request, jsonify
from data_sources.database_source import DatabaseSource
from data_sources.csv_source import CSVSource
from models.product import Product
import os

app = Flask(__name__)

# Configuratie
DATABASE_PATH = 'data/products.db'
CSV_PATH = 'data/products.csv'


@app.route('/')
def index():
    """Render de hoofdpagina met de gebruikersinterface."""
    return render_template('index.html')


@app.route('/api/products', methods=['GET'])
def get_products():
    """
    API endpoint voor het ophalen van producten.
    
    Query parameters:
        source (str): 'database' of 'csv' - kiest de databron
    
    Returns:
        JSON response met lijst van producten
    """
    source_type = request.args.get('source', 'database')
    
    try:
        # Factory Pattern: selecteer de juiste databron gebaseerd op input
        if source_type == 'csv':
            data_source = CSVSource(CSV_PATH)
        else:
            data_source = DatabaseSource(DATABASE_PATH)
        
        # Haal producten op via de gekozen bron
        products = data_source.get_all_products()
        
        # Converteer Product objecten naar dictionaries voor JSON
        products_data = [product.to_dict() for product in products]
        
        return jsonify({
            'success': True,
            'source': source_type,
            'products': products_data
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


if __name__ == '__main__':
    # Zorg dat de data directory bestaat
    os.makedirs('data', exist_ok=True)
    
    # Start de applicatie
    app.run(debug=True, port=5000)
