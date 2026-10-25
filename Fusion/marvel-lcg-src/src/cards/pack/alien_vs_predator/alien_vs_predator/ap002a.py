from . import *

# * Predator Warlord (A, standard) — MECHANT. YAUTJA. SCH 1, ATK 2, PV 16[per_hero].
# [star] When Predator Warlord schemes, place that threat on his side scheme instead of the main scheme, if able.
# [star] Forced Interrupt: When Predator Warlord attacks, either place 2 threat on the main scheme or he gets +1 ATK for this attack.
# When Defeated: Flip this card.
#
# Cartes de reference :
#  - redirection : `PlaceThreatOnCardWhenThisScheme` (07002) ; « his side scheme » = Skulls for the Taking ;
#  - « either ... or ... » a l'attaque : `WhenUnitWouldAttack(ForcedInterrupt)` + `ChooseAbilities` + `GainATKForThisAttack` (21092) ;
#  - « When Defeated: Flip this card » : `card.Flip` (modele tk).
#
# ⚠ Mots-pieges :
#  - « When Predator Warlord ATTACKS » (pas « attacks you ») : vaut aussi contre un allie (Predator's Prey, Trophy Taken) ;
#  - « place 2 threat on the MAIN scheme » : directement sur le complot, pas sur Skulls (ce n'est pas une manigance du mechant) ;
#  - le joueur attaque choisit (a defaut le premier joueur) ; « for this attack » seulement.


def GetAbilities() -> Sequence['Ability']:
    return CapacitesWarlord()
