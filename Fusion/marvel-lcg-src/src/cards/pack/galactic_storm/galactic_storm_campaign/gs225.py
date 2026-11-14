from . import *

# * Gladiator (KALLARK) — ALLIE de campagne (Basic / Campaign, n° 225). Cout 4. THW 1* / ATK 3**, 4 PV.
# AERIAL.
# Honorary.
# Response: After you play Gladiator from your hand, defeat a minion.
#
# Cartes de reference :
#  - **`core/spider_man/01002`** Black Cat : `AbilityFactory.AfterPlayerPlayedCard(ForcedResponse, "You",
#    "This", ...)` pour « After you play THIS card from your hand ».
#  - **`jj/jessica_jones/61002`** : `Faces.DefeatUnits([cible], this, effect)` pour un « defeat » direct
#    (pas des degats, une defaite sans calcul de PV).
#
# ⚠ Mots-pieges :
#  - « a MINION » : cible un sbire, pas le mechant (`.SetTarget(Minion)`) ;
#  - « Response » (pas Forced Response) : optionnelle au sens des regles, mais son declencheur est un
#    Forced Response moteur comme toute Response « After » qui n'a pas de cout a part le jeu de la carte
#    (modele Black Cat, meme AbilityType).


def GetAbilities() -> Sequence['Ability']:

    def gladiator(effect: 'Effect', message: 'Message.AfterPlayerPlayedCard') -> None:
        Unused(message)
        Faces.DefeatUnits(effect.targets, effect.this, effect)

    return [
        AbilityFactory.AfterPlayerPlayedCard(
            AbilityType.ForcedResponse,
            "You",
            "This",
            gladiator,
        ).SetTarget(Minion),
    ]
