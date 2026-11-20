from . import *

# Psychic Leech (TREACHERY PSIONIC TACTIC, x2 : hf618, hf619). Boost 1. « When Revealed : Discard your hand. Draw up to your hand size. For each card
# you discard in this way, heal 1 damage from Cassandra Nova, if you cannot, place a Cassandra Controls counter on your identity. »
# Cartes de reference : `Player.DiscardAllHands` (rend le nombre de cartes), `Player.DrawUp("Max")`, `HealHealth` (mt / hf122).
# ⚠ « if you cannot » : A CHAQUE carte defaussee (Nova sans degat -> compteur) ; ordre imprime : defausse, pioche, puis les soins / compteurs.


def GetAbilities() -> Sequence['Ability']:
    def revelee(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        n = joueur.DiscardAllHands(effect)
        joueur.DrawUp("Max", effect)
        for _ in range(n):
            villain = VilainCN(effect)
            if villain is not None and villain.IsInPlay() and villain.GetLostHealth() > 0:
                villain.HealHealth(1, effect)
            else:
                PoserControle(effect, joueur, 1)

    return [AbilityFactory.WhenThisRevealed(None, revelee)]
