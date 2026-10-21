# Cas test_capacites du scenario 1 « The Big Apple » (pack MC×DC 2026 « La ville ne dort jamais »), PU-5 fin / PU-7. Prefixe `[big]`.
# Ville REELLE : les 9 lieux (pu030-pu038) mis en jeu, chacun dans la zone de SA rangee (`Puzzle.InstallerVille(..., en_jeu=True)`),
# ⚠ `Puzzle.CreateEncounterDeck(a, b, c)` : le DESSUS du deck est le DERNIER argument.
# The City / Never Sleeps dans la zone COMMUNE (indice 1 : la zone 0 est celle de depart, la commune est creee la premiere).
FORME_HEROS = "Puzzle.ChangeForm('01001b')"
RIEN = ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01105', '01105', '01105')"]
GRILLE_REELLE = [["pu030", "pu031", "pu032"], ["pu033", "pu034", "pu035"], ["pu036", "pu037", "pu038"]]
G = repr(GRILLE_REELLE)
CLES_VILLE = ("case_de", "zone_de", "occupe", "zones", "schemes_vus", "allies_vus", "mechant_vu")


def ville(depart=(1, 1), communs=("pu005", "pu006")):
    """Pose la ville reelle (a mettre dans `declencher`) : lieux en jeu, environnements communs dans la zone commune."""
    return [*["Puzzle.PutIntoPlay('%s')" % x for x in communs],
            "Puzzle.InstallerVille(%s, %s, en_jeu=True)" % (G, repr(tuple(depart))),
            *["Puzzle.MoveCardToGameArea('%s', 1)" % x for x in communs]]


def _b(nom, pourquoi, declencher, attendu, mise=(), **cle):
    cas = {"nom": "[big] " + nom, "pourquoi": pourquoi, "scenario": "rhino", "heros": "spider_man",
           "mise_en_place": [*RIEN, FORME_HEROS, *mise], "declencher": declencher, "verifier": "big_etat",
           "attendu": attendu, "main_exclusive": ["01088"]}
    cas.update(cle)
    return cas


CAS = [
    _b("pu005 The City : Action « epuiser un personnage » -> le joueur se deplace de Midtown a Theater District (zone de la rangee 0) et s'epuise",
       "R2 : deplacement orthogonal, cout = epuiser un personnage que l'on controle ; R4 : changer de rangee = changer de zone",
       [*ville(), "Puzzle.Action('pu005', index=0)"],
       {"case_de": [[0, [0, 1]]], "zone_de": [["01001a", 2]], "exhausted": ["01001a"]}, cibles=["pu031"]),
    _b("pu005 The City : Action « depenser 1 ressource » -> Midtown vers Lower East Side (meme rangee, meme zone), personnage PAS epuise, carte payee defaussee",
       "R2 : le second cout est une ressource de n'importe quel type ; un deplacement horizontal ne change pas de zone",
       [*ville(), "Puzzle.Action('pu005', index=1)"],
       {"case_de": [[0, [1, 2]]], "zone_de": [["01001a", 3]], "pret": ["01001a"], "defausse": ["01088"]},
       cibles=["pu035"], payer_avec=["01088"]),
    _b("pu005 The City, TEMOIN D'ABSENCE DE LIMITE : deux deplacements dans le meme round (epuiser, puis 1 ressource) -> Midtown, Theater District, Hell's Kitchen",
       "R2 / FAQ : « autant de fois qu'on peut payer »",
       [*ville(), "Puzzle.Action('pu005', index=0)", "Puzzle.Action('pu005', index=0)"],
       {"case_de": [[0, [0, 0]]], "zone_de": [["01001a", 2]], "exhausted": ["01001a"], "defausse": ["01088"]},
       cibles=["pu031", "pu030"], payer_avec=["01088"]),
    # ---------------------------------------------------------------- pu031 Theater District (rangee 0, colonne 1)
    _b("pu031 Theater District : epuiser l'identite -> elle soigne 2 degats (4 -> 2)",
       "Action de lieu, cout = epuiser un personnage ; soin sur CE personnage",
       [*ville((0, 1)), "Puzzle.Damage('01001a', 4)", "Puzzle.Action('pu031', 'Action')"],
       {"degats": [["01001a", 2]], "exhausted": ["01001a"]}, cibles=["01001a"]),
    _b("pu031 Theater District, TEMOIN D'EPUISEMENT : seconde Action du round (avec un allie) -> refusee, l'allie garde son degat",
       "« Limit once per round » globale : 1 seule activation, 1 allie blesse reste blesse (degats 1)",
       [*ville((0, 1)), "Puzzle.PutIntoPlay('01075', under_control=True)", "Puzzle.Damage('01001a', 4)", "Puzzle.Damage('01075', 1)",
        "Puzzle.Action('pu031', 'Action')"],
       {"degats": [["01001a", 2], ["01075", 1]]}, cibles=["01001a"],
       declencher_tolerant=["Puzzle.Action('pu031', 'Action')"]),
    _b("pu031 Theater District, TEMOIN : le joueur est a Hell's Kitchen (MEME rangee, pas au lieu) -> aucune Action offerte (rien ne bouge)",
       "R3 : on n'interagit qu'avec le lieu qu'on occupe (`Ville.AuLieu`) ; meme zone, donc seule la condition peut bloquer",
       [*ville((0, 0)), "Puzzle.Damage('01001a', 4)"],
       {"degats": [["01001a", 4]], "pret": ["01001a"]},
       declencher_tolerant=["Puzzle.Action('pu031', 'Action')"]),
    # ---------------------------------------------------------------- pu036 Soho (rangee 2, colonne 0)
    _b("pu036 Soho : un evenement coute +1 -> Haymaker (2) avec 2 icones (Genius BB) est REFUSE, reste en main, Whirlwind indemne",
       "« Increase the cost of each event you play by 1 » : 2 + 1 = 3 > 2 icones",
       ["Puzzle.PutIntoPlay('01130')", *ville((2, 0))], {"en_main": ["01087", "01089"], "degats": [["01130", 0]]},
       main_exclusive=["01087", "01089"], jouer=["01087"], cibles=["01130"]),
    _b("pu036 Soho, TEMOIN : a Midtown le meme Haymaker se joue avec les memes 2 icones -> 3 degats a Whirlwind",
       "ligne de base : le +1 vient bien de Soho, et seul un joueur PRESENT a Soho le paie",
       ["Puzzle.PutIntoPlay('01130')", *ville((1, 1))], {"degats": [["01130", 3]], "defausse": ["01087", "01089"]},
       main_exclusive=["01087", "01089"], jouer=["01087"], cibles=["01130"]),
    _b("pu036 Soho, TEMOIN : a Financial District (MEME rangee, pas a Soho) le Haymaker se joue au prix normal -> 3 degats a Whirlwind",
       "R3 : le +1 ne touche que les joueurs presents a Soho ; meme zone, donc seule la condition `Ville.AuLieu` peut l'ecarter",
       ["Puzzle.PutIntoPlay('01130')", *ville((2, 1))], {"degats": [["01130", 3]], "defausse": ["01087", "01089"]},
       main_exclusive=["01087", "01089"], jouer=["01087"], cibles=["01130"]),
    _b("pu036 Soho : Action « piocher 2 puis defausser 2 » -> la main garde sa taille (3) et 2 cartes partent en defausse",
       "pioche d'abord, defausse ensuite ; la main finale = 3 + 2 - 2",
       [*ville((2, 0)), "Puzzle.Action('pu036', 'Action')"], {"taille_main": 3, "taille_deck_joueur": 29},
       main_exclusive=["01088", "01089", "01090"]),
    _b("pu036 Soho, TEMOIN D'EPUISEMENT : seconde Action du round -> refusee, la main reste a 3 (pas de nouvelle pioche)",
       "« Limit once per round » globale : la seconde Action ne pioche pas",
       [*ville((2, 0)), "Puzzle.Action('pu036', 'Action')"], {"taille_main": 3, "taille_deck_joueur": 29},
       main_exclusive=["01088", "01089", "01090"], declencher_tolerant=["Puzzle.Action('pu036', 'Action')"]),
    _b("pu036 Soho, TEMOIN : le joueur est a Financial District (meme rangee que Soho, pas au lieu) -> l'Action n'est pas offerte (la main ne bouge pas)",
       "R3 : seul le lieu occupe", [*ville((2, 1))], {"taille_main": 3, "taille_deck_joueur": 31},
       main_exclusive=["01088", "01089", "01090"], declencher_tolerant=["Puzzle.Action('pu036', 'Action')"]),
    # ---------------------------------------------------------------- pu034 Midtown (rangee 1, colonne 1, depart)
    _b("pu034 Midtown : Action -> le joueur choisi joue Black Widow (S.H.I.E.L.D., cout 3) pour 2 icones (Genius BB) : cout reduit de 1",
       "« reducing its cost by 1 » : 3 - 1 = 2 icones suffisent",
       [*ville(), "Puzzle.Action('pu034', 'Action')"], {"en_jeu": ["01075"]},
       main_exclusive=["01075", "01089"], cibles=["01001a", "01075"], payer_avec=["01089"]),
    _b("pu034 Midtown, TEMOIN : sans l'Action, Black Widow (cout 3) n'est PAS jouable avec 2 icones",
       "ligne de base : la reduction vient bien de Midtown",
       [*ville()], {"en_main": ["01075", "01089"]},
       main_exclusive=["01075", "01089"], jouer=["01075"]),
    _b("pu034 Midtown, TEMOIN DE TRAIT : Jessica Jones (DEFENDER, cout 3) n'est pas eligible -> rien n'est joue",
       "seuls AVENGER, S.H.I.E.L.D. ou TECH",
       [*ville()], {"en_main": ["01059", "01089"]},
       main_exclusive=["01059", "01089"], declencher_tolerant=["Puzzle.Action('pu034', 'Action')"], cibles=["01001a", "01059"],
       payer_avec=["01089"]),
    _b("pu034 Midtown, TEMOIN D'EPUISEMENT : seconde Action du round -> refusee, Hellcat (AVENGER) reste en main",
       "« Limit once per round » globale : une seule carte jouee",
       [*ville(), "Puzzle.Action('pu034', 'Action')"], {"en_jeu": ["01075"], "en_main": ["01020"]},
       main_exclusive=["01075", "01020", "01089", "01090"], cibles=["01001a", "01075"], payer_avec=["01089"],
       declencher_tolerant=["Puzzle.Action('pu034', 'Action')"]),
    _b("pu034 Midtown, TEMOIN : le joueur est a West Village (MEME rangee, pas a Midtown) -> l'Action n'est pas offerte",
       "R3 : seul le lieu occupe", [*ville((1, 0))], {"en_main": ["01075", "01089"]},
       main_exclusive=["01075", "01089"], declencher_tolerant=["Puzzle.Action('pu034', 'Action')"], cibles=["01001a", "01075"],
       payer_avec=["01089"]),
    # ---------------------------------------------------------------- pu032 Upper East Side (rangee 0, colonne 2)
    _b("pu032 Upper East Side : Action -> deux cartes defaussees puis la manigance annexe Breakin' & Takin' (01107) est revelee",
       "« Discard ... until a side scheme is discarded. Reveal that scheme » : 2 traitrises 01105 defaussees, 01107 en jeu",
       [*ville((0, 2)), "Puzzle.Action('pu032', 'Action')"], {"en_jeu": ["01107"], "defausse_rencontre": ["01105"]},
       mise=["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01105', '01105', '01107', '01105')"]),
    _b("pu032 Upper East Side, TEMOIN D'EPUISEMENT : seconde Action du round -> refusee, la 2e annexe (01109) reste dans le deck",
       "« Limit once per round » globale", [*ville((0, 2)), "Puzzle.Action('pu032', 'Action')"],
       {"en_jeu": ["01107"], "dans_deck_rencontre": ["01109"]},
       mise=["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01109', '01105', '01107', '01105')"],
       declencher_tolerant=["Puzzle.Action('pu032', 'Action')"]),
    _b("pu032 Upper East Side, TEMOIN : le joueur est a Theater District (MEME rangee, pas au lieu) -> l'Action n'est pas offerte",
       "R3", [*ville((0, 1))], {"dans_deck_rencontre": ["01107"]},
       mise=["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01105', '01107', '01105')"],
       declencher_tolerant=["Puzzle.Action('pu032', 'Action')"]),
    # ---------------------------------------------------------------- pu038 Chinatown (rangee 2, colonne 2)
    _b("pu038 Chinatown : on distribue une carte rencontre au joueur -> A LA PLACE le deck est defausse jusqu'a un sbire (Shocker 01103), revele : 1 degat",
       "Interrupt « instead » : la traitrise 01105 n'est pas distribuee ; Shocker (When Revealed : 1 degat a chaque heros) s'engage",
       [*ville((2, 2)), "Puzzle.Deal('01105')"],
       {"en_jeu": ["01103"], "degats_identite": 1, "defausse_rencontre": ["01105"]},
       mise=["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01105', '01103', '01105')"]),
    _b("pu038 Chinatown, TEMOIN D'EPUISEMENT : seconde carte distribuee dans le round -> la limite mord, pas de second sbire (Shocker 01103 seul en jeu, 1 degat)",
       "« Limit once per round » globale", [*ville((2, 2)), "Puzzle.Deal('01105')", "Puzzle.Deal('01105')"],
       {"en_jeu": ["01103"], "hors_jeu": ["01110"], "degats_identite": 1},
       mise=["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01105', '01110', '01105', '01103', '01105')"]),
    _b("pu038 Chinatown, TEMOIN : le joueur est a Financial District (MEME rangee, pas au lieu) -> aucune interruption, aucun sbire",
       "R3 : seul le lieu occupe", [*ville((2, 1)), "Puzzle.Deal('01105')"], {"hors_jeu": ["01103"], "degats_identite": 0},
       mise=["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01105', '01103', '01105')"]),
]

VERIFICATIONS = r'''
def big_etat(monde, aides):
    """Scinde `attendu` : les cles de la ville vont a `ville_etat` (banc de zones), le reste a `etat_attendu`."""
    cas = aides["cas"]
    attendu = cas.get("attendu") or {}
    cles_ville = ("case_de", "zone_de", "occupe", "zones", "schemes_vus", "allies_vus", "mechant_vu")
    soucis = []
    for fn, garde in ((ville_etat, lambda k: k in cles_ville), (etat_attendu, lambda k: k not in cles_ville)):
        part = {k: v for k, v in attendu.items() if garde(k)}
        if not part:
            continue
        cas["attendu"] = part
        try:
            ok, msg = fn(monde, aides)
        finally:
            cas["attendu"] = attendu
        if not ok:
            soucis.append(msg)
    return (False, " ; ".join(soucis)) if soucis else (True, "scenario Big Apple conforme")
'''
