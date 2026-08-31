from . import *

# * Otto Octavius — soutien signature. PERSONA. Cout 2.
# Alter-Ego Action: Exhaust Otto Octavius -> choose a player. That player
#   searches their deck for a TECH upgrade and add it to their hand.
#   (Shuffle.)
#
# Cartes de reference :
#  - squelette « Alter-Ego Action: Exhaust <soutien> -> choose a player.
#    That player ... [[Tech]] upgrade ... their hand » : 01034 * Stark Tower,
#    jumeau quasi exact (lui repeche dans la DEFAUSSE, ici on fouille le
#    DECK) — meme ciblage par identite via `Players.ForEachTargets` ;
#  - la fouille : an001b * Aldrif Odinsdottir, `Search.PlayerCard(...,
#    include_player_deck=True, ...)` + `GainCard`. Le « (Shuffle.) » imprime
#    est le comportement par defaut de la fouille (`not_move=False`).
#
# ⚠ « That player searches THEIR deck » : c'est le joueur choisi qui fouille
# et qui recoit la carte, pas le proprietaire d'Otto.

def GetAbilities() -> Sequence['Ability']:

    def otto(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        Unused(this, message)

        def action(player: 'Player'):
            face = Search.PlayerCard(
                effect,
                player,
                include_player_deck=True,
                trait="TECH",
                card_type=Upgrade,
            )
            if face:
                player.GainCard(face, effect)

        Players.ForEachTargets(effect.targets, action)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            otto
        ).SetTarget(Identity)
        .SetCostFunc(CostFunc.Exhaust("This"))
    ]
