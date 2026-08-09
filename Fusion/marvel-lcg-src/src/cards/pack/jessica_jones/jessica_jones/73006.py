from . import *

# Out in the Open — custom « ekAugust »
# Interrupt: When a treachery card is revealed from the encounter deck, cancel
#   its "When Revealed" effects. Discard cards from the top of the encounter
#   deck until you discard a side scheme. Reveal that side scheme.

def GetAbilities() -> Sequence['Ability']:

    def out_in_the_open(effect: 'Effect', message: 'Message.WhenPlayerRevealCard') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)

        message.CancelWhenRevealedEffect(effect)

        player = message.GetToPlayer()
        face = Worlds.DiscardEncounterCardsUntil(
            effect,
            card_type=SchemeSide2,
        )
        if face:
            face.Reveal(player, effect)

    return [
        AbilityFactory.WhenPlayerRevealCard(
            AbilityType.Interrupt,
            "AnyPlayer",
            Treachery,
            "WhenRevealed",
            out_in_the_open,
            from_encounter=True,
        ).SetPlay(),
    ]
