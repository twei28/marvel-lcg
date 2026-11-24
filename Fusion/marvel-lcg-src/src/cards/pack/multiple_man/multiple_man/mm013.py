from . import *

# Madrox, Agent of S.H.I.E.L.D. : MANIGANCE ANNEXE JOUEUR, cout 2, [energy]. Menace 4. Victory 0.
# Only a Dupe ally can remove threat from this scheme.
# Hero Response: After this side scheme is defeated, return the Dupe ally that defeated it to your hand → deal 2 damage to an enemy.
# While Madrox, Agent of S.H.I.E.L.D. is in the victory display, Multiple Man gains +1 THW, the S.H.I.E.L.D. trait, and your ally limit is increased by 1. (porte par l'IDENTITE : mm001a / mm001b)
#
# CARTES DE REFERENCE : voir mm012. Choix de la cible : `joueur.AskChooseFace(ennemis, effect)` (modele `ca022`) ; degats : `this.DealDamage([cible], 2, effect)`.
# TEXTE CONTRE CODE : cout 2 (glyphe « 2 » tourne). « deal 2 damage to AN enemy » : n'importe quel ennemi en jeu (vilain compris), au choix du joueur ; ce ne sont pas des degats d'attaque.


def GetAbilities() -> Sequence['Ability']:

    def degats(effect: 'Effect', joueur: 'Player', tueur: 'CardFace') -> None:
        Unused(tueur)
        ennemis = [f for f in Worlds.GetOnFieldEnemies(effect) if f.IsInPlay()]
        if not ennemis:
            return
        cible = joueur.AskChooseFace(ennemis, effect, forced=True) if len(ennemis) > 1 else ennemis[0]
        if cible is not None:
            effect.this.DealDamage([cible], 2, effect)

    return CapacitesPlateauJoueur(degats)
