from . import *

# X-Factor Investigations : SOUTIEN, cout 1, [physical]. LOCATION. X-FACTOR.
# Alter Ego Response: After Jamie Madrox defeats a side scheme, exhaust X-Factor Investigations → remove 3 threat from the main scheme.
#
# CARTES DE REFERENCE : `sn009` / `52001a` (`AfterUnitDefeatedScheme(.., "You", SchemeSide2, op)`), `mf009` (`RemoveThreatFromSchemes("MainScheme", n, effect)`).
# TEXTE CONTRE CODE : « After Jamie Madrox defeats A SIDE SCHEME » : n'importe quel complot annexe vaincu par l'identite (Dupe-seulement compris : elle le vainc par un thwart ; sans `is_from_thwart` :
#  « defeats »). « Alter Ego Response » : seulement en forme alter-ego. « the MAIN scheme » : le principal. Chiffres : cout 1, 3 menaces.


def GetAbilities() -> Sequence['Ability']:

    def enqueter(effect: 'Effect', message: 'Message.AfterUnitDefeatedScheme') -> None:
        Unused(message)
        effect.this.RemoveThreatFromSchemes("MainScheme", 3, effect)

    return [
        AbilityFactory.AfterUnitDefeatedScheme(
            AbilityType.AlterEgoResponse,
            "You",
            SchemeSide2,
            enqueter,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
