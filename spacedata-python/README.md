# Python avancé pour le traitement de données spatiales

Module de 24h (12h cours / 12h TP) — MSc SpaceData (IPSA/EPITA), M1 en alternance.

## Structure du projet

```
spacedata-python/
├── README.md
├── requirements.txt
├── .env.example
├── data/                          # jeux de données générés/locaux (fallback offline)
├── notebooks/                     # notebooks à trous, un par séance
│   ├── 01_pandas_formats_geodata.ipynb
│   ├── 02_apis_micro_api.ipynb
│   ├── 03_duckdb.ipynb
│   ├── 04_apis_spatiales.ipynb
│   └── 05_projet_fil_rouge.ipynb
├── corrections/                   # mêmes notebooks, avec les solutions
└── micro_api/                     # micro-API FastAPI utilisée en séance 2
    ├── server.py
    └── client.py
```

## Installation de l'environnement

Prérequis : Python 3.11+ (testé sur macOS).

```bash
cd spacedata-python
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## Lancer Jupyter

```bash
source .venv/bin/activate
jupyter notebook notebooks/
# ou, si tu préfères l'interface JupyterLab :
jupyter lab notebooks/
```
