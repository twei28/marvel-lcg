from . import *
# * Corsair's Gloves. Amelioration ITEM TECH, cout 2.
#
# Hero Resource: Exhaust Corsair's Gloves → generate a [wild] resource for a card tucked under Corsair.
#
# Cartes de reference : 01008 Web-Shooter (`CanGenerateResources(HeroResource, Resources("G"))` + `Exhaust("This")`),
# `conditions` de la fabrique (`Message.CheckPlayerCanPayCost`, `paying_for_effect` = l'effet de la carte payee).
# FAQ de l'auteur : cette ressource ne paie QUE la carte glissee qu'on joue, jamais autre chose.
def GetAbilities() -> Sequence['Ability']:
    def pour_une_glissee(effect: 'Effect', message: 'Message.CheckPlayerCanPayCost') -> bool:
        identite = IdentiteDe(effect)
        if identite is None:
            return False
        carte = message.paying_for_effect.this
        return carte in Glissees(identite)
    return [
        AbilityFactory.CanGenerateResources(
            AbilityType.HeroResource,
            Resources("G"),
            conditions=[pour_une_glissee],
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
