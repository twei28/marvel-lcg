from . import *

# * Jessica Drew — alter ego de Spider-Woman.
# Action : regardez la carte du dessus de n'importe quel deck. (Une fois par round.)
#
# CARTES DE REFERENCE
#  - `17020` Cosmo : « un deck de joueur ou le deck rencontre » choisi PAR SON NOM (`AskChooseOneText` sur les decks), jamais
#    par une cible qui montrerait les cartes du dessus face visible.
#
# TEXTE CONTRE CODE
#  « ANY deck » : tout deck de joueur (le sien, celui d'un autre, l'éventuel deck supplémentaire) ou le deck rencontre ; un
#    deck vide n'est pas proposé. « Look at the top card » : UNE carte, celle du deck choisi, après le choix.
#  Rapport #162 (22/11/2026) : l'ancienne cible `AnyDecksTopCard` montrait la carte du dessus de CHAQUE deck avant le choix.
#  Cas : tools/cas/jessica_drew.py (rouge avec l'ancien script, vert avec celui-ci).

def GetAbilities() -> Sequence['Ability']:

    def jessica_drew(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(AlterEgo)
        Unused(this)
        initiator = effect.GetInitiator()

        # « Look at the top card of ANY deck » : on choisit le deck PAR SON NOM, puis seulement on regarde sa carte du dessus.
        # Rapport #162 (22/11/2026) : l'ancienne cible (`AnyDecksTopCard`) montrait la carte du dessus de CHAQUE deck face
        # visible avant le choix, alors que la règle n'en donne qu'une.
        decks: List['Deck'] = []
        libelles: List[str] = []
        for player in Worlds.GetPlayers(effect):
            if player.player_deck.GetSize() > 0:
                decks.append(player.player_deck)
                libelles.append("Player deck (%s)" % player.GetIdentity().name.lstrip("* ").strip())
            if player.additional_deck.GetSize() > 0:
                decks.append(player.additional_deck)
                libelles.append("Additional deck (%s)" % player.GetIdentity().name.lstrip("* ").strip())
        for deck in Worlds.GetEncounterDecks(effect):
            if deck.GetSize() > 0:
                decks.append(deck)
                libelles.append("Encounter deck")
        if not decks:
            return
        deck = decks[0] if len(decks) == 1 else initiator.AskChooseOneText(decks, libelles, titre="Jessica Drew: look at the top card of which deck?")
        initiator.LookAtDeck(deck, 1, effect)

    return [
        # Double Agent — Choose two aspects instead of one during deck-building. You must include an equal number of cards from those aspects in your deck.
        # Action: Look at the top card of any deck. (Limit once per round.)
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            jessica_drew
        ).LimitOncePerRound(),
    ]
