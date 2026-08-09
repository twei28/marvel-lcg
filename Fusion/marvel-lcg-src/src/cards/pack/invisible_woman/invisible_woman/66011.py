from . import *


def GetAbilities() -> Sequence['Ability']:

    def psionic_fields(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        player = effect.GetInitiator()
        for _ in range(2):
            player.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility(
                    "Deal 4 damage to an enemy",
                    lambda targets: this.DealDamage(targets, 4, effect),
                ).SetTarget(Enemy),
                AbilityFactory.ForChoiceAbility(
                    "Stun an enemy",
                    lambda targets: Faces.GiveStatus(targets, "Stunned", effect),
                ).SetTarget(Enemy, canbe_status="Stunned"),
            )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            psionic_fields,
        ).SetPlay(only_if_your_identity_has_trait="PSIONIC")
        .SetLabel("attack")
        .SetName("Psionic Fields"),
    ]
