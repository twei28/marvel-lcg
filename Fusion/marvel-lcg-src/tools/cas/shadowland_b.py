# Cas test_capacites du scenario 2 SHADOWLAND « Shadow Labyrinth » (sets Shadow Labyrinth sl037-sl045 et Deadly Contraptions sl046-sl056). Prefixe de nom `[slb]`.
# Scenario REEL `shadow_labyrinth` (graine 42 -> vilain Dark Protege Elektra sl014 tire a la mise en place), Spider-Man en forme heros (identite 01001a, 10 PV ; l'alter-ego est 01001b).
# Les pieges se revelent par `Puzzle.Reveal('sl05x')` ; `dessus(...)` pose un piege au sommet du paquet piege. La main est fixee par `main_exclusive`.
HEROS = "spider_man"
FORME_HEROS = "Puzzle.ChangeForm('01001b')"
DECK10 = ["Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck(" + ", ".join(["'01086'"] * 10) + ")"]
AVANCE = "Puzzle.AdvanceMainScheme(1)"          # 1B -> 2A -> 2B : Shifting Corridors de cote, Elektra (face A) est le vilain
TOUS_LES_PIEGES = ["sl040", "sl050", "sl051", "sl052", "sl053", "sl054", "sl055", "sl056"]


def _t(nom, pourquoi, mise, declencher, attendu, forme_heros=True, scenario="shadow_labyrinth", avant_forme=(), **cle):
    """Cas du scenario REEL `shadow_labyrinth` (graine 42), Spider-Man en forme heros (`avant_forme` : commandes jouees AVANT le changement de forme, qui remet la menace a 0)."""
    cas = {"nom": "[slb] " + nom, "pourquoi": pourquoi, "scenario": scenario, "heros": HEROS,
           "mise_en_place": ["Puzzle.EmptyHand()", *avant_forme, *([FORME_HEROS] if forme_heros else []), *mise], "declencher": declencher, "verifier": "slb_etat", "attendu": attendu,
           "main_exclusive": cle.pop("main_exclusive", ["01088"])}
    cas.update(cle)
    return cas


def dessus(*ids):
    """Met ces pieges (le DERNIER nomme est au sommet) au-dessus du paquet piege : sortis puis remis."""
    return [c for i in ids for c in (f"Puzzle.MoveTo('{i}', 'AsideScenario')", f"Puzzle.MoveTo('{i}', 'TrapDeck')")]


def sans_pieges(*ids):
    """Retire ces cartes du paquet piege (elles quittent la partie)."""
    return [f"Puzzle.MoveTo('{i}', 'RemovedArea')" for i in ids]


CAS = [
    # ------------------------------------------------------------------------------------------------------ sl038a : mise en place
    _t("sl038a Setup : le paquet piege contient les 8 cartes TRAP! (Whisper in the Dark + les 7 pieges), la defausse piege est vide", "« Create the trap deck »",
       [], [], {"paquet_pieges": 8, "defausse_pieges": 0, "dans_paquet_piege": TOUS_LES_PIEGES}),
    _t("sl038a Setup avec le modulaire Arcade (3 cartes PIEGE ! : 47031 a 47033) : les 3 cartes PIEGE ! d'Arcade rejoignent le deck Piege (11 cartes) et ne sont plus dans le deck de rencontre",
       "livret FR p. 12 : « integrez-les egalement au deck Piege »", [], [], {"paquet_pieges": 11, "dans_paquet_piege": TOUS_LES_PIEGES + ["47031", "47032", "47033"]},
       modulaires_en_plus=["arcade"]),
    _t("sl038a Setup SANS Arcade, TEMOIN : seulement les 8 cartes (aucune carte d'un autre set)", "le deck Piege ne grossit que si un modulaire PIEGE ! est choisi",
       [], [], {"paquet_pieges": 8}),
    _t("sl038a Setup : un vilain Dark Protege est tire et RESTE de cote (aucun n'est en jeu), seules ses cartes liees sont dans le deck de rencontre", "« Choose 1 random villain ... shuffle each card linked to that villain into the encounter deck (keep the chosen villain set aside) »",
       [], [], {"vilain_choisi_de_cote": True, "vilains": ["sl037"]}),
] + [
    _t(f"sl038a Setup, graine {g} : le vilain tire et ses cartes liees sont COHERENTS", "le tirage change avec la graine ; l'invariant (liees = nommant ce vilain, toutes) reste",
       [], [], {"vilain_choisi_de_cote": True, "vilains": ["sl037"]}, graine=g) for g in range(1, 7)
] + [
    # ------------------------------------------------------------------------------------------------------ sl038b : 1B
    _t("sl038b Revele : 10 compteurs passage par joueur sur Shifting Corridors (1 joueur : 10)", "« Place 10[per_hero] passage counters on Shifting Corridors »",
       [], [], {"compteurs": [["sl037", "passage", 10]]}),
    _t("sl038b Revele a 2 joueurs : 20 compteurs passage", "10 PAR joueur", [], [], {"compteurs": [["sl037", "passage", 20]]}, heros2="spider_man"),
    _t("sl038b Revele en mode expert : 7 compteurs passage par joueur", "« (7[per_hero] instead in expert mode) »",
       [], [], {"compteurs": [["sl037", "passage", 7]]}, scenario="shadow_labyrinth_expert"),
    _t("sl038b Revele en expert a 2 joueurs : 14 compteurs", "7 PAR joueur en expert", [], [], {"compteurs": [["sl037", "passage", 14]]}, scenario="shadow_labyrinth_expert", heros2="spider_man"),
    _t("sl038b : 3 degats sur Shifting Corridors deviennent 3 menaces retirees du complot (25 -> 22), les degats ne s'accumulent pas", "« When Shifting Corridors would take any amount of damage, remove that much threat from here instead »",
       [], ["Puzzle.Damage('sl037', 3)"], {"menace": [["sl038b", 22]], "jetons": [["sl037", "damage", 0]]}),
    _t("sl038b : l'attaque de base du heros (ATQ 2) sur Shifting Corridors retire 2 menaces (25 -> 23)", "meme regle, par une vraie attaque",
       [], ["Puzzle.Attack('01001a')"], {"menace": [["sl038b", 23]]}),
    _t("sl038b : plus de degats (7) que de menace restante (3) : toute la menace part et le complot avance", "« remove that much threat » : jamais plus que la menace restante",
       ["Puzzle.SetThreat('sl038b', 3)"], ["Puzzle.Damage('sl037', 7)"], {"face_visible": [["sl039", "sl039b"]], "vilains": ["sl014a"]}),
    _t("sl038b : la derniere menace retiree FAIT AVANCER au stade 2 : Shifting Corridors de cote, le vilain choisi (Elektra, face A) en jeu, complot 2B",
       "« When the last threat is removed from this scheme, advance to stage 2A »", [], ["Puzzle.Damage('sl037', 25)"],
       {"vilains": ["sl014a"], "mis_de_cote_scenario": ["sl037"], "face_visible": [["sl039", "sl039b"]], "pas_finie": True}),
    _t("sl038b, TEMOIN : tant qu'il reste de la menace (1), le complot n'avance pas", "pas d'avance avant la derniere menace",
       ["Puzzle.SetThreat('sl038b', 2)"], ["Puzzle.Damage('sl037', 1)"], {"menace": [["sl038b", 1]], "vilains": ["sl037"], "face_visible": [["sl039", "sl039a"]]}),
    # ------------------------------------------------------------------------------------------------------ sl039a / sl039b : stade 2
    _t("sl039a Revele (standard) : Shifting Corridors est de cote (pas defausse), le vilain choisi est revele en face A",
       "« 1. Set Shifting Corridors aside. 3. Reveal the chosen villain's side A »", [], [AVANCE],
       {"vilains": ["sl014a"], "mis_de_cote_scenario": ["sl037"], "taille_defausse_rencontre": 0}),
    _t("sl039a Revele en EXPERT : le vilain choisi est revele en face B", "« side B instead in expert mode »", [], [AVANCE],
       {"vilains": ["sl014b"], "mis_de_cote_scenario": ["sl037"]}, scenario="shadow_labyrinth_expert"),
    # ------------------------------------------------------------------------------------------------------ sl037 : Shifting Corridors
    _t("sl037 : quand il s'active contre le heros (attaque), a LA PLACE : un compteur passage de moins (10 -> 9), le piege du dessus est revele (Caltrops : Trip, 2 degats et etourdi), aucune attaque du vilain",
       "« instead remove 1 passage counter from here and reveal the top card of the trap deck »", dessus("sl051"), ["Puzzle.Attack('sl037')"],
       {"compteurs": [["sl037", "passage", 9]], "degats_identite": 2, "statuts": [["01001a", "Stunned"]], "paquet_pieges": 7, "dans_defausse_piege": ["sl051"], "menace": [["sl038b", 25]]}),
    _t("sl037 en forme ALTER-EGO (manigance) : meme remplacement (passage 9) ; Poison Darts avec 2 mentales en main : Trip, 3 degats et alter-ego epuise", "l'activation est remplacee, qu'elle soit une attaque ou une manigance",
       dessus("sl054"), ["Puzzle.Scheme('sl037')"], {"compteurs": [["sl037", "passage", 9]], "degats_identite": 3, "exhausted": ["01001b"], "paquet_pieges": 7},
       forme_heros=False, main_exclusive=["01089"]),
    _t("sl037, TEMOIN : sans activation, les 10 compteurs restent et le paquet piege garde ses 8 cartes", "rien ne part sans activation",
       [], [], {"compteurs": [["sl037", "passage", 10]], "paquet_pieges": 8, "defausse_pieges": 0, "degats_identite": 0}),
    _t("sl037 : le DERNIER compteur passage retire (1 -> 0) : les joueurs PERDENT, aucun piege n'est plus revele", "« If the last passage counter is removed from here, the players lose the game »",
       ["Puzzle.Counter('sl037', 'passage', -9)"], ["Puzzle.Attack('sl037')"], {"perdue": True, "compteurs": [["sl037", "passage", 0]], "paquet_pieges": 8}),
    _t("sl037, TEMOIN : avec 2 compteurs restants, un seul est retire (1) et la partie continue", "la defaite n'a lieu qu'au dernier",
       ["Puzzle.Counter('sl037', 'passage', -8)"] + dessus("sl051"), ["Puzzle.Attack('sl037')"], {"compteurs": [["sl037", "passage", 1]], "pas_finie": True}),
    _t("sl037 est Stalwart (natif) : un etourdissement est refuse", "« Stalwart »", [], ["Puzzle.Stun('sl037')"], {"statuts_absents": [["sl037", "Stunned"]]}),
    # ------------------------------------------------------------------------------------------------------ sl039b : stade 2B
    _t("sl039b : apres un contre du heros sur le complot, le piege du dessus est revele (Flame Spout : Trip, 3 degats, 3 cartes du deck defaussees)",
       "« After you ... thwarts this scheme, reveal the top card of the trap deck »", [AVANCE, "Puzzle.SetThreat('sl039b', 6)", *DECK10, *dessus("sl052")], ["Puzzle.Thwart('01001a')"],
       {"menace": [["sl039b", 5]], "paquet_pieges": 7, "dans_defausse_piege": ["sl052"], "degats_identite": 3, "taille_deck_joueur": 7}),
    _t("sl039b, LIMITE « une fois par round et par joueur » : un 2e contre du MEME joueur (son allie Black Widow) dans le round ne revele rien (paquet 7, degats 2 : un seul Caltrops)",
       "« (Limit once per round per player.) »", [AVANCE, "Puzzle.SetThreat('sl039b', 6)", *dessus("sl051"), "Puzzle.PutIntoPlay('01075', under_control=True)"],
       ["Puzzle.Thwart('01001a')", "Puzzle.Thwart('01075')"], {"menace": [["sl039b", 3]], "paquet_pieges": 7, "degats_identite": 2}),
    _t("sl039b : « you OR AN ALLY you control » : le contre d'un ALLIE seul (Black Widow) revele aussi le piege", "un allie compte",
       [AVANCE, "Puzzle.SetThreat('sl039b', 6)", *dessus("sl051"), "Puzzle.PutIntoPlay('01075', under_control=True)"], ["Puzzle.Thwart('01075')"],
       {"menace": [["sl039b", 4]], "paquet_pieges": 7, "degats_identite": 2, "dans_defausse_piege": ["sl051"]}),
    _t("sl039b, PAR JOUEUR : le contre du 2e joueur dans le meme round revele AUSSI un piege (paquet 6)", "la limite est par joueur, pas globale",
       [AVANCE, "Puzzle.SetThreat('sl039b', 6)", "Puzzle.ChangeForm('01040b')", *dessus("sl050", "sl051")], ["Puzzle.Thwart('01001a')", "Puzzle.Thwart('01040a')"],
       {"menace": [["sl039b", 3]], "paquet_pieges": 6}, heros2="black_panther"),
    _t("sl039b, TEMOIN : sans contre, aucun piege n'est revele", "le piege ne part que sur un contre", [AVANCE], [], {"paquet_pieges": 8}),
    _t("sl039b : le vilain choisi VAINCU (Elektra face A) : les joueurs GAGNENT", "regle du jeu : le vilain vaincu = victoire (le moteur ne la declare pas seul avec d'autres vilains de cote)",
       [AVANCE], ["Puzzle.Damage('sl014a', 99)"], {"gagnee": True}),
    _t("sl039b : le vilain choisi vaincu en EXPERT (face B, Toughness : 2 coups) : victoire", "meme victoire en expert", [AVANCE], ["Puzzle.Damage('sl014b', 99)", "Puzzle.Damage('sl014b', 99)"],
       {"gagnee": True}, scenario="shadow_labyrinth_expert"),
    _t("sl039b, TEMOIN : le vilain choisi blesse sans etre vaincu : la partie continue", "pas de victoire avant la defaite", [AVANCE], ["Puzzle.Damage('sl014a', 3)"], {"pas_finie": True, "degats": [["sl014a", 3]]}),
    _t("sl039b : la menace du complot atteint 9 (cible) : les joueurs PERDENT", "« If this stage is completed, the players lose the game »", [AVANCE], ["Puzzle.SetThreat('sl039b', 9)"], {"perdue": True}),
    _t("sl039b EXPERT : a la revelation le vilain active contre CHAQUE joueur (alter-ego : manigance, au moins 1 menace sur 2B)", "« In expert mode, the villain activates against each player »",
       [], [AVANCE], {"menace_min": [["sl039b", 2]]}, scenario="shadow_labyrinth_expert", forme_heros=False),
    _t("sl039b STANDARD, TEMOIN : pas d'activation a la revelation (menace de depart seule : 1)", "l'activation est reservee au mode expert", [], [AVANCE], {"menace": [["sl039b", 1]]}, forme_heros=False),
    # ------------------------------------------------------------------------------------------------------ sl040 : Whisper in the Dark
    _t("sl040 Revele (Shifting Corridors en jeu) : le vilain choisi (Elektra) entre en jeu comme sbire ELITE a 6 PV, Guard + Villainous, engage avec le joueur, Whisper attache ; la vraie carte reste de cote",
       "« Treat attached villain as an ELITE minion with 6 printed hit points. It gains Guard. Villainous. When Revealed: ... put the set-aside chosen villain into play engaged with you, with this card attached »",
       [], ["Puzzle.Reveal('sl040')"],
       {"sosie": {"nom": "Elektra", "pv": 6, "elite": True, "guard": True, "villainous": True, "engage_avec_joueur": 0, "attaches": ["sl040"], "attaque": 2}, "vilains": ["sl037"],
        "mis_de_cote_scenario": ["sl014a"], "paquet_pieges": 7}),
    _t("sl040 : le sosie vaincu (6 degats) QUITTE la partie (« set this minion aside ») : Whisper est defausse (defausse piege), la vraie carte du vilain reste de cote, rien de generique en defausse de rencontre",
       "« When Defeated : Set this minion aside »", ["Puzzle.Reveal('sl040')"], ["Puzzle.Damage('Elektra', 6)"],
       {"aucun_sosie": True, "sosie_retire": True, "dans_defausse_piege": ["sl040"], "mis_de_cote_scenario": ["sl014a"], "pas_de_carte_generique_en_defausse": True, "taille_defausse_rencontre": 0}),
    _t("sl040, TEMOIN : le sosie blesse sans etre vaincu (5 degats) reste en jeu avec Whisper", "6 PV imprimes (pas 15)", ["Puzzle.Reveal('sl040')"], ["Puzzle.Damage('Elektra', 5)"],
       {"sosie": {"pv": 6, "attaches": ["sl040"]}}),
    _t("sl040 Revele APRES le stade 2 (Corridors de cote) : Whisper est mis de cote (aside), pas defausse, et le vilain manigance contre le joueur (au moins 1 menace de plus sur 2B)",
       "« otherwise, set this card aside and the villain schemes »", [AVANCE, "Puzzle.SetThreat('sl039b', 1)"], ["Puzzle.Reveal('sl040')"],
       {"mis_de_cote_scenario": ["sl040"], "menace_min": [["sl039b", 2]], "aucun_sosie": True, "defausse_pieges": 0}, forme_heros=False),
    _t("sl039a, Whisper encore au combat : le complot avance -> le sosie ET Whisper quittent la table, le vilain reel est revele (stade 2), Whisper en defausse piege",
       "« 2. Find the chosen Dark Protege villain. Discard each status card, token, and attached card from it »", ["Puzzle.Reveal('sl040')"], [AVANCE],
       {"aucun_sosie": True, "vilains": ["sl014a"], "dans_defausse_piege": ["sl040"], "mis_de_cote_scenario": ["sl037"], "pas_de_carte_generique_en_defausse": True}),
    # ------------------------------------------------------------------------------------------------------ sl041 : Lord Deathstrike
    _t("sl041 Revele (Corridors en jeu) : les 2 cartes du dessus du deck de rencontre sont melangees dans le paquet piege (8 -> 10), le deck de rencontre perd 2 cartes",
       "« shuffle the top 2 cards of the encounter deck into the trap deck »", ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01105', '01105', '01105')"], ["Puzzle.Reveal('sl041')"],
       {"paquet_pieges": 10, "n_dans_paquet_piege": [["01105", 2]], "taille_deck_rencontre": 1, "en_jeu": ["sl041"], "defausse_pieges": 0}),
    _t("sl041 Revele APRES le stade 2 : revele le piege du dessus (Caltrops : 2 degats, etourdi), rien n'est melange", "« otherwise, reveal the top card of the trap deck »",
       [AVANCE, *dessus("sl051"), "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01105', '01105', '01105')"], ["Puzzle.Reveal('sl041')"],
       {"paquet_pieges": 7, "dans_defausse_piege": ["sl051"], "degats_identite": 2, "taille_deck_rencontre": 3, "en_jeu": ["sl041"]}),
    _t("sl041 en BOOST : entre en jeu engage, SANS etre revelee (le paquet piege et le deck de rencontre ne bougent pas)", "« Boost: Put this minion into play engaged with you »",
       [AVANCE, "Puzzle.Exhaust('01001a')", "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01105', '01105', '01105')"], ["Puzzle.Boost('sl041')"],
       {"en_jeu": ["sl041"], "paquet_pieges": 8, "taille_deck_rencontre": 3}),
    # ------------------------------------------------------------------------------------------------------ sl042 : Dead End
    _t("sl042 Revele (Corridors en jeu) : un compteur passage retire (10 -> 9), AUCUNE menace ajoutee sur la manigance (2 de depart)", "« If Shifting Corridors is in play, remove 1 passage counter from it »",
       [], ["Puzzle.Reveal('sl042')"], {"compteurs": [["sl037", "passage", 9]], "menace": [["sl042", 2]]}),
    _t("sl042 Revele APRES le stade 2 : 1 menace de plus sur elle-meme (2 -> 3), pas de passage", "« otherwise, place 1[per_hero] threat here »",
       [AVANCE], ["Puzzle.Reveal('sl042')"], {"menace": [["sl042", 3]]}),
    _t("sl042 Revele avec 2 joueurs, apres le stade 2 : 2 menaces de plus (4 -> 6)", "1[per_hero] = 1 par joueur", [AVANCE], ["Puzzle.Reveal('sl042')"], {"menace": [["sl042", 6]]}, heros2="spider_man"),
    _t("sl042 Revele alors que Corridors n'a plus qu'UN passage : les joueurs PERDENT", "retirer le dernier compteur par une carte", ["Puzzle.Counter('sl037', 'passage', -9)"], ["Puzzle.Reveal('sl042')"], {"perdue": True}),
    # ------------------------------------------------------------------------------------------------------ sl043 : Hall of Hidden Doors
    _t("sl043 vaincue (1 menace, contre de 1) : 5 menaces retirees du complot principal (12 -> 7), puis le deck de rencontre est defausse jusqu'a la premiere manigance annexe (Dead End) ou sbire, revelee",
       "« removes 5 threat from the main scheme. They discard cards from the encounter deck until a minion or side scheme is discarded, then reveal it »",
       ["Puzzle.SetThreat('sl038b', 12)", "Puzzle.PutIntoPlay('sl043')", "Puzzle.SetThreat('sl043', 1)", "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('sl041', '01108', '01105')"],
       ["Puzzle.Thwart('01001a')"], {"menace": [["sl038b", 7]], "en_jeu": ["01108"], "defausse_rencontre": ["01105"], "dans_deck_rencontre": ["sl041"], "taille_deck_rencontre": 1, "hors_jeu": ["sl043"]},
       cibles=["sl043"]),
    _t("sl043 vaincue, le premier trouve est un SBIRE (Hydra Mercenary) : il est revele, la manigance qui suit reste dans le deck", "« a minion OR side scheme » : le premier des deux",
       ["Puzzle.PutIntoPlay('sl043')", "Puzzle.SetThreat('sl043', 1)", "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01108', '01101', '01105')"], ["Puzzle.Thwart('01001a')"],
       {"en_jeu": ["01101"], "dans_deck_rencontre": ["01108"], "defausse_rencontre": ["01105"]}, cibles=["sl043"]),
    _t("sl043 vaincue, AUCUN sbire dans le deck mais un sbire en DEFAUSSE : le deck epuise est remelange avec la defausse et la fouille continue : le sbire est revele",
       "« until a minion OR side scheme is discarded, then reveal it » : le deck s'epuise sans carte valable ; le remelange (regle du deck de rencontre epuise) met le sbire (Hydra Mercenary, en defausse) dans le deck, et on continue (defaut de `Worlds.DiscardEncounterCardsUntil` corrige le 23/10/2026)",
       ["Puzzle.PutIntoPlay('sl043')", "Puzzle.SetThreat('sl043', 1)", "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01105', '01105')", "Puzzle.CreateEncounterDiscardPile('01101')"],
       ["Puzzle.Thwart('01001a')"], {"en_jeu": ["01101"]}, cibles=["sl043"]),
    _t("sl043 vaincue, deck SANS sbire ni manigance : tout le deck est defausse, rien n'est revele (regle habituelle : le deck vide est remelange avec sa defausse : 2 cartes dans le deck, sl043 en defausse)", "« until a minion or side scheme is discarded » (aucune)",
       ["Puzzle.PutIntoPlay('sl043')", "Puzzle.SetThreat('sl043', 1)", "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01105', '01105')"], ["Puzzle.Thwart('01001a')"],
       {"taille_deck_rencontre": 2, "taille_defausse_rencontre": 1, "hors_jeu": ["sl043"]}, cibles=["sl043"]),
    _t("sl043 vaincue par le JOUEUR 2 (Black Panther) : c'est lui qui retire les 5 menaces et a qui le sbire trouve est REVELE (engage avec le joueur 2)", "« The defeating player removes 5 threat ... then reveal it »",
       ["Puzzle.SetThreat('sl038b', 12)", "Puzzle.PutIntoPlay('sl043')", "Puzzle.SetThreat('sl043', 2)", "Puzzle.ChangeForm('01040b')", "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01105', '01101', '01105')"],
       ["Puzzle.Thwart('01040a')"], {"menace": [["sl038b", 7]], "engage_avec": [["01101", 1]], "hors_jeu": ["sl043"]}, heros2="black_panther", cibles=["sl043"]),
    _t("sl043, TEMOIN : contree sans etre vaincue (menace 3, contre de 1) : rien ne se passe", "« When Defeated » seulement",
       ["Puzzle.SetThreat('sl038b', 12)", "Puzzle.PutIntoPlay('sl043')", "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01108', '01105')"], ["Puzzle.Thwart('01001a')"],
       {"menace": [["sl038b", 12], ["sl043", 2]], "taille_deck_rencontre": 2}, cibles=["sl043"]),
    _t("sl043 en BOOST : 3 menaces sur le complot principal (1 -> 4)", "« Boost: Place 3 threat on the main scheme »", [AVANCE, "Puzzle.SetThreat('sl039b', 1)", "Puzzle.Exhaust('01001a')", "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01105', '01105')"], ["Puzzle.Boost('sl043')"],
       {"menace": [["sl039b", 4]]}),
    # ------------------------------------------------------------------------------------------------------ sl044 : No Time to Think!
    _t("sl044 Revele apres le stade 2 (vilain Elektra, ATQ 2) : le vilain ATTAQUE le joueur (2 degats)", "« The villain activates against you »",
       [AVANCE, "Puzzle.Exhaust('01001a')", "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01105', '01105')"], ["Puzzle.Reveal('sl044')"], {"degats_identite": 2}),
    _t("sl044 Revele avec Shifting Corridors comme vilain : l'activation est REMPLACEE (passage 9, piege revele, aucune attaque : Caltrops 2 degats seulement)", "l'interruption de sl037 remplace l'activation",
       dessus("sl051"), ["Puzzle.Reveal('sl044')"], {"compteurs": [["sl037", "passage", 9]], "degats_identite": 2, "paquet_pieges": 7}),
    _t("sl044 revelee en BOOST d'une attaque d'Elektra : 2 icones de boost de plus (2 + 1 + 2 = 5 degats) ET overkill (l'allie Falcon, 3 PV, defend : l'exces va au heros)",
       "« If this activation is an attack, this card gains [boost][boost] and this attack gains overkill »", [AVANCE, "Puzzle.PutIntoPlay('03011', under_control=True)", "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01105', '01105')", "Puzzle.GiveFacedownBoost('sl014a', 'sl044')"],
       ["Puzzle.Attack('sl014a', defender='03011')"], {"hors_jeu": ["03011"], "degats_identite": 2, "defausse_rencontre": ["sl044"]}),
    _t("sl044 en BOOST d'une MANIGANCE : rien (la carte ne vaut que son icone de boost : 1)", "« If this activation is an attack »", [AVANCE, "Puzzle.SetThreat('sl039b', 1)", "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01105', '01105')", "Puzzle.GiveFacedownBoost('sl014a', 'sl044')"],
       ["Puzzle.Scheme('sl014a')"], {"menace": [["sl039b", 3]]}, forme_heros=False),
    # ------------------------------------------------------------------------------------------------------ sl045 : Sudden Shift
    _t("sl045 Revele : la defausse piege (1 carte) et les 3 cartes du dessus du deck de rencontre sont melangees dans le paquet piege, puis la carte du dessus est revelee (tout est « I'm Tough » : 4 cartes -> 3 restent)",
       "« Shuffle the trap discard pile and the top 3 cards of the encounter deck into the trap deck. Reveal the top card of the trap deck »",
       [*sans_pieges(*TOUS_LES_PIEGES), "Puzzle.MoveTo('01105', 'TrapDiscardPile')", "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01105', '01105', '01105', '01105')"], ["Puzzle.Reveal('sl045')"],
       {"paquet_pieges": 3, "defausse_pieges": 0, "taille_deck_rencontre": 1}),
    _t("sl045 en BOOST : defausse piege + 2 cartes du dessus melangees dans le paquet piege, RIEN n'est revele (5 cartes dans le paquet)", "« Boost: Shuffle the trap discard pile and the top 2 cards of the encounter deck into the trap deck »",
       [AVANCE, "Puzzle.Exhaust('01001a')", *sans_pieges(*TOUS_LES_PIEGES), "Puzzle.MoveTo('01105', 'TrapDiscardPile')", "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01105', '01105', '01105')"], ["Puzzle.Boost('sl045')"],
       {"paquet_pieges": 3, "defausse_pieges": 0, "taille_deck_rencontre": 1}),
    _t("sl045 : paquet piege vide ET defausse vide : rien n'est revele (le deck de rencontre perd tout de meme ses 3 cartes dans le paquet)", "pas de plantage sur un paquet vide",
       [*sans_pieges(*TOUS_LES_PIEGES), "Puzzle.EmptyEncounterDeck()"], ["Puzzle.Reveal('sl045')"], {"paquet_pieges": 0, "defausse_pieges": 0}),
    # ------------------------------------------------------------------------------------------------------ les 7 pieges de Deadly Contraptions : Avoid / Disarm / Trip
    # sl050 Blinding Powder
    _t("sl050 Avoid : defausse un evenement THWART de la main (Emergency) : aucun degat, l'autre carte reste, le piege va en defausse piege", "« Avoid — Discard a THWART event from your hand »",
       [], ["Puzzle.Reveal('sl050')"], {"defausse": ["01085"], "degats_identite": 0, "en_main": ["01088"], "dans_defausse_piege": ["sl050"]}, main_exclusive=["01085", "01088"], preferer_option="Avoid"),
    _t("sl050 Disarm : 2 cartes au hasard de la main (les 2) puis un statut Tough a un personnage controle", "« Disarm — Discard 2 cards at random from your hand, then give a character you control a tough status card »",
       [], ["Puzzle.Reveal('sl050')"], {"defausse": ["01088", "01089"], "taille_main": 0, "statuts": [["01001a", "Tough"]], "degats_identite": 0}, main_exclusive=["01088", "01089"], preferer_option="Disarm"),
    _t("sl050 Trip (seule option : pas d'evenement THWART, main d'une carte) : 2 degats a l'identite, confuse", "« Trip — Deal 2 damage to your identity and confuse it »",
       [], ["Puzzle.Reveal('sl050')"], {"degats_identite": 2, "statuts": [["01001a", "Confused"]], "en_main": ["01088"]}),
    _t("sl050, TEMOIN : un evenement DEFENSE (Backflip) n'est PAS un evenement THWART : Avoid n'est pas offerte, Trip a lieu et la carte reste en main", "Avoid ne vaut que pour un evenement THWART",
       [], ["Puzzle.Reveal('sl050')"], {"degats_identite": 2, "en_main": ["01003"]}, main_exclusive=["01003"]),
    # sl051 Caltrops
    _t("sl051 Avoid : defausse un evenement DEFENSE de la main (Backflip) : aucun degat", "« Avoid — Discard a DEFENSE event from your hand »",
       [], ["Puzzle.Reveal('sl051')"], {"defausse": ["01003"], "degats_identite": 0}, main_exclusive=["01003"], preferer_option="Avoid"),
    _t("sl051 Disarm : defausse 1 carte specifique au heros de la main (Backflip) puis 2 degats a un ennemi (Hydra Mercenary, 3 PV)", "« Disarm — Discard 1 identity-specific card from your hand, then deal 2 damage to an enemy »",
       ["Puzzle.PutIntoPlay('01101')"], ["Puzzle.Reveal('sl051')"], {"defausse": ["01003"], "degats": [["01101", 2]], "degats_identite": 0}, main_exclusive=["01003"], preferer_option="Disarm", cibles=["01101"]),
    _t("sl051 Disarm sans carte specifique au heros (main : Energy, carte de base) : pas offerte, Trip : 2 degats et etourdi", "« identity-specific » : une carte de base ne convient pas",
       ["Puzzle.PutIntoPlay('01101')"], ["Puzzle.Reveal('sl051')"], {"degats_identite": 2, "statuts": [["01001a", "Stunned"]], "degats": [["01101", 0]], "en_main": ["01088"]}, preferer_option="Disarm"),
    # sl052 Flame Spout
    _t("sl052 Avoid : defausse un allie de la main (Mockingbird)", "« Avoid — Discard an ally from your hand »",
       [], ["Puzzle.Reveal('sl052')"], {"defausse": ["01083"], "degats_identite": 0, "en_main": ["01088"]}, main_exclusive=["01083", "01088"], preferer_option="Avoid"),
    _t("sl052 Disarm : defausse un allie EN JEU (Black Widow) puis pioche 2 cartes (main 1 -> 3)", "« Disarm — Discard an ally you control, then draw 2 cards »",
       [*DECK10, "Puzzle.PutIntoPlay('01075', under_control=True)"], ["Puzzle.Reveal('sl052')"], {"defausse": ["01075"], "taille_main": 3, "degats_identite": 0}, preferer_option="Disarm"),
    _t("sl052 Trip : 3 degats a l'identite puis les 3 cartes du dessus du deck defaussees (deck 10 -> 7)", "« Trip — Deal 3 damage to your identity. Discard the top 3 cards of your deck »",
       DECK10, ["Puzzle.Reveal('sl052')"], {"degats_identite": 3, "taille_deck_joueur": 7}),
    # sl053 Oil Slick
    _t("sl053 Avoid : defausse une amelioration de la main (Web-Shooter)", "« Avoid — Discard an upgrade from your hand »",
       [], ["Puzzle.Reveal('sl053')"], {"defausse": ["01008"], "degats_identite": 0}, main_exclusive=["01008"], preferer_option="Avoid"),
    _t("sl053 Disarm : defausse une amelioration EN JEU (Web-Shooter) puis retire 4 menaces du complot principal (10 -> 6)", "« Disarm — Discard an upgrade you control, then remove 4 threat from the main scheme »",
       ["Puzzle.SetThreat('sl038b', 10)", "Puzzle.Attach('01008', '01001a')"], ["Puzzle.Reveal('sl053')"], {"defausse": ["01008"], "menace": [["sl038b", 6]]}, preferer_option="Disarm"),
    _t("sl053 Trip : 1 carte de la main defaussee puis 8 cartes du dessus du deck (main 2 -> 1, deck 10 -> 2)", "« Trip — Discard 1 card from your hand. Discard the top 8 cards of your deck »",
       DECK10, ["Puzzle.Reveal('sl053')"], {"taille_main": 1, "taille_deck_joueur": 2, "degats_identite": 0}, main_exclusive=["01088", "01089"]),
    # sl054 Poison Darts
    _t("sl054 Avoid : depenser [energy][energy] (Energy 01088) : aucun degat", "« Avoid — Spend [energy][energy] resources »",
       [], ["Puzzle.Reveal('sl054')"], {"defausse": ["01088"], "degats_identite": 0}, preferer_option="Avoid"),
    _t("sl054 Disarm : depenser [mental][mental][physical] (Genius + Strength) puis 3 degats au VILAIN : Shifting Corridors les convertit en 3 menaces retirees (25 -> 22)", "« Disarm — Spend [mental][mental][physical] resources, then deal 3 damage to the villain »",
       [], ["Puzzle.Reveal('sl054')"], {"defausse": ["01089", "01090"], "menace": [["sl038b", 22]], "degats_identite": 0}, main_exclusive=["01089", "01090"], preferer_option="Disarm"),
    _t("sl054 Disarm apres le stade 2 : 3 degats au vilain Elektra", "« deal 3 damage to the villain »",
       [AVANCE], ["Puzzle.Reveal('sl054')"], {"degats": [["sl014a", 3]], "defausse": ["01089", "01090"]}, main_exclusive=["01089", "01090"], preferer_option="Disarm"),
    _t("sl054 Trip (main : Genius seul, ni YY ni BBR) : 3 degats a l'identite et epuisee", "« Trip — Deal 3 damage to your identity and exhaust it »",
       [], ["Puzzle.Reveal('sl054')"], {"degats_identite": 3, "exhausted": ["01001a"], "en_main": ["01089"]}, main_exclusive=["01089"]),
    # sl055 Pressure Plate
    _t("sl055 Avoid : depenser [mental][mental] (Genius)", "« Avoid — Spend [mental][mental] resources »",
       [], ["Puzzle.Reveal('sl055')"], {"defausse": ["01089"], "degats_identite": 0}, main_exclusive=["01089"], preferer_option="Avoid"),
    _t("sl055 Disarm : depenser [energy][physical][physical] (Energy + Strength) puis chercher dans les 4 cartes du dessus du deck : 1 carte en main, deck 10 -> 9", "« Disarm — Spend ..., then search the top 4 cards of your deck for a card and add it to your hand »",
       DECK10, ["Puzzle.Reveal('sl055')"], {"defausse": ["01088", "01090"], "taille_main": 1, "taille_deck_joueur": 9, "degats_identite": 0}, main_exclusive=["01088", "01090"], preferer_option="Disarm"),
    _t("sl055 Trip : le deck de rencontre est defausse jusqu'au premier SBIRE (Hydra Mercenary), qui est revele ; la carte avant lui est defaussee", "« Trip — Discard cards from the top of the encounter deck until a minion is discarded, then reveal it »",
       ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01105', '01101', '01105')"], ["Puzzle.Reveal('sl055')"],
       {"en_jeu": ["01101"], "defausse_rencontre": ["01105"], "taille_deck_rencontre": 1, "degats_identite": 0}),
    # sl056 Tripwire
    _t("sl056 Avoid : defausse un evenement ATTACK de la main (Haymaker)", "« Avoid — Discard an ATTACK event from your hand »",
       [], ["Puzzle.Reveal('sl056')"], {"defausse": ["01087"], "degats_identite": 0}, main_exclusive=["01087"], preferer_option="Avoid"),
    _t("sl056 Disarm : defausse un soutien EN JEU (Aunt May) puis retire 3 menaces d'une manigance (le complot principal : 10 -> 7)", "« Disarm — Discard a support you control, then remove 3 threat from a scheme »",
       ["Puzzle.SetThreat('sl038b', 10)", "Puzzle.PutIntoPlay('01006', under_control=True)"], ["Puzzle.Reveal('sl056')"], {"defausse": ["01006"], "menace": [["sl038b", 7]]}, preferer_option="Disarm"),
    _t("sl056 Trip : le deck de rencontre est defausse jusqu'a la premiere manigance ANNEXE (Crowd Control), revelee", "« Trip — Discard cards from the top of the encounter deck until a side scheme is discarded, then reveal it »",
       ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01105', '01108', '01105')"], ["Puzzle.Reveal('sl056')"],
       {"en_jeu": ["01108"], "defausse_rencontre": ["01105"], "taille_deck_rencontre": 1}),
    # ------------------------------------------------------------------------------------------------------ sl046 : Nervous Jitters
    _t("sl046 Revele : s'attache a l'IDENTITE du joueur", "« Attach to your identity »", [], ["Puzzle.Reveal('sl046')"], {"hotes": [["sl046", "01001a"]]}),
    _t("sl046 : Avoid sur Poison Darts, type nomme « Minion » mais la carte defaussee est une TRAITRISE : 4 degats indirects et Jitters est defausse (+ l'Avoid se resout : Energy depensee)",
       "« If the card discarded this way was not of the named type, take 4 indirect damage and discard this attachment »",
       ["Puzzle.Reveal('sl046')", "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01105', '01105')"], ["Puzzle.Reveal('sl054')"],
       {"degats_identite": 4, "hors_jeu": ["sl046"], "defausse": ["01088"], "taille_deck_rencontre": 1}, preferer_option=["Avoid", "Minion"]),
    _t("sl046 : Avoid, type nomme « Minion » ET la carte defaussee est un SBIRE (Hydra Mercenary) : aucun degat, Jitters reste attache", "meme type = rien",
       ["Puzzle.Reveal('sl046')", "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01105', '01101')"], ["Puzzle.Reveal('sl054')"],
       {"degats_identite": 0, "hotes": [["sl046", "01001a"]], "defausse": ["01088"], "defausse_rencontre": ["01101"]}, preferer_option=["Avoid", "Minion"]),
    _t("sl046 : Disarm AUSSI declenche Jitters (Poison Darts Disarm : 3 degats au vilain = 3 menaces en moins ; type rate : 4 degats indirects)", "« the 'Avoid' effect or the 'Disarm' effect »",
       ["Puzzle.Reveal('sl046')", "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01105')"], ["Puzzle.Reveal('sl054')"],
       {"degats_identite": 4, "hors_jeu": ["sl046"], "menace": [["sl038b", 22]], "defausse": ["01089", "01090"]}, main_exclusive=["01089", "01090"], preferer_option=["Disarm", "Minion"]),
    _t("sl046, TEMOIN : Trip ne declenche PAS Jitters (3 degats seulement, deck de rencontre intact, Jitters reste)", "« Avoid or Disarm » seulement",
       ["Puzzle.Reveal('sl046')", "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01105')"], ["Puzzle.Reveal('sl054')"],
       {"degats_identite": 3, "hotes": [["sl046", "01001a"]], "taille_deck_rencontre": 1}, main_exclusive=["01089"]),
    _t("sl046 : Jitters porte par le joueur 1 ne reagit PAS au choix du joueur 2 (2 joueurs : le piege est revele au joueur 2, Avoid, type rate : le joueur 1 ne perd rien)", "« When YOU choose » : le porteur",
       ["Puzzle.Reveal('sl046')", "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01105')"], ["Puzzle.Reveal('sl054', by='01040a')"],
       {"degats_identite": 0, "hotes": [["sl046", "01001a"]], "taille_deck_rencontre": 1}, heros2="black_panther", main_exclusive=["01088"], forme_heros=True),
    # ------------------------------------------------------------------------------------------------------ sl047 : Iron Monk
    _t("sl047 engage avec le joueur : l'Avoid est INTERDITE (Blinding Powder, main : Emergency) : Trip, 2 degats, la carte reste en main", "« While Iron Monk is engaged with you, you cannot choose the 'Avoid' effect on TRAP! cards »",
       ["Puzzle.PutIntoPlay('sl047')"], ["Puzzle.Reveal('sl050')"], {"degats_identite": 2, "en_main": ["01085"]}, main_exclusive=["01085"], preferer_option="Avoid"),
    _t("sl047, TEMOIN : sans Iron Monk, la meme main permet l'Avoid (Emergency defaussee, aucun degat)", "la carte seule interdit l'Avoid",
       [], ["Puzzle.Reveal('sl050')"], {"degats_identite": 0, "defausse": ["01085"]}, main_exclusive=["01085"], preferer_option="Avoid"),
    _t("sl047, TEMOIN : Disarm reste permis sous Iron Monk (Poison Darts : 3 degats au vilain = 3 menaces en moins)", "seule l'option Avoid est interdite",
       ["Puzzle.PutIntoPlay('sl047')"], ["Puzzle.Reveal('sl054')"], {"menace": [["sl038b", 22]], "defausse": ["01089", "01090"], "degats_identite": 0}, main_exclusive=["01089", "01090"], preferer_option="Disarm"),
    _t("sl047, TEMOIN : sous Iron Monk, Trip reste permis (Poison Darts, main : Genius : 3 degats et epuise)", "Trip n'est pas interdit",
       ["Puzzle.PutIntoPlay('sl047')"], ["Puzzle.Reveal('sl054')"], {"degats_identite": 3, "exhausted": ["01001a"]}, main_exclusive=["01089"]),
    _t("sl047 engage avec le JOUEUR 2 seulement : le joueur 1 peut encore choisir l'Avoid (Emergency defaussee, aucun degat)", "« engaged with YOU »",
       ["Puzzle.PutIntoPlay('sl047', player=1)"], ["Puzzle.Reveal('sl050')"], {"degats_identite": 0, "defausse": ["01085"]}, heros2="black_panther", main_exclusive=["01085"], preferer_option="Avoid"),
    # ------------------------------------------------------------------------------------------------------ sl048 : Hall of Punishment
    _t("sl048 en jeu : le choix de Trip (Caltrops) fait defausser les 3 cartes du dessus du DECK du joueur (10 -> 7), en plus des 2 degats et de l'etourdissement", "« When you choose the 'Trip' effect on a TRAP! card, discard the top 3 cards of your deck »",
       [*DECK10, "Puzzle.PutIntoPlay('sl048')"], ["Puzzle.Reveal('sl051')"], {"taille_deck_joueur": 7, "degats_identite": 2, "statuts": [["01001a", "Stunned"]]}),
    _t("sl048 en jeu, TEMOIN : Avoid (Caltrops, Backflip) ne defausse rien du deck (10)", "Trip seulement",
       [*DECK10, "Puzzle.PutIntoPlay('sl048')"], ["Puzzle.Reveal('sl051')"], {"taille_deck_joueur": 10, "defausse": ["01003"]}, main_exclusive=["01003"], preferer_option="Avoid"),
    _t("sl048 en BOOST (manigance d'Elektra, forme alter-ego) : 1 menace sur le complot par personnage controle (alter-ego seul : 1 + SCH 1 d'Elektra = 3 sur 2B depuis 1)", "« Boost: Place 1 threat on the main scheme for each character you control »",
       [AVANCE, "Puzzle.SetThreat('sl039b', 1)", "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01105', '01105')"], ["Puzzle.Boost('sl048')"], {"menace": [["sl039b", 3]]}, forme_heros=False),
    _t("sl048 en BOOST avec un allie (Black Widow) : 2 personnages = 2 menaces (1 + 1 + 2 = 4)", "« each character you control » : allies compris",
       [AVANCE, "Puzzle.SetThreat('sl039b', 1)", "Puzzle.PutIntoPlay('01075', under_control=True)", "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01105', '01105')"], ["Puzzle.Boost('sl048')"],
       {"menace": [["sl039b", 4]]}, forme_heros=False),
    # ------------------------------------------------------------------------------------------------------ sl049 : Path of a Thousand Cuts
    _t("sl049 en jeu : l'Avoid (Poison Darts, Energy depensee) coute 2 degats INDIRECTS", "« When you choose the 'Avoid' effect or the 'Trip' effect on a TRAP! card, take 2 indirect damage »",
       ["Puzzle.PutIntoPlay('sl049')"], ["Puzzle.Reveal('sl054')"], {"degats_identite": 2, "defausse": ["01088"]}, preferer_option="Avoid"),
    _t("sl049 en jeu : le Trip (Caltrops : 2 degats, etourdi) coute 2 degats indirects de plus (4)", "Trip aussi",
       ["Puzzle.PutIntoPlay('sl049')"], ["Puzzle.Reveal('sl051')"], {"degats_identite": 4, "statuts": [["01001a", "Stunned"]]}),
    _t("sl049 en jeu, TEMOIN : le Disarm (Poison Darts : 3 degats au vilain) ne coute rien a l'identite", "Disarm n'est PAS cite",
       ["Puzzle.PutIntoPlay('sl049')"], ["Puzzle.Reveal('sl054')"], {"degats_identite": 0, "menace": [["sl038b", 22]]}, main_exclusive=["01089", "01090"], preferer_option="Disarm"),
    _t("sl049 en BOOST (manigance d'Elektra, alter-ego) : 1 degat a CHAQUE personnage controle : l'alter-ego ET l'allie Black Widow", "« Boost: Deal 1 damage to each character you control »",
       [AVANCE, "Puzzle.PutIntoPlay('01075', under_control=True)", "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01105', '01105')"], ["Puzzle.Boost('sl049')"],
       {"degats_identite": 1, "degats": [["01075", 1]]}, forme_heros=False),
    # ------------------------------------------------------------------------------------------------------ mots-cles et icones natifs (lus dans desc ; cas de DONNEES, verts sans module)
    _t("sl042 Dead End : Assault natif : le contre de base du heros (THW 1, ATQ 2) retire 2 menaces (2 de depart : vaincue)", "« Assault. (Basic thwarts against this scheme use ATK instead of THW.) »",
       ["Puzzle.PutIntoPlay('sl042')"], ["Puzzle.Thwart('01001a')"], {"hors_jeu": ["sl042"]}, cibles=["sl042"]),
    _t("sl042 Dead End porte 1 icone CRISIS", "icone imprimee (point d'exclamation)", ["Puzzle.PutIntoPlay('sl042')"], [], {"icones": [["Crisis", 1]], "icones_boost": [["sl042", 3]]}),
    _t("sl043 Hall of Hidden Doors porte 1 icone ACCELERATION (3 menaces de depart, pas par joueur)", "icone imprimee (toit avec une croix)", ["Puzzle.PutIntoPlay('sl043')"], [],
       {"icones": [["Acceleration", 1]], "menace": [["sl043", 3]]}),
    _t("sl047 Iron Monk : Toughness natif (statut Tough a l'entree en jeu), 4 PV", "« Patrol. Toughness. » et PV 4", ["Puzzle.PutIntoPlay('sl047')"], [], {"statuts": [["sl047", "Tough"]], "pv_max": [["sl047", 4]]}),
    _t("sl047 Iron Monk : Patrol natif : engage, il interdit au heros de contrer le complot principal (25 reste 25)", "« Patrol »", ["Puzzle.PutIntoPlay('sl047')"], ["Puzzle.Thwart('01001a')"], {"menace": [["sl038b", 25]]}),
    _t("sl041 Lord Deathstrike : Patrol natif, 5 PV", "« Patrol. »", ["Puzzle.PutIntoPlay('sl041')"], ["Puzzle.Thwart('01001a')"], {"menace": [["sl038b", 25]], "pv_max": [["sl041", 5]]}),
    _t("sl048 Hall of Punishment porte 1 icone CRISIS (2 menaces de depart par joueur)", "icone imprimee", ["Puzzle.PutIntoPlay('sl048')"], [], {"icones": [["Crisis", 1]], "menace": [["sl048", 2]]}),
    _t("sl049 Path of a Thousand Cuts : 5 menaces de depart (fixe)", "pas de menace par joueur", ["Puzzle.PutIntoPlay('sl049')"], [], {"menace": [["sl049", 5]]}, heros2="spider_man"),
]


VERIFICATIONS = r'''
def slb_etat(monde, aides):
    """etat_attendu + cles du scenario Shadow Labyrinth :
    `dans_paquet_piege` / `dans_defausse_piege` : [card_id] presents ; `n_dans_paquet_piege` : [[card_id, n]] ; `dessus_paquet_piege` : card_id du sommet ;
    `taille_deck_rencontre` / `taille_defausse_rencontre` ; `vilains` : card_id des vilains EN JEU (liste exacte) ; `gagnee` / `perdue` : fin de partie ;
    `face_visible` : [[prefixe, card_id]] ; `vilain_choisi_de_cote` : le vilain Dark Protege tire est de cote, ses cartes liees (et elles seules) sont dans le deck ;
    `sosie` : le vilain traite comme un sbire (Whisper in the Dark) ; `aucun_sosie` ; `pas_de_carte_generique_en_defausse` ; `engage_avec` : [[card_id, rang du joueur]] ; `sosie_retire` : un sosie a existe et n'est plus en jeu."""
    import re as _re
    from game.operate.worlds import Worlds as _W
    cas = aides["cas"]
    attendu = cas.get("attendu") or {}
    soucis = []
    decks = getattr(monde, "scenario_decks", {}) or {}
    piege = decks.get("TrapDeck")

    def ids(faces):
        return [str(getattr(f.paper, "card_id", "?")) for f in faces]

    if attendu.get("debug"):
        lignes = []
        for objet in monde.object_manager.card_dict.values():
            face = getattr(objet, "face", None)
            if face is None:
                continue
            zone = getattr(getattr(getattr(objet, "area", None), "deck_type", None), "name", "?")
            if zone in ("PlayerDeck", "HandsArea", "DiscardPile") or (str(face.paper.card_id).startswith("0") and str(face.paper.card_id) not in ("01101", "01105")):
                continue
            lignes.append(f"{face.paper.card_id}@{zone}")
        lignes.append("GAMEOVER=" + str(monde.is_game_over))
        lignes.append("ENC=" + ",".join(ids(_W.GetEncounterDeckCards(monde)[:6])))
        if piege is not None and piege.initialize:
            lignes.append("PIEGE=" + ",".join(ids(piege.deck.GetAll())) + " DEFAUSSE=" + ",".join(ids(piege.discard_pile.GetAll())))
        return False, " | ".join(sorted(lignes))[:3500]

    if "dans_paquet_piege" in attendu:
        presents = ids(piege.deck.GetAll()) if piege is not None and piege.initialize else None
        for c in attendu["dans_paquet_piege"]:
            if presents is None or c not in presents:
                soucis.append(f"{c} absent du paquet piege ({presents})")
    if "dans_defausse_piege" in attendu:
        presents = ids(piege.discard_pile.GetAll()) if piege is not None and piege.initialize else None
        for c in attendu["dans_defausse_piege"]:
            if presents is None or c not in presents:
                soucis.append(f"{c} absent de la defausse piege ({presents})")
    for c, n in attendu.get("n_dans_paquet_piege") or []:
        reel = ids(piege.deck.GetAll()).count(c) if piege is not None and piege.initialize else None
        if reel != n:
            soucis.append(f"{reel} exemplaire(s) de {c} dans le paquet piege (attendu {n})")
    if "dessus_paquet_piege" in attendu:
        haut = ids(piege.deck.Get(True))[:1] if piege is not None and piege.initialize else None
        if haut != [attendu["dessus_paquet_piege"]]:
            soucis.append(f"sommet du paquet piege {haut} (attendu {attendu['dessus_paquet_piege']})")
    if "taille_deck_rencontre" in attendu:
        n = len(_W.GetEncounterDeckCards(monde))
        if n != attendu["taille_deck_rencontre"]:
            soucis.append(f"deck de rencontre = {n} carte(s) (attendu {attendu['taille_deck_rencontre']})")
    if "taille_defausse_rencontre" in attendu:
        n = len(_W.GetEncounterDiscardPileCards(monde))
        if n != attendu["taille_defausse_rencontre"]:
            soucis.append(f"defausse de rencontre = {n} carte(s) (attendu {attendu['taille_defausse_rencontre']})")
    if attendu.get("pas_de_carte_generique_en_defausse"):
        parasites = [i for i in ids(_W.GetEncounterDiscardPileCards(monde)) if i in ("Minion", "rule_a")]
        if parasites:
            soucis.append(f"carte generique dans la defausse de rencontre : {parasites}")
    if "vilains" in attendu:
        vus = sorted(ids(_W.GetAllVillains(monde)))
        if vus != sorted(attendu["vilains"]):
            soucis.append(f"vilains en jeu {vus} (attendu {sorted(attendu['vilains'])})")
    if "gagnee" in attendu or "perdue" in attendu:
        if not monde.is_game_over:
            soucis.append("la partie n'est pas finie")
        else:
            gagnee = bool(getattr(monde.game_over, "players_won", False))
            if "gagnee" in attendu and gagnee != attendu["gagnee"]:
                soucis.append(f"players_won = {gagnee} (attendu {attendu['gagnee']})")
            if "perdue" in attendu and (not gagnee) != attendu["perdue"]:
                soucis.append(f"players_won = {gagnee} (attendu perdue = {attendu['perdue']})")
    if attendu.get("pas_finie") and monde.is_game_over:
        soucis.append("la partie est finie")
    for prefixe, voulu in attendu.get("face_visible") or []:
        vues = []
        for objet in monde.object_manager.card_dict.values():
            face = getattr(objet, "face", None)
            cid = str(getattr(getattr(face, "paper", None), "card_id", ""))
            if cid.startswith(prefixe) and cid not in vues:
                vues.append(cid)
        if vues != [voulu]:
            soucis.append(f"faces montrees pour {prefixe} : {vues} (attendu {voulu})")
    if attendu.get("vilain_choisi_de_cote"):
        base = getattr(monde, "sl_vilain_choisi", None)
        vilains = [f for f in monde.aside_deck.GetAll() if _re.match(r"^sl01[2-7][ab]?$", str(f.paper.card_id))]
        courants = sorted(str(f.paper.card_id) for f in vilains)
        if base is None or len(vilains) != 6:
            soucis.append(f"vilain choisi {base} ; vilains Dark Protege de cote : {courants} (attendu 6)")
        elif not any(c.startswith(base) for c in courants):
            soucis.append(f"le vilain choisi {base} n'est pas de cote : {courants}")
        else:
            nom = [f for f in vilains if str(f.paper.card_id).startswith(base)][0].paper.name.lstrip("* ").strip()
            def lies(face):
                m = _re.search(r"Linked \(([^)]*)\)", face.paper.text or "")
                return [] if m is None else [m.group(1)]
            liees = [f"sl0{n}" for n in range(18, 28)]
            deck = [f for f in _W.GetEncounterDeckCards(monde) if str(f.paper.card_id) in liees]
            cote = [f for f in monde.aside_deck.GetAll() if str(f.paper.card_id) in liees]
            faux = [str(f.paper.card_id) for f in deck if not any(nom in s for s in lies(f))]
            manque = [str(f.paper.card_id) for f in cote if any(nom in s for s in lies(f))]
            if faux: soucis.append(f"dans le deck mais PAS lies a {nom} : {faux}")
            if manque: soucis.append(f"lies a {nom} mais restees de cote : {manque}")
            if not deck: soucis.append(f"aucune carte liee a {nom} dans le deck de rencontre")
    sosies = [o.face for o in monde.object_manager.card_dict.values()
              if getattr(getattr(o, "face", None), "sl_sosie_du_vilain", False) and o.face.IsInPlay()]
    for card_id, rang in attendu.get("engage_avec") or []:
        face = aides["par_id"](monde, card_id)
        if face is None:
            soucis.append(f"{card_id} introuvable en jeu (engage_avec)")
        elif face.GetEngagedPlayer() is not monde.const_players[rang]:
            soucis.append(f"{card_id} engage avec {face.GetEngagedPlayer()} (attendu le joueur {rang})")
    if attendu.get("sosie_retire"):
        tous = [o.face for o in monde.object_manager.card_dict.values() if getattr(getattr(o, "face", None), "sl_sosie_du_vilain", False)]
        if not tous:
            soucis.append("aucun sosie n'a jamais existe (la revelation de Whisper n'a rien cree)")
        elif any(t.IsInPlay() for t in tous):
            soucis.append("un sosie est encore en jeu")
    if attendu.get("aucun_sosie") and sosies:
        soucis.append(f"un sosie du vilain est encore en jeu : {[s.name for s in sosies]}")
    voulu = attendu.get("sosie")
    if voulu is not None:
        if len(sosies) != 1:
            soucis.append(f"{len(sosies)} sosie(s) en jeu (attendu 1)")
        else:
            s = sosies[0]
            if voulu.get("nom") and voulu["nom"] not in s.name:
                soucis.append(f"nom du sosie {s.name} (attendu {voulu['nom']})")
            if "pv" in voulu and s.max_health != voulu["pv"]:
                soucis.append(f"PV max du sosie {s.max_health} (attendu {voulu['pv']})")
            if voulu.get("elite") and not s.HasTrait("ELITE"):
                soucis.append("le sosie n'est pas ELITE")
            if voulu.get("guard") and not s.IsGuard():
                soucis.append("le sosie n'a pas Guard")
            if voulu.get("villainous") and not s.IsVillainous():
                soucis.append("le sosie n'est pas Villainous")
            if "engage_avec_joueur" in voulu:
                reel = s.GetEngagedPlayer()
                if reel is not monde.players[voulu["engage_avec_joueur"]]:
                    soucis.append(f"sosie engage avec {reel}")
            for a in voulu.get("attaches") or []:
                if a not in ids(s.GetAttachedAttachments()):
                    soucis.append(f"{a} n'est pas attache au sosie ({ids(s.GetAttachedAttachments())})")
            if "attaque" in voulu and s.attack != voulu["attaque"]:
                soucis.append(f"ATQ du sosie {s.attack} (attendu {voulu['attaque']})")
    reste = {k: v for k, v in attendu.items() if k not in (
        "dans_paquet_piege", "dans_defausse_piege", "n_dans_paquet_piege", "dessus_paquet_piege", "taille_deck_rencontre", "taille_defausse_rencontre",
        "pas_de_carte_generique_en_defausse", "vilains", "gagnee", "perdue", "pas_finie", "face_visible", "vilain_choisi_de_cote", "aucun_sosie", "sosie", "engage_avec", "sosie_retire")}
    cas["attendu"] = reste
    try:
        ok, msg = etat_attendu(monde, aides)
    finally:
        cas["attendu"] = attendu
    if not ok:
        soucis.append(msg)
    return (False, " ; ".join(soucis)) if soucis else (True, "etat conforme")
'''
