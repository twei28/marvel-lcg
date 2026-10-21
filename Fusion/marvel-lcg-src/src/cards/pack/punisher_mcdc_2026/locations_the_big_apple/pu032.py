from . import *

# Upper East Side (3) — LIEU (environnement LOCATION).
# Action: Discard cards from the encounter deck until a side scheme is discarded. Reveal that scheme. (Limit once per round.)
#
# Cartes de reference : jj008 (Alias Investigations : meme Action, `Worlds.DiscardEncounterCardsUntil(effect, card_type=...)` puis
# `face.Reveal(joueur, effect)`), 24030 (Ruination, meme texte « until a side scheme is discarded. Reveal »), pu031 (Action de lieu
# + `LimitOncePerRound` globale + `Ville.AuLieu`).
# ⚠ « a side scheme » : une manigance ANNEXE de rencontre (`EncounterSideScheme`), pas la principale ; « Reveal that scheme » : revelee
# POUR le joueur qui a active l'Action ; si le deck n'en contient aucune, tout le deck est defausse et rien n'est revele.

def GetAbilities() -> Sequence['Ability']:

    def reveler_une_annexe(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        Unused(message)
        joueur = effect.GetInitiator()
        annexe = Worlds.DiscardEncounterCardsUntil(effect, card_type=EncounterSideScheme)
        if annexe:
            annexe.Reveal(joueur, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(AbilityType.Action, reveler_une_annexe, conditions=[Ville.AuLieu])
        .LimitOncePerRound(),
    ]
