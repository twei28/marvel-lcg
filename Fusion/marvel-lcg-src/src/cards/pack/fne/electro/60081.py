from . import *

# * Whiplash (CRIMINAL)
# Forced Interrupt: When Whiplash is attacked, remove 1 charge counter from
#   Electric Charge -> discard the top card of the encounter deck. Deal 1
#   damage to the attacker for each boost icon on the discarded card.
# Le retrait de charge est un COUT (la fleche) : CostFunc.Counter sur
# Electric Charge. `message.trigger` = l'attaquant (WhenUnitWouldAttack).
# Icones : FacesCounter.CountTotalBoostIcons (chiffrees ; « each boost icon »).

def GetAbilities() -> Sequence['Ability']:

    def contre_coup(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this.CastTo(Minion)
        face = Worlds.DiscardEncounterTopCard(effect)
        if face is None:
            return
        n = FacesCounter.CountTotalBoostIcons([face])
        if n > 0:
            this.DealDamage([message.trigger], n, effect)

    return [
        AbilityFactory.WhenUnitWouldBeAttacked(
            AbilityType.ForcedInterrupt,
            "This",
            contre_coup,
        ).SetCostFunc(CostFunc.Counter(CardFinder(name="Electric Charge"), 1, 'charge')),
    ]
