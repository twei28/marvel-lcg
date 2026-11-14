from . import *
# Reckless Maneuver (Justice, evenement 1 [physical]). THWART.
# Hero Action (thwart): Discard the top card of the encounter deck. Deal 1 damage to your identity for each icon ([star] and [boost]) in
# that card's boost area → remove 4 threat from a scheme.
#
# Cartes de reference : sy022 Reckless Attack (meme cout, helper `CoutImprudent`) ; us004 Reckless ; gam/18020 Hit and Run
# (`SetPlay().SetLabel(..).SetTarget(Scheme2)` + `RemoveThreatFromSchemes`).
def GetAbilities() -> Sequence['Ability']:
    def reckless_maneuver(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)
        if not CoutImprudent(effect, this):
            return
        this.RemoveThreatFromSchemes(effect.targets, 4, effect)
    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            reckless_maneuver,
        ).SetPlay().SetLabel('thwart')
        .SetTarget(Scheme2),
    ]
