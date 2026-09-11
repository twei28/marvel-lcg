from . import *
# * Hellcat's Claws — AMELIORATION, cout 2, [physical]. WEAPON.
# Hellcat gets +1 ATK.
# Hero Interrupt: When you make a basic attack, exhaust Hellcat's Claws and
#   spend a [mental] resource → you get +2 ATK and gain piercing for this attack.
#
# Modeles : 10009 Boundless Rage (`GiveKeywordToAttached(CardFinder(name=...),
# attack=1)`), 10003 Hulk Smash (`WhenUnitMakeAttack(..., is_basic_attack=True)`
# + `GainATKForThisAttack`), `GainPiercing` (sender_damage.py:107).
# ⚠ `CardFinder(name="Hellcat")` et non "You" : le texte nomme la FACE HEROS,
#   l'alter-ego Patsy n'a pas d'ATQ.

def GetAbilities() -> Sequence['Ability']:

    def claws(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)
        message.GainATKForThisAttack(2, effect)
        message.GainPiercing(effect)

    return [
        *AbilityFactory.GiveKeywordToAttached(CardFinder(name=HELLCAT), attack=1),
        AbilityFactory.WhenUnitMakeAttack(
            AbilityType.HeroInterrupt,
            "You",
            claws,
            is_basic_attack=True,
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetCostFunc(CostFunc.Spend(Cost("B"))),
    ]
