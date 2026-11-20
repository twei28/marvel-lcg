from . import *

# Focused Rage (variante Why Not) : cout 2 au lieu de 3 (desc), texte
# inchange. Modele 01027.


def GetAbilities() -> Sequence['Ability']:

    def focused_rage(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        initiator = effect.GetInitiator()
        initiator.DrawUp(1, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            focused_rage
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetCostFunc(CostFunc.TakeDamage(1, "Initiator")),
    ]
