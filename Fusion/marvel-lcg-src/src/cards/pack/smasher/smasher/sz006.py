from . import *
# Hyper-Strength, amelioration EXOSPEX. Cout 1, [physical]. SUPERPOWER.
#
# Smasher gets +2 ATK. Smasher's attacks gain overkill.
# Special: Stun an enemy.
#
# ⚠ TEXTE CHANGE LE 17/11/2026 (fichier Phenexian du 25/10/2026, image du Drive) : l'amelioration n'a PLUS de « Hero Response: After you play
# Hyper-Strength » ; elle porte une capacite « Special » (RECETTES / mots-cles/special.md : capacite nommee qu'une AUTRE carte resout, ici Accessing sz004).
# Jouer l'amelioration ne declenche donc plus rien : seuls le bonus attache et le mot-cle restent actifs ; l'effet n'arrive que par Accessing
# (`ResoudreLaReponseDe`, set `__init__.py`), qui choisit la cible pour le joueur.
#
# Cartes de reference : 01017 (bonus attache) ; fiche mots-cles/overkill.md (`UnitAttackGainKeyword(.., overkill=True)`) ; 62009 (Response a la jouee).
def GetAbilities() -> Sequence['Ability']:
    return [
        *AbilityFactory.GiveKeywordToAttached(CardFinder(name="Smasher"), attack=2),
        AbilityFactory.UnitAttackGainKeyword("You", overkill=True),
    ]
