from . import *

# Cotati Resiliency (x2) : ATTACHEMENT (CONDITION), nemesis de Mantis, boost 1.
# Attach to the enemy with the highest printed hit points and without stalwart. If you cannot, this card gains surge.
# Attached enemy gains stalwart.
# Hero Action: Spend [mental][physical] resources → discard this card.
#
# CARTES DE REFERENCE
#  - `02019` Goblin Glider : `AttachToFaceWhenPutIntoPlay(Enemy, highest_printed_hp=True, if_cannot_gain_surge=True)` + `PlayerActionToDiscardThis(HeroAction).SetCost(Cost(..))`.
#  - `tk006b` Gone Berserk! : `GiveKeywordToAttached(.., ..)` pour donner un mot-cle a la carte portee ; `mots-cles/stalwart.md` : donner Stalwart defausse les statuts Sonne/Desoriente deja poses.
#
# TEXTE CONTRE CODE
#  « the enemy with the highest PRINTED hit points » : PV imprimes (pas les PV courants), vilain compris. « AND WITHOUT stalwart » : un ennemi deja Stoique n'est pas eligible (filtre `check_face_fn`).
#  « If you cannot, this card gains surge » : aucun ennemi eligible. « Attached enemy gains stalwart » : tant que la carte est attachee. « Spend [mental][physical] » : UNE ressource mentale ET UNE physique.
#  Chiffres : boost 1, cout BR.


def GetAbilities() -> Sequence['Ability']:

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(
            CardFinder(card_type=Enemy, check_face_fn=lambda face: not face.IsStalwart()),
            highest_printed_hp=True,
            if_cannot_gain_surge=True,
        ),
        *AbilityFactory.GiveKeywordToAttached(
            Enemy,
            stalwart=1,
        ),
        AbilityFactory.PlayerActionToDiscardThis(
            AbilityType.HeroAction,
        ).SetCost(Cost("BR")),
    ]
