from . import *

# Binding Ritual — COMPLOT ANNEXE. Menace de depart 1 par joueur, Boost 2, Crisis.
# When Revealed : Each player chooses: • Place 1 corruption counter on their Creeping Corruption. • Place 3 threat here.
#
# Cartes de reference : core/under_attack/01151 (`WhenThisRevealed` + `Players.ForEachPlayer` + `ChooseAbilities(ForChoiceAbility(...).SetTarget("This"), ...)`).
# ⚠ Mots-pieges : « each player chooses » : chaque joueur, l'un apres l'autre, choisit POUR LUI (sa propre Creeping Corruption) ; les 3 menaces s'ajoutent a la menace de depart (1 par
#  joueur) ; sans Creeping Corruption le joueur n'a que la branche « menace ». Crisis, Boost 2 et la menace de depart sont lus dans `desc`.


def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(EncounterSideScheme)

        def choisir(joueur: 'Player') -> None:
            joueur.ChooseAbilities(
                effect,
                BrancheCorruption(effect, joueur, 1),
                AbilityFactory.ForChoiceAbility("Place 3 threat here", lambda cibles: this.PlaceThreatOnSchemes(cibles, 3, effect)).SetTarget("This"),
            )

        Players.ForEachPlayer(effect, choisir)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
    ]
