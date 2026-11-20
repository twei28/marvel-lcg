from . import *

# Majestrix's Verdict (2A) — MANIGANCE PRINCIPALE, stade 2.
# When Revealed: The players as a group choose 1 STARJAMMER ally tucked under Imprisoned on Chandilar and
#   remove it from the game (2 STARJAMMER allies instead in expert mode). Otherwise, the players as a group
#   choose 1 STARJAMMER ally in play and remove it from the game. Advance to stage 2B.
#
# Cartes de reference :
#  - « players as a group choose » : le premier joueur tranche (`ChoisirEnGroupe`, convention `Filter.One`).
#  - « remove it from the game » : `Faces.RemoveAllFromGame` (helper `RetirerDeLaPartie`, qui applique aussi
#    « If Lilandra is removed from the game, the players lose the game », texte de gs121 et de l'insert).
#  - « Advance to stage 2B » : une face A sans seuil avance seule (`MainScheme.OnAfterCardRevealedEnd`), comme
#    sk145a ; aucun appel a ecrire.
#  - « in expert mode » : `Worlds.IsExpert(effect)` (modele 50087a).
#
# ⚠ Mots-pieges : « Otherwise » = SEULEMENT si aucun STARJAMMER n'est glisse (FAQ du livret 1.2 p.12 : en expert
# avec un seul glisse, on retire celui-la et on ne passe PAS a « Otherwise ») ; « in play » = sous le controle
# de n'importe quel joueur.


def GetAbilities() -> Sequence['Ability']:

    def verdict(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        Unused(message)
        nombre = 2 if Worlds.IsExpert(effect) else 1
        glisses = GlissesSousLaPrison(effect)
        if glisses:
            RetirerDeLaPartie(ChoisirEnGroupe(effect, glisses, nombre), effect)
            return
        en_jeu = StarjammersEnJeu(effect)
        if en_jeu:
            RetirerDeLaPartie(ChoisirEnGroupe(effect, en_jeu, 1), effect)

    return [
        AbilityFactory.WhenThisRevealed(None, verdict),
    ]
