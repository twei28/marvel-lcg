from . import *
from cards.pack.synthezoid import GetSetAsideLeaderBasics
def GetAbilities() -> Sequence['Ability']:
    def setup(effect: 'Effect', message: 'Message.WhenCardSetup') -> None:
        this = effect.this.CastTo(MainScheme)
        Unused(this)
        first_player = Worlds.GetFirstPlayer(effect)
        face = Search.EncounterCard(effect, first_player, include_discard_pile=False, include_set_aside=True, card_type=EncounterSideScheme, name='Just Passing Through')
        if face:
            face.Reveal(first_player, effect)
        if GetSetAsideLeaderBasics(effect):
            card = CardFactory.GenerateCard('57039a,57039b', None, effect.world)
            card.face.Reveal(first_player, effect)
    return [AbilityFactory.WhenCardSetup('This', setup)]
