# Recovered automatically from Python 3.10 bytecode.
# Comments and original formatting were not present in the compiled file.

from . import *
def GetAbilities() -> Sequence['Ability']:
    def find_and_gain_shield(effect: 'Effect', message: 'Send.WhenCardSetup') -> None:
        initiator = effect.GetInitiator()
        Search.SearchForCards(effect, (initiator.player_deck.Get(True) + initiator.discard_pile.Get(True)), lambda face: face.Discard(effect), name="Captain America's Shield", card_type=Upgrade)
        assert False, '!!!'
    return [AbilityFactory.WhenCardSetup(find_and_gain_shield)]
