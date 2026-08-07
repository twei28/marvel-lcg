"""Verifie la generation des configurations du mode serveur.

Ne demarre AUCUN moteur : ce test lit launch.json, appelle le generateur et
regarde ce qui sort. Il ecrit dans un dossier temporaire, jamais dans le
dossier de jeu.

Usage: python3.10 tools/test_config_serveur.py
"""
import json
import os
import shutil
import sys
import tempfile

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RACINE, "tools"))

from config_serveur import PORT_BASE, construire_config, ecrire_configs

resultats = []


def verifier(nom, ok, detail=""):
    resultats.append((nom, bool(ok), str(detail)))


BASE = json.load(open(os.path.join(RACINE, "launch.json"), encoding="utf-8"))

# --- Cas nominal : ce qui change, place par place ---
for place in (1, 2, 3, 4):
    cfg = construire_config(BASE, place)
    port = PORT_BASE + place
    verifier(f"place {place} : port {port}",
             cfg["server_addresses"] == [f"127.0.0.1:{port}"],
             cfg["server_addresses"])
    verifier(f"place {place} : sauvegardes separees",
             cfg["replay_folders"] == [f"../replays/serveur-{place}/"],
             cfg["replay_folders"])
    verifier(f"place {place} : historique separe",
             cfg["games_history_file"] == f"../games_history-serveur-{place}.json",
             cfg["games_history_file"])
    verifier(f"place {place} : statistiques separees",
             cfg["game_statistics_file"] == f"../statistics-serveur-{place}.json",
             cfg["game_statistics_file"])
    verifier(f"place {place} : ecrit ses decks chez lui, lit ceux de l'hote",
             cfg["deck_folders"] == [f"./deck/serveur-{place}/", "./deck/custom/"],
             cfg["deck_folders"])
    verifier(f"place {place} : aucun mot de passe d'entree",
             cfg["password"] == "", cfg["password"])
    verifier(f"place {place} : aucun siege reserve",
             cfg["seat_passwords"] == [], cfg["seat_passwords"])

# --- Ce qui doit rester herite de launch.json ---
cfg = construire_config(BASE, 1)
verifier("images heritees", cfg["image_folders"] == BASE["image_folders"], cfg["image_folders"])
verifier("catalogue herite",
         cfg["cards_json_custom_file"] == BASE["cards_json_custom_file"],
         cfg["cards_json_custom_file"])
verifier("decks de depart herites",
         cfg["starter_deck_folder"] == BASE["starter_deck_folder"],
         cfg["starter_deck_folder"])

# --- La base ne doit pas etre abimee au passage ---
verifier("launch.json d'origine intact",
         BASE["server_addresses"] == ["127.0.0.1:2345"],
         BASE["server_addresses"])

# --- Cas limites : places hors bornes ---
for mauvaise in (0, 5, -1):
    try:
        construire_config(BASE, mauvaise)
        verifier(f"place {mauvaise} refusee", False, "aucune erreur levee")
    except ValueError:
        verifier(f"place {mauvaise} refusee", True)

# --- Ecriture reelle, dans un bac a sable ---
bac = tempfile.mkdtemp(prefix="test-config-serveur-")
try:
    shutil.copy(os.path.join(RACINE, "launch.json"), os.path.join(bac, "launch.json"))
    chemins = ecrire_configs(bac, 2)
    verifier("deux configurations ecrites", len(chemins) == 2, chemins)
    verifier("chemin attendu pour la place 1",
             chemins[0] == os.path.join(bac, ".serveur", "launch-1.json"), chemins[0])
    verifier("configuration relisible",
             json.load(open(chemins[1], encoding="utf-8"))["server_addresses"] == ["127.0.0.1:2352"])
    verifier("dossier de decks de la place 1 cree",
             os.path.isdir(os.path.join(bac, "deck", "serveur-1")))
    verifier("dossier de sauvegardes de la place 2 cree",
             os.path.isdir(os.path.join(bac, "..", "replays", "serveur-2")))
    verifier("place 3 non demandee, donc non creee",
             not os.path.exists(os.path.join(bac, ".serveur", "launch-3.json")))
    try:
        ecrire_configs(bac, 9)
        verifier("nb_places 9 refuse", False, "aucune erreur levee")
    except ValueError:
        verifier("nb_places 9 refuse", True)
finally:
    shutil.rmtree(bac, ignore_errors=True)
    shutil.rmtree(os.path.join(os.path.dirname(bac), "replays", "serveur-1"), ignore_errors=True)
    shutil.rmtree(os.path.join(os.path.dirname(bac), "replays", "serveur-2"), ignore_errors=True)

echecs = [r for r in resultats if not r[1]]
for nom, ok, detail in resultats:
    print(("  OK   " if ok else "  ECHEC") + f" {nom}" + (f"  ({detail})" if detail and not ok else ""))
print(f"\n{len(resultats) - len(echecs)}/{len(resultats)} verifications passees")
sys.exit(1 if echecs else 0)
