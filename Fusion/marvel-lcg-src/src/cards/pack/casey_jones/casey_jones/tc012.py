from . import *

# Persuader — AMELIORATION, cout 2, [physical]. WEAPON. Restricted.
# Your hero gets +1 ATK.
# Hero Interrupt: When you make a basic attack, exhaust Persuader → you get +1
#   ATK for that attack. This attack gains piercing.
#
# MOT-CLE : RESTRICTED — fiche `restricted.md` ; PIERCING — fiche `piercing.md`
# (« this attack gains piercing » = `message.GainPiercing(effect)` sur le
# message d'attaque).
#
# CARTES DE REFERENCE
#  - `tc009` Cricket Willow : « Your hero gets +1 ATK » =
#    `GiveKeywordToAttached(Hero, attack=1)`.
#  - `ar004` (ares) / `ho016` : `WhenUnitWouldAttack(..., is_basic_attack=True)`
#    + `message.GainPiercing(effect)` ; `message.GainATKForThisAttack(n, effect)`
#    (`sender_damage.py:114`).
#
# TEXTE CONTRE CODE
#  ⚠ « basic ATTACK » seulement : la defense et le contre ne declenchent rien
#    (`is_basic_attack=True`, pas `WhenUnitUseBasicPower`, qui couvre aussi la
#    defense).
#  ⚠ « +1 ATK for THAT attack » : cette attaque seulement, EN PLUS du +1 ATK
#    continu de la carte (deux bonus distincts, les deux comptent).
#  ⚠ « THIS attack gains piercing » : l'attaque en cours (les cartes Tough de la
#    cible sont defaussees au lieu d'absorber).
#  ⚠ « exhaust Persuader » est devant la fleche : un COUT.
#  ⚠ « Hero Interrupt » : forme heros seulement.


def GetAbilities() -> Sequence['Ability']:

    def persuader(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)

        message.GainATKForThisAttack(1, effect)
        message.GainPiercing(effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        *AbilityFactory.GiveKeywordToAttached(Hero, attack=1),
        AbilityFactory.WhenUnitWouldAttack(
            AbilityType.HeroInterrupt,
            "You",
            persuader,
            is_basic_attack=True,
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetTarget("YourIdentity"),
    ]
