from . import *

# Assassination Plot — custom « Rainy » (nemesis d'Agent 13 / Sharon Carter)
# When Revealed: Discard the ally you control with the highest remaining hit
#   points. If you cannot, place 2 threat on this scheme.
#
# Modele : Cull the Weak (moon_knight/moon_knight_nemesis/mk015.py), qui
# filtre les allies controles par le joueur via `GetControlByPlayer() ==
# player` puis trie sur `.health` -- les points de vie RESTANTS, pas les PV
# imprimes (`printed_hit_points`), exactement ce que dit « highest remaining
# hit points ». Cull the Weak prend le minimum (le plus faible) ; ici on
# prend le maximum (`max`). Le repli « impossible » pose 2 menaces sur ce
# complot lui-meme : `this.PlaceThreatOnSchemes("MainScheme", ...)` ne
# convient pas ("this scheme", pas la manigance principale) -- c'est
# `this.PlaceThreatOnSchemes([this], 2, effect)`, comme Bomb Scare (01109) et
# la plupart des complots annexes du depot.

def GetAbilities() -> Sequence['Ability']:

    def assassination_plot(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        player = message.GetToPlayer()

        allies = [
            x for x in Worlds.FindCardsOnField(effect, card_type=Ally)
            if x.GetControlByPlayer() == player
        ]
        if allies:
            plus_de_pv = max(allies, key=lambda x: x.health)
            Faces.DiscardAll([plus_de_pv], effect)
        else:
            this.PlaceThreatOnSchemes([this], 2, effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            assassination_plot
        ),
    ]
