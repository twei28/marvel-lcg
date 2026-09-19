from cards.pack import *
from cards.pack.fne.campaign import Retirees, SOUTIENS_DAILY_BUGLE, PRISONNIERS_DU_RAFT

# Environnements de campagne (60205-60209, une carte, deux faces : Completed
# recto, Failed verso) et l'alliee Mary Walker (60210). Leur texte « Setup: »
# se resout quand la carte est deja en jeu, posee par la mise en place de
# campagne (cards/pack/fne/campaign.py) : AfterGameSetup, qui part APRES les
# mulligans (« Resolve Character Setup Abilities », journal du 18/09/2026), ce
# qui couvre aussi les « After resolving mulligans » du livret.


def ChercherEnMain(effect: 'Effect', joueur: 'Player', card_type) -> None:
    """« each player may search their deck and discard pile for a <type> and
    add it to their hand. In expert mode, each player who did so discards
    1 card from their hand. »"""
    face = Search.SearchForCard(
        effect, joueur,
        include_player_deck=True, include_player_discard_pile=True,
        card_type=card_type, may=True, not_move=True,
    )
    if face is None:
        return
    Faces.AddToHand([face], joueur, effect)
    if Worlds.IsExpert(effect):
        DefausserDeLaMain(effect, joueur, 1)


def DefausserDeLaMain(effect: 'Effect', joueur: 'Player', n: int) -> None:
    for _ in range(n):
        main = list(joueur.hand_cards.Get(True))
        if not main:
            return
        carte = main[0] if len(main) == 1 else joueur.AskChooseFace(main, effect, prompt="Choose a card to discard")
        if carte is None:
            return
        Faces.DiscardAll([carte], effect)


def RechuteVers(card_type):
    def apres_revelation(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Ally)
        this.HealHealth("All", effect)
        this.card.Flip(effect)

    def par_son_controleur(effect: 'Effect', message: 'Message.WhenCardRevealed') -> bool:
        return message.GetToPlayer() is effect.this.GetControlByPlayer()

    return AbilityFactory.WhenCardRevealed(AbilityType.ForcedResponse, card_type, apres_revelation, conditions=[par_son_controleur])
