from . import *

# * Supreme Intelligence (I) — MECHANT (Supreme Intelligence). KREE. SCH 2, ATK 1, 13[per_hero] PV.
# Forced Response: After a KREE minion is defeated, heal 1 damage from the villain. If that minion has the
#   ELITE trait, give the villain a facedown boost card.
#
# Cartes de reference :
#  - **`skrull_pantheon/sk179`** Shapeless Wastes et **`fne/kingpin`** `ReponseForceeSoutien` :
#    `AfterUnitBeDefeated(ForcedResponse, <finder de sbire>, op)` = « after a minion is defeated » ; le trait
#    du vaincu se lit sur `message.trigger`.
#  - **`skrull_menace/communs_modulaires.DonnerBoostAuMechant`** / `sf011` : `Faces.GiveFacedownBoostCards`.
#  - `nt008` : `HealthUnits(cibles, 1, effect)` pour « heal 1 damage ».
#
# ⚠ Mots-pieges : « a KREE minion » (tout sbire KREE, quel que soit le joueur engage ; pas un allie) ;
# « AFTER ... is defeated » (Reponse : le sbire est deja parti) ; « if THAT minion has the ELITE trait » : le
# trait GAGNE par Genetic Augmentation compte (le sbire l'avait au moment de la defaite : `EtaitElite`) ;
# « heal 1 damage from the VILLAIN » (pas du sbire). Helper partage avec gs196 : `ReponseSbireKreeVaincu`.


def GetAbilities() -> Sequence['Ability']:
    return [ReponseSbireKreeVaincu(boost_si_elite_seulement=True)]
