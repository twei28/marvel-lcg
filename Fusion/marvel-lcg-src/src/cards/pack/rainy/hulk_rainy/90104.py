from . import *

# Brilliant Mind

def GetAbilities() -> Sequence['Ability']:

    def brilliant_mind(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)

        this.RemoveThreatFromSchemes(effect.targets, 3, effect)

        if not effect.GetPaidResources().OnlyHasColor("B"):
            return

        # Paye uniquement en [mental] : 2 menaces de plus, ou confusion.
        initiator = effect.GetInitiator()

        def menace_en_plus(targets: Sequence['CardFace']) -> None:
            this.RemoveThreatFromSchemes(effect.targets, 2, effect)

        def confusion(targets: Sequence['CardFace']) -> None:
            Faces.GiveStatus(list(targets), "Confused", effect)

        initiator.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Remove 2 additional threat from that scheme", menace_en_plus),
            AbilityFactory.ForChoiceAbility(
                "Confuse an enemy", confusion).SetTarget(Enemy),
        )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            brilliant_mind
        ).SetPlay().SetLabel('thwart')
        .SetTarget(Scheme2),
    ]
