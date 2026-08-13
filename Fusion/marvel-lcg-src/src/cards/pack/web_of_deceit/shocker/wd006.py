from . import *

# * Sandman

def GetAbilities() -> Sequence['Ability']:

    def sandman(effect: 'Effect', message: 'Message.AfterUnitAttackUnit') -> None:
        this = effect.this.CastTo(Minion)
        Unused(this)
        # « discard the top 6 cards of the encounter deck. »
        Faces.DiscardAll(Search.EncounterCardsTop(effect, None, 6) or [], effect)

    return [
        AbilityFactory.AfterUnitAttackAndDamageUnit(
            AbilityType.ForcedResponse,
            "This",
            "Character",
            sandman
        ),
        AbilityFactory.AfterMinionEngagePlayer(
            AbilityType.ForcedResponse,
            "This",
            "You",
            sandman
        ),
    ]
