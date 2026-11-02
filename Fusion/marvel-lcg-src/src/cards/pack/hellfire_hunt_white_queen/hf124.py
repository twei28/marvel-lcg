from . import *

# Mutant Supremacy. Manigance annexe. « Forced Response : After White Queen attacks and damages a character, stun that character. Forced Response :
# After White Queen schemes against you, you are confused. [star] Boost : If White Queen is in DIAMOND form, you are stunned. »
# Cartes de reference : 22028 Gamora (`AfterUnitAttackAndDamageUnit`), 41029 (`GiveStatus(..., "Confused")`), 47xxx (`AfterUnitSchemeAgainst`).


def GetAbilities() -> Sequence['Ability']:
    def etourdir(effect: 'Effect', message: 'Message.AfterUnitAttackUnit') -> None:
        Faces.GiveStatus([message.attacked], "Stunned", effect)

    def desorienter(effect: 'Effect', message: 'Message.AfterUnitSchemeEnd') -> None:
        joueur = message.GetAgainstPlayer()
        if joueur is not None:
            Faces.GiveStatus([joueur.GetIdentity()], "Confused", effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        if EstDiamant(VilainWQ(effect)):
            Faces.GiveStatus([message.GetToPlayer().GetIdentity()], "Stunned", effect)

    return [
        AbilityFactory.AfterUnitAttackAndDamageUnit(AbilityType.ForcedResponse, ChercheurWQ(), CardFinder(card_type=Hero | AlterEgo | Ally), etourdir),
        AbilityFactory.AfterUnitSchemeAgainst(AbilityType.ForcedResponse, ChercheurWQ(), "You", desorienter),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
