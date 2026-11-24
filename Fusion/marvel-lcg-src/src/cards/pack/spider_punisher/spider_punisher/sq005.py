from . import *


def GetAbilities() -> Sequence['Ability']:
    def neighborhood_watch(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this, message)
        Faces.ReadyAll(effect.targets, effect)

    def si_aerien(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> bool:
        return EstAerien(effect.GetInitiator())

    return [
        # « You gain the AERIAL trait when 2 or more upgrades you control are exhausted » : le VRAI trait est pose sur l'identite
        # (arbitrage du 26/10/2026), recalcule a chaque inclinaison / redressement ; modele `rl008` (valeur conditionnelle +
        # `ex_change_on_event`) et `dd010` (`trait="AERIAL"`).
        *AbilityFactory.GiveKeywordToAttached(
            "You",
            get_new_value=deux_ameliorations_inclinees,
            trait="AERIAL",
            ex_change_on_event=SurInclinaisonOuRedressement,
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            neighborhood_watch,
            conditions=[si_aerien],
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetTarget(name="Spider-Punisher", canbe_ready=True),
    ]
