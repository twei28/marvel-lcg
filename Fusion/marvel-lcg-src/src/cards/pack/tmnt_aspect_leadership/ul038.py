from . import *

# Unified Stike [sic] — EVENEMENT Leadership (TMNT Reskins, Inkwire), cout 0, [energy]. TACTIC.
# Hero Response: When an ally uses a basic power, exhaust your hero -> add your hero's matching power to that
#   ally's power for this use. That ally does not take consequential damage for this use.
#
# MODIFIEE (reskin de `58020` Unified Strike) : l'officielle est une « Hero INTERRUPT: When ... », le scan
# imprime « Hero RESPONSE: When ... » (et le titre « Stike »). QUESTION OUVERTE Q-UL-7 (coquille connue
# de la consigne). LECTURE CODEE EN ATTENDANT (option recommandee A) : Interruption de heros, comme
# l'officielle — c'est la seule lecture ou « for this use » a un sens (une Reponse arrive apres l'usage).
# Script propre copie de 58020.


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
