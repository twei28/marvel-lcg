from . import *

# Pulling The Strings — custom « DesignHacker » (side scheme némésis)
# The minion in play with the lowest SCH gets +1 ATK and +1 SCH.

def GetAbilities() -> Sequence['Ability']:

    def sbire_le_plus_faible(effect: 'Effect', unit: 'CardFace') -> int:
        """1 pour le sbire au SCH le plus bas, 0 pour les autres."""
        if not Minion.IsType(unit):
            return 0
        sbires = Worlds.FindCardsOnField(effect, card_type=Minion)
        if not sbires:
            return 0
        mini = min(x.scheme for x in sbires)
        return 1 if unit.scheme == mini else 0

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            CardFinder(card_type=Minion),
            get_new_value=sbire_le_plus_faible,
            attack=1,
            scheme=1,
        ),
    ]
