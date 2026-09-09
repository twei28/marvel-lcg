from . import *

# Symbiotic Bond — AMELIORATION, cout 2, RES [energy]. SYMBIOTE.
# Max 1 per player.
# Resource: Take 1 damage and exhaust this card -> generate a [wild] resource.
#
# CARTES DE REFERENCE
#  - `04033` Finesse : « Resource: Exhaust Finesse -> generate a [wild]
#    resource for an aspect card. » Le montage d'une amelioration-ressource,
#    `CanGenerateResources(... Resources("G")) + CostFunc.Exhaust("This")`.
#  - `CostFunc.TakeDamage(1, "YourIdentity")` (`cost_func.py:408`), tel que
#    l'emploient `bl009` et `45043` : le second cout, celui du sang.
#
# TEXTE CONTRE CODE
#  ⚠ « Resource » et non « Hero Resource » : la ressource se genere dans LES
#    DEUX formes -> `AbilityType.Resource`. C'est l'ecart avec `04033`.
#  ⚠ « generate a [wild] resource » SANS restriction : pas de `CardFinder`,
#    contrairement a `04033` qui la reserve aux cartes d'aspect.
#  ⚠ DEUX couts, tous deux avant la fleche : les degats ET l'inclinaison. Deux
#    `SetCostFunc` chaines, comme `01080` Med Team le fait pour l'inclinaison
#    et le pion.
#  ⚠ « Take 1 damage » vise « YourIdentity » et non le heros : le texte ne dit
#    pas « your hero », et en forme alter-ego la carte reste jouable.
def GetAbilities() -> Sequence['Ability']:

    return [
        AbilityFactory.CanGenerateResources(
            AbilityType.Resource,
            Resources("G"),
        ).SetCostFunc(CostFunc.TakeDamage(1, "YourIdentity"))
        .SetCostFunc(CostFunc.Exhaust("This")),
    ]
