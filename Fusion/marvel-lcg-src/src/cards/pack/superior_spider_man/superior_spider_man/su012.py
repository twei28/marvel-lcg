from . import *

# Contingency Plan — AMELIORATION signature, la 16e carte du pack.
# TACTIC. Permanent. Setup.
# The card attached here may be played as though it were in your hand.
# Action: Discard the attached card.
#
# CARTES DE REFERENCE
#  - `aa002` (pack agatha_harkness), `dz014` (pack dazzler) :
#    `YouMayPlayCardLikeInHand(NonKeyword, from_where="ThisPlacedCard")`, la
#    fabrique EXACTE de « may be played as though it were in your hand »
#    (play.py:376, le litteral `"ThisPlacedCard"` compare
#    `effect.this.GetPlacedCardArea()` a la zone de la carte).
#  - `Faces.DiscardAll` pour l'Action.
#
# TEXTE CONTRE CODE
#  ⚠ « Permanent. Setup. » sont des BASES AUTOMATIQUES lues dans `desc`
#    (fiches `permanent.md` et le mot-cle `Setup`) : la carte commence EN JEU
#    et ne peut pas etre defaussee par les effets ordinaires. AUCUN script pour
#    elles. ⚠ `Setup` ne se PROUVE que par une vraie partie montee avec le deck
#    (RECETTES §7) : un cas de test qui pose la carte a la main ne dit rien.
#  ⚠ La carte n'a PAS de cout imprime (le coin superieur gauche est vide) :
#    `desc` ne porte donc pas de cle `Cost`.
#  ⚠ « THE CARD ATTACHED HERE » : une seule, et c'est le plafond « to a maximum
#    of 1 » des trois cartes qui l'alimentent (su001b, su001c, su008) qui le
#    tient — pas cette carte-ci.
#  ⚠ « Action: Discard the attached card » : c'est la carte POSEE qu'on
#    defausse, pas Contingency Plan (qui est Permanent et ne peut de toute
#    facon pas partir). Confondre les deux vaudrait au joueur de perdre sa
#    carte permanente.
#  ⚠ Aucune limite imprimee : etape 7 bis sans objet.


def GetAbilities() -> Sequence['Ability']:

    def porte_une_carte(effect: 'Effect', message: Any) -> bool:
        Unused(message)
        return len(CartesPoseesSous(effect.this)) > 0

    def defausser_la_carte(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(message)
        posees = CartesPoseesSous(this)
        if posees:
            Faces.DiscardAll(posees, effect)

    return [
        *AbilityFactory.YouMayPlayCardLikeInHand(
            AbilityType.NonKeyword,
            None,
            from_where="ThisPlacedCard",
        ),

        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            defausser_la_carte,
            conditions=[porte_une_carte],
        ).SetName("Contingency Plan"),
    ]
