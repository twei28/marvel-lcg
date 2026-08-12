from . import *

# * Cassandra Webb — custom « Kajislav »
# Arachnophilia — You may include allies with the WEB-WARRIOR trait or with
#   "Spider" in their title from any aspect in your deck.
#   (Regle de construction de deck : appliquee par le deck-builder, pas par le
#   moteur, qui ne valide pas les decks. Rien a scripter ici.)
# Setup: Search your deck and discard pile for the Life-Support System upgrade
#   and put it into play.

def GetAbilities() -> Sequence['Ability']:

    def setup(effect: 'Effect', message: 'Message.WhenCardSetup') -> None:
        initiator = effect.GetInitiator()

        face = Search.PlayerCard(
            effect,
            initiator,
            include_player_deck=True,
            include_discard_pile=True,
            name="Life-Support System",
            card_type=Upgrade,
        )
        if face:
            face.PutIntoPlay(initiator, effect)

    return [
        AbilityFactory.WhenCardSetup(
            "This",
            setup
        ),
    ]
