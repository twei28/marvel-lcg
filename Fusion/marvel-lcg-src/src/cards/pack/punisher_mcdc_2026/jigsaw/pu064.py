from . import *

# * Eel — SBIRE UNIQUE. CRIMINAL. MAGGIA. SCH 1, ATQ 2★, 4 PV, Boost 1, Quickstrike 1.
# Quickstrike.
# ★ Forced Response : After Eel attacks and damages a character, exhaust that character. Otherwise, stun it.
#
# Cartes de reference : sm/sinister_six/27099.py (Vulture : `AfterUnitAttackUnit(ForcedResponse, "This", "You")`),
# skrull_menace/paibok/sk148.py (`Faces.GiveStatus(..., "Stunned", effect)`). Quickstrike : natif (`desc`).
#
# Regle : « that character » = le personnage ATTAQUE (le defenseur s'il y en a un, car il devient la cible de
# l'attaque) ; « attacks and damages » = il a subi au moins un degat. Sinon (defendu sans degat, Tenace, tout
# absorbe) il est etourdi. Un personnage deja epuise le reste ; un Stalwart ne peut pas etre etourdi (moteur).

def GetAbilities() -> Sequence['Ability']:

    def apres_attaque(effect: 'Effect', message: 'Message.AfterUnitAttackUnit') -> None:
        blesses = list(message.took_damage_targets)
        if blesses:
            Faces.ExhaustAll(blesses, effect)
            return
        cible = message.defender or message.attacked[0]
        Faces.GiveStatus([cible], "Stunned", effect)

    return [
        AbilityFactory.AfterUnitAttackUnit(AbilityType.ForcedResponse, "This", "You", apres_attaque),
    ]
