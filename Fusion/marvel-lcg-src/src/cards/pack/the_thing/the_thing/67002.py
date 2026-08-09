from . import *

# * Human Torch (Johnny Storm) — custom « DesignHacker »
# Response: After Human Torch enters play, choose one:
# - Deal 1 damage to The Thing, then give The Thing a tough status card.
# - Deal 3 damage to the villain.

def GetAbilities() -> Sequence['Ability']:

    def human_torch(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        this = effect.this.CastTo(Ally)

        initiator = effect.GetInitiator()
        hero = initiator.GetHero()
        villain = Worlds.FindVillain(effect)

        def renforcer(targets: Sequence['CardFace']) -> None:
            this.DealDamage([hero], 1, effect)
            if hero.IsInPlay():
                Faces.GiveStatus([hero], "Tough", effect)

        def frapper(targets: Sequence['CardFace']) -> None:
            if villain:
                this.DealDamage([villain], 3, effect)

        initiator.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Deal 1 damage to The Thing, then give The Thing a tough status card",
                renforcer,
                condition=hero is not None,
            ),
            AbilityFactory.ForChoiceAbility(
                "Deal 3 damage to the villain",
                frapper,
                condition=villain is not None,
            ),
        )

    return [
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.Response,
            "This",
            human_torch,
        ),
    ]
