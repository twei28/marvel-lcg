"""E4 : le plateau courant -> un puzzle de format 2 (23/10/2026).

`CapturePuzzle(world)` lit la partie en cours et rend un dictionnaire `PuzzleData`
(`docs/puzzle/FORMAT-V2.md`). Les piles (mains, decks, defausses) vont dans les champs
du format ; tout ce qui est EN JEU (allies, soutiens, ameliorations, sbires, complots
annexes, environnement) et tous les etats (PV, epuisement, cartes d'etat, compteurs,
jetons, menace) sont ecrits en commandes `Puzzle.RestoreCard` / `Puzzle.RestoreState`.

Ce qu'on ne sait PAS capturer n'est jamais tu : `CapturePuzzle` rend aussi la liste
`avertissements` (carte en jeu d'un genre inconnu, cartes glissees sous une autre...).
"""
from typing import Any, Dict, List, Tuple

STATUS_NAMES = ("Confused", "Stunned", "Tough", "Exposed", "Cloaked", "Dazed", "Intensified")


def _ids(zone: Any, pile: bool = True) -> List[str]:
    """Identifiants d'une zone. `GetAll` va du DESSOUS vers le dessus (mesure du 22/10) ;
    le format 2 donne les piles du DESSUS vers le dessous, donc on inverse. Une main
    (`pile=False`) garde son ordre."""
    ids = [f.paper.card_id for f in zone.GetAll() if f is not None]
    return list(reversed(ids)) if pile else ids


def _position(card_id: str, liste: List[str]) -> Any:
    """Rang de `card_id` dans la liste de la campagne (chaque entree peut etre « 01097a,01097b »)."""
    for rang, entree in enumerate(liste):
        if card_id in entree.split(","):
            return rang
    return None


def _litteral(valeur: Any) -> str:
    return repr(valeur)


class _Capture:
    def __init__(self, world: Any) -> None:
        self.world = world
        self.commandes: List[str] = []
        self.avertissements: List[str] = []
        self.compteur = 0
        self.cles: Dict[int, str] = {}   # id(face) -> cle

    # ------------------------------------------------------------------ etat d'une carte
    def _etat(self, face: Any) -> Dict[str, Any]:
        """Les arguments `exhausted / health / statuses / counters / tokens / threat`
        de cette carte, ceux qui different de l'etat neuf seulement."""
        from game.card.face.attribute.can_health import CanHealth
        from game.card.face.base import Scheme2
        etat: Dict[str, Any] = {}
        if not face.IsReady():
            etat["exhausted"] = True
        if CanHealth.IsType(face) and not face.is_infinite_health and face.health < face.max_health:
            etat["health"] = int(face.health)
        status = face.card.components.status
        statuses = [[nom, int(getattr(status, nom.lower()))] for nom in STATUS_NAMES
                    if getattr(status, nom.lower(), 0)]
        if statuses:
            etat["statuses"] = statuses
        counters = [[nom, int(n)] for nom, n in face.card.components.counter.counters.items() if n]
        if counters:
            etat["counters"] = counters
        est_complot = Scheme2.IsType(face)
        # La menace d'un complot est un jeton `threat` : elle a sa propre commande.
        tokens = [[nom, int(n)] for nom, n in face.card.components.token.token.items()
                  if n and nom != "first_player_token" and not (est_complot and nom == "threat")]
        if tokens:
            etat["tokens"] = tokens
        if est_complot and face.threat:
            etat["threat"] = int(face.threat)
        return etat

    @staticmethod
    def _args(etat: Dict[str, Any]) -> str:
        return "".join(f", {nom}={_litteral(valeur)}" for nom, valeur in etat.items())

    def _nouvelle_cle(self, face: Any) -> str:
        self.compteur += 1
        cle = f"e{self.compteur}"
        self.cles[id(face)] = cle
        return cle

    # ------------------------------------------------------------------ commandes
    def etat_existant(self, face: Any, cible: str, avec_cle: bool = False) -> None:
        """Une carte DEJA en jeu au depart (identite, mechant, complot principal)."""
        etat = self._etat(face)
        cle = self._nouvelle_cle(face) if avec_cle else None
        if not etat and not cle:
            return
        arguments = f"{_litteral(cible)}" + (f", key={_litteral(cle)}" if cle else "") + self._args(etat)
        self.commandes.append(f"Puzzle.RestoreState({arguments})")

    def poser(self, face: Any, kind: str, siege: int, engaged: bool = False, host: Any = None) -> None:
        cle = self._nouvelle_cle(face)
        arguments = f"{_litteral(cle)}, {_litteral(face.paper.card_id)}, {_litteral(kind)}, siege={siege}"
        if host is not None:
            arguments += f", host={_litteral(self.cles[id(host)])}"
        if engaged:
            arguments += ", engaged=True"
        self.commandes.append(f"Puzzle.RestoreCard({arguments}{self._args(self._etat(face))})")

    def ameliorations(self, hote: Any, siege: int) -> None:
        for amelioration in hote.card.components.inventory.GetDeck().GetAll():
            self.poser(amelioration, "upgrade", siege, host=hote)
            self.ameliorations(amelioration, siege)
        sous = hote.GetPlacedCardArea().GetAll()
        if sous:
            self.avertissements.append(
                f"{hote.name} : {len(sous)} carte(s) glissee(s) dessous, non capturee(s)")

    def porteur(self, face: Any, kind: str, siege: int, engaged: bool = False) -> None:
        self.poser(face, kind, siege, engaged=engaged)
        self.ameliorations(face, siege)


def CapturePuzzle(world: Any) -> Dict[str, Any]:
    """Le plateau courant sous forme de `PuzzleData` v2 (dictionnaire) + `avertissements`."""
    from game.operate.worlds import Worlds

    scene = world.scene
    campagne = scene.campaign
    cap = _Capture(world)
    villains = Worlds.GetAllVillains(world)
    villain = villains[0] if villains else None

    # ---- les joueurs : piles dans le format, le reste en commandes
    joueurs: List[Dict[str, Any]] = []
    sieges = list(world.const_seat_order_players)
    for siege, joueur in enumerate(sieges):
        heros = joueur.area_hero.GetAll()
        identite = heros[0] if heros else None
        joueurs.append({
            "identities": [identite.paper.card_id] if identite else [],
            "hand_cards": _ids(joueur.hand_cards, pile=False),
            "player_deck": _ids(joueur.player_deck),
            "player_discard_pile": _ids(joueur.discard_pile),
            "set_aside": _ids(joueur.set_aside_deck),
            "deck_name": "",
        })

    # ---- cartes DEJA en jeu au depart : leur etat
    for siege, joueur in enumerate(sieges):
        heros = joueur.area_hero.GetAll()
        if heros:
            cap.etat_existant(heros[0], heros[0].paper.card_id, avec_cle=True)
            cap.ameliorations(heros[0], siege)
    if villain is not None:
        cap.etat_existant(villain, villain.paper.card_id, avec_cle=True)
        cap.ameliorations(villain, 0)
    for complot in Worlds.GetAllMainSchemes(world):
        cap.etat_existant(complot, complot.paper.card_id, avec_cle=True)

    # ---- cartes a POSER
    for siege, joueur in enumerate(sieges):
        for allie in joueur.allies.GetAll():
            cap.porteur(allie, "ally", siege)
        for soutien in joueur.supports.GetAll():
            cap.porteur(soutien, "support", siege)
        for sbire in joueur.engaged_minions.GetAll():
            cap.porteur(sbire, "minion", siege, engaged=True)
        for env in joueur.area_environment.GetAll():
            cap.porteur(env, "environment", siege)
        for autre in joueur.obligations_area.GetAll():
            cap.avertissements.append(f"obligation en jeu non capturee : {autre.name}")
    for env in world.area_environment.GetAll():
        cap.porteur(env, "environment", 0)
    for complot in Worlds.GetAllSideSchemes(world):
        cap.porteur(complot, "side_scheme", 0)

    # ---- tout ce qui est en jeu et que l'on n'a pas range : dit, jamais tu
    from game.card.face.card_type import StatusCard
    for objet in world.object_manager.card_dict.values():
        face = objet.face
        if face is None or not face.IsInPlay() or id(face) in cap.cles or StatusCard.IsType(face):
            continue
        cap.avertissements.append(f"carte en jeu non capturee : {face.name} ({face.paper.card_id})")

    # ---- avancement du mechant et du complot principal : leur POSITION dans les listes
    # de la campagne (la pile de victoire ne les garde pas, mesure du 23/10/2026).
    # Un appel d'`AdvanceMainScheme` = un stade.
    commandes: List[str] = []
    if villain is not None:
        etape = _position(villain.paper.card_id, campagne.villain)
        if etape is None:
            cap.avertissements.append(f"stade du mechant inconnu : {villain.paper.card_id}")
        else:
            commandes += ["Puzzle.AdvanceVillain()"] * etape
    for complot in Worlds.GetAllMainSchemes(world)[:1]:
        etape = _position(complot.paper.card_id, campagne.schemes)
        if etape is None:
            cap.avertissements.append(f"stade du complot principal inconnu : {complot.paper.card_id}")
        else:
            commandes += ["Puzzle.AdvanceMainScheme()"] * etape
    commandes += cap.commandes
    premier = sieges.index(world.GetFirstPlayer())

    return {
        "puzzle": {
            "version": scene.version,
            "author": "",
            "cover": scene.cover,
            "comment": scene.comment,
            "seed": scene.seed,
            "villain": list(campagne.villain),
            "schemes": list(campagne.schemes),
            "encounter_deck": _ids(villain.encounter_deck) if villain else [],
            "encounter_discard_pile": _ids(villain.encounter_discard_pile) if villain else [],
            "set_aside": _ids(world.aside_deck),
            "expert": bool(campagne.expert),
            "players": joueurs,
            "puzzle_command": commandes,
            "format": 2,
            "first_player": premier,
        },
        "avertissements": cap.avertissements,
    }
