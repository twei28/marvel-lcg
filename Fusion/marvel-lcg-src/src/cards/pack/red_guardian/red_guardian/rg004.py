from . import *

# Shield Block
# Play only if Red Guardian's Shield is in your hand.
# Interrupt (defense): When you would take any amount of damage, prevent all of
#   that damage.
#
# Meme texte que le Shield Block de Captain America (03005), au cout d'entree
# pres : la carte officielle exige d'epuiser le bouclier EN JEU, celle-ci exige
# de l'avoir EN MAIN. On reprend donc son squelette exact.
#
# Pas de `is_from_attack` : le texte dit « any amount of damage », sans
# restreindre a une attaque — comme 03005, et contrairement a Backflip (01003).


def GetAbilities() -> Sequence['Ability']:

    def shield_block(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)

        message.PreventDamage("All", effect)

    return [
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.Interrupt,
            "You",
            shield_block,
            conditions=[BouclierEstEnMain],
        ).SetPlay().SetLabel('defense'),
    ]
