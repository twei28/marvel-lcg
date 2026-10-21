#!/usr/bin/env python3
"""Lanceur de la batterie « Marvelous » : `tools/test_capacites.py` avec les
cas de `generer_cas.py` a la place des siens.

    cp -a .game-src .game-src-marvelous     # une fois ; jamais .game
    PARALLELES=4 python3.10 tools/generateurs-marvelous/batterie_test_capacites.py \
        .game-src-marvelous 30000 /tmp/marvelous.json [filtre]

`MARVELOUS_DECKS="iron_man,spider_man_2099"` (noms de decks de depart ou de
sets, separes par des virgules) restreint aux cartes de ces heros : c'est le
pilote. Sans elle, toutes les cartes signature empruntables.

⚠ Le nom de ce fichier CONTIENT `test_capacites.py` : c'est ce que cherche le
garde-fou `_verifier_aucun_autre_harnais_en_cours` (pgrep). Le renommer le
rendrait invisible aux autres harnais, et eux invisibles a lui.

Comment il se greffe (rien n'est modifie dans test_capacites.py) :
  - `tc.CAS` remplace par nos cas, regeneres a l'identique dans chaque fils
    (le harnais relance CE fichier avec CAS_INDEX, d'ou `tc.__file__`) ;
  - `tc.VERIFICATIONS` prolonge du verificateur `marvelous_jouee` ;
  - `remplir_les_decks_vides` enveloppe : le cas Stan Lee remplace son
    `hero_deck` par celui du heros emprunte (`hero_deck_stan`) AVANT la mise
    en place, donc Marvelous prete les noms des la mise en place, comme en
    vraie partie ;
  - `Puzzle.AssertJouable(card_id)` (leve si `CardFace.CanPlayBy` dit non)
    greffe sur la classe du puzzle des que son module est importe.
"""
import json
import os
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
TOOLS = os.path.dirname(ICI)
sys.path.insert(0, ICI)
sys.path.insert(0, TOOLS)

import generer_cas  # noqa: E402
import test_capacites as tc  # noqa: E402

_voulus = [x.strip() for x in os.environ.get("MARVELOUS_DECKS", "").split(",") if x.strip()]
tc.CAS = generer_cas.generer(_voulus or None)
# `MARVELOUS_SAUF=<rapport.json>` : ne rejouer QUE les cas dont le nom n'est pas deja
# dans ce rapport (reprise apres une pause, 21/10/2026). On ne reprend pas « a partir
# de l'index N » : la liste a grandi entre-temps (nouveaux heros inseres au milieu),
# les index ne designent plus les memes cartes. Le nom, lui, ne bouge pas. La liste
# reduite est regeneree a l'identique dans chaque fils (CAS_INDEX), comme la liste entiere.
_sauf = os.environ.get("MARVELOUS_SAUF")
if _sauf:
    with open(_sauf, encoding="utf-8") as _f:
        _faits = {c["nom"] for c in json.load(_f)["cas"]}
    tc.CAS = [c for c in tc.CAS if c["nom"] not in _faits]
tc.VERIFICATIONS = tc.VERIFICATIONS + generer_cas.VERIFICATEURS
tc.__file__ = os.path.abspath(__file__)

_remplir_origine = tc.remplir_les_decks_vides


def _remplir(scene):
    _remplir_origine(scene)
    index = os.environ.get("CAS_INDEX")
    if index is None:
        return
    cas = tc.CAS[int(index)]
    deck = cas.get("hero_deck_stan")
    if deck and getattr(scene, "players", None):
        scene.players[0].hero_deck = list(deck)


tc.remplir_les_decks_vides = _remplir



def _AssertJouable(self, card_id):
    player = self.world.GetCurrentPlayer()
    face = None
    for f in player.hand_cards.GetAll():
        if getattr(f.paper, "card_id", None) == card_id:
            face = f
            break
    if face is None:
        raise RuntimeError(f"{card_id} n'est pas en main (AssertJouable)")
    if not face.CanPlayBy(player):
        qui = getattr(getattr(player.GetIdentity(), "paper", None), "name", "?")
        raise RuntimeError(f"{card_id} INJOUABLE pour {qui} (CanPlayBy False)")


# ⚠ PAS D'IMPORT ANTICIPE DU MOTEUR : `game.puzzle.puzzle` importe en tete de
# processus tombe en import circulaire (`game.object`). Le moteur exige l'ordre
# d'import du harnais (engine.network puis engine.device puis, en partie, le
# puzzle). On greffe donc `AssertJouable` a la volee, des que le module du
# puzzle est charge, via un crochet sur `__import__`.
import builtins  # noqa: E402

_import_origine = builtins.__import__


def _import_avec_greffe(name, *args, **kwargs):
    module = _import_origine(name, *args, **kwargs)
    puzzle = sys.modules.get("game.puzzle.puzzle")
    if puzzle is not None and not getattr(puzzle, "_marvelous_greffe", False):
        # Le crochet voit aussi les imports FAITS PAR puzzle.py lui-meme, alors
        # que ses classes n'existent pas encore : on ne coche qu'une fois
        # qu'une classe a vraiment ete greffee.
        greffees = 0
        for nom in ("RunPuzzle", "PuzzleHelper"):
            classe = getattr(puzzle, nom, None)
            if classe is not None and isinstance(classe, type):
                classe.AssertJouable = _AssertJouable
                greffees += 1
        if greffees:
            puzzle._marvelous_greffe = True
    return module


builtins.__import__ = _import_avec_greffe

if __name__ == "__main__":
    tc.main()
