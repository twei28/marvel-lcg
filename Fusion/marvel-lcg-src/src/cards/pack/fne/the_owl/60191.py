from . import *

# Flight Serum (SUPERPOWER) — +1 SCH / +1 ATK : cles desc "SCH+"/"ATK+".
# Attach to a non-AERIAL enemy. Otherwise, this card gains surge.
# Attached enemy gains AERIAL.
# Hero Action: Discard an ATTACK event from your hand -> discard this card.
#
# Modeles : AttachToFaceWhenPutIntoPlay(if_cannot_gain_surge=True), 18027 In A
# Bind (CostFunc.Discard("YourHandCards", trait="ATTACK", card_type=Event)).

def GetAbilities() -> Sequence['Ability']:
    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(
            CardFinder(non_trait="AERIAL", card_type=Enemy),
            if_cannot_gain_surge=True,
        ),
        *AbilityFactory.GiveKeywordToAttached(
            "Character",
            trait="AERIAL",
        ),
        AbilityFactory.PlayerActionToDiscardThis(
            AbilityType.HeroAction,
        ).SetCostFunc(CostFunc.Discard("YourHandCards", trait="ATTACK", card_type=Event)),
    ]
