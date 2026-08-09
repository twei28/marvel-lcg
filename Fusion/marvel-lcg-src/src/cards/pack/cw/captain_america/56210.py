from . import *
def GetAbilities() -> Sequence['Ability']:
    def peoples_hero(effect: 'Effect', message: 'Message.AfterCardsBeSpendAsResource') -> None:
        this = effect.this.CastTo(Resource)
        Unused(this)
        leader = Worlds.FindCardOnField(effect, name='Captain America', card_type=Leader)
        if leader:
            Faces.GiveFacedownBoostCards([leader], 1, effect)
    return [AbilityFactory.AfterYouSpendThisCard(AbilityType.HeroResponse, peoples_hero)]
