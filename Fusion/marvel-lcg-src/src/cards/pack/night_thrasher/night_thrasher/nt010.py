from . import *

# Multi-Skilled — amelioration signature, x1 (n/16 = 15). CONDITION.
# Cout 1, ressource [mental].
# Resource: Exhaust Multi-Skilled -> generate a [wild] resource for a
#   [[SKILL]] card.
#
# Cartes de reference :
#  - **`14017`** Nerves of Steel / `04010` Expert Marksman / `04033` Finesse :
#    `CanGenerateResources(AbilityType.Resource, Resources("G"), <CardFinder>)`
#    — le troisieme argument `for_card` est exactement « generate a [x]
#    resource FOR <telle carte> ». Quinze cartes officielles au meme montage.
#  - `ab007` * Donald Pierce / `as010` * Gwen Stacy pour
#    `.SetCostFunc(CostFunc.Exhaust("This"))`.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « a **[wild]** resource » : `Resources("G")`. Le [mental] du coin
#    superieur gauche est le COUT IMPRIME de la carte, pas ce qu'elle genere —
#    deux choses differentes sur la meme carte, c'est le piege classique de
#    lecture, et la leçon Lockjaw impose de croiser l'icone avec une autre
#    carte du MEME pack : `nt004` Drop In et `nt007` Tailblock portent la meme
#    icone bleue et coutent bien du [mental].
#  - « for a **[[SKILL]]** card » : le TRAIT, pas le type. Un allie, une
#    amelioration ou un evenement SKILL sont tous finançables — et le pack en
#    compte cinq, plus les cartes d'aspect Justice.
#  - ⚠ **UNE SEULE `CanGenerateResources` par carte** (assert du moteur).
#  - `CONDITION` est un trait imprime sans mecanique : rien a scripter pour
#    lui.


def GetAbilities() -> Sequence['Ability']:

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.CanGenerateResources(
            AbilityType.Resource,
            Resources("G"),
            CardFinder(trait="SKILL"),
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
