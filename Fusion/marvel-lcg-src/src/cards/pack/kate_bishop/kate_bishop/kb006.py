from . import *

# Smoke Arrow — ARROW
# Hero Interrupt: When an enemy initiates an activation, remove 1 arrow
#   counter from Kate's Bow -> cancel that activation. You may spend a
#   resource to flip to alter-ego form or ready your hero.
#
# Modele du « cancel that activation » : Web Binding (sm/ghost_spider/27006.py),
# `AbilityFactory.WhenEnemyWouldActivate(..., None, ...)` + `message.SetBeInstead`.
# Le cout (retirer 1 compteur) gate l'ability entiere : `CostFunc.Counter`
# fixe a 1 (pas variable ici, contrairement a Master Archer). Le choix
# optionnel final (« may spend a resource to... ») : `player.MayChooseOneAbility`
# avec 2 options, modele Parting Shots (agent_13/ag005.py) pour le choix
# optionnel a bascule de forme.
#
# CORRECTIF (test de comportement) : `ForChoiceAbility(...).SetCost(Cost("1"))`
# levait `AssertionError: Call ForChoiceAbilityWithCost instead` a chaque
# resolution (ability.py:322, `SetCost` interdit un cout sur une
# ForChoiceAbility). L'exception, avalee par le moteur au niveau de
# `EffectInvoker.InvokeOperation`, rendait tout le choix optionnel muet : ni
# exception visible en partie normale, ni bascule, ni redressement, jamais un
# seul ask pose au joueur. Modele corrige : `ForChoiceAbilityWithCost` (voir
# aos/batrocs_brigade/50102.py), qui prend le cout en premier argument et
# transmet les ressources payees en second parametre de l'operation.


def GetAbilities() -> Sequence['Ability']:

    def smoke_arrow(effect: 'Effect', message: 'Message.WhenEnemyWouldActivate') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)

        message.SetBeInstead(effect)

        initiator = effect.GetInitiator()
        if initiator is None:
            return

        def basculer(targets: Sequence['CardFace'], res: 'Resources') -> None:
            Unused(targets, res)
            initiator.GetIdentity().ChangeToForm(AlterEgo, effect)

        def redresser(targets: Sequence['CardFace'], res: 'Resources') -> None:
            Unused(res)
            Faces.ReadyAll(targets, effect)

        initiator.MayChooseOneAbility(
            effect,
            AbilityFactory.ForChoiceAbilityWithCost(
                Cost("1"),
                "Flip to alter-ego form",
                basculer,
            ),
            AbilityFactory.ForChoiceAbilityWithCost(
                Cost("1"),
                "Ready your hero",
                redresser,
            ).SetTarget("YourHero"),
        )

    return [
        AbilityFactory.WhenEnemyWouldActivate(
            AbilityType.HeroInterrupt,
            None,
            smoke_arrow,
        ).SetPlay()
        .SetCostFunc(CostFunc.Counter(CardFinder(name=NOM_ARC), 1, 'arrow')),
    ]
