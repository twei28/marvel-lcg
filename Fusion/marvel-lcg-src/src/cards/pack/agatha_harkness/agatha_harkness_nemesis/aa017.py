from . import *

# Funeral — obligation DU SET NEMESIS (cas rare : 2e obligation du pack).
# Boost 2. GiveTo: Agatha Harkness.
# Your hero gets -1 THW.
# Alter-Ego Action: Spend a [energy] resource -> discard this card.
#
# Cartes de reference (RECETTES-MOTEUR §5) :
#  - le malus continu : ho005/an002, `GiveKeywordToInPlayWhenApplyThis(
#    Identity, control_by="You", thwart=-1)` — l'obligation vit dans la zone
#    du joueur a qui elle a ete remise, « your hero » = son identite ;
#  - la sortie : wd005 `PlayerActionToDiscardThis(AlterEgoAction)` +
#    `SetCost(Cost("Y"))` (une ressource energie, comme imprime).

def GetAbilities() -> Sequence['Ability']:

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            Identity,
            control_by="You",
            thwart=-1,
        ),
        AbilityFactory.PlayerActionToDiscardThis(
            AbilityType.AlterEgoAction,
        ).SetCost(Cost("Y")),
    ]
