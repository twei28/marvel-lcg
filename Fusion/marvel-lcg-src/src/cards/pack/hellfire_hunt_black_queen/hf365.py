from . import *

# Soul Siphon (module Darkhold). Traitrise SPELL, SPELL OF DARKHOLD. « When Revealed : If Darkhold is attached to the villain, you are stunned and
# confused, remove 1 darkspell counter from Darkhold. Otherwise, find Darkhold and reveal it. [star] Boost : Reveal this card. »
# Cartes de reference : hf110 (`RevealThisCard` en boost), 41029 (`GiveStatus`), `ResolutionDeSort`.


def GetAbilities() -> Sequence['Ability']:
    def sort(effect: 'Effect', joueur: 'Player') -> None:
        identite = joueur.GetIdentity()
        Faces.GiveStatus([identite], "Stunned", effect)
        Faces.GiveStatus([identite], "Confused", effect)

    return [
        ResolutionDeSort(sort),
        AbilityFactory.WhenCardBecomeBoost("This", RevealThisCard),
    ]
