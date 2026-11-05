"""Client de démonstration pour la micro-API — séance 2 — CORRECTION ENSEIGNANT.

Exerce successivement chaque route codée dans server.py (exercices 1 à 10, bonus A à D).

Lance d'abord le serveur dans un terminal :
    fastapi dev server.py
Puis, dans un autre terminal :
    python client.py
"""
import os
from pathlib import Path

import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "http://127.0.0.1:8000"
API_KEY = os.getenv("MICRO_API_KEY", "cle-secrete-tp2")
HEADERS = {"Authorization": API_KEY}


def demo_page_html():
    reponse = requests.post(
        f"{BASE_URL}/page",
        json={"titre": "Ma page", "texte": "Construite depuis un f-string côté serveur."},
    )
    print(f"[page] {reponse.status_code}")


def demo_lister_villes():
    reponse = requests.get(f"{BASE_URL}/villes")
    print(f"[1. lister] {reponse.status_code}")
    print(pd.DataFrame(reponse.json()))


def demo_telecharger_dataframe():
    reponse_csv = requests.get(f"{BASE_URL}/villes/csv")
    Path("villes.csv").write_bytes(reponse_csv.content)
    print(f"[2.1 csv] {reponse_csv.status_code}, relu : {len(pd.read_csv('villes.csv'))} lignes")

    reponse_parquet = requests.get(f"{BASE_URL}/villes/parquet")
    Path("villes.parquet").write_bytes(reponse_parquet.content)
    print(f"[2.2 parquet] {reponse_parquet.status_code}, relu : {len(pd.read_parquet('villes.parquet'))} lignes")


def demo_ajouter_ville():
    nouvelle_ville = {
        "nom": "Rennes", "latitude": 48.1173, "longitude": -1.6778,
        "population": 220000, "region": "Bretagne",
    }
    reponse = requests.post(f"{BASE_URL}/villes", headers=HEADERS, json=nouvelle_ville)
    print(f"[3. ajouter] {reponse.status_code} {reponse.json()}")

    # Doublon : doit échouer avec un code d'erreur pertinent (409)
    reponse_doublon = requests.post(f"{BASE_URL}/villes", headers=HEADERS, json=nouvelle_ville)
    print(f"[3. doublon] {reponse_doublon.status_code} {reponse_doublon.json()}")


def demo_modifier_ville():
    reponse = requests.put(f"{BASE_URL}/villes/Rennes", headers=HEADERS, json={"population": 225000})
    print(f"[4. modifier] {reponse.status_code} {reponse.json()}")

    reponse_absente = requests.put(f"{BASE_URL}/villes/Inconnue", headers=HEADERS, json={"population": 1})
    print(f"[4. absente] {reponse_absente.status_code} {reponse_absente.json()}")


def demo_supprimer_ville():
    reponse = requests.delete(f"{BASE_URL}/villes/Rennes", headers=HEADERS)
    print(f"[5. supprimer] {reponse.status_code} {reponse.json()}")

    reponse_absente = requests.delete(f"{BASE_URL}/villes/Rennes", headers=HEADERS)
    print(f"[5. absente] {reponse_absente.status_code} {reponse_absente.json()}")


def demo_distance():
    reponse = requests.post(f"{BASE_URL}/villes/distance", json={"ville 1": "Paris", "ville 2": "Lyon"})
    print(f"[6. distance] {reponse.status_code} {reponse.json()}")


def demo_carte():
    reponse = requests.get(f"{BASE_URL}/villes/carte")
    Path("carte_villes.html").write_text(reponse.text, encoding="utf-8")
    print(f"[7. carte] {reponse.status_code}, enregistrée dans carte_villes.html")


def demo_timeout():
    try:
        requests.get(f"{BASE_URL}/attente", params={"delai": 3}, timeout=1)
        print("[8. timeout] pas de timeout levé (inattendu)")
    except requests.exceptions.Timeout:
        print("[8. timeout] Timeout levé comme attendu")


def demo_recherche():
    reponse = requests.get(f"{BASE_URL}/villes/recherche", params={"region": "Île-de-France"})
    print(f"[A. recherche] {reponse.status_code} {reponse.json()}")


def demo_plus_proche():
    reponse = requests.get(f"{BASE_URL}/villes/plus-proche", params={"latitude": 48.85, "longitude": 2.35})
    print(f"[B. plus proche] {reponse.status_code} {reponse.json()}")


def demo_logs():
    reponse = requests.get(f"{BASE_URL}/logs")
    print(f"[C. logs] {reponse.status_code}, {len(reponse.json())} requêtes enregistrées")


def demo_rate_limiting():
    dernier_statut = None
    for i in range(1, 62):
        reponse = requests.get(f"{BASE_URL}/ping")
        dernier_statut = reponse.status_code
        if i in (59, 60, 61):
            print(f"[D. rate limiting] requête {i} -> {reponse.status_code}")
    assert dernier_statut == 429, "La 61e requête devrait être rejetée (429)"


def main():
    demo_page_html()
    demo_lister_villes()
    demo_telecharger_dataframe()
    demo_ajouter_ville()
    demo_modifier_ville()
    demo_supprimer_ville()
    demo_distance()
    demo_carte()
    demo_timeout()
    demo_recherche()
    demo_plus_proche()
    demo_rate_limiting()
    demo_logs()


if __name__ == "__main__":
    main()
