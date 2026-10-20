from . import *

# Portal to the Negative Zone — MANIGANCE ANNEXE (ensemble Annihilus). Hinder 1.
# When Defeated: Each player may shuffle 1 identity-specific card from their discard pile into their deck.
#
# Cartes de reference :
#  - Hinder 1 : BASE AUTOMATIQUE (`desc.Hinder`), aucun module.
#  - « When Defeated: Each player may shuffle 1 ... from their discard pile into their deck » :
#    `WhenSchemeBeDefeated` + `AskChooseFace` + `Faces.ShuffleAllTo` ; `AbilityType.ForcedInterrupt`, PAS
#    `AbilityType.WhenDefeated` (avertissement explicite du moteur, `defeated.py` : « Don't try to use
#    "AbilityType.WhenDefeated", see "11033" » — modele reel `fne/sense_deck/60002.py` / `11033` Time
#    Portal, une manigance de RENCONTRE ; `hd012` est une manigance JOUEUR, regime different).
#
# ⚠ Mots-pieges : « EACH player MAY » (optionnel, par joueur, pas seulement celui qui a vaincu la
# manigance) ; « 1 identity-specific card » (pas n'importe quelle carte de la defausse) ; Hinder n'affecte
# que le seuil, pas ce module.


def GetAbilities() -> Sequence['Ability']:

    def vaincue(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        Unused(message)

        def remelanger(player: 'Player') -> None:
            candidats = [f for f in player.discard_pile.GetAll() if f.IsClass("IdentitySpecific")]
            if not candidats:
                return
            choisie = player.AskChooseFace(
                candidats, effect, forced=False,
                prompt="Shuffle 1 identity-specific card from your discard pile into your deck",
            )
            if choisie is not None:
                Faces.ShuffleAllTo([choisie], player.player_deck, effect)

        Players.ForEachPlayer(effect, remelanger)

    return [
        AbilityFactory.WhenSchemeBeDefeated(AbilityType.ForcedInterrupt, "This", vaincue),
    ]
