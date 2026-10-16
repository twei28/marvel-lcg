# Cas test_capacites du heros Donatello (TMNT Heroes, Inkwire, prefixe `td`) : un cas par capacite,
# sujet = le card_id dans le nom (« [donatello] tdNNN ... »). Gabarits PROCESSUS-CARTE :
# .planning/tmnt/donatello-gabarits-processus-carte.md.
#
# Rappels de montage : Donatello demarre en ALTER EGO (td001b) ; `ChangeForm('td001b')` la passe en
# forme heros (td001a). Le deck joueur du heros n'a PAS de moitie d'aspect : la main de depart est faite de
# cartes signature, dont les interruptions partiraient au milieu d'un cas -> toujours `main_exclusive`
# (ou `Puzzle.EmptyHand()` quand la main doit etre VIDE).
# Rhino = 01094, sa manigance principale 01097b, Hydra Mercenary 01101 (ATQ 1, PV 3, Guard), Shocker 01103
# (ATQ 2, PV 3), Whiplash 01172 (Retaliate 1), ah016 Fin Fang Foom (ATQ 4, PV 4, rien a l'attaque),
# 01088/01089/01090 = Energy YY / Genius BB / Strength RR, 01006 Aunt May (soutien, cout 1).

HEROS = {
    "scenario": "rhino",
    "heros": "donatello",
}
FORME_HEROS = "Puzzle.ChangeForm('td001b')"
MAIN_VIDE = "Puzzle.EmptyHand()"

CAS = []

# ========================================================================= td001a Kashikoi
CAS += [
    {
        "nom": "[donatello] td001a Kashikoi — depense BB : pioche 2 cartes",
        "pourquoi": ("Action « Spend [mental][mental] resources -> draw 2 cards ». Main = Genius (BB) + Energy : "
                     "Genius paie le cout, reste Energy (1) + 2 piochees = 3 cartes"),
        **HEROS,
        "mise_en_place": [FORME_HEROS],
        "main_exclusive": ["01089", "01088"],
        "declencher": ["Puzzle.Action('td001a', 'Action', 0)"],
        "verifier": "etat_attendu",
        "attendu": {"taille_main": 3, "defausse": ["01089"]},
    },
    {
        "nom": "[donatello] td001a Kashikoi — TEMOIN D'EPUISEMENT : la 2e activation du round est refusee",
        "pourquoi": ("« Limit once per round » : deux Genius en main + Energy. 1re activation : Genius paye, +2 cartes "
                     "(main 2 + 2 = 4). 2e activation : si la limite mord, la main reste a 4 ; si elle est inerte, "
                     "le 2e Genius est depense et la main vaut 5"),
        **HEROS,
        "mise_en_place": [FORME_HEROS],
        "main_exclusive": ["01089", "01089", "01088"],
        "declencher": ["Puzzle.Action('td001a', 'Action', 0)"],
        "declencher_tolerant": ["Puzzle.Action('td001a', 'Action', 0)"],
        "verifier": "etat_attendu",
        "attendu": {"taille_main": 4},
    },
    {
        "nom": "[donatello] td001a Kashikoi — le cout BB est obligatoire : sans ressource mentale, rien n'est pioche",
        "pourquoi": "main = Strength (RR) + Energy (YY) : aucune ressource [mental], l'action ne doit pas se payer ni piocher",
        **HEROS,
        "mise_en_place": [FORME_HEROS],
        "main_exclusive": ["01090", "01088"],
        "declencher": [],
        "declencher_tolerant": ["Puzzle.Action('td001a', 'Action', 0)"],
        "verifier": "etat_attendu",
        "attendu": {"taille_main": 2, "en_main": ["01090", "01088"]},
    },
]

# ========================================================================= td001b Donnie
CAS += [
    {
        "nom": "[donatello] td001b Donnie — defausse 1 carte : cherche td011 dans le deck, UNE seule carte, entree INCLINEE, attachee a l'identite",
        "pourquoi": ("Action « discard 1 card from your hand -> search your deck and discard pile for Donatello's Bo or "
                     "Donatello's Shell and put it into play, exhausted ». Deck : td012, td011 ; on designe td011. "
                     "td012 doit RESTER dans le deck (une seule carte)"),
        **HEROS,
        "mise_en_place": ["Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01088', 'td012', 'td011', '01088')"],
        "main_exclusive": ["01088"],
        "cibles": ["td011"],
        "declencher": ["Puzzle.Action('td001b', 'Action', 0)"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["td011"], "hors_jeu": ["td012"], "exhausted": ["td011"], "defausse": ["01088"],
                    "dans_deck_joueur": ["td012"], "attaches": [["td001b", "td011"]], "taille_main": 0},
    },
    {
        "nom": "[donatello] td001b Donnie — cherche aussi td012 (Carapace) : entree inclinee",
        "pourquoi": "l'autre moitie du « or » : on designe la Carapace td012, td011 reste dans le deck",
        **HEROS,
        "mise_en_place": ["Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01088', 'td012', 'td011', '01088')"],
        "main_exclusive": ["01088"],
        "cibles": ["td012"],
        "declencher": ["Puzzle.Action('td001b', 'Action', 0)"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["td012"], "hors_jeu": ["td011"], "exhausted": ["td012"], "dans_deck_joueur": ["td011"],
                    "attaches": [["td001b", "td012"]]},
    },
    {
        "nom": "[donatello] td001b Donnie — cherche aussi dans la DEFAUSSE (deck sans cible)",
        "pourquoi": "« search your deck AND discard pile » : td011 n'est que dans la defausse du joueur",
        **HEROS,
        "mise_en_place": ["Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01088', '01088')",
                          "Puzzle.CreatePlayerDiscardPile('td011')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Action('td001b', 'Action', 0)"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["td011"], "exhausted": ["td011"], "attaches": [["td001b", "td011"]]},
    },
    {
        "nom": "[donatello] td001b Donnie — aucune cible dans le deck ni la defausse : le cout est paye, rien ne plante, rien n'entre en jeu",
        "pourquoi": "ni td011 ni td012 nulle part : la carte defaussee part, aucune amelioration n'arrive",
        **HEROS,
        "mise_en_place": ["Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01088', '01088')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Action('td001b', 'Action', 0)"],
        "verifier": "etat_attendu",
        "attendu": {"hors_jeu": ["td011", "td012"], "defausse": ["01088"], "taille_main": 0},
    },
    {
        "nom": "[donatello] td001b Donnie — TEMOIN : main vide, le cout « discard 1 card » n'est pas payable, l'Action n'est pas offerte",
        "pourquoi": "sans carte a defausser (et rien sous une Carapace), td011 reste dans le deck",
        **HEROS,
        "mise_en_place": [MAIN_VIDE, "Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01088', 'td011', '01088')"],
        "declencher": [],
        "declencher_tolerant": ["Puzzle.Action('td001b', 'Action', 0)"],
        "verifier": "etat_attendu",
        "attendu": {"hors_jeu": ["td011"], "dans_deck_joueur": ["td011"], "taille_main": 0},
    },
]

# ========================================================================= td002 Metalhead
CAS += [
    {
        "nom": "[donatello] td002 Metalhead — entre en jeu avec Tenace, ATQ/CTR 2 et degats consecutifs",
        "pourquoi": ("Toughness (lu dans desc), PV 1, ATQ 2* et CTR 2* : l'etoile creuse sous ATQ/CTR est UN degat "
                     "consecutif (1 chacun)"),
        **HEROS,
        "mise_en_place": ["Puzzle.PutIntoPlay('td002', under_control=True)"],
        "declencher": [],
        "verifier": "td_etat_carte",
        "attendu": {"carte": "td002", "statut": "Tough", "pv": 1, "atq": 2, "ctr": 2, "consecutifs": [1, 1]},
    },
    {
        "nom": "[donatello] td002 Metalhead — Interrupt depuis la MAIN : Donatello se defend, B paye, jouee SANS payer son cout 2",
        "pourquoi": ("« When Donatello defends against an attack, spend a [mental] resource -> play Metalhead from your hand "
                     "without paying his resource cost ». Main : Metalhead, Genius (BB), Energy (YY). Fin Fang Foom attaque, "
                     "Donatello defend : Genius paie le B, Metalhead entre en jeu et Energy (qui aurait paye le cout 2) "
                     "reste en main"),
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.PutIntoPlay('ah016')"],
        "main_exclusive": ["td002", "01089", "01088"],
        "payer_avec": ["01089"],
        "declencher": ["Puzzle.Defend('td001a', 'ah016')"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["td002"], "defausse": ["01089"], "en_main": ["01088"], "absent_main": ["td002", "01089"],
                    "statuts": [["td002", "Tough"]]},
    },
    {
        "nom": "[donatello] td002 Metalhead — Interrupt depuis la CARAPACE : meme jeu, carte glissee sous Donatello's Shell",
        "pourquoi": ("« ... from your hand OR Donatello's Shell » : Metalhead est glissee sous la Carapace (rien en main que "
                     "Genius et Energy). Elle doit entrer en jeu depuis la Carapace, sans payer 2"),
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.PutIntoPlay('td012', under_control=True)",
                          "Puzzle.PlaceUnder('td002', 'td012')", "Puzzle.PutIntoPlay('ah016')"],
        "main_exclusive": ["01089", "01088"],
        "payer_avec": ["01089"],
        "declencher": ["Puzzle.Defend('td001a', 'ah016')"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["td002"], "taille_pose_sous": [["td012", 0]], "defausse": ["01089"], "en_main": ["01088"]},
    },
    {
        "nom": "[donatello] td002 Metalhead — TEMOIN : sans ressource [mental], l'Interrupt n'est pas payable, Metalhead reste en main",
        "pourquoi": "main : Metalhead + Energy (YY) + Strength (RR), aucune ressource mentale : l'interruption ne peut pas se payer",
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.PutIntoPlay('ah016')"],
        "main_exclusive": ["td002", "01088", "01090"],
        "declencher": ["Puzzle.Defend('td001a', 'ah016')"],
        "verifier": "etat_attendu",
        "attendu": {"hors_jeu": ["td002"], "en_main": ["td002", "01088", "01090"]},
    },
    {
        "nom": "[donatello] td002 Metalhead — NON proposee en alter ego (« When DONATELLO defends »)",
        "pourquoi": "Donnie (alter ego) se defend avec Genius en main : l'interruption vise la forme heros, Metalhead reste en main",
        **HEROS,
        "mise_en_place": ["Puzzle.PutIntoPlay('ah016')"],
        "main_exclusive": ["td002", "01089", "01088"],
        "declencher": ["Puzzle.Defend('td001b', 'ah016')"],
        "verifier": "etat_attendu",
        "attendu": {"hors_jeu": ["td002"], "en_main": ["td002", "01089", "01088"]},
    },
    {
        "nom": "[donatello] td002 Metalhead — NON proposee si Metalhead est deja en jeu (unique)",
        "pourquoi": "Metalhead en jeu + une autre copie en main + Genius : l'interruption ne doit pas jouer la 2e copie",
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.PutIntoPlay('ah016')", "Puzzle.PutIntoPlay('td002', under_control=True)"],
        "main_exclusive": ["01089", "01088"],
        # ⚠ `Puzzle.Gain('td002')` rendrait la copie DEJA en jeu (meme carte) : on CREE une 2e copie en main.
        "declencher": ["Puzzle.CreateHandCards('td002')", "Puzzle.Defend('td001a', 'ah016')"],
        "verifier": "etat_attendu",
        "attendu": {"en_main": ["td002", "01089", "01088"]},
    },
]

# ========================================================================= td003 Bo Tobu
CAS += [
    {
        "nom": "[donatello] td003 Bō Tobu — attaque de 4 : previent EXACTEMENT 3 degats et retire 3 menaces de la manigance",
        "pourquoi": ("« When you would take damage from an attack, prevent 3 of that damage and remove 3 threat from a scheme ». "
                     "Fin Fang Foom (ATQ 4) attaque, Donatello EPUISE (donc sans defense) : 4 - 3 = 1 degat ; manigance principale 5 -> 2. "
                     "Cout 1 paye par Genius"),
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.Exhaust('td001a')", "Puzzle.SetThreat('01097b', 5)", "Puzzle.PutIntoPlay('ah016')"],
        "main_exclusive": ["td003", "01089"],
        "declencher": ["Puzzle.Attack('ah016')"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 1, "menace": [["01097b", 2]], "defausse": ["td003", "01089"]},
    },
    {
        "nom": "[donatello] td003 Bō Tobu — attaque de 2 seulement : prevent 3 ne depasse pas les degats, 0 degat, 3 menaces retirees quand meme",
        "pourquoi": "Shocker (ATQ 2) : 2 degats, tous prevenus ; la 2e moitie (retirer 3 menaces) a lieu quand meme",
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.Exhaust('td001a')", "Puzzle.SetThreat('01097b', 5)", "Puzzle.PutIntoPlay('01103')"],
        "main_exclusive": ["td003", "01089"],
        "declencher": ["Puzzle.Attack('01103')"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 0, "menace": [["01097b", 2]], "defausse": ["td003"]},
    },
    {
        "nom": "[donatello] td003 Bō Tobu — TEMOIN : des degats qui ne viennent PAS d'une attaque ne sont pas prevenus",
        "pourquoi": "« from an attack » : 3 degats directs (hors attaque), la carte n'est pas offerte, reste en main, 3 degats subis",
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.SetThreat('01097b', 5)"],
        "main_exclusive": ["td003", "01089"],
        "declencher": ["Puzzle.Damage('td001a', 3)"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 3, "menace": [["01097b", 5]], "en_main": ["td003", "01089"]},
    },
]

# ========================================================================= td004 Chudan-Ura-Uke
CAS += [
    {
        "nom": "[donatello] td004 Chūdan-Ura-Uke — attaque de 4 : previent EXACTEMENT 3 et inflige 3 degats a l'attaquant",
        "pourquoi": ("« prevent 3 of that damage and deal 3 damage to the attacking enemy ». Fin Fang Foom (ATQ 4, PV 4) : "
                     "Donatello prend 1, l'attaquant prend 3 (et survit avec 1 PV)"),
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.Exhaust('td001a')", "Puzzle.PutIntoPlay('ah016')"],
        "main_exclusive": ["td004", "01089"],
        "declencher": ["Puzzle.Attack('ah016')"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 1, "degats": [["ah016", 3]], "defausse": ["td004"]},
    },
    {
        "nom": "[donatello] td004 Chūdan-Ura-Uke — l'attaquant vivant tombe s'il a au plus 3 PV (Shocker, ATQ 2)",
        "pourquoi": "Shocker (PV 3, ATQ 2) : 2 degats prevenus, 3 degats a l'attaquant : il est vaincu",
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.Exhaust('td001a')", "Puzzle.PutIntoPlay('01103')"],
        "main_exclusive": ["td004", "01089"],
        "declencher": ["Puzzle.Attack('01103')"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 0, "hors_jeu": ["01103"], "defausse": ["td004"]},
    },
    {
        "nom": "[donatello] td004 Chūdan-Ura-Uke — TEMOIN : degats hors attaque, la carte n'est pas offerte",
        "pourquoi": "3 degats directs : pas « from an attack », la carte reste en main, 3 degats subis, aucun ennemi touche",
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.Exhaust('td001a')", "Puzzle.PutIntoPlay('ah016')"],
        "main_exclusive": ["td004", "01089"],
        "declencher": ["Puzzle.Damage('td001a', 3)"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 3, "degats": [["ah016", 0]], "en_main": ["td004", "01089"]},
    },
]

CAS += [
    {
        "nom": "[donatello] td002 Metalhead — ATQ 2* : frappe pour 2 et subit 1 degat consecutif (Tenace l'absorbe)",
        "pourquoi": ("Metalhead (ATQ 2, 1 etoile) attaque Rhino : 2 degats ; l'etoile = 1 degat consecutif a lui-meme, "
                     "que sa carte Tenace absorbe (elle disparait, il reste a 0 degat)"),
        **HEROS,
        "mise_en_place": ["Puzzle.PutIntoPlay('td002', under_control=True)"],
        "declencher": ["Puzzle.Attack('td002')"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 2], ["td002", 0]], "statuts_absents": [["td002", "Tough"]]},
    },
    {
        "nom": "[donatello] td002 Metalhead — CTR 2* : contre pour 2 et subit 1 degat consecutif (Tenace l'absorbe)",
        "pourquoi": "meme montage cote contre : manigance principale 5 -> 3, la carte Tenace de Metalhead a absorbe le degat consecutif",
        **HEROS,
        "mise_en_place": ["Puzzle.PutIntoPlay('td002', under_control=True)", "Puzzle.SetThreat('01097b', 5)"],
        "declencher": ["Puzzle.Thwart('td002')"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["01097b", 3]], "degats": [["td002", 0]], "statuts_absents": [["td002", "Tough"]]},
    },
]

# ========================================================================= td005 Improvised Tactics
# ⚠ L'option « Cloak two friendly characters » est le travail d'un AUTRE agent (carte d'etat Cloaked) : aucun cas
# ci-dessous ne la choisit, aucun ne depend de son effet. On prouve les deux autres options et la structure
# « choose two, jamais deux fois la meme ».
CAS += [
    {
        "nom": "[donatello] td005 Improvised Tactics — choose two : « Stun » + « Draw 2 » : Rhino sonne, 2 cartes piochees, cout paye",
        "pourquoi": ("Hero Action « Exhaust a TECH upgrade you control -> choose two ». Gantelet (TECH) en jeu, main = "
                     "td005 + Energy (YY paie le cout 2). On choisit Sonner puis Piocher 2 : Rhino sonne, main = 2 cartes, "
                     "Gantelet incline"),
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.PutIntoPlay('td009', under_control=True)"],
        "main_exclusive": ["td005", "01088"],
        "preferer_option": ["Stun_or_confuse", "Draw_2_cards"],
        "declencher": [],
        "jouer": ["td005"],
        "verifier": "etat_attendu",
        "attendu": {"statuts": [["01094", "Stunned"]], "taille_main": 2, "exhausted": ["td009"], "defausse": ["td005", "01088"]},
    },
    {
        "nom": "[donatello] td005 Improvised Tactics — « Stun OR confuse » : la branche Desoriente existe",
        "pourquoi": "l'option « Stun or confuse an enemy » contient un choix : on prend Confuse, Rhino est desoriente et PAS sonne",
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.PutIntoPlay('td009', under_control=True)"],
        "main_exclusive": ["td005", "01088"],
        "preferer_option": ["Stun_or_confuse", "Draw_2_cards", "Confuse_an_enemy"],
        "declencher": [],
        "jouer": ["td005"],
        "verifier": "etat_attendu",
        "attendu": {"statuts": [["01094", "Confused"]], "statuts_absents": [["01094", "Stunned"]], "taille_main": 2},
    },
    {
        "nom": "[donatello] td005 Improvised Tactics — « cannot choose the same option twice » : Piocher 2 ne se fait qu'UNE fois",
        "pourquoi": ("on prefere « Draw 2 cards » aux deux questions : si la meme option pouvait etre prise deux fois la "
                     "main vaudrait 4 ; la deuxieme question propose autre chose, la main vaut 2"),
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.PutIntoPlay('td009', under_control=True)"],
        "main_exclusive": ["td005", "01088"],
        "preferer_option": ["Draw_2_cards"],
        "declencher": [],
        "jouer": ["td005"],
        "verifier": "etat_attendu",
        "attendu": {"taille_main": 2, "exhausted": ["td009"]},
    },
    {
        "nom": "[donatello] td005 Improvised Tactics — le cout est INCLINER une amelioration TECH : sans elle, la carte n'est pas jouable",
        "pourquoi": "aucune amelioration en jeu : la carte reste en main, rien n'est sonne ni pioche",
        **HEROS,
        "mise_en_place": [FORME_HEROS],
        "main_exclusive": ["td005", "01088"],
        "preferer_option": ["Stun_or_confuse", "Draw_2_cards"],
        "declencher": [],
        "jouer": ["td005"],
        "verifier": "etat_attendu",
        "attendu": {"en_main": ["td005", "01088"], "statuts_absents": [["01094", "Stunned"]], "taille_main": 2},
    },
]

# ========================================================================= td006 Singularity
CAS += [
    {
        "nom": "[donatello] td006 Singularity — INJOUABLE sans Anti-Gravity Gauntlet en jeu (« play only if you control »)",
        "pourquoi": "main = td006 + Genius + Strength (4 ressources, de quoi payer) mais aucun Gantelet : la carte reste en main, Rhino intact",
        **HEROS,
        "mise_en_place": [FORME_HEROS],
        "main_exclusive": ["td006", "01089", "01090"],
        "declencher": [],
        "jouer": ["td006"],
        "verifier": "etat_attendu",
        "attendu": {"en_main": ["td006"], "degats": [["01094", 0]]},
    },
    {
        "nom": "[donatello] td006 Singularity — avec le Gantelet : 10 degats a Rhino (aucune carte pour le +3 du Gantelet)",
        "pourquoi": ("Gantelet en jeu, main = td006 + Genius + Strength (cout 4 paye par les deux) : la main est vide apres le "
                     "paiement, l'interruption du Gantelet ne peut pas se payer, Rhino prend exactement 10"),
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.PutIntoPlay('td009', under_control=True)"],
        "main_exclusive": ["td006", "01089", "01090"],
        "payer_avec": ["01089", "01090"],
        "declencher": [],
        "jouer": ["td006"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 10]], "defausse": ["td006"], "pret": ["td009"]},
    },
    {
        "nom": "[donatello] td006 Singularity — OVERKILL : 10 degats sur Hydra Mercenary (PV 3), l'exces (7) va au vilain",
        "pourquoi": "« This attack gains overkill » : le sbire tombe, Rhino prend les 7 degats excedentaires",
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.PutIntoPlay('td009', under_control=True)", "Puzzle.PutIntoPlay('01101')"],
        "main_exclusive": ["td006", "01089", "01090"],
        "payer_avec": ["01089", "01090"],
        "cibles": ["01101"],
        "declencher": [],
        "jouer": ["td006"],
        "verifier": "etat_attendu",
        "attendu": {"hors_jeu": ["01101"], "degats": [["01094", 7]]},
    },
    {
        "nom": "[donatello] td006 Singularity — PIERCING : la carte Tenace de Black Widow est defaussee ET les 10 degats passent",
        "pourquoi": ("« This attack gains piercing » : Black Widow (PV 14) porte une carte Tenace ; sans perforation elle absorberait "
                     "les degats (0 degat). Avec : Tenace defaussee et 10 degats"),
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.PutIntoPlay('td009', under_control=True)", "Puzzle.PutIntoPlay('50148')",
                          "Puzzle.Tough('50148')"],
        "main_exclusive": ["td006", "01089", "01090"],
        "payer_avec": ["01089", "01090"],
        "cibles": ["50148"],
        "declencher": [],
        "jouer": ["td006"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["50148", 10]], "statuts_absents": [["50148", "Tough"]]},
    },
    {
        "nom": "[donatello] td006 Singularity — RANGED : la Riposte (Retaliate 1) de Black Widow est ignoree",
        "pourquoi": ("« This attack gains ranged » (ignore retaliate) : Black Widow (50148, PV 14, Retaliate 1) survit a 10 degats "
                     "et devrait riposter ; Donatello ne subit aucune riposte"),
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.PutIntoPlay('td009', under_control=True)", "Puzzle.PutIntoPlay('50148')"],
        "main_exclusive": ["td006", "01089", "01090"],
        "payer_avec": ["01089", "01090"],
        "cibles": ["50148"],
        "declencher": [],
        "jouer": ["td006"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 0, "degats": [["50148", 10]]},
    },
]

# ========================================================================= td007 Inspired Brilliance
# Carte sans texte ni script : seules comptent ses deux icones (mental + wild, desc.RES = BG).
CAS += [
    {
        "nom": "[donatello] td007 Inspired Brilliance — deux icones (mental + wild) : paie seule le cout 2 du Gantelet",
        "pourquoi": "main = Gantelet (cout 2) + td007 : la ressource doit valoir 2 (B + G), le Gantelet entre en jeu",
        **HEROS,
        "mise_en_place": [FORME_HEROS],
        "main_exclusive": ["td009", "td007"],
        "declencher": [],
        "jouer": ["td009"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["td009"], "defausse": ["td007"]},
    },
    {
        "nom": "[donatello] td007 Inspired Brilliance — TEMOIN : seulement DEUX icones, un cout de 4 (Singularity) n'est pas payable",
        "pourquoi": "main = Singularity (cout 4) + td007 : 2 icones ne suffisent pas, la carte reste en main (le Gantelet est en jeu)",
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.PutIntoPlay('td009', under_control=True)"],
        "main_exclusive": ["td006", "td007"],
        "declencher": [],
        "jouer": ["td006"],
        "verifier": "etat_attendu",
        "attendu": {"en_main": ["td006", "td007"], "degats": [["01094", 0]]},
    },
    {
        "nom": "[donatello] td007 Inspired Brilliance — la carte fournit bien une icone [mental] ET une icone wild",
        "pourquoi": "lecture directe de la ressource imprimee (desc.RES = BG) : B et G presentes, ni R ni Y",
        **HEROS,
        "mise_en_place": [FORME_HEROS],
        "main_exclusive": ["td007"],
        "declencher": [],
        "verifier": "td_ressource_imprimee",
        "attendu": {"carte": "td007", "presentes": ["B", "G"], "absentes": ["R", "Y"]},
    },
]

# ========================================================================= td008 Donnie's Lab
CAS += [
    {
        "nom": "[donatello] td008 Donnie's Lab — ramene une carte ANDROID de la defausse (Metalhead), incline le Laboratoire",
        "pourquoi": "Alter-Ego Action : Exhaust Lab -> add an ANDROID, ITEM or TECH card in your discard pile to your hand. Defausse : Metalhead (ANDROID)",
        **HEROS,
        "mise_en_place": ["Puzzle.PutIntoPlay('td008', under_control=True)", "Puzzle.CreatePlayerDiscardPile('td002', '01088')"],
        "main_exclusive": ["01088"],
        "cibles": ["td002"],
        "declencher": ["Puzzle.Action('td008', 'AlterEgoAction', 0)"],
        "verifier": "etat_attendu",
        "attendu": {"exhausted": ["td008"], "en_main": ["td002"], "taille_main": 2},
    },
    {
        "nom": "[donatello] td008 Donnie's Lab — ramene une carte ITEM (Truevision Goggles)",
        "pourquoi": "l'autre trait du « or » : td010 est ITEM et TECH, dans la defausse",
        **HEROS,
        "mise_en_place": ["Puzzle.PutIntoPlay('td008', under_control=True)", "Puzzle.CreatePlayerDiscardPile('td010', '01088')"],
        "main_exclusive": ["01088"],
        "cibles": ["td010"],
        "declencher": ["Puzzle.Action('td008', 'AlterEgoAction', 0)"],
        "verifier": "etat_attendu",
        "attendu": {"exhausted": ["td008"], "en_main": ["td010"]},
    },
    {
        "nom": "[donatello] td008 Donnie's Lab — ramene une carte TECH seule (Carapace td012 : ARMOR. TECH.)",
        "pourquoi": "td012 n'est ni ANDROID ni ITEM : seul le trait TECH la rend eligible",
        **HEROS,
        "mise_en_place": ["Puzzle.PutIntoPlay('td008', under_control=True)", "Puzzle.CreatePlayerDiscardPile('td012', '01088')"],
        "main_exclusive": ["01088"],
        "cibles": ["td012"],
        "declencher": ["Puzzle.Action('td008', 'AlterEgoAction', 0)"],
        "verifier": "etat_attendu",
        "attendu": {"exhausted": ["td008"], "en_main": ["td012"]},
    },
    {
        "nom": "[donatello] td008 Donnie's Lab — TEMOIN : une carte sans trait ANDROID/ITEM/TECH (Energy) n'est jamais ramenee",
        "pourquoi": ("la defausse contient Energy (sans trait) ET la main de depart defaussee par le harnais (cartes signature, dont "
                     "des TECH/ITEM) : on DEMANDE Energy, le moteur ne l'offre pas, la main n'en recoit jamais"),
        **HEROS,
        "mise_en_place": ["Puzzle.PutIntoPlay('td008', under_control=True)", "Puzzle.CreatePlayerDiscardPile('01088')"],
        "main_exclusive": ["01089"],
        "cibles": ["01088"],
        "declencher": ["Puzzle.Action('td008', 'AlterEgoAction', 0)"],
        "verifier": "etat_attendu",
        "attendu": {"exhausted": ["td008"], "absent_main": ["01088"], "taille_main": 2},
    },
    {
        "nom": "[donatello] td008 Donnie's Lab — « Alter-Ego Action » : refusee en forme HEROS (contre-cas)",
        "pourquoi": "forme heros, Metalhead dans la defausse : le Laboratoire reste pret, rien n'est ramene",
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.PutIntoPlay('td008', under_control=True)", "Puzzle.CreatePlayerDiscardPile('td002')"],
        "main_exclusive": ["01089"],
        "declencher": [],
        "declencher_tolerant": ["Puzzle.Action('td008', 'AlterEgoAction', 0)"],
        "verifier": "etat_attendu",
        "attendu": {"pret": ["td008"], "taille_main": 1, "absent_main": ["td002"]},
    },
]

# ========================================================================= td009 Anti-Gravity Gauntlet
CAS += [
    {
        "nom": "[donatello] td009 Anti-Gravity Gauntlet — Donatello gagne +1 ATQ en forme HEROS",
        "pourquoi": "ATQ imprime 1, +1 avec le Gantelet (nom propre : la face heros seulement)",
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.PutIntoPlay('td009', under_control=True)"],
        "declencher": [],
        "verifier": "etat_attendu",
        "attendu": {"attributs": {"attack": 1}},
    },
    {
        "nom": "[donatello] td009 Anti-Gravity Gauntlet — CONTRE-CAS : alter ego puis retour en heros, le bonus vaut toujours +1 (pas de cumul)",
        "pourquoi": ("Gantelet pose en forme heros, bascule en alter ego (Donnie n'a pas d'ATQ : rien ne peut fuir) puis retour : "
                     "ATQ = 1 imprime + 1, pas plus"),
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.PutIntoPlay('td009', under_control=True)", "Puzzle.ChangeForm('td001a')",
                          "Puzzle.ChangeForm('td001b')"],
        "declencher": [],
        "verifier": "etat_attendu",
        "attendu": {"forme": "Hero", "attributs": {"attack": 1}},
    },
    {
        "nom": "[donatello] td009 Anti-Gravity Gauntlet — Interrupt : evenement ATTACK joue, incline + defausse 1 carte -> +3 degats de CET evenement",
        "pourquoi": ("Press the Advantage (04043, ATTACK, cout 1, 2 degats). Main : l'evenement, Strength (RR paie le cout 1), Energy "
                     "(la carte defaussee pour le Gantelet). Rhino prend 2 + 3 = 5, Gantelet incline, Energy defaussee"),
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.PutIntoPlay('td009', under_control=True)"],
        "main_exclusive": ["04043", "01090", "01088"],
        "payer_avec": ["01090"],
        "declencher": [],
        "jouer": ["04043"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 5]], "exhausted": ["td009"], "defausse": ["01088", "04043"]},
    },
    {
        "nom": "[donatello] td009 Anti-Gravity Gauntlet — le +3 ne vaut que pour CET evenement : l'attaque de base suivante ne l'a pas",
        "pourquoi": ("apres l'evenement (Rhino a 5), une attaque de base : ATQ 1 + 1 (Gantelet) = 2 -> Rhino a 7 (un +3 fuyant "
                     "donnerait 10)"),
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.PutIntoPlay('td009', under_control=True)"],
        "main_exclusive": ["04043", "01090", "01088"],
        "payer_avec": ["01090"],
        "declencher": [],
        "jouer": ["04043"],
        "declencher_apres": ["Puzzle.Attack('td001a')"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 7]]},
    },
    {
        "nom": "[donatello] td009 Anti-Gravity Gauntlet — TEMOIN : evenement NON-ATTACK (Crisis Interdiction), l'interruption n'est pas offerte",
        "pourquoi": "01012 (thwart) joue : le Gantelet reste pret, la carte a defausser reste en main",
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.PutIntoPlay('td009', under_control=True)"],
        "main_exclusive": ["01012", "01088", "01089"],
        "payer_avec": ["01088"],
        "declencher": [],
        "jouer": ["01012"],
        "verifier": "etat_attendu",
        "attendu": {"pret": ["td009"], "en_main": ["01089"]},
    },
    {
        "nom": "[donatello] td009 Anti-Gravity Gauntlet — le cout « defausser 1 carte de la main » est obligatoire : main vide, pas de +3",
        "pourquoi": "Press the Advantage payee par Strength seule, plus aucune carte en main : Rhino prend 2 seulement, Gantelet pret",
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.PutIntoPlay('td009', under_control=True)"],
        "main_exclusive": ["04043", "01090"],
        "payer_avec": ["01090"],
        "declencher": [],
        "jouer": ["04043"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 2]], "pret": ["td009"]},
    },
]

# ========================================================================= td010 Truevision Goggles
CAS += [
    {
        "nom": "[donatello] td010 Truevision Goggles — contre de base : +1 CTR (3 au lieu de 2), Lunettes inclinees",
        "pourquoi": "manigance principale a 5 : contre de base 2 + 1 = 3 -> 2 ; aucun ennemi a statut, le +1 est offert quand meme",
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.PutIntoPlay('td010', under_control=True)", "Puzzle.SetThreat('01097b', 5)"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Thwart('td001a')"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["01097b", 2]], "exhausted": ["td010"]},
    },
    {
        "nom": "[donatello] td010 Truevision Goggles — « You MAY discard a status card from an enemy » : Rhino sonne perd sa carte",
        "pourquoi": "choix accepte (accepter_choix) : la carte Sonne de Rhino est defaussee, le +1 CTR a lieu aussi (5 -> 2)",
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.PutIntoPlay('td010', under_control=True)", "Puzzle.SetThreat('01097b', 5)",
                          "Puzzle.Stun('01094')"],
        "main_exclusive": ["01088"],
        "accepter_choix": True,
        "declencher": ["Puzzle.Thwart('td001a')"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["01097b", 2]], "statuts_absents": [["01094", "Stunned"]], "exhausted": ["td010"]},
    },
    {
        "nom": "[donatello] td010 Truevision Goggles — la defausse du statut est FACULTATIVE : le bouton Passer est offert, Rhino reste sonne",
        "pourquoi": "« You MAY » : on repond Passer a la question ; la carte Sonne reste, le +1 CTR a eu lieu (5 -> 2)",
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.PutIntoPlay('td010', under_control=True)", "Puzzle.SetThreat('01097b', 5)",
                          "Puzzle.Stun('01094')"],
        "main_exclusive": ["01088"],
        # La question « You may discard a status card from an enemy » propose une option « Cancel » : c'est elle qu'on choisit.
        "choisir_option": ["Cancel"],
        "questions_presentes": ["You may discard a status card from an enemy"],
        "declencher": ["Puzzle.Thwart('td001a')"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["01097b", 2]], "statuts": [["01094", "Stunned"]]},
    },
    {
        "nom": "[donatello] td010 Truevision Goggles — UNE seule carte de statut a la fois (sonne + desoriente : le choix en retire une)",
        "pourquoi": "Rhino sonne ET desoriente, on choisit « Discard a Confused » : seule Desoriente part, Sonne reste",
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.PutIntoPlay('td010', under_control=True)", "Puzzle.SetThreat('01097b', 5)",
                          "Puzzle.Stun('01094')", "Puzzle.Confuse('01094')"],
        "main_exclusive": ["01088"],
        "accepter_choix": True,
        "preferer_option": ["Discard_a_Confused"],
        "declencher": ["Puzzle.Thwart('td001a')"],
        "verifier": "etat_attendu",
        "attendu": {"statuts": [["01094", "Stunned"]], "statuts_absents": [["01094", "Confused"]]},
    },
    {
        "nom": "[donatello] td010 Truevision Goggles — TEMOIN : une attaque de base n'est pas un contre, Lunettes pretes, 2 degats (ATQ 1 +... aucun bonus)",
        "pourquoi": "« when you make a basic THWART » seulement : attaque de base (ATQ 1) -> Rhino 1 degat, Lunettes pretes",
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.PutIntoPlay('td010', under_control=True)"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Attack('td001a')"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 1]], "pret": ["td010"]},
    },
    {
        "nom": "[donatello] td010 Truevision Goggles — TEMOIN : un contre par EVENEMENT (Crisis Interdiction) n'est pas de base, Lunettes pretes",
        "pourquoi": "01012 retire 2 menaces (5 -> 3) sans le +1 : Lunettes pretes",
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.PutIntoPlay('td010', under_control=True)", "Puzzle.SetThreat('01097b', 5)"],
        "main_exclusive": ["01012", "01088"],
        "declencher": [],
        "jouer": ["01012"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["01097b", 3]], "pret": ["td010"]},
    },
]

# ========================================================================= td011 Donatello's Bo
CAS += [
    {
        "nom": "[donatello] td011 Donatello's Bō — Hero Action : incline le Bō, redresse Donatello",
        "pourquoi": "Donatello est incline (apres une action), l'action du Bō le redresse ; le Bō s'incline",
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.PutIntoPlay('td011', under_control=True)", "Puzzle.Exhaust('td001a')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Action('td011', 'HeroAction', 0)"],
        "verifier": "etat_attendu",
        "attendu": {"pret": ["td001a"], "exhausted": ["td011"]},
    },
    {
        "nom": "[donatello] td011 Donatello's Bō — contre-cas : refusee en ALTER EGO",
        "pourquoi": "forme alter ego : la Hero Action n'est pas offerte, le Bō reste pret",
        **HEROS,
        "mise_en_place": ["Puzzle.PutIntoPlay('td011', under_control=True)"],
        "main_exclusive": ["01088"],
        "declencher": [],
        "declencher_tolerant": ["Puzzle.Action('td011', 'HeroAction', 0)"],
        "verifier": "etat_attendu",
        "attendu": {"pret": ["td011"]},
    },
    {
        "nom": "[donatello] td011 Donatello's Bō — Restricted : 3 cartes Restreintes en jeu, une est defaussee (limite 2)",
        "pourquoi": ("Bō (td011, Restricted lu dans desc) + Captain America's Shield (03009) + Hawkeye's Bow (04002) : trois cartes "
                     "Restreintes, la limite de 2 impose d'en defausser une. Sans Restricted sur td011 les trois resteraient"),
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.PutIntoPlay('03009', under_control=True)", "Puzzle.PutIntoPlay('04002', under_control=True)",
                          "Puzzle.PutIntoPlay('td011', under_control=True)"],
        "main_exclusive": ["01088"],
        "declencher": [],
        "verifier": "td_compte_en_jeu",
        "attendu": {"ids": ["03009", "04002", "td011"], "nombre": 2},
    },
]

# ========================================================================= td012 Donatello's Shell
CAS += [
    {
        "nom": "[donatello] td012 Donatello's Shell — Hero Action : incline la Carapace et glisse UNE carte de la main dessous",
        "pourquoi": ("« Hero Action: Exhaust Donatello's Shell -> choose a card in your hand and tuck it here ». "
                     "Main = Genius + Energy, on choisit Genius : il part sous la Carapace, la main n'a plus qu'Energy"),
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.PutIntoPlay('td012', under_control=True)"],
        "main_exclusive": ["01089", "01088"],
        "cibles": ["01089"],
        "declencher": ["Puzzle.Action('td012', 'HeroAction', 0)"],
        "verifier": "etat_attendu",
        "attendu": {"exhausted": ["td012"], "pose_sous": [["td012", "01089"]],
                    "taille_pose_sous": [["td012", 1]], "taille_main": 1},
    },
    {
        "nom": "[donatello] td012 Donatello's Shell — TEMOIN « Max 1 tucked card » : une 2e carte n'est PAS glissee (Carapace redressee)",
        "pourquoi": ("la limite doit MORDRE seule : la Carapace est redressee entre les deux actions (sinon l'inclinaison "
                     "refuserait la 2e action et le cas ne prouverait rien). Si le plafond est inerte, la 2e carte "
                     "part dessous (2 cartes, Carapace inclinee) ; s'il mord, il reste 1 carte et la Carapace est prete"),
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.PutIntoPlay('td012', under_control=True)"],
        "main_exclusive": ["01089", "01088"],
        "cibles": ["01089"],
        "declencher": ["Puzzle.Action('td012', 'HeroAction', 0)", "Puzzle.Ready('td012')"],
        "declencher_tolerant": ["Puzzle.Action('td012', 'HeroAction', 0)"],
        "verifier": "etat_attendu",
        "attendu": {"pret": ["td012"], "taille_pose_sous": [["td012", 1]], "taille_main": 1},
    },
    {
        "nom": "[donatello] td012 Donatello's Shell — Hero Action : refusee en ALTER EGO (contre-cas)",
        "pourquoi": "la capacite est une « Hero Action » : en forme alter ego la Carapace reste prete et rien n'est glisse",
        **HEROS,
        "mise_en_place": ["Puzzle.PutIntoPlay('td012', under_control=True)"],
        "main_exclusive": ["01089", "01088"],
        "declencher": [],
        "declencher_tolerant": ["Puzzle.Action('td012', 'HeroAction', 0)"],
        "verifier": "etat_attendu",
        "attendu": {"pret": ["td012"], "taille_pose_sous": [["td012", 0]], "taille_main": 2},
    },
    {
        "nom": "[donatello] td012 Donatello's Shell — DEPENSER : une carte glissee paie le cout d'une carte de la main",
        "pourquoi": ("« spend ... cards tucked here as if they were in your hand ». Main = Aunt May (01006, cout 1, "
                     "Support) ; la SEULE ressource disponible est Energy (YY) glissee sous la Carapace. Aunt May doit "
                     "entrer en jeu et Energy finir en defausse"),
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.PutIntoPlay('td012', under_control=True)",
                          "Puzzle.PlaceUnder('01088', 'td012')"],
        "main_exclusive": ["01006"],
        "declencher": [],
        "jouer": ["01006"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["01006"], "defausse": ["01088"], "taille_pose_sous": [["td012", 0]]},
    },
    {
        "nom": "[donatello] td012 Donatello's Shell — DEPENSER, TEMOIN : sans carte glissee, Aunt May ne peut pas etre payee",
        "pourquoi": ("meme montage sans rien sous la Carapace et sans autre ressource en main : Aunt May reste en main "
                     "(sinon le cas precedent ne prouverait pas la Carapace)"),
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.PutIntoPlay('td012', under_control=True)"],
        "main_exclusive": ["01006"],
        "declencher": [],
        "jouer": ["01006"],
        "verifier": "etat_attendu",
        "attendu": {"hors_jeu": ["01006"], "en_main": ["01006"]},
    },
    {
        "nom": "[donatello] td012 Donatello's Shell — JOUER : une carte glissee se joue comme si elle etait en main",
        "pourquoi": ("« play ... cards tucked here as if they were in your hand ». Aunt May (cout 1) est glissee sous la "
                     "Carapace, la main ne garde qu'Energy (YY) qui paie : Aunt May doit entrer en jeu depuis la Carapace"),
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.PutIntoPlay('td012', under_control=True)",
                          "Puzzle.PlaceUnder('01006', 'td012')"],
        "main_exclusive": ["01088"],
        "declencher": [],
        "verifier": "td_jouer_sous_la_carapace",
        "attendu": {"carte": "01006", "en_jeu": ["01006"], "taille_pose_sous": [["td012", 0]]},
    },
    {
        "nom": "[donatello] td012 Donatello's Shell — DEFAUSSER (cout de td001b) : une carte glissee paie « discard 1 card from your hand »",
        "pourquoi": ("« ... or DISCARD cards tucked here as if they were in your hand » : Donnie (alter ego) a la main VIDE ; "
                     "Energy est glissee sous la Carapace. L'Action de td001b (cout : defausser 1 carte de la main) doit "
                     "etre offerte, defausser Energy et mettre td011 en jeu"),
        **HEROS,
        "mise_en_place": [MAIN_VIDE, "Puzzle.PutIntoPlay('td012', under_control=True)", "Puzzle.PlaceUnder('01088', 'td012')",
                          "Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01088', 'td011', '01088')"],
        "declencher": ["Puzzle.Action('td001b', 'Action', 0)"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["td011"], "defausse": ["01088"], "taille_pose_sous": [["td012", 0]], "taille_main": 0},
    },
    {
        "nom": "[donatello] td012 Donatello's Shell — DEFAUSSER, TEMOIN : main vide et rien sous la Carapace, l'Action de td001b n'est pas offerte",
        "pourquoi": "meme montage sans carte glissee : aucun cout payable, td011 reste dans le deck (sinon le cas precedent ne prouve rien)",
        **HEROS,
        "mise_en_place": [MAIN_VIDE, "Puzzle.PutIntoPlay('td012', under_control=True)",
                          "Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01088', 'td011', '01088')"],
        "declencher": [],
        "declencher_tolerant": ["Puzzle.Action('td001b', 'Action', 0)"],
        "verifier": "etat_attendu",
        "attendu": {"hors_jeu": ["td011"], "dans_deck_joueur": ["td011"]},
    },
    {
        "nom": "[donatello] td012 Donatello's Shell — DEFAUSSER (cout de td009) : la carte glissee paie le « discard 1 card from your hand » du Gantelet (+3 a Singularity)",
        "pourquoi": ("meme exigence sur une AUTRE carte du pack : Singularity (cout 4, payee par Genius + Strength) ; apres le paiement la main "
                     "est vide, Energy est sous la Carapace. L'interruption du Gantelet defausse Energy glissee : Rhino prend 10 + 3 = 13"),
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.PutIntoPlay('td012', under_control=True)",
                          "Puzzle.PutIntoPlay('td009', under_control=True)", "Puzzle.PlaceUnder('01088', 'td012')"],
        "main_exclusive": ["td006", "01089", "01090"],
        "payer_avec": ["01089", "01090"],
        "declencher": [],
        "jouer": ["td006"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 13]], "exhausted": ["td009"], "defausse": ["01088"], "taille_pose_sous": [["td012", 0]]},
    },
    {
        "nom": "[donatello] td012 Donatello's Shell — DEFAUSSER, TEMOIN : sans Carapace, la meme carte reste hors d'atteinte du Gantelet (10 degats seulement)",
        "pourquoi": "Energy est simplement dans le deck (pas sous une Carapace), main vide apres paiement : pas de +3, Rhino prend 10",
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.PutIntoPlay('td009', under_control=True)"],
        "main_exclusive": ["td006", "01089", "01090"],
        "payer_avec": ["01089", "01090"],
        "declencher": [],
        "jouer": ["td006"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 10]], "pret": ["td009"]},
    },
]

# ========================================================================= td013 Broken Shell
CAS += [
    {
        "nom": "[donatello] td013 Broken Shell — remise en forme heros : bascule en alter ego ET perd 5 PV (11 -> 6)",
        "pourquoi": "« Flip to alter-ego form and you lose 5 hit points » : Donatello (forme heros, 11 PV) recoit l'obligation",
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.Reveal('td013')"],
        "main_exclusive": ["01088"],
        "declencher": [],
        "verifier": "etat_attendu",
        "attendu": {"forme": "AlterEgo", "degats_identite": 5, "en_jeu": ["td013"]},
    },
    {
        "nom": "[donatello] td013 Broken Shell — « set your hit point dial to 1 instead » : plancher a 1 (PV 4 -> 1, pas de mort)",
        "pourquoi": "Donatello n'a plus que 4 PV (7 degats) : -5 le tuerait, le cadran passe a 1 et la partie continue",
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.Damage('td001a', 7)", "Puzzle.Reveal('td013')"],
        "main_exclusive": ["01088"],
        "declencher": [],
        "verifier": "etat_attendu",
        "attendu": {"forme": "AlterEgo", "degats_identite": 10, "en_jeu": ["td013"]},
    },
    {
        "nom": "[donatello] td013 Broken Shell — deja en ALTER EGO : pas de bascule a faire, -5 PV quand meme (11 -> 6)",
        "pourquoi": "Donnie recoit l'obligation : il est deja en alter ego, il perd 5 PV",
        **HEROS,
        "mise_en_place": ["Puzzle.Reveal('td013')"],
        "main_exclusive": ["01088"],
        "declencher": [],
        "verifier": "etat_attendu",
        "attendu": {"forme": "AlterEgo", "degats_identite": 5, "en_jeu": ["td013"]},
    },
    {
        "nom": "[donatello] td013 Broken Shell — « You cannot change to hero form » : le changement de forme est refuse",
        "pourquoi": "obligation en jeu, tentative de passer en forme heros : Donnie reste alter ego (et la partie ne plante pas)",
        **HEROS,
        "mise_en_place": ["Puzzle.Reveal('td013')"],
        "main_exclusive": ["01088"],
        "declencher": [],
        "declencher_tolerant": ["Puzzle.ChangeForm('td001b')"],
        "verifier": "etat_attendu",
        "attendu": {"forme": "AlterEgo", "en_jeu": ["td013"]},
    },
    {
        "nom": "[donatello] td013 Broken Shell — TEMOIN : sans l'obligation, le meme changement de forme reussit",
        "pourquoi": "meme geste sans Broken Shell : Donatello passe en forme heros (sinon le cas precedent ne prouve rien)",
        **HEROS,
        "mise_en_place": [],
        "main_exclusive": ["01088"],
        "declencher": [],
        "declencher_tolerant": ["Puzzle.ChangeForm('td001b')"],
        "verifier": "etat_attendu",
        "attendu": {"forme": "Hero"},
    },
    {
        "nom": "[donatello] td013 Broken Shell — Alter-Ego Action : depenser BB retire l'obligation DE LA PARTIE (pas defaussee)",
        "pourquoi": "Genius (BB) paie : Broken Shell n'est plus en jeu, et n'est pas dans la defausse de rencontre",
        **HEROS,
        "mise_en_place": ["Puzzle.Reveal('td013')"],
        "main_exclusive": ["01089"],
        "declencher": ["Puzzle.Action('td013', 'AlterEgoAction', 0)"],
        "verifier": "td_obligation_retiree",
        "attendu": {"carte": "td013", "defausse_genius": True},
    },
    {
        "nom": "[donatello] td013 Broken Shell — Alter-Ego Action : defausser la Carapace EN JEU retire l'obligation de la partie",
        "pourquoi": "aucune ressource mentale en main (Energy seulement) : seule la 2e capacite est offerte, la Carapace en jeu part a la defausse",
        **HEROS,
        "mise_en_place": ["Puzzle.Reveal('td013')", "Puzzle.PutIntoPlay('td012', under_control=True)"],
        "main_exclusive": ["01088"],
        # Les deux capacites « Remove Broken Shell » sont offertes dans l'ordre du script : 0 = BB, 1 = defausser la Carapace.
        "declencher": ["Puzzle.Action('td013', 'AlterEgoAction', 1)"],
        "verifier": "td_obligation_retiree",
        "attendu": {"carte": "td013", "defausse_carapace": True},
    },
    {
        "nom": "[donatello] td013 Broken Shell — apres le retrait, Donatello peut repasser en forme heros",
        "pourquoi": "obligation retiree par BB, puis changement de forme : il reussit",
        **HEROS,
        "mise_en_place": ["Puzzle.Reveal('td013')"],
        "main_exclusive": ["01089"],
        "declencher": ["Puzzle.Action('td013', 'AlterEgoAction', 0)", "Puzzle.ChangeForm('td001b')"],
        "verifier": "etat_attendu",
        "attendu": {"forme": "Hero", "hors_jeu": ["td013"]},
    },
    {
        "nom": "[donatello] td013 Broken Shell — TEMOIN : sans BB ni Carapace en jeu, l'Action n'est pas offerte, l'obligation reste",
        "pourquoi": "main = Energy, pas de Carapace : aucun des deux couts n'est payable",
        **HEROS,
        "mise_en_place": ["Puzzle.Reveal('td013')"],
        "main_exclusive": ["01088"],
        "declencher": [],
        "declencher_tolerant": ["Puzzle.Action('td013', 'AlterEgoAction', 0)", "Puzzle.Action('td013', 'AlterEgoAction', 1)"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["td013"], "en_main": ["01088"]},
    },
]

# ========================================================================= td014 Extermination!
DEUX = {"heros2": "spider_man"}
CAS += [
    {
        "nom": "[donatello] td014 Extermination! — manigance annexe : menace 2 par joueur (1 joueur : 2), icones : acceleration 1, boost 2",
        "pourquoi": "StartingThreat « 2 » + icone joueur = 2*, Acceleration 1 (comparee a Bomb Scare), 2 icones de boost",
        **HEROS,
        "mise_en_place": ["Puzzle.PutIntoPlay('td014')"],
        "declencher": [],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["td014", 2]], "icones": [["Acceleration", 1]], "icones_boost": [["td014", 2]]},
    },
    {
        "nom": "[donatello] td014 Extermination! — a DEUX joueurs : menace 4",
        "pourquoi": "« 2 par joueur » : 2 joueurs -> 4",
        **HEROS, **DEUX,
        "mise_en_place": ["Puzzle.PutIntoPlay('td014')"],
        "declencher": [],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["td014", 4]]},
    },
    {
        "nom": "[donatello] td014 Extermination! — When Defeated : un MOUSERS du deck rencontre entre en jeu, engage avec le premier joueur (UN seul)",
        "pourquoi": ("2 joueurs ; deck rencontre : Hydra Mercenary, td016 (MOUSERS), Shocker. Une fois la manigance deja vaincue, "
                     "td016 entre en jeu engage avec le PREMIER joueur ; ni Mercenary ni Shocker (un seul sbire)"),
        **HEROS, **DEUX,
        "mise_en_place": ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01103', 'td016', '01101')",
                          "Puzzle.PutIntoPlay('td014')"],
        "declencher": ["Puzzle.PlaceThreat('td014', -4)"],
        "verifier": "td_etat_carte",
        "attendu": {"carte": "td016", "compteurs": 2, "engage_premier": True, "absents": ["td014", "01101", "01103"]},
    },
    {
        "nom": "[donatello] td014 Extermination! — « MOUSER OR FLYBORG » : un FLYBORGS (td017) du deck rencontre convient aussi",
        "pourquoi": "l'autre moitie du « or » : deck rencontre = Mercenary + td017 seulement",
        **HEROS, **DEUX,
        "mise_en_place": ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('td017', '01101')",
                          "Puzzle.PutIntoPlay('td014')"],
        "declencher": ["Puzzle.PlaceThreat('td014', -4)"],
        "verifier": "td_etat_carte",
        "attendu": {"carte": "td017", "compteurs": 4, "engage_premier": True, "absents": ["td014", "01101"]},
    },
    {
        "nom": "[donatello] td014 Extermination! — cherche aussi dans la DEFAUSSE de rencontre",
        "pourquoi": "« the encounter deck AND discard pile » : td017 n'est que dans la defausse de rencontre, le deck n'a que Mercenary",
        **HEROS, **DEUX,
        "mise_en_place": ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01101')",
                          "Puzzle.CreateEncounterDiscardPile('td017')", "Puzzle.PutIntoPlay('td014')"],
        "declencher": ["Puzzle.PlaceThreat('td014', -4)"],
        "verifier": "td_etat_carte",
        "attendu": {"carte": "td017", "compteurs": 4, "engage_premier": True, "absents": ["td014"]},
    },
    {
        "nom": "[donatello] td014 Extermination! — aucun MOUSERS ni FLYBORGS nulle part : rien ne se passe (decision du 15/10), pas de plantage",
        "pourquoi": "deck rencontre = Mercenary + Shocker : la manigance est vaincue, aucun sbire n'entre en jeu",
        **HEROS, **DEUX,
        "mise_en_place": ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01103', '01101')",
                          "Puzzle.PutIntoPlay('td014')"],
        "declencher": ["Puzzle.PlaceThreat('td014', -4)"],
        "verifier": "etat_attendu",
        "attendu": {"hors_jeu": ["td014", "01101", "01103", "td016", "td017"]},
    },
]

# ========================================================================= td015 Baxter Stockman
CAS += [
    {
        "nom": "[donatello] td015 Baxter Stockman — PV 3, MNG 2, ATQ 0 (valeurs imprimees)",
        "pourquoi": "nombres du scan : disque orange 3 = PV, SCH 2, ATK 0",
        **HEROS,
        "mise_en_place": ["Puzzle.PutIntoPlay('td015')"],
        "declencher": [],
        "verifier": "td_etat_carte",
        "attendu": {"carte": "td015", "pv": 3, "atq": 0, "mng": 2},
    },
    {
        "nom": "[donatello] td015 Baxter Stockman — ne subit AUCUN degat tant qu'un MOUSERS (td016) est en jeu",
        "pourquoi": "td016 en jeu : 2 degats directs sur Baxter, aucun ne s'inscrit",
        **HEROS,
        "mise_en_place": ["Puzzle.PutIntoPlay('td015')", "Puzzle.PutIntoPlay('td016')"],
        "declencher": ["Puzzle.Damage('td015', 2)"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["td015", 0]]},
    },
    {
        "nom": "[donatello] td015 Baxter Stockman — ... ni tant qu'un FLYBORGS (td017) est en jeu",
        "pourquoi": "l'autre moitie du « or » : td017 en jeu, 2 degats sans effet",
        **HEROS,
        "mise_en_place": ["Puzzle.PutIntoPlay('td015')", "Puzzle.PutIntoPlay('td017')"],
        "declencher": ["Puzzle.Damage('td015', 2)"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["td015", 0]]},
    },
    {
        "nom": "[donatello] td015 Baxter Stockman — TEMOIN : aucun essaim en jeu, il subit les 2 degats",
        "pourquoi": "meme coup sans td016/td017 (un sbire ordinaire, Hydra Mercenary, ne le protege pas)",
        **HEROS,
        "mise_en_place": ["Puzzle.PutIntoPlay('td015')", "Puzzle.PutIntoPlay('01101')"],
        "declencher": ["Puzzle.Damage('td015', 2)"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["td015", 2]]},
    },
    {
        "nom": "[donatello] td015 Baxter Stockman — l'essaim parti, Baxter redevient vulnerable (la condition est dynamique)",
        "pourquoi": "td016 en jeu puis vaincu (3 degats) ; 2 degats sur Baxter ensuite : ils s'inscrivent",
        **HEROS,
        "mise_en_place": ["Puzzle.PutIntoPlay('td015')", "Puzzle.PutIntoPlay('td016')"],
        "declencher": ["Puzzle.Damage('td016', 3)", "Puzzle.Damage('td015', 2)"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["td015", 2]], "hors_jeu": ["td016"]},
    },
    {
        "nom": "[donatello] td015 Baxter Stockman — Forced Interrupt : il va attaquer, il MANIGANCE a la place (menace sur le complot, aucun degat)",
        "pourquoi": ("Baxter (ATQ 0) « would attack you, he schemes instead » : complot principal a 0 -> la menace monte "
                     "(MNG 2 + boost), Donatello n'est pas touche. Sans le module il attaquerait pour 0 et la menace resterait a 0"),
        **HEROS,
        "mise_en_place": ["Puzzle.SetThreat('01097b', 0)", "Puzzle.PutIntoPlay('td015')"],
        "declencher": ["Puzzle.Attack('td015')"],
        "verifier": "etat_attendu",
        "attendu": {"menace_min": [["01097b", 2]], "degats_identite": 0},
    },
    {
        "nom": "[donatello] td015 Baxter Stockman — Quickstrike : engage par la revelation, il agit aussitot et manigance",
        "pourquoi": "Quickstrike lu dans desc : Baxter revele s'engage et s'active tout de suite ; l'Interrupt le fait manigancer (menace >= 2)",
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.SetThreat('01097b', 0)", "Puzzle.Reveal('td015')"],
        "declencher": [],
        "verifier": "etat_attendu",
        "attendu": {"menace_min": [["01097b", 2]], "degats_identite": 0, "en_jeu": ["td015"]},
    },
    {
        "nom": "[donatello] td015 Baxter Stockman — Quickstrike : TEMOIN, engage avec Donnie (alter ego) il n'agit pas (regle du moteur : heros seulement)",
        "pourquoi": "meme revelation en forme alter ego : Quickstrike ne se declenche pas, la menace reste a 0",
        **HEROS,
        "mise_en_place": ["Puzzle.SetThreat('01097b', 0)", "Puzzle.Reveal('td015')"],
        "declencher": [],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["01097b", 0]], "en_jeu": ["td015"]},
    },
]

# ========================================================================= td016 / td017 : jeu reel des essaims
CAS += [
    {
        "nom": "[donatello] td016 Plague of M.O.U.S.E.R.s — attaque avec ATQ = compteurs : 2 degats a Donatello epuise",
        "pourquoi": "ATQ 2 (2 compteurs), Donatello epuise ne se defend pas : 2 degats",
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.Exhaust('td001a')", "Puzzle.PutIntoPlay('td016')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Attack('td016')"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 2},
    },
    {
        "nom": "[donatello] td016 Plague of M.O.U.S.E.R.s — l'ATQ SUIT les compteurs : 1 compteur retire, l'attaque ne fait plus que 1",
        "pourquoi": "1 degat (1 compteur) puis attaque : ATQ 1 -> 1 degat a Donatello epuise",
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.Exhaust('td001a')", "Puzzle.PutIntoPlay('td016')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Damage('td016', 1)", "Puzzle.Attack('td016')"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 1},
    },
    {
        "nom": "[donatello] td016 Plague of M.O.U.S.E.R.s — manigance avec MNG = compteurs : +2 menace sur le complot (a 0 au depart)",
        "pourquoi": "MNG 2 : Puzzle.Scheme pose au moins 2 menaces (et au plus 2 + les icones de boost du deck)",
        **HEROS,
        "mise_en_place": ["Puzzle.SetThreat('01097b', 0)", "Puzzle.PutIntoPlay('td016')"],
        "declencher": ["Puzzle.Scheme('td016')"],
        "verifier": "etat_attendu",
        "attendu": {"menace_min": [["01097b", 2]]},
    },
    {
        "nom": "[donatello] td016 Plague of M.O.U.S.E.R.s — attaque de base de Donatello (ATQ 1) : retire 1 compteur, le sbire survit avec 1",
        "pourquoi": "chemin reel d'une attaque de heros contre l'essaim : 1 degat -> 1 compteur, PV 1",
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.PutIntoPlay('td016')"],
        "main_exclusive": ["01088"],
        "cibles": ["td016"],
        "declencher": ["Puzzle.Attack('td001a')"],
        "verifier": "td_etat_carte",
        "attendu": {"carte": "td016", "compteurs": 1, "pv": 1, "atq": 1},
    },
    {
        "nom": "[donatello] td016 Plague of M.O.U.S.E.R.s — attaque de base avec le Gantelet (ATQ 2) : vaincu par le moteur, va en defausse de rencontre",
        "pourquoi": "ATQ 1 + 1 = 2 = les 2 compteurs : PV a 0, le moteur vainc le sbire, qui part en defausse de rencontre",
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.PutIntoPlay('td009', under_control=True)", "Puzzle.PutIntoPlay('td016')"],
        "main_exclusive": ["01088"],
        "cibles": ["td016"],
        "declencher": ["Puzzle.Attack('td001a')"],
        "verifier": "td_etat_carte",
        "attendu": {"carte": "td016", "en_jeu": False, "defausse_rencontre": True},
    },
    {
        "nom": "[donatello] td017 Flight of Flyborgs — 10 degats d'un coup (Singularity, Overkill) : vaincu, aucun exces pour Rhino (les degats sont REMPLACES)",
        "pourquoi": ("« remove that number of swarm counters INSTEAD » : le coup n'est pas un degat, donc pas d'exces a reporter : "
                     "le sbire (4 compteurs) est vaincu, Rhino reste a 0 degat (mesure du comportement du moteur)"),
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.PutIntoPlay('td009', under_control=True)", "Puzzle.PutIntoPlay('td017')"],
        "main_exclusive": ["td006", "01089", "01090"],
        "payer_avec": ["01089", "01090"],
        "cibles": ["td017"],
        "declencher": [],
        "jouer": ["td006"],
        "verifier": "td_etat_carte",
        "attendu": {"carte": "td017", "en_jeu": False, "defausse_rencontre": True, "rhino_degats": 0},
    },
]

# FIN-DES-CAS-A-COMPLETER

VERIFICATIONS = r'''
def td_etat_carte(monde, aides):
    """Etat d'une carte du pack Donatello. attendu : carte, en_jeu (defaut True), compteurs (swarm), pv (sante
    restante), pv_max, atq, mng, ctr, statut, consecutifs ([atq, ctr])."""
    attendu = aides["cas"]["attendu"]
    face = aides["par_id"](monde, attendu["carte"])
    # Cartes qui ne doivent PAS etre en jeu (un seul sbire cherche par Extermination!, etc.).
    presentes = [c for c in attendu.get("absents", []) if aides["par_id"](monde, c) is not None]
    if presentes:
        return False, f"encore en jeu alors qu'elles ne devraient pas : {presentes}"
    if "rhino_degats" in attendu:
        rhino = aides["par_id"](monde, "01094")
        if rhino.max_health - rhino.health != attendu["rhino_degats"]:
            return False, f"Rhino a {rhino.max_health - rhino.health} degat(s) (attendu {attendu['rhino_degats']})"
    if not attendu.get("en_jeu", True):
        if face is not None:
            return False, (f"{attendu['carte']} est encore en jeu (PV {face.health}/{face.max_health}, "
                           f"compteurs {face.GetCounters('swarm')})")
        if attendu.get("defausse_rencontre"):
            from game.operate.worlds import Worlds
            ids = [getattr(f.paper, "card_id", None) for f in Worlds.GetEncounterDiscardPileCards(monde)]
            if attendu["carte"] not in ids:
                return False, f"{attendu['carte']} n'est pas dans la defausse de rencontre ({ids})"
        return True, f"{attendu['carte']} n'est plus en jeu"
    if face is None:
        return False, f"{attendu['carte']} n'est pas en jeu"
    if attendu.get("engage_premier") and face.GetEngagedPlayer() is not monde.GetFirstPlayer():
        return False, f"{attendu['carte']} n'est pas engage avec le premier joueur (engage avec {face.GetEngagedPlayer()})"
    mesure = {"compteurs": face.GetCounters("swarm"), "pv": face.health, "pv_max": face.max_health,
              "atq": face.attack, "mng": getattr(face, "scheme", None), "ctr": getattr(face, "thwart", None)}
    ecarts = [f"{k}={mesure[k]} (attendu {v})" for k, v in attendu.items() if k in mesure and mesure[k] != v]
    if "statut" in attendu and not face.HasStatus(attendu["statut"]):
        ecarts.append(f"statut {attendu['statut']} absent")
    if "consecutifs" in attendu:
        vus = [face.attack_consequential_damage, face.thwart_consequential_damage]
        if vus != attendu["consecutifs"]:
            ecarts.append(f"degats consecutifs {vus} (attendu {attendu['consecutifs']})")
    if ecarts:
        return False, " ; ".join(ecarts) + f" [mesure {mesure}]"
    return True, f"etat conforme {mesure}"


def td_ressource_imprimee(monde, aides):
    """Couleurs de ressource imprimees d'une carte de la main. attendu : carte, presentes, absentes."""
    attendu = aides["cas"]["attendu"]
    face = None
    for f in monde.players[0].hand_cards.GetAll():
        if getattr(f.paper, "card_id", None) == attendu["carte"]:
            face = f
    if face is None:
        return False, f"{attendu['carte']} absente de la main"
    soucis = []
    for c in attendu.get("presentes", []):
        if not face.printed_resource.HasColorPrinted(c):
            soucis.append(f"icone {c} absente")
    for c in attendu.get("absentes", []):
        if face.printed_resource.HasColorPrinted(c):
            soucis.append(f"icone {c} presente a tort")
    if soucis:
        return False, " ; ".join(soucis)
    return True, "icones conformes"


def td_obligation_retiree(monde, aides):
    """Broken Shell est retiree DE LA PARTIE : plus en jeu, ni en defausse du joueur ni en defausse de rencontre ;
    elle est dans la zone « retiree » du monde. attendu : carte, defausse_genius / defausse_carapace (le cout)."""
    attendu = aides["cas"]["attendu"]
    cid = attendu["carte"]
    if aides["par_id"](monde, cid) is not None:
        return False, f"{cid} est encore en jeu"
    ids_joueur = [getattr(f.paper, "card_id", None) for f in monde.players[0].discard_pile.Get()]
    from game.operate.worlds import Worlds
    ids_rencontre = [getattr(f.paper, "card_id", None) for f in Worlds.GetEncounterDiscardPileCards(monde)]
    if cid in ids_joueur or cid in ids_rencontre:
        return False, f"{cid} a ete DEFAUSSEE (joueur {ids_joueur}, rencontre {ids_rencontre}) au lieu d'etre retiree de la partie"
    retirees = [getattr(f.paper, "card_id", None) for f in monde.area_removed.GetAll()]
    if cid not in retirees:
        return False, f"{cid} n'est pas dans la zone des cartes retirees de la partie ({retirees})"
    if attendu.get("defausse_genius") and "01089" not in ids_joueur:
        return False, "Genius (cout BB) n'est pas dans la defausse"
    if attendu.get("defausse_carapace") and "td012" not in ids_joueur:
        return False, "la Carapace (cout) n'est pas dans la defausse"
    return True, f"{cid} retiree de la partie ; defausse joueur {ids_joueur}"


def td_compte_en_jeu(monde, aides):
    """Nombre de cartes de `ids` encore en jeu. attendu : ids, nombre."""
    attendu = aides["cas"]["attendu"]
    en_jeu = [c for c in attendu["ids"] if aides["par_id"](monde, c) is not None]
    if len(en_jeu) != attendu["nombre"]:
        return False, f"{len(en_jeu)} en jeu {en_jeu} (attendu {attendu['nombre']})"
    return True, f"en jeu : {en_jeu}"


def td_jouer_sous_la_carapace(monde, aides):
    """Joue une carte GLISSEE sous Donatello's Shell par le vrai chemin (meme geste que le clic du joueur :
    on demande les effets « Play » de la carte, le filtre du gestionnaire d'evenements les ecarte ou non,
    puis on resout et on PAIE). Si le moteur n'offre pas la carte, le cas echoue. Puis `etat_attendu`."""
    from game.message import Message
    from game.effect.rule import GameRule
    from game.event.manager import EventManager
    attendu = aides["cas"]["attendu"]
    joueur = monde.players[0]
    carapace = aides["par_id"](monde, "td012")
    if carapace is None:
        return False, "td012 n'est pas en jeu"
    face = None
    for f in carapace.GetPlacedCardArea().Get(True):
        if f is not None and getattr(f.paper, "card_id", None) == attendu["carte"]:
            face = f
    if face is None:
        return False, f"{attendu['carte']} n'est pas glissee sous la Carapace"
    effets = face.effect.Find(func_name="Play", when=Message.WhenPlayerInTurn)
    message = Message.WhenPlayerLikeInTurn(joueur, GameRule(joueur.GetIdentity()))
    message.Send()
    disponibles = EventManager.FilterAvailableEffects(message, effets, joueur, monde, None)
    if not disponibles:
        return False, f"le moteur n'offre PAS de jouer {attendu['carte']} depuis la Carapace"
    joueur.ChooseEffects([disponibles[0]], message, forced=False)
    return etat_attendu(monde, aides)
'''
