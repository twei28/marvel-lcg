from . import *

# * Predator Warlord « Defeated » (A, standard) — face B du mechant. DEFEATED. YAUTJA.
# When Revealed: Heal 4[per_hero] damage from Alien Queen and give her a tough status card. Advance to stage 4A. Remove each
# permanent side scheme and this card from the game.
#
# Cartes de reference :
#  - « Heal X damage from <mechant> and give a tough status card » : `HealthUnits` + `Faces.GiveStatus(.., "Tough")` (27150, wd028) ;
#  - « Advance to stage 4A » : `World.AdvanceMainScheme(complot, face_du_stade, effect)` (saut direct, le moteur le permet par face) ;
#  - « Remove ... from the game » : `Faces.RemoveAllFromGame` (Permanent ne bloque que les effets d'un AUTRE set, permanent.md).
#
# ⚠ Mots-pieges :
#  - « 4[per_hero] » : 4 x nombre de joueurs ;
#  - « EACH permanent side scheme » : les DEUX (Expanding Hive ET Skulls for the Taking), pas seulement celle du mechant vaincu ;
#  - « and THIS card » : la face Defeated quitte la partie (le mechant vaincu ne reste pas en jeu) ;
#  - Alien Queen devient le mechant actif (3B / 4B : « Alien Queen is the active villain »), pose ici des le retournement.


def GetAbilities() -> Sequence['Ability']:
    return FaceVaincue(4, 'Alien Queen', 4)
