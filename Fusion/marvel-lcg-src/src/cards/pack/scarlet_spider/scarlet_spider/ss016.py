from . import *

# * Stings of Kaine — SUPERPOWER
# Scarlet Spider gets +1 ATK.
# Hero Interrupt: When you attack, exhaust Stings of Kaine -> that attack
#   gains piercing and overkill.
#
# "+1 ATK" fixe sur l'identite elle-meme (pas d'"Attach to..." imprime) :
# modele ok016 Royal Protector, `AbilityFactory.
# GiveKeywordToInPlayWhenApplyThis("You", attack=1)`. "When you attack,
# exhaust -> gains piercing and overkill" : modele cw/tigra/56005.py (Sharp
# Claws), `AbilityFactory.WhenUnitMakeAttack(HeroInterrupt, "You", ...)
# .SetCostFunc(CostFunc.Exhaust("This"))` + `message.GainPiercing(effect)` /
# `message.GainOverKill(effect)` (drax/19005.py pour le couple des deux
# methodes sur le meme message). `is_basic_attack` laisse a None : "when
# you attack" couvre aussi bien l'attaque de base que les evenements ATTACK
# (Precise Force, Unrestrained).


def GetAbilities() -> Sequence['Ability']:

    def stings_of_kaine(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)

        message.GainPiercing(effect)
        message.GainOverKill(effect)

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            "You",
            attack=1,
        ),
        AbilityFactory.WhenUnitMakeAttack(
            AbilityType.HeroInterrupt,
            "You",
            stings_of_kaine,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
