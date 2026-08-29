from . import *

# * Kate's Quiver — ITEM
# You may remove up to 5 arrow counters with your Master Archer Interrupt
#   instead. (Le plafond 3->5 est gere directement dans kb001a, qui verifie
#   la presence de Kate's Quiver en jeu -- voir le commentaire de ce fichier.)
# Resource: Exhaust Kate's Quiver -> generate a [wild] resource and place 1
#   arrow counter on Kate's Bow.


def GetAbilities() -> Sequence['Ability']:

    def kates_quiver(effect: 'Effect', message: 'Message.WhenPlayerPayingResources') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)

        PlacerCompteursFlecheSurArc(effect, 1)

    return [
        AbilityFactory.CanGenerateResources(
            AbilityType.Resource,
            Resources("G"),
            ex_operation=kates_quiver,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
