from cards.pack import *


def RetirerMenaceDUneManigance(effect: 'Effect', valeur: int) -> None:
    """« Remove N threat from a side scheme. »

    La manigance est CHOISIE par le premier joueur, et le choix compte : dans
    la campagne Web of Deceit, la manigance qui tient la victoire (The Long
    Night) est une manigance secondaire comme une autre. On ne propose que
    celles qui portent de la menace, sans quoi le choix serait vide de sens.
    """
    schemes = [x for x in Worlds.GetAllSideSchemes(effect)
               if x.CastTo(CanPlaceToken).GetTokens('threat') > 0]
    if not schemes:
        return
    joueur = Worlds.GetFirstPlayer(effect)
    cible = joueur.AskChooseFace(schemes, effect, prompt="Remove threat from")
    Faces.RemoveTokensOn([cible or schemes[0]], valeur, 'threat', effect)


def ChercherEtReveler(effect: 'Effect', **finder) -> 'CardFace|None':
    """Cherche une carte dans le deck rencontre ET sa defausse, puis la revele.

    `Find.FindAndReveal` regarde les deux : c'est ce que demandent les textes
    « search the encounter deck and discard pile for X and reveal it »."""
    return Find.FindAndReveal(
        effect,
        Worlds.GetFirstPlayer(effect),
        finder=CardFinder(**finder)
    )
