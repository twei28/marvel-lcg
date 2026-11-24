from . import *

# Madrox Prime : MANIGANCE ANNEXE JOUEUR, cout 2, [mental]. Menace 4. Victory 0.
# Only a Dupe ally can remove threat from this scheme.
# Hero Response: After this side scheme is defeated, return the Dupe ally that defeated it to your hand → heal 2 damage from Multiple Man.
# While Madrox Prime is in the victory display, Multiple Man gains +1 ATK, and the Makin' Dupes ability does not require exhausting. (porte par l'IDENTITE : mm001a)
#
# CARTES DE REFERENCE : `dt096` (Purple Peril : `CanPlayThisSchemeCard` + `WhenSchemeBeDefeated(HeroResponse, 'This', ..)`), `bc004` (Big Heist : `ThreatCannotBeRemovedFromWhile(..by_character=..)`), `ca001a` (soin :
#  `this.HealthUnits([identite], n, effect)`). Tout le montage est dans `CapacitesPlateauJoueur` (`multiple_man_commun.py`).
# TEXTE CONTRE CODE : le glyphe en coin est un « 2 » tourne (carte en paysage) : COUT 2 (decision utilisateur du 04/11). « Only a Dupe ally » : voir le helper. « Hero Response » : seulement en forme heros ;
#  vaincu pendant un tour d'alter-ego, le complot va quand meme a la zone de victoire (RRG, Hero Response). « heal 2 damage FROM MULTIPLE MAN » : l'identite (face heros).


def GetAbilities() -> Sequence['Ability']:

    def soigner(effect: 'Effect', joueur: 'Player', tueur: 'CardFace') -> None:
        Unused(tueur)
        effect.this.HealthUnits([joueur.GetIdentity()], 2, effect)

    return CapacitesPlateauJoueur(soigner)
