from . import *
# Super-Resistance, amelioration EXOSPEX. Cout 1, [physical]. SUPERPOWER.
#
# Smasher gets +2 DEF and gains Stalwart.
# Special: Give Smasher a tough status card.
#
# ⚠ TEXTE CHANGE LE 17/11/2026 (fichier Phenexian du 25/10/2026, image du Drive) : l'amelioration n'a PLUS de « Hero Response: After you play
# Super-Resistance » ; elle porte une capacite « Special » (RECETTES / mots-cles/special.md : capacite nommee qu'une AUTRE carte resout, ici Accessing sz004).
# Jouer l'amelioration ne declenche donc plus rien : seuls le bonus attache et le mot-cle restent actifs ; l'effet n'arrive que par Accessing
# (`ResoudreLaReponseDe`, set `__init__.py`), qui choisit la cible pour le joueur.
#
# Cartes de reference : 01017 ; fiche mots-cles/stalwart.md (`GiveKeywordToAttached(.., stalwart=1)`) ; 01105 « I'm Tough »
# (`Faces.GiveStatus([..], "Tough", effect)`).
def GetAbilities() -> Sequence['Ability']:
    return [
        *AbilityFactory.GiveKeywordToAttached(CardFinder(name="Smasher"), defense=2, stalwart=1),
    ]
