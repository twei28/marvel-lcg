from . import *

# * Cannonball (Sam Guthrie), ALLIE — X-FORCE. Cout 3, PV 3, ATK 2 (2 etoiles), THW 2 (2 etoiles).
# Response: After Cannonball attacks, reduce the cost of the next card you play this phase by 1.
#
# CARTES DE REFERENCE
#  - `05008` Nakia Bahadir : `Worlds.UpdateNextCardPlayCost(joueur, -1, effect, in_this="Phase")` (la prochaine carte de la phase).
#  - `01028` Superhuman Strength : `AfterUnitAttackEnd(type, finder, op)` pour « after X attacks ».
#  - `sz002` Cannonball (Smasher) : meme valeur de stats « 2** » (deux etoiles).
#
# TEXTE CONTRE CODE
#  ⚠ « the NEXT card you play THIS PHASE » : une seule carte, la phase en cours (`in_this="Phase"`).
#  ⚠ « After Cannonball attacks » : seulement ses propres attaques.


def GetAbilities() -> Sequence['Ability']:

    def cannonball(effect: 'Effect', message: 'Message.AfterUnitAttackEnd') -> None:
        Unused(message)
        joueur = JoueurQuiControle(effect)
        if joueur is None:
            return
        Worlds.UpdateNextCardPlayCost(joueur, -1, effect, in_this="Phase")

    return [
        AbilityFactory.AfterUnitAttackEnd(
            AbilityType.Response,
            "This",
            cannonball,
        ),
    ]
