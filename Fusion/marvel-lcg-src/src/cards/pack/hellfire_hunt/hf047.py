from . import *

# Enemy Of Enemy (manigance annexe de campagne). Icone Crisis (desc).
# When Defeated: The player who defeat this scheme searches Selene from the set-aside area, put it into play under the player's control.
# Remove this from the campaign.
# [star] Boost: Reveal this card. You are confused.
#
# Cartes de reference : 04092 (`WhenCardBecomeBoost` + `RevealThisCard`), 01083 (`Faces.GiveStatus(..., "Confused", effect)`).
def GetAbilities() -> Sequence['Ability']:
    def ennemi_boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        RevealThisCard(effect, message)
        joueur = message.GetToPlayer()
        Faces.GiveStatus([joueur.GetIdentity()], "Confused", effect)

    return [
        AbilityFactory.WhenCardBecomeBoost("This", ennemi_boost),
        AbilitePotentialAlly("Selene"),
    ]
