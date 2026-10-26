from . import *

# Break The Prison (POTENTIAL ALLY, Polaris). Victory 1. Assault (desc).
# [star] Boost: After this activation, reveal this card.
# When Defeated : Polaris.
#
# Carte de reference : 04092 Super Absorbing Power (`WhenCardBecomeBoost("This", ...)` ; `RevealThisCard`) ;
# `message.AfterThisActivation(effect, fn)` (boost.py:161, `WhenBoostShuffleThisIntoEncounterDeckAfterActivationEnd`) pour « after this activation ».
def GetAbilities() -> Sequence['Ability']:
    def prison_boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        # « After this activation, reveal this card » : `message.AfterThisActivation` (modele boost.py:161, WhenBoostShuffleThis...).
        message.AfterThisActivation(
            effect,
            lambda:
                RevealThisCard(effect, message)
        )

    return [
        AbilityFactory.WhenCardBecomeBoost("This", prison_boost),
        AbilitePotentialAlly("Polaris"),
    ]
