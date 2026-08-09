from . import *

# Threat Assessment — custom « DesignHacker »
# When Revealed: Deal 3 damage to the identity with the most remaining hit
#   points.


def GetAbilities() -> Sequence['Ability']:

    def threat_assessment(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)

        identities = [
            player.GetIdentity()
            for player in Worlds.GetPlayers(effect)
            if player.GetIdentity() is not None
        ]
        if not identities:
            return

        maximum = max(x.health for x in identities)
        cibles = [x for x in identities if x.health == maximum]

        this.DealDamage(cibles[:1], 3, effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            threat_assessment,
        ),
    ]
