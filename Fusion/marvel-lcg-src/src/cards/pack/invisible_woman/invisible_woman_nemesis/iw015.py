from . import *


def GetAbilities() -> Sequence['Ability']:

    def blank_this(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        this.TemporaryGain(effect, message, treat_as_blank=True)

    return [
        AbilityFactory.PlayersCannotChangeForms(AbilityType.NonKeyword, "EachPlayer"),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            blank_this,
        ).SetCostFunc(CostFunc.Discard("YourHandCards", range=(2, 2)))
        .SetName("Resist Manipulation"),
    ]
