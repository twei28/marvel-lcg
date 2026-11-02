# Cas test_capacites du scenario 4 « TORN » de la campagne Hellfire Hunt (Dipsome), prefixe `hf`, plus les modules Negasonic Teenage Warhead (hf341-hf348)
# et Immensity (hf351-hf358) : noms prefixes « [hf] » puis le card_id (hf5xx, hf34x, hf35x). Verificateur dedie : `hft_etat`.
#
# Rappels de montage (voir aussi tools/cas/hellfire_white_queen.py, memes pieges) :
#  - `spider_man` demarre en ALTER-EGO : `Puzzle.ChangeForm('01001a')` le passe en HEROS (le vilain ATTAQUE un heros, MANIGANCE contre un alter ego) ;
#  - le scenario monte : Emma Frost A1 (hf501a), complot The Hellfire Club's Revenge (hf503a puis 1B hf503b), Nova's Psychic Puppetry (hf504a, face CONTROLLED),
#    le deck Hellfire (hf301 hf302 hf331 hf341 hf351 : sbires ELITE HELLFIRE de Perfection, Shaw, Negasonic et Immensity) dont un est DEJA REVELE (engage) par le Forced Interrupt de 1B a la 1re phase des joueurs ;
#  - `Puzzle.BeginVillainPhase()` fait activer le vilain, avec UNE carte de boost avant son attaque ou son complot ;
#  - 01105 = « Bomb Scare » (aucune capacite de boost), remplissage inoffensif.
SC = "hellfire_torn"
SCX = "hellfire_torn_expert"
HEROS = "Puzzle.ChangeForm('01001a')"   # spider_man demarre en ALTER-EGO
REMPLI = "'01105'"


def deck(*cartes, remplissage=6):
    """Deck de rencontre de test, les cartes voulues listees DU DESSUS vers le dessous, puis du remplissage inoffensif.
    ⚠ `Puzzle.CreateEncounterDeck(a, b, c)` pose `a` en DERNIER : la derniere carte creee est le DESSUS du deck ; on inverse donc la liste."""
    ids = list(cartes) + ["01105"] * remplissage
    return ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck(%s)" % ", ".join("'%s'" % c for c in reversed(ids))]


def _c(nom, pourquoi, mise, declencher, attendu, **cle):
    # ⚠ Le complot 1B fait reveler un sbire du Hellfire deck des le DEBUT de la 1re phase des joueurs : au depart d'un cas, un sbire ELITE HELLFIRE est deja
    # engage avec le joueur. `libre=True` le garde (cas de mise en place) ; sinon il est retire pour ne pas fausser les mesures.
    libre = cle.pop("libre", False)
    cas = {"nom": "[hf] " + nom, "pourquoi": pourquoi, "scenario": cle.pop("scenario", SC),
           "heros": cle.pop("heros", "spider_man"),
           "mise_en_place": ["Puzzle.EmptyHand()"] + ([] if libre else ["Puzzle.RemoveMinionsInPlay()"]) + list(mise), "declencher": declencher,
           "verifier": cle.pop("verifier", "hft_etat"), "attendu": attendu}
    cas.update(cle)
    cas.setdefault("main_exclusive", ["01090"])
    return cas


CAS = [
    # ===================================================================== le scenario se monte
    _c("hf503a mise en place : Emma Frost A1 en jeu (PV 7), complot 1B, Nova's Psychic Puppetry (face A) a 13 menaces, deck Hellfire de 4 sbires ELITE",
       "le scenario `hellfire_torn` se charge ; le Setup du complot 1A cree le Hellfire deck (hf301 hf302 hf331 hf341 hf351) et met Puppetry en jeu (8 + Hinder 5 = 13)",
       deck("01105"), [],
       {"en_jeu": ["hf501a", "hf503b", "hf504a"], "vie": [["hf501a", 7]], "attaque": [["hf501a", 1]], "menace_de": [["hf504a", 13]],
        "hellfire_total": ["hf301", "hf302", "hf331", "hf341", "hf351"], "hellfire_defausse": [],
        "trait_de": [["hf501a", "PSIONIC", True], ["hf501a", "HELLFIRE", True], ["hf504a", "CONTROLLED", True]]}, libre=True),
    # ===================================================================== Emma Frost, face A1 / A2 (standard)
    _c("hf501a Reponse forcee : apres son complot, defausse 1 carte (PSIONIC : Astral Trap) -> +1 menace sur CHAQUE manigance (principale ET annexe)",
       "« After Emma Frost activates, discard 1 card from the top of the encounter deck, if it has the PSIONIC trait, place 1 threat on each scheme » : alter-ego, Emma MANIGANCE (SCH 2 : 1 + 2 = 3 sur la principale) puis +1 (4) ; Puppetry 13 -> 14",
       deck("01105", "hf303", "01105"), ["Puzzle.Activate('hf501a')"],
       {"menace_de": [["hf503b", 4], ["hf504a", 14]], "defausse_rencontre_ids": ["01105", "hf303"]}),
    _c("hf501a Reponse forcee : TEMOIN, la carte defaussee n'est pas PSIONIC (Bomb Scare) -> aucune menace de plus (principale 3, Puppetry 13)",
       "contre-cas du trait PSIONIC",
       deck("01105", "01105", "01105"), ["Puzzle.Activate('hf501a')"],
       {"menace_de": [["hf503b", 3], ["hf504a", 13]]}),
    _c("hf501a Interruption forcee : serait vaincue (7 degats) -> elle se RETOURNE (hf501b, PV infinis), 5 menaces partent de CHAQUE manigance, la partie continue",
       "« When Emma Frost would be defeated, remove 5 threat from each scheme in play, and flip this card instead » : principale 8 -> 3, Puppetry 13 -> 8 ; aucune defaite, aucune victoire",
       ["Puzzle.PlaceThreat('hf503b', 7)"] + deck("01105"), ["Puzzle.Damage('hf501a', 7)"],
       {"en_jeu": ["hf501b", "hf504a"], "absents": ["hf501a"], "menace_de": [["hf503b", 3], ["hf504a", 8]], "partie_finie": False}),
    _c("hf501a Interruption forcee : TEMOIN, 6 degats (< 7 PV) -> aucun retournement, aucune menace retiree",
       "contre-cas : seule la defaite declenche",
       ["Puzzle.PlaceThreat('hf503b', 7)"] + deck("01105"), ["Puzzle.Damage('hf501a', 6)"],
       {"en_jeu": ["hf501a"], "absents": ["hf501b"], "menace_de": [["hf503b", 8], ["hf504a", 13]], "degats_de": [["hf501a", 6]]}),
    _c("hf501b PV infinis : 100 degats ne la vainquent pas",
       "« HIT POINTS INF » (`desc.HP = INF`, can_health.py) : aucune defaite, aucune victoire",
       ["Puzzle.Flip('hf501a')"] + deck("01105"), ["Puzzle.Damage('hf501b', 100)"],
       {"en_jeu": ["hf501b"], "partie_finie": False}),
    _c("hf501b Interruption forcee : quand elle activerait, defausse 2 cartes du dessus du deck de rencontre A LA PLACE (aucune manigance : le complot reste a 1)",
       "« When Emma Frost would activate, discard 2 cards from the top of the encounter deck instead » : pas de carte de boost, pas de complot",
       ["Puzzle.Flip('hf501a')"] + deck("01105", "01090"), ["Puzzle.Activate('hf501b')"],
       {"defausse_rencontre_ids": ["01090", "01105"], "menace_de": [["hf503b", 1]]}),
    _c("hf501b Reponse forcee : apres la fin de la phase du vilain, elle se retourne (hf501a) et ses PV sont remis a leurs PV imprimes (20 degats pris sur la face infinie : 0)",
       "« After the end of the villain phase, flip this card, then set Emma Frost's hit point dial to her printed hit points » : `OnFlip` depuis une face a PV infinis",
       ["Puzzle.Flip('hf501a')", "Puzzle.Damage('hf501b', 20)"] + deck("01105"), ["Puzzle.EndVillainPhase()"],
       {"en_jeu": ["hf501a"], "absents": ["hf501b"], "degats_de": [["hf501a", 0]], "vie": [["hf501a", 7]]}),
    _c("hf501b Reponse forcee : le CYCLE complet (serait vaincue -> face infinie -> fin de la phase du vilain) : elle revient avec 7 PV pleins, 0 degat",
       "les deux faces ensemble : les 7 degats de la defaite sont gommes au retour",
       deck("01105"), ["Puzzle.Damage('hf501a', 7)", "Puzzle.EndVillainPhase()"],
       {"en_jeu": ["hf501a"], "absents": ["hf501b"], "degats_de": [["hf501a", 0]]}),
    _c("hf501b Reponse forcee : TEMOIN, la fin de la phase des JOUEURS ne la retourne pas",
       "« After the end of the VILLAIN phase » : pas l'autre phase",
       ["Puzzle.Flip('hf501a')"] + deck("01105"), ["Puzzle.EndPlayerPhase()"],
       {"en_jeu": ["hf501b"], "absents": ["hf501a"]}),
    # ===================================================================== Emma Frost, face B1 / B2 (expert)
    _c("hf502a mise en place EXPERT : Emma Frost B1 en jeu (PV 8, ATK 2, SCH 2), meme complot, Puppetry et deck Hellfire",
       "le scenario `hellfire_torn_expert` : villain hf502a,hf502b (livret : « Emma Frost (B1) instead for expert mode ») ; nombres texte <-> code",
       deck("01105"), [],
       {"en_jeu": ["hf502a", "hf503b", "hf504a"], "absents": ["hf501a"], "vie": [["hf502a", 8]], "attaque": [["hf502a", 2]], "menace_de": [["hf504a", 13]],
        "hellfire_total": ["hf301", "hf302", "hf331", "hf341", "hf351"]}, scenario=SCX, libre=True),
    _c("hf502a Reponse forcee : apres son complot, defausse 2 cartes ; DEUX cartes PSIONIC -> +2 menaces sur chaque manigance (principale 1 + 2 + 2 = 5, Puppetry 15)",
       "« discard 2 cards ..., for each PSIONIC card discarded in this way, place 1 threat on each scheme » : alter-ego, Emma manigance (SCH 2) ; la 1re carte du deck est la carte de boost",
       deck("01105", "hf303", "hf304", "01105"), ["Puzzle.Activate('hf502a')"],
       {"menace_de": [["hf503b", 5], ["hf504a", 15]], "defausse_rencontre_ids": ["hf303", "hf304", "01105"]}, scenario=SCX),
    _c("hf502a Reponse forcee : UNE seule carte PSIONIC sur les deux -> +1 seulement (principale 4, Puppetry 14)",
       "le compte est PAR carte PSIONIC defaussee",
       deck("01105", "hf303", "01105", "01105"), ["Puzzle.Activate('hf502a')"],
       {"menace_de": [["hf503b", 4], ["hf504a", 14]]}, scenario=SCX),
    _c("hf502a Reponse forcee : TEMOIN, aucune carte PSIONIC -> aucune menace de plus (principale 3, Puppetry 13)",
       "contre-cas", deck("01105", "01105", "01105", "01105"), ["Puzzle.Activate('hf502a')"],
       {"menace_de": [["hf503b", 3], ["hf504a", 13]]}, scenario=SCX),
    _c("hf502a Interruption forcee : serait vaincue (8 degats) -> elle se retourne (hf502b), 5 menaces partent de chaque manigance",
       "meme interruption que hf501a, PV 8 : principale 8 -> 3, Puppetry 13 -> 8",
       ["Puzzle.PlaceThreat('hf503b', 7)"] + deck("01105"), ["Puzzle.Damage('hf502a', 8)"],
       {"en_jeu": ["hf502b", "hf504a"], "absents": ["hf502a"], "menace_de": [["hf503b", 3], ["hf504a", 8]]}, scenario=SCX),
    _c("hf502b Interruption forcee : quand elle s'active contre un joueur, il recoit une carte de rencontre FACE CACHEE a la place (pas de complot : le complot reste a 1)",
       "« When Emma Frost activates against a player, give the player a facedown encounter card instead »",
       ["Puzzle.Flip('hf502a')"] + deck("01105", "01105"), ["Puzzle.Activate('hf502b')"],
       {"distribuees": 1, "menace_de": [["hf503b", 1]], "en_jeu": ["hf502b"]}, scenario=SCX),
    _c("hf502b Reponse forcee : apres la fin de la phase du vilain, elle se retourne (hf502a) et ses PV sont remis (8 pleins, 0 degat)",
       "« flip this card, then set Emma Frost's hit point dial to her printed hit points »",
       ["Puzzle.Flip('hf502a')", "Puzzle.Damage('hf502b', 30)"] + deck("01105"), ["Puzzle.EndVillainPhase()"],
       {"en_jeu": ["hf502a"], "absents": ["hf502b"], "degats_de": [["hf502a", 0]], "vie": [["hf502a", 8]]}, scenario=SCX),
    # ===================================================================== complot The Hellfire Club's Revenge / Free Cassandra Nova
    _c("hf503a Setup : Nova's Psychic Puppetry est mise en jeu face CONTROLLED (8 + Hinder 5 = 13 menaces, Permanent)",
       "« Put the Nova's Psychic Puppetry side scheme into play, CONTROLLED side face up » : prise dans la zone mise de cote du scenario (`set_aside`)",
       deck("01105"), [],
       {"en_jeu": ["hf504a"], "absents": ["hf504b"], "menace_de": [["hf504a", 13]], "trait_de": [["hf504a", "CONTROLLED", True]]}),
    _c("hf503a Setup : les sbires ELITE HELLFIRE de TOUS les modules sont retires du deck de rencontre et forment le Hellfire deck (White Queen x2, Shaw, Negasonic, Cassandra)",
       "« Shuffle every ELITE, HELLFIRE minion to create the Hellfire deck and set it next to the encounter deck » ; leur defausse est vide",
       [], [],
       {"hellfire_total": ["hf301", "hf302", "hf331", "hf341", "hf351"], "hellfire_defausse": [],
        "hors_deck_rencontre": ["hf301", "hf302", "hf331", "hf341", "hf351"]}, libre=True),
    _c("hf503a Setup : TEMOIN, les sbires HELLFIRE qui ne sont PAS elite ne vont pas dans le Hellfire deck (Hellfire Pawn : ajoute a la main au deck de rencontre puis re-cree le deck)",
       "le Setup ne prend QUE les sbires ELITE ET HELLFIRE : un module avec un Hellfire Pawn (hf313) laisse le Pawn dans le deck de rencontre",
       ["Puzzle.CreateEncounterDeck('hf313')", "Puzzle.SendCardSetup('hf503a')"], [],
       {"deck_rencontre_contient": ["hf313"]}),
    _c("hf503a Setup de campagne (mode campagne reel) : Xavier's Institute en jeu, 16 allies de cote, une manigance POTENTIAL ALLY melangee",
       "le complot 1A porte `hc.MiseEnPlace(4)` : `WhenCampaignSetup` ne part qu'en mode campagne (`campagne=True`)",
       [HEROS], [], {"en_jeu": ["hf048"]}, campagne=True, libre=True),
    _c("hf503a Setup de campagne : TEMOIN, HORS campagne Xavier's Institute n'est PAS en jeu",
       "pas de mise en place de campagne", [HEROS], [], {"absents": ["hf048"]}),
    _c("hf503b Valeurs imprimees : menace de depart 1, escalade 1 (par joueur), seuil 15 : 14 menaces de plus ne completent PAS le complot",
       "nombres texte <-> code : `TargetThreat 15*`, `StartingThreat 1*`, `EscalationThreat 1*`",
       deck("01105"), ["Puzzle.PlaceThreat('hf503b', 13)"],
       {"menace_de": [["hf503b", 14]], "partie_finie": False}),
    _c("hf503b « If this scheme is completed, the players lose the game » : le seuil de 15 est atteint -> partie perdue",
       "texte imprime lu par le moteur (scheme_main.py)",
       deck("01105"), ["Puzzle.PlaceThreat('hf503b', 14)"],
       {"gagnee": False, "partie_finie": True}),
    _c("hf503b Interruption forcee : au debut de la phase des joueurs, un joueur SANS sbire ELITE HELLFIRE engage revele le dessus du Hellfire deck (Negasonic, engagee avec lui)",
       "« each player not engaged with an ELITE, HELLFIRE minion reveals the top card of the Hellfire deck »",
       ["Puzzle.EmptyHellfireDeck()", "Puzzle.PutIntoHellfireDeck('hf341')"] + deck("01105"), ["Puzzle.BeginPlayerPhase()"],
       {"en_jeu": ["hf341"], "engages": ["hf341"], "hellfire_deck": []}),
    _c("hf503b Interruption forcee : TEMOIN, un joueur DEJA engage avec un sbire ELITE HELLFIRE ne revele rien (le deck Hellfire garde sa carte)",
       "« not engaged with an ELITE, HELLFIRE minion » : Cassandra (elite) est deja engagee ; Negasonic reste dans le deck",
       ["Puzzle.EmptyHellfireDeck()", "Puzzle.PutIntoHellfireDeck('hf341')", "Puzzle.PutIntoPlay('hf351')"] + deck("01105"), ["Puzzle.BeginPlayerPhase()"],
       {"en_jeu": ["hf351"], "hellfire_deck": ["hf341"], "absents": ["hf341"]}),
    _c("hf503b Interruption forcee : un sbire HELLFIRE NON elite engage (Hellfire Pawn) ne retient PAS le joueur : il revele quand meme",
       "« ELITE, HELLFIRE » : les deux traits ensemble",
       ["Puzzle.EmptyHellfireDeck()", "Puzzle.PutIntoHellfireDeck('hf341')", "Puzzle.PutIntoPlay('hf313')"] + deck("01105"), ["Puzzle.BeginPlayerPhase()"],
       {"en_jeu": ["hf341", "hf313"], "hellfire_deck": []}),
    _c("hf503b Hellfire deck VIDE : sa defausse est remelangee dedans SANS penalite (aucune carte de rencontre distribuee) et le dessus est revele",
       "« If the Hellfire deck is ever empty, shuffle the Hellfire discard pile into the Hellfire deck. There is no penalty for doing this »",
       ["Puzzle.EmptyHellfireDeck()", "Puzzle.PutIntoHellfireDeck('hf351', discard=True)"] + deck("01105"), ["Puzzle.BeginPlayerPhase()"],
       {"en_jeu": ["hf351"], "hellfire_deck": [], "hellfire_defausse": [], "distribuees": 0}),
    _c("hf503b Hellfire deck ET defausse vides : rien n'est revele, aucune erreur",
       "garde : deck et defausse vides", ["Puzzle.EmptyHellfireDeck()"] + deck("01105"), ["Puzzle.BeginPlayerPhase()"],
       {"hellfire_deck": [], "hellfire_defausse": [], "partie_finie": False}),
    _c("hf503b Hellfire deck : un sbire ELITE HELLFIRE VAINCU va dans la defausse HELLFIRE (pas dans celle du deck de rencontre)",
       "« When an ELITE, HELLFIRE minion is defeated or otherwise discarded, place it in the Hellfire discard pile » : Cassandra (2 PV) du Hellfire deck, revelee puis vaincue",
       ["Puzzle.EmptyHellfireDeck()", "Puzzle.PutIntoHellfireDeck('hf351')"] + deck("01105"), ["Puzzle.BeginPlayerPhase()", "Puzzle.Damage('hf351', 2)"],
       {"absents": ["hf351"], "hellfire_defausse": ["hf351"], "hellfire_deck": [], "defausse_rencontre_ids": []}),
    _c("hf503b Hellfire deck : un sbire ELITE HELLFIRE simplement DEFAUSSE (pas vaincu) va aussi dans la defausse HELLFIRE",
       "« defeated or otherwise discarded »", ["Puzzle.EmptyHellfireDeck()", "Puzzle.PutIntoHellfireDeck('hf341')"] + deck("01105"),
       ["Puzzle.BeginPlayerPhase()", "Puzzle.Discard('hf341')"],
       {"absents": ["hf341"], "hellfire_defausse": ["hf341"], "defausse_rencontre_ids": []}),
    # ===================================================================== hf504a / hf504b Nova's Psychic Puppetry
    _c("hf504a Interruption forcee : derniere menace retiree -> chaque sbire HELLFIRE en jeu est defausse (l'ELITE va dans la defausse HELLFIRE, l'autre dans celle de rencontre), chaque joueur recoit une carte face cachee, la carte se RETOURNE (hf504b)",
       "« discard each HELLFIRE minion in play and deal each player a facedown encounter card. Then, flip this card » ; face B : menace de depart 1 + Hinder 12 = 13",
       deck("01105", "01105") + [HEROS, "Puzzle.EmptyHellfireDeck()", "Puzzle.PutIntoHellfireDeck('hf341')", "Puzzle.BeginPlayerPhase()", "Puzzle.PutIntoPlay('hf313')"],
       ["Puzzle.PlaceThreat('hf504a', -13)"],
       {"en_jeu": ["hf504b"], "absents": ["hf504a", "hf341", "hf313"], "hellfire_defausse": ["hf341"], "defausse_rencontre_ids": ["hf313"], "distribuees": 1,
        "menace_de": [["hf504b", 13]], "trait_de": [["hf504b", "FRAGMENT", True]], "partie_finie": False}),
    _c("hf504a Interruption forcee : TEMOIN, il reste de la menace (13 - 12 = 1) -> aucune defausse, la carte ne se retourne pas",
       "contre-cas : seule la DERNIERE menace declenche", [HEROS, "Puzzle.PutIntoPlay('hf313')"] + deck("01105"), ["Puzzle.PlaceThreat('hf504a', -12)"],
       {"en_jeu": ["hf504a", "hf313"], "absents": ["hf504b"], "menace_de": [["hf504a", 1]], "distribuees": 0}),
    _c("hf504a Permanent : la carte reste en jeu a 0 menace (elle se retourne, elle n'est pas vaincue ni defaussee) : la partie continue",
       "« Permanent » (`desc.Permanent`, natif) : jamais de victoire par la face A",
       deck("01105"), ["Puzzle.PlaceThreat('hf504a', -13)"],
       {"en_jeu": ["hf504b"], "partie_finie": False}),
    _c("hf504a Reponse forcee : un sbire ELITE HELLFIRE est vaincu par le joueur -> 5 menaces partent d'UNE AUTRE manigance annexe (Psychic Entanglement 8 -> 3, Puppetry intacte a 13)",
       "« After an ELITE, HELLFIRE minion is defeated, remove 5 threat from another side scheme » : Cassandra (2 PV) revelee du Hellfire deck puis vaincue par l'attaque du heros",
       deck("01105") + [HEROS, "Puzzle.EmptyHellfireDeck()", "Puzzle.PutIntoHellfireDeck('hf351')", "Puzzle.BeginPlayerPhase()", "Puzzle.PutIntoPlay('hf508')"],
       ["Puzzle.Attack('01001a')"],
       {"absents": ["hf351"], "hellfire_defausse": ["hf351"], "menace_de": [["hf508", 3], ["hf504a", 13]]}, cibles=["hf351"], accepter_choix=True),
    _c("hf504a Reponse forcee : AUCUNE autre manigance annexe -> les 5 menaces partent d'ICI (13 -> 8)",
       "« Otherwise, remove 5 threat from here »", deck("01105") + [HEROS, "Puzzle.EmptyHellfireDeck()", "Puzzle.PutIntoHellfireDeck('hf351')", "Puzzle.BeginPlayerPhase()"],
       ["Puzzle.Attack('01001a')"],
       {"absents": ["hf351"], "menace_de": [["hf504a", 8]]}, cibles=["hf351"], accepter_choix=True),
    _c("hf504a Reponse forcee : TEMOIN, un sbire HELLFIRE NON elite vaincu (Hellfire Pawn) -> aucune menace retiree",
       "« an ELITE, HELLFIRE minion » : les deux traits", [HEROS, "Puzzle.PutIntoPlay('hf313')", "Puzzle.Damage('hf313', 1)"] + deck("01105"), ["Puzzle.Attack('01001a')"],
       {"absents": ["hf313"], "menace_de": [["hf504a", 13]]}, cibles=["hf313"], accepter_choix=True),
    _c("hf504b Interruption forcee : derniere menace retiree -> Emma Frost s'echappe : les joueurs GAGNENT la partie",
       "« Emma Frost escapes from the control of Cassandra Nova, the players win the game »",
       ["Puzzle.Flip('hf504a')", "Puzzle.SetThreat('hf504b', 13)"] + deck("01105"), ["Puzzle.PlaceThreat('hf504b', -13)"],
       {"gagnee": True, "partie_finie": True}),
    _c("hf504b Interruption forcee : TEMOIN, il reste 1 menace sur la face B -> la partie n'est PAS gagnee",
       "seule la DERNIERE menace retiree fait gagner",
       ["Puzzle.Flip('hf504a')", "Puzzle.SetThreat('hf504b', 13)"] + deck("01105"), ["Puzzle.PlaceThreat('hf504b', -12)"],
       {"partie_finie": False, "menace_de": [["hf504b", 1]]}),
    _c("hf504b Interruption forcee : TEMOIN, la face A (CONTROLLED) vidée ne fait PAS gagner",
       "contre-cas : seule la face B gagne", deck("01105"), ["Puzzle.PlaceThreat('hf504a', -13)"],
       {"gagnee": False}),
    _c("hf504b « Each HELLFIRE minion gains the ILLUSION trait » : un Hellfire Pawn en jeu devient ILLUSION",
       "`GiveKeywordToInPlayWhenApplyThis(CardFinder2(HELLFIRE, Minion), trait=ILLUSION)`",
       ["Puzzle.Flip('hf504a')", "Puzzle.PutIntoPlay('hf313')"] + deck("01105"), [],
       {"trait_de": [["hf313", "ILLUSION", True]]}),
    _c("hf504b ILLUSION : TEMOIN, sur la face A (CONTROLLED) le Hellfire Pawn n'est pas ILLUSION",
       "contre-cas de la face", ["Puzzle.PutIntoPlay('hf313')"] + deck("01105"), [], {"trait_de": [["hf313", "ILLUSION", False]]}),
    _c("hf504b ILLUSION : TEMOIN, un sbire NON HELLFIRE (Hydra Mercenary) ne gagne pas le trait",
       "« Each HELLFIRE minion »", ["Puzzle.Flip('hf504a')", "Puzzle.PutIntoPlay('01101')"] + deck("01105"), [], {"trait_de": [["01101", "ILLUSION", False]]}),
    _c("hf504b Reponse forcee : un sbire ELITE HELLFIRE vaincu -> 5 menaces d'une AUTRE manigance annexe (Psychic Bulwark 9 -> 4), la face B garde ses 13",
       "meme Reponse forcee que la face A",
       deck("01105") + [HEROS, "Puzzle.Flip('hf504a')", "Puzzle.SetThreat('hf504b', 13)", "Puzzle.EmptyHellfireDeck()", "Puzzle.PutIntoHellfireDeck('hf351')", "Puzzle.BeginPlayerPhase()", "Puzzle.PutIntoPlay('hf507')"],
       ["Puzzle.Attack('01001a')"],
       {"absents": ["hf351"], "menace_de": [["hf507", 4], ["hf504b", 13]]}, cibles=["hf351"], accepter_choix=True),
    # ===================================================================== hf505 Protect Students
    _c("hf505 revelee : « Your hero gets -1 ATK, and -1 DEF » (Spider-Man heros : ATQ 2 -> 1, DEF 3 -> 2)",
       "`GiveKeywordToInPlayWhenApplyThis(Hero, control_by=\"You\", attack=-1, defense=-1)` ; l'obligation est revelee devant le joueur",
       [HEROS] + deck("hf505", "01105"), ["Puzzle.Reveal('hf505')"],
       {"en_jeu": ["hf505"], "attributs": {"attack": -1, "defense": -1}}),
    _c("hf505 : TEMOIN, sans la carte l'attaque et la defense du heros sont celles imprimees",
       "contre-cas", [HEROS] + deck("01105"), [], {"attributs": {"attack": 0, "defense": 0}}),
    _c("hf505 Action d'alter-ego : incliner l'identite ET reveler 1 carte du Hellfire deck -> 1 degat soigne sur CHAQUE personnage ami (identite 3 -> 2, allie 1 -> 0), la carte est defaussee",
       "« Exhaust your identity and reveal 1 card from the Hellfire deck -> heal 1 damage from each friendly character in play. Discard this card. » : Negasonic revelee, engagee",
       deck("hf505", "01105") + ["Puzzle.EmptyHellfireDeck()", "Puzzle.PutIntoHellfireDeck('hf341')", "Puzzle.PutIntoPlay('01083', under_control=True)", "Puzzle.Damage('01001b', 3)",
                                  "Puzzle.Damage('01083', 1)", "Puzzle.Reveal('hf505')"],
       ["Puzzle.Action('hf505', 'AlterEgoAction')"],
       {"absents": ["hf505"], "en_jeu": ["hf341"], "engages": ["hf341"], "exhausted": ["01001b"], "degats_identite": 2, "degats_de": [["01083", 0]]}, accepter_choix=True),
    _c("hf505 Action d'alter-ego : TEMOIN, deck ET defausse Hellfire VIDES -> le cout (reveler) ne peut pas etre paye : rien n'est soigne, la carte reste",
       "« reveal 1 card from the Hellfire deck » est une partie du COUT", 
       deck("hf505", "01105") + ["Puzzle.EmptyHellfireDeck()", "Puzzle.Damage('01001b', 3)", "Puzzle.Reveal('hf505')"],
       ["Puzzle.Action('hf505', 'AlterEgoAction')"],
       {"en_jeu": ["hf505"], "degats_identite": 3}, accepter_choix=True),
    # ===================================================================== hf506 Uncover The Truth
    _c("hf506 Action d'alter-ego : incliner l'identite -> soigne 5 degats du vilain ET retire 5 menaces d'une manigance annexe (Puppetry 13 -> 8) ; la carte est defaussee",
       "« heal 5 damage from the villain and remove 5 threat from a side scheme. Discard this obligation » : les DEUX parties",
       deck("hf506", "01105") + ["Puzzle.Damage('hf501a', 5)", "Puzzle.Reveal('hf506')"], ["Puzzle.Action('hf506', 'AlterEgoAction')"],
       {"absents": ["hf506"], "degats_de": [["hf501a", 0]], "menace_de": [["hf504a", 8]], "exhausted": ["01001b"]}, cibles=["hf504a"], accepter_choix=True),
    _c("hf506 Action d'alter-ego : le soin du vilain est plafonne a ses degats (2 degats -> 0) et les 5 menaces partent quand meme",
       "mesure du « heal 5 » sur un vilain peu blesse", deck("hf506", "01105") + ["Puzzle.Damage('hf501a', 2)", "Puzzle.Reveal('hf506')"], ["Puzzle.Action('hf506', 'AlterEgoAction')"],
       {"degats_de": [["hf501a", 0]], "menace_de": [["hf504a", 8]]}, cibles=["hf504a"], accepter_choix=True),
    _c("hf506 Hazard : l'icone (carte penchee + croix) fait compter 1 icone Hazard en jeu une fois la carte revelee",
       "`desc.Hazard = 1` natif (fiche hazard.md) : `Worlds.GetHazardIcons`", deck("hf506", "01105") + ["Puzzle.Reveal('hf506')"], [],
       {"en_jeu": ["hf506"], "icones": [["Hazard", 1]]}),
    # ===================================================================== hf507 Psychic Bulwark
    _c("hf507 revelee : menace de depart 9 ; « Each minion gains guard and patrol » : un sbire en jeu (Weapons Runner) a Guard et Patrol",
       "`GiveKeywordToInPlayWhenApplyThis(Minion, guard=1, patrol=1)`", deck("hf507", "01105") + ["Puzzle.PutIntoPlay('01121')", "Puzzle.Reveal('hf507')"], [],
       {"en_jeu": ["hf507"], "menace_de": [["hf507", 9]], "garde": ["01121"], "patrouille": ["01121"]}),
    _c("hf507 Guard/Patrol : un sbire qui ENTRE APRES la carte les a aussi",
       "la regle vaut pour tous les sbires, y compris ceux qui arrivent ensuite", deck("hf507", "01105") + ["Puzzle.Reveal('hf507')", "Puzzle.PutIntoPlay('01121')"], [],
       {"garde": ["01121"], "patrouille": ["01121"]}),
    _c("hf507 Guard/Patrol : TEMOIN, sans la carte, Weapons Runner n'a ni Guard ni Patrol",
       "contre-cas : verifie par l'absence d'erreur et le comptage (le Guard natif du sbire est nul)", deck("01105") + ["Puzzle.PutIntoPlay('01121')"], [],
       {"en_jeu": ["01121"]}),
    _c("hf507 Boost : « Give each minion a tough status card » : un sbire en jeu (Weapons Runner) devient Tenace",
       "`Faces.GiveStatus(minions, \"Tough\")` pendant l'activation du vilain",
       deck("01105") + ["Puzzle.PutIntoPlay('01121')"], ["Puzzle.Boost('hf507')"],
       {"statuts": [["01121", "Tough"]]}),
    # ===================================================================== hf508 Psychic Entanglement
    _c("hf508 revelee : menace de depart 8 ; « Threat cannot be removed from other side schemes » : la contrarie du heros sur Puppetry n'enleve RIEN (5 -> 5)",
       "`ThreatCannotBeRemovedFromWhile(SchemeSide2, effect.this != message.trigger)` (modele 27107)",
       [HEROS, "Puzzle.SetThreat('hf504a', 5)"] + deck("hf508", "01105") + ["Puzzle.Reveal('hf508')"], ["Puzzle.Thwart('01001a')"],
       {"en_jeu": ["hf508"], "menace_de": [["hf508", 8], ["hf504a", 5]]}, cibles=["hf504a"], accepter_choix=True),
    _c("hf508 : TEMOIN, sans la carte la meme contrarie retire 1 menace (5 -> 4)",
       "contre-cas", [HEROS, "Puzzle.SetThreat('hf504a', 5)"] + deck("01105"), ["Puzzle.Thwart('01001a')"],
       {"menace_de": [["hf504a", 4]]}, cibles=["hf504a"], accepter_choix=True),
    _c("hf508 : on PEUT contrarier Psychic Entanglement elle-meme (8 -> 7) et le complot principal n'est pas vise",
       "« OTHER side schemes » : pas celle-ci, pas la principale", [HEROS] + deck("hf508", "01105") + ["Puzzle.Reveal('hf508')"], ["Puzzle.Thwart('01001a')"],
       {"menace_de": [["hf508", 7]]}, cibles=["hf508"], accepter_choix=True),
    _c("hf508 : l'interruption de defaite d'Emma Frost retire 5 menaces de la principale et d'ELLE-MEME, pas de Puppetry (13 reste 13)",
       "« Threat cannot be removed from OTHER side schemes » vaut aussi pour les effets de carte", ["Puzzle.PlaceThreat('hf503b', 7)"] + deck("hf508", "01105") + ["Puzzle.Reveal('hf508')"],
       ["Puzzle.Damage('hf501a', 7)"],
       {"menace_de": [["hf508", 3], ["hf504a", 13], ["hf503b", 3]], "en_jeu": ["hf501b"]}),
    _c("hf508 When Defeated : defaite -> chaque joueur recoit une carte face cachee ; Victory 1 : elle va dans la pile de victoire",
       "« When Defeated : Deal each player a facedown encounter card » ; `Victory 1` natif",
       [HEROS, "Puzzle.SetThreat('hf508', 1)"] + deck("hf508", "01105") + ["Puzzle.Reveal('hf508')", "Puzzle.SetThreat('hf508', 1)"], ["Puzzle.Thwart('01001a')"],
       {"absents": ["hf508"], "distribuees": 1, "dans_victoire": ["hf508"]}, cibles=["hf508"], accepter_choix=True),
    # ===================================================================== hf509 Psionic Paragon
    _c("hf509 revelee : menace 4 (par joueur) ; « Emma Frost gets +10 hit point » : PV 7 -> 17",
       "`GiveKeywordToInPlayWhenApplyThis(CardFinder(name=Emma Frost, Villain), health=10)`", deck("hf509", "01105") + ["Puzzle.Reveal('hf509')"], [],
       {"en_jeu": ["hf509"], "menace_de": [["hf509", 4]], "vie": [["hf501a", 17]]}),
    _c("hf509 : TEMOIN, sans la carte Emma Frost garde ses 7 PV", "contre-cas", deck("01105"), [], {"vie": [["hf501a", 7]]}),
    _c("hf509 When Revealed : un joueur SANS sbire engage recoit 1 carte face cachee",
       "« Deal 1 facedown encounter card to each player with no engaged minions »", deck("hf509", "01105"), ["Puzzle.Reveal('hf509')"],
       {"distribuees": 1}),
    _c("hf509 When Revealed : TEMOIN, un joueur ENGAGE avec un sbire n'en recoit pas",
       "contre-cas : sbire engage (Hellfire Pawn)", deck("hf509", "01105") + ["Puzzle.PutIntoPlay('hf313')"], ["Puzzle.Reveal('hf509')"],
       {"distribuees": 0}),
    _c("hf509 « Each ILLUSION card gains incite 1 » : reveler une carte ILLUSION (Astral Trap) pose 1 menace sur le complot principal (1 -> 2)",
       "`GiveKeywordToInPlayWhenApplyThis(CardFinder2(ILLUSION, EncounterCard), incite=1)` (modele 39035)", deck("hf509", "hf303", "01105") + ["Puzzle.Reveal('hf509')"], ["Puzzle.Reveal('hf303')"],
       {"menace_de": [["hf503b", 2]]}),
    _c("hf509 Incite : TEMOIN, sans la carte la meme revelation ne pose aucune menace (principale 1)",
       "contre-cas", deck("hf303", "01105"), ["Puzzle.Reveal('hf303')"], {"menace_de": [["hf503b", 1]]}),
    _c("hf509 Incite : TEMOIN, une carte NON ILLUSION (Bomb Scare) ne pose pas de menace",
       "« Each ILLUSION card » : Illusion Unraveled (SKILL, pas ILLUSION)", deck("hf509", "hf307", "01105") + ["Puzzle.Reveal('hf509')"], ["Puzzle.Reveal('hf307')"], {"en_jeu": ["hf307"], "menace_de": [["hf503b", 1]]}),
    # ===================================================================== hf510 Hellfire Assault
    _c("hf510 revelee : menace de depart 1 ; « Threat cannot be removed from here except by thwarting » : l'interruption de defaite d'Emma ne lui retire RIEN (6 reste 6), Puppetry perd 5",
       "`ThreatCannotBeRemovedFromWhile(\"This\", by_thwarting=False)`", ["Puzzle.SetThreat('hf510', 6)"] + deck("hf510", "01105") + ["Puzzle.Reveal('hf510')", "Puzzle.SetThreat('hf510', 6)"],
       ["Puzzle.Damage('hf501a', 7)"],
       {"menace_de": [["hf510", 6], ["hf504a", 8]], "en_jeu": ["hf501b"]}),
    _c("hf510 : la CONTRARIE du heros retire bien de la menace (6 -> 5)",
       "« except by thwarting »", [HEROS] + deck("hf510", "01105") + ["Puzzle.Reveal('hf510')", "Puzzle.SetThreat('hf510', 6)"], ["Puzzle.Thwart('01001a')"],
       {"menace_de": [["hf510", 5]]}, cibles=["hf510"], accepter_choix=True),
    _c("hf510 Reponse forcee : un sbire HELLFIRE (Hellfire Pawn) est vaincu PAR UN JOUEUR -> Emma Frost MANIGANCE (SCH 2 : principale 1 -> 3)",
       "« if it is White Queen, Emma Frost attacks the player. Otherwise, Emma Frost schemes »",
       [HEROS] + deck("hf510", "01105") + ["Puzzle.Reveal('hf510')", "Puzzle.PutIntoPlay('hf313')", "Puzzle.Damage('hf313', 1)"], ["Puzzle.Attack('01001a')"],
       {"absents": ["hf313"], "menace_de": [["hf503b", 3]]}, cibles=["hf313"], accepter_choix=True),
    _c("hf510 Reponse forcee : le sbire vaincu est WHITE QUEEN -> Emma Frost ATTAQUE le joueur (ATQ 1 : 1 degat sur l'identite, la principale ne bouge pas)",
       "le sbire White Queen (Perfection hf302) entre en jeu dans ce scenario (le vilain est Emma Frost, pas White Queen) ; le heros est incline pour ne pas defendre",
       [HEROS] + deck("hf510", "01105", "01105") + ["Puzzle.Reveal('hf510')", "Puzzle.PutIntoPlay('hf302')", "Puzzle.Damage('hf302', 2)"], ["Puzzle.Attack('01001a')", "Puzzle.Exhaust('01001a')"],
       {"absents": ["hf302"], "menace_de": [["hf503b", 1]], "degats_identite": 1}, cibles=["hf302"], accepter_choix=True),
    _c("hf510 Reponse forcee : TEMOIN, un sbire qui n'est PAS HELLFIRE vaincu (Weapons Runner) -> Emma ne fait rien (principale 1)",
       "« After a HELLFIRE minion is defeated »", [HEROS] + deck("hf510", "01105") + ["Puzzle.Reveal('hf510')", "Puzzle.PutIntoPlay('01121')", "Puzzle.Damage('01121', 0)"], ["Puzzle.Attack('01001a')"],
       {"absents": ["01121"], "menace_de": [["hf503b", 1]]}, cibles=["01121"], accepter_choix=True),
    _c("hf510 Boost : « Reveal this card » : Emma s'active (boost) et la carte est REVELEE (menace de depart 1 sur elle)",
       "(modele hf110 : `WhenCardBecomeBoost(\"This\", RevealThisCard)`)", deck("01105"), ["Puzzle.Boost('hf510')"],
       {"en_jeu": ["hf510"]}),
    # ===================================================================== MODULE NEGASONIC TEENAGE WARHEAD
    _c("hf341 sbire : PV 4, ATQ 2, MNG 1, Steady, Toughness (carte Tenace a l'entree en jeu), ELITE HELLFIRE",
       "nombres texte <-> code (scan) ; Steady et Toughness lus dans `desc`", deck("01105"), ["Puzzle.PutIntoPlay('hf341')"],
       {"en_jeu": ["hf341"], "vie": [["hf341", 4]], "attaque": [["hf341", 2]], "steady": ["hf341"], "statuts": [["hf341", "Tough"]],
        "trait_de": [["hf341", "ELITE", True], ["hf341", "HELLFIRE", True]]}),
    _c("hf341 Interruption : quand elle ATTAQUE le joueur, celui-ci doit incliner un soutien (Helicarrier) -> incline",
       "« [star] When Negasonic Teenage Warhead attacks you, you must exhaust a support or upgrade you control, if able » : le heros est en forme heros",
       [HEROS, "Puzzle.PutIntoPlay('01092', under_control=True)", "Puzzle.PutIntoPlay('hf341')"] + deck("01105"), ["Puzzle.Attack('hf341')"],
       {"exhausted": ["01092"]}),
    _c("hf341 Interruption : une AMELIORATION (Spider-Tracer sur le heros) peut etre inclinee a la place d'un soutien (seul candidat)",
       "« a support OR UPGRADE you control »", [HEROS, "Puzzle.AttachReel('01007', '01001a')", "Puzzle.PutIntoPlay('hf341')"] + deck("01105"),
       ["Puzzle.Attack('hf341')"], {"exhausted": ["01007"]}),
    _c("hf341 Interruption : « if able » : aucun soutien ni amelioration -> rien n'est incline, l'attaque a lieu (le heros defend : aucune erreur)",
       "contre-cas : aucun candidat", [HEROS, "Puzzle.PutIntoPlay('hf341')"] + deck("01105"), ["Puzzle.Attack('hf341')"],
       {"en_jeu": ["hf341"]}),
    _c("hf341 Interruption : TEMOIN, un soutien DEJA incline n'est pas un candidat (reste incline, aucune erreur)",
       "« exhaust » exige une carte prete", [HEROS, "Puzzle.PutIntoPlay('01092', under_control=True, exhaust=True)", "Puzzle.PutIntoPlay('hf341')"] + deck("01105"),
       ["Puzzle.Attack('hf341')"], {"exhausted": ["01092"]}),
    _c("hf341 Interruption : TEMOIN, elle ne vise que l'attaque CONTRE le joueur : le vilain qui attaque ne fait rien incliner",
       "« attacks you » : seule Negasonic", [HEROS, "Puzzle.PutIntoPlay('01092', under_control=True)"] + deck("01105", "01105"), ["Puzzle.Attack('hf501a')"],
       {"pret": ["01092"]}),
    _c("hf341 Boost : « Exhaust a support or upgrade you control » : Emma s'active (Negasonic en boost) -> Helicarrier est inclinee",
       "boost de l'activation du vilain", ["Puzzle.PutIntoPlay('01092', under_control=True)"] + deck("01105"), ["Puzzle.Boost('hf341')"],
       {"exhausted": ["01092"]}),
    _c("hf342 Perception Manipulation revelee : s'attache a l'identite ; « cannot be readied » : incline puis `Ready` -> reste incline",
       "`AttachToFaceWhenPutIntoPlay(\"YourIdentity\")` + `CardCannotReady(\"AttachedCharacter\")`", deck("hf342", "01105"),
       ["Puzzle.Reveal('hf342')", "Puzzle.Exhaust('01001b')", "Puzzle.Ready('01001b')"],
       {"attache": [["hf342", "01001b"]], "exhausted": ["01001b"]}),
    _c("hf342 cannot be readied : TEMOIN, sans la carte `Ready` redresse l'identite",
       "contre-cas", deck("01105"), ["Puzzle.Exhaust('01001b')", "Puzzle.Ready('01001b')"], {"pret": ["01001b"]}),
    _c("hf342 Action d'alter-ego : depenser [mental][mental] (un Genius imprime deux ressources mentales) -> la carte est defaussee",
       "« Alter-Ego Action : Spend [mental][mental] -> discard this card » : `Cost(\"BB\")` ; 01089 Genius genere [mental][mental]", deck("hf342", "01105") + ["Puzzle.Reveal('hf342')"], ["Puzzle.Action('hf342', 'AlterEgoAction')"],
       {"absents": ["hf342"]}, main_exclusive=["01089"], payer_avec=["01089"], payer_tout=True, accepter_choix=True),
    _c("hf342 Action d'alter-ego : TEMOIN, des ressources PHYSIQUES (Strength) ne paient pas [mental][mental] -> la carte reste",
       "le type des ressources", deck("hf342", "01105") + ["Puzzle.Reveal('hf342')"], ["Puzzle.Action('hf342', 'AlterEgoAction')"],
       {"en_jeu": ["hf342"]}, main_exclusive=["01090"], payer_avec=["01090"], payer_tout=True, accepter_choix=True),
    _c("hf342 Boost : « Change your form » : Emma s'active, le joueur passe de l'alter-ego a la forme heros",
       "`identite.ChangeToOtherIdentityForm`", deck("01105"), ["Puzzle.Boost('hf342')"], {"forme": "Hero"}),
    _c("hf343 Perception Manipulation (2e exemplaire) : meme effet (attachee a l'identite, ne se redresse pas)",
       "meme script que hf342", deck("hf343", "01105"), ["Puzzle.Reveal('hf343')", "Puzzle.Exhaust('01001b')", "Puzzle.Ready('01001b')"],
       {"attache": [["hf343", "01001b"]], "exhausted": ["01001b"]}),
    _c("hf344 Mind Over Matter : revele la PLUS HAUTE ATTACHEMENT de la defausse de rencontre (Astral Trap, au-dessus d'Illusory Defender)",
       "« Reveal the topmost attachment in the encounter discard pile » : hf303 est la derniere defaussee",
       deck("hf344", "01105") + ["Puzzle.EmptyEncounterDiscardPile()", "Puzzle.CreateEncounterDiscardPile('hf304', 'hf303')"], ["Puzzle.Reveal('hf344')"],
       {"en_jeu": ["hf303"], "absents": ["hf304"]}),
    _c("hf344 Mind Over Matter : sans attachement dans la defausse, la carte gagne surge (la carte suivante, Psychic Bulwark, est revelee)",
       "« Otherwise, this card gains surge »", deck("hf344", "hf507", "01105") + ["Puzzle.EmptyEncounterDiscardPile()"], ["Puzzle.Reveal('hf344')"],
       {"en_jeu": ["hf507"]}),
    _c("hf344 Boost : « Exhaust your hero » : Emma attaque, un ALLIE defend (le heros reste pret) puis la carte en boost incline le HEROS",
       "boost de l'activation du vilain ; ⚠ le heros ne doit pas defendre lui-meme (la defense l'incline deja) : Black Cat (01002) defend (`Puzzle.Attack(carte, defenseur)`)",
       [HEROS, "Puzzle.PutIntoPlay('01002', under_control=True)"] + deck("hf344", "01105"), ["Puzzle.Attack('hf501a', '01002')"], {"exhausted": ["01001a"]}),
    _c("hf344 Boost : TEMOIN, meme attaque, meme defenseur, avec une carte de boost sans effet : le heros reste PRET",
       "contre-cas : la defense de l'allie n'incline pas le heros", [HEROS, "Puzzle.PutIntoPlay('01002', under_control=True)"] + deck("01105"), ["Puzzle.Attack('hf501a', '01002')"],
       {"pret": ["01001a"]}),
    _c("hf344 Boost : TEMOIN, en forme ALTER-EGO rien n'est incline (pas de heros)",
       "« your HERO »", deck("01105"), ["Puzzle.Boost('hf344')"], {"pret": ["01001b"]}),
    _c("hf345 Mind Over Matter (2e exemplaire) : meme effet (revele l'attachement de la defausse)",
       "meme script que hf344", deck("hf345", "01105") + ["Puzzle.EmptyEncounterDiscardPile()", "Puzzle.CreateEncounterDiscardPile('hf303')"], ["Puzzle.Reveal('hf345')"],
       {"en_jeu": ["hf303"]}),
    _c("hf346 Matter Manipulation : defausse Helicarrier (soutien, cout 3) et met en jeu un soutien MOINS CHER du deck (Aunt May, cout 1)",
       "« Discard a card you control, then search your deck and discard pile for a card of the same type but with a resource cost less than ... and put that card into play »",
       deck("hf346", "01105") + ["Puzzle.PutIntoPlay('01092', under_control=True)", "Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01006', '01089')"], ["Puzzle.Reveal('hf346')"],
       {"absents": ["01092"], "en_jeu": ["01006"], "defausse": ["01092"]}, accepter_choix=True),
    _c("hf346 Matter Manipulation : la recherche couvre aussi la DEFAUSSE du joueur (Aunt May y est)",
       "« your deck and discard pile »", deck("hf346", "01105") + ["Puzzle.PutIntoPlay('01092', under_control=True)", "Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDiscardPile('01006')"],
       ["Puzzle.Reveal('hf346')"], {"en_jeu": ["01006"]}, accepter_choix=True),
    _c("hf346 Matter Manipulation : TEMOIN, aucune carte MOINS CHERE du meme type (un autre Helicarrier, cout 3, n'est pas < 3) -> defaussee quand meme, la carte gagne surge",
       "« less than » STRICT ; « Otherwise, this card gains surge » : la carte suivante (Psychic Bulwark) est revelee",
       deck("hf346", "hf507", "01105") + ["Puzzle.PutIntoPlay('01092', under_control=True)", "Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01092')"], ["Puzzle.Reveal('hf346')"],
       {"absents": ["01092"], "en_jeu": ["hf507"]}, accepter_choix=True),
    _c("hf346 Matter Manipulation : TEMOIN, un AUTRE TYPE moins cher (une amelioration Spider-Tracer, cout 1) n'est pas du meme type qu'un soutien -> surge",
       "« of the same type »", deck("hf346", "hf507", "01105") + ["Puzzle.PutIntoPlay('01092', under_control=True)", "Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01007')"],
       ["Puzzle.Reveal('hf346')"], {"absents": ["01007"], "en_jeu": ["hf507"]}, accepter_choix=True),
    _c("hf346 Matter Manipulation : sans carte controlee la carte gagne surge",
       "« Discard a card you control ... Otherwise, this card gains surge »", deck("hf346", "hf507", "01105"), ["Puzzle.Reveal('hf346')"], {"en_jeu": ["hf507"]}),
    _c("hf346 Matter Manipulation : une carte de cout 0 (Energy Channel) defaussee -> aucune carte moins chere possible -> surge",
       "cout 0 : « less than 0 » est impossible", deck("hf346", "hf507", "01105") + ["Puzzle.PutIntoPlay('01018', under_control=True)", "Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01018')"],
       ["Puzzle.Reveal('hf346')"], {"en_jeu": ["hf507"]}, accepter_choix=True),
    _c("hf347 Matter Manipulation (2e exemplaire) : meme effet", "meme script que hf346",
       deck("hf347", "01105") + ["Puzzle.PutIntoPlay('01092', under_control=True)", "Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01006')"], ["Puzzle.Reveal('hf347')"],
       {"en_jeu": ["01006"], "absents": ["01092"]}, accepter_choix=True),
    _c("hf348 Matter Manipulation (3e exemplaire) : meme effet", "meme script que hf346",
       deck("hf348", "01105") + ["Puzzle.PutIntoPlay('01092', under_control=True)", "Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01006')"], ["Puzzle.Reveal('hf348')"],
       {"en_jeu": ["01006"], "absents": ["01092"]}, accepter_choix=True),
    # ===================================================================== MODULE IMMENSITY
    _c("hf351 sbire : PV 2, ATQ 3, MNG 3, Steady, ELITE HELLFIRE PSIONIC",
       "nombres texte <-> code (scan)", deck("01105"), ["Puzzle.PutIntoPlay('hf351')"],
       {"en_jeu": ["hf351"], "vie": [["hf351", 2]], "attaque": [["hf351", 3]], "steady": ["hf351"], "trait_de": [["hf351", "ELITE", True], ["hf351", "HELLFIRE", True], ["hf351", "PSIONIC", True]]}),
    _c("hf351 When Revealed : cherche le manteau (Cassandra's Telepathic Cloak) dans le deck de rencontre et le met en jeu, attache a elle",
       "« Find the Cassandra's Telepathic Cloak attachment and put it into play »", deck("hf351", "hf354", "01105"), ["Puzzle.Reveal('hf351')"],
       {"en_jeu": ["hf351", "hf354"], "attache": [["hf354", "hf351"]]}),
    _c("hf351 When Revealed : le manteau peut etre dans la DEFAUSSE de rencontre",
       "« Find » : toutes les zones", deck("hf351", "01105") + ["Puzzle.EmptyEncounterDiscardPile()", "Puzzle.CreateEncounterDiscardPile('hf354')"], ["Puzzle.Reveal('hf351')"],
       {"en_jeu": ["hf351", "hf354"], "attache": [["hf354", "hf351"]]}),
    _c("hf351 When Revealed : sans manteau nulle part, elle entre quand meme en jeu (rien d'autre ne se passe)",
       "« Find » : rien a trouver", deck("hf351", "01105"), ["Puzzle.Reveal('hf351')"], {"en_jeu": ["hf351"], "absents": ["hf354"]}),
    _c("hf351 Boost : « Put Cassandra Nova into play engaged with you » : Emma s'active (boost) et Cassandra arrive engagee",
       "(modele 01121)", deck("hf351", "01105"), ["Puzzle.Boost('hf351')"], {"en_jeu": ["hf351"], "engages": ["hf351"]}),
    _c("hf352 Illusory Duty : defausse 3 cartes ; une OBLIGATION defaussee (Narrow Minded) est REVELEE ; la carte ne quitte pas la partie",
       "« Discard 3 cards from the top of the encounter deck. Reveal each obligation discarded in this way »", deck("hf352", "01105", "hf357", "01105", "01105"), ["Puzzle.Reveal('hf352')"],
       {"en_jeu": ["hf357"], "defausse_rencontre_ids": ["01105", "hf352", "01105"]}),
    _c("hf352 Illusory Duty : AUCUNE obligation dans les 3 cartes -> cherche l'obligation du JOUEUR (Eviction Notice) dans le deck, la revele et RETIRE Illusory Duty de la partie",
       "« search the encounter deck, discard pile, set-aside area, and removed-from-game area for a copy of your obligation, then reveal it and remove this card from the game » (lecture : voir QUESTIONS.md)",
       deck("hf352", "01105", "01105", "01105", "01165"), ["Puzzle.Reveal('hf352')"],
       {"hors_deck_rencontre": ["01165"], "exhausted": ["01001b"], "absents": ["hf352"], "defausse_rencontre_ids": ["01105", "01105", "01105"]}, accepter_choix=True),
    _c("hf352 Illusory Duty : l'obligation du joueur peut aussi etre dans la DEFAUSSE de rencontre",
       "« discard pile »", deck("hf352", "01105", "01105", "01105") + ["Puzzle.EmptyEncounterDiscardPile()", "Puzzle.CreateEncounterDiscardPile('01165')"], ["Puzzle.Reveal('hf352')"],
       {"exhausted": ["01001b"], "absents": ["hf352"]}, accepter_choix=True),
    _c("hf352 Illusory Duty : TEMOIN, une obligation parmi les 3 cartes -> on ne cherche PAS la sienne (Eviction Notice reste dans le deck)",
       "la branche de recherche ne part que sans obligation revelee", deck("hf352", "hf357", "01105", "01105", "01165"), ["Puzzle.Reveal('hf352')"],
       {"en_jeu": ["hf357"], "pret": ["01001b"], "deck_rencontre_contient": ["01165"]}, accepter_choix=True),
    _c("hf353 Mental Paralysis revelee : le joueur est Sonne ET Desoriente (alter-ego), la carte a Surge",
       "« Surge. When Revealed : You are stunned and confused » : Surge natif (le harnais joue l'ancienne regle : la carte suivante, Illusion Unraveled, est revelee tout de suite)", deck("hf353", "hf307", "hf307"), ["Puzzle.Reveal('hf353')"],
       {"statuts": [["01001b", "Stunned"], ["01001b", "Confused"]], "en_jeu": ["hf307"]}),
    _c("hf353 Boost : « You are stunned and confused » : Emma s'active (Mental Paralysis en boost), le joueur est Sonne et Desoriente",
       "boost de l'activation du vilain (3 icones : Mental Paralysis porte 3 icones de boost)", deck("01105"), ["Puzzle.Boost('hf353')"],
       {"statuts": [["01001b", "Stunned"], ["01001b", "Confused"]]}),
    _c("hf354 Cloak revelee, Cassandra DEJA en jeu : s'attache a elle ; « cannot take any amount of damage » : 2 degats sur Cassandra (2 PV) -> aucun degat, elle reste en jeu",
       "« Cassandra Nova cannot take any amount of damage » : `UnitCannotTakeDamage`", deck("hf354", "01105") + ["Puzzle.PutIntoPlay('hf351')"],
       ["Puzzle.Reveal('hf354')", "Puzzle.Damage('hf351', 2)"],
       {"attache": [["hf354", "hf351"]], "en_jeu": ["hf351"], "degats_de": [["hf351", 0]]}),
    _c("hf354 Cassandra Nova : TEMOIN, sans le manteau 2 degats la VAINCRAIENT",
       "contre-cas", deck("01105") + ["Puzzle.PutIntoPlay('hf351')"], ["Puzzle.Damage('hf351', 2)"], {"absents": ["hf351"]}),
    _c("hf354 Cloak revelee, Cassandra ABSENTE : la cherche dans le Hellfire deck, la REVELE et s'attache a elle",
       "« If she is not in play, find Cassandra Nova, reveal her, and then attach this card on her »", deck("hf354", "01105") + ["Puzzle.EmptyHellfireDeck()", "Puzzle.PutIntoHellfireDeck('hf351')"],
       ["Puzzle.Reveal('hf354')"], {"en_jeu": ["hf351", "hf354"], "attache": [["hf354", "hf351"]], "hellfire_deck": []}),
    _c("hf354 Reponse forcee : apres l'attaque de Cassandra contre le joueur, le manteau est defausse : 1 degat PREVENU avant l'attaque, 1 degat SUBI apres (le manteau ne protege plus)",
       "« After Cassandra Nova attacks you, discard this card » : Cassandra (2 PV) a 0 degat apres le 1er coup (manteau), 1 degat apres le 2e (plus de manteau)",
       [HEROS] + deck("hf354", "01105") + ["Puzzle.PutIntoPlay('hf351')"],
       ["Puzzle.Reveal('hf354')", "Puzzle.Damage('hf351', 1)", "Puzzle.Attack('hf351')", "Puzzle.Damage('hf351', 1)"],
       {"absents": ["hf354"], "en_jeu": ["hf351"], "degats_de": [["hf351", 1]]}),
    _c("hf354 Reponse forcee : TEMOIN, l'attaque d'un AUTRE sbire ne defausse pas le manteau",
       "« After CASSANDRA NOVA attacks you »", [HEROS] + deck("hf354", "01105") + ["Puzzle.PutIntoPlay('hf351')", "Puzzle.PutIntoPlay('hf313')"],
       ["Puzzle.Reveal('hf354')", "Puzzle.Attack('hf313')"], {"en_jeu": ["hf354"]}),
    _c("hf355 Jumpstart revelee : s'attache au sbire aux PV IMPRIMES les plus hauts (Hellfire Pawn 3 contre Weapons Runner 1) ; +2 SCH",
       "« Attach to the highest hit-point minion » ; `desc.SCH+ = 2` (le Pawn : SCH 1 + 2 = 3)", deck("hf355", "01105") + ["Puzzle.PutIntoPlay('hf313')", "Puzzle.PutIntoPlay('01121')"],
       ["Puzzle.Reveal('hf355')"], {"attache": [["hf355", "hf313"]]}),
    _c("hf355 Jumpstart : sans sbire en jeu, la carte gagne surge (la carte suivante, Psychic Bulwark, est revelee)",
       "« Otherwise, this gains surge »", deck("hf355", "hf507", "01105"), ["Puzzle.Reveal('hf355')"], {"en_jeu": ["hf507"], "absents": ["hf355"]}),
    _c("hf355 Interruption forcee : l'attaque du sbire VILLAINOUS (Black Bishop ATQ 1) contre le joueur recoit 1 carte de BOOST de plus : 2 cartes de 3 icones -> 1 + 3 + 3 = 7 degats a l'alter-ego",
       "« When the attached character attacks you, give them 1 additional boost card for this activation » : le sbire Villainous recoit deja 1 carte ; Psionic Active (3 icones, aucun effet de boost) x2 ; Jumpstart s'attache au PLUS haut PV imprime (Black Bishop 7)",
       ["Puzzle.PutIntoPlay('hf311')"] + deck("hf355", "hf120", "hf120", "01105") + ["Puzzle.Reveal('hf355')"], ["Puzzle.Attack('hf311')"],
       {"attache": [["hf355", "hf311"]], "degats_identite": 7}),
    _c("hf355 Interruption forcee : TEMOIN, sans Jumpstart la meme attaque ne recoit que la carte de boost du Villainous (1 + 3 = 4 degats)",
       "contre-cas", ["Puzzle.PutIntoPlay('hf311')"] + deck("hf120", "hf120", "01105"), ["Puzzle.Attack('hf311')"], {"degats_identite": 4}),
    _c("hf355 Boost : « Deal yourself 1 facedown encounter card » : Emma s'active (Jumpstart en boost), le joueur recoit 1 carte face cachee",
       "boost de l'activation du vilain", deck("01105"), ["Puzzle.Boost('hf355')"], {"distribuees": 1}),
    _c("hf356 Jumpstart (2e exemplaire) : meme effet (s'attache au sbire aux PV les plus hauts)",
       "meme script que hf355", deck("hf356", "01105") + ["Puzzle.PutIntoPlay('hf313')", "Puzzle.PutIntoPlay('01121')"], ["Puzzle.Reveal('hf356')"], {"attache": [["hf356", "hf313"]]}),
    _c("hf357 Narrow Minded : Action d'alter-ego, incliner l'identite -> la carte est defaussee",
       "« Alter-Ego Action : Exhaust your identity -> discard this card »", deck("hf357", "01105") + ["Puzzle.Reveal('hf357')"], ["Puzzle.Action('hf357', 'AlterEgoAction')"],
       {"absents": ["hf357"], "exhausted": ["01001b"]}, accepter_choix=True),
    _c("hf357 Narrow Minded : icone AMPLIFY (`desc.Amplify`) : 1 icone Amplify en jeu une fois revelee",
       "l'icone (avion + croix) est Amplify (livret p.4) ; `HasAmplify` ajoute au type Obligation (moteur)", deck("hf357", "01105") + ["Puzzle.Reveal('hf357')"], [],
       {"en_jeu": ["hf357"], "icones": [["Amplify", 1]]}),
    _c("hf358 Narrow Minded (2e exemplaire) : meme effet (Action d'alter-ego, incliner -> defaussee)",
       "meme script que hf357", deck("hf358", "01105") + ["Puzzle.Reveal('hf358')"], ["Puzzle.Action('hf358', 'AlterEgoAction')"],
       {"absents": ["hf358"], "exhausted": ["01001b"]}, accepter_choix=True),

    # ===================================================================== le sbire White Queen de Perfection dans CE scenario (correctif de hellfire_hunt_white_queen)
    _c("hf301 White Queen (sbire de Perfection) : au scenario 4 le vilain est Emma Frost -> le sbire ENTRE en jeu normalement (aucune carte distribuee)",
       "« When a White Queen minion attempts to enter play, give the engaged player a facedown encounter card and discard this card » : carte UNIQUE, ne vaut que si le VILAIN White Queen est en jeu (scenario 1)",
       deck("hf301", "01105", "01105"), ["Puzzle.Reveal('hf301')"],
       {"en_jeu": ["hf301"], "distribuees": 0, "engages": ["hf301"]}),
    # ===================================================================== carnet de campagne : releve de fin de victoire
    _c("hf503a CARNET SORTANT a la victoire : les allies Recruited en jeu, dans un deck/defausse de joueur, dans le deck ou la defausse Recruited Mutants sont NOTES ; celui qui reste de cote ne l'est pas",
       "livret p.14 : « Shuffle each RECRUITED ally in each player's deck and discard pile into the Recruited Mutants deck. Record the name of each ... ally in the Recruited Mutants Deck » ; chemin REEL : `Puzzle.Win()` -> `WriteCampaignLogAtGameOver(ReleveTorn)` -> fichier de carnet",
       [HEROS, "Puzzle.CreatePlayerDiscardPile('hf013')", "Puzzle.PutIntoRecruitedMutants('hf014')", "Puzzle.PutIntoRecruitedMutants('hf015', discard=True)",
        "Puzzle.PutIntoPlay('hf016', under_control=True)", "Puzzle.CreatePlayerDeck('hf018')"] + deck("01105"), ["Puzzle.Win()"],
       {"gagnee": True, "scenario": "hellfire_torn", "cles_presentes": ["Recruited Allies", "Removed Potential Allies"], "cles": {"Recruited Allies": "hf013;hf014;hf015;hf016;hf018"}},
       campagne=True, libre=True, verifier="fnefin_carnet_sortant"),
    _c("hf503a CARNET SORTANT a la DEFAITE : aucun allie n'est note (on rejoue sans penalite) ; l'estampille reste celle du scenario",
       "livret p.5 : « If the players lost, they may reset the scenario and try again with no penalty »",
       [HEROS, "Puzzle.PutIntoPlay('hf016', under_control=True)"] + deck("01105"), ["Puzzle.Lose()"],
       {"gagnee": False, "scenario": "hellfire_torn", "cles_absentes": ["Recruited Allies"]}, campagne=True, libre=True, verifier="fnefin_carnet_sortant"),

    _c("hf503b A DEUX JOUEURS : chaque joueur sans sbire ELITE HELLFIRE engage revele une carte du Hellfire deck, dans l'ordre des joueurs (2 sbires reveles)",
       "« in player order, each player not engaged with an ELITE, HELLFIRE minion reveals the top card of the Hellfire deck »",
       ["Puzzle.EmptyHellfireDeck()", "Puzzle.PutIntoHellfireDeck('hf341', 'hf351')"] + deck("01105"), ["Puzzle.BeginPlayerPhase()"],
       {"en_jeu": ["hf341", "hf351"], "hellfire_deck": []}, heros2="hawkeye"),
    _c("hf503b A DEUX JOUEURS : un joueur DEJA engage avec un sbire ELITE HELLFIRE ne revele pas ; l'autre revele (une seule carte revelee)",
       "chaque joueur est jugé pour LUI-MEME : seul le joueur 2 revele", ["Puzzle.EmptyHellfireDeck()", "Puzzle.PutIntoHellfireDeck('hf341')", "Puzzle.PutIntoPlay('hf351')"] + deck("01105"),
       ["Puzzle.BeginPlayerPhase()"], {"en_jeu": ["hf341", "hf351"], "hellfire_deck": []}, heros2="hawkeye"),

    _c("hf501b INTEGRATION (phase du mechant jouee en entier) : vaincue pendant la phase des joueurs -> face infinie ; la phase du mechant ne lui fait rien attaquer (2 cartes defaussees a la place), puis elle revient pleine : la menace du complot : 1 -> 0 par l'interruption de defaite, puis +1 d'escalade = 1 (alter-ego : une Emma qui manigancerait la ferait monter de plus)",
       "enchainement reel : `Puzzle.RunVillainPhase()` (menace, activations, cartes rencontre) puis `Puzzle.EndVillainPhase()` (retournement et remise des PV) ; filler inerte hf307 (01105 gagne surge sans Rhino : chaine de renforts)",
       deck("hf307", "hf307", "hf307", "hf307", "hf307", "hf307", "hf307", "hf307", remplissage=0), ["Puzzle.Damage('hf501a', 7)", "Puzzle.RunVillainPhase()", "Puzzle.EndVillainPhase()"],
       {"en_jeu": ["hf501a"], "absents": ["hf501b"], "degats_de": [["hf501a", 0]], "menace_de": [["hf503b", 1]]}),
]

VERIFICATIONS = r'''
def hft_etat(monde, aides):
    """Extensions de `etat_attendu` (meme famille que bb_etat) : compteurs_sur [[id, nom, n]], menace_de [[id, n]], attaque [[id, n]], vie [[id, pv_max]],
    degats_de [[id, n]], statuts_sur [[id, 'stunned'|'tough'|'confused', n]], absents [ids hors jeu], trait_de [[id, TRAIT, bool]],
    attache [[carte, hote]], boosts_de [[id, n]] (cartes de boost face cachee sur la carte), le reste va a etat_attendu."""
    attendu = aides["cas"].get("attendu") or {}
    # FILET (26/10/2026) : le moteur AVALE les exceptions des scripts de cartes (PROCESSUS-CARTE etape 7, point 6) ; un cas ne doit donc JAMAIS passer
    # au vert si le journal contient une trace d'exception.
    try:
        import os as _os
        _journal = open(f"/tmp/capacites_{_os.environ.get('CAS_PREFIX', '')}{aides['index']}.log", encoding="utf-8", errors="replace").read()
        _trace = [l for l in _journal.splitlines() if "Traceback" in l]
    except Exception:
        _trace = []
    propres = ("compteurs_sur", "menace_de", "attaque", "vie", "degats_de", "statuts_sur", "absents", "trait_de", "attache", "boosts_de", "steady", "acceleration", "gagnee", "partie_finie", "nb_en_jeu", "distribuees", "hors_deck_rencontre", "peut_defendre", "hote_pic", "hellfire_deck", "hellfire_defausse", "hellfire_total", "engages", "defausse_rencontre_ids", "deck_rencontre_contient", "dans_victoire", "garde", "patrouille", "releve_torn", "releve_torn_vide")
    reste = {k: v for k, v in attendu.items() if k not in propres}
    copie = dict(aides); copie["cas"] = dict(aides["cas"]); copie["cas"]["attendu"] = reste
    ok, msg = etat_attendu(monde, copie)
    soucis = [] if ok else [msg]
    if _trace:
        soucis.append("le journal contient une exception avalee par le moteur (Traceback)")
    par_id = aides["par_id"]
    def face(cid):
        f = par_id(monde, cid)
        if f is None:
            soucis.append(f"{cid} n'est pas en jeu")
        return f
    for cid, hote in attendu.get("attache", []):
        f = face(cid)
        if f is not None:
            b = f.bind_face
            got = getattr(getattr(b, "paper", None), "card_id", None) if b else None
            if got != hote:
                soucis.append(f"{cid} attache a {got} (attendu {hote})")
    for cid, nom, n in attendu.get("compteurs_sur", []):
        f = face(cid)
        if f is not None and f.GetCounters(nom) != n:
            soucis.append(f"{cid} compteurs {nom} = {f.GetCounters(nom)} (attendu {n})")
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
    for cid, n in attendu.get("degats_de", []):
        f = face(cid)
        if f is not None and (f.max_health - f.health) != n:
            soucis.append(f"{cid} degats = {f.max_health - f.health} (attendu {n})")
    for cid, st, n in attendu.get("statuts_sur", []):
        f = face(cid)
        if f is not None and getattr(f, st) != n:
            soucis.append(f"{cid} statut {st} = {getattr(f, st)} (attendu {n})")
    for cid in attendu.get("absents", []):
        if par_id(monde, cid) is not None:
            soucis.append(f"{cid} est encore en jeu")
    for cid, tr, b in attendu.get("trait_de", []):
        f = face(cid)
        if f is not None and bool(f.HasTrait(tr)) != b:
            soucis.append(f"{cid} trait {tr} = {f.HasTrait(tr)} (attendu {b})")
    for cid, n in attendu.get("boosts_de", []):
        f = face(cid)
        if f is not None:
            vus = f.components.boostable.GetDeck().GetSize()
            if vus != n:
                soucis.append(f"{cid} cartes de boost = {vus} (attendu {n})")
    for cid, n in attendu.get("acceleration", []):
        f = face(cid)
        if f is not None and f.acceleration_token != n:
            soucis.append(f"{cid} jetons d'acceleration = {f.acceleration_token} (attendu {n})")
    if "partie_finie" in attendu and bool(getattr(monde, "is_game_over", False)) != attendu["partie_finie"]:
        soucis.append(f"partie finie = {getattr(monde, 'is_game_over', False)} (attendu {attendu['partie_finie']})")
    if "gagnee" in attendu:
        fini = bool(getattr(monde, "is_game_over", False))
        gagne = fini and bool(monde.game_over.players_won)
        if gagne != attendu["gagnee"]:
            soucis.append(f"partie gagnee = {gagne} (attendu {attendu['gagnee']})")
    for cid, voulu in attendu.get("nb_en_jeu", []):
        total = 0
        for objet in monde.object_manager.card_dict.values():
            f = getattr(objet, "face", None) or objet
            if getattr(getattr(f, "paper", None), "card_id", None) == cid and f.IsInPlay():
                total += 1
        if total != voulu:
            soucis.append(f"{total} exemplaire(s) de {cid} en jeu (attendu {voulu})")
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
    for ally, attaquant, voulu in attendu.get("peut_defendre", []):
        f, a = face(ally), face(attaquant)
        if f is not None and a is not None and bool(f.IsCanDefense(a)) != voulu:
            soucis.append(f"{ally} peut defendre contre {attaquant} = {f.IsCanDefense(a)} (attendu {voulu})")
    for cid, pic in attendu.get("hote_pic", []):
        f = face(cid)
        if f is not None:
            hote = f.bind_face
            vu = getattr(hote, "pic_id", None) if hote else None
            if vu != pic:
                soucis.append(f"{cid} est attache a une carte d'image {vu} (attendu {pic})")
    for cid in attendu.get("steady", []):
        f = face(cid)
        if f is not None and not f.IsSteady():
            soucis.append(f"{cid} n'est pas Steady")

    # ---- cles propres au pack Torn (hft_etat) -------------------------------------------------------------------------------------------------
    def _ids(faces):
        return sorted(getattr(f.paper, "card_id", "?") for f in faces)
    def _hf():
        etat = getattr(monde, "hf_hellfire", None)
        if etat is None:
            return [], []
        return list(etat[0].Get(True)), list(etat[1].Get(True))
    if "hellfire_deck" in attendu:
        vus = _ids(_hf()[0])
        if vus != sorted(attendu["hellfire_deck"]):
            soucis.append(f"deck Hellfire = {vus} (attendu {sorted(attendu['hellfire_deck'])})")
    if "hellfire_defausse" in attendu:
        vus = _ids(_hf()[1])
        if vus != sorted(attendu["hellfire_defausse"]):
            soucis.append(f"defausse Hellfire = {vus} (attendu {sorted(attendu['hellfire_defausse'])})")
    if "hellfire_total" in attendu:
        engages_elite = [m for j in monde.players for m in j.GetEngagedMinions() if m.HasTrait("ELITE") and m.HasTrait("HELLFIRE")]
        vus = _ids(_hf()[0] + _hf()[1] + engages_elite)
        if vus != sorted(attendu["hellfire_total"]):
            soucis.append(f"sbires ELITE HELLFIRE (deck + defausse + engages) = {vus} (attendu {sorted(attendu['hellfire_total'])})")
    for cid in attendu.get("engages", []):
        engages = [getattr(m.paper, "card_id", None) for j in monde.players for m in j.GetEngagedMinions()]
        if cid not in engages:
            soucis.append(f"{cid} n'est engage avec aucun joueur (engages : {engages})")
    if "defausse_rencontre_ids" in attendu:
        from game.operate.worlds import Worlds
        vus = _ids(Worlds.GetEncounterDiscardPileCards(monde))
        if vus != sorted(attendu["defausse_rencontre_ids"]):
            soucis.append(f"defausse de rencontre = {vus} (attendu {sorted(attendu['defausse_rencontre_ids'])})")
    if "releve_torn" in attendu or attendu.get("releve_torn_vide"):
        releve = getattr(monde, "hft_releve", None)
        if releve is None:
            soucis.append("aucun releve de campagne calcule")
        elif attendu.get("releve_torn_vide"):
            if releve:
                soucis.append(f"le releve devait etre VIDE (defaite) : {releve}")
        else:
            voulu = attendu["releve_torn"]
            vus = sorted(i for i in str(releve.get("Recruited Allies", "")).split(";") if i)
            if vus != sorted(voulu):
                soucis.append(f"allies Recruited notes = {vus} (attendu {sorted(voulu)})")
    for cid in attendu.get("garde", []):
        f = face(cid)
        if f is not None and not f.IsGuard():
            soucis.append(f"{cid} n'a pas Guard")
    for cid in attendu.get("patrouille", []):
        f = face(cid)
        if f is not None and not f.IsPatrol():
            soucis.append(f"{cid} n'a pas Patrol")
    for cid in attendu.get("deck_rencontre_contient", []):
        from game.operate.worlds import Worlds
        if cid not in _ids(Worlds.GetEncounterDeckCards(monde)):
            soucis.append(f"{cid} n'est pas dans le deck de rencontre")
    for cid in attendu.get("dans_victoire", []):
        ok_v = False
        for objet in monde.object_manager.card_dict.values():
            f = getattr(objet, "face", None) or objet
            if getattr(getattr(f, "paper", None), "card_id", None) == cid and f.card.area.flags.is_victory_display:
                ok_v = True
        if not ok_v:
            soucis.append(f"{cid} n'est pas dans la pile de victoire")
    if soucis:
        return False, " ; ".join(soucis)
    return True, "etat conforme"
'''
