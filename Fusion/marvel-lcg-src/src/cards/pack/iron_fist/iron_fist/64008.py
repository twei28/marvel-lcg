from . import *

# Channel the Iron Fist — AMELIORATION, cout 0, [energy]. TECHNIQUE. x1 (Iron Fist 11/15).
# Temporary.
# Hero Interrupt: When you attack, remove 1 chi counter from Iron Fist -> increase the amount of
#   damage that attack deals by 1 (by 2 instead if it is a basic attack).
#
# CARTES DE REFERENCE
#  - « When you attack » + « increase the amount of damage that attack deals by 1 » :
#    `winter/54002` Cybernetic Arm et `32047` Aggressive Energy (`WhenUnitWouldAttack(..., "You",
#    ...)` puis `atk_message.DealAdditionalDamage(1, effect)`), `blade/bl008` Blade's Sword (Hero
#    Interrupt, meme methode).
#  - attaque de base : `message.IsBasicAttack()` (sender_damage.py, `is_basic_power`).
#  - cout en compteurs pris sur l'identite : `venus/tv001b` (`CostFunc.Counter("YourIdentity", ...)`).
#
# TEXTE CONTRE CODE
#  ⚠ Temporary : base automatique (`desc.Temporary`, fiche temporary.md), aucun script ; perdu
#    tant que Danny Rand est face visible (64001b).
#  ⚠ « When YOU attack » : l'identite attaque (attaque de base OU evenement d'attaque), pas un allie.
#  ⚠ « remove 1 chi counter from Iron Fist -> » : COUT (fleche) ; non offert sans compteur.
#  ⚠ « by 2 INSTEAD if it is a basic attack » : 2 au lieu de 1, jamais 1 + 2.
#  ⚠ Hero Interrupt : forme heros (type dedie, lecon 27009).


def GetAbilities() -> Sequence['Ability']:

    def canaliser(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)
        message.DealAdditionalDamage(2 if message.IsBasicAttack() else 1, effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.WhenUnitWouldAttack(
            AbilityType.HeroInterrupt,
            "You",
            canaliser,
            conditions=[AuMoinsChi(1)],
        ).SetCostFunc(CostFunc.Counter("YourIdentity", 1, CHI)),
    ]
