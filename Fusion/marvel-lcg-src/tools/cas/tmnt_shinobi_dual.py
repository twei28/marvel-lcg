# Cas test_capacites du pack tmnt_shinobi_dual (Inkwire, TMNT Shinobi, les 12 cartes DUAL, prefixe `sc`), 17/10/2026.
# Filtre : `[sc]`. Gabarits : .planning/tmnt/shinobi-dual-gabarits.md. Questions : .planning/tmnt/shinobi-dual-questions.md.
#
# Une carte Dual compte comme LES DEUX types, au deck-building ET en jeu (livret p.7). Preuves, pour CHAQUE carte :
#  - `sc_classes` : `IsClass` et `CardFinder(card_class=X)` / `card_classes=[X]` la reconnaissent pour CHACUN de ses deux
#    types, pas pour les deux autres, ni comme aspect, ni comme Basic ;
#  - cas « Jennika » : jouer la carte avec Jennika (Ninja Senpai : une Interruption par classe Shinobi, limite une fois par
#    round POUR CHAQUE Shinobi) donne +2/+2/+2 (deux classes = deux declenchements), contre +1/+1/+1 pour une carte a une
#    seule classe (cas de reference de tmnt_jennika.py) ;
#  - le deck-building (types du Path) est prouve par tools/tests-lanceur/regles-shinobi-dual.test.mjs.
#
# Conventions :
#  - Spider-Man (01001) demarre en ALTER EGO ; HEROS le met en forme heros ; Jennika demarre en alter-ego (tj001b) ;
#  - Rhino 01094 (14 PV), complot principal 01097b, 01101 Hydra Mercenary (3 PV) ; deck rencontre bourre de « I'm Tough »
#    (01105) : aucune carte rencontre ne brouille la mesure ;
#  - `main_exclusive` vide la main (APRES la mise en place) : chaque cas sait avec QUOI il paie
#    (01088 Energy = YY, 01089 Genius = BB, 01090 Strength = RR) ;
#  - 01046 Energy Daggers (core, WEAPON, aucun effet joue ici) est l'amelioration WEAPON sous controle des cas Nendo / Omawari.
SC = "rhino"
HEROS = "Puzzle.ChangeForm('01001b')"
JHEROS = "Puzzle.ChangeToFace('tj001b', 'tj001a')"
COMPLOT = "01097b"
ARME = "Puzzle.PutIntoPlay('01046', under_control=True)"
SANS_BOOST = ["Puzzle.EmptyEncounterDeck()",
              "Puzzle.CreateEncounterDeck('01105', '01105', '01105', '01105', '01105', '01105', '01105', '01105')"]
SENPAI_DEUX_CLASSES = {"attack": 2, "thwart": 2, "defense": 2}
CLASSES = {
    "sc001": ("Bushido", "Kuji-Kiri"), "sc002": ("Bushido", "Kuji-Kiri"), "sc003": ("Bushido", "Ninjutsu"),
    "sc004": ("Bushido", "Ninjutsu"), "sc005": ("Bushido", "Taijutsu"), "sc006": ("Bushido", "Taijutsu"),
    "sc007": ("Kuji-Kiri", "Ninjutsu"), "sc008": ("Kuji-Kiri", "Ninjutsu"), "sc009": ("Kuji-Kiri", "Taijutsu"),
    "sc010": ("Kuji-Kiri", "Taijutsu"), "sc011": ("Ninjutsu", "Taijutsu"), "sc012": ("Ninjutsu", "Taijutsu"),
}
NOMS = {"sc001": "Nendo", "sc002": "Shugorei", "sc003": "Omawari", "sc004": "Kuragari", "sc005": "Yoi-Dachi",
        "sc006": "Migatte", "sc007": "Mizuki", "sc008": "Naito Dansa", "sc009": "Yomi", "sc010": "Kusuri",
        "sc011": "Kenbu", "sc012": "Hitodama"}


def _c(nom, pourquoi, mise, declencher, attendu, **cle):
    # La main de depart est VIDEE juste apres le changement de forme : sinon le pilote, qui accepte la premiere option
    # jouable, y joue des Interruptions pendant la mise en place (`Puzzle.SetThreat` sur 01097b ouvre une fenetre ou
    # Spider-Man joue Emergency et ramene la menace posee a 0 : constate sur Mizuki, 17/10/2026).
    mise = list(mise)
    rang = 1 if mise and mise[0].startswith("Puzzle.Change") else 0
    mise.insert(rang, "Puzzle.EmptyHand()")
    if not cle.pop("avec_boost", False):
        mise = SANS_BOOST + mise
    cas = {"nom": "[sc] " + nom, "pourquoi": pourquoi, "scenario": cle.pop("scenario", SC),
           "heros": cle.pop("heros", "spider_man"), "mise_en_place": list(mise), "declencher": list(declencher),
           "verifier": cle.pop("verifier", "etat_attendu"), "attendu": attendu}
    cas.update(cle)
    return cas


CAS = []

# ========================================================================= les deux types, pour les douze (moteur)
for _cid, (_a, _b) in CLASSES.items():
    _autres = [k for k in ("Bushido", "Ninjutsu", "Kuji-Kiri", "Taijutsu") if k not in (_a, _b)]
    CAS.append(_c(f"{_cid} {NOMS[_cid]} (classe DUAL {_a};{_b}) : reconnue pour LES DEUX types par IsClass et CardFinder, ni aspect ni Basic",
                  f"livret p.7 : « Dual Shinobi cards count as both types » ; un filtre {_a} la trouve, un filtre {_b} la trouve, "
                  f"pas un filtre {_autres[0]} ni {_autres[1]}",
                  ["Puzzle.CreateHandCards('" + _cid + "')"], [],
                  {"carte": _cid, "oui": [_a, _b],
                   "non": _autres + ["Aspect", "Basic", "Aggression", "Justice", "Leadership", "Protection"]},
                  verifier="sc_classes"))

# ========================================================================= sc001 Nendo
CAS += [
    _c("sc001 Nendo : Hero Action (attack), un WEAPON s'incline -> 4 degats a Rhino ET Rhino est HEBETE (Dazed)",
       "« Exhaust a WEAPON upgrade you control -> deal 4 damage to an enemy. Daze that enemy » : 01046 (WEAPON) s'incline, "
       "Rhino perd 4 PV puis porte la carte Dazed, Nendo va en defausse",
       [HEROS, ARME], [],
       {"degats": [["01094", 4]], "statuts": [["01094", "Dazed"]], "exhausted": ["01046"], "defausse": ["sc001"]},
       main_exclusive=["sc001", "01090"], payer_avec=["01090"], jouer=["sc001"], cibles=["01094"]),
    _c("sc001 Nendo : SANS amelioration WEAPON en jeu la carte n'est PAS jouable (reste en main, aucun degat)",
       "le cout « Exhaust a WEAPON upgrade you control » est impayable : pas de degats, pas de Dazed",
       [HEROS], [],
       {"degats": [["01094", 0]], "statuts_absents": [["01094", "Dazed"]], "en_main": ["sc001"]},
       main_exclusive=["sc001", "01090"], payer_avec=["01090"], jouer=["sc001"], cibles=["01094"]),
    _c("sc001 Nendo : une amelioration NON WEAPON (01081 Armored Vest) ne paie pas le cout : reste en main",
       "« a WEAPON upgrade » : le trait compte ; une autre amelioration sous controle ne suffit pas",
       [HEROS, "Puzzle.PutIntoPlay('01081', under_control=True)"], [],
       {"degats": [["01094", 0]], "statuts_absents": [["01094", "Dazed"]], "en_main": ["sc001"], "pret": ["01081"]},
       main_exclusive=["sc001", "01090"], payer_avec=["01090"], jouer=["sc001"], cibles=["01094"]),
    _c("sc001 Nendo : un WEAPON DEJA incline ne paie pas le cout (cout = incliner) : reste en main",
       "« Exhaust » exige une carte redressee",
       [HEROS, "Puzzle.PutIntoPlay('01046', under_control=True, exhaust=True)"], [],
       {"degats": [["01094", 0]], "en_main": ["sc001"]},
       main_exclusive=["sc001", "01090"], payer_avec=["01090"], jouer=["sc001"], cibles=["01094"]),
    _c("sc001 Nendo : un sbire (Hydra Mercenary 3 PV) vaincu par les 4 degats : il quitte le jeu, rien ne plante",
       "4 >= 3 PV : le sbire est defait ; « Daze that enemy » ne vise plus rien (un ennemi vaincu n'est pas hebete)",
       [HEROS, ARME, "Puzzle.Reveal('01101')"], [],
       {"hors_jeu": ["01101"], "exhausted": ["01046"], "defausse": ["sc001"]},
       main_exclusive=["sc001", "01090"], payer_avec=["01090"], jouer=["sc001"], cibles=["01101"]),
    _c("sc001 Nendo avec JENNIKA : jouer une Dual Bushido/Kuji-Kiri declenche Ninja Senpai pour LES DEUX classes (+2/+2/+2)",
       "tj001a : une Interruption par classe Shinobi, une fois par round chacune ; Bushido ET Kuji-Kiri = deux declenchements",
       [JHEROS, ARME], [],
       {"attributs": SENPAI_DEUX_CLASSES, "defausse": ["sc001"], "degats": [["01094", 4]]},
       heros="jennika", main_exclusive=["sc001", "01090"], payer_avec=["01090"], jouer=["sc001"], cibles=["01094"]),
]

# ========================================================================= sc002 Shugorei
CAS += [
    _c("sc002 Shugorei : entre en jeu avec 4 compteurs samurai (Uses), payee par Genius (mental)",
       "« Uses (4 samurai counters) » : base native `desc.Uses = \"4,samurai\"`",
       [HEROS, "Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01089', '01089', '01089')"], [],
       {"compteurs": [["sc002", "samurai", 4]], "en_jeu": ["sc002"]},
       main_exclusive=["sc002", "01089"], payer_avec=["01089"], jouer=["sc002"]),
    _c("sc002 Shugorei Action : incliner + retirer 2 compteurs de CETTE carte -> piocher 1 carte (forme heros)",
       "« Exhaust this card and remove 2 samurai counters from it -> draw 1 card » : 4 -> 2 compteurs, carte inclinee, main 0 -> 1",
       [HEROS, "Puzzle.EmptyHand()", "Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01089', '01089', '01089')",
        "Puzzle.PutIntoPlay('sc002', under_control=True)"],
       ["Puzzle.Action('sc002', 'Action', 0)"],
       {"compteurs": [["sc002", "samurai", 2]], "exhausted": ["sc002"], "taille_main": 1, "taille_deck_joueur": 2}),
    _c("sc002 Shugorei Action : « Action » et non « Hero Action » : jouable aussi en forme ALTER-EGO",
       "forme alter-ego (Peter Parker) : meme resultat (2 compteurs, carte inclinee, 1 carte piochee)",
       ["Puzzle.EmptyHand()", "Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01089', '01089', '01089')",
        "Puzzle.PutIntoPlay('sc002', under_control=True)"],
       ["Puzzle.Action('sc002', 'Action', 0)"],
       {"compteurs": [["sc002", "samurai", 2]], "exhausted": ["sc002"], "taille_main": 1, "forme": "AlterEgo"}),
    _c("sc002 Shugorei : TEMOIN D'EPUISEMENT, deux usages (4 compteurs) puis la carte QUITTE le jeu (Uses) : 2 cartes piochees",
       "usage 1 : 4 -> 2 ; la carte se redresse ; usage 2 : 2 -> 0, dernier compteur retire -> defaussee ; main 0 -> 2",
       [HEROS, "Puzzle.EmptyHand()", "Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01089', '01089', '01089', '01089')",
        "Puzzle.PutIntoPlay('sc002', under_control=True)"],
       ["Puzzle.Action('sc002', 'Action', 0)", "Puzzle.Ready('sc002')", "Puzzle.Action('sc002', 'Action', 0)"],
       {"hors_jeu": ["sc002"], "taille_main": 2, "taille_deck_joueur": 2}),
    _c("sc002 Shugorei : « Exhaust this card » : une fois inclinee, plus d'Action proposee dans le meme round",
       "le cout d'inclinaison est le seul frein par round ; 0 action disponible apres un usage",
       [HEROS, "Puzzle.PutIntoPlay('sc002', under_control=True)"], ["Puzzle.Action('sc002', 'Action', 0)"],
       {"carte": "sc002", "type": "Action", "nombre": 0}, verifier="sc_actions_disponibles"),
    _c("sc002 Shugorei : Max 1 per player, une copie en jeu -> la 2e n'est PAS jouable",
       "« Max 1 per player » (MaxPerUnit) : la copie en main est refusee tant qu'une autre est en jeu",
       [HEROS, "Puzzle.CreateHandCards('sc002')", "Puzzle.PutIntoPlay('sc002', under_control=True)"], [],
       {"carte": "sc002", "jouable": False, "en_jeu": 1},
       main=["01089", "01089"], verifier="max_par_joueur_jouable"),
    _c("sc002 Shugorei : TEMOIN du Max 1, sans copie en jeu la carte est jouable",
       "contre-cas : c'est bien la copie en jeu qui bloque",
       [HEROS, "Puzzle.CreateHandCards('sc002')"], [],
       {"carte": "sc002", "jouable": True, "en_jeu": 0},
       main=["01089", "01089"], verifier="max_par_joueur_jouable"),
    _c("sc002 Shugorei avec JENNIKA : jouer une Dual Bushido/Kuji-Kiri donne Ninja Senpai pour LES DEUX classes (+2/+2/+2)",
       "deux classes Shinobi = deux Interruptions de tj001a",
       [JHEROS], [],
       {"attributs": SENPAI_DEUX_CLASSES, "en_jeu": ["sc002"]},
       heros="jennika", main_exclusive=["sc002", "01089"], payer_avec=["01089"], jouer=["sc002"]),
]

# ========================================================================= sc003 Omawari
CAS += [
    _c("sc003 Omawari : Hero Action, un WEAPON s'incline -> le HEROS est camoufle (Cloaked) ET recoit une carte Tough",
       "« Exhaust a WEAPON upgrade you control -> cloak your hero and give them a tough status card » : les DEUX statuts sur 01001a, "
       "01046 incline, Omawari en defausse",
       [HEROS, ARME], [],
       {"statuts": [["01001a", "Cloaked"], ["01001a", "Tough"]], "exhausted": ["01046"], "defausse": ["sc003"]},
       main_exclusive=["sc003", "01090"], payer_avec=["01090"], jouer=["sc003"]),
    _c("sc003 Omawari : SANS amelioration WEAPON la carte n'est PAS jouable (reste en main, aucun statut)",
       "cout impayable : pas de Cloaked, pas de Tough",
       [HEROS], [],
       {"statuts_absents": [["01001a", "Cloaked"], ["01001a", "Tough"]], "en_main": ["sc003"]},
       main_exclusive=["sc003", "01090"], payer_avec=["01090"], jouer=["sc003"]),
    _c("sc003 Omawari : un heros DEJA camoufle ne recoit pas une 2e carte Cloaked (un seul par personnage) mais recoit Tough",
       "« Normally characters can only have one Cloaked status card » : exactement 1 Cloaked apres jeu, Tough pose quand meme",
       [HEROS, ARME, "Puzzle.Cloak('01001a')"], [],
       {"statuts": [["01001a", "Cloaked"], ["01001a", "Tough"]], "exhausted": ["01046"], "defausse": ["sc003"]},
       main_exclusive=["sc003", "01090"], payer_avec=["01090"], jouer=["sc003"], verifier="sc_un_seul_cloaked"),
    _c("sc003 Omawari : « Hero Action » : en forme ALTER-EGO la carte n'est pas jouable (reste en main)",
       "Peter Parker : pas de Hero Action ; le WEAPON reste redresse",
       [ARME], [],
       {"statuts_absents": [["01001b", "Cloaked"]], "en_main": ["sc003"], "pret": ["01046"]},
       main_exclusive=["sc003", "01090"], payer_avec=["01090"], jouer=["sc003"]),
    _c("sc003 Omawari avec JENNIKA : jouer une Dual Bushido/Ninjutsu donne Ninja Senpai pour LES DEUX classes (+2/+2/+2)",
       "deux classes Shinobi = deux Interruptions de tj001a ; Jennika est aussi camouflee et tenace",
       [JHEROS, ARME], [],
       {"attributs": SENPAI_DEUX_CLASSES, "statuts": [["tj001a", "Cloaked"], ["tj001a", "Tough"]], "defausse": ["sc003"]},
       heros="jennika", main_exclusive=["sc003", "01090"], payer_avec=["01090"], jouer=["sc003"]),
]

# ========================================================================= sc004 Kuragari
CAS += [
    _c("sc004 Kuragari : entre en jeu avec 3 compteurs samurai (Uses), payee par Energy (YY)",
       "« Uses (3 samurai counters) » : base native `desc.Uses = \"3,samurai\"`",
       [HEROS], [],
       {"compteurs": [["sc004", "samurai", 3]], "en_jeu": ["sc004"]},
       main_exclusive=["sc004", "01088"], payer_avec=["01088"], jouer=["sc004"]),
    _c("sc004 Kuragari Action : incliner + retirer 3 compteurs -> le heros est CAMOUFLE et REDRESSE ; la carte quitte le jeu (Uses)",
       "heros incline au depart : apres l'Action il est pret et porte Cloaked ; les 3 compteurs partis, Kuragari est defaussee "
       "(UNE seule utilisation)",
       [HEROS, "Puzzle.Exhaust('01001a')", "Puzzle.PutIntoPlay('sc004', under_control=True)"],
       ["Puzzle.Action('sc004', 'Action', 0)"],
       {"statuts": [["01001a", "Cloaked"]], "pret": ["01001a"], "hors_jeu": ["sc004"]}),
    _c("sc004 Kuragari : TEMOIN, sans l'Action le heros reste incline et sans Cloaked",
       "meme position sans declencher : prouve que c'est bien l'Action qui redresse et camoufle",
       [HEROS, "Puzzle.Exhaust('01001a')", "Puzzle.PutIntoPlay('sc004', under_control=True)"], [],
       {"statuts_absents": [["01001a", "Cloaked"]], "exhausted": ["01001a"], "en_jeu": ["sc004"],
        "compteurs": [["sc004", "samurai", 3]]}),
    _c("sc004 Kuragari : TEMOIN D'EPUISEMENT, avec 2 compteurs seulement l'Action n'est PAS proposee (il en faut 3)",
       "le cout « remove 3 samurai counters from it » est impayable avec 2",
       [HEROS, "Puzzle.PutIntoPlay('sc004', under_control=True)", "Puzzle.Counter('sc004', 'samurai', -1)"], [],
       {"carte": "sc004", "type": "Action", "nombre": 0}, verifier="sc_actions_disponibles"),
    _c("sc004 Kuragari : avec 3 compteurs l'Action EST proposee (temoin du cas precedent)",
       "1 action disponible avant usage",
       [HEROS, "Puzzle.PutIntoPlay('sc004', under_control=True)"], [],
       {"carte": "sc004", "type": "Action", "nombre": 1}, verifier="sc_actions_disponibles"),
    _c("sc004 Kuragari : un heros DEJA camoufle ne recoit pas une 2e carte Cloaked, mais est redresse",
       "un seul Cloaked par personnage : exactement 1 apres l'Action ; le heros incline est pret",
       [HEROS, "Puzzle.Exhaust('01001a')", "Puzzle.Cloak('01001a')", "Puzzle.PutIntoPlay('sc004', under_control=True)"],
       ["Puzzle.Action('sc004', 'Action', 0)"],
       {"statuts": [["01001a", "Cloaked"]], "pret": ["01001a"], "hors_jeu": ["sc004"]}, verifier="sc_un_seul_cloaked"),
    _c("sc004 Kuragari (PROVISOIRE Q-D1) : « Action » en forme ALTER-EGO : l'identite est camouflee et redressee",
       "lecture provisoire : « your hero » = l'identite du joueur quand elle est en forme alter-ego ; a confirmer (Q-D1)",
       ["Puzzle.Exhaust('01001b')", "Puzzle.PutIntoPlay('sc004', under_control=True)"],
       ["Puzzle.Action('sc004', 'Action', 0)"],
       {"statuts": [["01001b", "Cloaked"]], "pret": ["01001b"], "hors_jeu": ["sc004"]}),
    _c("sc004 Kuragari avec JENNIKA : jouer une Dual Bushido/Ninjutsu donne Ninja Senpai pour LES DEUX classes (+2/+2/+2)",
       "deux classes Shinobi = deux Interruptions de tj001a",
       [JHEROS], [],
       {"attributs": SENPAI_DEUX_CLASSES, "en_jeu": ["sc004"]},
       heros="jennika", main_exclusive=["sc004", "01088"], payer_avec=["01088"], jouer=["sc004"]),
]

# ========================================================================= sc005 Yoi-Dachi
ATTAQUE_SANS_DEFENSE = ["Puzzle.Exhaust('01001a')"]
CAS += [
    _c("sc005 Yoi-Dachi : entre en jeu avec 3 compteurs samurai (Uses), payee par Energy (YY)",
       "« Uses (3 samurai counters) » : base native `desc.Uses = \"3,samurai\"`",
       [HEROS], [],
       {"compteurs": [["sc005", "samurai", 3]], "en_jeu": ["sc005"]},
       main_exclusive=["sc005", "01088"], payer_avec=["01088"], jouer=["sc005"]),
    _c("sc005 Yoi-Dachi Response : Rhino attaque le heros (incline : pas de defense), degats subis -> Rhino est HEBETE et -1 compteur",
       "« After you take damage from an enemy attack, remove 1 samurai counter from here -> daze that enemy » : ATQ 2 sans defense = "
       "2 degats, Rhino (l'attaquant) porte Dazed, la carte garde 2 compteurs",
       [HEROS, "Puzzle.PutIntoPlay('sc005', under_control=True)"] + ATTAQUE_SANS_DEFENSE, ["Puzzle.Attack('01094')"],
       {"degats_identite": 2, "statuts": [["01094", "Dazed"]], "compteurs": [["sc005", "samurai", 2]]},
       main_exclusive=["01090"]),
    _c("sc005 Yoi-Dachi : TEMOIN, sans Yoi-Dachi en jeu Rhino n'est pas hebete",
       "meme attaque sans la carte : le heros est blesse, aucun Dazed",
       [HEROS] + ATTAQUE_SANS_DEFENSE, ["Puzzle.Attack('01094')"],
       {"degats_identite": 2, "statuts_absents": [["01094", "Dazed"]]},
       main_exclusive=["01090"]),
    _c("sc005 Yoi-Dachi : « Response » (et non Hero Response) : aussi en forme ALTER-EGO",
       "Peter Parker incline subit l'attaque de Rhino : Rhino est hebete, 2 compteurs restent",
       ["Puzzle.PutIntoPlay('sc005', under_control=True)", "Puzzle.Exhaust('01001b')"], ["Puzzle.Attack('01094')"],
       {"degats_identite": 2, "statuts": [["01094", "Dazed"]], "compteurs": [["sc005", "samurai", 2]]},
       main_exclusive=["01090"]),
    _c("sc005 Yoi-Dachi : AUCUN degat subi (le heros est Tenace, la carte Tough absorbe) -> pas de Response, compteurs intacts",
       "« After you TAKE DAMAGE » : sans degat, rien ne part (Rhino pas hebete, 3 compteurs)",
       [HEROS, "Puzzle.PutIntoPlay('sc005', under_control=True)", "Puzzle.Tough('01001a')"] + ATTAQUE_SANS_DEFENSE,
       ["Puzzle.Attack('01094')"],
       {"degats_identite": 0, "statuts_absents": [["01094", "Dazed"]], "compteurs": [["sc005", "samurai", 3]]},
       main_exclusive=["01090"]),
    _c("sc005 Yoi-Dachi : un degat qui ne vient PAS d'une attaque ennemie (Puzzle.Damage) ne declenche rien",
       "« from an ENEMY ATTACK » : degats directs hors attaque -> Rhino n'est pas hebete, 3 compteurs",
       [HEROS, "Puzzle.PutIntoPlay('sc005', under_control=True)"], ["Puzzle.Damage('01001a', 2)"],
       {"degats_identite": 2, "statuts_absents": [["01094", "Dazed"]], "compteurs": [["sc005", "samurai", 3]]},
       main_exclusive=["01090"]),
    _c("sc005 Yoi-Dachi : « After YOU take damage » : l'attaque d'un sbire sur un ALLIE ne declenche rien",
       "Jessica Jones (allie) est attaquee par Hydra Mercenary et subit des degats : le joueur n'en subit pas ; pas de Dazed",
       [HEROS, "Puzzle.PutIntoPlay('sc005', under_control=True)", "Puzzle.PutIntoPlay('01059', under_control=True)",
        "Puzzle.PutIntoPlay('01101')", "Puzzle.Exhaust('01059')"],
       ["Puzzle.Attack('01101', defender='01059')"],
       {"degats_identite": 0, "statuts_absents": [["01101", "Dazed"]], "compteurs": [["sc005", "samurai", 3]]},
       main_exclusive=["01090"]),
    _c("sc005 Yoi-Dachi : Rhino DEJA hebete attaque avec ATQ 2 - 2 = 0 : aucun degat subi -> pas de Response, compteurs intacts",
       "le Dazed de Rhino est consomme par SON attaque (ATQ 0) : « After you take damage » ne se produit pas ; 3 compteurs, "
       "et la carte d'etat Dazed est partie (consommee, pas remplacee)",
       [HEROS, "Puzzle.PutIntoPlay('sc005', under_control=True)", "Puzzle.Daze('01094')"] + ATTAQUE_SANS_DEFENSE,
       ["Puzzle.Attack('01094')"],
       {"degats_identite": 0, "statuts_absents": [["01094", "Dazed"]], "compteurs": [["sc005", "samurai", 3]]},
       main_exclusive=["01090"]),
    _c("sc005 Yoi-Dachi : TEMOIN D'EPUISEMENT, avec 1 SEUL compteur : la Response part (Rhino hebete) puis la carte QUITTE le jeu (Uses)",
       "dernier compteur retire -> Yoi-Dachi defaussee (Uses), mais le daze a bien eu lieu",
       [HEROS, "Puzzle.PutIntoPlay('sc005', under_control=True)", "Puzzle.Counter('sc005', 'samurai', -2)"]
       + ATTAQUE_SANS_DEFENSE, ["Puzzle.Attack('01094')"],
       {"degats_identite": 2, "statuts": [["01094", "Dazed"]], "hors_jeu": ["sc005"]},
       main_exclusive=["01090"]),
    _c("sc005 Yoi-Dachi : Max 1 per player, une copie en jeu -> la 2e n'est PAS jouable",
       "« Max 1 per player » (MaxPerUnit)",
       [HEROS, "Puzzle.CreateHandCards('sc005')", "Puzzle.PutIntoPlay('sc005', under_control=True)"], [],
       {"carte": "sc005", "jouable": False, "en_jeu": 1},
       main=["01088", "01088"], verifier="max_par_joueur_jouable"),
    _c("sc005 Yoi-Dachi avec JENNIKA : jouer une Dual Bushido/Taijutsu donne Ninja Senpai pour LES DEUX classes (+2/+2/+2)",
       "deux classes Shinobi = deux Interruptions de tj001a",
       [JHEROS], [],
       {"attributs": SENPAI_DEUX_CLASSES, "en_jeu": ["sc005"]},
       heros="jennika", main_exclusive=["sc005", "01088"], payer_avec=["01088"], jouer=["sc005"]),
]

# ========================================================================= sc006 Migatte
# Capitaine Marvel (DEF 1, 12 PV) defend contre Fin Fang Foom (ATQ 4) : 4 - 1 = 3 degats ; avec Migatte (+2 DEF) : 4 - 3 = 1.
CM = "Puzzle.ChangeForm('01010b')"
FOOM = "Puzzle.PutIntoPlay('ah016')"
DEFENDRE = ["Puzzle.Defend('01010a', 'ah016')"]
CAS += [
    _c("sc006 Migatte : +2 DEF pour cette attaque : Fin Fang Foom (ATQ 4) contre DEF 1 + 2 = 3 -> 1 degat (au lieu de 3), payee par Strength",
       "« When your hero defends against an attack, it gets +2 DEF for that attack » ; payee par une carte NON Shinobi (Strength) : "
       "le heros reste incline (il a defendu)",
       [CM, FOOM], DEFENDRE,
       {"degats_identite": 1, "defausse": ["sc006"], "exhausted": ["01010a"]},
       heros="captain_marvel", main_exclusive=["sc006", "01090"], payer_avec=["01090"]),
    _c("sc006 Migatte : TEMOIN, sans Migatte la meme defense subit 3 degats",
       "base du cas precedent : ATQ 4 - DEF 1 = 3",
       [CM, FOOM], DEFENDRE,
       {"degats_identite": 3, "exhausted": ["01010a"]},
       heros="captain_marvel", main_exclusive=["01090"]),
    _c("sc006 Migatte : payee AVEC UNE CARTE SHINOBI (Nendo, Dual) : +2 DEF ET le heros est REDRESSE",
       "« If you paid for this card with a Shinobi card, ready your hero » : Nendo (classe Shinobi) defaussee pour sa ressource R ; "
       "le heros, incline par sa defense, est pret ; 1 degat",
       [CM, FOOM], DEFENDRE,
       {"degats_identite": 1, "defausse": ["sc006", "sc001"], "pret": ["01010a"]},
       heros="captain_marvel", main_exclusive=["sc006", "sc001"], payer_avec=["sc001"]),
    _c("sc006 Migatte : payee avec une carte Shinobi a UNE SEULE classe (Decisive Strike tj004, Taijutsu) : le heros est redresse",
       "toute carte portant l'une des quatre classes compte, pas seulement une Dual",
       [CM, FOOM], DEFENDRE,
       {"degats_identite": 1, "defausse": ["sc006", "tj004"], "pret": ["01010a"]},
       heros="captain_marvel", main_exclusive=["sc006", "tj004"], payer_avec=["tj004"]),
    _c("sc006 Migatte : payee avec une carte NON Shinobi (Haymaker 01087, Basic) : +2 DEF mais le heros RESTE incline",
       "ni aspect ni Basic ne comptent pour « a Shinobi card »",
       [CM, FOOM], DEFENDRE,
       {"degats_identite": 1, "defausse": ["sc006", "01087"], "exhausted": ["01010a"]},
       heros="captain_marvel", main_exclusive=["sc006", "01087"], payer_avec=["01087"]),
    _c("sc006 Migatte : « Hero Interrupt » : un ALTER-EGO qui defend ne la propose pas (reste en main, ATQ 4 sans DEF = 4 degats)",
       "forme alter-ego (aucune DEF) : « When your HERO defends » ne part pas ; Migatte reste en main",
       [FOOM], ["Puzzle.Defend('01010b', 'ah016')"],
       {"degats_identite": 4, "en_main": ["sc006", "01090"]},
       heros="captain_marvel", main_exclusive=["sc006", "01090"]),
    _c("sc006 Migatte avec JENNIKA : jouer une Dual Bushido/Taijutsu donne Ninja Senpai pour LES DEUX classes (+2/+2/+2)",
       "deux classes Shinobi = deux Interruptions de tj001a ; la carte est jouee en defense",
       [JHEROS, FOOM], ["Puzzle.Defend('tj001a', 'ah016')"],
       {"attributs": SENPAI_DEUX_CLASSES, "defausse": ["sc006"]},
       heros="jennika", main_exclusive=["sc006", "01090"], payer_avec=["01090"]),
]

# ========================================================================= sc007 Mizuki
CAS += [
    _c("sc007 Mizuki : 2 menaces retirees d'une manigance qui n'en avait que 2 (la derniere) -> choix « Cloak » : le HEROS est camoufle",
       "« Remove 2 threat from a scheme. If this removes the last threat on that scheme, choose: • Cloak a friendly character » : "
       "menace 2 -> 0 sur le complot, Cloaked sur 01001a",
       [HEROS, f"Puzzle.SetThreat('{COMPLOT}', 2)"], [],
       {"menace": [[COMPLOT, 0]], "statuts": [["01001a", "Cloaked"]], "defausse": ["sc007"]},
       main_exclusive=["sc007", "01089"], payer_avec=["01089"], jouer=["sc007"], cibles=[COMPLOT, "01001a"],
       preferer_option="Cloak a friendly"),
    _c("sc007 Mizuki : une menace seulement (1 -> 0, c'est bien la derniere) : le choix part aussi",
       "« removes the last threat » : 1 menace retiree (le complot n'en avait qu'une) suffit",
       [HEROS, f"Puzzle.SetThreat('{COMPLOT}', 1)"], [],
       {"menace": [[COMPLOT, 0]], "statuts": [["01001a", "Cloaked"]]},
       main_exclusive=["sc007", "01089"], payer_avec=["01089"], jouer=["sc007"], cibles=[COMPLOT, "01001a"],
       preferer_option="Cloak a friendly"),
    _c("sc007 Mizuki : TEMOIN, 3 menaces -> 1 : ce n'est PAS la derniere, aucun choix, aucun camouflage",
       "le complot garde 1 menace : ni Cloak ni retour d'evenement (l'evenement en defausse reste en defausse)",
       [HEROS, f"Puzzle.SetThreat('{COMPLOT}', 3)", "Puzzle.EmptyPlayerDiscardPile()", "Puzzle.CreatePlayerDiscardPile('01087')"], [],
       {"menace": [[COMPLOT, 1]], "statuts_absents": [["01001a", "Cloaked"]], "absent_main": ["01087"], "defausse": ["sc007"]},
       main_exclusive=["sc007", "01089"], payer_avec=["01089"], jouer=["sc007"], cibles=[COMPLOT],
       preferer_option="Return an event"),
    _c("sc007 Mizuki : 2e branche, derniere menace -> un EVENEMENT de la defausse revient en MAIN (Haymaker 01087)",
       "« Return an event from your discard pile to your hand » : 01087 quitte la defausse pour la main ; Mizuki est en defausse",
       [HEROS, f"Puzzle.SetThreat('{COMPLOT}', 2)", "Puzzle.EmptyPlayerDiscardPile()", "Puzzle.CreatePlayerDiscardPile('01087')"], [],
       {"menace": [[COMPLOT, 0]], "en_main": ["01087"], "statuts_absents": [["01001a", "Cloaked"]], "defausse": ["sc007"]},
       main_exclusive=["sc007", "01089"], payer_avec=["01089"], jouer=["sc007"], cibles=[COMPLOT],
       preferer_option="Return an event"),
    _c("sc007 Mizuki : 2e branche : une AMELIORATION de la defausse (Armored Vest 01081) n'est PAS un evenement : elle reste en defausse",
       "seul un evenement peut revenir ; la branche « Return » n'a pas de cible, la carte prend l'autre branche (Cloak)",
       [HEROS, f"Puzzle.SetThreat('{COMPLOT}', 2)", "Puzzle.EmptyPlayerDiscardPile()", "Puzzle.CreatePlayerDiscardPile('01081')"], [],
       {"menace": [[COMPLOT, 0]], "absent_main": ["01081"], "defausse": ["01081", "sc007"]},
       main_exclusive=["sc007", "01089"], payer_avec=["01089"], jouer=["sc007"], cibles=[COMPLOT, "01001a"],
       preferer_option="Return an event"),
    _c("sc007 Mizuki : « a FRIENDLY character » : un ALLIE (Jessica Jones) peut etre camoufle, pas besoin du heros",
       "branche Cloak, cible = l'allie 01059",
       [HEROS, f"Puzzle.SetThreat('{COMPLOT}', 2)", "Puzzle.PutIntoPlay('01059', under_control=True)"], [],
       {"menace": [[COMPLOT, 0]], "statuts": [["01059", "Cloaked"]], "statuts_absents": [["01001a", "Cloaked"]]},
       main_exclusive=["sc007", "01089"], payer_avec=["01089"], jouer=["sc007"], cibles=[COMPLOT, "01059"],
       preferer_option="Cloak a friendly"),
    _c("sc007 Mizuki : « Hero Action » : en forme ALTER-EGO la carte n'est pas jouable (reste en main, menace intacte)",
       "Peter Parker : pas de Hero Action",
       [f"Puzzle.SetThreat('{COMPLOT}', 2)"], [],
       {"menace": [[COMPLOT, 2]], "en_main": ["sc007"]},
       main_exclusive=["sc007", "01089"], payer_avec=["01089"], jouer=["sc007"], cibles=[COMPLOT]),
    _c("sc007 Mizuki avec JENNIKA : jouer une Dual Kuji-Kiri/Ninjutsu donne Ninja Senpai pour LES DEUX classes (+2/+2/+2)",
       "deux classes Shinobi = deux Interruptions de tj001a",
       [JHEROS, f"Puzzle.SetThreat('{COMPLOT}', 4)"], [],
       {"attributs": SENPAI_DEUX_CLASSES, "menace": [[COMPLOT, 2]], "defausse": ["sc007"]},
       heros="jennika", main_exclusive=["sc007", "01089"], payer_avec=["01089"], jouer=["sc007"], cibles=[COMPLOT]),
]

# ========================================================================= sc008 Naito Dansa
# Deck rencontre : CreateEncounterDeck ajoute AU-DESSUS (la derniere carte creee est le dessus).
DECK_ATTACHEMENT = "Puzzle.CreateEncounterDeck('01100', '01105', '01105')"      # dessus : 01105, 01105, puis 01100
DECK_MANIGANCE = "Puzzle.CreateEncounterDeck('01107', '01105')"                  # dessus : 01105, puis 01107
CAS += [
    _c("sc008 Naito Dansa : defausse jusqu'a un ATTACHEMENT (01100), le revele, camoufle 2 amis ET hebete 2 ennemis",
       "deck : 01105, 01105, puis l'attachement 01100 : les 2 traitrises sont defaussees, 01100 revele (s'attache a Rhino) ; "
       "Cloaked sur le heros et l'allie, Dazed sur Rhino et le sbire",
       [HEROS, DECK_ATTACHEMENT, "Puzzle.PutIntoPlay('01059', under_control=True)", "Puzzle.PutIntoPlay('01101')"], [],
       {"en_jeu": ["01100"], "statuts": [["01001a", "Cloaked"], ["01059", "Cloaked"], ["01094", "Dazed"], ["01101", "Dazed"]],
        "defausse_rencontre": ["01105"], "defausse": ["sc008"]},
       main_exclusive=["sc008", "01088"], payer_avec=["01088"], jouer=["sc008"], accepter_choix=True),
    _c("sc008 Naito Dansa : defausse jusqu'a une MANIGANCE ANNEXE (01107), la revele (entre en jeu)",
       "deck : 01105 puis 01107 : la manigance annexe est revelee (en jeu avec sa menace) avant le camouflage",
       [HEROS, DECK_MANIGANCE], [],
       {"en_jeu": ["01107"], "statuts": [["01001a", "Cloaked"], ["01094", "Dazed"]], "defausse_rencontre": ["01105"],
        "defausse": ["sc008"]},
       main_exclusive=["sc008", "01088"], payer_avec=["01088"], jouer=["sc008"], accepter_choix=True),
    _c("sc008 Naito Dansa : aucun attachement ni manigance annexe dans le deck : cout impaye, carte NON jouee (reste en main), ni Cloak ni Daze",
       "deck de traitrises seulement : tout est defausse, rien n'est revele, aucun effet",
       [HEROS], [],
       {"en_main": ["sc008"], "statuts_absents": [["01001a", "Cloaked"], ["01094", "Dazed"]]},
       main_exclusive=["sc008", "01088"], payer_avec=["01088"], jouer=["sc008"], accepter_choix=True),
    _c("sc008 Naito Dansa : « UP TO 2 » : on peut en choisir MOINS (le heros seulement camoufle, Rhino seul hebete ; allie et sbire intacts)",
       "cibles imposees : 01001a et 01094 ; l'allie 01059 et le sbire 01101 ne recoivent rien",
       [HEROS, DECK_ATTACHEMENT, "Puzzle.PutIntoPlay('01059', under_control=True)", "Puzzle.PutIntoPlay('01101')"], [],
       {"statuts": [["01001a", "Cloaked"], ["01094", "Dazed"]],
        "statuts_absents": [["01059", "Cloaked"], ["01101", "Dazed"]], "defausse": ["sc008"]},
       main_exclusive=["sc008", "01088"], payer_avec=["01088"], jouer=["sc008"], cibles=["01001a", "01094"]),
    _c("sc008 Naito Dansa : trois amis et trois ennemis : EXACTEMENT 2 camoufles et 2 hebetes (jamais 3)",
       "« up to 2 » est un plafond : heros + 2 allies, Rhino + 2 sbires, au plus 2 de chaque",
       [HEROS, DECK_ATTACHEMENT, "Puzzle.PutIntoPlay('01059', under_control=True)", "Puzzle.PutIntoPlay('01002', under_control=True)",
        "Puzzle.PutIntoPlay('01101')", "Puzzle.PutIntoPlay('01103')"], [],
       {"parmi_cloaked": [["01001a", "01059", "01002"], 2], "parmi_dazed": [["01094", "01101", "01103"], 2],
        "defausse": ["sc008"]},
       main_exclusive=["sc008", "01088"], payer_avec=["01088"], jouer=["sc008"], accepter_choix=True,
       verifier="sc_statuts_parmi"),
    _c("sc008 Naito Dansa : « Hero Action » : en forme ALTER-EGO la carte n'est pas jouable (deck de rencontre intact, reste en main)",
       "Peter Parker : pas de Hero Action",
       [DECK_ATTACHEMENT], [],
       {"en_main": ["sc008"], "hors_jeu": ["01100"], "statuts_absents": [["01094", "Dazed"]]},
       main_exclusive=["sc008", "01088"], payer_avec=["01088"], jouer=["sc008"]),
    _c("sc008 Naito Dansa avec JENNIKA : jouer une Dual Kuji-Kiri/Ninjutsu donne Ninja Senpai pour LES DEUX classes (+2/+2/+2)",
       "deux classes Shinobi = deux Interruptions de tj001a",
       [JHEROS, DECK_ATTACHEMENT], [],
       {"attributs": SENPAI_DEUX_CLASSES, "en_jeu": ["01100"], "defausse": ["sc008"]},
       heros="jennika", main_exclusive=["sc008", "01088"], payer_avec=["01088"], jouer=["sc008"], accepter_choix=True),
]

# ========================================================================= sc009 Yomi
CAS += [
    _c("sc009 Yomi : une carte de la DEFAUSSE rencontre est remise AU-DESSUS du deck, puis 2 menaces sont retirees d'une manigance",
       "« Choose 1 card from the encounter discard pile and put it on top of the encounter deck -> remove 2 threat from a scheme » : "
       "01107 passe de la defausse au dessus du deck ; menace du complot 5 -> 3",
       [HEROS, f"Puzzle.SetThreat('{COMPLOT}', 5)", "Puzzle.EmptyEncounterDiscardPile()", "Puzzle.CreateEncounterDiscardPile('01107')"], [],
       {"dessus": "01107", "taille_defausse": 0, "taille_deck": 9, "menace": [[COMPLOT, 3]], "defausse": ["sc009"]},
       main_exclusive=["sc009", "01088"], payer_avec=["01088"], jouer=["sc009"], cibles=[COMPLOT], verifier="sc_dessus_rencontre"),
    _c("sc009 Yomi : DEUX cartes en defausse : c'est LA CHOISIE (01107) qui va au-dessus, l'autre (01105) reste en defausse",
       "le joueur choisit : cibles = 01107 ; la defausse garde 1 carte",
       [HEROS, f"Puzzle.SetThreat('{COMPLOT}', 5)", "Puzzle.EmptyEncounterDiscardPile()",
        "Puzzle.CreateEncounterDiscardPile('01105', '01107')"], [],
       {"dessus": "01107", "taille_defausse": 1, "taille_deck": 9, "menace": [[COMPLOT, 3]]},
       main_exclusive=["sc009", "01088"], payer_avec=["01088"], jouer=["sc009"], cibles=["01107", COMPLOT],
       verifier="sc_dessus_rencontre"),
    _c("sc009 Yomi : defausse rencontre VIDE : le cout est impayable, la carte n'est PAS jouee (reste en main, menace intacte)",
       "« Choose 1 card from the encounter discard pile » : sans carte a choisir, rien ne part",
       [HEROS, f"Puzzle.SetThreat('{COMPLOT}', 5)", "Puzzle.EmptyEncounterDiscardPile()"], [],
       {"menace": [[COMPLOT, 5]], "en_main": ["sc009"]},
       main_exclusive=["sc009", "01088"], payer_avec=["01088"], jouer=["sc009"], cibles=[COMPLOT]),
    _c("sc009 Yomi : « from A scheme » : la manigance visee peut etre ANNEXE (Breakin' & Takin' 01107 en jeu : 3 -> 1)",
       "cible = la manigance annexe ; le complot principal n'est pas touche",
       [HEROS, f"Puzzle.SetThreat('{COMPLOT}', 5)", "Puzzle.Reveal('01107')", "Puzzle.EmptyEncounterDiscardPile()",
        "Puzzle.CreateEncounterDiscardPile('01105')"], [],
       {"menace": [[COMPLOT, 5], ["01107", 1]], "defausse": ["sc009"]},
       main_exclusive=["sc009", "01088"], payer_avec=["01088"], jouer=["sc009"], cibles=["01107"]),
    _c("sc009 Yomi : « Hero Action » : en forme ALTER-EGO la carte n'est pas jouable (defausse intacte, reste en main)",
       "Peter Parker : pas de Hero Action",
       [f"Puzzle.SetThreat('{COMPLOT}', 5)", "Puzzle.EmptyEncounterDiscardPile()", "Puzzle.CreateEncounterDiscardPile('01105')"], [],
       {"menace": [[COMPLOT, 5]], "en_main": ["sc009"], "defausse_rencontre": ["01105"]},
       main_exclusive=["sc009", "01088"], payer_avec=["01088"], jouer=["sc009"], cibles=[COMPLOT]),
    _c("sc009 Yomi avec JENNIKA : jouer une Dual Kuji-Kiri/Taijutsu donne Ninja Senpai pour LES DEUX classes (+2/+2/+2)",
       "deux classes Shinobi = deux Interruptions de tj001a",
       [JHEROS, f"Puzzle.SetThreat('{COMPLOT}', 5)", "Puzzle.EmptyEncounterDiscardPile()", "Puzzle.CreateEncounterDiscardPile('01107')"], [],
       {"attributs": SENPAI_DEUX_CLASSES, "menace": [[COMPLOT, 3]], "defausse": ["sc009"]},
       heros="jennika", main_exclusive=["sc009", "01088"], payer_avec=["01088"], jouer=["sc009"], cibles=[COMPLOT]),
]

# ========================================================================= sc010 Kusuri
CAS += [
    _c("sc010 Kusuri Action : incliner + defausser un evenement ATTACK de la main (Haymaker) -> 2 degats soignes sur le heros (3 -> 1)",
       "« Exhaust this card and discard an ATTACK event from your hand -> heal 2 damage from a friendly character » : "
       "Kusuri inclinee, Haymaker defaussee, le heros passe de 3 a 1 degat",
       [HEROS, "Puzzle.PutIntoPlay('sc010', under_control=True)", "Puzzle.Damage('01001a', 3)"],
       ["Puzzle.Action('sc010', 'Action', 0)"],
       {"degats_identite": 1, "exhausted": ["sc010"], "defausse": ["01087"]},
       main_exclusive=["01087"], cibles=["01001a"]),
    _c("sc010 Kusuri : « Action » : aussi en forme ALTER-EGO",
       "Peter Parker blesse de 3 : meme soin de 2",
       ["Puzzle.PutIntoPlay('sc010', under_control=True)", "Puzzle.Damage('01001b', 3)"],
       ["Puzzle.Action('sc010', 'Action', 0)"],
       {"degats_identite": 1, "exhausted": ["sc010"], "defausse": ["01087"]},
       main_exclusive=["01087"], cibles=["01001b"]),
    _c("sc010 Kusuri : « a FRIENDLY character » : on peut soigner un ALLIE (Jessica Jones 3 PV, blessee de 2 -> 0)",
       "cible = l'allie ; le heros blesse n'est pas soigne",
       [HEROS, "Puzzle.PutIntoPlay('sc010', under_control=True)", "Puzzle.PutIntoPlay('01059', under_control=True)",
        "Puzzle.Damage('01059', 2)", "Puzzle.Damage('01001a', 3)"],
       ["Puzzle.Action('sc010', 'Action', 0)"],
       {"degats": [["01059", 0]], "degats_identite": 3, "exhausted": ["sc010"], "defausse": ["01087"]},
       main_exclusive=["01087"], cibles=["01059"]),
    _c("sc010 Kusuri : un seul degat sur le heros : le soin s'arrete a 0 (jamais de PV en trop)",
       "2 soignes sur 1 degat : 0 degat",
       [HEROS, "Puzzle.PutIntoPlay('sc010', under_control=True)", "Puzzle.Damage('01001a', 1)"],
       ["Puzzle.Action('sc010', 'Action', 0)"],
       {"degats_identite": 0, "defausse": ["01087"]},
       main_exclusive=["01087"], cibles=["01001a"]),
    _c("sc010 Kusuri : un evenement NON ATTACK en main (Backflip 01003, DEFENSE) ne paie pas le cout : action non proposee",
       "« an ATTACK event » : le trait compte",
       [HEROS, "Puzzle.PutIntoPlay('sc010', under_control=True)", "Puzzle.Damage('01001a', 3)"], [],
       {"carte": "sc010", "type": "Action", "nombre": 0},
       main_exclusive=["01003", "01088"], verifier="sc_actions_disponibles"),
    _c("sc010 Kusuri : avec un evenement ATTACK en main l'action EST proposee (temoin du cas precedent)",
       "1 action disponible",
       [HEROS, "Puzzle.PutIntoPlay('sc010', under_control=True)", "Puzzle.Damage('01001a', 3)"], [],
       {"carte": "sc010", "type": "Action", "nombre": 1},
       main_exclusive=["01087", "01088"], verifier="sc_actions_disponibles"),
    _c("sc010 Kusuri : TEMOIN D'EPUISEMENT, deux evenements ATTACK en main mais Kusuri inclinee : une seule defausse par round",
       "apres un usage la carte est inclinee : 0 action ; la 2e Haymaker reste en main",
       [HEROS, "Puzzle.PutIntoPlay('sc010', under_control=True)", "Puzzle.Damage('01001a', 4)"],
       ["Puzzle.Action('sc010', 'Action', 0)"],
       {"degats_identite": 2, "exhausted": ["sc010"], "taille_main": 1, "en_main": ["01087"]},
       main_exclusive=["01087", "01087"], cibles=["01001a"]),
    _c("sc010 Kusuri : Max 1 per player, une copie en jeu -> la 2e n'est PAS jouable",
       "« Max 1 per player » (MaxPerUnit)",
       [HEROS, "Puzzle.CreateHandCards('sc010')", "Puzzle.PutIntoPlay('sc010', under_control=True)"], [],
       {"carte": "sc010", "jouable": False, "en_jeu": 1},
       main=["01090", "01090"], verifier="max_par_joueur_jouable"),
    _c("sc010 Kusuri avec JENNIKA : jouer une Dual Kuji-Kiri/Taijutsu donne Ninja Senpai pour LES DEUX classes (+2/+2/+2)",
       "deux classes Shinobi = deux Interruptions de tj001a",
       [JHEROS], [],
       {"attributs": SENPAI_DEUX_CLASSES, "en_jeu": ["sc010"]},
       heros="jennika", main_exclusive=["sc010", "01090"], payer_avec=["01090"], jouer=["sc010"]),
]

# ========================================================================= sc011 Kenbu
TROIS_ENNEMIS = ["Puzzle.PutIntoPlay('01110')", "Puzzle.PutIntoPlay('01103')"]
CAS += [
    _c("sc011 Kenbu : le Cloaked du heros est DEFAUSSE (cout) -> 1 degat a Rhino ET aux deux sbires, chacun est HEBETE",
       "« Discard a cloaked status card from your hero -> deal 1 damage to up to 3 enemies. Daze each enemy damaged this way » : "
       "le heros perd Cloaked ; Rhino, Hydra Bomber et Shocker prennent 1 degat et portent Dazed",
       [HEROS, "Puzzle.Cloak('01001a')"] + TROIS_ENNEMIS, [],
       {"degats": [["01094", 1], ["01110", 1], ["01103", 1]],
        "statuts": [["01094", "Dazed"], ["01110", "Dazed"], ["01103", "Dazed"]],
        "statuts_absents": [["01001a", "Cloaked"]], "defausse": ["sc011"]},
       main_exclusive=["sc011", "01089"], payer_avec=["01089"], jouer=["sc011"], cibles=["01094", "01110", "01103"]),
    _c("sc011 Kenbu : le heros n'est PAS camoufle -> la carte n'est pas jouable (reste en main, aucun degat)",
       "le cout « Discard a cloaked status card from your hero » est impayable",
       [HEROS] + TROIS_ENNEMIS, [],
       {"degats": [["01094", 0], ["01110", 0]], "statuts_absents": [["01094", "Dazed"]], "en_main": ["sc011"]},
       main_exclusive=["sc011", "01089"], payer_avec=["01089"], jouer=["sc011"], cibles=["01094", "01110", "01103"]),
    _c("sc011 Kenbu : « UP TO 3 » : un seul ennemi choisi (Rhino) : lui seul est blesse et hebete",
       "cibles imposees = 01094 ; sbires intacts",
       [HEROS, "Puzzle.Cloak('01001a')"] + TROIS_ENNEMIS, [],
       {"degats": [["01094", 1], ["01110", 0], ["01103", 0]], "statuts": [["01094", "Dazed"]],
        "statuts_absents": [["01110", "Dazed"], ["01103", "Dazed"]], "defausse": ["sc011"]},
       main_exclusive=["sc011", "01089"], payer_avec=["01089"], jouer=["sc011"], cibles=["01094"]),
    _c("sc011 Kenbu : « Daze each enemy DAMAGED this way » : Rhino TENACE (la carte Tough absorbe) n'est pas blesse -> PAS hebete ; le sbire l'est",
       "Rhino : degats 0 et pas de Dazed ; Hydra Bomber : 1 degat et Dazed",
       [HEROS, "Puzzle.Cloak('01001a')", "Puzzle.Tough('01094')"] + TROIS_ENNEMIS, [],
       {"degats": [["01094", 0], ["01110", 1]], "statuts_absents": [["01094", "Dazed"]],
        "statuts": [["01110", "Dazed"]], "defausse": ["sc011"]},
       main_exclusive=["sc011", "01089"], payer_avec=["01089"], jouer=["sc011"], cibles=["01094", "01110"]),
    _c("sc011 Kenbu : un sbire a 1 PV est VAINCU par le degat : il quitte le jeu (pas de Dazed sur un ennemi vaincu), Rhino est hebete",
       "Hydra Bomber (2 PV) deja blesse de 1 : 1 degat = vaincu ; Rhino : 1 degat et Dazed",
       [HEROS, "Puzzle.Cloak('01001a')", "Puzzle.PutIntoPlay('01110')", "Puzzle.Damage('01110', 1)"], [],
       {"hors_jeu": ["01110"], "degats": [["01094", 1]], "statuts": [["01094", "Dazed"]], "defausse": ["sc011"]},
       main_exclusive=["sc011", "01089"], payer_avec=["01089"], jouer=["sc011"], cibles=["01094", "01110"]),
    _c("sc011 Kenbu : « Hero Action » : en forme ALTER-EGO la carte n'est pas jouable (reste en main)",
       "Peter Parker camoufle : pas de Hero Action ; le Cloaked reste",
       ["Puzzle.Cloak('01001b')"] + TROIS_ENNEMIS, [],
       {"degats": [["01094", 0]], "statuts": [["01001b", "Cloaked"]], "en_main": ["sc011"]},
       main_exclusive=["sc011", "01089"], payer_avec=["01089"], jouer=["sc011"], cibles=["01094"]),
    _c("sc011 Kenbu avec JENNIKA : jouer une Dual Ninjutsu/Taijutsu donne Ninja Senpai pour LES DEUX classes (+2/+2/+2)",
       "deux classes Shinobi = deux Interruptions de tj001a ; le Cloaked de Jennika est defausse",
       [JHEROS, "Puzzle.Cloak('tj001a')"], [],
       {"attributs": SENPAI_DEUX_CLASSES, "degats": [["01094", 1]], "statuts": [["01094", "Dazed"]],
        "statuts_absents": [["tj001a", "Cloaked"]], "defausse": ["sc011"]},
       heros="jennika", main_exclusive=["sc011", "01089"], payer_avec=["01089"], jouer=["sc011"], cibles=["01094"]),
]

# ========================================================================= sc012 Hitodama (PROVISOIRE : Q-D2, Hero Response sans declencheur lue comme Hero Action)
CAS += [
    _c("sc012 Hitodama (PROVISOIRE Q-D2) : payee avec un evenement THWART (Crisis Interdiction 01012) : 3 degats a Rhino ET le heros est camoufle",
       "« Deal 3 damage to an enemy. If you paid for this card with a THWART event, cloak your hero » : lecture provisoire en Hero Action",
       [HEROS], [],
       {"degats": [["01094", 3]], "statuts": [["01001a", "Cloaked"]], "defausse": ["sc012", "01012"]},
       main_exclusive=["sc012", "01012", "01089"], payer_avec=["01012", "01089"], jouer=["sc012"], cibles=["01094"]),
    _c("sc012 Hitodama (PROVISOIRE Q-D2) : payee avec un evenement ATTACK (Haymaker 01087) : 3 degats mais PAS de Cloaked",
       "seul un evenement THWART compte",
       [HEROS], [],
       {"degats": [["01094", 3]], "statuts_absents": [["01001a", "Cloaked"]], "defausse": ["sc012", "01087"]},
       main_exclusive=["sc012", "01087", "01089"], payer_avec=["01087", "01089"], jouer=["sc012"], cibles=["01094"]),
    _c("sc012 Hitodama (PROVISOIRE Q-D2) : payee par de simples ressources (Genius BB) : 3 degats, pas de Cloaked",
       "aucune carte THWART dans le paiement",
       [HEROS], [],
       {"degats": [["01094", 3]], "statuts_absents": [["01001a", "Cloaked"]], "defausse": ["sc012", "01089"]},
       main_exclusive=["sc012", "01089"], payer_avec=["01089"], jouer=["sc012"], cibles=["01094"]),
    _c("sc012 Hitodama (PROVISOIRE Q-D2) : forme ALTER-EGO : la carte n'est pas jouable (reste en main)",
       "lecture provisoire en Hero Action : Peter Parker ne la joue pas",
       [], [],
       {"degats": [["01094", 0]], "en_main": ["sc012"]},
       main_exclusive=["sc012", "01089"], payer_avec=["01089"], jouer=["sc012"], cibles=["01094"]),
    _c("sc012 Hitodama avec JENNIKA : jouer une Dual Ninjutsu/Taijutsu donne Ninja Senpai pour LES DEUX classes (+2/+2/+2)",
       "deux classes Shinobi = deux Interruptions de tj001a",
       [JHEROS], [],
       {"attributs": SENPAI_DEUX_CLASSES, "degats": [["01094", 3]], "defausse": ["sc012"]},
       heros="jennika", main_exclusive=["sc012", "01089"], payer_avec=["01089"], jouer=["sc012"], cibles=["01094"]),
]


VERIFICATIONS = r'''
def sc_un_seul_cloaked(monde, aides):
    """Le heros porte EXACTEMENT une carte Cloaked (jamais deux) ; le reste est delegue a etat_attendu."""
    identite = aides["identite"](monde)
    n = identite.cloaked
    if n != 1:
        return False, f"l'identite porte {n} carte(s) Cloaked (attendu exactement 1)"
    return etat_attendu(monde, aides)


def sc_un_seul_dazed(monde, aides):
    """Rhino porte EXACTEMENT une carte Dazed (jamais deux) ; le reste est delegue a etat_attendu."""
    rhino = aides["par_id"](monde, "01094")
    n = rhino.dazed
    if n != 1:
        return False, f"Rhino porte {n} carte(s) Dazed (attendu exactement 1)"
    return etat_attendu(monde, aides)


def sc_statuts_parmi(monde, aides):
    """`attendu.parmi_cloaked` / `parmi_dazed` : [[card_id...], n] = EXACTEMENT n de ces cartes portent le statut ;
    le reste (`defausse`...) est delegue a etat_attendu."""
    attendu = aides["cas"]["attendu"]
    soucis = []
    for cle, propriete in (("parmi_cloaked", "cloaked"), ("parmi_dazed", "dazed")):
        if cle not in attendu:
            continue
        ids, voulu = attendu[cle]
        porteurs = []
        for card_id in ids:
            face = aides["par_id"](monde, card_id)
            if face is not None and getattr(face, propriete) > 0:
                porteurs.append(card_id)
        if len(porteurs) != voulu:
            soucis.append(f"{cle} : {len(porteurs)} porteur(s) {porteurs} parmi {ids} (attendu exactement {voulu})")
    if soucis:
        return False, " ; ".join(soucis)
    reste = {k: v for k, v in attendu.items() if k not in ("parmi_cloaked", "parmi_dazed")}
    aides["cas"]["attendu"] = reste
    ok, msg = etat_attendu(monde, aides)
    aides["cas"]["attendu"] = attendu
    return ok, "exactement le bon nombre de porteurs ; " + msg


def sc_dessus_rencontre(monde, aides):
    """`attendu` : dessus (card_id de la carte du DESSUS du deck de rencontre), taille_deck, taille_defausse
    (defausse de rencontre) ; le reste est delegue a etat_attendu."""
    from game.operate.worlds import Worlds
    attendu = aides["cas"]["attendu"]
    deck = [getattr(f.paper, "card_id", None) for f in Worlds.GetEncounterDeckCards(monde) if f is not None]
    defausse = [getattr(f.paper, "card_id", None) for f in Worlds.GetEncounterDiscardPileCards(monde) if f is not None]
    soucis = []
    if deck[:1] != [attendu["dessus"]]:
        soucis.append(f"dessus du deck de rencontre = {deck[:1]} (attendu {attendu['dessus']}) ; deck = {deck[:4]}...")
    if "taille_deck" in attendu and len(deck) != attendu["taille_deck"]:
        soucis.append(f"deck de rencontre = {len(deck)} carte(s) (attendu {attendu['taille_deck']})")
    if "taille_defausse" in attendu and len(defausse) != attendu["taille_defausse"]:
        soucis.append(f"defausse de rencontre = {len(defausse)} carte(s) {defausse} (attendu {attendu['taille_defausse']})")
    if soucis:
        return False, " ; ".join(soucis)
    reste = {k: v for k, v in attendu.items() if k not in ("dessus", "taille_deck", "taille_defausse")}
    aides["cas"]["attendu"] = reste
    ok, msg = etat_attendu(monde, aides)
    aides["cas"]["attendu"] = attendu
    return ok, f"dessus = {attendu['dessus']}, deck {len(deck)}, defausse {len(defausse)} ; " + msg


def sc_classes(monde, aides):
    """`attendu` : carte (n'importe quelle zone), `oui` (classes que `IsClass` ET `CardFinder(card_class=...)` /
    `card_classes=[...]` doivent reconnaitre), `non` (classes refusees). Retrouve la carte par son card_id dans tout le monde."""
    from game.card.card_finder import CardFinder
    attendu = aides["cas"]["attendu"]
    face = None
    for objet in monde.object_manager.card_dict.values():
        f = getattr(objet, "face", None) or objet
        if getattr(getattr(f, "paper", None), "card_id", None) == attendu["carte"]:
            face = f
            break
    if face is None:
        return False, f"{attendu['carte']} introuvable dans la partie"
    soucis = []
    for classe in attendu["oui"]:
        if not face.IsClass(classe):
            soucis.append(f"IsClass({classe}) devrait etre vrai")
        if not CardFinder(card_class=classe).Check(face):
            soucis.append(f"CardFinder(card_class={classe}) devrait retenir la carte")
        if not CardFinder(card_classes=[classe]).Check(face):
            soucis.append(f"CardFinder(card_classes=[{classe}]) devrait retenir la carte")
    for classe in attendu["non"]:
        if face.IsClass(classe):
            soucis.append(f"IsClass({classe}) devrait etre faux")
        if CardFinder(card_class=classe).Check(face):
            soucis.append(f"CardFinder(card_class={classe}) ne devrait PAS retenir la carte")
    toutes = ["Bushido", "Ninjutsu", "Kuji-Kiri", "Taijutsu"]
    if not CardFinder(card_classes=toutes).Check(face):
        soucis.append("CardFinder(card_classes=<les 4 Shinobi>) devrait retenir la carte (une carte Shinobi)")
    if soucis:
        return False, " ; ".join(soucis)
    return True, f"{attendu['carte']} : classes {attendu['oui']} reconnues, {len(attendu['non'])} classes refusees"


def sc_actions_disponibles(monde, aides):
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
