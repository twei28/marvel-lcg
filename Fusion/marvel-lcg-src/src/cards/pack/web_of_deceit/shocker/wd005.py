from . import *

# Vibro-Shock Gauntlets

def GetAbilities() -> Sequence['Ability']:

    def blesse(effect: 'Effect', message: 'Message.AfterUnitAttackUnit') -> None:
        # « After Shocker attacks and damages you, discard a card from your hand. »
        joueur = message.attacked.GetControlByPlayer()
        joueur.AskDiscardFaces(joueur.hand_cards.Get(), (1, 1), effect)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(
            Villain
        ),
        AbilityFactory.AfterUnitAttackAndDamageUnit(
            AbilityType.ForcedResponse,
            "AttachedVillain",
            "YourIdentity",
            blesse
        ),
        # « Hero Action: Spend [physical][mental] resources and remove a stunned
        # or confused status card from Shocker -> discard Vibro-Shock Gauntlets. »
        AbilityFactory.PlayerActionToDiscardThis(
            AbilityType.HeroAction,
        ).SetCost(Cost("RB")),
    ]
