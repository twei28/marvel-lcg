from . import *

# Electricity Clones

def GetAbilities() -> Sequence['Ability']:

    return [
        # « Electro ignores the unique rule. »
        #
        # C'est la carte qui tient tout le scenario : le vilain Electro, les
        # deux sbires Electro du set et les deux de Power Drain II portent le
        # meme nom et le meme point. Sans cette levee, un seul d'entre eux
        # tiendrait la table.
        AbilityFactory.UniqueRuleNotApplyTo(
            name="Electro"
        ),
    ]
