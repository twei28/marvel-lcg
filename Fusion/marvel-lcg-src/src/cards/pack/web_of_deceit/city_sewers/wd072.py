from . import *

# Ceiling Collapse

def GetAbilities() -> Sequence['Ability']:

    def revelation(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        # « When Revealed: Reveal the top card of the encounter deck. »
        Worlds.RevealEncounterDeckTopCard(message.GetToPlayer(), effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        # « [star] Boost: Deal yourself 1 facedown encounter card. »
        message.GetToPlayer().DealEncounterCards(1, effect)

    return [
        Negate(2),
        AbilityFactory.WhenThisRevealed(
            None,
            revelation
        ),
        AbilityFactory.WhenCardBecomeBoost(
            "This",
            boost
        ),
    ]
