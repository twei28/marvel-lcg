from . import *

# Great Responsibility — custom « Rainy » (ressource signature)
# Hero Response (thwart): After you spend this card, remove 2 threat from a
#   scheme. Montage identique a Great Power (71007).

def GetAbilities() -> Sequence['Ability']:

    def great_responsibility(effect: 'Effect', message: 'Message.WhenCardBeSpendAsResource') -> None:
        initiator = effect.GetInitiator()
        identity = initiator.GetIdentity()

        def apres_resolution(effect2: 'Effect', message2: 'Message.AfterEffectResolved') -> None:
            joueur = effect2.GetInitiator()

            def retirer(targets: Sequence['CardFace']) -> None:
                effect2.this.RemoveThreatFromSchemes(list(targets), 2, effect2)

            joueur.ChooseAbilities(
                effect2,
                AbilityFactory.ForChoiceAbility(
                    "Remove 2 threat from a scheme",
                    retirer,
                ).SetTarget(Scheme2, range=(1, 1)),
            )

        identity.effect.RegisterTemp(
            AbilityFactory.AfterCardResolveAbility(
                AbilityType.Response,
                None,
                CardFace,
                apres_resolution,
                which_effect=message.for_effect,
            ),
            unregister_after_exec=True,
            until_resolve_effect=message.for_effect,
        )

    return [
        AbilityFactory.WhenYouSpendThisCardToPlay(
            AbilityType.HeroResponse,
            great_responsibility,
        ),
    ]
