from . import *
def GetAbilities() -> Sequence['Ability']:
    def suit_up(effect: 'Effect', message: 'Message.AfterCardsBeSpendAsResource') -> None:
        this = effect.this.CastTo(Resource)
        Unused(this)
        leader = Worlds.FindCardOnField(effect, name='Iron Man', card_type=Leader)
        if leader:
            Faces.GiveStatus([leader], 'Tough', effect)
    return [AbilityFactory.AfterYouSpendThisCard(AbilityType.HeroResponse, suit_up)]
