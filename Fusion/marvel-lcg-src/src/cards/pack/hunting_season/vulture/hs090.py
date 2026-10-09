from . import *

# hs090 Projectile Feathers
# Attach to Vulture. Forced Interrupt : Vulture vous attaque, defaussez ceci et subissez 2 degats indirects (3 avec AERIAL).
# Hero Action : YY -> defaussez ceci, Vulture perd AERIAL jusqu'a la fin du tour.

def GetAbilities() -> Sequence['Ability']:

    def vous_attaque(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> bool:
        return PorteurEstAttaquant(effect, message) and AttaqueContreLeJoueur(message) is not None

    def tirer(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        identite = AttaqueContreLeJoueur(message).GetIdentity()
        degats = 3 if identite.HasTrait("AERIAL") else 2
        Faces.DiscardAll([effect.this], effect)
        effect.this.DealIndirectDamage(identite, degats, effect)

    return [
        AttacherALaRevelation(),
        AbilityFactory.WhenUnitWouldAttack(AbilityType.ForcedInterrupt, Villain, tirer, conditions=[vous_attaque]),
        ActionPerdreAerial(Cost("YY")),
    ]
