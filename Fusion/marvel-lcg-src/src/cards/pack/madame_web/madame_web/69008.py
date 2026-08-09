from . import *

# Webb's Team Strikes! — custom « Kajislav » (cout X)
# Hero Action (attack): Exhaust up to X allies you control -> deal 3 damage to
#   the villain for each ally exhausted this way.
#
# Les allies sont des CIBLES et non un CostFunc : X n'est connu qu'une fois les
# ressources payees (effect.GetCostX()), donc trop tard pour borner un cout.
# On selectionne donc « jusqu'a tous » les allies, puis on tronque a X, comme le
# font Speed Cyclone (14006) et Lethal Intent (22010).

def GetAbilities() -> Sequence['Ability']:

    def equipe_de_webb(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)

        allies = effect.targets[:effect.GetCostX()]
        allies = Faces.ExhaustAll(allies, effect)
        if allies:
            this.DealDamage(effect.targets2, 3 * len(allies), effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            equipe_de_webb
        ).SetPlay().SetLabel('attack')
        # « up to X » : de 0 a tous. Surtout PAS ("Zero", "All"), qui veut dire
        # « tous ou aucun » (SelectorRange.GetTargetMin rend len(targets) quand
        # le minimum vaut "Zero").
        .SetTarget("YourAlly", range=(0, "All"), canbe_exhaust=True)
        .SetTarget2(Villain),
    ]
