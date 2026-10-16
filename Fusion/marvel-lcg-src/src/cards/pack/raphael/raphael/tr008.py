from . import *

# * Shell Cycle — SOUTIEN, cout 1, [physical]. NYC. VEHICLE. UNIQUE.
# Hero Action: Exhaust Shell Cycle and spend 2 resources of any type -> ready
#   your hero. If you paid for this ability using [physical][physical]
#   resources, you get +1 THW until the end of the round.
#
# Valide en jeu : cas `tools/cas/tmnt_raphael.py` (voir .planning/todos/2026-10-16-raphael-gabarits-processus-carte.md).
#
# CARTES DE REFERENCE
#  - `01093` Tenacity / `44030` Stick-To-Itiveness : « spend a resource -> ready
#    your hero » = `SetCost(Cost(...))` + `Faces.ReadyAll([hero], effect)`.
#  - `sf008` Sunfire's Suit : « Exhaust X and spend N resources of any type » =
#    `.SetCostFunc(CostFunc.Exhaust("This")).SetCost(Cost("N"))` ; le litteral
#    `Cost("2")` ne demande qu'un NOMBRE, pas une couleur (`Cost("*")` n'existe
#    pas).
#  - `bw008` Heavy Lifting : `effect.GetPaidResources().GetColor("R")` compte
#    les ressources physiques payees ; `hero.GainUntilRoundEnd(effect, ...)`.
#  - `42018` / `26004` : un SOUTIEN a Action = `WhenInYourPlayTurn(HeroAction)`.
#
# TEXTE CONTRE CODE
#  ⚠ « Exhaust Shell Cycle AND spend 2 resources » : DEUX couts, tous deux
#    avant la fleche.
#  ⚠ « 2 resources of ANY type » -> `Cost("2")` ; la couleur ne contraint rien.
#  ⚠ « paid for THIS ABILITY using [physical][physical] » (les DEUX physiques,
#    `GetColor("R") >= 2`), et non « a physical resource ». Mot-piege releve :
#    ce n'est pas la carte qui est payee mais l'ABILITE.
#    A VERIFIER en phase C : `effect.GetPaidResources()` est-il renseigne pour
#    un cout d'ABILITE `Cost("2")` (et pas seulement pour une carte jouee) ?
#    Les compteurs de rage depenses comme [physical] comptent (tr001a).
#  ⚠ « YOU get +1 THW » -> « you » = l'identite ; une Hero Action impose la
#    forme heros, donc on donne le bonus au HEROS (`GainUntilRoundEnd`).
#  ⚠ « ready YOUR HERO » : `ReadyAll([heros])`, et le heros peut deja etre
#    redresse (la carte reste jouable, comme Tenacity).
#  ⚠ Carte UNIQUE (« * ») : le deck n'en porte qu'un exemplaire.


def GetAbilities() -> Sequence['Ability']:

    def cycle(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        Unused(this, message)

        heros = HerosDuJoueur(effect)
        if heros is None:
            return
        Faces.ReadyAll([heros], effect)

        if effect.GetPaidResources().GetColor("R") >= 2:
            heros.GainUntilRoundEnd(effect, thwart=1)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            cycle,
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetCost(Cost("2")),
    ]
