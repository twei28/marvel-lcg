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
