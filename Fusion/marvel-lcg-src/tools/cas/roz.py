# Cas test_capacites du pack ROZ (jakxin, prefixe `rz`) : noms prefixes « [rz] » puis le card_id
# (substituer_pack.py filtre dessus).
#
# Rappels de montage :
#  - le deck `roz` demarre en ALTER EGO (rz001b Rosalind Solomon) ; `Puzzle.ChangeToFace('rz001b', 'rz001a')` la passe
#    en HEROS SANS declencher de capacite ; `Puzzle.ChangeForm('rz001b')` change de forme en declenchant les reponses ;
#  - Rhino 01094 est le vilain (ATK 2, 14 PV par joueur), 01097b son complot principal (menace 0 au depart),
#    01103 Shocker un sbire (3 PV, ATK 2, boost 2) sans Guard, 01101 Hydra Mercenary un sbire a Guard (3 PV),
#    01184 M.O.D.O.K. un sbire (8 PV, Riposte 2), 01109 Bomb Scare une manigance annexe ;
#  - ressources : 01088 Energy = YY, 01089 Genius = BB, 01090 Strength = RR, 01085 Emergency (evenement Y) = 1 ;
#  - allies : 01083 Mockingbird (S.H.I.E.L.D., sans Special), 01084 Nick Fury, 51024 Okoye (WAKANDA, porte un Special) ;
#  - les Specials se declenchent par `Puzzle.ResolveSpecial` (resout le Special d'une carte en jeu, cibles et couts
#    compris), par la Reponse « Driven » de Roz, par une Reponse donnee aux Thor, ou par un evenement du pack.
SC = "rhino"
HEROS = "Puzzle.ChangeToFace('rz001b', 'rz001a')"
CIVIL = "Puzzle.ChangeToFace('rz001a', 'rz001b')"
VILAIN = "01094"
COMPLOT = "01097b"
SBIRE = "01103"
SBIRE_GUARD = "01101"
SBIRE_RIPOSTE = "01184"
SANS_BOOST = ["Puzzle.EmptyEncounterDeck()",
              "Puzzle.CreateEncounterDeck('01098', '01098', '01098', '01098', '01098', '01098', '01098', '01098')"]
DECK_BOOSTE = ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01103', '01103', '01103', '01103')"]


def en_jeu(*ids):
    return [f"Puzzle.PutIntoPlay('{i}', under_control=True)" for i in ids]


def epuise(*ids):
    return en_jeu(*ids) + [f"Puzzle.Exhaust('{i}')" for i in ids]


def menace(n):
    # Roz n'a aucune capacite qui touche la menace de mise en place : on la pose telle quelle.
    return [f"Puzzle.SetThreat('{COMPLOT}', {n})"]


def _c(nom, pourquoi, mise, declencher, attendu, **cle):
    # ⚠ La main de DEPART (6 cartes, tirage de la graine 42) contient des cartes du pack : une Reponse comme Hand-to-Hand
    # (rz012) se jouait pendant la mise en place des qu'un sbire ou une manigance entrait en jeu, et resolvait des Specials
    # en trop. `main_exclusive` ne vide la main qu'APRES la mise en place : on la vide AVANT (sauf `garder_main`).
    debut = [] if cle.pop("garder_main", False) else ["Puzzle.EmptyHand()"]
    mise = debut + list(cle.pop("sans", SANS_BOOST)) + list(mise)
    cas = {"nom": "[rz] " + nom, "pourquoi": pourquoi, "scenario": cle.pop("scenario", SC),
           "heros": cle.pop("heros", "roz"), "mise_en_place": mise, "declencher": declencher,
           "verifier": cle.pop("verifier", "rz_etat"), "attendu": attendu}
    cas.setdefault("regles", ["v16_all", "v18_all"])
    cas.update(cle)
    return cas


CAS = [
    # ============================================================ rz001a Roz (face heros)
    _c("rz001a Roz : valeurs imprimees PV 9, ATK 1, THW 2, DEF 1, main 5, S.H.I.E.L.D. SPY WAKANDA",
       "nombres texte <-> code (scan) : HAND SIZE 5 / HIT POINTS 9 ; THW 2, ATK 1, DEF 1",
       [HEROS], [], {"pv_max": [["rz001a", 9]], "traits": ["S.H.I.E.L.D", "SPY", "WAKANDA"],
                     "rz_stats": {"attack": 1, "thwart": 2, "defense": 1, "hand_size": 5}},
       main_exclusive=["01090"]),
    _c("rz001a Driven : apres un contre de base, le Special d'une AUTRE carte WAKANDA (Wakandan Jumpsuit) retire 2 menaces",
       "« After you use a basic power, resolve the Special on another WAKANDA card you control » : 5 - 2 (contre de "
       "base THW 2) - 2 (Special de rz005) = 1",
       [HEROS, *menace(5), *en_jeu("rz005")], ["Puzzle.Thwart('rz001a')"],
       {"menace": [[COMPLOT, 1]]}, main_exclusive=["01090"], cibles=[COMPLOT, "rz005", COMPLOT]),
    _c("rz001a Driven : CONTRE-CAS aucune autre carte WAKANDA a Special en jeu -> seul le contre de base retire 2 menaces",
       "Roz ne se resout pas elle-meme (« ANOTHER WAKANDA card ») et Mockingbird (S.H.I.E.L.D., sans WAKANDA) n'est pas propose : "
       "5 - 2 = 3 (vert aussi sans module : contre-cas d'absence assume)",
       [HEROS, *menace(5), *en_jeu("01083")], ["Puzzle.Thwart('rz001a')"],
       {"menace": [[COMPLOT, 3]]}, main_exclusive=["01090"], cibles=[COMPLOT]),
    _c("rz001a Special : redresse un AUTRE personnage ami (Mockingbird epuisee)",
       "« Ready another friendly character »",
       [HEROS, *epuise("01083")], ["Puzzle.ResolveSpecial('rz001a')"],
       {"pret": ["01083"]}, main_exclusive=["01090"], cibles=["01083"]),
    _c("rz001a Special : CONTRE-CAS Roz epuisee, aucun autre personnage -> elle ne se redresse pas elle-meme",
       "« ANOTHER friendly character » : `exclude=\"This\"`",
       [HEROS, "Puzzle.Exhaust('rz001a')"], ["Puzzle.ResolveSpecial('rz001a')"],
       {"exhausted": ["rz001a"]}, main_exclusive=["01090"]),
    _c("rz001a Special : TEMOIN D'EPUISEMENT, deux resolutions dans le meme round -> un seul allie redresse",
       "« (limit once per round) » : 1 allie pret + 1 encore epuise (jamais deux redresses)",
       [HEROS, *epuise("01083", "01084")], ["Puzzle.ResolveSpecial('rz001a')", "Puzzle.ResolveSpecial('rz001a')"],
       {"pret": ["01083"], "exhausted": ["01084"]}, main_exclusive=["01090"], cibles=["01083", "01084"]),

    # ============================================================ rz001b Rosalind Solomon (alter ego)
    _c("rz001b Rosalind Solomon : valeurs imprimees PV 9, REC 3, main 6, S.H.I.E.L.D. SPY WAKANDA",
       "nombres texte <-> code (scan) : HAND SIZE 6 / HIT POINTS 9 / REC 3",
       [], [], {"pv_max": [["rz001b", 9]], "traits": ["S.H.I.E.L.D", "SPY", "WAKANDA"],
                "rz_stats": {"recover": 3, "hand_size": 6}}, main_exclusive=["01090"]),
    _c("rz001b Setup : une amelioration WAKANDA du deck est ajoutee a la main de depart (6 + 1 = 7 cartes)",
       "« Setup: Find a WAKANDA upgrade and add it to your hand. » (le hasard du tirage ne pese pas : on mesure la TAILLE 7)",
       [], [], {"taille_main": 7, "rz_main_au_moins": [["rz004", "rz005", "rz006", "rz007"]]}, garder_main=True),
    _c("rz001b Agent E-23 : apres une recuperation de base, une carte S.H.I.E.L.D. du deck (Mockingbird) passe en main",
       "« After you make a basic recovery, search your deck for a S.H.I.E.L.D. or WAKANDA card » : deck = Genius (non) puis Mockingbird",
       [ "Puzzle.Damage('rz001b', 2)", "Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01089', '01083')"],
       ["Puzzle.Action('rz001b', 'BasicPower')"],
       {"rz_en_main": ["01083"], "rz_pas_en_main": ["01089"], "taille_main": 2},
       main_exclusive=["01090"]),
    _c("rz001b Agent E-23 : une carte WAKANDA (Okoye) convient aussi",
       "« S.H.I.E.L.D. OR WAKANDA card » (OU)",
       ["Puzzle.Damage('rz001b', 2)", "Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01089', '51024')"],
       ["Puzzle.Action('rz001b', 'BasicPower')"],
       {"rz_en_main": ["51024"], "rz_pas_en_main": ["01089"], "taille_main": 2},
       main_exclusive=["01090"]),
    _c("rz001b Agent E-23 : CONTRE-CAS une guerison par une carte (pas une recuperation DE BASE) ne cherche rien",
       "`is_basic_recovery=True` : « basic recovery »",
       ["Puzzle.Damage('rz001b', 2)", "Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01089', '01083')"],
       ["Puzzle.Heal('rz001b', 1)"],
       {"taille_main": 1, "rz_pas_en_main": ["01083"]}, main_exclusive=["01090"]),

    # ============================================================ rz002 Thor (Jane Foster)
    _c("rz002 Thor (Jane Foster) : valeurs imprimees cout 3, 3 PV, ATK 2, THW 2, ASGARD",
       "nombres texte <-> code (scan) : cout 3, HP 3, THW 2*, ATK 2*",
       [HEROS, *en_jeu("rz002")], [], {"rz_carte": [["rz002", {"health": 3, "attack": 2, "thwart": 2}, ["ASGARD"]]]},
       main_exclusive=["01090"]),
    _c("rz002 Thor (Jane Foster) : un Special resolu ce tour -> cout 3 - 1 = 2, payee avec Strength (RR)",
       "« Reduce the cost of this card by 1 for each Special ability resolved this turn » : Roz redresse Mockingbird (1 Special)",
       [HEROS, *epuise("01083")], ["Puzzle.ResolveSpecial('rz001a')"],
       {"en_jeu": ["rz002"]}, main_exclusive=["rz002", "01090"], payer_avec=["01090"], jouer_apres=["rz002"],
       cibles=["01083"]),
    _c("rz002 Thor (Jane Foster) : TEMOIN aucun Special ce tour -> cout 3, injouable avec 2 ressources",
       "sans Special resolu, le cout reste 3 (RR ne suffit pas)",
       [HEROS], [], {}, main_exclusive=["rz002", "01090"], jouer=["rz002"], payer_avec=["01090"],
       verifier="hellcat_carte_restee_en_main", restee="rz002"),
    _c("rz002 Thor (Jane Foster) : DEUX Specials ce tour -> cout 3 - 2 = 1, payee avec UNE ressource (Emergency)",
       "« for each Special ability resolved this turn » : Driven + Jumpsuit = 2 Specials ; la reduction vaut 2 exactement",
       [HEROS, *menace(5), *epuise("01083"), *en_jeu("rz005")],
       ["Puzzle.ResolveSpecial('rz001a')", "Puzzle.ResolveSpecial('rz005')"],
       {"en_jeu": ["rz002"]}, main_exclusive=["rz002", "01085"], payer_avec=["01085"], jouer_apres=["rz002"],
       cibles=["01083", COMPLOT]),
    _c("rz002 Reponse donnee : apres que Thor (Jane Foster) utilise un pouvoir de base, le Special d'une carte WAKANDA est resolu",
       "« Each Thor ally gains Response: After this card uses a basic power, resolve the Special on a WAKANDA card you control »",
       [HEROS, *menace(5), *en_jeu("rz002", "rz005", SBIRE)], ["Puzzle.Attack('rz002')"],
       {"menace": [[COMPLOT, 3]], "degats": [[SBIRE, 2]]}, main_exclusive=["01090"],
       cibles=[SBIRE, "rz005", COMPLOT]),

    _c("rz002 Reponse donnee : « Each Thor ally » inclut le Thor d'un AUTRE joueur (2 joueurs)",
       "CORRECTIF 26/10/2026 (aucun « you control » dans le texte) : Jane Foster (joueur 1) donne sa Reponse a l'Odinson du joueur 2, "
       "qui en porte alors DEUX (la sienne, donnee par lui-meme, et celle de Jane)",
       [HEROS, *en_jeu("rz002"), "Puzzle.PutIntoPlay('rz003', under_control=True, player=1)"], [],
       {"rz_nb_reponses": [["rz003", 2]]}, main_exclusive=["01090"], heros2="spider_man"),

    _c("rz002 Reponse donnee : TEMOIN, les deux Thor du MEME joueur : Odinson porte la Reponse de Jane ET la sienne",
       "ligne de base de `rz_nb_reponses` : meme joueur, aucun doute sur l'octroi (Jane puis Odinson entrent en jeu)",
       [HEROS, *en_jeu("rz002", "rz003")], [], {"rz_nb_reponses": [["rz003", 2]]}, main_exclusive=["01090"]),
    _c("rz002 Reponse donnee : TEMOIN, ordre inverse (Odinson puis Jane en jeu) : chaque Thor porte les DEUX Reponses",
       "meme mesure, l'autre ordre d'arrivee : l'octroi se rafraichit APRES l'entree en jeu d'un autre Thor (`EnterPlayAfter`) et ne passe pas par "
       "un nom (regle des capacites referentielles) ; avant le correctif chaque Thor ne portait que SA Reponse",
       [HEROS, *en_jeu("rz003", "rz002")], [], {"rz_nb_reponses": [["rz002", 2], ["rz003", 2]]}, main_exclusive=["01090"]),

    # ============================================================ rz003 Thor (Odinson)
    _c("rz003 Thor (Odinson) : valeurs imprimees cout 4, 4 PV, ATK 3, THW 1, ASGARD",
       "nombres texte <-> code (scan) : cout 4, HP 4, THW 1*, ATK 3*",
       [HEROS, *en_jeu("rz003")], [], {"rz_carte": [["rz003", {"health": 4, "attack": 3, "thwart": 1}, ["ASGARD"]]]},
       main_exclusive=["01090"]),
    _c("rz003 Thor (Odinson) : un Special resolu ce tour -> cout 4 - 2 = 2, payee avec Strength (RR)",
       "« Reduce the cost to play this card by 2 if you resolved a Special ability this turn »",
       [HEROS, *epuise("01083")], ["Puzzle.ResolveSpecial('rz001a')"],
       {"en_jeu": ["rz003"]}, main_exclusive=["rz003", "01090"], payer_avec=["01090"], jouer_apres=["rz003"],
       cibles=["01083"]),
    _c("rz003 Thor (Odinson) : TEMOIN aucun Special ce tour -> cout 4, injouable avec 2 ressources",
       "sans Special, le cout reste 4",
       [HEROS], [], {}, main_exclusive=["rz003", "01090"], jouer=["rz003"], payer_avec=["01090"],
       verifier="hellcat_carte_restee_en_main", restee="rz003"),
    _c("rz003 Reponse donnee : apres un Special resolu, 1 degat a un ennemi (Thor Odinson en jeu)",
       "« After you resolve a Special ability on a card you control, deal 1 damage to an enemy »",
       [HEROS, *epuise("01083"), *en_jeu("rz003")], ["Puzzle.ResolveSpecial('rz001a')"],
       {"degats": [[VILAIN, 1]]}, main_exclusive=["01090"], cibles=["01083", VILAIN]),
    _c("rz003 Reponse donnee : TEMOIN D'EPUISEMENT, deux Specials dans le meme TOUR -> 1 seul degat (limite)",
       "« (limit once per turn) » : Stealth Tech resout deux Specials (un par resolution : pioche, puis reduction) dans le meme tour, un seul degat",
       [HEROS, *en_jeu("rz003", "rz006")], ["Puzzle.ResolveSpecial('rz006')", "Puzzle.ResolveSpecial('rz006')"],
       {"degats": [[VILAIN, 1]]}, main_exclusive=["01090"], cibles=[VILAIN, VILAIN]),
    _c("rz003 Reponse donnee : un AUTRE tour du meme round -> la limite est levee (2 degats)",
       "CORRECTIF 26/10/2026 : « limit once per TURN » et non « per round » (RR « Limit ») ; premier Special (Roz, Mockingbird redressee) puis, "
       "un nouveau tour (`Puzzle.NewPlayerTurn`), second Special (Stealth Tech) : un degat par tour",
       [HEROS, *epuise("01083"), *en_jeu("rz003", "rz006")],
       ["Puzzle.ResolveSpecial('rz001a')", "Puzzle.NewPlayerTurn()", "Puzzle.ResolveSpecial('rz006')"],
       {"degats": [[VILAIN, 2]]}, main_exclusive=["01090"], cibles=["01083", VILAIN, VILAIN]),

    # ============================================================ rz004 Vibranium Gun
    _c("rz004 Vibranium Gun : Special (attaque) -> 2 degats a un ennemi",
       "« Special (attack): Deal 2 damage to an enemy »",
       [HEROS, *en_jeu("rz004", SBIRE)], ["Puzzle.ResolveSpecial('rz004')"],
       {"degats": [[SBIRE, 2]]}, main_exclusive=["01090"], cibles=[SBIRE]),
    _c("rz004 Vibranium Gun : Special -> perce la carte Tenace de l'ennemi (piercing)",
       "« This attack gains piercing » : Tough defausse ET 2 degats passent",
       [HEROS, *en_jeu("rz004", SBIRE), f"Puzzle.Tough('{SBIRE}')"], ["Puzzle.ResolveSpecial('rz004')"],
       {"degats": [[SBIRE, 2]], "statuts_absents": [[SBIRE, "Tough"]]}, main_exclusive=["01090"], cibles=[SBIRE]),
    _c("rz004 Vibranium Gun : attaque de BASE a distance -> pas de riposte de M.O.D.O.K. ; seule la riposte du Special (2) frappe Roz",
       "« Roz's basic attacks gain ranged » : Driven resout ensuite le Special du pistolet (1 + 2 = 3 degats a M.O.D.O.K.), qui n'est "
       "PAS ranged : Roz ne subit QUE la riposte du Special, 2 (4 si l'attaque de base n'etait pas a distance ; le journal dit « ignore Retaliate »)",
       [HEROS, *en_jeu("rz004", SBIRE_RIPOSTE)], ["Puzzle.Attack('rz001a')"],
       {"degats": [[SBIRE_RIPOSTE, 3]], "degats_identite": 2}, main_exclusive=["01090"],
       cibles=[SBIRE_RIPOSTE]),
    _c("rz004 Vibranium Gun : TEMOIN le Special (attaque) n'est PAS a distance : il contre-attaque... M.O.D.O.K. riposte (2 degats a Roz)",
       "seule l'attaque de BASE gagne ranged ; `ResolveSpecial` direct, cible M.O.D.O.K.",
       [HEROS, *en_jeu("rz004", SBIRE_RIPOSTE)], ["Puzzle.ResolveSpecial('rz004')"],
       {"degats": [[SBIRE_RIPOSTE, 2]], "degats_identite": 2}, main_exclusive=["01090"], cibles=[SBIRE_RIPOSTE]),
    _c("rz004 Vibranium Gun : TEMOIN sans le pistolet, la riposte de M.O.D.O.K. frappe Roz (2 degats) apres l'attaque de base",
       "sans `ranged`, Riposte 2 s'applique : montre que le cas ranged mesure bien la distance",
       [HEROS, *en_jeu(SBIRE_RIPOSTE)], ["Puzzle.Attack('rz001a')"],
       {"degats": [[SBIRE_RIPOSTE, 1]], "degats_identite": 2}, main_exclusive=["01090"], cibles=[SBIRE_RIPOSTE]),
    _c("rz004 Vibranium Gun : valeurs imprimees TECH WEAPON WAKANDA, Restricted 1",
       "scan : « Restricted » (base automatique), cout 2",
       [HEROS, *en_jeu("rz004")], [], {"rz_carte": [["rz004", {}, ["TECH", "WEAPON", "WAKANDA"]]]},
       main_exclusive=["01090"]),

    # ============================================================ rz005 Wakandan Jumpsuit
    _c("rz005 Wakandan Jumpsuit : « You get +3 hit points »",
       "PV max 9 + 3 = 12",
       [HEROS, *en_jeu("rz005")], [], {"pv_max": [["rz001a", 12]]}, main_exclusive=["01090"]),
    _c("rz005 Wakandan Jumpsuit : Special (contre) -> 2 menaces retirees",
       "« Special (thwart): Remove 2 threat from a scheme » : 5 - 2 = 3",
       [HEROS, *menace(5), *en_jeu("rz005")], ["Puzzle.ResolveSpecial('rz005')"],
       {"menace": [[COMPLOT, 3]]}, main_exclusive=["01090"], cibles=[COMPLOT]),
    _c("rz005 Wakandan Jumpsuit : valeurs imprimees ARMOR TECH WAKANDA",
       "scan",
       [HEROS, *en_jeu("rz005")], [], {"rz_carte": [["rz005", {}, ["ARMOR", "TECH", "WAKANDA"]]]},
       main_exclusive=["01090"]),

    # ============================================================ rz006 Wakandan Stealth Tech
    _c("rz006 Wakandan Stealth Tech : « Roz gets +1 DEF »",
       "DEF 1 + 1 = 2",
       [HEROS, *en_jeu("rz006")], [], {"rz_stats": {"defense": 2}}, main_exclusive=["01090"]),
    _c("rz006 Wakandan Stealth Tech : Special -> pioche 1 carte",
       "« Special: Draw 1 card (limit once per round) »",
       [HEROS, *en_jeu("rz006")], ["Puzzle.ResolveSpecial('rz006')"],
       {"taille_main": 2}, main_exclusive=["01090"]),
    _c("rz006 Wakandan Stealth Tech : UNE resolution = UN seul Special (la reduction n'est PAS appliquee quand on pioche)",
       "DECISION UTILISATEUR 26/10/2026 : « resolve the Special » sur une carte a deux Specials = un seul, au choix ; pioche choisie (premiere option), "
       "Haymaker (cout 2) reste donc en main : une seule Emergency ne le paie pas (la carte piochee est une carte de rencontre, sans ressource : "
       "sans elle la pioche aurait fourni la 2e ressource)",
       [HEROS, *en_jeu("rz006", SBIRE), "Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01098')"], ["Puzzle.ResolveSpecial('rz006')"],
       {}, main_exclusive=["01087", "01085"], jouer=["01087"], payer_avec=["01085"],
       verifier="hellcat_carte_restee_en_main", restee="01087", cibles=[SBIRE]),
    _c("rz006 Wakandan Stealth Tech : TEMOIN D'EPUISEMENT, deux resolutions dans le round -> UNE seule pioche",
       "chaque Special est limite a une fois par round ; la 2e resolution fait l'AUTRE Special (reduction), pas une 2e pioche",
       [HEROS, *en_jeu("rz006")], ["Puzzle.ResolveSpecial('rz006')", "Puzzle.ResolveSpecial('rz006')"],
       {"taille_main": 2}, main_exclusive=["01090"]),
    _c("rz006 Wakandan Stealth Tech : Special -> la PROCHAINE carte jouee ce tour coute 1 de moins (Haymaker 2 -> 1, payee avec Emergency)",
       "« Reduce the cost of the next card you play this turn by 1 »",
       [HEROS, *en_jeu("rz006", SBIRE)], ["Puzzle.ResolveSpecial('rz006')", "Puzzle.ResolveSpecial('rz006')"],
       {"hors_jeu": [SBIRE], "rz_pas_en_main": ["01087"]}, main_exclusive=["01087", "01085"],
       payer_avec=["01085"], jouer_apres=["01087"], cibles=[SBIRE]),
    _c("rz006 Wakandan Stealth Tech : TEMOIN sans Special, Haymaker coute 2 -> injouable avec UNE ressource",
       "montre que la reduction vient bien de la carte",
       [HEROS, *en_jeu(SBIRE)], [], {}, main_exclusive=["01087", "01085"], jouer=["01087"], payer_avec=["01085"],
       verifier="hellcat_carte_restee_en_main", restee="01087"),

    # ============================================================ rz007 Agent of Wakanda
    _c("rz007 Agent of Wakanda : « Roz gets +1 THW »",
       "THW 2 + 1 = 3",
       [HEROS, *en_jeu("rz007")], [], {"rz_stats": {"thwart": 3}}, main_exclusive=["01090"]),
    _c("rz007 Agent of Wakanda : Response -> un Special resolu sur une AUTRE carte (Jumpsuit) place 1 compteur agent",
       "« After you resolve a Special ability on another card, place 1 agent counter here »",
       [HEROS, *menace(5), *en_jeu("rz007", "rz005")], ["Puzzle.ResolveSpecial('rz005')"],
       {"compteurs": [["rz007", "agent", 1]]}, main_exclusive=["01090"], cibles=[COMPLOT]),
    _c("rz007 Agent of Wakanda : TEMOIN son propre Special ne place PAS de compteur (« another card »)",
       "6 compteurs depenses -> 0, et pas de compteur de plus",
       [HEROS, *en_jeu("rz007", SBIRE), "Puzzle.Counter('rz007', 'agent', 6)"], ["Puzzle.ResolveSpecial('rz007')"],
       {"compteurs": [["rz007", "agent", 0]], "exhausted": ["rz007"], "statuts": [[SBIRE, "Stunned"]]},
       main_exclusive=["01090"], cibles=[SBIRE], choisir_option=["Stun_an_enemy"]),
    _c("rz007 Agent of Wakanda : Special -> ou DESORIENTE un ennemi (6 compteurs, carte inclinee)",
       "« stun or confuse an enemy » : la 2e branche",
       [HEROS, *en_jeu("rz007", SBIRE), "Puzzle.Counter('rz007', 'agent', 6)"], ["Puzzle.ResolveSpecial('rz007')"],
       {"compteurs": [["rz007", "agent", 0]], "statuts": [[SBIRE, "Confused"]]},
       main_exclusive=["01090"], cibles=[SBIRE], choisir_option=["Confuse_an_enemy"]),
    _c("rz007 Agent of Wakanda : CONTRE-CAS avec 5 compteurs seulement -> le Special n'a pas lieu",
       "« remove 6 agent counters » est un COUT : 5 compteurs ne suffisent pas",
       [HEROS, *en_jeu("rz007", SBIRE), "Puzzle.Counter('rz007', 'agent', 5)"], ["Puzzle.ResolveSpecial('rz007')"],
       {"compteurs": [["rz007", "agent", 5]], "statuts_absents": [[SBIRE, "Stunned"], [SBIRE, "Confused"]]},
       main_exclusive=["01090"], cibles=[SBIRE]),

    # ============================================================ rz008 A.T.M.C.P.
    _c("rz008 A.T.M.C.P. : « You gain the AERIAL trait »",
       "trait continu de l'identite tant que le soutien est en jeu",
       [HEROS, *en_jeu("rz008")], [], {"traits": ["AERIAL"], "rz_carte": [["rz008", {}, ["VEHICLE", "WAKANDA"]]]},
       main_exclusive=["01090"]),
    _c("rz008 A.T.M.C.P. : Special, 1re branche -> Roz epuisee est redressee, le vehicule s'incline",
       "« Exhaust A.T.M.C.P. -> choose 1: Ready your identity »",
       [HEROS, *en_jeu("rz008"), "Puzzle.Exhaust('rz001a')"], ["Puzzle.ResolveSpecial('rz008')"],
       {"pret": ["rz001a"], "exhausted": ["rz008"]}, main_exclusive=["01090"], choisir_option=["Ready_your_identity"]),
    _c("rz008 A.T.M.C.P. : Special, 2e branche -> change de forme (Roz passe en alter ego)",
       "« Change form »",
       [HEROS, *en_jeu("rz008")], ["Puzzle.ResolveSpecial('rz008')"],
       {"forme": "AlterEgo", "exhausted": ["rz008"]}, main_exclusive=["01090"], choisir_option=["Change_form"]),

    # ============================================================ rz009 Trained Shots
    _c("rz009 Trained Shots : 2 degats a un ennemi, puis DEUX fois le Special d'une amelioration WAKANDA (Jumpsuit : -2 menaces chacun)",
       "« Deal 2 damage to an enemy. Resolve the Special on a WAKANDA upgrade. Resolve ... again » : 6 - 2 - 2 = 2",
       [HEROS, *menace(6), *en_jeu("rz005", SBIRE)], [],
       {"degats": [[SBIRE, 2]], "menace": [[COMPLOT, 2]], "defausse": ["rz009"]},
       main_exclusive=["rz009", "01089"], jouer=["rz009"], payer_avec=["01089"],
       cibles=[SBIRE, "rz005", COMPLOT, "rz005", COMPLOT]),
    _c("rz009 Trained Shots : sans amelioration WAKANDA, seuls les 2 degats partent",
       "pas d'amelioration a Special : rien a resoudre",
       [HEROS, *menace(6), *en_jeu(SBIRE)], [],
       {"degats": [[SBIRE, 2]], "menace": [[COMPLOT, 6]]},
       main_exclusive=["rz009", "01089"], jouer=["rz009"], payer_avec=["01089"], cibles=[SBIRE]),

    # ============================================================ rz010 Negotiator
    _c("rz010 Negotiator : retire 2 menaces, puis DEUX fois le Special d'une amelioration WAKANDA (Jumpsuit)",
       "« Remove 2 threat from a scheme. Resolve ... Resolve ... » : 6 - 2 - 2 - 2 = 0 (7 aurait accompli le complot)",
       [HEROS, *menace(6), *en_jeu("rz005")], [],
       {"menace": [[COMPLOT, 0]], "defausse": ["rz010"]},
       main_exclusive=["rz010", "01089"], jouer=["rz010"], payer_avec=["01089"],
       cibles=[COMPLOT, "rz005", COMPLOT, "rz005", COMPLOT]),

    # ============================================================ rz011 Nimble
    _c("rz011 Nimble : 4 degats de Rhino (ATK 2 + boost 2) -> 3 sont prevenus, 1 passe",
       "« When you would take any amount of damage, prevent 3 of that damage »",
       [HEROS, "Puzzle.Exhaust('rz001a')"], ["Puzzle.Attack('01094')"],
       {"degats_identite": 1, "defausse": ["rz011"]}, main_exclusive=["rz011", "01090"],
       sans=DECK_BOOSTE),
    _c("rz011 Nimble : TEMOIN sans Nimble, Rhino frappe pour 4",
       "montre que la baisse vient de la carte",
       [HEROS, "Puzzle.Exhaust('rz001a')"], ["Puzzle.Attack('01094')"],
       {"degats_identite": 4}, main_exclusive=["01090"], sans=DECK_BOOSTE),
    _c("rz011 Nimble : resout ensuite le Special d'une carte WAKANDA (Stealth Tech : pioche 1)",
       "« Resolve the Special ability of a WAKANDA card you control » : main 1 (Strength) puis +1 pioche",
       [HEROS, *en_jeu("rz006"), "Puzzle.Exhaust('rz001a')"], ["Puzzle.Attack('01094')"],
       {"rz_pas_en_main": ["01090"], "taille_main": 1}, main_exclusive=["rz011", "01090"], cibles=["rz006"],
       sans=DECK_BOOSTE),

    # ============================================================ rz012 Hand-to-Hand
    _c("rz012 Hand-to-Hand : un sbire entre en jeu -> Response, Special d'une carte WAKANDA (Jumpsuit : -2 menaces)",
       "« After a minion or side scheme enters play, resolve the Special on 1 WAKANDA card you control » ; cout 0",
       [HEROS, *menace(5), *en_jeu("rz005")], [f"Puzzle.PutIntoPlay('{SBIRE}')"],
       {"menace": [[COMPLOT, 3]], "defausse": ["rz012"]}, main_exclusive=["rz012"], cibles=["rz005", COMPLOT]),
    _c("rz012 Hand-to-Hand : une manigance annexe entre en jeu -> le meme Special",
       "« a minion OR SIDE SCHEME »",
       [HEROS, *menace(5), *en_jeu("rz005")], ["Puzzle.PutIntoPlay('01109')"],
       {"menace": [[COMPLOT, 3]], "defausse": ["rz012"]}, main_exclusive=["rz012"], cibles=["rz005", COMPLOT]),

    # ============================================================ rz013-rz015 ressources
    _c("rz013 Energy : ressource [energy][energy], Max 1 par deck (reskin de 01088)",
       "valeurs imprimees : RES YY, MaxPerDeck 1",
       [], [], {"rz_donnees": [["rz013", {"RES": "YY", "MaxPerDeck": "1", "Class": "Basic"}], ["rz014", {"RES": "BB", "MaxPerDeck": "1", "Class": "Basic"}], ["rz015", {"RES": "RR", "MaxPerDeck": "1", "Class": "Basic"}]]},
       main_exclusive=["01090"]),

    # ============================================================ rz016 Weighed Down
    _c("rz016 Weighed Down : Forced Response, apres un Special resolu sur une carte controlee -> 1 degat a l'identite",
       "« After you resolve the Special on a card you control, take 1 damage »",
       [HEROS, *epuise("01083"), *en_jeu("rz016")], ["Puzzle.ResolveSpecial('rz001a')"],
       {"degats_identite": 1}, main_exclusive=["01090"], cibles=["01083"]),
    _c("rz016 Weighed Down : Alter-Ego Action avec 2 cartes a Special (Jumpsuit, Stealth Tech) -> 2 degats, defaussee",
       "« Take 1 damage for each card you control with a Special ability. 2 or fewer -> discard » (en alter ego, pas de Roz hero)",
       [*en_jeu("rz005", "rz006", "rz016")], ["Puzzle.Action('rz016', 'AlterEgoAction')"],
       {"degats_identite": 2, "defausse_rencontre": ["rz016"]}, main_exclusive=["01090"]),
    _c("rz016 Weighed Down : Alter-Ego Action avec 3 cartes a Special -> 3 degats, RETIREE de la partie",
       "« 3 or more damage -> remove this card from the game »",
       [*en_jeu("rz005", "rz006", "rz004", "rz016")], ["Puzzle.Action('rz016', 'AlterEgoAction')"],
       {"degats_identite": 3, "retirees": ["rz016"]}, main_exclusive=["01090"]),
    _c("rz016 Weighed Down : plafond de 5 degats (6 cartes a Special)",
       "« (to a maximum of 5 damage) » : Jumpsuit, Stealth Tech, Gun, Agent of Wakanda, A.T.M.C.P., Okoye = 6 -> 5 degats",
       [*en_jeu("rz005", "rz006", "rz004", "rz007", "rz008", "51024", "rz016")], ["Puzzle.Action('rz016', 'AlterEgoAction')"],
       {"degats_identite": 5, "retirees": ["rz016"]}, main_exclusive=["01090"]),

    # ============================================================ rz017 Dario Agger
    _c("rz017 Dario Agger : valeurs imprimees PV 3, ATK 1, SCH 3, ROXXON",
       "nombres texte <-> code (scan)",
       [HEROS, *en_jeu("rz017")], [], {"rz_carte": [["rz017", {"health": 3, "attack": 1, "scheme": 3}, ["ROXXON"]]]},
       main_exclusive=["01090"]),
    _c("rz017 Dario Agger : attaque avec une amelioration en main -> elle est defaussee ET Dario (2 degats deja) est vaincu",
       "« must discard an upgrade or support from their hand or play area » : Stealth Tech (main) est defaussee, l'attaque de 1 degat acheve les 3 PV",
       [HEROS, "Puzzle.PutIntoPlay('rz017')", "Puzzle.Damage('rz017', 2)"], ["Puzzle.Attack('rz001a')"],
       {"hors_jeu": ["rz017"], "defausse": ["rz006"]}, main_exclusive=["rz006"], cibles=["rz017", "rz006"]),
    _c("rz017 Dario Agger : aucune amelioration ni soutien a defausser -> il ne peut pas etre vaincu par cette attaque",
       "« If no card is discarded this way, Dario Agger cannot be defeated by this attack » : 3 PV, 2 degats + 1 = 3, il reste en jeu",
       [HEROS, "Puzzle.PutIntoPlay('rz017')", "Puzzle.Damage('rz017', 2)"], ["Puzzle.Attack('rz001a')"],
       {"en_jeu": ["rz017"], "degats": [["rz017", 3]]}, main_exclusive=["01090"], cibles=["rz017"]),
    _c("rz017 Dario Agger : TEMOIN la meme attaque contre un sbire ordinaire (3 PV, 2 degats) le vainc",
       "montre que la survie de Dario vient bien de la carte",
       [HEROS, f"Puzzle.PutIntoPlay('{SBIRE}')", f"Puzzle.Damage('{SBIRE}', 2)"], ["Puzzle.Attack('rz001a')"],
       {"hors_jeu": [SBIRE]}, main_exclusive=["01090"], cibles=[SBIRE]),
    _c("rz017 Dario Agger : un SOUTIEN en jeu peut etre defausse a la place d'une amelioration",
       "« an upgrade OR SUPPORT from their hand OR PLAY AREA » : A.T.M.C.P. en jeu, rien en main",
       [HEROS, *en_jeu("rz008"), "Puzzle.PutIntoPlay('rz017')", "Puzzle.Damage('rz017', 2)"], ["Puzzle.Attack('rz001a')"],
       {"hors_jeu": ["rz017", "rz008"]}, main_exclusive=["01090"], cibles=["rz017", "rz008"]),

    # ============================================================ rz018 Legal Council
    _c("rz018 Legal Council : valeurs imprimees menace 2 par joueur, 1 icone Acceleration, boost 2",
       "scan : « 2 » avec glyphe par joueur, icone d'acceleration (comme 01109), 2 icones de boost",
       [HEROS, "Puzzle.PutIntoPlay('rz018')"], [], {"rz_carte": [["rz018", {}, []]], "menace": [["rz018", 2]]},
       main_exclusive=["01090"]),

    _c("rz018 Legal Council : le Special de Jumpsuit est ANNULE (on refuse de payer) -> la menace ne bouge pas",
       "« spend 1 resource of any type OR cancel its effects » : option « Cancel its effects »",
       [HEROS, *menace(5), *en_jeu("rz005"), "Puzzle.PutIntoPlay('rz018')"], ["Puzzle.ResolveSpecial('rz005')"],
       {"menace": [[COMPLOT, 5]]}, main_exclusive=["01090"], cibles=[COMPLOT], choisir_option=["Cancel_its_effects"]),
    _c("rz018 Legal Council : on PAIE 1 ressource (Strength) -> le Special de Jumpsuit part et la main est vide",
       "« spend 1 resource of any type » : 5 - 2 = 3, la carte de la main est depensee",
       [HEROS, *menace(5), *en_jeu("rz005"), "Puzzle.PutIntoPlay('rz018')"], ["Puzzle.ResolveSpecial('rz005')"],
       {"menace": [[COMPLOT, 3]], "taille_main": 0}, main_exclusive=["01090"], cibles=[COMPLOT],
       choisir_option=["Spend_1_resource_of_any_type"]),
    _c("rz018 Legal Council : TEMOIN sans la manigance, aucun choix : le Special de Jumpsuit part et la main est intacte",
       "montre que la question vient de la carte",
       [HEROS, *menace(5), *en_jeu("rz005")], ["Puzzle.ResolveSpecial('rz005')"],
       {"menace": [[COMPLOT, 3]], "taille_main": 1}, main_exclusive=["01090"], cibles=[COMPLOT]),

    # ============================================================ rz019 Minotaur
    _c("rz019 Minotaur : attache a Dario Agger -> +3 PV, Riposte 1, ATK +3, SCH -2",
       "« Dario Agger gets +3 hit points and gains retaliate 1 » + stats imprimees de l'attachement",
       [HEROS, *en_jeu("rz017"), "Puzzle.PutIntoPlay('rz019')"], [],
       {"rz_carte": [["rz017", {"health": 6, "attack": 4, "scheme": 1, "retaliate": 1}, ["ROXXON"]]]}, main_exclusive=["01090"]),

    # ============================================================ rz020 Lawyers
    _c("rz020 Lawyers : Action, 2 ressources de n'importe quel type (Strength = 2) -> la carte est defaussee",
       "« Action: Spend 2 resources of any type -> discard this card »",
       [HEROS, *en_jeu("rz017"), "Puzzle.PutIntoPlay('rz020')"], ["Puzzle.Action('rz020', 'Action')"],
       {"defausse_rencontre": ["rz020"]}, main_exclusive=["01090"]),
    _c("rz020 Lawyers : TEMOIN une seule ressource (Emergency = 1) ne suffit pas -> la carte reste attachee",
       "deux ressources exigees",
       [HEROS, *en_jeu("rz017"), "Puzzle.PutIntoPlay('rz020')"], [],
       {"rz_carte": [["rz020", {}, ["PERSONA"]]]}, main_exclusive=["01085"]),
    _c("rz020 Lawyers : attache a Dario Agger -> villainous, SCH +1",
       "« Attached character gains villainous »",
       [HEROS, *en_jeu("rz017"), "Puzzle.PutIntoPlay('rz020')"], [],
       {"rz_carte": [["rz017", {"scheme": 4, "villainous": 1}, ["ROXXON"]]]}, main_exclusive=["01090"]),
]


VERIFICATIONS = r'''
def rz_etat(monde, aides):
    """Cles propres : `rz_stats` ({attribut: valeur} lus sur l'identite), `rz_carte` ([[card_id, {attribut: valeur}, [traits]]]
    lus sur la carte EN JEU), `rz_donnees` ([[card_id, {cle desc: valeur}]]), `rz_en_main` / `rz_pas_en_main` ([card_id]),
    `rz_main_au_moins` ([[ids]] : au moins UN de ces ids en main), `rz_degats_min` ([[card_id, n]]), `retirees`
    ([card_id] dans la zone retiree du jeu) ; le reste va a etat_attendu."""
    cas = aides["cas"]
    attendu = cas.get("attendu") or {}
    soucis = []
    identite = aides["identite"](monde)
    for nom, valeur in (attendu.get("rz_stats") or {}).items():
        courant = getattr(identite, nom, None)
        if courant != valeur:
            soucis.append(f"{nom} = {courant} (attendu {valeur})")
    for card_id, attributs, traits in attendu.get("rz_carte") or []:
        face = aides["par_id"](monde, card_id)
        if face is None:
            soucis.append(f"{card_id} introuvable en jeu (rz_carte)")
            continue
        for nom, valeur in attributs.items():
            courant = getattr(face, nom, None)
            if courant != valeur:
                soucis.append(f"{card_id}.{nom} = {courant} (attendu {valeur})")
        for t in traits:
            if not face.HasTrait(t):
                soucis.append(f"{card_id} ne porte pas le trait {t}")
    for card_id, cles in attendu.get("rz_donnees") or []:
        # une ressource n'est jamais en jeu : on cherche la carte physique ou qu'elle soit (deck, main...)
        face = None
        for objet in monde.object_manager.card_dict.values():
            f = objet.face
            if f is not None and getattr(f.paper, "card_id", None) == card_id:
                face = f
                break
        desc = (getattr(face.paper, "desc", None) or {}) if face is not None else None
        if desc is None:
            soucis.append(f"{card_id} introuvable (rz_donnees)")
            continue
        for cle, valeur in cles.items():
            if desc.get(cle) != valeur:
                soucis.append(f"{card_id}.desc[{cle}] = {desc.get(cle)} (attendu {valeur})")
    for card_id, n in attendu.get("rz_nb_reponses") or []:
        # nombre de capacites « Response » ENREGISTREES sur la carte en jeu (dont celles qu'elle a reçues d'un autre Thor)
        from game.ability.ability import AbilityType
        face = aides["par_id"](monde, card_id)
        courant = len(face.effect.Find(type=AbilityType.Response)) if face is not None else None
        if courant != n:
            detail = [getattr(getattr(e.ability, "when", None), "__name__", "?") for e in face.effect.Find(type=AbilityType.Response)] if face is not None else []
            soucis.append(f"{card_id} : {courant} Reponse(s) enregistree(s) (attendu {n}) {detail}")
    main = {getattr(f.paper, "card_id", None) for f in monde.players[0].hand_cards.Get()}
    for card_id in attendu.get("rz_en_main") or []:
        if card_id not in main:
            soucis.append(f"{card_id} absente de la main {sorted(main)}")
    for card_id in attendu.get("rz_pas_en_main") or []:
        if card_id in main:
            soucis.append(f"{card_id} est en main (ne devrait pas)")
    for groupe in attendu.get("rz_main_au_moins") or []:
        if not (main & set(groupe)):
            soucis.append(f"aucune de {groupe} en main {sorted(main)}")
    for card_id, n in attendu.get("rz_degats_min") or []:
        face = aides["par_id"](monde, card_id)
        degats = (face.max_health - face.health) if face is not None else None
        if degats is None or degats < n:
            soucis.append(f"{card_id} : degats = {degats} (au moins {n} attendus)")
    ids_retirees = [getattr(f.paper, "card_id", None) for f in monde.area_removed.Get(True)]
    for card_id in attendu.get("retirees") or []:
        if card_id not in ids_retirees:
            soucis.append(f"{card_id} pas retiree du jeu (retirees = {ids_retirees})")
    cles_propres = ("rz_stats", "rz_carte", "rz_donnees", "rz_en_main", "rz_pas_en_main", "rz_main_au_moins", "rz_degats_min", "retirees", "rz_nb_reponses")
    reste = {k: v for k, v in attendu.items() if k not in cles_propres}
    copie = dict(aides); copie["cas"] = dict(cas); copie["cas"]["attendu"] = reste
    ok, message = etat_attendu(monde, copie)
    if not ok:
        soucis.append(message)
    if soucis:
        return False, " ; ".join(soucis)
    return True, message
'''
