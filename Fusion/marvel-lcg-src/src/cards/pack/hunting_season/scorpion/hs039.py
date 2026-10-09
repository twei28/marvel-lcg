from . import *

# hs039 Tail Laser

def GetAbilities() -> Sequence['Ability']:
    def revelee(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        AttacherALaQueue(effect.this.CastTo(Attachment), effect)

    def attaque(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        message.GainRanged(effect)
        message.GainOverKill(effect)

    def par_scorpion(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> bool:
        return ScorpionPorteCetteQueue(effect, message.attacker)

    def renforcer(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        Faces.ShuffleAllTo([effect.this], "EncounterDeck", effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revelee),
        AbilityFactory.WhenUnitWouldAttack(AbilityType.ForcedInterrupt, Villain, attaque, conditions=[par_scorpion]),
        AbilityFactory.WhenCardBecomeBoost("This", renforcer),
    ]
