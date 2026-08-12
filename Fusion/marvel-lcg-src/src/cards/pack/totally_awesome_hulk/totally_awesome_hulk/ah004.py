from . import *

# * Kegger — custom « DesignHacker »
# Resource: Shuffle Kegger into your deck → generate a [wild] resource.
# Action: Shuffle Kegger and a card from your hand into your deck →
#   ready your identity.


def GetAbilities() -> Sequence['Ability']:

    def shuffle_this(targets: Sequence['CardFace'], effect: 'Effect') -> bool:
        this = effect.this
        initiator = effect.GetInitiator()
        return Faces.ShuffleAllTo([this], initiator.player_deck, effect) == [this]

    def shuffle_this_and_target(targets: Sequence['CardFace'], effect: 'Effect') -> bool:
        this = effect.this
        initiator = effect.GetInitiator()
        faces = [this, *targets]
        return Faces.ShuffleAllTo(faces, initiator.player_deck, effect) == faces

    def kegger(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        initiator = effect.GetInitiator()
        identity = initiator.GetIdentity()

        Faces.ReadyAll([identity], effect)

    return [
        AbilityFactory.CanGenerateResources(
            AbilityType.Resource,
            Resources("G"),
        ).SetCostFunc(CostFunc.Custom(None, shuffle_this)),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            kegger,
        ).SetCostFunc(CostFunc.Custom(
            Select.From(
                CardFinder(),
                from_where=["YourHandCards"],
            ),
            shuffle_this_and_target,
        )),
    ]
