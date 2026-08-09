from . import *

# Pure Lightforce — custom « DesignHacker »
# Hero Response: After you spend this card on a LIGHTFORCE card, deal 1 damage
#   to the villain for each resource you overpaid for that card's cost.
#
# Même montage que The Power of Forgiveness (68007) : la ressource est
# défaussée au moment du paiement, l'effet différé est donc porté par
# l'IDENTITÉ et le surpaiement se lit à la résolution de la carte payée
# (paid_this_resources vs this_effect_need_cost, cf. WhenCardEnterPlay).


def GetAbilities() -> Sequence['Ability']:

    def pure_lightforce(effect: 'Effect', message: 'Message.WhenCardBeSpendAsResource') -> None:
        initiator = effect.GetInitiator()
        identity = initiator.GetIdentity()
        for_effect = message.for_effect

        def apres_resolution(effect2: 'Effect', message2: 'Message.AfterEffectResolved') -> None:
            paye = for_effect.context.paid_this_resources
            requis = for_effect.context.this_effect_need_cost
            if paye is None:
                return
            surpaye = paye.val - (requis.val if requis is not None else 0)
            if surpaye <= 0:
                return
            vilain = Worlds.FindCardOnField(effect2, card_type=Villain)
            if vilain:
                effect2.this.DealDamage([vilain], surpaye, effect2)

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
            pure_lightforce,
            to_pay_card=CardFinder(traits=["LIGHTFORCE"]),
        ),
    ]
