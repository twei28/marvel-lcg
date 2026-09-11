"""Un CONTRE qui ignore la Crise doit le DECLARER, pas seulement le passer.

    python3.10 tools/verifier_ignore_crise.py

POURQUOI CETTE GATE EXISTE (11/09/2026)
---------------------------------------
Depuis ce jour, la Crise verrouille la CIBLE et plus seulement la resolution :
`MainScheme.CanBeThwartBy` (scheme_main.py) ne propose plus le complot
principal a un contre tant qu'une icone de crise est en jeu. Garde et
Patrouille faisaient deja cela ; la Crise etait la seule des trois a laisser
choisir la cible puis a ne rien retirer, et un joueur l'a signale apres avoir
rejoue trois fois le meme coup en croyant a un bug.

Consequence pour les cartes qui PASSENT OUTRE la Crise : il ne suffit plus de
passer `ignore_crisis=True` a `RemoveThreatFromSchemes`, qui n'agit qu'A LA
RESOLUTION, donc trop tard pour le ciblage. Il faut aussi le DECLARER sur la
capacite, avec `.SetIgnoreKeyword('Crisis')`, que `IsIgnoreKeyword` consulte
au moment ou le moteur calcule les cibles legales.

CE QUE LA GATE CONTROLE, ET CE QU'ELLE NE CONTROLE PAS
------------------------------------------------------
Elle ne regarde QUE les modules qui sont des CONTRES (`SetLabel('thwart')`)
ET qui ignorent la Crise (`ignore_crisis=True`). Les six autres cartes a
`ignore_crisis=True` du depot sont des ACTIONS : elles ne passent pas par
`CanBeThwartBy`, le verrou ne les touche pas, et rien ne leur est demande.

⚠ C'est une lecture de TEXTE, pas du moteur charge. Elle attrape l'oubli
d'une ligne, pas une capacite construite dynamiquement. Le filet reel reste
le cas « CRISE — TEMOIN FORT » de `tools/test_capacites.py`, qui joue la
carte dans une vraie position.

CALIBRAGE (§9 : une gate qui repond OK ne prouve rien tant qu'on ne l'a pas
vue ECHOUER). Retirer la ligne `.SetIgnoreKeyword('Crisis')` de
`cards/pack/rainy/rescue_rainy/90119.py` doit la faire rougir.
"""
import os
import re
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PACKS = os.path.join(RACINE, "src", "cards", "pack")

EST_UN_CONTRE = re.compile(r"SetLabel\(\s*['\"]thwart['\"]\s*\)")
IGNORE_A_LA_RESOLUTION = re.compile(r"ignore_crisis\s*=\s*True")
DECLARE_L_IGNORANCE = re.compile(r"SetIgnoreKeyword\([^)]*['\"]Crisis['\"]")


def modules():
    for dossier, _, fichiers in os.walk(PACKS):
        for fichier in fichiers:
            if fichier.endswith(".py"):
                yield os.path.join(dossier, fichier)


def main() -> int:
    contres_qui_ignorent = []
    manquants = []
    for chemin in sorted(modules()):
        try:
            with open(chemin, encoding="utf-8") as f:
                source = f.read()
        except OSError:
            continue
        # Les lignes de commentaire ne comptent pas : ce qui est cite en
        # exemple dans une explication n'est pas du code.
        code = "\n".join(l for l in source.split("\n") if not l.lstrip().startswith("#"))
        if not (EST_UN_CONTRE.search(code) and IGNORE_A_LA_RESOLUTION.search(code)):
            continue
        relatif = os.path.relpath(chemin, PACKS)
        contres_qui_ignorent.append(relatif)
        if not DECLARE_L_IGNORANCE.search(code):
            manquants.append(relatif)

    print(f"contres qui ignorent la Crise : {len(contres_qui_ignorent)}")
    for c in contres_qui_ignorent:
        etat = "MANQUE la declaration" if c in manquants else "declare son ignorance"
        print(f"  {c:55} {etat}")

    if manquants:
        print()
        print(f"ECHEC : {len(manquants)} contre(s) ignorent la Crise sans la declarer.")
        print("Ajouter `.SetIgnoreKeyword('Crisis')` sur la capacite : sans elle, le")
        print("complot principal ne leur est plus propose comme cible (CanBeThwartBy).")
        return 1

    print()
    print("OK : tout contre qui ignore la Crise la declare sur sa capacite.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
