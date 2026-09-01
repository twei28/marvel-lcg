from . import *

# Beast's Lab — soutien signature. LOCATION. X-MEN. Cout 4. RES [mental]
# Hero Action: Exhaust Beast's Lab -> choose a player. That player searches
#   their deck and discard pile for an upgrade and places it into their hand.
#
# Cartes de reference :
#  - 01034 * Stark Tower : « Alter-Ego Action: Exhaust Stark Tower -> choose a
#    player. That player returns the topmost [[Tech]] upgrade... ». C'est le
#    MEME squelette de bout en bout — inclinaison en cout, choix d'un joueur
#    par un `SetTarget` qui rend des identites, puis `Players.ForEachTargets`
#    pour agir sur le joueur choisi. Seule la fouille differe (recette §2).
#  - la fouille deck + defausse : 04001b * Clint Barton et 04141 Prison Camps,
#    `Search.PlayerCard(effect, player, include_player_deck=True,
#    include_discard_pile=True, ...)` puis `player.GainCard(face, effect)`.
#
# ⚠ « THAT player searches THEIR deck » : c'est le joueur CHOISI qui fouille
# SES propres zones, pas le proprietaire du labo (mot-piege `that <nom>` de
# PROCESSUS-CARTE etape 5). Passer `initiator` a `Search.PlayerCard` ferait
# fouiller le mauvais deck en multijoueur.
#
# ⚠ « an upgrade », sans trait ni nom : contrairement a Stark Tower qui exige
# [[TECH]], on ne pose que `card_type=Upgrade`.
#
# ⚠ Le selecteur ne propose QUE les joueurs qui ont vraiment une amelioration
# a trouver, comme le fait Stark Tower : sans ce filtre, le joueur pourrait
# incliner un soutien a 4 ressources pour rien.
#
# ⚠ Le « (Shuffle.) » est implicite des qu'on fouille le DECK : c'est le
# comportement par defaut de `Search.PlayerCard` (recette moteur §2).

def GetAbilities() -> Sequence['Ability']:

    def beasts_lab(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        Unused(this, message)

        def action(player: 'Player'):
            face = Search.PlayerCard(
                effect,
                player,
                include_player_deck=True,
                include_discard_pile=True,
                card_type=Upgrade,
            )
            if face:
                player.GainCard(face, effect)

        Players.ForEachTargets(effect.targets, action)

    def joueurs_avec_une_amelioration(effect: 'Effect') -> Sequence['AlterEgo|Hero']:
        units: List['AlterEgo|Hero'] = []
        for player in Worlds.GetPlayers(effect):
            zones = player.player_deck.Get(True) + player.discard_pile.Get(True)
            if any(Upgrade.IsType(card) for card in zones):
                units.append(player.GetIdentity())
        return units

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            beasts_lab
        ).SetTarget(joueurs_avec_une_amelioration)
        .SetCostFunc(CostFunc.Exhaust("This")),
    ]
