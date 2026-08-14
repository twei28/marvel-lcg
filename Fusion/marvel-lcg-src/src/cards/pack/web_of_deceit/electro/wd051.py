from . import *

# High Voltage

def GetAbilities() -> Sequence['Ability']:

    def alter_ego(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        # « When Revealed (Alter-Ego): Discard the top 5 cards of your deck. »
        message.GetToPlayer().DiscardDeckTopCards(5, effect)

    def heros(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        # « When Revealed (Hero): Discard the top 5 cards of the encounter
        # deck. » La carte punit les deux formes, mais pas la meme pile.
        Worlds.DiscardEncounterCards(5, effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        # « [star] Boost: Discard the top 3 cards of the encounter deck. »
        Worlds.DiscardEncounterCards(3, effect)

    return [
        AbilityFactory.WhenThisRevealed(
            "Alter-Ego",
            alter_ego
        ),
        AbilityFactory.WhenThisRevealed(
            "Hero",
            heros
        ),
        AbilityFactory.WhenCardBecomeBoost(
            "This",
            boost
        ),
    ]
