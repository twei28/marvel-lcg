from . import *

# * Selene (Selene Gallio) : allie RECRUITED, cout 4, PV 2, THW 1*, ATK 3*. [star] Response.
# Response: After Selene attacks and defeats a minion, heal 2 damage from her.
#
# Carte de reference : `AfterUnitAttackAndDefeatUnit` (defeated.py:285).
def GetAbilities() -> Sequence['Ability']:
    def selene(effect: 'Effect', message: 'Message.AfterUnitDefeatedUnit') -> None:
        this = effect.this.CastTo(Ally)
        this.HealthUnits([this], 2, effect)

    return [
        AbilityFactory.AfterUnitAttackAndDefeatUnit(
            AbilityType.Response,
            "This",
            Minion,
            selene,
        ),
    ]
