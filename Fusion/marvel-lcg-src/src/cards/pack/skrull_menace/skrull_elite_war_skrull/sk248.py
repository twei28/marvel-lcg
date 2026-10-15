from . import *

# Skrull Geneticist — SBIRE (Skrull Elite - War Skrull). GENIUS. SKRULL. MNG 3, ATQ 0, PV 3, 1 icone de
# boost + etoile, icone HAZARD (carte penchee nue : lecture du 15/10/2026, voir defs/modulaires_questions.md).
# [star] Boost: Deal yourself a facedown encounter card.
#
# Cartes de reference :
#  - « Deal yourself a facedown encounter card » : **`ar012`** / **`16118`** Badoon Grunt
#    (`player.DealEncounterCards(1, effect)`) ; **`sk105`** Overthrow (`DealEncounterCard`).
#  - Hazard : natif (`desc.Hazard`, fiche mots-cles/hazard.md).
#
# ⚠ Mots-pieges : « YOURSELF » (le joueur qui retourne la carte de boost) ; « FACEDOWN » : la carte est
# distribuee face cachee, revelee a l'etape 4 de la phase du mechant ou a la fin de l'activation, pas tout de suite.


def GetAbilities() -> Sequence['Ability']:

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        message.GetToPlayer().DealEncounterCards(1, effect)

    return [
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
