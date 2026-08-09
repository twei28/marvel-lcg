from . import *

# Inhuman's Best Friend — custom « Nugget » (carte d'aspect BASIC)
# Team-Up (Lockjaw and Ms. Marvel). Max 1 per deck.
# Alter-Ego Action: Ready up to 4 supports you control.


def GetAbilities() -> Sequence['Ability']:

    def redresser(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)
        Faces.ReadyAll(effect.targets, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            redresser,
        ).SetPlay()
        .SetTarget(Support, range=(0, 4), canbe_ready=True),
    ]
