from . import *

# Focused Attention — TRAITRISE (Expert Skrull). 3 icones de boost, Surge.
# Surge.
# When Revealed: Give the villain 1 facedown boost card.
#
# Cartes de reference :
#  - Surge : natif (`desc.Surge`, fiche mots-cles/surge.md), aucun module pour lui.
#  - « Give the villain 1 facedown boost card » : **`sk167`** White Tiger / `30037` Solus
#    (`Faces.GiveFacedownBoostCards`), helper `DonnerBoostAuMechant`.
#
# ⚠ Mots-pieges : « the VILLAIN » (le mechant, pas un sbire) ; « FACEDOWN » : la carte attend la prochaine
# activation du mechant ; Surge et la carte de boost sont independants (le surge joue meme sans mechant).


def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        Unused(message)
        DonnerBoostAuMechant(effect, 1)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
    ]
