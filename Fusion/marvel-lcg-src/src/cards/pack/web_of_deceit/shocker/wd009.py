from . import *

# Feedback

def GetAbilities() -> Sequence['Ability']:

    def defausser_et_repiocher(effect: 'Effect', joueur: 'Player') -> None:
        joueur.DiscardAllHands(effect)
        joueur.DrawUp(joueur.GetIdentity().hand_size, effect)

    def revelation(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        Unused(this)
        joueur = message.GetToPlayer()
        Faces.GiveStatus([joueur.GetIdentity()], "Stunned", effect)
        villain = Worlds.FindVillain(effect)
        if villain:
            Faces.GiveStatus([villain], "Stunned", effect)
        defausser_et_repiocher(effect, joueur)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        defausser_et_repiocher(effect, message.GetToPlayer())

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
