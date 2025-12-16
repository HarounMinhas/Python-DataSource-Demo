# Product Afbeeldingen

Deze directory bevat product afbeeldingen voor de demo applicatie.

## Placeholder

Het bestand `placeholder.svg` wordt gebruikt als fallback wanneer een product afbeelding niet gevonden wordt.

## Product Afbeeldingen Toevoegen

Om echte product afbeeldingen toe te voegen:

1. Plaats PNG of JPG bestanden in deze directory
2. Gebruik exacte bestandsnamen zoals opgegeven in de database/CSV:
   - laptop.png
   - mouse.png
   - keyboard.png
   - monitor.png
   - usb-hub.png

3. Aanbevolen specificaties:
   - Formaat: PNG of JPG
   - Afmetingen: 400x400 pixels of groter
   - Transparante achtergrond (PNG) voor beste resultaat
   - Bestandsgrootte: max 500KB per afbeelding

## Waarom SVG?

De placeholder is een SVG bestand omdat:
- Het geen binaire data is (kan in Git worden opgeslagen)
- Het schaalt perfect naar elke grootte
- Kleine bestandsgrootte
- Bewerkbaar als tekstbestand

## Productie Gebruik

In een productie omgeving zou je:
- Afbeeldingen opslaan in een CDN of object storage (AWS S3, Azure Blob, etc.)
- Image optimization tools gebruiken
- Verschillende formaten genereren (webp, avif) voor betere performance
- Lazy loading implementeren
- Responsive images gebruiken met srcset
