from . import *

# Exemplar Punishment — TRAITRISE (Majestrix's Verdict), 2 exemplaires. 1 icone de boost.
# When Revealed: For each STARJAMMER ally tucked under Imprisoned on Chandilar choose to either take 1 indirect
#   damage or place 1 threat on the main scheme. If there is no ally tucked under Imprisoned on Chandilar,
#   place 2 threat on it.
#
# Cartes de reference :
#  - « choose to either A or B » : `ChooseAbilities(ForChoiceAbility(A), ForChoiceAbility(B))`, modele OFFICIEL
#    04096b Hunting Down Heroes ; repete une fois par STARJAMMER glisse.
#  - « take 1 indirect damage » : `identite.TakeIndirectDamage(this, 1)` (modele ra028, mf017).
#  - « place 2 threat on IT » : lu « sur Imprisoned on Chandilar » (antecedent le plus proche) ; question Q2 de
#    .planning/todos/2026-10-20-gs5-questions.md (alternative : la manigance principale).
#
# ⚠ Mots-pieges : « FOR EACH » = un choix PAR allie glisse (0 a 6) ; « you » = le joueur qui revele ;
# « If there is NO ally tucked » (Lilandra comprise : un seul glisse suffit a eviter la branche).


def GetAbilities() -> Sequence['Ability']:

    def punition(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this
        joueur = message.GetToPlayer()
        prison = Prison(effect)
        glisses = Glisses(prison)
        if not glisses:
            if prison is not None:
                this.PlaceThreatOnSchemes([prison], 2, effect)
            return
        for _ in glisses:
            joueur.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility(
                    "Take 1 indirect damage",
                    lambda targets: joueur.GetIdentity().TakeIndirectDamage(this, 1, effect),
                ),
                AbilityFactory.ForChoiceAbility(
                    "Place 1 threat on the main scheme",
                    lambda targets: this.PlaceThreatOnSchemes("MainScheme", 1, effect),
                ),
            )

    return [
        AbilityFactory.WhenThisRevealed(None, punition),
    ]
