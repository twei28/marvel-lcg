from . import *

# * Casey Jones (face heros) — VIGILANTE. PV 10, ATQ 2, CTR 2, DEF 2, main 5.
# Overswing — Resource: Discard a WEAPON upgrade you control with the
#   restricted keyword → generate [wild][wild][wild] resources for an ATTACK,
#   THWART, or DEFENSE event. (Limit once per phase.)
#
# CARTES DE REFERENCE
#  - `34001a` Phoenix (« Psionic Bond — Resource: remove a power counter →
#    generate a [wild] resource. (Limit once per phase.) ») : meme montage,
#    `CanGenerateResources(HeroResource, Resources("G")).SetName(...)
#    .SetCostFunc(...).LimitOncePerPhase()`. Ici le cout est une DEFAUSSE
#    d'amelioration et la ressource vaut trois wild.
#  - `32031a` Shadowcat / `32180` Brawler : « for an ATTACK or DEFENSE event » =
#    `for_card=CardFinder(traits=[...], card_type=Event)` (`traits` est un OU).
#  - `50177` : `CostFunc.Discard("YouControlCards", card_type=...)` pour
#    defausser une carte EN JEU que le joueur controle.
#
# TEXTE CONTRE CODE
#  ⚠ « a WEAPON upgrade YOU CONTROL » : cible `YouControlCards` (en jeu, sous le
#    controle du joueur), PAS la main ni la defausse (le `Default` de
#    `CostFunc.Discard` serait toute la table, RECETTES §5).
#  ⚠ « with the RESTRICTED keyword » : `face.restricted > 0` (le mot-cle LU, pas
#    une liste de cartes), filtre `check_effect`.
#  ⚠ « [wild][wild][wild] » : `Resources("GGG")`, trois icones wild (la meme
#    glyphe que `04010` / `04033`, verifiee par decoupe, voir
#    .planning/tmnt/pics-casey-icones/wild.png).
#  ⚠ « for an ATTACK, THWART, OR DEFENSE EVENT » : type Event ET l'un des trois
#    traits ; une amelioration ou un allie ne se paie pas avec.
#  ⚠ « (Limit once per phase.) » : `LimitOncePerPhase()` (temoin d'epuisement
#    dans tmnt_casey.py).
#  ⚠ Le nom italique « Overswing » : `SetName("Overswing")`.
#  Le `ex_operation` consigne l'arme defaussee sur la carte payee (Clap Back).


def GetAbilities() -> Sequence['Ability']:

    def avec_le_mot_cle_restricted(effect: 'Effect', face: 'CardFace') -> bool:
        Unused(effect)
        return getattr(face, "restricted", 0) > 0

    return [
        AbilityFactory.CanGenerateResources(
            AbilityType.Resource,
            Resources("GGG"),
            for_card=CardFinder(traits=["ATTACK", "THWART", "DEFENSE"], card_type=Event),
            ex_operation=ConsignerArmeDefausseePourPayer,
        ).SetName("Overswing")
        .SetCostFunc(CostFunc.Discard(
            "YouControlCards",
            card_type=Upgrade,
            trait=TRAIT_ARME,
            check_effect=avec_le_mot_cle_restricted,
        ))
        .LimitOncePerPhase(),
    ]
