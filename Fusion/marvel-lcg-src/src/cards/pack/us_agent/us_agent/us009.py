from . import *

# * Solid Gear — amelioration unique, cout 2, ressource [physical]. ARMOR. (version « _REV » du zip : la revisee.)
# Hero Interrupt: When an enemy initiates an attack, exhaust Solid Gear → reduce the resource cost of the next
# Protection (green) card you play this phase by 2.
#
# Cartes de reference :
#  - `19018` Subdue : « When an enemy initiates an attack » = `WhenUnitWouldAttack(HeroInterrupt, Enemy, op)` (n'importe quelle
#    attaque d'un ennemi, contre qui que ce soit).
#  - `01092` Helicarrier, `dz003`, `ch007` : « reduce the cost of the next card you play this phase » =
#    `Worlds.UpdateNextCardPlayCost(joueur, -N, effect, finder=CardFinder(...), in_this="Phase")` (RECETTES §6).
#
# ⚠ Mots-pieges :
#  - « the next PROTECTION card » : la CLASSE Protection (`CardFinder(card_classes=["Protection"])`), tous types de cartes
#    (evenement, amelioration, allie...) ; les Basic et les autres aspects ne profitent de rien.
#  - « THIS PHASE » : `in_this="Phase"`, pas « Round » ni « Turn » : l'interruption part pendant la phase du vilain, la
#    reduction vaut jusqu'a la fin de CETTE phase (RECETTES : « Phase tombe a la fin de la phase des joueurs »).
#  - « by 2 » : valeur NEGATIVE (-2) ; la fabrique ne descend pas sous 0.
#  - « exhaust Solid Gear → » : cout d'inclinaison ; sans exhaust possible, pas de capacite.


def GetAbilities() -> Sequence['Ability']:

    def solid_gear(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this, message)

        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return
        Worlds.UpdateNextCardPlayCost(
            joueur, -2, effect,
            finder=CardFinder(card_classes=["Protection"]),  # type: ignore
            in_this="Phase",
        )

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.WhenUnitWouldAttack(
            AbilityType.HeroInterrupt,
            Enemy,
            solid_gear,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
