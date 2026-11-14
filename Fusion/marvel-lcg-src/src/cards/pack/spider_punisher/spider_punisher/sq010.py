from . import *


def GetAbilities() -> Sequence['Ability']:
    def high_explosive_rounds(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(message)
        joueur = effect.GetInitiator()

        def pioche(vaincu: 'CardFace') -> None:
            Unused(vaincu)
            joueur.DrawUp(1, effect)

        this.DealDamage(effect.targets, 3, effect, if_this_attack_defeats=pioche)

    return [
        RessourceEnhancedCombatSense(CostFunc.Exhaust("This")),
        AbilityFactory.UnitAttackGainKeyword(
            "You",
            overkill=True,
            conditions=[AttaqueDeCetteCarte],
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            high_explosive_rounds,
            conditions=[ActionPayable("R")],
        ).SetLabel('attack')
        .SetCostFunc(CostFunc.Exhaust("This"))
        .SetCost(Cost("R"))
        .SetTarget(Enemy),
    ]
