from . import *


def GetAbilities() -> Sequence['Ability']:
    def revelry(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        Unused(message)
        joueur = effect.GetInitiator()
        # « If a minion was defeated this turn » : indicateur de TOUR alimente par wt002 (RR « Turn » : le tour du joueur).
        n = 3 if getattr(effect.world.stat, "wt_sbire_vaincu_ce_tour", False) else 2
        joueur.GetIdentity().GainUntilRoundEnd(effect, hand_size=n)

    return [
        AbilityFactory.WhenInYourPlayTurn(AbilityType.AlterEgoAction, revelry).SetPlay().SetLabel()
        .SetTarget("TeamUp"),
    ]
