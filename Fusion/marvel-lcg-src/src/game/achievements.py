"""Hauts faits : definitions, stockage et evaluation.

Trois familles, toutes construites sur ce que le moteur SAIT DEJA mesurer —
aucun haut fait n'est inatteignable :

  * progression  : cumuls et journal des parties (victoires, heros joues...) ;
  * defi         : conditions de fin de partie (gagner sans encaisser...) ;
  * exploit      : records atteints en cours de partie (gros coup unique...).

Le bac a sable est exclu : on y triche, rien ne s'y debloque.

Stockage : `achievements.json` a cote de `statistics.json`. On y garde, pour
chaque haut fait debloque, la date et le heros avec lequel il l'a ete.
"""
from core import *

import json
import os
import time

from engine.config import ConfigVariables
from engine.log import Log, Notify

ACHIEVEMENTS_FILE = ConfigVariables.File('achievements_file', 'achievements.json')

CATEGORY_NAME = "ACHIEVEMENT"

FAMILLE = Literal["progression", "defi", "exploit"]


class Definition:
    """Un haut fait. `mesure` renvoie la valeur atteinte, `seuil` la cible."""

    def __init__(self, cle: str, titre: str, description: str,
                 famille: 'FAMILLE', mesure: Callable[['Contexte'], int],
                 seuil: int = 1, par_heros: bool = False) -> None:
        self.cle = cle
        self.titre = titre
        self.description = description
        self.famille = famille
        self.mesure = mesure
        self.seuil = seuil
        # Un haut fait « par heros » se debloque separement pour chaque heros.
        self.par_heros = par_heros


class Contexte:
    """Tout ce qu'une regle peut consulter au moment de l'evaluation.

    `stats`     : les cumuls globaux (game/statistics/statistics.py)
    `journal`   : la liste des parties terminees (games_history.json)
    `partie`    : le resume de la partie qui vient de finir (ou None)
    `campagnes` : les campagnes du joueur, resumees par l'APPELANT sous la
                  forme {'code', 'difficulte', 'gagnee'}. Ce module ne lit
                  aucun fichier : savoir ou vivent les campagnes et combien
                  de scenarios compte une boite est le metier du serveur, pas
                  le sien.
    """

    def __init__(self, stats: Any, journal: 'List[Dict[str, Any]]',
                 partie: 'Dict[str, Any]|None' = None,
                 campagnes: 'List[Dict[str, Any]]|None' = None) -> None:
        self.stats = stats
        self.journal = journal
        self.partie = partie or {}
        self.campagnes = campagnes or []

    # --- raccourcis de lecture -------------------------------------------
    def s(self, nom: str) -> int:
        return int(getattr(self.stats, nom, 0) or 0)

    def victoires(self) -> 'List[Dict[str, Any]]':
        return [p for p in self.journal if p.get("won")]

    def heros_victorieux(self) -> 'Set[str]':
        noms: Set[str] = set()
        for p in self.victoires():
            for h in p.get("heroes", []):
                if h.get("card_id"):
                    noms.add(h["card_id"])
        return noms

    def scenarios_vaincus(self) -> 'Set[str]':
        return {p.get("scenario", "") for p in self.victoires() if p.get("scenario")}

    def campagnes_gagnees(self) -> 'List[Dict[str, Any]]':
        return [c for c in self.campagnes if c.get("gagnee")]

    def boites_de_campagne_gagnees(self) -> 'Set[str]':
        return {c.get("code", "") for c in self.campagnes_gagnees() if c.get("code")}


def definitions() -> 'List[Definition]':
    """La liste complete. Chaque entree est verifiee comme mesurable."""
    d: List[Definition] = []

    def ajouter(cle, titre, description, famille, mesure, seuil=1, par_heros=False):
        d.append(Definition(cle, titre, description, famille, mesure, seuil, par_heros))

    # ---------------------------------------------------------- progression
    for n in (1, 10, 25, 50, 100):
        ajouter(f"victoires_{n}", f"Vainqueur × {n}",
                f"Remporter {n} partie(s).", "progression",
                lambda c: len(c.victoires()), n)
    for n in (5, 20, 50):
        ajouter(f"parties_{n}", f"Habitué × {n}",
                f"Terminer {n} partie(s), gagnées ou perdues.", "progression",
                lambda c: len(c.journal), n)
    for n in (3, 10, 25):
        ajouter(f"heros_differents_{n}", f"Polyvalent × {n}",
                f"Gagner avec {n} héros différents.", "progression",
                lambda c: len(c.heros_victorieux()), n)
    for n in (3, 10):
        ajouter(f"scenarios_{n}", f"Chasseur de méchants × {n}",
                f"Vaincre {n} scénario(s) différent(s).", "progression",
                lambda c: len(c.scenarios_vaincus()), n)
    ajouter("expert_1", "Mode expert",
            "Remporter une partie en mode expert.", "progression",
            lambda c: sum(1 for p in c.victoires() if p.get("expert")), 1)

    # Campagnes menees a leur terme. Une campagne PERDUE au dernier scenario
    # ne compte pas : c'est `gagnee` qui le dit, et l'appelant l'a calcule.
    ajouter("campagne_1", "Chroniqueur",
            "Mener une campagne jusqu'a son dernier scenario, et le gagner.",
            "progression", lambda c: len(c.campagnes_gagnees()), 1)
    ajouter("campagne_boites_3", "Chroniqueur × 3",
            "Terminer les campagnes de 3 boites differentes.", "progression",
            lambda c: len(c.boites_de_campagne_gagnees()), 3)
    ajouter("campagne_experte", "Increvable",
            "Terminer une campagne en mode expert, ou la defaite du dernier "
            "scenario perd tout.", "defi",
            lambda c: sum(1 for x in c.campagnes_gagnees()
                          if x.get("difficulte") == "expert"), 1)

    for n in (100, 1000, 5000):
        ajouter(f"degats_{n}", f"Cogneur × {n}",
                f"Infliger {n} dégâts au total.", "progression",
                lambda c: c.s("total_damage_dealt") or c.s("dealt_damage"), n)
    for n in (100, 1000):
        ajouter(f"menace_{n}", f"Négociateur × {n}",
                f"Retirer {n} menaces au total.", "progression",
                lambda c: c.s("total_threats_removed") or c.s("removed_threats"), n)
    for n in (200, 2000):
        ajouter(f"pioche_{n}", f"Bibliothécaire × {n}",
                f"Piocher {n} cartes au total.", "progression",
                lambda c: c.s("total_cards_drawn") or c.s("drawn_cards"), n)
    for n in (100, 1000):
        ajouter(f"soin_{n}", f"Infirmier × {n}",
                f"Soigner {n} dégâts au total.", "progression",
                lambda c: c.s("total_damage_healed") or c.s("healed_damage"), n)

    # Style de jeu : un haut fait par aspect.
    for cle, nom in (("aggression", "Agression"), ("justice", "Justice"),
                     ("leadership", "Leadership"), ("protection", "Protection"),
                     ("pool", "'Pool")):
        ajouter(f"aspect_{cle}", f"Adepte : {nom}",
                f"Jouer 100 cartes de l'aspect {nom}.", "progression",
                lambda c, k=cle: c.s(f"play_aspect_{k}"), 100)
    for cle, nom in (("r", "physiques"), ("b", "mentales"),
                     ("y", "d'énergie"), ("g", "sauvages")):
        ajouter(f"ressource_{cle}", f"Générateur : {nom}",
                f"Générer 100 ressources {nom}.", "progression",
                lambda c, k=cle: c.s(f"generate_resources_{k}"), 100)

    # -------------------------------------------------------------- exploits
    ajouter("coup_15", "Coup de massue",
            "Infliger 15 dégâts ou plus en une seule fois.", "exploit",
            lambda c: c.s("max_single_damage_dealt") or c.s("maximum_single_damage"), 15)
    ajouter("coup_25", "Force de la nature",
            "Infliger 25 dégâts ou plus en une seule fois.", "exploit",
            lambda c: c.s("max_single_damage_dealt") or c.s("maximum_single_damage"), 25)
    ajouter("encaisse_10", "Encaisseur",
            "Encaisser 10 dégâts ou plus d'un seul coup.", "exploit",
            lambda c: c.s("max_single_damage_taken") or c.s("maximum_single_took_damage"), 10)
    ajouter("soin_8", "Remise sur pied",
            "Soigner 8 dégâts ou plus d'un seul coup.", "exploit",
            lambda c: c.s("max_single_damage_healed") or c.s("maximum_single_healing"), 8)
    ajouter("pioche_6", "Razzia",
            "Piocher 6 cartes ou plus d'un seul coup.", "exploit",
            lambda c: c.s("max_single_cards_drawn") or c.s("maximum_single_draw"), 6)
    ajouter("sbires_5", "Encerclé",
            "Avoir 5 sbires engagés en même temps.", "exploit",
            lambda c: c.s("max_engaged_minions"), 5)

    # Les cinq exploits deja implementes par le moteur (game/rule/achievement.py).
    ajouter("premier_sang", "Premier sang",
            "Vaincre le premier ennemi d'une partie.", "exploit",
            lambda c: c.s("achievement_first_blood"), 1)
    ajouter("double_kill", "Doublé",
            "Vaincre 2 ennemis dans la même phase.", "exploit",
            lambda c: c.s("achievement_double_kill"), 1)
    ajouter("triple_kill", "Triplé",
            "Vaincre 3 ennemis dans la même phase.", "exploit",
            lambda c: c.s("achievement_triple_kill"), 1)
    ajouter("ultra_kill", "Quadruplé",
            "Vaincre 4 ennemis dans la même phase.", "exploit",
            lambda c: c.s("achievement_ultra_kill"), 1)
    ajouter("rampage", "Carnage",
            "Vaincre 5 ennemis ou plus dans la même phase.", "exploit",
            lambda c: c.s("achievement_rampage"), 1)

    # ------------------------------------------------------------------ defis
    ajouter("victoire_rapide", "Expéditif",
            "Gagner une partie en 6 rounds ou moins.", "defi",
            lambda c: 1 if any(p.get("rounds", 99) <= 6 for p in c.victoires()) else 0, 1)
    ajouter("victoire_tres_rapide", "Foudroyant",
            "Gagner une partie en 4 rounds ou moins.", "defi",
            lambda c: 1 if any(p.get("rounds", 99) <= 4 for p in c.victoires()) else 0, 1)
    ajouter("marathon", "Marathonien",
            "Gagner une partie de 20 rounds ou plus.", "defi",
            lambda c: 1 if any(p.get("rounds", 0) >= 20 for p in c.victoires()) else 0, 1)
    ajouter("deck_vide", "Jusqu'à la dernière carte",
            "Épuiser son deck au moins une fois.", "defi",
            lambda c: c.s("run_out_of_deck"), 1)

    # Par heros : « gagner avec ce heros ». Une entree unique, dupliquee a
    # l'affichage pour chaque heros du journal (voir grille_par_heros).
    ajouter("victoire_heros", "Maîtrise",
            "Remporter une partie avec ce héros.", "progression",
            lambda c: len(c.heros_victorieux()), 1, par_heros=True)

    return d


# ---------------------------------------------------------------- stockage
def _chemin() -> str:
    return ACHIEVEMENTS_FILE.value or "achievements.json"


def charger() -> 'Dict[str, Any]':
    try:
        with open(_chemin(), encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, dict):
            data.setdefault("debloques", {})
            data.setdefault("par_heros", {})
            return data
    except Exception:
        pass
    return {"debloques": {}, "par_heros": {}}


def enregistrer(data: 'Dict[str, Any]') -> None:
    try:
        with open(_chemin(), "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=1)
    except Exception as exc:
        Log.Debug(CATEGORY_NAME, f"ecriture impossible : {exc}")


# -------------------------------------------------------------- evaluation
def evaluer(stats: Any, journal: 'List[Dict[str, Any]]',
            partie: 'Dict[str, Any]|None' = None,
            campagnes: 'List[Dict[str, Any]]|None' = None) -> 'List[Definition]':
    """Met a jour le fichier et renvoie les hauts faits NOUVELLEMENT debloques."""
    ctx = Contexte(stats, journal, partie, campagnes)
    data = charger()
    debloques = data["debloques"]
    nouveaux: List[Definition] = []

    for definition in definitions():
        if definition.par_heros:
            # Un enregistrement par heros victorieux.
            deja = data["par_heros"].setdefault(definition.cle, {})
            for card_id in ctx.heros_victorieux():
                if card_id not in deja:
                    deja[card_id] = int(time.time())
                    nouveaux.append(definition)
            continue

        if definition.cle in debloques:
            continue
        try:
            valeur = int(definition.mesure(ctx) or 0)
        except Exception as exc:
            Log.Debug(CATEGORY_NAME, f"{definition.cle} illisible : {exc}")
            continue
        if valeur >= definition.seuil:
            debloques[definition.cle] = int(time.time())
            nouveaux.append(definition)

    if nouveaux:
        enregistrer(data)
        for definition in nouveaux:
            Notify.Game(f"Haut fait : {definition.titre}")
            Log.Debug(CATEGORY_NAME, f"debloque : {definition.cle}")
    return nouveaux


def etat_complet(stats: Any, journal: 'List[Dict[str, Any]]',
                 campagnes: 'List[Dict[str, Any]]|None' = None) -> 'Dict[str, Any]':
    """Vue pour la galerie : chaque haut fait, sa progression, sa date."""
    ctx = Contexte(stats, journal, None, campagnes)
    data = charger()
    sortie: List[Dict[str, Any]] = []
    for definition in definitions():
        try:
            valeur = int(definition.mesure(ctx) or 0)
        except Exception:
            valeur = 0
        sortie.append({
            "cle": definition.cle,
            "titre": definition.titre,
            "description": definition.description,
            "famille": definition.famille,
            "seuil": definition.seuil,
            "valeur": min(valeur, definition.seuil),
            "par_heros": definition.par_heros,
            "debloque": data["debloques"].get(definition.cle),
            "heros": data["par_heros"].get(definition.cle, {}),
        })
    return {"hauts_faits": sortie}
