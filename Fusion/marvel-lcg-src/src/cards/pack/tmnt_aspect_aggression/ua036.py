from . import *

# * Ray Fillet — ALLIE 3 [mental], ATK 2 (1), THW 1 (1), PV 2. MANTA RAY. MUTANIMAL. SOLDIER.
# Ray Fillet enters play with 2 ammo counters on him.
# [star] Interrupt: When Ray Fillet uses a basic power, remove 1 ammo counter from him → deal 2 damage to an enemy.
#
# CARTES DE REFERENCE
#  - `38003` * Gambit : « enters play with 3 charge counters » = `ThisEnterPlayWithCounters(3, 'charge')` ;
#    « Interrupt: When Gambit attacks, remove 1 charge counter → deal 1 damage to an enemy » =
#    `CostFunc.Counter("This", 1, 'charge')` + `.SetTarget(Enemy)`.
#  - « uses a basic power » = `WhenUnitUseBasicPower(Interrupt, "This", ...)` (friend.py), qui couvre ATK ET THW.
# TEXTE CONTRE CODE
#  ⚠ « a basic power » : attaque OU contre (un allie n'a pas de DEF).
#  ⚠ Les « 1* » / « 2* » imprimes sur THW / ATK sont des ETOILES (rappel de cette capacite), pas des degats
#    consecutifs : les degats consecutifs sont les icones sous la valeur (1 et 1).


def GetAbilities() -> Sequence['Ability']:

    def ray_fillet(effect: 'Effect', message: 'Message.WhenUnitUseBasicPower') -> None:
        this = effect.this.CastTo(Ally)
        Unused(message)
        this.DealDamage(effect.targets, 2, effect)

    return [
        AbilityFactory.ThisEnterPlayWithCounters(2, 'ammo'),
        AbilityFactory.WhenUnitUseBasicPower(
            AbilityType.Interrupt,
            "This",
            ray_fillet,
        ).SetCostFunc(CostFunc.Counter("This", 1, 'ammo'))
        .SetTarget(Enemy),
    ]
