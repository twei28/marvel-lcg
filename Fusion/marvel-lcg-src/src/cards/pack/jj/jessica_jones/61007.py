from . import *

# * Piecing It All Together
# « This scheme does not count against the player side scheme limit. »
# Le moniteur de limite (world/limit_monitor/player_side_scheme_limit.py) exclut
# les faces portant `not_count_player_side_scheme_limit`. On la marque des sa
# mise en place, comme le fait la campagne NeXt Evolution.

def GetAbilities() -> Sequence['Ability']:
    def hors_limite(effect: 'Effect', message: 'Message.WhenCardSetup') -> None:
        effect.this.not_count_player_side_scheme_limit = True

    def when_defeated(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        this = effect.this.CastTo(PlayerSideScheme)
        Unused(this)
        player = message.GetDefeatingPlayer()
        if not player:
            player = effect.GetInitiator()
        player.DrawUp(3, effect)
    return [
        AbilityFactory.CanPlayThisSchemeCard(),
        AbilityFactory.WhenCardSetup("This", hors_limite),
        AbilityFactory.WhenSchemeBeDefeated(AbilityType.WhenDefeated, 'This', when_defeated, has_defeating_player=True),
    ]
