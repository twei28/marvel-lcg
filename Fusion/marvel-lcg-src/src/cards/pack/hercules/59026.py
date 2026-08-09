from . import *
def GetAbilities() -> Sequence['Ability']:
    def ancient_rivalry(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)
        initiator = effect.GetInitiator()
        face = Search.PlayerCard(effect, initiator, include_player_deck=False, include_discard_pile=True, may=True, finder=CardFinder(card_type=Upgrade, card_class='IdentitySpecific'))
        if face:
            Faces.AddToHand([face], initiator, effect)
        for name in ('Hercules', 'Thor'):
            hero = Worlds.FindCardOnField(effect, name=name, card_type=Hero)
            if hero:
                Faces.ReadyAll([hero], effect)
    return [AbilityFactory.WhenInYourPlayTurn(AbilityType.HeroAction, ancient_rivalry).SetPlay().SetLabel().SetTarget('TeamUp')]
