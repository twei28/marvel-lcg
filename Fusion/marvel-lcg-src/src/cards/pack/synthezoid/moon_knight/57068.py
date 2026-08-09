from . import *
def GetAbilities() -> Sequence['Ability']:
    def when_defeated(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        Unused(this)
        player = message.GetDefeatingPlayer() if hasattr(message, 'GetDefeatingPlayer') else None
        if not player:
            player = Worlds.GetFirstPlayer(effect)
        treachery = Worlds.DiscardEncounterCardsUntil(effect, card_type=Treachery)
        if treachery:
            # CORRECTIF : le texte dit « Resolve that card's WHEN REVEALED
            # ability », pas « reveal it ». Reveal() faisait une revelation
            # complete : elle resolvait aussi le Renfort et les icones de
            # mots-cles de la traitrise. Idiome employe partout ailleurs.
            Faces.ResolveAbility([treachery], player, AbilityType.WhenRevealed, effect)
    return [AbilityFactory.WhenSchemeBeDefeated(AbilityType.WhenDefeated, 'This', when_defeated, has_defeating_player=True)]
