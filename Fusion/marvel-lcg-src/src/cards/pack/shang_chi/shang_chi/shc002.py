from . import *

# State of Flow — SOUTIEN. Permanent. Setup. (card_id shc002, pas dans les 15 cartes du deck de heros)
# Forced Response: After you play an ATTACK event, place it faceup on top here, forming a pile. After the player deck
#   runs out, shuffle each card placed here back into the player deck.
# Keyword - Flow: Look at the top card here. If a printed resource on that card matches the resource required by the
#   "Flow" ability, you may also resolve its effects.
#
# Cartes de reference :
#  - `gs117a` / `gs119` (Galactic Storm) : « tuck » face VISIBLE = `hote.PlaceCardHere(faces, True, effect)` ; les
#    cartes posees vivent dans `hote.GetPlacedCardArea()`.
#  - `sk288` Sy-Torak Gem / `aa012` Regained Youth : « after your deck runs out » = `AfterDeckRunOut(type, deck_du_joueur, op)`.
#  - `28002` Ms. Marvel : `AfterPlayerPlayedCard(type, "You", CardFinder(...), op)`.
#  - le mot-cle Flow lui-meme : helpers `AccepterFlow` / `FlowResolu` du set (fiche mots-cles/flow.md).
#
# ⚠ Mots-pieges :
#  - « Permanent » et « Setup » : bases automatiques du moteur (`desc.Permanent`/`desc.Setup`) ; l'entree en jeu se fait par
#    shc001b (mise de cote, comme Storm) : aucun code ici.
#  - « After YOU play an ATTACK event » : un evenement ATTACK du joueur seulement (trait ATTACK, type Event), jamais un
#    evenement d'un autre joueur ni une carte sans ce trait.
#  - le Forced Response passe APRES la defausse de l'evenement (Event.OnAfterPlay defausse avant d'envoyer
#    AfterPlayerPlayedCard) : on le RETIRE donc de la defausse pour le poser sur la pile ; si une autre carte l'a deja
#    deplace (retour en main...), on n'y touche pas.
#  - « place it faceup on TOP here » : la derniere jouee est le dessus ; le Flow suivant regarde celle-la.
#  - « After the player deck runs out » : `AfterDeckRunOut` part quand le DERNIER tirage vide le deck ; chaque carte de la
#    pile retourne dans LE DECK DU JOUEUR (melange). Le moteur remelange ensuite la defausse avec penalite comme d'habitude.


def GetAbilities() -> Sequence['Ability']:

    def joueur_de_la_pile(effect: 'Effect') -> 'Player':
        return effect.this.GetControlByPlayer()

    def mon_deck(effect: 'Effect') -> 'Deck':
        return joueur_de_la_pile(effect).player_deck

    def empiler(effect: 'Effect', message: 'Message.AfterPlayerPlayedCard') -> None:
        this = effect.this.CastTo(Support)
        joueur = joueur_de_la_pile(effect)
        face = message.played_face
        if face not in joueur.discard_pile.Get():
            return
        this.PlaceCardHere([face], True, effect)

    def vider_dans_le_deck(effect: 'Effect', message: 'Message.AfterDeckRunOut') -> None:
        this = effect.this.CastTo(Support)
        Unused(message)

        joueur = joueur_de_la_pile(effect)
        cartes = list(this.GetPlacedCardArea().Get())
        if cartes:
            Faces.ShuffleAllTo(cartes, joueur.player_deck, effect)

    return [
        AbilityFactory.AfterPlayerPlayedCard(
            AbilityType.ForcedResponse,
            "You",
            CardFinder(card_type=Event, traits=["ATTACK"]),
            empiler,
        ),
        AbilityFactory.AfterDeckRunOut(
            AbilityType.ForcedResponse,
            mon_deck,
            vider_dans_le_deck,
        ),
    ]
