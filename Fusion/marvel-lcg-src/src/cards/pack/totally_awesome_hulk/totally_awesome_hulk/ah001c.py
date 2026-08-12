from . import *

# * Uncontrollable Hulk — custom « DesignHacker »
# Uncontrollable — You cannot change to or from this form without resolving the
#   effects of "The Trunk" support.
# Interrupt: When you attack, that attack deals 2 additional damage.


def GetAbilities() -> Sequence['Ability']:

    def uncontrollable(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        message.GainATKForThisAttack(2, effect)

    return [
        # « Uncontrollable » : on ne quitte pas cette forme autrement que par
        # « The Trunk » (l'entrée dans la forme est déjà verrouillée par
        # « Losing Control », face ah001a).
        AbilityFactory.PlayersCannotChangeForms(
            AbilityType.NonKeyword,
            "You",
            from_form=Hero,
            conditions=[
                lambda effect, message:
                    not CardFinder(name=TRUNK_NAME).Check(message.by_effect.this)
            ],
        ).SetName("Uncontrollable"),
        AbilityFactory.WhenUnitMakeAttack(
            AbilityType.Interrupt,
            "This",
            uncontrollable,
        ),
    ]
