from . import *
def GetAbilities() -> Sequence['Ability']:
    # `gain_hunted` retire le 4/8/2026 : stub vide jamais branche, le trait
    # HUNTED est deja donne par GiveKeywordToAttached juste en dessous.
    def discard_this(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Obligation)
        initiator = effect.GetInitiator()
        for _ in range(8):
            top = initiator.player_deck.GetTop()
            if not top:
                break
            Faces.DiscardAll([top], effect)
        Faces.DiscardAll([this], effect)
    return [*AbilityFactory.GiveKeywordToAttached('You', trait='HUNTED'),
            AbilityFactory.WhenInYourPlayTurn(AbilityType.AlterEgoAction, discard_this)]
