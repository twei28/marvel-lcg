from . import *

# Aviator Goggles

def GetAbilities() -> Sequence['Ability']:

    def revelation(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        # « Attach to Vulture and place 2 pigeon counters on the main scheme. »
        PigeonsSurLeComplot(effect, 2)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(
            Villain
        ),
        AbilityFactory.WhenThisRevealed(
            None,
            revelation
        ),
        # « Vulture gains steady. »
        *AbilityFactory.GiveKeywordToAttached(
            steady=1,
        ),
        # « Hero Response: After you attack and damage Vulture, spend an
        # [energy] resource → discard Aviator Goggles. »
        AbilityFactory.PlayerActionToDiscardThis(
            AbilityType.HeroResponse,
        ).SetCost(Cost("Y")),
    ]
