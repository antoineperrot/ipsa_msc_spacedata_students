# État des lieux — ce que les élèves ont vu et pratiqué (séances 1 & 2)

Document de préparation de la séance 3 (DuckDB & SQL analytique). Objectif : s'appuyer sur des notions déjà installées plutôt que les redémontrer, et repérer les briques qui manquent encore pour enchaîner naturellement sur SQL / DuckDB.

## Séance 1 — Pipeline data, pandas & formats de géodonnées

**Cours (slides `01_pipeline_pandas_formats.html`) + TP (`exercices/exercice.ipynb`, 2h30, 2 parties).**

### Notions installées
- **Pipeline data** en 4 étapes : collecte → validation → transformation → exploitation (vocabulaire réutilisé à chaque séance).
- **pandas — bases** : `Series` vs `DataFrame`, lecture de la doc (`help()`, `?`, Shift+Tab).
- **Index** : `.loc` (étiquette) vs `.iloc` (position), `set_index()` / `reset_index()` — y compris `reset_index()` après un `groupby` à plusieurs clés (MultiIndex → colonnes).
- **Exploration** : `head()`, `info()`, `describe()`.
- **Filtrage** multi-critères (`&`, `|`, `~`, parenthésage obligatoire), **tri** multi-colonnes (`sort_values(by=[...], ascending=[...])`).
- **Colonnes dérivées / filtres personnalisés** : `apply(lambda ...)` vs version vectorisée (`.str.*`) — avec la mise en garde performance.
- **`groupby`** : une ou plusieurs clés, agrégations multiples (`agg(["mean","max","min"])`), agrégations nommées (`agg(nom=("col","fonc"))`), fonction d'agrégation personnalisée.
- **Valeurs manquantes** : `isna().sum()`, `dropna()`, `fillna()` ; piège de `value_counts()` qui ignore les `NaN` par défaut (`dropna=False`).
- **Jointures `pd.merge`** : les 4 types (`inner`/`left`/`right`/`outer`), explicitement présentés comme l'équivalent pandas d'un **JOIN SQL** — pont direct déjà posé vers la séance 3.
- **Formats de géodonnées** : CSV, JSON, GeoJSON, Parquet — structure, poids, cas d'usage, et surtout **fidélité des types à la relecture** (CSV/JSON perdent le typage, GeoJSON/Parquet le préservent). Parquet déjà présenté comme binaire/colonnaire/compressé, pensé pour l'analytique — notion clé pour DuckDB.
- **CRS** : EPSG:4326 (stocker/partager, degrés) vs EPSG:2154 Lambert-93 (calculer en France, mètres) vs EPSG:3857 (afficher sur le web) ; reprojection avec `.to_crs()` avant tout calcul de distance.
- **Visualisation** : `.plot()` pandas (rapide, non diffusable), Plotly (`px.bar`, `scatter_geo` — interactif), folium (cartes Leaflet, export HTML).

### Pratiqué en TP
- Jeu de 30 villes françaises construit en Python (partie guidée) : filtrage, tri, `groupby` multi-clés, valeurs manquantes, jointure avec un second jeu (superficie des régions) pour calculer une densité.
- Partie autonome (60 villes) : chargement de **4 sources de formats différents** (GeoJSON, CSV, JSON, Parquet), nettoyage propre à chaque source, **fusion des 4 sur la clé `ville`**, création d'une colonne dérivée (quadrant géographique) via fonction personnalisée, agrégations multi-indicateurs par groupe, exploration avec `.plot()`, cartes Plotly et folium exportées en HTML.

### Ce qui n'a *pas* encore été vu
- Aucun SQL, aucune notion de base de données / moteur de requêtes.
- Pas de notion de performance sur gros volumes (le TP reste sur 30-60 lignes) : la justification "Parquet = analytique, gros volumes" est posée en cours mais jamais démontrée en pratique — angle naturel pour l'intro de séance 3 (DuckDB interrogeant du Parquet).

## Séance 2 — APIs & authentification

**Cours (slides `02_apis_authentification.html`) + TP (`exercices/README.md`, pas de notebook — fichiers `.py` + serveur FastAPI en tâche de fond).**

### Notions installées
- **Modèle client-serveur / HTTP** : requête-réponse, anatomie d'une URL (schéma, host, port, path), rôle du DNS, anatomie d'une requête HTTP (méthode, headers, body).
- **`requests`** : `timeout=` (+ tuple connexion/lecture), gestion `try/except` (`Timeout`, `RequestException`) — motif réutilisé en séance 4.
- **Verbes HTTP** : GET/POST/PUT/DELETE, avec body ou non, en code (`requests.get/post/put/delete`).
- **Codes de statut** : familles 2xx/4xx/5xx, réflexe de toujours vérifier le code avant d'exploiter une réponse.
- **Authentification** : clé API (header `Authorization`) pratiquée en TP ; token bearer et OAuth2 vus en **théorie seulement**, pratique reportée en séance 4 (Copernicus/NASA).
- **Bonne pratique sécurité** : jamais de clé en dur dans le code, usage de `.env` + `python-dotenv`.
- **Vocabulaire REST** : ressource, endpoint, rate limiting (concept introduit, implémentation en bonus D du TP).
- **Construire sa propre API avec FastAPI** : décorateurs (`@app.get`, `@app.post`...), notion générale de décorateur Python (fonction qui en enveloppe une autre), dépendances (`Depends()`) pour factoriser la vérification de clé API.
- **Documentation OpenAPI/Swagger** : génération automatique par FastAPI à partir des docstrings, type hints et modèles Pydantic ; `/docs` (Swagger UI, "Try it out") et `/redoc`.

### Pratiqué en TP (micro-API FastAPI construite de zéro, `server.py` + `client.py`)
- Route `GET /villes` (DataFrame → JSON) et reconversion côté client.
- Téléchargement du DataFrame en **CSV** et **Parquet** (`StreamingResponse`/`FileResponse`) — première manipulation concrète de fichiers Parquet générés par du code applicatif (pas juste lus depuis un fichier fourni).
- `POST`/`PUT`/`DELETE /villes` avec authentification par clé API et gestion d'erreurs (409 doublon, 404 absence).
- Calcul de **distance entre deux villes en EPSG:2154** (réutilisation directe du CRS de la séance 1, via `geopandas`/`shapely`).
- Carte interactive HTML (folium) exposée par une route GET.
- Route simulant un timeout + gestion client correspondante.
- Exposition de l'API sur Internet via **ngrok** (bonus, notion réseau).
- Enrichissement de la documentation OpenAPI (docstrings, `response_model`, Pydantic).
- Bonus (selon avancement) : recherche filtrée par query params, ville la plus proche, logs en mémoire (middleware), rate limiting (429).

### Ce qui n'a *pas* encore été vu
- Aucun SQL ni requête structurée sur les données récupérées via API — les données sont manipulées en pandas pur (filtrage, agrégation déjà vus séance 1), jamais interrogées en SQL.
- Pas encore d'API publique réelle interrogée (USGS annoncé en fin de séance 2 pour clôturer le TP, mais pas détaillé dans les slides fournies) — à confirmer selon ce qui a effectivement été fait en salle.
- Pas de notion de moteur de requêtes colonne, de plan d'exécution, ni de jointure/agrégation en SQL.

## Points d'appui directs pour la séance 3 (DuckDB & SQL)

- **`pd.merge` ↔ `JOIN` SQL** : le pont est déjà posé explicitement dans les slides de la séance 1 ("l'équivalent pandas d'un JOIN SQL, qu'on retrouvera en séance 3 avec DuckDB"). La séance 3 peut directement réutiliser le vocabulaire `inner/left/right/outer` sans le redéfinir.
- **Parquet** : déjà manipulé en lecture (séance 1, 4 formats) et en écriture (séance 2, téléchargement). La séance 3 peut capitaliser dessus pour illustrer DuckDB interrogeant directement des fichiers Parquet, et faire le lien "colonnaire ⇒ requêtes analytiques rapides" annoncé mais jamais démontré.
- **`groupby`/`agg` pandas ↔ `GROUP BY` SQL** : les élèves ont déjà manipulé agrégations multiples et nommées ; bon point de comparaison direct avec `SELECT ... GROUP BY` en SQL.
- **Valeurs manquantes / filtrage** : déjà maîtrisés côté pandas (`WHERE` SQL s'enseignera comme équivalent du filtrage booléen déjà pratiqué).
- **Jeu de données villes françaises** : réutilisé en filigrane depuis la séance 1 (30 puis 60 villes) et en séance 2 (micro-API) — candidat naturel pour continuer avec les mêmes données en SQL plutôt que d'en introduire un nouveau.
- **Lacune à combler en séance 3** : aucune notion de SQL pur n'a été vue (`SELECT`, `WHERE`, `GROUP BY`, `JOIN` en syntaxe SQL) — tout le vocabulaire conceptuel existe déjà côté pandas, mais la syntaxe SQL elle-même sera entièrement nouvelle.
- **Lacune à combler en séance 3** : aucune démonstration de performance sur gros volumes n'a encore été faite ; c'est un argument de vente naturel pour DuckDB (requêtes rapides sur Parquet/CSV volumineux) qui n'a pas encore de preuve concrète dans le module.

## Structure retenue pour la séance 3 (3h)

La séance a été scindée en deux parties inégales, pour rendre la partie exercice plus concrète qu'une simple reprise du jeu de villes :

- **Partie 1 (~30-40 min, reprise quasi à l'identique de l'ancienne version)** : prise en main de `duckdb.sql(...)` sur un `DataFrame`, lecture d'un Parquet sans chargement mémoire, jointure CSV, comparaison de temps pandas/DuckDB, 3 requêtes à trous. Sert de pont syntaxique SQL avant le projet.
- **Partie 2 (~2h-2h20 + bonus) — projet « indice de qualité de l'air »** : une base `data/qualite_air.duckdb` (4 réseaux de capteurs synthétiques mais réalistes, générés par `generation_base_donnees.ipynb` à partir du même jeu de 30 villes que la séance 1) sert de support à un exercice complet d'agrégation multi-tables : renommage de colonnes d'identifiant hétérogènes (`ALTER TABLE ... RENAME COLUMN`), nettoyage (NaN, valeurs aberrantes, filtrage métier), `UNION ALL` entre deux réseaux mesurant la même variable, maillage 10×10 km de la France (reprojection Lambert-93 — callback direct au CRS de la séance 1), interpolation spatiale pondérée par noyau gaussien en SQL (`CROSS JOIN` + `GROUP BY`, autre callback à la comparaison de performance de la Partie 1), construction d'un indice composite à 5 niveaux, carte interactive `folium`. Bonus (si le temps le permet) : cartes d'interpolation par variable avec capteurs au survol (`plotly`), indice de confiance, seuil « donnée non disponible ».

Trois fichiers dans `exercices/` : `generation_base_donnees.ipynb` (notebook de préparation, non destiné à être exécuté par les élèves, mais lisible comme documentation du jeu de données et de la méthodologie de l'indice), `exercice.ipynb` (à trous), `correction.ipynb` (solutions complètes, exécuté et vérifié).

**Reste à faire** : les slides (`03_duckdb_sql.html`) mentionnent encore l'ancienne durée de 2h et l'ancien contenu de TP — à mettre à jour dans un second temps pour refléter cette nouvelle structure.
