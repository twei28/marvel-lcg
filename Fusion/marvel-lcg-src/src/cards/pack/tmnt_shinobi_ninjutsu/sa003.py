from . import *

# Reconnaissance — EVENEMENT 1 [mental], Ninjutsu (TMNT Shinobi, Inkwire). TACTIC.
# Action: Cloak a character you control -> look at the top 3 cards of a player deck or encounter deck. Put those
# cards on the top and/or bottom of that deck in any order.
# « Looks like trouble... » —Donatello
#
# NOUVELLE. Mots-cles (fiches lues AVANT le code) : Cloak / Cloaked (cloak.md, cloaked.md).
#
# Cartes de reference :
#  - `27043` Global Logistics : « look at the top N cards of a player deck or the encounter deck ... put the others on the
#    top and/or bottom of that deck in any order » = `SetTarget(from_where=["PlayersDeckTop", "EncounterDeckTop"])` +
#    `initiator.LookAtDeck(deck, N, effect)` + `initiator.PlaceOnTopAndOrBottomInAnyOrder(faces, effect)` (ici SANS
#    defausse) ;
#  - `sk049` The Thing : cout PERSONNALISE sur un personnage (`CostFunc.Custom(CardFinder(...), fn)`).
#
# TEXTE CONTRE CODE
#  ⚠ « Cloak a character you control -> » est le COUT (devant la fleche) : paye AVANT, sur un personnage que le joueur
#    controle (identite ou allie) et qui peut recevoir une carte Cloaked (un seul par personnage) ; sinon l'evenement
#    n'est pas jouable (`CoutCamoufler`).
#  ⚠ « a PLAYER deck OR encounter deck » : un seul deck, au choix (le sien, celui d'un autre joueur, le deck rencontre).
#  ⚠ « the top 3 cards » : exactement 3 (moins si le deck est plus court) ; « those cards » = TOUTES les cartes
#    regardees sont remises, aucune defaussee ; « top and/or bottom ... in any order ».


def GetAbilities() -> Sequence['Ability']:

    def reconnaissance(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this, message)
        initiator = effect.GetInitiator()
        deck = effect.targets[0].card.area
        faces = initiator.LookAtDeck(deck, 3, effect)
        initiator.PlaceOnTopAndOrBottomInAnyOrder(faces, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            reconnaissance,
        ).SetPlay().SetLabel()
        .SetCostFunc(CoutCamoufler())
        .SetTarget(from_where=["PlayersDeckTop", "EncounterDeckTop"]),
    ]
