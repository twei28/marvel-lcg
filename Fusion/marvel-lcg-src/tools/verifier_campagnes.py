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


def champs_du_fichier(definition):
    for scenario in definition.get("scenarios") or []:
        for champ in scenario.get("victoire") or []:
            yield champ
    for nom in ("victoire_commune", "victoire_commune_expert"):
        for champ in definition.get(nom) or []:
            yield champ


def cles_du_fichier(definition):
    for scenario in definition.get("scenarios") or []:
        for champ in scenario.get("victoire") or []:
            yield champ["cle"]
    for nom in ("victoire_commune", "victoire_commune_expert"):
        for champ in definition.get(nom) or []:
            yield champ["cle"]


# Valeurs acceptees pour l'attribut `deck` d'un champ de victoire.
#
# `requis` : le moteur CHERCHE cette carte dans le deck du joueur a la mise en
# place du scenario suivant (« Planning Ahead » de sm). L'ecran des campagnes
# refuse donc, au retour de « Modifier les decks », un deck qui ne la contient
# plus. Sans `parJoueur`, la cle ne designerait le deck de personne : la forme
# globale est refusee ici plutot que d'etre ignoree en silence a l'ecran.
DECK_VALEURS = {"requis"}

# Les detecteurs disponibles, lus dans le code qui les implemente plutot que
# recopies ici : `detecter()` est un switch, chaque `case '<nom>'` est un
# detecteur. Une `detection` inconnue ne leve RIEN a l'execution — le champ reste
# vide, la recompense disparait, et c'est exactement le silence que cet outil
# existe pour casser (meme famille que la cle mal orthographiee du §5).
# Le depot met `ui-app` DEUX niveaux au-dessus de marvel-lcg-src
# (« Jeu Marvel Champions/ui-app »), et la copie de travail de ~/marvel-work ne
# l'a pas du tout. On cherche donc, et l'absence n'est pas une erreur : elle est
# annoncee, et les `detection` ne sont simplement pas verifiees la-bas.
CHEMINS_DETECTEURS = [
    os.path.join(haut, "ui-app", "src", "board", "campagne", "detecteurs.ts")
    for haut in (
        os.path.dirname(os.path.dirname(RACINE)),
        os.path.dirname(RACINE),
        RACINE,
    )
]


def detecteurs_connus():
    import re
    for chemin in CHEMINS_DETECTEURS:
        try:
            with open(chemin, encoding="utf-8") as f:
                source = f.read()
        except OSError:
            continue
        return set(re.findall(r"case '([a-z_]+)':", source))
    return None


def defauts_de_forme(definition, detecteurs=None):
    """Les champs dont un attribut ne veut rien dire."""
    defauts = []
    # Ordre de declaration : un champ a TIRAGE lit une piste qui doit avoir ete
    # calculee AVANT lui, sinon il tire sur le total de la veille. `preRemplir`
    # parcourt les champs dans cet ordre, sans le deviner.
    rang = {champ["cle"]: i for i, champ in enumerate(champs_du_fichier(definition))}
    for champ in champs_du_fichier(definition):
        tirage = champ.get("tirage")
        if tirage is not None:
            paliers = tirage.get("paliers")
            piste = tirage.get("cle_piste")
            if not isinstance(paliers, list) or not paliers or \
                    not all(isinstance(x, int) and x > 0 for x in paliers):
                defauts.append("%r : tirage.paliers doit etre une liste d'entiers positifs"
                               % champ["cle"])
            elif paliers != sorted(paliers):
                defauts.append("%r : tirage.paliers n'est pas croissant %r"
                               % (champ["cle"], paliers))
            if not champ.get("options"):
                defauts.append("%r : tirage sans options, il n'y a rien a tirer" % champ["cle"])
            if not piste or piste not in rang:
                defauts.append("%r : tirage.cle_piste=%r n'est declaree nulle part"
                               % (champ["cle"], piste))
            elif rang[piste] >= rang[champ["cle"]]:
                defauts.append("%r : tirage.cle_piste=%r est declaree APRES ce champ "
                               "(il tirerait sur le total precedent)" % (champ["cle"], piste))
            if champ.get("type") != "auto":
                defauts.append("%r : un tirage est releve par le jeu, donc type=auto"
                               % champ["cle"])
    for champ in champs_du_fichier(definition):
        detection = champ.get("detection")
        if detection and detecteurs is not None and detection not in detecteurs:
            defauts.append("%r : detection=%r n'existe pas dans detecteurs.ts (champ vide, en silence)"
                           % (champ["cle"], detection))
        if champ.get("cumulatif") and champ.get("format") != "int":
            defauts.append("%r : cumulatif n'a de sens que sur un format int"
                           % champ["cle"])
        valeur = champ.get("deck")
        if valeur is None:
            continue
        if valeur not in DECK_VALEURS:
            defauts.append("%r : deck=%r inconnu (attendu %s)"
                           % (champ["cle"], valeur, " ou ".join(sorted(DECK_VALEURS))))
        elif not champ.get("parJoueur"):
            defauts.append("%r : deck=%r exige parJoueur, sinon aucun deck n'est designe"
                           % (champ["cle"], valeur))
    return defauts


def main():
    total_manquantes = 0
    detecteurs = detecteurs_connus()
    if detecteurs is None:
        print("  (detecteurs.ts introuvable : les `detection` ne sont pas verifiees)")
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

        for d in defauts_de_forme(definition, detecteurs):
            total_manquantes += 1
            print("      forme refusee : %s" % d)

    print()
    if total_manquantes:
        print("  %d cle(s) ne correspondent a rien : la recompense sera vide, en silence."
              % total_manquantes)
        return 1
    print("  Toutes les cles declarees existent dans le moteur.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
