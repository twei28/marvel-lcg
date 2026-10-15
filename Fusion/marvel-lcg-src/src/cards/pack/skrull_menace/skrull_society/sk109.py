from . import *

# Skrull Telepath — SBIRE (Skrull Society). PSIONIC. SKRULL. SCH 2, ATK ★, 3 PV.
# ★ Forced Interrupt: When Skrull Telepath would attack, it schemes instead.
# ★ Boost: If this activation is a scheme, reveal this card.
#
# Cartes de reference : **`40146`** (`DoSchemeInstead`) ; **`16140`**
# (boost `RevealThisCard`) + `during_scheme=True` (factory/boost.py).
# ⚠ « If this activation is a SCHEME » : rien pendant une attaque.


def GetAbilities() -> Sequence['Ability']:

    def complote(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        message.DoSchemeInstead(effect)

    return [
        AbilityFactory.WhenUnitWouldAttack(AbilityType.ForcedInterrupt, "This", complote),
        AbilityFactory.WhenCardBecomeBoost("This", RevealThisCard, during_scheme=True),
    ]
