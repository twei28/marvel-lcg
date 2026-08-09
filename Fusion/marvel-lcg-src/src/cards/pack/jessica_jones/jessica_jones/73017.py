from . import *

# Stable Home Life — custom « ekAugust » (obligation)
# Give to the Jessica Jones player.
# You may flip to alter-ego form. Choose:
# - Exhaust your alter-ego -> remove Stable Home Life from the game.
# - Discard an On the Job side scheme from play. If you cannot, this card gains
#   surge. Discard this obligation.

ON_THE_JOB_SET = "On the Job"


def GetAbilities() -> Sequence['Ability']:

    def stable_home_life(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Obligation)

        player = message.GetGaveToPlayer()
        identity = player.GetIdentity()

        # « You may flip to alter-ego form. »
        if player.IsHero():
            player.MayChooseOneAbility(
                effect,
                AbilityFactory.ForChoiceAbility(
                    "Flip to alter-ego form",
                    lambda targets:
                        identity.ChangeToForm(AlterEgo, effect),
                ).SetHasNoTargetEffect(),
            )

        def se_reposer(targets: Sequence['CardFace']) -> None:
            Unused(targets)
            alter_ego = player.GetIdentity()
            Faces.ExhaustAll([alter_ego], effect)
            Faces.RemoveAllFromGame([this], effect)

        def classer_une_affaire(targets: Sequence['CardFace']) -> None:
            manigances = [x for x in Worlds.GetSideSchemes(effect)
                          if x.set_name == ON_THE_JOB_SET]
            if manigances:
                Faces.DiscardAll(manigances[:1], effect)
            else:
                this.GainSurge(1, effect)
            Faces.DiscardAll([this], effect)

        choix: List['Ability'] = []
        if not player.IsHero():
            choix.append(
                AbilityFactory.ForChoiceAbility(
                    "Exhaust your alter-ego -> remove Stable Home Life from the game",
                    se_reposer,
                ).SetHasNoTargetEffect()
            )
        choix.append(
            AbilityFactory.ForChoiceAbility(
                "Discard an On the Job side scheme from play",
                classer_une_affaire,
            ).SetHasNoTargetEffect()
        )

        player.ChooseAbilities(effect, *choix)

    return [
        AbilityFactory.WhenThisObligationRevealed(
            stable_home_life
        ),
    ]
