from . import *
def GetAbilities() -> Sequence['Ability']:
    def raw_power(effect: 'Effect', message: 'Message.AfterCardsBeSpendAsResource') -> None:
        this = effect.this.CastTo(Resource)
        Unused(this)
        attachment = Worlds.FindCardOnField(effect, name='Energy Channel')
        if attachment:
            attachment.PlaceCountersInternal(2, 'energy', effect)
    return [AbilityFactory.AfterYouSpendThisCard(AbilityType.HeroResponse, raw_power)]
