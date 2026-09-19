from . import *

# * Diamondback (CRIMINAL UNDERLING) — SCH 1 / ATK 1 / 6 PV, boost [star]+2. Villainous : base.
# [star] Forced Interrupt: When Diamondback attacks you, take 1 damage.
# [star] Boost: Take 1 damage.
# Modeles : 60144 (« When X attacks you » = WhenUnitWouldAttack "This"), 08029
# (identity.TakeDamage(this, 1, effect)) ; en boost, le joueur est
# message.GetToPlayer().

def GetAbilities() -> Sequence['Ability']:

    def un_degat(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this
        joueur = message.GetAgainstPlayer()
        if joueur is not None:
            joueur.GetIdentity().TakeDamage(this, 1, effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        this = effect.this
        message.GetToPlayer().GetIdentity().TakeDamage(this, 1, effect)

    return [
        AbilityFactory.WhenUnitWouldAttack(AbilityType.ForcedInterrupt, "This", un_degat),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
