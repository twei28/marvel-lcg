"""Releve, dans NOTRE catalogue (data/cards.json), les cartes officielles ANGLAISES qui ont un scan (assets/pics ou assets/pics-hd),
avec de quoi les comparer a une carte en cours de creation : type, nombre de mots du texte, nombre de declencheurs en gras.
Ecrit `public/createur-cartes/donnees/comparables.json` ([code, nom, type, mots, declencheurs]). Aucune image n'est copiee :
les scans sont servis par la route `/api/createur/scan/<code>` (session obligatoire).

    python3 tools/createur-cartes/extraire-comparables.py
"""
import json
import re
from pathlib import Path

RACINE = Path(__file__).resolve().parents[2]
cartes = json.loads((RACINE / "data/cards.json").read_text(encoding="utf-8"))
avec_scan = {p.stem for d in ("assets/pics", "assets/pics-hd") for p in (RACINE / d).glob("*.jpg")}
lignes = []
for liste in cartes.values():
    for c in liste:
        if not isinstance(c, dict) or not c.get("text") or c["card_id"] not in avec_scan:
            continue
        brut = c["text"]
        sans = re.sub(r"<[^>]*>|\[[a-z_]+\]", " ", brut)
        lignes.append([c["card_id"], re.sub(r"^\*\s*", "", c.get("name", "")), c["type"], len(sans.split()), len(re.findall(r"<b>", brut))])
sortie = RACINE / "public/createur-cartes/donnees/comparables.json"
sortie.write_text(json.dumps(lignes, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
print(len(lignes), "cartes ->", sortie, sortie.stat().st_size // 1024, "Ko")
