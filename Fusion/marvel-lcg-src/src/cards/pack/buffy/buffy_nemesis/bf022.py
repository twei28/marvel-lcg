from . import *

# * Drusilla — SBIRE nemesis (VAMPIRE). SCH 1, ATQ 2*, PV 5, boost 2. Teamwork (VAMPIRE).
# [star] Forced Response: After Drusilla attacks you, place 1 threat on each scheme.
#
# CARTES DE REFERENCE
#  - `Teamwork` : natif, `desc.Teamwork = "VAMPIRE"` (fiche `mots-cles/teamwork.md`), aucun script.
#  - `30031` Bora : `this.PlaceThreatOnSchemes("EachScheme", 1, effect)` pour « each scheme » ; `AfterUnitAttackEnd(.., against_who="You")`.
#
# TEXTE CONTRE CODE
#  « attacks YOU » -> `against_who="You"` (le joueur engage), pas n'importe quelle attaque. « each scheme » -> principale ET annexes.


def GetAbilities() -> Sequence['Ability']:

    def drusilla(effect: 'Effect', message: 'Message.AfterUnitAttackEnd') -> None:
        this = effect.this.CastTo(Minion)
        Unused(message)
        this.PlaceThreatOnSchemes("EachScheme", 1, effect)

    return [
        AbilityFactory.AfterUnitAttackEnd(
            AbilityType.ForcedResponse,
            "This",
            drusilla,
            against_who="You",
        ),
    ]
