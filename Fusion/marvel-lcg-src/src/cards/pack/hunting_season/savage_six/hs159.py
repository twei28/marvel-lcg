from . import *

# hs159 * Rhino
# [star] Ses attaques gagnent overkill. Forced Interrupt : a la fin de la phase du mechant, donnez-lui un statut tough.
# Boost : cette attaque gagne overkill.

def GetAbilities() -> Sequence['Ability']:

    def surdegats(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        message.GainOverKill(effect)

    def robuste(effect: 'Effect', message: 'Message.WhenPhaseEnd') -> None:
        Faces.GiveStatus([effect.this], "Tough", effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        atk = getattr(message, "would_atk_message", None)
        if atk is not None:
            atk.GainOverKill(effect)

    return [
        AbilityFactory.WhenUnitWouldAttack(AbilityType.NonKeywordStar, "This", surdegats),
        AbilityFactory.WhenPhaseEnd(AbilityType.ForcedInterrupt, "Villain", robuste),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
