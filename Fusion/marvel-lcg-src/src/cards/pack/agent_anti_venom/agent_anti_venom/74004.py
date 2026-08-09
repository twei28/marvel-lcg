from . import *

# Extricate — custom « DesignHacker »
# Hero Action (thwart): Remove 4 threat from a scheme. If Agent Anti-Venom has
#   exactly 10 hit points remaining, draw 1 card or confuse an enemy.

def GetAbilities() -> Sequence['Ability']:

    def extricate(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)

        intact = HasExactlyTen(effect)
        this.RemoveThreatFromSchemes(effect.targets, 4, effect)

        if not intact:
            return

        initiator = effect.GetInitiator()
        initiator.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Draw 1 card",
                lambda targets:
                    initiator.DrawUp(1, effect)
            ).SetHasNoTargetEffect(),
            AbilityFactory.ForChoiceAbility(
                "Confuse an enemy",
                lambda targets:
                    Faces.GiveStatus(targets, "Confused", effect)
            ).SetTarget(Enemy),
        )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            extricate,
        ).SetPlay()
        .SetLabel('thwart')
        .SetTarget(Scheme2),
    ]
