from . import *

# * Bloodmoon Battleaxe — amelioration signature, x1 (14/15). WEAPON.
# Restricted. Cout 2, ressource [Y].
# Response: After you play an event, exhaust Bloodmoon Battleaxe -> deal 2
# damage to an enemy.
#
# CARTE DE REFERENCE : `AbilityFactory.AfterPlayerPlayedCard(AbilityType,
# "You", Event, operation)` (play.py:333). « Restricted » lu directement
# dans `desc` (base automatique, PROCESSUS-CARTE etape 5).
#
# TEXTE CONTRE CODE : « Response » (pas « Hero Response ») : vit sur une
# amelioration DEJA EN JEU, active quelle que soit la forme -- comme `rs002`
# Conan.

def GetAbilities() -> Sequence['Ability']:

    def bloodmoon_battleaxe(effect: 'Effect', message: 'Message.AfterPlayerPlayedCard') -> None:
        this = effect.this.CastTo(Upgrade)
        this.DealDamage(effect.targets, 2, effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.AfterPlayerPlayedCard(
            AbilityType.Response,
            "You",
            Event,
            bloodmoon_battleaxe,
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetTarget(Enemy),
    ]
