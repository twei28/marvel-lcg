from . import *

# Alcohol Problems (obligation, boost 2)
# Give to the Zeus Panhellenios player.
# Zeus cannot resolve his "Skyfather's Tempest" ability.
# Alter-Ego Action: Exhaust your identity and spend a [lightning] resource →
# remove Alcohol Problems from the game.
#
# « Give to » est une base automatique (`desc.GiveTo`). L'interdiction n'est
# pas codee ici : le Tempest (`ze001a`) consulte `AlcoholProblemsDe(joueur)`
# dans ses conditions tant que la carte est en jeu. Ce module ne porte que
# l'action qui la retire, sur le modele de sg022 (action d'alter ego a cout
# double) et de `PlayerActionToRemoveThisFromGame` (attachment.py:29).
#
# ⚠ Elle coute la ressource la plus RARE du deck, un eclair : Thunder Strike
# defaussee, ou Mount Olympus (qui reclame lui-meme une energie).

def GetAbilities() -> Sequence['Ability']:

    return [
        AbilityFactory.PlayerActionToRemoveThisFromGame(
            AbilityType.AlterEgoAction,
        ).SetCostFunc(CostFunc.Exhaust("YourIdentity"))
        .SetCostFunc(CostFunc.Spend(Cost("L"))),
    ]
