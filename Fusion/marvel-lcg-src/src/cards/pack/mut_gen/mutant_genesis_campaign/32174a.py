from . import *
from cards.pack.mut_gen.campaign import ShuffleTopFuturePastIntoEncounter
def GetAbilities() -> Sequence['Ability']:
    def when_defeated(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        ShuffleTopFuturePastIntoEncounter(effect)
        this = effect.this.CastTo(EncounterSideScheme)
        player = message.GetDefeatingPlayer() if hasattr(message, 'GetDefeatingPlayer') else None
        if not player:
            player = Worlds.GetFirstPlayer(effect)
        this.card.Flip(effect)
        face = this.card.face
        face.CastTo(Obligation).PutIntoPlay(player, effect, under_control=True)
    return [AbilityFactory.WhenSchemeBeDefeated(AbilityType.WhenDefeated, 'This', when_defeated, has_defeating_player=True)]
