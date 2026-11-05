# Séances — Python avancé pour données spatiales

Chaque séance a son propre dossier, avec le deck de cours (HTML) et son dossier `exercices/` (notebook ou TP, correction, données). Séances 5 et 6 n'ont pas de deck : projet fil rouge en autonomie.

```
séances/
├── assets/
│   ├── theme.css          # design system partagé par tous les decks (couleurs, composants)
│   └── deck.js            # navigation + coloration syntaxique, sans dépendance externe
├── 01_pipeline_pandas_formats/
│   ├── 01_pipeline_pandas_formats.html
│   ├── exercices/
│   │   ├── exercice.ipynb
│   │   ├── correction.ipynb
│   │   └── data/
│   └── linkedin_s1/        # génération des cartes LinkedIn de la séance 1 (annexe)
├── 02_apis_authentification/
│   ├── 02_apis_authentification.html
│   └── exercices/
│       ├── README.md       # consignes du TP (pas de notebook, cf. micro-API)
│       ├── micro_api/       # server.py / client.py à compléter
│       └── correction/
├── 03_duckdb_sql/
│   ├── 03_duckdb_sql.html
│   └── exercices/
│       ├── exercice.ipynb
│       ├── correction.ipynb
│       └── etat_des_lieux_avant_seance3.md
├── 04_apis_spatiales/
│   ├── 04_apis_spatiales.html
│   └── exercices/
│       ├── exercice.ipynb
│       ├── correction.ipynb
│       └── data/
└── 05_projet_fil_rouge/
    └── exercices/
        ├── exercice.ipynb
        ├── exemple_enseignant.ipynb   # non suivi par git, usage interne
        └── data/
```

## Utiliser les slides

Ouvrez simplement le fichier `.html` de la séance dans un navigateur (double-clic, ou `open 01_pipeline_pandas_formats/01_pipeline_pandas_formats.html`). Tout est **100 % local et hors-ligne** — aucune dépendance CDN, aucune connexion internet requise en salle.

**Navigation :**
- `↓` / `→` / `Espace` / `Page suivante` — slide suivante
- `↑` / `←` / `Page précédente` — slide précédente
- `Home` / `End` — première / dernière slide
- `F` — plein écran
- Boutons `‹ ›` en bas de l'écran, ou clic dans la barre de défilement

Chaque slide est linkable : l'URL se met à jour (`#12`) et rechargeant la page revient à la même slide.

## Modifier ou étendre un deck

- Toutes les couleurs, espacements et composants (tableaux, blocs de code, diagrammes, badges HTTP, cartes de lien...) sont définis une seule fois dans `assets/theme.css` — tous les decks le partagent (référencé en `../assets/theme.css` depuis chaque dossier de séance).
- Chaque deck fixe sa couleur d'accent via l'attribut `data-accent` sur `<html>` (`blue`, `violet`, `aqua`, `orange` — un accent par séance, jamais mélangés dans un même deck).
- Les blocs de code utilisent `<code data-lang="python|sql|bash|json|text">` : `deck.js` applique une coloration syntaxique légère (mots-clés, chaînes, commentaires, nombres) sans librairie externe.
- Pour ajouter une slide, copiez un `<section class="slide ...">` existant et adaptez son contenu — les classes disponibles (bullets, tableaux comparatifs, diagrammes, badges, cartes de lien, callouts) sont toutes illustrées dans les decks existants.

## Correspondance deck / TP

| Séance | Deck | TP associé |
|---|---|---|
| 1 | `01_pipeline_pandas_formats/01_pipeline_pandas_formats.html` | `01_pipeline_pandas_formats/exercices/exercice.ipynb` |
| 2 | `02_apis_authentification/02_apis_authentification.html` | `02_apis_authentification/exercices/README.md` |
| 3 | `03_duckdb_sql/03_duckdb_sql.html` | `03_duckdb_sql/exercices/exercice.ipynb` |
| 4 | `04_apis_spatiales/04_apis_spatiales.html` | `04_apis_spatiales/exercices/exercice.ipynb` |
