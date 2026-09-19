from . import *

# * Master Key (ITEM) — Attach to the villain. Permanent (base).
# [star] Forced Response: After the villain schemes against you, deal each of
#   that activation's boost cards that is a minion to yourself as a facedown
#   encounter card.

def GetAbilities() -> Sequence['Ability']:

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        DistribuerLesBoostsDeCeType(effect, message, Minion, attaque=False, vilain_seulement=True)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(Villain),
        AbilityFactory.WhenCardBecomeBoost(None, boost),
    ]
