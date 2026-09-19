from . import *

# Maggia Enforcers (CRIMINAL, MAGGIA) — Guard : base automatique.
# [star] Maggia Enforcers's SCH is equal to the number of MAGGIA enemies in
#   play (including this one).
#
# SCH imprime = 0 (etoile), +1 par ennemi MAGGIA en jeu, lui compris. Modele :
# 24016 Mandrill (ThisGainKeywordForEachFaceInPlay), rafraichi par defaut a
# chaque entree/sortie d'une carte du filtre (OnEvent.CardInPlay).

def GetAbilities() -> Sequence['Ability']:
    return [
        AbilityFactory.ThisGainKeywordForEachFaceInPlay(
            CardFinder(trait="MAGGIA", card_type=Enemy),
            scheme=1,
        ),
    ]
