"""Site d'ESSAI pour la fonction « Decks des joueurs » : base jetable, trois
faux comptes, decks SYNTHETIQUES. Aucun fichier de joueur reel n'est lu, aucun
serveur de production n'est contacte, aucun moteur de jeu n'est allume.

Sert au test serveur (site/test_decks_admin.py, via `monter`) et a la page
Playwright (ui-check/tests/admin-decks-joueurs.spec.ts, via la ligne de
commande) :

    python3 site/serveur_essai_decks_admin.py 8097      # ecoute sur 127.0.0.1:8097

Comptes : arnaud (admin), alice, bob ; mot de passe `essai-mdp-12345`.
"""
import json
import os
import shutil
import sys
import tempfile

ICI = os.path.dirname(os.path.abspath(__file__))
MDP = "essai-mdp-12345"


def deck_synthetique(nom, hero="01001a,01001b", cartes=30):
    return {"name": nom, "version": "0.0.0", "metadata": {}, "hero": [hero],
            "hero_deck": ["01002"], "player_deck": ["01010"] * cartes,
            "obligations": [], "nemesis_set": [], "set_aside": []}


def monter(dossier=None):
    """Prepare l'environnement et rend `(orchestrateur, dossier, comptes)`.
    A appeler AVANT tout `import orchestrateur`."""
    dossier = dossier or tempfile.mkdtemp(prefix="decks-admin-")
    os.environ["BASE"] = os.path.join(dossier, "narwhal.db")
    os.environ["JOURNAL_DECKS_ADMIN"] = os.path.join(dossier, "journal-decks-admin.log")
    os.environ["ADMIN"] = "arnaud"
    sys.path.insert(0, ICI)
    import orchestrateur as o

    jeu = os.path.join(dossier, "jeu")
    os.makedirs(os.path.join(jeu, ".game", "deck"))
    os.makedirs(os.path.join(jeu, "data"))
    shutil.copy(os.path.join(o.RACINE_JEU, "launch.json"), os.path.join(jeu, "launch.json"))
    o.RACINE_JEU = jeu
    o.initialiser_base()
    places = {}
    for pseudo in ("arnaud", "alice", "bob"):
        o.inscrire(pseudo, pseudo + "@essai.invalid", MDP)
        o.changer_statut(pseudo, "valide")
        places[pseudo] = o.emplacement_de(pseudo)
        os.makedirs(os.path.join(jeu, ".game", "deck", "serveur-%d" % places[pseudo]))

    def ecrire(pseudo, fichier, deck):
        chemin = os.path.join(jeu, ".game", "deck", "serveur-%d" % places[pseudo], fichier + ".json")
        with open(chemin, "w", encoding="utf-8") as f:
            json.dump(deck, f)
        return chemin

    ecrire("alice", "mcdb-Equilibre", deck_synthetique("Équilibre de test", cartes=40))
    ecrire("alice", "Agressif", deck_synthetique("Agressif <b>test</b>", cartes=36))
    ecrire("bob", "Protection", deck_synthetique("Protection de test", "02001a,02001b", 41))
    ecrire("arnaud", "Deja-la", deck_synthetique("Deck de l'admin", cartes=40))
    return o, dossier, {"places": places, "ecrire": ecrire, "jeu": jeu}


if __name__ == "__main__":
    from http.server import ThreadingHTTPServer
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8097
    o, dossier, _ = monter()
    print("site d'essai : http://127.0.0.1:%d (donnees : %s)" % (port, dossier), flush=True)
    ThreadingHTTPServer(("127.0.0.1", port), o.Handler).serve_forever()
