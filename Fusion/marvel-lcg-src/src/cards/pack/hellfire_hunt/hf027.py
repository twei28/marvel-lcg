from . import *

# * Sebastian Shaw : allie RECRUITED, cout 3, PV 6, THW 1*, ATK 2**. [star] Interrupt.
# Response: After Sebastian Shaw is damaged, place an equal amount of energy counters here.
# [star] Interrupt: When Sebastian Shaw thwarts, remove each energy counter from him -> for each counter discarded this way, he gets
# +1 THW for this thwart.
#
# Cartes de reference : `AfterUnitTookDamage` (damage.py ; `message.took_damage`), `Faces.PlaceCountersOn` / `Faces.RemoveCountersOn`
# (faces.py:213-227), `message.GainTHWForThisThwart` (sender_friend.py:69).
# ⚠ « each energy counter » : tous, d'un coup ; le bonus ne vaut que pour CETTE contrariete.
def GetAbilities() -> Sequence['Ability']:
    def shaw_degats(effect: 'Effect', message: 'Message.AfterUnitTookDamage') -> None:
        this = effect.this.CastTo(Ally)
        if message.took_damage > 0:
            Faces.PlaceCountersOn([this], message.took_damage, 'energy', effect)

    def shaw_contre(effect: 'Effect', message: 'Message.WhenUnitWouldThwart') -> None:
        this = effect.this.CastTo(Ally)
        nombre = this.GetCounters('energy')
        if nombre > 0:
            Faces.RemoveCountersOn([this], "All", 'energy', effect)
            message.GainTHWForThisThwart(nombre, effect)

    return [
        AbilityFactory.AfterUnitTookDamage(
            AbilityType.Response,
            "This",
            shaw_degats,
        ),
        AbilityFactory.WhenUnitMakeThwart(
            AbilityType.Interrupt,
            "This",
            Scheme2,
            shaw_contre,
        ),
    ]
