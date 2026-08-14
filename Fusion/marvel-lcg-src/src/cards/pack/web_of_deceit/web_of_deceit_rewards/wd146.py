from . import *

# Not My Problem

def GetAbilities() -> Sequence['Ability']:

    def ignorer(effect: 'Effect', message: 'Message.WhenPlayerRevealCard') -> None:
        # « Hero Interrupt: When a treachery card would be revealed, cancel its
        # “When Revealed” ability. Then, place 2 threat on a scheme. »
        this = effect.this.CastTo(Event)
        message.CancelWhenRevealedEffect(effect)
        this.PlaceThreatOnSchemes(effect.targets, 2, effect)

    return [
        AbilityFactory.WhenPlayerRevealCard(
            AbilityType.HeroInterrupt,
            "AnyPlayer",
            Treachery,
            "WhenRevealed",
            ignorer,
            from_encounter=True,
        ).SetPlay().SetTarget(Scheme2),
    ]
