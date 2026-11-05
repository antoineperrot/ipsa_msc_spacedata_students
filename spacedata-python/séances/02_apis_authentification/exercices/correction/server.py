"""Micro-API — séance 2 (APIs) — CORRECTION ENSEIGNANT.

Résolution complète des exercices 1 à 10 et des bonus A à D du README.

Lancer avec :
    fastapi dev server.py
Ou directement depuis l'IDE (bouton "Run" sur ce fichier), grâce au bloc
if __name__ == "__main__" en bas de fichier.
"""
import datetime as dt
import io
import os
import time
from collections import defaultdict
from typing import Optional

import folium
import geopandas as gpd
import pandas as pd
import uvicorn
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, Header, HTTPException, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from pydantic import BaseModel
from shapely.geometry import Point

load_dotenv()

API_KEY = os.getenv("MICRO_API_KEY", "cle-secrete-tp2")

app = FastAPI(title="Micro-API Séance 2 — correction")

villes = pd.DataFrame([
    {"nom": "Paris", "latitude": 48.8566, "longitude": 2.3522, "population": 2145000, "region": "Île-de-France"},
    {"nom": "Lyon", "latitude": 45.7640, "longitude": 4.8357, "population": 522000, "region": "Auvergne-Rhône-Alpes"},
    {"nom": "Marseille", "latitude": 43.2965, "longitude": 5.3698, "population": 870000, "region": "Provence-Alpes-Côte d'Azur"},
])


class Ville(BaseModel):
    """Une ville du DataFrame, avec ses coordonnées et sa population."""
    nom: str
    latitude: float
    longitude: float
    population: int
    region: str


def verifier_cle(authorization: Optional[str] = Header(default=None)):
    """Vérifie que le header Authorization contient la bonne clé API."""
    if authorization != API_KEY:
        raise HTTPException(status_code=401, detail="Clé API manquante ou incorrecte")


def position_ville(nom: str) -> Point:
    """Retourne la position (longitude, latitude) d'une ville du DataFrame, en EPSG:4326."""
    ligne = villes.loc[villes["nom"] == nom]
    if ligne.empty:
        raise HTTPException(status_code=404, detail=f"Ville '{nom}' introuvable")
    row = ligne.iloc[0]
    return Point(row["longitude"], row["latitude"])


def distance_metres(point_a: Point, point_b: Point) -> float:
    """Distance en mètres entre deux points GPS (EPSG:4326), via le CRS métrique
    français Lambert-93 (EPSG:2154) vu en séance 1.
    """
    points = gpd.GeoSeries([point_a, point_b], crs="EPSG:4326").to_crs("EPSG:2154")
    return points.iloc[0].distance(points.iloc[1])


@app.get("/", tags=["accueil"])
def accueil():
    """Point d'entrée de la micro-API."""
    return {"message": "Micro-API prête (correction)."}


@app.post("/page", response_class=HTMLResponse, tags=["demo"])
def page_html(contenu: dict):
    """Exemple fourni : construit une page HTML lisible à partir d'un JSON reçu dans le corps
    de la requête.
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


# --- Exercice 1 : lister les villes ---

@app.get("/villes", response_model=list[Ville], tags=["villes"])
def lister_villes():
    """Retourne toutes les villes du DataFrame."""
    return villes.to_dict(orient="records")


# --- Exercice 2 : télécharger le DataFrame (CSV / Parquet) ---

@app.get("/villes/csv", tags=["villes"])
def telecharger_villes_csv():
    """Télécharge le DataFrame villes au format CSV."""
    buffer = io.StringIO()
    villes.to_csv(buffer, index=False)
    return StreamingResponse(
        iter([buffer.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=villes.csv"},
    )


@app.get("/villes/parquet", tags=["villes"])
def telecharger_villes_parquet():
    """Télécharge le DataFrame villes au format Parquet."""
    buffer = io.BytesIO()
    villes.to_parquet(buffer, index=False)
    buffer.seek(0)
    return StreamingResponse(
        buffer,
        media_type="application/octet-stream",
        headers={"Content-Disposition": "attachment; filename=villes.parquet"},
    )


# --- Exercice 3 : ajouter une ville ---

@app.post("/villes", status_code=201, tags=["villes"], dependencies=[Depends(verifier_cle)])
def ajouter_ville(ville: dict):
    """Ajoute une ville au DataFrame. Renvoie 409 si une ville du même nom existe déjà."""
    global villes
    if ville.get("nom") in villes["nom"].values:
        raise HTTPException(status_code=409, detail=f"La ville '{ville.get('nom')}' existe déjà")
    villes = pd.concat([villes, pd.DataFrame([ville])], ignore_index=True)
    return ville


# --- Exercice 4 : modifier une ville ---

@app.put("/villes/{nom}", tags=["villes"], dependencies=[Depends(verifier_cle)])
def modifier_ville(nom: str, mise_a_jour: dict):
    """Met à jour les champs fournis pour la ville `nom`. Renvoie 404 si elle n'existe pas."""
    if nom not in villes["nom"].values:
        raise HTTPException(status_code=404, detail=f"Ville '{nom}' introuvable")
    index = villes.index[villes["nom"] == nom][0]
    for cle, valeur in mise_a_jour.items():
        if cle in villes.columns:
            villes.at[index, cle] = valeur
    return villes.loc[index].to_dict()


# --- Exercice 5 : supprimer une ville ---

@app.delete("/villes/{nom}", tags=["villes"], dependencies=[Depends(verifier_cle)])
def supprimer_ville(nom: str):
    """Supprime la ville `nom` du DataFrame. Renvoie 404 si elle n'existe pas."""
    global villes
    if nom not in villes["nom"].values:
        raise HTTPException(status_code=404, detail=f"Ville '{nom}' introuvable")
    villes = villes[villes["nom"] != nom].reset_index(drop=True)
    return {"message": f"Ville '{nom}' supprimée"}


# --- Exercice 6 : distance entre deux villes (EPSG:2154) ---

@app.post("/villes/distance", tags=["villes"])
def calculer_distance(payload: dict):
    """Calcule la distance en mètres entre deux villes du DataFrame (clés "ville 1"/"ville 2")."""
    nom_a, nom_b = payload.get("ville 1"), payload.get("ville 2")
    distance = distance_metres(position_ville(nom_a), position_ville(nom_b))
    return {"ville 1": nom_a, "ville 2": nom_b, "distance_metres": round(distance, 1)}


# --- Exercice 7 : carte interactive HTML ---

@app.get("/villes/carte", response_class=HTMLResponse, tags=["villes"])
def carte_villes():
    """Retourne une carte interactive (folium) de toutes les villes du DataFrame."""
    centre = [villes["latitude"].mean(), villes["longitude"].mean()]
    carte = folium.Map(location=centre, zoom_start=5)
    for _, ville in villes.iterrows():
        folium.Marker(
            location=[ville["latitude"], ville["longitude"]],
            popup=f"{ville['nom']} ({ville['population']} hab.)",
        ).add_to(carte)
    return carte._repr_html_()


# --- Exercice 8 : simuler un timeout ---

@app.get("/attente", tags=["demo"])
def attendre(delai: float = 5.0):
    """Attend `delai` secondes avant de répondre — pour tester un timeout côté client."""
    time.sleep(delai)
    return {"message": f"Réponse après {delai} secondes"}


# --- Bonus A : filtrer la liste des villes ---

@app.get("/villes/recherche", tags=["bonus"])
def rechercher_villes(region: Optional[str] = None, population_min: Optional[int] = None):
    """Filtre les villes par région et/ou population minimale (query params optionnels)."""
    resultat = villes
    if region is not None:
        resultat = resultat[resultat["region"] == region]
    if population_min is not None:
        resultat = resultat[resultat["population"] >= population_min]
    return resultat.to_dict(orient="records")


# --- Bonus B : ville la plus proche de la position de l'utilisateur ---

@app.get("/villes/plus-proche", tags=["bonus"])
def ville_plus_proche(latitude: float, longitude: float):
    """Retourne la ville du DataFrame la plus proche de la position (latitude, longitude) fournie."""
    point_utilisateur = Point(longitude, latitude)
    distances = villes.apply(
        lambda ville: distance_metres(point_utilisateur, Point(ville["longitude"], ville["latitude"])),
        axis=1,
    )
    index_plus_proche = distances.idxmin()
    resultat = villes.loc[index_plus_proche].to_dict()
    resultat["distance_metres"] = round(distances.loc[index_plus_proche], 1)
    return resultat


# --- Bonus C : garder une trace des requêtes (middleware) ---

logs: list[dict] = []


@app.middleware("http")
async def journaliser_requetes(request: Request, call_next):
    """Enregistre chaque requête reçue (méthode, route, horodatage) en mémoire."""
    reponse = await call_next(request)
    logs.append({
        "methode": request.method,
        "route": request.url.path,
        "horodatage": dt.datetime.now().isoformat(timespec="seconds"),
    })
    return reponse


@app.get("/logs", tags=["bonus"])
def consulter_logs():
    """Liste les requêtes reçues par l'API depuis son démarrage."""
    return logs


# --- Bonus D : rate limiting (60 requêtes/minute par utilisateur) ---

LIMITE_REQUETES_PAR_MINUTE = 60
historique_requetes: dict[str, list[float]] = defaultdict(list)


def limiter_debit(authorization: Optional[str] = Header(default=None)):
    """Dépendance qui bloque un utilisateur au-delà de 60 requêtes par minute."""
    identifiant = authorization or "anonyme"
    maintenant = time.time()
    historique = historique_requetes[identifiant]
    historique[:] = [instant for instant in historique if maintenant - instant < 60]
    if len(historique) >= LIMITE_REQUETES_PAR_MINUTE:
        raise HTTPException(status_code=429, detail="Trop de requêtes, réessayez plus tard")
    historique.append(maintenant)


@app.get("/ping", tags=["bonus"], dependencies=[Depends(limiter_debit)])
def ping():
    """Route de démonstration pour le rate limiting (bonus D) : limitée à 60 appels/minute."""
    return {"message": "pong"}


if __name__ == "__main__":
    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=True)
