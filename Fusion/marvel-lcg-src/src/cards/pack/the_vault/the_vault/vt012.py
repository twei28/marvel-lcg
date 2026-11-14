from . import *

# * Nekra (II) — VILAIN, stade 2. Activation Order 6.
# When Revealed: Give each villain 1 facedown boost card.
# Forced Response: After you attack Nekra with a card you control, choose to either give Nekra 1 facedown boost card or place 1
#   threat on the main scheme.
#
# Cartes de reference :
#  - « After you attack X ... choose to either A or B » : `ChoixApresAttaque` (helper du set) = `AfterUnitAttackUnit(ForcedResponse,
#    "You", "This", ...)` (modele pu096) + `ChooseAbilities(ForChoiceAbility(A), ForChoiceAbility(B))` (modele OFFICIEL 04096b,
#    gs136) ; « place 1 threat on the main scheme » : `this.PlaceThreatOnSchemes("MainScheme", 1, effect)` (60148 Proxima).
#  - Option A : `GiveFacedownBoostCardsInternal(1, effect, None)` (modele bw021 Imperius Rex).
#  - When Revealed : `AbilityFactory.WhenThisRevealed(None, ...)` (modele ld002) ; l'effet est joue par CHAQUE joueur (`Worlds.GetPlayers`).
#
# ⚠ Mots-pieges : « you attack ... with a card you control » = l'ATTAQUANT du joueur (heros ou allie), le joueur qui a attaque choisit ;
# « the attacker » = `message.attacker` (le personnage qui a attaque, pas l'identite) ; « each character you control » = personnages
# du joueur qui a attaque (`GetControlCharacters`).


def GetAbilities() -> Sequence['Ability']:

    def revelee(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Villain)
        Unused(this)
        for mechant in Villains.All(effect):
            mechant.GiveFacedownBoostCardsInternal(1, effect, None)

    def option(effect: 'Effect', message: 'Message.AfterUnitAttackUnit', joueur: 'Player') -> None:
        this = effect.this.CastTo(Villain)
        Unused(this)
        this.GiveFacedownBoostCardsInternal(1, effect, None)

    return [
        *ChoixApresAttaque("Give Nekra 1 facedown boost card", option),
        AbilityFactory.WhenThisRevealed(None, revelee),
    ]
