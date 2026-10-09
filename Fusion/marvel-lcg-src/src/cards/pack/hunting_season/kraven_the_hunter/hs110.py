from . import *
from weakref import WeakKeyDictionary

# hs110 * Chameleon
# Ne peut pas subir de degats ; ses attaques deviennent des complots.
# Forced Interrupt : quand un ennemi serait vaincu, defausse Chameleon a la place. FAQ : l'ennemi recupere les degats de cette instance seulement.

_dernier_coup: 'WeakKeyDictionary[CardFace, int]' = WeakKeyDictionary()

def GetAbilities() -> Sequence['Ability']:
    def scheme_instead(effect, message):
        message.DoSchemeInstead(effect)

    def noter_coup(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        if message.trigger is not effect.this:
            _dernier_coup[message.trigger] = message.will_take_damage

    def remplacer(effect: 'Effect', message: 'Message.WhenUnitWouldBeDefeated') -> None:
        ennemi = message.trigger
        message.SetBeInstead(effect)
        instance = _dernier_coup.pop(ennemi, None)
        if instance is None:
            instance = max(1 - ennemi.health, 0)
        if instance > 0:
            ennemi.HealHealth(instance, effect)
        Faces.DiscardAll([effect.this], effect)

    def autre_ennemi(effect: 'Effect', message: 'Message.WhenUnitWouldBeDefeated') -> bool:
        return message.trigger is not effect.this

    return [AbilityFactory.UnitCannotTakeDamageWhile(AbilityType.NonKeyword, "This"),
            AbilityFactory.WhenUnitWouldAttack(AbilityType.ForcedInterrupt,
                                               "This", scheme_instead),
            AbilityFactory.WhenUnitWouldTakeDamage(AbilityType.NonKeyword, Enemy, noter_coup),
            AbilityFactory.WhenUnitWouldBeDefeated(AbilityType.ForcedInterrupt, Enemy, remplacer, conditions=[autre_ennemi])]
