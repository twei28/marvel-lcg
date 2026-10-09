from . import *

# Vermin (hs001)
# Forced Response: After Vermin activates against you, discard the top 1 cards
# of the encounter deck, puis met en jeu engage avec vous le RAT defausse.
# Modele : AfterEnemyActivatesAgainstYou("This") de 50030 / aa abyss.

def GetAbilities() -> Sequence['Ability']:

    def vermin(effect: 'Effect', message: 'Message.AfterEnemyActivationEnd') -> None:
        DefausserEtMettreEnJeu(effect, message.GetToPlayer(), 1, tous=False)

    return [
        AbilityFactory.AfterEnemyActivatesAgainstYou(
            AbilityType.ForcedResponse,
            "This",
            vermin,
        ),
    ]
