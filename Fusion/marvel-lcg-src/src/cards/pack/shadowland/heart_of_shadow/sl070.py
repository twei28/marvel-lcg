from . import *

# Veil of Nightmares — MANIGANCE ANNEXE x2. Menace de depart 5 par joueur, Hazard, Boost 2.
# Hero Action : Place 1 corruption counter on your Creeping Corruption → remove 5 threat from this scheme.
#
# Cartes de reference : 27133 Volunteer Work (Action d'une manigance annexe qui retire sa propre menace : `RemoveThreatFromSchemes([this], n, effect)`), iron_man_model_42 `CoutDuReacteur` (jeton
# pose PAR LE COUT), sl063 (`CoutPlacerCorruption`). Hazard et la menace de depart sont lus dans `desc`.
# ⚠ Mots-pieges : « remove 5 threat FROM THIS scheme » : de CETTE manigance, pas d'une autre, ni du complot principal ; « 5 » : au plus 5 (moins s'il en reste moins) ; le jeton est un COUT :
#  sans Creeping Corruption l'action n'est pas offerte (et la carte ne se vide pas a vide) ; Hero Action : forme heros ; ce n'est pas un contre : les Crises et Patrouilles ne s'y appliquent pas.


def GetAbilities() -> Sequence['Ability']:

    def dissiper(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        this.RemoveThreatFromSchemes([this], 5, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(AbilityType.HeroAction, dissiper, conditions=[PeutPayerCorruption])
            .SetCostFunc(CoutPlacerCorruption(1)),
    ]
