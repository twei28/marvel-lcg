from . import *

# * Reanimator Engine — AMELIORATION, cout 2, [wild]. CONSTRUCT. ELEMENT. x1.
# Hero Action: Exhaust this card and remove 2 dredge counters from Venus -> choose up to
#   2 cards in your discard pile and shuffle them into your deck.
#
# CARTES DE REFERENCE
#  - `tl002` Splinter : cible dans `from_where=["YourDiscardPile"]` ; `Faces.ShuffleAllTo(
#    faces, joueur.player_deck, effect)` (recette « pool qui alimente le deck », RECETTES §2).
#
# TEXTE CONTRE CODE
#  ⚠ « choose UP TO 2 » -> `range=(0, 2)` (un « up to » legitime, 0 compris, RECETTES §6).
#  ⚠ « shuffle THEM into your deck » -> melange le deck apres l'ajout des cartes choisies.
#  ⚠ Deux couts (inclinaison + 2 compteurs). Action de HEROS.


def GetAbilities() -> Sequence['Ability']:

    def reanimer(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this, message)
        joueur = JoueurDeCetteCarte(effect)
        cibles = [t for t in effect.targets if t is not None]
        if joueur is None or not cibles:
            return
        Faces.ShuffleAllTo(cibles, joueur.player_deck, effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            reanimer,
        ).SetTarget(card_type=CardFace, from_where=["YourDiscardPile"], range=(0, 2))
        .SetCostFunc(CostFunc.Exhaust("This"))
        .SetCostFunc(CostFunc.Counter("YourIdentity", 2, DREDGE)),
    ]
