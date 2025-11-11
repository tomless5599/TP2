# Extracteur de données ergonomiques

Ce projet ajoute un script en ligne de commande permettant d'extraire rapidement
les données importantes associées aux méthodes **Garg**, **Kodak** et **RSST**
depuis des documents PDF ou des images scannées. Les valeurs détectées sont
mises en tableau (CSV) ou dans un fichier JSON afin de faciliter les analyses
statistiques ultérieures.

## Installation

Créez un environnement virtuel puis installez les dépendances optionnelles selon
les formats que vous souhaitez traiter :

```bash
python -m venv .venv
source .venv/bin/activate
pip install pdfplumber pillow pytesseract
```

> ℹ️ Pour l'OCR des images il est également nécessaire d'installer le moteur
> [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) sur votre système.

## Utilisation

```bash
python -m ergodata.extractor <fichier> --output resultats.csv
```

Options principales :

- `--format {csv,json}` : format de sortie (par défaut `csv`).
- `--merge` : fusionner les résultats de plusieurs fichiers dans un seul bloc
  par méthode.

Exemples :

```bash
# Analyse un rapport PDF et produit un tableau CSV
python -m ergodata.extractor rapport.pdf --output donnees.csv

# Analyse plusieurs images et retourne un JSON fusionné
python -m ergodata.extractor page1.png page2.png --merge --format json --output donnees.json
```

Le fichier de sortie contient les valeurs retrouvées ainsi que les extraits de
texte correspondants lorsqu'on utilise le format JSON.

## Limitations

- Les expressions régulières sont basées sur la terminologie française utilisée
  par les méthodes Garg, Kodak et RSST. Des documents rédigés différemment
  peuvent nécessiter des ajustements.
- Les performances de l'OCR dépendent de la qualité des images et de la
  configuration de Tesseract.
