from . import *

# Secret Initiative — COMPLOT ANNEXE nemesis (N 1/5). Hazard 1, menace de
# depart 1[per_hero].
# [star] Threat cannot be removed from this scheme.
# Response: When cards from the encounter deck are looked at by player
#   abilities, put each minion found into play engaged with that player.
#   Place 1 skrull counter on this card for each minion put into play this
#   way. When there are 3+ counters here, discard this scheme.
#
# CARTES DE REFERENCE
#  - « Threat cannot be removed from this scheme », sans condition :
#    **`01139b`** Countdown to Oblivion (`AbilityFactory.
#    ThreatCannotBeRemovedFromWhile("This")`, aucun filtre).
#  - « put it into play engaged with <joueur> » : **`br011`** Hammer Time /
#    **`ar014`** (`face.PutIntoPlay(joueur, effect)` puis `face.CastTo(Minion)
#    .EngagePlayer(joueur, effect)`).
#  - « Place N counters » : **`sentry rr002`** (modele `Faces.
#    PlaceCountersOn([this], n, "skrull", effect)`).
#  - « When there are 3+ counters here, discard this » : **`AfterCounterPlacedOn
#    (.., at_least=3, ..)`** (factory/counter.py:97) + `Faces.DiscardAll([this],
#    effect)` (modele **`hf041`** Cerebro Insights pour le `DiscardAll`).
#  - Le declencheur « cards from the encounter deck are looked at BY PLAYER
#    ABILITIES » : primitive ajoutee le 04/11/2026 pour CETTE carte,
#    `AbilityFactory.AfterPlayerLookedAtEncounterDeck` (factory/deck.py),
#    posee depuis le point de passage unique `PlayerAction.LookAtDeck`
#    (joueur.py:1884 ; couvre Tri-Force Vision ET toute autre capacite « look
#    at the top N cards of the encounter deck » deja existante, une
#    soixantaine d'appels).
#
# TEXTE CONTRE CODE
#  « cards from the encounter deck are LOOKED AT » : le declencheur se pose au
#  moment du REGARD, pas d'un defaussement ou d'une revelation — les cartes
#  restent sur le deck. « EACH minion FOUND » : on filtre `message.
#  looked_faces` par type Minion, sans autre condition de trait. « engaged
#  with THAT PLAYER » : celui qui a regarde (`message.GetToPlayer()`), pas le
#  premier joueur. « for EACH minion put into play THIS WAY » : le compte de
#  jetons suit le nombre REELLEMENT mis en jeu (un `PutIntoPlay` peut echouer
#  si la carte n'est plus sur le deck au moment de la resolution), pas le
#  nombre trouve au regard. Decompte Hazard/menace de depart : natifs (`desc`).


def GetAbilities() -> Sequence['Ability']:

    def quand_regarde(effect: 'Effect', message: 'Message.AfterPlayerLookedAtEncounterDeck') -> None:
        joueur = message.GetToPlayer()
        minions = [f for f in message.looked_faces if Minion.IsType(f)]
        if not minions or joueur is None:
            return

        mises_en_jeu: List['CardFace'] = []
        for sbire in minions:
            if sbire.PutIntoPlay(joueur, effect):
                if sbire.card.IsOnField():
                    sbire.CastTo(Minion).EngagePlayer(joueur, effect)
                    mises_en_jeu.append(sbire)

        if mises_en_jeu:
            this = effect.this.CastTo(CanPlaceCounter)
            Faces.PlaceCountersOn([this], len(mises_en_jeu), "skrull", effect)

    def seuil_atteint(effect: 'Effect', message: 'Message.AfterCardPlacedCounter') -> None:
        Unused(message)
        Faces.DiscardAll([effect.this], effect)

    return [
        AbilityFactory.ThreatCannotBeRemovedFromWhile("This"),
        AbilityFactory.AfterPlayerLookedAtEncounterDeck(
            AbilityType.ForcedResponse,
            quand_regarde,
        ),
        AbilityFactory.AfterCounterPlacedOn(
            AbilityType.ForcedResponse,
            "This",
            "skrull",
            seuil_atteint,
            at_least=3,
        ),
    ]
