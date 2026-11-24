from . import *
# Disruptor Ray (Justice, amelioration 2 [mental]). TECH. WEAPON. Restricted. Uses (2 charge counters).
# Action: Exhaust disruptor ray and remove 1 charge counter from it → choose an attachment, non-ELITE minion, or side scheme. Until the end
# of the round, treat that card's printed text box as if it were blank (except for TRAITS).
#
# Cartes de reference : 16046 Hand Cannon (`desc.Uses "N,charge"` + `CostFunc.Counter("This", 1, 'charge')`) ; rl012 / `face.TreatAsIfBlank(
# effect, until_round_end=True)` (face_action.py:9 : « treat as blank » temporaire, TRAITS conserves) ; fiches uses.md, restricted.md.
# « an attachment, NON-ELITE minion, or side scheme » : trois types possibles (un sbire ELITE n'est pas une cible). « Until the end of the
# ROUND » : `until_round_end`. Le dernier compteur retire defausse la carte (Uses).
def GetAbilities() -> Sequence['Ability']:
    def disruptor(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        for face in effect.targets:
            face.TreatAsIfBlank(effect, until_round_end=True)
    def cible(effect: 'Effect', face: 'CardFace') -> bool:
        if Attachment.IsType(face) or SchemeSide2.IsType(face):
            return True
        return Minion.IsType(face) and not face.HasTrait("ELITE")
    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            disruptor,
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetCostFunc(CostFunc.Counter("This", 1, 'charge'))
        .SetTarget(check_fn=cible),
    ]
