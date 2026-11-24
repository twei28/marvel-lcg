from . import *
# * Christopher Summers, face alter ego. Prefixe `cr`.
#
# You may include STARJAMMER allies from any aspect in your deck.   -> deckbuilder (regles.js, id `corsair`).
# Setup: Find Corsair's Rapier and add it to your hand.
#
# Cartes de reference : ok001b (`WhenCardSetup` + `Search.PlayerCard(include_player_deck=True)` + `GainCard`).
# FAQ de l'auteur : « player setup abilities resolve after mulligans » : c'est le comportement du moteur.
def GetAbilities() -> Sequence['Ability']:
    def setup(effect: 'Effect', message: 'Message.WhenCardSetup') -> None:
        initiator = effect.GetInitiator()
        if initiator is None:
            return
        face = Search.PlayerCard(effect, initiator, include_player_deck=True, name="Corsair's Rapier")
        if face:
            initiator.GainCard(face, effect)
    return [
        AbilityFactory.WhenCardSetup("This", setup).SetName("Setup"),
    ]
