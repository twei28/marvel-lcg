"""Genere une configuration de moteur par place, pour le mode serveur.

Le moteur est mono-partie : une place egale un processus, donc un port et des
dossiers a lui. Tout ce qui distingue les places est ICI, nulle part ailleurs.

Ce qui est SEPARE par place : le port, les sauvegardes, l'historique, les
statistiques, et le dossier ou l'ami enregistre ses decks.
Ce qui reste COMMUN : les images, les sons, le catalogue de cartes, les decks
de depart, et les decks de l'hote (lus, jamais ecrits).

Usage: python3.10 tools/config_serveur.py <nb_places>
"""
import json
import os
import sys

PORT_BASE = 2350
PLACES_MAX = 4


def construire_config(base: dict, place: int) -> dict:
    if not isinstance(place, int) or place < 1 or place > PLACES_MAX:
        raise ValueError(f"Place hors bornes : {place} (attendu 1 a {PLACES_MAX})")
    cfg = json.loads(json.dumps(base))  # copie profonde, la base reste intacte
    cfg["server_addresses"] = [f"127.0.0.1:{PORT_BASE + place}"]
    cfg["replay_folders"] = [f"../replays/serveur-{place}/"]
    cfg["games_history_file"] = f"../games_history-serveur-{place}.json"
    cfg["game_statistics_file"] = f"../statistics-serveur-{place}.json"
    # L'ordre compte : le moteur ECRIT dans deck_folders[0] et LIT toute la
    # liste (server_get.py, save_deck et list_deck). L'ami construit donc ses
    # decks chez lui et voit ceux de l'hote, sans pouvoir les abimer.
    cfg["deck_folders"] = [f"./deck/serveur-{place}/", "./deck/custom/"]
    cfg["password"] = ""
    cfg["seat_passwords"] = []
    return cfg


def ecrire_configs(racine: str, nb_places: int) -> list:
    if not isinstance(nb_places, int) or nb_places < 1 or nb_places > PLACES_MAX:
        raise ValueError(f"Nombre de places hors bornes : {nb_places} (attendu 1 a {PLACES_MAX})")
    base = json.load(open(os.path.join(racine, "launch.json"), encoding="utf-8"))
    dossier_configs = os.path.join(racine, ".serveur")
    os.makedirs(dossier_configs, exist_ok=True)
    chemins = []
    for place in range(1, nb_places + 1):
        cfg = construire_config(base, place)
        # Les chemins de la configuration sont relatifs a la racine du jeu :
        # c'est de la que le moteur tourne.
        for relatif in cfg["replay_folders"] + [cfg["deck_folders"][0]]:
            os.makedirs(os.path.normpath(os.path.join(racine, relatif)), exist_ok=True)
        chemin = os.path.join(dossier_configs, f"launch-{place}.json")
        with open(chemin, "w", encoding="utf-8") as f:
            json.dump(cfg, f, ensure_ascii=False, indent=2)
        chemins.append(chemin)
    return chemins


if __name__ == "__main__":
    racine = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    try:
        nb = int(sys.argv[1]) if len(sys.argv) > 1 else PLACES_MAX
    except ValueError:
        print(f"Nombre de places invalide : {sys.argv[1]}", file=sys.stderr)
        sys.exit(2)
    try:
        for chemin in ecrire_configs(racine, nb):
            print(chemin)
    except ValueError as erreur:
        print(str(erreur), file=sys.stderr)
        sys.exit(2)
