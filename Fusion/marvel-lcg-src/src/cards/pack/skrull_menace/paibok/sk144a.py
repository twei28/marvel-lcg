from . import *
from cards.pack.skrull_menace.campaign import CampaignSetup

# Power Skrull Engineering 1A — complot principal, face A (mise en place).
# Contents: Paibok I and Paibok II (Paibok II and Paibok III for expert mode).
#   Paibok and Standard encounter sets. One modular encounter set (New Revengers).
# Setup: Place 1 mastery counter on Paibok.
#
# Cartes de reference : **`an001b`/`ok001b`** pour `WhenCardSetup("This", ...)`
# (recette RECETTES-MOTEUR « Setup ») ; compteur maison pose par
# `Faces.PlaceCountersOn` comme le 'momentum' de `40123` Head of Steam.
# « Contents » : decrit par data/scenarios/sk_paibok(_expert).json.
#
# ⚠ Mots-pieges : « on PAIBOK » (le mechant, pas le nemesis de Lyja : helper
# `PaibokEnJeu`) ; compteur 'mastery' declare dans card_face.py (sinon `IsCounter`
# refuse le nom). Un 1A sans TargetThreat avance seul en 1B : ne PAS appeler Advance.


def GetAbilities() -> Sequence['Ability']:

    def mise_en_place(effect: 'Effect', message: 'Message.WhenCardSetup') -> None:
        Unused(message)
        PoserMaitrise(effect)

    return [
        *CampaignSetup(3),  # mode campagne : mise en place, regle de cooperation, releve du carnet
        AbilityFactory.WhenCardSetup("This", mise_en_place),
    ]
