# Cas test_capacites du heros Michelangelo (TMNT Heroes v3, Inkwire) : prefixe « [michelangelo] ».
# Un cas par capacite, sujet = le card_id dans le nom. Gabarits : docs/michelangelo_cartes.md.
#
# Rappels de montage : Michelangelo demarre en alter ego (tm001b) ; `ChangeToFace('tm001b',
# 'tm001a')` le passe en forme heros. Le scenario `rhino` : vilain 01094, complot principal
# 01097b des le montage (SetThreat sur 01097b, jamais 01097a). 01101 = Hydra Mercenary (sbire),
# 01107 = Breakin' & Takin' (annexe sans Crise), 01108 = Crowd Control (annexe Crise 1).
# Le deck de depart du heros n'est PAS complete par le harnais (deck `michelangelo` : 15 cartes) ;
# `main_exclusive` donne la main exacte, `Puzzle.EmptyPlayerDeck`/`CreatePlayerDeck` le deck.
# `DeclareNumber(a, b)` est une question a options « a ».. « b » : `choisir_option: ["3"]` force 3.

HEROS = {
    "scenario": "rhino",
    "heros": "michelangelo",
}
FORME_HEROS = "Puzzle.ChangeToFace('tm001b', 'tm001a')"
COMPLOT = "01097b"

CAS = [
    # ===================================================================== tm001a Booyakasha
    {
        "nom": "[michelangelo] tm001a Booyakasha — apres une ATQ de base : 3 menaces passent de la principale a une annexe",
        "pourquoi": ("« After you use a basic power (THW, ATK or DEF), move up to 3 threat from one scheme to another ». "
                     "Principale a 5, annexe 01107 a 1 : le joueur declare 3, on part de la principale vers l'annexe -> 2 et 4"),
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.PutIntoPlay('01107')", "Puzzle.SetThreat('01107', 1)",
                          f"Puzzle.SetThreat('{COMPLOT}', 5)"],
        "declencher": ["Puzzle.Attack('tm001a')"],
        "choisir_option": ["3"],
        "cibles": [COMPLOT, "01107"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [[COMPLOT, 2], ["01107", 4]]},
    },
    {
        "nom": "[michelangelo] tm001a Booyakasha — apres un CTR de base : meme deplacement",
        "pourquoi": ("le pouvoir de base THW declenche aussi la Reponse. Principale a 5 : le contre en retire 1 (-> 4), "
                     "puis Booyakasha en deplace 3 vers l'annexe 01107 (1 -> 4) : principale 1, annexe 4"),
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.PutIntoPlay('01107')", "Puzzle.SetThreat('01107', 1)",
                          f"Puzzle.SetThreat('{COMPLOT}', 5)"],
        "declencher": ["Puzzle.Thwart('tm001a')"],
        "choisir_option": ["3"],
        "cibles": [COMPLOT, "01107"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [[COMPLOT, 1], ["01107", 4]]},
    },
    {
        "nom": "[michelangelo] tm001a Booyakasha — apres une DEF de base : meme deplacement",
        "pourquoi": ("le pouvoir de base DEF declenche aussi la Reponse : Rhino attaque, le heros defend (DEF 2 contre ATQ 2, "
                     "rien ne passe), puis 3 menaces passent de la principale (5) a l'annexe 01107 (1) : 2 et 4"),
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.PutIntoPlay('01107')", "Puzzle.SetThreat('01107', 1)",
                          f"Puzzle.SetThreat('{COMPLOT}', 5)"],
        "declencher": ["Puzzle.Defend('tm001a', '01094')"],
        "choisir_option": ["3"],
        "cibles": [COMPLOT, "01107"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [[COMPLOT, 2], ["01107", 4]]},
    },
    {
        "nom": "[michelangelo] tm001a Booyakasha — « jusqu'a 3 » : le joueur peut en deplacer moins (1 sur 5)",
        "pourquoi": "le nombre est declare entre 1 et 3 : ici 1, la principale passe de 5 a 4 et l'annexe de 1 a 2",
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.PutIntoPlay('01107')", "Puzzle.SetThreat('01107', 1)",
                          f"Puzzle.SetThreat('{COMPLOT}', 5)"],
        "declencher": ["Puzzle.Attack('tm001a')"],
        "choisir_option": ["1"],
        "cibles": [COMPLOT, "01107"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [[COMPLOT, 4], ["01107", 2]]},
    },
    {
        "nom": "[michelangelo] tm001a Booyakasha — annexe videe par le deplacement = VAINCUE (defaussee, menace sur la principale)",
        "pourquoi": ("decision du 15/10/2026 : une annexe dont on deplace toute la menace est vaincue. 01107 a 2 -> 0 : elle "
                     "quitte le jeu pour la defausse de rencontre ; la principale recoit les 2 (le choix est plafonne a "
                     "la menace presente : 2)"),
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.PutIntoPlay('01107')", "Puzzle.SetThreat('01107', 2)"],
        "declencher": ["Puzzle.Attack('tm001a')"],
        "choisir_option": ["2"],
        "cibles": ["01107", COMPLOT],
        "verifier": "etat_attendu",
        "attendu": {"menace": [[COMPLOT, 2]], "hors_jeu": ["01107"], "defausse_rencontre": ["01107"]},
    },
    {
        "nom": "[michelangelo] tm001a Booyakasha — destination annexe a 5 (1 joueur) REFUSEE : rien ne bouge",
        "pourquoi": ("« You cannot move threat onto a side scheme with 5[per_hero] or more threat » : 1 joueur -> 5. 01107 a 5 "
                     "et tm009 (I'm Here to Help, mise en jeu au Setup, annexe elle aussi) a 5 : aucune destination possible "
                     "(la principale est la source) : aucun deplacement, 3 / 5 / 5 inchanges"),
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.PutIntoPlay('01107')", "Puzzle.SetThreat('01107', 5)",
                          "Puzzle.SetThreat('tm009', 5)", f"Puzzle.SetThreat('{COMPLOT}', 3)"],
        "declencher": ["Puzzle.Attack('tm001a')"],
        "choisir_option": ["3"],
        "cibles": [COMPLOT, "01107"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [[COMPLOT, 3], ["01107", 5], ["tm009", 5]]},
    },
    {
        "nom": "[michelangelo] tm001a Booyakasha — destination annexe a 4 (1 joueur) ACCEPTEE : 4 + 3 = 7",
        "pourquoi": ("temoin du cas precedent : a 4 (< 5) la destination est permise, la limite se teste AVANT le deplacement ; "
                     "l'annexe monte donc a 7"),
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.PutIntoPlay('01107')", "Puzzle.SetThreat('01107', 4)",
                          f"Puzzle.SetThreat('{COMPLOT}', 3)"],
        "declencher": ["Puzzle.Attack('tm001a')"],
        "choisir_option": ["3"],
        "cibles": [COMPLOT, "01107"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [[COMPLOT, 0], ["01107", 7]]},
    },
    {
        "nom": "[michelangelo] tm001a Booyakasha — 2 joueurs : la limite devient 10, une annexe a 9 est acceptee",
        "pourquoi": "5[per_hero] a deux joueurs = 10 : 01107 a 9 (< 10) accepte 3 menaces (-> 12)",
        **HEROS,
        "heros2": "spider_man",
        "mise_en_place": [FORME_HEROS, "Puzzle.PutIntoPlay('01107')", "Puzzle.SetThreat('01107', 9)",
                          f"Puzzle.SetThreat('{COMPLOT}', 3)"],
        "declencher": ["Puzzle.Attack('tm001a')"],
        "choisir_option": ["3"],
        "cibles": [COMPLOT, "01107"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [[COMPLOT, 0], ["01107", 12]]},
    },
    {
        "nom": "[michelangelo] tm001a Booyakasha — 2 joueurs : une annexe a 10 est refusee",
        "pourquoi": ("5[per_hero] a deux joueurs = 10 : 01107 et tm009 a 10 sont REFUSEES, rien ne bouge "
                     "(principale 3, annexes 10 et 10)"),
        **HEROS,
        "heros2": "spider_man",
        "mise_en_place": [FORME_HEROS, "Puzzle.PutIntoPlay('01107')", "Puzzle.SetThreat('01107', 10)",
                          "Puzzle.SetThreat('tm009', 10)", f"Puzzle.SetThreat('{COMPLOT}', 3)"],
        "declencher": ["Puzzle.Attack('tm001a')"],
        "choisir_option": ["3"],
        "cibles": [COMPLOT, "01107"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [[COMPLOT, 3], ["01107", 10], ["tm009", 10]]},
    },
    {
        "nom": "[michelangelo] tm001a Booyakasha — CRISE active : la principale n'est PAS une source, la menace de l'annexe Crise remonte",
        "pourquoi": ("decision du 15/10/2026 : Crise bloque le deplacement DEPUIS la principale. 01108 (Crise) a 3, principale a 4 : "
                     "on essaie de partir de la principale (cibles forcees) ; elle n'est pas offerte, la source est 01108 "
                     "(3 -> 0, vaincue) et la principale monte de 4 a 7"),
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.PutIntoPlay('01108')", "Puzzle.SetThreat('01108', 3)",
                          f"Puzzle.SetThreat('{COMPLOT}', 4)"],
        "declencher": ["Puzzle.Attack('tm001a')"],
        "choisir_option": ["3"],
        "cibles": [COMPLOT, "01108"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [[COMPLOT, 7]], "hors_jeu": ["01108"]},
    },
    {
        "nom": "[michelangelo] tm001a Booyakasha — SANS Crise : la principale est bien une source (temoin du cas Crise)",
        "pourquoi": "meme montage sans 01108 : la principale (4) donne 3 a l'annexe 01107 (1 -> 4), elle tombe a 1",
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.PutIntoPlay('01107')", "Puzzle.SetThreat('01107', 1)",
                          f"Puzzle.SetThreat('{COMPLOT}', 4)"],
        "declencher": ["Puzzle.Attack('tm001a')"],
        "choisir_option": ["3"],
        "cibles": [COMPLOT, "01107"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [[COMPLOT, 1], ["01107", 4]]},
    },
    {
        "nom": "[michelangelo] tm001a Booyakasha — moteur : MoveThreat DEPUIS la principale est bloque par une Crise active",
        "pourquoi": ("preuve directe du moteur (scheme_main.py RemoveThreatInternal) : avec 01108 en jeu, "
                     "`principale.MoveThreat(2, ...)` ne deplace RIEN (0) et la principale garde ses 4 menaces"),
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.PutIntoPlay('01107')", "Puzzle.SetThreat('01107', 1)",
                          "Puzzle.PutIntoPlay('01108')", "Puzzle.SetThreat('01108', 3)",
                          f"Puzzle.SetThreat('{COMPLOT}', 4)"],
        "declencher": [],
        "verifier": "michelangelo_movethreat",
        "attendu": {"deplace": 0, "menace": [[COMPLOT, 4], ["01107", 1]]},
    },
    {
        "nom": "[michelangelo] tm001a Booyakasha — moteur : MoveThreat depuis la principale SANS Crise deplace bien (temoin)",
        "pourquoi": "meme appel sans 01108 : 2 menaces passent de la principale (4 -> 2) a l'annexe 01107 (1 -> 3)",
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.PutIntoPlay('01107')", "Puzzle.SetThreat('01107', 1)",
                          f"Puzzle.SetThreat('{COMPLOT}', 4)"],
        "declencher": [],
        "verifier": "michelangelo_movethreat",
        "attendu": {"deplace": 2, "menace": [[COMPLOT, 2], ["01107", 3]]},
    },
    # ===================================================================== tm001b Mikey : Setup
    {
        "nom": "[michelangelo] tm001b Mikey Setup — la partie met tm009 I'm Here to Help en jeu (menace 3), le deck garde les 14 autres",
        "pourquoi": ("« Setup : put the I'm Here to Help player side scheme into play » : decision du 15/10/2026, fouille du "
                     "deck (la carte reste dans les 15). Vraie mise en place : main 6, tm009 trouvee dans le deck (9 -> 8) "
                     "et posee avec ses 3 menaces"),
        **HEROS,
        "mise_en_place": [],
        "declencher": [],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["tm009"], "menace": [["tm009", 3]], "taille_deck_joueur": 8, "taille_main": 6},
    },
    {
        "nom": "[michelangelo] tm001b Mikey Setup — mulligan complet : tm009 est en jeu quoi qu'il arrive (main ou deck)",
        "pourquoi": ("le Setup part APRES la pioche de depart et le mulligan : si tm009 se retrouve dans la main, « put into "
                     "play » doit quand meme la poser. Mulligan « all » : la main change, tm009 doit etre en jeu"),
        **HEROS,
        "mulligan": "all",
        "mise_en_place": [],
        "declencher": [],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["tm009"], "menace": [["tm009", 3]]},
    },
    {
        "nom": "[michelangelo] tm001b Mikey Setup — tm009 dans la MAIN de depart : le Setup la met quand meme en jeu",
        "pourquoi": ("6 cartes sur 15 : tm009 peut etre dans la main de depart. On reproduit la situation (tm009 mise en "
                     "main, puis le Setup de l'alter-ego rejoue) : elle doit passer de la main au jeu avec 3 menaces"),
        **HEROS,
        "mise_en_place": ["Puzzle.MoveTo('tm009', 'HandsArea')"],
        "declencher": [],
        "verifier": "michelangelo_resetup",
        "attendu": {"en_jeu": ["tm009"], "menace": [["tm009", 3]], "avant_en_main": True},
    },
    {
        "nom": "[michelangelo] tm001b Mikey Setup — tm009 dans la DEFAUSSE (mulligan) : le Setup la met quand meme en jeu",
        "pourquoi": "meme situation avec tm009 en defausse (mulligan de depart) : elle doit entrer en jeu avec ses 3 menaces",
        **HEROS,
        "mise_en_place": ["Puzzle.MoveTo('tm009', 'DiscardPile')"],
        "declencher": [],
        "verifier": "michelangelo_resetup",
        "attendu": {"en_jeu": ["tm009"], "menace": [["tm009", 3]]},
    },
    # ===================================================================== tm001b Mikey : Action
    {
        "nom": "[michelangelo] tm001b Mikey Action — defausse 1 carte : les 2 Nunchuck (deck + defausse) entrent en jeu INCLINES",
        "pourquoi": ("« Discard 1 card from your hand -> search your deck and discard pile for up to 2 NUNCHUCK upgrades and put "
                     "them into play, exhausted ». Deck [tm011 sur 01090], defausse [tm012], main [01088] : la main part en "
                     "defausse (cout), tm011 vient du deck, tm012 de la defausse, les deux inclines"),
        **HEROS,
        "mise_en_place": ["Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01090', 'tm011')",
                          "Puzzle.CreatePlayerDiscardPile('tm012')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Action('tm001b', 'Action')"],
        "cibles": ["tm011", "tm012"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["tm011", "tm012"], "exhausted": ["tm011", "tm012"], "defausse": ["01088"],
                    "taille_deck_joueur": 1, "taille_main": 0},
    },
    {
        "nom": "[michelangelo] tm001b Mikey Action — un seul NUNCHUCK dans le deck : il entre, la 2e recherche ne trouve rien",
        "pourquoi": "« up to 2 » : un seul Nunchuck existe (tm011 dans le deck) ; il entre incline, le cout est quand meme paye",
        **HEROS,
        "mise_en_place": ["Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01090', 'tm011')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Action('tm001b', 'Action')"],
        "cibles": ["tm011", "tm012"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["tm011"], "exhausted": ["tm011"], "defausse": ["01088"], "taille_deck_joueur": 1},
    },
    {
        "nom": "[michelangelo] tm001b Mikey Action — aucun NUNCHUCK a trouver : rien n'entre, le cout reste paye",
        "pourquoi": "deck [01090] sans Nunchuck : la recherche ne ramene rien, la carte defaussee en cout est bien en defausse",
        **HEROS,
        "mise_en_place": ["Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01090')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Action('tm001b', 'Action')"],
        "verifier": "etat_attendu",
        "attendu": {"hors_jeu": ["tm011", "tm012"], "defausse": ["01088"], "taille_deck_joueur": 1},
    },
    {
        "nom": "[michelangelo] tm001b Mikey Action — main VIDE : l'Action est injouable (le cout de defausse ne peut etre paye)",
        "pourquoi": "sans carte en main le « -> » ne peut pas etre paye : les Nunchuck restent dans le deck",
        **HEROS,
        "mise_en_place": ["Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01090', 'tm011')", "Puzzle.EmptyHand()"],
        "declencher": [],
        "declencher_tolerant": ["Puzzle.Action('tm001b', 'Action')"],
        "verifier": "etat_attendu",
        "attendu": {"hors_jeu": ["tm011"], "taille_main": 0, "taille_deck_joueur": 2},
    },
    # ===================================================================== tm002 Slash
    {
        "nom": "[michelangelo] tm002 Slash — Toughness : entre en jeu avec une carte de statut Tough",
        "pourquoi": "« Toughness » est une base automatique (desc.Toughness) : en jeu, Slash porte le statut Tough",
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.PutIntoPlay('tm002', under_control=True)"],
        "declencher": [],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["tm002"], "statuts": [["tm002", "Tough"]]},
    },
    {
        "nom": "[michelangelo] tm002 Slash — Retaliate 1 : Rhino attaque, Slash defend, Rhino subit 1 degat",
        "pourquoi": ("« Retaliate 1 » (base automatique) : apres avoir ete attaque, Slash inflige 1 degat a l'attaquant. "
                     "Slash defend contre Rhino : Robustesse absorbe les degats de Rhino, Rhino subit 1"),
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.PutIntoPlay('tm002', under_control=True)"],
        "declencher": ["Puzzle.Defend('tm002', '01094')"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 1], ["tm002", 0]], "statuts_absents": [["tm002", "Tough"]]},
    },
    {
        "nom": "[michelangelo] tm002 Slash — ses attaques ont Piercing : la Robustesse de la cible est defaussee ET les 3 degats passent",
        "pourquoi": ("« [star] Slash's attacks gain piercing » : Sandman 01102 (Toughness) engage, Slash l'attaque (ATQ 3) : sans "
                     "Piercing la Robustesse absorberait tout (0 degat) ; avec, elle est defaussee et Sandman subit 3"),
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.PutIntoPlay('tm002', under_control=True)", "Puzzle.PutIntoPlay('01102')"],
        "declencher": ["Puzzle.Attack('tm002')"],
        "cibles": ["01102"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01102", 3]], "statuts_absents": [["01102", "Tough"]]},
    },
    {
        "nom": "[michelangelo] tm002 Slash — ATQ 3 avec 2 degats consecutifs : Rhino subit 3, la Robustesse de Slash absorbe les 2",
        "pourquoi": ("« ATQ 3 ** » : apres son attaque Slash subit 2 degats consecutifs. Avec sa Robustesse ils sont absorbes : "
                     "Slash survit sans degat, mais perd son statut Tough"),
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.PutIntoPlay('tm002', under_control=True)"],
        "declencher": ["Puzzle.Attack('tm002')"],
        "cibles": ["01094"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 3], ["tm002", 0]], "statuts_absents": [["tm002", "Tough"]], "en_jeu": ["tm002"]},
    },
    {
        "nom": "[michelangelo] tm002 Slash — ATQ 3 avec 2 degats consecutifs, SANS Robustesse : Slash (2 PV) est vaincue par son propre coup",
        "pourquoi": "meme montage sans statut Tough : les 2 degats consecutifs tuent Slash (2 PV) apres que Rhino a subi 3",
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.PutIntoPlay('tm002', under_control=True)", "Puzzle.Tough('tm002')"],
        "declencher": ["Puzzle.Attack('tm002')"],
        "cibles": ["01094"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 3]], "hors_jeu": ["tm002"]},
    },
    {
        "nom": "[michelangelo] tm002 Slash — CTR 0 avec 1 degat consecutif, sans Robustesse : Slash subit 1",
        "pourquoi": "« THW 0 * » : meme un contre de 0 inflige 1 degat consecutif a Slash (principale a 3, sans Robustesse)",
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.PutIntoPlay('tm002', under_control=True)", "Puzzle.Tough('tm002')",
                          f"Puzzle.SetThreat('{COMPLOT}', 3)"],
        "declencher": ["Puzzle.Thwart('tm002')"],
        "cibles": [COMPLOT],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["tm002", 1]], "menace": [[COMPLOT, 3]]},
    },
    # ===================================================================== tm003 Call for Help
    {
        "nom": "[michelangelo] tm003 Call for Help — cherche un ALLIE dans le deck : il rejoint la main",
        "pourquoi": ("« Search your deck and discard pile for an ally or the I'm Here to Help player side scheme and add it to "
                     "your hand ». Deck [01090, tm002 (allie)] : tm002 en main, deck reduit a 1 carte"),
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01090', 'tm002')",
                          "Puzzle.EmptyHand()"],
        "declencher": [],
        "jouer": ["tm003"],
        "cibles": ["tm002"],
        "verifier": "etat_attendu",
        "attendu": {"en_main": ["tm002"], "taille_deck_joueur": 1, "defausse": ["tm003"]},
    },
    {
        "nom": "[michelangelo] tm003 Call for Help — cherche tm009 dans la DEFAUSSE : la manigance rejoint la main",
        "pourquoi": ("tm009 (I'm Here to Help), en defausse apres avoir ete vaincue : « deck AND discard pile » ; deck [01090] "
                     "sans allie, tm009 revient en main"),
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01090')",
                          "Puzzle.MoveTo('tm009', 'DiscardPile')"],
        "declencher": [],
        "jouer": ["tm003"],
        "cibles": ["tm009"],
        "verifier": "etat_attendu",
        "attendu": {"en_main": ["tm009"], "hors_jeu": ["tm009"]},
    },
    {
        "nom": "[michelangelo] tm003 Call for Help — UNE seule carte : avec un allie ET tm009 disponibles, un seul rejoint la main",
        "pourquoi": ("« an ally OR the side scheme » : deck [01090, tm002] et tm009 en defausse : on choisit tm002, tm009 reste "
                     "en defausse (la main ne recoit qu'UNE carte)"),
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01090', 'tm002')",
                          "Puzzle.MoveTo('tm009', 'DiscardPile')", "Puzzle.EmptyHand()"],
        "declencher": [],
        "jouer": ["tm003"],
        "cibles": ["tm002"],
        "verifier": "etat_attendu",
        "attendu": {"en_main": ["tm002"], "absent_main": ["tm009"], "taille_main": 1, "defausse": ["tm003", "tm009"]},
    },
    {
        "nom": "[michelangelo] tm003 Call for Help — TEMOIN : ni allie ni tm009 a trouver, l'evenement est joue sans rien ramener",
        "pourquoi": "deck [01090] (ressource), tm009 en jeu : rien a chercher, la main reste vide, tm003 en defausse",
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01090')", "Puzzle.EmptyHand()"],
        "declencher": [],
        "jouer": ["tm003"],
        "verifier": "etat_attendu",
        "attendu": {"taille_main": 0, "defausse": ["tm003"], "taille_deck_joueur": 1},
    },
]

VERIFICATIONS = r'''
def michelangelo_resetup(monde, aides):
    """Rejoue le Setup de l'alter-ego (`Setup(False)`, comme `World.Setup`) apres que le cas a deplace tm009 hors du jeu."""
    attendu = aides["cas"]["attendu"]
    soucis = []
    if aides["par_id"](monde, "tm009") is not None:
        soucis.append("tm009 est encore en jeu avant le Setup rejoue (montage du cas)")
    if attendu.get("avant_en_main"):
        main = [getattr(f.paper, "card_id", None) for f in monde.players[0].hand_cards.GetAll()]
        if "tm009" not in main:
            soucis.append("tm009 n'est pas dans la main avant le Setup rejoue")
    monde.players[0].GetIdentity().Setup(False)
    face = aides["par_id"](monde, "tm009")
    if face is None:
        soucis.append("tm009 n'est pas en jeu apres le Setup rejoue")
    elif face.threat != 3:
        soucis.append(f"menace sur tm009 = {face.threat} (attendu 3)")
    if soucis:
        return False, " ; ".join(soucis)
    return True, "tm009 mise en jeu par le Setup rejoue, 3 menaces"


def michelangelo_movethreat(monde, aides):
    """Appelle `MoveThreat` du moteur DEPUIS la principale vers 01107 (2 menaces) et compare `deplace` et les menaces."""
    # ⚠ PAS une DebugRule : `Effect.IsIgnoreKeyword` repond VRAI a toute regle (`effect.is_rule`), la Crise
    # serait ignoree d'office. On emprunte le VRAI effet Booyakasha du heros (une capacite de carte).
    attendu = aides["cas"]["attendu"]
    principale = aides["par_id"](monde, "01097b")
    annexe = aides["par_id"](monde, "01107")
    heros = aides["par_id"](monde, "tm001a")
    regle = heros.effect.Find(name="Booyakasha")[0]
    deplace = principale.MoveThreat(2, regle, [annexe])
    soucis = []
    if deplace != attendu["deplace"]:
        soucis.append(f"MoveThreat a rendu {deplace} (attendu {attendu['deplace']})")
    for cid, voulu in attendu["menace"]:
        face = aides["par_id"](monde, cid)
        if face is None or face.threat != voulu:
            soucis.append(f"menace sur {cid} = {None if face is None else face.threat} (attendu {voulu})")
    if soucis:
        return False, " ; ".join(soucis)
    return True, f"MoveThreat a deplace {deplace} ; menaces conformes"


def michelangelo_debug(monde, aides):
    out = []
    for cid in ("tm011", "tm012", "tm001a"):
        f = aides["par_id"](monde, cid)
        if f is None:
            out.append(cid + " absent")
            continue
        out.append(cid + " exhaust=" + str(f.IsExhaust()) + " given=" + str(len(f.effect.given_effects)))
    return False, " | ".join(out)
'''
