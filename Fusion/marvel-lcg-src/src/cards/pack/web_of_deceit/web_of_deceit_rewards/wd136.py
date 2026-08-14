from . import *

# Team Spider-Sense

def GetAbilities() -> Sequence['Ability']:

    def equipe(effect: 'Effect', message: 'Message.WhenPlayerRevealCard') -> None:
        # « Alliance. Interrupt: When a treachery card is revealed from the
        # encounter deck, cancel its “When Revealed” effects. Each player draws
        # 1 card. »
        message.CancelWhenRevealedEffect(effect)
        Players.ForEachPlayer(effect, lambda joueur: joueur.DrawUp(1, effect))

    return [
        AbilityFactory.WhenPlayerRevealCard(
            AbilityType.Interrupt,
            "AnyPlayer",
            Treachery,
            "WhenRevealed",
            equipe,
            from_encounter=True,
        ).SetPlay(),
    ]
