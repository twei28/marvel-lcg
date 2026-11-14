from . import *

# * Araki — SBIRE (Majestrix's Verdict). SHI'AR. MNG 3, ATQ 1, PV 4. Aucune icone de boost (etoile seule).
# Patrol. Vulnerable.
# When Defeated: Place 2 threat on each scheme in play.
# [star] Boost: Place 1 threat on each scheme in play.
#
# Cartes de reference :
#  - Patrol, Vulnerable : BASES AUTOMATIQUES (`desc.Patrol`, `desc.Vulnerable`, fiches patrol.md, vulnerable.md).
#  - When Defeated : `WhenUnitBeDefeated(WhenDefeated, "This")`, modele sk155 General Kalamari.
#  - « each scheme in play » : `PlaceThreatOnSchemes("EachScheme", n)` (card_face.py, littéral moteur :
#    manigance principale ET annexes).
#  - Boost : `WhenCardBecomeBoost("This")` (RECETTES §1, modele an013).
#
# ⚠ Mots-pieges : « EACH SCHEME » = principale + annexes (la prison comprise) ; Vulnerable : defausse (pas
# « vaincu ») s'il est sonne ou desoriente, donc PAS de « When Defeated » dans ce cas.


def GetAbilities() -> Sequence['Ability']:

    def vaincu(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        Unused(message)
        effect.this.PlaceThreatOnSchemes("EachScheme", 2, effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        Unused(message)
        effect.this.PlaceThreatOnSchemes("EachScheme", 1, effect)

    return [
        AbilityFactory.WhenUnitBeDefeated(AbilityType.WhenDefeated, "This", vaincu),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
