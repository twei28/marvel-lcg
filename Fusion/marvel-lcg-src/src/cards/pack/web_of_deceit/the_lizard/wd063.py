from . import *

# Giant Alligator

def GetAbilities() -> Sequence['Ability']:

    def revelation(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        # « When Revealed: Discard the top 5 cards of your deck. »
        message.GetToPlayer().DiscardDeckTopCards(5, effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            revelation
        ),
    ]
