from . import *

# Greased Lightning

def GetAbilities() -> Sequence['Ability']:

    def complot(effect: 'Effect', message: 'Message.AfterEnemySchemeAndPlaceThreat') -> None:
        # « Forced Response: After the villain schemes, place an acceleration
        # token here. »
        JetonDAccelerationIci(effect)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(
            Villain
        ),
        AbilityFactory.AfterEnemySchemeAndPlaceThreat(
            AbilityType.ForcedResponse,
            "AttachedVillain",
            MainScheme,
            complot
        ),
        # « Hero Action: Discard each card from the encounter deck → discard
        # this card. » Le cout est le deck rencontre tout entier : la carte se
        # paie en cartes, pas en ressources.
        AbilityFactory.PlayerActionToDiscardThis(
            AbilityType.HeroAction,
            ex_operation=lambda effect, message: Faces.DiscardAll(
                Worlds.GetEncounterDeckCards(effect), effect),
        ),
    ]
