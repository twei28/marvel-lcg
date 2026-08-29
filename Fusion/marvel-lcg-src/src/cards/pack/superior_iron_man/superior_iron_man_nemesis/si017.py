from . import *

# Get My Body Back
#
# "Deal 1 damage to the Tony Stark player, then take 1 damage" : la cible du
# second "take 1 damage" n'est imprimee nulle part (ni EN ni FR). Decision
# utilisateur (29/08/2026) : le joueur Tony Stark, 2 fois de suite -- deux
# appels DealDamage separes (pas un DealDamage(2) unique) pour rester fidele
# a "puis" (deux instances de degats, pas une seule de 2).

def GetAbilities() -> Sequence['Ability']:

    def when_revealed(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        player = message.GetToPlayer()
        identity = player.GetIdentity()
        this.DealDamage([identity], 1, effect)
        this.DealDamage([identity], 1, effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            when_revealed,
        ),
    ]
