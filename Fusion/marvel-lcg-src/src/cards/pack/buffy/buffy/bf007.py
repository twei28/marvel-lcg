from . import *

# * Slayer Scythe — AMELIORATION (MYSTIC. WEAPON), cout 2, [wild]. Unique. Restricted. Linked (Enemies Aligned).
# Hero Resource: Exhaust Slayer Scythe → generate a [wild] resource. Any player may trigger this ability.
#
# CARTES DE REFERENCE
#  - `06008` God of Thunder : `CanGenerateResources(HeroResource, Resources(..)).SetCostFunc(Exhaust("This"))`.
#  - `fne/echo/60043` : le meme montage avec `.AnyPlayerCanDoThis()` pour « any player may trigger this ability ».
#  - `Restricted` est lu par le moteur dans `desc` (aucun module). `desc.Linked` n'est pas pose : « Enemies Aligned » n'est pas
#    fournie par le Drive (fiche `mots-cles/linked.md`).
#
# TEXTE CONTRE CODE
#  « Hero Resource » -> `AbilityType.HeroResource` (forme heros seulement). « [wild] » -> `Resources("G")`. « Any player » ->
#    `AnyPlayerCanDoThis`. Exhaust Slayer Scythe -> cout `Exhaust("This")`. Chiffres : une ressource, cout 2.


def GetAbilities() -> Sequence['Ability']:

    return [
        AbilityFactory.CanGenerateResources(
            AbilityType.HeroResource,
            Resources("G"),
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .AnyPlayerCanDoThis(),
    ]
