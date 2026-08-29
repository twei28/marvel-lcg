from . import *

# Pay the Price (1/2) — trahison nemesis d'Iron Lad (4/5)
# When Revealed: Discard 8 cards from your deck. If less than 8 cards were
#   discarded this way, this card gains surge.
#
# `player.DiscardDeckTopCards(8, effect)` rend la liste reellement
# defaussee (limitee par la taille du deck) ; `ThisCardGainSurge(effect)`
# est l'aide partagee du depot (modele : agent_13/agent_13_nemesis/
# ag014.py Hypnotic Suggestion).

def GetAbilities() -> Sequence['Ability']:

    def pay_the_price(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        Unused(this)

        player = message.GetToPlayer()
        discarded = player.DiscardDeckTopCards(8, effect)
        if len(discarded) < 8:
            ThisCardGainSurge(effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            pay_the_price,
        ),
    ]
