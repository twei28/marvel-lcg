from . import *

# * Hun — SBIRE nemesis. BRUTE. PURPLE DRAGONS. PV 4, ATQ 2, SCH 1, Boost 3.
# Toughness.
# Forced Response: After Hun attacks and damages a character, stun that
#   character.
# (Casey Jones' nemesis minion.)
#
# MOTS-CLES : TOUGHNESS — fiche `docs/reference/mots-cles/toughness.md`
# (`desc.Toughness = "1"`, AUCUN SCRIPT) ; `desc.Nemesis = "Casey Jones"`.
#
# CARTES DE REFERENCE
#  - `21156` Laufey (mts) : TEXTE IDENTIQUE (« Toughness. Forced Response: After
#    Laufey attacks and damages a character, stun that character »), montage
#    `AfterUnitAttackAndDamageUnit(ForcedResponse, "This", None, op,
#    target_in_play=True)` + `Faces.GiveStatus([message.attacked], "Stunned")`.
#
# TEXTE CONTRE CODE
#  ⚠ « attacks AND DAMAGES » : pas une attaque sans degat (Tough, defense
#    totale) ; `AfterUnitAttackAndDamageUnit`.
#  ⚠ « a CHARACTER » : heros, alter-ego OU allie (pas « you »).
#  ⚠ « stun THAT character » : l'attaque cible, et seulement elle.
#  ⚠ La Reponse n'a PAS de [star] : toujours active (pas reservee au mode expert).


def GetAbilities() -> Sequence['Ability']:

    def hun(effect: 'Effect', message: 'Message.AfterUnitAttackUnit') -> None:
        this = effect.this.CastTo(Minion)
        Unused(this)

        Faces.GiveStatus([message.attacked], "Stunned", effect)

    return [
        AbilityFactory.AfterUnitAttackAndDamageUnit(
            AbilityType.ForcedResponse,
            "This",
            None,
            hun,
            target_in_play=True,
        ),
    ]
