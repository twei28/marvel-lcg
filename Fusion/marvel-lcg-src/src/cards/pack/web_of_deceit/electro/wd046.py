from . import *

# * Electro (sbire, 12/24)

def GetAbilities() -> Sequence['Ability']:

    def frappe(effect: 'Effect', message: 'Message.AfterUnitAttackUnit') -> None:
        # « [star] Forced Response: After Electro attacks and damages you,
        # discard the top 7 cards of your deck. »
        joueur = message.attacked.GetControlByPlayer()
        joueur.DiscardDeckTopCards(7, effect)

    def defaite(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        # « When Defeated: Remove 4 threat from a side scheme. »
        RetirerMenaceDUneManigance(effect, 4)

    return [
        AbilityFactory.AfterUnitAttackAndDamageUnit(
            AbilityType.ForcedResponse,
            "This",
            "YourIdentity",
            frappe
        ),
        AbilityFactory.WhenUnitBeDefeated(
            AbilityType.WhenDefeated,
            "This",
            defaite
        ),
    ]
