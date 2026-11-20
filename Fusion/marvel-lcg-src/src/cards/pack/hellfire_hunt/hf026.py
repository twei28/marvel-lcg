from . import *

# * Charles Xavier : allie RECRUITED, cout 3, PV 2, THW 3*, ATK 0*.
# Response: After Charles Xavier enters play, choose one: draw 2 cards, stun an enemy, or ready your identity.
# At the end of the round, if Charles Xavier is still in play, discard him.
#
# Cartes de reference : 01084 Nick Fury (`ChooseAbilities` + `DiscardThisWhenRoundEnd`), 01083 (statut Stunned).
def GetAbilities() -> Sequence['Ability']:
    def xavier(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        initiator = effect.GetInitiator()

        def piocher(targets: Sequence['CardFace']) -> None:
            initiator.DrawUp(2, effect)

        def etourdir(targets: Sequence['CardFace']) -> None:
            Faces.GiveStatus(targets, "Stunned", effect)

        def redresser(targets: Sequence['CardFace']) -> None:
            Faces.ReadyAll(targets, effect)

        initiator.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility("Draw 2 cards", piocher).SetTarget("YourIdentity"),
            AbilityFactory.ForChoiceAbility("Stun an enemy", etourdir).SetTarget(Enemy, canbe_stunned=True),
            AbilityFactory.ForChoiceAbility("Ready your identity", redresser).SetTarget("YourIdentity", canbe_ready=True),
        )

    return [
        AbilityFactory.DiscardThisWhenRoundEnd(
            AbilityType.ForcedResponse,
        ),
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.Response,
            "This",
            xavier,
        ),
    ]
