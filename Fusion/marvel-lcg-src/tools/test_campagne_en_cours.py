"""La deduction « quelle campagne joue-t-on ? », eprouvee sur des fichiers.

Elle existait deja, enfouie dans secret_pour_le_moteur() : la campagne dont
`partieEnCours.depuis` est la plus recente. Ce test la verrouille AVANT de
l'extraire, pour qu'une extraction ratee se voie.

C'est cette deduction qui permet a un joueur qui REJOINT de savoir qu'il joue
une campagne : il n'a jamais pose la cle `mc-campagne-partie`, puisque c'est
l'ecran des campagnes qui l'ecrit et qu'il ne l'ouvre pas.

Usage: RELEASE=1 python3.10 tools/test_campagne_en_cours.py
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


def ecrire(dossier, nom, campagne):
    chemin = os.path.join(dossier, nom + ".json")
    with open(chemin, "w", encoding="utf-8", newline="") as f:
        json.dump(campagne, f)


def cas(nom, obtenu, attendu):
    if obtenu == attendu:
        print("  ok    %s" % nom)
        return 0
    print("  ECHEC %s : attendu %r, obtenu %r" % (nom, attendu, obtenu))
    return 1


def jeu_de(campagne):
    """Un moteur factice dont le monde porte la VRAIE regle `mode_campaign`.

    `WorldRule` et `SetRule` sont ceux du moteur : un faux monde a bool brut
    laisserait passer une garde qui testerait `is True` et casserait en
    production (la regle est un `VariableBool`).
    """
    from types import SimpleNamespace
    from game.world.world_rule import WorldRule
    regle = WorldRule()
    regle.SetRule(["mode_campaign"] if campagne else [], False, 1)
    return SimpleNamespace(world=SimpleNamespace(rule=regle))


def main():
    echecs = 0
    with tempfile.TemporaryDirectory() as dossier:
        server_campagne.CAMPAGNES_FOLDER.value = dossier

        echecs += cas("dossier vide", server_campagne._campagne_la_plus_recente(), None)

        ecrire(dossier, "ancienne", {
            "code": "trors", "nom": "Ancienne",
            "partieEnCours": {"scenario": "crossbones", "depuis": "2026-08-01T10:00:00"},
        })
        ecrire(dossier, "recente", {
            "code": "sm", "nom": "Recente",
            "partieEnCours": {"scenario": "sandman", "depuis": "2026-08-12T21:00:00"},
        })
        # Sans partie en cours : ne doit jamais l'emporter, meme ecrite en dernier.
        ecrire(dossier, "au_repos", {"code": "aoa", "nom": "Au repos", "partieEnCours": None})

        trouvee = server_campagne._campagne_la_plus_recente()
        echecs += cas("la plus recente gagne", trouvee and trouvee.get("id"), "recente")
        echecs += cas("le scenario suit", trouvee and trouvee["partieEnCours"]["scenario"], "sandman")

        # Une campagne au repos SEULE ne designe rien : la partie en cours n'est
        # pas une campagne, et pretendre le contraire ferait s'ouvrir le panneau
        # de recompenses sur une partie ordinaire.
        os.remove(os.path.join(dossier, "recente.json"))
        os.remove(os.path.join(dossier, "ancienne.json"))
        echecs += cas("au repos ne designe rien", server_campagne._campagne_la_plus_recente(), None)

        # Un fichier illisible ne doit pas faire tomber la deduction : la
        # campagne d'a cote reste jouable.
        with open(os.path.join(dossier, "casse.json"), "w", encoding="utf-8", newline="") as f:
            f.write("{ pas du json")
        ecrire(dossier, "valide", {
            "code": "sm", "nom": "Valide",
            "partieEnCours": {"scenario": "venom", "depuis": "2026-08-12T22:00:00"},
        })
        trouvee = server_campagne._campagne_la_plus_recente()
        echecs += cas("un fichier casse est saute", trouvee and trouvee.get("id"), "valide")

        # L'equipe voyage avec : c'est elle qui dit au siege N quel heros il
        # tient, et le salon en a besoin AVANT que la partie demarre.
        ecrire(dossier, "avec_equipe", {
            "code": "trors", "nom": "Avec equipe",
            "equipe": [{"heros": "spider_man", "nomHeros": "Spider-Man"},
                       {"heros": "she_hulk", "nomHeros": "She-Hulk"}],
            "partieEnCours": {"scenario": "crossbones", "depuis": "2026-08-13T09:00:00"},
        })
        trouvee = server_campagne._campagne_la_plus_recente()
        echecs += cas("l'equipe est portee", len(trouvee.get("equipe") or []), 2)

        # Le secret reste dans le dict rendu : c'est un usage INTERNE, et
        # secret_pour_le_moteur() en depend. Toute route doit le filtrer.
        ecrire(dossier, "secrete", {
            "code": "aos", "nom": "Secrete",
            server_campagne.CLE_SECRET: "50185;50188;50191",
            "partieEnCours": {"scenario": "aim", "depuis": "2026-08-13T10:00:00"},
        })
        trouvee = server_campagne._campagne_la_plus_recente()
        echecs += cas("le secret reste lisible en interne",
                      trouvee.get(server_campagne.CLE_SECRET), "50185;50188;50191")
        echecs += cas("secret_pour_le_moteur le rend",
                      server_campagne.secret_pour_le_moteur(),
                      {server_campagne.CLE_CARNET_SECRET: "50185;50188;50191"})

    # --- La ROUTE, et surtout ce qu'elle ne dit pas ---------------------
    #
    # Le secret de la taupe ne doit jamais atteindre le navigateur, et le
    # carnet n'a rien a faire ici : il se lit par /get_campagne, qui le filtre.
    # Une route neuve qui l'oublie ouvre l'enveloppe devant les joueurs.
    from engine.device.web.server.server_get import GameServerGet

    class Serveur(GameServerGet, server_campagne.GameServerCampagne):
        # `game` est une propriete en lecture seule du vrai serveur : le test
        # y met son moteur factice.
        game = None

    serveur = Serveur.__new__(Serveur)
    # La route ne parle que si la partie du MOTEUR est de campagne (regle
    # `mode_campaign`, 07/10/2026) : `partieEnCours` seul est un etat durable
    # qu'une partie ordinaire n'efface pas.
    serveur.game = jeu_de(True)
    boucle = asyncio.new_event_loop()
    with tempfile.TemporaryDirectory() as dossier:
        server_campagne.CAMPAGNES_FOLDER.value = dossier

        reponse = boucle.run_until_complete(serveur.get_campagne_en_cours(None))
        echecs += cas("hors campagne, la route ne dit rien",
                      json.loads(reponse.body.decode("utf-8")), {})

        ecrire(dossier, "ma_camp", {
            "code": "aos", "nom": "Ma campagne",
            "equipe": [{"heros": "spider_man", "nomHeros": "Spider-Man"},
                       {"heros": "she_hulk", "nomHeros": "She-Hulk"}],
            server_campagne.CLE_SECRET: "50185;50188;50191",
            "carnet": {"Player 1 Upgrade": "A"},
            "partieEnCours": {"scenario": "crossbones", "depuis": "2026-08-13T09:00:00"},
        })
        reponse = boucle.run_until_complete(serveur.get_campagne_en_cours(None))
        brut = reponse.body.decode("utf-8")
        corps = json.loads(brut)

        echecs += cas("la route donne l'identifiant", corps.get("id"), "ma_camp")
        echecs += cas("la route donne le scenario", corps.get("scenario"), "crossbones")
        echecs += cas("la route donne l'equipe, dans l'ordre des sieges",
                      [m["nomHeros"] for m in corps.get("equipe", [])],
                      ["Spider-Man", "She-Hulk"])
        echecs += cas("LE SECRET NE SORT PAS", server_campagne.CLE_SECRET in brut, False)
        echecs += cas("aucune preuve ne sort", "50185" in brut, False)
        echecs += cas("le carnet ne sort pas", "carnet" in corps, False)

        # --- LA GATE : une partie ORDINAIRE ne ressuscite pas la campagne -----
        #
        # Meme dossier, MEME `partieEnCours` arme : seul le moteur change. C'est
        # le defaut du 07/10/2026 (panneau de recompenses sur une victoire sans
        # rapport, salon « equipe fixee par la campagne » sur une table
        # ordinaire). Le temoin positif est juste au-dessus : sans lui, une
        # route qui ne dit plus jamais rien passerait pour correcte.
        serveur.game = jeu_de(False)
        reponse = boucle.run_until_complete(serveur.get_campagne_en_cours(None))
        echecs += cas("partie ordinaire malgre partieEnCours arme : la route ne dit rien",
                      json.loads(reponse.body.decode("utf-8")), {})
        serveur.game = None
        reponse = boucle.run_until_complete(serveur.get_campagne_en_cours(None))
        echecs += cas("aucune partie dans le moteur : la route ne dit rien",
                      json.loads(reponse.body.decode("utf-8")), {})
        from types import SimpleNamespace
        serveur.game = SimpleNamespace(world=None)
        reponse = boucle.run_until_complete(serveur.get_campagne_en_cours(None))
        echecs += cas("moteur sans monde monte : la route ne dit rien",
                      json.loads(reponse.body.decode("utf-8")), {})
        serveur.game = jeu_de(True)
        reponse = boucle.run_until_complete(serveur.get_campagne_en_cours(None))
        echecs += cas("partie de campagne : la route redit la campagne",
                      json.loads(reponse.body.decode("utf-8")).get("id"), "ma_camp")

        # --- L'INTENTION DE L'HOTE : une table ordinaire montee APRES un scenario
        # abandonne. Le moteur tient encore le monde de campagne, mais l'hote qui
        # distribue ses liens (`get_liens_sieges`) monte une partie ordinaire :
        # le salon ne doit pas annoncer « equipe fixee par la campagne ».
        from engine.device.web.server import server_base
        ancien = (list(server_base.SEAT_PASSWORDS.value), Serveur.tient_le_siege)
        server_base.SEAT_PASSWORDS.value = ["a", "b"]
        Serveur.tient_le_siege = lambda self, requete, siege: True
        try:
            reponse = boucle.run_until_complete(serveur.get_liens_sieges(None))
            echecs += cas("l'hote obtient ses liens", json.loads(reponse.body.decode("utf-8")).get("multi"), True)
        finally:
            server_base.SEAT_PASSWORDS.value, Serveur.tient_le_siege = ancien
        reponse = boucle.run_until_complete(serveur.get_campagne_en_cours(None))
        echecs += cas("monde de campagne MAIS table ordinaire declaree : la route ne dit rien",
                      json.loads(reponse.body.decode("utf-8")), {})
        serveur.table_ordinaire = False
        reponse = boucle.run_until_complete(serveur.get_campagne_en_cours(None))
        echecs += cas("le drapeau retombe : la route redit la campagne",
                      json.loads(reponse.body.decode("utf-8")).get("id"), "ma_camp")
    boucle.close()

    # --- /new : le secret ne va que dans une partie de CAMPAGNE -------------
    from engine.device.web.server.server_new_game import GameServerNewGame

    class _Jeu:
        recu = None

        def NewGame(self, nouvelle):
            self.recu = nouvelle

    class Nouveau(GameServerNewGame):
        game = None

    def lancer(regles):
        nouveau = Nouveau.__new__(Nouveau)
        nouveau.game = _Jeu()
        donnees = {
            "campaign_json": "{}", "encounter_set_names": [], "hero_json": [],
            "seed": 1, "timeout": 0, "challenges": [], "rules": regles,
            "campaign_log": {},
        }
        requete = type("R", (), {"rel_url": type("U", (), {"query": {"data": json.dumps(donnees)}})()})()
        nouveau.table_ordinaire = True
        asyncio.new_event_loop().run_until_complete(nouveau.new_game(requete))
        assert nouveau.table_ordinaire is False, "/new doit effacer la table ordinaire declaree"
        return nouveau.game.recu.campaign_log

    with tempfile.TemporaryDirectory() as dossier:
        server_campagne.CAMPAGNES_FOLDER.value = dossier
        ecrire(dossier, "aim_perimee", {
            "code": "aos", "nom": "A.I.M. perimee",
            server_campagne.CLE_SECRET: "50185;50188;50191",
            "partieEnCours": {"scenario": "aim", "depuis": "2026-08-13T10:00:00"},
        })
        echecs += cas("/new ordinaire : le secret n'est pas depose",
                      server_campagne.CLE_CARNET_SECRET in lancer(["v16_all"]), False)
        echecs += cas("/new de campagne : le secret est depose",
                      lancer(["v16_all", "mode_campaign"]).get(server_campagne.CLE_CARNET_SECRET),
                      "50185;50188;50191")

    print("ECHECS : %d" % echecs)
    return 1 if echecs else 0


if __name__ == "__main__":
    sys.exit(main())
