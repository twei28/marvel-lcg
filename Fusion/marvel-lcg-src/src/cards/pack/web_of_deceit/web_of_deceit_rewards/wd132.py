from . import *

# Spider-Tingle

def GetAbilities() -> Sequence['Ability']:

    def picotement(effect: 'Effect', message: 'Message.WhenPlayerRevealCard') -> None:
        # « Interrupt: When you reveal a treachery, discard Spider-Tingle →
        # cancel the “When Revealed” effects of that treachery. »
        this = effect.this.CastTo(Upgrade)
        Faces.DiscardAll([this], effect)
        message.CancelWhenRevealedEffect(effect)

    return [
        AbilityFactory.WhenPlayerRevealCard(
            AbilityType.Interrupt,
            "You",
            Treachery,
            "WhenRevealed",
            picotement,
            from_encounter=True,
        ),
    ]
