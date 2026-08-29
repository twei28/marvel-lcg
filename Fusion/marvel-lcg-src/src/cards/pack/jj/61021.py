from . import *
def GetAbilities() -> Sequence['Ability']:
    def when_defeated(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        this = effect.this.CastTo(PlayerSideScheme)
        player = message.GetDefeatingPlayer()
        if not player:
            player = effect.GetInitiator()
        # « The PLAYER WHO DEFEATED this scheme deals 5[per_hero] damage » :
        # la source des degats est le heros de ce joueur, pas la manigance. La
        # difference compte pour retaliate et pour les effets qui regardent qui
        # inflige les degats.
        villain = Worlds.FindVillain(effect)
        if villain and player:
            source = player.GetIdentity() or this
            source.DealDamage([villain], "5*", effect)
    return [AbilityFactory.WhenSchemeBeDefeated(AbilityType.WhenDefeated, 'This', when_defeated, has_defeating_player=True)]
