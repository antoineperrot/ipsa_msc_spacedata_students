# Séance 3 — DuckDB & SQL analytique : aperçu de la séance

Format prévu : **1h de cours (slides) + 3h de TP**.
Fichiers : `03_duckdb_sql.html` (slides) · `exercices/generation_base_donnees.ipynb` · `exercices/exercice.ipynb` · `exercices/correction.ipynb`.

---

## 1. Les slides (`03_duckdb_sql.html`, 34 slides, ~1h)

Fil conducteur : *une fois la donnée collectée (séance 2), comment l'interroger efficacement, même quand elle devient volumineuse ?* Puis le TP est présenté comme un **cas métier**, pas comme un exercice.

| Section | Slides | Contenu |
|---|---|---|
| Rappel séance 2 (~5 min) | 1 | Client-serveur, verbes HTTP, codes de statut, authentification. |
| 1. Pourquoi SQL malgré pandas ? (~10 min) | 1 | pandas = impératif (*comment*), SQL/DuckDB = déclaratif (*quoi*). Outils **complémentaires**. |
| 2. Bases SQL (~25 min) | 13 | Montée en difficulté sur une table fil rouge `satellites` : table/`NULL` ; squelette d'une requête ; `SELECT … FROM` + `AS` ; `WHERE` ; `AND/OR/IN/BETWEEN/LIKE/IS NULL` et le piège `= NULL` ; `ORDER BY`/`LIMIT` ; agrégats ; `GROUP BY` ; `WHERE` vs `HAVING` ; pourquoi joindre ; `INNER JOIN` ; `LEFT JOIN` ; **dictionnaire français → SQL** ; requête complète annotée. Chaque slide montre le code, son résultat et une note **« En français »** qui reformule la requête en phrase. |
| 3. DuckDB dans l'écosystème (~10 min) | 4 | In-process ; `duckdb.sql("... FROM df ...")` sur un DataFrame ; `read_parquet` sans tout charger ; ordre de grandeur pandas vs DuckDB ; comparatif DuckDB / Spark / BigQuery. |
| Récap | 1 | Ce qu'on a vu, transition vers le TP. |
| 4. Le TP : un cas concret (~10 min) | 8 | Présenté comme une mission client : (1) **le brief** — des données partielles (quelques centaines de capteurs, 4 réseaux, données sales) pour répondre à un besoin (la qualité de l'air en tout point de la France, en 5 niveaux) ; (2) **le livrable attendu**, avec la capture de la carte de la correction ; (3) les 4 tables transmises et leurs défauts ; (4) la démarche en 5 étapes (Fiabiliser, Rapprocher, Couvrir, Estimer, Qualifier) reliées aux briques SQL ; (5) l'interpolation par moyenne pondérée (idée + squelette SQL) ; (6) les 3 règles de l'indice (sous-indices, pire polluant, vent) ; (7) checklist de démarrage + répartition du temps. |

La capture du livrable est `img/carte_qualite_air.png` (générée depuis `air_quality_index` de la correction).

---|---|---|
| Rappel séance 2 (~5 min) | 1 | Client-serveur, verbes HTTP, codes de statut, authentification. |
| 1. Pourquoi SQL malgré pandas ? (~10 min) | 1 | pandas = impératif (*comment*), SQL/DuckDB = déclaratif (*quoi*). Outils **complémentaires**. |
| 2. Bases SQL (~30 min) | 15 | Montée en difficulté sur une table fil rouge `satellites` (8 lignes) : (1) une table, lignes/colonnes/types/`NULL` ; (2) le squelette d'une requête ; (3) `SELECT … FROM` ; (4) colonnes calculées et `AS` ; (5) `WHERE` + opérateurs de comparaison ; (6) `AND/OR/IN/BETWEEN/LIKE/IS NULL` et le piège `= NULL` ; (7) `ORDER BY` / `LIMIT` ; (8) ordre d'écriture vs ordre d'exécution ; (9) agrégats `COUNT/SUM/AVG/MIN/MAX` ; (10) `GROUP BY` ; (11) `WHERE` vs `HAVING` ; (12) pourquoi joindre (clés primaire/étrangère) avec `missions` ; (13) `INNER JOIN` ; (14) `LEFT JOIN` ; puis un **dictionnaire français → SQL** (« pour chaque… » = `GROUP BY`, « seulement ceux qui… » = `WHERE`…) et une requête complète annotée clause par clause. Chaque slide montre le code, son résultat, et une note **« En français »** qui reformule la requête en phrase, mots-clés SQL en regard, pour montrer que SQL est presque une traduction mot à mot. |
| 3. DuckDB dans l'écosystème (~10 min) | 4 | In-process (pas de serveur) ; `duckdb.sql("... FROM df ...").df()` référence un DataFrame ; `read_parquet(...)` sans tout charger ; ordre de grandeur pandas (~1–2 s) vs DuckDB (~0,1 s) ; comparatif DuckDB / Spark / BigQuery. |
| Récap + transition TP (~5 min) | 1 | Renvoi vers `exercices/exercice.ipynb`. |

---|---|
| Rappel séance 2 | Client-serveur, verbes HTTP, codes de statut, authentification (clé API, bearer, `.env`). |
| 1. Pourquoi SQL malgré pandas ? | pandas = impératif (on décrit *comment*), SQL/DuckDB = déclaratif (on décrit *quoi*). Outils **complémentaires** : DuckDB pour agréger/joindre, pandas pour la suite. |
| 2. Bases SQL | `SELECT / WHERE / ORDER BY`, `GROUP BY / HAVING` (`WHERE` filtre les lignes avant regroupement, `HAVING` les groupes après), `INNER JOIN` vs `LEFT JOIN`. Exemples sur une table fictive `satellites`. |
| 3. DuckDB dans l'écosystème | In-process (pas de serveur) ; `duckdb.sql("... FROM df ...").df()` référence directement un DataFrame ; `read_parquet(...)` lit un fichier sans le charger en mémoire ; ordre de grandeur pandas (~1–2 s) vs DuckDB (~0,1 s) ; comparatif DuckDB / Spark / BigQuery. |
| Récap | SQL + pandas complémentaires ; bases SQL ; DuckDB zero-copy + Parquet. Puis renvoi vers le TP. |

> ⚠️ **Slides à mettre à jour** : elles annoncent encore *« 2h de cours + 2h de TP »* et un TP nommé `03_duckdb.ipynb`, et le sommaire totalise ~95 min. Le TP réel dure maintenant 3h et s'appelle `exercices/exercice.ipynb`. Le récap des slides ne mentionne pas non plus le projet « qualité de l'air ».

---

## 2. Le TP (3h)

### Avant de commencer (côté élèves)
1. Environnement Python installé (`requirements.txt` à la racine : `duckdb`, `pandas`, `geopandas`, `folium`, `plotly`...).
2. **Générer la base** en exécutant une fois `generation_base_donnees.ipynb` (quelques secondes) : il produit `exercices/data/qualite_air.duckdb`. Le fichier n'est **pas versionné** (`*.duckdb` est dans le `.gitignore`).
3. *(Optionnel)* installer le **DuckDB CLI** (instructions Mac/Windows en tête du notebook) et lancer `duckdb -ui data/qualite_air.duckdb` pour explorer les tables dans le navigateur.

### Partie 1 — Prise en main de DuckDB (~30-40 min)
Sur les données de villes de la séance 1 (30 villes, régénérées automatiquement si absentes) :
- SQL directement sur un **DataFrame pandas** (`duckdb.sql(...).df()`) ;
- SQL directement sur un **fichier Parquet** (`read_parquet`) ;
- agrégation + **jointure** entre deux CSV (`read_csv_auto`) ;
- **comparaison de temps pandas vs DuckDB** sur 1 million de lignes (fait écho aux slides) ;
- **À faire** : 3 requêtes à trous (top 5 des villes par population ; nb de villes et population moyenne par région ; villes > 14 °C via une jointure).

### Partie 2 — Projet « indice de qualité de l'air pour la France » (~2h-2h20 + bonus)

**Les données** (`qualite_air.duckdb`, générée avec une graine fixe) : 4 réseaux de capteurs synthétiques mais réalistes, volontairement « sales » :

| Table | Variables | Colonne ID | Particularités |
|---|---|---|---|
| `releves_meteo` | température, humidité, précipitations, vent (vitesse, direction) | `id_station_meteo` | répartition plutôt uniforme |
| `releves_qualite_air_urbain` | NO2, PM10, PM2.5 | `code_capteur_aq` | concentrée autour des villes ; colonne `type_implantation` (fond urbain / trafic / industriel) |
| `releves_ozone_rural` | O3 | `ref_station_o3` | stations volontairement éloignées des villes |
| `releves_citoyen_pm` | PM10 | `capteur_uid_pm` | très dense, bruitée, biais à la hausse (capteurs low-cost) |

Chaque table contient aussi des **colonnes inutiles** (fabricant, numéro de série, pseudo...), des **valeurs manquantes** et des **valeurs aberrantes**, et son identifiant de capteur porte un **nom différent** d'une table à l'autre.

**Ce que les élèves voient en ouvrant la base** : 4 tables brutes ; au fil du TP apparaissent `*_propre`, `capteurs_*`, `maille`, `air_quality_index`.

**Étapes du TP** (les `<TODO>` sont indiqués) :

| # | Étape | Compétence / ce qu'ils écrivent |
|---|---|---|
| 1 | Connexion + `DESCRIBE` des 4 tables | repérer l'hétérogénéité des schémas |
| 2 | Harmoniser les identifiants → `id_capteur` | `ALTER TABLE ... RENAME COLUMN` |
| 3 | Nettoyage | compter les `NULL` (`SUM(CASE WHEN ... IS NULL ...)`) ; choisir des bornes physiques réalistes avec `WHERE ... BETWEEN` (qui élimine aussi les `NULL`) ; filtre métier `type_implantation = 'fond urbain'` |
| 4 | Un pool de capteurs par variable | `SELECT ... AS valeur`, **`UNION ALL`** pour fusionner capteurs officiels + citoyens sur PM10 ; reprojection Lambert-93 (rappel séance 1) |
| 5 | Maillage régulier 10×10 km de la France (~5 400 mailles) | choisir le pas en mètres (`10_000`) ; grille construite en Lambert-93 avec geopandas |
| 6 | **Interpolation spatiale en SQL** | `CROSS JOIN` mailles × capteurs, poids gaussien `w = exp(-(D/l)²)`, `SUM(w·valeur)/SUM(w)` avec `GROUP BY` ; ils choisissent la longueur caractéristique `l` par variable. `SUM(w)` est conservé comme mesure de confiance. DuckDB traite sans effort plusieurs millions de lignes (écho à la comparaison de perf de la Partie 1). |
| 7 | **Fonction de qualité de l'air** (Python) | sous-indice 1–5 par polluant (PM10, PM2.5, NO2, O3) via seuils ; indice global = **pire sous-indice** ; modulation par le vent (< 5 km/h : +1 niveau ; > 25 km/h : −1) ; libellés Très bon / Bon / Moyen / Dégradé / Très dégradé |
| 8 | Écrire la table `air_quality_index` en base + **carte** | carte folium (donnée) puis version plotly équivalente (fournies, non à trous) |

**Bonus** (si le temps le permet) :
1. Carte NO2 plotly : champ interpolé + capteurs bruts avec identifiant au survol (1 `<TODO>` : le texte du survol).
2. **Indice de confiance** : minimum des `Σw` des 4 polluants ; choix d'un seuil d'après les quantiles ; mailles sous le seuil → « Donnée non disponible » (grises) ; carte avec la confiance au survol.

### Résultat attendu (correction)
Avec la graine par défaut : ~5 375 mailles, majoritairement « Bon » (≈ 4 400), quelques poches « Très dégradé » près des grandes villes (≈ 115), et avec le seuil au premier quartile ≈ 1 340 mailles passent en « Donnée non disponible ».

### À propos du notebook `generation_base_donnees.ipynb`
Pas un TP : il documente comment les données sont fabriquées (champ d'influence gaussien des 30 villes, longueur caractéristique ∝ √population, tirage de points en France par *rejection sampling* dans un contour simplifié, taux de NaN/aberrants configurables par réseau, méthodologie et seuils de l'indice). Il se lit comme une spécification de ce que les élèves doivent reconstruire.

---

## 3. Pense-bête avant la séance
- Vérifier que chaque élève a généré `qualite_air.duckdb` **avant** le TP (sinon `FileNotFoundError` explicite).
- Si le notebook est ouvert dans plusieurs kernels, DuckDB pose un verrou sur le fichier : fermer/redémarrer les autres kernels (et `duckdb -ui`) avant de lancer le notebook.
- Les 57 `<TODO>` de `exercice.ipynb` sont résolus dans `correction.ipynb` (exécuté, sans erreur lors de la dernière vérification).
