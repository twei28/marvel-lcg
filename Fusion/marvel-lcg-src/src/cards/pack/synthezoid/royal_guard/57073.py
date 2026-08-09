from . import *
def GetAbilities() -> Sequence['Ability']:
    def when_defeated(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        Unused(this)
        player = message.GetDefeatingPlayer() if hasattr(message, 'GetDefeatingPlayer') else None
        if not player:
            player = Worlds.GetFirstPlayer(effect)
        face = Search.EncounterCard(effect, player, include_discard_pile=True, name='Blood Debt', card_type=Obligation)
        if face:
            player.DealEncounterCard(face, effect)
    return [AbilityFactory.WhenSchemeBeDefeated(AbilityType.WhenDefeated, 'This', when_defeated, has_defeating_player=True)]
