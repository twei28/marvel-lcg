from . import *

# * Intelligentsia — SBIRE (Skrull Empire). SKRULL. SCH 2, ATK ★, 5 PV,
# 1 icone Acceleration, 2 boosts.
# Each other SKRULL enemy gets +1 SCH.
# ★ Forced Interrupt: When Intelligentsia would attack, she schemes instead.
#
# Cartes de reference : **`40146`** / `39012a` : `WhenUnitWouldAttack(
# ForcedInterrupt, "This", op)` + `message.DoSchemeInstead(effect)` ;
# `GiveKeywordToInPlayWhenApplyThis(..., scheme=1, not_include_this=True)`.
#
# ⚠ Mots-pieges : « each OTHER » (pas elle) ; « SKRULL ENEMY » : sbires ET
# mechant ; ATK ★ = renvoi au texte (desc « 0* »). Acceleration : desc, natif.


def GetAbilities() -> Sequence['Ability']:

    def complote(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        message.DoSchemeInstead(effect)

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(CardFinder2("SKRULL", Enemy), scheme=1, not_include_this=True),
        AbilityFactory.WhenUnitWouldAttack(AbilityType.ForcedInterrupt, "This", complote),
    ]
