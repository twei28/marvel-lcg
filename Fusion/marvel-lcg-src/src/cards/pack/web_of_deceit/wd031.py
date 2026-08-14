from . import *

# "Vote for Fisk" (expert)

def GetAbilities() -> Sequence['Ability']:

    # `AbilityFactory.ExpertModeOnly()` ne convient PAS ici : elle RETOURNE la
    # carte hors mode expert, ce qui suppose deux faces. Les deux « Vote for
    # Fisk » sont deux cartes distinctes, et c'est la mise en place du scenario
    # qui choisit laquelle entre en jeu (`Worlds.IsExpert`).
    return [
        VoteForFisk(2),
    ]
