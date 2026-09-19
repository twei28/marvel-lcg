from . import *

# Art Museum Heist (COMPLETED) — Setup: Give each identity a tough status card.

def GetAbilities() -> Sequence['Ability']:

    def mise_en_place(effect: 'Effect', message: 'Message.WhenGameWouldBegin') -> None:
        identites = [p.GetIdentity() for p in Worlds.GetPlayers(effect)]
        Faces.GiveStatus(identites, "Tough", effect)

    return [AbilityFactory.AfterGameSetup(mise_en_place)]
