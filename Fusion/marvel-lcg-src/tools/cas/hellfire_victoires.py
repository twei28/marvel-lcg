# Cas « VICTOIRE » des cinq scenarios de la campagne Hellfire Hunt (prefixe `hf`) : y a-t-il, avec les cartes imprimees, un chemin de jeu
# qui GAGNE la partie ? Le pilote automatique ne sait pas defaire Captured by Hellfire! (Black King) ni vider Nova's Psychic Puppetry (Torn) :
# ses 0 % ne prouvent rien. Ces cas jouent la partie par le MOTEUR (attaques et contres de heros reels `Puzzle.Attack` / `Puzzle.Thwart`,
# fins de round, avancees du complot), en ne forcant que l'etat de depart (PV pre-endommages, menaces posees) : jamais la victoire elle-meme.
# Le verificateur est `hfn_etat` (tools/cas/hellfire_cassandra_nova.py) : `gagnee` / `partie_finie` / `en_victoire` / `absents` / `menace_de`.
#
#  - `spider_man` demarre en ALTER-EGO : `Puzzle.ChangeForm('01001a')` le passe en HEROS ;
#  - `Puzzle.Ready('01001a')` entre deux actions du meme heros (une attaque ou un contre epuise le heros) ;
#  - 01105 = « Bomb Scare » (aucune capacite de boost), remplissage inoffensif.
HEROS = "Puzzle.ChangeForm('01001a')"


def deck(*cartes, remplissage=14):
    ids = list(cartes) + ["01105"] * remplissage
    return ["Puzzle.EmptyEncounterDiscardPile()", "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck(%s)" % ", ".join("'%s'" % c for c in reversed(ids))]


def _c(nom, pourquoi, mise, declencher, attendu, **cle):
    attendu = dict(attendu)
    for _k in ("questions_presentes", "questions_absentes"):
        if _k in attendu:
            cle[_k] = attendu.pop(_k)
    cas = {"nom": "[hf] hf-victoire " + nom, "pourquoi": pourquoi, "scenario": cle.pop("scenario"),
           "heros": cle.pop("heros", "spider_man"), "mise_en_place": ["Puzzle.EmptyHand()"] + list(mise), "declencher": declencher,
           "verifier": cle.pop("verifier", "hfv_etat"), "attendu": attendu}
    cas.update(cle)
    cas.setdefault("main_exclusive", ["01090"])
    return cas


def frappe(cible):
    """Un tour de heros : le heros se redresse et attaque."""
    return ["Puzzle.Ready('01001a')", "Puzzle.Attack('01001a')"]


CAS = []

R = "Puzzle.Ready('01001a')"
T = "Puzzle.Thwart('01001a')"
A = "Puzzle.Attack('01001a')"

CAS += [
    # ===================================================================== Black King
    _c("Black King (standard, 1 joueur) : Captured by Hellfire! contree a la main (5 -> 0), le captif est libere, le complot avance (2A), puis Shaw I et Shaw II vaincus par des attaques -> VICTOIRE",
       "le pilote ne defait jamais Captured by Hellfire! : preuve par le MOTEUR que la partie est gagnable. Seuls les PV de Shaw sont pre-endommages (13 -> 1 PV, 15 -> 1 PV)",
       [HEROS, "Puzzle.Damage('hf201', 12)"] + deck("01105"),
       [T, R, T, R, T, R, T, R, T, R, A, R, "Puzzle.Damage('hf202', 13)", A],
       {"gagnee": True, "partie_finie": True, "en_victoire": ["hf206"]},
       scenario="hellfire_black_king", cibles=["hf206", "hf201", "hf202"], accepter_choix=True),
]

VERIFICATIONS = r'''
def hfv_etat(monde, aides):
    """hfn_etat + un instantane d'etat (cartes de jeu a PV/menace) ecrit dans /tmp/hffv_dump_<CAS_PREFIX><index>.txt pour lire un cas rouge."""
    import os as _os
    lignes = []
    try:
        lignes.append(f"is_game_over={getattr(monde, 'is_game_over', None)} round={getattr(monde, 'round_id', None)}")
        go = getattr(monde, "game_over", None)
        if go is not None:
            lignes.append(f"players_won={getattr(go, 'players_won', None)}")
        for objet in monde.object_manager.card_dict.values():
            f = getattr(objet, "face", None) or objet
            cid = getattr(getattr(f, "paper", None), "card_id", None)
            try:
                en_jeu = f.IsInPlay()
            except Exception:
                en_jeu = False
            if cid and en_jeu:
                lignes.append(f"{cid} {getattr(f, 'name', '')} PV={getattr(f, 'health', None)}/{getattr(f, 'max_health', None)} menace={getattr(f, 'threat', None)}")
        vic = [getattr(getattr(f, "paper", None), "card_id", None) for f in monde.victory_display.Get(True)] if hasattr(monde, "victory_display") else None
        lignes.append(f"victoire={vic}")
    except Exception as e:
        lignes.append(f"ERREUR dump {e!r}")
    try:
        open(f"/tmp/hffv_dump_{_os.environ.get('CAS_PREFIX', '')}{aides['index']}.txt", "w").write("\n".join(lignes))
    except Exception:
        pass
    return hfn_etat(monde, aides)
'''

CAS += [
    _c("Black King (expert, 1 joueur) : Captured by Hellfire! contree a la main, Shaw II (15 PV) puis Shaw III (17 PV) vaincus -> VICTOIRE",
       "expert : Shaw II et III ; meme chemin que le standard",
       [HEROS, "Puzzle.Damage('hf202', 14)"] + deck("01105"),
       [T, R, T, R, T, R, T, R, T, R, A, R, "Puzzle.Damage('hf203', 16)", A],
       {"gagnee": True, "partie_finie": True, "en_victoire": ["hf206"]},
       scenario="hellfire_black_king_expert", cibles=["hf206", "hf202", "hf203"], accepter_choix=True),
    _c("Black King (standard) : TEMOIN, Shaw I vaincu mais Shaw II intact -> la partie n'est PAS gagnee",
       "contre-cas de calibrage : la victoire exige le DERNIER stade",
       [HEROS, "Puzzle.Damage('hf201', 12)"] + deck("01105"),
       [A],
       {"gagnee": False, "partie_finie": False}, scenario="hellfire_black_king", cibles=["hf201"], accepter_choix=True),
    _c("Black King (standard) : on peut vaincre Shaw SANS vider Captured by Hellfire! (chemin court, mesure)",
       "mesure : Captured by Hellfire! n'est pas necessaire a la victoire (le texte n'impose rien) ; elle n'est qu'un bonus de captifs",
       [HEROS, "Puzzle.Damage('hf201', 12)"] + deck("01105"),
       [A, R, "Puzzle.Damage('hf202', 13)", A],
       {"gagnee": True, "partie_finie": True}, scenario="hellfire_black_king", cibles=["hf201", "hf202"], accepter_choix=True),
    # ===================================================================== White Queen
    _c("White Queen (standard, 1 joueur) : White Queen A1 (12 PV) puis A2 (15 PV) vaincues par des attaques -> VICTOIRE",
       "le chemin gagnant du scenario hellfire_white_queen par le moteur (PV pre-endommages)",
       [HEROS, "Puzzle.Damage('hf101a', 11)"] + deck("01105"),
       [A, R, "Puzzle.Damage('hf102a', 14)", A],
       {"gagnee": True, "partie_finie": True}, scenario="hellfire_white_queen", cibles=["hf101a", "hf102a"], accepter_choix=True),
    _c("White Queen (expert, 1 joueur) : White Queen A2 (15 PV) puis A3 (19 PV) vaincues -> VICTOIRE",
       "expert : stades 2 et 3",
       [HEROS, "Puzzle.Damage('hf102a', 14)"] + deck("01105"),
       [A, R, "Puzzle.Damage('hf103a', 18)", A],
       {"gagnee": True, "partie_finie": True}, scenario="hellfire_white_queen_expert", cibles=["hf102a", "hf103a"], accepter_choix=True),
    # ===================================================================== Black Queen
    _c("Black Queen (standard, 1 joueur) : Selene I (12 PV) puis Selene II (14 PV, Toughness) vaincues -> VICTOIRE",
       "Toughness : Selene II entre avec un statut tough, un premier degat le retire sans blesser (`Damage` 1), puis les PV",
       [HEROS, "Puzzle.Damage('hf401', 11)"] + deck("01105"),
       [A, R, "Puzzle.Damage('hf402', 1)", "Puzzle.Damage('hf402', 12)", A],
       {"gagnee": True, "partie_finie": True}, scenario="hellfire_black_queen", cibles=["hf401", "hf402"], accepter_choix=True),
    _c("Black Queen (expert, 1 joueur) : Selene II (14 PV) puis Selene III (17 PV, Steady, Toughness) vaincues -> VICTOIRE",
       "expert : stades 2 et 3",
       [HEROS, "Puzzle.Damage('hf402', 1)", "Puzzle.Damage('hf402', 12)"] + deck("01105"),
       [A, R, "Puzzle.Damage('hf403', 1)", "Puzzle.Damage('hf403', 15)", A],
       {"gagnee": True, "partie_finie": True}, scenario="hellfire_black_queen_expert", cibles=["hf402", "hf403"], accepter_choix=True),
    # ===================================================================== Cassandra Nova
    _c("Cassandra Nova (standard, 1 joueur) : Nova I (15 PV) puis Nova II (18 PV, Steady) vaincues par des attaques -> VICTOIRE",
       "le chemin gagnant du scenario par le moteur",
       [HEROS, "Puzzle.Damage('hf601', 14)"] + deck("01105"),
       [A, R, "Puzzle.Damage('hf602', 17)", A],
       {"gagnee": True, "partie_finie": True}, scenario="hellfire_cassandra_nova", cibles=["hf601", "hf602"], accepter_choix=True),
    _c("Cassandra Nova (expert, 1 joueur) : Nova II (18 PV) puis Nova III (20 PV, Stalwart) vaincues -> VICTOIRE",
       "expert : stades 2 et 3",
       [HEROS, "Puzzle.Damage('hf602', 17)"] + deck("01105"),
       [A, R, "Puzzle.Damage('hf603', 19)", A],
       {"gagnee": True, "partie_finie": True}, scenario="hellfire_cassandra_nova_expert", cibles=["hf602", "hf603"], accepter_choix=True),
]

def _elite(cid, pv):
    """Un sbire ELITE HELLFIRE entre en jeu, ramene a 1 PV (un 1er degat ote d'abord un eventuel statut tough : hf341 Tenace) ou 2, et le heros le vainc (Nova's Psychic Puppetry : -5 menaces)."""
    return ["Puzzle.PutIntoPlay('%s')" % cid, "Puzzle.Damage('%s', 1)" % cid, "Puzzle.Damage('%s', %d)" % (cid, max(pv - 2, 0)), A, R]


CAS += [
    # ===================================================================== Torn
    _c("Torn (standard, 1 joueur) : trois ELITE HELLFIRE vaincus (Puppetry 13 -> 8 -> 3 -> 0, elle se retourne), deux de plus (13 -> 8 -> 3), trois contres -> Emma s'echappe : VICTOIRE",
       "le pilote ne sait pas vider Nova's Psychic Puppetry : preuve par le MOTEUR que la partie est gagnable (Hinder 5 puis 12 par joueur, -5 par ELITE HELLFIRE vaincu, contres)",
       [HEROS] + deck("01105"),
       _elite("hf351", 2) + _elite("hf331", 6) + _elite("hf341", 4) + _elite("hf301", 8) + _elite("hf302", 4) + [T, R, T, R, T],
       {"gagnee": True, "partie_finie": True}, scenario="hellfire_torn",
       cibles=["hf351", "hf331", "hf341", "hf301", "hf302", "hf504a", "hf504b"], accepter_choix=True, verifier="hfv_etat"),
    _c("Torn (standard, 1 joueur) : TEMOIN, trois ELITE seulement (Puppetry 13 -> 0, retournee a 13) -> PAS gagnee",
       "contre-cas : la face B doit etre videe aussi",
       [HEROS] + deck("01105"),
       _elite("hf351", 2) + _elite("hf331", 6) + _elite("hf341", 4),
       {"gagnee": False, "partie_finie": False, "menace_de": [["hf504b", 13]]}, scenario="hellfire_torn",
       cibles=["hf351", "hf331", "hf341"], accepter_choix=True),
]

CAS += [
    _c("Torn (expert, 1 joueur) : meme chemin gagnant (Emma Frost B1 : 8 PV, face infinie) -> Emma s'echappe : VICTOIRE",
       "expert : Emma Frost (B1) ; la Puppetry est identique",
       [HEROS] + deck("01105"),
       _elite("hf351", 2) + _elite("hf331", 6) + _elite("hf341", 4) + _elite("hf301", 8) + _elite("hf302", 4) + [T, R, T, R, T],
       {"gagnee": True, "partie_finie": True}, scenario="hellfire_torn_expert",
       cibles=["hf351", "hf331", "hf341", "hf301", "hf302", "hf504a", "hf504b"], accepter_choix=True),
]

CAS += [
    _c("Cassandra Nova : DEUX Exploding Their Head (hf608 + hf609) en jeu et deux allies de cout 2 : la fin de tour ne bloque pas (ordre des Reponses forcees), le jeu continue",
       "blocage de pilote releve en autoplay (captain_marvel, graine 3) : la question « Forced abilities would initiate at the same moment » revenait a l'identique ; preuve que la partie avance avec un choix reel",
       [HEROS, "Puzzle.PutIntoPlay('01002', under_control=True)", "Puzzle.PutIntoPlay('01081', under_control=True)", "Puzzle.PutIntoPlay('hf608')", "Puzzle.PutIntoPlay('hf609')"] + deck("01105"),
       ["Puzzle.EndPlayerTurn()"],
       {"partie_finie": False}, scenario="hellfire_cassandra_nova", accepter_choix=True),
]
