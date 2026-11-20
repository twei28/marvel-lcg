# Cas test_capacites de KINGSFALL MULTI-TABLES (assemblees, « pods »). Prefixe `[pod]`. Decisions : .planning/mcdc-punisher/decisions-multi-tables.md.
# Cette table = `p1` (1 joueur, Spider-Man). Une AUTRE table `p2` (2 joueurs) est dans l'assemblee `KING-TEST` : seuil de Longue vie = 2 x 3 + 2 x 2 = 10.
# L'etat des autres tables se pose AVANT la mise en place (cle `assemblee_avant` du harnais) ; le verificateur lit le stockage commun APRES.
import importlib.util, os
_s = importlib.util.spec_from_file_location("cp", os.path.join(os.path.dirname(__file__), "campagne_punisher.py"))
_cp = importlib.util.module_from_spec(_s); _s.loader.exec_module(_cp)

CODE = "KING-TEST"
AVANT = [{"creer": ["p1", 1], "code": CODE}, {"rejoindre": ["p2", 2]}]
REGLES = ["assemblee_%s_p1" % CODE]
HEROS_K = _cp.HEROS_K


def _p(nom, pourquoi, mise, declencher, attendu, avant=(), base=None, **cle):
    cle.setdefault("verifier", "pod_etat")
    return _cp._k("[pod] " + nom, pourquoi, mise, declencher, attendu, regles=REGLES, assemblee_avant=[*(AVANT if base is None else base), *avant], **cle)


# DEUX TABLES DE DEUX (question de l'utilisateur, 22/10/2026) : 2 groupes x 2 joueurs = 4 joueurs -> seuil 2 x 4 + 2 x 2 = 12.
DEUX_DE_DEUX = [{"creer": ["p1", 2], "code": CODE}, {"rejoindre": ["p2", 2]}]


CAS = [
    _p("Setup en assemblee : Longue vie (pu149a), Power to the People (pu148, 1 compteur) ET Le Roi (pu151) sont en jeu chez cette table (miroir)",
       "decision 3 : Longue vie et Le Roi chez TOUS", [], [],
       {"en_jeu": ["pu149a", "pu148", "pu151"], "compteurs": [["pu148", "counter", 1]], "assemblee": {"total_jetons": 0, "retournee": False}}),
    _p("fin de phase des joueurs : les jetons de Public Support vont au total COMMUN (2), le miroir de Longue vie les montre, pas de retournement (seuil 10)",
       "« move each support counter from your Public Support to here » : ici = le total de l'assemblee",
       [HEROS_K, "Puzzle.Counter('60163a', 'support', 2)"], ["Puzzle.EndPlayerPhase()"],
       {"compteurs": [["60163a", "support", 0], ["pu149a", "support", 2]], "en_jeu": ["pu149a"], "assemblee": {"total_jetons": 2, "retournee": False}}),
    _p("le total COMMUN franchit le seuil (9 verses par l'autre table + 1 par celle-ci = 10) : Longue vie se retourne en A bas, Public Support de CETTE table = 2 x 1 + 3 = 5",
       "« if there are 2[per_hero]+2[per_group] counters here, flip » : tous groupes confondus", 
       [HEROS_K, "Puzzle.Counter('60163a', 'support', 1)"], ["Puzzle.EndPlayerPhase()"],
       {"en_jeu": ["pu149b"], "hors_jeu": ["pu149a"], "compteurs": [["60163a", "support", 5]], "assemblee": {"total_jetons": 10, "retournee": True}}, avant=[{"verser": 9}]),
    _p("TEMOIN : 8 + 1 = 9 < 10 -> pas de retournement (le seuil est celui de l'ASSEMBLEE, pas celui de cette table : 2 x 1 + 2 = 4 serait deja depasse)",
       "un seuil local retournerait la carte a tort", [HEROS_K, "Puzzle.Counter('60163a', 'support', 1)"], ["Puzzle.EndPlayerPhase()"],
       {"en_jeu": ["pu149a"], "hors_jeu": ["pu149b"], "compteurs": [["60163a", "support", 0]], "assemblee": {"total_jetons": 9, "retournee": False}}, avant=[{"verser": 8}]),
    _p("une AUTRE table a fait franchir le seuil : a la phase du Mechant de cette table, Longue vie se retourne et Public Support est remis a 2 x 1 + 3 = 5",
       "A bas : « Each group resets the number of support counters on their Public Support »", [HEROS_K, "Puzzle.Counter('60163a', 'support', 1)"],
       ["Puzzle.AssembleeAutreTable('verser', 10)", "Puzzle.BeginVillainPhase()"],
       {"en_jeu": ["pu149b"], "hors_jeu": ["pu149a"], "compteurs": [["60163a", "support", 5]], "assemblee": {"retournee": True}}),
    _p("Action d'assemblee vers l'AUTRE groupe (p2) : 1 jeton quitte Public Support de cette table et attend chez p2",
       "« Choose a group in the pod. Move 1 counter from your Public Support to their Power to the People. »",
       [HEROS_K, "Puzzle.Counter('60163a', 'support', 2)"], ["Puzzle.Action('pu149a', 'Action')"],
       {"compteurs": [["60163a", "support", 1], ["pu148", "counter", 1]], "assemblee": {"recus": {"p2": 1, "p1": 0}}}, preferer_option="p2"),
    _p("Action d'assemblee vers SOI-MEME : le jeton arrive tout de suite sur Power to the People de cette table (1 -> 2)", "le groupe choisi peut etre le sien",
       [HEROS_K, "Puzzle.Counter('60163a', 'support', 2)"], ["Puzzle.Action('pu149a', 'Action')"],
       {"compteurs": [["60163a", "support", 1], ["pu148", "counter", 2]], "assemblee": {"recus": {"p2": 0, "p1": 0}}}, preferer_option="this_table"),
    _p("des jetons envoyes par l'autre groupe arrivent sur Power to the People de cette table (1 + 2 = 3) a sa prochaine synchronisation, et ne sont poses qu'UNE fois",
       "reception des Actions d'assemblee des autres groupes", [HEROS_K], ["Puzzle.AssembleeAutreTable('envoyer', 'p1')", "Puzzle.AssembleeAutreTable('envoyer', 'p1')", "Puzzle.BeginVillainPhase()", "Puzzle.BeginVillainPhase()"],
       {"compteurs": [["pu148", "counter", 3]], "assemblee": {"recus": {"p1": 0}}}),
    _p("Le Roi (miroir) montre les degats communs : p2 (2 joueurs) a vaincu le Caid -> 2 degats ; et la menace commune 0", "« When Kingpin is defeated in this pod, place 1 damage here for each player in that game »",
       [HEROS_K], ["Puzzle.AssembleeAutreTable('terminer', 'p2', True)", "Puzzle.BeginVillainPhase()"],
       {"compteurs": [["pu151", "king_damage", 2], ["pu151", "king_threat", 0]], "assemblee": {"degats": 2, "menace": 0}}),
    _p("fin de partie : CETTE table gagne -> 1 degat (1 joueur) sur Le Roi, chez tout le monde ; la table est marquee gagnee", "Kingpin vaincu = 1 degat par joueur du groupe",
       [], ["Puzzle.Win()"], {"assemblee": {"degats": 1, "menace": 0, "etats": {"p1": 1, "p2": 0}}}),
    _p("fin de partie : CETTE table perd -> 1 menace (1 joueur) sur Le Roi ; l'assemblee n'est pas terminee tant que p2 joue", "« When the players lose a game in this pod, place 1 threat here for each player in that game »",
       [], ["Puzzle.Lose()"], {"assemblee": {"degats": 0, "menace": 1, "etats": {"p1": 2, "p2": 0}, "terminee": False}}),
    _p("DEUX TABLES DE DEUX : 11 jetons au total (10 de l'autre table + 1 ici) < 12 -> pas de retournement",
       "seuil = 2 x 4 joueurs + 2 x 2 groupes = 12", [HEROS_K, "Puzzle.Counter('60163a', 'support', 1)"], ["Puzzle.EndPlayerPhase()"],
       {"en_jeu": ["pu149a"], "compteurs": [["60163a", "support", 0]], "assemblee": {"total_jetons": 11, "retournee": False}},
       base=DEUX_DE_DEUX, avant=[{"verser": 10}], heros2="spider_man"),
    _p("DEUX TABLES DE DEUX : 12 jetons -> Longue vie se retourne ; A bas remet Public Support de cette table (2 joueurs) a 2 x 2 + 3 = 7",
       "reset a 2 par joueur DE CE GROUPE + 3", [HEROS_K, "Puzzle.Counter('60163a', 'support', 2)"], ["Puzzle.EndPlayerPhase()"],
       {"en_jeu": ["pu149b"], "hors_jeu": ["pu149a"], "compteurs": [["60163a", "support", 7]], "assemblee": {"total_jetons": 12, "retournee": True}},
       base=DEUX_DE_DEUX, avant=[{"verser": 10}], heros2="spider_man"),
    _p("DEUX TABLES DE DEUX : victoire de cette table = 2 degats (ses 2 joueurs), victoire de l'autre = 2 aussi -> degats 4 >= menace 0, l'assemblee gagne a la fin des DEUX parties",
       "« When Kingpin is defeated in this pod, place 1 damage here for each player in that game »", [HEROS_K], ["Puzzle.AssembleeAutreTable('terminer', 'p2', True)", "Puzzle.Win()"],
       {"assemblee": {"degats": 4, "menace": 0, "terminee": True, "gagnee": True}}, base=DEUX_DE_DEUX, heros2="spider_man"),
    _p("DEUX TABLES DE DEUX : une victoire (2 degats) et une defaite (2 menaces) -> egalite -> l'assemblee GAGNE (« equal to or greater »)",
       "2 >= 2", [HEROS_K], ["Puzzle.AssembleeAutreTable('terminer', 'p2', True)", "Puzzle.Lose()"],
       {"assemblee": {"degats": 2, "menace": 2, "terminee": True, "gagnee": True}}, base=DEUX_DE_DEUX, heros2="spider_man"),
]

VERIFICATIONS = r'''
def pod_etat(monde, aides):
    from game.operate.assemblee import Assemblee
    cas = aides["cas"]
    attendu = cas.get("attendu") or {}
    soucis = []
    voulu = attendu.get("assemblee")
    if voulu is not None:
        etat = Assemblee.Etat("KING-TEST")
        if etat is None:
            soucis.append("assemblee KING-TEST introuvable")
        else:
            for cle in ("total_jetons", "retournee", "degats", "menace", "terminee", "gagnee"):
                if cle in voulu and etat[cle] != voulu[cle]:
                    soucis.append(f"assemblee {cle} = {etat[cle]} (attendu {voulu[cle]})")
            par_table = {g["tab"]: g for g in etat["groupes"]}
            for tab, n in (voulu.get("recus") or {}).items():
                if par_table[tab]["recus"] != n:
                    soucis.append(f"jetons en attente chez {tab} = {par_table[tab]['recus']} (attendu {n})")
            for tab, e in (voulu.get("etats") or {}).items():
                if par_table[tab]["etat"] != e:
                    soucis.append(f"etat de {tab} = {par_table[tab]['etat']} (attendu {e})")
    reste = {k: v for k, v in attendu.items() if k != "assemblee"}
    cas["attendu"] = reste
    try:
        ok, msg = etat_attendu(monde, aides)
    finally:
        cas["attendu"] = attendu
    if not ok:
        soucis.append(msg)
    return (False, " ; ".join(soucis)) if soucis else (True, "assemblee conforme")
'''
