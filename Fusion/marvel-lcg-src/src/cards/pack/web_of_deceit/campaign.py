from . import *

# LE CARNET DE LA CAMPAGNE « WEB OF DECEIT »
#
# La voie a ete tranchee au §15 de la fiche : les arbres de talents passent par
# le carnet, qui sait deja poser des cartes IMPOSEES dans le deck d'un joueur
# entre deux scenarios. Un palier d'arbre est exactement cela — « ces cartes
# restent avec le joueur pour le reste de la campagne et DOIVENT figurer dans
# son deck » (livret p.2).
#
# ⚠ CE QUE CETTE VOIE NE REND PAS : l'arbre ne s'affiche pas comme un arbre. Le
# joueur voit, entre deux rencontres, la liste des cartes de son palier — les
# cinq arbres melanges, puisque le carnet ne retient pas lequel il a choisi.
# La progression est fidele, sa mise en scene ne l'est pas.

PALIERS = ("Talent Tier 0", "Talent Tier 1", "Talent Tier 2",
           "Talent Tier 3", "Talent Tier 4")


def ChaqueJoueurRetrouveSesTalents() -> 'Ability':
    """Remet dans le deck de chaque joueur les cartes de talent deja gagnees.

    Le carnet enregistre un choix par palier et par joueur (`parJoueur`), sous
    les cles listees ci-dessus. A chaque mise en place de campagne, on les relit
    et on genere les cartes dans le deck de leur proprietaire : le deck grossit
    d'une carte par scenario gagne, ce que le livret demande.
    """
    from game.operate.worlds import Worlds
    from game.operate.campaign_logs import CampaignLog
    from game.card.factory import CardFactory

    def action(effect: 'Effect', message: 'Message.WhenCampaignSetup') -> None:
        for player in Worlds.GetPlayers(effect):
            gagnees = []
            for cle in PALIERS:
                card_id = CampaignLog.GetStrByPlayer(cle, player.player_id, effect)
                if card_id:
                    gagnees.append(card_id)
            if gagnees:
                CardFactory.GenerateCards(gagnees, player.player_deck, effect.world)
                player.player_deck.Shuffle(effect)

    return AbilityFactoryCampaign.WhenCampaignSetup(
        action,
    )
