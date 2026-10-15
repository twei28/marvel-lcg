from . import *

# Super-Skrull Training Program — COMPLOT ANNEXE (Skrull Elite - Xavin). Menace 2[per_hero], 1 icone de boost,
# icone AMPLIFY (croix + avion : lecture du 15/10/2026, voir defs/modulaires_questions.md).
# When Revealed: Give each SKRULL enemy a tough status card.
#
# Cartes de reference :
#  - « Give each X a tough status card » : **`sk128`** Mt'nox (`Faces.GiveStatus([unit], "Tough", effect)`) ; liste
#    des ennemis SKRULL : helper `EnnemisSkrull` (communs_modulaires, modele skrull_empire).
#  - Amplify : natif (`desc.Amplify`, fiche mots-cles/amplify.md).
#
# ⚠ Mots-pieges : « EACH SKRULL ENEMY » (sbires ET mechant porteurs du trait SKRULL) ; « a TOUGH status card »
# (une carte Robuste par ennemi ; un ennemi qui en porte deja une n'en recoit pas de seconde : regle native) ;
# aucun ennemi SKRULL : rien.


def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        Unused(message)
        ennemis = EnnemisSkrull(effect)
        if ennemis:
            Faces.GiveStatus(ennemis, "Tough", effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
    ]
