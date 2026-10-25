from . import *

# * Mad Thinker (II) — VILAIN, stade 2. Activation Order 5.
# When Revealed: Place 1 threat on the main scheme for each enemy in play.
# Forced Response: After you attack Mad Thinker with a card you control, choose to either place 1 threat on each side scheme or place 1
#   threat on the main scheme.
#
# Cartes de reference :
#  - « After you attack X ... choose to either A or B » : `ChoixApresAttaque` (helper du set) = `AfterUnitAttackUnit(ForcedResponse,
#    "You", "This", ...)` (modele pu096) + `ChooseAbilities(ForChoiceAbility(A), ForChoiceAbility(B))` (modele OFFICIEL 04096b,
#    gs136) ; « place 1 threat on the main scheme » : `this.PlaceThreatOnSchemes("MainScheme", 1, effect)` (60148 Proxima).
#  - Option A : `this.PlaceThreatOnSchemes(manigances, 1, effect)` (modele sl004a ; `Worlds.GetAllSideSchemes`).
#  - When Revealed : `AbilityFactory.WhenThisRevealed(None, ...)` (modele ld002) ; l'effet est joue par CHAQUE joueur (`Worlds.GetPlayers`).
#
# ⚠ Mots-pieges : « you attack ... with a card you control » = l'ATTAQUANT du joueur (heros ou allie), le joueur qui a attaque choisit ;
# « the attacker » = `message.attacker` (le personnage qui a attaque, pas l'identite) ; « each character you control » = personnages
# du joueur qui a attaque (`GetControlCharacters`).


def GetAbilities() -> Sequence['Ability']:

    def revelee(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Villain)
        Unused(this)
        ennemis = list(Worlds.GetVillains(effect)) + list(Worlds.GetOnFieldMinions(effect))
        if ennemis:
            this.PlaceThreatOnSchemes("MainScheme", len(ennemis), effect)

    def option(effect: 'Effect', message: 'Message.AfterUnitAttackUnit', joueur: 'Player') -> None:
        this = effect.this.CastTo(Villain)
        Unused(this)
        this.PlaceThreatOnSchemes(Worlds.GetAllSideSchemes(effect), 1, effect)

    return [
        *ChoixApresAttaque("Place 1 threat on each side scheme", option),
        AbilityFactory.WhenThisRevealed(None, revelee),
    ]
