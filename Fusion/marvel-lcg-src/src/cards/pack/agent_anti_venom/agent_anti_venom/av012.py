from . import *

# Spread Too Thin — custom « DesignHacker » (obligation)
# Give to the Flash Thompson player.
# You may flip to alter-ego form. Choose:
# - Deal 3 damage to your identity -> remove Spread Too Thin from the game.
# - Remove an upgrade you control from the game. Discard this obligation.

def GetAbilities() -> Sequence['Ability']:

    def spread_too_thin(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Obligation)

        player = message.GetGaveToPlayer()
        identity = player.GetIdentity()

        if player.IsHero():
            player.MayChooseOneAbility(
                effect,
                AbilityFactory.ForChoiceAbility(
                    "Flip to alter-ego form",
                    lambda targets:
                        identity.ChangeToForm(AlterEgo, effect),
                ).SetHasNoTargetEffect(),
            )

        def encaisser(targets: Sequence['CardFace']) -> None:
            Unused(targets)
            courante = player.GetIdentity()
            courante.TakeDamage(this, 3, effect)
            Faces.RemoveAllFromGame([this], effect)

        def sacrifier_amelioration(targets: Sequence['CardFace']) -> None:
            Faces.RemoveAllFromGame(list(targets), effect)
            Faces.DiscardAll([this], effect)

        player.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Deal 3 damage to your identity -> remove Spread Too Thin from the game",
                encaisser,
            ).SetHasNoTargetEffect(),
            AbilityFactory.ForChoiceAbility(
                "Remove an upgrade you control from the game",
                sacrifier_amelioration,
            ).SetTarget(Upgrade, from_where=["InPlay"]),
        )

    return [
        AbilityFactory.WhenThisObligationRevealed(
            spread_too_thin
        ),
    ]
