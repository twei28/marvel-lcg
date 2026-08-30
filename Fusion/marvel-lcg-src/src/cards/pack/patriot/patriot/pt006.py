from . import *

# Covered Fire (2/2) — exemplaire physique 2/2, contenu identique a pt005
# (voir ce fichier pour le detail des modeles et des arbitrages, notamment la
# difference avec pt003 : l'allie est CHOISI, pas epuise).


def GetAbilities() -> Sequence['Ability']:

    def covered_fire(effect: 'Effect', message: 'Message.WhenUnitWouldDefend') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        initiator = effect.GetInitiator()
        if initiator is None or not effect.targets:
            return

        allie = effect.targets[0].CastTo(Ally)
        atk = allie.attack
        thw = allie.thwart

        initiator.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                f"Deal {atk} damage to an enemy (that ally's ATK)",
                lambda targets:
                    this.DealDamage(list(targets), atk, effect),
            ).SetTarget(Enemy, range=(1, 1)),
            AbilityFactory.ForChoiceAbility(
                f"Remove {thw} threat from a scheme (that ally's THW)",
                lambda targets:
                    this.RemoveThreatFromSchemes(list(targets), thw, effect),
            ).SetTarget(Scheme2, range=(1, 1)),
        )

    return [
        AbilityFactory.WhenUnitDefendAgainstAttack(
            AbilityType.HeroInterrupt,
            "YourHero",
            covered_fire,
        ).SetPlay()
        .SetLabel('defense')
        .SetTarget("YourAlly", range=(1, 1)),
    ]
