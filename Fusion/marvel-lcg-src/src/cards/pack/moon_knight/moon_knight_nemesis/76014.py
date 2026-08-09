from . import *

# Mano a Mano — custom « DesignHacker » (némésis de Moon Knight)
# Moon Knight and Mr. Knight get -1 ATK.


def GetAbilities() -> Sequence['Ability']:

    def cette_manigance_en_jeu(effect: 'Effect') -> bool:
        return effect.this.IsInPlay()

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            CardFinder(name="Moon Knight", card_type=Hero),
            condition=cette_manigance_en_jeu,
            attack=-1,
        ),
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            CardFinder(name="Mr. Knight", card_type=Hero),
            condition=cette_manigance_en_jeu,
            attack=-1,
        ),
    ]
