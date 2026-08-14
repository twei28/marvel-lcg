from . import *

# Viper Fangs

def GetAbilities() -> Sequence['Ability']:

    def transpercement(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        # « [star] Forced Interrupt: When attached villain attacks, the attack
        # gains piercing. »
        message.GainPiercing(effect)

    def menace(effect: 'Effect', message: 'Message.AfterUnitAttackUnit') -> None:
        # « If that attack deals damage to an identity, place 1 threat on the
        # main scheme. » Meme modele que les Ionic Boots du lot 1 : la seconde
        # moitie de la phrase est une reponse a l'attaque QUI A BLESSE, pas une
        # suite de l'interruption.
        this = effect.this.CastTo(Attachment)
        this.PlaceThreatOnSchemes("MainScheme", 1, effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        # « [star] Boost: Attach this card to The Lizard. »
        this = effect.this.CastTo(Attachment)
        lizard = Worlds.FindVillain(effect)
        if lizard:
            this.AttachTo2(lizard, effect)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(
            Villain
        ),
        AbilityFactory.WhenUnitMakeAttack(
            AbilityType.ForcedInterrupt,
            "AttachedVillain",
            transpercement
        ),
        AbilityFactory.AfterUnitAttackAndDamageUnit(
            AbilityType.ForcedResponse,
            "AttachedVillain",
            "YourIdentity",
            menace
        ),
        AbilityFactory.WhenCardBecomeBoost(
            "This",
            boost
        ),
    ]
