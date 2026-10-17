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

VERIFICATIONS = r'''

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
