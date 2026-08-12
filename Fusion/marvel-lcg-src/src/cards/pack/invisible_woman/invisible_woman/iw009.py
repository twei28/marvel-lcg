from . import *


def GetAbilities() -> Sequence['Ability']:

    def infiltrate(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        effect.GetInitiator().ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Remove up to 4 threat from a scheme",
                lambda targets: this.RemoveThreatFromSchemes(targets, 4, effect),
            ).SetTarget(Scheme2),
            AbilityFactory.ForChoiceAbility(
                "Remove up to 2 threat from each scheme",
                lambda targets: this.RemoveThreatFromSchemes(targets, 2, effect),
            ).SetTarget(Scheme2, range=(1, "All")),
        )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            infiltrate,
        ).SetPlay(only_if_your_identity_has_trait="INVISIBLE")
        .SetLabel("thwart")
        .SetName("Infiltrate"),
    ]
