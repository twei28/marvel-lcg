from . import *

# Silent Takeover (2B), stade 2. Menace 11[per_hero], escalade +1[per_hero], menace de depart 2[per_hero].
# « Forced Response : After your turn ends, if there is Cassandra Controls counter on your identity, you must choose to either place 2 threat here
# or deal yourself 1 facedown encounter card. Hero Action : Discard 6 cards from the top of the encounter deck -> remove a Cassandra Controls
# counter from your identity. (Limit once per round per player.) »
# Cartes de reference : hf604b (meme squelette), `Player.DealEncounterCards` (modele hf118 / sk).


def GetAbilities() -> Sequence['Ability']:
    return [
        ReponseFinDeTour(2, "Deal yourself 1 facedown encounter card", PenaliteCarteRencontre),
        ActionRetirerControle(6),
    ]
