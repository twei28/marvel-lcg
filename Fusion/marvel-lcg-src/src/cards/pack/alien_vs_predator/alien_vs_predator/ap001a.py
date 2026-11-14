from . import *

# * Alien Queen (A, standard) — MECHANT. XENOMORPH. SCH 2, ATK 1, PV 18[per_hero].
# [star] When Alien Queen schemes, place that threat on her side scheme instead of the main scheme, if able.
# [star] Forced Response: After Alien Queen attacks and damages a character you control, shuffle a Xenomorph card into your deck.
# When Defeated: Flip this card.
#
# Cartes de reference :
#  - redirection de la menace : `PlaceThreatOnCardWhenThisScheme` (Wrecking Crew 07002, bw020) ; « her side scheme » = Expanding Hive
#    (« Alien Queen's Scheme ») ;
#  - « attacks and damages a character you control » : `AfterUnitAttackAndDamageUnit(.., "This", "YouControlCharacter")` (27161 Kraven) ;
#    « shuffle a Xenomorph card » : une carte au hasard du deck Xenomorph glisse sous elle (helper `MelangerUnXenomorph`) ;
#  - « When Defeated: Flip this card » : `card.Flip` (le retournement revele la face Defeated, modele tk Bebop & Rocksteady).
#
# ⚠ Mots-pieges :
#  - « if able » : Expanding Hive retiree du jeu -> la menace va au complot principal ;
#  - « a character YOU control » : le joueur attaque (identite ou allie) recoit la carte, pas le premier joueur ;
#  - deck Xenomorph vide : rien n'est melange (insert) ;
#  - « Flip » : seulement si Predator Warlord est encore en jeu ; derniere mechante vaincue -> les joueurs gagnent (arbitrage 2).


def GetAbilities() -> Sequence['Ability']:
    return CapacitesReine()
