from . import *

# * X-S Sentinel II — sbire. EARTH-6160. SENTINEL. PV 7, ATK 1★, SCH 1★, boost 3. QUICKSTRIKE. VILLAINOUS.
# [star] Forced Response: After X-S Sentinel II activates, heal 3 damage from X-S Sentinel II.
#
# Cartes de reference : Quickstrike et Villainous sont NATIFS (`desc`, fiches mots-cles/quickstrike.md et villainous.md,
# aucun script) ; `ap005a` / `AfterEnemyActivationEnd(ForcedResponse, ...)` pour « after X activates » ;
# `35001a` (`this.HealthUnits`). Les ★ sur ATK et SCH sont des marques d'impression (la valeur est 1 et 1).
#
# Mots-pieges : « activates » (attaque OU manigance) ; « heal 3 damage FROM X-S Sentinel II » (lui-meme) ; une activation
# remplacee par un statut Sonne n'envoie pas ce message (RECETTES §25) : elle ne soigne pas.


def GetAbilities() -> Sequence['Ability']:

    def regeneration(effect: 'Effect', message: 'Message.AfterEnemyActivationEnd') -> None:
        this = effect.this.CastTo(Minion)
        this.HealthUnits([this], 3, effect)

    return [
        AbilityFactory.AfterEnemyActivationEnd(
            AbilityType.ForcedResponse,
            "This",
            regeneration,
        ),
    ]
