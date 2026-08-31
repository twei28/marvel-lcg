from . import *

# * Black Cat (Felicia Hardy) — allie signature. HERO FOR HIRE.
# Cout 2 / PV 2 / THW 1* / ATK 3**
# [star] Black Cat's basic thwart ignores crisis icons ([crisis]).
#
# Carte de reference : 32002 * Shadowcat (pack mut_gen), qui rend le meme
# service avec `AbilityFactory.UnitIgnoreKeywordIcons("This", ...)`. Shadowcat
# ignore guard + patrol + crisis ; Black Cat n'imprime QUE crisis, on ne coche
# donc que celui-la (pas de capacite fantome, PROCESSUS-CARTE etape 5).

def GetAbilities() -> Sequence['Ability']:

    return [
        AbilityFactory.UnitIgnoreKeywordIcons(
            "This",
            crisis=True,
        ),
    ]
