# Cas test_capacites du pack d'aspect TMNT JUSTICE (Inkwire, prefixe `uj`, pack `tmnt_aspect_justice`).
# Filtre : `[uj]`. Gabarits PROCESSUS-CARTE : .planning/tmnt/aspects-justice-gabarits.md.
#
# Deux familles :
#  - les RESKINS (scan IDENTIQUE a une officielle, `ability_link`, aucun script) : un cas sur la carte
#    TMNT et un TEMOIN identique sur l'officielle, meme chiffre attendu (RECETTES-MOTEUR §11) ;
#  - les cartes MODIFIEES ou NOUVELLES, scriptees dans src/cards/pack/tmnt_aspect_justice/.
#
# Conventions (reprises de tools/cas/rampage.py) :
#  - Spider-Man (01001) demarre en ALTER EGO ; HEROS le met en forme heros (01001a) ;
#  - `main_exclusive` : la main ne contient QUE la carte jouee et de quoi payer
#    (01088 Energy = [energy], 01089 Genius = [mental], 01090 Strength = [physical], 01087 = [wild]) ;
#  - Rhino 01094 (14 PV), sa manigance principale 01097b, ses manigances annexes 01107 / 01108 ;
#  - 01101 Hydra Mercenary (3 PV) est le sbire de mesure.
SC = "rhino"
HEROS = "Puzzle.ChangeForm('01001b')"
SANS_DECK = "Puzzle.EmptyPlayerDeck()"
DECK6 = "Puzzle.CreatePlayerDeck('01089', '01089', '01089', '01089', '01089', '01089')"


def _c(nom, pourquoi, mise, declencher, attendu, **cle):
    # La main de depart est VIDEE juste apres le changement de forme : sinon le pilote, qui accepte la premiere
    # option jouable, y joue des Interruptions pendant la mise en place (constate : `Puzzle.SetThreat` sur
    # 01097b ouvrait une fenetre ou une carte de la main de Spider-Man ramenait la menace a 0).
    mise = list(mise)
    rang = 1 if mise and mise[0].startswith("Puzzle.ChangeForm") else 0
    if cle.pop("garder_main", False) is False:
        mise.insert(rang, "Puzzle.EmptyHand()")
    cas = {"nom": "[uj] " + nom, "pourquoi": pourquoi, "scenario": cle.pop("scenario", SC),
           "heros": cle.pop("heros", "spider_man"), "mise_en_place": mise, "declencher": list(declencher),
           "verifier": cle.pop("verifier", "etat_attendu"), "attendu": attendu}
    cas.update(cle)
    return cas


def _paire(tmnt, officielle, libelle, pourquoi, mise, declencher, attendu, **cle):
    """Un cas sur le reskin TMNT + le TEMOIN identique sur l'officielle (chaque card_id est remplace
    partout : mise en place, declencheurs, attendu, main, jouer, cibles)."""
    import json

    def sub(obj, de, vers):
        return json.loads(json.dumps(obj).replace(de, vers))

    cas_tmnt = _c(f"{tmnt} {libelle} (reskin de {officielle})", pourquoi, mise, declencher, attendu, **dict(cle))
    temoin = _c(f"{tmnt} TEMOIN {officielle} (officielle) : {libelle}",
                "le reskin doit rendre EXACTEMENT le meme chiffre que l'original",
                sub(mise, tmnt, officielle), sub(declencher, tmnt, officielle), sub(attendu, tmnt, officielle),
                **sub(dict(cle), tmnt, officielle))
    return [cas_tmnt, temoin]


CAS = []

# ================================================================== RESKINS (ability_link)
CAS += _paire(
    "uj001", "58016", "Battlefield Benevolence : soigne 2 degats de Rhino puis le desoriente",
    "« Heal 2 damage from an enemy → confuse that enemy » : Rhino a 3 degats -> 1, statut Confused",
    [HEROS, "Puzzle.Damage('01094', 3)"], [],
    {"degats": [["01094", 1]], "statuts": [["01094", "Confused"]], "defausse": ["uj001"]},
    main_exclusive=["uj001", "01090"], jouer=["uj001"], cibles=["01094"])
CAS += _paire(
    "uj003", "04049", "Clear the Area : retire 2 menaces et pioche 1 (derniere menace retiree)",
    "« Remove 2 threat ... If this removes the last threat on that scheme, draw 1 card » : 2 -> 0, main 0 -> 1",
    [HEROS, "Puzzle.SetThreat('01097b', 2)"], [],
    {"menace": [["01097b", 0]], "taille_main": 1, "defausse": ["uj003"]},
    main_exclusive=["uj003", "01089"], jouer=["uj003"], cibles=["01097b"])
CAS += _paire(
    "uj007", "47013", "Disguise : Action, incliner Disguise et l'identite -> 2 menaces retirees",
    "« Exhaust Disguise and your identity → remove 2 threat from a scheme » : 5 -> 3, les deux inclines",
    [HEROS, "Puzzle.PutIntoPlay('uj007', under_control=True)", "Puzzle.SetThreat('01097b', 5)"],
    ["Puzzle.Action('uj007')"],
    {"menace": [["01097b", 3]], "exhausted": ["uj007", "01001a"]},
    cibles=["01097b"])
CAS += _paire(
    "uj010", "41017", "Float Like a Butterfly : +1 degat a une attaque contre un ennemi desoriente",
    "« When a character you control attacks a confused enemy, increase the amount of damage ... by 1 » : "
    "Spider-Man ATK 2 -> 3 degats sur Rhino desoriente",
    [HEROS, "Puzzle.PutIntoPlay('uj010', under_control=True)", "Puzzle.Confuse('01094')"],
    ["Puzzle.Attack('01001a')"],
    {"degats": [["01094", 3]]}, cibles=["01094"], accepter_choix=True)
CAS += _paire(
    "uj011", "01060", "For Justice! paye en [mental] : 4 menaces retirees au lieu de 3",
    "« Remove 3 threat (4 threat instead if you paid for this card using a [mental] resource) » : 6 -> 2",
    [HEROS, "Puzzle.SetThreat('01097b', 6)"], [],
    {"menace": [["01097b", 2]]},
    main_exclusive=["uj011", "01089"], jouer=["uj011"], cibles=["01097b"])
CAS += _paire(
    "uj011", "01060", "For Justice! paye SANS [mental] : 3 menaces seulement",
    "contre-cas de la parenthese : paye en [physical], 6 -> 3",
    [HEROS, "Puzzle.SetThreat('01097b', 6)"], [],
    {"menace": [["01097b", 3]]},
    main_exclusive=["uj011", "01090"], jouer=["uj011"], cibles=["01097b"])
CAS += _paire(
    "uj013", "58021", "Heroic Conditioning : +3 PV au joueur, +1 THW au heros",
    "« You get +3 hit points and your hero gets +1 THW »",
    [HEROS, "Puzzle.PutIntoPlay('uj013', under_control=True)"], [],
    {"attributs": {"health": 3, "thwart": 1}})
CAS += _paire(
    "uj014", "01065", "Heroic Intuition : +1 THW au heros",
    "« Your hero gets +1 THW »",
    [HEROS, "Puzzle.PutIntoPlay('uj014', under_control=True)"], [],
    {"attributs": {"thwart": 1}})
CAS += _paire(
    "uj015", "61036", "Innate Perception : +1 THW au heros",
    "« Your hero gets +1 THW » (le mot-cle Starting est porte par le meme module : voir le gabarit)",
    [HEROS, "Puzzle.PutIntoPlay('uj015', under_control=True)"], [],
    {"attributs": {"thwart": 1}})
CAS += _paire(
    "uj017", "60023", "Know Your Enemy : retire 1 menace, puis 1 menace (deux choix)",
    "« Remove 1 threat from a scheme. Remove 1 threat from a scheme. » : 5 -> 3",
    [HEROS, "Puzzle.SetThreat('01097b', 5)"], [],
    {"menace": [["01097b", 3]], "defausse": ["uj017"]},
    main_exclusive=["uj017", "01089"], jouer=["uj017"], cibles=["01097b"])
CAS += _paire(
    "uj017", "60023", "Know Your Enemy : Discount 1 (MARTIAL ARTIST controle) -> jouable SANS ressource",
    "« [star] Discount 1 (Martial Artist) » : Daredevil 60039 (MARTIAL ARTIST) en jeu, la main ne contient que "
    "la carte (cout 1 -> 0) ; elle est jouee et resout",
    [HEROS, "Puzzle.PutIntoPlay('60039', under_control=True)", "Puzzle.SetThreat('01097b', 5)"], [],
    {"menace": [["01097b", 3]], "defausse": ["uj017"]},
    main_exclusive=["uj017"], jouer=["uj017"], cibles=["01097b"])
CAS += _paire(
    "uj022", "60027", "Move in Shadow : jouee, sa propre Reponse retire 1 menace",
    "« After you play a card (including this one), remove 1 threat from a scheme » : 5 -> 4",
    [HEROS, "Puzzle.SetThreat('01097b', 5)"], [],
    {"menace": [["01097b", 4]], "en_jeu": ["uj022"]},
    main_exclusive=["uj022", "01088"], jouer=["uj022"], cibles=["01097b"])
CAS += _paire(
    "uj023", "08011", "Night-Blade : entre en jeu -> va chercher une carte PREPARATION dans le deck",
    "« search your deck and discard pile for a Preparation card and add it to your hand » : 08018 Spycraft "
    "(PREPARATION) au fond d'un deck de Genius",
    [HEROS, SANS_DECK, "Puzzle.CreatePlayerDeck('01089', '01089', '08018', '01089')"], [],
    {"en_main": ["08018"], "en_jeu": ["uj023"]},
    main_exclusive=["uj023", "01089", "01088"], jouer=["uj023"], accepter_choix=True)
CAS += _paire(
    "uj024", "22015", "One Way or Another : revele une manigance annexe du deck rencontre -> pioche 3",
    "« Search the encounter deck for a side scheme. Reveal that side scheme → draw 3 cards » : 01107 en jeu, main 3",
    [HEROS, "Puzzle.CreateEncounterDeck('01104', '01107', '01104')"], [],
    {"en_jeu": ["01107"], "taille_main": 3, "defausse": ["uj024"]},
    main_exclusive=["uj024"], jouer=["uj024"], accepter_choix=True)
CAS += _paire(
    "uj025", "30019", "Overwatch : 1 menace contree sur la manigance principale -> 1 retiree d'une AUTRE manigance",
    "« When any amount of threat is removed from attached scheme by a thwart, discard this card → remove an equal "
    "amount of threat from a different scheme » : Spider-Man THW 1 sur 01097b, 01107 3 -> 2, Overwatch defaussee",
    [HEROS, "Puzzle.Reveal('01107')", "Puzzle.SetThreat('01107', 3)", "Puzzle.SetThreat('01097b', 5)",
     "Puzzle.PutIntoPlay('uj025', under_control=True)", "Puzzle.Attach('uj025', '01097b')"],
    ["Puzzle.Thwart('01001a')"],
    {"menace": [["01097b", 4], ["01107", 2]], "hors_jeu": ["uj025"]},
    cibles=["01097b", "01107"], accepter_choix=True)
CAS += _paire(
    "uj029", "04047", "Skilled Investigator : manigance annexe vaincue -> incliner -> piocher 1",
    "« After a side scheme is defeated, exhaust Skilled Investigator → draw 1 card » : 01107 a 1 menace, contree",
    [HEROS, "Puzzle.PutIntoPlay('uj029', under_control=True)", "Puzzle.Reveal('01107')",
     "Puzzle.SetThreat('01107', 1)", "Puzzle.EmptyHand()"],
    ["Puzzle.Thwart('01001a')"],
    {"hors_jeu": ["01107"], "taille_main": 1, "exhausted": ["uj029"]},
    cibles=["01107"], accepter_choix=True)
CAS += _paire(
    "uj030", "08013", "Stealth Strike : 4 degats tuent le sbire -> 2 menaces retirees",
    "« Deal 4 damage to an enemy. If that enemy is defeated by this attack, remove 2 threat from a scheme »",
    [HEROS, "Puzzle.PutIntoPlay('01101')", "Puzzle.SetThreat('01097b', 5)"], [],
    {"hors_jeu": ["01101"], "menace": [["01097b", 3]]},
    main_exclusive=["uj030", "01089", "01089"], jouer=["uj030"], cibles=["01101", "01097b"])
CAS += _paire(
    "uj031", "60028", "Stealth Training : contrer et vaincre EXACTEMENT une manigance annexe -> etourdir Rhino",
    "« After you thwart and exactly defeat a side scheme, exhaust Stealth Training → stun an enemy » : 01107 a 1 "
    "menace, Spider-Man THW 1",
    [HEROS, "Puzzle.PutIntoPlay('uj031', under_control=True)", "Puzzle.Reveal('01107')",
     "Puzzle.SetThreat('01107', 1)"],
    ["Puzzle.Thwart('01001a')"],
    {"hors_jeu": ["01107"], "statuts": [["01094", "Stunned"]], "exhausted": ["uj031"]},
    cibles=["01107", "01094"], accepter_choix=True)
CAS += _paire(
    "uj032", "47015", "Three Steps Ahead : paye en [mental] + [physical] (2 types) -> 2 x 2 menaces",
    "« For each different resource type you used to pay for this card, choose a scheme and remove 2 threat » : "
    "deux types, deux manigances a 2 retraits",
    [HEROS, "Puzzle.Reveal('01107')", "Puzzle.SetThreat('01107', 3)", "Puzzle.SetThreat('01097b', 5)"], [],
    {"menace": [["01097b", 3], ["01107", 1]]},
    main_exclusive=["uj032", "01089", "01090"], jouer=["uj032"], cibles=["01097b", "01107"])
CAS += _paire(
    "uj035", "06031", "Under Surveillance : seuil de la manigance principale +4",
    "« Increase the target threat value of attached scheme by 4 »",
    [HEROS, "Puzzle.PutIntoPlay('uj035', under_control=True)", "Puzzle.Attach('uj035', '01097b')"], [],
    {"attributs_carte": [["01097b", "target_threat", 4]]})
CAS += _paire(
    "uj040", "21050", "Zone of Silence (identite MYSTIC) : defausse 4 du deck -> 4 menaces retirees",
    "« discard up to 4 cards from the top of your deck → remove 1 threat from that scheme for each card discarded » : "
    "le pilote choisit 4 ; ligne de base du deck : la partie de Doctor Strange en retire deja 1 des 6 (mesure : "
    "choix « 1 » -> 4 restantes), donc 6 - 1 - 4 = 1",
    ["Puzzle.ChangeForm('09001b')", SANS_DECK, DECK6, "Puzzle.SetThreat('01097b', 6)"], [],
    {"menace": [["01097b", 2]], "taille_deck_joueur": 1},
    heros="doctor_strange", main_exclusive=["uj040", "01089"], jouer=["uj040"], cibles=["01097b"],
    choisir_option="4")
CAS += _paire(
    "uj040", "21050", "Zone of Silence : Spider-Man (pas MYSTIC) ne peut PAS la jouer",
    "« Play only if your identity has the Mystic trait »",
    [HEROS, "Puzzle.Gain('uj040')"], [],
    {"carte": "uj040", "jouable": False, "en_jeu": 0},
    main=["01089", "01089"], verifier="max_par_joueur_jouable")
CAS += _paire(
    "uj036", "51014", "Venus : entre en jeu -> le joueur choisi va chercher une manigance JOUEUR dans son deck",
    "« That player searches their deck and a discard pile for a player side scheme and adds it to their hand » : "
    "40018 Call for Backup au milieu d'un deck de Genius (lecture codee = Manifold, question Q-uj036 ouverte)",
    [HEROS, SANS_DECK, "Puzzle.CreatePlayerDeck('01089', '40018', '01089')"], [],
    {"en_main": ["40018"], "en_jeu": ["uj036"]},
    main_exclusive=["uj036", "01088", "01089"], jouer=["uj036"], accepter_choix=True)
CAS += [
    _c("uj024 One Way or Another : Max 1 per round, TEMOIN D'EPUISEMENT : la 2e copie n'est PAS jouable le meme round",
       "« Max 1 per round » : une copie jouee, la seconde (deux manigances annexes encore dans le deck) est refusee",
       [HEROS, "Puzzle.CreateEncounterDeck('01107', '01108', '01104')", "Puzzle.CreateHandCards('uj024', 'uj024')"],
       [], {"carte": "uj024", "jouable": False, "en_jeu": 0},
       jouer=["uj024"], accepter_choix=True, verifier="max_par_joueur_jouable"),
    _c("uj024 One Way or Another : contre-cas, sans copie jouee ce round la carte est jouable",
       "c'est bien la copie deja jouee qui bloque la seconde",
       [HEROS, "Puzzle.CreateEncounterDeck('01107', '01108', '01104')", "Puzzle.CreateHandCards('uj024', 'uj024')"],
       [], {"carte": "uj024", "jouable": True, "en_jeu": 0}, verifier="max_par_joueur_jouable"),
    _c("uj007 Disguise : Max 1 per player, une copie en jeu -> la 2e n'est PAS jouable",
       "« Max 1 per player » (MaxPerUnit 1 recopie de 47013 : donnee, ne vient pas par ability_link)",
       [HEROS, "Puzzle.Gain('uj007')", "Puzzle.PutIntoPlay('uj007', under_control=True)"], [],
       {"carte": "uj007", "jouable": False, "en_jeu": 1},
       main=["01088", "01089"], verifier="max_par_joueur_jouable"),
]

# Bandeaux « ✦ <titre d'origine> » (decision Q-R1) : l'officielle en jeu bloque la carte TMNT, et inversement.
for _tmnt, _orig, _nom in [("uj023", "08011", "Agent Coulson"), ("uj026", "61016", "Spider-Woman"),
                           ("uj028", "60021", "Dagger"), ("uj036", "51014", "Manifold"),
                           ("uj038", "60020", "Cloak"), ("uj039", "61017", "Squirrel Girl")]:
    CAS += [
        _c(f"{_tmnt} bandeau « ✦ {_nom} » : {_orig} en jeu -> {_tmnt} PAS jouable",
           "decision Q-R1 : l'unicite se juge sur les deux titres (`unique_also`)",
           [HEROS, f"Puzzle.Gain('{_tmnt}')", f"Puzzle.PutIntoPlay('{_orig}', under_control=True)"], [],
           {"carte": _tmnt, "jouable": False, "en_jeu": 0},
           main=["01088", "01089", "01088"], verifier="max_par_joueur_jouable"),
        _c(f"{_tmnt} bandeau : sens inverse, {_tmnt} en jeu -> {_orig} PAS jouable",
           "le titre secondaire bloque dans les deux sens",
           [HEROS, f"Puzzle.Gain('{_orig}')", f"Puzzle.PutIntoPlay('{_tmnt}', under_control=True)"], [],
           {"carte": _orig, "jouable": False, "en_jeu": 0},
           main=["01088", "01089", "01088"], verifier="max_par_joueur_jouable"),
        _c(f"{_tmnt} bandeau : TEMOIN, sans {_orig} en jeu {_tmnt} est jouable",
           "contre-cas : c'est bien l'officielle qui bloque",
           [HEROS, f"Puzzle.Gain('{_tmnt}')"], [],
           {"carte": _tmnt, "jouable": True, "en_jeu": 0},
           main=["01088", "01089", "01088"], verifier="max_par_joueur_jouable"),
    ]

# ================================================================== RAMPAGE (uj006, uj009)
PAIE_DS = ["uj006", "01088"]
CAS += [
    _c("uj006 Dire Straits : Rampage 3 paye (3 degats, 3 cartes defaussees) puis 3 menaces retirees",
       "cout additionnel + « Remove 3 threat from a scheme » : deck de 6 -> 3, menace 5 -> 2 ; sans soutien NYC le "
       "heros reste incline (on l'incline avant de jouer)",
       [HEROS, SANS_DECK, DECK6, "Puzzle.SetThreat('01097b', 5)", "Puzzle.Exhaust('01001a')"], [],
       {"degats_identite": 3, "taille_deck_joueur": 3, "menace": [["01097b", 2]], "defausse": ["uj006", "01089"],
        "exhausted": ["01001a"]},
       main_exclusive=PAIE_DS, jouer=["uj006"], cibles=["01097b"]),
    _c("uj006 Dire Straits : soutien NYC controle -> le heros incline est PRET apres resolution",
       "« If you control a NYC support, ready your hero » : tr008 Shell Cycle (soutien NYC)",
       [HEROS, SANS_DECK, DECK6, "Puzzle.PutIntoPlay('tr008', under_control=True)", "Puzzle.SetThreat('01097b', 5)",
        "Puzzle.Exhaust('01001a')"], [],
       {"degats_identite": 3, "menace": [["01097b", 2]], "pret": ["01001a"]},
       main_exclusive=PAIE_DS, jouer=["uj006"], cibles=["01097b"]),
    _c("uj006 Dire Straits : deck de 2 cartes (< X) : jouable, cout paye (decision confirmee), 3 menaces retirees",
       "decision utilisateur confirmee : Rampage avec moins de X cartes reste jouable, on defausse le reste",
       [HEROS, SANS_DECK, "Puzzle.CreatePlayerDeck('01089', '01089')", "Puzzle.SetThreat('01097b', 5)"], [],
       {"degats_identite": 3, "menace": [["01097b", 2]], "defausse": ["uj006"]},
       main_exclusive=PAIE_DS, jouer=["uj006"], cibles=["01097b"]),
    _c("uj006 Dire Straits : identite Tenace : cout NON paye -> aucune menace retiree, deck intact",
       "« If taking damage is a cost, that cost is not considered paid unless all of that damage was taken »",
       [HEROS, SANS_DECK, DECK6, "Puzzle.Tough('01001a')", "Puzzle.SetThreat('01097b', 5)"], [],
       {"degats_identite": 0, "taille_deck_joueur": 6, "menace": [["01097b", 5]]},
       main_exclusive=PAIE_DS, jouer=["uj006"], cibles=["01097b"]),
    _c("uj009 Feral Cunning : Rampage 2 paye puis 1 degat a Rhino ET Rhino desoriente",
       "cout additionnel + « Deal 1 damage to an enemy and confuse it » : deck 6 -> 4",
       [HEROS, SANS_DECK, DECK6], [],
       {"degats_identite": 2, "taille_deck_joueur": 4, "degats": [["01094", 1]], "statuts": [["01094", "Confused"]],
        "defausse": ["uj009"]},
       main_exclusive=["uj009", "01088"], jouer=["uj009"], cibles=["01094"]),
    _c("uj009 Feral Cunning : identite Tenace : cout NON paye -> ni degat ni desorientation",
       "cout impaye = l'effet n'a pas lieu",
       [HEROS, SANS_DECK, DECK6, "Puzzle.Tough('01001a')"], [],
       {"degats_identite": 0, "taille_deck_joueur": 6, "degats": [["01094", 0]], "statuts_absents": [["01094", "Confused"]]},
       main_exclusive=["uj009", "01088"], jouer=["uj009"], cibles=["01094"]),
    _c("uj009 Feral Cunning : sbire Tenace : le degat est absorbe mais le sbire est QUAND MEME desoriente",
       "« deal 1 damage AND confuse it » : deux effets independants sur la meme cible",
       [HEROS, SANS_DECK, DECK6, "Puzzle.Tough(Puzzle.PutIntoPlay('01101'))"], [],
       {"degats": [["01101", 0]], "statuts": [["01101", "Confused"]], "statuts_absents": [["01101", "Tough"]]},
       main_exclusive=["uj009", "01088"], jouer=["uj009"], cibles=["01101"]),
]
# ⚠ Le « sens inverse » de uj026 (Ram-Shell en jeu -> 61016 Spider-Woman PAS jouable) est retire : une sonde a
# montre que 61016 reste « jouable » meme contre une AUTRE COPIE de 61016 en jeu (defaut de l'officielle, hors
# perimetre : son module declare une Action d'allie en jeu avec `.SetPlay()`, que `CanPlayBy` prend pour une
# capacite de jeu). Signale dans le rapport, non corrige ici.
CAS = [c for c in CAS if not c["nom"].startswith("[uj] uj026 bandeau : sens inverse")]

# ================================================================== CARTES SCRIPTEES (MODIFIEES / NOUVELLES)
TROIS = ["01088", "01089"]          # [energy][energy] + [mental][mental] : 4 ressources
PRINC5 = "Puzzle.SetThreat('01097b', 5)"
CAS += [
    # ---------------------------------------------------------------- uj002 Chance Encounter
    _c("uj002 Chance Encounter : « Attach to a scheme » -> jouable sur la manigance PRINCIPALE (lecture du scan)",
       "MODIFIEE : la cible de jeu est « a scheme » (26034 : « a side scheme ») ; question Q-uj002 ouverte",
       [HEROS], [], {"accroche_a": [["uj002", "01097b"]]},
       main_exclusive=["uj002"], jouer=["uj002"], cibles=["01097b"]),
    _c("uj002 Chance Encounter : manigance ANNEXE attachee vaincue -> un allie du deck va en main",
       "« When attached side scheme is defeated, search your deck and discard pile for an ally and add it to your "
       "hand » : 01107 a 1 menace, Spider-Man contre ; 60039 Daredevil (allie) dans un deck de Genius",
       [HEROS, SANS_DECK, "Puzzle.CreatePlayerDeck('01089', '60039', '01089')", "Puzzle.Reveal('01107')",
        "Puzzle.SetThreat('01107', 1)", "Puzzle.PutIntoPlay('uj002', under_control=True)",
        "Puzzle.Attach('uj002', '01107')"],
       ["Puzzle.Thwart('01001a')"],
       {"hors_jeu": ["01107"], "en_main": ["60039"]}, cibles=["01107"], accepter_choix=True),
    # ---------------------------------------------------------------- uj004 Cowabunga
    _c("uj004 Cowabunga : entre en jeu, defausse une carte RESSOURCE -> pioche 2 et soigne 2 a Spider-Man",
       "« discard a resource card from your hand → draw 2 cards and heal 2 damage from a friendly character » : "
       "paye avec 01088, 01090 Strength (ressource) defaussee, main 0 -> 2, identite 3 -> 1 degat",
       [HEROS, SANS_DECK, DECK6, "Puzzle.Damage('01001a', 3)"], [],
       {"taille_main": 2, "degats_identite": 1, "defausse": ["01090"], "en_jeu": ["uj004"]},
       main_exclusive=["uj004", "01088", "01090"], jouer=["uj004"], cibles=["01001a"], accepter_choix=True),
    _c("uj004 Cowabunga : contre-cas, aucune carte RESSOURCE en main -> ni pioche ni soin",
       "le cout (carte de type Resource) est impayable : seule une carte non-ressource (60039) reste en main",
       [HEROS, SANS_DECK, DECK6, "Puzzle.Damage('01001a', 3)"], [],
       {"taille_main": 1, "degats_identite": 3, "en_jeu": ["uj004"]},
       main_exclusive=["uj004", "01088", "60039"], jouer=["uj004"], accepter_choix=True),
    # ---------------------------------------------------------------- uj005 Delirium
    _c("uj005 Delirium : sbire attaque par TON heros ce tour -> jouable",
       "« Attach to a minion that your hero attacked this turn » : Spider-Man attaque 01101 puis la carte est jouable",
       [HEROS, "Puzzle.PutIntoPlay('01101')", "Puzzle.Gain('uj005')"], ["Puzzle.Attack('01001a')"],
       {"carte": "uj005", "jouable": True, "en_jeu": 0},
       main=["01089"], cibles=["01101"], verifier="max_par_joueur_jouable"),
    _c("uj005 Delirium : contre-cas, sbire NON attaque ce tour -> PAS jouable",
       "sans attaque du heros, aucune cible legale",
       [HEROS, "Puzzle.PutIntoPlay('01101')", "Puzzle.Gain('uj005')"], [],
       {"carte": "uj005", "jouable": False, "en_jeu": 0},
       main=["01089"], verifier="max_par_joueur_jouable"),
    _c("uj005 Delirium : sbire non-ELITE vulnerable : desoriente -> defausse ; l'Interruption retire 2 menaces",
       "« it gains vulnerable » (defausse s'il devient desoriente) + « When attached minion leaves play, remove 2 "
       "threat from a scheme » : 5 -> 3",
       [HEROS, "Puzzle.PutIntoPlay('01101')", PRINC5], ["Puzzle.Attack('01001a')"],
       {"hors_jeu": ["01101"], "menace": [["01097b", 3]]},
       main_exclusive=["uj005", "01089"], jouer=["uj005"], declencher_apres=["Puzzle.Confuse(Puzzle.FindFaceInPlay('01101'))"],
       cibles=["01101", "01097b"], accepter_choix=True),
    _c("uj005 Delirium : sbire ELITE (01102 Sandman) : PAS vulnerable, desoriente il reste en jeu",
       "« If attached to a non-ELITE minion » : sur un ELITE, aucun mot-cle gagne",
       [HEROS, "Puzzle.PutIntoPlay('01102')", PRINC5], ["Puzzle.Attack('01001a')"],
       {"en_jeu": ["01102"], "statuts": [["01102", "Confused"]], "menace": [["01097b", 5]]},
       main_exclusive=["uj005", "01089"], jouer=["uj005"], declencher_apres=["Puzzle.Confuse('01102')"],
       cibles=["01102", "01097b"], accepter_choix=True),
    # ---------------------------------------------------------------- uj008 Dreadmon
    _c("uj008 Dreadmon : attaque, 2 degats consecutifs -> il se redresse",
       "« After Dreadmon takes consequential damage, ready him » : ATK 2 sur Rhino, 2 degats sur Dreadmon, pret",
       [HEROS, "Puzzle.PutIntoPlay('uj008', under_control=True)"], ["Puzzle.Attack('uj008')"],
       {"degats": [["01094", 2], ["uj008", 2]], "pret": ["uj008"]}, cibles=["01094"], accepter_choix=True),
    _c("uj008 Dreadmon : contre-cas, sans la Reponse (refusee) il reste incline",
       "temoin de la Reponse : refusee, l'allie reste incline apres son attaque",
       [HEROS, "Puzzle.PutIntoPlay('uj008', under_control=True)"], ["Puzzle.Attack('uj008')"],
       {"degats": [["01094", 2], ["uj008", 2]], "exhausted": ["uj008"]}, cibles=["01094"],
       passer_sur_option="Response"),
    _c("uj008 Dreadmon : Forced Interrupt, fin du round -> defausse",
       "« When the round ends, discard Dreadmon »",
       [HEROS, "Puzzle.PutIntoPlay('uj008', under_control=True)"], [],
       {"hors_jeu": ["uj008"]}, verifier="uj_fin_de_round"),
    # ---------------------------------------------------------------- uj012 Hatamoto
    _c("uj012 Hatamoto : entre en jeu avec une carte Tough (Toughness)",
       "« Toughness » : desc.Toughness lu par le moteur",
       [HEROS, "Puzzle.PutIntoPlay('uj012', under_control=True)"], [],
       {"statuts": [["uj012", "Tough"]]}),
    _c("uj012 Hatamoto : defend contre Rhino -> Interruption, 1 menace retiree (5 -> 4)",
       "« When Hatamoto defends against an attack, remove 1 threat from a scheme »",
       [HEROS, "Puzzle.PutIntoPlay('uj012', under_control=True)", PRINC5], ["Puzzle.Defend('uj012', '01094')"],
       {"menace": [["01097b", 4]]}, cibles=["01097b"], accepter_choix=True),
    # ---------------------------------------------------------------- uj016 Inspector Ishida
    _c("uj016 Inspector Ishida : joue de la main, choix 1 -> 2 menaces retirees",
       "« After you play Inspector Ishida from your hand, choose: • Remove 2 threat from a scheme » : 5 -> 3",
       [HEROS, PRINC5], [], {"menace": [["01097b", 3]], "en_jeu": ["uj016"]},
       main_exclusive=["uj016"] + TROIS, jouer=["uj016"], cibles=["01097b"],
       preferer_option="Remove 2 threat", accepter_choix=True),
    _c("uj016 Inspector Ishida : choix 2 -> regarde 3 cartes rencontre, aucune menace retiree, rien ne quitte le deck",
       "« Look at the top 3 cards of the encounter deck and put them back in any order » : menace intacte, les 3 "
       "cartes semees restent dans le deck rencontre",
       [HEROS, PRINC5, "Puzzle.CreateEncounterDeck('01104', '01107', '01108')"], [],
       {"menace": [["01097b", 5]], "dans_deck_rencontre": ["01104", "01107", "01108"]},
       main_exclusive=["uj016"] + TROIS, jouer=["uj016"], preferer_option="Look at the top 3", accepter_choix=True),
    _c("uj016 Inspector Ishida : contre-cas, mis en jeu par un effet (pas joue de la main) -> aucune Reponse",
       "« After you PLAY ... FROM YOUR HAND »",
       [HEROS, PRINC5, "Puzzle.PutIntoPlay('uj016', under_control=True)"], [],
       {"menace": [["01097b", 5]]}, accepter_choix=True),
    # ---------------------------------------------------------------- uj018 Lita
    _c("uj018 Lita : contre -> regarde le dessus du deck, defausse 1 carte de la main pour le prendre",
       "« look at the top card of your deck. You may discard 1 card from your hand to add that card to your hand »",
       [HEROS, SANS_DECK, "Puzzle.CreatePlayerDeck('01090')", "Puzzle.PutIntoPlay('uj018', under_control=True)", PRINC5],
       ["Puzzle.Thwart('uj018')"],
       # Le deck ne contenait que 01090 : pris en main, le deck s'epuise et la defausse (01088, defaussee pour le
       # payer) est remelangee dedans (mesure au journal : « Energy defaussee », « Strength rendue a la main »).
       {"en_main": ["01090"], "absent_main": ["01088"], "dans_deck_joueur": ["01088"], "taille_deck_joueur": 1},
       main=["01088"], cibles=["01088"], accepter_choix=True),
    _c("uj018 Lita : refuse (Annuler) -> la carte reste au dessus du deck, la main est intacte",
       "« You MAY » : le refus laisse tout en place",
       [HEROS, SANS_DECK, "Puzzle.CreatePlayerDeck('01090')", "Puzzle.PutIntoPlay('uj018', under_control=True)", PRINC5],
       ["Puzzle.Thwart('uj018')"],
       {"en_main": ["01088"], "taille_deck_joueur": 1}, main=["01088"], preferer_option="Cancel"),
    # ---------------------------------------------------------------- uj019 Mission Training
    _c("uj019 Mission Training : sur un allie NINJA (Night-Blade uj023) -> +1 THW, +2 PV",
       "« Attach to a NINJA or MUTANIMAL ally. Attached ally gets +1 THW and +2 hit points »",
       [HEROS, "Puzzle.PutIntoPlay('uj023', under_control=True)"], [],
       {"accroche_a": [["uj019", "uj023"]], "attributs_carte": [["uj023", "thwart", 1], ["uj023", "health", 2]]},
       main_exclusive=["uj019", "01089"], jouer=["uj019"], cibles=["uj023"]),
    _c("uj019 Mission Training : seul allie en jeu = Daredevil 60039 (ni NINJA ni MUTANIMAL) -> PAS jouable",
       "la cible change par rapport a 34016 (X-MEN) : un allie sans les deux traits n'est pas une cible",
       [HEROS, "Puzzle.PutIntoPlay('60039', under_control=True)", "Puzzle.Gain('uj019')"], [],
       {"carte": "uj019", "jouable": False, "en_jeu": 0}, main=["01089"], verifier="max_par_joueur_jouable"),
    _c("uj019 Mission Training : Max 1 TRAINING par allie : allie MUTANIMAL deja equipe -> 2e copie PAS jouable",
       "« Max 1 TRAINING upgrade per ally » : Mondo Gecko uj021 (MUTANIMAL) porte deja une Mission Training",
       [HEROS, "Puzzle.PutIntoPlay('uj021', under_control=True)", "Puzzle.PutIntoPlay('uj019', under_control=True)",
        "Puzzle.Attach('uj019', 'uj021')", "Puzzle.CreateHandCards('uj019')"], [],
       {"carte": "uj019", "jouable": False, "en_jeu": 1}, main=["01089"], verifier="max_par_joueur_jouable"),
    _c("uj019 Mission Training : TEMOIN, allie MUTANIMAL sans TRAINING -> jouable",
       "contre-cas : c'est bien la Mission Training deja attachee qui bloque",
       [HEROS, "Puzzle.PutIntoPlay('uj021', under_control=True)", "Puzzle.Gain('uj019')"], [],
       {"carte": "uj019", "jouable": True, "en_jeu": 0}, main=["01089"], verifier="max_par_joueur_jouable"),
    # ---------------------------------------------------------------- uj020 Mona Lisa
    _c("uj020 Mona Lisa : entre en jeu -> glisse un evenement THWART de la defausse sous elle",
       "« choose a THWART event in your discard pile and tuck it here » : 04049 Clear the Area",
       [HEROS, "Puzzle.EmptyPlayerDiscardPile()", "Puzzle.CreatePlayerDiscardPile('04049')"], [],
       {"pose_sous": [["uj020", "04049"]], "en_jeu": ["uj020"]},
       main_exclusive=["uj020"], jouer=["uj020"], accepter_choix=True),
    _c("uj020 Mona Lisa : Action -> joue la carte glissee (cout paye), PUIS Mona Lisa est defaussee",
       "« Play the card tucked here (paying its cost). Then, discard Mona Lisa » : 04049 retire 2 menaces (5 -> 3), "
       "payee avec 01089, Mona Lisa et 04049 en defausse",
       [HEROS, "Puzzle.EmptyPlayerDiscardPile()", "Puzzle.CreatePlayerDiscardPile('04049')", PRINC5], [],
       {"menace": [["01097b", 3]], "hors_jeu": ["uj020"], "defausse": ["uj020", "04049", "01089"]},
       main_exclusive=["uj020", "01089"], jouer=["uj020"], declencher_apres=["Puzzle.Action('uj020')"],
       cibles=["01097b"], accepter_choix=True),
    _c("uj020 Mona Lisa : « THEN » : carte glissee IMPAYABLE (main vide) -> pas jouee, Mona Lisa RESTE en jeu",
       "Rules Reference v1.8 « THEN » : la partie apres « then » ne se resout que si la premiere a reussi ; 04049 "
       "reste glissee, menace intacte",
       [HEROS, "Puzzle.EmptyPlayerDiscardPile()", "Puzzle.CreatePlayerDiscardPile('04049')", PRINC5], [],
       {"menace": [["01097b", 5]], "en_jeu": ["uj020"], "pose_sous": [["uj020", "04049"]]},
       main_exclusive=["uj020"], jouer=["uj020"], declencher_tolerant=["Puzzle.Action('uj020')"],
       cibles=["01097b"], accepter_choix=True),
    _c("uj020 Mona Lisa : contre-cas, aucun evenement THWART en defausse -> rien de glisse, Action indisponible",
       "« the card tucked here » : sans carte glissee, pas d'Action (la tentative est refusee, Mona Lisa reste)",
       [HEROS, "Puzzle.EmptyPlayerDiscardPile()", "Puzzle.CreatePlayerDiscardPile('01090')"], [],
       {"en_jeu": ["uj020"], "taille_pose_sous": [["uj020", 0]]},
       main_exclusive=["uj020"], jouer=["uj020"], declencher_tolerant=["Puzzle.Action('uj020')"],
       accepter_choix=True),
    # ---------------------------------------------------------------- uj021 Mondo Gecko
    _c("uj021 Mondo Gecko : entre en jeu -> camoufle (carte d'etat Cloaked)",
       "« After Mondo Gecko enters play, cloak him »",
       [HEROS], [], {"statuts": [["uj021", "Cloaked"]], "en_jeu": ["uj021"]},
       main_exclusive=["uj021", "01088"], jouer=["uj021"], accepter_choix=True),
    # ---------------------------------------------------------------- uj026 Ram-Shell
    _c("uj026 Ram-Shell : ton heros contre -> 1 compteur momentum (Ram-Shell gardee)",
       "« After a character you control thwarts, place 1 momentum counter here » ; la defausse est refusee",
       [HEROS, PRINC5, "Puzzle.PutIntoPlay('uj026', under_control=True)"], ["Puzzle.Thwart('01001a')"],
       {"compteurs": [["uj026", "momentum", 1]]}, preferer_option="Cancel"),
    _c("uj026 Ram-Shell : 2 contres (heros + Ram-Shell) puis defausse -> 2 degats a Rhino",
       "« You may discard Ram-Shell to deal 1 damage to an enemy for each momentum counter here » : le 1er contre "
       "pose 1 (refus), le 2e (Ram-Shell elle-meme, allie que tu controles) pose le 2e et on defausse : 2 degats",
       [HEROS, PRINC5, "Puzzle.PutIntoPlay('uj026', under_control=True)", "Puzzle.PlaceCounters('uj026', 'momentum', 1)"],
       ["Puzzle.Thwart('uj026')"],
       {"hors_jeu": ["uj026"], "degats": [["01094", 2]]}, cibles=["01094"], accepter_choix=True),
    _c("uj026 Ram-Shell : plafond de 8 compteurs",
       "« (to a maximum of 8) » : 8 deja poses, un contre n'en ajoute pas",
       [HEROS, PRINC5, "Puzzle.PutIntoPlay('uj026', under_control=True)", "Puzzle.PlaceCounters('uj026', 'momentum', 8)"],
       ["Puzzle.Thwart('01001a')"],
       {"compteurs": [["uj026", "momentum", 8]]}, preferer_option="Cancel"),
    # ---------------------------------------------------------------- uj027 Sally Pride
    _c("uj027 Sally Pride : attaque -> 2 menaces retirees",
       "« After Sally Pride attacks or thwarts, remove 2 threat from a scheme » : branche ATTAQUE, 5 -> 3",
       [HEROS, "Puzzle.PutIntoPlay('uj027', under_control=True)", PRINC5], ["Puzzle.Attack('uj027')"],
       {"menace": [["01097b", 3]], "degats": [["01094", 2]]}, cibles=["01094", "01097b"], accepter_choix=True),
    _c("uj027 Sally Pride : contre -> 2 de son THW puis 2 de la Reponse",
       "branche CONTRE : 5 - 2 (THW) - 2 = 1",
       [HEROS, "Puzzle.PutIntoPlay('uj027', under_control=True)", PRINC5], ["Puzzle.Thwart('uj027')"],
       {"menace": [["01097b", 1]]}, cibles=["01097b"], accepter_choix=True),
    # ---------------------------------------------------------------- uj028 Screwloose / uj038 Wingnut
    _c("uj028 Screwloose : Wingnut en jeu -> Wingnut perd son icone [acceleration]",
       "« Wingnut loses each [acceleration] icon » : 1 icone imprimee sur uj038, 0 en jeu",
       [HEROS, "Puzzle.PutIntoPlay('uj038', under_control=True)", "Puzzle.PutIntoPlay('uj028', under_control=True)"],
       [], {"icones": [["Acceleration", 0]]}),
    _c("uj028 Screwloose : TEMOIN, Wingnut seul -> 1 icone [acceleration]",
       "ligne de base : l'icone imprimee de Wingnut est bien comptee",
       [HEROS, "Puzzle.PutIntoPlay('uj038', under_control=True)"], [], {"icones": [["Acceleration", 1]]}),
    _c("uj028 Screwloose : Wingnut en jeu -> -1 degat consecutif apres son attaque (2 -> 1)",
       "« If Wingnut is in play, Screwloose takes -1 consequential damage after he uses a basic power »",
       [HEROS, "Puzzle.PutIntoPlay('uj038', under_control=True)", "Puzzle.PutIntoPlay('uj028', under_control=True)"],
       ["Puzzle.Attack('uj028')"], {"degats": [["uj028", 1], ["01094", 2]]}, cibles=["01094"]),
    _c("uj028 Screwloose : TEMOIN sans Wingnut -> 2 degats consecutifs",
       "contre-cas de la condition « If Wingnut is in play »",
       [HEROS, "Puzzle.PutIntoPlay('uj028', under_control=True)"],
       ["Puzzle.Attack('uj028')"], {"degats": [["uj028", 2], ["01094", 2]]}, cibles=["01094"]),
    _c("uj038 Wingnut : Action, incliner + [energy][energy] -> Screwloose (du deck) mis en jeu",
       "« Exhaust Wingnut and spend [energy][energy] resources → find Screwloose and put him into play »",
       [HEROS, SANS_DECK, "Puzzle.CreatePlayerDeck('01089', 'uj028', '01089')",
        "Puzzle.PutIntoPlay('uj038', under_control=True)"], ["Puzzle.Action('uj038')"],
       {"en_jeu": ["uj028"], "exhausted": ["uj038"], "defausse": ["01088"]}, main_exclusive=["01088"]),
    # ---------------------------------------------------------------- uj033 Tomoe Ame
    _c("uj033 Tomoe Ame : tue un sbire -> pioche 1",
       "« After Tomoe Ame defeats a side scheme or minion, draw 1 card » : ATK 3 sur 01101 (3 PV)",
       [HEROS, SANS_DECK, DECK6, "Puzzle.PutIntoPlay('uj033', under_control=True)", "Puzzle.PutIntoPlay('01101')"],
       ["Puzzle.Attack('uj033')"], {"hors_jeu": ["01101"], "taille_main": 1}, cibles=["01101"],
       accepter_choix=True),
    _c("uj033 Tomoe Ame : vainc une manigance annexe -> pioche 1",
       "branche « side scheme » : THW 2 sur 01107 a 2 menaces",
       [HEROS, SANS_DECK, DECK6, "Puzzle.PutIntoPlay('uj033', under_control=True)", "Puzzle.Reveal('01107')",
        "Puzzle.SetThreat('01107', 2)"],
       ["Puzzle.Thwart('uj033')"], {"hors_jeu": ["01107"], "taille_main": 1}, cibles=["01107"],
       accepter_choix=True),
    _c("uj033 Tomoe Ame : contre-cas, attaque Rhino sans le vaincre -> pas de pioche",
       "« defeats » : une attaque qui ne tue pas ne pioche pas",
       [HEROS, SANS_DECK, DECK6, "Puzzle.PutIntoPlay('uj033', under_control=True)"],
       ["Puzzle.Attack('uj033')"], {"degats": [["01094", 3]], "taille_main": 0}, cibles=["01094"],
       accepter_choix=True),
    # ---------------------------------------------------------------- uj034 Turtle Line
    _c("uj034 Turtle Line : attachee au heros, il contre -> incliner + 1 corde -> 2 menaces retirees",
       "« After attached character uses a basic power, exhaust this card and remove 1 rope counter → remove 2 "
       "threat » : 5 - 1 (THW 1) - 2 = 2, 3 cordes -> 2",
       [HEROS, PRINC5, "Puzzle.PutIntoPlay('uj034', under_control=True)", "Puzzle.Attach('uj034', '01001a')"],
       ["Puzzle.Thwart('01001a')"],
       {"menace": [["01097b", 2]], "compteurs": [["uj034", "rope", 2]], "exhausted": ["uj034"]},
       cibles=["01097b"], accepter_choix=True),
    _c("uj034 Turtle Line : attachee a un ALLIE (uj021), apres son attaque -> 2 menaces retirees",
       "« a friendly character » : un allie aussi ; « uses a basic power » : l'attaque compte",
       [HEROS, PRINC5, "Puzzle.PutIntoPlay('uj021', under_control=True)",
        "Puzzle.PutIntoPlay('uj034', under_control=True)", "Puzzle.Attach('uj034', 'uj021')"],
       ["Puzzle.Attack('uj021')"],
       {"menace": [["01097b", 3]], "compteurs": [["uj034", "rope", 2]]}, cibles=["01094", "01097b"],
       accepter_choix=True),
    _c("uj034 Turtle Line : Uses, dernier pion retire -> la carte quitte le jeu (apres les 2 menaces)",
       "« Uses (3 rope counters) » : 1 seul pion restant, l'usage le retire, la carte part",
       [HEROS, PRINC5, "Puzzle.PutIntoPlay('uj034', under_control=True)", "Puzzle.Attach('uj034', '01001a')"],
       ["Puzzle.Thwart('01001a')"],
       {"menace": [["01097b", 2]], "hors_jeu": ["uj034"]}, cibles=["01097b"], accepter_choix=True,
       declencher_avant_rope=1),
    _c("uj034 Turtle Line : attachee au HEROS -> restricted 1",
       "« While attached to an identity, this card gains restricted »",
       [HEROS, "Puzzle.PutIntoPlay('uj034', under_control=True)", "Puzzle.Attach('uj034', '01001a')"], [],
       {}, verifier="uj_restricted", restricted_attendu=1),
    _c("uj034 Turtle Line : JOUEE sur un ALLIE (uj021) -> restricted 0",
       "contre-cas : hors d'une identite, pas de restricted (carte jouee de la main, cible choisie)",
       [HEROS, "Puzzle.PutIntoPlay('uj021', under_control=True)"], [],
       {}, verifier="uj_restricted", restricted_attendu=0,
       main_exclusive=["uj034", "01088"], jouer=["uj034"], cibles=["uj021"]),
    _c("uj034 Turtle Line : JOUEE sur le HEROS -> restricted 1",
       "meme chemin de jeu que le contre-cas, cible l'identite",
       [HEROS, "Puzzle.PutIntoPlay('uj021', under_control=True)"], [],
       {}, verifier="uj_restricted", restricted_attendu=1,
       main_exclusive=["uj034", "01088"], jouer=["uj034"], cibles=["01001a"]),
    # ---------------------------------------------------------------- uj037 Watch the Exits
    _c("uj037 Watch the Exits : soutien NYC controle -> cout 2 reduit a 1 (payee avec une seule ressource)",
       "« Reduce the cost to play this card by 1 if you control a NYC support » : tr008 en jeu, 01087 Haymaker "
       "([energy] x1) seule en main",
       [HEROS, "Puzzle.PutIntoPlay('tr008', under_control=True)"], [],
       {"en_jeu": ["uj037"]}, main_exclusive=["uj037", "01087"], jouer=["uj037"]),
    _c("uj037 Watch the Exits : SANS soutien NYC, une seule ressource -> la carte n'est PAS jouee (reste en main)",
       "contre-cas : cout 2 plein, 01087 ne fournit qu'une ressource",
       [HEROS], [],
       {"en_main": ["uj037"], "hors_jeu": ["uj037"]}, main_exclusive=["uj037", "01087"], jouer=["uj037"]),
    _c("uj037 Watch the Exits : un sbire t'engage -> defausser -> 2 menaces retirees ET heros redresse",
       "« After a minion engages you, discard Watch the Exits → remove 2 threat from a scheme and ready your hero »",
       [HEROS, PRINC5, "Puzzle.PutIntoPlay('uj037', under_control=True)", "Puzzle.Exhaust('01001a')"],
       ["Puzzle.PutIntoPlay('01101')"],
       {"menace": [["01097b", 3]], "pret": ["01001a"], "hors_jeu": ["uj037"]}, cibles=["01097b"],
       accepter_choix=True),
]
# Turtle Line : dernier pion. Le montage pose les 3 pions de Uses a l'entree en jeu ; on en retire 2 avant.
for _cas in CAS:
    if _cas.pop("declencher_avant_rope", None):
        _cas["mise_en_place"].append("Puzzle.PlaceCounters('uj034', 'rope', -2)")


# Sonde sur l'OFFICIELLE 61016 (citee dans uj026.py) : sa Reponse « You » part-elle apres un contre du heros ?
CAS += [_c("SONDE 61016 Spider-Woman (officielle) : compteur limb apres un contre du heros",
           "mesure du declencheur `AfterUnitThwartScheme(..., You, ...)` de l'officielle (rapport, pas une preuve uj)",
           [HEROS, PRINC5, "Puzzle.PutIntoPlay('61016', under_control=True)"], ["Puzzle.Thwart('01001a')"],
           {"compteurs": [["61016", "limb", 1]]}, accepter_choix=True)]


VERIFICATIONS = r'''
def uj_fin_de_round(monde, aides):
    """Envoie la fin de round (Message.WhenRoundEnd, modele brawn_hulk_out_fin_de_round) puis lit `attendu`."""
    from game.message import Message
    Message.WhenRoundEnd(monde).Send()
    return etat_attendu(monde, aides)


def uj_restricted(monde, aides):
    """uj034 Turtle Line : valeur courante de `restricted` de la copie en jeu (`restricted_attendu` du cas)."""
    faces = [o.face for o in monde.object_manager.card_dict.values()
             if o.face is not None and getattr(o.face.paper, "card_id", None) == "uj034" and o.face.IsInPlay()]
    if not faces:
        return False, "uj034 pas en jeu"
    face = faces[0]
    hote = getattr(getattr(face, "bind_face", None), "paper", None)
    attendu = aides["cas"]["restricted_attendu"]
    return (face.restricted == attendu,
            f"restricted={face.restricted} attachee a {getattr(hote, 'card_id', None)} (attendu {attendu})")
'''
