from . import *

# * Venom (Eddie Brock) — custom « Rainy »
# Hunger — Response: After you defeat an enemy, heal 1 damage from Venom.
#
# ⚠ DEFAUT CONNU (5/8/2026, NON corrige) : Hunger ne repond jamais. Constate en
# achevant un sbire de 2 PV a l'attaque de base — le journal montre bien
# « was defeated by Venom », mais aucun soin. Quatre pistes ecartees :
#   - `GetControlBy()` remplace par `GetControlByPlayer()` : sans effet ;
#   - bascule sur `AfterUnitDefeatedUnit`, la fabrique prevue pour « apres que
#     VOUS ayez vaincu un ennemi », avec `who_killer` a « You » puis « This » ;
#   - ajout du `SetTarget("This", canbe_heal=True)` du modele officiel Tigra
#     01051, au cas ou la Response soit filtree faute de cible legale.
# Aucune ne declenche. A verifier en partie reelle.
# Symbiotic Bond — Resource: Take 1 damage -> generate a [wild] resource.
#   (Limit once per phase.)

def GetAbilities() -> Sequence['Ability']:

    def hunger(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        this = effect.this.CastTo(Hero)
        this.HealthUnits([this], 1, effect)

    def vaincu_par_moi(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> bool:
        return message.GetDefeatingPlayer() == effect.this.GetControlBy()

    def symbiotic_bond_cost(targets: Sequence['CardFace'], effect: 'Effect') -> bool:
        this = effect.this
        this.TakeDamage(this, 1, effect)
        return True

    return [
        AbilityFactory.WhenUnitBeDefeated(
            AbilityType.Response,
            Enemy,
            hunger,
            has_defeating_player=True,
            conditions=[vaincu_par_moi],
        ).SetName("Hunger"),

        AbilityFactory.CanGenerateResources(
            AbilityType.HeroResource,
            Resources("G"),
        ).SetName("Symbiotic Bond")
        .SetCostFunc(CostFunc.Custom(None, symbiotic_bond_cost))
        .LimitOncePerPhase(),
    ]
