from . import *

# Replaced — ATTACHEMENT (ensemble Veranke), x2 exemplaires.
# CONDITION.
# Treat attached ally as a SKRULL minion with a blank text box. Attached minion's SCH is equal to its
#   printed THW and it does not take consequential damage.
# When Revealed: Attach to an ally you control without Replaced attached. Attached ally engages its
#   controller. Otherwise, this card gains surge.
#
# Cartes de reference :
#  - Tout le premier paragraphe (texte blanc, SCH = THW imprime, pas de degats consequents) est NATIF a
#    `AbilityFactory.TreatAttachedCardAsMinion(Ally, "Skrull Minion")` : AUCUN code supplementaire requis
#    (modele EXACT, meme texte imprime mot pour mot : `skrull_menace/skrull_empire/sk098.py` Impostor,
#    « engages its controller » egalement natif a ce mecanisme).
#  - « Attach to an ally you control without Replaced attached. Otherwise, gains surge » :
#    `AttachToFaceWhenPutIntoPlay(CardFinder(card_type=Ally), without_another_copy=True,
#    if_cannot_gain_surge=True)` (modele sk196 Super-Skrull Enhancement).
#
# ⚠ Mots-pieges : « an ally YOU control » = seulement les allies DU JOUEUR qui revele (`from_where=
# ["YouControlCards"]` implicite via `AttachToFaceWhenPutIntoPlay` sur un allie en jeu — a verifier que le
# ciblage se limite bien au controleur courant, sinon filtrer explicitement) ; « WITHOUT Replaced attached »
# exclut un allie qui porte deja un exemplaire (les deux exemplaires comptent, `without_another_copy`).


def GetAbilities() -> Sequence['Ability']:
    return [
        AbilityFactory.TreatAttachedCardAsMinion(Ally, "Skrull Minion"),
        AbilityFactory.AttachToFaceWhenPutIntoPlay(
            CardFinder(card_type=Ally),
            without_another_copy=True,
            if_cannot_gain_surge=True,
        ),
    ]
