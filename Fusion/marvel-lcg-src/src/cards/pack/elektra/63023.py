from . import *

# Hunting Shadows — EVENEMENT 0 [mental], aspect Basic (Elektra Natchios 23). TACTIC.
# Hero Action: Search the top 8 cards of the encounter deck for a card and set it aside. Shuffle the encounter deck and put the
#   set-aside card on top of it.
#
# CARTES DE REFERENCE
#  - `18011` Angela : « search the top N cards of the encounter deck for a card » = `Search.EncounterCardTop(effect, joueur, N)` ;
#    ici `not_move=True` : la recherche NE melange PAS, c'est la carte qui melange (texte imprime : « Shuffle ... and put ... on top »).
#  - moteur : `Deck.Shuffle`, `Card.MoveToTop(deck, effect)`, `world.aside_deck` (zone « mis de cote »).
#
# TEXTE CONTRE CODE
#  ⚠ « the TOP 8 cards » : seulement les 8 premieres (cas : un 9e n'est pas proposable).
#  ⚠ « a card » : n'importe quel type, y compris une Traitrise (cas).
#  ⚠ « SHUFFLE THE ENCOUNTER DECK » : tout le deck est melange, la carte mise de cote n'en fait plus partie pendant ce temps ;
#    puis elle est REMISE AU DESSUS : c'est la prochaine carte revelee (cas).
#  ⚠ « Hero Action » SANS (attack) : forme heros seulement.


def GetAbilities() -> Sequence['Ability']:

    def hunting_shadows(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this, message)
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return
        face = Search.EncounterCardTop(effect, joueur, 8, not_move=True)
        if face is None:
            return
        paquet = face.card.area
        Faces.MoveAllTo([face], effect.world.aside_deck, effect)
        paquet.Shuffle(effect)
        face.card.MoveToTop(paquet, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            hunting_shadows,
        ).SetPlay(),
    ]
