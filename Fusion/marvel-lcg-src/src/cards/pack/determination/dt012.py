from . import *

# Gone in a Flash

def GetAbilities() -> Sequence['Ability']:

    def check_half_hp(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> bool:
        hero = effect.GetInitiator().GetHero()
        return hero.health < hero.starting_health/2

    def gone_in_a_flash(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)

        Faces.GiveStatus(effect.targets, "Confused", effect)
        effect.GetInitiator().GetIdentity().ChangeToOtherForm(effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            gone_in_a_flash,
            conditions=[check_half_hp],
        ).SetPlay()
        .SetTarget(Enemy, canbe_confused=True),
    ]
