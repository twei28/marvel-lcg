from . import *

# Alone
#
# Modele Business Problems (core/iron_man/01170.py, l'obligation OFFICIELLE de
# Tony Stark : premiere branche identique mot pour mot). Seconde branche
# "Spend 3 resources of any type. If you cannot, this card gains surge." :
# `player.AskSpendResourcesInternal(Cost("3"), effect)` rend None si le
# paiement echoue/est refuse (player_action.py:946) ; `ThisCardGainSurge`
# modele Soldiers of Fortune (aos/50102.py).

def GetAbilities() -> Sequence['Ability']:

    def alone(effect: 'Effect', message: 'Message.WhenObligationGiveToPlayer') -> None:
        this = effect.this.CastTo(Obligation)
        player = message.GetGaveToPlayer()

        def spend_or_surge(targets: Sequence['CardFace']) -> None:
            res = player.AskSpendResourcesInternal(Cost("3"), effect)
            if res is None:
                ThisCardGainSurge(effect)
            Faces.DiscardAll([this], effect)

        YouMayFlipToYourAlterEgoForm(player, effect)

        player.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Exhaust Tony Stark → remove Alone from the game",
                lambda targets:
                    Faces.RemoveAllFromGame([this], effect),
                condition=player.IsAlterEgo(),
            ).SetCostFunc(CostFunc.Exhaust("YourIdentity")),
            AbilityFactory.ForChoiceAbility(
                "Spend 3 resources of any type. If you cannot, this card gains surge. Discard this obligation",
                spend_or_surge,
            ),
        )

    return [
        AbilityFactory.WhenThisObligationGiveToYou(
            alone
        )
    ]
