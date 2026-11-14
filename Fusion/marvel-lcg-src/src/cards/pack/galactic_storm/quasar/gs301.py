from . import *

# * Quantum Bands — amelioration signature (QUASAR 1/16), ITEM, sans cout.
# Icone de ressource imprimee : [wild] (case verte a etoile, identique a sk010 /
# sk025 du meme auteur, RES=G : verifie par decoupe le 20/10/2026).
# Permanent.
# Quasar gains the AERIAL trait.
# Hero Resource: Exhaust Quantum Bands → generate a [wild] resource.
#
# Cartes de reference :
#  - **`sk002a`** Skrull Origin (meme auteur) : amelioration PERMANENTE sans
#    cout posee au Setup, « Hulkling gains the [[SKRULL]] trait » =
#    `*GiveKeywordToAttached(CardFinder(name="Hulkling"), trait=...)`.
#  - **`41002b`** Psi-Katana / `sk013` Excelsior : ressource d'amelioration
#    `CanGenerateResources(type, Resources(...)).SetCostFunc(CostFunc.Exhaust(
#    "This"))` (RECETTES §4) ; « Hero Resource » = `AbilityType.HeroResource`.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « Permanent. » : base automatique (desc.Permanent, has_permanent.py),
#    aucun script. Exception codee dans le moteur pour gs099q Maelstrom, qui
#    la glisse sous lui (voir has_permanent.py et le gabarit de gs099q).
#  - « **Quasar** gains » : NOM de la face HEROS (piege an002 Sera, RECETTES
#    §3) : Wendell Vaughn n'est pas AERIAL. `card_type=Hero` en plus du nom,
#    pour ne jamais viser l'allie officiel homonyme `21047` * Quasar.
#  - « **Hero** Resource » : uniquement en forme heros.
#  - « generate a [wild] » : l'icone du texte est l'etoile du joker (decoupe
#    contre sk010/sk025). Le joueur choisit la couleur quand un effet la lit
#    (No Holding Back : `GetPaidResources(True)` -> `AskSpecifyResources`,
#    conforme a la FAQ p.22 du livret 1.2).
#  - UNE SEULE `CanGenerateResources` par carte (assert, RECETTES §4).


def GetAbilities() -> Sequence['Ability']:
    return [
        *AbilityFactory.GiveKeywordToAttached(
            CardFinder(name="Quasar", card_type=Hero),
            trait="AERIAL",
        ),
        AbilityFactory.CanGenerateResources(
            AbilityType.HeroResource,
            Resources("G"),
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
