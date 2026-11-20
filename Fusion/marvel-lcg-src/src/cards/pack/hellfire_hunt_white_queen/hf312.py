from . import *

# White Bishop. Sbire ELITE HELLFIRE, Quickstrike + Villainous (desc). « [star] Forced Response : After White Bishop attacks and damages a character,
# stun that character. [star] Boost : You are stunned. » Meme patron que hf311 avec le statut Stunned.


def GetAbilities() -> Sequence['Ability']:
    def etourdir(effect: 'Effect', message: 'Message.AfterUnitAttackUnit') -> None:
        Faces.GiveStatus([message.attacked], "Stunned", effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        Faces.GiveStatus([message.GetToPlayer().GetIdentity()], "Stunned", effect)

    return [
        AbilityFactory.AfterUnitAttackAndDamageUnit(AbilityType.ForcedResponse, "This", CardFinder(card_type=Hero | AlterEgo | Ally), etourdir),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
