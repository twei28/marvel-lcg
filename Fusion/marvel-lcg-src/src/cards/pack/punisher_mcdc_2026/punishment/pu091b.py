from . import *

# Target Lock (6B, DISTRACTED) — ATTACHEMENT. Permanent. Attach to Punisher. SCH +★, ATQ +1.
# ★ Forced Interrupt : When Punisher would scheme, flip this card instead.
# Forced Interrupt : At the end of the round, flip this card.
#
# Cartes de reference : `AbilityFactory.WhenUnitWouldScheme` + `message.SetBeInstead` (pu059), `AfterRoundEnd`/`WhenRoundEnd`
# (turn_phase.py), `RetournerLAttachement` (fne/__init__.py : un attachement recto-verso ne se perd pas au retournement).
# ⚠ « flip this card INSTEAD » : Punisher ne manigance pas, la carte revient FOCUSED ; « At the END OF THE ROUND » : chaque
# manche, la carte DISTRACTED revient FOCUSED ; ATQ +1 : natif (`desc`).

def GetAbilities() -> Sequence['Ability']:

    def au_lieu_de_comploter(effect: 'Effect', message: 'Message.WhenUnitWouldScheme') -> None:
        message.SetBeInstead(effect)
        RetournerTargetLockVersFocused(effect)

    def fin_de_manche(effect: 'Effect', message: 'Message.WhenRoundEnd') -> None:
        RetournerTargetLockVersFocused(effect)

    return [
        AbilityFactory.WhenUnitWouldScheme(AbilityType.ForcedInterrupt, CardFinder(name="Punisher"), au_lieu_de_comploter),
        AbilityFactory.WhenRoundEnd(AbilityType.ForcedInterrupt, None, fin_de_manche),
    ]
