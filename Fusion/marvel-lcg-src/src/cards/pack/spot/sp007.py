from . import *

# * Rocket Racer

def GetAbilities() -> Sequence['Ability']:
    def au_moins_deux_menaces(effect: 'Effect', ui: List['CardFace']) -> int:
        return 1 if effect.this.CastTo(CanPlaceToken).GetTokens('threat') >= 2 else 0

    return [
        # « Rocket Racer gains patrol and guard while he has 2 or more threat
        # on him. » Les deux mots-cles d'un coup : `Gain` les accepte tous les
        # deux, et le rafraichissement suit les jetons.
        AbilityFactory.ThisGainKeyword(
            au_moins_deux_menaces,
            patrol=1,
            guard=1,
            change_on_event=OnEvent.Token("This", 'threat')
        ),
    ]
