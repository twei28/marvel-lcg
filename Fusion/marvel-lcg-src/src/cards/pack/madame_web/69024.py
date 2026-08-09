from . import *

# * Spider-Woman: May Parker — custom « Kajislav », carte d'aspect PROTECTION
# Hero Interrupt: When the villain initiates an attack against you, draw 1 card.

def GetAbilities() -> Sequence['Ability']:

    def may_parker(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this.CastTo(Ally)
        Unused(this)

        for target in effect.targets:
            player = target.GetControlByPlayer()
            player.DrawUp(1, effect)

    return [
        AbilityFactory.WhenUnitInitiatesAttackAgainst(
            AbilityType.HeroInterrupt,
            Villain,
            "You",
            may_parker
        ).SetTarget("Initiator"),
    ]
