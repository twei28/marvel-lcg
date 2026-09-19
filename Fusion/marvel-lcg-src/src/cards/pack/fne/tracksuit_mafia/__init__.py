from cards.pack import *


def TrouverTracksuitMafia(effect: 'Effect') -> 'EncounterSideScheme|None':
    return Worlds.FindCardOnField(effect, name="Tracksuit Mafia", card_type=EncounterSideScheme)
