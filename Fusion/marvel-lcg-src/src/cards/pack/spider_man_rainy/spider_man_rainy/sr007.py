from . import *

# Great Power — custom « Rainy » (ressource signature)
# Hero Response (attack): After you spend this card, deal 2 damage to an
#   enemy.
# Meme montage differe que The Power of Forgiveness (ah007) : l'effet est
# porte par l'identite, la ressource etant defaussee au moment du paiement.

def GetAbilities() -> Sequence['Ability']:

    def great_power(effect: 'Effect', message: 'Message.WhenCardBeSpendAsResource') -> None:
        initiator = effect.GetInitiator()
        identity = initiator.GetIdentity()

        def apres_resolution(effect2: 'Effect', message2: 'Message.AfterEffectResolved') -> None:
            joueur = effect2.GetInitiator()
            ennemis = list(Worlds.FindCardsOnField(effect2, card_type=Enemy))
            if not ennemis:
                return
            joueur.ChooseAbilities(
                effect2,
                AbilityFactory.ForChoiceAbility(
                    "Deal 2 damage to an enemy",
                    lambda targets: effect2.this.DealDamage(list(targets), 2, effect2),
                ).SetTarget(Select.From(faces=ennemis), range=(1, 1)),
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
            great_power,
        ),
    ]
