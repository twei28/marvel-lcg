from . import *

# * The Captain America — SOUTIEN (VEHICLE), cout 2, [energy]. Unique.
# Resource: Exhaust this card → generate a [wild] resource for a player who controls a GUARDIAN character.
#
# CARTES DE REFERENCE
#  - `32020` The X-Jet : `CanGenerateResources(AbilityType.Resource, Resources("G"))` + `Exhaust("This")`.
#  - `16142` Milano : `.AnyPlayerCanDoThis()` pour offrir la ressource a un autre joueur.
#
# TEXTE CONTRE CODE
#  « a player who controls a GUARDIAN character » -> `ControleUnGardien` sur le joueur qui paie (identite OU allie GUARDIAN),
#    et non `for_player_whose_identity_has_trait` qui ne regarderait que l'identite. « Resource » nu : generee dans les
#    DEUX formes. « [wild] » -> `Resources("G")`.


def GetAbilities() -> Sequence['Ability']:

    def pour_un_joueur_gardien(effect: 'Effect', message: 'Message.CheckPlayerCanPayCost') -> bool:
        Unused(effect)
        joueur = message.GetToPlayer()
        return joueur is not None and ControleUnGardien(joueur)

    return [
        AbilityFactory.CanGenerateResources(
            AbilityType.Resource,
            Resources("G"),
            conditions=[pour_un_joueur_gardien],
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .AnyPlayerCanDoThis(),
    ]
