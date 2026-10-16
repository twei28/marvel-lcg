# Cas test_capacites du heros CASEY JONES (TMNT Heroes v3, Inkwire, prefixe `tc`).
# Format identique a tools/test_capacites.py ; noms prefixes `[casey]` (filtre : `[casey]`),
# un `card_id` sujet dans chaque nom (substituer_pack.py filtre dessus : prefixe `tc`).
#
# Conventions :
#  - le heros demarre en ALTER EGO (tc001b) ; HEROS le met en forme heros (tc001a) ;
#  - `main_exclusive` vide la main : chaque cas sait avec QUOI il paie
#    (01088 Energy = YY, 01089 Genius = BB, 01090 Strength = RR) ;
#  - Rhino 01094 est le vilain, 01101 Hydra Mercenary (3 PV, Guard) le sbire de mesure ;
#  - Overswing (tc001a) est la SEULE source de paiement quand la main ne contient que la carte jouee :
#    la carte est alors payee par la defausse d'une arme Restricted en jeu ;
#  - HOMONYME : l'allie « Casey Jones » de Raphael (tr002) existe ; aucun cas ne le designe par le nom.
SC = "rhino"
HEROS = "Puzzle.ChangeToFace('tc001b', 'tc001a')"
CIVIL = "Puzzle.ChangeToFace('tc001a', 'tc001b')"
SANS_DECK = "Puzzle.EmptyPlayerDeck()"
SANS_BOOST = ["Puzzle.EmptyEncounterDeck()",
              "Puzzle.CreateEncounterDeck('01105', '01105', '01105', '01105', '01105', '01105', '01105', '01105')"]
UNE_ICONE = ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01101')"]


def _c(nom, pourquoi, mise, declencher, attendu, **cle):
    if not cle.pop("avec_boost", False):
        mise = SANS_BOOST + list(mise)
    cas = {"nom": "[casey] " + nom, "pourquoi": pourquoi, "scenario": cle.pop("scenario", SC),
           "heros": cle.pop("heros", "casey_jones"), "mise_en_place": mise, "declencher": declencher,
           "verifier": cle.pop("verifier", "etat_attendu"), "attendu": attendu}
    cas.update(cle)
    return cas


def _arme(card_id):
    return "Puzzle.PutIntoPlay('%s', under_control=True)" % card_id


CAS = [
    # ===================================================================== tc001a Overswing
    _c("tc001a Overswing : defausse la Baseball Bat (Restricted) pour payer Grand Slam (3 wild, Requirement wild) : 8 degats",
       "« Resource: Discard a WEAPON upgrade you control with the restricted keyword -> generate [wild][wild][wild] resources for an ATTACK event » : "
       "main vide sauf Grand Slam (cout 3, Requirement wild), SEULE source = Overswing ; l'arme doit partir en defausse",
       [HEROS, _arme("tc007")], [],
       {"degats": [["01094", 8]], "defausse": ["tc005", "tc007"], "hors_jeu": ["tc007"]},
       main_exclusive=["tc005"], jouer=["tc005"], cibles=["01094"]),
    _c("tc001a Overswing : defausse le Raphael's Sai (WEAPON Restricted d'un AUTRE heros) : toute arme Restricted convient",
       "« a WEAPON upgrade you control with the restricted keyword » : pas seulement les armes de Casey (la Sai tr011 est WEAPON + Restricted)",
       [HEROS, _arme("tr011")], [],
       {"degats": [["01094", 8]], "defausse": ["tc005", "tr011"], "hors_jeu": ["tr011"]},
       main_exclusive=["tc005"], jouer=["tc005"], cibles=["01094"]),
    _c("tc001a Overswing : une arme SANS le mot-cle Restricted (Energy Daggers 01046) ne peut PAS etre defaussee : Grand Slam reste en main",
       "contre-cas « with the restricted keyword » : 01046 est WEAPON mais pas Restricted (`face.restricted == 0`) ; aucune autre source de paiement",
       [HEROS, _arme("01046")], [],
       {"en_main": ["tc005"], "en_jeu": ["01046"], "degats": [["01094", 0]]},
       main_exclusive=["tc005"], jouer=["tc005"], cibles=["01094"]),
    _c("tc001a Overswing : une amelioration Restricted qui n'est PAS une arme (Captain America's Shield 03009) ne peut pas etre defaussee",
       "contre-cas « a WEAPON upgrade » : 03009 est Restricted mais pas WEAPON (trait ITEM)",
       [HEROS, _arme("03009")], [],
       {"en_main": ["tc005"], "en_jeu": ["03009"], "degats": [["01094", 0]]},
       main_exclusive=["tc005"], jouer=["tc005"], cibles=["01094"]),
    _c("tc001a Overswing : ne paie PAS une carte qui n'est pas un evenement ATTACK/THWART/DEFENSE (Anything Goes, amelioration cout 1)",
       "« for an ATTACK, THWART, or DEFENSE EVENT » : une amelioration reste en main, l'arme reste en jeu",
       [HEROS, _arme("tc007")], [],
       {"en_main": ["tc006"], "en_jeu": ["tc007"]},
       main_exclusive=["tc006"], jouer=["tc006"]),
    _c("tc001a Overswing : ne paie PAS un evenement sans trait ATTACK/THWART/DEFENSE (First Aid 01086, evenement de base)",
       "contre-cas sur le TYPE Event : un evenement dont les traits ne sont pas ceux de la liste n'est pas finance par Overswing",
       [HEROS, _arme("tc007")], [],
       {"en_main": ["01086"], "en_jeu": ["tc007"]},
       main_exclusive=["01086"], jouer=["01086"]),
    _c("tc001a Overswing : paie aussi un evenement ATTACK moins cher (Face-Off, cout 2) : les 3 wild couvrent 2",
       "temoin positif du cout : Face-Off (2) est paye, 3 degats au vilain (l'excedent est perdu)",
       [HEROS, _arme("tc007")], [],
       {"degats": [["01094", 3]], "defausse": ["tc004", "tc007"]},
       main_exclusive=["tc004"], jouer=["tc004"], cibles=["01094"]),
    _c("tc001a Overswing : LIMITE une fois par phase (temoin d'epuisement) : 2e carte non payable, 2e arme intacte, 8 degats et non 11",
       "deux armes Restricted en jeu, Grand Slam puis Face-Off dans la MEME phase : le 2e Overswing est refuse, donc Face-Off reste en main ; "
       "chiffre mesure au 2e declenchement = les degats du vilain (8, jamais 11)",
       [HEROS, _arme("tc007"), _arme("tc010")], [],
       {"degats": [["01094", 8]], "en_main": ["tc004"], "en_jeu": ["tc010"], "hors_jeu": ["tc007"]},
       main_exclusive=["tc005", "tc004"], jouer=["tc005", "tc004"], cibles=["01094"]),
    _c("tc001a Overswing : temoin SANS limite atteinte (une seule carte jouee) : le 2e usage reste possible a la phase suivante, ici la 2e arme est intacte",
       "ligne de base du temoin precedent : sans 2e carte, la 2e arme n'est pas touchee (une seule defausse par usage)",
       [HEROS, _arme("tc007"), _arme("tc010")], [],
       {"degats": [["01094", 8]], "en_jeu": ["tc010"], "hors_jeu": ["tc007"]},
       main_exclusive=["tc005"], jouer=["tc005"], cibles=["01094"]),
    # ===================================================================== tc001b Casey Jones (alter-ego)
    _c("tc001b Setup : la vraie mise en place met le Sac (tc013) en jeu, attache a l'identite, tire du deck",
       "« Setup: Search your deck and discard pile for the Casey's Bag upgrade and put it into play » : vraie mise en place (main 6, deck 10)",
       [], [],
       {"en_jeu": ["tc013"], "attaches": [["tc001b", "tc013"]], "taille_main": 6},
       avec_boost=True),
    _c("tc001b Setup : le Sac dans la DEFAUSSE (mulligan, defausse) est trouve aussi : « deck AND discard pile »",
       "le Setup rejoue apres que le cas a deplace tc013 dans la defausse ; la recherche couvre les DEUX zones",
       [], [],
       {"depart": "defausse", "en_jeu": ["tc013"]}, verifier="casey_resetup"),
    _c("tc001b Setup : le Sac dans la MAIN de depart est AUSSI trouve et mis en jeu (decision utilisateur Q2)",
       "DECISION UTILISATEUR (16/10/2026, Q2) : fouiller aussi la main, comme tm001b de Michelangelo ; le Sac est toujours mis en jeu au Setup, meme s'il est dans la main de depart (environ 1 partie sur 3)",
       [], [],
       {"depart": "main", "en_jeu": ["tc013"]}, verifier="casey_resetup"),
    _c("tc001b Setup : le Sac dans le DECK (apres un rejeu du Setup) est trouve, mis en jeu et le deck perd la carte",
       "meme montage que les deux cas precedents, avec le Sac remis dans le deck : branche « deck » de la recherche",
       [], [],
       {"depart": "deck", "en_jeu": ["tc013"]}, verifier="casey_resetup"),
    _c("tc001b Response : en repassant en alter-ego, ramene l'arme de la defausse en main (WEAPON quelconque, ici la Baseball Bat)",
       "« After you change to this form, return a WEAPON upgrade from your discard pile to your hand »",
       [HEROS, "Puzzle.CreatePlayerDiscardPile('tc007')"], [CIVIL],
       {"en_main": ["tc007"], "forme": "AlterEgo"}, cibles=["tc007"]),
    _c("tc001b Response : le choix est LIBRE parmi les armes de la defausse (Baseball Bat OU Raphael's Sai) : on designe la Sai",
       "« A WEAPON upgrade » : pas seulement celles de Casey ; une seule carte revient, l'autre reste en defausse",
       [HEROS, "Puzzle.CreatePlayerDiscardPile('tc007', 'tr011')"], [CIVIL],
       {"en_main": ["tr011"], "defausse": ["tc007"], "forme": "AlterEgo"}, cibles=["tr011"]),
    _c("tc001b Response : une amelioration qui n'est PAS une arme (Donatello's Shell td012, ARMOR. TECH.) ne revient pas",
       "contre-cas « a WEAPON upgrade » : la Carapace reste en defausse (carte d'un autre heros : absente de la main de depart)",
       [HEROS, "Puzzle.CreatePlayerDiscardPile('td012')"], [CIVIL],
       {"defausse": ["td012"], "absent_main": ["td012"], "forme": "AlterEgo"}),
    _c("tc001b Response : en passant en forme HEROS rien ne revient (contre-cas « to THIS form »)",
       "la Response est imprimee sur la face alter-ego : le changement vers le heros ne la declenche pas",
       ["Puzzle.CreatePlayerDiscardPile('tc007')"], [HEROS],
       {"defausse": ["tc007"], "absent_main": ["tc007"], "forme": "Hero"}),
    _c("tc001b Response : defausse sans arme : rien ne revient, aucun plantage",
       "defausse vide d'arme : la Response n'est pas offerte",
       [HEROS], [CIVIL],
       {"forme": "AlterEgo", "taille_main": 6}),
    # ===================================================================== tc002 Clap Back
    _c("tc002 Clap Back : retire 5 menaces (6 -> 1), payee sans arme : l'ennemi n'est PAS confus",
       "« Remove 5 threat from a scheme » ; sans arme defaussee « to pay for this card », pas de confusion",
       [HEROS, "Puzzle.SetThreat('01097b', 6)"], [],
       {"menace": [["01097b", 1]], "defausse": ["tc002"], "statuts_absents": [["01094", "Confused"]]},
       main_exclusive=["tc002", "01088", "01089"], payer_avec=["01088", "01089"], jouer=["tc002"], cibles=["01097b"]),
    _c("tc002 Clap Back : payee par Overswing en defaussant une arme de CASEY (Baseball Bat) : 5 menaces ET ennemi confus",
       "« If a Casey Jones WEAPON upgrade was discarded to pay for this card, confuse an enemy » : Overswing est la seule source",
       [HEROS, "Puzzle.SetThreat('01097b', 6)", _arme("tc007")], [],
       {"menace": [["01097b", 1]], "defausse": ["tc002", "tc007"], "statuts": [["01094", "Confused"]]},
       main_exclusive=["tc002"], jouer=["tc002"], cibles=["01097b", "01094"]),
    _c("tc002 Clap Back : payee par Overswing en defaussant une arme d'un AUTRE heros (Raphael's Sai) : 5 menaces, PAS de confusion",
       "« a CASEY JONES WEAPON » : le Sai de Raphael est WEAPON mais pas du set Casey Jones (Q1) : contre-cas de portee",
       [HEROS, "Puzzle.SetThreat('01097b', 6)", _arme("tr011")], [],
       {"menace": [["01097b", 1]], "defausse": ["tc002", "tr011"], "statuts_absents": [["01094", "Confused"]]},
       main_exclusive=["tc002"], jouer=["tc002"], cibles=["01097b", "01094"]),
    _c("tc002 Clap Back : une arme de Casey defaussee AVANT (pas pour payer) ne compte pas : payee en ressources, ennemi pas confus",
       "« discarded TO PAY for this card » : la marque vit sur l'effet de cette carte seulement",
       [HEROS, "Puzzle.SetThreat('01097b', 6)", _arme("tc007")], ["Puzzle.Discard('tc007')"],
       {"menace": [["01097b", 1]], "statuts_absents": [["01094", "Confused"]]},
       main_exclusive=["tc002", "01088", "01089"], payer_avec=["01088", "01089"], jouer=["tc002"], cibles=["01097b", "01094"]),
    _c("tc002 Clap Back : sous Crise le complot principal n'est pas offert, mais une manigance annexe l'est (menace 7 -> 2 sur l'annexe)",
       "label `thwart` : le verrou de ciblage de la Crise s'applique (mots-cles/crisis.md) ; 01108 Crowd Control (Crise 1) en jeu, cible l'annexe",
       [HEROS, "Puzzle.PutIntoPlay('01108')", "Puzzle.SetThreat('01108', 7)", "Puzzle.SetThreat('01097b', 6)"], [],
       {"menace": [["01108", 2], ["01097b", 6]]},
       main_exclusive=["tc002", "01088", "01089"], payer_avec=["01088", "01089"], jouer=["tc002"], cibles=["01108"]),
    # ===================================================================== tc003 Cross Block
    _c("tc003 Cross Block : +3 DEF a la defense (DEF 5 contre ATQ 3 : 0 degat), Casey REDRESSE et recoit Tough",
       "Rhino ATQ 2 + 1 icone de boost = 3 contre DEF 2 : 1 degat sans la carte (cas temoin) ; avec +3 : 0 ; puis « ready Casey Jones and give him a tough status card »",
       [HEROS] + UNE_ICONE, ["Puzzle.Defend('tc001a', '01094')"],
       {"degats_identite": 0, "defausse": ["tc003"], "pret": ["tc001a"], "statuts": [["tc001a", "Tough"]]},
       main_exclusive=["tc003", "01088"], payer_avec=["01088"], avec_boost=True),
    _c("tc003 Cross Block : TEMOIN sans la carte : la meme defense laisse 1 degat, Casey incline, sans Tough",
       "ligne de base : DEF 2 contre 3 = 1 degat ; Casey s'incline en defendant et ne recoit aucun Tough",
       [HEROS] + UNE_ICONE, ["Puzzle.Defend('tc001a', '01094')"],
       {"degats_identite": 1, "exhausted": ["tc001a"], "statuts_absents": [["tc001a", "Tough"]]},
       main_exclusive=["01088"], avec_boost=True),
    _c("tc003 Cross Block : payee par Overswing (arme defaussee) : le DEFENSE event est finance par les 3 wild",
       "« DEFENSE event » : la Baseball Bat part en defausse, +3 DEF, Casey pret",
       [HEROS, _arme("tc007")] + UNE_ICONE, ["Puzzle.Defend('tc001a', '01094')"],
       {"degats_identite": 0, "defausse": ["tc003", "tc007"], "pret": ["tc001a"], "statuts": [["tc001a", "Tough"]]},
       main_exclusive=["tc003"], avec_boost=True),
    _c("tc003 Cross Block : « When YOU defend » : quand un ALLIE defend, la carte n'est pas jouee",
       "`is_basic_defense` + « You » : Splinter (allie) defend, Cross Block reste en main",
       [HEROS, "Puzzle.PutIntoPlay('tl002', under_control=True)"] + UNE_ICONE, ["Puzzle.Defend('tl002', '01094')"],
       {"en_main": ["tc003"], "statuts_absents": [["tc001a", "Tough"]]},
       main_exclusive=["tc003", "01088"], payer_avec=["01088"], avec_boost=True),
    # ===================================================================== tc004 Face-Off
    _c("tc004 Face-Off : 3 degats a Rhino, Casey REDRESSE puis Rhino L'ATTAQUE : Casey defend (DEF 2 contre ATQ 2 : 0 degat) et s'incline",
       "Casey incline au depart : « Ready your hero and deal 3 damage to an enemy. That enemy attacks you » : redresse, 3 degats, Rhino attaque et Casey peut defendre",
       [HEROS, "Puzzle.Exhaust('tc001a')"], [],
       {"degats": [["01094", 3]], "degats_identite": 0, "exhausted": ["tc001a"], "defausse": ["tc004"]},
       main_exclusive=["tc004", "01090"], payer_avec=["01090"], jouer=["tc004"], cibles=["01094"]),
    _c("tc004 Face-Off : TEMOIN sans la carte : Casey incline, l'attaque de Rhino passe en entier (2 degats)",
       "ligne de base du precedent : sans « ready », l'attaque de Rhino (ATQ 2) frappe un heros incline",
       [HEROS, "Puzzle.Exhaust('tc001a')"], ["Puzzle.Attack('01094')"],
       {"degats_identite": 2}, main_exclusive=["01090"]),
    _c("tc004 Face-Off : l'ennemi vaincu par les 3 degats n'attaque PAS (Hydra Mercenary, 3 PV) et Casey reste REDRESSE",
       "« THAT enemy attacks you » : un sbire hors jeu ne frappe pas ; aucune defense donc Casey, redresse par la carte, reste pret",
       [HEROS, "Puzzle.Exhaust('tc001a')", "Puzzle.PutIntoPlay('01101')"], [],
       {"hors_jeu": ["01101"], "degats_identite": 0, "pret": ["tc001a"], "defausse": ["tc004"]},
       main_exclusive=["tc004", "01090"], payer_avec=["01090"], jouer=["tc004"], cibles=["01101"]),
    _c("tc004 Face-Off : la carte est PAYEE par Overswing (arme defaussee) : Casey redresse, 3 degats, attaque en retour",
       "Face-Off est un evenement ATTACK : financable par Overswing",
       [HEROS, _arme("tc007"), "Puzzle.Exhaust('tc001a')"], [],
       {"degats": [["01094", 3]], "defausse": ["tc004", "tc007"], "degats_identite": 0},
       main_exclusive=["tc004"], jouer=["tc004"], cibles=["01094"]),
    # ===================================================================== tc005 Grand Slam
    _c("tc005 Grand Slam : Requirement wild satisfait par une vraie carte wild (Rocket Raccoon 16019, RES wild) + Strength RR : 8 degats",
       "Requirement ([wild]) : le paiement (cout 3) doit COMPORTER une ressource wild ; wild 1 + RR 2 = 3, sans Overswing",
       [HEROS], [],
       {"degats": [["01094", 8]], "defausse": ["tc005"]},
       main_exclusive=["tc005", "16019", "01090"], payer_avec=["16019", "01090"], jouer=["tc005"], cibles=["01094"]),
    _c("tc005 Grand Slam : Requirement wild NON satisfait (Strength RR + Energy YY, aucune wild) : refusee, reste en main",
       "contre-cas du Requirement : 4 icones payables mais aucune wild : la carte n'est pas jouable",
       [HEROS], [],
       {"en_main": ["tc005"], "degats": [["01094", 0]]},
       main_exclusive=["tc005", "01090", "01088"], payer_avec=["01090", "01088"], jouer=["tc005"], cibles=["01094"]),
    _c("tc005 Grand Slam : 8 degats au MINION choisi (Hydra Mercenary, 3 PV : vaincu), pas au vilain",
       "« Deal 8 damage to AN enemy » : l'ennemi designe seul ; le vilain n'est pas touche",
       [HEROS, _arme("tc007"), "Puzzle.PutIntoPlay('01101')"], [],
       {"hors_jeu": ["01101"], "degats": [["01094", 0]]},
       main_exclusive=["tc005"], jouer=["tc005"], cibles=["01101"]),
    # ===================================================================== tc006 Anything Goes
    _c("tc006 Anything Goes : ECHANGE la Baseball Bat (en jeu) et le Cricket Willow (range sous le Sac) : la batte est rangee, le Willow entre en jeu",
       "« swap a Casey Jones WEAPON upgrade you control with a Casey Jones WEAPON upgrade tucked under Casey's Bag » : l'arme en jeu part SOUS le Sac (pas en defausse), la rangee entre en jeu, attachee a Casey ; Anything Goes s'incline",
       [HEROS, _arme("tc013"), _arme("tc006"), _arme("tc007"), "Puzzle.PlaceUnder('tc009', 'tc013')"],
       ["Puzzle.Action('tc006', 'HeroAction')"],
       {"en_jeu": ["tc009"], "hors_jeu": ["tc007"], "pose_sous": [["tc013", "tc007"]], "taille_pose_sous": [["tc013", 1]],
        "exhausted": ["tc006"], "pret": ["tc009"], "attaches": [["tc001a", "tc009"]]},
       main_exclusive=["01090"], cibles=["tc007"]),
    _c("tc006 Anything Goes : la limite Restricted n'empeche pas l'echange (deux Restricted en jeu, on range d'abord)",
       "deux armes Restricted en jeu (la limite du heros), une 3e rangee : l'echange doit passer, sinon la 3e serait refusee a l'entree",
       [HEROS, _arme("tc013"), _arme("tc006"), _arme("tc007"), _arme("tc010"), "Puzzle.PlaceUnder('tc009', 'tc013')"],
       ["Puzzle.Action('tc006', 'HeroAction')"],
       {"en_jeu": ["tc009", "tc010"], "hors_jeu": ["tc007"], "pose_sous": [["tc013", "tc007"]]},
       main_exclusive=["01090"], cibles=["tc007"]),
    _c("tc006 Anything Goes : deux armes rangees : le joueur CHOISIT laquelle entre (on designe le Hockey Stick, pas le Willow)",
       "le choix de la carte entrante est libre parmi les armes de Casey rangees ; l'autre reste sous le Sac",
       [HEROS, _arme("tc013"), _arme("tc006"), _arme("tc007"), "Puzzle.PlaceUnder('tc009', 'tc013')", "Puzzle.PlaceUnder('tc011', 'tc013')"],
       ["Puzzle.Action('tc006', 'HeroAction')"],
       {"en_jeu": ["tc011"], "hors_jeu": ["tc007", "tc009"], "pose_sous": [["tc013", "tc007"], ["tc013", "tc009"]],
        "taille_pose_sous": [["tc013", 2]]},
       main_exclusive=["01090"], cibles=["tc007", "tc011"]),
    _c("tc006 Anything Goes : aucune arme rangee sous le Sac : l'Action n'est PAS offerte",
       "les DEUX moities sont exigees : sans arme tucked, pas d'echange (et Anything Goes n'est pas incline pour rien)",
       [HEROS, _arme("tc013"), _arme("tc006"), _arme("tc007")], [],
       {"carte": "tc006", "type": "HeroAction", "nombre": 0}, verifier="casey_actions", main_exclusive=["01090"]),
    _c("tc006 Anything Goes : aucune arme de Casey EN JEU (seulement le Sai de Raphael) : l'Action n'est PAS offerte",
       "« a Casey Jones WEAPON upgrade you control » : le Sai (WEAPON d'un autre set) ne compte pas",
       [HEROS, _arme("tc013"), _arme("tc006"), _arme("tr011"), "Puzzle.PlaceUnder('tc009', 'tc013')"], [],
       {"carte": "tc006", "type": "HeroAction", "nombre": 0}, verifier="casey_actions", main_exclusive=["01090"]),
    _c("tc006 Anything Goes : l'arme RANGEE doit etre une arme de Casey (le Sai de Raphael range sous le Sac ne compte pas)",
       "« a Casey Jones WEAPON upgrade TUCKED »",
       [HEROS, _arme("tc013"), _arme("tc006"), _arme("tc007"), "Puzzle.PlaceUnder('tr011', 'tc013')"], [],
       {"carte": "tc006", "type": "HeroAction", "nombre": 0}, verifier="casey_actions", main_exclusive=["01090"]),
    _c("tc006 Anything Goes : TEMOIN positif : une arme de Casey en jeu ET une rangee : l'Action est offerte (1)",
       "contre-cas des trois precedents : la meme position complete offre bien l'Action",
       [HEROS, _arme("tc013"), _arme("tc006"), _arme("tc007"), "Puzzle.PlaceUnder('tc009', 'tc013')"], [],
       {"carte": "tc006", "type": "HeroAction", "nombre": 1}, verifier="casey_actions", main_exclusive=["01090"]),
    # ===================================================================== tc007 Baseball Bat
    _c("tc007 Baseball Bat : +1 a l'ATTAQUE de base (ATQ 2 -> 3 : 3 degats a Rhino), la batte s'incline",
       "« When you use a basic power, exhaust Baseball Bat -> you get +1 to that power for this use »",
       [HEROS, _arme("tc007")], ["Puzzle.Attack('tc001a')"],
       {"degats": [["01094", 3]], "exhausted": ["tc007"]}, main_exclusive=["01090"], cibles=["01094"]),
    _c("tc007 Baseball Bat : +1 au CONTRE de base (CTR 2 -> 3 : menace 6 -> 3)",
       "le pouvoir de base utilise peut etre le contre : `GainValue` route vers THW",
       [HEROS, _arme("tc007"), "Puzzle.SetThreat('01097b', 6)"], ["Puzzle.Thwart('tc001a')"],
       {"menace": [["01097b", 3]], "exhausted": ["tc007"]}, main_exclusive=["01090"]),
    _c("tc007 Baseball Bat : +1 a la DEFENSE de base (DEF 2 -> 3 contre ATQ 3 : 0 degat)",
       "Rhino ATQ 2 + 1 icone de boost = 3 : sans la batte 1 degat (voir tc003, temoin)",
       [HEROS, _arme("tc007")] + UNE_ICONE, ["Puzzle.Defend('tc001a', '01094')"],
       {"degats_identite": 0, "exhausted": ["tc007"]}, main_exclusive=["01090"], avec_boost=True),
    _c("tc007 Baseball Bat : « When YOU use » : l'attaque d'un ALLIE (Splinter) n'est pas amelioree, la batte reste prete",
       "« You » = l'identite : l'allie frappe a sa valeur imprimee (2)",
       [HEROS, _arme("tc007"), "Puzzle.PutIntoPlay('tl002', under_control=True)"], ["Puzzle.Attack('tl002')"],
       {"degats": [["01094", 2]], "pret": ["tc007"]}, main_exclusive=["01090"], cibles=["01094"]),
    # ===================================================================== tc008 Casey's Mask
    _c("tc008 Casey's Mask : redresse Casey Jones (identite incline au depart), le Masque s'incline",
       "« Hero Action: Exhaust Casey's Mask -> ready Casey Jones » : cout d'inclinaison puis redressement de l'identite",
       [HEROS, _arme("tc008"), "Puzzle.Exhaust('tc001a')"], ["Puzzle.Action('tc008', 'HeroAction')"],
       {"pret": ["tc001a"], "exhausted": ["tc008"]}, main_exclusive=["01090"]),
    _c("tc008 Casey's Mask : en forme ALTER-EGO l'Action n'est pas offerte (Hero Action), le Masque reste pret",
       "contre-cas de forme : `HeroAction` seulement en forme heros",
       [_arme("tc008")], [],
       {"carte": "tc008", "type": "HeroAction", "nombre": 0}, verifier="casey_actions", main_exclusive=["01090"]),
    _c("tc008 Casey's Mask : une 2e Mask ne peut pas entrer en jeu (carte UNIQUE : `desc` « * »)",
       "le Masque est unique : un seul exemplaire en jeu (regle moteur, nom prefixe « * »)",
       [HEROS, _arme("tc008"), "Puzzle.CreateHandCards('tc008')"], [],
       {"en_main": ["tc008"], "en_jeu": ["tc008"]}, main_exclusive=["01090"], jouer=["tc008"]),
    # ===================================================================== tc009 Cricket Willow
    _c("tc009 Cricket Willow : « Your hero gets +1 ATK » : ATQ 2 -> 3 en forme heros",
       "bonus continu d'identite : `GiveKeywordToAttached(Hero, attack=1)`",
       [HEROS, _arme("tc009")], [],
       {"attributs": {"attack": 1}}, main_exclusive=["01090"]),
    _c("tc009 Cricket Willow : le bonus suit la FORME, pas le moment de la pose : pose en alter-ego puis passage en heros -> ATQ 2 -> 3",
       "« Your HERO gets +1 ATK » : l'arme attachee a Casey en civil donne +1 des que la face heros revient (le filtre est le type Hero)",
       [_arme("tc009")], [HEROS],
       {"attributs": {"attack": 1}, "forme": "Hero"}, main_exclusive=["01090"]),
    _c("tc009 Cricket Willow : CONTRE-CAS dans l'AUTRE forme : retour en alter-ego avec le Willow en jeu, aucune erreur, le Willow reste attache",
       "un alter-ego n'a pas d'ATQ : l'arme ne doit rien lui donner (ni planter) ; elle reste en jeu, attachee a l'identite",
       [HEROS, _arme("tc009")], [CIVIL],
       {"forme": "AlterEgo", "en_jeu": ["tc009"], "attaches": [["tc001b", "tc009"]]}, main_exclusive=["01090"]),
    _c("tc009 Cricket Willow : apres l'attaque, defausse le Willow et ETOURDIT l'ennemi attaque (Rhino 3 degats, Stunned)",
       "« After you attack an enemy, discard Cricket Willow -> stun that enemy » : ATQ 2+1 = 3 degats, puis le cout (defausse) et le statut",
       [HEROS, _arme("tc009")], ["Puzzle.Attack('tc001a')"],
       {"degats": [["01094", 3]], "statuts": [["01094", "Stunned"]], "defausse": ["tc009"], "hors_jeu": ["tc009"]},
       main_exclusive=["01090"], cibles=["01094"]),
    _c("tc009 Cricket Willow : l'ennemi VAINCU par l'attaque (Hydra Mercenary, 3 PV) n'est pas etourdi : le Willow reste en jeu",
       "« stun THAT enemy » : plus d'ennemi, la Reponse n'est pas offerte et la defausse (cout) n'est pas payee pour rien",
       [HEROS, _arme("tc009"), "Puzzle.PutIntoPlay('01101')"], ["Puzzle.Attack('tc001a')"],
       {"hors_jeu": ["01101"], "en_jeu": ["tc009"]},
       main_exclusive=["01090"], cibles=["01101"]),
    # ===================================================================== tc010 Driving Iron
    _c("tc010 Driving Iron : option « 1 degat a un ennemi » (Rhino -1), le Driving Iron s'incline",
       "« deal 1 damage to an enemy, or remove 1 threat from a scheme » : branche degats",
       [HEROS, _arme("tc010"), "Puzzle.SetThreat('01097b', 5)"], ["Puzzle.Action('tc010', 'HeroAction')"],
       {"degats": [["01094", 1]], "menace": [["01097b", 5]], "exhausted": ["tc010"]},
       main_exclusive=["01090"], cibles=["01094"], preferer_option=["Deal 1 damage"]),
    _c("tc010 Driving Iron : option « retirer 1 menace » (5 -> 4), pas de degats",
       "branche menace : UN SEUL des deux effets (choix du joueur)",
       [HEROS, _arme("tc010"), "Puzzle.SetThreat('01097b', 5)"], ["Puzzle.Action('tc010', 'HeroAction')"],
       {"degats": [["01094", 0]], "menace": [["01097b", 4]], "exhausted": ["tc010"]},
       main_exclusive=["01090"], cibles=["01097b"], preferer_option=["Remove 1 threat"]),
    _c("tc010 Driving Iron : en forme ALTER-EGO l'Action n'est pas offerte (Hero Action)",
       "contre-cas de forme",
       [_arme("tc010")], [],
       {"carte": "tc010", "type": "HeroAction", "nombre": 0}, verifier="casey_actions", main_exclusive=["01090"]),
    # ===================================================================== tc011 Hockey Stick
    _c("tc011 Hockey Stick : +2 a l'ATTAQUE de base (ATQ 2 -> 4 : 4 degats), le bâton s'incline",
       "« When you make a basic attack or defense, exhaust Hockey Stick -> +2 to that power for this use »",
       [HEROS, _arme("tc011")], ["Puzzle.Attack('tc001a')"],
       {"degats": [["01094", 4]], "exhausted": ["tc011"]}, main_exclusive=["01090"], cibles=["01094"]),
    _c("tc011 Hockey Stick : +2 a la DEFENSE de base (DEF 2 -> 4 contre ATQ 3 : 0 degat)",
       "second pouvoir cite : la defense",
       [HEROS, _arme("tc011")] + UNE_ICONE, ["Puzzle.Defend('tc001a', '01094')"],
       {"degats_identite": 0, "exhausted": ["tc011"]}, main_exclusive=["01090"], avec_boost=True),
    _c("tc011 Hockey Stick : CONTRE-CAS : aucun bonus au CONTRE de base (CTR 2 : menace 6 -> 4), le baton reste pret",
       "« basic attack OR DEFENSE » : le contre n'est pas cite (filtre `powers=[ATK, DEF]`)",
       [HEROS, _arme("tc011"), "Puzzle.SetThreat('01097b', 6)"], ["Puzzle.Thwart('tc001a')"],
       {"menace": [["01097b", 4]], "pret": ["tc011"]}, main_exclusive=["01090"]),
    # ===================================================================== tc012 Persuader
    _c("tc012 Persuader : +1 ATQ continu ET +1 pour cette attaque (ATQ 2 -> 4 : 4 degats), le Persuader s'incline",
       "« Your hero gets +1 ATK » (continu) puis « +1 ATK for that attack » (Interruption) : 2 + 1 + 1 = 4",
       [HEROS, _arme("tc012")], ["Puzzle.Attack('tc001a')"],
       {"degats": [["01094", 4]], "exhausted": ["tc012"]}, main_exclusive=["01090"], cibles=["01094"]),
    _c("tc012 Persuader : « This attack gains PIERCING » : le Tough de Rhino est defausse ET les 4 degats passent",
       "avec Persuader, l'attaque perfore : degats 4 et plus de Tough (voir le temoin sans carte : 0 degat)",
       [HEROS, _arme("tc012"), "Puzzle.Tough('01094')"], ["Puzzle.Attack('tc001a')"],
       {"degats": [["01094", 4]], "statuts_absents": [["01094", "Tough"]]}, main_exclusive=["01090"], cibles=["01094"]),
    _c("tc012 Persuader : TEMOIN sans piercing : une attaque sans arme contre un Rhino Tough : 0 degat, le Tough est defausse",
       "ligne de base du precedent : le Tough absorbe l'attaque ordinaire (sans lui le cas piercing ne prouverait rien)",
       [HEROS, "Puzzle.Tough('01094')"], ["Puzzle.Attack('tc001a')"],
       {"degats": [["01094", 0]], "statuts_absents": [["01094", "Tough"]]}, main_exclusive=["01090"], cibles=["01094"]),
    _c("tc012 Persuader : CONTRE-CAS : a la DEFENSE l'Interruption ne part pas (DEF 2 contre ATQ 3 : 1 degat), le Persuader reste pret",
       "« basic ATTACK » seulement",
       [HEROS, _arme("tc012")] + UNE_ICONE, ["Puzzle.Defend('tc001a', '01094')"],
       {"degats_identite": 1, "pret": ["tc012"]}, main_exclusive=["01090"], avec_boost=True),
    _c("tc012 Persuader : CONTRE-CAS : au CONTRE de base l'Interruption ne part pas (CTR 2 : menace 6 -> 4)",
       "« basic attack » seulement : pas de bonus ni de piercing au contre",
       [HEROS, _arme("tc012"), "Puzzle.SetThreat('01097b', 6)"], ["Puzzle.Thwart('tc001a')"],
       {"menace": [["01097b", 4]], "pret": ["tc012"]}, main_exclusive=["01090"]),
    _c("tc012 Persuader : « Your hero gets +1 ATK » continu : ATQ 2 -> 3 en forme heros",
       "bonus continu d'identite", [HEROS, _arme("tc012")], [],
       {"attributs": {"attack": 1}}, main_exclusive=["01090"]),
    _c("tc012 Persuader : le bonus suit la FORME : pose en alter-ego puis passage en heros -> ATQ 2 -> 3",
       "« Your HERO gets +1 ATK » : filtre de type Hero, voir tc009",
       [_arme("tc012")], [HEROS],
       {"attributs": {"attack": 1}, "forme": "Hero"}, main_exclusive=["01090"]),
    _c("tc012 Persuader : CONTRE-CAS dans l'AUTRE forme : retour en alter-ego avec le Persuader en jeu, aucune erreur, il reste attache",
       "un alter-ego n'a pas d'ATQ : l'arme ne doit rien lui donner ni planter",
       [HEROS, _arme("tc012")], [CIVIL],
       {"forme": "AlterEgo", "en_jeu": ["tc012"], "attaches": [["tc001b", "tc012"]]}, main_exclusive=["01090"]),
    # ===================================================================== tc013 Casey's Bag
    _c("tc013 Casey's Bag : on peut JOUER une carte rangee dessous (Baseball Bat, cout 1, payee par Energy) : elle entre en jeu",
       "« You may play cards tucked here as if they were in your hand » : la batte est glissee sous le Sac, puis jouee PAR LE VRAI CHEMIN "
       "(le moteur doit l'OFFRIR ; `Puzzle.Gain` la ramenerait en main et ne prouverait rien)",
       [HEROS, _arme("tc013"), "Puzzle.PlaceUnder('tc007', 'tc013')"], [],
       {"carte": "tc007", "en_jeu": ["tc007"], "taille_pose_sous": [["tc013", 0]], "attaches": [["tc001a", "tc007"]]},
       main_exclusive=["01088"], payer_avec=["01088"], verifier="casey_jouer_sous_le_sac"),
    _c("tc013 Casey's Bag : TOUT type de carte rangee se joue (Face-Off, evenement cout 2, payee par Strength) : 3 degats",
       "« cards tucked here » sans filtre de type : un evenement rangé sous le Sac est offert et resolu",
       [HEROS, _arme("tc013"), "Puzzle.PlaceUnder('tc004', 'tc013')"], [],
       {"carte": "tc004", "degats": [["01094", 3]], "defausse": ["tc004"], "taille_pose_sous": [["tc013", 0]]},
       main_exclusive=["01090"], payer_avec=["01090"], cibles=["01094"], verifier="casey_jouer_sous_le_sac"),
    _c("tc013 Casey's Bag : TEMOIN : une carte rangee sous une AUTRE carte (Casey's Mask tc008, sans permission de jeu) n'est PAS offerte",
       "le Sac ne rend jouables que SES cartes (`ThisPlacedCard`) : la Baseball Bat glissee sous le Masque reste injouable",
       [HEROS, _arme("tc013"), _arme("tc008"), "Puzzle.PlaceUnder('tc007', 'tc008')"], [],
       {"carte": "tc007", "refuse_sous": "tc013"}, main_exclusive=["01088"], verifier="casey_jouer_sous_le_sac"),
    _c("tc013 Casey's Bag : Hero Action : range la PLUS BASSE arme de la defausse (la Baseball Bat, devant le Willow), le Sac s'incline",
       "« tuck the bottommost WEAPON upgrade in your discard pile under this card » : defausse [tc007 (fond), tc009] -> tc007 rangee, tc009 reste",
       [HEROS, _arme("tc013"), "Puzzle.CreatePlayerDiscardPile('tc007', 'tc009')"], ["Puzzle.Action('tc013', 'HeroAction')"],
       {"pose_sous": [["tc013", "tc007"]], "taille_pose_sous": [["tc013", 1]], "defausse": ["tc009"], "exhausted": ["tc013"]},
       main_exclusive=["01090"]),
    _c("tc013 Casey's Bag : « bottommost WEAPON » : une carte qui n'est pas une arme au FOND est sautee (Shell td012 puis Baseball Bat)",
       "le fond de la defausse est la Carapace (pas une arme) : la plus basse ARME est la batte",
       [HEROS, _arme("tc013"), "Puzzle.CreatePlayerDiscardPile('td012', 'tc007', 'tc009')"], ["Puzzle.Action('tc013', 'HeroAction')"],
       {"pose_sous": [["tc013", "tc007"]], "defausse": ["td012", "tc009"]},
       main_exclusive=["01090"]),
    _c("tc013 Casey's Bag : n'importe quelle arme se range (pas seulement celles de Casey) : le Sai de Raphael est la plus basse",
       "« the bottommost WEAPON upgrade » sans mention de Casey Jones",
       [HEROS, _arme("tc013"), "Puzzle.CreatePlayerDiscardPile('tr011', 'tc007')"], ["Puzzle.Action('tc013', 'HeroAction')"],
       {"pose_sous": [["tc013", "tr011"]], "defausse": ["tc007"]},
       main_exclusive=["01090"]),
    _c("tc013 Casey's Bag : aucune arme dans la defausse : l'Action n'est PAS offerte (le Sac ne s'incline pas pour rien)",
       "condition ecrite sur l'Action : « Exhaust » est un cout",
       [HEROS, _arme("tc013"), "Puzzle.CreatePlayerDiscardPile('td012')"], [],
       {"carte": "tc013", "type": "HeroAction", "nombre": 0}, verifier="casey_actions"),
    _c("tc013 Casey's Bag : en forme ALTER-EGO l'Action n'est pas offerte (Hero Action)",
       "contre-cas de forme",
       [_arme("tc013"), "Puzzle.CreatePlayerDiscardPile('tc007')"], [],
       {"carte": "tc013", "type": "HeroAction", "nombre": 0}, verifier="casey_actions", main_exclusive=["01090"]),
    _c("tc013 Casey's Bag : PERMANENT : un effet d'un autre set (Puzzle.Discard) ne le defausse pas",
       "mot-cle Permanent (desc, AUCUN SCRIPT) : le Sac reste en jeu",
       [HEROS, _arme("tc013")], [],
       {"en_jeu": ["tc013"]}, main_exclusive=["01090"], declencher_tolerant=["Puzzle.Discard('tc013')"]),
    # ===================================================================== tc014 Daddy Issues
    _c("tc014 Daddy Issues (recue en forme HEROS) : retourne Casey en alter-ego, non incline",
       "« Flip to alter-ego form » : l'obligation est donnee au joueur Casey Jones",
       [HEROS], ["Puzzle.Reveal('tc014')"],
       {"forme": "AlterEgo", "en_jeu": ["tc014"], "pret": ["tc001b"]}, main_exclusive=["01090"]),
    _c("tc014 Daddy Issues (recue en alter-ego) : reste alter-ego, obligation en jeu",
       "« flip » sans effet quand on l'est deja",
       [], ["Puzzle.Reveal('tc014')"],
       {"forme": "AlterEgo", "en_jeu": ["tc014"]}, main_exclusive=["01090"]),
    _c("tc014 Daddy Issues : « GiveTo Casey Jones » vise le BON joueur (2 joueurs : Casey en 2e siege, tous deux en forme heros)",
       "le joueur qui n'est pas Casey n'est pas retourne : Casey (siege 1) repasse en alter-ego, Spider-Man (siege 0) reste heros",
       ["Puzzle.ChangeToFace('01001b', '01001a')", "Puzzle.ChangeToFace('tc001b', 'tc001a')"], ["Puzzle.Reveal('tc014')"],
       {"forme_joueur": [[1, "AlterEgo"], [0, "Hero"]]},
       heros="spider_man", heros2="casey_jones", main_exclusive=["01090"], verifier="casey_etat"),
    _c("tc014 Daddy Issues : « You cannot change forms » : le passage en forme heros est refuse (reste alter-ego)",
       "`PlayersCannotChangeForms` sur le joueur rattache",
       [], ["Puzzle.Reveal('tc014')"],
       {"forme": "AlterEgo", "en_jeu": ["tc014"]}, main_exclusive=["01090"],
       declencher_apres=["Puzzle.ChangeForm('tc001b')"]),
    _c("tc014 Daddy Issues : Action = incline Casey Jones et RETIRE l'obligation DU JEU (pas la defausse)",
       "« Action: Exhaust Casey Jones -> remove Daddy Issues from the game » : cout d'inclinaison de l'identite ; l'obligation sort de la partie",
       [], ["Puzzle.Reveal('tc014')", "Puzzle.Action('tc014', 'Action')"],
       {"hors_jeu": ["tc014"], "exhausted": ["tc001b"], "forme": "AlterEgo"}, main_exclusive=["01090"]),
    _c("tc014 Daddy Issues : identite deja INCLINEE : l'Action n'est PAS offerte (le cout ne peut pas etre paye)",
       "« Exhaust Casey Jones » est un cout : une identite inclinee ne peut pas payer",
       [], ["Puzzle.Reveal('tc014')", "Puzzle.Exhaust('tc001b')"],
       {"carte": "tc014", "type": "Action", "nombre": 0}, verifier="casey_actions", main_exclusive=["01090"]),
    # ===================================================================== tc015 The Purple Dragons
    _c("tc015 The Purple Dragons : Incite 1 par joueur : a la revelation, 1 menace de plus sur le complot principal (1 joueur : +1)",
       "« Incite 1[per_hero] » : `desc.Incite = 1*` ; base automatique (menace du complot avant / apres)",
       [], ["Puzzle.Reveal('tc015')"],
       {"menace": [["01097b", 1]], "en_jeu": ["tc015"]}, main_exclusive=["01090"]),
    _c("tc015 The Purple Dragons : menace de depart 3 (sans icone par joueur : 3 meme a 2 joueurs)",
       "`StartingThreat = 3` (pas `3*`) : le scan imprime « 3 » sans icone de joueur",
       [], ["Puzzle.Reveal('tc015')"],
       {"menace": [["tc015", 3]]}, main_exclusive=["01090"], heros2="spider_man"),
    _c("tc015 The Purple Dragons : Incite 1 PAR JOUEUR : a 2 joueurs, +2 menaces sur le complot principal",
       "le glyphe « joueur » apres le 1 : valeur multipliee par le nombre de joueurs (`FormatPlayerNumValue`)",
       [], ["Puzzle.Reveal('tc015')"],
       {"menace": [["01097b", 2]]}, main_exclusive=["01090"], heros2="spider_man"),
    _c("tc015 The Purple Dragons : Crise 1 (glyphe central) : une manigance annexe a Crise est en jeu",
       "icone « ! » identique a 01108 Crowd Control (verifiee par decoupe) : base automatique `desc.Crisis`",
       [], ["Puzzle.Reveal('tc015')"],
       {"icones": [["Crisis", 1]]}, main_exclusive=["01090"]),
    # ===================================================================== tc016 Hun
    _c("tc016 Hun : entre en jeu avec une carte Tough (Toughness, base automatique)",
       "« Toughness. » : lu dans `desc`, aucun script",
       [], ["Puzzle.PutIntoPlay('tc016')"],
       {"statuts": [["tc016", "Tough"]], "en_jeu": ["tc016"]}, main_exclusive=["01090"]),
    _c("tc016 Hun : apres avoir attaque ET blesse un personnage, l'etourdit (Casey incline : ATQ 2 = 2 degats, Stunned)",
       "« Forced Response: After Hun attacks and damages a character, stun that character » : Casey incline ne se defend pas, 2 degats",
       [HEROS, "Puzzle.Exhaust('tc001a')", "Puzzle.PutIntoPlay('tc016')"], ["Puzzle.Attack('tc016')"],
       {"degats_identite": 2, "statuts": [["tc001a", "Stunned"]]}, main_exclusive=["01090"]),
    _c("tc016 Hun : une attaque qui ne blesse PAS (Casey DEFEND : DEF 2 contre ATQ 2 = 0 degat) n'etourdit pas",
       "contre-cas « attacks AND DAMAGES » : le journal de partie montre l'attaque a 0 degat (la defense de Casey), aucun statut pose",
       [HEROS, "Puzzle.PutIntoPlay('tc016')"], ["Puzzle.Attack('tc016')"],
       {"degats_identite": 0, "statuts_absents": [["tc001a", "Stunned"]], "exhausted": ["tc001a"]}, main_exclusive=["01090"]),
    _c("tc016 Hun : une attaque absorbee par Tough (Casey incline et Tenace : 0 degat) n'etourdit pas, le Tough est defausse",
       "meme contre-cas par une autre voie : l'attaque a lieu, Tough prevoit les degats",
       [HEROS, "Puzzle.Exhaust('tc001a')", "Puzzle.Tough('tc001a')", "Puzzle.PutIntoPlay('tc016')"], ["Puzzle.Attack('tc016')"],
       {"degats_identite": 0, "statuts_absents": [["tc001a", "Stunned"], ["tc001a", "Tough"]]}, main_exclusive=["01090"]),
    _c("tc016 Hun : « a CHARACTER » : un ALLIE blesse est etourdi aussi (Splinter defend : 2 degats sur 3 PV, Stunned)",
       "la Reponse vise le personnage attaque, pas « you » : Splinter (tl002, PV 3) declare la defense, l'identite n'est pas touchee",
       [HEROS, "Puzzle.PutIntoPlay('tc016')", "Puzzle.PutIntoPlay('tl002', under_control=True)"],
       ["Puzzle.Attack('tc016', 'tl002')"],
       {"degats": [["tl002", 2]], "statuts": [["tl002", "Stunned"]], "statuts_absents": [["tc001a", "Stunned"]], "degats_identite": 0},
       main_exclusive=["01090"]),
    # ===================================================================== tc017 Purple Dragon Goons
    _c("tc017 Purple Dragon Goons : When Revealed : place une carte Tough sur le VILAIN",
       "« Place a tough status card on the villain »",
       [], ["Puzzle.Reveal('tc017')"],
       {"statuts": [["01094", "Tough"]], "en_jeu": ["tc017"]}, main_exclusive=["01090"]),
    _c("tc017 Purple Dragon Goons : le vilain deja Tough n'en recoit pas un second (plafond du statut)",
       "`tough_max` : un seul Tough sur le vilain",
       [], ["Puzzle.Tough('01094')", "Puzzle.Reveal('tc017')"],
       {"statuts": [["01094", "Tough"]], "en_jeu": ["tc017"]}, main_exclusive=["01090"]),
    _c("tc017 Purple Dragon Goons : Guard : tant qu'il est engage, l'attaque de Casey ne peut viser QUE lui (Goons -2, Rhino intact)",
       "« Guard » (desc) : `Villain.CanBeAttackBy` ; le sbire lui-meme reste attaquable (c'est la facon de lever le blocage)",
       [HEROS, "Puzzle.PutIntoPlay('tc017')"], [],
       {"degats": [["tc017", 2], ["01094", 0]]}, main_exclusive=["01090"],
       declencher_tolerant=["Puzzle.Attack('tc001a')"]),
    _c("tc017 Purple Dragon Goons : TEMOIN sans Guard : la meme attaque frappe Rhino (2 degats)",
       "ligne de base du precedent : sans sbire Guard, le vilain est attaquable",
       [HEROS], [],
       {"degats": [["01094", 2]]}, main_exclusive=["01090"],
       declencher_tolerant=["Puzzle.Attack('tc001a')"]),
    _c("tc017 Purple Dragon Goons : Patrol : tant qu'il est engage, Casey ne peut pas contrer le complot principal (menace 4 inchangee)",
       "« Patrol » (desc) : `MainScheme.CanBeThwartBy` ; la menace ne bouge pas",
       [HEROS, "Puzzle.PutIntoPlay('tc017')", "Puzzle.SetThreat('01097b', 4)"], [],
       {"menace": [["01097b", 4]]}, main_exclusive=["01090"],
       declencher_tolerant=["Puzzle.Thwart('tc001a')"]),
    _c("tc017 Purple Dragon Goons : TEMOIN sans Patrol : le meme contre retire 2 menaces (4 -> 2)",
       "ligne de base du precedent : sans sbire Patrol, le complot principal est contrecarrable (CTR 2)",
       [HEROS, "Puzzle.SetThreat('01097b', 4)"], [],
       {"menace": [["01097b", 2]]}, main_exclusive=["01090"],
       declencher_tolerant=["Puzzle.Thwart('tc001a')"]),
    # ===================================================================== etape 6 : nombres et donnees imprimes (scan <-> cards.json)
    # Table relue sur les 18 scans (pas sur le script) : type, nom, unicite, traits, ensemble et `desc`.
    # Les cas portent « (tc001a-tc017) » SANS « <id> » suivi d'un espace : substituer_pack.py ne les compte pas.
    _c("etape 6 : donnees imprimees des deux faces d'identite et de l'obligation (cartes tc001a..tc014, identite et obligation)",
       "PV 10, ATQ 2, CTR 2, DEF 2, main 5 (heros) ; REC 4, PV 10, main 6 (alter-ego) ; obligation a 2 icones de boost",
       ["Puzzle.CreateHandCards('tc001a', 'tc001b', 'tc014')"], [],
       {"cartes": {
           "tc001a": {"type": "Hero", "name": "Casey Jones", "unique": True, "set_name": "Casey Jones", "traits": ["VIGILANTE"],
                      "desc": {"HP": "10", "ATK": "2", "THW": "2", "DEF": "2", "HS": "5"}},
           "tc001b": {"type": "AlterEgo", "name": "Casey Jones", "unique": True, "set_name": "Casey Jones", "traits": ["CIVILIAN"],
                      "desc": {"HP": "10", "REC": "4", "HS": "6"}},
           "tc014": {"type": "Obligation", "name": "Daddy Issues", "unique": False, "set_name": "Casey Jones", "traits": [],
                     "desc": {"Boost": "2", "GiveTo": "Casey Jones"}}}},
       verifier="casey_desc"),
    _c("etape 6 : donnees imprimees des evenements (cartes tc002..tc005, voir pourquoi)",
       "couts 3/2/2/3, ressources B/Y/R/R, Requirement wild de Grand Slam ; icones de ressource verifiees par decoupe contre 01088 (jaune = energie), 01089 (bleu = mental), 01090 (rouge = physique) : "
       ".planning/tmnt/pics-casey-icones/icons.png ; l'etoile de Grand Slam = wild (04010, wild.png)",
       ["Puzzle.CreateHandCards('tc002', 'tc003', 'tc004', 'tc005')"], [],
       {"cartes": {
           "tc002": {"type": "Event", "name": "Clap Back", "unique": False, "set_name": "Casey Jones", "traits": ["THWART"],
                     "desc": {"Cost": "3", "RES": "B", "Class": "Hero"}},
           "tc003": {"type": "Event", "name": "Cross Block", "unique": False, "set_name": "Casey Jones", "traits": ["DEFENSE"],
                     "desc": {"Cost": "2", "RES": "Y", "Class": "Hero"}},
           "tc004": {"type": "Event", "name": "Face-Off", "unique": False, "set_name": "Casey Jones", "traits": ["ATTACK"],
                     "desc": {"Cost": "2", "RES": "R", "Class": "Hero"}},
           "tc005": {"type": "Event", "name": "Grand Slam", "unique": False, "set_name": "Casey Jones", "traits": ["ATTACK"],
                     "desc": {"Cost": "3", "RES": "R", "Requirement": "G", "Class": "Hero"}}}},
       verifier="casey_desc"),
    _c("etape 6 : donnees imprimees des ameliorations (cartes tc006..tc013, voir pourquoi)",
       "Anything Goes, Bat, Mask, Willow, Iron, Hockey, Persuader, Bag : couts 1/1/3/2/1/2/2/aucun ; ressources R/Y/B/Y/B/Y/R/B ; Restricted 1 sur les cinq armes (tc007, tc009-tc012) ; Permanent 1 et AUCUN cout sur le Sac",
       ["Puzzle.CreateHandCards('tc006', 'tc007', 'tc008', 'tc009', 'tc010', 'tc011', 'tc012', 'tc013')"], [],
       {"cartes": {
           "tc006": {"type": "Upgrade", "name": "Anything Goes", "unique": False, "set_name": "Casey Jones", "traits": ["SKILL"],
                     "desc": {"Cost": "1", "RES": "R", "Class": "Hero"}},
           "tc007": {"type": "Upgrade", "name": "Baseball Bat", "unique": False, "set_name": "Casey Jones", "traits": ["WEAPON"],
                     "desc": {"Cost": "1", "RES": "Y", "Restricted": "1", "Class": "Hero"}},
           "tc008": {"type": "Upgrade", "name": "Casey's Mask", "unique": True, "set_name": "Casey Jones", "traits": ["ARMOR"],
                     "desc": {"Cost": "3", "RES": "B", "Class": "Hero"}},
           "tc009": {"type": "Upgrade", "name": "Cricket Willow", "unique": False, "set_name": "Casey Jones", "traits": ["WEAPON"],
                     "desc": {"Cost": "2", "RES": "Y", "Restricted": "1", "Class": "Hero"}},
           "tc010": {"type": "Upgrade", "name": "Driving Iron", "unique": False, "set_name": "Casey Jones", "traits": ["WEAPON"],
                     "desc": {"Cost": "1", "RES": "B", "Restricted": "1", "Class": "Hero"}},
           "tc011": {"type": "Upgrade", "name": "Hockey Stick", "unique": False, "set_name": "Casey Jones", "traits": ["WEAPON"],
                     "desc": {"Cost": "2", "RES": "Y", "Restricted": "1", "Class": "Hero"}},
           "tc012": {"type": "Upgrade", "name": "Persuader", "unique": False, "set_name": "Casey Jones", "traits": ["WEAPON"],
                     "desc": {"Cost": "2", "RES": "R", "Restricted": "1", "Class": "Hero"}},
           "tc013": {"type": "Upgrade", "name": "Casey's Bag", "unique": True, "set_name": "Casey Jones", "traits": ["ITEM"],
                     "desc": {"RES": "B", "Permanent": "1", "Class": "Hero"}, "sans_cle": ["Cost"]}}},
       verifier="casey_desc"),
    _c("etape 6 : donnees imprimees du set nemesis (cartes tc015..tc017, voir pourquoi)",
       "menace 3, Incite 1 par joueur, Crise 1, Hun PV 4, Goons PV 3, Guard, Patrol, Toughness ; scans « CASEY JONES NEMESIS (n/5) » : manigance 3 / 2 icones de boost ; Hun PV 4 ATQ 2 CTR 1 boost 3 Tenacite ; Goons PV 3 ATQ 2 CTR 1 boost 2 Garde Patrouille",
       ["Puzzle.CreateHandCards('tc015', 'tc016', 'tc017')"], [],
       {"cartes": {
           "tc015": {"type": "SideScheme", "name": "The Purple Dragons", "unique": False, "set_name": "Casey Jones Nemesis", "traits": [],
                     "desc": {"Boost": "2", "StartingThreat": "3", "Crisis": "1", "Incite": "1*"}},
           "tc016": {"type": "Minion", "name": "Hun", "unique": True, "set_name": "Casey Jones Nemesis", "traits": ["BRUTE", "PURPLE DRAGONS"],
                     "desc": {"HP": "4", "ATK": "2", "SCH": "1", "Boost": "3", "Toughness": "1", "Nemesis": "Casey Jones"}},
           "tc017": {"type": "Minion", "name": "Purple Dragon Goons", "unique": False, "set_name": "Casey Jones Nemesis", "traits": ["PURPLE DRAGONS"],
                     "desc": {"HP": "3", "ATK": "2", "SCH": "1", "Boost": "2", "Guard": "1", "Patrol": "1"}}}},
       verifier="casey_desc"),
]

VERIFICATIONS = r'''
def casey_resetup(monde, aides):
    """Rejoue le Setup de l'alter-ego (`Setup(False)`, comme `World.Setup`) apres que le cas a deplace le Sac tc013 hors du deck.
    `attendu` : depart ("defausse" | "main"), en_jeu (liste attendue en jeu apres), en_jeu_absent, reste_en_main."""
    attendu = aides["cas"]["attendu"]
    soucis = []
    joueur = monde.players[0]
    # Le Sac est PERMANENT : seul un effet du MEME set peut le faire quitter le jeu (has_permanent.py).
    # La regle de debogage emprunte donc l'identite de Casey (set « Casey Jones »).
    from game.effect.rule import DebugRule
    from game.operate.faces import Faces
    sac = aides["par_id"](monde, "tc013")
    if sac is not None:
        zone = {"defausse": joueur.discard_pile, "main": joueur.hand_cards, "deck": joueur.player_deck}[attendu["depart"]]
        Faces.MoveAllTo([sac], zone, DebugRule(joueur.GetIdentity()))
    if aides["par_id"](monde, "tc013") is not None:
        soucis.append("tc013 est encore en jeu avant le Setup rejoue (montage du cas)")
    main = [getattr(f.paper, "card_id", None) for f in joueur.hand_cards.GetAll()]
    defausse = [getattr(f.paper, "card_id", None) for f in joueur.discard_pile.GetAll()]
    if attendu["depart"] == "main" and "tc013" not in main:
        soucis.append("tc013 n'est pas dans la main avant le Setup rejoue")
    if attendu["depart"] == "defausse" and "tc013" not in defausse:
        soucis.append("tc013 n'est pas dans la defausse avant le Setup rejoue")
    deck = [getattr(f.paper, "card_id", None) for f in joueur.player_deck.GetAll()]
    if attendu["depart"] == "deck" and "tc013" not in deck:
        soucis.append("tc013 n'est pas dans le deck avant le Setup rejoue")
    joueur.GetIdentity().Setup(False)
    for cid in attendu.get("en_jeu", []):
        if aides["par_id"](monde, cid) is None:
            soucis.append(f"{cid} n'est pas en jeu apres le Setup rejoue")
    for cid in attendu.get("en_jeu_absent", []):
        if aides["par_id"](monde, cid) is not None:
            soucis.append(f"{cid} est en jeu apres le Setup rejoue (attendu : absent)")
    main = [getattr(f.paper, "card_id", None) for f in joueur.hand_cards.GetAll()]
    for cid in attendu.get("reste_en_main", []):
        if cid not in main:
            soucis.append(f"{cid} a quitte la main (attendu : reste en main)")
    if soucis:
        return False, " ; ".join(soucis)
    return True, f"Setup rejoue depuis « {attendu['depart']} » : conforme"
def casey_actions(monde, aides):
    """Nombre d'actions REELLEMENT disponibles sur `carte` (type `type`), comme Puzzle.Action les numerote."""
    from game.ability.ability import AbilityType
    from game.event.manager import EventManager
    from game.message import Message
    from game.effect.rule import GameRule
    attendu = aides["cas"]["attendu"]
    face = aides["par_id"](monde, attendu["carte"])
    if face is None:
        return False, f"{attendu['carte']} introuvable en jeu"
    joueur = monde.GetCurrentPlayer()
    type_capacite = getattr(AbilityType, attendu["type"]) if attendu.get("type") else None
    candidats = [x for x in face.effect.Find(when=Message.WhenPlayerInTurn, type=type_capacite)
                 if not x.ability.is_play]
    message = Message.WhenPlayerLikeInTurn(joueur, GameRule(joueur.GetIdentity()))
    message.Send()
    dispo = EventManager.FilterAvailableEffects(message, candidats, joueur, monde, None)
    n = len(dispo)
    if n != attendu["nombre"]:
        return False, f"{attendu['carte']} offre {n} action(s) {attendu.get('type')} (attendu {attendu['nombre']})"
    return True, f"{attendu['carte']} : {n} action(s) {attendu.get('type')} disponible(s), comme attendu"


def casey_etat(monde, aides):
    """`attendu.forme_joueur` : [[siege, "Hero" | "AlterEgo"]] (cles communes de etat_attendu en plus)."""
    attendu = dict(aides["cas"].get("attendu") or {})
    voulues = attendu.pop("forme_joueur", [])
    soucis = []
    for siege, forme in voulues:
        reelle = "Hero" if monde.players[siege].IsHero() else "AlterEgo"
        if reelle != forme:
            soucis.append(f"siege {siege} : forme {reelle} (attendu {forme})")
    if soucis:
        return False, " ; ".join(soucis)
    return True, f"formes des joueurs conformes : {voulues}"
def casey_desc(monde, aides):
    """`attendu.cartes` : {card_id: {type, name, unique, set_name, traits, desc, sans_cle}} comparee A LA LETTRE aux
    donnees que le MOTEUR a chargees (`face.paper`), pour des cartes creees en main (`Puzzle.CreateHandCards`).
    La table est relue sur les scans, pas sur le script."""
    attendu = aides["cas"]["attendu"]["cartes"]
    soucis = []
    for cid, voulu in attendu.items():
        face = None
        for objet in monde.object_manager.card_dict.values():
            f = objet.face
            if f is not None and getattr(f.paper, "card_id", None) == cid:
                face = f
                break
        if face is None:
            soucis.append(f"{cid} introuvable (CreateHandCards)")
            continue
        p = face.paper
        if p.type != voulu["type"]:
            soucis.append(f"{cid} type {p.type} (attendu {voulu['type']})")
        if p.name != voulu["name"]:
            soucis.append(f"{cid} nom « {p.name} » (attendu « {voulu['name']} »)")
        if p.is_unique != voulu["unique"]:
            soucis.append(f"{cid} unique={p.is_unique} (attendu {voulu['unique']})")
        if p.set_name != voulu["set_name"]:
            soucis.append(f"{cid} ensemble « {p.set_name} » (attendu « {voulu['set_name']} »)")
        if sorted(p.traits) != sorted(voulu["traits"]):
            soucis.append(f"{cid} traits {p.traits} (attendu {voulu['traits']})")
        for cle, valeur in voulu["desc"].items():
            if str(p.desc.get(cle)) != valeur:
                soucis.append(f"{cid} desc[{cle}]={p.desc.get(cle)!r} (attendu {valeur!r})")
        inattendues = sorted(set(p.desc) - set(voulu["desc"]))
        if inattendues:
            soucis.append(f"{cid} cles desc non prevues : {inattendues}")
        for cle in voulu.get("sans_cle", []):
            if cle in p.desc:
                soucis.append(f"{cid} porte desc[{cle}] alors que le scan n'en imprime pas")
    if soucis:
        return False, " ; ".join(soucis)
    return True, f"{len(attendu)} carte(s) conformes a la table relue sur les scans"


def casey_jouer_sous_le_sac(monde, aides):
    """Joue une carte GLISSEE sous Casey's Bag par le vrai chemin (meme geste que le clic du joueur : on demande les
    effets « Play » de la carte, le filtre du gestionnaire d'evenements les ecarte ou non, puis on resout et on PAIE).
    Si le moteur n'offre pas la carte, le cas echoue. `attendu.refuse_sous` : card_id de la carte sous laquelle la carte
    est rangee ET qui ne doit PAS la rendre jouable (temoin) : le cas reussit alors si le moteur la REFUSE.
    Puis `etat_attendu` (cles communes)."""
    from game.message import Message
    from game.effect.rule import GameRule
    from game.event.manager import EventManager
    attendu = dict(aides["cas"]["attendu"])
    joueur = monde.players[0]
    face = None
    hote = None
    for objet in monde.object_manager.card_dict.values():
        porteur = objet.face
        if porteur is None or not porteur.IsInPlay():
            continue
        try:
            rangees = porteur.GetPlacedCardArea().Get(True)
        except Exception:
            continue
        for f in rangees:
            if f is not None and getattr(f.paper, "card_id", None) == attendu["carte"]:
                face, hote = f, porteur
    if face is None:
        return False, f"{attendu['carte']} n'est glissee sous aucune carte en jeu"
    effets = face.effect.Find(func_name="Play", when=Message.WhenPlayerInTurn)
    message = Message.WhenPlayerLikeInTurn(joueur, GameRule(joueur.GetIdentity()))
    message.Send()
    disponibles = EventManager.FilterAvailableEffects(message, effets, joueur, monde, None)
    if attendu.get("refuse_sous"):
        sous = getattr(hote.paper, "card_id", None)
        if sous == attendu["refuse_sous"]:
            return False, "montage du temoin : la carte est rangee sous la carte qui devait la refuser"
        if disponibles:
            return False, f"le moteur OFFRE de jouer {attendu['carte']} rangee sous {sous} (attendu : refus)"
        return True, f"{attendu['carte']} rangee sous {sous} : non offerte, comme attendu"
    if not disponibles:
        return False, f"le moteur n'offre PAS de jouer {attendu['carte']} depuis le Sac"
    joueur.ChooseEffects([disponibles[0]], message, forced=False)
    aides["cas"]["attendu"] = {k: v for k, v in attendu.items() if k != "carte"}
    return etat_attendu(monde, aides)
'''
