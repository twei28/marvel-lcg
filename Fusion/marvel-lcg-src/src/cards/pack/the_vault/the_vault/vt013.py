from . import *

# * Vapor (I) — VILAIN, stade 1. Activation Order 7.
# Forced Response: After you attack Vapor with a card you control, choose to either confuse the attacker or place 1
#   threat on the main scheme.
#
# Cartes de reference :
#  - « After you attack X ... choose to either A or B » : `ChoixApresAttaque` (helper du set) = `AfterUnitAttackUnit(ForcedResponse,
#    "You", "This", ...)` (modele pu096) + `ChooseAbilities(ForChoiceAbility(A), ForChoiceAbility(B))` (modele OFFICIEL 04096b,
#    gs136) ; « place 1 threat on the main scheme » : `this.PlaceThreatOnSchemes("MainScheme", 1, effect)` (60148 Proxima).
#  - Option A : `Faces.GiveStatus(cibles, "Confused", effect)` (modeles 05015 / 01083).
#  - When Revealed : `AbilityFactory.WhenThisRevealed(None, ...)` (modele ld002) ; l'effet est joue par CHAQUE joueur (`Worlds.GetPlayers`).
#
# ⚠ Mots-pieges : « you attack ... with a card you control » = l'ATTAQUANT du joueur (heros ou allie), le joueur qui a attaque choisit ;
# « the attacker » = `message.attacker` (le personnage qui a attaque, pas l'identite) ; « each character you control » = personnages
# du joueur qui a attaque (`GetControlCharacters`).


def GetAbilities() -> Sequence['Ability']:

    def option(effect: 'Effect', message: 'Message.AfterUnitAttackUnit', joueur: 'Player') -> None:
        this = effect.this.CastTo(Villain)
        Unused(this)
        Faces.GiveStatus([message.attacker], "Confused", effect)

    return [
        *ChoixApresAttaque("Confuse the attacker", option),
    ]
