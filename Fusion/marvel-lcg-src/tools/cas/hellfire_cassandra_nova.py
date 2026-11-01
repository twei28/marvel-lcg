# Cas test_capacites du scenario 5 « CASSANDRA NOVA » de la campagne Hellfire Hunt (Dipsome), prefixe `hf`, pack hellfire_hunt_cassandra_nova (set 245) :
# noms prefixes « [hf] » puis le card_id (substituer_pack.py filtre dessus). Modules : Mind Control (hf371-hf376), Mutant Extinction Agenda (hf381-hf388).
#
# Rappels de montage (voir aussi tools/cas/hellfire_white_queen.py, dont celui-ci reprend les conventions) :
#  - `spider_man` demarre en ALTER-EGO : `Puzzle.ChangeForm('01001a')` le passe en HEROS (le vilain ATTAQUE un heros, MANIGANCE contre un alter ego) ;
#  - le vilain est Cassandra Nova I (hf601) et le complot Diplomatic Sabotage 1B (hf604b : menace 1 a la mise en place, cible 7) ;
#  - 01105 = « Bomb Scare » (aucune capacite de boost), remplissage inoffensif ; `Puzzle.CreateEncounterDeck(a, b)` pose `a` en DERNIER ;
#  - `Puzzle.BeginVillainPhase()` ne fait pas activer le vilain : `Puzzle.Attack('<vilain>')` / `Puzzle.Scheme('<vilain>')`.
SC = "hellfire_cassandra_nova"
SCX = "hellfire_cassandra_nova_expert"
HEROS = "Puzzle.ChangeForm('01001a')"   # spider_man demarre en ALTER-EGO
CTR = "cassandra_controls"
LIB_MENACE = "Place 2 threat on each scheme"
LIB_STATUTS = "Stun and confuse your identity"
LIB_DEGATS = "Deal 3 indirect damage to another friendly character"


def deck(*cartes, remplissage=14):
    """Deck de rencontre de test, les cartes voulues listees DU DESSUS vers le dessous, puis du remplissage inoffensif."""
    ids = list(cartes) + ["01105"] * remplissage
    return ["Puzzle.EmptyEncounterDiscardPile()", "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck(%s)" % ", ".join("'%s'" % c for c in reversed(ids))]


def controles(n, carte="01001b"):
    """Pose n compteurs « Cassandra Controls » sur l'identite (alter-ego `01001b` au depart ; a poser AVANT `HEROS`) : etat de depart du cas.
    ⚠ A 3 compteurs ou plus, Cassandra Domination se declenche : les cas qui ne la visent pas restent a 2 au plus."""
    return ["Puzzle.PlaceCounters('%s', '%s', %d)" % (carte, CTR, n)] if n else []


def _c(nom, pourquoi, mise, declencher, attendu, **cle):
    # `questions_presentes` / `questions_absentes` sont des cles du CAS (lues par le pilote), pas de `attendu` : posees dans `attendu` elles etaient ignorees en
    # silence (decouvert le 01/11/2026 par le garde-fou de hfn_etat). On les remonte ici pour que chaque cas les ecrive la ou il est naturel de les lire.
    attendu = dict(attendu)
    for _k in ("questions_presentes", "questions_absentes"):
        if _k in attendu:
            cle[_k] = attendu.pop(_k)
    cas = {"nom": "[hf] " + nom, "pourquoi": pourquoi, "scenario": cle.pop("scenario", SC),
           "heros": cle.pop("heros", "spider_man"), "mise_en_place": ["Puzzle.EmptyHand()"] + list(mise), "declencher": declencher,
           "verifier": cle.pop("verifier", "hfn_etat"), "attendu": attendu}
    cas.update(cle)
    cas.setdefault("main_exclusive", ["01090"])
    return cas


CAS = [
    _c("hf604a mise en place : Cassandra Nova I (hf601) en jeu, PV 15, complot 1B (hf604b) a 1 menace, Cassandra Domination (hf607) en jeu",
       "le scenario `hellfire_cassandra_nova` se charge : cartes imprimees (nombres texte <-> code), environnement mis de cote puis en jeu",
       deck("01105"), [],
       {"en_jeu": ["hf601", "hf604b", "hf607"], "vie": [["hf601", 15]], "attaque": [["hf601", 1]], "menace_de": [["hf604b", 1]],
        "trait_de": [["hf601", "MUMMUDRAI", True], ["hf601", "PSIONIC", True]], "compteurs_identite": [[CTR, 0]]}),

    _c("hf604a mise en place EXPERT : Cassandra Nova II (hf602) en jeu, le complot a avance au stade 2 (hf605b), Cassandra Domination en jeu, 1 compteur sur l'identite",
       "« In expert mode, advance to stage 2A » + villain (II) et (III) : le stade II est revele a la mise en place (« Place 1 Cassandra Controls counter on each identity »)",
       deck("01105"), [],
       {"en_jeu": ["hf602", "hf605b", "hf607"], "absents": ["hf601", "hf604b"], "vie": [["hf602", 18]], "compteurs_identite": [[CTR, 1]]}, scenario=SCX),
    _c("hf604a Setup : le sbire Cassandra Nova du module Immensity (hf351) est RETIRE du jeu (il n'est plus dans le deck de rencontre)",
       "« Remove Cassandra Nova minion from the game » ; le vilain homonyme reste en jeu",
       [], [], {"en_jeu": ["hf601"], "hors_deck_rencontre": ["hf351"]}),
    # ===================================================================== les compteurs vivent sur l'IDENTITE (quelle que soit la forme)
    _c("hf607 compteur sur l'identite : il reste quand le joueur change de forme (alter-ego -> heros)",
       "le stock de « Cassandra Controls » est celui de la CARTE d'identite : `01001b` et `01001a` partagent les compteurs",
       controles(2) + deck("01105"), [HEROS], {"compteurs_identite": [[CTR, 2]]}),
    # ===================================================================== hf601 : Reponse forcee apres activation CONTRE le joueur
    _c("hf601 Reponse forcee : apres son ATTAQUE contre le joueur (heros), 1 compteur Cassandra Controls sur l'identite",
       "« After Cassandra Nova activates against you, place 1 Cassandra Controls counter on your identity card » : attaque (heros)",
       [HEROS] + deck("01105"), ["Puzzle.Attack('hf601')"], {"compteurs_identite": [[CTR, 1]]}),
    _c("hf601 Reponse forcee : apres son COMPLOT contre le joueur (alter-ego), 1 compteur",
       "« activates » couvre l'attaque ET le complot", deck("01105"), ["Puzzle.Scheme('hf601')"], {"compteurs_identite": [[CTR, 1]]}),
    _c("hf601 Reponse forcee : TEMOIN, un SBIRE qui attaque (Wild Sentinel) ne pose aucun compteur",
       "la reponse n'est portee que par Cassandra Nova elle-meme (« This »)",
       [HEROS, "Puzzle.PutIntoPlay('hf382')"] + deck("01105"), ["Puzzle.Attack('hf382')"], {"compteurs_identite": [[CTR, 0]]}),
    _c("hf601 Reponse forcee : A DEUX JOUEURS, seul le joueur VISE recoit le compteur",
       "« activates against YOU » : l'attaque vise le joueur courant (siege 1) ; le second identite reste a 0",
       [HEROS] + deck("01105"), ["Puzzle.Attack('hf601')"], {"compteurs_identite": [[CTR, 1]], "controles_joueurs": [1, 0]}, heros2="spider_man"),
    _c("hf602 When Revealed : le stade 2 est revele quand le stade 1 est vaincu : 1 compteur sur CHAQUE identite (2 joueurs), Steady, PV 18 par joueur, ATK 2",
       "« Place 1 Cassandra Controls counter on each identity » ; valeurs imprimees : PV 18[per_hero], ATK 2, SCH 3, Steady",
       deck("01105"), ["Puzzle.Damage('hf601', 30)"],
       {"en_jeu": ["hf602"], "absents": ["hf601"], "vie": [["hf602", 36]], "attaque": [["hf602", 2]], "steady": ["hf602"], "controles_joueurs": [1, 1]},
       heros2="spider_man"),
    _c("hf602 When Revealed : en SOLO, 1 compteur et valeurs imprimees (PV 18, ATK 2, SCH 3 : un complot seul pose 3 menaces)",
       "contre-cas du nombre de joueurs", deck("01105"), ["Puzzle.Damage('hf601', 15)"],
       {"en_jeu": ["hf602"], "vie": [["hf602", 18]], "attaque": [["hf602", 2]], "compteurs_identite": [[CTR, 1]]}),
    _c("hf603 When Revealed (EXPERT) : le stade III est revele : 1 compteur sur chaque identite ET 1 jeton d'acceleration par joueur (2) sur le complot ; Stalwart ; PV 20 par joueur",
       "« Place 1 Cassandra Controls counter on each identity and place 1[per_hero] acceleration tokens on the main scheme »",
       deck("01105"), ["Puzzle.Damage('hf602', 40)"],
       {"en_jeu": ["hf603"], "absents": ["hf602"], "vie": [["hf603", 40]], "attaque": [["hf603", 3]], "stalwart": ["hf603"], "acceleration": [["hf605b", 2]],
        "controles_joueurs": [2, 2]}, scenario=SCX, heros2="spider_man"),
    _c("hf603 When Revealed (EXPERT) : en SOLO, 1 seul jeton d'acceleration",
       "« 1[per_hero] » : un joueur, un jeton", deck("01105"), ["Puzzle.Damage('hf602', 18)"],
       {"en_jeu": ["hf603"], "acceleration": [["hf605b", 1]], "compteurs_identite": [[CTR, 2]]}, scenario=SCX),

    # ===================================================================== hf604b / hf605b / hf606b : Reponse forcee de fin de tour
    _c("hf604b Reponse forcee : fin de tour avec 1 compteur -> le joueur CHOISIT : 1 menace sur le complot (premiere option)",
       "« After your turn ends, if there is Cassandra Controls counter on your identity, you must choose to either place 1 threat here or take 2 damage »",
       controles(1) + deck("01105"), ["Puzzle.EndPlayerTurn()"],
       {"menace_de": [["hf604b", 2]], "degats_identite": 0, "questions_presentes": ["Place 1 threat here", "Take 2 damage"]}),
    _c("hf604b Reponse forcee : le joueur choisit l'AUTRE branche : 2 degats a l'identite, pas de menace",
       "« or take 2 damage » : degats DIRECTS a l'identite", controles(1) + deck("01105"), ["Puzzle.EndPlayerTurn()"],
       {"menace_de": [["hf604b", 1]], "degats_identite": 2}, choisir_option="Take_2_damage"),
    _c("hf604b Reponse forcee : TEMOIN, sans compteur sur l'identite rien ne se passe et aucune question n'est posee",
       "la condition « if there is Cassandra Controls counter on your identity »", deck("01105"), ["Puzzle.EndPlayerTurn()"],
       {"menace_de": [["hf604b", 1]], "degats_identite": 0, "questions_absentes": ["Place 1 threat here"]}),
    _c("hf604b Reponse forcee : A DEUX JOUEURS, seul le joueur dont le tour finit et qui est controle est concerne (2e joueur sans compteur : 1 seule menace)",
       "« your turn » / « your identity » : le compteur du joueur 1 compte, pas celui de l'autre", controles(1) + deck("01105"),
       ["Puzzle.EndPlayerTurn()"], {"menace_de": [["hf604b", 2 + 1]]}, heros2="spider_man"),
    _c("hf604b Action de heros : defausse 5 cartes du dessus du deck de rencontre -> retire 1 compteur de l'identite",
       "« Discard 5 cards from the top of the encounter deck -> remove a Cassandra Controls counter from your identity »",
       controles(2) + [HEROS] + deck("01105"), ["Puzzle.Action('hf604b', 'HeroAction')"],
       {"compteurs_identite": [[CTR, 1]], "taille_defausse_rencontre": 5}),
    _c("hf604b Action de heros : TEMOIN d'EPUISEMENT, une SECONDE action dans le meme round est refusee (1 compteur retire seulement, 5 cartes defaussees)",
       "« (Limit once per round per player.) » : deux declenchements dans le meme round, chiffre mesure au second",
       controles(2) + [HEROS] + deck("01105"), ["Puzzle.Action('hf604b', 'HeroAction')"],
       {"compteurs_identite": [[CTR, 1]], "taille_defausse_rencontre": 5}, declencher_tolerant=["Puzzle.Action('hf604b', 'HeroAction')"]),
    _c("hf604b Action de heros : sans compteur sur l'identite l'action n'est pas proposee (rien n'est defausse)",
       "le retrait n'aurait aucun effet", [HEROS] + deck("01105"), [],
       {"compteurs_identite": [[CTR, 0]], "taille_defausse_rencontre": 0}, declencher_tolerant=["Puzzle.Action('hf604b', 'HeroAction')"]),

    # ===================================================================== hf605a / hf605b : Silent Takeover
    _c("hf605a When Revealed : le complot avance a Silent Takeover -> chaque joueur trouve SON sbire nemesis (Vulture) et le met en jeu engage avec lui",
       "« Each player finds their own nemesis minion and put it into play engaged with themself »",
       deck("01105"), ["Puzzle.AdvanceMainScheme()"], {"en_jeu": ["hf605b", "01167"], "absents": ["hf604b"]}),
    _c("hf605a When Revealed : sans sbire nemesis a trouver, rien ne se passe (pas de plantage, le complot est avance)",
       "« finds » : aucune carte trouvee -> aucune mise en jeu", ["Puzzle.RemoveNemesisAside()"] + deck("01105"), ["Puzzle.AdvanceMainScheme()"],
       {"en_jeu": ["hf605b"], "absents": ["hf604b", "01167"]}),
    _c("hf605b Reponse forcee : fin de tour avec 1 compteur -> 2 menaces sur le complot (premiere option)",
       "« you must choose to either place 2 threat here or deal yourself 1 facedown encounter card »",
       ["Puzzle.RemoveNemesisAside()", "Puzzle.AdvanceMainScheme()"] + controles(1) + deck("01105"), ["Puzzle.EndPlayerTurn()"],
       {"menace_de": [["hf605b", 4]], "distribuees": 0, "questions_presentes": ["Place 2 threat here", "Deal yourself 1 facedown encounter card"]}),
    _c("hf605b Reponse forcee : l'AUTRE branche -> 1 carte rencontre face cachee, la menace ne bouge pas",
       "« or deal yourself 1 facedown encounter card »", ["Puzzle.RemoveNemesisAside()", "Puzzle.AdvanceMainScheme()"] + controles(1) + deck("01105"),
       ["Puzzle.EndPlayerTurn()"], {"menace_de": [["hf605b", 2]], "distribuees": 1}, choisir_option="Deal_yourself_1_facedown_encounter_card"),
    _c("hf605b Action de heros : defausse 6 cartes du deck de rencontre -> retire 1 compteur (limite 1 par round et par joueur : la seconde est refusee)",
       "« Discard 6 cards ... remove a Cassandra Controls counter » + temoin d'epuisement (2 compteurs au depart, un seul retire)",
       ["Puzzle.RemoveNemesisAside()", "Puzzle.AdvanceMainScheme()"] + controles(2) + [HEROS] + deck("01105"), ["Puzzle.Action('hf605b', 'HeroAction')"],
       {"compteurs_identite": [[CTR, 1]], "taille_defausse_rencontre": 6}, declencher_tolerant=["Puzzle.Action('hf605b', 'HeroAction')"]),
    # ===================================================================== hf606a / hf606b : Mutant Extermination
    _c("hf606a When Revealed : 1 carte rencontre face cachee par personnage controle (l'identite + 1 allie = 2)",
       "« Deal each player 1 facedown encounter card for each character they control »",
       ["Puzzle.RemoveNemesisAside()", "Puzzle.PutIntoPlay('01083', under_control=True)"] + deck("01105"), ["Puzzle.AdvanceMainScheme(2)"],
       {"en_jeu": ["hf606b"], "distribuees": 2}),
    _c("hf606a When Revealed : TEMOIN, sans allie, 1 seule carte (l'identite)",
       "le compte suit les personnages controles", ["Puzzle.RemoveNemesisAside()"] + deck("01105"), ["Puzzle.AdvanceMainScheme(2)"],
       {"en_jeu": ["hf606b"], "distribuees": 1}),
    _c("hf606b Reponse forcee : 3 menaces OU defausser 1 carte de la main (premiere option : menace)",
       "« you must choose to either place 3 threat here or discard 1 card from your hand »",
       ["Puzzle.RemoveNemesisAside()", "Puzzle.AdvanceMainScheme(2)", "Puzzle.CreateHandCards('01089')"] + controles(1) + deck("01105"), ["Puzzle.EndPlayerTurn()"],
       {"menace_de": [["hf606b", 6]], "taille_main": 1}, main_exclusive=["01089"]),
    _c("hf606b Reponse forcee : l'AUTRE branche -> 1 carte defaussee de la main (choisie par le joueur), la menace ne bouge pas",
       "« or discard 1 card from your hand »", ["Puzzle.RemoveNemesisAside()", "Puzzle.AdvanceMainScheme(2)"] + controles(1) + deck("01105"),
       ["Puzzle.EndPlayerTurn()"], {"menace_de": [["hf606b", 3]], "taille_main": 1}, main_exclusive=["01089", "01090"], choisir_option="Discard_1_card_from_your_hand"),
    _c("hf606b Reponse forcee : main VIDE -> l'option « defausser » DISPARAIT, il ne reste que la menace",
       "option impossible = retiree du choix", ["Puzzle.RemoveNemesisAside()", "Puzzle.AdvanceMainScheme(2)"] + controles(1) + deck("01105"), ["Puzzle.EndPlayerTurn()"],
       {"menace_de": [["hf606b", 6]], "taille_main": 0, "questions_absentes": ["Discard 1 card from your hand"]}, main_exclusive=[]),
    _c("hf606b Action de heros : defausse 7 cartes du deck de rencontre -> retire 1 compteur",
       "« Discard 7 cards from the top of the encounter deck -> remove a Cassandra Controls counter »",
       ["Puzzle.RemoveNemesisAside()", "Puzzle.AdvanceMainScheme(2)"] + controles(2) + [HEROS] + deck("01105"), ["Puzzle.Action('hf606b', 'HeroAction')"],
       {"compteurs_identite": [[CTR, 1]], "taille_defausse_rencontre": 7}),
    _c("hf606b : complot COMPLETE -> les joueurs PERDENT la partie (regle du dernier stade, ajoutee a la main)",
       "« When this scheme is completed, the players lose the game » ; cible 13 par joueur",
       ["Puzzle.RemoveNemesisAside()", "Puzzle.AdvanceMainScheme(2)"] + deck("01105"), ["Puzzle.PlaceThreat('hf606b', 13)"],
       {"gagnee": False, "partie_finie": True}),
    _c("hf606b : TEMOIN, 12 menaces (sous la cible 13) -> la partie continue",
       "contre-cas du seuil", ["Puzzle.RemoveNemesisAside()", "Puzzle.AdvanceMainScheme(2)"] + deck("01105"), ["Puzzle.SetThreat('hf606b', 12)"],
       {"partie_finie": False}),
    # ===================================================================== hf607 Cassandra Domination
    _c("hf607 Reponse forcee : le 3e compteur est pose (attaque de Nova) -> 3 compteurs RETIRES, premiere option : 2 menaces sur CHAQUE manigance (complot 1 -> 3, annexe 2 -> 4)",
       "« remove 3 counters from it -> you choose one : place 2 threat on each scheme... » ; une manigance annexe (Breakin' & Takin') pour « each scheme »",
       controles(2) + [HEROS, "Puzzle.PutIntoPlay('01107')"] + deck("01105"), ["Puzzle.Attack('hf601')"],
       {"compteurs_identite": [[CTR, 0]], "menace_de": [["hf604b", 3], ["01107", 4]], "questions_presentes": [LIB_MENACE, LIB_STATUTS]}),
    _c("hf607 Reponse forcee : branche 2, etourdir ET desorienter l'identite",
       "« stun and confuse your identity »", controles(2) + [HEROS] + deck("01105"), ["Puzzle.Attack('hf601')"],
       {"compteurs_identite": [[CTR, 0]], "menace_de": [["hf604b", 1]], "statuts": [["01001a", "Stunned"], ["01001a", "Confused"]]}, choisir_option="Stun_and_confuse_your_identity"),
    _c("hf607 Reponse forcee : branche 3, 3 degats indirects a un AUTRE personnage ami (Jessica Jones, PV 3 : vaincue ; l'identite ne perd rien)",
       "« deal 3 indirect damage to another friendly character » : Jessica Jones est le seul autre personnage ami, elle peut absorber 3",
       controles(2) + [HEROS, "Puzzle.PutIntoPlay('01059', under_control=True)"] + deck("01105"), ["Puzzle.Attack('hf601', defender='01001a')"],
       {"compteurs_identite": [[CTR, 0]], "degats_identite": 0, "hors_jeu": ["01059"], "questions_presentes": [LIB_DEGATS]},
       choisir_option="Deal_3_indirect_damage_to_another_friendly_character"),
    _c("hf607 FAQ p.22 : un SEUL autre personnage ami a moins de 3 PV (Black Cat, 2 PV) -> l'option « degats » DISPARAIT, restent menace et etourdir/desorienter",
       "« you can't deal the full 3 indirect damage among another friendly characters ... This eliminates the damage option »",
       controles(2) + [HEROS, "Puzzle.PutIntoPlay('01002', under_control=True)"] + deck("01105"), ["Puzzle.Attack('hf601', defender='01001a')"],
       {"compteurs_identite": [[CTR, 0]], "questions_absentes": [LIB_DEGATS], "questions_presentes": [LIB_MENACE, LIB_STATUTS]}),
    _c("hf607 FAQ p.22 : AUCUN autre personnage ami -> l'option « degats » disparait aussi (on ne peut pas se blesser soi-meme)",
       "« you cannot damage yourself »", controles(2) + [HEROS] + deck("01105"), ["Puzzle.Attack('hf601')"],
       {"compteurs_identite": [[CTR, 0]], "questions_absentes": [LIB_DEGATS], "questions_presentes": [LIB_MENACE, LIB_STATUTS]}),
    _c("hf607 FAQ p.22 : identite DEJA etourdie -> l'option « etourdir/desorienter » disparait",
       "« If you're already stunned or confused, that option is also out »", controles(2) + [HEROS, "Puzzle.Stun('01001a')", "Puzzle.PutIntoPlay('01059', under_control=True)"] + deck("01105"),
       ["Puzzle.Attack('hf601', defender='01001a')"],
       {"compteurs_identite": [[CTR, 0]], "questions_absentes": [LIB_STATUTS], "questions_presentes": [LIB_MENACE, LIB_DEGATS]}),
    _c("hf607 FAQ p.22 : identite DEJA desorientee -> meme exclusion (l'identite desorientee depuis la mise en place)",
       "« already stunned or confused »", controles(2) + [HEROS, "Puzzle.Confuse('01001a')", "Puzzle.PutIntoPlay('01059', under_control=True)"] + deck("01105"),
       ["Puzzle.Attack('hf601', defender='01001a')"],
       {"compteurs_identite": [[CTR, 0]], "questions_absentes": [LIB_STATUTS], "questions_presentes": [LIB_MENACE, LIB_DEGATS]}),
    _c("hf607 FAQ p.22 : DEUX exclusions a la fois (deja etourdie ET aucun autre ami) -> il ne reste que la menace (+2 sur le complot)",
       "« it will leave only placing threat » : seule option, resolue sans question de statut ni de degats",
       controles(2) + [HEROS, "Puzzle.Stun('01001a')"] + deck("01105"), ["Puzzle.Attack('hf601')"],
       {"compteurs_identite": [[CTR, 0]], "menace_de": [["hf604b", 3]], "questions_absentes": [LIB_STATUTS, LIB_DEGATS]}),
    _c("hf607 A DEUX JOUEURS : un AUTRE personnage ami = l'identite de l'autre joueur : l'option « degats » reste offerte sans allie",
       "« another friendly character » : l'identite du second joueur est un personnage ami", controles(2) + [HEROS] + deck("01105"),
       ["Puzzle.Attack('hf601')"], {"compteurs_identite": [[CTR, 0]], "questions_presentes": [LIB_DEGATS]}, heros2="spider_man"),
    _c("hf607 SEUIL : a 2 compteurs seulement (1 + celui de l'attaque) rien ne se declenche (aucune question, 2 compteurs restent)",
       "« if there is at least 3 Cassandra Controls counter »", controles(1) + [HEROS] + deck("01105"), ["Puzzle.Attack('hf601')"],
       {"compteurs_identite": [[CTR, 2]], "questions_absentes": [LIB_MENACE, LIB_STATUTS], "menace_de": [["hf604b", 1]]}),
    _c("hf607 SEUIL : 4 compteurs d'un coup (2 + 2 de Global Opinion Controls en boost) -> UNE resolution, il en reste 1",
       "« remove 3 » une seule fois par pose ; reste 4 - 3 = 1", controles(2) + [HEROS] + deck("hf620"), ["Puzzle.Attack('hf601')"],
       {"compteurs_identite": [[CTR, 2]], "questions_presentes": [LIB_MENACE]}),

    # ===================================================================== hf608 / hf609 Exploding Their Head
    _c("hf608 Obligation revelee : elle va dans la zone du joueur ; Reponse forcee de fin de tour : Black Cat (cout 2) est defaussee, 1 degat a l'identite, l'obligation est defaussee",
       "« discard cards you control that the total resource cost of cards is at least 2. Take 1 damage for each card you discarded. Then, discard this card »",
       ["Puzzle.PutIntoPlay('01002', under_control=True)"] + deck("01105"), ["Puzzle.Reveal('hf608')", "Puzzle.EndPlayerTurn()"],
       {"hors_jeu": ["01002", "hf608"], "degats_identite": 1}),
    _c("hf608 Reponse forcee : DEUX cartes de cout 1 (2 ameliorations) pour atteindre 2 -> 2 degats",
       "« Take 1 damage for each card you discarded » : Armored Vest + Indomitable (cout 1 + 1)",
       [HEROS, "Puzzle.PutIntoPlay('01081', under_control=True)", "Puzzle.PutIntoPlay('01082', under_control=True)"] + deck("01105"),
       ["Puzzle.Reveal('hf608')", "Puzzle.EndPlayerTurn()"],
       {"hors_jeu": ["01081", "01082", "hf608"], "degats_identite": 2}),
    _c("hf608 « Otherwise » : le total controle (1) est INFERIEUR a 2 -> 1 carte rencontre face cachee, l'obligation RESTE en jeu, rien n'est defausse",
       "« Otherwise, deal yourself 1 facedown encounter card »", [HEROS, "Puzzle.PutIntoPlay('01081', under_control=True)"] + deck("01105"),
       ["Puzzle.Reveal('hf608')", "Puzzle.EndPlayerTurn()"], {"en_jeu": ["01081", "hf608"], "distribuees": 1, "degats_identite": 0}),
    _c("hf608 Peril : « Each encounter card you revealed gains peril » : un sbire revele par le joueur porte Peril 1",
       "`GiveKeywordToInPlayWhenApplyThis(EncounterCard, peril=1)` : l'obligation est en jeu", deck("01105"),
       ["Puzzle.Reveal('hf608')", "Puzzle.Reveal('01110')"], {"en_jeu": ["hf608", "01110"], "peril": [["01110", 1]]}),
    _c("hf608 Peril : TEMOIN, sans l'obligation le sbire revele n'a pas Peril",
       "contre-cas", deck("01105"), ["Puzzle.Reveal('01110')"], {"en_jeu": ["01110"], "peril": [["01110", 0]]}),
    # ===================================================================== hf610-hf612 Psychic Control
    _c("hf610 Reponse forcee : fin de tour -> Nova MANIGANCE contre le joueur (alter-ego : +2 menaces, +1 compteur par sa propre Reponse), l'identite est Desorientee, l'obligation est defaussee",
       "« After your turn ends, Cassandra Nova schemes. Confuse your identity, then, discard this card »",
       deck("01105"), ["Puzzle.Reveal('hf610')", "Puzzle.EndPlayerTurn()"],
       {"hors_jeu": ["hf610"], "statuts": [["01001b", "Confused"]], "compteurs_identite": [[CTR, 1]], "menace_de": [["hf604b", 3]]}),
    _c("hf610 Action d'alter-ego : incliner l'identite -> defausse l'obligation (sans fin de tour : rien d'autre ne bouge)",
       "« Alter-Ego Action : Exhaust your identity -> discard this card »", deck("01105"),
       ["Puzzle.Reveal('hf610')", "Puzzle.Action('hf610', 'AlterEgoAction')"],
       {"hors_jeu": ["hf610"], "exhausted": ["01001b"], "compteurs_identite": [[CTR, 0]], "menace_de": [["hf604b", 1]]}),
    _c("hf610 Action d'alter-ego : TEMOIN, sous forme HEROS l'action n'est pas offerte (l'obligation reste)",
       "« Alter-Ego Action » : alter-ego seulement", [HEROS] + deck("01105"), ["Puzzle.Reveal('hf610')"],
       {"en_jeu": ["hf610"]}, declencher_tolerant=["Puzzle.Action('hf610', 'AlterEgoAction')"]),
    _c("hf610 Boost 3 imprime (nombres texte <-> code) : l'obligation ajoute 3 icones a l'attaque de Nova (1 + 3 = 4 degats)",
       "icones de boost : `Boost` = 3", [HEROS, "Puzzle.Exhaust('01001a')"] + deck("hf610"), ["Puzzle.Attack('hf601')"], {"degats_identite": 4}),
    # ===================================================================== hf613-hf615 Shatter Your Mind
    _c("hf613 When Revealed : stade I -> 2 cartes defaussees ; chaque carte du set Cassandra Nova defaussee pose 1 compteur (2 cartes Nova = 2 compteurs)",
       "« Discard X cards ... where X is equal to double the villain's stage number. Each time a Cassandra Nova card is discarded this way, place 1 Cassandra Controls counter on your identity »",
       deck("hf608", "hf621", "hf608"), ["Puzzle.Reveal('hf613')"], {"compteurs_identite": [[CTR, 2]], "taille_defausse_rencontre": 3}),
    _c("hf613 When Revealed : TEMOIN, seule 1 des 2 cartes defaussees est de l'ensemble Cassandra Nova -> 1 compteur",
       "les cartes d'autres ensembles ne comptent pas", deck("01105", "hf608", "hf608"), ["Puzzle.Reveal('hf613')"],
       {"compteurs_identite": [[CTR, 1]], "taille_defausse_rencontre": 3}),
    _c("hf613 When Revealed : stade II -> 4 cartes defaussees (double du stade 2) ; 3 cartes Nova + le compteur du stade II revele = 4 -> Domination se declenche (3 retires)",
       "« double the villain's stage number » : le stade II (avance par la defaite du I) ; le compteur du When Revealed du stade II (1) + 3 = 4 compteurs : Cassandra Domination en retire 3",
       ["Puzzle.Damage('hf601', 15)"] + deck("hf608", "hf609", "hf621", "01105"), ["Puzzle.Reveal('hf613')"],
       {"compteurs_identite": [[CTR, 1]], "taille_defausse_rencontre": 5, "questions_presentes": [LIB_MENACE]}),
    _c("hf613 Boost 2 imprime : la carte ajoute 2 icones a l'attaque de Nova (1 + 2 = 3 degats)",
       "icones de boost : `Boost` = 2", [HEROS, "Puzzle.Exhaust('01001a')"] + deck("hf613"), ["Puzzle.Attack('hf601')"], {"degats_identite": 3}),
    # ===================================================================== hf616 / hf617 Psychic Combo
    _c("hf616 When Revealed (alter-ego) : Nova ACTIVE contre le joueur (complot : +2 menaces, +1 compteur) PUIS le joueur est Etourdi",
       "« Cassandra Nova activates against you. You are stunned. »", deck("01105", "01105"), ["Puzzle.Reveal('hf616')"],
       {"compteurs_identite": [[CTR, 1]], "statuts": [["01001b", "Stunned"]], "menace_de": [["hf604b", 3]]}),
    _c("hf616 When Revealed (heros) : Nova ATTAQUE le joueur : 1 compteur, joueur Etourdi",
       "« activates against you » : forme heros -> attaque", [HEROS] + deck("01105", "01105"), ["Puzzle.Reveal('hf616')"],
       {"compteurs_identite": [[CTR, 1]], "statuts": [["01001a", "Stunned"]]}),
    _c("hf616 Boost (attaque) : « this attack gains overkill » : Black Cat (2 PV) defend, 1 + 1 (icone) = 2... + boost : l'exces passe au heros (overkill)",
       "« If this activation is an attack, this attack gains overkill and piercing » : Cassandra Nova II (ATK 2) + 1 icone = 3 contre Black Cat (2 PV) : 1 degat d'exces au heros",
       [HEROS, "Puzzle.PutIntoPlay('01002', under_control=True)", "Puzzle.Damage('hf601', 15)"] + deck("hf616"), ["Puzzle.Attack('hf602', defender='01002')"],
       {"hors_jeu": ["01002"], "degats_identite": 1}),
    _c("hf616 Boost (attaque) : TEMOIN, meme attaque avec Psychic Leech en boost (1 icone, aucun effet) : Black Cat meurt, PAS d'exces",
       "contre-cas d'overkill", [HEROS, "Puzzle.PutIntoPlay('01002', under_control=True)", "Puzzle.Damage('hf601', 15)"] + deck("hf618"),
       ["Puzzle.Attack('hf602', defender='01002')"], {"hors_jeu": ["01002"], "degats_identite": 0}),
    _c("hf616 Boost (complot) : la carte pose autant de menaces que de compteurs sur l'identite (1) en plus des icones : 1 menace de plus que le temoin (compteurs maintenus sous 3 : pas de Domination)",
       "« Otherwise, place threat on the main scheme equals to the number of Cassandra Controls counter on your identity »",
       controles(1) + deck("hf616"), ["Puzzle.Scheme('hf601')"], {"menace_de": [["hf604b", 1 + 2 + 1 + 1]]}),
    _c("hf616 Boost (complot) : TEMOIN avec Psychic Leech (meme icone, aucun effet) : 1 + 2 + 1",
       "contre-cas", controles(1) + deck("hf618"), ["Puzzle.Scheme('hf601')"], {"menace_de": [["hf604b", 1 + 2 + 1]]}),
    _c("hf617 Psychic Combo (illustration 2) : meme effet",
       "les deux exemplaires portent le meme texte", deck("01105", "01105"), ["Puzzle.Reveal('hf617')"],
       {"compteurs_identite": [[CTR, 1]], "statuts": [["01001b", "Stunned"]]}),
    # ===================================================================== hf618 / hf619 Psychic Leech
    _c("hf618 When Revealed : la main (2 cartes) est defaussee puis repiochee ; Nova blessee (5 degats) : -1 degat par carte defaussee -> 3 ; aucun compteur",
       "« For each card you discard in this way, heal 1 damage from Cassandra Nova »", ["Puzzle.Damage('hf601', 5)"] + deck("01105"),
       ["Puzzle.Reveal('hf618')"], {"degats_de": [["hf601", 3]], "compteurs_identite": [[CTR, 0]]}, main_exclusive=["01089", "01090"]),
    _c("hf618 When Revealed : « if you cannot » : Nova SANS degat -> 1 compteur PAR carte defaussee (2)",
       "« if you cannot, place a Cassandra Controls counter on your identity »", deck("01105"), ["Puzzle.Reveal('hf618')"],
       {"degats_de": [["hf601", 0]], "compteurs_identite": [[CTR, 2]]}, main_exclusive=["01089", "01090"]),
    _c("hf618 When Revealed : MIXTE : Nova a 1 seul degat, 2 cartes defaussees -> 1 soin PUIS 1 compteur",
       "le « if you cannot » se juge carte par carte", ["Puzzle.Damage('hf601', 1)"] + deck("01105"), ["Puzzle.Reveal('hf618')"],
       {"degats_de": [["hf601", 0]], "compteurs_identite": [[CTR, 1]]}, main_exclusive=["01089", "01090"]),
    _c("hf618 When Revealed : main VIDE -> rien n'est defausse, rien ne se passe (Nova garde ses degats)",
       "« For each card you discard » : zero carte", ["Puzzle.Damage('hf601', 5)"] + deck("01105"), ["Puzzle.Reveal('hf618')"],
       {"degats_de": [["hf601", 5]], "compteurs_identite": [[CTR, 0]]}, main_exclusive=[]),
    _c("hf619 Psychic Leech (illustration 2) : meme effet",
       "les deux exemplaires portent le meme texte", ["Puzzle.Damage('hf601', 5)"] + deck("01105"), ["Puzzle.Reveal('hf619')"],
       {"degats_de": [["hf601", 3]]}, main_exclusive=["01089", "01090"]),
    # ===================================================================== hf620 Global Opinion Controls
    _c("hf620 When Revealed : 1 menace par compteur en jeu (2 compteurs) en plus de la menace de depart 2 -> 4",
       "« For each Cassandra Controls counter in play, place 1 threat here » ; menace de depart 2", controles(2) + deck("01105"), ["Puzzle.Reveal('hf620')"],
       {"menace_de": [["hf620", 4]]}),
    _c("hf620 When Revealed : TEMOIN, aucun compteur en jeu -> menace de depart seule (2)",
       "contre-cas", deck("01105"), ["Puzzle.Reveal('hf620')"], {"menace_de": [["hf620", 2]]}),
    _c("hf620 When Revealed : A DEUX JOUEURS, les compteurs de TOUTES les identites comptent (1 + 2 = 3) : 2 + 3 = 5",
       "« in play » : chaque identite", controles(1) + ["Puzzle.PlaceCounters('04001b', 'cassandra_controls', 2)"] + deck("01105"), ["Puzzle.Reveal('hf620')"],
       {"menace_de": [["hf620", 2 + 3]]}, heros2="hawkeye"),
    _c("hf620 Texte des soutiens VIDE : Med Team (soin 2 par Action) ne soigne plus tant que la manigance est en jeu",
       "« Treat each support's text box as if it were blank » : Action de Med Team non offerte", [HEROS, "Puzzle.Damage('01001a', 4)", "Puzzle.PutIntoPlay('01080', under_control=True)"] + deck("01105"),
       ["Puzzle.Reveal('hf620')"], {"degats_identite": 4}, declencher_tolerant=["Puzzle.Action('01080', 'Action')"]),
    _c("hf620 Texte des soutiens VIDE : TEMOIN, sans la manigance Med Team soigne (4 -> 2 degats)",
       "contre-cas", [HEROS, "Puzzle.Damage('01001a', 4)", "Puzzle.PutIntoPlay('01080', under_control=True)"] + deck("01105"), ["Puzzle.Action('01080', 'Action')"],
       {"degats_identite": 2}, cibles=["01001a"], accepter_choix=True),
    _c("hf620 Boost : 2 compteurs Cassandra Controls sur l'identite du joueur vise : 2 + 1 (Reponse de Nova) = 3 -> Cassandra Domination se declenche (0 restent)",
       "« [star] Boost : Place 2 Cassandra Controls counters on your identity card » ; la preuve est le declenchement de Domination (sans le boost : 1 seul compteur, aucune question)",
       [HEROS] + deck("hf620"), ["Puzzle.Attack('hf601')"],
       {"compteurs_identite": [[CTR, 0]], "questions_presentes": [LIB_MENACE]}),
    _c("hf620 Boost : TEMOIN, sans la carte en boost (boost sans effet) : 1 seul compteur et aucune question",
       "contre-cas du boost", [HEROS] + deck("hf618"), ["Puzzle.Attack('hf601')"],
       {"compteurs_identite": [[CTR, 1]], "questions_absentes": [LIB_MENACE]}),
    # ===================================================================== hf621 The Hate Machine
    _c("hf621 When Revealed : 1 menace par compteur en jeu (1) + menace de depart 2 = 3",
       "« For each Cassandra Controls counter in play, place 1 threat here »", controles(1) + deck("01105"), ["Puzzle.Reveal('hf621')"],
       {"menace_de": [["hf621", 3]]}),
    _c("hf621 « you cannot attack Cassandra Nova » : avec 1 compteur sur l'identite, l'attaque du heros contre Nova est impossible (aucun degat)",
       "« While at least 1 Cassandra Control counter on your identity, you cannot attack Cassandra Nova »", controles(1) + [HEROS] + deck("01105"),
       ["Puzzle.Reveal('hf621')"], {"degats_de": [["hf601", 0]]}, declencher_tolerant=["Puzzle.Attack('01001a')"], cibles=["hf601"]),
    _c("hf621 « you cannot attack Cassandra Nova » : TEMOIN, SANS compteur sur l'identite le heros blesse Nova (2 degats)",
       "la condition porte sur les compteurs de l'identite", [HEROS] + deck("01105"), ["Puzzle.Reveal('hf621')", "Puzzle.Attack('01001a')"],
       {"degats_de": [["hf601", 2]]}, cibles=["hf601"], accepter_choix=True),
    _c("hf621 « you cannot attack Cassandra Nova » : TEMOIN, un SBIRE peut etre attaque malgre le compteur (Hydra Bomber 2 PV vaincu)",
       "seule Cassandra Nova est protegee", controles(1) + [HEROS, "Puzzle.PutIntoPlay('01110')"] + deck("01105"), ["Puzzle.Reveal('hf621')", "Puzzle.Attack('01001a')"],
       {"hors_jeu": ["01110"]}, cibles=["01110"], accepter_choix=True),
    _c("hf621 « you cannot thwart the main scheme » : avec 1 compteur, le heros ne retire aucune menace du complot",
       "« or thwart the main scheme »", controles(1) + [HEROS, "Puzzle.SetThreat('hf604b', 4)"] + deck("01105"), ["Puzzle.Reveal('hf621')"],
       {"menace_de": [["hf604b", 4]]}, declencher_tolerant=["Puzzle.Thwart('01001a')"], cibles=["hf604b"]),
    _c("hf621 « you cannot thwart the main scheme » : TEMOIN, sans compteur le heros retire 1 menace (4 -> 3)",
       "contre-cas", [HEROS, "Puzzle.SetThreat('hf604b', 4)"] + deck("01105"), ["Puzzle.Reveal('hf621')", "Puzzle.Thwart('01001a')"],
       {"menace_de": [["hf604b", 3]]}, cibles=["hf604b"], accepter_choix=True),
    _c("hf621 « you cannot... » : TEMOIN, un ALLIE (Black Cat) peut encore contrer le complot malgre le compteur (4 -> 3)",
       "« you » = le heros, pas ses allies", controles(1) + [HEROS, "Puzzle.PutIntoPlay('01002', under_control=True)", "Puzzle.SetThreat('hf604b', 4)"] + deck("01105"),
       ["Puzzle.Reveal('hf621')", "Puzzle.Thwart('01002')"], {"menace_de": [["hf604b", 3]]}, cibles=["hf604b"], accepter_choix=True),
    _c("hf621 Boost : « Reveal this card » : la manigance annexe est revelee et entre en jeu",
       "« [star] Boost : Reveal this card »", [HEROS] + deck("hf621"), ["Puzzle.Attack('hf601')"], {"en_jeu": ["hf621"]}),

    # ===================================================================== module MIND CONTROL (hf371-hf376)
    _c("hf371 Psychic Aegis : mot-cle Setup -> en jeu des la mise en place, ATTACHEE au vilain (Cassandra Nova)",
       "« Setup. Attach to the villain. » (`desc.Setup`, `AttachToFaceWhenPutIntoPlay(Villain)`)", deck("01105"), [],
       {"en_jeu": ["hf371"], "hotes": [["hf371", "hf601"]]}),
    _c("hf371 « Attached character cannot be confused » : Cassandra Nova ne peut pas etre desorientee",
       "`UnitCannotBeConfused(\"AttachedCharacter\")`", deck("01105"), ["Puzzle.Confuse('hf601')"],
       {"statuts_absents": [["hf601", "Confused"]]}),
    _c("hf371 « cannot be confused » : TEMOIN, sans Psychic Aegis (retiree) Cassandra Nova peut etre desorientee",
       "contre-cas", ["Puzzle.Remove('hf371')"] + deck("01105"), ["Puzzle.Confuse('hf601')"],
       {"statuts": [["hf601", "Confused"]]}),
    _c("hf371 « cannot take damage from a player while that player is confused » : le heros DESORIENTE n'inflige aucun degat a Nova",
       "`PlayersCannotDamageUnit(\"AnyPlayer\", \"AttachedCharacter\")` + condition « that player is confused »", [HEROS, "Puzzle.Confuse('01001a')"] + deck("01105"),
       ["Puzzle.Attack('01001a')"], {"degats_de": [["hf601", 0]]}, cibles=["hf601"], accepter_choix=True),
    _c("hf371 « ... while that player is confused » : TEMOIN, le heros NON desoriente blesse Nova (2 degats)",
       "contre-cas", [HEROS] + deck("01105"), ["Puzzle.Attack('01001a')"], {"degats_de": [["hf601", 2]]}, cibles=["hf601"], accepter_choix=True),
    _c("hf371 Action : depenser [mental][mental] -> defausse Psychic Aegis",
       "« Action : Spend [mental][mental] resources -> discard this card » : deux Genius (01089 = B)", deck("01105"), ["Puzzle.Action('hf371', 'Action')"],
       {"absents": ["hf371"]}, main_exclusive=["01089", "01089"], payer_avec=["01089", "01089"], payer_tout=True, accepter_choix=True),
    _c("hf371 Boost : « Reveal this card » : revelee depuis le deck, elle s'attache au vilain",
       "« [star] Boost : Reveal this card » (la copie de depart est retiree pour laisser la place)", [HEROS, "Puzzle.Remove('hf371')"] + deck("hf371"),
       ["Puzzle.Attack('hf601')"], {"en_jeu": ["hf371"], "hotes": [["hf371", "hf601"]]}),
    _c("hf372 False Reality : s'attache au complot principal ; Interruption forcee : Jessica Jones (THW 2 : +1 par manigance annexe) contre 2 menaces -> les 2 sont EMPECHEES, le joueur est desoriente",
       "« prevent 2 of that threat from being removed. Then, confuse that player »", ["Puzzle.SetThreat('hf604b', 3)", "Puzzle.PutIntoPlay('01107')", "Puzzle.PutIntoPlay('01059', under_control=True)"] + deck("01105"),
       ["Puzzle.Reveal('hf372')", "Puzzle.Thwart('01059')"],
       {"hotes": [["hf372", "hf604b"]], "menace_de": [["hf604b", 3]], "statuts": [["01001b", "Confused"]]}, cibles=["hf604b"], accepter_choix=True),
    _c("hf372 Interruption forcee : TEMOIN, sans False Reality Jessica Jones retire ses 2 menaces (3 -> 1), personne n'est desoriente",
       "contre-cas", ["Puzzle.SetThreat('hf604b', 3)", "Puzzle.PutIntoPlay('01107')", "Puzzle.PutIntoPlay('01059', under_control=True)"] + deck("01105"), ["Puzzle.Thwart('01059')"],
       {"menace_de": [["hf604b", 1]], "statuts_absents": [["01001b", "Confused"]]}, cibles=["hf604b"], accepter_choix=True),
    _c("hf372 TEMOIN D'EPUISEMENT « Limit once per phase » : un SECOND retrait dans la meme phase n'est plus empeche (Black Cat 1 menace : 3 -> 2)",
       "deux retraits (Jessica Jones puis Black Cat) : le premier est empeche (3 reste 3), le second passe", ["Puzzle.SetThreat('hf604b', 3)", "Puzzle.PutIntoPlay('01107')", "Puzzle.PutIntoPlay('01059', under_control=True)", "Puzzle.PutIntoPlay('01002', under_control=True)"] + deck("01105"),
       ["Puzzle.Reveal('hf372')", "Puzzle.Thwart('01059')", "Puzzle.Thwart('01002')"], {"menace_de": [["hf604b", 2]]}, cibles=["hf604b"], accepter_choix=True),
    _c("hf372 Action de heros : depenser [mental][mental] -> defausse False Reality",
       "« Hero Action : Spend [mental][mental] resource -> discard this card »", [HEROS] + deck("01105"), ["Puzzle.Reveal('hf372')", "Puzzle.Action('hf372', 'HeroAction')"],
       {"absents": ["hf372"]}, main_exclusive=["01089", "01089"], payer_avec=["01089", "01089"], payer_tout=True, accepter_choix=True),
    _c("hf373 Mind Maze : s'attache a l'identite ; Interruption forcee : le contre du HEROS est REMPLACE : la carte est defaussee, aucune menace retiree, le joueur est desoriente",
       "« When you would thwart, discard this card instead. Then, you are confused »", [HEROS, "Puzzle.SetThreat('hf604b', 4)"] + deck("01105"),
       ["Puzzle.Reveal('hf373')", "Puzzle.Thwart('01001a')"],
       {"absents": ["hf373"], "menace_de": [["hf604b", 4]], "statuts": [["01001a", "Confused"]]}, cibles=["hf604b"], accepter_choix=True),
    _c("hf373 Mind Maze : s'attache bien a l'identite du joueur",
       "« Attach to your identity »", [HEROS] + deck("01105"), ["Puzzle.Reveal('hf373')"], {"hotes": [["hf373", "01001a"]]}),
    _c("hf373 Interruption forcee : TEMOIN, un ALLIE (Black Cat) contre normalement et la carte RESTE (« When YOU thwart » = l'identite)",
       "seul le contre de l'identite est remplace", [HEROS, "Puzzle.SetThreat('hf604b', 4)", "Puzzle.PutIntoPlay('01002', under_control=True)"] + deck("01105"),
       ["Puzzle.Reveal('hf373')", "Puzzle.Thwart('01002')"], {"en_jeu": ["hf373"], "menace_de": [["hf604b", 3]]}, cibles=["hf604b"], accepter_choix=True),
    _c("hf373 Action : depenser [mental][mental] -> defausse Mind Maze",
       "« Action : Spend [mental][mental] resources -> discard this card »", [HEROS] + deck("01105"), ["Puzzle.Reveal('hf373')", "Puzzle.Action('hf373', 'Action')"],
       {"absents": ["hf373"]}, main_exclusive=["01089", "01089"], payer_avec=["01089", "01089"], payer_tout=True, accepter_choix=True),
    _c("hf374 Illusory Attacks : l'identite est desorientee PUIS chaque personnage desoriente subit 1 degat (identite 1, allie Black Cat desoriente 1, sbire Hydra Bomber desoriente 1, allie non desoriente 0)",
       "« You are confused. Deal 1 damage to each confused character in play »",
       [HEROS, "Puzzle.PutIntoPlay('01002', under_control=True)", "Puzzle.PutIntoPlay('01059', under_control=True)", "Puzzle.PutIntoPlay('01110')", "Puzzle.Confuse('01002')", "Puzzle.Confuse('01110')"] + deck("01105"),
       ["Puzzle.Reveal('hf374')"], {"degats_identite": 1, "degats": [["01002", 1], ["01110", 1], ["01059", 0]], "statuts": [["01001a", "Confused"]]}),
    _c("hf374 Boost : « You are confused » : le joueur vise par l'attaque est desoriente",
       "« [star] Boost : You are confused »", [HEROS] + deck("hf374"), ["Puzzle.Attack('hf601')"], {"statuts": [["01001a", "Confused"]]}),
    _c("hf375 Illusory Attacks (illustration 2) : meme effet",
       "les deux exemplaires portent le meme texte", [HEROS] + deck("01105"), ["Puzzle.Reveal('hf375')"], {"degats_identite": 1, "statuts": [["01001a", "Confused"]]}),
    _c("hf376 Mind Shatter : Peril 1 imprime, desoriente, main de 4 cartes SANS defausse volontaire -> X = moitie arrondie au superieur = 2 degats a l'identite",
       "« deal X damage to each identity in play, where X is equal to half of the number of cards from your hand » (QUESTIONS.md n°2)", [HEROS] + deck("01105"),
       ["Puzzle.Reveal('hf376')"], {"degats_identite": 2, "statuts": [["01001a", "Confused"]]}, main_exclusive=["01089", "01090", "01089", "01090"]),
    _c("hf376 Mind Shatter : main de 3 cartes -> X = 2 (moitie de 3 arrondie au superieur)",
       "arrondi au superieur", [HEROS] + deck("01105"), ["Puzzle.Reveal('hf376')"], {"degats_identite": 2}, main_exclusive=["01089", "01090", "01089"]),
    _c("hf376 Mind Shatter : main VIDE -> X = 0, aucun degat",
       "moitie de 0", [HEROS] + deck("01105"), ["Puzzle.Reveal('hf376')"], {"degats_identite": 0}, main_exclusive=[]),
    _c("hf376 Mind Shatter : A DEUX JOUEURS, chaque identite subit X (main de 2 : X = 1 pour chacun)",
       "« to each identity in play »", [HEROS] + deck("01105"), ["Puzzle.Reveal('hf376')"], {"degats_joueurs": [1, 1]}, main_exclusive=["01089", "01090"], heros2="spider_man"),
    # ===================================================================== module MUTANT EXTINCTION AGENDA (hf381-hf388)
    _c("hf381 Mutant Extinction Agenda : When Revealed : le joueur cherche une SENTINEL (Wild Sentinel) et la met en jeu ENGAGEE ; menace de depart 2[per_hero] ; la SENTINEL gagne +1 ATK et +1 SCH (3 et 2)",
       "« Each SENTINEL minion gets +1 ATK and +1 SCH » ; Wild Sentinel imprime ATK 2, SCH 1, PV 4", deck("hf382", "01105"), ["Puzzle.Reveal('hf381')"],
       {"en_jeu": ["hf381", "hf382"], "menace_de": [["hf381", 2]], "attaque": [["hf382", 3]], "schema": [["hf382", 2]], "vie": [["hf382", 4]]}),
    _c("hf381 Mutant Extinction Agenda : TEMOIN, un sbire qui n'est PAS une SENTINEL (Hydra Bomber) ne recoit pas le bonus (ATK 1, SCH 1)",
       "le bonus ne vise que le trait SENTINEL", ["Puzzle.PutIntoPlay('01110')"] + deck("hf382", "01105"), ["Puzzle.Reveal('hf381')"],
       {"attaque": [["01110", 1]], "schema": [["01110", 1]]}),
    _c("hf381 « cannot be defeated while a SENTINEL minion is in play » : la menace tombe a 0 mais la manigance RESTE en jeu",
       "`SchemeCannotLeavlPlayWhile` : defaite remplacee tant qu'une SENTINEL est en jeu", [HEROS, "Puzzle.PutIntoPlay('hf382')", "Puzzle.PutIntoPlay('hf381')", "Puzzle.SetThreat('hf381', 1)"] + deck("01105"),
       ["Puzzle.Thwart('01001a')"], {"en_jeu": ["hf381", "hf382"], "menace_de": [["hf381", 0]]}, cibles=["hf381"], accepter_choix=True),
    _c("hf381 « cannot be defeated while... » : TEMOIN, SANS SENTINEL en jeu la manigance est vaincue a 0 menace (pile de victoire : Victory 1)",
       "contre-cas ; Victory 1 natif", [HEROS, "Puzzle.PutIntoPlay('hf381')", "Puzzle.SetThreat('hf381', 1)"] + deck("01105"), ["Puzzle.Thwart('01001a')"],
       {"hors_jeu": ["hf381"], "en_victoire": ["hf381"]}, cibles=["hf381"], accepter_choix=True),
    _c("hf381 Boost : « Put this card into play » : la manigance entre en jeu (sans When Revealed : aucune SENTINEL cherchee)",
       "« [star] Boost : Put this card into play »", [HEROS] + deck("hf381", "hf382"), ["Puzzle.Attack('hf601')"], {"en_jeu": ["hf381"], "hors_jeu": ["hf382"]}),
    _c("hf382 Wild Sentinel : valeurs imprimees (PV 4, ATK 2, SCH 1), trait SENTINEL",
       "nombres texte <-> code (scan)", ["Puzzle.PutIntoPlay('hf382')"] + deck("01105"), [],
       {"en_jeu": ["hf382"], "vie": [["hf382", 4]], "attaque": [["hf382", 2]], "schema": [["hf382", 1]], "trait_de": [["hf382", "SENTINEL", True]]}),
    _c("hf382 When Defeated : le joueur qui la vainc choisit « subir 2 degats » -> 2 degats a l'identite ; la carte va a la DEFAUSSE de rencontre",
       "« The defeating player chooses to either take 2 damage or place this card on the bottom of the encounter deck instead of the discard pile »",
       [HEROS, "Puzzle.PutIntoPlay('hf382')", "Puzzle.Damage('hf382', 2)"] + deck("01105"), ["Puzzle.Attack('01001a')"],
       {"hors_jeu": ["hf382"], "degats_identite": 2, "defausse_rencontre": ["hf382"]}, cibles=["hf382"], accepter_choix=True, choisir_option="Take_2_damage"),
    _c("hf382 When Defeated : l'AUTRE branche -> la carte va SOUS le deck de rencontre (pas dans la defausse), aucun degat",
       "« place this card on the bottom of the encounter deck instead of the discard pile »",
       [HEROS, "Puzzle.PutIntoPlay('hf382')", "Puzzle.Damage('hf382', 2)"] + deck("01105"), ["Puzzle.Attack('01001a')"],
       {"hors_jeu": ["hf382"], "degats_identite": 0, "absent_defausse_rencontre": ["hf382"], "dessous_du_deck": "hf382"}, cibles=["hf382"], accepter_choix=True,
       choisir_option="Place_this_card_on_the_bottom_of_the_encounter_deck_instead_of_the_discard_pile"),
    _c("hf382 When Defeated : TEMOIN, vaincue par un EFFET sans joueur (degats directs) -> aucune question, defausse normale",
       "« The defeating player » : pas de joueur vainqueur, pas de choix", ["Puzzle.PutIntoPlay('hf382')"] + deck("01105"), ["Puzzle.Damage('hf382', 4)"],
       {"hors_jeu": ["hf382"], "degats_identite": 0, "defausse_rencontre": ["hf382"], "questions_absentes": ["Take 2 damage"]}),
    _c("hf383 Wild Sentinel (illustration 2) : meme effet (choix 2 degats)",
       "les quatre exemplaires portent le meme texte", [HEROS, "Puzzle.PutIntoPlay('hf383')", "Puzzle.Damage('hf383', 2)"] + deck("01105"), ["Puzzle.Attack('01001a')"],
       {"hors_jeu": ["hf383"], "degats_identite": 2}, cibles=["hf383"], accepter_choix=True, choisir_option="Take_2_damage"),
    _c("hf384 Wild Sentinel (illustration 3) : meme effet (choix 2 degats)",
       "idem", [HEROS, "Puzzle.PutIntoPlay('hf384')", "Puzzle.Damage('hf384', 2)"] + deck("01105"), ["Puzzle.Attack('01001a')"],
       {"hors_jeu": ["hf384"], "degats_identite": 2}, cibles=["hf384"], accepter_choix=True, choisir_option="Take_2_damage"),
    _c("hf385 Wild Sentinel (illustration 4) : meme effet (choix 2 degats)",
       "idem", [HEROS, "Puzzle.PutIntoPlay('hf385')", "Puzzle.Damage('hf385', 2)"] + deck("01105"), ["Puzzle.Attack('01001a')"],
       {"hors_jeu": ["hf385"], "degats_identite": 2}, cibles=["hf385"], accepter_choix=True, choisir_option="Take_2_damage"),
    _c("hf386 E for Extinction : DEUX SENTINEL en jeu -> 2 degats indirects a chaque joueur (l'identite les prend)",
       "« For each SENTINEL minion in play, deal 1 indirect damage to each player »", [HEROS, "Puzzle.PutIntoPlay('hf382')", "Puzzle.PutIntoPlay('hf383')"] + deck("01105"),
       ["Puzzle.Reveal('hf386')"], {"degats_identite": 2}),
    _c("hf386 E for Extinction : AUCUNE SENTINEL en jeu -> le joueur en cherche une dans le deck et la met en jeu engagee ; aucun degat",
       "« If there is no SENTINEL minion in play, search the encounter deck and discard pile ... and put it into play engaged with you »", [HEROS] + deck("hf382", "01105"),
       ["Puzzle.Reveal('hf386')"], {"en_jeu": ["hf382"], "degats_identite": 0}),
    _c("hf387 E for Extinction (illustration 2) : meme effet (2 SENTINEL -> 2 degats)",
       "les deux exemplaires portent le meme texte", [HEROS, "Puzzle.PutIntoPlay('hf382')", "Puzzle.PutIntoPlay('hf383')"] + deck("01105"), ["Puzzle.Reveal('hf387')"],
       {"degats_identite": 2}),
    _c("hf388 Worldwide Sentinel Deployment : A DEUX JOUEURS, chacun cherche une SENTINEL (2 en jeu) ; menace de depart 3[per_hero] = 6 ; icone Hazard 1",
       "« Each player search ... in player order. Put it into play engaged with you » ; valeurs imprimees (menace 3 par joueur, Hazard 1)", deck("hf382", "hf383", "01105"),
       ["Puzzle.Reveal('hf388')"], {"en_jeu": ["hf388", "hf382", "hf383"], "menace_de": [["hf388", 6]], "hazard": [["hf388", 1]]}, heros2="spider_man"),
    _c("hf381 « cannot be defeated while... » : la DERNIERE SENTINEL part alors que la manigance est a 0 menace -> la manigance est vaincue et rejoint la pile de victoire",
       "etat coince evite : sans cette verification la carte resterait a 0 menace, impossible a contrer",
       [HEROS, "Puzzle.PutIntoPlay('hf382')", "Puzzle.PutIntoPlay('hf381')", "Puzzle.SetThreat('hf381', 0)"] + deck("01105"), ["Puzzle.Damage('hf382', 4)"],
       {"hors_jeu": ["hf381", "hf382"], "en_victoire": ["hf381"]}),
    _c("hf381 : TEMOIN, la SENTINEL part mais la manigance a encore 1 menace -> elle reste en jeu",
       "contre-cas : seule une manigance a 0 menace est vaincue", [HEROS, "Puzzle.PutIntoPlay('hf382')", "Puzzle.PutIntoPlay('hf381')"] + deck("01105"), ["Puzzle.Damage('hf382', 4)"],
       {"en_jeu": ["hf381"], "hors_jeu": ["hf382"]}),
    _c("hf616 Boost (attaque) : « piercing » : Black Cat TENACE (carte Tenace) est blessee quand meme (la carte Tenace est defaussee d'abord) : 1 + 1 icone = ...",
       "« this attack gains overkill and piercing » (Perçant : defausse TOUTES les cartes Tenace de la cible avant les degats)",
       [HEROS, "Puzzle.PutIntoPlay('01002', under_control=True)", "Puzzle.Tough('01002')", "Puzzle.Damage('hf601', 15)"] + deck("hf616"),
       ["Puzzle.Attack('hf602', defender='01002')"], {"hors_jeu": ["01002"], "statuts_absents": [["01001a", "Stunned"]]}),
    _c("hf616 Boost (attaque) : TEMOIN de piercing : meme attaque avec Psychic Leech en boost -> la carte Tenace absorbe les degats, Black Cat survit (Tenace defaussee)",
       "contre-cas", [HEROS, "Puzzle.PutIntoPlay('01002', under_control=True)", "Puzzle.Tough('01002')", "Puzzle.Damage('hf601', 15)"] + deck("hf618"),
       ["Puzzle.Attack('hf602', defender='01002')"], {"en_jeu": ["01002"], "degats": [["01002", 0]], "statuts_absents": [["01002", "Tough"]]}),
    _c("hf609 Exploding Their Head (illustration 2) : meme effet (Black Cat defaussee, 1 degat, obligation defaussee)",
       "les deux exemplaires portent le meme texte", ["Puzzle.PutIntoPlay('01002', under_control=True)"] + deck("01105"), ["Puzzle.Reveal('hf609')", "Puzzle.EndPlayerTurn()"],
       {"hors_jeu": ["01002", "hf609"], "degats_identite": 1}),
    _c("hf611 Psychic Control (illustration 2) : meme effet (Nova manigance, desorientee, obligation defaussee)",
       "les trois exemplaires portent le meme texte", deck("01105"), ["Puzzle.Reveal('hf611')", "Puzzle.EndPlayerTurn()"],
       {"hors_jeu": ["hf611"], "statuts": [["01001b", "Confused"]], "compteurs_identite": [[CTR, 1]]}),
    _c("hf612 Psychic Control (illustration 3) : meme effet",
       "idem", deck("01105"), ["Puzzle.Reveal('hf612')", "Puzzle.EndPlayerTurn()"],
       {"hors_jeu": ["hf612"], "statuts": [["01001b", "Confused"]], "compteurs_identite": [[CTR, 1]]}),
    _c("hf614 Shatter Your Mind (illustration 2) : meme effet (2 cartes Nova defaussees = 2 compteurs)",
       "les trois exemplaires portent le meme texte", deck("hf608", "hf621", "hf608"), ["Puzzle.Reveal('hf614')"],
       {"compteurs_identite": [[CTR, 2]]}),
    _c("hf615 Shatter Your Mind (illustration 3) : meme effet",
       "idem", deck("hf608", "hf621", "hf608"), ["Puzzle.Reveal('hf615')"], {"compteurs_identite": [[CTR, 2]]}),
    _c("hf371 Psychic Aegis : RESTE attachee au vilain quand le stade I est vaincu (elle passe sur Cassandra Nova II)",
       "un attachement au vilain suit le vilain d'un stade a l'autre", deck("01105"), ["Puzzle.Damage('hf601', 15)"],
       {"en_jeu": ["hf602", "hf371"], "hotes": [["hf371", "hf602"]]}),
    _c("hf604a mise en place A DEUX JOUEURS : PV de Nova 30 (15 par joueur), menace de depart 2 (1 par joueur), cible 14, 2 identites",
       "valeurs « par joueur » (`15*`, `1*`) a deux joueurs", deck("01105"), [],
       {"en_jeu": ["hf601", "hf604b", "hf607"], "vie": [["hf601", 30]], "menace_de": [["hf604b", 2]]}, heros2="spider_man"),
    _c("hf602 VICTOIRE (standard) : le stade II vaincu est le DERNIER stade du vilain -> les joueurs GAGNENT la partie (victoire de campagne)",
       "livret p.16 : « Cassandra Nova is defeated, the players win the campaign ! »", deck("01105"), ["Puzzle.Damage('hf601', 15)", "Puzzle.Damage('hf602', 18)"],
       {"gagnee": True, "partie_finie": True}),
    _c("hf603 VICTOIRE (expert) : le stade III vaincu -> les joueurs GAGNENT la partie",
       "mode expert : Nova II puis Nova III", deck("01105"), ["Puzzle.Damage('hf602', 18)", "Puzzle.Damage('hf603', 20)"],
       {"gagnee": True, "partie_finie": True}, scenario=SCX),
    _c("hf602 TEMOIN de victoire : le stade I vaincu ne gagne PAS la partie (le stade II prend la suite)",
       "contre-cas", deck("01105"), ["Puzzle.Damage('hf601', 15)"], {"partie_finie": False, "en_jeu": ["hf602"]}),
]

VERIFICATIONS = r'''
def hfn_etat(monde, aides):
    attendu = aides["cas"].get("attendu") or {}
    propres = ("degats_de", "taille_defausse_rencontre", "menace_de", "attaque", "vie", "trait_de", "compteurs_sur", "absents", "nb_en_jeu", "hors_deck_rencontre", "steady", "stalwart",
               "acceleration", "controles_joueurs", "schema", "en_victoire", "peril", "degats_joueurs", "dessous_du_deck", "hazard", "absent_defausse_rencontre", "partie_finie", "gagnee", "distribuees")
    reste = {k: v for k, v in attendu.items() if k not in propres}
    copie = dict(aides); copie["cas"] = dict(aides["cas"]); copie["cas"]["attendu"] = reste
    ok, msg = etat_attendu(monde, copie)
    soucis = [] if ok else [msg]
    # GARDE-FOU (01/11/2026) : une cle `attendu` que personne ne lit est IGNOREE EN SILENCE (c'est arrive a `degats_de`, decouvert par la preuve par substitution).
    connues = set(globals().get("CLES_ETAT_ATTENDU", set())) | set(propres)
    inconnues = sorted(set(attendu) - connues)
    if inconnues:
        soucis.append(f"cle(s) attendu INCONNUE(S) de hfn_etat : {inconnues}")
    par_id = aides["par_id"]
    def face(cid):
        f = par_id(monde, cid)
        if f is None:
            soucis.append(f"{cid} n'est pas en jeu")
        return f
    for cid, n in attendu.get("degats_de", []):
        f = face(cid)
        if f is not None and (f.max_health - f.health) != n:
            soucis.append(f"{cid} degats = {f.max_health - f.health} (attendu {n})")
    for cid, n in attendu.get("menace_de", []):
        f = face(cid)
        if f is not None and f.threat != n:
            soucis.append(f"{cid} menace = {f.threat} (attendu {n})")
    for cid, n in attendu.get("attaque", []):
        f = face(cid)
        if f is not None and f.attack != n:
            soucis.append(f"{cid} ATK = {f.attack} (attendu {n})")
    for cid, n in attendu.get("vie", []):
        f = face(cid)
        if f is not None and f.max_health != n:
            soucis.append(f"{cid} PV max = {f.max_health} (attendu {n})")
    for cid, tr, b in attendu.get("trait_de", []):
        f = face(cid)
        if f is not None and bool(f.HasTrait(tr)) != b:
            soucis.append(f"{cid} trait {tr} = {f.HasTrait(tr)} (attendu {b})")
    for cid in attendu.get("absents", []):
        if par_id(monde, cid) is not None:
            soucis.append(f"{cid} est encore en jeu")
    for cid in attendu.get("steady", []):
        f = face(cid)
        if f is not None and not f.IsSteady():
            soucis.append(f"{cid} n'est pas Steady")
    for cid in attendu.get("stalwart", []):
        f = face(cid)
        if f is not None and f.GetKeyword('Stalwart') < 1:
            soucis.append(f"{cid} n'est pas Stalwart")
    for cid, n in attendu.get("acceleration", []):
        f = face(cid)
        if f is not None and f.acceleration_token != n:
            soucis.append(f"{cid} jetons d'acceleration = {f.acceleration_token} (attendu {n})")
    if "controles_joueurs" in attendu:
        vus = [j.GetIdentity().GetCounters('cassandra_controls') for j in monde.players]
        if vus != attendu["controles_joueurs"]:
            soucis.append(f"compteurs par joueur = {vus} (attendu {attendu['controles_joueurs']})")
    for cid, n in attendu.get("schema", []):
        f = face(cid)
        if f is not None and f.scheme != n:
            soucis.append(f"{cid} SCH = {f.scheme} (attendu {n})")
    for cid in attendu.get("en_victoire", []):
        trouve = False
        for objet in monde.object_manager.card_dict.values():
            f = getattr(objet, "face", None) or objet
            if getattr(getattr(f, "paper", None), "card_id", None) == cid and f.card.area.flags.is_victory_display:
                trouve = True
        if not trouve:
            soucis.append(f"{cid} n'est pas dans la pile de victoire")
    for cid, n in attendu.get("peril", []):
        f = face(cid)
        if f is not None and f.GetKeyword('Peril') != n:
            soucis.append(f"{cid} Peril = {f.GetKeyword('Peril')} (attendu {n})")
    for cid, n in attendu.get("hazard", []):
        f = face(cid)
        if f is not None and f.GetKeyword('Hazard') != n:
            soucis.append(f"{cid} Hazard = {f.GetKeyword('Hazard')} (attendu {n})")
    if "degats_joueurs" in attendu:
        vus = [j.GetIdentity().max_health - j.GetIdentity().health for j in monde.players]
        if vus != attendu["degats_joueurs"]:
            soucis.append(f"degats des identites = {vus} (attendu {attendu['degats_joueurs']})")
    if "dessous_du_deck" in attendu:
        from game.operate.worlds import Worlds
        deck = Worlds.GetEncounterDeckCards(monde)
        bas = getattr(deck[-1].paper, "card_id", None) if deck else None
        # le deck liste le DESSUS en premier : le dessous est le dernier element ; on accepte aussi le premier si l'ordre est inverse
        if attendu["dessous_du_deck"] not in (bas,):
            soucis.append(f"dessous du deck de rencontre = {bas} (attendu {attendu['dessous_du_deck']})")
    for cid in attendu.get("absent_defausse_rencontre", []):
        from game.operate.worlds import Worlds
        if cid in [getattr(f.paper, "card_id", None) for f in Worlds.GetEncounterDiscardPileCards(monde)]:
            soucis.append(f"{cid} est dans la defausse de rencontre (il devait en etre absent)")
    if "taille_defausse_rencontre" in attendu:
        from game.operate.worlds import Worlds
        n = len(Worlds.GetEncounterDiscardPileCards(monde))
        if n != attendu["taille_defausse_rencontre"]:
            soucis.append(f"defausse de rencontre = {n} carte(s) (attendu {attendu['taille_defausse_rencontre']})")
    if "partie_finie" in attendu and bool(getattr(monde, "is_game_over", False)) != attendu["partie_finie"]:
        soucis.append(f"partie finie = {getattr(monde, 'is_game_over', False)} (attendu {attendu['partie_finie']})")
    if "gagnee" in attendu:
        fini = bool(getattr(monde, "is_game_over", False))
        gagne = fini and bool(monde.game_over.players_won)
        if gagne != attendu["gagnee"]:
            soucis.append(f"partie gagnee = {gagne} (attendu {attendu['gagnee']})")
    if "distribuees" in attendu:
        n = len(list(monde.players[0].dealt_encounter_cards.Get(True)))
        if n != attendu["distribuees"]:
            soucis.append(f"cartes rencontre distribuees = {n} (attendu {attendu['distribuees']})")
    if attendu.get("hors_deck_rencontre"):
        from game.operate.worlds import Worlds
        ids = {getattr(f.paper, "card_id", None) for f in Worlds.GetEncounterDeckCards(monde)}
        for cid in attendu["hors_deck_rencontre"]:
            if cid in ids:
                soucis.append(f"{cid} est dans le deck de rencontre (il devait en etre retire)")
    for cid, nom, n in attendu.get("compteurs_sur", []):
        f = face(cid)
        if f is not None and f.GetCounters(nom) != n:
            soucis.append(f"{cid} compteurs {nom} = {f.GetCounters(nom)} (attendu {n})")
    # FILET (26/10/2026) : le moteur AVALE les exceptions des scripts de cartes ; un cas ne passe jamais au vert si le journal contient un Traceback.
    try:
        import os as _os
        _journal = open(f"/tmp/capacites_{_os.environ.get('CAS_PREFIX', '')}{aides['index']}.log", encoding="utf-8", errors="replace").read()
        if any("Traceback" in l for l in _journal.splitlines()):
            soucis.append("le journal contient une exception avalee par le moteur (Traceback)")
    except Exception:
        pass
    if soucis:
        return False, " ; ".join(soucis)
    return True, "etat conforme"
'''
