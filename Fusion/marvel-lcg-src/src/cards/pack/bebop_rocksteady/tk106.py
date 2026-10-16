from . import *

# * Channel 6 News

def GetAbilities() -> Sequence['Ability']:

    def apres_revelation(effect: 'Effect', message: 'Message.AfterCardRevealedEnd') -> None:
        effect.this.RemoveThreatFromSchemes(effect.targets, 2, effect)

    return [
        AbilityFactory.AfterPlayerRevealCard(
            AbilityType.Response, "AnyPlayer",
            CardFinder(card_type=EncounterSideScheme, trait="NYC"),
            apres_revelation,
        ).SetCostFunc(CostFunc.Exhaust("This")).SetTarget(Scheme2),
    ]
