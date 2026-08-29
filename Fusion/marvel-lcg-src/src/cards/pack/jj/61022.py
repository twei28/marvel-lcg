from . import *
def GetAbilities() -> Sequence['Ability']:
    def determination(effect: 'Effect', message: 'Message.AfterCardsBeSpendAsResource') -> None:
        this = effect.this.CastTo(Resource)
        this.RemoveThreatFromSchemes("MainScheme", 1, effect)
    return [AbilityFactory.AfterYouSpendThisCard(AbilityType.HeroResponse, determination)]
