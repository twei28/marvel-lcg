from . import *
# Hyper-Speed, amelioration EXOSPEX. Cout 1, [energy]. SUPERPOWER.
#
# Smasher gets +1 ATK, +1 THW and +1 DEF.
# Special: Ready Smasher.
#
# ⚠ TEXTE CHANGE LE 17/11/2026 (fichier Phenexian du 25/10/2026, image du Drive) : l'amelioration n'a PLUS de « Hero Response: After you play
# Hyper-Speed » ; elle porte une capacite « Special » (RECETTES / mots-cles/special.md : capacite nommee qu'une AUTRE carte resout, ici Accessing sz004).
# Jouer l'amelioration ne declenche donc plus rien : seuls le bonus attache et le mot-cle restent actifs ; l'effet n'arrive que par Accessing
# (`ResoudreLaReponseDe`, set `__init__.py`), qui choisit la cible pour le joueur.
#
# Cartes de reference : 01017 (bonus attache) ; 01082 Indomitable (`.SetTarget("YourHero", canbe_ready=True)` + `ReadyAll`) ; 62009.
def GetAbilities() -> Sequence['Ability']:
    return [
        *AbilityFactory.GiveKeywordToAttached(CardFinder(name="Smasher"), attack=1, thwart=1, defense=1),
    ]
