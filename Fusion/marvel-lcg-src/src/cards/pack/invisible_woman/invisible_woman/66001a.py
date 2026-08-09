from . import *


def GetAbilities() -> Sequence['Ability']:

    def boo(effect: 'Effect', message: 'Message.AfterUnitAttackEnd') -> None:
        ChangeToPsionicForm(effect.GetInitiator(), effect)

    return [
        AbilityFactory.AfterUnitAttackEnd(
            AbilityType.ForcedResponse,
            "You",
            boo,
            against_who=Enemy,
        ).SetName("Boo!"),
    ]
