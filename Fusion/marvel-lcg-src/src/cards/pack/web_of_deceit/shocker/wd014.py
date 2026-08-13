from . import *

# Get Shocked!

def GetAbilities() -> Sequence['Ability']:

    def revelation(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)

        joueur = message.GetToPlayer()
        Faces.GiveStatus([joueur.GetIdentity()], "Stunned", effect)

        def degat(autre: 'Player') -> None:
            this.DealDamage([autre.GetIdentity()], 1, effect)

        Players.ForEachPlayer(effect, degat)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        joueur = message.GetToPlayer()
        joueur.DiscardAllHands(effect)
        joueur.DrawUp(joueur.GetIdentity().hand_size, effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            revelation
        ),
        AbilityFactory.WhenCardBecomeBoost(
            "This",
            boost
        ),
    ]
