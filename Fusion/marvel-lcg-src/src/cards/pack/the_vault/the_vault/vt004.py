from . import *

# * Mentallo (II) — VILAIN, stade 2. Activation Order 2.
# When Revealed: Each player exhausts a character they control.
# Forced Response: After you attack Mentallo with a card you control, choose to either exhaust your identity or place 1
#   threat on the main scheme.
#
# Cartes de reference :
#  - « After you attack X ... choose to either A or B » : `ChoixApresAttaque` (helper du set) = `AfterUnitAttackUnit(ForcedResponse,
#    "You", "This", ...)` (modele pu096) + `ChooseAbilities(ForChoiceAbility(A), ForChoiceAbility(B))` (modele OFFICIEL 04096b,
#    gs136) ; « place 1 threat on the main scheme » : `this.PlaceThreatOnSchemes("MainScheme", 1, effect)` (60148 Proxima).
#  - Option A : `Faces.ExhaustAll([identite], effect)`.
#  - When Revealed : `AbilityFactory.WhenThisRevealed(None, ...)` (modele ld002) ; l'effet est joue par CHAQUE joueur (`Worlds.GetPlayers`).
#
# ⚠ Mots-pieges : « you attack ... with a card you control » = l'ATTAQUANT du joueur (heros ou allie), le joueur qui a attaque choisit ;
# « the attacker » = `message.attacker` (le personnage qui a attaque, pas l'identite) ; « each character you control » = personnages
# du joueur qui a attaque (`GetControlCharacters`).


def GetAbilities() -> Sequence['Ability']:

    def revelee(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Villain)
        Unused(this)
        for joueur in Worlds.GetPlayers(effect):
            prets = [c for c in joueur.GetControlCharacters() if not c.card.IsExhaust()]
            cible = prets[0] if len(prets) == 1 else (joueur.AskChooseFace(prets, effect, not_move=True) if prets else None)
            if cible is not None:
                Faces.ExhaustAll([cible], effect)

    def option(effect: 'Effect', message: 'Message.AfterUnitAttackUnit', joueur: 'Player') -> None:
        this = effect.this.CastTo(Villain)
        Unused(this)
        Faces.ExhaustAll([joueur.GetIdentity()], effect)

    return [
        *ChoixApresAttaque("Exhaust your identity", option),
        AbilityFactory.WhenThisRevealed(None, revelee),
    ]
