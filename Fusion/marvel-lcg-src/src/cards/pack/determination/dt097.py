from . import *

# Timeslide

def GetAbilities() -> Sequence['Ability']:

    def timeslide(effect: 'Effect', message: 'Message.AfterUnitBeDefeated') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)

        initiator = effect.GetInitiator()
        vaincue = message.trigger

        def au_tableau_des_victoires(targets: Sequence['CardFace']) -> None:
            Faces.MoveAllTo([vaincue], Worlds.VictoryDisplay(effect), effect)
            initiator.DrawUp(1, effect)

        initiator.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Place it in the victory display and draw 1 card",
                au_tableau_des_victoires
            ).SetHasNoTargetEffect(),
        )

    def check_a_vous(effect: 'Effect', message: 'Message.AfterUnitBeDefeated') -> bool:
        initiator = effect.GetInitiator()
        return initiator is not None \
            and message.trigger.GetControlByPlayer() == initiator

    return [
        AbilityFactory.AfterUnitBeDefeated(
            AbilityType.HeroResponse,
            None,
            timeslide,
            conditions=[check_a_vous],
        ).SetPlay(),
    ]
