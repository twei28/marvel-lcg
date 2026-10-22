"""Les regles de l'ASSEMBLEE (Kingsfall multi-tables), sans moteur de jeu : le stockage partage entre les tables.

    PYTHONPATH=src ../../.venv-linux/bin/python tools/test_assemblee.py

Chaque test travaille sur son propre fichier SQLite (variable `MCLCG_ASSEMBLEES`).
"""
import os, sys, tempfile, threading

os.environ.setdefault("RELEASE", "1")
import importlib.util
_spec = importlib.util.spec_from_file_location("assemblee", os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src", "game", "operate", "assemblee.py"))
_m = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(_m)
Assemblee, ErreurAssemblee, EN_COURS, VICTOIRE, DEFAITE, ABANDON = _m.Assemblee, _m.ErreurAssemblee, _m.EN_COURS, _m.VICTOIRE, _m.DEFAITE, _m.ABANDON
if False:
    from game.operate.assemblee import Assemblee, ErreurAssemblee, EN_COURS, VICTOIRE, DEFAITE, ABANDON  # noqa: E402

echecs = []


def cas(nom):
    def decor(f):
        dossier = tempfile.mkdtemp()
        os.environ["MCLCG_ASSEMBLEES"] = os.path.join(dossier, "assemblees.db")
        try:
            f()
            print("OK  ", nom)
        except Exception as exc:   # noqa: BLE001
            import traceback
            echecs.append(nom)
            print("ECHEC", nom, "->", repr(exc))
            traceback.print_exc()
        return f
    return decor


@cas("creer : code KING-xxxx, la 1re table est l'organisatrice, seuil 2 par joueur + 2 par groupe")
def _():
    code = Assemblee.Creer("p1", 3, "Spider-Man, Hawkeye, Thor")
    assert code.startswith("KING-") and len(code) == 9
    e = Assemblee.Etat(code)
    assert e["organisateur"] == "p1" and e["joueurs"] == 3 and e["seuil"] == 2 * 3 + 2 * 1 and not e["retournee"] and not e["terminee"]


@cas("rejoindre : le seuil suit les groupes (1 groupe de 3 + 2 groupes de 4 -> 28, exemple du livret)")
def _():
    code = Assemblee.Creer("p1", 3)
    Assemblee.Rejoindre(code, "p2", 4)
    Assemblee.Rejoindre(code.lower(), "p3", 4)          # le code se recopie a la main : casse indifferente
    assert Assemblee.Etat(code)["seuil"] == 28 and len(Assemblee.Etat(code)["groupes"]) == 3


@cas("rejoindre : code inconnu, table deja inscrite, cinquieme groupe : refus")
def _():
    code = Assemblee.Creer("p1", 2)
    for table in ("p2", "p3", "p4"):
        Assemblee.Rejoindre(code, table, 2)
    for args in (("KING-ZZZZ", "p9", 2), (code, "p2", 2), (code, "p5", 2), ("", "p5", 2)):
        try:
            Assemblee.Rejoindre(*args)
        except ErreurAssemblee:
            continue
        raise AssertionError(f"{args} aurait du etre refuse")


@cas("verser : le total s'accumule, l'assemblee se retourne UNE fois au seuil, pas avant")
def _():
    code = Assemblee.Creer("p1", 3)          # seuil 8
    assert not Assemblee.VerserJetons(code, 7)["retournee"]
    e = Assemblee.VerserJetons(code, 1)
    assert e["retournee"] and e["total_jetons"] == 8
    v = e["version"]
    e2 = Assemblee.VerserJetons(code, 0)
    assert e2["retournee"] and e2["version"] == v      # rien ne change, la version ne bouge pas


@cas("action d'assemblee : un jeton envoye arrive une seule fois chez la cible, jamais chez une table finie ou inconnue")
def _():
    code = Assemblee.Creer("p1", 2)
    Assemblee.Rejoindre(code, "p2", 2)
    assert Assemblee.EnvoyerJeton(code, "p2") and Assemblee.EnvoyerJeton(code, "p2")
    assert Assemblee.PrendreLesJetonsRecus(code, "p2") == 2
    assert Assemblee.PrendreLesJetonsRecus(code, "p2") == 0
    assert Assemblee.PrendreLesJetonsRecus(code, "p1") == 0
    assert not Assemblee.EnvoyerJeton(code, "p9")
    Assemblee.Terminer(code, "p2", True)
    assert not Assemblee.EnvoyerJeton(code, "p2")


@cas("le Roi : victoire = 1 degat par joueur, defaite et abandon = 1 menace par joueur, une table ne compte qu'UNE fois")
def _():
    code = Assemblee.Creer("p1", 3)
    Assemblee.Rejoindre(code, "p2", 2)
    Assemblee.Rejoindre(code, "p3", 4)
    e = Assemblee.Terminer(code, "p1", True)
    assert (e["degats"], e["menace"], e["terminee"]) == (3, 0, False)
    Assemblee.Terminer(code, "p1", False)               # deja finie : ignoree
    assert (Assemblee.Etat(code)["degats"], Assemblee.Etat(code)["menace"]) == (3, 0)
    e = Assemblee.Terminer(code, "p2", False)
    assert (e["degats"], e["menace"]) == (3, 2)
    e = Assemblee.Terminer(code, "p3", False, abandon=True)
    assert (e["degats"], e["menace"], e["terminee"]) == (3, 6, True) and not e["gagnee"]
    assert [g["etat"] for g in e["groupes"]] == [VICTOIRE, DEFAITE, ABANDON]


@cas("le Roi : l'assemblee gagne si les degats egalent ou depassent la menace, a la fin de TOUTES les parties")
def _():
    code = Assemblee.Creer("p1", 3)
    Assemblee.Rejoindre(code, "p2", 3)
    Assemblee.Terminer(code, "p1", True)
    assert not Assemblee.Etat(code)["gagnee"]           # p2 encore en cours : pas de verdict
    e = Assemblee.Terminer(code, "p2", False)
    assert e["terminee"] and e["degats"] == 3 and e["menace"] == 3 and e["gagnee"]      # egalite : gagne


@cas("concurrence : 4 tables versent en meme temps, aucun jeton perdu")
def _():
    code = Assemblee.Creer("p1", 4)
    fils = [threading.Thread(target=lambda: [Assemblee.VerserJetons(code, 1) for _ in range(25)]) for _ in range(4)]
    [f.start() for f in fils]
    [f.join() for f in fils]
    assert Assemblee.Etat(code)["total_jetons"] == 100

@cas("fermeture d'une table : defaite de son groupe dans chaque assemblee ou il joue encore, une table deja finie ne compte pas deux fois")
def _():
    a = Assemblee.Creer("p1", 2)
    Assemblee.Rejoindre(a, "p2", 3)
    b = Assemblee.Creer("p2", 4)           # p2 est aussi dans une 2e assemblee (apres la fin d'une partie, une table en rouvre une)
    Assemblee.Terminer(a, "p1", True)
    assert Assemblee.AbandonnerTable("p2") == 2
    ea, eb = Assemblee.Etat(a), Assemblee.Etat(b)
    assert (ea["degats"], ea["menace"], ea["terminee"], ea["gagnee"]) == (2, 3, True, False)
    assert (eb["degats"], eb["menace"], eb["terminee"]) == (0, 4, True)
    assert Assemblee.AbandonnerTable("p2") == 0 and Assemblee.AbandonnerTable("inconnue") == 0
    assert [g["etat"] for g in ea["groupes"]] == [VICTOIRE, ABANDON]


print("\nBILAN :", "tout passe" if not echecs else f"{len(echecs)} echec(s)")
sys.exit(1 if echecs else 0)
