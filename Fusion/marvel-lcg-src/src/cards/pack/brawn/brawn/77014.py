from . import *

# Forward-Thinking — custom « Rainy »
# Response: After you play a card from your reserve, ready your identity.
#
# Pas de restriction de forme ici, contrairement a Brawn's Suit et Totally
# Awesome : la carte imprime « Response » sec, elle joue donc aussi en
# alter-ego — ce qui est utile, Amadeus Cho ayant lui aussi une action a
# epuisement.

def GetAbilities() -> Sequence['Ability']:

    def redresser_identite(effect: 'Effect', message: 'Message.AfterPlayerPlayedCard') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)

        joueur = message.GetToPlayer()
        identite = joueur.GetIdentity()
        if identite is not None:
            Faces.ReadyAll([identite], effect)

    return [
        ApresCarteJoueeDepuisLaReserve(
            AbilityType.Response,
            redresser_identite,
        ),
    ]
