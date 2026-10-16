from . import *

# Fallen Empires

def GetAbilities() -> Sequence['Ability']:

    def revelee(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        lieux = LieuxAmis(effect)

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Discard a friendly LOCATION",
                lambda targets: Faces.DiscardAll(list(targets), effect),
                condition=bool(lieux)).SetTarget(Support, trait="LOCATION"),
            AbilityFactory.ForChoiceAbility(
                "Discard 1 card from your hand",
                lambda targets: joueur.DiscardHandCards((1, 1), effect),
                condition=joueur.hand_cards.GetSize() > 0),
        )

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        message.GetToPlayer().DiscardHandCards((1, 1), effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revelee),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
