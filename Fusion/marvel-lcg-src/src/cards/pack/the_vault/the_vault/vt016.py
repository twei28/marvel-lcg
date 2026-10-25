from . import *

# * Venom (II) — VILAIN, stade 2. Activation Order 8.
# Stalwart. Toughness. (natifs : desc.Stalwart et desc.Toughness, aucun module)
# Forced Response: After you attack Venom with a card you control, choose to either heal 1 damage from him or place 1
#   threat on the main scheme.
#
# Cartes de reference :
#  - « After you attack X ... choose to either A or B » : `ChoixApresAttaque` (helper du set) = `AfterUnitAttackUnit(ForcedResponse,
#    "You", "This", ...)` (modele pu096) + `ChooseAbilities(ForChoiceAbility(A), ForChoiceAbility(B))` (modele OFFICIEL 04096b,
#    gs136) ; « place 1 threat on the main scheme » : `this.PlaceThreatOnSchemes("MainScheme", 1, effect)` (60148 Proxima).
#  - Option A : `this.HealthUnits([cible], 1, effect)` (modele 42018 Angel's Aerie).
#
# ⚠ Mots-pieges : « you attack ... with a card you control » = l'ATTAQUANT du joueur (heros ou allie), le joueur qui a attaque choisit ;
# « the attacker » = `message.attacker` (le personnage qui a attaque, pas l'identite) ; « each character you control » = personnages
# du joueur qui a attaque (`GetControlCharacters`).


def GetAbilities() -> Sequence['Ability']:

    def option(effect: 'Effect', message: 'Message.AfterUnitAttackUnit', joueur: 'Player') -> None:
        this = effect.this.CastTo(Villain)
        Unused(this)
        this.HealthUnits([this], 1, effect)

    return [
        *ChoixApresAttaque("Heal 1 damage from him", option),
    ]
