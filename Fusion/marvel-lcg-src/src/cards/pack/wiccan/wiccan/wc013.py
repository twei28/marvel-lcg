from . import *

# Transmutation — custom « CptScorp »
# Cout 0, [mental], classe Hero, traits SPELL / SUPERPOWER.
# Action: Search the encounter deck for a card. Then, shuffle the encounter
#   deck and put that card on top of it. Draw 1 card.
#
# La SEULE carte SPELL du pack qui ne compte AUCUNE icone de bonus : elle
# choisit la carte que les autres compteront. Elle est donc volontairement
# absente de `EVENEMENTS_QUI_COMPTENT_LES_BOOSTS` (wiccan/__init__.py) et wc016
# Wiccan's Cloak ne la rejoue jamais.
#
# « Search the encounter deck » -> `Search.SearchForCard(effect, initiator,
# include_encounter_deck=True, not_move=True)` (game/operate/search.py:196).
# On appelle `SearchForCard` directement, et non le raccourci
# `Search.EncounterCard`, parce que ce dernier ne transmet PAS `not_move`
# (search.py:47-77) : sans lui, la carte trouvee est deplacee hors du deck par
# le selecteur, alors que le texte veut qu'elle y reste et remonte sur le
# dessus. Modele du raccourci : il019/hood, modele de la remontee sur le
# dessus : ag001b (Sharon Carter), `Faces.MoveAllToDeck([face], deck, "Top",
# effect)` (faces.py:60).
#
# « Then, shuffle the encounter deck » : c'est le SELECTEUR qui remelange, pas
# une ligne de code. `SearchInternal.SearchForCardsInternal` construit
# `Select.From(..., not_shuffle=False, by_search=True)` : toute fouille de deck
# du moteur remelange le deck fouille (search_internal.py:60-66). La remontee
# sur le dessus a donc bien lieu APRES le melange, dans l'ordre imprime.
#
# « Draw 1 card » -> `initiator.DrawUp(1, effect)`, inconditionnel (aucun
# « if » imprime) : la pioche a lieu meme si aucune carte n'a ete trouvee.
#
# « Action: » nu sur une carte JOUEUR -> `AbilityType.Action`, jouable dans les
# deux formes (meme lecture que wc011 Teleport).

def GetAbilities() -> Sequence['Ability']:

    def transmutation(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this, message)

        initiator = effect.GetInitiator()
        if initiator is None:
            return

        face = Search.SearchForCard(
            effect,
            initiator,
            include_encounter_deck=True,
            not_move=True,
        )
        if face is not None:
            deck = Worlds.GetEncounterDeck(effect)
            Faces.MoveAllToDeck([face], deck, "Top", effect)

        initiator.DrawUp(1, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            transmutation,
        ).SetPlay(),
    ]
