from . import *

# Reaver Tracker — SBIRE (x3). REAVER. PV 3, ATK 2, SCH 1, Boost 1.
# When Revealed: Resolve the "Special" ability on the copy of Bleeding Out attached to your identity. If you did not discard an
#   identity-specific card this way, place 1 threat on the main scheme.
#
# Cartes de reference :
#  - `WhenThisRevealed(None, op)` + `message.GetToPlayer()` (`nt015`, `56167`) ; helper `ResoudreSaignement` (ld005) qui RENDS
#    « a-t-on defausse une carte d'identite ? » ;
#  - `this.PlaceThreatOnSchemes("MainScheme", 1, effect)` (`01107`).
#
# ⚠ Mots-pieges :
#  - « If you DID NOT discard an identity-specific card » : la menace se pose quand AUCUNE carte d'identite n'a ete defaussee
#    (deck vide ou cartes d'aspect seules) ; si une est defaussee, le joueur a pris son degat et PAS de menace ;
#  - « YOUR identity » : le joueur a qui le sbire est revele.


def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Minion)

        if not ResoudreSaignement(effect, message.GetToPlayer()):
            this.PlaceThreatOnSchemes("MainScheme", 1, effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            revele,
        ),
    ]
