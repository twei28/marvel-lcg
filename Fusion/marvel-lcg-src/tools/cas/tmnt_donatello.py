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
        "nom": "[donatello] td006 Singularity — PIERCING : un sbire Tenace tombe quand meme (la carte Tenace est defaussee, pas obstacle)",
        "pourquoi": ("« This attack gains piercing » : Hydra Mercenary porte une carte Tenace ; sans perforation elle absorberait "
                     "les degats et le sbire survivrait"),
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.PutIntoPlay('td009', under_control=True)", "Puzzle.PutIntoPlay('01101')",
                          "Puzzle.Tough('01101')"],
        "main_exclusive": ["td006", "01089", "01090"],
        "payer_avec": ["01089", "01090"],
        "cibles": ["01101"],
        "declencher": [],
        "jouer": ["td006"],
        "verifier": "etat_attendu",
        "attendu": {"hors_jeu": ["01101"]},
    },
    {
        "nom": "[donatello] td006 Singularity — RANGED : la Riposte de Whiplash (Retaliate 1) est ignoree",
        "pourquoi": ("« This attack gains ranged » (ignore retaliate) : Whiplash (PV 4, Tenace retiree) est vaincu par 10 degats ; "
                     "Donatello ne subit aucune riposte"),
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.PutIntoPlay('td009', under_control=True)", "Puzzle.PutIntoPlay('01172')"],
        "main_exclusive": ["td006", "01089", "01090"],
        "payer_avec": ["01089", "01090"],
        "cibles": ["01172"],
        "declencher": [],
        "jouer": ["td006"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 0},
    },
]

# FIN-DES-CAS-A-COMPLETER

VERIFICATIONS = r'''
def td_etat_carte(monde, aides):
    """Etat d'une carte du pack Donatello. attendu : carte, en_jeu (defaut True), compteurs (swarm), pv (sante
    restante), pv_max, atq, mng, ctr, statut, consecutifs ([atq, ctr])."""
    attendu = aides["cas"]["attendu"]
    face = aides["par_id"](monde, attendu["carte"])
    if not attendu.get("en_jeu", True):
        if face is not None:
            return False, (f"{attendu['carte']} est encore en jeu (PV {face.health}/{face.max_health}, "
                           f"compteurs {face.GetCounters('swarm')})")
        return True, f"{attendu['carte']} n'est plus en jeu"
    if face is None:
        return False, f"{attendu['carte']} n'est pas en jeu"
    mesure = {"compteurs": face.GetCounters("swarm"), "pv": face.health, "pv_max": face.max_health,
              "atq": face.attack, "mng": getattr(face, "scheme", None), "ctr": face.thwart}
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
