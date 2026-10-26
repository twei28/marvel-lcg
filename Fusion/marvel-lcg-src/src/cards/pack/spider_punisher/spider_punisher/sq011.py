from . import *


def GetAbilities() -> Sequence['Ability']:
    def incendiary_rounds(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(message)
        joueur = effect.GetInitiator()
        cible = list(effect.targets)
        autres = [e for e in Worlds.FindCardsOnField(effect, card_type=Enemy) if e is not cible[0] and not e.IsDefeated()]
        k = min(2, len(autres))                     # « to a maximum of 2 »
        this.DealDamage(cible, 3 - k, effect)       # « Reduce this damage by 1 for each other enemy in play »
        restants = list(autres)
        touches: List['CardFace'] = []
        for _ in range(k):                          # « Then deal 1 damage to that many other enemies »
            if len(restants) == k - len(touches):
                touches.extend(restants)
                break
            choisi = joueur.AskChooseFace(restants, effect, prompt="Deal 1 damage")
            restants.remove(choisi)
            touches.append(choisi)
        if touches:
            this.DealDamage(touches, 1, effect)

    return [
        RessourceEnhancedCombatSense(CostFunc.Exhaust("This")),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            incendiary_rounds,
            conditions=[ActionPayable("1")],
        ).SetLabel('attack')
        .SetCostFunc(CostFunc.Exhaust("This"))
        .SetCost(Cost("1"))
        .SetTarget(Enemy),
    ]
