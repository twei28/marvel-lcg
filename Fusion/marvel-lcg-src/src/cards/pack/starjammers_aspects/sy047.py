from . import *
# Reckless Defense (Protection, evenement 0 [physical]). DEFENSE.
# Hero Interrupt (defense): When a character would take damage from an attack, discard the top card of the encounter deck. Deal 1 damage to
# your identity for each icon ([star] and [boost]) in that card's boost area → prevent all damage from that attack.
#
# Cartes de reference : 01003 Backflip (`WhenUnitWouldTakeDamage(Interrupt, who, op, is_from_attack=True).SetPlay().SetLabel('defense')` +
# `message.PreventDamage("All", effect)`) ; sy022 (cout `CoutImprudent`, RR Cost : prevention partielle = cout non paye = rien n'est prevenu).
# « a CHARACTER » : tout personnage ami (allie ou identite), pas seulement vous ; « Hero Interrupt » : forme heros.
def GetAbilities() -> Sequence['Ability']:
    def reckless_defense(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        this = effect.this.CastTo(Event)
        if CoutImprudent(effect, this):
            message.PreventDamage("All", effect)
    return [
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.HeroInterrupt,
            Friend,
            reckless_defense,
            is_from_attack=True,
        ).SetPlay().SetLabel('defense'),
    ]
