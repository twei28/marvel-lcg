from . import *

def GetAbilities() -> Sequence['Ability']:
    def apres_un_sbire_vaincu(effect: 'Effect', message: 'Message.AfterUnitDefeatedUnit') -> None:
        Unused(message)
        PlusUneTailleDeMain(effect, IdentiteDe(effect))

    return [
        AbilityFactory.UnitAttackGainKeyword(
            "You",
            overkill=True,
        ),
        AbilityFactory.AfterUnitDefeatedUnit(
            AbilityType.HeroResponse,
            "You",
            Minion,
            apres_un_sbire_vaincu,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
