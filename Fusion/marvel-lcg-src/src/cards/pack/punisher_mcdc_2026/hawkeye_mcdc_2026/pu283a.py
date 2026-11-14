from . import *

# * Hawkeye (MC×DC 2026) — face HEROS (p284). THW 2, ATK 1, DEF 2, main 5, 9 PV. AVENGER. S.H.I.E.L.D.
# Hawkeye's basic attacks gain ranged.
# "Quick Draw" — Action : Ready Hawkeye's Bow. (Limit once per phase.)
#
# Cartes de reference : trors/hawkeye/04001a (le Hawkeye OFFICIEL : meme Quick Draw, cible `Upgrade name=HAWKEYE_BOW_NAME canbe_ready=True`, mais cout « Exhaust
# Hawkeye » ici SUPPRIME et limite par phase), punisher_mcdc_2026/pu146 (`UnitAttackGainKeyword("This", ranged=True)`, meme famille « X's attacks gain ranged »).
# ⚠ Mots-pieges : « basic attacks » = `is_basic_attack=True` (pas les attaques d'evenement : l'Arc donne deja ranged aux fleches) ; « Ready Hawkeye's Bow » : pas de
# cout d'inclinaison de Hawkeye (differe du 04001a) ; « Limit once per PHASE » (pas par round).


def GetAbilities() -> Sequence['Ability']:

    def quick_draw(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        Faces.ReadyAll(effect.targets, effect)

    return [
        AbilityFactory.UnitAttackGainKeyword("This", is_basic_attack=True, ranged=True),
        AbilityFactory.WhenInYourPlayTurn(AbilityType.Action, quick_draw).SetName("Quick Draw")
        .LimitOncePerPhase()
        .SetTarget(Upgrade, name=HAWKEYE_BOW_NAME, canbe_ready=True),
    ]
