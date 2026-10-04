"""Genere une configuration de moteur par place, pour le mode serveur.

Le moteur est mono-partie : une place egale un processus, donc un port et des
dossiers a lui. Tout ce qui distingue les places est ICI, nulle part ailleurs.

Ce qui est SEPARE par place : le port, les sauvegardes, l'historique, les
statistiques, le dossier ou l'ami enregistre ses decks, ses campagnes en
cours et ses hauts faits.
Ce qui reste COMMUN : les images, les sons, le catalogue de cartes, les decks
de depart, les decks de l'hote (lus, jamais ecrits), et les definitions de
campagnes (boites livrees, en lecture seule).

Usage: python3.10 tools/config_serveur.py <nb_places>
"""
import json
import os
import sys

PORT_BASE = 2350
# ⚠ RELEVE DE 4 A 20 LE 05/09/2026 pour le site NarwhalChampions, dont
# l'orchestrateur (`site/orchestrateur.py`) reutilise `construire_config` :
# c'est le SEUL endroit qui sait quelles cles doivent etre separees par place,
# et le dupliquer aurait garanti la divergence.
# `launcher-serveur.sh` continue de se limiter a 4 tout seul, dans son propre
# controle d'argument : ce relevement ne change donc rien a son comportement.
# 30 depuis le 18/09/2026 (etait 20). Le plafond REEL est la memoire : le banc
# du 16/09 a tenu 70 tables ouvertes sans casser, mais une table JOUEE porte en
# plus son cache d'images (~30 Ko par carte vue). Trente tables pleines pesent
# environ 3,3 Go pour 3,2 Go disponibles : le swap couvre le depassement.
# ⚠ TROIS ENDROITS DOIVENT S'ACCORDER : cette constante, `NB_EMPLACEMENTS`
# (orchestrateur) et les routes `p1..pN` du Caddyfile. Une place sans route
# Caddy donne une table qui tourne et que personne ne peut joindre.
PLACES_MAX = 30


def construire_config(base: dict, place: int) -> dict:
    if not isinstance(place, int) or place < 1 or place > PLACES_MAX:
        raise ValueError(f"Place hors bornes : {place} (attendu 1 a {PLACES_MAX})")
    cfg = json.loads(json.dumps(base))  # copie profonde, la base reste intacte
    cfg["server_addresses"] = [f"127.0.0.1:{PORT_BASE + place}"]
    cfg["replay_folders"] = [f"../replays/serveur-{place}/"]
    # GARDER LES PARTIES TERMINEES (13/09/2026, demande de l'utilisateur :
    # « que je puisse les revoir comme si j'y etais »).
    #
    # Le moteur sait ecrire un enregistrement complet a la sortie d'une partie
    # (`game.py`, OnExitGameInternal). Le drapeau existait depuis toujours et
    # valait False : une partie finie ne laissait aucune trace jouable, sauf si
    # quelqu'un avait pense a appuyer sur Save. Le bouton « Revoir » de
    # l'assistant, lui, savait deja les rejouer.
    cfg["auto_save_after_game_over"] = True
    cfg["games_history_file"] = f"../games_history-serveur-{place}.json"
    cfg["game_statistics_file"] = f"../statistics-serveur-{place}.json"
    # Sans separation, les quatre places partagent le meme dossier que la
    # partie solo de l'hote (campagne_definitions_folder reste commun : ce
    # sont des boites livrees, en lecture seule).
    cfg["campagne_folder"] = f"../campagnes-serveur-{place}/"
    cfg["achievements_file"] = f"../achievements-serveur-{place}.json"
    # La fiche du mode Legacy : la vague atteinte, les jetons. Separee comme
    # le reste de ce qui appartient au compte, sans quoi la progression de
    # l'un ouvrirait les boites de l'autre.
    cfg["legacy_file"] = f"../legacy-serveur-{place}.json"
    # Les arts alternatifs de heros du compte : suivent le joueur d'un appareil
    # a l'autre (le navigateur, lui, ne suit que l'appareil).
    cfg["arts_heros_file"] = f"../arts-heros-serveur-{place}.json"
    cfg["campaign_log_last_file"] = f"./campaign-log-last-serveur-{place}.json"
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
        # Les chemins de la configuration sont relatifs a .game/, pas a la
        # racine : le moteur fait os.chdir(.game) avant de les resoudre.
        for relatif in cfg["replay_folders"] + [cfg["deck_folders"][0], cfg["campagne_folder"]]:
            os.makedirs(os.path.normpath(os.path.join(racine, ".game", relatif)), exist_ok=True)
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
