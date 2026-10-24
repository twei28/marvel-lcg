from . import *

# Martial Mastery — AMELIORATION, cout 2, [wild]. SKILL. (card_id shc017, 15/15)
# Uses (3 chi counters).
# Hero Interrupt: When you use one of your hero's basic powers (THW, ATK, or DEF), exhaust Martial Mastery and remove
#   1 chi counter from it → your hero gets +1 to that power for this use.
#
# Cartes de reference :
#  - `20010` Venom's Pistol / `tg009` Frogjolnir : `WhenUnitUseBasicPower(HeroInterrupt, ..., op)` + `message.GainValue(+1, effect)`
#    (« +1 to that power for this use » : `GainValue` route vers ATK/THW/DEF selon le pouvoir).
#  - `sh010` Martial Skill : `desc.Uses = "N,chi"` + double cout `Exhaust("This")` + `Counter("This", 1, 'chi')`.
#
# ⚠ Mots-pieges :
#  - « Uses (3 chi counters) » : natif (`desc.Uses`) ; la carte quitte le jeu au DERNIER compteur retire : ne PAS coder la sortie.
#  - « basic powers (THW, ATK, or DEF) » : PAS la recuperation (REC de l'alter-ego) : `powers=["THW", "ATK", "DEF"]`.
#  - « YOUR hero » : le heros que contrôle le porteur de l'amelioration (`control_by="You"`), pas le heros d'un autre joueur.
#  - « +1 for THIS USE » : pour cet usage seulement (pas pour le round).
#  - le cout est le double (incliner ET retirer 1 compteur) ; avec 0 compteur la carte a deja quitte le jeu.


def GetAbilities() -> Sequence['Ability']:

    def un_chi(effect: 'Effect', message: 'Message.WhenUnitUseBasicPower') -> bool:
        Unused(message)
        return effect.this.GetCounters('chi') >= 1

    def martial_mastery(effect: 'Effect', message: 'Message.WhenUnitUseBasicPower') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)

        message.GainValue(+1, effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.WhenUnitUseBasicPower(
            AbilityType.HeroInterrupt,
            Hero,
            martial_mastery,
            powers=["THW", "ATK", "DEF"],
            control_by="You",
            conditions=[un_chi],
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetCostFunc(CostFunc.Counter("This", 1, 'chi')),
    ]
