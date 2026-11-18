from . import *
# Penta-Vision, amelioration EXOSPEX. Cout 1, [mental]. SUPERPOWER.
#
# Smasher gets +1 ATK and +1 THW. Smasher's attacks gain ranged.
# Special (attack): Deal 3 damage to an enemy.
#
# ⚠ TEXTE CHANGE LE 17/11/2026 (fichier Phenexian du 25/10/2026, image du Drive) : l'amelioration n'a PLUS de « Hero Response: After you play
# Penta-Vision » ; elle porte une capacite « Special » (RECETTES / mots-cles/special.md : capacite nommee qu'une AUTRE carte resout, ici Accessing sz004).
# Jouer l'amelioration ne declenche donc plus rien : seuls le bonus attache et le mot-cle restent actifs ; l'effet n'arrive que par Accessing
# (`ResoudreLaReponseDe`, set `__init__.py`), qui choisit la cible pour le joueur.
#
# Cartes de reference : 01017 Cosmic Flight (`GiveKeywordToAttached(CardFinder(name=..))`) ; fiche mots-cles/ranged.md
# (`UnitAttackGainKeyword(.., ranged=True)`, permanent) ; 62009 (`AfterYouPlayThisFromHand`) ; 08010 Widow's Bite (Hero Response (attack) :
# `.SetLabel('attack')` + cible).
def GetAbilities() -> Sequence['Ability']:
    return [
        *AbilityFactory.GiveKeywordToAttached(CardFinder(name="Smasher"), attack=1, thwart=1),
        AbilityFactory.UnitAttackGainKeyword("You", ranged=True),
    ]
