from . import *

# Anti-Venom Goo — custom « DesignHacker »
# Hero Interrupt: When you spend this card to play an event, reduce the cost to
#   play that event by 1. Then, heal 1 damage from a friendly character for
#   each resource you overpaid for that event's cost with this card.
#
# La « reduction de cout » est rendue par une GENERATION SUPPLEMENTAIRE, montage
# d'Energy Siphon (58006) : au moment de payer un evenement, la carte rend 3
# [energy] au lieu des 2 imprimees. Vis-a-vis du cout a couvrir et du
# surpaiement, « -1 au cout » et « +1 ressource » sont equivalents, et cette
# voie-la fonctionne.
#
# Pourquoi pas la voie directe : le moteur fige le cout AVANT de demander les
# ressources, donc un `ReduceCostToPlayFaceWhen` pose depuis
# `WhenCardBeSpendAsResource` arrive trop tard (verifie en test le 4/8/2026,
# l'evenement a 1 ne comptait qu'1 de surpaiement au lieu de 2).
#
# Le soin, lui, est un effet differe porte par l'IDENTITE : la ressource est
# defaussee au moment du paiement, on lit donc le surpaiement a la resolution
# de l'evenement paye (montage Pure Lightforce cd006).

BONUS_POUR_EVENEMENT = 1


def GetAbilities() -> Sequence['Ability']:

    def _paye_un_evenement(message: Any) -> bool:
        for_effect = getattr(message, "for_effect", None)
        return for_effect is not None and Event.IsType(for_effect.this)

    def goo_res(effect: 'Effect', message: 'Message.WhenPlayerPayingResources') -> 'Resources':
        this = effect.this.CastTo(Resource)
        Unused(this)

        if _paye_un_evenement(message):
            return Resources('Y' * (2 + BONUS_POUR_EVENEMENT))
        return Resources('YY')

    def goo_check(effect: 'Effect', message: 'Message.CheckPlayerCanPayCost') -> 'Resources':
        this = effect.this.CastTo(Resource)
        Unused(this)

        # Pour le controle « peux-tu payer ? », on annonce le maximum.
        return Resources('Y' * (2 + BONUS_POUR_EVENEMENT))

    def anti_venom_goo(effect: 'Effect', message: 'Message.WhenCardBeSpendAsResource') -> None:
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
            initiator.ChooseAbilities(
                effect2,
                AbilityFactory.ForChoiceAbility(
                    "Heal damage from a friendly character",
                    lambda targets:
                        effect2.this.HealthUnits(targets, surpaye, effect2)
                # « friendly character » : Friend, PAS Unit2. Avec Unit2 le soin
                # partait sur Rhino (constate en test le 4/8/2026). Meme
                # ciblage que Med Team 01080.
                ).SetTarget(Friend, canbe_heal=True)
            )

        identity.effect.RegisterTemp(
            AbilityFactory.AfterCardResolveAbility(
                AbilityType.Response,
                None,
                CardFace,
                apres_resolution,
                which_effect=for_effect,
            ),
            unregister_after_exec=True,
            until_resolve_effect=for_effect,
        )

    return [
        AbilityFactory.DoDiscardThisToGenerateResources(
            # CORRECTIF (4/8/2026) : le moteur n'autorise les func_names
            # DoGenerateResources/DiscardPay qu'en `Interrupt` (voir
            # `check_sub_type` dans game/ability/ability.py). En
            # `HeroInterrupt` la partie PLANTE des que la carte sert.
            AbilityType.Interrupt,
            res_fn=goo_res,
        ),
        AbilityFactory.CheckThisCanDropPay(goo_check),

        AbilityFactory.WhenYouSpendThisCardToPlay(
            AbilityType.HeroInterrupt,
            anti_venom_goo,
            to_pay_card=CardFinder(card_type=Event),
        ),
    ]
