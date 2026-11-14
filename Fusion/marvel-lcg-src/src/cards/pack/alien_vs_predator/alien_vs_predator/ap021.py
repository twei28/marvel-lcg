from . import *

# * Alien Praetorian — SBIRE unique. ELITE. XENOMORPH. SCH 2, ATK 2, PV 8. Boost 3.
# Villainous.
# Forced Response: After the villain phase begins, Alien Praetorian engages the first player.
#
# Cartes de reference : Villainous natif (`desc`, fiche villainous.md) ; « After the villain phase begins » : `AfterPhaseBegin(ForcedResponse,
#   "Villain")` (16026) ; « engages the first player » : `EngagePlayer(premier)` (21143).
#
# ⚠ Mots-pieges : deja engage avec le premier joueur -> rien ne change ; le premier joueur du round (le jeton tourne).


def GetAbilities() -> Sequence['Ability']:

    def engage(effect: 'Effect', message: 'Message.AfterPhaseBegin') -> None:
        Unused(message)
        premier = Worlds.GetFirstPlayer(effect)
        sbire = effect.this.CastTo(Minion)
        if premier is not None and sbire.GetEngagedPlayer() is not premier:
            sbire.EngagePlayer(premier, effect)

    return [
        AbilityFactory.AfterPhaseBegin(AbilityType.ForcedResponse, "Villain", engage),
    ]
