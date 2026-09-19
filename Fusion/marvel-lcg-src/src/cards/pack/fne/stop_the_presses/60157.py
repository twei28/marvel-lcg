from . import *

# Exclusive Interview (side scheme 6)
# DAILY BUGLE supports cannot ready.
# When Revealed: Exhaust each DAILY BUGLE support.

def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        soutiens = SoutiensDailyBugle(effect)
        if soutiens:
            Faces.ExhaustAll(soutiens, effect)

    return [
        *AbilityFactory.CardCannotReady(CardFinder(trait="DAILY BUGLE", card_type=Support)),
        AbilityFactory.WhenThisRevealed(None, revele),
    ]
