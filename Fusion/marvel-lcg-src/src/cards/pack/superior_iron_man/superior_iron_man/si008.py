from . import *

# Stark Island
#
# "recherchez... et mettez-le en jeu sous votre controle en payant son cout" :
# aucune carte du jeu entier ne combine recherche + mise en jeu + paiement du
# cout (toutes les recherches similaires jouent gratuitement ou ajoutent
# seulement a la main -- verifie par balayage complet de cards.json). Decision
# utilisateur (29/08/2026) : suivre le texte imprime, creer le mecanisme
# manquant. `Player.PlayAnAlly(ally, paying_cost)` (player_action.py:598) fait
# exactement ca mais est artificiellement restreint aux Ally : son corps
# n'utilise que des attributs generiques a toute carte jouable (`face.card`,
# `face.effect`, `face.Play`, `CardPlayer.Play` vit dans card_player.py, pas
# dans Ally). Generalisee en `Player.PlayACard(face, paying_cost)`, ajoutee a
# cote de PlayAnAlly sans y toucher (voir CORRECTIF dans player_action.py).
# Recherche modele The Bifrost (valk/25023.py) : `Search.PlayerCard(...)`.

def GetAbilities() -> Sequence['Ability']:

    def stark_island(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        Unused(this)
        initiator = effect.GetInitiator()
        face = Search.PlayerCard(
            effect,
            initiator,
            include_player_deck=True,
            include_discard_pile=True,
            trait="INDIVIDUAL",
            card_type=Support,
            may=True,
        )
        if face:
            initiator.PlayACard(face, True)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            stark_island,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
