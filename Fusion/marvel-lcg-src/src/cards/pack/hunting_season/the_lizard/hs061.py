from . import *

# Enhanced Lizard Senses

def GetAbilities() -> Sequence['Ability']:

    def annuler(effect: 'Effect', message: 'Message.WhenPlayerWouldPlayCard') -> None:
        message.CancelEffects(effect, discard_it=True)
        AuFondDeLaDefausse(effect, effect.this)

    return [
        AttacherAuLizard(),
        AbilityFactory.WhenPlayerWouldPlayCard(
            AbilityType.ForcedInterrupt, "AnyPlayer", Event, annuler,
            conditions=[lambda e, m: not m.be_cancel],
        ),
    ]
