from . import *

# True Grit — custom « DesignHacker »
# Hero Action: Deal 2 damage to The Thing -> ready your hero and discard a
# status card from him. (Max once per round.)

def GetAbilities() -> Sequence['Ability']:

    def true_grit(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)

        initiator = effect.GetInitiator()
        hero = initiator.GetHero()
        if hero is None:
            return

        this.DealDamage([hero], 2, effect)
        if not hero.IsInPlay():
            return

        Faces.ReadyAll([hero], effect)

        initiator.MayChooseOneAbility(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Discard a tough status card",
                lambda targets: hero.DiscardTough(effect, rule=1),
                condition=hero.IsTough(),
            ),
            # CORRECTIF 4/8/2026 : `Faces.DiscardStatus` n'existe pas, les deux
            # options plantaient des que le joueur les choisissait. Ce sont des
            # methodes de la FACE, comme le DiscardTough juste au-dessus
            # (modele Uncanny Resilience 07045).
            AbilityFactory.ForChoiceAbility(
                "Discard a stunned status card",
                lambda targets: hero.DiscardStunned(effect, rule=1),
                condition=hero.HasStatus("Stunned"),
            ),
            AbilityFactory.ForChoiceAbility(
                "Discard a confused status card",
                lambda targets: hero.DiscardConfused(effect, rule=1),
                condition=hero.HasStatus("Confused"),
            ),
        )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            true_grit
        ).LimitOncePerRound(),
    ]
