from . import *

# Lightning Speed

def GetAbilities() -> Sequence['Ability']:

    def clone(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        # « Forced Response: After a copy of Electro enters play, place an
        # acceleration token here. » Chaque clone qui arrive accelere la partie.
        JetonDAccelerationIci(effect)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(
            Villain
        ),
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.ForcedResponse,
            CardFinder(name="Electro"),
            clone
        ),
        AbilityFactory.PlayerActionToDiscardThis(
            AbilityType.HeroAction,
            ex_operation=lambda effect, message: Faces.DiscardAll(
                Worlds.GetEncounterDeckCards(effect), effect),
        ),
    ]
