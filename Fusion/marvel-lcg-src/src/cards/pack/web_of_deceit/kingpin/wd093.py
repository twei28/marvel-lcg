from . import *

# * Kingpin (III)

def GetAbilities() -> Sequence['Ability']:

    def revelation(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        # « When Revealed: Each player puts the top card of their deck into play
        # facedown as a CORRUPT side scheme. Search the encounter deck and
        # discard pile for Kingpin's Suit and reveal it. »
        Players.ForEachPlayer(
            effect, lambda joueur: PoserUneManiganceCorrompue(joueur, effect))
        ChercherEtReveler(effect, name="Kingpin's Suit")

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            revelation
        ),
    ]
