from . import *

# Unified Strike — EVENEMENT Leadership (TMNT Reskins, Inkwire), cout 0, [energy]. TACTIC.
# Hero Interrupt: When an ally uses a basic power, exhaust your hero -> add your hero's matching power to that
#   ally's power for this use. That ally does not take consequential damage for this use.
#
# MODIFIEE (reskin de `58020` Unified Strike) : l'officielle est une « Hero INTERRUPT: When ... », le scan
# imprime « Hero RESPONSE: When ... » (et le titre « Stike »). Coquille CONFIRMEE le 17/10/2026 : titre
# « Unified Strike », Interruption de heros comme l'officielle (texte affiche corrige). Script propre
# copie de 58020.


def GetAbilities() -> Sequence['Ability']:

    def unified_strike(effect: 'Effect', message: 'Message.WhenUnitUseBasicPower') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)

        allies = effect.cost_func.Get(CostFunc.Exhaust).return_exhausted_cards
        message.AddThatMatchingPower(allies, effect)
        message.DoesNotTakeConsequentialDamage(effect)

    return [
        AbilityFactory.WhenUnitUseBasicPower(
            AbilityType.HeroInterrupt,
            Ally,
            unified_strike
        ).SetPlay().SetLabel()
        .SetCostFunc(CostFunc.Exhaust("YourHero")),
    ]
