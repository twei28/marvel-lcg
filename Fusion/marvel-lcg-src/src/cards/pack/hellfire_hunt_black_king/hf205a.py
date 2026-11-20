from . import *

# Operation Hellfire Ascendant (2A). « When Revealed : Deal each player a facedown encounter card. Flip Black King attachment. »
# Cartes de reference : tk007a (`card.Flip(effect)` d'un attachement a deux faces), 01121 / hf124 (`DealEncounterCards`).


def GetAbilities() -> Sequence['Ability']:
    def revelee(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        for joueur in Worlds.GetPlayers(effect):
            joueur.DealEncounterCards(1, effect)
        roi = BlackKing(effect)
        if roi is not None:
            roi.card.Flip(effect)

    return [AbilityFactory.WhenThisRevealed(None, revelee)]
