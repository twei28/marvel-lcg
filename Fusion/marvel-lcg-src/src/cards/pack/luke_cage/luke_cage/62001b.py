from . import *
def GetAbilities() -> Sequence['Ability']:
    def search_burstein(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(AlterEgo)
        Unused(this)
        player = effect.GetInitiator()
        face = Search.SearchForCard(effect, player, include_player_deck=True, include_player_discard_pile=True, name='Burstein Process', card_type=Upgrade)
        if face:
            face.card.MoveToArea(player.hand_cards, effect)
    return [
        AbilityFactory.ThisCanHaveAdditionalTough("Any"),
        AbilityFactory.UnitAttackGainKeyword(None, "This", lost_piercing=True),
        AbilityFactory.WhenInYourPlayTurn(AbilityType.Action, search_burstein)
        .SetName("Unbreakable Skin").LimitOncePerPhase(),
    ]
