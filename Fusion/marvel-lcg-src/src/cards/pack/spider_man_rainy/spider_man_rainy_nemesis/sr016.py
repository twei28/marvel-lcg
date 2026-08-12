from . import *

# Jump Scare — custom « Rainy » (nemesis de Peter Parker)
# When Revealed: Deal yourself a facedown encounter card. Take 1 damage for
#   each facedown encounter card you have in front of you.
# [star] Boost: Deal yourself a facedown encounter card.

def GetAbilities() -> Sequence['Ability']:

    def jump_scare(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        player = message.GetToPlayer()

        player.DealEncounterCards(1, effect)
        n = player.dealt_encounter_cards.GetSize()
        if n > 0:
            this.DealDamage([player.GetIdentity()], n, effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        this = effect.this.CastTo(Treachery)
        Unused(this)
        player = message.GetToPlayer()
        if player:
            player.DealEncounterCards(1, effect)

    return [
        AbilityFactory.WhenThisRevealed(None, jump_scare),

        AbilityFactory.WhenCardBecomeBoost(
            "This",
            boost
        ),
    ]
