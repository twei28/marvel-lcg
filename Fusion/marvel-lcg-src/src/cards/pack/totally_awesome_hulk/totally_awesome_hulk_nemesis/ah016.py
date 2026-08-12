from . import *

# * Fin Fang Foom — custom « DesignHacker »
# When Revealed: Fin Fang Foom gets +2 hit points per player.
# Forced Interrupt: When Fin Fang Foom has 2 hit points per player or fewer
#   remaining, his attacks gain overkill.


def GetAbilities() -> Sequence['Ability']:

    def par_joueur(effect: 'Effect', ui: List['CardFace']) -> int:
        return len(Worlds.GetPlayers(effect))

    def overkill(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        message.GainOverKill(effect)

    def presque_vaincu(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> bool:
        this = effect.this.CastTo(Minion)
        return this.health <= 2 * len(Worlds.GetPlayers(effect))

    return [
        # « +2 hit points per player » : appliqué en permanence plutôt qu'au
        # seul instant de la révélation, pour que les PV maximums restent
        # cohérents tant que le sbire est en jeu.
        AbilityFactory.ThisGainKeyword(
            par_joueur,
            health=2,
        ),
        AbilityFactory.WhenUnitMakeAttack(
            AbilityType.ForcedInterrupt,
            "This",
            overkill,
            conditions=[presque_vaincu],
        ),
    ]
