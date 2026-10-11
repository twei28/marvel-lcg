from . import *

# Melee in the Mojo-seum

def GetAbilities() -> Sequence['Ability']:

    def melee_in_the_mojo_seum(effect: 'Effect', message: 'Message.WhenMainSchemeStageWouldBeCompleted') -> None:
        this = effect.this.CastTo(MainScheme)

        # Ruling FFG n°32 + RR 1.8 p.11 : « cannot » l'emporte. Si la menace ne
        # peut pas etre retiree (Crime Scene Investigation), l'Interruption
        # ne se resout pas : pas de cotes, la manigance se complete.
        before = this.threat
        this.RemoveThreatFromSchemes([this], before, effect)
        if this.threat >= before:
            return

        message.SetBeInstead(effect)

        champion = FindTheChampion(effect)
        if champion:
            Faces.PlaceCountersOn([champion], "2*", 'ratings', effect)

    return [
        # TODO: The players cannot win the game unless they wow the crowd as The Challengers.
        AbilityFactory.WhenMainSchemeStageWouldBeCompleted(
            AbilityType.WhenCompleted,
            "This",
            melee_in_the_mojo_seum
        ),
    ]

