from . import *

# Where'd He Go? — custom « DesignHacker »
# Choose one:
# - Action: Change to hero form -> confuse an enemy.
# - Action: Change to alter-ego form -> stun an enemy.


def GetAbilities() -> Sequence['Ability']:

    def vers_heros(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)
        initiator = effect.GetInitiator()
        ChoisirEtChangerDeForme(initiator, effect, vers_heros=True)
        Faces.GiveStatus(effect.targets, "Confused", effect)

    def vers_alter_ego(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)
        initiator = effect.GetInitiator()
        ChoisirEtChangerDeForme(initiator, effect, vers_heros=False)
        Faces.GiveStatus(effect.targets, "Stunned", effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            vers_heros,
            conditions=[
                lambda effect, message: effect.GetInitiator().IsAlterEgo(),
            ],
        ).SetPlay()
        .SetTarget(Enemy, canbe_confused=True),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            vers_alter_ego,
            conditions=[
                lambda effect, message: effect.GetInitiator().IsHero(),
            ],
        ).SetPlay()
        .SetTarget(Enemy, canbe_stunned=True),
    ]
