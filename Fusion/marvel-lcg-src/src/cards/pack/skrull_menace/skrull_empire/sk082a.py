from . import *
from cards.pack.skrull_menace.campaign import CampaignSetup

# Rise of the Skrull Empire — complot principal 1A (mise en place).
# Contents: All villains (I) and (II) (stages (II) and (III) instead for the
#   expert mode). Skrull Empire, Skrull Society and Standard sets. One modular
#   set (Army of Skrulls).
# Setup: Create the PLANET and the Villain deck (see insert). Reveal the top
#   card of the Villain deck. Put the Skrull Empire environment (I) into play
#   (stage (II) instead for the expert mode).
#
# Cartes de reference :
#  - **`55033a`** (God of Lies, 1A) : quatre mechants differents mis de cote
#    (json `"villain": []`), un revele dans `WhenCardSetupBeforePutSetupCards`,
#    les autres poses dans `scenario.villain_deck` ; le `WhenCardSetup` met
#    les environnements en jeu.
#  - **`hs107a`** (Kraven, 1A) + `hunting_season/trap` : creation d'un paquet
#    de scenario nomme (`ScenarioDeck(...).Create(...)`).
#
# ⚠ Choix :
#  - « Contents » : decrit par data/scenarios/sk_skrull_empire(_expert).json ;
#    en expert, seuls les mechants (II)+(III) et les environnements II+III sont
#    mis de cote : `PremierStade` lit donc le mode sans `IsExpert`.
#  - « Put the Skrull Empire environment (I) into play » : MISE EN JEU, pas une
#    revelation ; le When Revealed de l'environnement II (Overthrow) ne part
#    donc pas au setup expert, ce qui ne change rien (aucun Overthrow n'est
#    encore mis de cote).
#  - Un 1A sans TargetThreat avance seul en 1B (scheme_main.py) : ne PAS
#    appeler Advance (lecon gb004a).


def GetAbilities() -> Sequence['Ability']:

    def avant(effect: 'Effect', message: 'Message.WhenCardSetup') -> None:
        InstallerMechants(effect, PremierStade(effect))

    def mise_en_place(effect: 'Effect', message: 'Message.WhenCardSetup') -> None:
        CreerPaquetPlanete(effect)
        env = EnvironnementMisDeCote(effect, PremierStade(effect))
        if env is not None:
            env.PutIntoPlay(Worlds.GetFirstPlayer(effect), effect)

    return [
        *CampaignSetup(1),  # mode campagne : mise en place, regle de cooperation, releve du carnet
        AbilityFactory.WhenCardSetupBeforePutSetupCards(avant),
        AbilityFactory.WhenCardSetup("This", mise_en_place),
    ]
