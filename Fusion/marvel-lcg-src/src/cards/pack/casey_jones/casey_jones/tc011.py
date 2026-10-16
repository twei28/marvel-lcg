from . import *

# Hockey Stick — AMELIORATION, cout 2, [energy]. WEAPON. Restricted.
# Hero Interrupt: When you make a basic attack or defense, exhaust Hockey Stick
#   → you get +2 to that power for this use.
#
# MOT-CLE : RESTRICTED — fiche `restricted.md` (`desc.Restricted = "1"`, AUCUN
# SCRIPT pour la limite).
#
# CARTES DE REFERENCE
#  - `tg009` Frogjolnir / `tc007` Baseball Bat : MEME montage
#    (`WhenUnitUseBasicPower(HeroInterrupt, "You", op, powers=[...])` +
#    `message.GainValue(n, effect)`). Ici le filtre `powers=["ATK", "DEF"]`
#    ecarte le contre.
#
# TEXTE CONTRE CODE
#  ⚠ « basic ATTACK OR DEFENSE » : deux pouvoirs, PAS le contre (CTR) : un
#    contre-cas mesure qu'un contre ne declenche rien.
#  ⚠ « +2 » (pas +1 comme la batte) « to THAT power FOR THIS USE ».
#  ⚠ « exhaust Hockey Stick » est devant la fleche : un COUT.
#  ⚠ « Hero Interrupt » : forme heros seulement.


def GetAbilities() -> Sequence['Ability']:

    def hockey_stick(effect: 'Effect', message: 'Message.WhenUnitUseBasicPower') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)

        message.GainValue(+2, effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.WhenUnitUseBasicPower(
            AbilityType.HeroInterrupt,
            "You",
            hockey_stick,
            powers=["ATK", "DEF"],
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetTarget("YourIdentity"),
    ]
