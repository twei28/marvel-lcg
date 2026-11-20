from . import *

# Precognition (x2) : EVENEMENT (PSIONIC. THWART.), cout 2, [mental]. Hero Class.
# Hero Action (thwart): Remove 2 threat from a scheme. Search the top 3 cards of your deck for a card and add it to your hand. If it is a Mantis card, remove
# 1 threat from a scheme. Shuffle your deck.
#
# CARTES DE REFERENCE
#  - `rc002` Authorized Force (RoboCop) : evenement « thwart » a `SetTarget(Scheme2)` + `RemoveThreatFromSchemes`, second choix par `ChooseAbilities`.
#  - `jj013` Chase Down a Lead : `Search.PlayerDeckTop(effect, joueur, 5, ..)` puis `GainCard` (la fouille melange le deck : le « Shuffle your deck » imprime).
#
# TEXTE CONTRE CODE
#  « Remove 2 threat from A scheme » : une manigance au choix, 2 menaces. « the top 3 cards » : seulement les 3 du dessus. « If IT is a Mantis card » : la carte PRISE (classe
#    Hero du deck de Mantis), pas une carte du deck en general. « remove 1 threat from A scheme » : seconde manigance au choix (peut etre la meme). Hero Action : forme heros seulement.
#  Chiffres : cout 2, 2 menaces, 3 cartes, 1 menace.


def GetAbilities() -> Sequence['Ability']:

    def precognition(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)
        joueur = effect.GetInitiator()
        this.RemoveThreatFromSchemes(effect.targets, 2, effect)
        face = ChercherAuSommet(effect, joueur, 3)
        if face is not None and CarteMantis(face):
            RetirerUneMenace(effect, joueur, this, 1)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            precognition,
        ).SetPlay().SetLabel('thwart')
        .SetTarget(Scheme2),
    ]
