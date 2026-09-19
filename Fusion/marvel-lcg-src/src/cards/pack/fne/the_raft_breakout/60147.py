from . import *

# * Mysterio (CRIMINAL, ELITE, PRISONER) — Villainous : base.
# [star] Forced Response: After Mysterio attacks you, deal each of that
#   activation's boost cards that is a treachery to yourself as a facedown
#   encounter card.

def GetAbilities() -> Sequence['Ability']:

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        DistribuerLesBoostsDeCeType(effect, message, Treachery, attaque=True, vilain_seulement=False)

    return [
        AbilityFactory.WhenCardBecomeBoost(None, boost),
    ]
