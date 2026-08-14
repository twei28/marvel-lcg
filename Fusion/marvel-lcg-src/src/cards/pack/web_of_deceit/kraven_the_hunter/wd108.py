from . import *

# * Kraven the Hunter

def GetAbilities() -> Sequence['Ability']:

    def epuiser(effect: 'Effect', message: 'Message.AfterUnitAttackUnit') -> None:
        # « [star] Forced Response: After Kraven the Hunter attacks and damages
        # you, exhaust 1 upgrade or support you control. »
        joueur = message.attacked.GetControlByPlayer()
        cartes = [x for x in joueur.GetControlCards()
                  if (Upgrade.IsType(x) or Support.IsType(x)) and x.CanExhaust()]
        if not cartes:
            return
        choisie = joueur.AskChooseFace(cartes, effect, prompt="Exhaust an upgrade or support")
        Faces.ExhaustAll([choisie or cartes[0]], effect)

    return [
        AbilityFactory.AfterUnitAttackAndDamageUnit(
            AbilityType.ForcedResponse,
            "This",
            "YourIdentity",
            epuiser
        ),
    ]
