"""L'ecriture partielle du carnet : chacun ses champs, sans s'ecraser.

`/save_campagne` remplace la campagne ENTIERE. Deux joueurs qui valident en
meme temps se perdent l'un l'autre, en silence. Cette route-ci ne sait que
fusionner des cles de carnet, et rien d'autre : elle ne peut ni terminer un
scenario, ni gagner une campagne, ni toucher au secret.

L'etroitesse est le point. Un siege distant n'a aucune raison de pouvoir faire
ces trois choses, et le lui interdire PAR LA FORME DE LA ROUTE coute moins cher
que de le verifier partout ailleurs.

Usage: RELEASE=1 python3.10 tools/test_carnet_partiel.py
"""
import asyncio
import json
import os
import sys
import tempfile

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RACINE, "src"))
os.environ.setdefault("RELEASE", "1")

from engine.device.web.server import server_campagne


class RequeteFeinte:
    """Le minimum que la route lit d'une requete : son corps JSON."""

    def __init__(self, charge):
        self._charge = charge

    async def json(self):
        return self._charge


def lire(dossier, nom):
    with open(os.path.join(dossier, nom + ".json"), encoding="utf-8", newline="") as f:
        return json.load(f)


def ecrire(dossier, nom, campagne):
    with open(os.path.join(dossier, nom + ".json"), "w", encoding="utf-8", newline="") as f:
        json.dump(campagne, f)


def cas(nom, obtenu, attendu):
    if obtenu == attendu:
        print("  ok    %s" % nom)
        return 0
    print("  ECHEC %s : attendu %r, obtenu %r" % (nom, attendu, obtenu))
    return 1


def main():
    echecs = 0
    serveur = server_campagne.GameServerCampagne.__new__(server_campagne.GameServerCampagne)
    boucle = asyncio.new_event_loop()
    appeler = lambda charge: boucle.run_until_complete(
        serveur.save_carnet_partiel(RequeteFeinte(charge)))

    with tempfile.TemporaryDirectory() as dossier:
        server_campagne.CAMPAGNES_FOLDER.value = dossier
        ecrire(dossier, "ma_campagne", {
            "code": "trors", "nom": "Ma campagne", "id": "ma_campagne",
            "termines": ["crossbones"],
            "carnet": {"Player 1 Upgrade": "A"},
            server_campagne.CLE_SECRET: "50185;50188;50191",
        })

        # Le joueur 2 ecrit SON champ. Celui du joueur 1 doit survivre : c'est
        # tout l'objet de la route.
        appeler({"id": "ma_campagne", "champs": {"Player 2 Upgrade": "B"}})
        apres = lire(dossier, "ma_campagne")
        echecs += cas("le champ du joueur 2 est ecrit", apres["carnet"].get("Player 2 Upgrade"), "B")
        echecs += cas("celui du joueur 1 survit", apres["carnet"].get("Player 1 Upgrade"), "A")

        # Rien d'autre que le carnet ne bouge, MEME si le client l'envoie.
        appeler({
            "id": "ma_campagne",
            "champs": {"Player 3 Upgrade": "C"},
            "termines": ["crossbones", "absorbing_man"],
            "perdue": True,
            "partieEnCours": None,
        })
        apres = lire(dossier, "ma_campagne")
        echecs += cas("termines intact", apres.get("termines"), ["crossbones"])
        echecs += cas("perdue non pose", apres.get("perdue"), None)
        echecs += cas("le secret survit", apres.get(server_campagne.CLE_SECRET),
                      "50185;50188;50191")

        # Une reponse ne montre JAMAIS le secret.
        reponse = appeler({"id": "ma_campagne", "champs": {"Player 4 Upgrade": "D"}})
        brut = reponse.body.decode("utf-8")
        echecs += cas("le secret ne sort pas", server_campagne.CLE_SECRET in brut, False)
        echecs += cas("aucune preuve ne sort", "50185" in brut, False)
        echecs += cas("la reponse rend le carnet fusionne",
                      sorted(json.loads(brut)["carnet"].keys()),
                      ["Player 1 Upgrade", "Player 2 Upgrade",
                       "Player 3 Upgrade", "Player 4 Upgrade"])

        # Une campagne inconnue est refusee, sans creer de fichier : sinon un
        # identifiant mal tape fabriquerait une campagne fantome.
        reponse = appeler({"id": "inconnue", "champs": {"X": "1"}})
        echecs += cas("campagne inconnue -> 404", reponse.status, 404)
        echecs += cas("aucun fichier cree",
                      os.path.exists(os.path.join(dossier, "inconnue.json")), False)

        # Le carnet est un dict de CHAINES : c'est ainsi que le moteur le lit
        # (game/operate/campaign_logs.py). Y glisser autre chose le casserait
        # au scenario suivant, loin d'ici.
        echecs += cas("champ non-chaine -> 400",
                      appeler({"id": "ma_campagne", "champs": {"X": {"imbrique": 1}}}).status, 400)
        echecs += cas("champs absent -> 400",
                      appeler({"id": "ma_campagne"}).status, 400)
        echecs += cas("champs non-dict -> 400",
                      appeler({"id": "ma_campagne", "champs": ["X"]}).status, 400)

        # Le refus ne doit rien avoir ecrit au passage.
        apres = lire(dossier, "ma_campagne")
        echecs += cas("un refus n'ecrit rien", "X" in apres["carnet"], False)

    boucle.close()
    print("ECHECS : %d" % echecs)
    return 1 if echecs else 0


if __name__ == "__main__":
    sys.exit(main())
