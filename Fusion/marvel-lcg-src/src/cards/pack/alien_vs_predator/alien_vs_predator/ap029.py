from . import *

# Predation — TRAITRISE. Boost ★ + 2.
# When Revealed: Heal 3 damage from the active villain and give them a tough status card. Deal 3 damage to an enemy whose trait does not
#   match the active villain.
# [star] Boost: Place 2 threat on each scheme.
#
# Cartes de reference : `HealthUnits` + `GiveStatus("Tough")` (wd028) ; `DealDamage` a un ennemi au choix ; « each scheme » : complot +
#   toutes les manigances annexes (`Worlds.GetOnFieldSchemes`).
#
# ⚠ Mots-pieges :
#  - « an enemy whose trait does not match the active villain » : un ennemi SANS le trait du mechant actif (XENOMORPH pour la Reine,
#    YAUTJA pour le Warlord) : l'autre mechant, ses sbires, un sbire sans trait ; au choix du joueur ;
#  - « EACH scheme » : principal ET annexes (y compris les manigances permanentes).


def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this
        joueur = JoueurDuMessage(message, effect)
        actif = MechantActif(effect)
        if actif is None:
            return
        this.HealthUnits([actif], 3, effect)
        Faces.GiveStatus([actif], "Tough", effect)
        trait = TRAIT_DE.get(NomDuMechant(actif), "")
        cibles = [e for e in Worlds.GetOnFieldEnemies(effect) if not e.HasTrait(trait)]
        if cibles:
            cible = joueur.AskChooseFace(cibles, effect, prompt="Deal 3 damage to an enemy") or cibles[0]
            this.DealDamage([cible], 3, effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        Unused(message)
        effect.this.PlaceThreatOnSchemes(list(Worlds.GetOnFieldSchemes(effect)), 2, effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
