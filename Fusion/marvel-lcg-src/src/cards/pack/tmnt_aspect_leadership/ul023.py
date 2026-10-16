from . import *

# Rubble Rouser — EVENEMENT Leadership (TMNT Aspects, Inkwire), cout 1*, [physical]. FERAL. NYC.
# [star] Rampage 3. (As an additional cost for this card, take 3 damage and discard 3 cards from the top
#   of your deck.)
# Hero Response: After an ally is defeated, search your deck for an ally and put it into play, exhausted.
#   (Shuffle.)
#
# MOT-CLE (fiche lue AVANT le code) : RAMPAGE X — docs/reference/mots-cles/rampage.md.
#   `CostFunc.Rampage(3)` sur la capacite de JEU (ici la Reponse de heros), « 1* » = simple rappel.
#
# CARTES DE REFERENCE
#  - `bk014` Proper Funeral : « Response: After an ally is defeated » joue depuis la main =
#    `AfterUnitBeDefeated(<type>, Ally, op).SetPlay()`.
#  - `td001b` Donnie : « search your deck for X and put it into play, exhausted. (Shuffle.) » =
#    `Search.PlayerCard(..., include_player_deck=True, ...)` puis `PutIntoPlay(joueur, effect, exhaust=True)`.
#  - `ua015` Demolish : Rampage sur la capacite de jeu.
#
# TEXTE CONTRE CODE
#  ⚠ « HERO Response » : sous-type `HeroResponse` (forme heros uniquement).
#  ⚠ « an ally is defeated » : N'IMPORTE quel allie (le votre ou celui d'un autre joueur), quelle que
#    soit la cause.
#  ⚠ « search YOUR deck for AN ally » : n'importe quel allie de votre deck ; aucun -> rien (on melange).
#  ⚠ « put it into play, EXHAUSTED » : sous votre controle, incline.
#  ⚠ Rampage est un COUT : impaye (identite Tenace, deck et defausse vides) -> carte non jouee.
#  Aucune limite imprimee.


def GetAbilities() -> Sequence['Ability']:

    def rubble_rouser(effect: 'Effect', message: 'Message.AfterUnitBeDefeated') -> None:
        this = effect.this.CastTo(Event)
        Unused(this, message)

        joueur = effect.GetInitiator()
        allie = Search.PlayerCard(
            effect,
            joueur,
            include_player_deck=True,
            card_type=Ally,
        )
        if allie is not None:
            allie.PutIntoPlay(joueur, effect, exhaust=True)

    return [
        AbilityFactory.AfterUnitBeDefeated(
            AbilityType.HeroResponse,
            Ally,
            rubble_rouser,
        ).SetPlay()
        .SetCostFunc(CostFunc.Rampage(3)),
    ]
