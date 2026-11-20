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
#  - `spider_man_rainy/sr009` J. Jonah Jameson : meme probleme (« a picture of
#    X » est du dessin, le moteur ne le lit pas), meme solution (poser la
#    question au joueur).
#
# ⚠ ARBITRAGE, decision utilisateur du 13/09/2026 puis du 08/11/2026.
#  1. « l'image de votre identite » ne se devine pas : le RELEVE manuel des
#     illustrations (`PorteLImageDe`, 5746 images) est reste vide — personne
#     ne l'a jamais rempli, et Muse n'a donc JAMAIS tourne sur la vraie regle,
#     seulement sur son repli (« carte signature »), qui n'est pas ce texte
#     imprime demande. Remplace le 08/11/2026 : on pose la question au joueur,
#     qui REGARDE les cartes defaussees (visibles dans la defausse) et compte
#     lui-meme. Une seule question par joueur (un nombre, 0 a 3), pas trois
#     questions Oui/Non d'affilee (decision utilisateur du 08/11/2026).
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
            if not defaussees:
                return
            noms = ", ".join(f'"{c.name}"' for c in defaussees)
            combien = joueur.AskChooseOneText(
                list(range(len(defaussees) + 1)),
                [str(i) for i in range(len(defaussees) + 1)],
                f"Art Imitates Death: of the {len(defaussees)} cards just discarded "
                f"({noms}), how many have a picture of your identity on them?",
            )
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
