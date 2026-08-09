from . import *

# * New Attilan — custom « Nugget »
# Alter-Ego Action: Exhaust New Attilan → discard cards from the top of your
#   deck until you discard a Lockjaw card. Then, add that card to your hand.
#
# « une carte Lockjaw » = une carte du set signature du héros, que le moteur
# désigne par `card_class="IdentitySpecific"` (même filtre que « hero-specific
# card » d'Amadeus Cho 68001b).


def GetAbilities() -> Sequence['Ability']:

    def fouiller(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        Unused(this)
        initiator = effect.GetInitiator()

        face = initiator.DiscardDeckUntil(
            effect,
            card_class="IdentitySpecific",
        )
        if face:
            initiator.GainCard(face, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            fouiller,
        ).SetName("New Attilan")
        .SetCostFunc(CostFunc.Exhaust("This")),
    ]
