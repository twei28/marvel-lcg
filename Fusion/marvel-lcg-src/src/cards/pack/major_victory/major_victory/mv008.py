from . import *

# Psychic Link — EVENEMENT, cout 3, [mental]. PSIONIC. THWART.
# Hero Action (thwart): Remove 5 threat from a scheme. Each player who controls a GUARDIAN character draws 1 card.
#
# CARTES DE REFERENCE
#  - `04049` Clear the Area : `HeroAction` etiquetee thwart + `RemoveThreatFromSchemes` + `DrawUp`.
#  - `mv001a` porte le trait GUARDIAN (la carte « Founder of the Guardians » le donne aussi aux identites).
#
# TEXTE CONTRE CODE
#  « each player who controls a GUARDIAN character » -> chaque joueur de la partie (pas seulement toi), conditionne par
#    `ControleUnGardien` (identite OU allie). Un joueur sans GUARDIAN ne pioche pas.
#  « draws 1 card » -> `DrawUp(1, ..)` par joueur concerne. Chiffres : 5 menace, 1 carte.
#  La pioche a lieu meme si le complot est deja a 0 (aucune condition sur la menace retiree).


def GetAbilities() -> Sequence['Ability']:

    def psychic_link(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        this.RemoveThreatFromSchemes(effect.targets, 5, effect)
        for joueur in Worlds.GetPlayers(effect):
            if ControleUnGardien(joueur):
                joueur.DrawUp(1, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            psychic_link,
        ).SetPlay().SetLabel('thwart')
        .SetTarget(Scheme2),
    ]
