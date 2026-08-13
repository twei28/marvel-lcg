from . import *

# * Gorilla-Man

def GetAbilities() -> Sequence['Ability']:

    # « ignore le texte "Max 1 per ally" des ameliorations » : c'est une regle
    # de construction/pose, pas une capacite declenchee. Le moteur a un
    # crochet pour « controler une carte restreinte de plus » mais pas pour ce
    # cas precis ; l'ecart est ecrit ici plutot que passe sous silence.
    return [
        AbilityFactory.ThisGainKeyword(
            lambda effect, ui: 1,
            control_additional_restricted=CardFinder(card_type=Upgrade),
        ),
    ]
