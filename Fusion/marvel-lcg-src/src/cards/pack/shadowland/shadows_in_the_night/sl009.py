from . import *

# Surround the Fortress — COMPLOT ANNEXE. Menace de depart 2 par joueur, Boost 1, Crisis 1.
# When Revealed : Change the villain's position if it has not changed this phase. If the villain's position is Atop the Tenshu, place 1[per_hero] threat on the
#   main scheme; otherwise, place 1[per_hero] threat here.
#
# Cartes de reference : sm/sinister_six/27100a (`PlaceThreatOnSchemes([face], n, effect)`), mut_gen/sabretooth/32069 (`PlaceThreatOnSchemes("MainScheme", n, effect)`).
# ⚠ « 1[per_hero] » = 1 PAR JOUEUR ("1*") ; « here » = sur CETTE manigance annexe ; la position est lue apres le changement eventuel.


def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        Unused(message)
        this = effect.this.CastTo(EncounterSideScheme)
        ChangerSiPasChange(effect)
        if AuTenshu(effect):
            this.PlaceThreatOnSchemes("MainScheme", "1*", effect)
        else:
            this.PlaceThreatOnSchemes([this], "1*", effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
    ]
