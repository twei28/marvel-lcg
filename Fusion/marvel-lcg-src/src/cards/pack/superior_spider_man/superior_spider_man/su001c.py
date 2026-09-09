from . import *

# * Elliot Tolliver — ALTER-EGO. REC 4, main 6, 10 PV. CLONE. GENIUS. SCIENTIST.
# Master Planner — Action: Attach 1 card from your hand facedown to Contingency
#   Plan (to a maximum of 1) -> draw 1 card. (Limit once per round.)
#
# ⚠⚠ CE HEROS A DEUX ALTER-EGOS, ET CELUI-CI EN EST UN. L'autre est
# `su001b Peter Parker`, au texte STRICTEMENT IDENTIQUE ; seuls le nom, les traits et
# l'obligation (su014 Crisis of Conscience) changent. L'insert : « choose one of these
# alter-egos to use this game and its corresponding obligation ». Deux decks de
# depart, arbitrage utilisateur du 08/09/2026 — voir l'en-tete du set.
#
# CARTES DE REFERENCE
#  - `aa002` (pack agatha_harkness) et `dz014` (pack dazzler) : le couple
#    « poser une carte face cachee sous une autre » +
#    `YouMayPlayCardLikeInHand(from_where="ThisPlacedCard")`. Ici cette seconde
#    moitie vit sur `su012` Contingency Plan, la carte qui RECOIT.
#  - `face.PlaceCardHere(cartes, False, effect)` (card_face.py:1037) : le
#    `False` est le `face_up`, donc bien FACE CACHEE.
#
# TEXTE CONTRE CODE
#  ⚠ « ATTACH ... TO CONTINGENCY PLAN » : la carte doit etre EN JEU. Sans elle
#    l'Action n'a aucune cible — d'ou la condition, qui evite de proposer une
#    action impossible (RECETTES §1, lecon `bc010`).
#  ⚠ « TO A MAXIMUM OF 1 » : le plafond porte sur ce qui est DEJA pose sous
#    Contingency Plan, pas sur le nombre d'usages. Deuxieme filtre de la
#    condition.
#  ⚠ « -> draw 1 card » : la fleche fait de l'attache le COUT et de la pioche
#    l'EFFET. Si rien n'est attache, rien n'est pioche.
#  ⚠ « Action » et non « Alter-Ego Action » : mais la capacite vit sur la face
#    ALTER-EGO, elle n'existe donc qu'en forme civile. Rien a ajouter.
#  ⚠ « Limit once per round » -> `LimitOncePerRound()`. Temoin d'epuisement
#    exige (PROCESSUS-CARTE 7 bis) : deux Actions dans le meme round, et la
#    TAILLE DE MAIN mesuree au second.


def GetAbilities() -> Sequence['Ability']:

    def plan_disponible(effect: 'Effect', message: Any) -> bool:
        Unused(message)
        plan = ContingencyPlanDuJoueur(effect)
        if plan is None:
            return False
        if len(CartesPoseesSous(plan)) >= 1:
            return False
        joueur = JoueurDeCetteCarte(effect)
        return joueur is not None and len(list(joueur.hand_cards.Get())) > 0

    def master_planner(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(AlterEgo)
        Unused(this, message)
        joueur = JoueurDeCetteCarte(effect)
        plan = ContingencyPlanDuJoueur(effect, joueur)
        if joueur is None or plan is None:
            return

        cartes = [c for c in effect.targets if c is not None]
        if not cartes:
            return
        if not plan.PlaceCardHere(cartes[:1], False, effect):
            return
        joueur.DrawUp(1, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            master_planner,
            conditions=[plan_disponible],
        ).SetName("Master Planner")
        .SetTarget(CardFinder(), range=(1, 1), from_where=["YourHandCards"])
        .LimitOncePerRound(),
    ]
