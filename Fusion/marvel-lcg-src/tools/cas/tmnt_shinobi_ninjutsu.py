# Cas test_capacites du pack tmnt_shinobi_ninjutsu (Inkwire, TMNT Shinobi, les 20 cartes NINJUTSU, prefixe `sa`), 17/10/2026.
# Filtre : `[sa]`. Gabarits : .planning/tmnt/shinobi-ninjutsu-gabarits.md. Questions : .planning/tmnt/shinobi-ninjutsu-questions.md.
#
# Conventions (reprises de tools/cas/tmnt_shinobi_paths.py) :
#  - Spider-Man (01001) demarre en ALTER EGO ; HEROS le met en forme heros (carte 01001a, 10 PV, ATQ 2, CTR 1, DEF 3) ;
#  - le HEROS est camoufle par `Puzzle.Cloak('01001a')` (BASCULE : un second appel retire la carte) ;
#  - Rhino 01094 (14 PV, ATQ 2) est le vilain du scenario `rhino`, 01101 Hydra Mercenary (3 PV) le sbire, 01097b le complot principal ;
#  - `main_exclusive` vide la main (APRES la mise en place) : chaque cas sait avec QUOI il paie
#    (01088 Energy = YY, 01089 Genius = BB, 01090 Strength = RR) ;
#  - deck rencontre bourre de « I'm Tough » (01105, sans icone de boost) : aucune carte rencontre ne brouille la mesure ;
#  - la substitution (preuve) retire le module de la carte : `tools/substituer_pack.py` ou le script jetable du gabarit.
SC = "rhino"
HEROS = "Puzzle.ChangeForm('01001b')"
CLOAK = "Puzzle.Cloak('01001a')"
SBIRE = "Puzzle.PutIntoPlay('01101')"
SANS_BOOST = ["Puzzle.EmptyEncounterDeck()",
              "Puzzle.CreateEncounterDeck('01105', '01105', '01105', '01105', '01105', '01105', '01105', '01105')"]


def _c(nom, pourquoi, mise, declencher, attendu, **cle):
    if not cle.pop("avec_boost", False):
        mise = SANS_BOOST + list(mise)
    cas = {"nom": "[sa] " + nom, "pourquoi": pourquoi, "scenario": cle.pop("scenario", SC),
           "heros": cle.pop("heros", "spider_man"), "mise_en_place": list(mise), "declencher": list(declencher),
           "verifier": cle.pop("verifier", "etat_attendu"), "attendu": attendu}
    cas.update(cle)
    return cas


def _jouable(nom, pourquoi, mise, carte, jouable, **cle):
    """Cas « la carte en main est (ou n'est pas) jouable »."""
    cle.setdefault("main_exclusive", [carte, "01088", "01088"])
    return _c(nom, pourquoi, mise, cle.pop("declencher", []), {"carte": carte, "jouable": jouable},
              verifier="sn_jouable", **cle)


def _dispo(nom, pourquoi, mise, carte, type_, nombre, **cle):
    """Cas « l'action de la carte EN JEU est (ou n'est pas) proposee » : `nombre` actions reellement disponibles."""
    return _c(nom, pourquoi, mise, cle.pop("declencher", []), {"carte": carte, "type": type_, "nombre": nombre},
              verifier="sn_actions_disponibles", **cle)


def _en_jeu(cid):
    return f"Puzzle.PutIntoPlay('{cid}', under_control=True)"


CAS = [
    # ===================================================================== sa001 Assassinate
    _c("sa001 Assassinate : heros camoufle, 7 degats a un sbire (Hydra Mercenary vaincu), la carte est defaussee",
       "« Action (attack): Deal 7 damage to a minion » : 3 PV, 7 degats -> vaincu ; Cloaked reste sur le heros (aucun cout)",
       [HEROS, CLOAK, SBIRE], [],
       {"hors_jeu": ["01101"], "defausse": ["sa001"], "statuts": [["01001a", "Cloaked"]]},
       main_exclusive=["sa001", "01088"], jouer=["sa001"], cibles=["01101"], accepter_choix=True),
    _c("sa001 Assassinate : « gains piercing » : le sbire CORIACE est vaincu (la Coriace part d'abord, les 7 degats passent)",
       "sans piercing, la Coriace absorberait toute l'attaque (le sbire resterait en jeu, sans Coriace) ; avec : 3 PV - 7 -> vaincu",
       [HEROS, CLOAK, SBIRE, "Puzzle.Tough('01101')"], [],
       {"hors_jeu": ["01101"], "defausse": ["sa001"]},
       main_exclusive=["sa001", "01088"], jouer=["sa001"], cibles=["01101"], accepter_choix=True),
    _jouable("sa001 Assassinate : TEMOIN, heros NON camoufle -> injouable",
             "« Play only if your hero is cloaked » : sans Cloaked sur le heros, la carte en main n'est pas jouable",
             [HEROS, SBIRE], "sa001", False),
    _jouable("sa001 Assassinate : heros camoufle -> jouable (temoin positif du precedent)",
             "meme montage avec Cloaked : jouable",
             [HEROS, CLOAK, SBIRE], "sa001", True),
    _jouable("sa001 Assassinate : forme ALTER-EGO (identite camouflee) -> injouable (pas de heros)",
             "en forme alter-ego il n'y a pas de heros en jeu : « your hero is cloaked » est faux (Q-N1)",
             [SBIRE, "Puzzle.Cloak('01001b')"], "sa001", False),
    _jouable("sa001 Assassinate : aucun sbire (seul le vilain) -> injouable (« a MINION », pas un ennemi)",
             "heros camoufle mais aucune cible legale : Rhino n'est pas un sbire",
             [HEROS, CLOAK], "sa001", False),
]

# Cartes de rencontre qui fixent les icones de boost de l'attaque de Rhino (ATQ 2) : 01101 = 1 icone, 01111 = 2, 01119 = 3.
UNE_ICONE = ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01101')"]
DEUX_ICONES = ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01111')"]
TROIS_ICONES = ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01119')"]

CAS += [
    # ===================================================================== sa002 Shroud and Protect
    _c("sa002 Shroud and Protect : +1 DEF (DEF 4 contre ATQ 4 : 0 degat) -> le heros est camoufle ET REDRESSE",
       "Rhino ATQ 2 + 2 icones = 4 contre DEF 3 : 1 degat sans la carte (temoin) ; avec +1 DEF : 0 degat -> « cloak and ready your hero » "
       "(le heros, incline par sa defense, est redresse ; une carte Cloaked est posee)",
       [HEROS] + DEUX_ICONES, ["Puzzle.Defend('01001a', '01094')"],
       {"degats_identite": 0, "defausse": ["sa002"], "pret": ["01001a"], "statuts": [["01001a", "Cloaked"]]},
       main_exclusive=["sa002", "01088"], payer_avec=["01088"], avec_boost=True),
    _c("sa002 Shroud and Protect : TEMOIN sans la carte : la meme defense laisse 1 degat, le heros reste incline, sans Cloaked",
       "ligne de base : DEF 3 contre ATQ 4 = 1 degat ; le heros s'incline en defendant",
       [HEROS] + DEUX_ICONES, ["Puzzle.Defend('01001a', '01094')"],
       {"degats_identite": 1, "exhausted": ["01001a"], "statuts_absents": [["01001a", "Cloaked"]]},
       main_exclusive=["01088"], avec_boost=True),
    _c("sa002 Shroud and Protect : « If you take NO damage » : 1 degat subi (ATQ 5 contre DEF 4) -> ni Cloaked ni redressement",
       "3 icones : ATQ 5 contre DEF 3 + 1 = 4 : 1 degat ; la branche conditionnelle ne part pas, le heros reste incline",
       [HEROS] + TROIS_ICONES, ["Puzzle.Defend('01001a', '01094')"],
       {"degats_identite": 1, "defausse": ["sa002"], "exhausted": ["01001a"], "statuts_absents": [["01001a", "Cloaked"]]},
       main_exclusive=["sa002", "01088"], payer_avec=["01088"], avec_boost=True),
    _c("sa002 Shroud and Protect : heros DEJA camoufle : la defense consomme sa carte (+2 DEF), la nouvelle carte Cloaked le remplace (une seule)",
       "livret p.8 : « If I defend with a Cloaked status card, ... +2 DEF, then the status card will be discarded before any excess "
       "damage » ; ATQ 5 contre DEF 3 + 1 + 2 = 6 : 0 degat (sans le +2 du Cloaked il y en aurait 1) ; la carte consommee, « cloak your "
       "hero » en pose UNE autre : jamais deux",
       [HEROS, CLOAK] + TROIS_ICONES, ["Puzzle.Defend('01001a', '01094')"],
       {"degats_identite": 0, "defausse": ["sa002"], "pret": ["01001a"], "statuts": [["01001a", "Cloaked"]]},
       main_exclusive=["sa002", "01088"], payer_avec=["01088"], avec_boost=True, verifier="sn_un_seul_cloaked"),
    _c("sa002 Shroud and Protect : « Hero Interrupt » : en forme ALTER-EGO la carte n'est pas jouee (3 degats subis, carte en main)",
       "l'alter-ego n'a pas de defense : Rhino 2 + 1 icone = 3 degats ; l'Interruption de heros ne part pas",
       [] + UNE_ICONE, ["Puzzle.Attack('01094')"],
       {"degats_identite": 3, "en_main": ["sa002"]},
       main_exclusive=["sa002", "01088"], avec_boost=True),
    _c("sa002 Shroud and Protect : « When YOU defend » : quand un ALLIE defend, la carte n'est pas jouee",
       "`is_basic_defense` + « You » : Splinter (tl002, allie) defend, la carte reste en main et le heros n'est pas camoufle",
       [HEROS, "Puzzle.PutIntoPlay('tl002', under_control=True)"] + UNE_ICONE, ["Puzzle.Defend('tl002', '01094')"],
       {"en_main": ["sa002"], "statuts_absents": [["01001a", "Cloaked"]]},
       main_exclusive=["sa002", "01088"], payer_avec=["01088"], avec_boost=True),
]

DECK_RENCONTRE = ["Puzzle.EmptyEncounterDeck()",
                  "Puzzle.CreateEncounterDeck('01105', '01105', '01105', '01105', '01124', '01133', '01111')"]  # dessus = 01111
DECK_JOUEUR = ["Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01088', '01090', '01119', '01124', '01133')"]  # dessus = 01133

CAS += [
    # ===================================================================== sa003 Reconnaissance
    _c("sa003 Reconnaissance : le HEROS est camoufle (cout), les 3 cartes du dessus du deck RENCONTRE sont regardees, le deck garde sa taille",
       "« Cloak a character you control -> look at the top 3 cards of a player deck or encounter deck » : cout paye sur le heros, "
       "evenement defausse, 3 cartes visibles du joueur, aucune carte n'a quitte le deck (7 cartes)",
       [HEROS] + DECK_RENCONTRE, [],
       {"deck": "rencontre", "vus": 3, "ids_vus": ["01111", "01133", "01124"], "taille": 7, "defausse": ["sa003"],
        "dessus": "01111", "dessous": ["01133", "01124"],
        "statuts": [["01001a", "Cloaked"]]},
       verifier="sn_a_regarde", main_exclusive=["sa003", "01089"], jouer=["sa003"], cibles=["01111"], accepter_choix=True,
       avec_boost=True),
    _c("sa003 Reconnaissance : « a PLAYER deck » : les 3 cartes du dessus de SON deck sont regardees",
       "meme evenement, autre deck : le deck du joueur (5 cartes), 3 visibles, taille intacte",
       [HEROS] + DECK_JOUEUR, [],
       {"deck": "joueur", "vus": 3, "ids_vus": ["01133", "01124", "01119"], "taille": 5, "defausse": ["sa003"],
        "dessus": "01133", "dessous": ["01124", "01119"],
        "statuts": [["01001a", "Cloaked"]]},
       verifier="sn_a_regarde", main_exclusive=["sa003", "01089"], jouer=["sa003"], cibles=["01133"], accepter_choix=True),
    _c("sa003 Reconnaissance : « a PLAYER deck » : le deck d'un AUTRE joueur (partie a deux)",
       "le deck du second joueur est un choix legal : ses 3 cartes du dessus (dont 01119 pose dessus) sont regardees",
       [HEROS, "Puzzle.MoveTo('01119', 'PlayerDeck', 'Top', 1)"], [],
       {"deck": "autre", "vus": 3, "defausse": ["sa003"], "statuts": [["01001a", "Cloaked"]]},
       verifier="sn_a_regarde", main_exclusive=["sa003", "01089"], jouer=["sa003"], cibles=["01119"], accepter_choix=True,
       heros2="iron_man"),
    _c("sa003 Reconnaissance : forme ALTER-EGO : « Action » (pas Hero Action), le cout camoufle l'identite alter-ego",
       "Action utilisable dans les deux formes : l'alter-ego (identite = personnage controle) recoit la carte Cloaked",
       [] + DECK_RENCONTRE, [],
       {"deck": "rencontre", "vus": 3, "taille": 7, "defausse": ["sa003"], "statuts": [["01001b", "Cloaked"]]},
       verifier="sn_a_regarde", main_exclusive=["sa003", "01089"], jouer=["sa003"], cibles=["01111"], accepter_choix=True,
       avec_boost=True),
    _c("sa003 Reconnaissance : « a character you control » : heros DEJA camoufle, le cout se paie sur l'ALLIE (une seule Cloaked par personnage)",
       "le heros a deja sa carte Cloaked : seul Splinter (tl002) est une cible legale du cout ; il est camoufle, le heros garde UNE carte",
       [HEROS, CLOAK, "Puzzle.PutIntoPlay('tl002', under_control=True)"] + DECK_RENCONTRE, [],
       {"deck": "rencontre", "vus": 3, "taille": 7, "defausse": ["sa003"], "statuts": [["tl002", "Cloaked"], ["01001a", "Cloaked"]]},
       verifier="sn_a_regarde", main_exclusive=["sa003", "01089"], jouer=["sa003"], cibles=["01111"], accepter_choix=True,
       avec_boost=True),
    _jouable("sa003 Reconnaissance : TEMOIN, tous les personnages controles deja camoufles -> injouable (le cout ne peut pas etre paye)",
             "« Cloak a character you control » est le COUT : le heros (seul personnage) porte deja une carte Cloaked",
             [HEROS, CLOAK], "sa003", False, main_exclusive=["sa003", "01089"]),
    _jouable("sa003 Reconnaissance : un personnage sans Cloaked -> jouable (temoin positif du precedent)",
             "meme montage sans Cloaked : jouable",
             [HEROS], "sa003", True, main_exclusive=["sa003", "01089"]),
]

DECK6 = ["Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01090', '01090', '01090', '01090', '01090', '01090')"]
SIDE_SCHEME = "Puzzle.PutIntoPlay('01107')"   # Breakin' & Takin' : complot annexe, 2 menaces au depart

CAS += [
    # ===================================================================== sa004 Scale the Wall
    _c("sa004 Scale the Wall : heros camoufle -> pioche 2 cartes ; la carte Cloaked n'est PAS depensee",
       "« Hero Action: Draw 2 cards » : main vide + 2 ; evenement defausse ; Cloaked toujours sur le heros (aucun cout)",
       [HEROS, CLOAK] + DECK6, [],
       {"taille_main": 2, "defausse": ["sa004"], "statuts": [["01001a", "Cloaked"]]},
       main_exclusive=["sa004"], jouer=["sa004"], accepter_choix=True),
    _jouable("sa004 Scale the Wall : TEMOIN, heros NON camoufle -> injouable",
             "« Play only if your hero is cloaked »", [HEROS] + DECK6, "sa004", False, main_exclusive=["sa004"]),
    _jouable("sa004 Scale the Wall : forme ALTER-EGO (identite camouflee) -> injouable (pas de heros)",
             "« your hero is cloaked » faux en alter-ego (Q-N1)", [CLOAK.replace("01001a", "01001b")] + DECK6, "sa004", False,
             main_exclusive=["sa004"]),
    _c("sa004 Scale the Wall : TEMOIN D'EPUISEMENT « Max 1 per round » : une SECONDE copie, meme round -> injouable (main 1 + 2 piochees = 3)",
       "la 1re copie est jouee (pioche 2 : main = la 2e copie + 2) ; la 2e copie est refusee (limite imprimee, chiffre : jouable=False)",
       [HEROS, CLOAK] + DECK6, [],
       {"carte": "sa004", "jouable": False, "taille_main": 3, "defausse": ["sa004"]},
       verifier="sn_jouable", main_exclusive=["sa004", "sa004"], jouer=["sa004"], accepter_choix=True),

    # ===================================================================== sa005 Run the Rooftops
    _c("sa005 Run the Rooftops : heros camoufle -> retire 2 menaces du complot principal (5 -> 3) ; Cloaked conserve",
       "« Hero Action (thwart): Remove 2 threat from a scheme » : complot principal 01097b a 5 menaces",
       [HEROS, CLOAK, "Puzzle.EmptyHand()", "Puzzle.SetThreat('01097b', 5)"], [],
       {"menace": [["01097b", 3]], "defausse": ["sa005"], "statuts": [["01001a", "Cloaked"]]},
       main_exclusive=["sa005"], jouer=["sa005"], cibles=["01097b"], accepter_choix=True),
    _c("sa005 Run the Rooftops : « a scheme » : un COMPLOT ANNEXE (2 menaces) est vaincu par les 2 menaces retirees",
       "pas seulement le complot principal : Breakin' & Takin' (01107, 2 menaces) tombe a 0 et part",
       [HEROS, CLOAK, SIDE_SCHEME], [],
       {"hors_jeu": ["01107"], "defausse": ["sa005"]},
       main_exclusive=["sa005"], jouer=["sa005"], cibles=["01107"], accepter_choix=True),
    _c("sa005 Run the Rooftops : 2 menaces EXACTEMENT : le complot principal n'en perd pas plus (menace 4 -> 2, jamais 0)",
       "borne haute : 2, pas 3 ni « toutes »",
       [HEROS, CLOAK, "Puzzle.EmptyHand()", "Puzzle.SetThreat('01097b', 4)"], [],
       {"menace": [["01097b", 2]]},
       main_exclusive=["sa005"], jouer=["sa005"], cibles=["01097b"], accepter_choix=True),
    _jouable("sa005 Run the Rooftops : TEMOIN, heros NON camoufle -> injouable",
             "« Play only if your hero is cloaked »", [HEROS, "Puzzle.EmptyHand()", "Puzzle.SetThreat('01097b', 5)"], "sa005", False, main_exclusive=["sa005"]),
    _jouable("sa005 Run the Rooftops : forme ALTER-EGO (identite camouflee) -> injouable",
             "« Hero Action » : forme heros seulement ; « your hero is cloaked » faux en alter-ego",
             ["Puzzle.Cloak('01001b')", "Puzzle.EmptyHand()", "Puzzle.SetThreat('01097b', 5)"], "sa005", False, main_exclusive=["sa005"]),

    # ===================================================================== sa006 Cut-and-Run
    _c("sa006 Cut-and-Run : 4 degats a un sbire de 3 PV (vaincu) -> le heros est camoufle",
       "« If this attack defeats an enemy, cloak your hero » : Hydra Mercenary (3 PV) meurt, le heros recoit sa carte Cloaked",
       [HEROS, SBIRE], [],
       {"hors_jeu": ["01101"], "defausse": ["sa006"], "statuts": [["01001a", "Cloaked"]]},
       main_exclusive=["sa006", "01088"], jouer=["sa006"], cibles=["01101"], accepter_choix=True),
    _c("sa006 Cut-and-Run : 4 degats EXACTEMENT a un sbire de 4 PV (Advanced Ultron Drone) -> vaincu, camoufle",
       "borne : 4 degats contre 4 PV = « defeats »",
       [HEROS, "Puzzle.PutIntoPlay('01143')"], [],
       {"hors_jeu": ["01143"], "statuts": [["01001a", "Cloaked"]]},
       main_exclusive=["sa006", "01088"], jouer=["sa006"], cibles=["01143"], accepter_choix=True),
    _c("sa006 Cut-and-Run : TEMOIN, 4 degats au VILAIN (14 PV, non vaincu) -> 4 degats poses, le heros n'est PAS camoufle",
       "« an ENEMY » : le vilain est une cible legale ; il survit : pas de Cloaked",
       [HEROS], [],
       {"degats": [["01094", 4]], "defausse": ["sa006"], "statuts_absents": [["01001a", "Cloaked"]]},
       main_exclusive=["sa006", "01088"], jouer=["sa006"], cibles=["01094"], accepter_choix=True),
    _c("sa006 Cut-and-Run : TEMOIN, sbire CORIACE : la Coriace absorbe les 4 degats, le sbire survit -> pas de Cloaked",
       "« defeats » : un sbire non vaincu (Coriace) ne declenche rien",
       [HEROS, SBIRE, "Puzzle.Tough('01101')"], [],
       {"en_jeu": ["01101"], "statuts_absents": [["01001a", "Cloaked"]], "defausse": ["sa006"]},
       main_exclusive=["sa006", "01088"], jouer=["sa006"], cibles=["01101"], accepter_choix=True),
    _c("sa006 Cut-and-Run : heros DEJA camoufle, sbire vaincu : il garde UNE seule carte Cloaked",
       "une seule carte Cloaked par personnage : « cloak your hero » ne pose rien de plus",
       [HEROS, CLOAK, SBIRE], [],
       {"hors_jeu": ["01101"], "statuts": [["01001a", "Cloaked"]]},
       main_exclusive=["sa006", "01088"], jouer=["sa006"], cibles=["01101"], accepter_choix=True, verifier="sn_un_seul_cloaked"),
]

ALLIE = "Puzzle.PutIntoPlay('tl002', under_control=True)"        # Splinter (allie) sous le controle du joueur 1
AUTRE_ALLIE = "Puzzle.PutIntoPlay('01059', under_control=True)"  # Jessica Jones (allie)

CAS += [
    # ===================================================================== sa007 Hamato Clan
    _c("sa007 Hamato Clan : un ALLIE que je controle est defausse -> 1 compteur shadow sur Hamato Clan",
       "« Response: After an ally you control leaves play, place 1 shadow counter here » ; la carte entre en jeu SANS compteur",
       [HEROS, _en_jeu("sa007"), ALLIE], ["Puzzle.Discard('tl002')"],
       {"compteurs": [["sa007", "shadow", 1]]}, accepter_choix=True),
    _c("sa007 Hamato Clan : l'allie est VAINCU par des degats (il quitte le jeu) -> 1 compteur",
       "« leaves play » couvre la defaite, pas seulement la defausse",
       [HEROS, _en_jeu("sa007"), ALLIE], ["Puzzle.Damage('tl002', 20)"],
       {"compteurs": [["sa007", "shadow", 1]], "hors_jeu": ["tl002"]}, accepter_choix=True),
    _c("sa007 Hamato Clan : DEUX allies partent -> 2 compteurs (un par allie)",
       "un compteur PAR allie parti",
       [HEROS, _en_jeu("sa007"), ALLIE, AUTRE_ALLIE], ["Puzzle.Discard('tl002')", "Puzzle.Discard('01059')"],
       {"compteurs": [["sa007", "shadow", 2]]}, accepter_choix=True),
    _c("sa007 Hamato Clan : TEMOIN, l'allie d'un AUTRE joueur part -> aucun compteur (« you control »)",
       "partie a deux : Splinter est sous le controle du joueur 2",
       [HEROS, _en_jeu("sa007"), "Puzzle.PutIntoPlay('tl002', player=1, under_control=True)"], ["Puzzle.Discard('tl002')"],
       {"compteurs": [["sa007", "shadow", 0]]}, accepter_choix=True, heros2="iron_man"),
    _c("sa007 Hamato Clan : TEMOIN, un SBIRE qui part n'est pas un allie -> aucun compteur",
       "« an ally » : un sbire defausse ne declenche rien",
       [HEROS, _en_jeu("sa007"), SBIRE], ["Puzzle.Discard('01101')"],
       {"compteurs": [["sa007", "shadow", 0]]}, accepter_choix=True),
    _c("sa007 Hamato Clan Action : s'incline, retire 1 compteur, camoufle l'ALLIE choisi",
       "« Exhaust this card and remove 1 shadow counter from here -> cloak an ally you control »",
       [HEROS, _en_jeu("sa007"), ALLIE, "Puzzle.Counter('sa007', 'shadow', 1)"], ["Puzzle.Action('sa007', 'Action', 0)"],
       {"statuts": [["tl002", "Cloaked"]], "compteurs": [["sa007", "shadow", 0]], "exhausted": ["sa007"]}, cibles=["tl002"]),
    _c("sa007 Hamato Clan Action : 2 compteurs -> il en reste 1 apres un usage",
       "un seul compteur retire par usage",
       [HEROS, _en_jeu("sa007"), ALLIE, "Puzzle.Counter('sa007', 'shadow', 2)"], ["Puzzle.Action('sa007', 'Action', 0)"],
       {"statuts": [["tl002", "Cloaked"]], "compteurs": [["sa007", "shadow", 1]], "exhausted": ["sa007"]}, cibles=["tl002"]),
    _dispo("sa007 Hamato Clan : TEMOIN, sans compteur shadow l'Action n'est pas proposee",
           "le cout inclut un compteur", [HEROS, _en_jeu("sa007"), ALLIE], "sa007", "Action", 0),
    _dispo("sa007 Hamato Clan : TEMOIN D'EPUISEMENT, inclinee (meme avec des compteurs) l'Action n'est plus proposee",
           "« Exhaust this card » : 2 compteurs, un usage, puis 0 action disponible malgre le compteur restant",
           [HEROS, _en_jeu("sa007"), ALLIE, "Puzzle.Counter('sa007', 'shadow', 2)"], "sa007", "Action", 0,
           declencher=["Puzzle.Action('sa007', 'Action', 0)"], cibles=["tl002"]),
    _dispo("sa007 Hamato Clan : TEMOIN, sans ALLIE sous mon controle l'Action n'est pas proposee (« cloak an ally you control »)",
           "le heros n'est pas un allie", [HEROS, _en_jeu("sa007"), "Puzzle.Counter('sa007', 'shadow', 1)"], "sa007", "Action", 0),
    _dispo("sa007 Hamato Clan : avec compteur, pret et un allie -> 1 action (temoin positif)",
           "montage complet", [HEROS, _en_jeu("sa007"), ALLIE, "Puzzle.Counter('sa007', 'shadow', 1)"], "sa007", "Action", 1),
    _dispo("sa007 Hamato Clan : « Action » (pas Hero Action) : proposee aussi en forme ALTER-EGO",
           "les deux formes", [_en_jeu("sa007"), ALLIE, "Puzzle.Counter('sa007', 'shadow', 1)"], "sa007", "Action", 1),

    # ===================================================================== sa008 Smoke Bombs
    _c("sa008 Smoke Bombs : entre en jeu avec 2 compteurs smoke (Uses 2)",
       "« Uses (2 smoke counters) » : base native, 2 compteurs a l'entree en jeu",
       [HEROS], [],
       {"compteurs": [["sa008", "smoke", 2]], "en_jeu": ["sa008"]},
       main_exclusive=["sa008", "01090"], jouer=["sa008"], accepter_choix=True),
    _c("sa008 Smoke Bombs : « Max 1 per player » : la 1re copie est jouee, la 2e (restee en main) est injouable",
       "limite imprimee `MaxPerUnit = 1` : 1 en jeu -> la copie en main n'est plus jouable (chiffre : jouable=False)",
       [HEROS], [], {"carte": "sa008", "jouable": False, "en_jeu": ["sa008"]},
       verifier="sn_jouable", main_exclusive=["sa008", "sa008", "01090", "01090"], payer_avec=["01090"], ne_pas_depenser=["sa008"],
       jouer=["sa008"], accepter_choix=True),
    _jouable("sa008 Smoke Bombs : TEMOIN, sans autre copie en jeu -> jouable",
             "meme montage sans la copie en jeu", [HEROS], "sa008", True, main_exclusive=["sa008", "01090"]),
    _c("sa008 Smoke Bombs Hero Action : s'incline, retire 1 compteur, camoufle un personnage AMI (le heros)",
       "« Exhaust this card and remove 1 smoke counter from it -> cloak a friendly character »",
       [HEROS, _en_jeu("sa008")], ["Puzzle.Action('sa008', 'HeroAction', 0)"],
       {"statuts": [["01001a", "Cloaked"]], "compteurs": [["sa008", "smoke", 1]], "exhausted": ["sa008"]}, cibles=["01001a"]),
    _c("sa008 Smoke Bombs : « a FRIENDLY character » : un ALLIE peut etre camoufle (le heros reste sans Cloaked)",
       "identites ET allies amis", [HEROS, _en_jeu("sa008"), ALLIE], ["Puzzle.Action('sa008', 'HeroAction', 0)"],
       {"statuts": [["tl002", "Cloaked"]], "statuts_absents": [["01001a", "Cloaked"]], "compteurs": [["sa008", "smoke", 1]]},
       cibles=["tl002"]),
    _c("sa008 Smoke Bombs : DEUX usages (redresse entre les deux) : le 2e retire le dernier compteur, la carte est defaussee (Uses)",
       "2 compteurs, 2 utilisations (meme cible : la 2e carte Cloaked n'est pas empilee), puis la carte part : Splinter reste camoufle, UNE carte",
       [HEROS, _en_jeu("sa008"), ALLIE],
       ["Puzzle.Action('sa008', 'HeroAction', 0)", "Puzzle.Ready('sa008')", "Puzzle.Action('sa008', 'HeroAction', 0)"],
       {"hors_jeu": ["sa008"], "defausse": ["sa008"], "statuts": [["tl002", "Cloaked"]]},
       cibles=["tl002"]),
    _dispo("sa008 Smoke Bombs : TEMOIN D'EPUISEMENT, inclinee (1 compteur restant) l'action n'est plus proposee",
           "« Exhaust this card » : apres un usage, 0 action disponible",
           [HEROS, _en_jeu("sa008")], "sa008", "HeroAction", 0, declencher=["Puzzle.Action('sa008', 'HeroAction', 0)"],
           cibles=["01001a"]),
    _dispo("sa008 Smoke Bombs : Hero Action NON proposee en forme alter-ego",
           "forme heros seulement", [_en_jeu("sa008")], "sa008", "HeroAction", 0),
]

CAS += [
    # ===================================================================== sa009 Twilight Sentry
    _c("sa009 Twilight Sentry : se pose sur un ALLIE que je controle ET le camoufle (Forced Response a la pose)",
       "« Attach to an ally you control and cloak them » : Splinter recoit l'amelioration et une carte Cloaked ; le heros n'est pas touche",
       [HEROS, ALLIE], [],
       {"accroche_a": [["sa009", "tl002"]], "statuts": [["tl002", "Cloaked"]], "statuts_absents": [["01001a", "Cloaked"]]},
       main_exclusive=["sa009", "01089"], jouer=["sa009"], cibles=["tl002"], accepter_choix=True),
    _jouable("sa009 Twilight Sentry : TEMOIN, aucun allie -> injouable (« an ally you control »)",
             "le heros n'est pas une cible legale", [HEROS], "sa009", False, main_exclusive=["sa009", "01089"]),
    _jouable("sa009 Twilight Sentry : TEMOIN, un allie d'un AUTRE joueur seulement -> injouable (« you control »)",
             "partie a deux : Splinter est sous le controle du joueur 2",
             [HEROS, "Puzzle.PutIntoPlay('tl002', player=1, under_control=True)"], "sa009", False,
             main_exclusive=["sa009", "01089"], heros2="iron_man"),
    _jouable("sa009 Twilight Sentry : un allie que je controle -> jouable (temoin positif)",
             "meme montage avec mon allie", [HEROS, ALLIE], "sa009", True, main_exclusive=["sa009", "01089"]),
    _jouable("sa009 Twilight Sentry : « Max 1 TRAINING upgrade per ally » : l'allie porte deja une TRAINING -> injouable",
             "Attack Training (ua004, trait TRAINING) deja attachee a Splinter, seul allie",
             [HEROS, ALLIE, "Puzzle.AttachReel('ua004', 'tl002')"], "sa009", False, main_exclusive=["sa009", "01089"]),
    _c("sa009 Twilight Sentry Interrupt [LECTURE PROVISOIRE Q-N3, ordre du moteur] : l'allie camoufle va subir 3 degats -> le STATUT Cloaked resout "
       "d'abord (-2, defausse), l'allie en subit 1, l'Interruption n'a plus de carte Cloaked a defausser",
       "RR : les cartes d'etat resolvent AVANT les Interruptions (`TimingPriority.Status` < `Interrupt`) : Sentry n'est jamais proposee a un allie "
       "porteur d'UNE carte Cloaked ; question Q-N3 posee a l'utilisateur (resolution recommandee : Sentry AVANT le statut, 0 degat)",
       [HEROS, ALLIE, "Puzzle.AttachReel('sa009', 'tl002')"], ["Puzzle.Damage('tl002', 3)"],
       {"degats": [["tl002", 1]], "statuts_absents": [["tl002", "Cloaked"]], "accroche_a": [["sa009", "tl002"]]}, accepter_choix=True),
    _c("sa009 Twilight Sentry : TEMOIN sans Sentry : un allie camoufle qui subit 3 degats n'en evite que 2 (1 subi, Cloaked consomme)",
       "ligne de base : le statut Cloaked seul prevoit 2 (cloaked.md)",
       [HEROS, ALLIE, "Puzzle.Cloak('tl002')"], ["Puzzle.Damage('tl002', 3)"],
       {"degats": [["tl002", 1]], "statuts_absents": [["tl002", "Cloaked"]]}, accepter_choix=True),
    _c("sa009 Twilight Sentry : TEMOIN, l'allie n'est PAS camoufle : l'Interruption n'est pas proposee, il subit les degats (2)",
       "« discard a cloaked status card from them » : sans Cloaked, rien a defausser, donc pas d'Interruption",
       [HEROS, ALLIE, "Puzzle.AttachReel('sa009', 'tl002')", "Puzzle.Cloak('tl002')"], ["Puzzle.Damage('tl002', 2)"],
       {"degats": [["tl002", 2]], "accroche_a": [["sa009", "tl002"]]}, accepter_choix=True),
    _c("sa009 Twilight Sentry : « attached ally » : un AUTRE allie camoufle (sans Sentry) n'est pas protege (1 degat sur 3)",
       "Sentry est attachee a Splinter ; Jessica Jones camoufle subit 3 degats : le Cloaked prevoit 2",
       [HEROS, ALLIE, AUTRE_ALLIE, "Puzzle.AttachReel('sa009', 'tl002')", "Puzzle.Cloak('01059')"], ["Puzzle.Damage('01059', 3)"],
       {"degats": [["01059", 1]], "statuts": [["tl002", "Cloaked"]]}, accepter_choix=True),

    # ===================================================================== sa010 Opportunist
    _c("sa010 Opportunist : defausse la carte Cloaked du heros et s'incline -> retire 3 menaces (5 -> 2)",
       "« Discard a cloaked status card from a character you control and exhaust Opportunist -> remove 3 threat from a scheme »",
       [HEROS, CLOAK, _en_jeu("sa010"), "Puzzle.EmptyHand()", "Puzzle.SetThreat('01097b', 5)"], ["Puzzle.Action('sa010', 'HeroAction', 0)"],
       {"menace": [["01097b", 2]], "statuts_absents": [["01001a", "Cloaked"]], "exhausted": ["sa010"]}, cibles=["01097b"]),
    _c("sa010 Opportunist : « a character you control » : la carte Cloaked peut venir d'un ALLIE (le heros n'est pas camoufle)",
       "Splinter camoufle : sa carte est defaussee, le complot perd 3 menaces",
       [HEROS, ALLIE, "Puzzle.Cloak('tl002')", _en_jeu("sa010"), "Puzzle.EmptyHand()", "Puzzle.SetThreat('01097b', 5)"], ["Puzzle.Action('sa010', 'HeroAction', 0)"],
       {"menace": [["01097b", 2]], "statuts_absents": [["tl002", "Cloaked"]], "exhausted": ["sa010"]}, cibles=["tl002", "01097b"]),
    _c("sa010 Opportunist : « a scheme » : un complot ANNEXE de 2 menaces est vaincu (3 menaces retirees, au plus 2 presentes)",
       "pas seulement le complot principal", [HEROS, CLOAK, _en_jeu("sa010"), SIDE_SCHEME], ["Puzzle.Action('sa010', 'HeroAction', 0)"],
       {"hors_jeu": ["01107"], "statuts_absents": [["01001a", "Cloaked"]]}, cibles=["01107"]),
    _dispo("sa010 Opportunist : TEMOIN, aucune carte Cloaked chez moi -> l'action n'est pas proposee",
           "le cout exige une carte Cloaked", [HEROS, _en_jeu("sa010"), "Puzzle.EmptyHand()", "Puzzle.SetThreat('01097b', 5)"], "sa010", "HeroAction", 0),
    _dispo("sa010 Opportunist : TEMOIN, la carte Cloaked est sur un personnage d'un AUTRE joueur -> pas proposee (« you control »)",
           "partie a deux : Splinter camoufle est sous le controle du joueur 2",
           [HEROS, "Puzzle.PutIntoPlay('tl002', player=1, under_control=True)", "Puzzle.Cloak('tl002')", _en_jeu("sa010"),
            "Puzzle.EmptyHand()", "Puzzle.SetThreat('01097b', 5)"], "sa010", "HeroAction", 0, heros2="iron_man"),
    _dispo("sa010 Opportunist : TEMOIN D'EPUISEMENT, inclinee (un Cloaked reste) -> plus proposee",
           "cout « exhaust Opportunist » : heros et allie camoufles, un usage, puis 0 action malgre le Cloaked restant",
           [HEROS, CLOAK, ALLIE, "Puzzle.Cloak('tl002')", _en_jeu("sa010"), "Puzzle.EmptyHand()", "Puzzle.SetThreat('01097b', 5)"], "sa010", "HeroAction", 0,
           declencher=["Puzzle.Action('sa010', 'HeroAction', 0)"], cibles=["tl002", "01097b"]),
    _dispo("sa010 Opportunist : Hero Action NON proposee en forme alter-ego (identite camouflee)",
           "forme heros seulement", ["Puzzle.Cloak('01001b')", _en_jeu("sa010"), "Puzzle.EmptyHand()", "Puzzle.SetThreat('01097b', 5)"], "sa010", "HeroAction", 0),
    _dispo("sa010 Opportunist : cout payable (Cloaked + pret + complot) -> 1 action (temoin positif)",
           "montage complet", [HEROS, CLOAK, _en_jeu("sa010"), "Puzzle.EmptyHand()", "Puzzle.SetThreat('01097b', 5)"], "sa010", "HeroAction", 1),
    _c("sa010 Opportunist : « Max 1 per player » : la 1re copie est jouee, la 2e (restee en main) est injouable",
       "limite imprimee `MaxPerUnit = 1` : 1 en jeu -> la copie en main n'est plus jouable (chiffre : jouable=False)",
       [HEROS], [], {"carte": "sa010", "jouable": False, "en_jeu": ["sa010"]},
       verifier="sn_jouable", main_exclusive=["sa010", "sa010", "01090", "01090", "01090"], payer_avec=["01090"], ne_pas_depenser=["sa010"],
       jouer=["sa010"], accepter_choix=True),
    _jouable("sa010 Opportunist : TEMOIN, sans autre copie en jeu -> jouable",
             "meme montage sans la copie", [HEROS], "sa010", True, main_exclusive=["sa010", "01090", "01090"]),
]

HERO_FATIGUE = "Puzzle.Exhaust('01001a')"
SBIRE_1PV = "Puzzle.Damage(Puzzle.PutIntoPlay('01101'), 2)"   # Hydra Mercenary (3 PV) a 1 PV restant

CAS += [
    # ===================================================================== sa011 Stealth Proficiency
    _c("sa011 Stealth Proficiency (Hero Action) : defausse la carte Cloaked du heros -> le heros INCLINE est redresse",
       "« Hero Action: Discard a cloaked status card from your hero -> ready your hero » : cout paye sur le heros, evenement defausse",
       [HEROS, CLOAK, HERO_FATIGUE], [],
       {"pret": ["01001a"], "statuts_absents": [["01001a", "Cloaked"]], "defausse": ["sa011"]},
       main_exclusive=["sa011"], jouer=["sa011"], accepter_choix=True),
    _c("sa011 Stealth Proficiency : TEMOIN, heros NON camoufle -> l'Action n'est pas jouable (le heros reste incline, la carte en main)",
       "le cout (une carte Cloaked du heros) ne peut pas etre paye", [HEROS, HERO_FATIGUE], [],
       {"exhausted": ["01001a"], "en_main": ["sa011"]},
       main_exclusive=["sa011"], jouer=["sa011"], accepter_choix=True),
    _c("sa011 Stealth Proficiency (Hero Response) : apres une ATTAQUE de base du heros -> le heros est camoufle",
       "« After you use one of your basic powers, cloak your hero » : ATQ de base sur Rhino ; la carte (cout 0) est jouee depuis la main",
       [HEROS], ["Puzzle.Attack('01001a')"],
       {"statuts": [["01001a", "Cloaked"]], "defausse": ["sa011"]},
       main_exclusive=["sa011"], accepter_choix=True),
    _c("sa011 Stealth Proficiency (Hero Response) : apres un CONTRE de base (THW) -> le heros est camoufle",
       "un autre pouvoir de base du heros", [HEROS, "Puzzle.EmptyHand()", "Puzzle.SetThreat('01097b', 3)"], ["Puzzle.Thwart('01001a')"],
       {"statuts": [["01001a", "Cloaked"]], "defausse": ["sa011"]},
       main_exclusive=["sa011"], accepter_choix=True),
    _c("sa011 Stealth Proficiency (Hero Response) : apres une DEFENSE de base -> le heros est camoufle",
       "DEF est un pouvoir de base : Rhino attaque (ATQ 2 < DEF 3, 0 degat), le heros defend, puis la Reponse part",
       [HEROS], ["Puzzle.Defend('01001a', '01094')"],
       {"statuts": [["01001a", "Cloaked"]], "defausse": ["sa011"], "degats_identite": 0},
       main_exclusive=["sa011"], accepter_choix=True),
    _c("sa011 Stealth Proficiency : TEMOIN, un ALLIE utilise son pouvoir de base : pas « you » -> la carte reste en main, le heros n'est pas camoufle",
       "« After YOU use one of YOUR basic powers »", [HEROS, ALLIE], ["Puzzle.Attack('tl002')"],
       {"en_main": ["sa011"], "statuts_absents": [["01001a", "Cloaked"]]},
       main_exclusive=["sa011"], accepter_choix=True),
    _c("sa011 Stealth Proficiency (Response) : heros DEJA camoufle qui attaque : le +2 consomme la carte, la Reponse en pose UNE autre",
       "une seule carte Cloaked par personnage, jamais deux ; l'ATQ de base prend le +2 (2 + 2 = 4 degats sur Rhino)",
       [HEROS, CLOAK], ["Puzzle.Attack('01001a')"],
       {"statuts": [["01001a", "Cloaked"]], "defausse": ["sa011"], "degats": [["01094", 4]]},
       main_exclusive=["sa011"], accepter_choix=True, verifier="sn_un_seul_cloaked"),

    # ===================================================================== sa012 Black Ops (QUESTION OUVERTE Q-N2 : lecture provisoire = Hero Response)
    _c("sa012 Black Ops : le heros VAINC un sbire -> Black Ops est defaussee et le heros incline est redresse",
       "(lecture provisoire Hero Response) « After your hero defeats a minion, discard Black Ops -> ready your hero » : l'attaque de base "
       "incline le heros, la carte le redresse",
       [HEROS, _en_jeu("sa012"), SBIRE_1PV], ["Puzzle.Attack('01001a')"],
       {"hors_jeu": ["01101"], "pret": ["01001a"], "defausse": ["sa012"]}, cibles=["01101"], accepter_choix=True),
    _c("sa012 Black Ops : le heros VAINC un complot ANNEXE (1 menace) -> meme effet",
       "« a minion OR side scheme »", [HEROS, _en_jeu("sa012"), SIDE_SCHEME, "Puzzle.SetThreat('01107', 1)"], ["Puzzle.Thwart('01001a')"],
       {"hors_jeu": ["01107"], "pret": ["01001a"], "defausse": ["sa012"]}, cibles=["01107"], accepter_choix=True),
    _c("sa012 Black Ops : TEMOIN, le sbire n'est PAS vaincu (3 PV, ATQ 2) -> Black Ops reste, le heros reste incline",
       "« defeats »", [HEROS, _en_jeu("sa012"), SBIRE], ["Puzzle.Attack('01001a')"],
       {"en_jeu": ["01101", "sa012"], "exhausted": ["01001a"]}, cibles=["01101"], accepter_choix=True),
    _c("sa012 Black Ops : TEMOIN, un ALLIE vainc le sbire (pas « your hero ») -> Black Ops reste, le heros reste incline",
       "« After YOUR HERO defeats »", [HEROS, ALLIE, _en_jeu("sa012"), SBIRE_1PV, HERO_FATIGUE], ["Puzzle.Attack('tl002')"],
       {"hors_jeu": ["01101"], "en_jeu": ["sa012"], "exhausted": ["01001a"]}, cibles=["01101"], accepter_choix=True),
]

MOJA_EN_JEU = "Puzzle.PutIntoPlay('sa017', under_control=True)"   # sa017 entre en jeu ET se camoufle (Reponse d'entree en jeu)
NINJA_ALLIE = "ub041"   # Raphael (NINJA, TURTLE ; aucun Response) : l'allie NINJA des cas de Shadow Summon / Up in Smoke

CAS += [
    # ===================================================================== sa013 Up in Smoke
    _c("sa013 Up in Smoke (Hero Action) : redresse un allie NINJA incline",
       "« Ready a NINJA ally » : Splinter (NINJA) incline est redresse ; evenement defausse",
       [HEROS, ALLIE, "Puzzle.Exhaust('tl002')"], [],
       {"pret": ["tl002"], "defausse": ["sa013"]}, main_exclusive=["sa013"], jouer=["sa013"], cibles=["tl002"], accepter_choix=True),
    _c("sa013 Up in Smoke : TEMOIN, un allie NON NINJA incline n'est pas une cible : l'Action n'est pas jouee (allie reste incline)",
       "Jessica Jones n'a pas le trait NINJA", [HEROS, AUTRE_ALLIE, "Puzzle.Exhaust('01059')"], [],
       {"exhausted": ["01059"], "en_main": ["sa013"]}, main_exclusive=["sa013"], jouer=["sa013"], accepter_choix=True),
    _c("sa013 Up in Smoke (Hero Interrupt) : un allie VAINCU par des degats retourne dans la MAIN de son proprietaire a la place de la defausse",
       "« When an ally would be discarded from play, return it to its owner's hand instead » : Splinter subit 5 degats (3 PV)",
       [HEROS, ALLIE], ["Puzzle.Damage('tl002', 5)"],
       {"hors_jeu": ["tl002"], "en_main": ["tl002"], "defausse": ["sa013"]}, main_exclusive=["sa013"], accepter_choix=True),
    _c("sa013 Up in Smoke (Hero Interrupt) : un allie defausse PAR UN EFFET retourne aussi en main",
       "« discarded from play » : pas seulement la defaite", [HEROS, ALLIE], ["Puzzle.Discard('tl002')"],
       {"hors_jeu": ["tl002"], "en_main": ["tl002"], "defausse": ["sa013"]}, main_exclusive=["sa013"], accepter_choix=True),
    _c("sa013 Up in Smoke : TEMOIN sans la carte : l'allie vaincu va a la DEFAUSSE",
       "ligne de base", [HEROS, ALLIE], ["Puzzle.Damage('tl002', 5)"],
       {"hors_jeu": ["tl002"], "defausse": ["tl002"]}, main_exclusive=["01088"], accepter_choix=True),
    _c("sa013 Up in Smoke : TEMOIN, un SBIRE defausse n'est pas un allie : la carte reste en main",
       "« an ally »", [HEROS, SBIRE], ["Puzzle.Discard('01101')"],
       {"hors_jeu": ["01101"], "en_main": ["sa013"]}, main_exclusive=["sa013"], accepter_choix=True),
    _c("sa013 Up in Smoke : TEMOIN, un allie defausse DE LA MAIN (pas « from play ») : la carte reste en main, l'allie va en defausse",
       "« discarded FROM PLAY »", [HEROS], ["Puzzle.Discard('tl002')"],
       {"defausse": ["tl002"], "en_main": ["sa013"]}, main_exclusive=["sa013", "tl002"], accepter_choix=True),
    _c("sa013 Up in Smoke : TEMOIN, forme ALTER-EGO : « Hero Interrupt » non proposee, l'allie va en defausse",
       "forme heros seulement", [ALLIE], ["Puzzle.Damage('tl002', 5)"],
       {"hors_jeu": ["tl002"], "defausse": ["tl002"], "en_main": ["sa013"]}, main_exclusive=["sa013"], accepter_choix=True),

    # ===================================================================== sa014 Hidden Passage
    _c("sa014 Hidden Passage (Alter-Ego Action) : incline, defausse la carte Cloaked de l'identite -> pioche 1",
       "« Exhaust Hidden Passage and discard a cloaked status card from your identity -> draw 1 card » : main vide + 1",
       [_en_jeu("sa014"), "Puzzle.Cloak('01001b')"] + DECK6 + ["Puzzle.EmptyHand()"], ["Puzzle.Action('sa014', 'AlterEgoAction', 0)"],
       {"taille_main": 1, "exhausted": ["sa014"], "statuts_absents": [["01001b", "Cloaked"]]}),
    _dispo("sa014 Hidden Passage : TEMOIN, identite NON camouflee -> l'Action n'est pas proposee",
           "le cout exige une carte Cloaked sur l'identite", [_en_jeu("sa014")], "sa014", "AlterEgoAction", 0),
    _dispo("sa014 Hidden Passage : TEMOIN, forme HEROS (identite camouflee) -> « Alter-Ego Action » non proposee",
           "forme alter-ego seulement", [HEROS, CLOAK, _en_jeu("sa014")], "sa014", "AlterEgoAction", 0),
    _dispo("sa014 Hidden Passage : TEMOIN D'EPUISEMENT, inclinee -> plus d'Action",
           "« Exhaust Hidden Passage » : un usage, puis 0 action meme si l'identite est de nouveau camouflee",
           [_en_jeu("sa014"), "Puzzle.Cloak('01001b')"] + DECK6, "sa014", "AlterEgoAction", 0,
           declencher=["Puzzle.Action('sa014', 'AlterEgoAction', 0)", "Puzzle.Cloak('01001b')"]),
    _dispo("sa014 Hidden Passage : alter-ego camoufle et soutien pret -> 1 action (temoin positif)",
           "montage complet", [_en_jeu("sa014"), "Puzzle.Cloak('01001b')"], "sa014", "AlterEgoAction", 1),
    _c("sa014 Hidden Passage (Hero Response) : apres un changement de forme vers la forme HEROS -> incline et camoufle l'identite",
       "« After you change form, exhaust Hidden Passage -> cloak your identity »", [_en_jeu("sa014")], ["Puzzle.ChangeForm('01001b')"],
       {"statuts": [["01001a", "Cloaked"]], "exhausted": ["sa014"]}, accepter_choix=True),
    _c("sa014 Hidden Passage : TEMOIN, changement vers la forme ALTER-EGO : la Reponse de heros n'est pas proposee",
       "« Hero Response » : forme heros seulement (le joueur est alter-ego apres le changement)", [HEROS, _en_jeu("sa014")],
       ["Puzzle.ChangeForm('01001a')"], {"statuts_absents": [["01001b", "Cloaked"]], "pret": ["sa014"]}, accepter_choix=True),
    _c("sa014 Hidden Passage : TEMOIN, deja inclinee : le changement de forme ne camoufle pas",
       "« exhaust Hidden Passage » est le cout", [_en_jeu("sa014"), "Puzzle.Exhaust('sa014')"], ["Puzzle.ChangeForm('01001b')"],
       {"statuts_absents": [["01001a", "Cloaked"]], "exhausted": ["sa014"]}, accepter_choix=True),
    _c("sa014 Hidden Passage : identite DEJA camouflee avant le changement : une seule carte Cloaked apres",
       "une seule Cloaked par personnage (la carte persiste ou est remplacee, jamais deux)",
       [_en_jeu("sa014"), "Puzzle.Cloak('01001b')"], ["Puzzle.ChangeForm('01001b')"],
       {"statuts": [["01001a", "Cloaked"]]}, accepter_choix=True, verifier="sn_un_seul_cloaked"),

    # ===================================================================== sa015 Kusari-Kagi
    _c("sa015 Kusari-Kagi : incline, defausse la carte Cloaked du heros -> 1 degat a un ennemi ET pioche 1",
       "« Exhaust this card and discard a cloaked status card from your hero -> deal 1 damage to an enemy and draw 1 card »",
       [HEROS, CLOAK, _en_jeu("sa015"), SBIRE] + DECK6 + ["Puzzle.EmptyHand()"], ["Puzzle.Action('sa015', 'HeroAction', 0)"],
       {"degats": [["01101", 1]], "taille_main": 1, "exhausted": ["sa015"], "statuts_absents": [["01001a", "Cloaked"]]}, cibles=["01101"]),
    _c("sa015 Kusari-Kagi : l'ennemi est VAINCU par le degat (1 PV) : la carte est piochee quand meme",
       "« deal 1 damage to an enemy AND draw 1 card » : les deux effets",
       [HEROS, CLOAK, _en_jeu("sa015"), SBIRE_1PV] + DECK6 + ["Puzzle.EmptyHand()"], ["Puzzle.Action('sa015', 'HeroAction', 0)"],
       {"hors_jeu": ["01101"], "taille_main": 1}, cibles=["01101"]),
    _c("sa015 Kusari-Kagi : « an enemy » : le VILAIN prend 1 degat",
       "pas seulement les sbires", [HEROS, CLOAK, _en_jeu("sa015")] + DECK6 + ["Puzzle.EmptyHand()"], ["Puzzle.Action('sa015', 'HeroAction', 0)"],
       {"degats": [["01094", 1]], "taille_main": 1}, cibles=["01094"]),
    _dispo("sa015 Kusari-Kagi : TEMOIN, la carte Cloaked est sur un ALLIE (pas « your hero ») -> pas proposee",
           "le cout vise le heros", [HEROS, ALLIE, "Puzzle.Cloak('tl002')", _en_jeu("sa015")], "sa015", "HeroAction", 0),
    _dispo("sa015 Kusari-Kagi : TEMOIN, heros sans Cloaked -> pas proposee",
           "cout impayable", [HEROS, _en_jeu("sa015")], "sa015", "HeroAction", 0),
    _dispo("sa015 Kusari-Kagi : TEMOIN D'EPUISEMENT, inclinee -> plus proposee meme si le heros est de nouveau camoufle",
           "« Exhaust this card »", [HEROS, CLOAK, _en_jeu("sa015")] + DECK6, "sa015", "HeroAction", 0,
           declencher=["Puzzle.Action('sa015', 'HeroAction', 0)", "Puzzle.Cloak('01001a')"], cibles=["01094"]),
    _dispo("sa015 Kusari-Kagi : Hero Action NON proposee en forme alter-ego",
           "forme heros seulement", ["Puzzle.Cloak('01001b')", _en_jeu("sa015")], "sa015", "HeroAction", 0),
    _dispo("sa015 Kusari-Kagi : heros camoufle et carte prete -> 1 action (temoin positif)",
           "montage complet", [HEROS, CLOAK, _en_jeu("sa015")], "sa015", "HeroAction", 1),
]

DECK_NINJA = ["Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01090', '01090', 'ub041', '01088', '01088')"]  # dessus : 2 Energy puis Raphael

CAS += [
    # ===================================================================== sa016 Shadow Summon
    _c("sa016 Shadow Summon : defausse du dessus jusqu'a un allie NINJA (2 cartes puis Raphael) et le met en jeu",
       "« Discard cards from the top of your deck until you discard a NINJA ally and put it into play » : 2 Energy en defausse, Raphael en jeu, 2 cartes restent",
       [HEROS] + DECK_NINJA, [],
       {"en_jeu": ["ub041"], "defausse": ["01088", "sa016"], "taille_deck_joueur": 2},
       main_exclusive=["sa016", "01088"], jouer=["sa016"], accepter_choix=True),
    _c("sa016 Shadow Summon : « If that ally is still in play at the end of the phase, add it to your hand » : fin de phase -> Raphael en MAIN",
       "controle a la fin de la PHASE des joueurs",
       [HEROS] + DECK_NINJA, ["Puzzle.EndPlayerPhase()"] if False else [],
       {"en_main": ["ub041"], "hors_jeu": ["ub041"]},
       main_exclusive=["sa016", "01088"], jouer=["sa016"], declencher_apres=["Puzzle.EndPlayerPhase()"], accepter_choix=True),
    _c("sa016 Shadow Summon : TEMOIN, l'allie est parti avant la fin de la phase (vaincu) : il reste en DEFAUSSE, pas en main",
       "« still in play »", [HEROS] + DECK_NINJA, [],
       {"hors_jeu": ["ub041"], "defausse": ["ub041"], "absent_main": ["ub041"]},
       main_exclusive=["sa016", "01088"], jouer=["sa016"], declencher_apres=["Puzzle.Damage('ub041', 20)", "Puzzle.EndPlayerPhase()"],
       accepter_choix=True),
    _c("sa016 Shadow Summon : « until you discard a NINJA ALLY » : un allie NON NINJA du dessus est defausse, pas mis en jeu",
       "Jessica Jones (non NINJA) est defaussee ; Raphael, dessous, entre en jeu",
       [HEROS, "Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01090', 'ub041', '01059')"], [],
       {"en_jeu": ["ub041"], "hors_jeu": ["01059"], "defausse": ["01059"], "taille_deck_joueur": 1},
       main_exclusive=["sa016", "01088"], jouer=["sa016"], accepter_choix=True),
    _c("sa016 Shadow Summon : TEMOIN, aucun allie NINJA nulle part : aucun allie n'entre en jeu (l'allie non NINJA du deck est defausse, pas joue)",
       "« until you discard a NINJA ally » : le deck s'epuise sans allie NINJA ; le moteur remelange alors la defausse dans le deck "
       "(`DiscardUntil`, comportement du moteur commun a `22009` Combat Ready) : on ne mesure que ce que la carte promet",
       [HEROS, "Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01090', '01090', '01059')"], [],
       {"hors_jeu": ["01059"], "defausse": ["sa016"]},
       main_exclusive=["sa016", "01088"], jouer=["sa016"], accepter_choix=True),
    _c("sa016 Shadow Summon : « Action » : jouable aussi en forme ALTER-EGO",
       "les deux formes", [] + DECK_NINJA, [],
       {"en_jeu": ["ub041"], "defausse": ["sa016"]}, main_exclusive=["sa016", "01088"], jouer=["sa016"], accepter_choix=True),

    # ===================================================================== sa017 Moja
    _c("sa017 Moja (Response) : apres son entree en jeu, elle est camouflee",
       "« After Moja enters play, cloak her » : jouee depuis la main, cout 3 (Energy YY + Strength RR)",
       [HEROS], [],
       {"en_jeu": ["sa017"], "statuts": [["sa017", "Cloaked"]]},
       main_exclusive=["sa017", "01088", "01090"], jouer=["sa017"], accepter_choix=True),
    _c("sa017 Moja : valeurs imprimees (3 PV) : sans carte Cloaked, 2 degats -> 2 degats poses (la Reponse d'entree en jeu l'a camouflee : on la retire)",
       "PV 3 : 2 degats -> 2 degats poses, 1 PV restant ; `Puzzle.PutIntoPlay` declenche la Reponse d'entree en jeu (Moja camouflee), `Puzzle.Cloak` "
       "BASCULE : second appel = retrait", [HEROS, MOJA_EN_JEU, "Puzzle.Cloak('sa017')"], ["Puzzle.Damage('sa017', 2)"],
       {"degats": [["sa017", 2]], "statuts_absents": [["sa017", "Cloaked"]]}),
    _c("sa017 Moja (Response 2) : apres des degats CONSEQUENTIELS (1 par etoile), elle defausse une carte Ninjutsu de la main et est camouflee",
       "Moja (sans Cloaked) attaque Rhino (ATQ 1) : 1 degat consecutif, puis « discard a Ninjutsu card from your hand -> cloak Moja » "
       "(Moonlighting tj005 est Jennika ET Ninjutsu : une carte Dual/signature compte pour sa classe Ninjutsu)",
       [HEROS, MOJA_EN_JEU, "Puzzle.Cloak('sa017')"], ["Puzzle.Attack('sa017')"],
       {"degats": [["sa017", 1], ["01094", 1]], "statuts": [["sa017", "Cloaked"]], "defausse": ["tj005"]},
       main_exclusive=["tj005"], accepter_choix=True),
    _c("sa017 Moja : TEMOIN, aucune carte Ninjutsu en main (une carte TAIJUTSU) : la Reponse n'est pas proposee, elle n'est pas camouflee",
       "« a NINJUTSU card » : Decisive Strike (tj004) est Taijutsu, pas Ninjutsu", [HEROS, MOJA_EN_JEU, "Puzzle.Cloak('sa017')"],
       ["Puzzle.Attack('sa017')"],
       {"degats": [["sa017", 1]], "statuts_absents": [["sa017", "Cloaked"]], "en_main": ["tj004"]},
       main_exclusive=["tj004"], accepter_choix=True),
    _c("sa017 Moja : DEJA camouflee qui attaque : le +2 ATQ consomme la carte AVANT les degats consecutifs, puis la Reponse la remet",
       "livret p.8 : « Consequential damage resolves last, so the Cloaked status card would first give the +2 THW/ATK, and would be discarded "
       "before the consequential damage occurs » : Rhino 3 degats (1 + 2), Moja 1 degat consecutif (pas evite), puis nouvelle Cloaked "
       "(cout : une carte Ninjutsu)",
       [HEROS, MOJA_EN_JEU], ["Puzzle.Attack('sa017')"],
       {"degats": [["sa017", 1], ["01094", 3]], "statuts": [["sa017", "Cloaked"]], "defausse": ["tj005"]},
       main_exclusive=["tj005"], accepter_choix=True),
    _c("sa017 Moja : TEMOIN, Moja CORIACE : la Coriace absorbe les degats consecutifs, elle n'en « subit » pas -> pas de Reponse",
       "« After Moja TAKES consequential damage » : rien n'est subi", [HEROS, "Puzzle.PutIntoPlay('sa017', under_control=True)", "Puzzle.Tough('sa017')"],
       ["Puzzle.Attack('sa017')"],
       {"degats": [["sa017", 0]], "statuts_absents": [["sa017", "Cloaked"]], "en_main": ["tj005"]},
       main_exclusive=["tj005"], accepter_choix=True),

    # ===================================================================== sa018 Smokescreen
    _c("sa018 Smokescreen : identite camouflee -> cout reduit de 1 (cout 0, jouee sans ressource)",
       "« Reduce the cost to play this card by 1 if your identity is cloaked » : aucune ressource en main",
       [HEROS, CLOAK], [], {"en_jeu": ["sa018"]}, main_exclusive=["sa018"], jouer=["sa018"], accepter_choix=True),
    _c("sa018 Smokescreen : TEMOIN, identite NON camouflee -> cout 1, injouable sans ressource (reste en main)",
       "pas de reduction", [HEROS], [], {"en_main": ["sa018"], "hors_jeu": ["sa018"]},
       main_exclusive=["sa018"], jouer=["sa018"], accepter_choix=True),
    _c("sa018 Smokescreen : « your IDENTITY » : une identite ALTER-EGO camouflee suffit (cout 0)",
       "pas « your hero » ; ⚠ Peter Parker genere lui-meme une ressource [mental] (Scientist) : on lui INTERDIT de payer (`ne_pas_depenser`), "
       "sinon le cas resterait vert sans la reduction de cout",
       ["Puzzle.Cloak('01001b')"], [], {"en_jeu": ["sa018"]},
       main_exclusive=["sa018"], ne_pas_depenser=["01001b"], jouer=["sa018"], accepter_choix=True),
    _c("sa018 Smokescreen (Hero Interrupt) : attaque de Rhino (ATQ 4) sur le heros incline : 2 degats evites, la carte est defaussee",
       "« When an enemy attack would deal damage to a friendly character, discard this card -> prevent 2 of that damage » : 4 - 2 = 2",
       [HEROS, HERO_FATIGUE, _en_jeu("sa018")] + DEUX_ICONES, ["Puzzle.Attack('01094')"],
       {"degats_identite": 2, "defausse": ["sa018"]}, accepter_choix=True, avec_boost=True),
    _c("sa018 Smokescreen : TEMOIN sans la carte : la meme attaque inflige 4 degats",
       "ligne de base", [HEROS, HERO_FATIGUE] + DEUX_ICONES, ["Puzzle.Attack('01094')"],
       {"degats_identite": 4}, accepter_choix=True, avec_boost=True),
    _c("sa018 Smokescreen : « prevent 2 OF THAT DAMAGE » : une attaque de 2 seulement est entierement evitee (0 degat), pas 2 de plus",
       "ATQ 2 (sans icone) : tout est evite", [HEROS, HERO_FATIGUE, _en_jeu("sa018")], ["Puzzle.Attack('01094')"],
       {"degats_identite": 0, "defausse": ["sa018"]}, accepter_choix=True),
    _c("sa018 Smokescreen : « a FRIENDLY character » : un ALLIE qui defend est protege (Rhino 2 -> 0 degat sur Splinter)",
       "pas seulement l'identite", [HEROS, ALLIE, _en_jeu("sa018")], ["Puzzle.Defend('tl002', '01094')"],
       {"degats": [["tl002", 0]], "defausse": ["sa018"]}, accepter_choix=True),
    _c("sa018 Smokescreen : TEMOIN, des degats qui ne viennent PAS d'une attaque ennemie (3 degats directs) : la carte reste en jeu",
       "« an enemy ATTACK »", [HEROS, _en_jeu("sa018")], ["Puzzle.Damage('01001a', 3)"],
       {"degats_identite": 3, "en_jeu": ["sa018"]}, accepter_choix=True),
    _c("sa018 Smokescreen : TEMOIN, forme ALTER-EGO : « Hero Interrupt » non proposee, 2 degats subis, la carte reste en jeu",
       "forme heros seulement", [_en_jeu("sa018")], ["Puzzle.Attack('01094')"],
       {"degats_identite": 2, "en_jeu": ["sa018"]}, accepter_choix=True),

    # ===================================================================== sa019 Gaslight
    _c("sa019 Gaslight (choix 1) : defausse la carte Cloaked du heros -> retire 3 menaces d'un complot (5 -> 2)",
       "« Discard a cloaked status card from your hero -> choose: Remove 3 threat from a scheme »",
       [HEROS, CLOAK, "Puzzle.EmptyHand()", "Puzzle.SetThreat('01097b', 5)"], [],
       {"menace": [["01097b", 2]], "statuts_absents": [["01001a", "Cloaked"]], "defausse": ["sa019"]},
       main_exclusive=["sa019", "01089"], jouer=["sa019"], preferer_option="Remove 3", cibles=["01097b"], accepter_choix=True),
    _c("sa019 Gaslight (choix 2) : Rhino est DESORIENTE (Confused), aucune menace retiree",
       "« Confuse an enemy » : l'autre branche ; une seule branche (la menace reste a 5)",
       [HEROS, CLOAK, "Puzzle.EmptyHand()", "Puzzle.SetThreat('01097b', 5)"], [],
       {"statuts": [["01094", "Confused"]], "menace": [["01097b", 5]], "statuts_absents": [["01001a", "Cloaked"]]},
       main_exclusive=["sa019", "01089"], jouer=["sa019"], preferer_option="Confuse", cibles=["01094"], accepter_choix=True),
    _jouable("sa019 Gaslight : TEMOIN, heros NON camoufle -> injouable",
             "le cout exige une carte Cloaked sur le heros", [HEROS], "sa019", False, main_exclusive=["sa019", "01089"]),
    _jouable("sa019 Gaslight : TEMOIN, seule un ALLIE est camoufle (pas « your hero ») -> injouable",
             "le cout vise le heros", [HEROS, ALLIE, "Puzzle.Cloak('tl002')"], "sa019", False, main_exclusive=["sa019", "01089"]),
    _jouable("sa019 Gaslight : TEMOIN, forme ALTER-EGO (identite camouflee) -> injouable (« Hero Action », pas de heros)",
             "forme heros seulement", ["Puzzle.Cloak('01001b')"], "sa019", False, main_exclusive=["sa019", "01089"]),
    _jouable("sa019 Gaslight : heros camoufle -> jouable (temoin positif)",
             "montage complet", [HEROS, CLOAK], "sa019", True, main_exclusive=["sa019", "01089"]),

    # ===================================================================== sa020 From the Shadows
    _c("sa020 From the Shadows : depensee pour jouer une carte NINJUTSU (Cut-and-Run) -> le heros est camoufle",
       "« After you spend this card to play a Ninjutsu card, cloak your hero » : Cut-and-Run (cout 2) payee par la ressource [wild] + Energy ; "
       "il frappe Rhino sans le vaincre : le Cloaked vient bien de la ressource",
       [HEROS], [],
       {"statuts": [["01001a", "Cloaked"]], "defausse": ["sa020", "sa006"]},
       main_exclusive=["sa006", "sa020", "01088"], payer_avec=["sa020", "01088"], jouer=["sa006"], cibles=["01094"], accepter_choix=True),
    _c("sa020 From the Shadows : TEMOIN, depensee pour une carte NON Ninjutsu (Swinging Web Kick 01005) -> pas de Cloaked",
       "« to play a NINJUTSU card »", [HEROS], [],
       {"statuts_absents": [["01001a", "Cloaked"]], "defausse": ["sa020", "01005"]},
       main_exclusive=["01005", "sa020", "01088"], payer_avec=["sa020", "01088"], jouer=["01005"], cibles=["01094"], accepter_choix=True),
    _c("sa020 From the Shadows : TEMOIN, la carte Ninjutsu est payee SANS la ressource (Energy seule) -> pas de Cloaked, sa020 reste en main",
       "« After you spend THIS card »", [HEROS], [],
       {"statuts_absents": [["01001a", "Cloaked"]], "en_main": ["sa020"]},
       main_exclusive=["sa006", "sa020", "01088"], payer_avec=["01088"], ne_pas_depenser=["sa020"], jouer=["sa006"], cibles=["01094"],
       accepter_choix=True),
    _c("sa020 From the Shadows : TEMOIN, forme ALTER-EGO : « Hero Response » non proposee (Shadow Summon payee par la ressource)",
       "forme heros seulement", [] + DECK_NINJA, [],
       {"statuts_absents": [["01001b", "Cloaked"]], "defausse": ["sa020", "sa016"]},
       main_exclusive=["sa016", "sa020"], payer_avec=["sa020"], jouer=["sa016"], accepter_choix=True),
]

VERIFICATIONS = r'''
def sn_jouable(monde, aides):
    """`attendu` : carte (en main), jouable (bool attendu de `CanPlayBy`)."""
    attendu = aides["cas"]["attendu"]
    joueur = monde.players[0]
    code = attendu["carte"]
    main = [f for f in joueur.hand_cards.GetAll() if getattr(f.paper, "card_id", None) == code]
    if not main:
        return False, f"{code} absente de la main"
    jouable = bool(main[0].CanPlayBy(joueur))
    if jouable != attendu["jouable"]:
        return False, f"{code} jouable={jouable} (attendu {attendu['jouable']})"
    reste = {k: v for k, v in attendu.items() if k in CLES_ETAT_ATTENDU}
    if reste:
        aides2 = dict(aides); aides2["cas"] = dict(aides["cas"], attendu=reste)
        ok, msg = etat_attendu(monde, aides2)
        return ok, f"{code} jouable={jouable} ; {msg}"
    return True, f"{code} jouable={jouable}, comme attendu"


def sn_a_regarde(monde, aides):
    """`attendu` : deck (rencontre|joueur|autre), vus (nombre de cartes du dessus devenues visibles du joueur),
    taille (facultatif) ; le reste (statuts, defausse...) est delegue a etat_attendu."""
    from game.operate.worlds import Worlds
    attendu = aides["cas"]["attendu"]
    joueur = monde.players[0]
    if attendu["deck"] == "rencontre":
        cartes = list(Worlds.GetEncounterDeckCards(monde))
    elif attendu["deck"] == "joueur":
        cartes = list(joueur.player_deck.Get(True))
    else:
        cartes = list(monde.players[1].player_deck.Get(True))
    visibles = [f.card.visible.IsVisible(joueur) for f in cartes]
    n = attendu["vus"]
    if len(cartes) < n + 1:
        return False, f"deck trop court pour la mesure ({len(cartes)} cartes)"
    # Les cartes regardees ne sont plus forcement dessus (elles sont remises en haut et/ou en bas) : on mesure donc
    # l'ENSEMBLE des cartes visibles (exactement `vus`, et ce sont les `ids_vus` quand le cas les donne).
    vues = sorted(getattr(f.paper, "card_id", "?") for f, v in zip(cartes, visibles) if v)
    if len(vues) != n:
        return False, f"{len(vues)} carte(s) visible(s) {vues} (attendu {n}) : {visibles}"
    if attendu.get("ids_vus") and vues != sorted(attendu["ids_vus"]):
        return False, f"cartes visibles {vues} (attendu {sorted(attendu['ids_vus'])})"
    ids = [getattr(f.paper, "card_id", "?") for f in cartes]
    # `cartes[0]` est le DESSUS du deck. `dessus` : la carte du dessus ; `dessous` : les cartes du fond (ensemble).
    if attendu.get("dessus") and ids[0] != attendu["dessus"]:
        return False, f"dessus du deck = {ids[0]} (attendu {attendu['dessus']}) ; deck {ids}"
    if attendu.get("dessous") and sorted(ids[-len(attendu["dessous"]):]) != sorted(attendu["dessous"]):
        return False, f"fond du deck = {ids[-len(attendu['dessous']):]} (attendu {attendu['dessous']}) ; deck {ids}"
    if "taille" in attendu and len(cartes) != attendu["taille"]:
        return False, f"le deck a {len(cartes)} cartes (attendu {attendu['taille']}) : une carte a bouge"
    reste = {k: v for k, v in attendu.items() if k in CLES_ETAT_ATTENDU}
    aides2 = dict(aides); aides2["cas"] = dict(aides["cas"], attendu=reste)
    ok, msg = etat_attendu(monde, aides2)
    return ok, f"visibles={visibles} ; {msg}"


def sn_un_seul_cloaked(monde, aides):
    """L'identite porte EXACTEMENT une carte Cloaked (jamais deux) ; le reste est delegue a etat_attendu."""
    n = aides["identite"](monde).cloaked
    if n != 1:
        return False, f"l'identite porte {n} carte(s) Cloaked (attendu exactement 1)"
    return etat_attendu(monde, aides)


def sn_actions_disponibles(monde, aides):
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
