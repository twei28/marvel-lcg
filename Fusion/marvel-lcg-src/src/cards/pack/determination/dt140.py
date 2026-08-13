from . import *

# Path of Mercy

def GetAbilities() -> Sequence['Ability']:

    def path_of_mercy(effect: 'Effect', message: 'Message.AfterUnitAttackUnit') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)

        player = this.GetControlByPlayer()
        sbire = message.attacked
        if player is None or sbire.CastTo(CanHealth).health != 1:
            return
        player.DrawUp(1, effect)
        if len(Worlds.GetPlayers(effect)) == 1:
            Faces.DiscardAll([sbire], effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(
            "Players"
        ),
        AbilityFactory.AfterUnitAttackUnit(
            AbilityType.HeroResponse,
            "You",
            Minion,
            path_of_mercy,
        ),
    ]
