"""Micro-API de démonstration — séance 2 (APIs).

Lancer avec :
    fastapi dev server.py
Ou directement depuis l'IDE (bouton "Run" sur ce fichier), grâce au bloc
if __name__ == "__main__" en bas de fichier.
"""
import os
from typing import Optional

import pandas as pd
import uvicorn
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.responses import HTMLResponse

load_dotenv()

API_KEY = os.getenv("MICRO_API_KEY", "cle-secrete-tp2")

app = FastAPI(title="Micro-API Séance 2")

villes = pd.DataFrame([
    {"nom": "Paris", "latitude": 48.8566, "longitude": 2.3522, "population": 2145000, "region": "Île-de-France"},
    {"nom": "Lyon", "latitude": 45.7640, "longitude": 4.8357, "population": 522000, "region": "Auvergne-Rhône-Alpes"},
    {"nom": "Marseille", "latitude": 43.2965, "longitude": 5.3698, "population": 870000, "region": "Provence-Alpes-Côte d'Azur"},
])


def verifier_cle(authorization: Optional[str] = Header(default=None)):
    """Vérifie que le header Authorization contient la bonne clé API."""
    if authorization != API_KEY:
        raise HTTPException(status_code=401, detail="Clé API manquante ou incorrecte")


@app.get("/")
def accueil():
    return {"message": "Micro-API prête. Complétez les routes ci-dessous."}


@app.post("/page", response_class=HTMLResponse)
def page_html(contenu: dict):
    """Exemple fourni : construit une page HTML lisible à partir d'un JSON reçu dans le corps
    de la requête. Réutilisez ce modèle pour les routes qui doivent renvoyer du HTML (carte, etc.).
    """
    titre = contenu.get("titre", "Sans titre")
    texte = contenu.get("texte", "")
    return f"""
    <html>
      <head><title>{titre}</title></head>
      <body>
        <h1>{titre}</h1>
        <p>{texte}</p>
      </body>
    </html>
    """


# TODO Exercice 1 : route GET /villes qui retourne le DataFrame villes en JSON

# TODO Exercice 2 : routes GET qui téléchargent le DataFrame villes en CSV, puis en Parquet

# TODO Exercice 3 : route POST /villes qui ajoute une ville (auth requise, erreur si déjà présente)

# TODO Exercice 4 : route PUT /villes/{nom} qui modifie une ville (auth requise, erreur si absente)

# TODO Exercice 5 : route DELETE qui supprime une ville (auth requise, erreur si absente)

# TODO Exercice 6 : route qui calcule la distance entre deux villes (CRS EPSG:2154)

# TODO Exercice 7 : route GET qui retourne une carte interactive HTML des villes

# TODO Exercice 8 : route GET qui simule un timeout


# --- Pour aller plus loin (bonus) ---

# TODO Bonus A : route GET /villes/recherche avec filtres en query params (region, population_min...)

# TODO Bonus B : route qui trouve la ville la plus proche de la position de l'utilisateur

# TODO Bonus C : route GET /logs qui liste les requêtes reçues (méthode, route, horodatage)

# TODO Bonus D : rate limiting (max 60 requêtes/minute par utilisateur)


if __name__ == "__main__":
    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=True)
