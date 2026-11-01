from . import *

# Emma Frost, face A2 (standard, face RETOURNEE, PV infinis : `desc.HP = INF`). « [star] Forced Interrupt : When Emma Frost would activate, discard 2 cards
# from the top of the encounter deck instead. Forced Response : After the end of the villain phase, flip this card, then set Emma Frost's hit point dial
# to her printed hit points. »
# Cartes de reference : sl037 Shifting Corridors (`WhenEnemyWouldActivate` + `SetBeInstead`, PV infinis), can_health.py `OnFlip` (une carte qui quitte une
# face a PV infinis retrouve ses PV : le « set hit point dial » imprime), 16080a (retournement).


def GetAbilities() -> Sequence['Ability']:
    def avant_activation(effect: 'Effect', message: 'Message.WhenEnemyWouldActivate') -> None:
        message.SetBeInstead(effect)
        Worlds.DiscardEncounterCards(2, effect)

    return [
        AbilityFactory.WhenEnemyWouldActivate(AbilityType.ForcedInterrupt, "This", avant_activation),
        RetourSurLaFaceActive(),
    ]
