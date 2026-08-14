from . import *

# Trapped in the Pipes

def GetAbilities() -> Sequence['Ability']:

    def changement_de_forme(effect: 'Effect', message: 'Message.AfterUnitChangeForm') -> None:
        # « [star] Forced Response: After you change form, discard this card. »
        Faces.DiscardAll([effect.this], effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        # « [star] Boost: You are confused. »
        Faces.GiveStatus([message.GetToPlayer().GetIdentity()], "Confused", effect)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(
            "YourIdentity"
        ),
        Negate(1),
        AbilityFactory.AfterUnitChangeForm(
            AbilityType.ForcedResponse,
            "AttachedIdentity",
            changement_de_forme
        ),
        AbilityFactory.WhenCardBecomeBoost(
            "This",
            boost
        ),
    ]
