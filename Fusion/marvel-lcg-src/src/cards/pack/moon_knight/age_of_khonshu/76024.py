from . import *

# * The Iron Fist — custom « DesignHacker » (Age of Khonshu)
# Linked (Iron Fist) : mis en jeu par le When Defeated de 76019.
# Hero Interrupt: When you attack an enemy, exhaust The Iron Fist and remove 1
#   mystic counter from it → that attack deals +1 damage and stuns that enemy.


def GetAbilities() -> Sequence['Ability']:

    def renforcer_l_attaque(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)
        message.GainATKForThisAttack(1, effect)
        Faces.GiveStatus(list(message.attacked_targets), "Stunned", effect)

    def attaque_de_son_controleur(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> bool:
        controleur = effect.this.GetControlByPlayer()
        if controleur is None:
            return False
        identite = controleur.GetIdentity()
        return identite is not None and message.attacker == identite

    return [
        AbilityFactory.WhenUnitMakeAttack(
            AbilityType.HeroInterrupt,
            None,
            renforcer_l_attaque,
            conditions=[attaque_de_son_controleur],
        ).SetName("The Iron Fist")
        .SetCostFunc(CostFunc.Exhaust("This"))
        .SetCostFunc(CostFunc.Counter("This", 1, 'mystic')),
    ]
