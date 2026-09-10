from . import *

# * Rachel Carpenter — SOUTIEN, cout 2, RES [energy]. PERSONA.
# Alter-Ego Action: Exhaust Rachel Carpenter -> ready Julia Carpenter.
#
# ⚠ La fille de Julia, et la carte la plus simple du pack : elle rend une
# seconde Action d'alter ego par round, donc 3 compteurs de plus.
#
# CARTE DE REFERENCE
#  - `01034` * Stark Tower et la famille des soutiens qui redressent : le
#    montage est `WhenInYourPlayTurn(AlterEgoAction, op)` +
#    `CostFunc.Exhaust("This")` + `Faces.ReadyAll`.
#
# TEXTE CONTRE CODE
#  ⚠ « ready JULIA CARPENTER » : l'IDENTITE, et seulement en forme civile —
#    l'Action d'alter ego s'en charge, on ne teste pas la forme deux fois.
#  ⚠ Rachel s'incline, Julia se redresse : deux cartes distinctes, ne pas
#    inverser.


def GetAbilities() -> Sequence['Ability']:

    def redresser_julia(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        Unused(message)
        identite = IdentiteDe(effect.GetInitiator())
        if identite is not None:
            Faces.ReadyAll([identite], effect)

    return [
        AbilityFactory.CanPlayThisSupportCard(),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            redresser_julia,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
