from . import *

# Art Museum Heist (FAILED) — Setup: Each player chooses to stun or confuse
#   their identity (in expert mode, do both instead).

def GetAbilities() -> Sequence['Ability']:

    def mise_en_place(effect: 'Effect', message: 'Message.WhenGameWouldBegin') -> None:
        def chacun(player: 'Player') -> None:
            identite = player.GetIdentity()
            if Worlds.IsExpert(effect):
                Faces.GiveStatus([identite], "Stunned", effect)
                Faces.GiveStatus([identite], "Confused", effect)
                return
            player.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility("Stun your identity", lambda targets: Faces.GiveStatus([identite], "Stunned", effect)),
                AbilityFactory.ForChoiceAbility("Confuse your identity", lambda targets: Faces.GiveStatus([identite], "Confused", effect)),
            )
        Players.ForEachPlayer(effect, chacun)

    return [AbilityFactory.AfterGameSetup(mise_en_place)]
