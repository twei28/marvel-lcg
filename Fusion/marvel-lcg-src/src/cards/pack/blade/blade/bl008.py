from . import *

# * Blade's Sword — AMELIORATION, cout 1, [physical]. WEAPON. UNIQUE.
# Restricted.
# Hero Interrupt: When Blade makes an attack with piercing, increase the amount
#   of damage that attack deals by 1.
#
# CARTES DE REFERENCE
#  - `WhenUnitMakeKeyWordAttack(..., has_keyword="Piercing")` (do_attack.py:105) :
#    la fabrique faite pour « an attack WITH PIERCING ». Son message est envoye
#    APRES `WhenUnitWouldAttack` (can_attack.py:358), donc apres le Bandolier
#    (bl007) et le Bandolier nemesis (bl015) qui DONNENT le percant : une
#    attaque de base rendue percante par un pieu recoit bien le +1 de l'epee.
#  - `DealAdditionalDamage` sur ce message (sender_damage.py:33).
#
# TEXTE CONTRE CODE
#  ⚠ « When BLADE makes an attack » -> `"You"` = l'identite, forme heros de
#    fait (Hero Interrupt).
#  ⚠ « increase the amount of damage by 1 » -> AVANT le doublement du set
#    nemesis (`WhenRecalculateAttackDamage`, envoye apres) : 4 + 1 = 5 -> 10
#    sur un Vampire. Arbitrage utilisateur du 07/09/2026.
#  ⚠ Restricted : lu dans `desc`, rien a coder (fiche restricted.md).
#  ⚠ « Hero Interrupt » sans cout : le joueur peut refuser le +1 (cas rare :
#    ne pas achever un ennemi). Le pilote le prend.


def GetAbilities() -> Sequence['Ability']:

    def trancher(effect: 'Effect', message: 'Message.WhenUnitMakeKeyWordAttack') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)
        message.DealAdditionalDamage(1, effect)

    return [
        AbilityFactory.WhenUnitMakeKeyWordAttack(
            AbilityType.HeroInterrupt,
            "You",
            trancher,
            has_keyword="Piercing",
        ),
    ]
