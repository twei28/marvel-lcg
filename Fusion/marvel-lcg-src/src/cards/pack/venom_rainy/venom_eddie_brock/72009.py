from . import *

# * Lethal Protector — custom « Rainy »
# Venom gets +1 DEF.
# Hero Interrupt (attack/defense): When an enemy initiates an attack, exhaust
#   Lethal Protector -> deal 2 damage to that enemy. If an enemy was defeated
#   this way, ready Lethal Protector.

def GetAbilities() -> Sequence['Ability']:

    def lethal_protector(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this.CastTo(Upgrade)

        cible = message.attacker
        this.DealDamage([cible], 2, effect)
        # CORRECTIF (4/8/2026) : `IsInField` n'existe sur AUCUNE face du
        # moteur. La carte plantait des qu'elle arrivait ici. La bonne
        # methode est `IsInPlay`.
        if not cible.IsInPlay():
            Faces.ReadyAll([this], effect)

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            "You",
            defense=1,
        ),

        AbilityFactory.WhenUnitWouldAttack(
            AbilityType.HeroInterrupt,
            Enemy,
            lethal_protector,
        ).SetLabel('defense')
        .SetCostFunc(CostFunc.Exhaust("This")),
    ]
