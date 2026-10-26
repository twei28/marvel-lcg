from . import *

# Illusion Unraveled. Attachement SKILL. « Attach to the villain. Forced Interrupt : When an ILLUSION attachment is discarded, give that card to the
# villain as a facedown boost card. Discard this card. » Cartes de reference : 56091 Dangerous Recruits / 49042 (`villain.GiveBoostCard(face, effect)`),
# 04075 (`AttachToFaceWhenPutIntoPlay(Villain)`).


def GetAbilities() -> Sequence['Ability']:
    def defaussee(effect: 'Effect', message: 'Message.WhenCardWouldDiscard') -> None:
        this = effect.this
        villain = Worlds.FindVillain(effect)
        if villain is not None:
            message.SetBeInstead(effect)
            villain.GiveBoostCard(message.trigger, effect)
            Faces.DiscardAll([this], effect)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(Villain),
        AbilityFactory.WhenCardWouldDiscard(AbilityType.ForcedInterrupt, CardFinder(card_type=Attachment, trait=ILLUSION), defaussee),
    ]
