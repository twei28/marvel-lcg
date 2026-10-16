from . import *

# Baseball Bat — AMELIORATION, cout 1, [energy]. WEAPON. Restricted.
# Hero Interrupt: When you use a basic power, exhaust Baseball Bat → you get +1
#   to that power for this use.
#
# MOT-CLE : RESTRICTED — fiche `docs/reference/mots-cles/restricted.md`
# (`desc.Restricted = "1"`, limite de 2 cartes Restricted gerees par le moteur,
# AUCUN SCRIPT).
#
# CARTES DE REFERENCE
#  - `tg009` Frogjolnir et `20010` Venom's Pistol : MEME texte mot pour mot —
#    `WhenUnitUseBasicPower(HeroInterrupt, <qui>, op).SetCostFunc(Exhaust(
#    "This")).SetTarget("YourIdentity")` + `message.GainValue(+1, effect)`,
#    qui route seul vers ATQ / CTR / DEF (`sender_unit.py:21`).
#
# TEXTE CONTRE CODE
#  ⚠ « When YOU use a basic power » : l'identite du joueur (`"You"`), pas un
#    allie, pas un autre joueur. Pas de filtre `powers=` : les trois pouvoirs de
#    base du heros.
#  ⚠ « +1 to THAT power FOR THIS USE » : pour cet usage seulement
#    (`GainValue`, pas un bonus de round).
#  ⚠ « exhaust Baseball Bat » est devant la fleche : un COUT.
#  ⚠ « Hero Interrupt » : forme heros seulement (la recuperation d'alter-ego
#    n'est pas couverte).


def GetAbilities() -> Sequence['Ability']:

    def baseball_bat(effect: 'Effect', message: 'Message.WhenUnitUseBasicPower') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)

        message.GainValue(+1, effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.WhenUnitUseBasicPower(
            AbilityType.HeroInterrupt,
            "You",
            baseball_bat,
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetTarget("YourIdentity"),
    ]
