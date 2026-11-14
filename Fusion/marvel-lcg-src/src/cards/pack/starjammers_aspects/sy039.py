from . import *
# Targeting Station (Leadership, soutien 2 [mental]). LOCATION. TECH. WEAPON. Uses (3 ammo counters).
# Action: Exhaust a character you control and remove 1 ammo counter from this card → deal 3 damage to an enemy.
#
# Cartes de reference : us007 / 04064 (`desc.Uses "N,ammo"` + `CostFunc.Counter("This", 1, 'ammo')`) ; rl006 (`CostFunc.Exhaust(.., from_where=
# ["YouControlCards"])`) ; fiche uses.md (le dernier compteur retire defausse la carte).
# « a character YOU control » : identite ou allie ; le cout ne peut pas viser le soutien lui-meme (pas un personnage).
def GetAbilities() -> Sequence['Ability']:
    def targeting_station(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        Unused(message)
        this.DealDamage(effect.targets, 3, effect)
    return [
        AbilityFactory.CanPlayThisSupportCard(),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            targeting_station,
        ).SetCostFunc(CostFunc.Exhaust(card_type=Friend, from_where=["YouControlCards"]))
        .SetCostFunc(CostFunc.Counter("This", 1, 'ammo'))
        .SetTarget(Enemy),
    ]
