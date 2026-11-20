from . import *

# * Marrow (Sarah Rushman) : allie RECRUITED, cout 1, PV 2, THW 1*, ATK 1*.
# Response: After Marrow attacks an enemy, spend a [physical] resource -> stun that enemy.
#
# Cartes de reference : 04100 Elektra (`SetCost(Cost("R"))` : depenser une ressource physique), 01083 Mockingbird (`GiveStatus "Stunned"`),
# `AfterUnitAttackUnit` (do_attack.py, `message.attacked` = la cible).
def GetAbilities() -> Sequence['Ability']:
    def marrow(effect: 'Effect', message: 'Message.AfterUnitAttackUnit') -> None:
        cible = message.attacked
        if cible is not None and cible.IsInPlay():
            Faces.GiveStatus([cible], "Stunned", effect)

    return [
        AbilityFactory.AfterUnitAttackUnit(
            AbilityType.Response,
            "This",
            Enemy,
            marrow,
        ).SetCost(Cost("R")),
    ]
