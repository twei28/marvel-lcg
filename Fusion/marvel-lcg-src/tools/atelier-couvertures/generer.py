"""Assemble `public/atelier-couvertures.html` : le modele + les calques du PSD en data: URI.

Un seul fichier a double-cliquer. Les calques sont inlines pour que le canvas reste
exportable (une page ouverte en file:// qui charge des images externes est « tainted »
et ne peut plus produire de PNG).

    python3 tools/atelier-couvertures/generer.py
"""
import base64
import json
from pathlib import Path

ici = Path(__file__).parent
calques = {
    p.stem: "data:image/png;base64," + base64.b64encode(p.read_bytes()).decode()
    for p in sorted((ici / "calques").glob("*.png"))
}
modele = (ici / "modele.html").read_text(encoding="utf-8")
(ici.parent.parent / "public" / "atelier-couvertures.html").write_text(
    modele.replace("/*CALQUES*/", "const CALQUES = " + json.dumps(calques) + ";"), encoding="utf-8"
)
print(f"{len(calques)} calques -> public/atelier-couvertures.html")
