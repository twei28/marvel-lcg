from . import *

# Global Influence : EVENEMENT (SPLIT. SUPERPOWER. THWART.), cout 2, [mental]. Classe Hero. (x2)
# Hero Action (thwart): Remove up to 3 threat from among schemes, ignoring the patrol keyword and any crisis icons in play (5 threat instead if there are 3+ balance counters in play).
# Special: Place X threat on each scheme, where X is equal to the Void's SCH.
#
# CARTES DE REFERENCE
#  - `ca010` (Sinister Flight) : `this.RemoveThreatFromSchemes(effect.targets, n, effect, ignore_crisis=True)` + `.SetPlay().SetLabel('thwart').SetTarget(Scheme2).SetIgnoreKeyword('Patrol')`.
#  - Special : `this.PlaceThreatOnSchemes("EachScheme", X, effect)` (card_face.py:1032) ; `.NoOutOfPlayLimit()`.
#
# TEXTE CONTRE CODE
#  « up to 3 threat FROM AMONG schemes » : lecture codee = UNE manigance choisie (modele `ca010`), jusqu'a 3 (5 a 3+ compteurs) ; « ignoring patrol AND any crisis icons » : les deux. « X = the Void's SCH » : le SCH COURANT du Void
#  (= compteurs sur Duality Aspect) ; sans Void en jeu, pas d'effet. « EACH scheme » : principale et annexes. Chiffres : cout 2, 3 ou 5.


def GetAbilities() -> Sequence['Ability']:

    def global_influence(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        Unused(message)
        this = effect.this.CastTo(Event)
        n = 5 if EquilibreEnJeu(effect) >= 3 else 3
        this.RemoveThreatFromSchemes(effect.targets, n, effect, ignore_crisis=True)

    def special(effect: 'Effect', message: 'Message.WhenResolveSpecialAbility') -> None:
        Unused(message)
        this = effect.this
        void = VoidEnJeu(effect)
        if void is None:
            return
        x = int(void.scheme or 0)
        if x > 0:
            this.PlaceThreatOnSchemes("EachScheme", x, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(AbilityType.HeroAction, global_influence).SetPlay().SetLabel('thwart')
        .SetTarget(Scheme2).SetIgnoreKeyword('Patrol'),
        AbilityFactory.WhenResolveSpecialAbility("This", special).NoOutOfPlayLimit(),
    ]
