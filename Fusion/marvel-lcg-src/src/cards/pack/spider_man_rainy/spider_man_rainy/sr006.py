from . import *

# Webbed Up — custom « Rainy »
# Hero Action: Choose an enemy and web them up to 3 times.
# Hero Interrupt (defense): When an identity would take damage from an
#   attack, prevent all of that damage.
#
# « up to 3 times » : on pose les 3 compteurs d'un coup (le plafond de 3 par
# ennemi s'applique) ; en poser moins n'est jamais un avantage, le retrait a
# l'activation etant de toute facon integral.

def GetAbilities() -> Sequence['Ability']:

    def toiles(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)
        Weber(effect.targets, 3, effect)

    def prevention(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)
        message.PreventDamage("All", effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            toiles
        ).SetPlay(hero_form_only=True)
        .SetTarget(Enemy),

        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.HeroInterrupt,
            Identity,
            prevention,
            is_from_attack=True,
        ).SetPlay(hero_form_only=True)
        .SetLabel('defense'),
    ]
