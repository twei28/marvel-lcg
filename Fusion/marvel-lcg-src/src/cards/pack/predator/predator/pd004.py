from . import *

# Ghost Protocol — EVENEMENT, cout 1, [energy]. THWART. x2.
# Hero Action (thwart): Remove 2 threat from a scheme (4 threat instead if you are cloaked).
#
# Cartes de reference :
#  - `core/01052` Chase Them Down : `this.RemoveThreatFromSchemes(effect.targets, n, effect)` + `.SetPlay().SetLabel('thwart')`
#    + `.SetTarget(Scheme2)` (la manigance est choisie par le selecteur de la carte).
#  - `ShinobiCloak` / `IsCloaked` : la carte Cloaked (fiche mots-cles/cloaked.md).
#
# ⚠ Mots-pieges :
#  - « 4 threat INSTEAD if YOU are cloaked » : 4 au lieu de 2 (pas 2 + 4) ; « you » = Predator (la face HEROS porte la carte
#    Cloaked) ; la carte Cloaked n'est PAS consommee par cet evenement (il la lit seulement).
#  - « from A scheme » : une manigance au choix, principale ou annexe.


def GetAbilities() -> Sequence['Ability']:

    def protocole_fantome(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)
        valeur = 4 if EstCamoufle(JoueurDeCetteCarte(effect)) else 2
        this.RemoveThreatFromSchemes(effect.targets, valeur, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            protocole_fantome,
        ).SetPlay().SetLabel('thwart')
        .SetTarget(Scheme2),
    ]
