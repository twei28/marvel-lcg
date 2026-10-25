from . import *

# * Colonel Dillon — SBIRE (set « Predator Alt Nemesis »). SOLDIER. PV 4, MNG 1, ATQ 2★, Boost 2. Patrol. Teamwork (SOLDIER).
# ★ Forced Response: After Colonel Dillon attacks you, place 1 threat on each scheme.
#
# Cartes de reference :
#  - `AfterUnitAttackEnd(ForcedResponse, "This", op, against_who="You")` (do_attack.py) pour « after X attacks you » ;
#    `27094` : `this.PlaceThreatOnSchemes("EachScheme", 1, effect)` ;
#  - `Patrol` et `Teamwork` : bases automatiques (`desc`, fiches patrol.md, teamwork.md).
#
# ⚠ Mots-pieges :
#  - « After Dillon ATTACKS YOU » : une ATTAQUE contre le joueur (pas une manigance, pas une attaque contre un allie) ;
#  - « on EACH scheme » : principal + annexes, 1 menace chacune ; « Teamwork (SOLDIER) » : le trait de Dutch Schaefer / Dillon.


def GetAbilities() -> Sequence['Ability']:

    def menace_partout(effect: 'Effect', message: 'Message.AfterUnitAttackEnd') -> None:
        this = effect.this.CastTo(Minion)
        Unused(message)
        this.PlaceThreatOnSchemes("EachScheme", 1, effect)

    return [
        AbilityFactory.AfterUnitAttackEnd(
            AbilityType.ForcedResponse,
            "This",
            menace_partout,
            against_who="You",
        ),
    ]
