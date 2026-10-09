from . import *

# hs032 * Scorpion

def GetAbilities() -> Sequence['Ability']:

    def laser(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        Find.FindAndReveal(
            effect, message.GetToPlayer(),
            finder=CardFinder(name="Tail Laser", card_type=Attachment,
                              check_face_fn=lambda f: not f.IsInPlay()),
        )

    return [
        AbilityFactory.UnitCannotBeStunned("This"),
        AbilityFactory.WhenThisRevealed(None, laser),
        ForcedInterruptQueue(),
    ]
