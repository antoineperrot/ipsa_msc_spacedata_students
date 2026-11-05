# Séance 2 — APIs & micro-API

## Avant de commencer : pourquoi pas de notebook aujourd'hui ?

Un notebook Jupyter est pratique pour explorer des données pas à pas, mais il n'est **pas adapté pour faire tourner un serveur** : une API doit s'exécuter en continu, en tâche de fond, indépendamment de toute cellule qu'on exécute. Aujourd'hui, vous allez donc construire votre API dans un **fichier `.py` classique** et la lancer depuis un terminal.

## Mise en place

- Dans `micro_api/`, vous trouverez un `server.py` et un `client.py` de base. `server.py` contient déjà :
  - un `DataFrame` `villes` (colonnes `nom`, `latitude`, `longitude`, `population`, `region`) ;
  - une fonction `verifier_cle` pour protéger une route par clé API (header `Authorization`) ;
  - une route `/page` déjà fonctionnelle, qui génère une page HTML lisible à partir d'un JSON — vous pouvez vous en inspirer pour toutes les routes qui doivent renvoyer du HTML.
- Lancez le serveur dans un terminal et laissez-le tourner :
  ```bash
  cd micro_api
  fastapi dev server.py
  ```
  Le rechargement automatique à chaque sauvegarde de `server.py` est inclus.
- Dans un second terminal, utilisez `client.py` (ou tout autre script, ou une console Python) pour interroger l'API au fur et à mesure que vous ajoutez des routes.

## Exercices

Complétez `server.py` et `client.py` au fur et à mesure. L'idée est de construire une vraie petite application au fil des exercices, en réutilisant à chaque fois ce que vous avez déjà codé.

### 1. Lister les villes
Ajoutez une route `GET /villes` qui retourne le `DataFrame` `villes` en JSON. Côté client, appelez cette route et reconvertissez la réponse en `pandas.DataFrame`.

### 2. Télécharger le DataFrame
2.1. Ajoutez une route `GET` qui permet de télécharger le `DataFrame` `villes` au format **CSV**.
2.2. Ajoutez une route `GET` qui permet de le télécharger au format **Parquet**.

Dans les deux cas, regardez du côté de `fastapi.responses.FileResponse` (ou `StreamingResponse`). Vérifiez côté client que le fichier téléchargé se recharge correctement avec `pandas`.

### 3. Ajouter une ville
Ajoutez une route `POST /villes` qui prend en argument un dictionnaire JSON (une ville) et l'ajoute au `DataFrame` si elle n'existe pas déjà. Si une ville du même nom existe déjà, renvoyez un code d'erreur pertinent plutôt que de l'ajouter en double. Cette route nécessite une authentification par clé API.

### 4. Modifier une ville
Ajoutez une route `PUT /villes/{nom}` qui met à jour une ville existante (population, region...). Si la ville n'existe pas, renvoyez un code d'erreur pertinent. Cette route nécessite une authentification par clé API.

### 5. Supprimer une ville
Ajoutez une route `DELETE` qui supprime une ville du `DataFrame` à partir de son nom. Si la ville n'existe pas, la route doit renvoyer un code de statut différent de `200`, cohérent avec la situation. Cette route nécessite elle aussi une authentification par clé API.

### 6. Distance entre deux villes
Ajoutez une route qui prend en argument un JSON avec les clés `"ville 1"` et `"ville 2"`, et calcule la distance entre ces deux villes du `DataFrame`. Pour un calcul de distance correct en mètres, reprojetez les coordonnées dans le CRS métrique français vu en séance 1 (**Lambert-93, EPSG:2154**) avant de calculer la distance — ne calculez pas directement sur des degrés GPS. Vérifiez le bon fonctionnement de votre route en ajoutant deux villes que vous connaissez bien et en comparant la distance obtenue à la réalité.

### 7. Carte interactive des villes
Ajoutez une route `GET` qui retourne une carte interactive HTML affichant toutes les villes du `DataFrame`. Aide : exportez une carte `plotly` ou `folium` (vu en séance 1) en HTML, et renvoyez-la avec `HTMLResponse`.

### 8. Route qui simule un timeout
Ajoutez une route qui attend un délai donné avant de répondre (`time.sleep`, délai passé en paramètre de requête). Côté client, appelez cette route avec un `timeout` (paramètre `timeout=` de `requests.get`) plus court que le délai simulé, mesurez le temps écoulé, et gérez proprement l'exception levée (`requests.exceptions.Timeout`).

### 9. Exposer son API sur Internet avec ngrok
Créez un compte gratuit sur ngrok, installez l'outil, et exposez votre API locale (port 8000) sur une URL publique. Vérifiez que vous pouvez consulter votre API (par exemple `/docs`) depuis le navigateur de votre téléphone, en 4G/5G — pas en wifi sur le même réseau que votre ordinateur.

**Config ngrok (une seule fois)** : créer un compte gratuit sur
[ngrok.com](https://dashboard.ngrok.com/signup), récupérer l'authtoken sur
[dashboard.ngrok.com/get-started/your-authtoken](https://dashboard.ngrok.com/get-started/your-authtoken),
puis le mettre dans `.env`. Sans authtoken (ou sans connexion internet vers
ngrok), l'app se rabat automatiquement sur l'IP locale de la machine
(`http://<ip-locale>:5000`, accessible uniquement sur le même Wi-Fi)

### 10. Documentation automatique
Comme vu en cours, FastAPI génère automatiquement une documentation interactive à partir de votre code — vous n'avez rien à générer manuellement, seulement à la consulter et à l'améliorer :

1. Ajoutez des **docstrings** à vos fonctions de route, et des **modèles Pydantic** (avec `response_model=`) là où c'est pertinent, pour enrichir le schéma généré.
2. Lancez votre serveur, puis ouvrez `/docs` dans votre navigateur (Swagger UI) : vérifiez que toutes les routes que vous avez codées apparaissent, avec une description qui reflète ce qu'elles font.
3. Dépliez une route, cliquez sur **"Try it out"**, remplissez les champs puis **"Execute"** : vérifiez que vous obtenez bien la même réponse qu'avec `requests` côté client.
4. Jetez aussi un œil à `/redoc`, la présentation alternative en lecture seule.

## Pour aller plus loin

Si vous avez terminé les exercices 1 à 10, voici quelques pistes pour aller plus loin.

### A. Filtrer la liste des villes
Ajoutez une route `GET /villes/recherche` qui accepte des paramètres de requête optionnels (par exemple `region` et `population_min`) et ne retourne que les villes correspondantes.

### B. Trouver la ville la plus proche de l'utilisateur
Ajoutez une route qui prend en paramètres la position de l'utilisateur (latitude/longitude, par exemple en query params) et retourne la ville du `DataFrame` la plus proche de cette position. Réutilisez le calcul de distance en EPSG:2154 de l'exercice 6.

### C. Garder une trace des requêtes
Ajoutez une route `GET /logs` qui liste les requêtes reçues par votre API (méthode, route, horodatage), stockées en mémoire. Aide : un décorateur (ou un middleware FastAPI) qui enregistre chaque appel avant de l'exécuter, comme vu en cours.

### D. Rate limiting
Ajoutez une limite de débit à votre API : un même utilisateur ne doit pas pouvoir faire plus de 60 requêtes par minute sur une route donnée. Au-delà, l'API doit répondre avec un code `429` (Too Many Requests). Écrivez un script côté client qui démontre que ça fonctionne : 59 requêtes en une minute doivent toutes réussir, 61 requêtes doivent voir au moins un échec.
