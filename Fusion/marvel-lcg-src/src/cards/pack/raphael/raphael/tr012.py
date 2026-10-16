from . import *

# * Raphael's Other Sai — AMELIORATION, cout 1, [physical]. NINJA. SAI. WEAPON.
# UNIQUE. Restricted.
# Each [[SAI]] upgrade you control gains: "Hero Response: After Raphael defeats
#   an enemy, exhaust this card -> draw 1 card."
#
# Valide en jeu : cas `tools/cas/tmnt_raphael.py` (voir .planning/todos/2026-10-16-raphael-gabarits-processus-carte.md).
#
# MOTS-CLES : RESTRICTED — `docs/reference/mots-cles/restricted.md` (base
# automatique, `desc.Restricted = "1"`, aucun script).
#
# CARTES DE REFERENCE
#  - `59017` Prince of Power / `04160b` : « After you/Raphael defeats an enemy,
#    exhaust this card -> ... » = `AfterUnitDefeatedUnit(HeroResponse,
#    "YourHero"|"You", Enemy|Minion, op).SetCostFunc(CostFunc.Exhaust("This"))`
#    sur une AMELIORATION (`CanPlayThisUpgradeCard()`).
#  - Voir `tr011` et l'en-tete du __init__ pour le « gains » (aucun modele
#    moteur pour des cartes joueur).
#
# TEXTE CONTRE CODE
#  ⚠ « After RAPHAEL defeats AN ENEMY » : tout ennemi (vilain OU sbire), par le
#    HEROS, attaque ou non : pas de `is_from_attack`, type `Enemy` (pas
#    `Minion`).
#  ⚠ « exhaust THIS card -> draw 1 card » : l'inclinaison est le cout, la
#    pioche suit. Une Sai inclinee (par exemple entree en jeu epuisee via
#    `tr001b`, ou ayant servi a attaquer) ne peut pas repondre.
#  ⚠ « EACH SAI upgrade » : la Reponse existe aussi sur `tr011`, sous la
#    condition « `tr012` en jeu ». Encart : on peut utiliser l'une OU les deux
#    Sai pour un meme ennemi vaincu.
#  ⚠ RECETTES §1 : `AfterUnitDefeatedUnit` + limite est INERTE si on y colle
#    `LimitOncePerRound` ; ICI aucune limite imprimee, l'inclinaison borne.
#  Aucune limite imprimee, donc pas de temoin d'epuisement de limite (le
#    cout d'inclinaison, lui, doit etre mesure en phase C).


def GetAbilities() -> Sequence['Ability']:

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        CapaciteAttaqueSai(),
        CapaciteReponseSai(),
    ]
