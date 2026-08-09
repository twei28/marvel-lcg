from . import *

# Goddess of Thunder — custom "Rainy"
# Hero Resource: Exhaust Goddess of Thunder -> generate a [energy] resource,
# or [energy][energy] resources instead for a Thor card.

def GetAbilities() -> Sequence['Ability']:

    def goddess_of_thunder(effect: 'Effect', message: 'Message.CheckPlayerCanPayCost') -> 'Resources|None':
        card = message.paying_for_card
        if card is not None and getattr(card.paper, 'set_name', '') == 'Thor (Jane Foster)':
            return Resources("YY")
        return Resources("Y")

    return [
        AbilityFactory.CanGenerateResources(
            AbilityType.HeroResource,
            # CORRECTIF (4/8/2026) : le 2e argument POSITIONNEL est `resources`
            # (un objet Resources), pas `resources_fn`. La fonction y etait
            # stockee telle quelle, l'assert `resources != None` passait, et la
            # capacite generait un objet fonction au lieu de ressources : elle
            # ne servait donc jamais a payer quoi que ce soit.
            resources_fn=goddess_of_thunder,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
