# Cas test_capacites du heros VENUS (TMNT Heroes v3, Inkwire, prefixe `tv`) : nom prefixe « [venus] ».
# Un cas par capacite, sujet = le card_id dans le nom (substituer_pack.py filtre dessus).
# Gabarits PROCESSUS-CARTE : docs/packs/venus_cartes.md. Questions en attente :
# .planning/tmnt/venus-questions.md. Decisions : .planning/tmnt/decisions-phase-b.md.
#
# Rappels de montage :
#  - Venus demarre en ALTER EGO (tv001b, Bonnie) ; `Puzzle.ChangeToFace('tv001b', 'tv001a')` la passe
#    en forme HEROS ;
#  - ⚠ LE SETUP DE BONNIE TOURNE A CHAQUE DEPART : il defausse le deck jusqu'a une amelioration ELEMENT
#    et la met en jeu. Mesure du depart (graine du harnais) : tv014 Turtle Shell est deja EN JEU, main 6,
#    deck 8. Tout cas qui COMPTE des ameliorations ELEMENT doit donc en tenir compte (ou la retirer
#    par `Puzzle.Remove('tv014')`) ;
#  - `main_exclusive` vide la main : chaque cas sait avec QUOI il paie
#    (01088 Energy = YY, 01089 Genius = BB, 01090 Strength = RR, tv008 Evanescence = GGG, jokers) ;
#  - Rhino 01094 est le vilain, 01101 Hydra Mercenary (3 PV, Guard) le sbire de mesure ;
#  - `choisir_option: ["N"]` force la reponse N a `DeclareNumber` (le pilote prend sinon le minimum).
SC = "rhino"
HEROS_ = {"scenario": SC, "heros": "venus"}
HEROS = "Puzzle.ChangeToFace('tv001b', 'tv001a')"
CIVIL = "Puzzle.ChangeToFace('tv001a', 'tv001b')"
SANS_DECK = "Puzzle.EmptyPlayerDeck()"
# Deck rencontre sans boost : les attaques de Rhino n'ont alors AUCUN boost (mesure du degat exact).
SANS_BOOST = ["Puzzle.EmptyEncounterDeck()",
              "Puzzle.CreateEncounterDeck('01105', '01105', '01105', '01105', '01105', '01105', '01105', '01105')"]
COMPLOT = "01097b"
ARMURE = "01036"        # Mark V Armor : amelioration SANS trait ELEMENT (« +6 PV »)


def en_jeu_sous_controle(*ids):
    return [f"Puzzle.PutIntoPlay('{i}', under_control=True)" for i in ids]


def _c(nom, pourquoi, mise, declencher, attendu, **cle):
    if not cle.pop("avec_boost", False):
        mise = SANS_BOOST + list(mise)
    cas = {"nom": "[venus] " + nom, "pourquoi": pourquoi, "scenario": cle.pop("scenario", SC),
           "heros": cle.pop("heros", "venus"), "mise_en_place": mise, "declencher": declencher,
           "verifier": cle.pop("verifier", "venus_etat"), "attendu": attendu}
    cas.update(cle)
    return cas


CAS = [
    # ===================================================================== tv001a Venus (face heros) : Action
    _c("tv001a Venus : l'Action pose 1 dredge par amelioration ELEMENT controlee (3 en jeu -> 3 compteurs)",
       "« Place 1 dredge counter on Venus for each ELEMENT upgrade you control » : tv014 (Setup) + tv009 + tv010 = 3 ELEMENT",
       [HEROS, *en_jeu_sous_controle("tv009", "tv010")], ["Puzzle.Action('tv001a', 'Action')"],
       {"en_jeu": ["tv014", "tv009", "tv010"], "compteurs_identite": [["dredge", 3]]}, main_exclusive=["01090"]),
    _c("tv001a Venus : une amelioration SANS le trait ELEMENT n'est pas comptee (tv009 + Mark V Armor -> 2 : tv014 + tv009)",
       "contre-cas « each ELEMENT upgrade » : l'armure en jeu ne compte pas",
       [HEROS, *en_jeu_sous_controle("tv009", ARMURE)], ["Puzzle.Action('tv001a', 'Action')"],
       {"en_jeu": ["tv014", "tv009", ARMURE], "compteurs_identite": [["dredge", 2]]}, main_exclusive=["01090"]),
    _c("tv001a Venus : zero amelioration ELEMENT -> zero compteur (l'Action se resout quand meme)",
       "Setup retire (tv014 hors jeu) : « for each » vaut 0 ; aucun compteur, pas d'erreur",
       [HEROS, "Puzzle.Remove('tv014')"], ["Puzzle.Action('tv001a', 'Action')"],
       {"hors_jeu": ["tv014"], "compteurs_identite": [["dredge", 0]]}, main_exclusive=["01090"]),
    _c("tv001a Venus : plafond de 6 sur le STOCK (2 deja + 6 ELEMENT en jeu -> 6, pas 8) [TODO-QUESTION Q1]",
       "« (to a maximum of 6) » : lecture retenue = plafond du stock de l'identite (venus-questions.md Q1)",
       [HEROS, "Puzzle.Counter('tv001a', 'dredge', 2)", *en_jeu_sous_controle("tv009", "tv010", "tv011", "tv012", "tv013")],
       ["Puzzle.Action('tv001a', 'Action')"],
       {"compteurs_identite": [["dredge", 6]]}, main_exclusive=["01090"]),
    _c("tv001a Venus : limite 1 par round (TEMOIN D'EPUISEMENT) : 2e Action refusee meme avec un 4e ELEMENT en jeu",
       "« Limit once per round » : 1re Action = 3 compteurs ; un ELEMENT de plus entre en jeu ; la 2e Action doit etre "
       "refusee : 3 compteurs et non 7 (chiffre mesure au second declenchement)",
       [HEROS, *en_jeu_sous_controle("tv009", "tv010")],
       ["Puzzle.Action('tv001a', 'Action')", "Puzzle.PutIntoPlay('tv012', under_control=True)"],
       {"compteurs_identite": [["dredge", 3]]}, main_exclusive=["01090"],
       declencher_tolerant=["Puzzle.Action('tv001a', 'Action')"]),
    _c("tv001a Venus : l'Action est ABSENTE en alter-ego (Bonnie : aucun compteur pose)",
       "contre-cas dans l'AUTRE forme : l'Action « place dredge » est imprimee sur la face heros seulement",
       [*en_jeu_sous_controle("tv009")], [],
       {"compteurs_identite": [["dredge", 0]]}, main_exclusive=["01090"],
       declencher_tolerant=["Puzzle.Action('tv001a', 'Action')"]),
    # ===================================================================== tv001b Bonnie (alter ego) : Setup
    _c("tv001b Bonnie Setup : le depart met un ELEMENT en jeu (tv014, au sommet du deck : rien defausse avant lui)",
       "« Setup: Discard cards from the top of your deck until you discard an ELEMENT upgrade. Put that card into play » : "
       "vraie mise en place (main 6, deck 15 - 6 - 1 = 8)",
       [], [], {"en_jeu": ["tv014"], "taille_deck_joueur": 8, "taille_main": 6, "compteurs_identite": [["dredge", 0]]}, avec_boost=True),
    _c("tv001b Bonnie Setup : les cartes traversees restent en DEFAUSSE, l'ELEMENT trouve entre en jeu (Setup rejoue)",
       "deck force (dessus -> bas) : 01090, 01088, tv010, 01089 ; le Setup defausse 01090, 01088, puis tv010 (ELEMENT) qui "
       "entre en jeu ; 01089 reste dans le deck",
       ["Puzzle.Remove('tv014')", SANS_DECK, "Puzzle.CreatePlayerDeck('01089', 'tv010', '01088', '01090')"], [],
       {"en_jeu": ["tv010"], "defausse_exacte": ["01090", "01088"], "dans_deck_joueur": ["01089"], "taille_deck_joueur": 1},
       verifier="venus_resetup"),
    _c("tv001b Bonnie Setup : aucun ELEMENT dans le deck -> tout le deck est defausse, rien en jeu (Setup rejoue)",
       "« until you discard an ELEMENT upgrade » : sans ELEMENT on ne s'arrete qu'au deck vide ; ni un allie (tv002) ni "
       "une amelioration SANS le trait ELEMENT (Mark V Armor) ne l'arretent : seul le trait compte. Deck epuise : le moteur "
       "remelange la defausse dans le deck (regle du deck epuise) : defausse vide, deck de 4",
       ["Puzzle.Remove('tv014')", SANS_DECK, f"Puzzle.CreatePlayerDeck('01089', 'tv002', '01088', '{ARMURE}')"], [],
       {"hors_jeu": ["tv002", "tv014"], "defausse_exacte": [], "taille_deck_joueur": 4},
       verifier="venus_resetup"),
    _c("tv001b Bonnie Setup : l'ELEMENT est la TOUTE DERNIERE carte du deck -> trouve quand meme (piege DiscardUntil)",
       "01090, 01088 puis tv013 sont defaussees, le deck epuise remelange la defausse (3 cartes) : tv013 est RENDUE quand meme "
       "et entre en jeu ; il reste 2 cartes dans le deck, defausse vide",
       ["Puzzle.Remove('tv014')", SANS_DECK, "Puzzle.CreatePlayerDeck('tv013', '01088', '01090')"], [],
       {"en_jeu": ["tv013"], "defausse_exacte": [], "taille_deck_joueur": 2},
       verifier="venus_resetup"),
    # ===================================================================== tv001b Bonnie : Action
    _c("tv001b Bonnie Action : retire 1 dredge (cout) et soigne 2 degats d'un personnage ami (Bludgeon blesse)",
       "« Remove 1 dredge counter from Bonnie -> heal 2 damage from a friendly character » : 1 compteur sur l'identite ; "
       "Bludgeon (3 PV) a 2 degats ; les 2 sont soignes, le compteur est depense",
       ["Puzzle.PutIntoPlay('tv002')", "Puzzle.Damage('tv002', 2)", "Puzzle.Counter('tv001b', 'dredge', 1)"],
       ["Puzzle.Action('tv001b', 'Action')"],
       {"degats": [["tv002", 0]], "compteurs_identite": [["dredge", 0]]}, main_exclusive=["01090"], cibles=["tv002"]),
    _c("tv001b Bonnie Action : soigne aussi l'IDENTITE elle-meme (4 degats -> 2)",
       "« a friendly character » : l'identite est un personnage ami",
       ["Puzzle.Damage('tv001b', 4)", "Puzzle.Counter('tv001b', 'dredge', 1)"], ["Puzzle.Action('tv001b', 'Action')"],
       {"degats_identite": 2, "compteurs_identite": [["dredge", 0]]}, main_exclusive=["01090"]),
    _c("tv001b Bonnie Action : SANS compteur de dragage, l'Action est refusee (cout impayable, rien n'est soigne)",
       "le retrait de compteur est un COUT : 0 compteur = pas de soin",
       ["Puzzle.Damage('tv001b', 4)"], [],
       {"degats_identite": 4, "compteurs_identite": [["dredge", 0]]}, main_exclusive=["01090"],
       declencher_tolerant=["Puzzle.Action('tv001b', 'Action')"]),
    _c("tv001b Bonnie Action : jamais un SBIRE (Hydra Mercenary blesse, identite saine) : rien n'est soigne, compteur intact",
       "« friendly character » = Friend : un sbire n'est pas ami",
       ["Puzzle.PutIntoPlay('01101')", "Puzzle.Damage('01101', 2)", "Puzzle.Counter('tv001b', 'dredge', 1)"], [],
       {"degats": [["01101", 2]], "compteurs_identite": [["dredge", 1]]}, main_exclusive=["01090"],
       declencher_tolerant=["Puzzle.Action('tv001b', 'Action')"]),
    _c("tv001b Bonnie Action : limite 1 par round (TEMOIN D'EPUISEMENT) : 2 compteurs, 4 degats, la 2e Action est refusee",
       "« Limit once per round » : 1re Action = soigne 2 (4 -> 2), 1 compteur depense ; la 2e est refusee : 2 degats restent, "
       "1 compteur reste (chiffres mesures au second declenchement)",
       ["Puzzle.Damage('tv001b', 4)", "Puzzle.Counter('tv001b', 'dredge', 2)"], ["Puzzle.Action('tv001b', 'Action')"],
       {"degats_identite": 2, "compteurs_identite": [["dredge", 1]]}, main_exclusive=["01090"],
       declencher_tolerant=["Puzzle.Action('tv001b', 'Action')"]),

    # ===================================================================== valeurs imprimees des deux faces
    _c("tv001a Venus : valeurs imprimees PV 10, ATQ 1, CTR 2, DEF 2, main 4 (lues sur le scan)",
       "nombres texte <-> code : HAND SIZE 4 / HIT POINTS 10, THW 2, ATK 1, DEF 2",
       [HEROS], [],
       {"attrs": [["tv001a", "max_health", 10], ["tv001a", "attack", 1], ["tv001a", "thwart", 2],
                  ["tv001a", "defense", 2], ["tv001a", "hand_size", 4]]}, main_exclusive=["01090"]),
    _c("tv001b Bonnie : valeurs imprimees PV 10, REC 4, main 6 (lues sur le scan)",
       "nombres texte <-> code : HAND SIZE 6 / HIT POINTS 10, REC 4",
       [], [],
       {"attrs": [["tv001b", "max_health", 10], ["tv001b", "recover", 4], ["tv001b", "hand_size", 6]]},
       main_exclusive=["01090"]),
    # ===================================================================== tv002 Bludgeon
    _c("tv002 Bludgeon : Response a l'entree : une carte de la defausse va SUR LE DESSUS du deck",
       "« After Bludgeon enters play, put 1 card from your discard pile on top of your deck » : Bludgeon (cout 3) payee "
       "par Evanescence (GGG) ; la defausse contient 01089 (choisie) ; elle doit etre au sommet du deck",
       [SANS_DECK, "Puzzle.CreatePlayerDeck('01090', '01088')", "Puzzle.CreatePlayerDiscardPile('01089')"], [],
       {"en_jeu": ["tv002"], "dessus": "01089", "taille_deck_joueur": 3},
       main_exclusive=["tv002", "tv008"], jouer=["tv002"], cibles=["01089"], accepter_choix=True),
    _c("tv002 Bludgeon : la carte choisie QUITTE la defausse (01089 n'y est plus) et le choix est libre (une carte Hero aussi)",
       "« 1 card from your discard pile » : toute carte, pas seulement une carte specifique : on force tv008 (carte Hero "
       "defaussee par le paiement) au sommet",
       [SANS_DECK, "Puzzle.CreatePlayerDeck('01090', '01088')"], [],
       {"en_jeu": ["tv002"], "dessus": "tv008", "taille_deck_joueur": 3, "hors_defausse": ["tv008"]},
       main_exclusive=["tv002", "tv008"], jouer=["tv002"], cibles=["tv008"], accepter_choix=True),
    _c("tv002 Bludgeon : ATQ 2* / CTR 2* = 1 degat consecutif chacun, 3 PV (cout 3)",
       "« 2* » : desc.ATK/THW lus par can_attack.py -> consequential damage 1 sur les deux pouvoirs",
       ["Puzzle.PutIntoPlay('tv002', under_control=True)"], [],
       {"attrs": [["tv002", "attack", 2], ["tv002", "thwart", 2], ["tv002", "attack_consequential_damage", 1],
                  ["tv002", "thwart_consequential_damage", 1], ["tv002", "max_health", 3]]}, main_exclusive=["01090"]),
    # ===================================================================== tv003 Arc Nova
    _c("tv003 Arc Nova : X = 2 (3 compteurs) -> 4 degats a DEUX ennemis, 2 compteurs retires",
       "« Remove X dredge counters from Venus -> deal 4 damage to X enemies » : X=2 declare ; Rhino (14 PV) et Hydra "
       "Mercenary (3 PV, vaincu) ; il reste 1 compteur",
       [HEROS, "Puzzle.PutIntoPlay('01101')", "Puzzle.Counter('tv001a', 'dredge', 3)"], [],
       {"degats": [["01094", 4]], "hors_jeu": ["01101"], "compteurs_identite": [["dredge", 1]], "defausse": ["tv003"]},
       main_exclusive=["tv003", "01088"], jouer=["tv003"], choisir_option=["2"], cibles=["01094", "01101"]),
    _c("tv003 Arc Nova : X = 1 -> UN seul ennemi frappe (Hydra intact), 1 compteur retire",
       "X est le nombre de compteurs retires ET d'ennemis touches : X=1 sur 3 compteurs",
       [HEROS, "Puzzle.PutIntoPlay('01101')", "Puzzle.Counter('tv001a', 'dredge', 3)"], [],
       {"degats": [["01094", 4], ["01101", 0]], "en_jeu": ["01101"], "compteurs_identite": [["dredge", 2]]},
       main_exclusive=["tv003", "01088"], jouer=["tv003"], choisir_option=["1"], cibles=["01094"]),
    _c("tv003 Arc Nova : X = 3 pour UN seul ennemi en jeu -> 4 degats une fois (pas 12), les 3 compteurs sont perdus",
       "« to X enemies » : un ennemi ne prend pas les degats plusieurs fois ; les compteurs en trop partent quand meme",
       [HEROS, "Puzzle.Counter('tv001a', 'dredge', 3)"], [],
       {"degats": [["01094", 4]], "compteurs_identite": [["dredge", 0]]},
       main_exclusive=["tv003", "01088"], jouer=["tv003"], choisir_option=["3"]),
    _c("tv003 Arc Nova : X = 0 est legal (la carte est jouee, rien n'est retire ni touche)",
       "X choisi par le joueur, zero compris : aucun compteur retire, aucun degat",
       [HEROS, "Puzzle.Counter('tv001a', 'dredge', 3)"], [],
       {"degats": [["01094", 0]], "compteurs_identite": [["dredge", 3]], "defausse": ["tv003"]},
       main_exclusive=["tv003", "01088"], jouer=["tv003"], choisir_option=["0"]),
    _c("tv003 Arc Nova : sans AUCUN compteur, rien ne se passe (la carte est jouee, aucun degat)",
       "0 compteur = X ne peut valoir que 0",
       [HEROS], [],
       {"degats": [["01094", 0]], "compteurs_identite": [["dredge", 0]]},
       main_exclusive=["tv003", "01088"], jouer=["tv003"]),
    _c("tv003 Arc Nova : EVENEMENT Hero Action : injouable en forme alter-ego (Bonnie)",
       "contre-cas dans l'AUTRE forme : « Hero Action » exige la forme heros",
       [], [],
       {"jouable": [["tv003", False]]}, main_exclusive=["tv003", "01088"], verifier="venus_jouable"),
    # ===================================================================== tv004 Brain Burn
    _c("tv004 Brain Burn : retire 2 menaces d'une manigance (principale 5 -> 3)",
       "« Hero Action (thwart): Remove 2 threat from a scheme » : sans choix facultatif accepte",
       [HEROS, f"Puzzle.SetThreat('{COMPLOT}', 5)", "Puzzle.Counter('tv001a', 'dredge', 2)"], [],
       {"menace": [[COMPLOT, 3]], "compteurs_identite": [["dredge", 2]], "statuts_absents": [["01094", "Confused"], ["01094", "Stunned"]]},
       main_exclusive=["tv004", "01090"], jouer=["tv004"], cibles=[COMPLOT], choisir_option=["Cancel"]),
    _c("tv004 Brain Burn : choix accepte : 2 compteurs retires -> l'ennemi est DESORIENTE ET SONNE",
       "« You may remove 2 dredge counters from Venus to confuse AND stun an enemy » : Rhino recoit les deux statuts, "
       "les 2 compteurs partent",
       [HEROS, f"Puzzle.SetThreat('{COMPLOT}', 5)", "Puzzle.Counter('tv001a', 'dredge', 2)"], [],
       {"menace": [[COMPLOT, 3]], "compteurs_identite": [["dredge", 0]],
        "statuts": [["01094", "Confused"], ["01094", "Stunned"]]},
       main_exclusive=["tv004", "01090"], jouer=["tv004"], cibles=[COMPLOT, "01094"], choisir_option=["Remove_2_dredge"]),
    _c("tv004 Brain Burn : un seul compteur : la branche n'est PAS offerte (menace retiree, aucun statut, compteur intact)",
       "le retrait de 2 compteurs est un COUT : 1 compteur ne suffit pas",
       [HEROS, f"Puzzle.SetThreat('{COMPLOT}', 5)", "Puzzle.Counter('tv001a', 'dredge', 1)"], [],
       {"menace": [[COMPLOT, 3]], "compteurs_identite": [["dredge", 1]],
        "statuts_absents": [["01094", "Confused"], ["01094", "Stunned"]]},
       main_exclusive=["tv004", "01090"], jouer=["tv004"], cibles=[COMPLOT]),
    # ===================================================================== tv005 Eldritch Lance
    _c("tv005 Eldritch Lance : 5 degats a un ennemi (Rhino), payee SANS ressource wild (YY + RR) : aucune carte piochee",
       "« Draw 1 card for each [wild] resource used to pay » : 0 wild = 0 carte ; 5 degats a Rhino",
       [HEROS, SANS_DECK, "Puzzle.CreatePlayerDeck('01073', '01073', '01073', '01073', '01073', '01073')"], [],
       {"degats": [["01094", 5]], "taille_main": 0, "taille_deck_joueur": 6},
       main_exclusive=["tv005", "01088", "01090"], jouer=["tv005"], cibles=["01094"]),
    _c("tv005 Eldritch Lance : payee par Evanescence (GGG) + Energy (YY) : 3 jokers = 3 cartes piochees",
       "chiffre mesure : GetPaidResources().g = 3 (les 2 energies ne comptent pas)",
       [HEROS, SANS_DECK, "Puzzle.CreatePlayerDeck('01073', '01073', '01073', '01073', '01073', '01073')"], [],
       {"degats": [["01094", 5]], "taille_main": 3, "taille_deck_joueur": 3},
       main_exclusive=["tv005", "tv008", "01088"], jouer=["tv005"], cibles=["01094"]),
    _c("tv005 Eldritch Lance : Overkill : l'exces d'un sbire vaincu passe au VILAIN (Hydra 3 PV : 5 - 3 = 2 sur Rhino)",
       "« This attack gains overkill » : 2 degats d'exces sur le vilain",
       [HEROS, "Puzzle.PutIntoPlay('01101')"], [],
       {"hors_jeu": ["01101"], "degats": [["01094", 2]]},
       main_exclusive=["tv005", "01088", "01090"], jouer=["tv005"], cibles=["01101"]),
    _c("tv005 Eldritch Lance : EVENEMENT Hero Action : injouable en forme alter-ego (Bonnie)",
       "contre-cas dans l'AUTRE forme", [], [],
       {"jouable": [["tv005", False]]}, main_exclusive=["tv005", "01088", "01090"], verifier="venus_jouable"),
    # ===================================================================== tv006 Quantanucleic Acid
    _c("tv006 Quantanucleic Acid : Venus recoit une carte d'etat TENACE (Tough) ; sans option, rien d'autre",
       "« Give Venus a tough status card » : l'identite (forme heros) devient Tough ; le choix de piocher est refuse",
       [HEROS, SANS_DECK, "Puzzle.CreatePlayerDeck('01073', '01073', '01073')", "Puzzle.Counter('tv001a', 'dredge', 2)"], [],
       {"statuts": [["tv001a", "Tough"]], "compteurs_identite": [["dredge", 2]], "taille_main": 0},
       main_exclusive=["tv006", "01090"], jouer=["tv006"], choisir_option=["Cancel"]),
    _c("tv006 Quantanucleic Acid : choix accepte : 2 compteurs retires -> 2 cartes piochees",
       "« You may remove 2 dredge counters from Venus to draw 2 cards »",
       [HEROS, SANS_DECK, "Puzzle.CreatePlayerDeck('01073', '01073', '01073')", "Puzzle.Counter('tv001a', 'dredge', 2)"], [],
       {"statuts": [["tv001a", "Tough"]], "compteurs_identite": [["dredge", 0]], "taille_main": 2, "taille_deck_joueur": 1},
       main_exclusive=["tv006", "01090"], jouer=["tv006"], choisir_option=["Remove_2_dredge"]),
    _c("tv006 Quantanucleic Acid : un seul compteur : pas de pioche (branche non offerte), l'etat Tough est donne",
       "cout impayable : 1 < 2",
       [HEROS, SANS_DECK, "Puzzle.CreatePlayerDeck('01073', '01073', '01073')", "Puzzle.Counter('tv001a', 'dredge', 1)"], [],
       {"statuts": [["tv001a", "Tough"]], "compteurs_identite": [["dredge", 1]], "taille_main": 0},
       main_exclusive=["tv006", "01090"], jouer=["tv006"]),
    # ===================================================================== tv007 Resistance
    _c("tv007 Resistance : Rhino attaque (ATQ 2 > DEF) : TOUS les degats sont prevenus, la carte est jouee",
       "« prevent all damage from that attack » (heros incline : pas de defense de base)",
       [HEROS, "Puzzle.Exhaust('tv001a')"], ["Puzzle.Attack('01094')"],
       {"degats_identite": 0, "defausse": ["tv007"]},
       main_exclusive=["tv007", "01090"], accepter_choix=True, choisir_option=["Cancel"]),
    _c("tv007 Resistance : choix accepte : 2 compteurs retires -> 3 cartes piochees (apres la prevention)",
       "« You may remove 2 dredge counters from Venus to draw 3 cards » : main 0 -> 3 (le paiement de Resistance vide la main)",
       [HEROS, "Puzzle.Exhaust('tv001a')", SANS_DECK, "Puzzle.CreatePlayerDeck('01073', '01073', '01073', '01073')",
        "Puzzle.Counter('tv001a', 'dredge', 2)"], ["Puzzle.Attack('01094')"],
       {"degats_identite": 0, "compteurs_identite": [["dredge", 0]], "taille_main": 3, "taille_deck_joueur": 1},
       main_exclusive=["tv007", "01090"], accepter_choix=True, choisir_option=["Remove_2_dredge"]),
    _c("tv007 Resistance : sans carte jouee (temoin) : Rhino frappe 2 degats",
       "ligne de base : sans Resistance, Rhino (ATQ 2) inflige 2 degats a un heros incline",
       [HEROS, "Puzzle.Exhaust('tv001a')"], ["Puzzle.Attack('01094')"],
       {"degats_identite": 2}, main_exclusive=["01090"]),
    _c("tv007 Resistance : « from an ATTACK » : des degats HORS attaque (Puzzle.Damage 2) ne sont PAS prevenus",
       "contre-cas : `is_from_attack=True`, la carte n'est pas jouee et les 2 degats passent",
       [HEROS], ["Puzzle.Damage('tv001a', 2)"],
       {"degats_identite": 2, "en_main": ["tv007"]}, main_exclusive=["tv007", "01090"], accepter_choix=True),
    # ===================================================================== tv008 Evanescence
    _c("tv008 Evanescence : RESSOURCE GGG : trois jokers paient SEULS Bludgeon (cout 3)",
       "RES = GGG (trois icones wild imprimees) : une carte de cout 3 est payee par elle seule",
       [], [],
       {"en_jeu": ["tv002"]},
       main_exclusive=["tv002", "tv008"], jouer=["tv002"], payer_avec=["tv008"], cibles=[], accepter_choix=True),

    # ===================================================================== tv009 Arcane Emitting Diode
    _c("tv009 Arcane Emitting Diode : incline + defausse 2 cartes du dessus (cout) -> 2 degats a Rhino",
       "« Exhaust this card and discard the top 2 cards of your deck -> deal 2 damage to an enemy » : deck de 3 -> 1",
       [HEROS, *en_jeu_sous_controle("tv009"), SANS_DECK, "Puzzle.CreatePlayerDeck('01073', '01073', '01073')"],
       ["Puzzle.Action('tv009', 'HeroAction')"],
       {"degats": [["01094", 2]], "exhausted": ["tv009"], "taille_deck_joueur": 1}, main_exclusive=["01090"], cibles=["01094"]),
    _c("tv009 Arcane Emitting Diode : « an enemy » : un SBIRE est une cible legale (Hydra Mercenary 3 PV -> 1)",
       "la cible n'est pas limitee au vilain",
       [HEROS, *en_jeu_sous_controle("tv009"), "Puzzle.PutIntoPlay('01101')", SANS_DECK,
        "Puzzle.CreatePlayerDeck('01073', '01073', '01073')"],
       ["Puzzle.Action('tv009', 'HeroAction')"],
       {"degats": [["01101", 2], ["01094", 0]], "exhausted": ["tv009"]}, main_exclusive=["01090"], cibles=["01101"]),
    _c("tv009 Arcane Emitting Diode : deck VIDE -> le cout (defausser 2 cartes) est impayable : refusee, rien d'incline ni inflige",
       "le deuxieme cout n'est pas payable sans carte a defausser : aucune inclinaison, aucun degat",
       [HEROS, *en_jeu_sous_controle("tv009"), SANS_DECK], [],
       {"degats": [["01094", 0]], "exhausted": []}, main_exclusive=["01090"], cibles=["01094"],
       declencher_tolerant=["Puzzle.Action('tv009', 'HeroAction')"]),
    _c("tv009 Arcane Emitting Diode : inclinee, elle ne sert plus avant d'etre redressee (2e Action refusee : 2 degats et pas 4)",
       "l'inclinaison est un cout : un seul usage tant qu'elle n'est pas redressee",
       [HEROS, *en_jeu_sous_controle("tv009"), SANS_DECK,
        "Puzzle.CreatePlayerDeck('01073', '01073', '01073', '01073', '01073', '01073')"],
       ["Puzzle.Action('tv009', 'HeroAction')"],
       {"degats": [["01094", 2]], "exhausted": ["tv009"], "taille_deck_joueur": 4}, main_exclusive=["01090"], cibles=["01094"],
       declencher_tolerant=["Puzzle.Action('tv009', 'HeroAction')"]),
    _c("tv009 Arcane Emitting Diode : Hero Action : absente en alter-ego (Bonnie : aucun degat)",
       "contre-cas dans l'AUTRE forme", [*en_jeu_sous_controle("tv009"), SANS_DECK,
        "Puzzle.CreatePlayerDeck('01073', '01073', '01073')"], [],
       {"degats": [["01094", 0]], "exhausted": [], "taille_deck_joueur": 3}, main_exclusive=["01090"],
       declencher_tolerant=["Puzzle.Action('tv009', 'HeroAction')"]),
    # ===================================================================== tv010 Cosmic Requiem
    _c("tv010 Cosmic Requiem : incline + 2 compteurs (cout) -> defausse jusqu'a un EVENEMENT et l'ajoute a la main",
       "deck (dessus -> bas) : 01073, 01053 (evenement), 01083 : 01073 est traversee, 01053 va en main, 01083 reste ; "
       "2 compteurs retires, Requiem inclinee",
       [HEROS, "Puzzle.EmptyHand()", *en_jeu_sous_controle("tv010"), "Puzzle.Counter('tv001a', 'dredge', 2)", SANS_DECK,
        "Puzzle.CreatePlayerDeck('01083', '01053', '01073')"],
       ["Puzzle.Action('tv010', 'HeroAction')"],
       {"en_main": ["01053"], "taille_main": 1, "taille_deck_joueur": 1, "dans_deck_joueur": ["01083"],
        "exhausted": ["tv010"], "compteurs_identite": [["dredge", 0]], "defausse": ["01073"]}),
    _c("tv010 Cosmic Requiem : un ALLIE n'arrete pas la fouille (seul un evenement compte) : 01083 traversee, 01053 en main",
       "« until you discard an EVENT » : deck (dessus -> bas) : 01083 (allie), 01053 (evenement), 01073",
       [HEROS, "Puzzle.EmptyHand()", *en_jeu_sous_controle("tv010"), "Puzzle.Counter('tv001a', 'dredge', 2)", SANS_DECK,
        "Puzzle.CreatePlayerDeck('01073', '01053', '01083')"],
       ["Puzzle.Action('tv010', 'HeroAction')"],
       {"en_main": ["01053"], "taille_main": 1, "defausse": ["01083"], "dans_deck_joueur": ["01073"]}),
    _c("tv010 Cosmic Requiem : un seul compteur : refusee (cout impayable), rien d'incline, deck intact",
       "retrait de 2 compteurs = cout", [HEROS, "Puzzle.EmptyHand()", *en_jeu_sous_controle("tv010"), "Puzzle.Counter('tv001a', 'dredge', 1)",
        SANS_DECK, "Puzzle.CreatePlayerDeck('01053', '01073')"], [],
       {"exhausted": [], "taille_deck_joueur": 2, "compteurs_identite": [["dredge", 1]], "taille_main": 0},
       declencher_tolerant=["Puzzle.Action('tv010', 'HeroAction')"]),
    _c("tv010 Cosmic Requiem : AUCUN evenement dans le deck : tout est defausse (puis remelange), rien en main, cout paye",
       "« until you discard an event » sans evenement : deck epuise, moteur : defausse remelangee ; aucune carte en main",
       [HEROS, "Puzzle.EmptyHand()", *en_jeu_sous_controle("tv010"), "Puzzle.Counter('tv001a', 'dredge', 2)", SANS_DECK,
        "Puzzle.CreatePlayerDeck('01083', '01073')"],
       ["Puzzle.Action('tv010', 'HeroAction')"],
       {"taille_main": 0, "exhausted": ["tv010"], "compteurs_identite": [["dredge", 0]]}),
    # ===================================================================== tv011 Dragon Scale
    _c("tv011 Dragon Scale : « Resource » : incline + 1 compteur -> UNE ressource wild paie Brain Burn (cout 1) seule",
       "main = Brain Burn seule ; le seul moyen de payer est Dragon Scale ; incline, 1 compteur retire, carte jouee",
       [HEROS, *en_jeu_sous_controle("tv011"), "Puzzle.Counter('tv001a', 'dredge', 1)", f"Puzzle.SetThreat('{COMPLOT}', 5)"], [],
       {"exhausted": ["tv011"], "compteurs_identite": [["dredge", 0]], "menace": [[COMPLOT, 3]], "defausse": ["tv004"]},
       main_exclusive=["tv004"], jouer=["tv004"], payer_avec=["tv011"], cibles=[COMPLOT]),
    _c("tv011 Dragon Scale : « Resource » (SANS Hero) : payable aussi en forme ALTER-EGO, sur l'identite Bonnie (First Aid)",
       "les compteurs sont sur l'IDENTITE : Bonnie les depense (decision « Raphael en civil »)",
       [*en_jeu_sous_controle("tv011"), "Puzzle.Counter('tv001b', 'dredge', 1)", "Puzzle.Damage('tv001b', 3)"], [],
       {"exhausted": ["tv011"], "compteurs_identite": [["dredge", 0]], "degats_identite": 1, "defausse": ["01086"]},
       main_exclusive=["01086"], jouer=["01086"], payer_avec=["tv011"], cibles=["tv001b"]),
    _c("tv011 Dragon Scale : sans compteur, la ressource n'est pas offerte : Brain Burn (cout 1) n'est PAS jouee, Dragon Scale prete",
       "cout impayable (1 compteur) : la carte reste en main, la manigance garde ses 5 menaces, rien n'est incline",
       [HEROS, *en_jeu_sous_controle("tv011"), f"Puzzle.SetThreat('{COMPLOT}', 5)"], [],
       {"exhausted": [], "menace": [[COMPLOT, 5]], "en_main": ["tv004"]},
       main_exclusive=["tv004"], jouer=["tv004"], payer_avec=["tv011"], cibles=[COMPLOT]),
    # ===================================================================== tv012 Dream Weaver
    _c("tv012 Dream Weaver : defausse jusqu'a un ALLIE ou une AMELIORATION -> l'allie (01083) va en main",
       "deck (dessus -> bas) : 01073, 01083 (allie), 01053 : 01073 traversee, 01083 en main",
       [HEROS, "Puzzle.EmptyHand()", *en_jeu_sous_controle("tv012"), "Puzzle.Counter('tv001a', 'dredge', 2)", SANS_DECK,
        "Puzzle.CreatePlayerDeck('01053', '01083', '01073')"],
       ["Puzzle.Action('tv012', 'HeroAction')"],
       {"en_main": ["01083"], "taille_main": 1, "dans_deck_joueur": ["01053"], "exhausted": ["tv012"],
        "compteurs_identite": [["dredge", 0]], "defausse": ["01073"]}),
    _c("tv012 Dream Weaver : une AMELIORATION arrete aussi la fouille (01036 en main, l'evenement 01053 au-dessus est traverse)",
       "« an ally OR upgrade » : deck (dessus -> bas) : 01053 (evenement : traversee), 01036 (amelioration), 01073",
       [HEROS, "Puzzle.EmptyHand()", *en_jeu_sous_controle("tv012"), "Puzzle.Counter('tv001a', 'dredge', 2)", SANS_DECK,
        "Puzzle.CreatePlayerDeck('01073', '01036', '01053')"],
       ["Puzzle.Action('tv012', 'HeroAction')"],
       {"en_main": ["01036"], "taille_main": 1, "defausse": ["01053"], "dans_deck_joueur": ["01073"]}),
    _c("tv012 Dream Weaver : un seul compteur : refusee (cout impayable), rien d'incline",
       "retrait de 2 compteurs = cout", [HEROS, "Puzzle.EmptyHand()", *en_jeu_sous_controle("tv012"), "Puzzle.Counter('tv001a', 'dredge', 1)",
        SANS_DECK, "Puzzle.CreatePlayerDeck('01083', '01073')"], [],
       {"exhausted": [], "taille_deck_joueur": 2, "taille_main": 0},
       declencher_tolerant=["Puzzle.Action('tv012', 'HeroAction')"]),
    # ===================================================================== tv013 Reanimator Engine
    _c("tv013 Reanimator Engine : incline + 2 compteurs -> 2 cartes choisies de la defausse sont REMELANGEES dans le deck",
       "« choose up to 2 cards in your discard pile and shuffle them into your deck » : defausse 01074, 01075 -> deck 1 + 2 = 3",
       [HEROS, *en_jeu_sous_controle("tv013"), "Puzzle.Counter('tv001a', 'dredge', 2)", SANS_DECK,
        "Puzzle.CreatePlayerDeck('01083')", "Puzzle.CreatePlayerDiscardPile('01074', '01075')"],
       ["Puzzle.Action('tv013', 'HeroAction')"],
       {"taille_deck_joueur": 3, "dans_deck_joueur": ["01074", "01075", "01083"], "exhausted": ["tv013"],
        "compteurs_identite": [["dredge", 0]]}, cibles=["01074", "01075"]),
    _c("tv013 Reanimator Engine : « up to 2 » : UNE seule carte choisie -> une seule remelangee, l'autre reste en defausse",
       "range=(0, 2) : le joueur en choisit 1",
       [HEROS, *en_jeu_sous_controle("tv013"), "Puzzle.Counter('tv001a', 'dredge', 2)", SANS_DECK,
        "Puzzle.CreatePlayerDeck('01083')", "Puzzle.CreatePlayerDiscardPile('01074', '01075')"],
       ["Puzzle.Action('tv013', 'HeroAction')"],
       {"taille_deck_joueur": 2, "dans_deck_joueur": ["01074"], "defausse": ["01075"], "exhausted": ["tv013"]},
       cibles=["01074"]),
    _c("tv013 Reanimator Engine : un seul compteur : refusee (cout impayable)",
       "retrait de 2 compteurs = cout", [HEROS, *en_jeu_sous_controle("tv013"), "Puzzle.Counter('tv001a', 'dredge', 1)",
        SANS_DECK, "Puzzle.CreatePlayerDeck('01083')", "Puzzle.CreatePlayerDiscardPile('01074')"], [],
       {"exhausted": [], "taille_deck_joueur": 1, "defausse": ["01074"]},
       declencher_tolerant=["Puzzle.Action('tv013', 'HeroAction')"]),
    # ===================================================================== tv014 Turtle Shell
    _c("tv014 Turtle Shell : incline + defausse 2 cartes (cout) -> Venus (inclinee) est REDRESSEE",
       "tv014 est deja en jeu (Setup de Bonnie) ; deck de 3 -> 1 ; le heros etait incline",
       [HEROS, "Puzzle.Exhaust('tv001a')", SANS_DECK, "Puzzle.CreatePlayerDeck('01073', '01073', '01073')"],
       ["Puzzle.Action('tv014', 'HeroAction')"],
       {"pret": ["tv001a"], "exhausted": ["tv014"], "taille_deck_joueur": 1}, main_exclusive=["01090"]),
    _c("tv014 Turtle Shell : deck VIDE -> cout impayable : refusee, Venus reste inclinee",
       "la defausse des 2 cartes est un cout",
       [HEROS, "Puzzle.Exhaust('tv001a')", SANS_DECK], [],
       {"exhausted": ["tv001a"]}, main_exclusive=["01090"], declencher_tolerant=["Puzzle.Action('tv014', 'HeroAction')"]),
    # ===================================================================== tv015 Faulty Creation
    _c("tv015 Faulty Creation : donnee a Bonnie en forme heros : le joueur PEUT passer en alter-ego (choix accepte)",
       "« You may flip to alter-ego form » : choix facultatif, accepte -> forme AlterEgo ; l'obligation reste en jeu",
       [HEROS], ["Puzzle.Reveal('tv015')"],
       {"forme": "AlterEgo", "en_jeu": ["tv015"]}, choisir_option=["Flip_to_alter-ego_form"], main_exclusive=["01090"]),
    _c("tv015 Faulty Creation : le choix de passer en alter-ego est REFUSABLE (Cancel) : le heros reste Venus",
       "« MAY flip » (pas « flip ») : contre-cas, refus",
       [HEROS], ["Puzzle.Reveal('tv015')"],
       {"forme": "Hero", "en_jeu": ["tv015"]}, choisir_option=["Cancel"], main_exclusive=["01090"]),
    _c("tv015 Faulty Creation : deja en alter-ego : aucune question, l'obligation entre en jeu",
       "rien a basculer", [], ["Puzzle.Reveal('tv015')"],
       {"forme": "AlterEgo", "en_jeu": ["tv015"]}, main_exclusive=["01090"]),
    _c("tv015 Faulty Creation : Alter-Ego Action : incline Bonnie -> l'obligation est RETIREE DE LA PARTIE",
       "« Exhaust Bonnie -> remove Faulty Creation from the game »",
       [], ["Puzzle.Reveal('tv015')", "Puzzle.Action('tv015', 'AlterEgoAction')"],
       {"hors_jeu": ["tv015"], "exhausted": ["tv001b"]}, main_exclusive=["01090"]),
    _c("tv015 Faulty Creation : l'Alter-Ego Action est ABSENTE en forme heros (l'obligation reste en jeu, rien d'incline)",
       "contre-cas dans l'AUTRE forme",
       [HEROS], ["Puzzle.Reveal('tv015')"],
       {"en_jeu": ["tv015"], "exhausted": []}, main_exclusive=["01090"], choisir_option=["Cancel"],
       declencher_tolerant=["Puzzle.Action('tv015', 'AlterEgoAction')"]),
    _c("tv015 Faulty Creation : icone HAZARD imprimee (carte inclinee + croix) : 1 icone Hazard en jeu une fois revelee",
       "desc.Hazard = 1, lu nativement ; verifiee par decoupe contre 01107 (docs/packs/venus_cartes.md)",
       [], ["Puzzle.Reveal('tv015')"],
       {"icones": [["Hazard", 1]]}, main_exclusive=["01090"]),
    _c("tv015 Faulty Creation : Boost 2 : Rhino (ATQ 2) + 2 icones = 4 degats a Bonnie (alter-ego)",
       "desc.Boost = 2 : l'obligation retournee en boost ajoute 2",
       ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('tv015')"], ["Puzzle.Attack('01094')"],
       {"degats_identite": 4}, main_exclusive=["01090"], avec_boost=True),
    # ===================================================================== tv016 Jasper Barlow's Lab
    _c("tv016 Jasper Barlow's Lab : Hinder 2[par joueur] (menace 2 pour 1 joueur) et Incite 2 (principale 3 -> 5)",
       "complot annexe : StartingThreat 0 + Hinder 2* = 2 sur la carte ; Incite 2 = 2 sur le complot principal",
       [f"Puzzle.SetThreat('{COMPLOT}', 3)"], ["Puzzle.Reveal('tv016')"],
       {"menace": [["tv016", 2], [COMPLOT, 5]], "icones": [["Hazard", 1]]}, main_exclusive=["01090"]),
    _c("tv016 Jasper Barlow's Lab : a DEUX joueurs, Hinder 2* = 4 menaces sur la carte, Incite 2 inchange (principale 3 -> 5)",
       "le « 2* » imprime est PAR joueur",
       [f"Puzzle.SetThreat('{COMPLOT}', 3)"], ["Puzzle.Reveal('tv016')"],
       {"menace": [["tv016", 4], [COMPLOT, 5]]}, main_exclusive=["01090"], heros2="spider_man"),
    _c("tv016 Jasper Barlow's Lab : Boost 2 : Rhino (ATQ 2) + 2 icones = 4 degats a Bonnie",
       "desc.Boost = 2 (deux icones rouges du scan)",
       ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('tv016')"], ["Puzzle.Attack('01094')"],
       {"degats_identite": 4}, main_exclusive=["01090"], avec_boost=True),
    # ===================================================================== tv017 Jasper Barlow
    _c("tv017 Jasper Barlow : valeurs imprimees PV 2, MNG 2, ATQ 0 (lues sur le scan)",
       "nombres texte <-> code : disque orange 2, SCH 2, ATK 0",
       ["Puzzle.PutIntoPlay('tv017')"], [],
       {"attrs": [["tv017", "max_health", 2], ["tv017", "scheme", 2], ["tv017", "attack", 0]]}, main_exclusive=["01090"]),
    _c("tv017 Jasper Barlow : When Revealed : un carte Tough sur CHAQUE sbire engage avec vous (Hydra Mercenary) ET sur lui-meme",
       "« Place a tough status card on each minion engaged with you » : Hydra (engage) et Jasper (engage a la revelation)",
       ["Puzzle.PutIntoPlay('01101')"], ["Puzzle.Reveal('tv017')"],
       {"statuts": [["01101", "Tough"], ["tv017", "Tough"]], "statuts_absents": [["01094", "Tough"]]}, main_exclusive=["01090"]),
    _c("tv017 Jasper Barlow : un sbire engage avec un AUTRE joueur ne recoit RIEN (2 joueurs)",
       "« engaged with YOU » : piege `each` / `with you`",
       ["Puzzle.PutIntoPlay('01101')", "Puzzle.Engage('01101', 1)"], ["Puzzle.Reveal('tv017')"],
       {"statuts": [["tv017", "Tough"]], "statuts_absents": [["01101", "Tough"]]}, main_exclusive=["01090"], heros2="spider_man"),
    _c("tv017 Jasper Barlow : [star] Boost : la carte est donnee au PREMIER joueur face cachee (pas a la defausse), 0 icone : 2 degats",
       "Rhino attaque, la carte de boost est Jasper : « Deal this card to the first player as a facedown encounter card » ; "
       "aucune icone numerique : Rhino frappe son ATQ 2 seule",
       ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('tv017')"], ["Puzzle.Attack('01094')"],
       {"carte": "tv017", "degats_identite": 2}, main_exclusive=["01090"], avec_boost=True, verifier="venus_boost"),
    # ===================================================================== tv018 Groundchuck-Dirtbag
    _c("tv018 Groundchuck-Dirtbag : valeurs imprimees PV 4, MNG 1, ATQ 3 ; Guard et Toughness lus par le moteur (Tough a l'entree)",
       "disque orange 4, SCH 1, ATK 3 ; `desc.Guard`, `desc.Toughness` : aucun module",
       ["Puzzle.PutIntoPlay('tv018')"], [],
       {"carte": "tv018", "guard": True, "toughness": True, "attrs": [["tv018", "max_health", 4], ["tv018", "scheme", 1], ["tv018", "attack", 3]],
        "statuts": [["tv018", "Tough"]]}, main_exclusive=["01090"], verifier="venus_mots_cles"),
    _c("tv018 Groundchuck-Dirtbag : [star] Boost : la carte est donnee au PREMIER joueur face cachee, 0 icone : 2 degats",
       "meme boost que Jasper Barlow (fabrique partagee)",
       ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('tv018')"], ["Puzzle.Attack('01094')"],
       {"carte": "tv018", "degats_identite": 2}, main_exclusive=["01090"], avec_boost=True, verifier="venus_boost"),
    # ===================================================================== tv019 Salvaged Scales
    _c("tv019 Salvaged Scales : 2 menaces sur la principale (3 -> 5) ; SANS Jasper Barlow en jeu, aucun statut Tough",
       "« If Jasper Barlow is in play » : condition de presence, ici fausse : ni le vilain ni le sbire engage ne sont Tough",
       ["Puzzle.PutIntoPlay('01101')", f"Puzzle.SetThreat('{COMPLOT}', 3)"], ["Puzzle.Reveal('tv019')"],
       {"menace": [[COMPLOT, 5]], "statuts_absents": [["01094", "Tough"], ["01101", "Tough"]]}, main_exclusive=["01090"]),
    _c("tv019 Salvaged Scales : AVEC Jasper Barlow en jeu : Tough sur le VILAIN et sur chaque sbire engage avec vous (+2 menaces)",
       "Jasper et Hydra Mercenary engages : trois cartes Tough (Rhino, Hydra, Jasper) ; principale 3 -> 5",
       ["Puzzle.PutIntoPlay('01101')", "Puzzle.PutIntoPlay('tv017')", f"Puzzle.SetThreat('{COMPLOT}', 3)"],
       ["Puzzle.Reveal('tv019')"],
       {"menace": [[COMPLOT, 5]], "statuts": [["01094", "Tough"], ["01101", "Tough"], ["tv017", "Tough"]]}, main_exclusive=["01090"]),
    _c("tv019 Salvaged Scales : Jasper en jeu mais un sbire engage avec un AUTRE joueur : seul le vilain et les sbires engages avec vous",
       "« each minion engaged with YOU » : Hydra engage avec le joueur 2 ne recoit rien ; le vilain si",
       ["Puzzle.PutIntoPlay('01101')", "Puzzle.Engage('01101', 1)", "Puzzle.PutIntoPlay('tv017')"],
       ["Puzzle.Reveal('tv019')"],
       {"statuts": [["01094", "Tough"], ["tv017", "Tough"]], "statuts_absents": [["01101", "Tough"]]}, main_exclusive=["01090"], heros2="spider_man"),
    _c("tv019 Salvaged Scales : Boost 2 : Rhino (ATQ 2) + 2 icones = 4 degats a Bonnie",
       "desc.Boost = 2 (deux icones rouges du scan)",
       ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('tv019')"], ["Puzzle.Attack('01094')"],
       {"degats_identite": 4}, main_exclusive=["01090"], avec_boost=True),
]

VERIFICATIONS = r'''
CLES_VENUS = {'defausse_exacte', 'main_ids', 'dessus', 'attrs', 'hors_defausse', 'defausse_sans'}


def venus_etat(monde, aides):
    """etat_attendu + cles propres au pack : defausse_exacte (ensemble des card_id de la defausse),
    main_ids (ensemble de la main), dessus (card_id du dessus du deck)."""
    cas = aides["cas"]
    attendu = dict(cas.get("attendu") or {})
    propres = {k: attendu.pop(k) for k in list(attendu) if k in CLES_VENUS}
    j = monde.players[0]
    soucis = []
    if "defausse_exacte" in propres:
        vu = sorted(getattr(f.paper, "card_id", "?") for f in j.discard_pile.Get())
        if vu != sorted(propres["defausse_exacte"]):
            soucis.append(f"defausse = {vu} (attendu {sorted(propres['defausse_exacte'])})")
    if "main_ids" in propres:
        vu = sorted(getattr(f.paper, "card_id", "?") for f in j.hand_cards.GetAll())
        if vu != sorted(propres["main_ids"]):
            soucis.append(f"main = {vu} (attendu {sorted(propres['main_ids'])})")
    if "dessus" in propres:
        haut = j.player_deck.GetTop()
        vu = getattr(getattr(haut, "paper", None), "card_id", None)
        if vu != propres["dessus"]:
            soucis.append(f"dessus du deck = {vu} (attendu {propres['dessus']})")
    for cid, attr, voulu in propres.get("attrs") or []:
        face = aides["par_id"](monde, cid)
        if face is None:
            soucis.append(f"{cid} introuvable en jeu (attrs)")
        elif getattr(face, attr) != voulu:
            soucis.append(f"{cid}.{attr} = {getattr(face, attr)} (attendu {voulu})")
    if propres.get("hors_defausse") or propres.get("defausse_sans"):
        pile = [getattr(f.paper, "card_id", "?") for f in j.discard_pile.Get()]
        for cid in (propres.get("hors_defausse") or []) + (propres.get("defausse_sans") or []):
            if cid in pile:
                soucis.append(f"{cid} est dans la defausse (defausse = {pile})")
    sauvegarde = cas["attendu"]
    cas["attendu"] = attendu
    try:
        ok, msg = etat_attendu(monde, aides)
    finally:
        cas["attendu"] = sauvegarde
    if not ok:
        soucis.append(msg)
    if soucis:
        return False, " ; ".join(soucis)
    return True, msg


def venus_resetup(monde, aides):
    """Rejoue le Setup de l'alter-ego (`Setup(False)`, comme `World.Setup`) sur un deck force, puis venus_etat.
    Le cas a retire l'ELEMENT du depart (tv014) et fixe le deck dans `mise_en_place`."""
    if aides["par_id"](monde, "tv014") is not None:
        return False, "tv014 est encore en jeu avant le Setup rejoue (montage du cas)"
    monde.players[0].GetIdentity().Setup(False)
    return venus_etat(monde, aides)


def venus_jouable(monde, aides):
    """`attendu.jouable` = [[card_id, bool]] : la carte EN MAIN est-elle jouable (`CanPlayBy`) ?"""
    soucis = []
    j = monde.players[0]
    for cid, voulu in aides["cas"]["attendu"]["jouable"]:
        main = [f for f in j.hand_cards.GetAll() if getattr(f.paper, "card_id", None) == cid]
        if not main:
            soucis.append(f"{cid} absente de la main")
            continue
        vu = bool(main[0].CanPlayBy(j))
        if vu != voulu:
            soucis.append(f"{cid} jouable={vu} (attendu {voulu})")
    reste = {k: v for k, v in aides["cas"]["attendu"].items() if k != "jouable"}
    if reste:
        cas = aides["cas"]
        sauvegarde = cas["attendu"]
        cas["attendu"] = reste
        try:
            ok, msg = venus_etat(monde, aides)
        finally:
            cas["attendu"] = sauvegarde
        if not ok:
            soucis.append(msg)
    if soucis:
        return False, " ; ".join(soucis)
    return True, "jouabilite conforme"


def venus_boost(monde, aides):
    """`attendu.carte` doit etre parmi les cartes rencontre distribuees (face cachee) du premier joueur, et PAS dans la
    defausse de rencontre ; le reste (degats...) est delegue a venus_etat."""
    from game.operate.worlds import Worlds
    attendu = aides["cas"]["attendu"]
    cid = attendu["carte"]
    premier = monde.GetFirstPlayer()
    distribuees = [getattr(f.paper, "card_id", None) for f in premier.dealt_encounter_cards.GetAll()]
    defausse = [getattr(f.paper, "card_id", None) for f in Worlds.GetEncounterDiscardPileCards(monde)]
    soucis = []
    if cid not in distribuees:
        soucis.append(f"{cid} n'est pas distribuee au premier joueur (distribuees = {distribuees}, defausse = {defausse})")
    if cid in defausse:
        soucis.append(f"{cid} est aussi dans la defausse rencontre")
    reste = {k: v for k, v in attendu.items() if k != "carte"}
    cas = aides["cas"]
    cas["attendu"] = reste
    try:
        ok, msg = venus_etat(monde, aides)
    finally:
        cas["attendu"] = attendu
    if not ok:
        soucis.append(msg)
    if soucis:
        return False, " ; ".join(soucis)
    return True, f"{cid} distribuee au premier joueur, absente de la defausse ; {msg}"


def venus_mots_cles(monde, aides):
    """`attendu.carte` porte (ou non) guard / toughness (IsGuard / IsToughness), puis le reste est delegue a venus_etat."""
    attendu = aides["cas"]["attendu"]
    face = aides["par_id"](monde, attendu["carte"])
    if face is None:
        return False, f"{attendu['carte']} introuvable en jeu"
    soucis = []
    for mot, fn in (("guard", "IsGuard"), ("toughness", "IsToughness")):
        if mot in attendu and bool(getattr(face, fn)()) != attendu[mot]:
            soucis.append(f"{attendu['carte']}.{mot} = {getattr(face, fn)()} (attendu {attendu[mot]})")
    reste = {k: v for k, v in attendu.items() if k not in ("carte", "guard", "toughness")}
    cas = aides["cas"]
    cas["attendu"] = reste
    try:
        ok, msg = venus_etat(monde, aides)
    finally:
        cas["attendu"] = attendu
    if not ok:
        soucis.append(msg)
    if soucis:
        return False, " ; ".join(soucis)
    return True, "mots-cles conformes"
'''
