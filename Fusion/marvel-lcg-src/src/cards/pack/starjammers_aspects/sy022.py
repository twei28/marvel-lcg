from . import *
# Reckless Attack (Aggression, evenement 1 [physical]). ATTACK.
# Hero Action (attack): Discard the top card of the encounter deck. Deal 1 damage to your identity for each icon ([star] and [boost]) in
# that card's boost area → deal 4 damage to an enemy.
#
# Cartes de reference : us004 Reckless (« Take X damage → remove X threat and deal X damage » : le cout « degats subis » ecrit DANS
# l'operation, RR Cost « not considered paid unless all of that damage was taken ») ; gam/18020 Hit and Run (`SetPlay().SetLabel(..).SetTarget(Enemy)`) ;
# RECETTES §3 (`CountTotalBoostStarAndBoost` : « each icon ([star] and [boost]) »).
# ⚠ Le cout (defausse + degats a l'identite) est PAYE AVANT les 4 degats, dans `CoutImprudent` (helper du pack).
def GetAbilities() -> Sequence['Ability']:
    def reckless_attack(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)
        if not CoutImprudent(effect, this):
            return
        this.DealDamage(effect.targets, 4, effect)
    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            reckless_attack,
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy),
    ]
