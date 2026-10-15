from . import *

# * Empress R'Klll — MECHANT, stade 1 (Skrull Empire). SKRULL. Sans PV.
# When Revealed: Empress R'Klll attacks each player in hero form.
# ★ Empress R'Klll's attacks gain piercing.
#
# Carte de reference : **`sk032`** Empress R'Klll (sbire nemesis de Hulkling,
# MEME texte) : `WhenThisRevealed` + `DoAttackYou` pour chaque joueur en
# forme heros (modele 39014b Spiral) ; `UnitAttackGainKeyword("This",
# piercing=True)`.
# ⚠ FAQ du livret p. 20 : si ce mechant est revele alors que le SBIRE nemesis
# Empress R'Klll est en jeu, le sbire est defausse (unicite) et le mechant
# active contre le joueur qui l'avait engage. Regle d'unicite native.


def GetAbilities() -> Sequence['Ability']:

    def revelation(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Villain)
        Unused(message)

        def attaque(joueur: 'Player') -> None:
            if Hero.IsType(joueur.GetIdentity()) and this.IsInPlay():
                this.DoAttackYou(joueur, effect)

        Players.ForEachPlayer(effect, attaque)

    return [
        AbilityFactory.UnitAttackGainKeyword("This", piercing=True),
        AbilityFactory.WhenThisRevealed(None, revelation),
    ]
