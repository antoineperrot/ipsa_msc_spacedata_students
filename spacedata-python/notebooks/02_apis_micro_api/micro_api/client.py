"""Client de test pour la micro-API — séance 2.

Lance d'abord le serveur dans un terminal :
    fastapi dev server.py
Puis, dans un autre terminal :
    python client.py
"""
import requests

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


if __name__ == "__main__":
    main()
