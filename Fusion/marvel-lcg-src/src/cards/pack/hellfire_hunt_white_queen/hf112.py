from . import *

# Illusory Sentinel (x2). Sbire ILLUSION, Quickstrike + Steady (desc). « [star] Illusory Sentinel's attacks gain overkill. [star] Boost : If this
# activation is an attack, this card gets +2 boost icons for this activation. »
# Carte de reference EXACTE : 16121 Badoon Warlord (`UnitAttackGainKeyword("This", overkill=True)` + `message.GainBoostIcon(2, effect)` pendant une attaque).


def GetAbilities() -> Sequence['Ability']:
    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        message.GainBoostIcon(2, effect)

    return [
        AbilityFactory.UnitAttackGainKeyword("This", overkill=True),
        AbilityFactory.WhenCardBecomeBoost("This", boost, during_attack=True),
    ]
