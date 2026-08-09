from . import *

# For The Queen! — custom « DesignHacker »
# Hinder 1 per player (desc).
# While Lady Hellbender is in play, MONSTER minions gain villainous.


def GetAbilities() -> Sequence['Ability']:

    def hellbender_en_jeu(effect: 'Effect') -> bool:
        return Worlds.FindCardOnField(effect, CardFinder(name="Lady Hellbender")) is not None

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            CardFinder2("MONSTER", Minion),
            condition=hellbender_en_jeu,
            villainous=1,
        ),
    ]
