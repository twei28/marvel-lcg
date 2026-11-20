from . import *

# Beast Be Praised (2B) — MANIGANCE PRINCIPALE, stade 2. Menace 9 par joueur, depart 2 par joueur, escalade +1 par joueur★.
# [star] Forced Response : After resolving step one of the villain phase, each player chooses:
#   • Place 1 corruption counter on their Creeping Corruption.
#   • Place 3 threat here.
# If this stage is completed, the players lose the game.
#
# Cartes de reference : galactic_storm/majestrixs_verdict `ApresEtapeUn` (`AfterResolveVillainPhaseStep(ForcedResponse, 1, ..)`), sl060b (le choix par joueur), sl002b
# (`IfThisSchemeStageIsCompletedPlayersLoseTheGame`).
# ⚠ Mots-pieges : « AFTER resolving step ONE » : apres l'etape 1 de la phase du mechant (la menace d'escalade), pas apres la phase ; « EACH player chooses » : chaque joueur, pour lui ;
#  « place 3 threat HERE » : sur CE complot (2B), 3 par joueur qui choisit cette branche (pas 3 par joueur en tout) ; la branche corruption exige une Creeping Corruption ;
#  l'etoile de l'escalade renvoie a ce texte : rien de plus a coder (decision Q3 de QUESTIONS.md).


def GetAbilities() -> Sequence['Ability']:

    def apres_etape_un(effect: 'Effect', message: 'Message.AfterResolveVillainPhaseStep') -> None:
        Unused(message)
        this = effect.this.CastTo(MainScheme)

        def choisit(joueur: 'Player') -> None:
            def corruption(cibles: Sequence['CardFace']) -> None:
                Unused(cibles)
                PlacerCorruption(effect, joueur, 1)

            def menace(cibles: Sequence['CardFace']) -> None:
                Unused(cibles)
                this.PlaceThreatOnSchemes([this], 3, effect)

            joueur.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility("Place 1 corruption counter on your Creeping Corruption", corruption, condition=PeutPlacerCorruption(joueur)),
                AbilityFactory.ForChoiceAbility("Place 3 threat here", menace),
            )

        Players.ForEachPlayer(effect, choisit)

    return [
        AbilityFactory.AfterResolveVillainPhaseStep(AbilityType.ForcedResponse, 1, apres_etape_un),
        AbilityFactory.IfThisSchemeStageIsCompletedPlayersLoseTheGame(),
    ]
