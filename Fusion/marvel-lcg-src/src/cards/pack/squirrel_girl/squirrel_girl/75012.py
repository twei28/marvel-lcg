from . import *

# * Network of Trees
# Interrupt: When you would call a Squirrel, exhaust Network of Trees → look at
#   the top 2 cards of the Squirrel deck. Call 1 of them and put the other on
#   the bottom of the Squirrel deck.
#
# Le moteur n'a pas de message « quand tu appellerais un ecureuil » : appeler
# est une notion maison du pack. L'interruption est donc resolue dans
# AppelerEcureuil (voir __init__.py), seul point de passage de tous les appels,
# qui verifie la presence de cette carte prete sous le controle du joueur.
# Cette carte ne porte donc que sa capacite de mise en jeu. Ecart documente §9.

def GetAbilities() -> Sequence['Ability']:

    return [
        AbilityFactory.CanPlayThisSupportCard(),
    ]
