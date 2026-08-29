from . import *

# Animal Instinct
# Hero Interrupt: When Wolverine makes a basic thwart, she gets +X THW for
#   this thwart, where X is equal to her ATK.
#
# Copie d'Animal Instinct (43004). Le declencheur est cherche par nom, donc
# borne au controleur (cf. __init__.py) : sinon un Wolverine officiel a la
# table declencherait cette carte.


def GetAbilities() -> Sequence['Ability']:

    def animal_instinct(effect: 'Effect', message: 'Message.WhenUnitWouldThwart') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)

        value = message.trigger.CastTo(HasAttack).attack
        message.GainTHWForThisThwart(value, effect)

    return [
        AbilityFactory.WhenUnitMakeThwart(
            AbilityType.HeroInterrupt,
            CardFinder(name=NOM_HEROS, check_effect_fn=EstTonHeros),
            None,
            animal_instinct,
            is_basic_thwart=True
        ).SetPlay().SetLabel(),
    ]
