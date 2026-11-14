from . import *

# * Captain Britain (Brian Braddock) : allie Leadership, cout 5, PV 4, THW 2**, ATK 2**. AERIAL. EXCALIBUR.
# Response: After your turn begins, search the top 5 cards of your deck for an ally card and add it to your hand. Shuffle your deck.
#
# Cartes de reference : 22001a / rm002 (`AfterPlayerTurnBegin(Response, "You", ...)`), 04141 Prison Camps (`Search.PlayerCard(...)`),
# `most_top=5` (search.py). Le melange est fait par `Search`.
def GetAbilities() -> Sequence['Ability']:
    def captain_britain(effect: 'Effect', message: 'Message.AfterPlayerTurnBegin') -> None:
        joueur = JoueurDe(effect)
        face = Search.PlayerCard(
            effect,
            joueur,
            include_player_deck=True,
            most_top=5,
            card_type=Ally,
        )
        if face:
            joueur.GainCard(face, effect)

    return [
        AbilityFactory.AfterPlayerTurnBegin(
            AbilityType.Response,
            "You",
            captain_britain,
        ),
    ]
