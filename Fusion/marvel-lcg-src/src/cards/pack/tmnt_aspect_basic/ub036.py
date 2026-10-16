from . import *

# * Party Wagon — SOUTIEN 3 [energy], aspect Basic (TMNT Reskins). NYC. VEHICLE.
# Resource: Exhaust Party Wagon → generate a [wild] resource for a player whose identity has the [[NINJA]] or
#   [[TURTLE]] trait.
#
# MODIFIEE de 32020 The X-Jet : X-MEN -> NINJA ou TURTLE. Script copie de 32020.
# `for_player_whose_identity_has_trait` n'accepte qu'UN trait ; on reproduit ses deux effets a la main :
# (1) la condition de paiement (le joueur qui paie a NINJA ou TURTLE), (2) n'importe quel joueur a ce
# trait peut s'en servir (`any_player_can_trigger_this_when`, comme `AnyPlayerCanDoThis`).

TRAITS = ["NINJA", "TURTLE"]


def _a_le_trait(identite: 'CardFace|None') -> bool:
    return identite is not None and any(identite.HasTrait(t) for t in TRAITS)


def GetAbilities() -> Sequence['Ability']:
    ability = AbilityFactory.CanGenerateResources(
        AbilityType.Resource,
        Resources("G"),
        conditions=[
            lambda effect, message: _a_le_trait(message.GetToPlayer().GetIdentity()),
        ],
    ).SetCostFunc(CostFunc.Exhaust("This"))
    ability.any_player_can_trigger_this_when.append(
        lambda effect: _a_le_trait(effect.GetInitiator().GetIdentity()))
    return [ability]
