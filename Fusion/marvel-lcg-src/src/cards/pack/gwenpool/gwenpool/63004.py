from . import *

# Fun Background Noise — custom « ekAugust »
# Hero Interrupt: When a treachery card is revealed from the encounter deck,
# cancel its "When Revealed" effects and discard it. Then, ____.
# Bulle : « Give Gwenpool a tough status card. »

def GetAbilities() -> Sequence['Ability']:

    def fun_background_noise(effect: 'Effect', message: 'Message.WhenPlayerRevealCard') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)

        message.CancelWhenRevealedEffect(effect)
        ResolveBlank(effect)

    return [
        AbilityFactory.WhenPlayerRevealCard(
            AbilityType.HeroInterrupt,
            "AnyPlayer",
            Treachery,
            "WhenRevealed",
            fun_background_noise,
            from_encounter=True,
        ).SetPlay()
    ]
