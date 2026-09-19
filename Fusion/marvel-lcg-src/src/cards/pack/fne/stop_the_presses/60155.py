from . import *

# * J. Jonah Jameson (DAILY BUGLE, PERSONA) — Uses (3 stamina) : base.
# Action: Exhaust J. Jonah Jameson, remove 1 stamina counter from him, and
#   deal yourself 1 facedown encounter card -> draw 2 cards.
# Trois couts : Exhaust, Counter, DealPlayerEncounterCard(1, "Initiator").

def GetAbilities() -> Sequence['Ability']:

    def piocher(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        effect.GetInitiator().DrawUp(2, effect)

    a = AbilityFactory.WhenInYourPlayTurn(AbilityType.Action, piocher).SetName("J. Jonah Jameson: deal yourself 1 encounter card, draw 2 cards")
    for c in CoutDeReporter() + [CostFunc.DealPlayerEncounterCard(1, "Initiator")]:
        a = a.SetCostFunc(c)
    return [a]
