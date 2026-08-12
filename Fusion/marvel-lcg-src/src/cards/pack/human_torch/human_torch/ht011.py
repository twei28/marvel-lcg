from . import *

# Flame Off — custom « DesignHacker » (obligation de Human Torch)
# Give to the Johnny Storm player.
# Flip to alter-ego form and remove all flame counters from enemies in play.
# Then:
# - If up to 3 counters were removed this way, discard this obligation.
# - If 4 or more flame counters were removed this way, remove Flame Off from
#   the game.

def GetAbilities() -> Sequence['Ability']:

    def flame_off(effect: 'Effect', message: 'Message.WhenObligationGiveToPlayer') -> None:
        this = effect.this.CastTo(Obligation)

        player = message.GetGaveToPlayer()

        identity = player.GetIdentity()
        if player.IsHero():
            identity.ChangeToForm(AlterEgo, effect)

        ennemis = Worlds.GetOnFieldEnemies(effect)
        retires = Faces.RemoveCountersOn(ennemis, "All", 'flame', effect) or 0

        if retires >= 4:
            Faces.RemoveAllFromGame([this], effect)
        else:
            Faces.DiscardAll([this], effect)

    return [
        AbilityFactory.WhenThisObligationGiveToYou(
            flame_off
        ),
    ]
