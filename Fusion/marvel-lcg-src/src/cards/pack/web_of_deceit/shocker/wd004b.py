from . import *

# The Gang's All Here (3B)

def GetAbilities() -> Sequence['Ability']:

    return [
        # « Vibro-Shock Gauntlets gains permanent. » Le mot-cle est donne a la
        # carte EN JEU, pas au stade : c'est l'attachement qui devient
        # indefaussable, tant que ce stade est la.
        # ⚠ Cette fabrique rend une LISTE d'abilites, pas une : sans l'etoile,
        # la carte se construit avec une liste dans sa liste et le moteur
        # plante au chargement du scenario.
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            CardFinder(name="Vibro-Shock Gauntlets"),
            permanent=1,
        ),
    ]
