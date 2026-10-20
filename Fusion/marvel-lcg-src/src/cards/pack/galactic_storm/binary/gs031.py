from . import *

# Forgotten Life — OBLIGATION. 2 icones de boost. Bandeau « BINARY ».
# (Numero imprime « 4 », comme Pursued by the Flame : card_id gs031, rang de la
#  carte dans la liste du deck de depart, question Q1.)
# Give to the Carol Danvers player.
# While in hero form, your hand size is reduced by 1.
# Alter-Ego Action: Exhaust Carol Danvers and discard an identity-specific card
#   from your hand → remove Forgotten Life from the game.
#
# Cartes de reference :
#  - **`sunfire/sf010`** Shame : obligation QUI RESTE EN JEU, bonus continu de
#    taille de main + « Alter-Ego Action: Exhaust <alter-ego> and discard 1
#    card from your hand → remove <obligation> from the game » =
#    `GiveKeywordToInPlayWhenApplyThis(..., hand_size=-1)` +
#    `PlayerActionToRemoveThisFromGame(AlterEgoAction)
#    .SetCostFunc(CostFunc.Exhaust("YourIdentity"))
#    .SetCostFunc(CostFunc.Discard("YourHandCards", ...))`.
#  - **`trors/04165`** Martial Law pour le couple bonus / action de retrait.
#  - « identity-specific card » : `card_class="IdentitySpecific"` (une classe
#    `Hero` de cards.json est lue IdentitySpecific, card_player.py).
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « WHILE IN HERO FORM, YOUR hand size » : seulement en forme heros ; la
#    cible est la face HEROS du joueur (`"YourHero"`, RECETTES §13 « Your hero
#    gains »), pas `"You"` (qui couvrirait aussi Carol Danvers : contre-cas).
#  - « REMOVE ... FROM THE GAME » (pas discard) : elle ne revient jamais.
#  - DEUX couts : incliner Carol Danvers ET defausser une carte SIGNATURE de la
#    main ; une carte d'aspect ou basique ne paie pas (contre-cas) ; sans carte
#    signature en main, l'Action n'est pas proposee.
#  - « Give to the Carol Danvers player » : `desc.GiveTo`, aucun script.


def GetAbilities() -> Sequence['Ability']:

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            "YourHero",
            hand_size=-1,
        ),
        AbilityFactory.PlayerActionToRemoveThisFromGame(
            AbilityType.AlterEgoAction,
        ).SetCostFunc(CostFunc.Exhaust("YourIdentity"))
        .SetCostFunc(CostFunc.Discard("YourHandCards", card_class="IdentitySpecific", range=(1, 1))),
    ]
