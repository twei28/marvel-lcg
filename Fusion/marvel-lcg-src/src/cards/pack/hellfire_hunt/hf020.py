from . import *

# * Oya (Idie Okonkwo) : allie RECRUITED, cout 4, PV 2, THW 1*, ATK 2*.
# Response: After Oya enters play, choose one: deal 4 damage to an enemy, or stun an enemy.
#
# Carte de reference : 01084 Nick Fury (`initiator.ChooseAbilities(effect, AbilityFactory.ForChoiceAbility(...).SetTarget(...))`).
def GetAbilities() -> Sequence['Ability']:
    def oya(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        this = effect.this.CastTo(Ally)
        initiator = effect.GetInitiator()

        def quatre_degats(targets: Sequence['CardFace']) -> None:
            this.DealDamage(targets, 4, effect)

        def etourdir(targets: Sequence['CardFace']) -> None:
            Faces.GiveStatus(targets, "Stunned", effect)

        initiator.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Deal 4 damage to an enemy",
                quatre_degats,
            ).SetTarget(Enemy),
            AbilityFactory.ForChoiceAbility(
                "Stun an enemy",
                etourdir,
            ).SetTarget(Enemy, canbe_stunned=True),
        )

    return [
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.Response,
            "This",
            oya,
        ),
    ]
