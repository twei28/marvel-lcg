from . import *

# hs210 Son of Kraven (set de campagne experte)
# Quickstrike (donnees). Piochee dans le deck d'un joueur : entre en jeu engagee avec lui.

def _pioche(effect: 'Effect', message: 'Message.AfterPlayerDrewCards') -> None:
    # Livret p.11 : une carte rencontre piochee dans le deck du joueur entre
    # immediatement en jeu dans sa zone, sans etre remplacee.
    effect.this.PutIntoPlay(message.to_player, effect)


def GetAbilities() -> Sequence['Ability']:
    return [AbilityFactory.AfterPlayerDrewCards(AbilityType.Campaign, "AnyPlayer", "This", _pioche)]
