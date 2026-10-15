from . import *

# * Emperor Dorrek VII — MECHANT, stade 1 (Skrull Empire). SKRULL. Sans PV.
# Incite 1[per_hero].
# ★ Emperor Dorrek VII's attacks gain overkill.
#
# Cartes de reference : `sk032` / `41002b` pour
# `UnitAttackGainKeyword("This", overkill=True)` ; Incite (fiche
# mots-cles/incite.md) : « When a card with incite X is revealed, place X threat
# on the main scheme ».
# ⚠ Le moteur ne resout Incite que sur les cartes rencontre NON mechant
# (CanIncite est porte par EncounterNonVillainCard) : sur un mechant, le mot-cle
# est ecrit ici en `WhenThisRevealed`, avec la valeur PAR JOUEUR imprimee
# (« 1[per_hero] »). Il part a chaque revelation (setup exclu : Dorrek I ouvre
# toujours le stade), donc apres un Overthrow ou un changement de stade.


def GetAbilities() -> Sequence['Ability']:

    def incite(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Villain)
        Unused(message)
        complot = Worlds.FindMainScheme(effect)
        if complot is not None:
            this.PlaceThreatOnSchemes([complot], Worlds.GetPlayerNumIcon(effect), effect)

    return [
        AbilityFactory.UnitAttackGainKeyword("This", overkill=True),
        AbilityFactory.WhenThisRevealed(None, incite),
    ]
