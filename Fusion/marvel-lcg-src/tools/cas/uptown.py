# Cas test_capacites de l'extension UPTOWN (PU-10, 22/10/2026) : 3 lieux (pu023 Upper West Side, pu024 Harlem, pu025 The Bronx), 3 pistes (pu026 West Side Warrior,
# pu027 The Harlem Hustle, pu028 Bronx Bombered) et la mise en place (4e rangee, 4 CAPO, 12 pistes). Prefixe `[upt]`.
# Ville du banc : la rangee Uptown est la LIGNE 0 de la grille d'essai (les cases se lisent `(ligne, colonne)`), puis les 3 rangees de la grille ; le vrai scenario
# (`the_big_apple_uptown`) la numerote -1 (voir `the_big_apple/__init__.py`). Verificateurs : `pist_etat` (pistes en victoire) et `upt_etat` (mise en place reelle).
FORME_HEROS = "Puzzle.ChangeForm('01001b')"
RIEN = ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01105', '01105', '01105')"]
SANS_BOOST = ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01105', '01105', '01105', '01105', '01105', '01105')"]
GRILLE_UP = [["pu023", "pu024", "pu025"], ["pu030", "pu031", "pu032"], ["pu033", "pu034", "pu035"], ["pu036", "pu037", "pu038"]]
G = repr(GRILLE_UP)
CASE = {"pu023": (0, 0), "pu024": (0, 1), "pu025": (0, 2), "pu030": (1, 0), "pu031": (1, 1), "pu032": (1, 2)}
BOOST1 = ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01105', '01105', '01105', '01105', '01101')"]


def ville(lieu, communs=("pu005", "pu006")):
    return [*["Puzzle.PutIntoPlay('%s')" % x for x in communs],
            "Puzzle.InstallerVille(%s, %s, en_jeu=True)" % (G, repr(CASE[lieu])),
            *["Puzzle.MoveCardToGameArea('%s', 1)" % x for x in communs]]


def _l(nom, pourquoi, lieu, avant, declencher, attendu, apres=(), **cle):
    """Un LIEU Uptown : le joueur est sur la case `lieu` de la grille d'essai ; ce qui touche les degats et les sbires vient AVANT la ville."""
    cas = {"nom": "[upt] " + nom, "pourquoi": pourquoi, "scenario": "rhino", "heros": "spider_man",
           "mise_en_place": [*RIEN, FORME_HEROS, *avant, *ville(lieu), *apres], "declencher": declencher, "verifier": "etat_attendu",
           "attendu": attendu, "main_exclusive": ["01088"]}
    cas.update(cle)
    return cas


def _p(nom, pourquoi, lieu, piste, avant, declencher, attendu, suivante="pu040", deck=None, **cle):
    """Une PISTE Uptown : posee dans l'aire du joueur, paquet LEADS a une carte (`suivante`)."""
    apres = [x for x in avant if x.startswith(("Puzzle.PlaceCounters", "Puzzle.MoveCardToGameArea", "Puzzle.SetThreat"))]
    avant = [x for x in avant if x not in apres]
    cas = {"nom": "[upt] " + nom, "pourquoi": pourquoi, "scenario": "rhino", "heros": "spider_man",
           "mise_en_place": [*(RIEN if deck is None else deck), FORME_HEROS, *avant, *ville(lieu), "Puzzle.PutIntoPlay('%s', under_control=True)" % piste,
                             "Puzzle.CreateLeadsDeck('%s')" % suivante, *apres],
           "declencher": declencher, "verifier": "pist_etat", "attendu": attendu, "main_exclusive": ["01088"]}
    cas.update(cle)
    return cas


def _fin(piste, **plus):
    """attendu d'une piste TERMINEE : en victoire, la suivante revelee (pu040), 1 carte piochee (main 1 + 1)."""
    d = {"victoire": [piste], "en_jeu": ["pu040"], "taille_main": 2}
    d.update(plus)
    return d


PLUS1 = "+1_to_that_power_for_this_use"
MOINS1 = "-1_to_that_power_for_this_use"

CAS = [
    # ------------------------------------------------------------------ pu023 Upper West Side (U1) : Hero Interrupt +1 / -1
    _l("pu023 Upper West Side : le heros attaque (ATK 2), choisit +1 -> Shocker (3 PV) est vaincu",
       "« When a hero uses a basic power, choose to get either +1 or -1 to that power for this use » : 2 + 1 = 3 degats",
       "pu023", ["Puzzle.PutIntoPlay('01103')"], ["Puzzle.Attack('01001a')"], {"hors_jeu": ["01103"]},
       choisir_option=PLUS1, cibles=["01103"]),
    _l("pu023 Upper West Side : le heros choisit -1 -> Shocker ne subit que 1 degat", "2 - 1 = 1 degat", "pu023",
       ["Puzzle.PutIntoPlay('01103')"], ["Puzzle.Attack('01001a')"], {"degats": [["01103", 1]]},
       choisir_option=MOINS1, cibles=["01103"]),
    _l("pu023 Upper West Side, TEMOIN : le heros est a Harlem (MEME rangee, pas au lieu) -> aucun bonus, 2 degats", "R3 : on n'interagit qu'avec le lieu occupe",
       "pu024", ["Puzzle.PutIntoPlay('01103')"], ["Puzzle.Attack('01001a')"], {"degats": [["01103", 2]]},
       choisir_option=PLUS1, cibles=["01103"]),
    _l("pu023 Upper West Side, TEMOIN D'EPUISEMENT : deux attaques dans la meme phase (+1 les deux fois demande) -> 3 + 2 = 5 degats a Whirlwind (6 PV), pas 6",
       "« Limit once per phase » : la seconde utilisation est refusee", "pu023", ["Puzzle.PutIntoPlay('01130')"],
       ["Puzzle.Attack('01001a')", "Puzzle.Ready('01001a')", "Puzzle.Attack('01001a')"], {"degats": [["01130", 5]]},
       choisir_option=PLUS1, cibles=["01130"]),
    _l("pu023 Upper West Side : le pouvoir DEF aussi (Melter ATK 3 contre DEF 3, choisit -1) -> DEF 2, le heros subit 1 degat",
       "« a hero uses a basic power » : ATK, THW et DEF ; -1 sur la defense", "pu023", ["Puzzle.PutIntoPlay('01132')", *SANS_BOOST],
       ["Puzzle.Attack('01132', defender='01001a')"], {"degats_identite": 1}, choisir_option=MOINS1),
    # ------------------------------------------------------------------ pu024 Harlem (U2) : Response, redresser un allie
    _l("pu024 Harlem : le heros attaque, un allie EPUISE a Harlem se redresse", "« After an identity uses a basic power, ready an ally at this location »",
       "pu024", ["Puzzle.PutIntoPlay('01103')", "Puzzle.PutIntoPlay('01075', under_control=True)", "Puzzle.Exhaust('01075')"],
       ["Puzzle.Attack('01001a')"], {"pret": ["01075"]}, cibles=["01103"], accepter_choix=True),
    _l("pu024 Harlem, TEMOIN : le heros est a Upper West Side (meme rangee, pas au lieu) -> l'allie reste epuise", "R3 : seul le lieu occupe",
       "pu023", ["Puzzle.PutIntoPlay('01103')", "Puzzle.PutIntoPlay('01075', under_control=True)", "Puzzle.Exhaust('01075')"],
       ["Puzzle.Attack('01001a')"], {"exhausted": ["01075"]}, cibles=["01103"], accepter_choix=True),
    _l("pu024 Harlem, TEMOIN D'EPUISEMENT : deux attaques dans la meme phase, deux allies epuises -> UN SEUL se redresse (le 1er) : le 2e reste epuise",
       "« Limit once per phase »", "pu024",
       ["Puzzle.PutIntoPlay('01130')", "Puzzle.PutIntoPlay('01075', under_control=True)", "Puzzle.PutIntoPlay('01076', under_control=True)",
        "Puzzle.Exhaust('01075', '01076')"],
       ["Puzzle.Attack('01001a')", "Puzzle.Ready('01001a')", "Puzzle.Attack('01001a')"], {"pret": ["01075"], "exhausted": ["01076"]}, cibles=["01130"], accepter_choix=True),
    # ------------------------------------------------------------------ pu025 The Bronx (U3) : overkill sur chaque attaque
    # ------------------------------------------------------------------ pu025 The Bronx (U3) : overkill sur chaque attaque
    _l("pu025 The Bronx : le heros attaque Hydra Bomber (1 PV restant) avec ATK 2 -> l'OVERKILL envoie 1 degat de trop sur le vilain (Rhino)",
       "« Each attack in The Bronx gains overkill » : attaque du heros", "pu025", ["Puzzle.PutIntoPlay('01110')", "Puzzle.Damage('01110', 1)"],
       ["Puzzle.Attack('01001a')"], {"hors_jeu": ["01110"], "degats": [["01094", 1]]}, cibles=["01110"], apres=["Puzzle.MoveCardToGameArea('01094', 2)"]),
    _l("pu025 The Bronx, TEMOIN : meme attaque a Harlem (meme rangee, pas au lieu) -> le sbire meurt, le vilain n'a rien", "R3 : seul un joueur present a The Bronx",
       "pu024", ["Puzzle.PutIntoPlay('01110')", "Puzzle.Damage('01110', 1)"], ["Puzzle.Attack('01001a')"],
       {"hors_jeu": ["01110"], "degats": [["01094", 0]]}, cibles=["01110"], apres=["Puzzle.MoveCardToGameArea('01094', 2)"]),
    _l("pu025 The Bronx : une attaque ENNEMIE aussi (Shocker ATK 2 contre Black Widow, 1 PV restant, qui defend) -> 1 degat excedentaire au heros",
       "« Each attack » : toutes, y compris celles des sbires contre un allie", "pu025",
       ["Puzzle.PutIntoPlay('01103')", "Puzzle.PutIntoPlay('01075', under_control=True)", "Puzzle.Damage('01075', 1)", *SANS_BOOST],
       ["Puzzle.Attack('01103', defender='01075')"], {"hors_jeu": ["01075"], "degats_identite": 1}),
    _l("pu025 The Bronx, TEMOIN : la meme attaque a Harlem -> l'allie meurt, le heros n'a rien", "R3", "pu024",
       ["Puzzle.PutIntoPlay('01103')", "Puzzle.PutIntoPlay('01075', under_control=True)", "Puzzle.Damage('01075', 1)", *SANS_BOOST],
       ["Puzzle.Attack('01103', defender='01075')"], {"hors_jeu": ["01075"], "degats_identite": 0}),
    # ------------------------------------------------------------------ pu026 West Side Warrior (U1, 3 dojo)
    # ⚠ A Upper West Side, pu023 est EN JEU : son Interrupt donne +1/-1 (DEF 3 -> 4 ou 2) ; les cas choisissent -1 contre Rhino (ATK 2) pour la parade pile.
    _p("pu026 piste : le joueur pare PILE une attaque a Upper West Side (Rhino ATK 2 contre DEF 3 - 1 de pu023 = 2) -> 1 compteur dojo", "« exactly defend an attack » : attaque == DEF",
       "pu023", "pu026", ["Puzzle.PutIntoPlay('01094')", *SANS_BOOST], ["Puzzle.Attack('01094', defender='01001a')"],
       {"compteurs": [["pu026", "dojo", 1]], "victoire": []}, choisir_option=MOINS1),
    _p("pu026 piste, TEMOIN : attaque INFERIEURE a la DEF (Rhino ATK 2 contre DEF 3 + 1 = 4) -> aucun compteur", "pas une parade pile", "pu023", "pu026",
       ["Puzzle.PutIntoPlay('01094')", *SANS_BOOST], ["Puzzle.Attack('01094', defender='01001a')"], {"compteurs": [["pu026", "dojo", 0]]}, choisir_option=PLUS1),
    _p("pu026 piste, TEMOIN : attaque SUPERIEURE a la DEF (Melter ATK 3 contre DEF 3 - 1 = 2) -> aucun compteur", "pas une parade pile", "pu023", "pu026",
       ["Puzzle.PutIntoPlay('01132')", *SANS_BOOST], ["Puzzle.Attack('01132', defender='01001a')"], {"compteurs": [["pu026", "dojo", 0]]}, choisir_option=MOINS1),
    _p("pu026 piste : le joueur vainc PILE un ennemi (Shocker 3 PV, ATK 2 + 1 de pu023 = 3) a Upper West Side -> 1 compteur dojo", "« exactly defeat an enemy » : sans exces",
       "pu023", "pu026", ["Puzzle.PutIntoPlay('01103')"], ["Puzzle.Attack('01001a')"], {"compteurs": [["pu026", "dojo", 1]]}, cibles=["01103"], choisir_option=PLUS1),
    _p("pu026 piste, TEMOIN : il vainc avec EXCES (Hydra Bomber 1 PV restant, ATK 3) -> aucun compteur", "degats excedentaires = pas « exactly »", "pu023", "pu026",
       ["Puzzle.PutIntoPlay('01110')", "Puzzle.Damage('01110', 1)"], ["Puzzle.Attack('01001a')"], {"compteurs": [["pu026", "dojo", 0]]}, cibles=["01110"], choisir_option=PLUS1),
    _p("pu026 piste : le joueur vainc PILE une manigance annexe (menace 2, THW 1 + 1 de pu023) a Upper West Side -> 1 compteur dojo", "« exactly defeat a side scheme » : menace enlevee == menace restante",
       "pu023", "pu026", ["Puzzle.PutIntoPlay('01107')", "Puzzle.MoveCardToGameArea('01107', 2)", "Puzzle.SetThreat('01107', 2)"], ["Puzzle.Thwart('01001a')"],
       {"compteurs": [["pu026", "dojo", 1]]}, choisir_option=PLUS1),
    _p("pu026 piste, TEMOIN : avec EXCES (menace 1, Black Widow THW 2) -> aucun compteur", "menace enlevee 2 > menace restante 1", "pu023", "pu026",
       ["Puzzle.PutIntoPlay('01075', under_control=True)", "Puzzle.PutIntoPlay('01107')", "Puzzle.MoveCardToGameArea('01107', 2)", "Puzzle.SetThreat('01107', 1)"],
       ["Puzzle.Thwart('01075')"], {"compteurs": [["pu026", "dojo", 0]]}),
    _p("pu026 piste, TEMOIN : la meme parade pile a Harlem (meme rangee) -> aucun compteur", "« While in Upper West Side »", "pu024", "pu026",
       ["Puzzle.PutIntoPlay('01132')", *SANS_BOOST], ["Puzzle.Attack('01132', defender='01001a')"], {"compteurs": [["pu026", "dojo", 0]]}),
    _p("pu026 piste, FIN : 2 compteurs + 1 parade pile = 3 -> en victoire, suivante revelee, 1 carte", "seuil 3", "pu023", "pu026",
       ["Puzzle.PutIntoPlay('01094')", *SANS_BOOST, "Puzzle.PlaceCounters('pu026', 'dojo', 2)"], ["Puzzle.Attack('01094', defender='01001a')"], _fin("pu026"), choisir_option=MOINS1),
    # ------------------------------------------------------------------ pu027 The Harlem Hustle (U2, 3 hustle)
    _p("pu027 piste : le heros attaque (pouvoir de base) a Harlem -> 1 compteur hustle ET 3 menaces sur le complot principal", "Response ; « place a hustle counter here and add 3 threat to the main scheme »",
       "pu024", "pu027", ["Puzzle.PutIntoPlay('01110')"], ["Puzzle.SetThreat('01097b', 1)", "Puzzle.Attack('01001a')"],
       {"compteurs": [["pu027", "hustle", 1]], "menace": [["01097b", 4]], "victoire": []}, cibles=["01110"]),
    _p("pu027 piste : un ALLIE que je controle attaque aussi (Black Widow) -> 1 compteur et 3 menaces", "« a character you control »", "pu024", "pu027",
       ["Puzzle.PutIntoPlay('01110')", "Puzzle.PutIntoPlay('01075', under_control=True)"], ["Puzzle.SetThreat('01097b', 1)", "Puzzle.Attack('01075')"],
       {"compteurs": [["pu027", "hustle", 1]], "menace": [["01097b", 4]]}, cibles=["01110"]),
    _p("pu027 piste, TEMOIN : la meme attaque a Upper West Side (meme rangee) -> ni compteur ni menace", "« While in Harlem »", "pu023", "pu027",
       ["Puzzle.PutIntoPlay('01110')"], ["Puzzle.SetThreat('01097b', 1)", "Puzzle.Attack('01001a')"],
       {"compteurs": [["pu027", "hustle", 0]], "menace": [["01097b", 1]]}, cibles=["01110"]),
    _p("pu027 piste, FIN : 2 compteurs + 1 attaque = 3 -> les 3 menaces sont ajoutees PUIS la piste se termine (victoire, suivante, 1 carte)", "seuil 3 ; la menace est ajoutee a chaque attaque, y compris la 3e",
       "pu024", "pu027", ["Puzzle.PutIntoPlay('01110')", "Puzzle.PlaceCounters('pu027', 'hustle', 2)"], ["Puzzle.SetThreat('01097b', 1)", "Puzzle.Attack('01001a')"],
       _fin("pu027", menace=[["01097b", 4]]), cibles=["01110"]),
    # ------------------------------------------------------------------ pu028 Bronx Bombered (U3, degats >= PV imprimes du vilain)
    _p("pu028 piste : le heros inflige 2 degats a Diamondback (13 PV) a The Bronx -> il les subit ET la piste recoit 2 jetons de degats", "« after you deal damage to the villain, place an equal amount of damage here » (apres, pas a la place)",
       "pu025", "pu028", ["Puzzle.PutIntoPlay('pu055a')", "Puzzle.MoveCardToGameArea('pu055a', 2)"], ["Puzzle.Attack('01001a')"],
       {"jetons": [["pu028", "damage", 2]], "degats": [["pu055a", 2]], "victoire": []}, cibles=["pu055a"]),
    _p("pu028 piste, TEMOIN : la meme attaque a Harlem (meme rangee) -> le vilain subit 2, la piste n'a rien", "« While in The Bronx »", "pu024", "pu028",
       ["Puzzle.PutIntoPlay('pu055a')", "Puzzle.MoveCardToGameArea('pu055a', 2)"], ["Puzzle.Attack('01001a')"],
       {"jetons": [["pu028", "damage", 0]], "degats": [["pu055a", 2]]}, cibles=["pu055a"]),
    _p("pu028 piste, FIN : 11 + 2 = 13 >= 13 PV imprimes -> victoire, suivante revelee, 1 carte", "seuil = PV IMPRIMES du vilain", "pu025", "pu028",
       ["Puzzle.PutIntoPlay('pu055a')", "Puzzle.MoveCardToGameArea('pu055a', 2)", "Puzzle.Token('pu028', 'damage', 11)"], ["Puzzle.Attack('01001a')"],
       _fin("pu028"), cibles=["pu055a"]),
    _p("pu028 piste, TEMOIN de seuil : 10 + 2 = 12 < 13 -> pas terminee", "le seuil mord", "pu025", "pu028",
       ["Puzzle.PutIntoPlay('pu055a')", "Puzzle.MoveCardToGameArea('pu055a', 2)", "Puzzle.Token('pu028', 'damage', 10)"], ["Puzzle.Attack('01001a')"],
       {"jetons": [["pu028", "damage", 12]], "victoire": [], "taille_main": 1}, cibles=["pu055a"]),
    # ------------------------------------------------------------------ mise en place REELLE : scenario the_big_apple_uptown
    {"nom": "[upt] mise en place : Uptown ajoute la rangee U1 U2 U3 AU-DESSUS de la grille (12 lieux), un 4e CAPO (4 en jeu, un par rangee) et 3 pistes (12 au total, 1 revelee)",
     "pourquoi": "p057 : « 3 new locations... 3 new LEADS... a fourth CAPO villain to take charge of the uptown turf »", "scenario": "the_big_apple_uptown", "heros": "spider_man",
     "mise_en_place": [], "declencher": [], "verifier": "upt_etat", "attendu": {"lieux": 12, "capos": 4, "pistes": 12, "pistes_en_jeu": 1, "rangee_uptown": True}},
    {"nom": "[upt] mise en place, EXPERT : meme chose (12 lieux, 4 CAPO face B, 12 pistes)", "pourquoi": "la difficulte ne change pas la grille", "scenario": "the_big_apple_uptown_expert",
     "heros": "spider_man", "mise_en_place": [], "declencher": [], "verifier": "upt_etat", "attendu": {"lieux": 12, "capos": 4, "pistes": 12, "pistes_en_jeu": 1, "rangee_uptown": True}},
    {"nom": "[upt] mise en place, TEMOIN : sans Uptown (the_big_apple) -> 9 lieux, 3 CAPO, 9 pistes, aucune rangee U", "pourquoi": "l'extension est OPTIONNELLE : le combat 1 de la campagne l'exclut",
     "scenario": "the_big_apple", "heros": "spider_man", "mise_en_place": [], "declencher": [], "verifier": "upt_etat",
     "attendu": {"lieux": 9, "capos": 3, "pistes": 9, "pistes_en_jeu": 1, "rangee_uptown": False}},
    {"nom": "[upt] mise en place : la rangee U est au NORD de la grille (U2 est voisin de Theater District), le depart reste Midtown, et un CAPO tient la rangee U",
     "pourquoi": "le schema de p057 : U1 U2 U3 au-dessus de 1 2 3 ; deplacement orthogonal (R2)", "scenario": "the_big_apple_uptown", "heros": "spider_man",
     "mise_en_place": [], "declencher": [], "verifier": "upt_etat", "attendu": {"voisin_nord": ["pu031", "pu024"], "depart": "pu034", "capo_rangee_uptown": True}},
]

VERIFICATIONS = r'''
def upt_etat(monde, aides):
    """Cles : lieux, capos, pistes (total), pistes_en_jeu, rangee_uptown (la ligne -1 existe), voisin_nord [lieu, voisin], depart (lieu du joueur 1), capo_rangee_uptown."""
    from game.operate.ville import Ville
    attendu = aides["cas"].get("attendu") or {}
    etat = Ville.Etat(monde)
    if etat is None:
        return False, "aucune ville installee"
    soucis = []
    faces = [getattr(o, "face", None) for o in monde.object_manager.card_dict.values()]
    faces = [f for f in faces if f is not None]
    if "lieux" in attendu and len(etat.cases) != attendu["lieux"]:
        soucis.append(f"{len(etat.cases)} lieux (attendu {attendu['lieux']})")
    if "capos" in attendu:
        capos = [f for f in faces if f.IsInPlay() and f.HasTrait("CAPO") and type(f).__name__ == "EncounterVillain"]
        if len(capos) != attendu["capos"]:
            soucis.append(f"{len(capos)} CAPO en jeu (attendu {attendu['capos']})")
    if "pistes" in attendu:
        pistes = [f for f in faces if f.HasTrait("LEAD")]
        if len(pistes) != attendu["pistes"]:
            soucis.append(f"{len(pistes)} pistes (attendu {attendu['pistes']})")
    if "pistes_en_jeu" in attendu:
        n = len([f for f in faces if f.HasTrait("LEAD") and f.IsInPlay()])
        if n != attendu["pistes_en_jeu"]:
            soucis.append(f"{n} piste(s) revelee(s) (attendu {attendu['pistes_en_jeu']})")
    if "rangee_uptown" in attendu and ((-1 in etat.zones) != attendu["rangee_uptown"]):
        soucis.append(f"rangee Uptown (ligne -1) presente = {-1 in etat.zones} (attendu {attendu['rangee_uptown']})")
    if "voisin_nord" in attendu:
        lieu, voisin = attendu["voisin_nord"]
        case = next((c for c, f in etat.cases.items() if f.paper.card_id == lieu), None)
        voisins = [etat.cases[v].paper.card_id for v in Ville.Adjacentes(monde, case)] if case else []
        if voisin not in voisins:
            soucis.append(f"voisins de {lieu} = {voisins} (attendu {voisin})")
    if "depart" in attendu:
        occ = Ville.Lieu(monde, monde.const_players[0])
        if occ is None or occ.paper.card_id != attendu["depart"]:
            soucis.append(f"le joueur 1 est a {None if occ is None else occ.paper.card_id} (attendu {attendu['depart']})")
    if attendu.get("capo_rangee_uptown"):
        zone = etat.zones.get(-1)
        capos = [f for f in faces if f.IsInPlay() and f.HasTrait("CAPO") and f.card.game_area is zone]
        if len(capos) != 1:
            soucis.append(f"{len(capos)} CAPO dans la zone de la rangee Uptown (attendu 1)")
    return (False, " ; ".join(soucis)) if soucis else (True, "ville Uptown conforme")
'''
