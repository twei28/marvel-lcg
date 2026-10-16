from . import *

# * Eastman Theater

def GetAbilities() -> Sequence['Ability']:

    def apres_defaite(effect: 'Effect', message: 'Message.AfterSchemeBeDefeated') -> None:
        Faces.ReadyAll(effect.targets, effect)

    return [
        AbilityFactory.AfterSchemeBeDefeated(
            AbilityType.HeroResponse,
            CardFinder(card_type=EncounterSideScheme, trait="NYC"),
            apres_defaite,
        ).SetCostFunc(CostFunc.Exhaust("This")).SetTarget(Hero),
    ]
