from . import *
from cards.pack.mut_gen.campaign import ShuffleTopFuturePastIntoEncounter
def GetAbilities() -> Sequence['Ability']:
    def when_defeated(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        ShuffleTopFuturePastIntoEncounter(effect)
        this = effect.this.CastTo(EncounterSideScheme)
        this.card.Flip(effect)
    return [AbilityFactory.WhenSchemeBeDefeated(AbilityType.WhenDefeated, 'This', when_defeated)]
