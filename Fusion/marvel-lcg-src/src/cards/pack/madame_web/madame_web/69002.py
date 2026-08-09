from . import *

# * Spider-Woman: Julia Carpenter — custom « Kajislav »
# Spider-Woman enters play with 2 psionic web counters.
# Response: After a side scheme enters play, remove 1 psionic web counter from
#   Spider-Woman -> remove 2 threat from that side scheme.

def GetAbilities() -> Sequence['Ability']:

    def toile_psionique(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        this = effect.this.CastTo(Ally)

        # « ce plan-la » : la cible est le complot secondaire qui vient d'entrer
        # en jeu, comme le casque de Rescue (90124).
        this.RemoveThreatFromSchemes([message.trigger], 2, effect)

    return [
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.Response,
            SchemeSide2,
            toile_psionique
        ).SetLabel('thwart')
        .SetCostFunc(CostFunc.Counter("This", 1, 'psionic')),
        AbilityFactory.ThisEnterPlayWithCounters(2, 'psionic'),
    ]
