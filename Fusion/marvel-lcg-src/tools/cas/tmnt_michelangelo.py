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
    # ===================================================================== tm011 / tm012 : octroi aux NUNCHUCK
    {
        "nom": "[michelangelo] tm011 Nunchuck — seul en jeu : il recoit la Reponse, +1 ATQ et il s'incline",
        "pourquoi": ("« Each NUNCHUCK upgrade you control gains : Hero Response : after you play an event, exhaust this card -> +1 "
                     "to a basic power until the end of the round ». tm011 seul en jeu se donne l'aptitude a LUI-MEME ; on joue "
                     "tm003 (evenement, cout 0) : ATQ 1 -> 2, tm011 incline"),
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.PutIntoPlay('tm011', under_control=True)"],
        "declencher": [],
        "jouer": ["tm003"],
        "verifier": "etat_attendu",
        "attendu": {"attributs": {"attack": 1}, "exhausted": ["tm011"], "en_jeu": ["tm011"]},
    },
    {
        "nom": "[michelangelo] tm011 Nunchuck — TEMOIN : sans Nunchuck en jeu, un evenement ne donne aucun bonus",
        "pourquoi": "meme jeu de tm003 sans aucun Nunchuck : ATQ inchangee (1)",
        **HEROS,
        "mise_en_place": [FORME_HEROS],
        "declencher": [],
        "jouer": ["tm003"],
        "verifier": "etat_attendu",
        "attendu": {"attributs": {"attack": 0}},
    },
    {
        "nom": "[michelangelo] tm011 Nunchuck — tm012 seul en jeu NE recoit PAS la Reponse de tm011 (la donneuse est absente)",
        "pourquoi": ("tm012 seul : il ne porte que SA propre aptitude (l'Interruption) ; l'evenement ne declenche rien : ATQ inchangee, "
                     "tm012 reste pret"),
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.PutIntoPlay('tm012', under_control=True)"],
        "declencher": [],
        "jouer": ["tm003"],
        "verifier": "etat_attendu",
        "attendu": {"attributs": {"attack": 0}, "pret": ["tm012"]},
    },
    {
        "nom": "[michelangelo] tm011 Nunchuck — les DEUX en jeu : tm012 recoit la Reponse de tm011 (deux exemplaires independants, +2 ATQ)",
        "pourquoi": ("risque connu : la MEME instance d'Ability enregistree chez deux porteurs. Les deux Nunchuck en jeu : apres "
                     "un evenement, CHACUN declenche sa Reponse (ATQ 1 -> 3) et s'incline separement"),
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.PutIntoPlay('tm011', under_control=True)",
                          "Puzzle.PutIntoPlay('tm012', under_control=True)"],
        "declencher": [],
        "jouer": ["tm003"],
        "verifier": "etat_attendu",
        "attendu": {"attributs": {"attack": 2}, "exhausted": ["tm011", "tm012"]},
    },
    {
        "nom": "[michelangelo] tm011 Nunchuck — un Nunchuck incline ne repond pas : l'autre donne seul son +1 (les deux sont independants)",
        "pourquoi": "les deux en jeu, tm012 deja incline (cout impossible) : seule la Reponse de tm011 part, ATQ 1 -> 2",
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.PutIntoPlay('tm011', under_control=True)",
                          "Puzzle.PutIntoPlay('tm012', under_control=True, exhaust=True)"],
        "declencher": [],
        "jouer": ["tm003"],
        "verifier": "etat_attendu",
        "attendu": {"attributs": {"attack": 1}, "exhausted": ["tm011", "tm012"]},
    },
    {
        "nom": "[michelangelo] tm011 Nunchuck — la donneuse PART : tm012 perd la Reponse (disparition de l'octroi)",
        "pourquoi": ("les deux en jeu puis tm011 defaussee : tm012 ne porte plus la Reponse de tm011, un evenement ne donne aucun "
                     "bonus (ATQ inchangee) et tm012 reste pret"),
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.PutIntoPlay('tm011', under_control=True)",
                          "Puzzle.PutIntoPlay('tm012', under_control=True)", "Puzzle.Discard('tm011')"],
        "declencher": [],
        "jouer": ["tm003"],
        "verifier": "etat_attendu",
        "attendu": {"attributs": {"attack": 0}, "pret": ["tm012"], "hors_jeu": ["tm011"]},
    },
    {
        "nom": "[michelangelo] tm011 Nunchuck — le Nunchuck mis en jeu APRES la donneuse la recoit aussi",
        "pourquoi": "tm011 d'abord, tm012 ensuite (ordre inverse du cas des deux en jeu) : les deux declenchent, ATQ 1 -> 3",
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.PutIntoPlay('tm012', under_control=True)",
                          "Puzzle.PutIntoPlay('tm011', under_control=True)"],
        "declencher": [],
        "jouer": ["tm003"],
        "verifier": "etat_attendu",
        "attendu": {"attributs": {"attack": 2}, "exhausted": ["tm011", "tm012"]},
    },
    {
        "nom": "[michelangelo] tm011 Nunchuck — la Reponse est celle du HEROS : en alter-ego, un evenement ne declenche rien",
        "pourquoi": "Hero Response : en forme d'alter-ego (Mikey) elle n'est pas offerte, tm011 reste pret",
        **HEROS,
        "mise_en_place": ["Puzzle.PutIntoPlay('tm011', under_control=True)"],
        "declencher": [],
        "jouer": ["tm006"],
        "verifier": "etat_attendu",
        "attendu": {"pret": ["tm011"]},
    },
    {
        "nom": "[michelangelo] tm012 Other Nunchuck — Interruption : -1 degat de l'attaque, 1 degat a l'attaquant, tm012 incline",
        "pourquoi": ("« When you would take damage from an attack, exhaust this card -> reduce that damage by 1 and deal 1 "
                     "damage to the attacking enemy ». Heros epuise (ne defend pas) : l'attaque de Rhino vaut 4 dans ce montage "
                     "(mesure du temoin ci-dessous) -> 3 degats a l'identite, Rhino subit 1"),
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.PutIntoPlay('tm012', under_control=True)", "Puzzle.Exhaust('tm001a')"],
        "declencher": ["Puzzle.Attack('01094')"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 3, "degats": [["01094", 1]], "exhausted": ["tm012"]},
    },
    {
        "nom": "[michelangelo] tm012 Other Nunchuck — TEMOIN : sans Nunchuck, l'attaque passe en entier (4) et Rhino ne subit rien",
        "pourquoi": "meme attaque sans tm012 : 4 degats a l'identite (ligne de base de ce montage), 0 a Rhino",
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.Exhaust('tm001a')"],
        "declencher": ["Puzzle.Attack('01094')"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 4, "degats": [["01094", 0]]},
    },
    {
        "nom": "[michelangelo] tm012 Other Nunchuck — des degats qui ne viennent PAS d'une attaque ne declenchent pas l'Interruption",
        "pourquoi": "« from an attack » : 2 degats directs (Puzzle.Damage) a l'identite : rien n'est reduit, tm012 reste pret",
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.PutIntoPlay('tm012', under_control=True)"],
        "declencher": ["Puzzle.Damage('tm001a', 2)"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 2, "degats": [["01094", 0]], "pret": ["tm012"]},
    },
    {
        "nom": "[michelangelo] tm012 Other Nunchuck — les DEUX en jeu : tm011 recoit l'Interruption, chacun reduit 1 (attaque 4 -> 2, Rhino subit 2)",
        "pourquoi": ("tm011 porte aussi l'Interruption donnee par tm012 : deux exemplaires independants, deux reductions de 1 "
                     "(attaque de 4 : 2 degats), deux degats a Rhino, les deux inclines"),
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.PutIntoPlay('tm011', under_control=True)",
                          "Puzzle.PutIntoPlay('tm012', under_control=True)", "Puzzle.Exhaust('tm001a')"],
        "declencher": ["Puzzle.Attack('01094')"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 2, "degats": [["01094", 2]], "exhausted": ["tm011", "tm012"]},
    },
    {
        "nom": "[michelangelo] tm012 Other Nunchuck — la donneuse PART : tm011 perd l'Interruption (seul tm011 en jeu : attaque passee en entier)",
        "pourquoi": "les deux puis tm012 defaussee : tm011 n'a plus l'Interruption, l'attaque de 4 passe en entier, Rhino indemne",
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.PutIntoPlay('tm011', under_control=True)",
                          "Puzzle.PutIntoPlay('tm012', under_control=True)", "Puzzle.Discard('tm012')",
                          "Puzzle.Exhaust('tm001a')"],
        "declencher": ["Puzzle.Attack('01094')"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 4, "degats": [["01094", 0]], "pret": ["tm011"]},
    },
    {
        "nom": "[michelangelo] tm011/tm012 Restricted — pas plus de 2 cartes Restricted : un 3e objet fait partir le plus ancien (base moteur)",
        "pourquoi": ("base automatique desc.Restricted : tm011 et tm012 (Restricted) en jeu, un troisieme objet Restricted "
                     "(03009 Captain America's Shield) entre et le moteur defausse le plus ancien (tm011) : il ne reste jamais "
                     "plus de 2 Restricted"),
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.PutIntoPlay('tm011', under_control=True)",
                          "Puzzle.PutIntoPlay('tm012', under_control=True)", "Puzzle.PutIntoPlay('03009', under_control=True)"],
        "declencher": [],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["tm012", "03009"], "hors_jeu": ["tm011"]},
    },
    # ===================================================================== tm004 Impulsive
    {
        "nom": "[michelangelo] tm004 Impulsive — 2 menaces sur la principale, heros ET arme (WEAPON) redresses, pioche 1",
        "pourquoi": ("« Place 2 threat on the main scheme -> ready Michelangelo and a WEAPON you control. Draw 1 card. » Heros et "
                     "tm012 (WEAPON) inclines, principale a 3, main [01088] payant le cout 1 : principale 5, heros et tm012 prets, "
                     "main = 1 carte piochee"),
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.PutIntoPlay('tm012', under_control=True, exhaust=True)",
                          "Puzzle.Exhaust('tm001a')", f"Puzzle.SetThreat('{COMPLOT}', 3)"],
        "main_exclusive": ["01088"],
        "declencher": [],
        "jouer": ["tm004"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [[COMPLOT, 5]], "pret": ["tm001a", "tm012"], "taille_main": 1, "defausse": ["tm004"]},
    },
    {
        "nom": "[michelangelo] tm004 Impulsive — SANS WEAPON : jouable quand meme (decision du 15/10/2026), heros redresse, pioche 1",
        "pourquoi": "aucune arme en jeu : la carte se joue, les 2 menaces sont posees, le heros est redresse, 1 carte piochee",
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.Exhaust('tm001a')", f"Puzzle.SetThreat('{COMPLOT}', 3)"],
        "main_exclusive": ["01088"],
        "declencher": [],
        "jouer": ["tm004"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [[COMPLOT, 5]], "pret": ["tm001a"], "taille_main": 1, "defausse": ["tm004"]},
    },
    {
        "nom": "[michelangelo] tm004 Impulsive — jouable en MAIN sans WEAPON (CanPlayBy vrai, pas seulement le resultat)",
        "pourquoi": "preuve directe que la carte en main est jouable quand aucune arme n'est en jeu",
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.Gain('tm004')", "Puzzle.Gain('01088')"],
        "declencher": [],
        "verifier": "michelangelo_jouable",
        "attendu": {"carte": "tm004", "jouable": True},
    },
    # ===================================================================== tm005 Kaiten
    {
        "nom": "[michelangelo] tm005 Kaiten — 3 degats a un ennemi ; epuiser un Nunchuck pret : Rhino est SONNE",
        "pourquoi": ("« Deal 3 damage to an enemy. You may exhaust a NUNCHUCK upgrade you control to confuse or stun that "
                     "enemy » : cout 2 paye par [01090], tm012 pret : Rhino subit 3 et est Sonne, tm012 s'incline"),
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.PutIntoPlay('tm012', under_control=True)"],
        "main_exclusive": ["01090"],
        "declencher": [],
        "jouer": ["tm005"],
        "cibles": ["01094"],
        "preferer_option": ["stun that enemy"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 3]], "statuts": [["01094", "Stunned"]], "exhausted": ["tm012"]},
    },
    {
        "nom": "[michelangelo] tm005 Kaiten — l'autre branche : Rhino est DESORIENTE",
        "pourquoi": "meme montage, branche « confuse » : Rhino subit 3 et est Desoriente, pas Sonne",
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.PutIntoPlay('tm012', under_control=True)"],
        "main_exclusive": ["01090"],
        "declencher": [],
        "jouer": ["tm005"],
        "cibles": ["01094"],
        "preferer_option": ["confuse that enemy"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 3]], "statuts": [["01094", "Confused"]], "statuts_absents": [["01094", "Stunned"]],
                    "exhausted": ["tm012"]},
    },
    {
        "nom": "[michelangelo] tm005 Kaiten — Nunchuck deja INCLINE (cout impossible) : seulement les 3 degats",
        "pourquoi": "tm012 incline : aucune branche payable, Rhino subit 3 sans statut",
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.PutIntoPlay('tm012', under_control=True, exhaust=True)"],
        "main_exclusive": ["01090"],
        "declencher": [],
        "jouer": ["tm005"],
        "cibles": ["01094"],
        "preferer_option": ["stun that enemy"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 3]], "statuts_absents": [["01094", "Stunned"], ["01094", "Confused"]]},
    },
    {
        "nom": "[michelangelo] tm005 Kaiten — sans aucun Nunchuck : seulement les 3 degats",
        "pourquoi": "pas de Nunchuck du tout : Rhino subit 3 sans statut",
        **HEROS,
        "mise_en_place": [FORME_HEROS],
        "main_exclusive": ["01090"],
        "declencher": [],
        "jouer": ["tm005"],
        "cibles": ["01094"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 3]], "statuts_absents": [["01094", "Stunned"], ["01094", "Confused"]]},
    },
    {
        "nom": "[michelangelo] tm005 Kaiten — « you MAY » : on peut refuser l'epuisement, le Nunchuck reste pret",
        "pourquoi": "Nunchuck pret mais choix « Passer » : 3 degats, pas de statut, tm012 reste pret",
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.PutIntoPlay('tm012', under_control=True)"],
        "main_exclusive": ["01090"],
        "declencher": [],
        "jouer": ["tm005"],
        "cibles": ["01094"],
        "choisir_option": ["Cancel"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 3]], "statuts_absents": [["01094", "Stunned"], ["01094", "Confused"]],
                    "pret": ["tm012"]},
    },
    {
        "nom": "[michelangelo] tm005 Kaiten — libelle attaque : un heros SONNE voit son attaque annulee (statut consomme, 0 degat)",
        "pourquoi": ("l'evenement est une attaque (SetLabel('attack')) : heros Sonne, la carte jouee consomme Sonne et n'inflige "
                     "rien a Rhino"),
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.Stun('tm001a')"],
        "main_exclusive": ["01090"],
        "declencher": [],
        "jouer": ["tm005"],
        "cibles": ["01094"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 0]], "statuts_absents": [["tm001a", "Stunned"]]},
    },
    # ===================================================================== tm006 Majime
    {
        "nom": "[michelangelo] tm006 Majime — X = 3 reellement subis : -3 menace sur la principale, 3 degats a Rhino",
        "pourquoi": ("« Take X damage (max 3) -> remove X threat from a scheme and deal X damage to an enemy ». Declare 3, rien ne "
                     "previent : identite -3 PV, principale 5 -> 2, Rhino subit 3"),
        **HEROS,
        "mise_en_place": [FORME_HEROS, f"Puzzle.SetThreat('{COMPLOT}', 5)"],
        "main_exclusive": [],
        "declencher": [],
        "jouer": ["tm006"],
        "choisir_option": ["3"],
        "cibles": [COMPLOT, "01094"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 3, "menace": [[COMPLOT, 2]], "degats": [["01094", 3]]},
    },
    {
        "nom": "[michelangelo] tm006 Majime — X = 0 : rien ne se passe",
        "pourquoi": "declare 0 : aucun degat subi, aucun retrait de menace, Rhino indemne",
        **HEROS,
        "mise_en_place": [FORME_HEROS, f"Puzzle.SetThreat('{COMPLOT}', 5)"],
        "declencher": [],
        "jouer": ["tm006"],
        "choisir_option": ["0"],
        "cibles": [COMPLOT, "01094"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 0, "menace": [[COMPLOT, 5]], "degats": [["01094", 0]]},
    },
    {
        "nom": "[michelangelo] tm006 Majime — Robustesse du heros : les 3 degats declares sont PREVENUS, X reel = 0, aucun effet",
        "pourquoi": ("decision du 15/10/2026 : X = degats REELLEMENT subis. Heros Tough, declare 3 : Tough absorbe tout, X = 0, "
                     "principale inchangee (5), Rhino indemne (l'ancien script, X declare, aurait retire 3 et inflige 3)"),
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.Tough('tm001a')", f"Puzzle.SetThreat('{COMPLOT}', 5)"],
        "declencher": [],
        "jouer": ["tm006"],
        "choisir_option": ["3"],
        "cibles": [COMPLOT, "01094"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 0, "menace": [[COMPLOT, 5]], "degats": [["01094", 0]],
                    "statuts_absents": [["tm001a", "Tough"]]},
    },
    {
        "nom": "[michelangelo] tm006 Majime — reduction de 1 (05017 Energy Barrier) : declare 3, subis 2 -> cout NON paye, aucun effet (RR Cost, 26/10/2026)",
        "pourquoi": ("RR Cost : « If taking damage is a cost, that cost is not considered paid unless all of that damage was taken » : "
                     "Energy Barrier previent 1 des 3 degats declares (et inflige 1 a un ennemi), l'identite subit 2 sur 3, le cout n'est pas paye : "
                     "principale inchangee (5), Rhino ne subit QUE le 1 degat d'Energy Barrier (meme arbitrage que us004 Reckless ; remplace la lecture "
                     "« X reel = 2 » de decisions-phase-b.md du 15/10/2026)"),
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.PutIntoPlay('05017', under_control=True)", f"Puzzle.SetThreat('{COMPLOT}', 5)"],
        "declencher": [],
        "jouer": ["tm006"],
        "choisir_option": ["3"],
        "cibles": [COMPLOT, "01094"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 2, "menace": [[COMPLOT, 5]], "degats": [["01094", 1]]},
    },
    {
        "nom": "[michelangelo] tm006 Majime — libelle attaque/contre : consomme Sonne ET Desoriente du heros (annule, aucun effet)",
        "pourquoi": ("Hero Action (attack/thwart) : heros Sonne : l'attaque est annulee (Sonne consomme), rien ne se passe ; "
                     "Rhino indemne, menace inchangee"),
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.Stun('tm001a')", f"Puzzle.SetThreat('{COMPLOT}', 5)"],
        "declencher": [],
        "jouer": ["tm006"],
        "choisir_option": ["3"],
        "cibles": [COMPLOT, "01094"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 0]], "menace": [[COMPLOT, 5]], "statuts_absents": [["tm001a", "Stunned"]]},
    },
    # ===================================================================== tm007 Optimism
    {
        "nom": "[michelangelo] tm007 Optimism — depensee : soigne 1 a l'identite ET pioche 1",
        "pourquoi": ("« After you spend this card, heal 1 damage from your identity and draw 1 card » : on paie tm012 (cout 1) avec "
                     "tm007, identite a 2 degats : 1 degat restant, main = 1 carte piochee"),
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.Damage('tm001a', 2)"],
        "main_exclusive": ["tm007"],
        "declencher": [],
        "jouer": ["tm012"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 1, "taille_main": 1, "en_jeu": ["tm012"]},
    },
    {
        "nom": "[michelangelo] tm007 Optimism — a pleine sante la pioche part quand meme",
        "pourquoi": "identite indemne : rien a soigner, mais la carte est piochee (les deux effets sont independants)",
        **HEROS,
        "mise_en_place": [FORME_HEROS],
        "main_exclusive": ["tm007"],
        "declencher": [],
        "jouer": ["tm012"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 0, "taille_main": 1, "en_jeu": ["tm012"]},
    },
    {
        "nom": "[michelangelo] tm007 Optimism — Reponse (pas Hero Response) : marche aussi en ALTER-EGO",
        "pourquoi": "alter-ego (Mikey) a 2 degats paie Mikey's Couch (tm008, cout 1) avec tm007 : soigne 1, pioche 1",
        **HEROS,
        "mise_en_place": ["Puzzle.Damage('tm001b', 2)"],
        "main_exclusive": ["tm007"],
        "declencher": [],
        "jouer": ["tm008"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 1, "taille_main": 1, "en_jeu": ["tm008"]},
    },
    # ===================================================================== tm008 Mikey's Couch
    {
        "nom": "[michelangelo] tm008 Mikey's Couch — Mikey gagne +1 REC",
        "pourquoi": "« Mikey gets +1 REC » : en alter-ego (Mikey, REC 3) le canape donne REC 4",
        **HEROS,
        "mise_en_place": ["Puzzle.PutIntoPlay('tm008', under_control=True)"],
        "declencher": [],
        "verifier": "etat_attendu",
        "attendu": {"attributs": {"recover": 1}, "en_jeu": ["tm008"]},
    },
    {
        "nom": "[michelangelo] tm008 Mikey's Couch — Action d'alter-ego : epuise, jusqu'a 2 cartes de la defausse retournent dans le deck",
        "pourquoi": ("« Exhaust Mikey's Couch -> choose up to 2 cards in your discard pile and shuffle them into your deck » : "
                     "defausse [01088, 01089, 01091], deck [01090] : on choisit 01088 et 01089 -> deck 3, defausse 1, canape incline"),
        **HEROS,
        "mise_en_place": ["Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01090')", "Puzzle.CreatePlayerDiscardPile('01088', '01089', '01091')",
                          "Puzzle.PutIntoPlay('tm008', under_control=True)"],
        "declencher": ["Puzzle.Action('tm008', 'AlterEgoAction')"],
        "cibles": ["01088", "01089"],
        "accepter_choix": True,
        "verifier": "michelangelo_couch",
        "attendu": {"deck": 3, "defausse": 1, "exhausted": ["tm008"]},
    },
    {
        "nom": "[michelangelo] tm008 Mikey's Couch — l'Action est une Action d'ALTER-EGO : en forme de heros elle n'est pas offerte",
        "pourquoi": "forme de heros : Action tentee puis refusee, canape reste pret, defausse inchangee",
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01090')",
                          "Puzzle.CreatePlayerDiscardPile('01088', '01089')", "Puzzle.PutIntoPlay('tm008', under_control=True)"],
        "declencher": [],
        "declencher_tolerant": ["Puzzle.Action('tm008', 'AlterEgoAction')"],
        "verifier": "michelangelo_couch",
        "attendu": {"deck": 1, "defausse": 2, "pret": ["tm008"]},
    },
    # ===================================================================== tm009 I'm Here to Help
    {
        "nom": "[michelangelo] tm009 I'm Here to Help — hors limite : en jeu, une AUTRE manigance-joueur reste jouable",
        "pourquoi": ("« does not count against the player side scheme limit » : tm009 en jeu (Setup), 40054 Take Out the Guards "
                     "en main est jouable (limite 1 non entamee)"),
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.Gain('40054')"],
        "declencher": [],
        "verifier": "michelangelo_jouable",
        "attendu": {"carte": "40054", "jouable": True},
    },
    {
        "nom": "[michelangelo] tm009 I'm Here to Help — temoin : la limite MORD sur les manigances ordinaires, jamais sur tm009",
        "pourquoi": ("tm009 + 40054 en jeu, on joue 40020 (cout 1) : la limite de 1 est depassee, UNE des deux manigances "
                     "ordinaires part (40054 ou 40020), tm009 reste en jeu"),
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.PutIntoPlay('40054', under_control=True)"],
        "main_exclusive": ["01088"],
        "declencher": [],
        "jouer": ["40020"],
        "verifier": "michelangelo_mains",
        "attendu": {"en_jeu": ["tm009"], "un_seul_en_jeu": ["40054", "40020"]},
    },
    {
        "nom": "[michelangelo] tm009 I'm Here to Help — jouee DEPUIS LA MAIN, elle ne compte pas non plus (40054 deja en jeu)",
        "pourquoi": ("tm009 retiree de la partie puis redonnee en main, 40054 en jeu : tm009 reste jouable (cout 0) et entre avec "
                     "3 menaces malgre la limite atteinte"),
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.Remove('tm009')", "Puzzle.PutIntoPlay('40054', under_control=True)",
                          "Puzzle.Gain('tm009')"],
        "declencher": [],
        "jouer": ["tm009"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["tm009", "40054"], "menace": [["tm009", 3]]},
    },
    {
        "nom": "[michelangelo] tm009 I'm Here to Help — Reponse forcee : a la fin de la phase des joueurs, -1 menace (3 -> 2)",
        "pourquoi": "« After the player phase ends, remove 1 threat from this card » : EndPlayerPhase, menace 3 -> 2, rien pioche",
        **HEROS,
        "mise_en_place": [FORME_HEROS],
        "declencher": ["Puzzle.EndPlayerPhase()"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["tm009", 2]], "taille_main": 6},
    },
    {
        "nom": "[michelangelo] tm009 I'm Here to Help — vaincue par la Reponse forcee en forme de heros : le proprietaire pioche 3",
        "pourquoi": ("menace 1 puis fin de phase : la carte est vaincue, « Hero Interrupt : draw 3 cards » : main 6 -> 9 "
                     "(forme de heros, proprietaire)"),
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.SetThreat('tm009', 1)"],
        "declencher": ["Puzzle.EndPlayerPhase()"],
        "verifier": "etat_attendu",
        "attendu": {"hors_jeu": ["tm009"], "taille_main": 9},
    },
    {
        "nom": "[michelangelo] tm009 I'm Here to Help — vaincue en ALTER-EGO : personne ne pioche (l'insert : forme de heros obligatoire)",
        "pourquoi": "meme montage en forme d'alter-ego : la manigance est vaincue mais l'Interruption de heros ne part pas (main 6)",
        **HEROS,
        "mise_en_place": ["Puzzle.SetThreat('tm009', 1)"],
        "declencher": ["Puzzle.EndPlayerPhase()"],
        "verifier": "etat_attendu",
        "attendu": {"hors_jeu": ["tm009"], "taille_main": 6},
    },
    {
        "nom": "[michelangelo] tm009 I'm Here to Help — vaincue par un CONTRE du heros : le proprietaire pioche 3",
        "pourquoi": "tm009 a 1 menace, le heros la contre (THW 1) : vaincue, 3 cartes piochees (main 6 -> 9)",
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.SetThreat('tm009', 1)"],
        "declencher": ["Puzzle.Thwart('tm001a')"],
        "cibles": ["tm009"],
        "verifier": "etat_attendu",
        "attendu": {"hors_jeu": ["tm009"], "taille_main": 9},
    },
    {
        "nom": "[michelangelo] tm009 I'm Here to Help — « only the Michelangelo player » : vaincue par un AUTRE joueur, personne ne pioche",
        "pourquoi": ("2 joueurs (Spider-Man en second) : tm009 a 1 menace, Spider-Man (heros) la contre : elle est vaincue mais "
                     "Michelangelo (proprietaire) ne pioche pas : sa main reste a 6"),
        **HEROS,
        "heros2": "spider_man",
        "mise_en_place": [FORME_HEROS, "Puzzle.ChangeForm('01001b')", "Puzzle.SetThreat('tm009', 1)"],
        "declencher": ["Puzzle.Thwart('01001a')"],
        "cibles": ["tm009"],
        "verifier": "michelangelo_mains",
        "attendu": {"hors_jeu": ["tm009"], "main0": 6},
    },
    # ===================================================================== tm010 Mikey's Skateboard
    {
        "nom": "[michelangelo] tm010 Skateboard — apres un changement de forme alter-ego -> heros : s'incline et redresse l'identite",
        "pourquoi": ("« After you change form, exhaust Mikey's Skateboard -> ready your identity » : identite epuisee, "
                     "changement de forme : l'identite (face heros) est prete, le Skateboard est incline"),
        **HEROS,
        "mise_en_place": ["Puzzle.PutIntoPlay('tm010', under_control=True)", "Puzzle.Exhaust('tm001b')"],
        "declencher": ["Puzzle.ChangeToFace('tm001b', 'tm001a')"],
        "verifier": "etat_attendu",
        "attendu": {"pret": ["tm001a"], "exhausted": ["tm010"], "forme": "Hero"},
    },
    {
        "nom": "[michelangelo] tm010 Skateboard — DANS L'AUTRE SENS (heros -> alter-ego) : meme Reponse",
        "pourquoi": "« After you change form » sans precision : heros epuise, passage en alter-ego : l'identite est prete, Skateboard incline",
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.PutIntoPlay('tm010', under_control=True)", "Puzzle.Exhaust('tm001a')"],
        "declencher": ["Puzzle.ChangeToFace('tm001a', 'tm001b')"],
        "verifier": "etat_attendu",
        "attendu": {"pret": ["tm001b"], "exhausted": ["tm010"], "forme": "AlterEgo"},
    },
    {
        "nom": "[michelangelo] tm010 Skateboard — deja INCLINE : le cout ne peut pas etre paye, l'identite reste epuisee",
        "pourquoi": "Skateboard incline : pas de Reponse, l'identite epuisee le reste apres le changement de forme",
        **HEROS,
        "mise_en_place": ["Puzzle.PutIntoPlay('tm010', under_control=True, exhaust=True)", "Puzzle.Exhaust('tm001b')"],
        "declencher": ["Puzzle.ChangeToFace('tm001b', 'tm001a')"],
        "verifier": "etat_attendu",
        "attendu": {"exhausted": ["tm001a", "tm010"]},
    },
    # ===================================================================== tm013 All Alone
    {
        "nom": "[michelangelo] tm013 All Alone — revelee : passe en alter-ego, epuise chaque allie et soutien",
        "pourquoi": ("« Flip to alter-ego form. Exhaust each ally and support you control » : heros avec Slash (allie) et Couch "
                     "(soutien) prets : alter-ego, les deux inclines"),
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.PutIntoPlay('tm002', under_control=True)",
                          "Puzzle.PutIntoPlay('tm008', under_control=True)"],
        "declencher": ["Puzzle.Reveal('tm013')"],
        "verifier": "etat_attendu",
        "attendu": {"forme": "AlterEgo", "exhausted": ["tm002", "tm008"], "en_jeu": ["tm013"]},
    },
    {
        "nom": "[michelangelo] tm013 All Alone — « You cannot change forms » : le retour en heros est refuse tant qu'elle est en jeu",
        "pourquoi": "apres la revelation, ChangeForm vers le heros est annule : l'identite reste Mikey",
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.Reveal('tm013')"],
        "declencher": [],
        "declencher_tolerant": ["Puzzle.ChangeToFace('tm001b', 'tm001a')"],
        "verifier": "etat_attendu",
        "attendu": {"forme": "AlterEgo", "en_jeu": ["tm013"]},
    },
    {
        "nom": "[michelangelo] tm013 All Alone — Action d'alter-ego : epuise l'identite ET defausse 1 carte -> retiree de la partie",
        "pourquoi": ("« Exhaust your identity and discard 1 card from your hand -> remove All Alone from the game » : main [01088] "
                     "defaussee, identite epuisee, tm013 retiree (ni en jeu ni en defausse)"),
        **HEROS,
        "mise_en_place": ["Puzzle.Reveal('tm013')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Action('tm013', 'AlterEgoAction')"],
        "verifier": "etat_attendu",
        "attendu": {"hors_jeu": ["tm013"], "exhausted": ["tm001b"], "defausse": ["01088"], "taille_main": 0},
    },
    {
        "nom": "[michelangelo] tm013 All Alone — Action : identite deja epuisee, le cout n'est pas payable, elle reste en jeu",
        "pourquoi": "identite epuisee (cout 1 impossible) : tentative toleree, tm013 reste en jeu, la carte de la main n'est pas defaussee",
        **HEROS,
        "mise_en_place": ["Puzzle.Reveal('tm013')", "Puzzle.Exhaust('tm001b')"],
        "main_exclusive": ["01088"],
        "declencher": [],
        "declencher_tolerant": ["Puzzle.Action('tm013', 'AlterEgoAction')"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["tm013"], "taille_main": 1},
    },
    {
        "nom": "[michelangelo] tm013 All Alone — 2 joueurs : seuls les allies et soutiens de Mikey sont epuises (celui de l'autre reste pret)",
        "pourquoi": "« you control » : Hulk (01050) sous le controle de Spider-Man reste pret, Slash (a Michelangelo) est epuise",
        **HEROS,
        "heros2": "spider_man",
        "mise_en_place": [FORME_HEROS, "Puzzle.PutIntoPlay('tm002', under_control=True)",
                          "Puzzle.PutIntoPlay('01050', player=1, under_control=True)"],
        "declencher": ["Puzzle.Reveal('tm013')"],
        "verifier": "etat_attendu",
        "attendu": {"exhausted": ["tm002"], "pret": ["01050"]},
    },
    # ===================================================================== tm014 Sewer Problems
    {
        "nom": "[michelangelo] tm014 Sewer Problems — revelee : chaque joueur defausse les 3 cartes du dessus de SON deck (1 joueur)",
        "pourquoi": "deck de 5 cartes : 3 vont en defausse, 2 restent ; menace de depart 4 par heros (1 joueur : 4)",
        **HEROS,
        "mise_en_place": ["Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01088', '01089', '01090', '01091', '01088')"],
        "declencher": ["Puzzle.Reveal('tm014')"],
        "verifier": "michelangelo_mains",
        "attendu": {"en_jeu": ["tm014"], "menace": [["tm014", 4]], "deck0": 2, "defausse0": 3},
    },
    {
        "nom": "[michelangelo] tm014 Sewer Problems — 2 joueurs : CHAQUE joueur defausse 3 cartes de son deck, menace 4 x 2 = 8",
        "pourquoi": "deux joueurs : le deck de Michelangelo (5 -> 2) et celui de Spider-Man perdent chacun 3 cartes ; menace 8",
        **HEROS,
        "heros2": "spider_man",
        "mise_en_place": ["Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01088', '01089', '01090', '01091', '01088')"],
        "declencher": ["Puzzle.Reveal('tm014')"],
        "verifier": "michelangelo_mains",
        "attendu": {"en_jeu": ["tm014"], "menace": [["tm014", 8]], "deck0": 2, "defausse0": 3, "defausse1_min": 3},
    },
    {
        "nom": "[michelangelo] tm014 Sewer Problems — Crise 1 : une icone de Crise en jeu (le glyphe central, identique a 01108)",
        "pourquoi": "decision du 15/10/2026 : Crise 1. En jeu, le compte d'icones Crise vaut 1",
        **HEROS,
        "mise_en_place": ["Puzzle.PutIntoPlay('tm014')"],
        "declencher": [],
        "verifier": "etat_attendu",
        "attendu": {"icones": [["Crisis", 1]]},
    },
    {
        "nom": "[michelangelo] tm014 Sewer Problems — Crise : le heros ne peut pas contrer la principale tant qu'elle est en jeu",
        "pourquoi": ("principale a 5, tm014 en jeu : le CTR de base du heros ne peut pas viser la principale (cible forcee refusee), "
                     "il retire 1 menace a tm014 ou tm009 ; Booyakasha peut ensuite deplacer cette menace VERS la principale (6) : "
                     "elle ne descend jamais sous 5"),
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.PutIntoPlay('tm014')", f"Puzzle.SetThreat('{COMPLOT}', 5)"],
        "declencher": ["Puzzle.Thwart('tm001a')"],
        "cibles": [COMPLOT],
        "choisir_option": ["0"],
        "verifier": "etat_attendu",
        "attendu": {"menace_min": [[COMPLOT, 5]]},
    },
    {
        "nom": "[michelangelo] tm014 Sewer Problems — 3 icones de Boost",
        "pourquoi": "Boost 3 imprime : 3 icones de boost comptees sur la carte en jeu",
        **HEROS,
        "mise_en_place": ["Puzzle.PutIntoPlay('tm014')"],
        "declencher": [],
        "verifier": "etat_attendu",
        "attendu": {"icones_boost": [["tm014", 3]]},
    },
    # ===================================================================== tm015 Wyrm
    {
        "nom": "[michelangelo] tm015 Wyrm — Toughness : entre en jeu avec une carte de statut Tough",
        "pourquoi": "base automatique desc.Toughness : Wyrm en jeu porte Tough",
        **HEROS,
        "mise_en_place": ["Puzzle.PutIntoPlay('tm015')"],
        "declencher": [],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["tm015"], "statuts": [["tm015", "Tough"]]},
    },
    {
        "nom": "[michelangelo] tm015 Wyrm — vaincu : remelange dans le deck Rencontre (pas en defausse)",
        "pourquoi": "« When Defeated : Shuffle Wyrm into the encounter deck » : Robustesse retiree, 3 degats (3 PV) : hors jeu, dans le deck Rencontre",
        **HEROS,
        "mise_en_place": ["Puzzle.PutIntoPlay('tm015')", "Puzzle.Tough('tm015')"],
        "declencher": ["Puzzle.Damage('tm015', 3)"],
        "verifier": "etat_attendu",
        "attendu": {"hors_jeu": ["tm015"], "dans_deck_rencontre": ["tm015"]},
    },
    # ===================================================================== tm016 Smash!
    {
        "nom": "[michelangelo] tm016 Smash! — revelee sans allie : 2 degats indirects a l'identite",
        "pourquoi": "« You take 2 indirect damage » : aucun allie, les 2 degats vont a l'identite",
        **HEROS,
        "mise_en_place": [FORME_HEROS],
        "declencher": ["Puzzle.Reveal('tm016')"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 2},
    },
    {
        "nom": "[michelangelo] tm016 Smash! — revelee avec un allie : les 2 degats indirects se repartissent entre identite et allie (total 2)",
        "pourquoi": ("degats INDIRECTS : le joueur les repartit librement entre son identite et ses allies (Hulk 01050 en jeu) ; "
                     "le total subi par les deux vaut 2, rien n'est perdu ni double"),
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.PutIntoPlay('01050', under_control=True)"],
        "declencher": ["Puzzle.Reveal('tm016')"],
        "verifier": "michelangelo_indirect",
        "attendu": {"total": 2},
    },
    # ===================================================================== tm001a / tm001b : valeurs imprimees
    {
        "nom": "[michelangelo] tm001a Michelangelo — valeurs imprimees : THW 1, ATQ 1, DEF 2, PV 11, main 5",
        "pourquoi": "scan : THW 1 / ATK 1 / DEF 2, HAND SIZE 5 / HIT POINTS 11 (valeurs LUES sur la face heros en jeu)",
        **HEROS,
        "mise_en_place": [FORME_HEROS],
        "declencher": [],
        "verifier": "michelangelo_valeurs",
        "attendu": {"thwart": 1, "attack": 1, "defense": 2, "max_health": 11, "hand_size": 5},
    },
    {
        "nom": "[michelangelo] tm001b Mikey — valeurs imprimees : REC 3, PV 11, main 6",
        "pourquoi": "scan : REC 3, HAND SIZE 6 / HIT POINTS 11 (valeurs LUES sur l'alter-ego en jeu)",
        **HEROS,
        "mise_en_place": [],
        "declencher": [],
        "verifier": "michelangelo_valeurs",
        "attendu": {"recover": 3, "max_health": 11, "hand_size": 6},
    },
]

VERIFICATIONS = r'''
def michelangelo_valeurs(monde, aides):
    """Valeurs absolues de l'identite en jeu : cles de `attendu` = attributs de la face (attack, thwart, defense, recover, hand_size, max_health)."""
    attendu = aides["cas"]["attendu"]
    identite = aides["identite"](monde)
    soucis = []
    for nom, voulu in attendu.items():
        courant = getattr(identite, nom)
        if courant != voulu:
            soucis.append(f"{nom} = {courant} (attendu {voulu})")
    if soucis:
        return False, " ; ".join(soucis)
    return True, "valeurs conformes"


def michelangelo_indirect(monde, aides):
    """Total des degats subis par l'identite et par Hulk (01050)."""
    attendu = aides["cas"]["attendu"]
    identite = aides["identite"](monde)
    hulk = aides["par_id"](monde, "01050")
    total = identite.max_health - identite.health
    if hulk is not None:
        total += hulk.max_health - hulk.health
    if total != attendu["total"]:
        return False, f"total des degats = {total} (attendu {attendu['total']})"
    return True, f"total {total} (identite {identite.max_health - identite.health})"
'''
_SUITE = r'''
def michelangelo_mains(monde, aides):
    """Etat multi-joueur : `main0` (taille de la main du joueur 1), `deck0`/`defausse0` (tailles), `defausse1_min`,
    `hors_jeu` / `en_jeu` (card_ids), `menace` [[id, n]]."""
    attendu = aides["cas"]["attendu"]
    soucis = []
    j0 = monde.players[0]
    if "main0" in attendu:
        n = len(list(j0.hand_cards.GetAll()))
        if n != attendu["main0"]:
            soucis.append(f"main du joueur 1 = {n} (attendu {attendu['main0']})")
    if "deck0" in attendu:
        n = len(list(j0.player_deck.Get(True)))
        if n != attendu["deck0"]:
            soucis.append(f"deck du joueur 1 = {n} (attendu {attendu['deck0']})")
    if "defausse0" in attendu:
        n = len(list(j0.discard_pile.GetAll()))
        if n != attendu["defausse0"]:
            soucis.append(f"defausse du joueur 1 = {n} (attendu {attendu['defausse0']})")
    if "defausse1_min" in attendu:
        n = len(list(monde.players[1].discard_pile.GetAll()))
        if n < attendu["defausse1_min"]:
            soucis.append(f"defausse du joueur 2 = {n} (attendu au moins {attendu['defausse1_min']})")
    if attendu.get("un_seul_en_jeu"):
        presents = [cid for cid in attendu["un_seul_en_jeu"] if aides["par_id"](monde, cid) is not None]
        if len(presents) != 1:
            soucis.append(f"en jeu parmi {attendu['un_seul_en_jeu']} : {presents} (attendu exactement une)")
    for cid in attendu.get("hors_jeu") or []:
        if aides["par_id"](monde, cid) is not None:
            soucis.append(f"{cid} est encore en jeu")
    for cid in attendu.get("en_jeu") or []:
        if aides["par_id"](monde, cid) is None:
            soucis.append(f"{cid} n'est pas en jeu")
    for cid, voulu in attendu.get("menace") or []:
        f = aides["par_id"](monde, cid)
        if f is None or f.threat != voulu:
            soucis.append(f"menace sur {cid} = {None if f is None else f.threat} (attendu {voulu})")
    if soucis:
        return False, " ; ".join(soucis)
    return True, "etat multi-joueur conforme"


def michelangelo_couch(monde, aides):
    """Taille du deck (`deck`) et de la defausse (`defausse`) du joueur 1 ; `exhausted` / `pret` comme etat_attendu."""
    attendu = aides["cas"]["attendu"]
    joueur = monde.players[0]
    n_deck = len(list(joueur.player_deck.Get(True)))
    n_def = len(list(joueur.discard_pile.GetAll()))
    soucis = []
    if n_deck != attendu["deck"]:
        soucis.append(f"deck = {n_deck} carte(s) (attendu {attendu['deck']})")
    if n_def != attendu["defausse"]:
        soucis.append(f"defausse = {n_def} carte(s) (attendu {attendu['defausse']})")
    for cid in attendu.get("exhausted") or []:
        f = aides["par_id"](monde, cid)
        if f is None or not f.IsExhaust():
            soucis.append(f"{cid} n'est pas incline")
    for cid in attendu.get("pret") or []:
        f = aides["par_id"](monde, cid)
        if f is None or f.IsExhaust():
            soucis.append(f"{cid} n'est pas pret")
    if soucis:
        return False, " ; ".join(soucis)
    return True, f"deck {n_deck}, defausse {n_def}"


def michelangelo_jouable(monde, aides):
    """`attendu` = {"carte": id, "jouable": bool} : la carte EN MAIN est-elle jouable (`CanPlayBy`) ?"""
    attendu = aides["cas"]["attendu"]
    joueur = monde.players[0]
    main = [f for f in joueur.hand_cards.GetAll() if getattr(f.paper, "card_id", None) == attendu["carte"]]
    if not main:
        return False, f"{attendu['carte']} absente de la main"
    jouable = bool(main[0].CanPlayBy(joueur))
    if jouable != attendu["jouable"]:
        return False, f"{attendu['carte']} jouable={jouable} (attendu {attendu['jouable']})"
    return True, f"{attendu['carte']} jouable={jouable}"


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
'''

VERIFICATIONS = VERIFICATIONS + _SUITE
