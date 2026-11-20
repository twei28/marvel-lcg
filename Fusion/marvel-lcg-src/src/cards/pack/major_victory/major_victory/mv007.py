from . import *

# Telekinetic Throw — EVENEMENT, cout 1, [mental]. PSIONIC.
# Hero Interrupt: When you deal damage from your "Shield Toss" ability, exhaust Major Victory →
#   deal 4 damage to an enemy and deal 4 damage to an enemy.
#
# CARTES DE REFERENCE
#  - `sf006` Atomic Samurai : `WhenUnitWouldTakeDamage` filtre sur la SOURCE des degats (`message.by_effect`).
#  - `mv001a` : la capacite « Shield Toss » dont on lit le nom.
#
# ARBITRAGE UTILISATEUR (30/10/2026) : « deal 4 damage to an enemy and deal 4 damage to an enemy » = DEUX CHOIX INDEPENDANTS
# (lecture standard des regles) : chaque phrase choisit son ennemi, qui peut etre le meme (8 degats au total). La liste des
# ennemis est relue avant le second choix : un ennemi vaincu par le premier coup n'est plus eligible.
#
# TEXTE CONTRE CODE
#  « when YOU deal damage » -> `par.GetInitiator() == effect.GetInitiator()` : seulement les degats de TA capacite.
#  « from your "Shield Toss" ability » -> nom de la capacite (`DegatsDeShieldToss`), pas le nom de la carte.
#  « exhaust Major Victory » -> `CostFunc.Exhaust("YourIdentity")` (modele `cards/test_001`).
#  Les degats de Telekinetic Throw ne portent pas le nom « Shield Toss » : pas de boucle.


def GetAbilities() -> Sequence['Ability']:

    def telekinetic_throw(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        this = effect.this.CastTo(Event)
        joueur = effect.GetInitiator()
        if joueur is None:
            return
        for _ in range(2):
            cible = ChoisirUne(joueur, Worlds.GetOnFieldEnemies(effect), effect, "Telekinetic Throw : deal 4 damage to an enemy")
            if cible is not None:
                this.DealDamage([cible], 4, effect)

    return [
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.HeroInterrupt,
            None,
            telekinetic_throw,
            conditions=[DegatsDeShieldToss],
        ).SetPlay(hero_form_only=True)
        .SetCostFunc(CostFunc.Exhaust("YourIdentity")),
    ]
