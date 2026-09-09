from . import *

# Web-Shooters — AMELIORATION, cout 1 [wild]. ITEM. TECH. Uses (3 web).
# Your hero gains the AERIAL trait.
# Hero Resource: Exhaust Web-Shooters and remove 1 web counter from it ->
#   generate a [wild] resource.
#
# CARTES DE REFERENCE
#  - `53006` Falcon's Flock, `55055` : `CanGenerateResources(HeroResource,
#    Resources("G")).SetCostFunc(...)`, le montage exact d'une ressource payee
#    par un pion.
#  - `an008`, `ho008`, `sm012` Web Cape : « Your hero gains the X trait » =
#    `GiveKeywordToAttached(Hero, trait=...)`.
#
# TEXTE CONTRE CODE
#  ⚠⚠ « YOUR HERO gains AERIAL » : `Hero` et NON `"You"`. Avec `"You"` le trait
#    irait a l'IDENTITE, donc aussi a l'alter-ego — defaut mesure le 08/09/2026
#    sur `sm012` Web Cape, attrape par son contre-cas dans l'autre forme
#    (lecon `an002` Sera, RECETTES §3). Contre-cas du ici aussi.
#  ⚠ Le trait AERIAL n'est PAS decoratif dans ce pack : `su003` Agility previent
#    TOUS les degats au lieu de 3 quand le heros le porte. Les deux cartes se
#    repondent.
#  ⚠ « Uses (3 web counters) » : base automatique (`desc.Uses`), la carte sort
#    du jeu au dernier pion. Le compteur `web` existait deja.
#  ⚠ « Hero Resource » : sous-type dedie, rien en forme civile.
#  ⚠ « UNE SEULE `CanGenerateResources` par carte » (assert du moteur).
#  ⚠ Aucune limite imprimee : etape 7 bis sans objet.


def GetAbilities() -> Sequence['Ability']:

    return [
        *AbilityFactory.GiveKeywordToAttached(
            Hero,
            trait=TRAIT_AERIAL,
        ),

        AbilityFactory.CanGenerateResources(
            AbilityType.HeroResource,
            Resources("G"),
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetCostFunc(CostFunc.Counter("This", 1, COMPTEUR_TOILE)),
    ]
