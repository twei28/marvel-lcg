from . import *

# Responsive

def GetAbilities() -> Sequence['Ability']:

    def responsive(effect: 'Effect', message: 'Message.AfterUnitUseBasicPower') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)

        initiator = effect.GetInitiator()
        hero = initiator.GetHero()

        Faces.ReadyAll([hero], effect)

        def bonus(**kwargs) -> None:
            hero.GainUntilRoundEnd(effect, **kwargs)

        initiator.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility("+1 THW", lambda targets: bonus(thwart=1)),
            AbilityFactory.ForChoiceAbility("+1 ATK", lambda targets: bonus(attack=1)),
            AbilityFactory.ForChoiceAbility("+1 DEF", lambda targets: bonus(defense=1)),
        )

    return [
        AbilityFactory.AfterUnitUseBasicPower(
            AbilityType.HeroResponse,
            "You",
            responsive,
            powers="Hero"
        ).SetPlay(),
    ]
