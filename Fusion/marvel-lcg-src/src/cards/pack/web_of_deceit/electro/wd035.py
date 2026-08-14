from . import *

# * Electro (I)

def GetAbilities() -> Sequence['Ability']:

    def decharge(effect: 'Effect', message: 'Message.AfterEnemyActivationEnd') -> None:
        # « Forced Response: After Electro activates against you, discard cards
        # from the top of the encounter deck until a treachery is discarded. »
        DefausserJusquAUneTraitrise(effect)

    return [
        AbilityFactory.AfterEnemyActivatesAgainstYou(
            AbilityType.ForcedResponse,
            "This",
            decharge
        ),
    ]
