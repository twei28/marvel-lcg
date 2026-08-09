from . import *

# * Gwenpool — custom « ekAugust »
# Medium Awareness — Interrupt: When you resolve an ability on a Gwenpool
# card, replace "____" with a phrase from a speech bubble. (Limit each bubble
# once per phase.)  -> implémenté par ResolveBlank() dans __init__.py.
# Bulle : « Draw 1 card. »
#
# Porte aussi le suivi « le Méchant a intrigué cette manche » utilisé par
# "It Can't End Like This!" (63003).

def GetAbilities() -> Sequence['Ability']:

    def noter_scheme(effect: 'Effect', message: 'Message.AfterUnitSchemeEnd') -> None:
        NoterVillainScheme(effect)

    return [
        AbilityFactory.AfterUnitSchemeEnd(
            AbilityType.Rule,
            Villain,
            noter_scheme,
        ),
    ]
