from . import *

# Counterpart Elimination — custom « Kajislav » (obligation d'Albert)
# Give to the Albert player.
# You cannot resolve Albert's "Initiate Protocol" ability.
#   (vérifié dans le gestionnaire Special du héros, ab001a)
# When Revealed: Find a WOLVERINE minion and reveal it.
# Response: After a WOLVERINE minion is defeated, discard this card.

def GetAbilities() -> Sequence['Ability']:

    def counterpart_elimination(effect: 'Effect', message: 'Message.WhenObligationGiveToPlayer') -> None:
        this = effect.this.CastTo(Obligation)
        Unused(this)

        player = message.GetGaveToPlayer()

        Find.FindAndReveal(
            effect,
            player,
            trait="WOLVERINE",
            card_type=Minion,
        )

    def wolverine_defeated(effect: 'Effect', message: 'Message.AfterUnitBeDefeated') -> None:
        this = effect.this.CastTo(Obligation)
        Faces.DiscardAll([this], effect)

    return [
        AbilityFactory.WhenThisObligationGiveToYou(
            counterpart_elimination
        ),
        AbilityFactory.AfterUnitBeDefeated(
            AbilityType.Response,
            CardFinder(trait="WOLVERINE", card_type=Minion),
            wolverine_defeated,
        ),
    ]
