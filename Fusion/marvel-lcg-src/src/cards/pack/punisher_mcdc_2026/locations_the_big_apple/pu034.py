from . import *

# Midtown (5) — LIEU (environnement LOCATION), lieu de depart des joueurs.
# Action: Choose a player in this turf. They play an AVENGER, S.H.I.E.L.D., or TECH card from their hand, reducing its cost by 1.
# (Limit once per round.)
#
# Cartes de reference : 12024 (Team-Building Exercise : `PlayCardsLikeInTurn(cartes, effect, update_resources_cost=-1)` et cible
# `canbe_play=True`), 28020 (« choose a player » = cible `Identity`, joueur = `GetControlByPlayer()`), pu031 (Action de lieu
# + `LimitOncePerRound` + `Ville.AuLieu`), commun.py `AuChoixDuJoueur` (`ChooseAbilities` : c'est le JOUEUR CHOISI qui choisit sa carte).
# ⚠ « a player IN THIS TURF » : tout joueur dont la zone est celle de la rangee de Midtown (lui-meme compris), pas seulement celui qui
# occupe Midtown ; l'Action, elle, n'est offerte qu'a un joueur present a Midtown (`Ville.AuLieu`).
# ⚠ « AVENGER, S.H.I.E.L.D., OR TECH » : l'un des trois traits suffit (OU), `check_fn` ; « reducing its cost by 1 » : cout en ressources.
# ⚠ « Limit once per round » sans « per player » : globale.

TRAITS_MIDTOWN = ("AVENGER", "S.H.I.E.L.D", "TECH")


def GetAbilities() -> Sequence['Ability']:

    def dans_le_territoire(effect: 'Effect', face: 'CardFace') -> bool:
        joueur = face.GetControlByPlayer()
        return joueur is not None and joueur.GetGameArea() == effect.this.card.game_area

    def jouer_une_carte(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        Unused(message)
        for identite in effect.targets:
            joueur = identite.GetControlByPlayer()
            joueur.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility(
                    "",
                    lambda cartes, joueur=joueur: joueur.PlayCardsLikeInTurn(cartes, effect, update_resources_cost=-1),
                ).SetTarget(
                    traits=list(TRAITS_MIDTOWN), canbe_play=True, from_where=["YourHandCards"],
                ),
            )

    return [
        AbilityFactory.WhenInYourPlayTurn(AbilityType.Action, jouer_une_carte, conditions=[Ville.AuLieu])
        .SetTarget(Identity, check_fn=dans_le_territoire, is_optional=False)
        .LimitOncePerRound(),
    ]
