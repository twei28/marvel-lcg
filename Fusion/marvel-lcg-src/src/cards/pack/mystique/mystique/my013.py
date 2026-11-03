from . import *

# Unnoticed (Inapercu) (x2) : EVENEMENT (SHAPESHIFTER. THWART.), cout 2, [mental].
# Hero Action (thwart): Remove 3 threat from a scheme. If the Civilian shapeshift form upgrade is faceup, ignore any crisis icon for this thwart and remove 1 threat from each scheme.
# (FR 1.1.1 : l'icone de Crise n'est ignoree QUE si Civilian est face visible ; l'EN beta l'ignorait toujours : le FR prime)
#
# CARTES DE REFERENCE
#  - `90119` Search and Rescue (rescue_rainy) : le seul contre du depot qui ignore la Crise ; `.SetIgnoreKeyword('Crisis', condition=..)` declare l'ignorance pour le CIBLAGE (crisis.md) et `ignore_crisis=True` pour la resolution.
#  - `01037` Mark V Helmet : « remove 1 threat from each scheme » = `RemoveThreatFromSchemes("EachScheme", n, effect)` (retire AUSSI des manigances annexes, `hf501a`).
#
# TEXTE CONTRE CODE
#  « Remove 3 threat from a scheme » : 3 sur UNE manigance choisie. « If the Civilian form is faceup » : my003 face `a` ; alors la Crise est ignoree pour CE contre (ciblage ET resolution) ET 1 menace est retiree de CHAQUE
#    manigance (principale et annexes, aussi sous Crise puisque la Crise est ignoree pour ce contre). Forme cachee : contre normal, la Crise s'applique.
#  Chiffres : cout 2, 3 menaces, 1 par manigance.


def GetAbilities() -> Sequence['Ability']:

    def civil_visible(effect: 'Effect') -> bool:
        joueur = effect.GetInitiator()
        return joueur is not None and FormeVisible(joueur, ID_CIVILIAN)

    def unnoticed(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        Unused(message)
        this = effect.this
        ignore = civil_visible(effect)
        this.RemoveThreatFromSchemes(effect.targets, 3, effect, ignore_crisis=ignore)
        if ignore:
            this.RemoveThreatFromSchemes("EachScheme", 1, effect, ignore_crisis=True)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            unnoticed,
        ).SetPlay().SetLabel('thwart')
        .SetIgnoreKeyword('Crisis', condition=civil_visible)
        .SetTarget(Scheme2),
    ]
