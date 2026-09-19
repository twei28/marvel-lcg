from . import *

# Security Guard (CIVILIAN, INFLUENCED) — Patrol, Vulnerable : bases.
# When Defeated: Discard the ally with the highest ATK (among allies) in play.

def GetAbilities() -> Sequence['Ability']:

    def vaincu(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        allie = Filter.One(Worlds.GetOnFieldAllies(effect), effect, highest_atk=True)
        if allie:
            Faces.DiscardAll([allie], effect)

    return [
        AbilityFactory.WhenUnitBeDefeated(AbilityType.WhenDefeated, "This", vaincu),
    ]
