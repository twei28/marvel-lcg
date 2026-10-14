from . import *
from cards.pack.mojo import DiscardEachSettingAndGainSurge

# Wild Wild Mojo

def GetAbilities() -> Sequence['Ability']:

    def wild_wild_mojo(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        this = effect.this.CastTo(Environment)
        Unused(this)

        # RR 1.8 FAQ : +1 sur les degats initiaux, puis +1 sur l'exces d'overkill (+2 au total).
        message.IncreaseDamage(1, effect, inclure_overkill=True)


    return [
        AbilityFactory.UnitAttackGainKeyword(
            Enemy,
            overkill=True
        ),
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.ForcedInterrupt,
            None,
            wild_wild_mojo,
            # include_overkill=False
        ),
        DiscardEachSettingAndGainSurge()
    ]

