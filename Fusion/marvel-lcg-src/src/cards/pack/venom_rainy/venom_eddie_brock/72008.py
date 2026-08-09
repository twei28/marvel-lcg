from . import *

# Camouflage — custom « Rainy »
# Hero Interrupt (attack): When an enemy would initiate an attack, discard
#   Camouflage -> deal 4 damage to that enemy and confuse them. If no enemy
#   was confused this way, remove 2 threat from a scheme.

def GetAbilities() -> Sequence['Ability']:

    def camouflage(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this.CastTo(Upgrade)

        cible = message.attacker
        this.DealDamage([cible], 4, effect)

        confus = False
        # CORRECTIF (4/8/2026) : `IsInField` n'existe sur AUCUNE face du
        # moteur. La carte plantait des qu'elle arrivait ici. La bonne
        # methode est `IsInPlay`.
        if cible.IsInPlay() and not cible.IsConfused():
            Faces.GiveStatus([cible], "Confused", effect)
            confus = cible.IsConfused()

        if not confus:
            initiator = effect.GetInitiator()

            def retirer(targets: Sequence['CardFace']) -> None:
                this.RemoveThreatFromSchemes(list(targets), 2, effect)

            initiator.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility(
                    "Remove 2 threat from a scheme",
                    retirer,
                ).SetTarget(Scheme2, range=(1, 1)),
            )

    return [
        AbilityFactory.WhenUnitWouldAttack(
            AbilityType.HeroInterrupt,
            Enemy,
            camouflage,
        ).SetLabel('attack')
        .SetCostFunc(CostFunc.Discard("This")),
    ]
