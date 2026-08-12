from . import *

# Raw Darkforce — custom « DesignHacker »
# Hero Response: After you spend this card on a DARKFORCE card, remove 1
#   threat from the main scheme for each resource you overpaid for that card's
#   cost.
# Montage identique à Pure Lightforce (cd006), cf. ah007.


def GetAbilities() -> Sequence['Ability']:

    def raw_darkforce(effect: 'Effect', message: 'Message.WhenCardBeSpendAsResource') -> None:
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
            scheme = Worlds.FindMainScheme(effect2.this)
            if scheme:
                effect2.this.RemoveThreatFromSchemes([scheme], surpaye, effect2)

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
            raw_darkforce,
            to_pay_card=CardFinder(traits=["DARKFORCE"]),
        ),
    ]
