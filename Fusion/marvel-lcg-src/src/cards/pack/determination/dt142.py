from . import *

# Path of Temperance

def GetAbilities() -> Sequence['Ability']:

    def path_of_temperance(effect: 'Effect', message: 'Message.AfterUnitAttackUnit') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)

        sbire = message.attacked
        # « exactement vaincu » : le sbire est tombe SANS degat en trop.
        if not message.has_defeated_target or message.excess_damage > 0:
            return
        Unused(sbire)
        for player in Worlds.GetPlayers(effect):
            faces = player.DiscardHandCards((0, 1), effect)
            if faces:
                player.DrawUp(1, effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(
            "Players"
        ),
        AbilityFactory.AfterUnitAttackUnit(
            AbilityType.HeroResponse,
            "You",
            Minion,
            path_of_temperance,
        ),
    ]
