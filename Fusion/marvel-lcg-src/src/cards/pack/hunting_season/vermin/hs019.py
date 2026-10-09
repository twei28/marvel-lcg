from . import *

# Swarmed by Rats (hs019)
# Attach to your identity. Each RAT minion engaged with you gains guard.
# Interrupt (code en Response, decision utilisateur) : After you defeat a RAT minion
# engaged with you, discard two cards from your hand -> discard this card.
# Modeles : AttachToFaceWhenPutIntoPlay (dr013), GiveKeywordToInPlayWhenApplyThis,
# CostFunc.Discard("HandCard", range=(2, 2)) (gorr gb013).

def GetAbilities() -> Sequence['Ability']:

    def rat_vaincu(effect: 'Effect', message: 'Message.AfterUnitDefeatedUnit') -> bool:
        return EstRat(message.target)

    def engage_avec_moi(effect: 'Effect', face: 'Minion') -> bool:
        return face.GetEngagedPlayer() == effect.GetInitiator()

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay("YourIdentity"),
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            CardFinder(trait="RAT", card_type=Minion, check_effect_fn=engage_avec_moi),
            guard=1,
            change_on_event=[OnEvent.CardType(CardFinder(trait="RAT")), OnEvent.PlayAreaCard(Minion)],
        ),
        AbilityFactory.AfterUnitDefeatedUnit(
            AbilityType.Response,
            "You",
            Minion,
            DiscardThisCard,
            conditions=[rat_vaincu],
        ).SetCostFunc(CostFunc.Discard("HandCard", range=(2, 2))),
    ]
