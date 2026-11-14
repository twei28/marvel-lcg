from . import *

# Beast Be Praised (2A) — MANIGANCE PRINCIPALE, stade 2.
# When Revealed : Each player whose Creeping Corruption has the OVERPOWERING trait discards 1 random card from their hand. Each other player discards a card they control from play.
#   In expert mode, deal each player 1 facedown encounter card.
#
# Cartes de reference : sm/personal_nightmare/27154 (`player.DiscardRandomHandCards(n, effect)`), sl006 (« discard 1 card you control » = `AskChooseFaces` parmi les cartes controlees),
# sl002a (`Worlds.IsExpert`, `DealEncounterCards`).
# ⚠ Mots-pieges : « EACH player WHOSE Creeping Corruption has OVERPOWERING » : se lit sur la face visible de SA Creeping Corruption (sl072b) ; « EACH OTHER player » : tous les autres,
#  y compris un joueur SANS Creeping Corruption ; « RANDOM card from their HAND » : au hasard dans la main, pas de choix ; « a card they CONTROL FROM PLAY » : une carte EN JEU (allie,
#  amelioration, soutien), au CHOIX du joueur, obligatoire s'il en a une ; la Creeping Corruption est Permanent (jamais proposee) ; « IN EXPERT MODE » : une carte rencontre face cachee a
#  CHAQUE joueur, ceux qui ont deja defausse comme les autres.


def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        Unused(message)

        def punit(joueur: 'Player') -> None:
            if CorruptionOverpowering(joueur):
                joueur.DiscardRandomHandCards(1, effect)
                return
            candidates = CartesControleesDefaussables(joueur)
            if candidates:
                choisie = joueur.AskChooseFaces(candidates, (1, 1), effect, not_move=True)
                Faces.DiscardAll(list(choisie), effect)

        Players.ForEachPlayer(effect, punit)
        if Worlds.IsExpert(effect):
            Players.ForEachPlayer(effect, lambda joueur: joueur.DealEncounterCards(1, effect))

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
    ]
