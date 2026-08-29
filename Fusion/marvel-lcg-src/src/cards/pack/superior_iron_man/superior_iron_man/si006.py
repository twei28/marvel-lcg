from . import *

# Mason Thomas
#
# Identique a Daniel Hall (si004) : voir ce fichier pour les references.

def GetAbilities() -> Sequence['Ability']:

    def apres_generation(effect: 'Effect', message: 'Message.WhenPlayerPayingResources') -> None:
        this = effect.this.CastTo(Support)
        if this.GetCounters('cash') == 0:
            initiator = effect.GetInitiator()
            face = initiator.AskChooseFace(list(initiator.hand_cards.Get()), effect)
            if face:
                Faces.DiscardAll([face], effect)

    return [
        AbilityFactory.CanGenerateResources(
            AbilityType.Resource,
            Resources("G"),
            ex_operation=apres_generation,
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetCostFunc(CostFunc.Counter("This", 1, 'cash')),
    ]
