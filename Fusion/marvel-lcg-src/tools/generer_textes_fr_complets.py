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


# Errata officiels (Rules Reference 1.7 et 1.8) absents des traductions FR imprimees : appliques par-dessus.
ERRATA_FR = {
    "01029a": "Votre taille de main augmente de +1 pour chaque amélioration [[TECH]] que vous contrôlez (jusqu'à +6 de taille de main maximum).",
    "04028": "<b>Une fois révélée</b> : le joueur de Clint Barton cherche Mockingbird dans sa main, son deck, sa pile de défausse ou zone de jeu et la glisse, face visible, sous cette carte. Quand cette manigance est déjouée, renvoyez la Mockingbird glissée dans la main de son propriétaire.",
    "08009": "Black Widow gagne +1 DEF.\n<b>Réponse de héros</b> : après avoir résolu la capacité d'une carte [[Préparation]] que vous contrôlez, inclinez le Costume Synthétique → redressez Black Widow.",
    "56098": "Permanent.\n<b>Réponse forcée</b> : après qu'un leader, un héros ou un allié a attaqué Captain Marvel, placez 1 jeton Énergie ici. Ensuite, s'il y a au moins 4 jetons Énergie sur cette carte, retirez-les tous et Captain Marvel attaque ce personnage. Cette attaque gagne Déferlement.",
    "57065": "Riposte 2. Ténacité.\n<b>Une fois révélée</b> : résolvez la capacité « <b>Une fois révélée</b> » de la traîtrise la plus proche du dessus de la pile de défausse Rencontre. (Une fois par phase max.)",
    "27133": "Vous ne pouvez pas contrer cette manigance.\n<b>Action d'alter ego</b> : dépensez 2 ressources de n'importe quel type → retirez de cette manigance un nombre de menaces égal à la REC de votre alter ego. Si votre identité a le trait [[CIVIL]], piochez 1 carte.",
    "27171":"L'allié attaché perd le texte imprimé dans sa boîte de texte <i> sauf les [[TRAIT]])</i> et est considéré comme un sbire. La MNG du sbire attaché est égale à son CTR imprimé et il ne subit pas de dégâts consécutifs.\n<b>Une fois révélée</b> : attachez cette carte à l'allié que vous contrôlez ayant le coût le moins élevé. L'allié attaché engage son contrôleur. Sinon, cette carte gagne Renfort.",
}


def main() -> int:
    catalogue = json.loads(imp.CARTES_JEU.read_text(encoding="utf-8"))
    codes_du_jeu = set()
    for paquet in catalogue.values():
        if isinstance(paquet, list):
            for carte in paquet:
                if isinstance(carte, dict) and isinstance(carte.get("card_id"), str):
                    codes_du_jeu.add(carte["card_id"])
    _, textes_fr, noms_fr = imp.charger_marvelcdb()
    textes_en, noms_en = imp.charger_marvelcdb_anglais()
    # Complement mc4db (08/10/2026) : les cartes que fr.marvelcdb.com n'a pas traduites.
    imp.completer(textes_fr, noms_fr, textes_en, noms_en)
    gardes = {}
    for code, texte in sorted(textes_fr.items()):
        if code not in codes_du_jeu:
            continue
        if textes_en.get(code, "").strip() == texte.strip():
            continue  # pas traduit : l'anglais sous un titre francais serait un mensonge
        gardes[code] = texte
    for code, texte in ERRATA_FR.items():
        if code in codes_du_jeu:
            gardes[code] = texte
    lignes = [
        "// Genere par tools/generer_textes_fr_complets.py — NE PAS EDITER A LA MAIN.",
        "//",
        "// Texte francais OFFICIEL de toutes les cartes du catalogue que fr.marvelcdb.com",
        "// a traduites, complete par mc4db.merlindumesnil.net pour ce qu'il n'a pas",
        "// traduit (les non traduites sont ecartees : leur texte y est l'anglais).",
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
