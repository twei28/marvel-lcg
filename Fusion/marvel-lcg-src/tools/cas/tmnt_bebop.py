# Cas test_capacites du scenario BEBOP & ROCKSTEADY (TMNT Villains v3, Inkwire, prefixe `tk`).
SC = "bebop_rocksteady"
SCX = "bebop_rocksteady_expert"
HEROS = "Puzzle.ChangeForm('01001a')"   # spider_man demarre en ALTER-EGO
SANS_BOOST = ["Puzzle.EmptyEncounterDeck()",
              "Puzzle.CreateEncounterDeck('01105', '01105', '01105', '01105', '01105', '01105', '01105', '01105')"]


def _c(nom, pourquoi, mise, declencher, attendu, **cle):
    if not cle.pop("avec_boost", False):
        mise = SANS_BOOST + list(mise)
    cas = {"nom": "[bebop] " + nom, "pourquoi": pourquoi, "scenario": cle.pop("scenario", SC),
           "heros": cle.pop("heros", "spider_man"), "mise_en_place": mise, "declencher": declencher,
           "verifier": cle.pop("verifier", "bb_etat"), "attendu": attendu}
    cas.update(cle)
    return cas


CAS = [
    _c("tk005a mise en place : deux vilains, environnement, annexe, deux Temper accroches",
       "Setup du complot : Bebop et Rocksteady en jeu, tk006a, tk101, Hog Wild sur Bebop, Rhino Rage sur Rocksteady",
       [], [],
       {"en_jeu": ["tk001a", "tk003a", "tk006a", "tk007a", "tk008a", "tk101"],
        "attache": [["tk007a", "tk001a"], ["tk008a", "tk003a"]]}),
    _c("tk007a Hog Wild : +1 ATK a Bebop par compteur knucklehead (2 compteurs -> ATK 2)",
       "« Bebop gets +1 ATK for each knucklehead counter here »",
       ["Puzzle.Counter('tk007a', 'knucklehead', 2)"], [],
       {"attaque": [["tk001a", 2]], "compteurs_sur": [["tk007a", "knucklehead", 2]]}),
    _c("tk007a Hog Wild : sans compteur, ATK 0 (ligne de base)",
       "contre-cas : Bebop A1 a ATK 0",
       [], [], {"attaque": [["tk001a", 0]]}),
    _c("tk007a Hog Wild : Special = 1 compteur (apres 1 degat sur Bebop)",
       "Reponse Forcee de tk001a : resoudre le Special du Temper",
       ["Puzzle.Damage('tk001a', 1)"], [],
       {"compteurs_sur": [["tk007a", "knucklehead", 1]], "degats": [["tk001a", 1]]}),
    _c("tk007a Hog Wild : a 3 compteurs il se retourne sur Headfirst (ENRAGED, +3 ATK, trait ENRAGED au vilain)",
       "« If there are at least 3 knucklehead counters here, flip this card to its ENRAGED side »",
       ["Puzzle.Counter('tk007a', 'knucklehead', 2)"], ["Puzzle.Damage('tk001a', 1)"],
       {"en_jeu": ["tk007b"], "absents": ["tk007a"], "attache": [["tk007b", "tk001a"]],
        "compteurs_sur": [["tk007b", "knucklehead", 3]], "trait_de": [["tk001a", "ENRAGED", True]],
        "attaque": [["tk001a", 3]]}),
]

CAS += [
    # ===================================================================== villains ALERT : phase du mechant
    _c("tk001a Bebop ALERT : debut de phase, sans compteur -> 1 menace sur le complot (et Rocksteady : 1 degat)",
       "« remove 1 knucklehead counter ... or place 1 threat on the main scheme » : aucun compteur, seule l'option menace reste",
       [], ["Puzzle.BeginVillainPhase()"],
       {"menace_de": [["tk005b", 1]], "degats_identite": 1}),
    _c("tk001a Bebop ALERT : debut de phase avec compteurs -> retire 1 compteur (option par defaut), pas de menace",
       "option 1 offerte seulement s'il y a un compteur ; le pilote prend la premiere option",
       ["Puzzle.Counter('tk007a', 'knucklehead', 2)"], ["Puzzle.BeginVillainPhase()"],
       {"compteurs_sur": [["tk007a", "knucklehead", 1]], "menace_de": [["tk005b", 0]]}),
    _c("tk001a Bebop ALERT : le choix « menace » est possible meme avec des compteurs",
       "les deux options ouvertes : on force la seconde",
       ["Puzzle.Counter('tk007a', 'knucklehead', 2)"], ["Puzzle.BeginVillainPhase()"],
       {"compteurs_sur": [["tk007a", "knucklehead", 2]], "menace_de": [["tk005b", 1]]},
       choisir_option="Place_1_threat_on_the_main_scheme"),
    _c("tk002a Bebop ALERT (expert) : 2 menaces sur le complot",
       "stade B1 : « place 2 threat on the main scheme »",
       [], ["Puzzle.BeginVillainPhase()"],
       {"menace_de": [["tk005b", 2]]}, scenario=SCX),
    _c("tk003a Rocksteady ALERT : debut de phase -> carte Robuste + 1 degat au premier joueur (aucun compteur)",
       "« give Rocksteady a tough status card. Remove 1 counter ... or deal 1 damage to the first player »",
       [], ["Puzzle.BeginVillainPhase()"],
       {"degats_identite": 1, "statuts_sur": [["tk003a", "tough", 1]]}),
    _c("tk003a Rocksteady ALERT : avec un compteur Rhino Rage -> le retire (defaut), aucun degat",
       "option 1 (compteur) offerte et prise par defaut",
       ["Puzzle.Counter('tk008a', 'knucklehead', 1)"], ["Puzzle.BeginVillainPhase()"],
       {"compteurs_sur": [["tk008a", "knucklehead", 0]], "degats_identite": 0, "statuts_sur": [["tk003a", "tough", 1]]}),
    _c("tk004a Rocksteady ALERT (expert) : 2 degats au premier joueur",
       "stade B1 : « deal 2 damage to the first player »",
       [], ["Puzzle.BeginVillainPhase()"],
       {"degats_identite": 2}, scenario=SCX),
    # ===================================================================== Reponse Forcee « apres avoir subi des degats »
    _c("tk003a Rocksteady ALERT : apres 1 degat, Special de Rhino Rage = 1 compteur",
       "« After Rocksteady takes damage, resolve the Special ability on the RHINO attachment »",
       ["Puzzle.Damage('tk003a', 1)"], [],
       {"compteurs_sur": [["tk008a", "knucklehead", 1]]}),
    _c("tk003a Rocksteady ALERT : une Reponse par EVENEMENT de degats (2 evenements -> 2 compteurs)",
       "chaque instance de degats declenche la Reponse Forcee",
       [], ["Puzzle.Damage('tk003a', 1)", "Puzzle.Damage('tk003a', 1)"],
       {"compteurs_sur": [["tk008a", "knucklehead", 2]]}),
    _c("tk001b Bebop K.O. : PAS de Reponse Forcee (le texte n'est imprime que sur la face ALERT)",
       "contre-cas : Bebop K.O. blesse -> Hog Wild ne recoit rien",
       ["Puzzle.Flip('tk001a')"], ["Puzzle.Damage('tk001b', 1)"],
       {"compteurs_sur": [["tk007a", "knucklehead", 0]]}),
    # ===================================================================== villains K.O.
    _c("tk001b Bebop K.O. : activation = retire 1 compteur a la place (pas d'attaque), reste K.O. s'il en reste",
       "« When Bebop activates, remove 1 knucklehead counter from the HOG attachment instead »",
       ["Puzzle.Counter('tk007a', 'knucklehead', 2)", "Puzzle.Flip('tk001a')", "Puzzle.Exhaust('01001a')"],
       ["Puzzle.Attack('tk001b')"],
       {"en_jeu": ["tk001b"], "compteurs_sur": [["tk007a", "knucklehead", 1]], "degats_identite": 0}),
    _c("tk001b Bebop K.O. : dernier compteur retire -> se retourne sur ALERT",
       "« If there are no knucklehead counters there, flip Bebop to his ALERT side » : lecture sequentielle (retire puis teste)",
       ["Puzzle.Counter('tk007a', 'knucklehead', 1)", "Puzzle.Flip('tk001a')", "Puzzle.Exhaust('01001a')"],
       ["Puzzle.Attack('tk001b')"],
       {"en_jeu": ["tk001a"], "absents": ["tk001b"], "compteurs_sur": [["tk007a", "knucklehead", 0]], "degats_identite": 0}),
    _c("tk001b Bebop K.O. : sans aucun compteur, l'activation le reveille aussi",
       "« If there are no knucklehead counters there » : zero compteur au depart",
       ["Puzzle.Flip('tk001a')", "Puzzle.Exhaust('01001a')"], ["Puzzle.Attack('tk001b')"],
       {"en_jeu": ["tk001a"], "absents": ["tk001b"], "degats_identite": 0}),
    _c("tk002b Bebop K.O. (expert) : retire 2 compteurs",
       "stade B2 : « remove 2 knucklehead counters »",
       ["Puzzle.Counter('tk007a', 'knucklehead', 3)", "Puzzle.Flip('tk002a')", "Puzzle.Exhaust('01001a')"],
       ["Puzzle.Attack('tk002b')"],
       {"compteurs_sur": [["tk007a", "knucklehead", 1]], "en_jeu": ["tk002b"]}, scenario=SCX),
    _c("tk003b Rocksteady K.O. : retire 1 compteur de Rhino Rage et reste K.O.",
       "meme mecanique que Bebop, sur l'attachement RHINO",
       ["Puzzle.Counter('tk008a', 'knucklehead', 2)", "Puzzle.Flip('tk003a')", "Puzzle.Exhaust('01001a')"],
       ["Puzzle.Attack('tk003b')"],
       {"compteurs_sur": [["tk008a", "knucklehead", 1]], "en_jeu": ["tk003b"], "degats_identite": 0}),
    _c("tk004b Rocksteady K.O. (expert) : 2 compteurs d'un coup, 1 seul disponible -> se reveille",
       "« remove 2 ... » avec un seul compteur : on retire ce qu'il y a, puis ALERT",
       ["Puzzle.Counter('tk008a', 'knucklehead', 1)", "Puzzle.Flip('tk004a')", "Puzzle.Exhaust('01001a')"],
       ["Puzzle.Attack('tk004b')"],
       {"en_jeu": ["tk004a"], "compteurs_sur": [["tk008a", "knucklehead", 0]]}, scenario=SCX),
    _c("tk001b Bebop K.O. ET etourdi : le statut passe d'abord (la carte Etourdi est retiree, les compteurs restent)",
       "FAQ de l'encart : « Status cards always take priority... you would remove the stun status card instead »",
       ["Puzzle.Counter('tk007a', 'knucklehead', 2)", "Puzzle.Flip('tk001a')", "Puzzle.Stun('tk001b')", "Puzzle.Exhaust('01001a')"],
       ["Puzzle.Attack('tk001b')"],
       {"statuts_sur": [["tk001b", "stunned", 0]], "compteurs_sur": [["tk007a", "knucklehead", 2]]}),
]

CAS += [
    # ===================================================================== Temper ENRAGED : Headfirst / Headstrong
    _c("tk007b Headfirst : Special = 1 degat a l'identite (apres 1 degat sur Bebop), AUCUN compteur de plus",
       "« Special: Deal 1 damage to your identity » ; FAQ : pas de compteur quand le Temper est deja ENRAGED",
       ["Puzzle.Counter('tk007a', 'knucklehead', 3)", "Puzzle.Flip('tk007a')"], ["Puzzle.Damage('tk001a', 1)"],
       {"degats_identite": 1, "compteurs_sur": [["tk007b", "knucklehead", 3]]}),
    _c("tk008b Headstrong : Special = 1 menace sur le complot (apres 1 degat sur Rocksteady)",
       "« Special: Place 1 threat on the main scheme »",
       ["Puzzle.Counter('tk008a', 'knucklehead', 3)", "Puzzle.Flip('tk008a')"], ["Puzzle.Damage('tk003a', 1)"],
       {"menace_de": [["tk005b", 1]], "compteurs_sur": [["tk008b", "knucklehead", 3]]}),
    _c("tk007b Headfirst : +3 ATK a Bebop SEUL (Rocksteady ENRAGED absent) : Bebop attaque pour 3, rien ne se retourne",
       "contre-cas de l'Interruption : « if Headstrong is in play » est faux",
       ["Puzzle.Counter('tk007a', 'knucklehead', 3)", "Puzzle.Flip('tk007a')", "Puzzle.Exhaust('01001a')"],
       ["Puzzle.Attack('tk001a')"],
       {"degats_identite": 3, "en_jeu": ["tk001a", "tk003a", "tk007b"]}),
    _c("tk007b Headfirst : Bebop ENRAGED + Headstrong en jeu -> quand Bebop devrait s'activer, les deux vilains passent K.O., les deux Temper ROWDY",
       "« When Bebop would activate, if Headstrong is in play, flip Bebop and Rocksteady to their K.O. sides and flip both TEMPER attachments to their ROWDY sides »",
       ["Puzzle.Counter('tk007a', 'knucklehead', 3)", "Puzzle.Flip('tk007a')",
        "Puzzle.Counter('tk008a', 'knucklehead', 3)", "Puzzle.Flip('tk008a')", "Puzzle.Exhaust('01001a')"],
       ["Puzzle.Attack('tk001a')"],
       {"en_jeu": ["tk001b", "tk003b", "tk007a", "tk008a"], "absents": ["tk001a", "tk003a", "tk007b", "tk008b"],
        "compteurs_sur": [["tk008a", "knucklehead", 3]], "degats_identite": 0}),
    _c("tk007b Headfirst : l'activation qui declenche le retournement est une activation K.O. (1 compteur retire a Hog Wild)",
       "lecture retenue Q2 (bebop-questions.md) : Bebop est K.O. quand il s'active -> retire 1 compteur",
       ["Puzzle.Counter('tk007a', 'knucklehead', 3)", "Puzzle.Flip('tk007a')",
        "Puzzle.Counter('tk008a', 'knucklehead', 3)", "Puzzle.Flip('tk008a')", "Puzzle.Exhaust('01001a')"],
       ["Puzzle.Attack('tk001a')"],
       {"compteurs_sur": [["tk007a", "knucklehead", 2]]}),
    _c("tk008b Headstrong : Rocksteady ENRAGED s'active, Headfirst en jeu -> les deux vilains passent K.O.",
       "symetrique : « When Rocksteady would activate, if Headfirst is in play, flip ... »",
       ["Puzzle.Counter('tk007a', 'knucklehead', 3)", "Puzzle.Flip('tk007a')",
        "Puzzle.Counter('tk008a', 'knucklehead', 3)", "Puzzle.Flip('tk008a')", "Puzzle.Exhaust('01001a')"],
       ["Puzzle.Attack('tk003a')"],
       {"en_jeu": ["tk001b", "tk003b", "tk007a", "tk008a"], "compteurs_sur": [["tk007a", "knucklehead", 3], ["tk008a", "knucklehead", 2]]}),
    _c("tk008b Headstrong : Rocksteady ETOURDI et ENRAGED : la carte Etourdi passe d'abord, rien ne se retourne",
       "« Status cards always take priority »",
       ["Puzzle.Counter('tk007a', 'knucklehead', 3)", "Puzzle.Flip('tk007a')",
        "Puzzle.Counter('tk008a', 'knucklehead', 3)", "Puzzle.Flip('tk008a')", "Puzzle.Stun('tk003a')", "Puzzle.Exhaust('01001a')"],
       ["Puzzle.Attack('tk003a')"],
       {"en_jeu": ["tk001a", "tk003a", "tk007b", "tk008b"], "statuts_sur": [["tk003a", "stunned", 0]]}),
    # ===================================================================== Destructive Dunderheads
    _c("tk006a Dunderheads (Double Trouble) : les DEUX vilains s'activent contre le joueur (phase du mechant)",
       "« During step two of the villain phase, both villains activate against each player » : Bebop ATK 2 + Rocksteady ATK 2 + 2 de l'obligation de Spider-Man = 6 (le BASELINE sans tk006a : 4)",
       [HEROS, "Puzzle.Counter('tk007a', 'knucklehead', 2)", "Puzzle.Counter('tk008a', 'knucklehead', 1)", "Puzzle.Exhaust('01001a')"],
       ["Puzzle.RunVillainPhase()"],
       {"degats_identite": 6}),
    _c("tk006a Dunderheads : a DEUX joueurs, chaque vilain s'active contre CHAQUE joueur (+2 sur le premier joueur par rapport au BASELINE)",
       "« both villains activate against each player »",
       [HEROS, "Puzzle.Counter('tk007a', 'knucklehead', 2)", "Puzzle.Counter('tk008a', 'knucklehead', 1)", "Puzzle.Exhaust('01001a')"],
       ["Puzzle.RunVillainPhase()"],
       {"degats_identite": 7}, heros2="black_panther"),
    _c("tk006a Dunderheads : « the villain » -> le joueur choisit UN vilain (overkill sur un sbire : 4 degats a celui choisi)",
       "encart : « the player ... chooses a singular villain for that effect » ; le pilote prend le premier (Bebop)",
       ["Puzzle.ChangeToFace('ar001b', 'ar001a')", "Puzzle.PutIntoPlay('39043')", "Puzzle.PutIntoPlay('ar008', under_control=True)"],
       ["Puzzle.Attack('ar001a')"],
       {"degats": [["tk001a", 4], ["tk003a", 0]]},
       heros="ares", main_exclusive=["01090"], cibles=["39043"], questions_presentes=["Choose Bebop or Rocksteady"]),
    _c("tk006a Dunderheads : Bebop vaincu -> lui et son Temper sont MIS DE COTE, Rocksteady reste ALERT et Gone Berserk l'equipe",
       "« set that villain and their TEMPER attachment aside. Flip the remaining villain to their ALERT side, and this card to its FERAL side »",
       [], ["Puzzle.Damage('tk001a', 15)"],
       {"absents": ["tk001a", "tk007a", "tk006a"], "en_jeu": ["tk003a", "tk008a", "tk006b"],
        "attache": [["tk006b", "tk003a"]], "vie": [["tk003a", 29]], "trait_de": [["tk003a", "ALERT", True]]}),
    _c("tk006a Dunderheads : Bebop vaincu alors que Rocksteady est K.O. -> Rocksteady repasse ALERT",
       "« Flip the remaining villain to their ALERT side »",
       ["Puzzle.Flip('tk003a')"], ["Puzzle.Damage('tk001a', 15)"],
       {"en_jeu": ["tk003a", "tk006b"], "absents": ["tk003b"]}),
    _c("tk006a Dunderheads : Rocksteady vaincu -> Bebop (ALERT, +12 PV) et son Temper restent",
       "meme chose dans l'autre sens ; 12 PV par joueur",
       [], ["Puzzle.Damage('tk003a', 17)"],
       {"absents": ["tk003a", "tk008a"], "en_jeu": ["tk001a", "tk007a", "tk006b"], "vie": [["tk001a", 27]],
        "attache": [["tk006b", "tk001a"]]}),
    _c("tk006a Dunderheads : les DEUX vilains vaincus -> les joueurs GAGNENT",
       "plus aucun vilain en jeu : fin de partie, victoire",
       ["Puzzle.Damage('tk001a', 15)"], ["Puzzle.Damage('tk003a', 29)"],
       {"gagnee": True}),
    _c("tk006a Dunderheads : un seul vilain vaincu ne termine PAS la partie",
       "contre-cas de la victoire",
       [], ["Puzzle.Damage('tk001a', 15)"],
       {"gagnee": False}),
    _c("tk006b Gone Berserk : +12 PV PAR joueur (2 joueurs : Rocksteady 17x2 + 12x2 = 58)",
       "« Attached villain gets +12[per_hero] hit points »",
       [], ["Puzzle.Damage('tk001a', 30)"],
       {"vie": [["tk003a", 58]]}, heros2="black_panther"),
    _c("tk006b Gone Berserk : le vilain ne peut plus etre desoriente",
       "« Attached villain cannot be confused »",
       [], ["Puzzle.Damage('tk001a', 15)", "Puzzle.Confuse('tk003a')"],
       {"statuts_sur": [["tk003a", "confused", 0]]}),
    _c("tk006b Gone Berserk : contre-cas, SANS Gone Berserk Rocksteady se laisse desorienter",
       "ligne de base",
       [], ["Puzzle.Confuse('tk003a')"],
       {"statuts_sur": [["tk003a", "confused", 1]]}),
    # ===================================================================== complot principal 1B
    _c("tk005b Demolition Crew : menace atteinte -> remise a 0 a la place, et les DEUX vilains attaquent",
       "« When this scheme would be completed, remove all threat from here instead. Then ... Bebop and Rocksteady attack each player » : Bebop 1 + Rocksteady 2 = 3",
       ["Puzzle.Counter('tk007a', 'knucklehead', 1)", "Puzzle.Counter('tk008a', 'knucklehead', 1)", "Puzzle.Exhaust('01001a')",
        "Puzzle.SetThreat('tk005b', 6)"],
       ["Puzzle.PlaceThreat('tk005b', 1)"],
       {"menace_de": [["tk005b", 0]], "degats_identite": 3, "gagnee": False}),
    _c("tk005b Demolition Crew : en ALTER-EGO le joueur est quand meme ATTAQUE (pas de manigance)",
       "« (even if they are in alter-ego form) »",
       ["Puzzle.Counter('tk007a', 'knucklehead', 1)", "Puzzle.Counter('tk008a', 'knucklehead', 1)",
        "Puzzle.SetThreat('tk005b', 6)"],
       ["Puzzle.PlaceThreat('tk005b', 1)"],
       {"menace_de": [["tk005b", 0]], "degats_identite": 3, "forme": "AlterEgo"}),
    _c("tk005b Demolition Crew : A DEUX joueurs, chacun est attaque par les deux vilains (3 chacun)",
       "« in player order, Bebop and Rocksteady attack each player »",
       ["Puzzle.Counter('tk007a', 'knucklehead', 1)", "Puzzle.Counter('tk008a', 'knucklehead', 1)", "Puzzle.Exhaust('01001a')",
        "Puzzle.SetThreat('tk005b', 12)"],
       ["Puzzle.PlaceThreat('tk005b', 2)"],
       {"menace_de": [["tk005b", 0]], "degats_identite": 3}, heros2="black_panther"),
]

CAS += [
    _c("tk006a Dunderheads : BASELINE sans l'environnement un SEUL vilain s'active (Bebop 2 + obligation 2)",
       "contre-cas du Double Trouble : sans tk006a retire du jeu, un vilain seulement",
       [HEROS, "Puzzle.Remove('tk006a')", "Puzzle.Counter('tk007a', 'knucklehead', 2)", "Puzzle.Counter('tk008a', 'knucklehead', 1)", "Puzzle.Exhaust('01001a')"],
       ["Puzzle.RunVillainPhase()"],
       {"degats_identite": 4}),
    _c("tk006a Dunderheads : BASELINE a 2 joueurs, un seul vilain",
       "meme contre-cas a deux joueurs",
       [HEROS, "Puzzle.Remove('tk006a')", "Puzzle.Counter('tk007a', 'knucklehead', 2)", "Puzzle.Counter('tk008a', 'knucklehead', 1)", "Puzzle.Exhaust('01001a')"],
       ["Puzzle.RunVillainPhase()"],
       {"degats_identite": 5}, heros2="black_panther"),
]


# Verification outillee du pack : etat_attendu (cles de base) + extensions lues sur les faces EN JEU.
VERIFICATIONS = r'''
def bb_etat(monde, aides):
    """Extensions de `etat_attendu` : attache [[carte, hote]], compteurs_sur [[id, nom, n]],
    menace_de [[id, n]], attaque [[id, n]], statuts_sur [[id, 'stunned'|'tough'|'confused', n]],
    vie [[id, pv_max]], absents [ids hors jeu], trait_de [[id, TRAIT, bool]], bascule : etat_attendu d'abord."""
    attendu = aides["cas"].get("attendu") or {}
    ok, msg = etat_attendu(monde, aides)
    soucis = [] if ok else [msg]
    par_id = aides["par_id"]
    for cid, hote in attendu.get("attache", []):
        f = par_id(monde, cid)
        if f is None:
            soucis.append(f"{cid} n'est pas en jeu"); continue
        b = f.bind_face
        got = getattr(getattr(b, "paper", None), "card_id", None) if b else None
        if got != hote:
            soucis.append(f"{cid} attache a {got} (attendu {hote})")
    for cid, nom, n in attendu.get("compteurs_sur", []):
        f = par_id(monde, cid)
        if f is None:
            soucis.append(f"{cid} n'est pas en jeu"); continue
        if f.GetCounters(nom) != n:
            soucis.append(f"{cid} compteurs {nom} = {f.GetCounters(nom)} (attendu {n})")
    for cid, n in attendu.get("menace_de", []):
        f = par_id(monde, cid)
        if f is None:
            soucis.append(f"{cid} n'est pas en jeu"); continue
        if f.threat != n:
            soucis.append(f"{cid} menace = {f.threat} (attendu {n})")
    for cid, n in attendu.get("attaque", []):
        f = par_id(monde, cid)
        if f is None:
            soucis.append(f"{cid} n'est pas en jeu"); continue
        if f.attack != n:
            soucis.append(f"{cid} ATK = {f.attack} (attendu {n})")
    for cid, n in attendu.get("vie", []):
        f = par_id(monde, cid)
        if f is None:
            soucis.append(f"{cid} n'est pas en jeu"); continue
        if f.max_health != n:
            soucis.append(f"{cid} PV max = {f.max_health} (attendu {n})")
    for cid, st, n in attendu.get("statuts_sur", []):
        f = par_id(monde, cid)
        if f is None:
            soucis.append(f"{cid} n'est pas en jeu"); continue
        v = getattr(f, st)
        if v != n:
            soucis.append(f"{cid} statut {st} = {v} (attendu {n})")
    for cid in attendu.get("absents", []):
        if par_id(monde, cid) is not None:
            soucis.append(f"{cid} est encore en jeu")
    for cid, tr, b in attendu.get("trait_de", []):
        f = par_id(monde, cid)
        if f is None:
            soucis.append(f"{cid} n'est pas en jeu"); continue
        if bool(f.HasTrait(tr)) != b:
            soucis.append(f"{cid} trait {tr} = {f.HasTrait(tr)} (attendu {b})")
    for cid in attendu.get("steady", []):
        f = par_id(monde, cid)
        if f is None:
            soucis.append(f"{cid} n'est pas en jeu"); continue
        if not f.IsSteady():
            soucis.append(f"{cid} n'est pas Steady")
    if "gagnee" in attendu:
        fini = bool(getattr(monde, "is_game_over", False))
        gagne = fini and bool(monde.game_over.players_won)
        if (fini and gagne) != attendu["gagnee"]:
            soucis.append(f"partie finie={fini} gagnee={gagne} (attendu gagnee={attendu['gagnee']})")
    if soucis:
        return False, " ; ".join(soucis)
    return True, "etat conforme"
'''
