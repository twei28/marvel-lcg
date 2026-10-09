from . import *

# hs165 * Old Man Logan (Experience Cost 4)
# Interrupt : quand il defend contre une attaque, inflige a l'attaquant des degats egaux a son ATK.

def GetAbilities() -> Sequence['Ability']:

    def riposte(effect: 'Effect', message: 'Message.WhenUnitWouldDefend') -> None:
        this = effect.this.CastTo(Ally)
        this.DealDamage(effect.targets, this.attack, effect)

    return [
        AbilityFactory.WhenUnitDefendAgainstAttack(AbilityType.Interrupt, "This", riposte).SetTarget("Attacker"),
    ]
