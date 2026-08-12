from . import *

# Thwip! — custom « Rainy »
# Hero Action: Ready your hero and web an enemy (maximum 3 web counters per
#   enemy).

def GetAbilities() -> Sequence['Ability']:

    def thwip(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)

        initiator = effect.GetInitiator()
        Faces.ReadyAll([initiator.GetIdentity()], effect)
        Weber(effect.targets, 1, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            thwip
        ).SetPlay(hero_form_only=True)
        .SetTarget(Enemy),
    ]
