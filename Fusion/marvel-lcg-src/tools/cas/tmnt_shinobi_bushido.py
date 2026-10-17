# Cas test_capacites du pack tmnt_shinobi_bushido (Inkwire, TMNT Shinobi, les 20 cartes BUSHIDO, prefixe `sb`), 17/10/2026.
# Filtre : `[sb]`. Gabarits : .planning/tmnt/shinobi-bushido-gabarits.md. Questions : .planning/tmnt/shinobi-bushido-questions.md.
#
# Conventions (reprises de tools/cas/tmnt_shinobi_paths.py) :
#  - Spider-Man (01001) demarre en ALTER EGO ; HEROS le met en forme heros (face heros = 01001a) ;
#  - Rhino 01094 (vilain du scenario `rhino`) est la cible des attaques, 01101 Hydra Mercenary (3 PV) le sbire ;
#  - `main_exclusive` vide la main (APRES la mise en place) : chaque cas sait avec QUOI il paie
#    (01088 Energy = YY, 01089 Genius = BB, 01090 Strength = RR) ;
#  - deck rencontre bourre de « I'm Tough » (01105, sans icone de boost) : aucune carte rencontre ne vient brouiller la mesure ;
#  - une amelioration posee par `Puzzle.PutIntoPlay('sbNNN', under_control=True)` s'attache a l'identite ; Uses pose ses compteurs
#    samurai a l'entree en jeu ;
#  - `Puzzle.Defend('01001a', '01094')` : Rhino attaque, le heros defend (pouvoir de base DEF) ; sans defenseur le pilote fait
#    defendre le heros s'il est pret, donc le temoin « pas de defense » incline le heros d'abord.
SC = "rhino"
HEROS = "Puzzle.ChangeForm('01001b')"
COMPLOT = "01097b"
MENACE = "Puzzle.PlaceThreat('01097b', 6)"
SANS_BOOST = ["Puzzle.EmptyEncounterDeck()",
              "Puzzle.CreateEncounterDeck('01105', '01105', '01105', '01105', '01105', '01105', '01105', '01105')"]
TOUS = [("sb001", "Loyalty"), ("sb002", "Rectitude"), ("sb003", "Courage"), ("sb004", "Glory"), ("sb005", "Gratitude"),
        ("sb006", "Mercy"), ("sb007", "Integrity"), ("sb008", "Self-Control"), ("sb009", "Devotion"), ("sb010", "Tsujigiri"),
        ("sb011", "Vow"), ("sb012", "Kensei"), ("sb013", "Santoryu Ogi"), ("sb014", "Kosho"), ("sb015", "Oathbreaker"),
        ("sb016", "Wakizashi"), ("sb017", "Uno"), ("sb018", "Musha Shugyo"), ("sb019", "Gusoku"), ("sb020", "Iaido")]


def _poser(cid):
    return f"Puzzle.PutIntoPlay('{cid}', under_control=True)"


def _c(nom, pourquoi, mise, declencher, attendu, **cle):
    if not cle.pop("avec_boost", False):
        mise = SANS_BOOST + list(mise)
    cas = {"nom": "[sb] " + nom, "pourquoi": pourquoi, "scenario": cle.pop("scenario", SC),
           "heros": cle.pop("heros", "spider_man"), "mise_en_place": list(mise), "declencher": list(declencher),
           "verifier": cle.pop("verifier", "etat_attendu"), "attendu": attendu}
    cas.update(cle)
    return cas


def _dispo(nom, pourquoi, mise, carte, type_, nombre, **cle):
    """Cas « l'action est (ou n'est pas) proposee » : `nombre` actions REELLEMENT disponibles."""
    return _c(nom, pourquoi, mise, cle.pop("declencher", []), {"carte": carte, "type": type_, "nombre": nombre},
              verifier="sb_actions_disponibles", **cle)


CAS = []

# ========================================================================= sb001 Loyalty, sb002 Rectitude, sb003 Courage
# Trois ameliorations jumelles : +1 a un pouvoir de base, et UN compteur samurai retire apres CE pouvoir de base du heros.
for _cid, _nom, _stat, _decl, _decl_autre, _autre in [
        ("sb001", "Loyalty", "defense", "Puzzle.Defend('01001a', '01094')", "Puzzle.Attack('01001a')", "attaque de base"),
        ("sb002", "Rectitude", "thwart", "Puzzle.Thwart('01001a')", "Puzzle.Attack('01001a')", "attaque de base"),
        ("sb003", "Courage", "attack", "Puzzle.Attack('01001a')", "Puzzle.Thwart('01001a')", "contre de base")]:
    _pouvoir = {"defense": "defense de base", "thwart": "contre de base", "attack": "attaque de base"}[_stat]
    CAS += [
        _c(f"{_cid} {_nom} : « Your hero gets +1 {_stat.upper()[:3]} » en forme heros, 3 compteurs samurai (Uses)",
           "bonus continu de +1 sur le pouvoir imprime ; Uses pose 3 compteurs samurai a l'entree en jeu",
           [HEROS, _poser(_cid)], [],
           {"attributs": {_stat: 1}, "compteurs": [[_cid, "samurai", 3]], "en_jeu": [_cid]}),
        _c(f"{_cid} {_nom} Forced Response : apres {_pouvoir} du heros, 1 compteur samurai retire de CETTE carte",
           f"« After your hero makes a basic {_stat} » : 3 -> 2 compteurs, la carte reste en jeu",
           [MENACE, HEROS, _poser(_cid)], [_decl], {"compteurs": [[_cid, "samurai", 2]], "en_jeu": [_cid]}, main_exclusive=["01090"]),
        _c(f"{_cid} {_nom} : TEMOIN, un autre pouvoir de base ({_autre}) ne retire AUCUN compteur",
           f"seul le pouvoir de base {_stat} compte ; mesure 3 compteurs apres {_autre}",
           [MENACE, HEROS, _poser(_cid)], [_decl_autre], {"compteurs": [[_cid, "samurai", 3]], "en_jeu": [_cid]}, main_exclusive=["01090"]),
        _c(f"{_cid} {_nom} : le DERNIER compteur retire, Uses defausse la carte",
           "1 compteur restant -> apres le pouvoir de base la carte est defaussee (plus en jeu, dans la defausse)",
           [MENACE, HEROS, _poser(_cid), f"Puzzle.Counter('{_cid}', 'samurai', -2)"], [_decl],
           {"hors_jeu": [_cid], "defausse": [_cid]}, main_exclusive=["01090"]),
    ]
CAS.append(_c("sb001 Loyalty : TEMOIN, aucune defense declaree (heros incline) : aucun compteur retire",
              "pas de pouvoir de base DEF utilise : l'attaque de Rhino est encaissee sans defenseur, les 3 compteurs restent",
              [HEROS, _poser("sb001"), "Puzzle.Exhaust('01001a')"], ["Puzzle.Attack('01094')"],
              {"compteurs": [["sb001", "samurai", 3]], "en_jeu": ["sb001"]}))


# ========================================================================= sb004 Glory
_COMPLOT_ANNEXE = ["Puzzle.PutIntoPlay('01107')", "Puzzle.SetThreat('01107', 1)"]
CAS += [
    _c("sb004 Glory Hero Response : apres avoir vaincu un complot ANNEXE, la carte est defaussee (cout) et 4 compteurs samurai sont poses",
       "« After your hero defeats a side scheme, discard this card -> place a total of 4 samurai counters among any number of OATH "
       "upgrades you control » : sb001 Loyalty (1 compteur) devient 5 ; Glory part en defausse",
       [HEROS, _poser("sb001"), "Puzzle.Counter('sb001', 'samurai', -2)", _poser("sb004")] + _COMPLOT_ANNEXE,
       ["Puzzle.Thwart('01001a')"],
       {"compteurs": [["sb001", "samurai", 5]], "defausse": ["sb004"], "hors_jeu": ["sb004", "01107"]},
       main_exclusive=["01090"], cibles=["01107"], accepter_choix=True),
    _c("sb004 Glory : « among ANY NUMBER of OATH upgrades » : tout sur une AUTRE amelioration (sb003 designee) : sb001 intacte",
       "le joueur choisit la carte a chaque compteur : les 4 vont sur Courage (3 -> 7), Loyalty reste a 3",
       [HEROS, _poser("sb001"), _poser("sb003"), _poser("sb004")] + _COMPLOT_ANNEXE,
       ["Puzzle.Thwart('01001a')"],
       {"compteurs": [["sb003", "samurai", 7], ["sb001", "samurai", 3]], "defausse": ["sb004"]},
       main_exclusive=["01090"], cibles=["01107", "sb003"], accepter_choix=True),
    _c("sb004 Glory : sans AUCUNE amelioration OATH restante le cout est paye quand meme (carte defaussee), rien ne se pose",
       "le seul OATH sous controle etait Glory elle-meme, defaussee en cout : pas de cible, pas de compteur",
       [HEROS, _poser("sb004")] + _COMPLOT_ANNEXE, ["Puzzle.Thwart('01001a')"],
       {"defausse": ["sb004"], "hors_jeu": ["sb004", "01107"]},
       main_exclusive=["01090"], cibles=["01107"], accepter_choix=True),
    _c("sb004 Glory : TEMOIN, vaincre un SBIRE (et non un complot annexe) ne declenche pas Glory",
       "Hydra Mercenary (1 PV apres 2 degats) vaincu par l'attaque de base : Glory reste en jeu, aucun compteur pose",
       [HEROS, _poser("sb001"), "Puzzle.Counter('sb001', 'samurai', -2)", _poser("sb004"), "Puzzle.PutIntoPlay('01101')",
        "Puzzle.Damage('01101', 2)"],
       ["Puzzle.Attack('01001a')"],
       {"compteurs": [["sb001", "samurai", 1]], "en_jeu": ["sb004"], "hors_jeu": ["01101"]},
       main_exclusive=["01090"], cibles=["01101"]),
    _c("sb004 Glory : « Max 1 per player » : une seconde copie en main n'est pas jouable",
       "`desc.MaxPerUnit = 1` : avec Glory deja en jeu, la copie en main est refusee",
       [HEROS, "Puzzle.Gain('sb004')", _poser("sb004")], [], {"carte": "sb004", "jouable": False, "en_jeu": 1},
       main=["01088", "01089"], verifier="max_par_joueur_jouable"),
    _c("sb004 Glory : TEMOIN de « Max 1 per player » : sans copie en jeu la carte en main est jouable",
       "contre-cas : aucune Glory en jeu, la copie en main est jouable (cout 0)",
       [HEROS, "Puzzle.Gain('sb004')"], [], {"carte": "sb004", "jouable": True, "en_jeu": 0},
       main=["01088", "01089"], verifier="max_par_joueur_jouable"),
]

# ========================================================================= sb005 Gratitude
CAS += [
    _c("sb005 Gratitude Action : incline la carte, retire 1 compteur samurai, soigne 1 degat de l'identite (forme heros)",
       "« Action: Exhaust this card and remove 1 samurai counter from it -> heal 1 damage from your identity » : Spider-Man (3 degats) "
       "-> 2 ; Gratitude inclinee, 2 -> 1 compteur",
       [HEROS, _poser("sb005"), "Puzzle.Damage('01001a', 3)"], ["Puzzle.Action('sb005', 'Action', 0)"],
       {"degats_identite": 2, "exhausted": ["sb005"], "compteurs": [["sb005", "samurai", 1]]}),
    _c("sb005 Gratitude : « Action » (et non Hero Action) : proposee AUSSI en forme alter-ego, elle soigne Peter Parker",
       "alter-ego (2 degats) -> 1 ; l'action est offerte quelle que soit la forme",
       [_poser("sb005"), "Puzzle.Damage('01001b', 2)"], ["Puzzle.Action('sb005', 'Action', 0)"],
       {"degats_identite": 1, "exhausted": ["sb005"], "compteurs": [["sb005", "samurai", 1]]}),
    _c("sb005 Gratitude : « You may discard 1 status card from your identity » : la carte Sonne du heros est defaussee",
       "choix accepte (accepter_choix) : Stunned retire de l'identite ; le soin a eu lieu aussi (3 -> 2 degats)",
       [HEROS, _poser("sb005"), "Puzzle.Damage('01001a', 3)", "Puzzle.Stun('01001a')"],
       ["Puzzle.Action('sb005', 'Action', 0)"],
       {"degats_identite": 2, "statuts_absents": [["01001a", "Stunned"]]}, accepter_choix=True),
    _c("sb005 Gratitude : TEMOIN, le « may » se REFUSE : la carte d'etat reste, le soin a eu lieu",
       "choisir « Cancel » : Stunned encore la, 3 -> 2 degats",
       [HEROS, _poser("sb005"), "Puzzle.Damage('01001a', 3)", "Puzzle.Stun('01001a')"],
       ["Puzzle.Action('sb005', 'Action', 0)"],
       {"degats_identite": 2, "statuts": [["01001a", "Stunned"]]}, choisir_option="Cancel"),
    _c("sb005 Gratitude : « status card » = N'IMPORTE LAQUELLE : une carte Camoufle (Cloaked) peut etre defaussee",
       "statut Cloaked defausse alors que ce n'est ni Sonne, ni Desoriente, ni Tenace",
       [HEROS, _poser("sb005"), "Puzzle.Cloak('01001a')"], ["Puzzle.Action('sb005', 'Action', 0)"],
       {"statuts_absents": [["01001a", "Cloaked"]]}, accepter_choix=True),
    _c("sb005 Gratitude : sans degat a soigner, on peut quand meme defausser une carte d'etat (phrases independantes)",
       "aucun degat : le soin ne fait rien, Desoriente est defaussee",
       [HEROS, _poser("sb005"), "Puzzle.Confuse('01001a')"], ["Puzzle.Action('sb005', 'Action', 0)"],
       {"degats_identite": 0, "statuts_absents": [["01001a", "Confused"]]}, accepter_choix=True),
    _c("sb005 Gratitude : le DERNIER compteur (2e usage) defausse la carte (Uses)",
       "1 compteur restant : l'action retire le dernier, Gratitude quitte le jeu, le soin a eu lieu",
       [HEROS, _poser("sb005"), "Puzzle.Counter('sb005', 'samurai', -1)", "Puzzle.Damage('01001a', 3)"],
       ["Puzzle.Action('sb005', 'Action', 0)"], {"degats_identite": 2, "hors_jeu": ["sb005"], "defausse": ["sb005"]}),
    _dispo("sb005 Gratitude : TEMOIN D'EPUISEMENT, inclinee elle ne propose plus l'Action dans le meme round (il reste 1 compteur)",
           "cout = incliner + 1 compteur : apres un usage (2 -> 1 compteur) la carte est inclinee, 0 action disponible",
           [HEROS, _poser("sb005")], "sb005", "Action", 0, declencher=["Puzzle.Action('sb005', 'Action', 0)"]),
    _dispo("sb005 Gratitude : l'Action est proposee quand la carte est prete (temoin positif)",
           "1 action disponible avant usage", [HEROS, _poser("sb005")], "sb005", "Action", 1),
]

# ========================================================================= sb006 Mercy (LECTURE PROVISOIRE, Q-B1)
_DECK5 = ["Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01073', '01074', '01075', '01076', '01077')"]
CAS += [
    _c("sb006 Mercy (provisoire Q-B1) : le heros allait VAINCRE Hydra Mercenary : la carte est defaussee, le sbire survit a 1 PV, 3 cartes piochees",
       "Hydra Mercenary (3 PV, 2 degats deja) : l'attaque de base du heros (1 degat) le vaincrait ; Hero Interrupt : Mercy defaussee "
       "(cout), PV restants = 1 (degats 2), main 1 + 3 = 4",
       [HEROS, _poser("sb006"), "Puzzle.PutIntoPlay('01101')", "Puzzle.Damage('01101', 2)"] + _DECK5,
       ["Puzzle.Attack('01001a')"],
       {"en_jeu": ["01101"], "degats": [["01101", 2]], "defausse": ["sb006"], "hors_jeu": ["sb006"], "taille_main": 4},
       main_exclusive=["01090"], cibles=["01101"]),
    _c("sb006 Mercy : TEMOIN, sans Mercy le meme coup VAINC Hydra Mercenary",
       "contre-cas du precedent : aucune amelioration, le sbire est vaincu (hors jeu)",
       [HEROS, "Puzzle.PutIntoPlay('01101')", "Puzzle.Damage('01101', 2)"] + _DECK5, ["Puzzle.Attack('01001a')"],
       {"hors_jeu": ["01101"], "taille_main": 1}, main_exclusive=["01090"], cibles=["01101"]),
    _c("sb006 Mercy : « defeated by YOUR HERO » : un ALLIE (Mockingbird) qui allait vaincre le sbire ne declenche pas Mercy",
       "temoin d'absence : le sbire est vaincu par l'allie, Mercy reste en jeu, aucune carte piochee",
       [HEROS, _poser("sb006"), "Puzzle.PutIntoPlay('01083', under_control=True)", "Puzzle.PutIntoPlay('01101')",
        "Puzzle.Damage('01101', 2)"] + _DECK5, ["Puzzle.Attack('01083')"],
       {"hors_jeu": ["01101"], "en_jeu": ["sb006"], "taille_main": 1}, main_exclusive=["01090"], cibles=["01101"]),
    _c("sb006 Mercy : « Max 1 per player » : une seconde copie en main n'est pas jouable",
       "`desc.MaxPerUnit = 1`", [HEROS, "Puzzle.Gain('sb006')", _poser("sb006")], [],
       {"carte": "sb006", "jouable": False, "en_jeu": 1}, main=["01088", "01089"], verifier="max_par_joueur_jouable"),
]

# ========================================================================= sb007 Integrity
CAS += [
    _c("sb007 Integrity Response : apres avoir JOUE une amelioration OATH (Loyalty), Integrity s'incline et 1 compteur samurai est place sur l'OATH choisie",
       "Loyalty (cout 0) jouee depuis la main : Integrity s'incline, le compteur va sur Loyalty (3 -> 4) ; la pose elle-meme ne compte pas deux fois",
       [HEROS, _poser("sb007")], [],
       {"exhausted": ["sb007"], "compteurs": [["sb001", "samurai", 4]], "en_jeu": ["sb001"]},
       main_exclusive=["sb001"], jouer=["sb001"], cibles=["sb001"]),
    _c("sb007 Integrity : « an OATH upgrade YOU control » : le joueur CHOISIT, ici une AUTRE amelioration OATH (Courage en jeu) que celle jouee",
       "Loyalty jouee, Courage deja en jeu : le compteur va sur Courage (3 -> 4), Loyalty garde ses 3",
       [HEROS, _poser("sb007"), _poser("sb003")], [],
       {"exhausted": ["sb007"], "compteurs": [["sb003", "samurai", 4], ["sb001", "samurai", 3]]},
       main_exclusive=["sb001"], jouer=["sb001"], cibles=["sb003"]),
    _c("sb007 Integrity : TEMOIN D'EPUISEMENT, une SECONDE OATH jouee dans le meme round ne declenche plus rien (Integrity inclinee)",
       "Loyalty puis Courage (cout 1, payee Strength RR) : un seul compteur ajoute en tout (Loyalty 4, Courage 3)",
       [HEROS, _poser("sb007")], [],
       {"exhausted": ["sb007"], "compteurs": [["sb001", "samurai", 4], ["sb003", "samurai", 3]]},
       main_exclusive=["sb001", "sb003", "01090"], payer_avec=["01090"], jouer=["sb001", "sb003"], cibles=["sb001"]),
    _c("sb007 Integrity : TEMOIN, une amelioration NON OATH jouee (Armored Vest 01081) ne declenche rien",
       "Armored Vest (cout 1, payee Strength) : Integrity reste prete, Loyalty garde ses 3 compteurs",
       [HEROS, _poser("sb007"), _poser("sb001")], [],
       {"pret": ["sb007"], "compteurs": [["sb001", "samurai", 3]], "en_jeu": ["01081"]},
       main_exclusive=["01081", "01090"], payer_avec=["01090"], jouer=["01081"], cibles=["sb001"]),
    _c("sb007 Integrity : TEMOIN, un evenement joue (pas une amelioration) ne declenche rien",
       "Haymaker 01087 (cout 2, evenement) joue : Integrity reste prete",
       [HEROS, _poser("sb007"), _poser("sb001")], [],
       {"pret": ["sb007"], "compteurs": [["sb001", "samurai", 3]]},
       main_exclusive=["01087", "01090"], payer_avec=["01090"], jouer=["01087"], cibles=["01094"]),
    _c("sb007 Integrity : Integrity JOUEE elle-meme est une amelioration OATH jouee : elle repond a sa propre pose",
       "Integrity (cout 2) jouee avec Loyalty en jeu : le message de jeu est envoye apres sa mise en jeu, elle s'incline et place 1 compteur "
       "sur Loyalty (3 -> 4)",
       [HEROS, _poser("sb001")], [],
       {"exhausted": ["sb007"], "compteurs": [["sb001", "samurai", 4]]},
       main_exclusive=["sb007", "01090"], payer_avec=["01090"], jouer=["sb007"], cibles=["sb001"]),
]

# ========================================================================= sb008 Self-Control
CAS += [
    _c("sb008 Self-Control Resource : SEULE source de paiement, elle paie Armored Vest (cout 1) : Self-Control s'incline, 3 -> 2 compteurs",
       "main vide sauf Armored Vest 01081 : la ressource wild generee par Self-Control paie la carte, qui entre en jeu",
       [HEROS, _poser("sb008")], [],
       {"en_jeu": ["01081"], "exhausted": ["sb008"], "compteurs": [["sb008", "samurai", 2]]},
       main_exclusive=["01081"], jouer=["01081"]),
    _c("sb008 Self-Control : « Resource » (et non Hero Resource) : fonctionne aussi en forme ALTER-EGO",
       "Peter Parker (alter-ego, qui genere lui-meme 1 ressource) joue Combat Training 01057 (amelioration non OATH, cout 2) : les deux sources paient, dont Self-Control "
       "(inclinee, 3 -> 2 compteurs)",
       [_poser("sb008")], [],
       {"en_jeu": ["01057"], "exhausted": ["sb008"], "compteurs": [["sb008", "samurai", 2]]},
       main_exclusive=["01057"], jouer=["01057"]),
    _c("sb008 Self-Control : « generate A resource » : UNE seule ressource, elle ne paie pas une carte de cout 2 (Haymaker reste en main)",
       "Haymaker 01087 (cout 2) avec Self-Control pour seule source : une ressource ne suffit pas, rien n'est paye (carte en main, "
       "Self-Control prete, 3 compteurs)",
       [HEROS, _poser("sb008")], [],
       {"en_main": ["01087"], "pret": ["sb008"], "compteurs": [["sb008", "samurai", 3]]},
       main_exclusive=["01087"], jouer=["01087"], cibles=["01094"]),
    _c("sb008 Self-Control : le DERNIER compteur retire PENDANT le paiement : la carte payee entre en jeu, Self-Control est defaussee (Uses)",
       "1 compteur restant : le cout le retire, Uses defausse Self-Control, Armored Vest entre quand meme en jeu",
       [HEROS, _poser("sb008"), "Puzzle.Counter('sb008', 'samurai', -2)"], [],
       {"en_jeu": ["01081"], "hors_jeu": ["sb008"], "defausse": ["sb008"]},
       main_exclusive=["01081"], jouer=["01081"]),
    _c("sb008 Self-Control : TEMOIN D'EPUISEMENT, Self-Control deja inclinee ne genere plus de ressource (Armored Vest reste en main)",
       "cout « Exhaust this card » : inclinee, la ressource n'est pas offerte ; les 3 compteurs restent",
       [HEROS, _poser("sb008"), "Puzzle.Exhaust('sb008')"], [],
       {"en_main": ["01081"], "compteurs": [["sb008", "samurai", 3]]},
       main_exclusive=["01081"], jouer=["01081"]),
]

# ========================================================================= sb009 Devotion
# armes de matiere : 01046 (WEAPON, non Restricted) et jennika/tj008 Jennika's Bow (WEAPON, Restricted).
CAS += [
    _c("sb009 Devotion Hero Action : incline la carte, retire 1 compteur samurai, REDRESSE l'arme inclinee (01046)",
       "« ready a WEAPON upgrade you control » : 01046 inclinee -> prete ; Devotion inclinee, 3 -> 2 compteurs",
       [HEROS, _poser("sb009"), _poser("01046"), "Puzzle.Exhaust('01046')"], ["Puzzle.Action('sb009', 'HeroAction', 0)"],
       {"pret": ["01046"], "exhausted": ["sb009"], "compteurs": [["sb009", "samurai", 2]]}, accepter_choix=True),
    _c("sb009 Devotion : « A weapon » : UNE seule arme redressee, au choix (tj008 designee) : l'autre arme inclinee le reste",
       "deux armes inclinees (01046 et tj008) : seule tj008 est redressee",
       [HEROS, _poser("sb009"), _poser("01046"), _poser("tj008"), "Puzzle.Exhaust('01046')", "Puzzle.Exhaust('tj008')"],
       ["Puzzle.Action('sb009', 'HeroAction', 0)"],
       {"pret": ["tj008"], "exhausted": ["sb009", "01046"]}, cibles=["tj008"], accepter_choix=True),
    _c("sb009 Devotion : « you control » comprend l'arme attachee a un ALLIE (Mockingbird)",
       "01046 attachee a Mockingbird (allie sous mon controle) et inclinee : Devotion la redresse",
       [HEROS, _poser("sb009"), "Puzzle.PutIntoPlay('01083', under_control=True)", "Puzzle.AttachReel('01046', '01083')",
        "Puzzle.Exhaust('01046')"], ["Puzzle.Action('sb009', 'HeroAction', 0)"],
       {"pret": ["01046"], "exhausted": ["sb009"]}, accepter_choix=True),
    _c("sb009 Devotion : le DERNIER compteur retire (1 restant) : l'arme est redressee, Devotion est defaussee (Uses)",
       "1 compteur : le cout le retire, Uses defausse Devotion, l'effet a lieu quand meme",
       [HEROS, _poser("sb009"), "Puzzle.Counter('sb009', 'samurai', -2)", _poser("01046"), "Puzzle.Exhaust('01046')"],
       ["Puzzle.Action('sb009', 'HeroAction', 0)"],
       {"pret": ["01046"], "hors_jeu": ["sb009"], "defausse": ["sb009"]}, accepter_choix=True),
    _dispo("sb009 Devotion : TEMOIN D'EPUISEMENT, inclinee elle ne propose plus l'action dans le meme round (2 compteurs restants, 2 armes inclinees)",
           "apres un usage la carte est inclinee : 0 action disponible malgre les compteurs et une arme inclinee",
           [HEROS, _poser("sb009"), _poser("01046"), _poser("tj008"), "Puzzle.Exhaust('01046')", "Puzzle.Exhaust('tj008')"],
           "sb009", "HeroAction", 0, declencher=["Puzzle.Action('sb009', 'HeroAction', 0)"], accepter_choix=True),
    _dispo("sb009 Devotion : l'action est proposee avec une arme inclinee (temoin positif)",
           "1 action disponible", [HEROS, _poser("sb009"), _poser("01046"), "Puzzle.Exhaust('01046')"], "sb009", "HeroAction", 1),
    _dispo("sb009 Devotion : une arme DEJA PRETE n'est pas une cible : l'action n'est pas proposee",
           "ready sur une carte deja prete : aucune cible legale (`canbe_ready`)",
           [HEROS, _poser("sb009"), _poser("01046")], "sb009", "HeroAction", 0),
    _dispo("sb009 Devotion : une amelioration inclinee qui n'est PAS une arme (Loyalty) n'est pas une cible",
           "seule Loyalty (OATH, pas WEAPON) est inclinee : aucune cible, action non proposee",
           [HEROS, _poser("sb009"), _poser("sb001"), "Puzzle.Exhaust('sb001')"], "sb009", "HeroAction", 0),
    _dispo("sb009 Devotion : Hero Action NON proposee en forme alter-ego",
           "forme heros uniquement", [_poser("sb009"), _poser("01046"), "Puzzle.Exhaust('01046')"], "sb009", "HeroAction", 0),
]

# ========================================================================= sb010 Tsujigiri
# Spider-Man a 2 d'ATQ ; Hydra Mercenary 01101 a 3 PV ; Strength 01090 (RR) paie Tsujigiri (cout 2).
_PAYE_2R = dict(payer_avec=["01090"])
CAS += [
    _c("sb010 Tsujigiri : « damage equal to your ATK » : ATQ 2 -> 2 degats a Rhino",
       "Hero Action (attack) : 2 degats (l'ATQ courant de Spider-Man) ; Rhino survit, pas de compteur",
       [HEROS, _poser("sb001")], [],
       {"degats": [["01094", 2]], "defausse": ["sb010"], "compteurs": [["sb001", "samurai", 3]]},
       main_exclusive=["sb010", "01090"], jouer=["sb010"], cibles=["01094"], **_PAYE_2R),
    _c("sb010 Tsujigiri : l'ATQ COURANT compte (Courage +1 ATQ : 3 degats a Rhino)",
       "Courage en jeu : ATQ 2 + 1 = 3 degats, lus a la resolution",
       [HEROS, _poser("sb003")], [],
       {"degats": [["01094", 3]], "defausse": ["sb010"]},
       main_exclusive=["sb010", "01090"], jouer=["sb010"], cibles=["01094"], **_PAYE_2R),
    _c("sb010 Tsujigiri : « If this attack defeats that enemy, you MAY place 1 samurai counter » : sbire vaincu, compteur place sur l'OATH (3 -> 4)",
       "Hydra Mercenary (3 PV, 2 degats deja) vaincu par les 2 degats de la carte : le joueur place 1 compteur sur Loyalty",
       [HEROS, _poser("sb001"), "Puzzle.PutIntoPlay('01101')", "Puzzle.Damage('01101', 2)"], [],
       {"hors_jeu": ["01101"], "compteurs": [["sb001", "samurai", 4]]},
       main_exclusive=["sb010", "01090"], jouer=["sb010"], cibles=["01101", "sb001"], **_PAYE_2R),
    _c("sb010 Tsujigiri : TEMOIN, l'attaque ne VAINC pas la cible (Hydra Mercenary a 3 PV) : aucun compteur",
       "2 degats sur un sbire a 3 PV : il survit, Loyalty garde ses 3 compteurs",
       [HEROS, _poser("sb001"), "Puzzle.PutIntoPlay('01101')"], [],
       {"en_jeu": ["01101"], "degats": [["01101", 2]], "compteurs": [["sb001", "samurai", 3]]},
       main_exclusive=["sb010", "01090"], jouer=["sb010"], cibles=["01101", "sb001"], **_PAYE_2R),
    _c("sb010 Tsujigiri : TEMOIN, le « may » se REFUSE (Cancel) : le sbire est vaincu, aucun compteur place",
       "choix refuse : Loyalty garde 3 compteurs, le sbire est quand meme vaincu",
       [HEROS, _poser("sb001"), "Puzzle.PutIntoPlay('01101')", "Puzzle.Damage('01101', 2)"], [],
       {"hors_jeu": ["01101"], "compteurs": [["sb001", "samurai", 3]]},
       main_exclusive=["sb010", "01090"], jouer=["sb010"], cibles=["01101"], choisir_option="Cancel", **_PAYE_2R),
    _c("sb010 Tsujigiri : sans amelioration OATH sous controle, vaincre la cible ne pose rien et ne bloque rien",
       "aucune OATH en jeu : le sbire est vaincu, aucune question de compteur, la carte est defaussee",
       [HEROS, "Puzzle.PutIntoPlay('01101')", "Puzzle.Damage('01101', 2)"], [],
       {"hors_jeu": ["01101"], "defausse": ["sb010"]},
       main_exclusive=["sb010", "01090"], jouer=["sb010"], cibles=["01101"], **_PAYE_2R),
]

# ========================================================================= sb011 Vow
# Spider-Man a 1 de CTR ; Energy 01088 (YY) paie Vow (cout 2). Le DESSUS du deck est la DERNIERE carte de `CreatePlayerDeck`.
_PAYE_2Y = dict(payer_avec=["01088"])
_DECK_OATH = ["Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01073', 'sb001', '01074')"]
CAS += [
    _c("sb011 Vow : retire la DERNIERE menace d'un complot annexe : recherche une OATH dans le deck, l'ajoute a la main (deck 3 -> 2)",
       "complot annexe a 1 menace, CTR 1 : menace retiree jusqu'a 0 (complot vaincu), Loyalty (sb001) du deck passe en main",
       [HEROS, "Puzzle.PutIntoPlay('01107')", "Puzzle.SetThreat('01107', 1)"] + _DECK_OATH, [],
       {"hors_jeu": ["01107"], "en_main": ["sb001"], "taille_deck_joueur": 2, "defausse": ["sb011"]},
       main_exclusive=["sb011", "01088"], jouer=["sb011"], cibles=["01107"], accepter_choix=True, **_PAYE_2Y),
    _c("sb011 Vow : TEMOIN, un retrait PARTIEL (complot principal a 6) ne declenche pas la recherche",
       "menace 6 -> 5 : Loyalty reste dans le deck, rien en main",
       [MENACE, HEROS] + _DECK_OATH, [],
       {"menace": [["01097b", 5]], "dans_deck_joueur": ["sb001"], "absent_main": ["sb001"], "taille_deck_joueur": 3},
       main_exclusive=["sb011", "01088"], jouer=["sb011"], cibles=["01097b"], accepter_choix=True, **_PAYE_2Y),
    _c("sb011 Vow : « equal to your hero's THW » : CTR 1, complot annexe a 2 menaces -> il en reste 1, pas de recherche",
       "sans bonus de CTR le retrait n'est que de 1 : le complot survit, Loyalty reste dans le deck",
       [HEROS, "Puzzle.PutIntoPlay('01107')", "Puzzle.SetThreat('01107', 2)"] + _DECK_OATH, [],
       {"menace": [["01107", 1]], "dans_deck_joueur": ["sb001"], "absent_main": ["sb001"]},
       main_exclusive=["sb011", "01088"], jouer=["sb011"], cibles=["01107"], accepter_choix=True, **_PAYE_2Y),
    _c("sb011 Vow : « equal to your hero's THW » : avec Rectitude (+1 CTR = 2), les 2 menaces partent : recherche et OATH en main",
       "meme position avec Rectitude en jeu : CTR 2, complot annexe vaincu, Loyalty en main",
       [HEROS, _poser("sb002"), "Puzzle.PutIntoPlay('01107')", "Puzzle.SetThreat('01107', 2)"] + _DECK_OATH, [],
       {"hors_jeu": ["01107"], "en_main": ["sb001"]},
       main_exclusive=["sb011", "01088"], jouer=["sb011"], cibles=["01107"], accepter_choix=True, **_PAYE_2Y),
    _c("sb011 Vow : « search your DECK » : une OATH dans la DEFAUSSE n'est pas trouvee",
       "Loyalty en defausse, aucune OATH dans le deck : la recherche ne ramene rien",
       [HEROS, "Puzzle.PutIntoPlay('01107')", "Puzzle.SetThreat('01107', 1)", "Puzzle.EmptyPlayerDeck()",
        "Puzzle.CreatePlayerDeck('01073', '01074')", "Puzzle.CreatePlayerDiscardPile('sb001')"], [],
       {"hors_jeu": ["01107"], "absent_main": ["sb001"], "taille_deck_joueur": 2},
       main_exclusive=["sb011", "01088"], jouer=["sb011"], cibles=["01107"], accepter_choix=True, **_PAYE_2Y),
    _c("sb011 Vow : « an OATH upgrade » : une amelioration NON OATH du deck (Armored Vest) n'est pas ramenee",
       "deck sans OATH : Armored Vest 01081 reste dans le deck, rien n'entre en main",
       [HEROS, "Puzzle.PutIntoPlay('01107')", "Puzzle.SetThreat('01107', 1)", "Puzzle.EmptyPlayerDeck()",
        "Puzzle.CreatePlayerDeck('01073', '01081', '01074')"], [],
       {"hors_jeu": ["01107"], "absent_main": ["01081"], "dans_deck_joueur": ["01081"]},
       main_exclusive=["sb011", "01088"], jouer=["sb011"], cibles=["01107"], accepter_choix=True, **_PAYE_2Y),
]

# ========================================================================= sb012 Kensei
# Genius 01089 (BB) paie Kensei (cout 1). Le heros est incline d'abord (sinon « ready your hero » n'a pas de cible).
_PAYE_B = dict(payer_avec=["01089"])
CAS += [
    _c("sb012 Kensei Hero Action : incline une arme (01046) en cout et REDRESSE le heros incline",
       "heros incline, arme prete : apres Kensei le heros est pret, l'arme est inclinee, Kensei defaussee",
       [HEROS, _poser("01046"), "Puzzle.Exhaust('01001a')"], [],
       {"pret": ["01001a"], "exhausted": ["01046"], "defausse": ["sb012"]},
       main_exclusive=["sb012", "01089"], jouer=["sb012"], accepter_choix=True, **_PAYE_B),
    _c("sb012 Kensei : « a WEAPON upgrade YOU control » comprend l'arme attachee a un ALLIE (Mockingbird)",
       "01046 attachee a Mockingbird (allie sous mon controle) : elle paie le cout, le heros est redresse",
       [HEROS, "Puzzle.PutIntoPlay('01083', under_control=True)", "Puzzle.AttachReel('01046', '01083')",
        "Puzzle.Exhaust('01001a')"], [],
       {"pret": ["01001a"], "exhausted": ["01046"], "defausse": ["sb012"]},
       main_exclusive=["sb012", "01089"], jouer=["sb012"], accepter_choix=True, **_PAYE_B),
    _c("sb012 Kensei : TEMOIN, heros DEJA PRET : « ready your hero » sans cible, la carte n'est pas jouable (reste en main, arme intacte)",
       "precedent 27016 : un heros pret n'est pas une cible de `ready`",
       [HEROS, _poser("01046")], [],
       {"en_main": ["sb012"], "pret": ["01046", "01001a"]},
       main_exclusive=["sb012", "01089"], jouer=["sb012"], accepter_choix=True, **_PAYE_B),
    _c("sb012 Kensei : TEMOIN, sans arme sous controle le cout est impayable : carte en main, heros toujours incline",
       "aucune amelioration WEAPON : Kensei reste en main, le heros reste incline",
       [HEROS, "Puzzle.Exhaust('01001a')"], [],
       {"en_main": ["sb012"], "exhausted": ["01001a"]},
       main_exclusive=["sb012", "01089"], jouer=["sb012"], accepter_choix=True, **_PAYE_B),
    _c("sb012 Kensei : TEMOIN, une arme DEJA inclinee ne peut pas etre inclinee de nouveau : carte en main",
       "la seule arme est inclinee : cout impayable",
       [HEROS, _poser("01046"), "Puzzle.Exhaust('01046')", "Puzzle.Exhaust('01001a')"], [],
       {"en_main": ["sb012"], "exhausted": ["01001a", "01046"]},
       main_exclusive=["sb012", "01089"], jouer=["sb012"], accepter_choix=True, **_PAYE_B),
    _c("sb012 Kensei : TEMOIN, une amelioration prete qui n'est PAS une arme (Loyalty) ne paie pas le cout",
       "seule Loyalty (OATH) est en jeu : carte en main, heros incline, Loyalty prete",
       [HEROS, _poser("sb001"), "Puzzle.Exhaust('01001a')"], [],
       {"en_main": ["sb012"], "exhausted": ["01001a"], "pret": ["sb001"]},
       main_exclusive=["sb012", "01089"], jouer=["sb012"], accepter_choix=True, **_PAYE_B),
]

# ========================================================================= sb014 Kosho
# Mockingbird 01083 (allie, 3 PV) ; Alopex ul001 (allie NINJA) ; Strength 01090 (RR) paie Kosho (cout 1).
_ALLIE = "Puzzle.PutIntoPlay('01083', under_control=True)"
_PAYE_R = dict(payer_avec=["01090"])
CAS += [
    _c("sb014 Kosho : jouee depuis la main, elle s'attache a l'ALLIE sous controle (Mockingbird), Uses pose 2 compteurs samurai",
       "« Attach to an ally you control » : Kosho attachee a Mockingbird, 2 compteurs, en jeu",
       [HEROS, _ALLIE], [],
       {"hotes": [["sb014", "01083"]], "compteurs": [["sb014", "samurai", 2]], "en_jeu": ["sb014"]},
       main_exclusive=["sb014", "01090"], jouer=["sb014"], cibles=["01083"], **_PAYE_R),
    _c("sb014 Kosho Hero Action : incline la carte, retire ses 2 compteurs (Uses la defausse), SOIGNE 2 degats de l'allie porteur ET le REDRESSE",
       "Mockingbird (3 PV) a 2 degats et inclinee : apres l'action, 0 degat, prete ; Kosho defaussee (ses 2 compteurs partis)",
       [HEROS, _ALLIE, "Puzzle.Damage('01083', 2)", "Puzzle.Exhaust('01083')"], [],
       {"degats": [["01083", 0]], "pret": ["01083"], "hors_jeu": ["sb014"], "defausse": ["sb014"]},
       main_exclusive=["sb014", "01090"], jouer=["sb014"], cibles=["01083"], declencher_apres=["Puzzle.Action('sb014', 'HeroAction', 0)"],
       **_PAYE_R),
    _c("sb014 Kosho : « heal 2 damage » : 1 seul degat a soigner -> 0 (le soin ne depasse pas les degats), l'allie est redresse",
       "Mockingbird a 1 degat, prete : l'action soigne 1 et ne bloque pas ; la carte est defaussee",
       [HEROS, _ALLIE, "Puzzle.Damage('01083', 1)"], [],
       {"degats": [["01083", 0]], "hors_jeu": ["sb014"], "defausse": ["sb014"]},
       main_exclusive=["sb014", "01090"], jouer=["sb014"], cibles=["01083"], declencher_apres=["Puzzle.Action('sb014', 'HeroAction', 0)"],
       **_PAYE_R),
    _c("sb014 Kosho : « Max 1 TRAINING upgrade per ally » : une seconde amelioration TRAINING (Attack Training ua004) ne s'attache pas a Alopex deja equipee",
       "Kosho (TRAINING) sur Alopex (NINJA) ; Attack Training reste en main (plafond du moteur, trait TRAINING), Kosho reste attachee",
       [HEROS, "Puzzle.PutIntoPlay('ul001', under_control=True)"], [],
       {"hotes": [["sb014", "ul001"]], "en_main": ["ua004"]},
       main_exclusive=["sb014", "ua004", "01090", "01090"], jouer=["sb014", "ua004"], cibles=["ul001"], **_PAYE_R),
    _c("sb014 Kosho : « an ally YOU control » : sans allie sous mon controle (celui du 2e joueur seul) elle n'est pas jouable",
       "partie a deux : Mockingbird est a l'AUTRE joueur ; Kosho reste en main",
       [HEROS, "Puzzle.PutIntoPlay('01083', under_control=True, player=1)"], [],
       {"en_main": ["sb014"], "hors_jeu": ["sb014"]},
       main_exclusive=["sb014", "01090"], jouer=["sb014"], heros2="iron_man", **_PAYE_R),
    _dispo("sb014 Kosho : l'action est proposee en forme heros (temoin positif)",
           "Kosho attachee, 2 compteurs : 1 Hero Action disponible", [HEROS, _ALLIE], "sb014", "HeroAction", 1,
           main_exclusive=["sb014", "01090"], jouer=["sb014"], cibles=["01083"], **_PAYE_R),
    _dispo("sb014 Kosho : Hero Action NON proposee en forme alter-ego",
           "forme heros uniquement", [_ALLIE], "sb014", "HeroAction", 0,
           main_exclusive=["sb014", "01090"], jouer=["sb014"], cibles=["01083"], **_PAYE_R),
]

# ========================================================================= sb015 Oathbreaker
# False Alarm 01112 : « You are confused » (effet VISIBLE : Confused sur l'identite). Revelee par `Puzzle.Reveal` depuis le deck rencontre.
CAS += [
    _c("sb015 Oathbreaker Hero Interrupt : annule False Alarm (revelee du deck rencontre) : le heros n'est PAS desoriente, la carte est defaussee",
       "cout : Loyalty (OATH) defaussee ; « cancel all of that card's effects and discard it » : pas de Desoriente, False Alarm dans la defausse rencontre",
       [HEROS, _poser("sb001")], ["Puzzle.Reveal('01112')"],
       {"statuts_absents": [["01001a", "Confused"]], "defausse_rencontre": ["01112"], "defausse": ["sb015", "sb001"], "hors_jeu": ["sb001"]},
       main_exclusive=["sb015"], accepter_choix=True),
    _c("sb015 Oathbreaker : TEMOIN, sans amelioration OATH le cout est impayable : False Alarm se resout (heros desoriente), Oathbreaker reste en main",
       "aucune OATH sous controle : l'interruption n'est pas offerte",
       [HEROS], ["Puzzle.Reveal('01112')"],
       {"statuts": [["01001a", "Confused"]], "en_main": ["sb015"]},
       main_exclusive=["sb015"], accepter_choix=True),
    _c("sb015 Oathbreaker : « an OATH upgrade you control » : le joueur CHOISIT laquelle defausser (Courage designee) : Loyalty reste",
       "Loyalty et Courage en jeu : Courage est defaussee en cout, Loyalty garde ses 3 compteurs",
       [HEROS, _poser("sb001"), _poser("sb003")], ["Puzzle.Reveal('01112')"],
       {"hors_jeu": ["sb003"], "en_jeu": ["sb001"], "compteurs": [["sb001", "samurai", 3]], "statuts_absents": [["01001a", "Confused"]]},
       main_exclusive=["sb015"], cibles=["sb003"], accepter_choix=True),
    _c("sb015 Oathbreaker : TEMOIN, « Hero Interrupt » : en forme alter-ego l'interruption n'est pas offerte, l'alter-ego est desoriente",
       "Peter Parker (alter-ego) : False Alarm se resout, Loyalty reste en jeu, Oathbreaker en main",
       [_poser("sb001")], ["Puzzle.Reveal('01112')"],
       {"statuts": [["01001b", "Confused"]], "en_jeu": ["sb001"], "en_main": ["sb015"]},
       main_exclusive=["sb015"], accepter_choix=True),
]

# ========================================================================= sb016 Wakizashi
CAS += [
    _c("sb016 Wakizashi Hero Response : une OATH (Loyalty) DEFAUSSEE DU JEU : Wakizashi s'incline, 1 carte piochee (main 1 -> 2)",
       "`Puzzle.Discard` d'une amelioration OATH en jeu : Hero Response, cout Exhaust, pioche 1",
       [HEROS, _poser("sb016"), _poser("sb001")] + _DECK5, ["Puzzle.Discard('sb001')"],
       {"exhausted": ["sb016"], "taille_main": 2, "defausse": ["sb001"]}, main_exclusive=["01090"], accepter_choix=True),
    _c("sb016 Wakizashi : la defausse par USES (dernier compteur retire par Loyalty apres une defense) en est une aussi : 1 carte piochee",
       "Loyalty a 1 compteur, defense de base : Forced Response retire le dernier, Uses la defausse, Wakizashi pioche",
       [HEROS, _poser("sb016"), _poser("sb001"), "Puzzle.Counter('sb001', 'samurai', -2)"] + _DECK5,
       ["Puzzle.Defend('01001a', '01094')"],
       {"exhausted": ["sb016"], "taille_main": 2, "hors_jeu": ["sb001"]}, main_exclusive=["01090"], accepter_choix=True),
    _c("sb016 Wakizashi : « an OATH upgrade » de N'IMPORTE QUEL joueur : l'OATH du 2e joueur (partie a deux) defaussee fait piocher",
       "Loyalty du second joueur en jeu, defaussee : Wakizashi du premier joueur pioche",
       [HEROS, _poser("sb016"), "Puzzle.PutIntoPlay('sb001', under_control=True, player=1)"] + _DECK5, ["Puzzle.Discard('sb001')"],
       {"exhausted": ["sb016"], "taille_main": 2}, main_exclusive=["01090"], heros2="iron_man", accepter_choix=True),
    _c("sb016 Wakizashi : TEMOIN, une amelioration NON OATH defaussee du jeu (Armored Vest) ne fait rien piocher",
       "Armored Vest defaussee : Wakizashi reste prete, main inchangee",
       [HEROS, _poser("sb016"), _poser("01081")] + _DECK5, ["Puzzle.Discard('01081')"],
       {"pret": ["sb016"], "taille_main": 1}, main_exclusive=["01090"], accepter_choix=True),
    _c("sb016 Wakizashi : TEMOIN, « discarded FROM PLAY » : une OATH defaussee du DECK (et non du jeu) ne fait rien piocher",
       "Loyalty au milieu du deck puis defaussee : Wakizashi reste prete, main = 1 (Strength). (`Puzzle.Discard` cherche dans le deck, la "
       "defausse puis le jeu, jamais dans la main ; une carte introuvable serait FABRIQUEE : d'ou le deck.)",
       [HEROS, _poser("sb016"), "Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01073', 'sb001', '01074')"], ["Puzzle.Discard('sb001')"],
       {"pret": ["sb016"], "taille_main": 1, "defausse": ["sb001"]}, main_exclusive=["01090"], accepter_choix=True),
    _c("sb016 Wakizashi : TEMOIN D'EPUISEMENT, deux OATH defaussees dans le meme round : UNE seule carte piochee (main 1 -> 2, pas 3)",
       "Wakizashi inclinee apres la 1re : la 2e defausse ne declenche plus rien",
       [HEROS, _poser("sb016"), _poser("sb001"), _poser("sb003")] + _DECK5, ["Puzzle.Discard('sb001')", "Puzzle.Discard('sb003')"],
       {"exhausted": ["sb016"], "taille_main": 2, "defausse": ["sb001", "sb003"]}, main_exclusive=["01090"], accepter_choix=True),
    _c("sb016 Wakizashi : TEMOIN, Hero Response : en forme alter-ego rien n'est pioche",
       "Peter Parker : l'OATH defaussee ne declenche pas Wakizashi (Hero Response), main inchangee",
       [_poser("sb016"), _poser("sb001")] + _DECK5, ["Puzzle.Discard('sb001')"],
       {"pret": ["sb016"], "taille_main": 1}, main_exclusive=["01090"], accepter_choix=True),
    _c("sb016 Wakizashi : base automatique « Restricted » (1) lue dans `desc`, traits NINJA et WEAPON, carte unique",
       "`face.restricted == 1` en jeu ; traits NINJA + WEAPON ; la carte est unique",
       [HEROS, _poser("sb016")], [],
       {"carte": "sb016", "attributs": {"restricted": 1}, "traits": ["NINJA", "WEAPON"], "unique": True},
       verifier="sb_attributs_carte"),
]

# ========================================================================= sb017 Uno
_UNO = "Puzzle.PutIntoPlay('sb017', under_control=True)"
CAS += [
    _c("sb017 Uno Response : apres SON attaque de base, 1 compteur samurai est place sur l'OATH choisie (Loyalty 3 -> 4)",
       "« After Uno uses a basic power » : attaque de base d'Uno (ATQ 1) sur Rhino, puis le compteur va sur Loyalty",
       [HEROS, _UNO, _poser("sb001")], ["Puzzle.Attack('sb017')"],
       {"compteurs": [["sb001", "samurai", 4]], "degats": [["01094", 1]]}, main_exclusive=["01090"], cibles=["01094", "sb001"]),
    _c("sb017 Uno : « uses A basic power » : son CONTRE de base compte aussi (Loyalty 3 -> 4, menace 6 -> 5)",
       "contre de base d'Uno (CTR 1) sur le complot principal, puis le compteur va sur Loyalty",
       [MENACE, HEROS, _UNO, _poser("sb001")], ["Puzzle.Thwart('sb017')"],
       {"compteurs": [["sb001", "samurai", 4]], "menace": [["01097b", 5]]}, main_exclusive=["01090"], cibles=["01097b", "sb001"]),
    _c("sb017 Uno : « the OATH upgrade YOU choose » : le compteur va sur une AUTRE OATH (Courage designee), Loyalty garde ses 3",
       "deux OATH en jeu : le joueur designe Courage", [HEROS, _UNO, _poser("sb001"), _poser("sb003")], ["Puzzle.Attack('sb017')"],
       {"compteurs": [["sb003", "samurai", 4], ["sb001", "samurai", 3]]}, main_exclusive=["01090"], cibles=["01094", "sb003"]),
    _c("sb017 Uno : TEMOIN, « After UNO » : l'attaque de base du HEROS ne declenche pas la Response (Loyalty garde 3 compteurs)",
       "Spider-Man attaque : aucun compteur place par Uno",
       [HEROS, _UNO, _poser("sb001")], ["Puzzle.Attack('01001a')"],
       {"compteurs": [["sb001", "samurai", 3]]}, main_exclusive=["01090"], cibles=["01094", "sb001"]),
    _c("sb017 Uno : sans amelioration OATH sous controle la Response ne pose rien et ne bloque pas l'attaque",
       "aucune OATH : l'attaque a lieu (1 degat), aucune erreur", [HEROS, _UNO], ["Puzzle.Attack('sb017')"],
       {"degats": [["01094", 1]], "en_jeu": ["sb017"]}, main_exclusive=["01090"], cibles=["01094"]),
    _c("sb017 Uno : ATQ 1, CTR 1, 3 PV, unique, traits NINJA SAMURAI TURTLE",
       "valeurs imprimees (etape 6) : ATQ 1*, CTR 1*, PV 3 (la sonde lit `attack`, `thwart`, `max_health`)",
       [HEROS, _UNO], [],
       {"carte": "sb017", "attributs": {"attack": 1, "thwart": 1, "max_health": 3}, "traits": ["NINJA", "SAMURAI", "TURTLE"],
        "unique": True},
       verifier="sb_attributs_carte"),
]

# ========================================================================= sb018 Musha Shugyo
# jouee depuis la main (cout 1 [energy], payee par Energy 01088) puis ramenee a 1 menace : `declencher_apres` s'execute APRES `jouer`.
_MUSHA = dict(main_exclusive=["sb018", "01088"], jouer=["sb018"], payer_avec=["01088"])
# ⚠ `Puzzle.SetThreat` / `PlaceThreat` negatif font retirer la menace PAR LA MANIGANCE ELLE-MEME (`face.RemoveThreatFromSchemes([face], ...)`) :
# la regle « characters other than the owner cannot remove threat » de Musha Shugyo la BLOQUE (lecon payee le 17/10/2026). On la vainc donc
# pour de vrai : 5 contres de base du heros (CTR 1) separes par un redressement, les 5 menaces.
_VAINCRE = ["Puzzle.Thwart('01001a')", "Puzzle.Ready('01001a')"] * 4 + ["Puzzle.Thwart('01001a')"]
_DECK_3_OATH = ["Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01073', 'sb003', 'sb001')"]
CAS += [
    _c("sb018 Musha Shugyo : jouee depuis la main, elle entre en jeu avec 5 menaces (fixe, sans etoile)",
       "StartingThreat 5 : menace 5 sur la carte, en jeu", [HEROS], [],
       {"menace": [["sb018", 5]], "en_jeu": ["sb018"]}, **_MUSHA),
    _c("sb018 Musha Shugyo : le PROPRIETAIRE (Spider-Man) retire la derniere menace : elle est vaincue, deck et defausse sont fouilles : DEUX OATH en jeu",
       "deck [Loyalty, Courage] : « up to 2 » : les deux entrent en jeu (le joueur accepte les deux recherches)",
       [HEROS] + _DECK_3_OATH, [],
       {"hors_jeu": ["sb018"], "en_jeu": ["sb001", "sb003"]},
       declencher_apres=_VAINCRE, cibles=["sb018"], accepter_choix=True, **_MUSHA),
    _c("sb018 Musha Shugyo : la recherche couvre aussi la DEFAUSSE (Rectitude y est, rien dans le deck)",
       "« search their deck AND discard pile » : Rectitude de la defausse entre en jeu",
       [HEROS, "Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01073', '01074')", "Puzzle.CreatePlayerDiscardPile('sb002')"], [],
       {"hors_jeu": ["sb018"], "en_jeu": ["sb002"]},
       declencher_apres=_VAINCRE, cibles=["sb018"], accepter_choix=True, **_MUSHA),
    _c("sb018 Musha Shugyo : « UP TO 2 » : trois OATH disponibles (deck + defausse) : DEUX seulement entrent en jeu, la troisieme reste dans le deck",
       "deck [Loyalty, Courage], defausse [Rectitude] : choix Loyalty puis Rectitude : Courage reste dans le deck",
       [HEROS] + _DECK_3_OATH + ["Puzzle.CreatePlayerDiscardPile('sb002')"], [],
       {"en_jeu": ["sb001", "sb002"], "hors_jeu": ["sb018", "sb003"], "dans_deck_joueur": ["sb003"]},
       declencher_apres=_VAINCRE, cibles=["sb018", "sb001", "sb002"], accepter_choix=True, **_MUSHA),
    _c("sb018 Musha Shugyo : « Characters other than the owner » : un ALLIE du proprietaire (Mockingbird) ne retire PAS de menace",
       "Mockingbird (CTR 1) contre la carte (5 menaces) : la menace reste a 5, la carte reste en jeu",
       [HEROS, "Puzzle.PutIntoPlay('01083', under_control=True)"], [],
       {"menace": [["sb018", 5]], "en_jeu": ["sb018"]},
       declencher_apres=["Puzzle.Thwart('01083')"], cibles=["sb018"], **_MUSHA),
    _c("sb018 Musha Shugyo : TEMOIN positif, un evenement du proprietaire (Vow, CTR 1) retire de la menace (5 -> 4)",
       "la source d'un evenement est l'IDENTITE de celui qui le joue (`event.py` OnRemoveSchemeThreat) : retrait autorise",
       [HEROS], [],
       {"menace": [["sb018", 4]]},
       jouer_apres=["sb011"], cibles=["sb018"],
       main_exclusive=["sb018", "sb011", "01088", "01088"], jouer=["sb018"], payer_avec=["01088"]),
    _c("sb018 Musha Shugyo : TEMOIN positif, le contre de base du heros proprietaire retire de la menace (5 -> 4)",
       "Spider-Man (CTR 1) : un contre de base, la menace passe a 4",
       [HEROS], [],
       {"menace": [["sb018", 4]]},
       declencher_apres=["Puzzle.Thwart('01001a')"], cibles=["sb018"], **_MUSHA),
    _c("sb018 Musha Shugyo : vaincue elle va a l'AFFICHAGE DES VICTOIRES (Victory 0)",
       "« Victory 0 » : base automatique ; la carte vaincue est dans l'affichage des victoires, pas en defausse",
       [HEROS, "Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01073', '01074')"], [],
       {"carte": "sb018", "zone": "victoire"},
       declencher_apres=_VAINCRE, cibles=["sb018"], accepter_choix=True,
       verifier="sb_carte_en_zone", **_MUSHA),
]

# ========================================================================= sb019 Gusoku
_GUSOKU = "Puzzle.PutIntoPlay('sb019', under_control=True)"
CAS += [
    _c("sb019 Gusoku Hero Response : apres l'ATTAQUE de base du heros, Gusoku s'incline, retire 1 compteur a Loyalty (3 -> 2) et REDRESSE le heros",
       "le heros est incline par son attaque, puis redresse par la Response",
       [HEROS, _GUSOKU, _poser("sb001")], ["Puzzle.Attack('01001a')"],
       {"pret": ["01001a"], "exhausted": ["sb019"], "compteurs": [["sb001", "samurai", 2]]},
       main_exclusive=["01090"], cibles=["01094", "sb001"], accepter_choix=True),
    _c("sb019 Gusoku : apres le CONTRE de base du heros (complot principal a 6) : meme effet",
       "contre de base : heros redresse, Gusoku inclinee, Loyalty 3 -> 2",
       [MENACE, HEROS, _GUSOKU, _poser("sb001")], ["Puzzle.Thwart('01001a')"],
       {"pret": ["01001a"], "exhausted": ["sb019"], "compteurs": [["sb001", "samurai", 2]]},
       main_exclusive=["01090"], cibles=["01097b", "sb001"], accepter_choix=True),
    _c("sb019 Gusoku : apres la DEFENSE de base du heros (Rhino attaque) : meme effet",
       "defense de base : le heros defenseur s'incline puis est redresse ; l'OATH est Courage (Loyalty, elle, perdrait AUSSI un compteur "
       "apres une defense : sa propre Forced Response)",
       [HEROS, _GUSOKU, _poser("sb003")], ["Puzzle.Defend('01001a', '01094')"],
       {"pret": ["01001a"], "exhausted": ["sb019"], "compteurs": [["sb003", "samurai", 2]]},
       main_exclusive=["01090"], cibles=["sb003"], accepter_choix=True),
    _c("sb019 Gusoku : « FROM AN OATH upgrade » : le joueur CHOISIT laquelle perd un compteur (Rectitude designee), Loyalty garde 3",
       "deux OATH (Loyalty, Rectitude) apres un contre de base (Rectitude perd AUSSI 1 compteur par sa Forced Response : 3 -> 2, puis "
       "Gusoku en retire 1 : 1) ; Loyalty garde ses 3",
       [MENACE, HEROS, _GUSOKU, _poser("sb001"), _poser("sb002")], ["Puzzle.Thwart('01001a')"],
       {"pret": ["01001a"], "compteurs": [["sb002", "samurai", 1], ["sb001", "samurai", 3]]},
       main_exclusive=["01090"], cibles=["01097b", "sb002"], accepter_choix=True),
    _c("sb019 Gusoku : TEMOIN, sans compteur samurai a retirer le cout est impayable : le heros reste incline apres son attaque",
       "Loyalty n'a plus qu'un compteur... retire ? non : aucune OATH en jeu : pas de Response, heros incline, Gusoku prete",
       [HEROS, _GUSOKU], ["Puzzle.Attack('01001a')"],
       {"exhausted": ["01001a"], "pret": ["sb019"]}, main_exclusive=["01090"], cibles=["01094"], accepter_choix=True),
    _c("sb019 Gusoku : TEMOIN, « YOUR basic powers » : l'attaque d'un ALLIE (Mockingbird) ne declenche pas Gusoku (heros incline d'avance)",
       "le heros reste incline, Loyalty garde ses 3 compteurs",
       [HEROS, _GUSOKU, _poser("sb001"), "Puzzle.PutIntoPlay('01083', under_control=True)", "Puzzle.Exhaust('01001a')"],
       ["Puzzle.Attack('01083')"],
       {"exhausted": ["01001a"], "pret": ["sb019"], "compteurs": [["sb001", "samurai", 3]]},
       main_exclusive=["01090"], cibles=["01094", "sb001"], accepter_choix=True),
    _c("sb019 Gusoku : TEMOIN D'EPUISEMENT, deux attaques de base dans le meme round : la 2e ne declenche plus rien (heros incline, 1 seul compteur retire)",
       "Gusoku inclinee apres la 1re Response : apres la 2e attaque le heros reste incline, Loyalty 2 (et non 1)",
       [HEROS, _GUSOKU, _poser("sb001")], ["Puzzle.Attack('01001a')", "Puzzle.Attack('01001a')"],
       {"exhausted": ["01001a", "sb019"], "compteurs": [["sb001", "samurai", 2]]},
       main_exclusive=["01090"], cibles=["01094", "sb001"], accepter_choix=True),
    _c("sb019 Gusoku : le DERNIER compteur d'une OATH retire en cout : l'OATH est defaussee (Uses), le heros est redresse",
       "Loyalty a 1 compteur : retire par le cout, Loyalty defaussee, heros pret",
       [HEROS, _GUSOKU, _poser("sb001"), "Puzzle.Counter('sb001', 'samurai', -2)"], ["Puzzle.Attack('01001a')"],
       {"pret": ["01001a"], "hors_jeu": ["sb001"], "defausse": ["sb001"]},
       main_exclusive=["01090"], cibles=["01094", "sb001"], accepter_choix=True),
    _c("sb019 Gusoku : unique, ARMOR, Hero Response seulement : valeurs imprimees (traits, unicite)",
       "traits ARMOR, unique ✦", [HEROS, _GUSOKU], [],
       {"carte": "sb019", "attributs": {}, "traits": ["ARMOR"], "unique": True}, verifier="sb_attributs_carte"),
]

# ========================================================================= sb020 Iaido
# Genius 01089 (BB) paie Iaido (cout 1) ; l'evenement est joue PAR LE PILOTE pendant le pouvoir de base (interruption), sans `jouer`.
# Spider-Man : ATQ 2, CTR 1, DEF 1 ; Rhino 01094.
_DEUX_ICONES = ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01111')"]   # Explosion : 2 icones de boost


def _i(nom, pourquoi, mise, declencher, attendu, **cle):
    return _c(nom, pourquoi, mise, declencher, attendu, main_exclusive=["sb020", "01089"], payer_avec=["01089"], **cle)


CAS += [
    _i("sb020 Iaido Hero Interrupt : l'ATTAQUE de base du heros gagne +2 (ATQ 2 + 2 = 4 degats a Rhino) ET 1 compteur samurai est place (Loyalty 3 -> 4)",
       "evenement joue pendant l'attaque (interruption), le bonus compte dans le pouvoir",
       [HEROS, _poser("sb001")], ["Puzzle.Attack('01001a')"],
       {"degats": [["01094", 4]], "compteurs": [["sb001", "samurai", 4]], "defausse": ["sb020"]},
       cibles=["01094", "sb001"], accepter_choix=True),
    _c("sb020 Iaido : TEMOIN, sans Iaido la meme attaque ne fait que 2 degats",
       "contre-cas : ATQ 2 seul", [HEROS], ["Puzzle.Attack('01001a')"], {"degats": [["01094", 2]]},
       main_exclusive=["01090"], cibles=["01094"]),
    _i("sb020 Iaido : le CONTRE de base gagne +2 aussi (CTR 1 + 2 = 3 : menace 6 -> 3)",
       "« +2 to THAT power » : le contre de base",
       [MENACE, HEROS, _poser("sb001")], ["Puzzle.Thwart('01001a')"],
       {"menace": [["01097b", 3]], "compteurs": [["sb001", "samurai", 4]]},
       cibles=["01097b", "sb001"], accepter_choix=True),
    _i("sb020 Iaido : la DEFENSE de base gagne +2 (DEF 3 + 2 = 5 contre Rhino ATQ 2 + 2 icones de boost = 4 : aucun degat pour l'identite)",
       "« When you use a basic power » : la defense aussi ; le compteur est place sur Courage (Loyalty, elle, perdrait AUSSI 1 compteur apres la defense)",
       [HEROS, _poser("sb003")] + _DEUX_ICONES, ["Puzzle.Defend('01001a', '01094')"],
       {"degats_identite": 0, "compteurs": [["sb003", "samurai", 4]]},
       cibles=["sb003"], accepter_choix=True, avec_boost=True),
    _c("sb020 Iaido : TEMOIN de la defense, sans Iaido le meme coup (ATQ 4 contre DEF 3) inflige 1 degat a l'identite",
       "contre-cas : DEF 3 seule contre Rhino ATQ 2 + 2 icones de boost", [HEROS] + _DEUX_ICONES,
       ["Puzzle.Defend('01001a', '01094')"], {"degats_identite": 1},
       main_exclusive=["01090"], avec_boost=True),
    _i("sb020 Iaido : « FOR THIS USE » : apres l'attaque l'ATQ courant du heros est revenu a sa valeur imprimee (le +2 n'est pas durable)",
       "ATQ courant = imprime apres l'attaque amelioree (ecart 0), 4 degats infliges",
       [HEROS], ["Puzzle.Attack('01001a')"],
       {"attributs": {"attack": 0}, "degats": [["01094", 4]]},
       cibles=["01094"], accepter_choix=True),
    _i("sb020 Iaido : « You MAY place » : refus (Cancel) : le +2 compte quand meme (4 degats) mais Loyalty garde 3 compteurs",
       "le « may » porte sur le compteur seulement",
       [HEROS, _poser("sb001")], ["Puzzle.Attack('01001a')"],
       {"degats": [["01094", 4]], "compteurs": [["sb001", "samurai", 3]]},
       cibles=["01094"], choisir_option="Cancel"),
    _i("sb020 Iaido : sans amelioration OATH le +2 s'applique sans question de compteur (4 degats)",
       "aucune OATH sous controle", [HEROS], ["Puzzle.Attack('01001a')"], {"degats": [["01094", 4]], "defausse": ["sb020"]},
       cibles=["01094"], accepter_choix=True),
    _i("sb020 Iaido : TEMOIN, « When YOU use » : l'attaque d'un ALLIE (Mockingbird, ATQ 1) n'ouvre pas Iaido : 1 degat, carte en main",
       "le pouvoir de base d'un allie n'est pas le votre",
       [HEROS, "Puzzle.PutIntoPlay('01083', under_control=True)"], ["Puzzle.Attack('01083')"],
       {"degats": [["01094", 1]], "en_main": ["sb020"]},
       cibles=["01094"], accepter_choix=True),
]


VERIFICATIONS = r'''
def sb_carte_en_zone(monde, aides):
    """`attendu` : carte, zone (victoire | defausse). La carte (par card_id) doit se trouver dans cette zone."""
    attendu = aides["cas"]["attendu"]
    zones = {"victoire": [f for f in monde.victory_display.GetAll()],
             "defausse": [f for j in monde.players for f in j.discard_pile.GetAll()]}
    ids = [getattr(f.paper, "card_id", None) for f in zones[attendu["zone"]]]
    if attendu["carte"] not in ids:
        return False, f"{attendu['carte']} n'est pas dans {attendu['zone']} ({ids})"
    return True, f"{attendu['carte']} est dans {attendu['zone']}"


def sb_attributs_carte(monde, aides):
    """`attendu` : carte (en jeu), attributs {nom: valeur} lus par getattr, traits [..], unique (bool)."""
    attendu = aides["cas"]["attendu"]
    face = aides["par_id"](monde, attendu["carte"])
    if face is None:
        return False, f"{attendu['carte']} introuvable en jeu"
    soucis = []
    for nom, valeur in (attendu.get("attributs") or {}).items():
        courant = getattr(face, nom, None)
        if courant != valeur:
            soucis.append(f"{nom}={courant!r} (attendu {valeur!r})")
    for trait in attendu.get("traits") or []:
        if not face.HasTrait(trait):
            soucis.append(f"trait {trait} absent")
    if "unique" in attendu and bool(face.IsUnique()) != attendu["unique"]:
        soucis.append(f"unique={face.IsUnique()} (attendu {attendu['unique']})")
    if soucis:
        return False, " ; ".join(soucis)
    return True, f"{attendu['carte']} : attributs {attendu.get('attributs')} traits {attendu.get('traits')} conformes"


def sb_debug(monde, aides):
    rep = []
    for objet in monde.object_manager.card_dict.values():
        f = getattr(objet, "face", None)
        if f is not None and f.IsInPlay():
            rep.append(f"{getattr(f.paper,'card_id','?')}:thr={getattr(f,'threat','-')}:exh={f.IsExhaust() if hasattr(f,'IsExhaust') else '-'}")
    ident = aides["identite"](monde)
    return False, f"thw={ident.thwart} {' '.join(rep)}"

def sb_actions_disponibles(monde, aides):
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
'''
