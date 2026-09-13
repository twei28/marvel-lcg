from . import *

# Art Imitates Death — MANIGANCE ANNEXE du set modulaire. 2[per_hero] menaces,
# 2 icones de boost.
# <i>Muse is painting his macabre murals as a warning - are you next?</i>
# When Revealed: Discard the top 3 cards of each player's deck. For each card
#   discarded this way, deal 1 damage to each character whose picture was on
#   that card.
#
# CARTES DE REFERENCE
#  - `27086` * Mysterio : « discard the top N cards of EACH player's deck »,
#    par `Players.ForEachPlayer` + `joueur.DiscardDeckTopCards(n, effect)`.
#  - `as025` Underworld Impact : compter les cartes d'un joueur puis frapper
#    son identite d'autant.
#
# ⚠ ARBITRAGE, decision utilisateur du 13/09/2026 (deux questions posees).
#  1. « l'image de votre identite » = une CARTE SIGNATURE (helper
#     `EstUneCarteSignature`, voir le `__init__.py` du set).
#  2. « chaque PERSONNAGE dont l'image etait sur cette carte » : c'est le
#     HEROS DONT C'EST LE DECK qui encaisse, quoi que montre la carte. Une
#     carte signature ne represente pas toujours son heros — Nova Prime montre
#     Nova Prime — mais faire dependre les degats de l'allie represente rendait
#     l'effet loterie, et il pouvait ne rien faire du tout. Ici : jusqu'a 3
#     degats par joueur, previsibles, et c'est ce que raconte l'illustration
#     (Muse peint le heros sur son mur).
#
# TEXTE CONTRE CODE
#  ⚠ « EACH player » : tous les joueurs, pas seulement celui qui revele.
#  ⚠ « the top 3 cards » : trois, meme si le deck en contient moins — le
#    moteur remelange la defausse tout seul, on ne compte que ce qui SORT.
#  ⚠ Les degats ne sont PAS indirects : la carte ne le dit pas.
#  ⚠ Une manigance annexe n'a aucune capacite « When Defeated » ici : elle
#    frappe une fois, a la revelation, et reste sur la table pour sa menace.


def GetAbilities() -> Sequence['Ability']:

    def art_imitates_death(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        Unused(message)

        def peindre(joueur: 'Player') -> None:
            defaussees = joueur.DiscardDeckTopCards(3, effect)
            combien = len(CartesSignatureDe(defaussees))
            if combien <= 0:
                return
            identite = joueur.GetIdentity()
            if identite is not None:
                this.DealDamage([identite], combien, effect)

        Players.ForEachPlayer(effect, peindre)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            art_imitates_death,
        ),
    ]
