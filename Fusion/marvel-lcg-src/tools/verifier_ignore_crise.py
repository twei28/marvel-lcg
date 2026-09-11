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
`cards/pack/rainy/rescue_rainy/90119.py` doit la faire rougir. Et remettre
dans `cards/pack/scw/15012.py` la lambda `condition=lambda effect: ...` a la
place de `paid_with="B"` doit la faire rougir aussi (calibre le 11/09/2026) ;
idem pour `cards/pack/hellcat/hellcat/hc006.py` (`paid_with="B", only=True`),
que la premiere version de la gate ne voyait meme pas (`ignore_crisis=mental`).
"""
import os
import re
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PACKS = os.path.join(RACINE, "src", "cards", "pack")

EST_UN_CONTRE = re.compile(r"SetLabel\(\s*['\"]thwart['\"]\s*\)")
# ⚠ Toute valeur autre que False : `ignore_crisis=True`, mais aussi
# `ignore_crisis=mental` (hc006, une variable). La forme `=True` seule
# laissait passer hc006 (constate le 11/09/2026 au soir).
IGNORE_A_LA_RESOLUTION = re.compile(r"ignore_crisis\s*=\s*(?!False\b)[A-Za-z_]")
DECLARE_L_IGNORANCE = re.compile(r"SetIgnoreKeyword\([^)]*['\"]Crisis['\"]")
# AJOUT 11/09/2026 (modale de paiement) : une ignorance CONDITIONNELLE de la
# Crise doit passer par `paid_with="B"`, jamais par une `condition=` ecrite a
# la main. Seule la forme `paid_with` renseigne le rendu (`Effect.Render`),
# donc le plateau, qui previent le joueur avant un paiement sans effet. Une
# lambda maison produirait la meme regle de jeu... et un joueur qui perd sa
# carte sans un mot, le defaut d'origine.
CONDITION_A_LA_MAIN = re.compile(r"SetIgnoreKeyword\([^)]*['\"]Crisis['\"][^)]*condition\s*=")
# Une `condition=` qui ne lit PAS le paiement (br002 Beta Ray Bill : « si tu
# as le vol ou le marteau ») est legitime : elle se sait des le ciblage.
LIT_LE_PAIEMENT = re.compile(r"GetPaidResources\s*\(")


def modules():
    for dossier, _, fichiers in os.walk(PACKS):
        for fichier in fichiers:
            if fichier.endswith(".py"):
                yield os.path.join(dossier, fichier)


def main() -> int:
    contres_qui_ignorent = []
    manquants = []
    conditions_a_la_main = []
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
        if CONDITION_A_LA_MAIN.search(code) and LIT_LE_PAIEMENT.search(code):
            conditions_a_la_main.append(relatif)

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

    if conditions_a_la_main:
        print()
        print(f"ECHEC : {len(conditions_a_la_main)} contre(s) declarent une ignorance "
              "de la Crise qui depend du PAIEMENT avec `condition=` ecrite a la main.")
        for c in conditions_a_la_main:
            print(f"  {c}")
        print("Ecrire `.SetIgnoreKeyword('Crisis', paid_with=\"B\")` (ou `only=True` pour")
        print("« using only [mental] ») : c'est la seule forme que le rendu connait pour")
        print("prevenir le joueur d'un paiement sans effet.")
        return 1

    print()
    print("OK : tout contre qui ignore la Crise la declare sur sa capacite.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
