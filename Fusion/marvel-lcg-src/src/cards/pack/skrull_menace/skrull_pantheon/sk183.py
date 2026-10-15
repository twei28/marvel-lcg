from . import *

# Talisman of the Skrulls (183) — TRAITRISE. 3 icones Y.
# When Revealed: Search the encounter deck and discard pile for Nogor and reveal him. If Nogor did not
#   enter play this way, this card gains surge.
#
# Cartes de reference :
#  - Recherche + revelation : **`01136`** Ultron / sk145a (`Search.EncounterCard(include_discard_pile=True,
#    name=...)` + `face.Reveal(joueur, effect)`) ;
#  - « If ... did not enter play this way, this card gains surge » : **`skrull_empire/sk103`** Giving Orders
#    (`ThisCardGainSurge(effect)`).
#
# ⚠ Mots-pieges : « Search the encounter deck AND DISCARD PILE » ; « reveal HIM » (Nogor entre en jeu engage
# avec le joueur, son « When Revealed » retourne le mechant) ; « did NOT ENTER PLAY THIS WAY » : Nogor deja en
# jeu (introuvable dans le deck) ou absent partout = Renfort, mais aussi Nogor trouve et NON entre en jeu.


def GetAbilities() -> Sequence['Ability']:

    def revelation(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        nogor = Search.EncounterCard(effect, include_discard_pile=True, name="Nogor", card_type=Minion)
        entre = False
        if nogor is not None:
            nogor.Reveal(joueur, effect)
            entre = nogor.IsInPlay()
        if not entre:
            ThisCardGainSurge(effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revelation),
    ]
