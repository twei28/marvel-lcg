from . import *

# * The World Eater (sbire nemesis de Silver Surfer) — PV 5, AUCUNE valeur d'ATK ni de SCH imprimee. COSMIC. ELITE.
# Galactus cannot take damage and his attacks gain overkill.
# When Defeated: Remove The World Eater from the game.
#
# Cartes de reference :
#  - `01136` Ultron / `01181` Madame Hydra : « X cannot take damage while Y » ; ici l'immunite est posee sur
#    une AUTRE carte (Galactus) par `*AbilityFactory.UnitCannotTakeDamage(finder)` (damage.py, correctif du
#    30/08/2026 : rend une LISTE, deballage `*`).
#  - `yd016` Sword-Gun-Arm : `UnitAttackGainKeyword(..., overkill=True)` pour « attacks gain overkill ».
#  - `04130` The Sleeper : « When Defeated: Remove X from the game ».
#  - `51038` (bp) : `EnemyCannotActivate` pour un sbire qui ne s'active pas.
#
# ⚠ Mots-pieges :
#  - ARBITRAGE UTILISATEUR (24/10/2026, question posee avec le scan) : aucune valeur d'ATK/SCH imprimee -> le
#    sbire NE S'ACTIVE PAS DU TOUT (ni attaque, ni manigance, pas de carte boost). `desc` porte ATK 0 / SCH 0
#    pour le moteur, l'activation est interdite par `EnemyCannotActivate`.
#  - « Galactus » = la carte nommee, quel que soit le porteur ; l'effet dure tant que The World Eater est EN JEU.
#  - « his attacks gain overkill » : toutes les attaques de Galactus, pas seulement les attaques de base.


def GetAbilities() -> Sequence['Ability']:

    def mangeur_vaincu(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        this = effect.this.CastTo(Minion)
        Unused(message)

        Faces.RemoveAllFromGame([this], effect)

    galactus = CardFinder(name=NOM_GALACTUS, card_type=Minion)

    return [
        *AbilityFactory.UnitCannotTakeDamage(galactus),
        AbilityFactory.UnitAttackGainKeyword(galactus, overkill=True),
        AbilityFactory.EnemyCannotActivate(AbilityType.NonKeyword, "This"),
        AbilityFactory.WhenUnitBeDefeated(
            AbilityType.WhenDefeated,
            "This",
            mangeur_vaincu,
        ),
    ]
