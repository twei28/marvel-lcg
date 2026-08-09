from . import *
def GetAbilities() -> Sequence['Ability']:
    def when_defeated(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        this = effect.this.CastTo(PlayerSideScheme)
        Unused(this)
        def action(player: 'Player'):
            face = Search.PlayerCard(effect, player, include_player_deck=True, include_discard_pile=True, may=True, finder=(CardFinder(trait='AVENGER') | CardFinder(trait='S.H.I.E.L.D')))
            if face:
                Faces.AddToHand([face], player, effect)
                Worlds.UpdateNextCardPlayCost(player, -2, effect, finder=CardFinder(check_face_fn=lambda f, chosen=face: f is chosen), in_this='Phase')
        Players.ForEachPlayer(effect, action)
    return [AbilityFactory.CanPlayThisSchemeCard().SetPlay(only_if_your_identity_has_one_of_traits=['AVENGER', 'S.H.I.E.L.D']),
            AbilityFactory.WhenSchemeBeDefeated(AbilityType.WhenDefeated, 'This', when_defeated)]
