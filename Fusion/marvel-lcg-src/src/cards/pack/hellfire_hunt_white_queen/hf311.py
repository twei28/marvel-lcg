from . import *

# Black Bishop. Sbire ELITE HELLFIRE, Toughness + Villainous (desc). « [star] Forced Response : After Black Bishop attacks and damages a character,
# confuse that character. [star] Boost : You are confused. » Cartes de reference : 22028 Gamora (`AfterUnitAttackAndDamageUnit`), 41029 (`Confused`).


def GetAbilities() -> Sequence['Ability']:
    def desorienter(effect: 'Effect', message: 'Message.AfterUnitAttackUnit') -> None:
        Faces.GiveStatus([message.attacked], "Confused", effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        Faces.GiveStatus([message.GetToPlayer().GetIdentity()], "Confused", effect)

    return [
        AbilityFactory.AfterUnitAttackAndDamageUnit(AbilityType.ForcedResponse, "This", CardFinder(card_type=Hero | AlterEgo | Ally), desorienter),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
