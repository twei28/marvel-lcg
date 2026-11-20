from . import *
from cards.pack.galactic_storm.campaign import CampaignSetup

# Hidden Might of Hala (1A) — MANIGANCE PRINCIPALE, stade 1.
# Contents: Kree Leader (I) and Kree Leader (II) (Kree Leader (II) and Kree Leader (III) instead for expert
#   mode). Hala Ultimatum and Standard encounter sets. One modular encounter set (Accuser Corps).
# Setup: Put the Hala environment into play. Each player searches the encounter deck for a KREE minion and
#   reveals it.
#
# Cartes de reference :
#  - « Setup » d'une face 1A : `WhenCardSetup("This")`, modele gs117a (Majestrix) / gs079a (Kree Sentry).
#  - « Put the Hala environment into play » : `SetupCards.PutIntoPlay` (modele gs079a, sans `under_control`
#    pour un Environment, qui n'appartient a aucun joueur).
#  - « each player searches the encounter deck for a KREE minion and reveals it » :
#    `ChercherEtReveleMinionKree` (hala_ultimatum/__init__.py) + `Players.ForEachPlayer`.
#  - « Contents » : composition du scenario, portee par data/scenarios/gs_hala_ultimatum*.json.
#
# ⚠ Mots-pieges : « EACH player » (une recherche par joueur, pas une seule pour le groupe) ; la recherche ne
# porte PAS sur la defausse (« the encounter deck » seul, contrairement a l'Action de Hala qui ajoute « and
# discard pile »).


def GetAbilities() -> Sequence['Ability']:

    def mise_en_place(effect: 'Effect', message: 'Message.WhenCardSetup') -> None:
        Unused(message)
        SetupCards.PutIntoPlay(effect, "FirstPlayer", False, name=NOM_HALA, card_type=Environment)

        def chacun(joueur: 'Player') -> None:
            ChercherEtReveleMinionKree(effect, joueur, avec_defausse=False)
        Players.ForEachPlayer(effect, chacun)

    return [
        AbilityFactory.WhenCardSetup("This", mise_en_place),
        *CampaignSetup(3),
    ]
