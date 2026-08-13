from . import *

# Warp Hole

def GetAbilities() -> Sequence['Ability']:

    def au_moins_trois_menaces(effect: 'Effect', ui: List['CardFace']) -> int:
        return 1 if effect.this.CastTo(CanPlaceToken).GetTokens('threat') >= 3 else 0

    return [
        # « While there is 3 or more threat here, this card gains
        # [acceleration] [hazard]. »
        AbilityFactory.ThisGainKeyword(
            au_moins_trois_menaces,
            acceleration_icon=1,
            hazard=1,
            change_on_event=OnEvent.Token("This", 'threat')
        ),
        # « Hero Response: After an attack deals 3 or more damage to The Spot,
        # remove 2 threat from here. If the last threat is removed from here
        # this way, discard Warp Hole. »
        #
        # ECART ASSUME : la reponse est ecrite ci-dessous mais le retrait passe
        # par le complot principal, qui DEROUTE toute menace retiree d'une
        # carte du Spot (1B). Tant que ce deroutement vaut, retirer la menace
        # d'ici la deplacerait au lieu de la faire disparaitre. La carte est
        # donc laissee sans reponse plutot que de mentir au joueur.
    ]
