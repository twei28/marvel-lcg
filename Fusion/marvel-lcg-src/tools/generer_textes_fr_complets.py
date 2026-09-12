"""Le texte francais de TOUTES les cartes du catalogue, pour le plateau.

    python3 tools/generer_textes_fr_complets.py

POURQUOI (12/09/2026). `textes-fr.ts` ne porte que les cartes SANS scan
francais : c'etait le seul endroit ou le plateau lisait un texte. Depuis que
le panneau des fenetres de reaction ecrit le texte de la capacite proposee
(« I Object! » de Jennifer Walters), il lui faut le francais de toutes les
cartes, scan ou pas : « pourquoi j'ai encore et toujours du texte en anglais
quand je joue en FR ».

Reprend les deux chargements de tools/importer_scans_fr.py (fr.marvelcdb.com
et marvelcdb.com, 8 Mo chacun, une requete) et le meme filtre de sincerite :
fr.marvelcdb.com renvoie l'anglais tel quel pour ce qu'il n'a pas traduit, et
ces entrees-la ne sont PAS ecrites. Seules les cartes de data/cards.json sont
gardees.

Ecrit ui-app/src/board/textes-fr-complets.ts, charge PARESSEUSEMENT par le
plateau (import dynamique : il pese plusieurs centaines de Ko, il ne doit pas
alourdir le premier affichage).
"""
import json
import sys
from pathlib import Path

ICI = Path(__file__).resolve().parent
sys.path.insert(0, str(ICI))
import importer_scans_fr as imp  # noqa: E402

SORTIE = ICI.parent.parent.parent / "ui-app" / "src" / "board" / "textes-fr-complets.ts"


def main() -> int:
    catalogue = json.loads(imp.CARTES_JEU.read_text(encoding="utf-8"))
    codes_du_jeu = set()
    for paquet in catalogue.values():
        if isinstance(paquet, list):
            for carte in paquet:
                if isinstance(carte, dict) and isinstance(carte.get("card_id"), str):
                    codes_du_jeu.add(carte["card_id"])
    _, textes_fr, _ = imp.charger_marvelcdb()
    textes_en, _ = imp.charger_marvelcdb_anglais()
    gardes = {}
    for code, texte in sorted(textes_fr.items()):
        if code not in codes_du_jeu:
            continue
        if textes_en.get(code, "").strip() == texte.strip():
            continue  # pas traduit : l'anglais sous un titre francais serait un mensonge
        gardes[code] = texte
    lignes = [
        "// Genere par tools/generer_textes_fr_complets.py — NE PAS EDITER A LA MAIN.",
        "//",
        "// Texte francais OFFICIEL de toutes les cartes du catalogue que fr.marvelcdb.com",
        "// a traduites (les non traduites sont ecartees : leur texte y est l'anglais).",
        "// Charge paresseusement par le plateau (import dynamique) : il ne sert qu'aux",
        "// fenetres de reaction, qui ecrivent le texte de la capacite proposee.",
        "export const TEXTES_FR_COMPLETS: Readonly<Record<string, string | undefined>> = {",
    ]
    for code, texte in gardes.items():
        lignes.append(f"  {json.dumps(code)}: {json.dumps(texte, ensure_ascii=False)},")
    lignes.append("}")
    SORTIE.write_text("\n".join(lignes) + "\n", encoding="utf-8")
    print(f"{len(gardes)} textes francais ecrits dans {SORTIE} ({SORTIE.stat().st_size // 1024} Ko)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
