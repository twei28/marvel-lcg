from . import *

# Vermin (hs003)
# Forced Response: After Vermin activates against you, discard the top 2 cards
# of the encounter deck, puis met en jeu engage avec vous le RAT defausse.
# Modele : AfterEnemyActivatesAgainstYou("This") de 50030 / aa abyss.

def GetAbilities() -> Sequence['Ability']:

    def vermin(effect: 'Effect', message: 'Message.AfterEnemyActivationEnd') -> None:
        DefausserEtMettreEnJeu(effect, message.GetToPlayer(), 2, tous=True)
        ResoudreSpecialEvenMoreRats(effect)

    return [
        AbilityFactory.AfterEnemyActivatesAgainstYou(
            AbilityType.ForcedResponse,
            "This",
            vermin,
        ),
    ]
