from . import *

# * Anchovy

def GetAbilities() -> Sequence['Ability']:

    def vaincu(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        Faces.ShuffleAllTo([effect.this], "EncounterDeck", effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        this = effect.this.CastTo(Minion)

        def apres_l_activation():
            Worlds.GetFirstPlayer(effect).DealEncounterCard(this, effect)
        message.AfterThisActivation(effect, apres_l_activation)

    return [
        AbilityFactory.WhenUnitBeDefeated(AbilityType.ForcedInterrupt, "This", vaincu),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
