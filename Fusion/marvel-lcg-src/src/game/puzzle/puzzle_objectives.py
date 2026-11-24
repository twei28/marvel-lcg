"""Objectifs et fin d'un puzzle (E3, 23/10/2026). Specification : docs/puzzle/PLAN.md.

Un puzzle de format 2 declare des objectifs (`scene.puzzle_objectifs`, un JSON par
objectif) et un mode (`all` : tous requis ; `any` : au moins un). Ce module les
suit pendant la partie et pose la fin :
- tous les objectifs requis sont atteints : VICTOIRE (raison « Players Won ») ;
- le round se termine sans que ce soit le cas : DEFAITE du puzzle ;
- une vraie defaite du moteur (heros elimines, complot principal achevé sans que ce
  soit l'objectif, deck de rencontre vide) reste une defaite.

Sans objectif (puzzle v1, bac a sable) rien ne change : le moteur conduit la fin de
partie comme avant.
"""
import json
from typing import Any, Dict, List, TYPE_CHECKING

if TYPE_CHECKING:
    from game.world import World
    from game.card.face import CardFace

REASON_ALL_MET = "Players Won"
REASON_NOT_MET = "The Puzzle Objectives were not Met"

_VILLAIN_DEFEATED = "The Final Stage of the Villain was Defeated"
_MAIN_SCHEME_DONE = ("The Final Stage of the Main Scheme was Completed", "The Main Scheme was Completed")


class PuzzleObjectives:

    def __init__(self, world: 'World') -> None:
        self.world = world
        self.done: List[bool] = []
        self._ending = False

    # ------------------------------------------------------------------ lecture
    @property
    def items(self) -> List[Dict[str, Any]]:
        result: List[Dict[str, Any]] = []
        for raw in self.world.scene.puzzle_objectifs:
            try:
                result.append(json.loads(raw))
            except ValueError:
                continue
        return result

    @property
    def active(self) -> bool:
        return self.world.scene.is_puzzle and bool(self.world.scene.puzzle_objectifs)

    @property
    def mode(self) -> str:
        return "any" if self.world.scene.puzzle_objectifs_mode == "any" else "all"

    def _sync(self) -> List[Dict[str, Any]]:
        items = self.items
        if len(self.done) != len(items):
            self.done = [False] * len(items)
        return items

    def Status(self) -> List[Dict[str, Any]]:
        """Pour l'interface : `[{kind, text, target, done}]`."""
        if not self.active:
            return []
        items = self._sync()
        return [{"kind": x.get("kind", ""), "text": x.get("text", ""), "target": x.get("target", ""),
                 "done": self.done[i]} for i, x in enumerate(items)]

    def IsSatisfied(self) -> bool:
        items = self._sync()
        if not items:
            return False
        return any(self.done) if self.mode == "any" else all(self.done)

    # ------------------------------------------------------------------ marquage
    def _Mark(self, kind: str, matches=None) -> bool:
        items = self._sync()
        changed = False
        for i, item in enumerate(items):
            if item.get("kind") == kind and not self.done[i] and (matches is None or matches(item)):
                self.done[i] = True
                changed = True
        return changed

    def ValidateFree(self, index: int) -> None:
        """Le resolveur valide a la main un objectif libre (`Puzzle.ValidateObjective`)."""
        items = self._sync()
        if not 0 <= index < len(items):
            raise ValueError(f"objectif {index} : il n'y en a que {len(items)}")
        if items[index].get("kind") != "free_text":
            raise ValueError(f"objectif {index} : seul un objectif libre se valide a la main")
        self.done[index] = True
        self._FinishIfSatisfied()

    @staticmethod
    def _TargetMatches(item: Dict[str, Any], face: 'CardFace') -> bool:
        target = str(item.get("target", "")).strip()
        if not target:
            return False
        target = target.lower()
        card_id = str(getattr(face.paper, "card_id", "") or "").lower()
        if target == str(face.name).lower() or target == card_id:
            return True
        # Un complot a deux faces (« 01097a » / « 01097b ») : l'identifiant sans la lettre de face designe la carte entiere, quelle que soit la
        # face visible au moment ou on la teste.
        racine = target[:-1] if target[-1:] in ("a", "b", "c") and any(ch.isdigit() for ch in target[:-1]) else target
        return len(racine) >= 4 and racine == (card_id[:-1] if card_id[-1:] in ("a", "b", "c") else card_id)

    # ------------------------------------------------------------------ accroches
    def InterceptGameOver(self, reason: str, by_effect: Any) -> bool:
        """Appele par `GameOverReason.SetGameOver`. Rend vrai = la fin est absorbee."""
        if not self.active or self._ending:
            return False
        if reason == _VILLAIN_DEFEATED:
            self._Mark("defeat_villain")
            self._FinishIfSatisfied(by_effect)
            return True
        if reason in _MAIN_SCHEME_DONE:
            scheme = getattr(by_effect, "this", None)
            if scheme is not None and any(
                    x.get("kind") == "complete_scheme" and self._TargetMatches(x, scheme)
                    for x in self._sync()):
                self._Mark("complete_scheme", lambda item: self._TargetMatches(item, scheme))
                self._FinishIfSatisfied(by_effect)
                return True
        return False

    def OnSchemeDefeated(self, scheme: 'CardFace') -> None:
        """Un complot annexe (ou tout complot vaincu a zero menace) a ete vaincu."""
        if not self.active or self._ending:
            return
        if self._Mark("complete_scheme", lambda item: self._TargetMatches(item, scheme)):
            self._FinishIfSatisfied()

    def OnRoundEnd(self) -> None:
        """Fin du round : « survivre » est atteint ; sinon, le puzzle est perdu."""
        if not self.active or self._ending or self.world.is_game_over:
            return
        self._Mark("survive")
        if self._FinishIfSatisfied():
            return
        self._Fail()

    # ------------------------------------------------------------------ fin
    def _EndEffect(self, by_effect: Any = None) -> Any:
        if by_effect is not None:
            return by_effect
        from game.effect.rule import GameRule
        from game.operate.worlds import Worlds
        return GameRule(Worlds.GetAllMainSchemes(self.world)[0])

    def _FinishIfSatisfied(self, by_effect: Any = None) -> bool:
        if self.world.is_game_over or not self.IsSatisfied():
            return False
        self._ending = True
        self.world.game_over.SetGameOver(REASON_ALL_MET, self._EndEffect(by_effect))
        return True

    def _Fail(self) -> None:
        self._ending = True
        self.world.game_over.SetGameOver(REASON_NOT_MET, self._EndEffect())
