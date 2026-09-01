from . import *

# Multi-Tasking ([physical]) — evenement signature. THWART. ATTACK. Cout 1.
# Hero Action (thwart)(attack): Deal 1 damage to all enemy characters and
#   remove 1 threat from all schemes. If this was the first card you played
#   this turn -> repeat this hero action.
#
# ⚠ DEUX card_id pour UNE carte : l'exemplaire 6/15 porte une ressource
# [mental] et l'exemplaire 7/15 une ressource [physical]. Meme nom, meme
# texte, meme cout — seule l'icone change. Precedent moteur : 01043a/b/c/d
# « Wakanda Forever! », quatre card_id pour quatre ressources. Ce fichier est
# la copie stricte de bt007a, dont il partage toute l'analyse.
#
# Cartes de reference :
#  - degats a TOUS les ennemis : 01022 Ground Stomp. Elle emploie
#    `SetTarget(Enemy, range="All")`, ce qui ne convient PAS ici : la carte a
#    un SECOND effet de zone sur les manigances, et un `SetTarget` ne porte
#    qu'un type de cible. On passe donc par
#    `Worlds.FindCardsOnField(effect, card_type=Enemy)`, qui rend la meme
#    liste sans monopoliser le selecteur.
#  - retrait sur TOUTES les manigances : le litteral moteur `"EachScheme"` de
#    `RemoveThreatFromSchemes` (card_face.py:707), comme 50134/ho015 le font
#    pour la pose (recette moteur §2).
#  - « premiere carte jouee ce tour » : aucune carte officielle ne l'exprime.
#    Le compteur existe pourtant : `player.stat.this_turn_played_cards`
#    (player_stat.py:7), vide a chaque debut de tour.
#
# ⚠ ARBITRAGE (utilisateur, 31/08/2026) : « repeat this hero action » relu
# naivement BOUCLE A L'INFINI — la condition « first card you played this
# turn » reste vraie pendant la repetition, donc l'effet se relancerait sans
# fin. La carte est codee avec **une seule** repetition : l'effet se resout
# deux fois au total, jamais plus. Consigne au §6 du journal de portage,
# point 5, pour l'auteur.
#
# ⚠ On compte les AUTRES cartes jouees, pas la longueur de la liste : selon le
# moment ou le moteur enregistre la carte jouee, Multi-Tasking peut deja y
# figurer ou non. Filtrer sur `is not this` donne le meme resultat dans les
# deux cas.

def GetAbilities() -> Sequence['Ability']:

    def multi_tasking(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        initiator = effect.GetInitiator()
        if initiator is None:
            return

        autres = [f for f in initiator.stat.this_turn_played_cards if f is not this]
        premiere_carte = (len(autres) == 0)

        def corps() -> None:
            ennemis = Worlds.FindCardsOnField(effect, card_type=Enemy)
            if ennemis:
                this.DealDamage(ennemis, 1, effect)
            this.RemoveThreatFromSchemes("EachScheme", 1, effect)

        corps()
        if premiere_carte:
            corps()

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            multi_tasking
        # ⚠ UN SEUL appel a SetLabel, avec les deux libelles : `SetLabel` pose
        # `assert self.labels == []` (ability.py:380), donc le chainer deux
        # fois leve une AssertionError des le chargement de la carte.
        ).SetPlay().SetLabel('thwart', 'attack'),
    ]
