from . import *

# The Raft Breakout 1B — 2[per_hero], cible 11[per_hero], +1[per_hero] : bases.
# Each minion gains: "When Defeated: Remove 1 threat from the main scheme
#   (2 threat instead if this minion has the ELITE trait)."
# If this stage is completed, the players lose the game.
# ⚠ GiveAbilityToInPlayWhenApplyThis(Minion, abilities=[...]) ne donne la
# capacite QUE sur un evenement Faceup (environment_helper2.py:213,
# « Fix for 50070 ») : un sbire mis en jeu sans etre retourne (PutIntoPlay,
# Zemo qui convertit un allie...) ne la recoit jamais (harnais 18/09/2026).
# Le complot ecoute donc lui-meme la defaite de chaque sbire : meme resultat,
# et un sbire au texte vide (DECEIVED) garde la capacite, comme le veulent
# les regles (un texte vide n'efface que le texte IMPRIME).

def GetAbilities() -> Sequence['Ability']:

    def evade(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        this = effect.this.CastTo(MainScheme)
        sbire = message.trigger
        n = 2 if sbire.HasTrait("ELITE") else 1
        this.RemoveThreatFromSchemes([this], n, effect)

    return [
        AbilityFactory.WhenUnitBeDefeated(AbilityType.ForcedResponse, Minion, evade),
        AbilityFactory.IfThisSchemeStageIsCompletedPlayersLoseTheGame(),
    ]
