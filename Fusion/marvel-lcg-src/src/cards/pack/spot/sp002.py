from . import *

# * The Spot (I)

def GetAbilities() -> Sequence['Ability']:
    # « Threat Level 1. Characters may thwart against The Spot. »
    #
    # Le niveau est porte par le `desc` ; le maniganceage contre lui est
    # offert par la carte, faute de pouvoir viser un ennemi avec la
    # puissance de base.
    return [
        CaracteresPeuventManigancerContreLui(),
        # « The Spot gains retaliate 1 for every 5 threat here, to a maximum
        # of retaliate 3. »
        GagneParMenacePosee(5, maximum=3, retaliate=1),
    ]
