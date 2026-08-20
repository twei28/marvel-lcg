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
        #
        # ⚠ C'EST UNE REPONSE, PAS UNE ACTION. `PlayerActionToDiscardThis` est
        # un `WhenInYourPlayTurn` : sans declencheur, le joueur defaussait les
        # lunettes quand il voulait pour 1 [energy], sans jamais avoir frappe
        # Vulture. La fenetre du texte est l'attaque QUI A BLESSE.
        AbilityFactory.AfterUnitAttackAndDamageUnit(
            AbilityType.HeroResponse,
            "YourIdentity",
            "AttachedVillain",
            lambda effect, message: Faces.DiscardAll([effect.this], effect),
        ).SetCost(Cost("Y")),
    ]
