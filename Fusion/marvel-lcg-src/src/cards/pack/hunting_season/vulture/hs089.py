from . import *

# hs089 Metal Talons
# Attach to Vulture. Vulture gains retaliate 1. * Forced Interrupt : son attaque gagne piercing.
# Hero Response : apres avoir attaque Vulture, defaussez une carte de la main -> defaussez ceci.

def GetAbilities() -> Sequence['Ability']:

    def par_le_porteur(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> bool:
        return PorteurEstAttaquant(effect, message)

    def perforer(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        message.GainPiercing(effect)

    def vulture_attaque(effect: 'Effect', message: 'Message.AfterUnitAttackEnd') -> bool:
        cible = effect.this.CastTo(Attachment).bind_face
        return cible is not None and cible in message.attacked_targets

    def defausser_main_et_ceci(effect: 'Effect', message: 'Message.AfterUnitAttackEnd') -> None:
        joueur = message.attacker.GetControlByPlayer()
        if DefausserUneCarteDeLaMain(effect, joueur):
            Faces.DiscardAll([effect.this], effect)

    return [
        AttacherALaRevelation(),
        *AbilityFactory.GiveKeywordToAttached(retaliate=1),
        AbilityFactory.WhenUnitWouldAttack(AbilityType.ForcedInterrupt, Villain, perforer, conditions=[par_le_porteur]),
        AbilityFactory.AfterUnitAttackEnd(
            AbilityType.HeroResponse, "YourIdentity", defausser_main_et_ceci, conditions=[vulture_attaque],
        ),
    ]
