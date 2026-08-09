from . import *

# Self-Sacrifice — custom « Rainy »
# Hero Action (thwart): Remove 3 threat from a scheme. You may take 2 damage
#   to remove 3 additional threat from that scheme.

def GetAbilities() -> Sequence['Ability']:

    def self_sacrifice(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)

        cibles = list(effect.targets)
        this.RemoveThreatFromSchemes(cibles, 3, effect)

        initiator = effect.GetInitiator()

        def encore(targets: Sequence['CardFace']) -> None:
            identity = initiator.GetIdentity()
            identity.TakeDamage(this, 2, effect)
            this.RemoveThreatFromSchemes(cibles, 3, effect)

        initiator.MayChooseOneAbility(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Take 2 damage to remove 3 additional threat",
                encore,
            ),
        )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            self_sacrifice
        ).SetPlay(hero_form_only=True)
        .SetLabel('thwart')
        .SetTarget(Scheme2),
    ]
