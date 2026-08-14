from . import *

# Feather Daggers

def GetAbilities() -> Sequence['Ability']:

    def lames(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        # « [star] Vulture's attacks gain piercing and ranged. »
        message.GainPiercing(effect)
        message.GainRanged(effect)

    def riposte(effect: 'Effect', message: 'Message.AfterUnitAttackUnit') -> None:
        # « Hero Response: After Vulture attacks you, discard Feather Daggers →
        # Vulture activates against you. »
        this = effect.this.CastTo(Attachment)
        vulture = this.attached_face
        joueur = effect.GetInitiator()
        Faces.DiscardAll([this], effect)
        if vulture:
            vulture.CastTo(Enemy).DoActivate(joueur, effect)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(
            Villain
        ),
        AbilityFactory.WhenUnitMakeAttack(
            AbilityType.ForcedInterrupt,
            "AttachedVillain",
            lames
        ),
        AbilityFactory.AfterUnitAttackUnit(
            AbilityType.HeroResponse,
            "AttachedVillain",
            "YourIdentity",
            riposte
        ),
    ]
