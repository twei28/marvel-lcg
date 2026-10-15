from . import *

# Galactic Ambassador — COMPLOT ANNEXE (Paibok). Menace 2[per_hero], icone ACCELERATION, 1 boost.
# When Revealed: Place 2 additional threat here for each friendly character with a status card.
#
# Cartes de reference :
#  - Poser de la menace sur soi : `this.PlaceThreatOnSchemes([this], n, effect)` (recette §2, modele
#    `50134`) ; compter des personnages : `player.GetControlCharacters()` (modele 24017).
#  - Icone Acceleration : `desc.Acceleration` natif (fiche mots-cles/acceleration.md), lecture validee
#    par l'utilisateur le 15/10/2026 (NOTES.md).
#
# ⚠ Mots-pieges : « FOR EACH friendly character WITH A STATUS CARD » : un personnage compte UNE fois,
# meme avec Sonne ET Desoriente ; « friendly » = aux joueurs (tous les joueurs, pas seulement celui qui
# revele) ; Robuste est une carte d'etat comme les autres ; « 2 ADDITIONAL » = 2 par personnage, en plus
# de la menace de depart.


def GetAbilities() -> Sequence['Ability']:

    def revelation(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        Unused(message)
        this = effect.this.CastTo(EncounterSideScheme)
        nombre = sum(1 for joueur in Worlds.GetPlayers(effect) for perso in joueur.GetControlCharacters()
                     if perso.IsStunned() or perso.IsConfused() or perso.IsTough())
        if nombre:
            this.PlaceThreatOnSchemes([this], 2 * nombre, effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revelation),
    ]
