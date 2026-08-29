from . import *

# Malevolent Mimic — side scheme nemesis d'Okoye
# Nakia has coopted a Wakandan secret weapon—a mimic. She's poisoned it to
#   wreak havoc on innocent civilians!
# Forced Response: After an ally is defeated, place 2 threat here.
#
# Modele du declencheur : bkw/08031.py (`AfterUnitBeDefeated`), cible `Ally`
# sans restriction de controle ("an ally", pas "an ally you control" --
# contrairement a Close Ranks/ok010). Pose la menace sur SOI-MEME (`[this]`),
# modele `PlaceThreatOnSchemes` deja utilise par kb008 sur une AUTRE
# manigance.


def GetAbilities() -> Sequence['Ability']:

    def malevolent_mimic(effect: 'Effect', message: 'Message.AfterUnitBeDefeated') -> None:
        # CORRECTIF (empiriquement trouve via test_capacites, cas ok020) :
        # NameError, 'SideScheme' n'existe pas dans l'espace de noms des
        # scripts -- le type JSON "SideScheme" correspond a la classe
        # `EncounterSideScheme` (piege documente au GUIDE §10). Le cas etait
        # passe au VERT pour une mauvaise raison (StartingThreat=2* imprime
        # coincidait avec les 2 menaces attendues de la Response, qui
        # plantait en silence) : lecon retenue, verifier desormais remis a 0.
        this = effect.this.CastTo(EncounterSideScheme)
        Unused(message)

        this.PlaceThreatOnSchemes([this], 2, effect)

    return [
        AbilityFactory.AfterUnitBeDefeated(
            AbilityType.ForcedResponse,
            Ally,
            malevolent_mimic,
        ),
    ]
