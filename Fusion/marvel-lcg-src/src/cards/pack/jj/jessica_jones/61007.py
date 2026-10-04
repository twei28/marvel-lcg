from . import *

# * Piecing It All Together
# « This scheme does not count against the player side scheme limit. »
# Le moniteur de limite (world/limit_monitor/player_side_scheme_limit.py) exclut
# les faces portant `not_count_player_side_scheme_limit`. On la marque a
# l'ENTREE EN JEU : la carte se JOUE, et `WhenCardSetup` n'existe qu'a la mise
# en place, donc le drapeau n'etait jamais pose (signalement du 02/10/2026).
# ⚠ `WhenCardEnterPlay` et NON `AfterCardEnterPlay` (modele ip002a) : le
# controle de limite se fait dans `PlayerSideScheme.OnAfterCardEnterPlay`,
# AVANT l'envoi du message « After » ; le drapeau arrivait trop tard.

def GetAbilities() -> Sequence['Ability']:
    def hors_limite(effect: 'Effect', message: 'Message.WhenCardEnterPlay') -> None:
        Unused(message)
        for face in effect.this.card.printed_faces:
            face.not_count_player_side_scheme_limit = True

    def when_defeated(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        this = effect.this.CastTo(PlayerSideScheme)
        Unused(this)
        player = message.GetDefeatingPlayer()
        if not player:
            player = effect.GetInitiator()
        player.DrawUp(3, effect)
    return [
        AbilityFactory.CanPlayThisSchemeCard(),
        AbilityFactory.WhenCardEnterPlay(AbilityType.Temp0, "This", hors_limite),
        AbilityFactory.WhenSchemeBeDefeated(AbilityType.WhenDefeated, 'This', when_defeated, has_defeating_player=True),
    ]
