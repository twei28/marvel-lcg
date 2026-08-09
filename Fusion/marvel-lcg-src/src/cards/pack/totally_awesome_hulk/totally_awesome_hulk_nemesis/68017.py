from . import *

# * Krackalakassian — custom « DesignHacker »
# When Revealed: Krackalakassian gets +2 hit points per player.
# Forced Interrupt: When Krackalakassian attacks, take 2 indirect damage.


def GetAbilities() -> Sequence['Ability']:

    def par_joueur(effect: 'Effect', ui: List['CardFace']) -> int:
        return len(Worlds.GetPlayers(effect))

    def krackalakassian(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this.CastTo(Minion)

        player = this.GetEngagedPlayer()
        if player is not None:
            player.GetIdentity().TakeIndirectDamage(2, effect)

    return [
        AbilityFactory.ThisGainKeyword(
            par_joueur,
            health=2,
        ),
        AbilityFactory.WhenUnitMakeAttack(
            AbilityType.ForcedInterrupt,
            "This",
            krackalakassian,
        ),
    ]
