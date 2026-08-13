from . import *

# I Can Do This All Day

def GetAbilities() -> Sequence['Ability']:

    def i_can_do_this_all_day(effect: 'Effect', message: 'Message.WhenUnitWouldBeDefeated') -> None:
        this = effect.this.CastTo(Upgrade)

        message.SetBeInstead(effect)
        # « 1 [per_hero] threat » : la notation "1*" du moteur, que
        # ConvertPerPlayerIconToInt multiplie par le nombre de joueurs.
        this.PlaceThreatOnSchemes("MainScheme", "1*", effect)
        for target in effect.targets:
            target.SetHealth(1, effect)
        Faces.RemoveAllFromGame([this], effect)

    return [
        AbilityFactory.WhenUnitWouldBeDefeated(
            AbilityType.Interrupt,
            "YourIdentity",
            i_can_do_this_all_day
        ).SetTarget("YourIdentity"),
    ]
