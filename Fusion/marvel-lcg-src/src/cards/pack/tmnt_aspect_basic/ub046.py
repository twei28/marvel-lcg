from . import *

# Shuriken — AMELIORATION 2 [energy], aspect Basic (TMNT Aspects, Inkwire). NINJA. WEAPON.
# Attach to a friendly character. Max 1 per character.
# Hero Action: Exhaust this card and discard 1 card from your hand → deal 1 damage to up to 3 enemies.
#
# NOUVELLE. Cartes de reference :
#  - « Attach to a friendly character. Max 1 per character » : 31029 Clarity of Purpose,
#    `CanPlayThisUpgradeCard(Friend)` ; « Max 1 per character » = `desc.MaxPerUnit`.
#  - cout « exhaust this and discard 1 card from your hand » : `CostFunc.Exhaust("This")` +
#    `CostFunc.Discard("YourHandCards", range=(1, 1))` (ar010).
#  - « deal N damage to up to 3 enemies » : 10005 Thunderclap, `SetTarget(Enemy, range=(1, 3))`.
# TEXTE CONTRE CODE : « Hero Action » (forme heros) ; « up to 3 » (1 a 3, distincts : un ennemi n'est
#   choisi qu'une fois) ; « 1 damage » chacun ; le cout se paie AVANT.


def GetAbilities() -> Sequence['Ability']:

    def shuriken(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        this.DealDamage(effect.targets, 1, effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(Friend),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            shuriken
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetCostFunc(CostFunc.Discard("YourHandCards", range=(1, 1)))
        .SetTarget(Enemy, range=(1, 3)),
    ]
