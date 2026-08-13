from . import *

# * The Spot (III)

def GetAbilities() -> Sequence['Ability']:
    # « Threat Level 1. Characters may thwart against The Spot. »
    #
    # ECART ASSUME, ecrit plutot que silencieux : maniganceer CONTRE un VILAIN
    # n'a aucun crochet. `ThwartInternal` (can_thwart.py) ne prend que des
    # `Scheme2`, et un vilain n'en est pas un. Le Threat Level, lui, est bien
    # porte (desc `ThreatLevel`), et la menace se pose bien sur lui (`Hinder`,
    # et les cartes du set qui l'y placent). Ce qui manque est donc UNIQUEMENT
    # la maniere d'en RETIRER en maniganceant.
    return [
        # « The Spot gains retaliate 1 for every 5 threat here, to a maximum
        # of retaliate 3. »
        GagneParMenacePosee(5, maximum=4, retaliate=1),
    ]
