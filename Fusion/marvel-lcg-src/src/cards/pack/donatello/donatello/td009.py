from . import *

# * Anti-Gravity Gauntlet — AMELIORATION, cout 2, [energy]. TECH. WEAPON.
# Donatello gets +1 ATK.
# Hero Interrupt: When you play an ATTACK event, exhaust Anti-Gravity Gauntlet
#   and discard 1 card from your hand -> increase the amount of damage that
#   event does by 3.
#
# CARTES DE REFERENCE
#  - `ho006` Norman Osborn : MEME montage au nombre pres — `WhenPlayerPlayCard(
#    HeroInterrupt, "You", CardFinder2("ATTACK", Event), op)` + temp
#    `WhenUnitWouldAttack(Temp0, "You", DealAdditionalDamage(n),
#    by_effect=message.played_effect)` lie a l'evenement joue.
#  - `ho011` / `60038` : `CanPlayThisUpgradeCard()` + `GiveKeywordToAttached(
#    Hero, attack=1)` pour « Donatello gets +1 ATK ».
#  - `03001a` / `sf010` : `CostFunc.Discard("YourHandCards")` en cout.
#
# TEXTE CONTRE CODE
#  « DONATELLO gets +1 ATK » : un NOM PROPRE ne designe que la face HEROS
#    (RECETTES §3) -> `GiveKeywordToAttached(Hero, ...)`, pas "You". Contre-cas
#    obligatoire en phase C : l'identite en alter-ego n'a aucun bonus.
#  « +3 » (ho006 : +1) ; « exhaust ... AND discard 1 card from your hand » :
#    les DEUX sont des couts (deux `SetCostFunc` s'ajoutent).
#  « that event » -> le bonus est lie a `message.played_effect`, pas a toutes
#    les attaques du round.


def GetAbilities() -> Sequence['Ability']:

    def gantelet(effect: 'Effect', message: 'Message.WhenPlayerPlayCard') -> None:
        this = effect.this.CastTo(Upgrade)

        this.effect.RegisterTemp(
            AbilityFactory.WhenUnitWouldAttack(
                AbilityType.Temp0,
                "You",
                lambda effect, atk_message:
                    atk_message.DealAdditionalDamage(3, effect),
                by_effect=message.played_effect,
            ),
            unregister_after_exec=False,
            until_resolve_effect=message.played_effect
        )

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        *AbilityFactory.GiveKeywordToAttached(
            Hero,
            attack=1,
        ),
        AbilityFactory.WhenPlayerPlayCard(
            AbilityType.HeroInterrupt,
            "You",
            CardFinder2("ATTACK", Event),
            gantelet,
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetCostFunc(CostFunc.Discard("YourHandCards", range=(1, 1))),
    ]
