from . import *

# hs123 / hs124 Stalking Prey
# When Revealed : distribue un piege, puis 1 menace sur le complot principal par TRAP qui vous a ete distribue.
# Boost : si au moins un TRAP vous a ete distribue, 1 menace sur le complot principal.

def GetAbilities() -> Sequence['Ability']:

    def traque(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        DonnerPiege(effect, joueur)
        n = PiegesDonnesAuJoueur(effect, joueur)
        if n > 0:
            effect.this.PlaceThreatOnSchemes("MainScheme", n, effect)

    def en_boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        if PiegesDonnesAuJoueur(effect, message.GetToPlayer()) > 0:
            effect.this.PlaceThreatOnSchemes("MainScheme", 1, effect)

    return [
        AbilityFactory.WhenThisRevealed(None, traque),
        AbilityFactory.WhenCardBecomeBoost("This", en_boost),
    ]
