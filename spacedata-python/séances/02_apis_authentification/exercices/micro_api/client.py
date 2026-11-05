"""Client de test pour la micro-API — séance 2.

Lance d'abord le serveur dans un terminal :
    fastapi dev server.py
Puis, dans un autre terminal :
    python client.py
"""
import requests

from tools.qcm_app.quiz_sessions import responses_dir

BASE_URL = "http://127.0.0.1:8000"


def demo_page_html():
    """Exemple fourni : appelle la route /page avec un JSON, et affiche le HTML généré."""
    reponse = requests.post(
        f"{BASE_URL}/page",
        json={"titre": "Ma page", "texte": "Construite depuis un f-string côté serveur."},
    )
    print(f"Statut : {reponse.status_code}")
    print(reponse.text)


def main():
    reponse = requests.get(BASE_URL)
    print(f"Statut : {reponse.status_code}")
    print(reponse.json())

    demo_page_html()

    print("Exercice 1")
    reponse = requests.get(f"{BASE_URL}/villes")
    villes_dict = reponse.json()
    print(villes_dict)

    print("Exercice 3")

    new_ville = {"nom": "Toulouse", "latitude": 40, "longitude": 2.35, "population": 1_500_000, "region": "Occitanie"}
    response = requests.post(f"{BASE_URL}/villes", json=new_ville)
    print(f"Statut : {response.status_code}")
    villes_dict = requests.get(f"{BASE_URL}/villes").json()
    print(villes_dict)

    #print("Exercice 4")


if __name__ == "__main__":
    main()
