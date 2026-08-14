from . import *

# Anti-Gravitational Harness

def GetAbilities() -> Sequence['Ability']:

    def se_defaire(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        # « Alter-Ego Action: Discard a card from your hand and place 2 pigeon
        # counters on the main scheme → discard this card. »
        #
        # Le harnais donne le vol, mais s'en defaire nourrit le reseau : deux
        # pigeons de plus sur le complot, soit un tour de bouclier gagne pour
        # le vilain.
        PigeonsSurLeComplot(effect, 2)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(
            "YourIdentity"
        ),
        # « Attached character gains the AERIAL trait. »
        *AbilityFactory.GiveKeywordToAttached(
            trait=["AERIAL"],
        ),
        AbilityFactory.PlayerActionToDiscardThis(
            AbilityType.AlterEgoAction,
            ex_operation=lambda effect, message: se_defaire(effect, message),
        ).SetCostFunc(CostFunc.Discard(from_where=["YourHandCards"])),
    ]
