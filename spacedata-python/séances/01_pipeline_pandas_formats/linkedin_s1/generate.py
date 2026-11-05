"""Génère les 5 cartes LinkedIn (HTML -> PNG carré) pour la séance 1."""
from pathlib import Path
from playwright.sync_api import sync_playwright

HERE = Path(__file__).parent
TEMPLATE = (HERE / "card_template.html").read_text()

CARDS = [
    {
        "class": "card--cover",
        "counter": "1/5",
        "content": """
        <div class="logo-badge"><img src="assets/Logo_IPSA.svg" alt="IPSA"></div>
        <div class="module-name">MSc SpaceData — IPSA / EPITA · Python avancé pour la datascience</div>
        <h1 class="title">Mardi dernier, j'étais à l'IPSA pour la séance 1 de mon module Python avancé pour la datascience.</h1>
        <p class="body-text">Master of Science en alternance</p>
        """,
    },
    {
        "class": "",
        "counter": "2/5",
        "content": """
        <div class="kicker">LE FIL ROUGE</div>
        <h2 class="title">Une donnée brute ne sert à rien</h2>
        <p class="body-text" style="margin-bottom:12px;">On a commencé par poser les bases : avant d'être utile, une donnée doit être collectée, validée, transformée et exploitée.</p>
        <div class="diagram">
          <div class="diagram-step">
            <div class="diagram-icon">📥</div>
            <div class="diagram-text"><div class="diagram-title">Collecte</div><div class="diagram-desc">Récupérer la donnée brute</div></div>
          </div>
          <div class="diagram-arrow-down">↓</div>
          <div class="diagram-step">
            <div class="diagram-icon">🔍</div>
            <div class="diagram-text"><div class="diagram-title">Validation</div><div class="diagram-desc">Types, valeurs manquantes, aberrantes</div></div>
          </div>
          <div class="diagram-arrow-down">↓</div>
          <div class="diagram-step">
            <div class="diagram-icon">⚙️</div>
            <div class="diagram-text"><div class="diagram-title">Transformation</div><div class="diagram-desc">Nettoyer, agréger, croiser</div></div>
          </div>
          <div class="diagram-arrow-down">↓</div>
          <div class="diagram-step">
            <div class="diagram-icon">📊</div>
            <div class="diagram-text"><div class="diagram-title">Exploitation</div><div class="diagram-desc">Export, visualisation, interprétation</div></div>
          </div>
        </div>
        """,
    },
    {
        "class": "",
        "counter": "3/5",
        "content": """
        <div class="kicker">PLACE À LA PRATIQUE</div>
        <h2 class="title">4 fichiers, 4 formats, 60 villes</h2>
        <p class="body-text" style="margin-bottom:4px;">À fusionner et nettoyer — sans code fourni, cette fois.</p>
        <div class="format-grid">
          <div class="format-tile"><div class="format-name">CSV</div><div class="format-desc">Démographie des villes</div></div>
          <div class="format-tile"><div class="format-name">JSON</div><div class="format-desc">Indicateurs économiques</div></div>
          <div class="format-tile"><div class="format-name">GeoJSON</div><div class="format-desc">Géométries &amp; régions</div></div>
          <div class="format-tile"><div class="format-name">Parquet</div><div class="format-desc">Données climatiques</div></div>
        </div>
        """,
    },
    {
        "class": "",
        "counter": "4/5",
        "content": """
        <div class="kicker">LE RÉSULTAT</div>
        <h2 class="title">60 villes, 4 quadrants</h2>
        <p class="body-text">Réparties géographiquement et prêtes à être comparées sur leurs indicateurs.</p>
        <div style="margin-top:28px; border-radius:20px; overflow:hidden; border:1px solid var(--hairline, #2c2c2a); height:540px;">
          <img src="assets/carte_villes_dark.png" style="display:block; width:100%; height:100%; object-fit:cover; object-position:center;">
        </div>
        """,
    },
    {
        "class": "card--section",
        "counter": "5/5",
        "content": """
        <div class="section-num">02</div>
        <div class="kicker">À SUIVRE</div>
        <h2 class="title">Place aux APIs</h2>
        <p class="body-text">Rendez-vous la semaine prochaine pour la séance 2.</p>
        """,
    },
]


def build_html(index: int, card: dict) -> str:
    dots = "".join(
        f'<div class="dot{" active" if i == index else ""}"></div>'
        for i in range(len(CARDS))
    )
    html = TEMPLATE
    html = html.replace("__CARD_CLASS__", card["class"])
    html = html.replace("__CONTENT__", card["content"])
    html = html.replace("__DOTS__", dots)
    html = html.replace("__COUNTER__", card["counter"])
    return html


def main():
    html_dir = HERE / "html"
    png_dir = HERE / "png"
    html_dir.mkdir(exist_ok=True)
    png_dir.mkdir(exist_ok=True)

    paths = []
    for i, card in enumerate(CARDS, start=1):
        html = build_html(i - 1, card)
        html_path = html_dir / f"carte_{i}.html"
        html_path.write_text(html)
        paths.append(html_path)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1080, "height": 1080}, device_scale_factor=2)
        for i, html_path in enumerate(paths, start=1):
            page.goto(html_path.as_uri())
            png_path = png_dir / f"carte_{i}.png"
            page.screenshot(path=str(png_path))
            print("saved", png_path)
        browser.close()


if __name__ == "__main__":
    main()
