from . import *

# Madame Web's Powers — AMELIORATION, cout 2, RES [energy]. SUPERPOWER.
# You gain the PSIONIC trait.
# Hero Resource: Exhaust Madame Web's Powers and place 1 psionic web counter on
#   Spider-Woman (to a maximum of 10) -> generate a [mental] resource.
#
# ⚠ LA CARTE PAIE LE PACK AVEC LUI-MEME : elle produit la ressource [mental]
# que cinq cartes comptent pour poser des compteurs, ET pose un compteur au
# passage. C'est la seule source de [mental] du set heros.
#
# CARTES DE REFERENCE
#  - `ab007` * Donald Pierce / `bt014` * Peter Parker :
#    `CanGenerateResources(AbilityType.HeroResource, Resources("B"))
#    .SetCostFunc(CostFunc.Exhaust("This"))`.
#  - `06009` * Mjolnir : donner un TRAIT en continu, par
#    `GiveKeywordToInPlayWhenApplyThis("You", control_by="You", trait=...)`.
#
# TEXTE CONTRE CODE
#  ⚠ « YOU gain the PSIONIC trait » : l'IDENTITE, pas la carte. Deux cartes du
#    pack en dependent — `sw006` et `sw007` sont PSIONIC elles-memes, mais
#    c'est l'identite qui doit porter le trait pour les effets qui la lisent.
#  ⚠ DEUX COUTS avant la fleche : l'inclinaison ET la pose d'un compteur. Le
#    second n'est pas un effet, c'est un prix — et il ne se paie pas si le
#    stock est plein... sauf que « to a maximum of 10 » ne dit PAS que la
#    capacite est interdite a 10. On pose donc ce qu'on peut (zero) et la
#    ressource sort quand meme : le plafond borne la pose, pas la capacite.
#  ⚠ UNE SEULE `CanGenerateResources` par carte (assert du moteur). Respecte.


def GetAbilities() -> Sequence['Ability']:

    def poser_une_toile(cibles: Sequence['CardFace'], effect: 'Effect') -> bool:
        Unused(cibles)
        PoserDesToiles(effect.GetInitiator(), 1, effect)
        return True

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            "You",
            control_by="You",
            trait="PSIONIC",
        ),
        AbilityFactory.CanGenerateResources(
            AbilityType.HeroResource,
            Resources("B"),
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetCostFunc(CostFunc.Custom(None, poser_une_toile)),
    ]
