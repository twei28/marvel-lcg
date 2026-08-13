from . import *

# The Long Night

def GetAbilities() -> Sequence['Ability']:

    def sbire_vaincu(effect: 'Effect', message: 'Message.AfterUnitBeDefeated') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        Faces.RemoveTokensOn([this], 2, 'threat', effect)

    def la_nuit_est_passee(effect: 'Effect', message: 'Message.AfterCardRemovedToken') -> None:
        # « When the last threat is removed from this scheme, the players
        # survive the night and win the game. » C'est LA condition de victoire
        # du scenario : Shocker, lui, ne meurt jamais.
        Worlds.SetGameOver(True, effect)

    return [
        AbilityFactory.AfterUnitBeDefeated(
            AbilityType.Response,
            Minion,
            sbire_vaincu,
            conditions=[
                lambda effect, message:
                    message.trigger.HasTrait("CRIMINAL")
            ],
        ),
        AbilityFactory.WhenLastThreatRemoveFromThisScheme(
            AbilityType.ForcedInterrupt,
            la_nuit_est_passee
        ),
    ]
