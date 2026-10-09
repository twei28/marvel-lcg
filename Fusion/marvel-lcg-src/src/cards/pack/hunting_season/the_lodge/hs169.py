from . import *

# hs169 Evade (Experience Cost 2)
# Interrupt : quand tu subirais des degats d'une attaque, en prevenir 3.
# Si tu ne subis aucun degat de cette attaque, pioche 1 carte.

def GetAbilities() -> Sequence['Ability']:

    def esquiver(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        message.PreventDamage(3, effect)
        if message.will_take_damage == 0:
            effect.GetInitiator().DrawUp(1, effect)

    return [
        AbilityFactory.WhenUnitWouldTakeDamage(AbilityType.Interrupt, "You", esquiver, is_from_attack=True).SetPlay(),
    ]
