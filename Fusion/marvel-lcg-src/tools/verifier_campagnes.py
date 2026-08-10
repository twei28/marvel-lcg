"""Verifie que les cles d'un fichier de campagne existent vraiment dans le moteur.

Le piege est documente au §5 de docs/CAMPAGNES.md et ne fait AUCUN bruit : une
cle mal orthographiee dans `data/campagnes/*.json` ne leve rien du tout. Le
moteur lit une valeur vide, la recompense ne s'applique pas, et la campagne a
l'air de fonctionner. C'est le genre de defaut qu'on ne decouvre qu'en jouant
cinq scenarios pour rien.

Cet outil compare donc chaque cle declaree aux chaines litterales du
`campaign.py` du pack. Le prefixe « Player N » ajoute par `parJoueur` est
retire avant comparaison, puisque le moteur ecrit `Player 1 Role` a partir du
litteral `Role`.

    ~/marvel-work/python/bin/python3.10 tools/verifier_campagnes.py

Sortie : une ligne par campagne, et la liste des cles introuvables. Code de
retour non nul s'il en reste une.
"""
import ast
import json
import os
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAMPAGNES = os.path.join(RACINE, "data", "campagnes")
PACKS = os.path.join(RACINE, "src", "cards", "pack")

# Ecrites par WriteCampaignLogAtGameOver, commun aux quatre boites, pas par le
# campaign.py de chaque pack.
COMMUNES = {"Remaining hit points", "Identity"}


def litteraux(chemin):
    """Toutes les chaines litterales d'un module Python."""
    trouves = set()
    try:
        arbre = ast.parse(open(chemin, encoding="utf-8").read())
    except Exception:
        return trouves
    for noeud in ast.walk(arbre):
        if isinstance(noeud, ast.Constant) and isinstance(noeud.value, str):
            trouves.add(noeud.value)
        # f'Player {N} Role' : on garde le morceau litteral, « Role » ici.
        elif isinstance(noeud, ast.JoinedStr):
            for part in noeud.values:
                if isinstance(part, ast.Constant) and isinstance(part.value, str):
                    trouves.add(part.value.strip())
    return trouves


def connue(cle, litteraux):
    """La cle existe-t-elle dans le moteur, ecrite ou COMPOSEE ?

    Beaucoup de cles sont fabriquees a l'execution : `f'Campaign Pool: {nom}'`,
    ou le prefixe est un litteral et le nom vient d'une table (CAMPAIGN_SCHEMES,
    OVERSEERS, MISSIONS...). Chercher la cle entiere ne trouve donc rien, et
    l'outil criait au loup sur les 21 cles de next_evol et aoa alors qu'elles
    sont toutes justes. On accepte donc aussi une cle qui se decoupe en un
    prefixe litteral suivi d'un suffixe litteral.
    """
    if cle in litteraux:
        return True
    for prefixe in litteraux:
        if prefixe and prefixe.endswith(" ") and cle.startswith(prefixe):
            if cle[len(prefixe):] in litteraux:
                return True
    return False


def cles_du_fichier(definition):
    for scenario in definition.get("scenarios") or []:
        for champ in scenario.get("victoire") or []:
            yield champ["cle"]
    for nom in ("victoire_commune", "victoire_commune_expert"):
        for champ in definition.get(nom) or []:
            yield champ["cle"]


def main():
    total_manquantes = 0
    for fichier in sorted(os.listdir(CAMPAGNES)):
        if not fichier.endswith(".json"):
            continue
        definition = json.load(open(os.path.join(CAMPAGNES, fichier), encoding="utf-8"))
        code = definition.get("code", fichier[:-5])
        connues = set(COMMUNES)
        # Une cle peut vivre a trois endroits, et se limiter au campaign.py du
        # pack fait crier au loup : `sm` et `trors` n'en ont pas du tout, leurs
        # cles sont dans le registre commun et dans les scripts de cartes
        # (« Number of delay counters on main scheme » est ecrite par
        # trors/red_skull/04128a.py). On ratisse donc le pack ENTIER, plus le
        # registre commun, plus les helpers de mts que les quatre boites a
        # collecteur partagent.
        for chemin in (
            os.path.join(RACINE, "src", "game", "operate", "campaign_logs.py"),
            os.path.join(RACINE, "src", "game", "ability", "factory", "campaign.py"),
            os.path.join(PACKS, "mts", "campaign.py"),
        ):
            if os.path.exists(chemin):
                connues |= litteraux(chemin)
        for racine, _, fichiers in os.walk(os.path.join(PACKS, code)):
            for nom in fichiers:
                if nom.endswith(".py"):
                    connues |= litteraux(os.path.join(racine, nom))

        cles = list(cles_du_fichier(definition))
        manquantes = [c for c in cles if not connue(c, connues)]
        total_manquantes += len(manquantes)
        etat = "OK" if not manquantes else "%d INTROUVABLE(S)" % len(manquantes)
        print("  %-10s %2d cle(s) declaree(s)  %s" % (code, len(cles), etat))
        for c in manquantes:
            print("      introuvable dans le moteur : %r" % c)

    print()
    if total_manquantes:
        print("  %d cle(s) ne correspondent a rien : la recompense sera vide, en silence."
              % total_manquantes)
        return 1
    print("  Toutes les cles declarees existent dans le moteur.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
