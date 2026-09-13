from . import *

# * Head (Destroyed) — COMPONENT. DESTROYED. TECH.
# Permanent.
# Your [[THWART]] events cost 1 additional resource.
#
# Cartes de reference :
#  - `nt003b` Battle Board (face WEAPON) : la seconde face d'une amelioration
#    permanente, atteinte uniquement par retournement.
#  - `aa018` / `39062` Growing Pains : le surcout de jeu, par
#    `EachCardYouPlayCostAdditionalResource`. Cette fabrique ne filtre que par
#    TYPE de carte ; le filtre par TRAIT passe par le helper du pack.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « Your THWART **events** » : les EVENEMENTS seulement. Une amelioration
#    ou un soutien portant le trait THWART n'est pas concerne.
#  - « Your » : les cartes jouees par le CONTROLEUR de ce Component, pas par
#    n'importe quel joueur. Le helper compare `GetControlBy()` au joueur qui
#    joue la carte.
#  - Cette face n'a PAS `desc.Setup` : on n'y arrive qu'en detruisant Head.


def GetAbilities() -> Sequence['Ability']:
    return [
        VosEvenementsDeTraitCoutentUnDePlus("THWART"),
    ]
