from . import *
# Reckless Charge (Leadership, evenement 2 [physical]). TACTIC.
# Hero Action: Discard the top card of the encounter deck. Deal 1 damage to your identity for each icon ([star] and [boost]) in that card's
# boost area → ready up to 3 characters.
#
# Cartes de reference : sy022 Reckless Attack (cout `CoutImprudent`) ; 42031 Flying Formation (« ready up to 3 characters » :
# `SetTarget(Unit2, range=(0, 3), canbe_ready=True)` + `Faces.ReadyAll`).
# ⚠ « up to 3 » : 0 a 3 cibles (le minimum 0 est ici imprime). « characters » : heros, allies (le pilote du harnais prend le minimum).
def GetAbilities() -> Sequence['Ability']:
    def reckless_charge(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)
        if not CoutImprudent(effect, this):
            return
        Faces.ReadyAll(effect.targets, effect)
    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            reckless_charge,
        ).SetPlay().SetLabel()
        .SetTarget(Friend, range=(0, 3), canbe_ready=True),
    ]
