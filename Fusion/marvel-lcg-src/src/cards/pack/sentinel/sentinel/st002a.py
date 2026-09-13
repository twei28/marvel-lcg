from . import *

# * Head (Intact) — COMPONENT. INTACT. TECH.
# Permanent. Setup.
# Hero Action: Exhaust Head (Intact) → expose 2 enemies.
#
# Cartes de reference :
#  - `nt003a` Battle Board : l'amelioration PERMANENTE recto-verso posee par
#    `desc.Setup`. Aucun script pour « Permanent. » ni pour « Setup. », les
#    deux sont des bases automatiques lues dans `desc`.
#  - `av009` Bear Arms / `09009` Cloak of Levitation : l'action de heros d'une
#    amelioration, `WhenInYourPlayTurn` + `CostFunc.Exhaust("This")`.
#  - `dz037` Coolest Team-Up Ever! : la fourchette de cibles multiples.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « expose 2 enemies » n'est PAS « up to 2 » : le joueur doit en prendre
#    deux s'il y en a deux. `range=("Zero", 2)` dit exactement cela — le
#    minimum vaut le nombre de cibles legales, plafonne au maximum
#    (selector.py:103). Avec un seul ennemi sur la table, la carte reste
#    jouable et expose ce seul ennemi.
#  - « enemies » : vilain ET sbires, donc `Enemy`, pas `Minion`.
#  - EXPOSER n'est pas un mot-cle du moteur : c'est poser la carte d'etat
#    maison Exposed (fiche docs/reference/mots-cles/exposed.md), par
#    `Exposer()` du pack.


def GetAbilities() -> Sequence['Ability']:

    def scanner(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this, message)

        Exposer(effect.targets, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            scanner,
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetTarget(Enemy, range=("Zero", 2)),
    ]
