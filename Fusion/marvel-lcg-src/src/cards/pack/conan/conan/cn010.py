from . import *

# Savage Tales — ressource (14/16), [physical] + [energy].
# Hero Response: After you spend this card, place 1 Crom counter on The
#   Cimmerian (2 instead if you are King Conan).
#
# CARTES DE REFERENCE
#  - `AfterYouSpendThisCard(HeroResponse, op)` : rs010 She Devil with a Sword.
#  - RES « RY » : deux icones empilees, convention de rs010 / 45010.


def GetAbilities() -> Sequence['Ability']:

    def savage_tales(effect: 'Effect', message: 'Message.AfterCardsBeSpendAsResource') -> None:
        Unused(message)
        joueur = JoueurDe(effect)
        PoserCrom(joueur, 2 if EstKingConan(joueur) else 1, effect)

    return [
        AbilityFactory.AfterYouSpendThisCard(
            AbilityType.HeroResponse,
            savage_tales,
        ),
    ]
