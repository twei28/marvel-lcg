from . import *

# * Collector — sbire nemesis de Howard the Duck, ELDER — 5 PV, SCH 3, ATK 1
# Villainous. (When this minion activates, give it a boost card.)
# When Revealed: Discard an ally or support you control. If you cannot, put
#   the topmost scheme from the encounter deck into play.
#
# « Villainous » est un mot-cle AUTOMATIQUE lu dans `desc.Villainous` : aucun
# code (precedent ok021 pour « Steady », meme famille de mots-cles
# purement declaratifs).
#
# « Discard an ALLY OR SUPPORT you control » : les deux types autorises sont
# demandes directement au moteur par
# `player.GetControlCardsByType(CardFinder(canbe_discard=True), ally=True,
# support=True)`. Le filtre `canbe_discard` (checker.py:169-171) ecarte les
# cartes PERMANENTES, qui ne peuvent pas quitter le jeu : sans lui, le moteur
# plante sur `assert controller.is_eliminated` (card_face.py:463-473) — bug
# reel rencontre sur la carte soeur hd026 en autoplay le 30/08/2026, corrige
# ici par prudence meme si aucun soutien permanent n'existe dans ce kit.
# `GetControlCardsByType` (player_get.py:107-143) ne rend QUE les cartes de
# ce joueur — piege
# `you control` du tableau : la cible ne doit jamais pouvoir viser une carte
# du vilain. On n'utilise pas `SetTarget` : la carte est une carte RENCONTREE,
# son ability n'a pas de selecteur propre au joueur cible ; le choix se fait a
# la main via `player.AskChooseFace` (modele kb008/ok023, meme montage
# « When Revealed puis choix par le joueur vise »).
#
# « If you CANNOT » (et non « if you choose not to ») : la branche de repli ne
# se declenche que s'il n'existe AUCUN allie ni soutien controle — verifie
# avant de proposer le choix, pas apres un refus. « put the topmost scheme
# from the encounter deck into play » : `Search.EncounterCard(...,
# card_type=EncounterSideScheme)` puis `face.PutIntoPlay(player, effect)`,
# modele exact ss007 (Spider-pathy), qui fait la meme chose pour « the topmost
# minion ».


def GetAbilities() -> Sequence['Ability']:

    def collector(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Minion)
        Unused(this)

        player = message.GetToPlayer()
        if player is None:
            return

        candidates = player.GetControlCardsByType(
            CardFinder(canbe_discard=True), ally=True, support=True,
        )

        if candidates:
            cible = candidates[0] if len(candidates) == 1 else player.AskChooseFace(candidates, effect)
            if cible is not None:
                Faces.DiscardAll([cible], effect)
                return

        face = Search.EncounterCard(
            effect,
            player,
            include_discard_pile=False,
            card_type=EncounterSideScheme,
        )
        if face:
            face.PutIntoPlay(player, effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            collector,
        ),
    ]
