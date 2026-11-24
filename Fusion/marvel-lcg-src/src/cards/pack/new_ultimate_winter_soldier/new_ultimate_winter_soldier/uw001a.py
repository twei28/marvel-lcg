from . import *

# * Winter Soldier (face HEROS) — EARTH-6160. OPPOSITION. SOLDIER. PV 10, THW 2, ATK 2, DEF 2, main 5.
# Healing Factor — Response: After the villain phase begins, heal 2 damage.
#
# Carte de reference : `35001a` * Wolverine (meme « Healing Factor », meme cible `YourHero`, `canbe_heal=True`) ;
# la seule difference imprimee est le MOMENT : « the VILLAIN phase begins » (35001a : « the player phase begins »).
# `AfterPhaseBegin(Response, "Villain", ...)` : modeles `53011`, `45032`, `18025` (« After the villain phase begins »).


def GetAbilities() -> Sequence['Ability']:

    def healing_factor(effect: 'Effect', message: 'Message.AfterPhaseBegin') -> None:
        this = effect.this.CastTo(Hero)
        this.HealthUnits(effect.targets, 2, effect)

    return [
        AbilityFactory.AfterPhaseBegin(
            AbilityType.Response,
            "Villain",
            healing_factor,
        ).SetTarget("YourHero", canbe_heal=True)
        .SetName("Healing Factor"),
    ]
