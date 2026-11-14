# Cas test_capacites du heros U.S. AGENT (DesignHacker, « SEALED », prefixe `us`) : noms prefixes « [us] » puis le card_id
# (substituer_pack.py filtre dessus). Un cas par capacite, sujet = le card_id dans le nom.
#
# Rappels de montage :
#  - le deck us_agent demarre en ALTER EGO (us001b John Walker) ; `Puzzle.ChangeToFace('us001b', 'us001a')` le passe en
#    forme HEROS SANS declencher de Reponse ; `Puzzle.ChangeToFace('us001a', 'us001b')` revient en alter ego ;
#  - Rhino 01094 est le vilain, 01097b son complot principal (menace 0 au depart), 01101 Hydra Mercenary (3 PV, Guard),
#    01103 Shocker (3 PV), 01121 Weapons Runner (2 PV, ATQ 1), 01182 Hydra Soldier (4 PV, Guard), 01184 M.O.D.O.K. (8 PV,
#    Retaliate 2) ; 01098 sert de boost neutre (aucune icone) ;
#  - ressources : 01088 Energy = YY, 01089 Genius = BB, 01090 Strength = RR (cartes Basic) ; 01020 Hellcat (RES G) ne
#    rapporte qu'UNE ressource [wild] ;
#  - `main_exclusive` donne la main EXACTE apres la mise en place ; le deck de 15 cartes signature et la decklist d'aspect
#    de l'auteur sont donc ecartes des mesures.
SC = "rhino"
HEROS = "Puzzle.ChangeToFace('us001b', 'us001a')"
CIVIL = "Puzzle.ChangeToFace('us001a', 'us001b')"
SANS_BOOST = ["Puzzle.EmptyEncounterDeck()",
              "Puzzle.CreateEncounterDeck('01098', '01098', '01098', '01098', '01098', '01098', '01098', '01098')"]
COMPLOT = "01097b"
VILAIN = "01094"
BOUCLIER = "us011"


def en_jeu(*ids):
    return [f"Puzzle.PutIntoPlay('{i}', under_control=True)" for i in ids]


def _c(nom, pourquoi, mise, declencher, attendu, **cle):
    mise = SANS_BOOST + list(mise)
    cas = {"nom": "[us] " + nom, "pourquoi": pourquoi, "scenario": cle.pop("scenario", SC),
           "heros": cle.pop("heros", "us_agent"), "mise_en_place": mise, "declencher": declencher,
           "verifier": cle.pop("verifier", "us_etat"), "attendu": attendu}
    cas.setdefault("regles", ["v16_all", "v18_all"])
    cas.update(cle)
    return cas


CAS = [
    # ============================================================ us001a U.S. Agent : valeurs imprimees
    _c("us001a U.S. Agent : valeurs imprimees PV 11, THW 2, ATK 2, DEF 2, main 6, AVENGER SOLDIER",
       "nombres texte <-> code (scan) : HAND SIZE 6 / HIT POINTS 11 ; THW 2 ATK 2 DEF 2",
       [HEROS], [], {"pv_max": [["us001a", 11]], "traits": ["AVENGER", "SOLDIER"],
                     "us_stats": {"attack": 2, "thwart": 2, "defense": 2, "hand_size": 6}},
       main_exclusive=["01090"]),
    # ============================================================ us001a Bolster
    _c("us001a Bolster : apres sa DEFENSE, une amelioration INCLINEE est redressee",
       "« Response: After you defend, ready an upgrade you control » : le bouclier est incline, le heros defend contre Rhino "
       "(DEF 2 contre ATQ 2 : aucun degat), le bouclier se redresse",
       [HEROS] + en_jeu(BOUCLIER) + ["Puzzle.Exhaust('us011')"], ["Puzzle.Defend('us001a', '01094')"],
       {"pret": [BOUCLIER], "degats_identite": 0}, main_exclusive=["01090"], accepter_choix=True),
    _c("us001a Bolster : TEMOIN, une ATTAQUE de base (pas une defense) ne redresse rien",
       "« After you DEFEND » : le heros attaque Rhino, le bouclier incline reste incline",
       [HEROS] + en_jeu(BOUCLIER) + ["Puzzle.Exhaust('us011')"], ["Puzzle.Attack('us001a')"],
       {"exhausted": [BOUCLIER]}, main_exclusive=["01090"], accepter_choix=True, cibles=[VILAIN]),
    # ============================================================ us001b John Walker
    _c("us001b John Walker : valeurs imprimees PV 11, REC 3, main 6, SOLDIER",
       "nombres texte <-> code (scan) : HAND SIZE 6 / HIT POINTS 11 / REC 3",
       [], [], {"pv_max": [["us001b", 11]], "traits": ["SOLDIER"], "us_stats": {"recover": 3, "hand_size": 6}},
       main_exclusive=["01090"]),
    _c("us001b John Walker : Action -> le bouclier est cherche dans le DECK et ajoute a la main, John Walker s'incline",
       "« Action: Exhaust John Walker -> search your deck and discard pile for the U.S. Agent's Shield upgrade and add it to your hand »",
       ["Puzzle.EmptyHand()", "Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01090', 'us011', '01089')"], ["Puzzle.Action('us001b', 'Action')"],
       {"en_main": [BOUCLIER], "exhausted": ["us001b"], "taille_main": 1}),
    _c("us001b John Walker : Action -> le bouclier est cherche dans la DEFAUSSE",
       "« search your deck AND DISCARD PILE » : bouclier en defausse, deck sans bouclier",
       ["Puzzle.EmptyHand()", "Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01090', '01089')", "Puzzle.CreatePlayerDiscardPile('us011')"],
       ["Puzzle.Action('us001b', 'Action')"],
       {"en_main": [BOUCLIER], "exhausted": ["us001b"], "taille_main": 1}),
    _c("us001b John Walker : Action SANS bouclier ni en deck ni en defausse -> rien en main, mais John Walker est incline (cout paye)",
       "la recherche ne trouve rien ; l'inclinaison est un COUT, payee avant",
       ["Puzzle.EmptyHand()", "Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01090', '01089')"], ["Puzzle.Action('us001b', 'Action')"],
       {"taille_main": 0, "exhausted": ["us001b"]}),

    # ============================================================ us002 Bouncing Bulwark
    _c("us002 Bouncing Bulwark : 4 degats a Rhino, le bouclier part en DEFAUSSE (pas d'exces)",
       "« Discard U.S. Agent's Shield -> deal 4 damage to an enemy » ; Rhino (14 PV) ne meurt pas : aucun exces, le bouclier reste en defausse",
       [HEROS] + en_jeu(BOUCLIER), [],
       {"degats": [[VILAIN, 4]], "hors_jeu": [BOUCLIER], "defausse": ["us002", BOUCLIER]},
       main_exclusive=["us002"], jouer=["us002"], cibles=[VILAIN], accepter_choix=True),
    _c("us002 Bouncing Bulwark : EXCES de 2 exactement (Weapons Runner 2 PV) -> le bouclier REVIENT en jeu depuis la defausse",
       "« if this attack deals 2 or more excess damage, put U.S. Agent's Shield into play from your discard pile » : 4 - 2 = 2",
       [HEROS, "Puzzle.PutIntoPlay('01121')"] + en_jeu(BOUCLIER), [],
       {"hors_jeu": ["01121"], "en_jeu": [BOUCLIER], "defausse": ["us002"]},
       main_exclusive=["us002"], jouer=["us002"], cibles=["01121"], accepter_choix=True),
    _c("us002 Bouncing Bulwark : EXCES de 3 (sbire a 1 PV restant) -> le bouclier revient aussi",
       "« 2 OR MORE » : 4 - 1 = 3",
       [HEROS, "Puzzle.PutIntoPlay('01121')", "Puzzle.Damage('01121', 1)"] + en_jeu(BOUCLIER), [],
       {"hors_jeu": ["01121"], "en_jeu": [BOUCLIER], "defausse": ["us002"]},
       main_exclusive=["us002"], jouer=["us002"], cibles=["01121"], accepter_choix=True),
    _c("us002 Bouncing Bulwark : EXCES de 1 seulement (Shocker 3 PV) -> le bouclier RESTE en defausse",
       "4 - 3 = 1 : sous le seuil de 2, il ne revient pas",
       [HEROS, "Puzzle.PutIntoPlay('01103')"] + en_jeu(BOUCLIER), [],
       {"hors_jeu": ["01103", BOUCLIER], "defausse": ["us002", BOUCLIER]},
       main_exclusive=["us002"], jouer=["us002"], cibles=["01103"], accepter_choix=True),
    _c("us002 Bouncing Bulwark : sans le bouclier EN JEU la carte est injouable (le cout est de le defausser)",
       "« Discard U.S. Agent's Shield -> » est un COUT : la carte reste en main",
       [HEROS], [], {}, main_exclusive=["us002"], jouer=["us002"], accepter_choix=True,
       verifier="hellcat_carte_restee_en_main", restee="us002"),

    # ============================================================ us003 Deflection
    _c("us003 Deflection : TEMOIN (ligne de base) : Rhino frappe le heros incline, bouclier incline en jeu, SANS la carte en main",
       "mesure les degats de l'attaque de Rhino dans ce montage",
       [HEROS, "Puzzle.Exhaust('us001a')", "Puzzle.PutIntoPlay('01121')", "Puzzle.PutIntoPlay('01103')"]
       + en_jeu(BOUCLIER) + ["Puzzle.Exhaust('us011')"], [f"Puzzle.Attack('{VILAIN}')"],
       {"degats_identite": 2}, main_exclusive=["01090"]),
    _c("us003 Deflection : 2 degats subis d'un ENNEMI, bouclier en jeu -> 2 sbires sur 3 sont ETOURDIS (le vilain et le 3e non)",
       "« After an enemy deals 2 or more damage to you, if U.S. Agent's Shield is in play, stun up to 2 minions » ; Strength (RR) paie le cout 1",
       [HEROS, "Puzzle.Exhaust('us001a')", "Puzzle.PutIntoPlay('01121')", "Puzzle.PutIntoPlay('01103')", "Puzzle.PutIntoPlay('01182')"]
       + en_jeu(BOUCLIER) + ["Puzzle.Exhaust('us011')"], [f"Puzzle.Attack('{VILAIN}')"],
       {"degats_identite": 2, "statuts": [["01121", "Stunned"], ["01103", "Stunned"]],
        "statuts_absents": [["01182", "Stunned"], [VILAIN, "Stunned"]], "defausse": ["us003", "01090"]},
       main_exclusive=["us003", "01090"], payer_avec=["01090"], cibles=["01121", "01103"], accepter_choix=True),
    _c("us003 Deflection : « up to 2 » avec UN seul sbire en jeu -> il est etourdi",
       "cibles facultatives (0 a 2) : un seul sbire disponible",
       [HEROS, "Puzzle.Exhaust('us001a')", "Puzzle.PutIntoPlay('01103')"] + en_jeu(BOUCLIER) + ["Puzzle.Exhaust('us011')"],
       [f"Puzzle.Attack('{VILAIN}')"],
       {"statuts": [["01103", "Stunned"]], "defausse": ["us003", "01090"]},
       main_exclusive=["us003", "01090"], payer_avec=["01090"], cibles=["01103"], accepter_choix=True),
    _c("us003 Deflection : TEMOIN, SANS le bouclier en jeu la carte n'est pas proposee (elle reste en main)",
       "« if U.S. Agent's Shield is in play » : aucun bouclier, aucun sbire etourdi",
       [HEROS, "Puzzle.Exhaust('us001a')", "Puzzle.PutIntoPlay('01103')"], [f"Puzzle.Attack('{VILAIN}')"],
       {"degats_identite": 2, "statuts_absents": [["01103", "Stunned"]], "en_main": ["us003"]},
       main_exclusive=["us003", "01090"], payer_avec=["01090"], cibles=["01103"], accepter_choix=True),
    _c("us003 Deflection : TEMOIN, 1 SEUL degat subi (Weapons Runner ATQ 1) -> pas de Reponse",
       "« 2 OR MORE damage » : 1 degat ne declenche rien",
       [HEROS, "Puzzle.Exhaust('us001a')", "Puzzle.PutIntoPlay('01121')", "Puzzle.PutIntoPlay('01103')"]
       + en_jeu(BOUCLIER) + ["Puzzle.Exhaust('us011')"], ["Puzzle.Attack('01121')"],
       {"degats_identite": 1, "statuts_absents": [["01103", "Stunned"], ["01121", "Stunned"]], "en_main": ["us003"]},
       main_exclusive=["us003", "01090"], payer_avec=["01090"], cibles=["01103"], accepter_choix=True),
    _c("us003 Deflection : TEMOIN, 3 degats qui ne viennent PAS d'un ennemi (degats directs) -> pas de Reponse",
       "« After an ENEMY deals... » : un effet sans source ennemie ne declenche pas",
       [HEROS, "Puzzle.PutIntoPlay('01103')"] + en_jeu(BOUCLIER) + ["Puzzle.Exhaust('us011')"], ["Puzzle.Damage('us001a', 3)"],
       {"degats_identite": 3, "statuts_absents": [["01103", "Stunned"]], "en_main": ["us003"]},
       main_exclusive=["us003", "01090"], payer_avec=["01090"], cibles=["01103"], accepter_choix=True),

    # ============================================================ us004 Reckless
    _c("us004 Reckless : X = 3 -> le heros subit 3, -3 menace sur la principale (5 -> 2), 3 degats a Rhino",
       "« Take X damage -> remove X threat from a scheme and deal X damage to an enemy » : le joueur declare 3 (modele Majime)",
       [HEROS, f"Puzzle.SetThreat('{COMPLOT}', 5)"], [],
       {"degats_identite": 3, "menace": [[COMPLOT, 2]], "degats": [[VILAIN, 3]], "defausse": ["us004"]},
       main_exclusive=["us004"], jouer=["us004"], choisir_option=["3"], cibles=[COMPLOT, VILAIN]),
    _c("us004 Reckless : X = 4 (le MAXIMUM) -> 4 degats au heros, 6 -> 2 de menace, 4 degats a Rhino",
       "« to a maximum of 4 » : la valeur la plus haute declarable",
       [HEROS, f"Puzzle.SetThreat('{COMPLOT}', 6)"], [],
       {"degats_identite": 4, "menace": [[COMPLOT, 2]], "degats": [[VILAIN, 4]]},
       main_exclusive=["us004"], jouer=["us004"], choisir_option=["4"], cibles=[COMPLOT, VILAIN]),
    _c("us004 Reckless : X = 0 -> rien ne se passe",
       "declare 0 : aucun degat subi, aucune menace retiree, Rhino indemne",
       [HEROS, f"Puzzle.SetThreat('{COMPLOT}', 5)"], [],
       {"degats_identite": 0, "menace": [[COMPLOT, 5]], "degats": [[VILAIN, 0]]},
       main_exclusive=["us004"], jouer=["us004"], choisir_option=["0"], cibles=[COMPLOT, VILAIN]),
    _c("us004 Reckless : heros ROBUSTE, X declare 3 -> la robustesse absorbe tout, X reel = 0 (decision Majime du 15/10/2026)",
       "X = les degats REELLEMENT subis : Tough prevenant tout, aucun effet",
       [HEROS, "Puzzle.Tough('us001a')", f"Puzzle.SetThreat('{COMPLOT}', 5)"], [],
       {"degats_identite": 0, "menace": [[COMPLOT, 5]], "degats": [[VILAIN, 0]], "statuts_absents": [["us001a", "Tough"]]},
       main_exclusive=["us004"], jouer=["us004"], choisir_option=["3"], cibles=[COMPLOT, VILAIN]),
    _c("us004 Reckless : X = 3 mais 1 degat PREVENU (Jessica's Jacket) -> cout NON paye, aucun effet (RR Cost, arbitrage 26/10/2026)",
       "RR Cost : « If taking damage is a cost, that cost is not considered paid unless all of that damage was taken » : "
       "le heros subit 2 sur 3, la menace et les degats a Rhino ne partent PAS (la Veste retire 1 menace de la principale : 5 -> 4)",
       [HEROS, f"Puzzle.SetThreat('{COMPLOT}', 5)"] + en_jeu("jj010"), [],
       {"degats_identite": 2, "menace": [[COMPLOT, 4]], "degats": [[VILAIN, 0]], "exhausted": ["jj010"]},
       main_exclusive=["us004"], jouer=["us004"], choisir_option=["3"], cibles=[COMPLOT, VILAIN], accepter_choix=True),
    _c("us004 Reckless : libelles ATTACK, TACTIC, THWART lus EN MAIN (un evenement n'est jamais en jeu)",
       "trait (attack/thwart) du scan : ATTACK. TACTIC. THWART.",
       [HEROS], [], {"us_traits_main": [["us004", ["ATTACK", "TACTIC", "THWART"]]]}, main_exclusive=["us004"]),
    # ============================================================ us005 Roundhouse
    _c("us005 Roundhouse : payee avec une carte PROTECTION (Armored Vest) -> 2 degats ET Rhino DESORIENTE",
       "« If you paid for this card using a Protection (green) or Justice (yellow) card, confuse that enemy »",
       [HEROS], [],
       {"degats": [[VILAIN, 2]], "statuts": [[VILAIN, "Confused"]], "defausse": ["us005", "01081"]},
       main_exclusive=["us005", "01081"], jouer=["us005"], payer_avec=["01081"], cibles=[VILAIN], accepter_choix=True),
    _c("us005 Roundhouse : payee avec une carte JUSTICE (For Justice!) -> Rhino DESORIENTE",
       "l'autre classe du « or »",
       [HEROS], [],
       {"degats": [[VILAIN, 2]], "statuts": [[VILAIN, "Confused"]], "defausse": ["us005", "01060"]},
       main_exclusive=["us005", "01060"], jouer=["us005"], payer_avec=["01060"], cibles=[VILAIN], accepter_choix=True),
    _c("us005 Roundhouse : TEMOIN, payee avec une carte AGGRESSION (Chase Them Down) -> 2 degats, PAS de desorientation",
       "la classe de la carte payeuse compte, pas la couleur de sa ressource",
       [HEROS], [],
       {"degats": [[VILAIN, 2]], "statuts_absents": [[VILAIN, "Confused"]], "defausse": ["us005", "01052"]},
       main_exclusive=["us005", "01052"], jouer=["us005"], payer_avec=["01052"], cibles=[VILAIN], accepter_choix=True),
    _c("us005 Roundhouse : TEMOIN, payee avec une carte LEADERSHIP (Make the Call) -> pas de desorientation",
       "Leadership n'est ni Protection ni Justice",
       [HEROS], [],
       {"degats": [[VILAIN, 2]], "statuts_absents": [[VILAIN, "Confused"]], "defausse": ["us005", "01071"]},
       main_exclusive=["us005", "01071"], jouer=["us005"], payer_avec=["01071"], cibles=[VILAIN], accepter_choix=True),
    _c("us005 Roundhouse : TEMOIN, payee avec une carte BASIC (First Aid) -> pas de desorientation",
       "Basic n'est ni Protection ni Justice",
       [HEROS], [],
       {"degats": [[VILAIN, 2]], "statuts_absents": [[VILAIN, "Confused"]], "defausse": ["us005", "01086"]},
       main_exclusive=["us005", "01086"], jouer=["us005"], payer_avec=["01086"], cibles=[VILAIN], accepter_choix=True),
    _c("us005 Roundhouse : TEMOIN, payee avec Strength (Basic, 2 ressources) -> pas de desorientation",
       "payer avec une carte Basic a deux ressources ne change rien",
       [HEROS], [],
       {"degats": [[VILAIN, 2]], "statuts_absents": [[VILAIN, "Confused"]], "defausse": ["us005", "01090"]},
       main_exclusive=["us005", "01090"], jouer=["us005"], payer_avec=["01090"], cibles=[VILAIN], accepter_choix=True),
    _c("us005 Roundhouse : TEMOIN, payee avec une carte HERO (Hellcat) -> pas de desorientation",
       "une carte signature d'un autre heros n'est ni Protection ni Justice",
       [HEROS], [],
       {"degats": [[VILAIN, 2]], "statuts_absents": [[VILAIN, "Confused"]], "defausse": ["us005", "01020"]},
       main_exclusive=["us005", "01020"], jouer=["us005"], payer_avec=["01020"], cibles=[VILAIN], accepter_choix=True),
    _c("us005 Roundhouse : payee Protection, cible = un SBIRE a 3 PV -> 2 degats et le sbire est DESORIENTE (la meme cible)",
       "« that enemy » : la cible des degats, vivante (3 PV - 2 = 1)",
       [HEROS, "Puzzle.PutIntoPlay('01103')"], [],
       {"degats": [["01103", 2]], "statuts": [["01103", "Confused"]], "defausse": ["us005", "01081"]},
       main_exclusive=["us005", "01081"], jouer=["us005"], payer_avec=["01081"], cibles=["01103"], accepter_choix=True),
    _c("us005 Roundhouse : payee Protection, cible VAINCUE (Weapons Runner 2 PV) -> aucune erreur, le sbire part",
       "« confuse that enemy » sur un ennemi mort : rien a desorienter, pas d'exception avalee",
       [HEROS, "Puzzle.PutIntoPlay('01121')"], [],
       {"hors_jeu": ["01121"], "defausse": ["us005", "01081"]},
       main_exclusive=["us005", "01081"], jouer=["us005"], payer_avec=["01081"], cibles=["01121"], accepter_choix=True),

    # ============================================================ us006 Walker's Chopper
    _c("us006 Walker's Chopper : apres la RECUPERATION de base de John Walker -> forme HEROS, U.S. Agent PRET, le soutien s'incline",
       "« After you exhaust John Walker to recover... exhaust Walker's Chopper -> change to hero form, then ready U.S. Agent »",
       ["Puzzle.Damage('us001b', 3)"] + en_jeu("us006"), ["Puzzle.Action('us001b', 'BasicPower')"],
       {"forme": "Hero", "pret": ["us001a"], "exhausted": ["us006"]}, main_exclusive=["01090"], accepter_choix=True),
    _c("us006 Walker's Chopper : apres la RECHERCHE du bouclier (Action de John Walker) -> forme HEROS, U.S. Agent PRET",
       "« ...or search for U.S. Agent's Shield » : le bouclier est aussi ajoute a la main",
       ["Puzzle.EmptyHand()", "Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01090', 'us011', '01089')"] + en_jeu("us006"),
       ["Puzzle.Action('us001b', 'Action')"],
       {"forme": "Hero", "pret": ["us001a"], "exhausted": ["us006"], "en_main": [BOUCLIER]}, accepter_choix=True),
    _c("us006 Walker's Chopper : TEMOIN, le soutien est deja INCLINE -> la recuperation ne change pas de forme",
       "« exhaust Walker's Chopper -> » est un cout : incline, la Reponse n'est pas offerte",
       ["Puzzle.Damage('us001b', 3)"] + en_jeu("us006") + ["Puzzle.Exhaust('us006')"], ["Puzzle.Action('us001b', 'BasicPower')"],
       {"forme": "AlterEgo", "exhausted": ["us006"]}, main_exclusive=["01090"], accepter_choix=True),
    _c("us006 Walker's Chopper : TEMOIN, une guerison de CARTE (pas le pouvoir de base) ne declenche pas la Reponse",
       "« After you exhaust John Walker to RECOVER » : un soin direct n'incline pas John Walker",
       ["Puzzle.Damage('us001b', 3)"] + en_jeu("us006"), ["Puzzle.Heal('us001b', 2)"],
       {"forme": "AlterEgo", "pret": ["us006"]}, main_exclusive=["01090"], accepter_choix=True),
    _c("us006 Walker's Chopper : TEMOIN, sans le soutien en jeu la recuperation reste en alter ego",
       "ligne de base du cas 1 : sans la carte, John Walker reste John Walker",
       ["Puzzle.Damage('us001b', 3)"], ["Puzzle.Action('us001b', 'BasicPower')"],
       {"forme": "AlterEgo"}, main_exclusive=["01090"], accepter_choix=True),

    # ============================================================ us007 Convincer
    _c("us007 Convincer : entre en jeu avec 3 compteurs charge ; +1 ATQ -> l'attaque de base de U.S. Agent inflige 3 a Rhino",
       "« U.S. Agent gets +1 ATK. Uses (3 charge counters.) » : ATQ 2 + 1 = 3 ; le vilain n'est pas un sbire : pas d'etourdissement",
       [HEROS] + en_jeu("us007"), ["Puzzle.Attack('us001a')"],
       {"degats": [[VILAIN, 3]], "compteurs": [["us007", "charge", 3]], "pret": ["us007"],
        "statuts_absents": [[VILAIN, "Stunned"]]}, main_exclusive=["01090"], cibles=[VILAIN], accepter_choix=True),
    _c("us007 Convincer : sbire a 4 PV imprimes (Hydra Soldier) touche -> ETOURDI, Convincer s'incline et perd 1 compteur",
       "« After you damage a minion with base hit points of 5 or less, exhaust Convincer and remove 1 charge counter -> stun that minion » : 3 degats sur 4 PV, il survit",
       [HEROS, "Puzzle.PutIntoPlay('01182')"] + en_jeu("us007"), ["Puzzle.Attack('us001a')"],
       {"degats": [["01182", 3]], "statuts": [["01182", "Stunned"]], "exhausted": ["us007"], "compteurs": [["us007", "charge", 2]]},
       main_exclusive=["01090"], cibles=["01182"], accepter_choix=True),
    _c("us007 Convincer : TEMOIN, sbire a 8 PV imprimes (M.O.D.O.K.) -> PAS d'etourdissement, Convincer intact",
       "« 5 or LESS » : 8 PV imprimes, la Reponse ne part pas",
       [HEROS, "Puzzle.PutIntoPlay('01184')"] + en_jeu("us007"), ["Puzzle.Attack('us001a')"],
       {"degats": [["01184", 3]], "statuts_absents": [["01184", "Stunned"]], "pret": ["us007"], "compteurs": [["us007", "charge", 3]]},
       main_exclusive=["01090"], cibles=["01184"], accepter_choix=True),
    _c("us007 Convincer : TEMOIN, Convincer deja INCLINE -> pas d'etourdissement",
       "« exhaust Convincer » est un cout",
       [HEROS, "Puzzle.PutIntoPlay('01182')"] + en_jeu("us007") + ["Puzzle.Exhaust('us007')"], ["Puzzle.Attack('us001a')"],
       {"degats": [["01182", 3]], "statuts_absents": [["01182", "Stunned"]], "compteurs": [["us007", "charge", 3]]},
       main_exclusive=["01090"], cibles=["01182"], accepter_choix=True),
    _c("us007 Convincer : dernier compteur -> la carte part en defausse apres l'etourdissement (Uses natif)",
       "« Uses (3 charge counters) » : sans compteur, la carte est defaussee",
       [HEROS, "Puzzle.PutIntoPlay('01182')"] + en_jeu("us007") + ["Puzzle.Counter('us007', 'charge', -2)"], ["Puzzle.Attack('us001a')"],
       {"statuts": [["01182", "Stunned"]], "hors_jeu": ["us007"]},
       main_exclusive=["01090"], cibles=["01182"], accepter_choix=True),
    # ============================================================ us008 Obstinance
    _c("us008 Obstinance : TEMOIN, une ATQ de base sans Obstinance laisse le heros INCLINE",
       "ligne de base : le heros s'incline pour attaquer et le reste",
       [HEROS], ["Puzzle.Attack('us001a')"],
       {"exhausted": ["us001a"], "degats": [[VILAIN, 2]]}, main_exclusive=["01089"], cibles=[VILAIN], accepter_choix=True),
    _c("us008 Obstinance : ATQ de base, 1 ressource [mental] (Genius) -> U.S. Agent est REDRESSE, Obstinance s'incline",
       "« When you exhaust to use a basic power..., exhaust Obstinance and spend 1 [mental] or [physical] resource -> ready U.S. Agent »",
       [HEROS] + en_jeu("us008"), ["Puzzle.Attack('us001a')"],
       {"pret": ["us001a"], "exhausted": ["us008"], "degats": [[VILAIN, 2]], "defausse": ["01089"]},
       main_exclusive=["01089"], payer_avec=["01089"], cibles=[VILAIN], accepter_choix=True),
    _c("us008 Obstinance : ATQ de base, 1 ressource [physical] (Strength) -> U.S. Agent est REDRESSE (l'autre branche du « or »)",
       "la seconde capacite : [physical]",
       [HEROS] + en_jeu("us008"), ["Puzzle.Attack('us001a')"],
       {"pret": ["us001a"], "exhausted": ["us008"], "defausse": ["01090"]},
       main_exclusive=["01090"], payer_avec=["01090"], cibles=[VILAIN], accepter_choix=True,
       preferer_option="Spend a [physical] resource"),
    _c("us008 Obstinance : ressource [wild] (Hellcat) -> paie aussi, U.S. Agent REDRESSE",
       "[wild] couvre [mental] comme [physical]",
       [HEROS] + en_jeu("us008"), ["Puzzle.Attack('us001a')"],
       {"pret": ["us001a"], "exhausted": ["us008"], "defausse": ["01020"]},
       main_exclusive=["01020"], payer_avec=["01020"], cibles=[VILAIN], accepter_choix=True),
    _c("us008 Obstinance : CONTRE de base (Thwart) -> U.S. Agent REDRESSE",
       "« a basic power » : le contre aussi (menace 3 -> 1)",
       [HEROS, f"Puzzle.SetThreat('{COMPLOT}', 3)"] + en_jeu("us008"), ["Puzzle.Thwart('us001a')"],
       {"pret": ["us001a"], "exhausted": ["us008"], "menace": [[COMPLOT, 1]], "defausse": ["01089"]},
       main_exclusive=["01089"], payer_avec=["01089"], accepter_choix=True),
    _c("us008 Obstinance : DEFENSE de base -> U.S. Agent REDRESSE",
       "« a basic power » : la defense aussi (DEF 2 contre ATQ 2 de Rhino : aucun degat). Obstinance s'incline pour son cout puis "
       "Bolster (us001a, « After you defend, ready an upgrade you control ») la REDRESSE : les deux sont prets a la fin",
       [HEROS] + en_jeu("us008"), [f"Puzzle.Defend('us001a', '{VILAIN}')"],
       {"pret": ["us001a", "us008"], "degats_identite": 0, "defausse": ["01089"]},
       main_exclusive=["01089"], payer_avec=["01089"], accepter_choix=True),
    _c("us008 Obstinance : TEMOIN, main VIDE (aucune ressource a depenser) -> pas d'Interruption, heros incline",
       "le cout en ressource est impayable : la capacite n'est pas offerte",
       [HEROS] + en_jeu("us008"), ["Puzzle.Attack('us001a')"],
       {"exhausted": ["us001a"], "pret": ["us008"]}, main_exclusive=["01090"], payer_avec=[], ne_pas_depenser=["01090"],
       cibles=[VILAIN], accepter_choix=True),
    _c("us008 Obstinance : TEMOIN, seulement une ressource [energy] (Energy YY) -> impayable, heros incline",
       "« [mental] or [physical] » : l'energie ne paie pas",
       [HEROS] + en_jeu("us008"), ["Puzzle.Attack('us001a')"],
       {"exhausted": ["us001a"], "pret": ["us008"], "en_main": ["01088"]},
       main_exclusive=["01088"], ne_pas_depenser=["01088"], cibles=[VILAIN], accepter_choix=True),
    _c("us008 Obstinance : TEMOIN, Obstinance deja INCLINEE -> pas d'Interruption, heros incline",
       "« exhaust Obstinance » est un cout",
       [HEROS] + en_jeu("us008") + ["Puzzle.Exhaust('us008')"], ["Puzzle.Attack('us001a')"],
       {"exhausted": ["us001a", "us008"], "en_main": ["01089"]},
       main_exclusive=["01089"], ne_pas_depenser=["01089"], cibles=[VILAIN], accepter_choix=True),

    # ============================================================ us009 Solid Gear
    _c("us009 Solid Gear : Rhino INITIE une attaque -> Solid Gear s'incline ; la prochaine carte PROTECTION coute 2 de moins (Armored Vest gratuit)",
       "« When an enemy initiates an attack, exhaust Solid Gear -> reduce the resource cost of the next Protection card you play this phase by 2 » : cout 1 -> 0",
       [HEROS, "Puzzle.Exhaust('us001a')"] + en_jeu("us009"), [f"Puzzle.Attack('{VILAIN}')"],
       {"exhausted": ["us009"], "en_jeu": ["01081"], "degats_identite": 2},
       main_exclusive=["01081"], jouer=["01081"], payer_avec=[], accepter_choix=True),
    _c("us009 Solid Gear : TEMOIN, sans Solid Gear Armored Vest (cout 1) est INJOUABLE sans ressource",
       "ligne de base du cas precedent",
       [HEROS, "Puzzle.Exhaust('us001a')"], [f"Puzzle.Attack('{VILAIN}')"], {},
       main_exclusive=["01081"], jouer=["01081"], payer_avec=[], accepter_choix=True,
       verifier="hellcat_carte_restee_en_main", restee="01081"),
    _c("us009 Solid Gear : « the NEXT Protection card » -> seule la premiere est gratuite, la seconde est injouable",
       "deux amelioration Protection de cout 1 en main, aucune ressource : Armored Vest passe, Unflappable reste",
       [HEROS, "Puzzle.Exhaust('us001a')"] + en_jeu("us009"), [f"Puzzle.Attack('{VILAIN}')"],
       {"exhausted": ["us009"], "en_jeu": ["01081"], "en_main": ["09020"]},
       main_exclusive=["01081", "09020"], jouer=["01081", "09020"], payer_avec=[], accepter_choix=True),
    _c("us009 Solid Gear : TEMOIN, une carte qui n'est PAS Protection (Tenacity, Basic cout 2) ne profite pas de la reduction",
       "« Protection (green) card » : la classe Basic reste a plein tarif, injouable sans ressource",
       [HEROS, "Puzzle.Exhaust('us001a')"] + en_jeu("us009"), [f"Puzzle.Attack('{VILAIN}')"],
       {"exhausted": ["us009"]},
       main_exclusive=["01093"], jouer=["01093"], payer_avec=[], accepter_choix=True,
       verifier="hellcat_carte_restee_en_main", restee="01093"),
    _c("us009 Solid Gear : TEMOIN, Solid Gear deja INCLINE -> aucune reduction",
       "« exhaust Solid Gear » est un cout",
       [HEROS, "Puzzle.Exhaust('us001a')"] + en_jeu("us009") + ["Puzzle.Exhaust('us009')"], [f"Puzzle.Attack('{VILAIN}')"], {},
       main_exclusive=["01081"], jouer=["01081"], payer_avec=[], accepter_choix=True,
       verifier="hellcat_carte_restee_en_main", restee="01081"),

    # ============================================================ us010 U.S. Agent's Machine Gun
    _c("us010 Machine Gun : +1 ATQ ; apres avoir blesse RHINO -> 2 degats a CHAQUE sbire engage (pas au vilain), un compteur ammo en moins",
       "« After you damage an enemy, remove 1 ammo counter -> deal 2 damage to each minion engaged with you » : Rhino 2+1 = 3 ; Weapons Runner (2 PV) meurt de la rafale, donc aucune cible pour la re-proposer (ammo 3 -> 2)",
       [HEROS, "Puzzle.PutIntoPlay('01121')"] + en_jeu("us010"), ["Puzzle.Attack('us001a')"],
       {"degats": [[VILAIN, 3]], "hors_jeu": ["01121"], "compteurs": [["us010", "ammo", 2]]},
       main_exclusive=["01090"], cibles=[VILAIN], accepter_choix=True),
    _c("us010 Machine Gun : attaque d'un SBIRE (Hydra Soldier 4 PV) : il meurt (3 + 2), l'autre sbire (Shocker) prend 2",
       "le sbire touche est lui aussi engage avec soi : il subit les 2 degats de la rafale ; Shocker (3 PV) en prend 2, puis la "
       "Reponse est RE-PROPOSEE a chaque degat (RR Response, une par occurrence) : Shocker meurt a la 2e rafale, les 3 compteurs partent",
       [HEROS, "Puzzle.PutIntoPlay('01182')", "Puzzle.PutIntoPlay('01103')"] + en_jeu("us010"), ["Puzzle.Attack('us001a')"],
       {"hors_jeu": ["01182", "01103", "us010"]},
       main_exclusive=["01090"], cibles=["01182", "01103"], accepter_choix=True),
    _c("us010 Machine Gun : la rafale est une NOUVELLE occurrence -> Reponse re-proposee jusqu'a la fin des compteurs (M.O.D.O.K. 8 PV : 3 rafales = 6)",
       "RR Response : « once per occurrence » ; les 2 degats de la rafale sont « you damage an enemy » : ils re-proposent la Reponse (facultative). "
       "Arbitrage du 26/10/2026 ; avant, la garde `pas_sa_propre_rafale` l'interdisait : 1 seule rafale, M.O.D.O.K. a 2",
       [HEROS, "Puzzle.PutIntoPlay('01184')"] + en_jeu("us010"), ["Puzzle.Attack('us001a')"],
       {"degats": [["01184", 6]], "hors_jeu": ["us010"]},
       main_exclusive=["01090"], cibles=[VILAIN], accepter_choix=True),
    _c("us010 Machine Gun : TEMOIN, AUCUN sbire engage -> la rafale ne part pas, les 3 compteurs restent",
       "« deal 2 damage to each minion engaged with you » sans sbire : pas de cible, le cout n'est pas paye",
       [HEROS] + en_jeu("us010"), ["Puzzle.Attack('us001a')"],
       {"degats": [[VILAIN, 3]], "compteurs": [["us010", "ammo", 3]]},
       main_exclusive=["01090"], cibles=[VILAIN], accepter_choix=True),
    _c("us010 Machine Gun : dernier compteur -> la rafale part puis la carte est defaussee (Uses natif)",
       "« Uses (3 ammo counters) » : 1 compteur restant, 0 apres l'usage",
       [HEROS, "Puzzle.PutIntoPlay('01103')"] + en_jeu("us010") + ["Puzzle.Counter('us010', 'ammo', -2)"], ["Puzzle.Attack('us001a')"],
       {"degats": [["01103", 2]], "hors_jeu": ["us010"]},
       main_exclusive=["01090"], cibles=[VILAIN], accepter_choix=True),
    _c("us010 Machine Gun : TEMOIN, sans Machine Gun l'attaque ne blesse que Rhino (2) et le sbire est indemne",
       "ligne de base du premier cas",
       [HEROS, "Puzzle.PutIntoPlay('01103')"], ["Puzzle.Attack('us001a')"],
       {"degats": [[VILAIN, 2], ["01103", 0]]}, main_exclusive=["01090"], cibles=[VILAIN], accepter_choix=True),

    # ============================================================ us011 U.S. Agent's Shield
    _c("us011 Shield : Rhino attaque -> option « Deal 2 damage to the attacker » : Rhino subit 2, le bouclier s'incline, le heros subit l'attaque",
       "« When you are attacked by an enemy, exhaust U.S. Agent's Shield -> deal 2 damage to the attacker or prevent 1 damage » ; heros incline (ne defend pas) : 2 degats",
       [HEROS, "Puzzle.Exhaust('us001a')"] + en_jeu(BOUCLIER), [f"Puzzle.Attack('{VILAIN}')"],
       {"degats": [[VILAIN, 2]], "degats_identite": 2, "exhausted": [BOUCLIER]},
       main_exclusive=["01090"], accepter_choix=True, preferer_option="Deal 2 damage to the attacker"),
    _c("us011 Shield : option « Prevent 1 damage from this attack » : le heros subit 1 de moins, Rhino indemne",
       "l'autre branche du « or » : 2 - 1 = 1",
       [HEROS, "Puzzle.Exhaust('us001a')"] + en_jeu(BOUCLIER), [f"Puzzle.Attack('{VILAIN}')"],
       {"degats": [[VILAIN, 0]], "degats_identite": 1, "exhausted": [BOUCLIER]},
       main_exclusive=["01090"], accepter_choix=True, preferer_option="Prevent 1 damage"),
    _c("us011 Shield : TEMOIN, bouclier deja INCLINE -> ni degats a l'attaquant ni prevention",
       "« exhaust U.S. Agent's Shield » est un cout",
       [HEROS, "Puzzle.Exhaust('us001a')"] + en_jeu(BOUCLIER) + ["Puzzle.Exhaust('us011')"], [f"Puzzle.Attack('{VILAIN}')"],
       {"degats": [[VILAIN, 0]], "degats_identite": 2}, main_exclusive=["01090"], accepter_choix=True),
    _c("us011 Shield : TEMOIN, une attaque contre un ALLIE (Mockingbird) ne declenche pas l'Interruption",
       "« When YOU are attacked » : Rhino frappe l'allie, le bouclier reste pret",
       [HEROS, "Puzzle.Exhaust('us001a')"] + en_jeu(BOUCLIER, "01083"), [f"Puzzle.EnemyAttacks('{VILAIN}', '01083')"],
       {"degats": [[VILAIN, 0]], "pret": [BOUCLIER]}, main_exclusive=["01090"], accepter_choix=True),
    _c("us011 Shield : RESTRICTED -> trois armes Restricted en jeu : la plus ancienne part (base moteur)",
       "desc.Restricted : le Shield, le Convincer et la Machine Gun sont Restricted ; la troisieme fait partir la plus ancienne",
       [HEROS] + en_jeu(BOUCLIER, "us007", "us010"), [],
       {"en_jeu": ["us007", "us010"], "hors_jeu": [BOUCLIER]}, main_exclusive=["01090"]),
    # ============================================================ us012 Forced Leave
    _c("us012 Forced Leave : forme HEROS, bouclier en jeu -> bascule en ALTER EGO, branche 1 : John Walker s'incline, bouclier defausse, obligation RETIREE de la partie",
       "« Flip to alter-ego form. Choose: Exhaust John Walker and discard U.S. Agent's Shield -> remove this obligation from the game »",
       [HEROS] + en_jeu(BOUCLIER), ["Puzzle.Reveal('us012')"],
       {"forme": "AlterEgo", "exhausted": ["us001b"], "hors_jeu": [BOUCLIER], "defausse": [BOUCLIER], "us_hors_defausse_rencontre": ["us012"]},
       main_exclusive=["01090"], preferer_option="Exhaust John Walker"),
    _c("us012 Forced Leave : branche 2 -> 1 carte DEFAUSSEE AU HASARD, l'obligation est DEFAUSSEE (pas retiree), le bouclier reste en jeu",
       "« Discard 1 card from your hand at random -> discard this obligation » : main de 2 cartes -> 1",
       [HEROS] + en_jeu(BOUCLIER), ["Puzzle.Reveal('us012')"],
       {"forme": "AlterEgo", "taille_main": 1, "en_jeu": [BOUCLIER], "defausse_rencontre": ["us012"]},
       main_exclusive=["01090", "01089"], preferer_option="Discard 1 card from your hand at random"),
    _c("us012 Forced Leave : SANS bouclier en jeu la branche 1 n'est pas offerte -> branche 2 d'office",
       "cout impayable : seule la defausse au hasard reste",
       [HEROS], ["Puzzle.Reveal('us012')"],
       {"forme": "AlterEgo", "taille_main": 1, "defausse_rencontre": ["us012"]},
       main_exclusive=["01090", "01089"], preferer_option="Exhaust John Walker"),
    _c("us012 Forced Leave : DEJA en alter ego, bouclier en jeu -> branche 1 sans bascule",
       "« Flip to alter-ego form » sans effet quand on y est deja ; John Walker pret : il s'incline",
       [] + en_jeu(BOUCLIER), ["Puzzle.Reveal('us012')"],
       {"forme": "AlterEgo", "exhausted": ["us001b"], "hors_jeu": [BOUCLIER], "us_hors_defausse_rencontre": ["us012"]},
       main_exclusive=["01090"], preferer_option="Exhaust John Walker"),
    _c("us012 Forced Leave : John Walker deja INCLINE (apres la bascule) -> branche 1 impayable, branche 2",
       "« Exhaust John Walker » exige un John Walker PRET : alter ego incline, la defausse au hasard s'impose",
       en_jeu(BOUCLIER) + ["Puzzle.Exhaust('us001b')"], ["Puzzle.Reveal('us012')"],
       {"forme": "AlterEgo", "taille_main": 1, "en_jeu": [BOUCLIER], "defausse_rencontre": ["us012"]},
       main_exclusive=["01090", "01089"], preferer_option="Exhaust John Walker"),

    # ============================================================ us013 Nuke
    _c("us013 Nuke : valeurs imprimees PV 5, SCH 1, ATQ 2, CYBORG SOLDIER",
       "nombres texte <-> code (scan NEMESIS 1/5) : 5 PV, SCH 1, ATK 2",
       [HEROS, "Puzzle.PutIntoPlay('us013')"], [],
       {"pv_max": [["us013", 5]], "traits_de": [["us013", "CYBORG"], ["us013", "SOLDIER"]]}, main_exclusive=["01090"]),
    _c("us013 Nuke : TEMOIN, dessus du deck NI Aggression NI physique (Genius) -> l'attaque vaut 2",
       "la carte est defaussee mais rien ne s'ajoute",
       [HEROS, "Puzzle.Exhaust('us001a')", "Puzzle.PutIntoPlay('us013')", "Puzzle.EmptyPlayerDeck()",
        "Puzzle.CreatePlayerDeck('01088', '01089')"], ["Puzzle.Attack('us013')"],
       {"degats_identite": 2, "defausse": ["01089"]}, main_exclusive=["01090"]),
    _c("us013 Nuke : carte AGGRESSION defaussee (Chase Them Down, ressource [mental]) -> +1 degat (3)",
       "« an Aggression (red) card » : la classe suffit, meme sans ressource physique",
       [HEROS, "Puzzle.Exhaust('us001a')", "Puzzle.PutIntoPlay('us013')", "Puzzle.EmptyPlayerDeck()",
        "Puzzle.CreatePlayerDeck('01088', '01052')"], ["Puzzle.Attack('us013')"],
       {"degats_identite": 3, "defausse": ["01052"]}, main_exclusive=["01090"]),
    _c("us013 Nuke : carte avec une ressource [physical] IMPRIMEE hors Aggression (Strength, Basic) -> +1 degat (3)",
       "« or a card with a printed [physical] resource »",
       [HEROS, "Puzzle.Exhaust('us001a')", "Puzzle.PutIntoPlay('us013')", "Puzzle.EmptyPlayerDeck()",
        "Puzzle.CreatePlayerDeck('01088', '01090')"], ["Puzzle.Attack('us013')"],
       {"degats_identite": 3, "defausse": ["01090"]}, main_exclusive=["01089"]),
    _c("us013 Nuke : carte Protection a ressource [physical] (Counter-Punch) -> +1 degat (3)",
       "une autre classe que Aggression, ressource physique imprimee",
       [HEROS, "Puzzle.Exhaust('us001a')", "Puzzle.PutIntoPlay('us013')", "Puzzle.EmptyPlayerDeck()",
        "Puzzle.CreatePlayerDeck('01088', '01077')"], ["Puzzle.Attack('us013')"],
       {"degats_identite": 3, "defausse": ["01077"]}, main_exclusive=["01089"]),
    _c("us013 Nuke : Aggression ET physique (Uppercut) -> +1 SEUL degat (3), jamais +2",
       "les deux conditions sont un OU sur une meme carte",
       [HEROS, "Puzzle.Exhaust('us001a')", "Puzzle.PutIntoPlay('us013')", "Puzzle.EmptyPlayerDeck()",
        "Puzzle.CreatePlayerDeck('01088', '01054')"], ["Puzzle.Attack('us013')"],
       {"degats_identite": 3, "defausse": ["01054"]}, main_exclusive=["01089"]),
    _c("us013 Nuke : TEMOIN, ressource [wild] (Hellcat) n'est pas [physical] -> l'attaque vaut 2",
       "« printed [physical] » : l'icone physique, pas le joker",
       [HEROS, "Puzzle.Exhaust('us001a')", "Puzzle.PutIntoPlay('us013')", "Puzzle.EmptyPlayerDeck()",
        "Puzzle.CreatePlayerDeck('01088', '01020')"], ["Puzzle.Attack('us013')"],
       {"degats_identite": 2, "defausse": ["01020"]}, main_exclusive=["01089"]),
    _c("us013 Nuke : la carte est defaussee AVANT la defense -> le heros defend (DEF 2) une attaque de 3 : 1 degat",
       "Interruption forcee : le supplement joue AVANT la defense (ATQ 2 + 1 - DEF 2 = 1)",
       [HEROS, "Puzzle.PutIntoPlay('us013')", "Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01088', '01090')"],
       ["Puzzle.Defend('us001a', 'us013')"],
       {"degats_identite": 1, "defausse": ["01090"]}, main_exclusive=["01089"]),

    # ============================================================ us014 Battle of the Patriots
    _c("us014 Battle of the Patriots : menace de depart 4 (fixe), icone Acceleration imprimee",
       "nombres texte <-> code (scan NEMESIS 2/5) : menace 4 ; l'icone du centre est l'Acceleration",
       [HEROS], ["Puzzle.Reveal('us014')"], {"menace": [["us014", 4]]}, main_exclusive=["01090"]),
    _c("us014 Battle of the Patriots : une carte AGGRESSION (Relentless Assault, cout 2) coute 3 -> injouable avec 2 ressources",
       "« Aggression (red) ... cards cost 1 additional resource »",
       [HEROS, "Puzzle.PutIntoPlay('01103')", "Puzzle.PutIntoPlay('us014')"], [],
       {}, main_exclusive=["01053", "01088"], jouer=["01053"], payer_avec=["01088"], cibles=["01103"], accepter_choix=True,
       verifier="hellcat_carte_restee_en_main", restee="01053"),
    _c("us014 Battle of the Patriots : TEMOIN, SANS la manigance la meme carte est jouee (5 degats au sbire)",
       "ligne de base : Relentless Assault cout 2 paye par Energy (YY)",
       [HEROS, "Puzzle.PutIntoPlay('01182')"], [],
       {"hors_jeu": ["01182"], "defausse": ["01053", "01088"]},
       main_exclusive=["01053", "01088"], jouer=["01053"], payer_avec=["01088"], cibles=["01182"], accepter_choix=True),
    _c("us014 Battle of the Patriots : une carte BASIC (Haymaker, cout 2) coute 3 -> injouable",
       "« Basic (gray) »",
       [HEROS, "Puzzle.PutIntoPlay('us014')"], [],
       {}, main_exclusive=["01087", "01088"], jouer=["01087"], payer_avec=["01088"], cibles=[VILAIN], accepter_choix=True,
       verifier="hellcat_carte_restee_en_main", restee="01087"),
    _c("us014 Battle of the Patriots : une carte LEADERSHIP (Get Ready, cout 0) coute 1 -> injouable sans ressource",
       "« Leadership (blue) » : cout 0 -> 1, une seule carte en main, aucune ressource",
       [HEROS, "Puzzle.PutIntoPlay('us014')"] + en_jeu("01083") + ["Puzzle.Exhaust('01083')"], [],
       {}, main_exclusive=["01069"], jouer=["01069"], payer_avec=[], accepter_choix=True,
       verifier="hellcat_carte_restee_en_main", restee="01069"),
    _c("us014 Battle of the Patriots : TEMOIN, la meme carte LEADERSHIP (cout 0) est jouee SANS la manigance : l'allie est redresse",
       "ligne de base de Get Ready",
       [HEROS] + en_jeu("01083") + ["Puzzle.Exhaust('01083')"], [],
       {"pret": ["01083"], "defausse": ["01069"]}, main_exclusive=["01069"], jouer=["01069"], payer_avec=[], accepter_choix=True),
    _c("us014 Battle of the Patriots : TEMOIN, une carte PROTECTION (Armored Vest, cout 1) reste a 1 : jouee avec UNE ressource",
       "Protection n'est pas concernee",
       [HEROS, "Puzzle.PutIntoPlay('us014')"], [],
       {"en_jeu": ["01081"], "defausse": ["01020"]}, main_exclusive=["01081", "01020"], jouer=["01081"], payer_avec=["01020"],
       accepter_choix=True),
    _c("us014 Battle of the Patriots : TEMOIN, une carte JUSTICE (Heroic Intuition, cout 2) reste a 2 : jouee avec YY",
       "Justice n'est pas concernee",
       [HEROS, "Puzzle.PutIntoPlay('us014')"], [],
       {"en_jeu": ["01065"], "defausse": ["01088"]}, main_exclusive=["01065", "01088"], jouer=["01065"], payer_avec=["01088"],
       accepter_choix=True),
    _c("us014 Battle of the Patriots : TEMOIN, une carte HERO (Obstinance, cout 1) reste a 1 : jouee avec UNE ressource",
       "les cartes signature (classe Hero) ne sont pas Aggression / Basic / Leadership",
       [HEROS, "Puzzle.PutIntoPlay('us014')"], [],
       {"en_jeu": ["us008"], "defausse": ["01020"]}, main_exclusive=["us008", "01020"], jouer=["us008"], payer_avec=["01020"],
       accepter_choix=True),
    _c("us014 Battle of the Patriots : la manigance QUITTE le jeu -> le cout redevient normal (Relentless Assault jouee)",
       "l'effet est continu : il tombe avec la carte",
       [HEROS, "Puzzle.PutIntoPlay('01182')", "Puzzle.PutIntoPlay('us014')", "Puzzle.Remove('us014')"], [],
       {"hors_jeu": ["01182"], "defausse": ["01053", "01088"]},
       main_exclusive=["01053", "01088"], jouer=["01053"], payer_avec=["01088"], cibles=["01182"], accepter_choix=True),

    # ============================================================ us015 Seeing Red
    _c("us015 Seeing Red : 2 cartes defaussees, la 2e a une ressource [physical] (Strength) -> 2 degats INDIRECTS au heros",
       "« Discard the top 2 cards from your deck. If a card with a printed [physical] resource was discarded this way, take 2 indirect damage »",
       [HEROS, "Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01089', '01090', '01088')"], ["Puzzle.Reveal('us015')"],
       {"degats_identite": 2, "defausse": ["01088", "01090"], "taille_deck_joueur": 1}, main_exclusive=["01020"]),
    _c("us015 Seeing Red : les DEUX cartes ont une ressource [physical] -> 2 degats seulement (pas 4)",
       "« if A card ... was discarded »",
       [HEROS, "Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01089', '01090', '01077')"], ["Puzzle.Reveal('us015')"],
       {"degats_identite": 2, "defausse": ["01077", "01090"]}, main_exclusive=["01020"]),
    _c("us015 Seeing Red : TEMOIN, aucune ressource [physical] (Energy, Genius) -> 0 degat",
       "les deux cartes sont defaussees, aucun degat",
       [HEROS, "Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01090', '01089', '01088')"], ["Puzzle.Reveal('us015')"],
       {"degats_identite": 0, "defausse": ["01088", "01089"], "taille_deck_joueur": 1}, main_exclusive=["01020"]),
    _c("us015 Seeing Red : TEMOIN, une ressource [wild] (Hellcat) n'est pas [physical] -> 0 degat",
       "« printed [physical] » : pas le joker",
       [HEROS, "Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01090', '01020', '01088')"], ["Puzzle.Reveal('us015')"],
       {"degats_identite": 0, "defausse": ["01088", "01020"]}, main_exclusive=["01089"]),
    _c("us015 Seeing Red : TEMOIN, la 3e carte (non defaussee) est [physical] -> 0 degat",
       "seules les 2 cartes du dessus comptent",
       [HEROS, "Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01090', '01089', '01088')"], ["Puzzle.Reveal('us015')"],
       {"degats_identite": 0, "taille_deck_joueur": 1}, main_exclusive=["01020"]),

    # ============================================================ us016 Spear of Odin
    _c("us016 Spear of Odin : s'attache a l'ennemi qui a le PLUS de PV RESTANTS (Rhino contre un sbire)",
       "« Attach to the enemy with the most remaining hit points »",
       [HEROS, "Puzzle.PutIntoPlay('01182')"], ["Puzzle.Reveal('us016')"],
       {"hotes": [["us016", VILAIN]]}, main_exclusive=["01090"]),
    _c("us016 Spear of Odin : PV RESTANTS, pas imprimes : Rhino tres blesse, M.O.D.O.K. (8 PV) en a plus -> il porte la lance",
       "« most REMAINING hit points »",
       [HEROS, "Puzzle.PutIntoPlay('01184')", f"Puzzle.Damage('{VILAIN}', 12)"], ["Puzzle.Reveal('us016')"],
       {"hotes": [["us016", "01184"]]}, main_exclusive=["01090"]),
    _c("us016 Spear of Odin : l'ennemi porteur blesse le HEROS -> une amelioration au choix est defaussee, puis la lance",
       "« Forced Interrupt: When attached enemy deals damage to your hero, discard an upgrade you control, then discard Spear of Odin »",
       [HEROS, "Puzzle.Exhaust('us001a')", "Puzzle.PutIntoPlay('us016')"] + en_jeu("us008"), [f"Puzzle.Attack('{VILAIN}')"],
       {"degats_identite": 2, "hors_jeu": ["us008", "us016"], "defausse": ["us008"]}, main_exclusive=["01090"]),
    _c("us016 Spear of Odin : SANS amelioration la lance se defausse quand meme",
       "« then discard Spear of Odin » : pas de condition sur la premiere moitie",
       [HEROS, "Puzzle.Exhaust('us001a')", "Puzzle.PutIntoPlay('us016')"], [f"Puzzle.Attack('{VILAIN}')"],
       {"degats_identite": 2, "hors_jeu": ["us016"]}, main_exclusive=["01090"]),
    _c("us016 Spear of Odin : TEMOIN, un AUTRE ennemi (Weapons Runner) blesse le heros -> la lance reste attachee a Rhino, l'amelioration reste",
       "« attached enemy » : seul le porteur declenche",
       [HEROS, "Puzzle.Exhaust('us001a')", "Puzzle.PutIntoPlay('us016')", "Puzzle.PutIntoPlay('01121')"] + en_jeu("us008"),
       ["Puzzle.Attack('01121')"],
       {"degats_identite": 1, "en_jeu": ["us008", "us016"], "hotes": [["us016", VILAIN]]}, main_exclusive=["01090"]),
    _c("us016 Spear of Odin : TEMOIN, en forme ALTER EGO les degats du porteur ne declenchent pas (« your HERO »)",
       "« damage to your HERO » : l'identite sous sa forme alter ego n'est pas le heros",
       ["Puzzle.PutIntoPlay('us016')"] + en_jeu("us008"), [f"Puzzle.Attack('{VILAIN}')"],
       {"en_jeu": ["us008", "us016"]}, main_exclusive=["01090"]),
]


VERIFICATIONS = r'''
def us_etat(monde, aides):
    """Cles propres : `retirees` (card_id dans la zone retiree du jeu), `us_stats` ({attribut: valeur} lus sur
    l'identite), `us_traits_main` ([[card_id, [traits exacts]]] d'une carte EN MAIN) ; le reste va a etat_attendu."""
    cas = aides["cas"]
    attendu = cas.get("attendu") or {}
    soucis = []
    ids = [getattr(f.paper, "card_id", None) for f in monde.area_removed.Get(True)]
    for c in attendu.get("retirees") or []:
        if c not in ids:
            soucis.append(f"{c} pas retiree du jeu (retirees = {ids})")
    for c in attendu.get("us_hors_defausse_rencontre") or []:
        # `us012` (obligation) est deja dans la zone retiree des la mise en place (EmptyEncounterDeck) : « retiree de la
        # partie » se prouve donc par l'ABSENCE de la defausse de rencontre, pas par la presence dans la zone retiree.
        from game.operate.worlds import Worlds
        piles = [monde.GetScenario().encounter_discard_pile]
        for villain in getattr(monde, "villains", []) or []:
            pile = getattr(villain, "encounter_discard_pile", None)
            if pile is not None:
                piles.append(pile)
        cartes = [getattr(f.paper, "card_id", None) for pile in piles for f in pile.GetAll()]
        cartes += [getattr(f.paper, "card_id", None) for f in Worlds.GetEncounterDiscardPileCards(monde)]
        if c in cartes:
            soucis.append(f"{c} est dans la defausse de rencontre alors qu'elle devait etre RETIREE de la partie ({cartes})")
    identite = aides["identite"](monde)
    for nom, valeur in (attendu.get("us_stats") or {}).items():
        courant = getattr(identite, nom, None)
        if courant != valeur:
            soucis.append(f"{nom} = {courant} (attendu {valeur})")
    main = {getattr(f.paper, "card_id", None): f for f in monde.players[0].hand_cards.Get()}
    for card_id, traits in attendu.get("us_traits_main") or []:
        face = main.get(card_id)
        if face is None:
            soucis.append(f"{card_id} absente de la main (us_traits_main)")
            continue
        for t in ("ATTACK", "TACTIC", "THWART", "SKILL"):
            if face.HasTrait(t) != (t in traits):
                soucis.append(f"{card_id} : trait {t} {'present' if face.HasTrait(t) else 'absent'} (attendu {traits})")
    reste = {k: v for k, v in attendu.items() if k not in ("retirees", "us_hors_defausse_rencontre", "us_stats", "us_traits_main")}
    copie = dict(aides); copie["cas"] = dict(cas); copie["cas"]["attendu"] = reste
    ok, message = etat_attendu(monde, copie)
    if not ok:
        soucis.append(message)
    if soucis:
        return False, " ; ".join(soucis)
    return True, message
'''
