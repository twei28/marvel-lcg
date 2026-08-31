from . import *

# Eat Them All! — amelioration. SYMBIOTE. Cout 2.
# Hero Response: After Venompool attacks, heal 1 damage from him.
#   (Limit once per phase.)
#
# Cartes de reference : 04001b Clint Barton pour `.LimitOncePerPhase()`,
# 44008 Chimichanga Truck (pack deadpool) pour le montage « Response apres
# une action de l'identite portee par une carte attachee ».
#
# ⚠ « attacks » TOUT COURT, pas « makes a basic attack » : la carte vp010
# True Form, dans le MEME pack, ecrit explicitement « makes a basic attack ».
# Le contraste est voulu par l'auteur, donc `is_basic_attack` reste None ici
# (n'importe quelle attaque, y compris celle d'un evenement du pack) et vaut
# True sur vp010.

def GetAbilities() -> Sequence['Ability']:

    def eat_them_all(effect: 'Effect', message: 'Message.AfterUnitAttackUnit') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(message)

        identity = GetVenompool(effect)
        if identity is not None:
            this.HealthUnits([identity], 1, effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.AfterUnitAttackUnit(
            AbilityType.HeroResponse,
            "YourHero",
            Enemy,
            eat_them_all,
        ).LimitOncePerPhase(),
    ]
