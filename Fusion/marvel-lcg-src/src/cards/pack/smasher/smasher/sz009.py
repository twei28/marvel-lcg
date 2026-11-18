from . import *
# Exo-Flight, amelioration EXOSPEX AERIAL. Cout 1, [energy]. SUPERPOWER.
#
# Smasher gets +1 THW, +1 DEF and gains the AERIAL trait.
# Special (thwart): Remove 3 threat from a scheme.
#
# ⚠ TEXTE CHANGE LE 17/11/2026 (fichier Phenexian du 25/10/2026, image du Drive) : l'amelioration n'a PLUS de « Hero Response: After you play
# Exo-Flight » ; elle porte une capacite « Special » (RECETTES / mots-cles/special.md : capacite nommee qu'une AUTRE carte resout, ici Accessing sz004).
# Jouer l'amelioration ne declenche donc plus rien : seuls le bonus attache et le mot-cle restent actifs ; l'effet n'arrive que par Accessing
# (`ResoudreLaReponseDe`, set `__init__.py`), qui choisit la cible pour le joueur.
#
# Cartes de reference : 01017 Cosmic Flight (`GiveKeywordToAttached(.., trait="AERIAL")`) ; 47004 Jubilee's Coat (Hero Response (thwart) :
# `.SetLabel('thwart')` + `.SetTarget(Scheme2)`).
def GetAbilities() -> Sequence['Ability']:
    return [
        *AbilityFactory.GiveKeywordToAttached(CardFinder(name="Smasher"), thwart=1, defense=1, trait=TRAIT_AERIAL),
    ]
