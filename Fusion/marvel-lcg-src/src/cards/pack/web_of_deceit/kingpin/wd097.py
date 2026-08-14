from . import *

# Long Live the King

def GetAbilities() -> Sequence['Ability']:

    def revelation(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        # « When Revealed: Put the top card of your deck into play facedown as a
        # CORRUPT side scheme. Place 1 pursuit counter on Pursued by the Past. »
        PoserUneManiganceCorrompue(message.GetToPlayer(), effect)
        CompteursDePoursuite(effect, 1)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            revelation
        ),
    ]
