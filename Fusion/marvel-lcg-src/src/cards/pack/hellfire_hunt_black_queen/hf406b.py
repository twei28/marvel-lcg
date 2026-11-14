from . import *

# Ascending to Godhood (3B). « [star] Forced Response : After step one of the villain phase, place 1 threat here for each time counter on
# Under the Moonlight or Beneath the Sun. If this stage is completed, the players lose the game. »
# Cartes de reference : 04112b / trors/zola `TheMadDoctor` (`AfterResolveVillainPhaseStep(ForcedResponse, 1, ...)`) ; la defaite est lue dans
# le texte imprime par `scheme_main.py` (comme hf106b).
# Le complot garde AUSSI son escalade imprimee (+2 par joueur) : QUESTIONS.md n°3.


def GetAbilities() -> Sequence['Ability']:
    def apres_l_etape_un(effect: 'Effect', message: 'Message.AfterResolveVillainPhaseStep') -> None:
        this = effect.this.CastTo(MainScheme)
        env = Temps(effect)
        n = env.GetCounters(COMPTEUR_TEMPS) if env is not None else 0
        if n > 0:
            this.PlaceThreatInternal(n, effect)

    return [AbilityFactory.AfterResolveVillainPhaseStep(AbilityType.ForcedResponse, 1, apres_l_etape_un)]
