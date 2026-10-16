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
    # `Puzzle.Thwart('01001a')` : le heros manigance ; la manigance visee est la carte revelee dans la mise en place.
    if "Puzzle.Thwart('01001a')" in declencher and "cibles" not in cas:
        import re
        ids = re.findall(r"Puzzle\.Reveal\('(tk\d+)'\)", " ".join(mise))
        if ids:
            cas["cibles"] = [ids[0]]
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

CAS += [
    # ===================================================================== accessoires attaches (Shutter Shades, Aviator Cap, Roberta, Juniper)
    _c("tk009 Shutter Shades : revelee, Bebop ALERT -> s'attache a Bebop, Bebop STEADY, 1 compteur sur Hog Wild",
       "« Attach to Bebop if he is ALERT. Bebop gains steady. When Revealed: Place 1 knucklehead counter on the HOG attachment »",
       [], ["Puzzle.Reveal('tk009')"],
       {"attache": [["tk009", "tk001a"]], "steady": ["tk001a"], "compteurs_sur": [["tk007a", "knucklehead", 1]]}),
    _c("tk009 Shutter Shades : Bebop K.O. -> NE S'ATTACHE PAS (la carte gagne Surge), le When Revealed place quand meme son compteur",
       "« Otherwise, this card gains surge » ; lecture litterale : le When Revealed se resout toujours",
       ["Puzzle.Flip('tk001a')"], ["Puzzle.Reveal('tk009')"],
       {"absents": ["tk009"], "compteurs_sur": [["tk007a", "knucklehead", 1]]}),
    _c("tk009 Shutter Shades : apres que Bebop passe K.O., la carte est defaussee",
       "« Forced Response: After Bebop flips to his K.O. side, discard this card »",
       [], ["Puzzle.Reveal('tk009')", "Puzzle.Flip('tk001a')"],
       {"absents": ["tk009"], "en_jeu": ["tk001b"]}),
    _c("tk009 Shutter Shades : Steady -> il faut DEUX etourdissements pour etre etourdi (1 carte ne suffit pas)",
       "Bebop STEADY : « n'est etourdi que s'il a deja deux compteurs Stun » ; temoin de l'effet du mot-cle donne",
       [], ["Puzzle.Reveal('tk009')", "Puzzle.Stun('tk001a')", "Puzzle.Exhaust('01001a')", "Puzzle.Counter('tk007a', 'knucklehead', 1)", "Puzzle.Attack('tk001a')"],
       {"degats_identite": 2, "steady": ["tk001a"]}),
    _c("tk010 Aviator Cap : revelee, Rocksteady ALERT -> s'attache, STEADY, 1 compteur sur Rhino Rage",
       "meme carte que Shutter Shades, cote Rocksteady / RHINO",
       [], ["Puzzle.Reveal('tk010')"],
       {"attache": [["tk010", "tk003a"]], "steady": ["tk003a"], "compteurs_sur": [["tk008a", "knucklehead", 1]]}),
    _c("tk010 Aviator Cap : Rocksteady passe K.O. -> defaussee",
       "« After Rocksteady flips to his K.O. side, discard this card »",
       [], ["Puzzle.Reveal('tk010')", "Puzzle.Flip('tk003a')"],
       {"absents": ["tk010"], "en_jeu": ["tk003b"]}),
    _c("tk010 Aviator Cap : Rocksteady K.O. -> pas d'attache (surge)",
       "« Otherwise, this card gains surge »",
       ["Puzzle.Flip('tk003a')"], ["Puzzle.Reveal('tk010')"],
       {"absents": ["tk010"]}),
    _c("tk011 Roberta : l'attaque de Bebop est PERCANTE (la carte Robuste saute ET les degats passent)",
       "« Bebop's attacks gain piercing » ; Bebop ATK 1 (1 compteur) contre un heros Robuste",
       [HEROS, "Puzzle.Tough('01001a')", "Puzzle.Exhaust('01001a')", "Puzzle.Counter('tk007a', 'knucklehead', 1)", "Puzzle.Reveal('tk011')"],
       ["Puzzle.Attack('tk001a')"],
       {"attache": [["tk011", "tk001a"]], "degats_identite": 1, "statuts_sur": [["01001a", "tough", 0]]}),
    _c("tk011 Roberta : CONTRE-CAS sans Roberta, la carte Robuste absorbe l'attaque",
       "ligne de base : pas de percant",
       [HEROS, "Puzzle.Tough('01001a')", "Puzzle.Exhaust('01001a')", "Puzzle.Counter('tk007a', 'knucklehead', 1)"],
       ["Puzzle.Attack('tk001a')"],
       {"degats_identite": 0, "statuts_sur": [["01001a", "tough", 0]]}),
    _c("tk011 Roberta : Bebop passe K.O. -> Roberta defaussee",
       "« After Bebop flips to his K.O. side, discard this card »",
       [], ["Puzzle.Reveal('tk011')", "Puzzle.Flip('tk001a')"],
       {"absents": ["tk011"]}),
    _c("tk012 Juniper : l'attaque de Rocksteady a OVERKILL (1 degat d'exces sur l'allie va a l'identite)",
       "« Rocksteady's attacks gain overkill » ; Rocksteady ATK 3 contre un allie a 2 PV",
       ["Puzzle.ChangeForm('01001a')", "Puzzle.PutIntoPlay('01011', under_control=True)", "Puzzle.Counter('tk008a', 'knucklehead', 2)", "Puzzle.Reveal('tk012')"],
       ["Puzzle.Attack('tk003a', '01011')"],
       {"attache": [["tk012", "tk003a"]], "degats_identite": 1}, main_exclusive=["01088"]),
    _c("tk012 Juniper : CONTRE-CAS sans Juniper, l'exces est perdu",
       "ligne de base : pas d'overkill",
       ["Puzzle.ChangeForm('01001a')", "Puzzle.PutIntoPlay('01011', under_control=True)", "Puzzle.Counter('tk008a', 'knucklehead', 2)"],
       ["Puzzle.Attack('tk003a', '01011')"],
       {"degats_identite": 0}, main_exclusive=["01088"]),
    _c("tk012 Juniper : Rocksteady passe K.O. -> Juniper defaussee",
       "« After Rocksteady flips to his K.O. side, discard this card »",
       [], ["Puzzle.Reveal('tk012')", "Puzzle.Flip('tk003a')"],
       {"absents": ["tk012"]}),
    # ===================================================================== manigances annexes du set
    _c("tk016 Collision Course : revelee -> 1 compteur sur CHAQUE Temper",
       "« When Revealed: Place 1 knucklehead counter on each TEMPER attachment »",
       [], ["Puzzle.Reveal('tk016')"],
       {"compteurs_sur": [["tk007a", "knucklehead", 1], ["tk008a", "knucklehead", 1]], "en_jeu": ["tk016"]}),
    _c("tk016 Collision Course : vaincue -> chaque vilain est ETOURDI",
       "« When Defeated: Stun each villain »",
       [HEROS, "Puzzle.Reveal('tk016')", "Puzzle.SetThreat('tk016', 1)"], ["Puzzle.Thwart('01001a')"],
       {"absents": ["tk016"], "statuts_sur": [["tk001a", "stunned", 1], ["tk003a", "stunned", 1]]}),
    _c("tk018 Ole! : Hinder 1 par joueur (menace de depart 2 + 1 = 3, solo)",
       "« Hinder 1[per_hero] » lu dans desc",
       [], ["Puzzle.Reveal('tk018')"],
       {"menace_de": [["tk018", 3]]}),
    _c("tk018 Ole! : Hinder 1 par joueur a DEUX joueurs (2 + 2 = 4)",
       "le « par joueur » ne se voit qu'a deux",
       [], ["Puzzle.Reveal('tk018')"],
       {"menace_de": [["tk018", 4]]}, heros2="black_panther"),
    _c("tk018 Ole! : vaincue -> 2 degats PAR joueur a chaque vilain ; seul le vilain ENRAGED blesse est etourdi",
       "« Deal 2[per_hero] damage to each villain. Stun each ENRAGED villain damaged this way » : Bebop ENRAGED (Headfirst) -> etourdi, Rocksteady non",
       [HEROS, "Puzzle.Counter('tk007a', 'knucklehead', 3)", "Puzzle.Flip('tk007a')", "Puzzle.Reveal('tk018')", "Puzzle.SetThreat('tk018', 1)"],
       ["Puzzle.Thwart('01001a')"],
       {"degats": [["tk001a", 2], ["tk003a", 2]], "statuts_sur": [["tk001a", "stunned", 1], ["tk003a", "stunned", 0]]}),
    _c("tk018 Ole! : a DEUX joueurs, 4 degats a chaque vilain",
       "« 2[per_hero] » : 2 x 2 joueurs",
       [HEROS, "Puzzle.Reveal('tk018')", "Puzzle.SetThreat('tk018', 1)"], ["Puzzle.Thwart('01001a')"],
       {"degats": [["tk001a", 4], ["tk003a", 4]]}, heros2="black_panther"),
    _c("tk020 Toro! Toro! : Dodgy ACCEPTE -> le heros manigance avec sa DEF (3) au lieu de sa THW (1) : 4 -> 1",
       "« they may use their DEF instead of their THW » ; Spider-Man THW 1, DEF 3",
       [HEROS, "Puzzle.Reveal('tk020')"], ["Puzzle.Thwart('01001a')"],
       {"menace_de": [["tk020", 1]]}, accepter_choix=True),
    _c("tk020 Toro! Toro! : Dodgy REFUSE (facultatif) -> THW 1 : 4 -> 3",
       "Dodgy n'oblige pas a se servir de la DEF (contrairement a Assault)",
       [HEROS, "Puzzle.Reveal('tk020')"], ["Puzzle.Thwart('01001a')"],
       {"menace_de": [["tk020", 3]]}, choisir_option="Cancel"),
    _c("tk020 Toro! Toro! : vaincue -> 2 compteurs sur un Temper",
       "« When Defeated: Place 2 knucklehead counters on a TEMPER attachment »",
       [HEROS, "Puzzle.Reveal('tk020')", "Puzzle.SetThreat('tk020', 1)"], ["Puzzle.Thwart('01001a')"],
       {"absents": ["tk020"], "compteurs_sur": [["tk007a", "knucklehead", 2]]}),
]

CAS += [
    # ===================================================================== Bumbling Buffoons (3 illustrations, meme texte)
    _c("tk013 Bumbling Buffoons : Dodgy accepte (DEF 3 au lieu de THW 1) : 4 -> 1",
       "« Dodgy » (insert) ; illustration 1/3",
       [HEROS, "Puzzle.Reveal('tk013')"], ["Puzzle.Thwart('01001a')"],
       {"menace_de": [["tk013", 1]]}, accepter_choix=True),
    _c("tk014 Bumbling Buffoons (illustration 2/3) : meme Dodgy",
       "meme texte, card_id propre : la capacite doit aussi exister sur tk014",
       [HEROS, "Puzzle.Reveal('tk014')"], ["Puzzle.Thwart('01001a')"],
       {"menace_de": [["tk014", 1]]}, accepter_choix=True),
    _c("tk015 Bumbling Buffoons (illustration 3/3) : meme Dodgy",
       "meme texte, card_id propre",
       [HEROS, "Puzzle.Reveal('tk015')"], ["Puzzle.Thwart('01001a')"],
       {"menace_de": [["tk015", 1]]}, accepter_choix=True),
    _c("tk013 Bumbling Buffoons : vaincue -> l'ennemi choisi t'attaque (Bebop ATK 2 -> 2 degats), sans redirection",
       "« Choose an enemy. That enemy attacks you » ; la redirection est facultative et refusee",
       [HEROS, "Puzzle.Counter('tk007a', 'knucklehead', 2)", "Puzzle.Reveal('tk013')", "Puzzle.SetThreat('tk013', 1)"],
       ["Puzzle.Thwart('01001a')"],
       {"absents": ["tk013"], "degats_identite": 2}, choisir_option="Cancel"),
    _c("tk013 Bumbling Buffoons : vaincue, redirection ACCEPTEE -> les degats de l'attaque vont a un AUTRE ennemi",
       "« You may deal damage from this attack to another enemy of your choice instead » : Rocksteady prend les 2 degats de Bebop (et Bebop ne touche pas l'identite)",
       [HEROS, "Puzzle.Counter('tk007a', 'knucklehead', 2)", "Puzzle.Reveal('tk013')", "Puzzle.SetThreat('tk013', 1)"],
       ["Puzzle.Thwart('01001a')"],
       {"absents": ["tk013"], "degats_identite": 0, "degats": [["tk003a", 2]]}, accepter_choix=True),
    # ===================================================================== traitrises du set
    _c("tk022 Lay the Beatdown (ALTER-EGO) : l'identite est DESORIENTEE",
       "« When Revealed (Alter-Ego): Confuse your identity »",
       [], ["Puzzle.Reveal('tk022')"],
       {"statuts_sur": [["01001b", "confused", 1]], "degats_identite": 0}),
    _c("tk022 Lay the Beatdown (HEROS) : par defaut 2 degats indirects au heros",
       "« When Revealed (Hero): Choose: Deal 2 indirect damage to your hero. / Stun your hero. »",
       [HEROS], ["Puzzle.Reveal('tk022')"],
       {"degats_identite": 2, "statuts_sur": [["01001a", "confused", 0]]}),
    _c("tk022 Lay the Beatdown (HEROS) : l'autre option etourdit le heros (et ne blesse pas)",
       "seconde branche du choix",
       [HEROS], ["Puzzle.Reveal('tk022')"],
       {"degats_identite": 0, "statuts_sur": [["01001a", "stunned", 1]]}, choisir_option="Stun_your_hero"),
    _c("tk022 Lay the Beatdown : en HEROS, rien ne desoriente (contre-cas de la branche alter-ego)",
       "la branche Alter-Ego ne part pas en forme heros",
       [HEROS], ["Puzzle.Reveal('tk022')"],
       {"statuts_sur": [["01001a", "confused", 0]]}),
    _c("tk024 Pummel : par defaut, degats egaux a l'ATK d'un vilain (Bebop ATK 2 -> 2)",
       "« Take damage equal to either Bebop or Rocksteady's ATK » ; le pilote prend Bebop",
       ["Puzzle.Counter('tk007a', 'knucklehead', 2)"], ["Puzzle.Reveal('tk024')"],
       {"degats_identite": 2}, questions_presentes=["Choose Bebop or Rocksteady"]),
    _c("tk024 Pummel : l'autre option defausse la carte de plus haut cout (Helicarrier 3 > Aunt May 1)",
       "« Discard the highest-cost upgrade or support you control »",
       ["Puzzle.PutIntoPlay('01006', under_control=True)", "Puzzle.PutIntoPlay('01092', under_control=True)"], ["Puzzle.Reveal('tk024')"],
       {"absents": ["01092"], "en_jeu": ["01006"], "degats_identite": 0},
       choisir_option="Discard_the_highest-cost_upgrade_or_support_you_control"),
    _c("tk024 Pummel : sans amelioration ni soutien, l'option defausse n'est PAS offerte (la premiere reste)",
       "une option impossible ne se choisit pas",
       ["Puzzle.Counter('tk007a', 'knucklehead', 1)"], ["Puzzle.Reveal('tk024')"],
       {"degats_identite": 1}),
    _c("tk026 Trample (ALTER-EGO) : defausse 1 carte de la main",
       "« When Revealed (Alter-Ego): Discard 1 card from your hand »",
       [], ["Puzzle.Reveal('tk026')"],
       {"taille_main": 0, "defausse": ["01090"]}, main_exclusive=["01090"]),
    _c("tk026 Trample (HEROS) : un vilain attaque le personnage ami aux PV restants les plus bas (allie a 3 PV, pas l'identite a 10)",
       "« Choose a villain. That villain attacks the friendly character with the fewest remaining hit points » ; Bebop ATK 1",
       [HEROS, "Puzzle.PutIntoPlay('01059', under_control=True)", "Puzzle.Counter('tk007a', 'knucklehead', 1)", "Puzzle.Exhaust('01001a')"], ["Puzzle.Reveal('tk026')"],
       {"degats": [["01059", 1]], "degats_identite": 0}, main_exclusive=["01090"]),
    _c("tk026 Trample (HEROS) : sans allie, c'est l'identite qui est visee",
       "le seul personnage ami",
       [HEROS, "Puzzle.Counter('tk007a', 'knucklehead', 1)", "Puzzle.Exhaust('01001a')"], ["Puzzle.Reveal('tk026')"],
       {"degats_identite": 1}),
    _c("tk026 Trample : « [star] Boost: Deal 1 damage to an ally you control »",
       "boost : 1 degat a un allie du joueur attaque",
       [HEROS, "Puzzle.PutIntoPlay('01059', under_control=True)"], ["Puzzle.Boost('tk026')"],
       {"degats": [["01059", 1]]}, main_exclusive=["01090"]),
    # ===================================================================== Anchovy
    _c("tk028 Anchovy : entre en jeu avec une carte Robuste (Toughness)",
       "« Toughness. »",
       [], ["Puzzle.PutIntoPlay('tk028')"],
       {"statuts_sur": [["tk028", "tough", 1]]}),
    _c("tk028 Anchovy : vaincu -> REMELANGE dans le deck rencontre (apres sa carte Robuste)",
       "« Forced Interrupt: When Anchovy is defeated, shuffle him into the encounter deck »",
       ["Puzzle.PutIntoPlay('tk028')"], ["Puzzle.Damage('tk028', 1)", "Puzzle.Damage('tk028', 1)"],
       {"absents": ["tk028"], "dans_deck_rencontre": ["tk028"]}),
    _c("tk028 Anchovy : « [star] Boost: After this activation resolves, deal this card to the first player as a facedown encounter card »",
       "Anchovy est revelee en boost de l'attaque de Bebop : apres l'attaque, elle est distribuee face cachee au premier joueur",
       [HEROS, "Puzzle.Exhaust('01001a')", "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01105', '01105', 'tk028')"],
       ["Puzzle.Attack('tk001a')"],
       {"distribuees": 1}, avec_boost=True),
]

CAS += [
    # ===================================================================== Concrete Jungle
    _c("tk101 Welcome to the Jungle : vaincue -> le joueur met en jeu UNE carte NYC mise de cote (Eastman Theater choisi)",
       "« Each player may choose 1 set-aside NYC card and put it into play » ; les 4 cartes Linked sont de cote des la mise en place",
       [HEROS, "Puzzle.SetThreat('tk101', 1)"], ["Puzzle.Thwart('01001a')"],
       {"absents": ["tk101"], "en_jeu": ["tk107"], "hors_jeu": ["tk106", "tk108", "tk109"]},
       cibles=["tk101", "tk107"], accepter_choix=True),
    _c("tk101 Welcome to the Jungle : A DEUX joueurs, CHAQUE joueur en choisit une (deux cartes en jeu)",
       "« Each player may choose »",
       [HEROS, "Puzzle.SetThreat('tk101', 1)"], ["Puzzle.Thwart('01001a')"],
       {"absents": ["tk101"], "en_jeu": ["tk107", "tk106"]},
       cibles=["tk101", "tk107", "tk106"], accepter_choix=True, heros2="black_panther"),
    _c("tk101 Welcome to the Jungle : Linked -> les 4 cartes sont de cote (ni en jeu ni dans un deck) au depart",
       "desc.Linked = « Welcome to the Jungle » : creees par le moteur avec la carte",
       [], [],
       {"hors_jeu": ["tk106", "tk107", "tk108", "tk109"], "en_jeu": ["tk101"]}),
    _c("tk106 Channel 6 News : apres la revelation d'une manigance annexe NYC, s'epuise -> retire 2 menaces (4 -> 2)",
       "« Response: After a NYC side scheme is revealed, exhaust Channel 6 News -> remove 2 threat from a scheme »",
       ["Puzzle.PutIntoPlay('tk106', under_control=True)"], ["Puzzle.Reveal('tk013')"],
       {"exhausted": ["tk106"], "menace_de": [["tk013", 2]]}, accepter_choix=True, cibles=["tk013"]),
    _c("tk106 Channel 6 News : une manigance annexe SANS le trait NYC ne declenche rien",
       "contre-cas du filtre `NYC` : Breakin' & Takin' (01107)",
       ["Puzzle.PutIntoPlay('tk106', under_control=True)"], ["Puzzle.Reveal('01107')"],
       {"exhausted": [], "menace_de": [["01107", 3]]}, accepter_choix=True, cibles=["01107"]),
    _c("tk107 Eastman Theater : apres la defaite d'une manigance annexe NYC, s'epuise -> redresse un heros ami",
       "« Hero Response: After a NYC side scheme is defeated, exhaust Eastman Theater -> ready a friendly hero »",
       [HEROS, "Puzzle.PutIntoPlay('tk107', under_control=True)", "Puzzle.Reveal('tk016')", "Puzzle.SetThreat('tk016', 1)"],
       ["Puzzle.Thwart('01001a')"],
       {"exhausted": ["tk107"], "pret": ["01001a"], "absents": ["tk016"]}, accepter_choix=True, cibles=["tk016", "01001a"]),
    _c("tk108 Powder Keg : vaincue -> 2 degats a chaque ennemi, 4 si l'ennemi est etourdi ou desoriente",
       "Bebop etourdi -> 4, Rocksteady -> 2 ; la carte ne compte pas dans la limite de manigances joueur",
       [HEROS, "Puzzle.Stun('tk001a')", "Puzzle.PutIntoPlay('tk108', under_control=True)", "Puzzle.SetThreat('tk108', 1)"],
       ["Puzzle.Thwart('01001a')"],
       {"absents": ["tk108"], "degats": [["tk001a", 4], ["tk003a", 2]]}, cibles=["tk108"]),
    _c("tk108 Powder Keg : ne compte PAS dans la limite de manigances joueur (drapeau pose a l'entree en jeu)",
       "« This card does not count against the player side scheme limit »",
       [], ["Puzzle.PutIntoPlay('tk108', under_control=True)"],
       {"en_jeu": ["tk108"], "hors_limite": ["tk108"]}),
    _c("tk109 Power Play : apres avoir retire de la menace, defausse 1 carte -> retire 2 menaces de plus (6 -1 -2 = 3)",
       "« Hero Response: After you remove threat from this scheme, discard 1 card from your hand -> remove 2 threat from this scheme »",
       [HEROS, "Puzzle.EmptyHand()", "Puzzle.Gain('01090')", "Puzzle.PutIntoPlay('tk109', under_control=True)", "Puzzle.SetThreat('tk109', 6)"],
       ["Puzzle.Thwart('01001a')"],
       {"menace_de": [["tk109", 3]], "defausse": ["01090"], "hors_limite": ["tk109"], "taille_main": 0},
       cibles=["tk109"], accepter_choix=True),
    _c("tk109 Power Play : sans carte a defausser, la Reponse est impayable (6 - 1 = 5)",
       "le cout de la Reponse (defausser 1 carte) doit etre payable",
       [HEROS, "Puzzle.EmptyHand()", "Puzzle.PutIntoPlay('tk109', under_control=True)", "Puzzle.SetThreat('tk109', 6)"],
       ["Puzzle.Thwart('01001a')"],
       {"menace_de": [["tk109", 5]]}, cibles=["tk109"], accepter_choix=True),
    _c("tk109 Power Play : la Reponse se REPETE tant qu'on retire de la menace et qu'on a des cartes (3 cartes : 6 -1 -2 -2 -2 -> 0, vaincue)",
       "chaque retrait « par vous » redeclenche la Reponse (aucune limite imprimee)",
       [HEROS, "Puzzle.EmptyHand()", "Puzzle.Gain('01090', '01089', '01088')", "Puzzle.PutIntoPlay('tk109', under_control=True)", "Puzzle.SetThreat('tk109', 7)"],
       ["Puzzle.Thwart('01001a')"],
       {"absents": ["tk109"], "taille_main": 0}, cibles=["tk109"], accepter_choix=True),
    _c("tk109 Power Play : vaincue -> le joueur peut etourdir ET desorienter un ennemi",
       "« When Defeated: Each player may stun and confuse an enemy »",
       [HEROS, "Puzzle.PutIntoPlay('tk109', under_control=True)", "Puzzle.SetThreat('tk109', 1)"],
       ["Puzzle.Thwart('01001a')"],
       {"absents": ["tk109"], "statuts_sur": [["tk001a", "stunned", 1], ["tk001a", "confused", 1]]},
       cibles=["tk109", "tk001a"], accepter_choix=True),
    _c("tk102 Road to Ruin (ALTER-EGO) : sans LOCATION, aucune option -> rien (pas de « Stun your hero » hors forme heros)",
       "« Stun your hero » exige un heros (lecture litterale, Q4)",
       [], ["Puzzle.Reveal('tk102')"],
       {"statuts_sur": [["01001b", "stunned", 0]], "en_jeu": ["tk102"]}),
    _c("tk102 Road to Ruin (HEROS) : sans LOCATION, le heros est etourdi",
       "« Choose: Discard a friendly LOCATION / Stun your hero » : seule la seconde option reste",
       [HEROS], ["Puzzle.Reveal('tk102')"],
       {"statuts_sur": [["01001a", "stunned", 1]]}),
    _c("tk102 Road to Ruin (HEROS) : avec une LOCATION, la premiere option la defausse",
       "Channel 6 News (LOCATION) en jeu",
       [HEROS, "Puzzle.PutIntoPlay('tk106', under_control=True)"], ["Puzzle.Reveal('tk102')"],
       {"absents": ["tk106"], "statuts_sur": [["01001a", "stunned", 0]]}),
    _c("tk102 Road to Ruin : vaincue -> etourdit un ennemi",
       "« When Defeated: Stun an enemy »",
       [HEROS, "Puzzle.Reveal('tk102')", "Puzzle.SetThreat('tk102', 1)"], ["Puzzle.Thwart('01001a')"],
       {"absents": ["tk102"], "statuts_sur": [["tk001a", "stunned", 1]]}, cibles=["tk102", "tk001a"]),
    _c("tk104 Fallen Empires : sans LOCATION, defausse 1 carte de la main",
       "« Choose: Discard a friendly LOCATION / Discard 1 card from your hand »",
       [], ["Puzzle.Reveal('tk104')"],
       {"taille_main": 0, "defausse": ["01090"]}, main_exclusive=["01090"]),
    _c("tk104 Fallen Empires : avec une LOCATION, la defausse par defaut",
       "premiere option",
       ["Puzzle.PutIntoPlay('tk106', under_control=True)"], ["Puzzle.Reveal('tk104')"],
       {"absents": ["tk106"], "taille_main": 1}, main_exclusive=["01090"]),
    _c("tk104 Fallen Empires : « [star] Boost: Discard 1 card from your hand »",
       "boost",
       [], ["Puzzle.Boost('tk104')"],
       {"taille_main": 0, "defausse": ["01090"]}, main_exclusive=["01090"]),
    # ===================================================================== Rock the Block
    _c("tk201 Hittin' the Town : defausse du deck rencontre jusqu'a une manigance annexe ou un attachement, et la REVELE",
       "« Discard cards from the top of the villain deck until an attachment or side scheme is discarded and reveal it » (deck rencontre, Q5) ; deux 01105 puis Toro! Toro!",
       [HEROS, "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('tk020', '01105', '01105')"], ["Puzzle.Reveal('tk201')"],
       {"en_jeu": ["tk020"]}, avec_boost=True),
    _c("tk201 Hittin' the Town : rien a trouver (ni attachement ni manigance annexe) -> ne boucle pas",
       "garde anti-boucle : deck et defausse sans cible",
       ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01105', '01105')"], ["Puzzle.Reveal('tk201')"],
       {"dans_deck_rencontre": ["01105"]}, avec_boost=True),
    _c("tk203 Jagerbombs : par defaut, etourdit l'identite",
       "« Choose one: Stun your identity / Confuse your identity »",
       [], ["Puzzle.Reveal('tk203')"],
       {"statuts_sur": [["01001b", "stunned", 1], ["01001b", "confused", 0]]}),
    _c("tk203 Jagerbombs : l'autre option desoriente l'identite",
       "seconde branche",
       [], ["Puzzle.Reveal('tk203')"],
       {"statuts_sur": [["01001b", "stunned", 0], ["01001b", "confused", 1]]}, choisir_option="Confuse_your_identity"),
    _c("tk205 Get Your Swell On : soigne 1 degat a chaque ennemi ET leur donne une carte Robuste",
       "« Heal 1 damage from each enemy. Give each enemy a tough status card » ; Bebop a 2 degats (+1 compteur) avant",
       ["Puzzle.Damage('tk001a', 2)"], ["Puzzle.Reveal('tk205')"],
       {"degats": [["tk001a", 1], ["tk003a", 0]], "statuts_sur": [["tk001a", "tough", 1], ["tk003a", "tough", 1]]}),
]

CAS += [
    _c("tk008a Rhino Rage : s'accroche a Rocksteady (et PAS a Bebop)",
       "« Attach to Rocksteady » ; son jumeau tk007a vise Bebop",
       [], [],
       {"attache": [["tk008a", "tk003a"], ["tk007a", "tk001a"]]}),
    _c("tk008a Rhino Rage : +1 ATQ a Rocksteady par jeton Andouille (2 jetons -> ATQ 1 + 2 = 3)",
       "« Rocksteady gets +1 ATK for each knucklehead counter here »",
       ["Puzzle.Counter('tk008a', 'knucklehead', 2)"], [],
       {"attaque": [["tk003a", 3]]}),
    _c("tk008a Rhino Rage : sans jeton, ATQ de base (1)",
       "ligne de base",
       [], [], {"attaque": [["tk003a", 1]]}),
    _c("tk008a Rhino Rage : a 3 jetons, se retourne sur Headstrong (ENRAGED, +3 ATQ) : ATQ 1 + 3 = 4",
       "« If there are at least 3 knucklehead counters here, flip this card to its ENRAGED side »",
       ["Puzzle.Counter('tk008a', 'knucklehead', 2)"], ["Puzzle.Damage('tk003a', 1)"],
       {"en_jeu": ["tk008b"], "absents": ["tk008a"], "attache": [["tk008b", "tk003a"]],
        "compteurs_sur": [["tk008b", "knucklehead", 3]], "trait_de": [["tk003a", "ENRAGED", True]], "attaque": [["tk003a", 4]]}),
    _c("tk006b Gone Berserk : Crise -> on ne peut plus retirer de menace du complot principal (3 -> 3)",
       "icones imprimees : Crise 1, Amplification 1, Aleas 1 (desc) ; la Crise verrouille le complot",
       [HEROS, "Puzzle.EmptyHand()", "Puzzle.Damage('tk001a', 15)", "Puzzle.SetThreat('tk005b', 3)"],
       ["Puzzle.Thwart('01001a')"],
       {"menace_de": [["tk005b", 3]]}, cibles=["tk005b"]),
    _c("tk006b Gone Berserk : CONTRE-CAS sans Gone Berserk le complot peut etre contre (3 -> 2)",
       "ligne de base de la Crise",
       [HEROS, "Puzzle.EmptyHand()", "Puzzle.SetThreat('tk005b', 3)"],
       ["Puzzle.Thwart('01001a')"],
       {"menace_de": [["tk005b", 2]]}, cibles=["tk005b"]),
]
CAS += [
    _c("tk018 Ole! : les degats aux deux vilains se resolvent UN PAR UN : Bebop (1 PV) meurt, Gone Berserk donne +12 PV a Rocksteady (1 PV) qui survit",
       "cas limite de Destructive Dunderheads : « Deal 2 damage to each villain » est sequentiel dans le moteur (DealDamage boucle sur les unites) ; la 1re defaite retourne l'environnement AVANT les degats du 2e vilain",
       [HEROS, "Puzzle.Damage('tk001a', 14)", "Puzzle.Damage('tk003a', 16)", "Puzzle.Reveal('tk018')", "Puzzle.SetThreat('tk018', 1)"],
       ["Puzzle.Thwart('01001a')"],
       {"gagnee": False, "absents": ["tk001a"], "en_jeu": ["tk003a", "tk006b"], "vie": [["tk003a", 29]]}),
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
    for cid in attendu.get("hors_limite", []):
        f = par_id(monde, cid)
        if f is None:
            soucis.append(f"{cid} n'est pas en jeu"); continue
        if not getattr(f, "not_count_player_side_scheme_limit", False):
            soucis.append(f"{cid} compte dans la limite de manigances joueur")
    if "distribuees" in attendu:
        n = len(list(monde.players[0].dealt_encounter_cards.Get(True)))
        if n != attendu["distribuees"]:
            soucis.append(f"cartes rencontre distribuees = {n} (attendu {attendu['distribuees']})")
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
