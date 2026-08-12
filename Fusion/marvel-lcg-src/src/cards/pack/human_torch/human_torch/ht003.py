from . import *

# Johnny's Workshop — custom « DesignHacker »
# Response: After you change to Johnny Storm, draw 1 card.
# Response: After you change to Human Torch, ready a FIRE card.

def GetAbilities() -> Sequence['Ability']:

    def vers_alter_ego(effect: 'Effect', message: 'Message.AfterUnitChangeForm') -> None:
        this = effect.this.CastTo(Support)
        Unused(this)

        initiator = effect.GetInitiator()
        initiator.DrawUp(1, effect)

    def vers_heros(effect: 'Effect', message: 'Message.AfterUnitChangeForm') -> None:
        this = effect.this.CastTo(Support)
        Unused(this)

        Faces.ReadyAll(effect.targets, effect)

    return [
        AbilityFactory.AfterUnitChangeForm(
            AbilityType.Response,
            "You",
            vers_alter_ego,
            to_form=AlterEgo,
        ),
        AbilityFactory.AfterUnitChangeForm(
            AbilityType.Response,
            "You",
            vers_heros,
            to_form=Hero,
        ).SetTarget(trait="FIRE", canbe_ready=True, from_where=["YouControlCards"]),
    ]
