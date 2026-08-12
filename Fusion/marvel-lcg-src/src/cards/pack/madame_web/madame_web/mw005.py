from . import *

# Astral Form — custom « Kajislav »
# Hero Action (thwart): Exhaust Astral Form and spend a [mental] resource ->
#   remove X threat from among schemes in play where X is the number of allies
#   you control.
#
# « from among schemes » = X menaces REPARTIES, pas X sur chaque complot. Le
# moteur exprime cela par `repeat_rules="Threat"` (le complot est propose
# autant de fois qu'il porte de menaces) et `RemoveThreatFromSchemesTotal`, qui
# retire 1 menace par occurrence choisie. Meme montage que Mutant Peacekeepers
# (34018), dont le X est lui aussi calcule.

def GetAbilities() -> Sequence['Ability']:

    def nombre_allies(effect: 'Effect') -> int:
        return len(effect.GetInitiator().GetControlAllies())

    def forme_astrale(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)

        this.RemoveThreatFromSchemesTotal(effect.targets, nombre_allies(effect), effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            forme_astrale
        ).SetLabel('thwart')
        .SetCost(Cost("B"))
        .SetCostFunc(CostFunc.Exhaust("This"))
        .SetTarget(Scheme2, range=(1, nombre_allies), repeat_rules="Threat"),
    ]
