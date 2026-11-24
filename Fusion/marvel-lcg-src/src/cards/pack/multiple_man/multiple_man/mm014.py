from . import *

# Prepare For Future Tragedy : MANIGANCE ANNEXE JOUEUR, cout 2, [physical]. Menace 4. Victory 0.
# Only a Dupe ally can remove threat from this scheme.
# Hero Response: After this side scheme is defeated, return the Dupe ally that defeated it to your hand → remove 2 threat from a different scheme.
# While Prepare For Future Tragedy is in the victory display, Multiple Man gains +1 DEF, and Dupe allies gain Toughness. (porte par l'IDENTITE : mm001a / mm001b)
#
# CARTES DE REFERENCE : voir mm012. `lj019` / `ra009` : `this.RemoveThreatFromSchemes([scheme], n, effect)`.
# TEXTE CONTRE CODE : cout 2 (glyphe « 2 » tourne). « a DIFFERENT scheme » : pas cette manigance ; le choix est au joueur ; une manigance « seul un Dupe » ne peut pas etre choisie utilement (la source est
#  cette carte, pas un Dupe : retrait refuse, decision utilisateur du 04/11).


def GetAbilities() -> Sequence['Ability']:

    def retirer(effect: 'Effect', joueur: 'Player', tueur: 'CardFace') -> None:
        Unused(tueur)
        autres = [f for f in Worlds.FindCardsOnField(effect, card_type=Scheme2) if f is not effect.this]
        if not autres:
            return
        cible = joueur.AskChooseFace(autres, effect, forced=True) if len(autres) > 1 else autres[0]
        if cible is not None:
            effect.this.RemoveThreatFromSchemes([cible], 2, effect)

    return CapacitesPlateauJoueur(retirer)
