from . import *


def GetAbilities() -> Sequence['Ability']:

    def family_time(effect: 'Effect', message: 'Message.WhenObligationGiveToPlayer') -> None:
        this = effect.this.CastTo(Obligation)
        player = message.GetGaveToPlayer()

        # CORRECTIF : « You MAY flip to alter-ego form » figure sur la carte et
        # etait absent du script.
        identity = player.GetIdentity()
        if Hero.IsType(identity):
            player.MayChooseOneAbility(
                effect,
                AbilityFactory.ForChoiceAbility(
                    "Flip to alter-ego form",
                    lambda targets: identity.ChangeToOtherIdentityForm(effect),
                ),
            )

        player.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                # CORRECTIF : le scan dit « remove Family Time FROM THE GAME »,
                # comme les cinq obligations du set de base. Le script la
                # defaussait, donc elle revenait dans le deck Rencontre.
                "Exhaust Sue Storm and remove this obligation from the game",
                lambda targets: Faces.RemoveAllFromGame([this], effect),
                targets_is_exhaust_cost=True,
            ).SetCostFunc(CostFunc.Exhaust("YourIdentity")),
            AbilityFactory.ForChoiceAbility(
                "Discard 1 card from your hand and discard this obligation",
                lambda targets: (Faces.DiscardAll(targets, effect), Faces.DiscardAll([this], effect)),
            ).SetTarget("YourHandCards", range=(1, 1), canbe_discard=True),
        )

    return [
        AbilityFactory.WhenThisObligationGiveToYou(family_time),
    ]
