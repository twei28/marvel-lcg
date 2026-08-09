from . import *
def GetAbilities() -> Sequence['Ability']:
    def secret_contact(effect: 'Effect', message: 'Message.AfterCardsBeSpendAsResource') -> None:
        this = effect.this.CastTo(Resource)
        Unused(this)
        attachment = Worlds.FindCardOnField(effect, name='Finesse')
        if attachment:
            attachment.PlaceCountersInternal(2, 'skill', effect)
    return [AbilityFactory.AfterYouSpendThisCard(AbilityType.HeroResponse, secret_contact)]
