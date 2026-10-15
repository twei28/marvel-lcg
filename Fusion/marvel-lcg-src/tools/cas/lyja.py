# Cas test_capacites du heros Lyja (Kajislav, coffret Skrull Menace) : prefixe « [lyja] ».
# Un cas par capacite, sujet = le card_id dans le nom. Voir .planning/skrull-menace/LYJA-GABARITS.md.
#
# Rappels de montage : `Puzzle.CreateEncounterDeck(a, b, c)` : la DERNIERE carte creee est
# sur le dessus ; Lyja demarre en alter ego (sk037b) ; `ChangeToFace('sk037b', 'sk037a')`
# la passe en forme heros ; 01111 Explosion et 01112 False Alarm sont des traitrises du
# set Bomb Scare (sans effet a la revelation qui gene la mesure), 01101 un sbire.

HEROS = {
    "scenario": "rhino",
    "heros": "lyja",
}
FORME_HEROS = "Puzzle.ChangeToFace('sk037b', 'sk037a')"

CAS = [
    # ===================================================================== sk037a / sk037b
    {
        "nom": "[lyja] sk037a Skrull Spy — depense 1 ressource : une traitrise du deck rencontre va sur le dessus",
        "pourquoi": ("Action « spend up to 1[per_hero] resources → search the encounter deck for a TREACHERY card "
                     "for each resource spent, shuffle, place on top ». Solo : 1 ressource (01088 de la main), "
                     "deck rencontre 01101 (sbire) / 01111 / 01112 (traitrises) / 01101"),
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.EmptyEncounterDeck()",
                          "Puzzle.CreateEncounterDeck('01101', '01112', '01111', '01101')"],
        "main_exclusive": ["sk064"],  # UNE icone de ressource (le cout est « jusqu'a 1 »)
        "surpayer": True,  # up_to : le pilote ne paie rien sans cela
        "declencher": ["Puzzle.Action('sk037a', 'Action', 0)"],
        "verifier": "lyja_dessus_rencontre",
        "attendu": {"dessus_parmi": [["01111", "01112"]], "taille": 4, "traitrises_dessus": 1, "face_cachee": True},
    },
    {
        "nom": "[lyja] sk037a Skrull Spy — a DEUX joueurs : jusqu'a 2 ressources, 2 traitrises sur le dessus",
        "pourquoi": ("« up to 1[per_hero] » : 2 joueurs -> jusqu'a 2 ressources (sk064 + sk043, une icone chacune), "
                     "2 traitrises cherchees (01111 et 01112) puis posees sur le dessus dans l'ordre choisi"),
        "scenario": "rhino",
        "heros": "lyja",
        "heros2": "spider_man",
        "mise_en_place": [FORME_HEROS, "Puzzle.EmptyEncounterDeck()",
                          "Puzzle.CreateEncounterDeck('01101', '01112', '01111', '01101')"],
        "main_exclusive": ["sk064", "sk043"],
        "surpayer": True,
        "declencher": ["Puzzle.Action('sk037a', 'Action', 0)"],
        "verifier": "lyja_dessus_rencontre",
        "attendu": {"dessus_parmi": [["01111", "01112"], ["01111", "01112"]], "taille": 4, "traitrises_dessus": 2, "face_cachee": True},
    },
    {
        "nom": "[lyja] sk037a Skrull Spy — TEMOIN : aucune traitrise dans le deck rencontre, rien ne monte",
        "pourquoi": "contre-cas : sans traitrise a trouver, la recherche ne ramene rien ; le deck garde ses 3 cartes",
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.EmptyEncounterDeck()",
                          "Puzzle.CreateEncounterDeck('01101', '01102', '01103')"],
        "main_exclusive": ["sk064"],  # UNE icone de ressource (le cout est « jusqu'a 1 »)
        "surpayer": True,  # up_to : le pilote ne paie rien sans cela
        "declencher": ["Puzzle.Action('sk037a', 'Action', 0)"],
        "verifier": "lyja_dessus_rencontre",
        "attendu": {"taille": 3, "traitrises_dessus": 0},
    },
    {
        "nom": "[lyja] sk037b Playing Along — une traitrise du deck joueur monte sur le dessus",
        "pourquoi": ("Action d'alter ego « search your deck for a TREACHERY card, shuffle, place on top ». "
                     "Deck : 01090 (dessus), 01088, sk039, 01089 -> sk039 doit etre sur le dessus"),
        **HEROS,
        "mise_en_place": ["Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01089', 'sk039', '01088', '01090')"],
        "declencher": ["Puzzle.Action('sk037b', 'Action', 0)"],
        "verifier": "lyja_dessus_deck_joueur",
        "attendu": {"dessus": ["sk039"], "taille": 4},
    },
    {
        "nom": "[lyja] sk037b Playing Along — TEMOIN D'EPUISEMENT : la 2e activation du round est refusee",
        "pourquoi": ("« Limit once per round » : 1re activation (une traitrise monte), on la pioche, puis 2e activation. "
                     "Deck : 01090 (dessus), 01088, sk040, sk039, 01089. Si la limite mord, la 2e activation "
                     "n'a pas lieu et le dessus reste une carte NON traitrise ; si elle est inerte, l'autre traitrise "
                     "remonte sur le dessus"),
        **HEROS,
        "mise_en_place": ["Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01089', 'sk039', 'sk040', '01088', '01090')"],
        "declencher": ["Puzzle.Action('sk037b', 'Action', 0)", "Puzzle.Draw(1)"],
        "declencher_tolerant": ["Puzzle.Action('sk037b', 'Action', 0)"],
        "verifier": "lyja_dessus_deck_joueur",
        "attendu": {"dessus_non_traitrise": True, "taille": 4},
    },
    {
        "nom": "[lyja] sk037b Playing Along — TEMOIN D'ABSENCE : sans traitrise dans le deck, rien ne se passe",
        "pourquoi": "le deck est fouille et melange, aucune traitrise ne monte sur le dessus",
        **HEROS,
        "mise_en_place": ["Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01089', '01088', '01090')"],
        "declencher": ["Puzzle.Action('sk037b', 'Action', 0)"],
        "verifier": "lyja_dessus_deck_joueur",
        "attendu": {"taille": 3, "dessus_non_traitrise": True},
    },
    # ===================================================================== sk038
    {
        "nom": "[lyja] sk038 Human Torch — apres avoir quitte le jeu : une traitrise du deck rencontre va sur le dessus",
        "pourquoi": ("Reponse « after Human Torch leaves play, search the encounter deck for a TREACHERY card, "
                     "shuffle, place on top ». Human Torch defausse du jeu ; deck 01101 / 01112 / 01101"),
        **HEROS,
        "mise_en_place": ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01101', '01112', '01101')",
                          "Puzzle.PutIntoPlay('sk038', under_control=True)"],
        "declencher": ["Puzzle.Discard('sk038')"],
        "verifier": "lyja_dessus_rencontre",
        "attendu": {"dessus": ["01112"], "taille": 3, "face_cachee": True},
    },
    # ===================================================================== sk039
    {
        "nom": "[lyja] sk039 Faking Death — Hero Action : l'evenement se melange dans le deck rencontre",
        "pourquoi": "Hero Action « shuffle this card into the encounter deck » : cout 1 paye (01088), la carte quitte la main",
        **HEROS,
        "mise_en_place": [FORME_HEROS],
        "main_exclusive": ["sk039", "01088"],
        "jouer": ["sk039"],
        "declencher": [],
        "verifier": "etat_attendu",
        "attendu": {"dans_deck_rencontre": ["sk039"], "absent_main": ["sk039"]},
    },
    {
        "nom": "[lyja] sk039 Faking Death — When Revealed : l'ennemi est sonne ; la carte va dans la defausse du joueur",
        "pourquoi": ("« Choose to either stun or confuse an enemy » : le pilote prend la 1re option (sonner), "
                     "Rhino est la seule cible. Carte joueur revelee depuis le deck rencontre : defausse du PROPRIETAIRE"),
        **HEROS,
        "mise_en_place": [],
        "declencher": ["Puzzle.Reveal('sk039')"],
        "verifier": "etat_attendu",
        "attendu": {"statuts": [["01094", "Stunned"]], "defausse": ["sk039"], "aucune_en_resolution": True},
    },
    {
        "nom": "[lyja] sk039 Faking Death — Boost : l'ennemi qui active (Rhino ATK 2) perd 2 ATK pour cette attaque",
        "pourquoi": ("★ Boost « the activating enemy gets -2 SCH and -2 ATK for this activation » : Rhino (ATK 2) attaque "
                     "Laura Green sans defenseur, carte de boost = sk039 : 2 - 2 = 0 degat"),
        **HEROS,
        "mise_en_place": ["Puzzle.EmptyEncounterDeck()", "Puzzle.MoveTo('sk039', 'EncounterDeck')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Attack('01094')"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 0},
    },
    {
        "nom": "[lyja] sk039 Faking Death — Boost, TEMOIN : avec une carte de boost 01101 (1 icone), Rhino fait 3 degats",
        "pourquoi": "ligne de base de la mesure precedente : Rhino ATK 2 + 1 icone de boost (Hydra Mercenary) = 3",
        **HEROS,
        "mise_en_place": ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01101')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Attack('01094')"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 3},
    },
    # ===================================================================== sk040
    {
        "nom": "[lyja] sk040 Feign Loyalty — When Revealed : l'attachement a Hero Action est defausse, l'autre reste",
        "pourquoi": ("« Discard an attachment with the uses keyword or the text Hero Action / Hero Response » : "
                     "01100 Enhanced Ivory Horn (Hero Action) part, 01098 Armored Rhino Suit (aucun) reste"),
        **HEROS,
        "mise_en_place": ["Puzzle.PutIntoPlay('01100')", "Puzzle.PutIntoPlay('01098')"],
        "declencher": ["Puzzle.Reveal('sk040')"],
        "verifier": "etat_attendu",
        "attendu": {"hors_jeu": ["01100"], "en_jeu": ["01098"], "defausse": ["sk040"], "aucune_en_resolution": True},
    },
    {
        "nom": "[lyja] sk040 Feign Loyalty — Boost : le joueur pioche 2 cartes",
        "pourquoi": "★ Boost « draw 2 cards » : main de depart 1 carte (01088), Rhino attaque, boost = sk040 -> main 3",
        **HEROS,
        "mise_en_place": ["Puzzle.EmptyEncounterDeck()", "Puzzle.MoveTo('sk040', 'EncounterDeck')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Attack('01094')"],
        "verifier": "etat_attendu",
        "attendu": {"taille_main": 3},
    },
    # ===================================================================== sk041
    {
        "nom": "[lyja] sk041 Hero Appearance — When Revealed : 4 degats repartis sur les ennemis en jeu",
        "pourquoi": ("« The Lyja player deals 4 damage among enemies in play » : Rhino seul ennemi, 4 choix -> 4 degats "
                     "par l'identite de Lyja"),
        **HEROS,
        "mise_en_place": [],
        "declencher": ["Puzzle.Reveal('sk041')"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 4]], "defausse": ["sk041"], "aucune_en_resolution": True},
    },
    {
        "nom": "[lyja] sk041 Hero Appearance — Boost : 3 degats a un ennemi",
        "pourquoi": "★ Boost « the Lyja player deals 3 damage to an enemy » : Rhino active, boost = sk041 -> 3 degats sur Rhino",
        **HEROS,
        "mise_en_place": ["Puzzle.EmptyEncounterDeck()", "Puzzle.MoveTo('sk041', 'EncounterDeck')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Attack('01094')"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 3]]},
    },
    # ===================================================================== sk042
    {
        "nom": "[lyja] sk042 Posing as a Civilian — When Revealed : retire 3 menaces du complot principal",
        "pourquoi": "« removes 3 threat from among schemes in play » : menace 6 sur The Break-In! (01097b) -> 3",
        **HEROS,
        "mise_en_place": ["Puzzle.SetThreat('01097b', 6)"],
        "declencher": ["Puzzle.Reveal('sk042')"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["01097b", 3]], "defausse": ["sk042"], "aucune_en_resolution": True},
    },
    {
        "nom": "[lyja] sk042 Posing as a Civilian — Boost : retire 2 menaces d'une manigance",
        "pourquoi": ("★ Boost « the Lyja player removes 2 threat from a scheme » : Rhino attaque Laura Green "
                     "(forme heros, sans defenseur) ; menace 6 -> 4"),
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.SetThreat('01097b', 6)", "Puzzle.EmptyEncounterDeck()",
                          "Puzzle.MoveTo('sk042', 'EncounterDeck')"],
        "main_exclusive": ["01088"],
        "passer_sur_option": "Defense",
        "declencher": ["Puzzle.Attack('01094')"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["01097b", 4]]},
    },
    # ===================================================================== sk043
    {
        "nom": "[lyja] sk043 New York Bookstore — Laura Green gagne +2 REC (REC 3 -> 5)",
        "pourquoi": "« Laura Green gets +2 REC » : `GiveKeywordToInPlayWhenApplyThis(CardFinder(name='Laura Green'), recover=2)` ; l'alter ego est la forme de depart",
        **HEROS,
        "mise_en_place": ["Puzzle.PutIntoPlay('sk043', under_control=True)"],
        "declencher": [],
        "verifier": "etat_attendu",
        "attendu": {"attributs": {"recover": 2}},
    },
    {
        "nom": "[lyja] sk043 New York Bookstore — Alter-Ego Response : apres une recuperation de base, pioche 1 carte",
        "pourquoi": ("modele tg007 : `AfterUnitMakeRecovery(AlterEgoResponse, 'You', op, is_basic_recovery=True)`. Main d'une carte "
                     "(01090, non depensee), deck [01089] : la recuperation de base (Laura blessee de 6) pioche -> 2 cartes"),
        **HEROS,
        "mise_en_place": ["Puzzle.PutIntoPlay('sk043', under_control=True)", "Puzzle.Damage('sk037b', 6)",
                          "Puzzle.CreatePlayerDeck('01089')"],
        "main_exclusive": ["01090"],
        "ne_pas_depenser": ["01090"],
        "declencher": ["Puzzle.Action('sk037b', 'BasicPower')"],
        "verifier": "etat_attendu",
        "attendu": {"taille_main": 2},
    },
    # ===================================================================== sk044
    {
        "nom": "[lyja] sk044 Lazerfist — Lyja gagne +1 ATK en forme heros (ATK 1 -> 2)",
        "pourquoi": "« Lyja gets +1 ATK » : `GiveKeywordToAttached(CardFinder(name='Lyja'), attack=1)`",
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.PutIntoPlay('sk044', under_control=True)"],
        "declencher": [],
        "verifier": "etat_attendu",
        "attendu": {"attributs": {"attack": 1}},
    },
    {
        "nom": "[lyja] sk044 Lazerfist — Hero Resource : s'incline pour payer une carte (sk043, cout 1)",
        "pourquoi": ("« Hero Resource: exhaust → generate a [energy] resource » : seule la ressource de Lazerfist (`payer_avec`) "
                     "peut payer sk043, la main ne contient qu'elle"),
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.PutIntoPlay('sk044', under_control=True)"],
        "main_exclusive": ["sk043"],
        "declencher": [],
        "jouer": ["sk043"],
        "payer_avec": ["sk044"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["sk043"], "exhausted": ["sk044"]},
    },
    # ===================================================================== sk045
    {
        "nom": "[lyja] sk045 Ministerial Tiara — une carte de boost a etoile (sk039) : la Tiare s'incline, pioche 1 carte",
        "pourquoi": ("Interruption « when a boost card is turned faceup, if it has a star icon, exhaust → draw 1 ». Rhino attaque, "
                     "carte de boost = sk039 (★ Boost) : main 1 -> 2, Tiare inclinee"),
        **HEROS,
        "mise_en_place": ["Puzzle.PutIntoPlay('sk045', under_control=True)", "Puzzle.EmptyEncounterDeck()",
                          "Puzzle.MoveTo('sk039', 'EncounterDeck')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Attack('01094')"],
        "verifier": "etat_attendu",
        "attendu": {"taille_main": 2, "exhausted": ["sk045"]},
    },
    {
        "nom": "[lyja] sk045 Ministerial Tiara — CONTRE-CAS : carte de boost SANS etoile (01101), rien ne se passe",
        "pourquoi": "Hydra Mercenary (1 icone de boost chiffree, aucune etoile) : la Tiare reste prete, la main ne bouge pas (reste vert sans module)",
        **HEROS,
        "mise_en_place": ["Puzzle.PutIntoPlay('sk045', under_control=True)", "Puzzle.EmptyEncounterDeck()",
                          "Puzzle.CreateEncounterDeck('01101')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Attack('01094')"],
        "verifier": "etat_attendu",
        "attendu": {"taille_main": 1, "pret": ["sk045"]},
    },
    # ===================================================================== sk046
    {
        "nom": "[lyja] sk046 Mole — une traitrise defaussee du DESSUS du deck rencontre : son When Revealed se resout",
        "pourquoi": ("Hero Interrupt « when a TREACHERY card is discarded from the top of the encounter deck, exhaust Mole → resolve "
                     "its When Revealed ». sk042 (Posing as a Civilian : retire 3 menaces) est sur le dessus, menace 6 -> 3, "
                     "Mole inclinee ; la carte part ensuite chez son proprietaire"),
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.PutIntoPlay('sk046', under_control=True)", "Puzzle.SetThreat('01097b', 6)",
                          "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01101')",
                          "Puzzle.MoveTo('sk042', 'EncounterDeck')"],
        "declencher": ["Puzzle.Discard('sk042')"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["01097b", 3]], "exhausted": ["sk046"], "defausse": ["sk042"]},
    },
    {
        "nom": "[lyja] sk046 Mole — CONTRE-CAS : la traitrise n'est PAS au sommet du deck, rien ne se resout",
        "pourquoi": "« FROM THE TOP » : sk042 est la 2e carte du deck rencontre, sa defausse ne declenche pas Mole (menace 6 inchangee)",
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.PutIntoPlay('sk046', under_control=True)", "Puzzle.SetThreat('01097b', 6)",
                          "Puzzle.EmptyEncounterDeck()", "Puzzle.MoveTo('sk042', 'EncounterDeck')",
                          "Puzzle.CreateEncounterDeck('01101')"],
        "declencher": ["Puzzle.Discard('sk042')"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["01097b", 6]], "pret": ["sk046"]},
    },
    # ===================================================================== sk047
    {
        "nom": "[lyja] sk047 Shapeshifter — Lyja gagne +1 THW en forme heros (THW 2 -> 3)",
        "pourquoi": "« Lyja gets +1 THW » : `GiveKeywordToAttached(CardFinder(name='Lyja'), thwart=1)`",
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.PutIntoPlay('sk047', under_control=True)"],
        "declencher": [],
        "verifier": "etat_attendu",
        "attendu": {"attributs": {"thwart": 1}},
    },
    {
        "nom": "[lyja] sk047 Shapeshifter — Hero Response : apres un evenement TREACHERY joue, Lyja se redresse",
        "pourquoi": ("Lyja est inclinee, sk039 (TREACHERY, cout 1) est joue avec 01088 : Shapeshifter s'incline et Lyja se redresse"),
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.PutIntoPlay('sk047', under_control=True)", "Puzzle.Exhaust('sk037a')"],
        "main_exclusive": ["sk039", "01088"],
        "declencher": [],
        "jouer": ["sk039"],
        "verifier": "etat_attendu",
        "attendu": {"pret": ["sk037a"], "exhausted": ["sk047"], "dans_deck_rencontre": ["sk039"]},
    },
    {
        "nom": "[lyja] sk047 Shapeshifter — CONTRE-CAS : un evenement NON TREACHERY (sk052) ne redresse pas Lyja",
        "pourquoi": "sk052 Going Ballistic (ATTACK, cout 0) : Lyja reste inclinee, Shapeshifter prete (reste vert sans module)",
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.PutIntoPlay('sk047', under_control=True)", "Puzzle.Exhaust('sk037a')"],
        "main_exclusive": ["sk052"],
        "cibles": ["01094"],
        "declencher": [],
        "jouer": ["sk052"],
        "verifier": "etat_attendu",
        "attendu": {"exhausted": ["sk037a"], "pret": ["sk047"]},
    },
    # ===================================================================== sk049
    {
        "nom": "[lyja] sk049 The Thing — Toughness : il entre en jeu avec un statut Tenace",
        "pourquoi": "« Toughness » lu dans desc (fiche toughness.md) : aucun script, mais le comportement est a prouver",
        **HEROS,
        "mise_en_place": ["Puzzle.PutIntoPlay('sk049', under_control=True)"],
        "declencher": [],
        "verifier": "etat_attendu",
        "attendu": {"statuts": [["sk049", "Tough"]]},
    },
    {
        "nom": "[lyja] sk049 The Thing — Action : defausse son Tenace, 2 degats a chacun de 2 ennemis",
        "pourquoi": ("cout = defausser le statut Tenace de LUI ; cibles Rhino et Hydra Mercenary (01101) : 2 degats chacun, "
                     "Tenace parti"),
        **HEROS,
        "mise_en_place": ["Puzzle.PutIntoPlay('sk049', under_control=True)", "Puzzle.PutIntoPlay('01101')"],
        "cibles": ["01094", "01101"],
        "declencher": ["Puzzle.Action('sk049', 'Action', 0)"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 2], ["01101", 2]], "statuts_absents": [["sk049", "Tough"]]},
    },
    {
        "nom": "[lyja] sk049 The Thing — TEMOIN : sans statut Tenace (2e Action), l'action n'est plus offerte",
        "pourquoi": "le cout exige le Tenace : 2 Actions de suite, la 2e est refusee, Rhino n'a subi que 2 degats (pas 4)",
        **HEROS,
        "mise_en_place": ["Puzzle.PutIntoPlay('sk049', under_control=True)"],
        "cibles": ["01094"],
        "declencher": ["Puzzle.Action('sk049', 'Action', 0)", "Puzzle.Ready('sk049')"],
        "declencher_tolerant": ["Puzzle.Action('sk049', 'Action', 0)"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 2]]},
    },
    # ===================================================================== sk052
    {
        "nom": "[lyja] sk052 Going Ballistic — defausse la main (1 autre carte) : 2 degats",
        "pourquoi": "« discard your hand, 2 damage for each card discarded » : main sk052 + 01088 -> 1 carte defaussee -> 2 degats sur Rhino",
        **HEROS,
        "mise_en_place": [FORME_HEROS],
        "main_exclusive": ["sk052", "01088"],
        "cibles": ["01094"],
        "declencher": [],
        "jouer": ["sk052"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 2]], "taille_main": 0},
    },
    {
        "nom": "[lyja] sk052 Going Ballistic — plafond : 5 cartes defaussees = 10 -> 6 degats maximum",
        "pourquoi": "« (to a maximum of 6) » : la main entiere part (5 cartes), les degats s'arretent a 6",
        **HEROS,
        "mise_en_place": [FORME_HEROS],
        "main_exclusive": ["sk052", "01088", "01089", "01090", "01090", "01088"],
        "cibles": ["01094"],
        "declencher": [],
        "jouer": ["sk052"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 6]], "taille_main": 0},
    },
    # ===================================================================== sk053
    {
        "nom": "[lyja] sk053 Hit the Weak Spot — Melter (etoile seule, 0 icone chiffree) : 1 icone -> 2 degats",
        "pourquoi": "« 2 damage for each icon (★ and Y) in that minion's boost area » : 01132 Melter a un ★ Boost sans icone Y = 1 icone",
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.PutIntoPlay('01132')"],
        "main_exclusive": ["sk053", "01088"],
        "cibles": ["01132"],
        "declencher": [],
        "jouer": ["sk053"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01132", 2]]},
    },
    {
        "nom": "[lyja] sk053 Hit the Weak Spot — Hired Gun (2 icones Y + ★ = 3) : 6 degats, le sbire (3 PV) est vaincu",
        "pourquoi": "2 x (2 + 1) = 6 degats : 02007 Hired Gun (Boost 2, ★ Boost) tombe",
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.PutIntoPlay('02007')"],
        "main_exclusive": ["sk053", "01088"],
        "cibles": ["02007"],
        "declencher": [],
        "jouer": ["sk053"],
        "verifier": "etat_attendu",
        "attendu": {"hors_jeu": ["02007"]},
    },
    {
        "nom": "[lyja] sk053 Hit the Weak Spot — Sandman (Tenace, 2 icones) : l'attaque est PERCANTE, 4 degats passent",
        "pourquoi": ("« This attack gains piercing » : 01102 Sandman (Toughness, 4 PV, Boost 2) : 2 x 2 = 4 degats, le Tenace "
                     "est defausse au lieu de bloquer -> Sandman est vaincu"),
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.PutIntoPlay('01102')"],
        "main_exclusive": ["sk053", "01088"],
        "cibles": ["01102"],
        "declencher": [],
        "jouer": ["sk053"],
        "verifier": "etat_attendu",
        "attendu": {"hors_jeu": ["01102"]},
    },
    # ===================================================================== sk056
    {
        "nom": "[lyja] sk056 Invisible Woman — apres son attaque, 1 compteur revelation sur la cible (aucun degat consecutif)",
        "pourquoi": "Reponse forcee « place 1 revelation counter on the target » ; 1re attaque : aucun compteur avant, Sue ne subit rien",
        **HEROS,
        "mise_en_place": ["Puzzle.PutIntoPlay('sk056', under_control=True)"],
        "cibles": ["01094"],
        "declencher": ["Puzzle.Attack('sk056')"],
        "verifier": "etat_attendu",
        "attendu": {"compteurs": [["01094", "revelation", 1]], "degats": [["sk056", 0], ["01094", 1]]},
    },
    {
        "nom": "[lyja] sk056 Invisible Woman — 2e attaque sur la meme cible : +1 degat consecutif (1 compteur deja la)",
        "pourquoi": "« takes +1 consequential damage for each revelation counter on the target » : 2e attaque, 1 compteur -> Sue subit 1 ; 2 compteurs ensuite",
        **HEROS,
        "mise_en_place": ["Puzzle.PutIntoPlay('sk056', under_control=True)"],
        "cibles": ["01094"],
        "declencher": ["Puzzle.Attack('sk056')", "Puzzle.Ready('sk056')", "Puzzle.Attack('sk056')"],
        "verifier": "etat_attendu",
        "attendu": {"compteurs": [["01094", "revelation", 2]], "degats": [["sk056", 1], ["01094", 2]]},
    },
    {
        "nom": "[lyja] sk056 Invisible Woman — son contre (THW) pose aussi un compteur revelation, sur la manigance",
        "pourquoi": "« a basic power » : attaque ET contre ; le compteur va sur la manigance contree (menace 6 -> 5)",
        **HEROS,
        "mise_en_place": ["Puzzle.PutIntoPlay('sk056', under_control=True)", "Puzzle.SetThreat('01097b', 6)"],
        "cibles": ["01097b"],
        "declencher": ["Puzzle.Thwart('sk056')"],
        "verifier": "etat_attendu",
        "attendu": {"compteurs": [["01097b", "revelation", 1]], "menace": [["01097b", 5]]},
    },
    # ===================================================================== sk057
    {
        "nom": "[lyja] sk057 Mister Fantastic — Resource : s'incline et prend 1 degat pour payer sk043 (cout 1)",
        "pourquoi": "« Resource: exhaust Mister Fantastic and deal 1 damage to him → generate a [mental] resource » : les DEUX couts payes",
        **HEROS,
        "mise_en_place": ["Puzzle.PutIntoPlay('sk057', under_control=True)"],
        "main_exclusive": ["sk043"],
        "declencher": [],
        "jouer": ["sk043"],
        "payer_avec": ["sk057"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["sk043"], "exhausted": ["sk057"], "degats": [["sk057", 1]]},
    },
    # ===================================================================== sk058
    {
        "nom": "[lyja] sk058 Laser Tag — redresse Human Torch, Lyja et les ameliorations SUPERPOWER (pas la Tiare)",
        "pourquoi": ("Team-Up (Human Torch et Lyja) : tout est incline, sk058 (cout 2) payee par 01088 -> Torch, Lyja, Lazerfist et "
                     "Shapeshifter (SUPERPOWER) prets ; Ministerial Tiara (ITEM) reste inclinee"),
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.EmptyPlayerDeck()", "Puzzle.PutIntoPlay('sk038', under_control=True)",
                          "Puzzle.PutIntoPlay('sk044', under_control=True)", "Puzzle.PutIntoPlay('sk047', under_control=True)",
                          "Puzzle.PutIntoPlay('sk045', under_control=True)",
                          "Puzzle.Exhaust('sk037a')", "Puzzle.Exhaust('sk038')", "Puzzle.Exhaust('sk044')",
                          "Puzzle.Exhaust('sk047')", "Puzzle.Exhaust('sk045')"],
        "main_exclusive": ["sk058", "01088"],
        "declencher": [],
        "jouer": ["sk058"],
        "verifier": "etat_attendu",
        "attendu": {"pret": ["sk037a", "sk038", "sk044", "sk047"], "exhausted": ["sk045"]},
    },
    {
        "nom": "[lyja] sk058 Laser Tag — CONTRE-CAS Team-Up : sans Human Torch en jeu, l'evenement n'est pas jouable",
        "pourquoi": "« Team-Up (Human Torch and Lyja) » : seule Lyja est la, sk058 reste en main (Human Torch absent)",
        **HEROS,
        "mise_en_place": [FORME_HEROS],
        "main_exclusive": ["sk058", "01088"],
        "declencher": [],
        "jouer": ["sk058"],
        "verifier": "etat_attendu",
        "attendu": {"en_main": ["sk058"]},
    },
    # ===================================================================== sk062
    {
        "nom": "[lyja] sk062 Baxter Building — cout 4 reduit a 3 avec un personnage FANTASTIC FOUR (Lyja) : jouable avec 3 ressources",
        "pourquoi": "preuve par insuffisance : main sk062 + 01088 (YY) + sk064 (1) = 3 ressources, impayable au cout imprime 4",
        **HEROS,
        "mise_en_place": [FORME_HEROS],
        "main_exclusive": ["sk062", "01088", "sk064"],
        "declencher": [],
        "jouer": ["sk062"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["sk062"]},
    },
    {
        "nom": "[lyja] sk062 Baxter Building — CONTRE-CAS : en alter ego (aucun FANTASTIC FOUR), 3 ressources ne suffisent pas",
        "pourquoi": "Laura Green (SKRULL. SPY) n'est pas FF : le cout reste 4, la carte n'est pas jouable avec la meme main",
        **HEROS,
        "mise_en_place": [],
        "main_exclusive": ["sk062", "01088", "sk064"],
        "declencher": [],
        "jouer": ["sk062"],
        "verifier": "etat_attendu",
        "attendu": {"hors_jeu": ["sk062"], "en_main": ["sk062"]},
    },
    {
        "nom": "[lyja] sk062 Baxter Building — Resource : s'incline pour payer sk043 (cout 1), generique pour tout joueur",
        "pourquoi": "« Resource: exhaust → generate a [wild] resource for any player » : seule ressource disponible",
        **HEROS,
        "mise_en_place": ["Puzzle.PutIntoPlay('sk062', under_control=True)"],
        "main_exclusive": ["sk043"],
        "declencher": [],
        "jouer": ["sk043"],
        "payer_avec": ["sk062"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["sk043"], "exhausted": ["sk062"]},
    },
    # ===================================================================== sk063
    {
        "nom": "[lyja] sk063 Fantasti-Car — Response a l'entree en jeu : redresse une carte FANTASTIC FOUR (Lyja inclinee)",
        "pourquoi": "« After Fantasti-Car enters play, ready a FANTASTIC FOUR card » : Lyja (FF) est inclinee, sk063 (cout 2) payee par 01088",
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.Exhaust('sk037a')"],
        "main_exclusive": ["sk063", "01088"],
        "cibles": ["sk037a"],
        "declencher": [],
        "jouer": ["sk063"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["sk063"], "pret": ["sk037a"]},
    },
    {
        "nom": "[lyja] sk063 Fantasti-Car — Alter-Ego Action : le joueur remet 1 carte de sa defausse dans son deck",
        "pourquoi": "« Exhaust Fantasti-Car → choose a player. That player may shuffle 1 card from their discard pile into their deck » : 01089 en defausse",
        **HEROS,
        "mise_en_place": ["Puzzle.PutIntoPlay('sk063', under_control=True)", "Puzzle.CreatePlayerDiscardPile('01089')"],
        "declencher": ["Puzzle.Action('sk063', 'AlterEgoAction', 0)"],
        "verifier": "etat_attendu",
        "attendu": {"dans_deck_joueur": ["01089"], "exhausted": ["sk063"]},
    },
    # ===================================================================== sk064
    {
        "nom": "[lyja] sk064 Fantastic Four Member — sur un allie : +1 PV et le trait FANTASTIC FOUR",
        "pourquoi": ("Black Belt (62037) est le meme texte. Lyja (identite FF) en forme heros ; l'amelioration vise Mockingbird "
                     "(01083, 3 PV, non FF) : 4 PV et trait FF"),
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.PutIntoPlay('01083', under_control=True)"],
        "main_exclusive": ["sk064"],
        "cibles": ["01083"],
        "declencher": [],
        "jouer": ["sk064"],
        "verifier": "etat_attendu",
        "attendu": {"pv_max": [["01083", 4]], "traits_de": [["01083", "FANTASTIC FOUR"]]},
    },
    {
        "nom": "[lyja] sk064 Fantastic Four Member — CONTRE-CAS : en alter ego (Laura Green n'est pas FF), non jouable",
        "pourquoi": "« Play only if your identity has the FANTASTIC FOUR trait » : Laura Green est SKRULL. SPY.",
        **HEROS,
        "mise_en_place": ["Puzzle.PutIntoPlay('01083', under_control=True)"],
        "main_exclusive": ["sk064"],
        "declencher": [],
        "jouer": ["sk064"],
        "verifier": "etat_attendu",
        "attendu": {"hors_jeu": ["sk064"], "en_main": ["sk064"]},
    },
    {
        "nom": "[lyja] sk064 Fantastic Four Member — TEMOIN D'EPUISEMENT « Max 1 per character » : le 2e exemplaire ne se pose pas sur le meme allie",
        "pourquoi": ("deux exemplaires en main (deck [sk064, sk064] + Gain x2), les deux visent Mockingbird : le 1er s'y pose (4 PV), "
                     "le 2e est refuse sur elle (MaxPerUnit 1) et va ailleurs ou reste en main : PV max de Mockingbird = 4, jamais 5"),
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.EmptyHand()", "Puzzle.EmptyPlayerDeck()",
                          "Puzzle.CreatePlayerDeck('sk064', 'sk064')", "Puzzle.PutIntoPlay('01083', under_control=True)",
                          "Puzzle.Gain('sk064')", "Puzzle.Gain('sk064')"],
        "cibles": ["01083"],
        "declencher": [],
        "jouer": ["sk064", "sk064"],
        "verifier": "etat_attendu",
        "attendu": {"pv_max": [["01083", 4]]},
    },
    # ===================================================================== sk065
    {
        "nom": "[lyja] sk065 Untrustworthiness — le When Revealed d'une traitrise TREACHERY (sk042) est annule, et on recoit 1 carte face cachee",
        "pourquoi": ("Forced Interrupt « cancel that ability. Then deal yourself 1 facedown encounter card » : l'obligation est en jeu, sk042 "
                     "(retire 3 menaces) est revelee : menace 6 inchangee, 1 carte rencontre distribuee"),
        **HEROS,
        "mise_en_place": ["Puzzle.Reveal('sk065')", "Puzzle.SetThreat('01097b', 6)"],
        "declencher": ["Puzzle.Reveal('sk042')"],
        "verifier": "lyja_untrust",
        "attendu": {"menace": 6, "cartes_distribuees": 1},
    },
    {
        "nom": "[lyja] sk065 Untrustworthiness — TEMOIN : sans l'obligation, sk042 retire bien ses 3 menaces",
        "pourquoi": "ligne de base : meme revelation sans sk065 en jeu -> menace 3, aucune carte distribuee",
        **HEROS,
        "mise_en_place": ["Puzzle.SetThreat('01097b', 6)"],
        "declencher": ["Puzzle.Reveal('sk042')"],
        "verifier": "lyja_untrust",
        "attendu": {"menace": 3, "cartes_distribuees": 0},
    },
    {
        "nom": "[lyja] sk065 Untrustworthiness — le When Revealed d'une traitrise de TYPE Treachery (sk068) est annule aussi",
        "pourquoi": ("sk068 chercherait 01112 dans le deck et la defausserait ; annule : 01112 reste dans le deck rencontre, "
                     "1 carte distribuee (et sk068 ne gagne pas surge)"),
        **HEROS,
        "mise_en_place": ["Puzzle.Reveal('sk065')", "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01112', '01101')"],
        "declencher": ["Puzzle.Reveal('sk068')"],
        "verifier": "lyja_untrust",
        "attendu": {"cartes_distribuees": 1, "dans_deck_rencontre": ["01112"]},
    },
    {
        "nom": "[lyja] sk065 Untrustworthiness — le ★ Boost d'une traitrise TREACHERY (sk041) est annule, et on recoit 1 carte face cachee",
        "pourquoi": "boost sk041 (3 degats a un ennemi) annule : Rhino indemne ; 1 carte distribuee",
        **HEROS,
        "mise_en_place": ["Puzzle.Reveal('sk065')", "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01101')",
                          "Puzzle.MoveTo('sk041', 'EncounterDeck')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Attack('01094')"],
        "verifier": "lyja_untrust",
        "attendu": {"cartes_distribuees": 1, "degats_rhino": 0},
    },
    {
        "nom": "[lyja] sk065 Untrustworthiness — CONTRE-CAS : une carte non TREACHERY (sbire 01101) revelee, rien n'est annule",
        "pourquoi": "Hydra Mercenary n'est pas une traitrise : aucune carte distribuee (reste vert sans module)",
        **HEROS,
        "mise_en_place": ["Puzzle.Reveal('sk065')"],
        "declencher": ["Puzzle.Reveal('01101')"],
        "verifier": "lyja_untrust",
        "attendu": {"cartes_distribuees": 0},
    },
    {
        "nom": "[lyja] sk065 Untrustworthiness — Alter-Ego Action : Laura Green s'incline, l'obligation est defaussee",
        "pourquoi": "« Exhaust Laura Green → discard Untrustworthiness »",
        **HEROS,
        "mise_en_place": ["Puzzle.Reveal('sk065')"],
        "declencher": ["Puzzle.Action('sk065', 'AlterEgoAction', 0)"],
        "verifier": "etat_attendu",
        "attendu": {"hors_jeu": ["sk065"], "exhausted": ["sk037b"]},
    },
    # ===================================================================== sk066
    {
        "nom": "[lyja] sk066 Paibok — Toughness : il entre en jeu avec un statut Tenace",
        "pourquoi": "Toughness lu dans desc",
        **HEROS,
        "mise_en_place": ["Puzzle.PutIntoPlay('sk066')"],
        "declencher": [],
        "verifier": "etat_attendu",
        "attendu": {"statuts": [["sk066", "Tough"]]},
    },
    {
        "nom": "[lyja] sk066 Paibok — une traitrise defaussee est attachee face cachee a Paibok : +1 SCH et +1 ATK",
        "pourquoi": ("Forced Interrupt « when a TREACHERY card would be discarded, attach it facedown to Paibok instead » + « ★ +1 SCH "
                     "and +1 ATK for each TREACHERY card attached » : 01112 (traitrise du deck rencontre) defaussee"),
        **HEROS,
        "mise_en_place": ["Puzzle.PutIntoPlay('sk066')", "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01112')"],
        "declencher": ["Puzzle.Discard('01112')"],
        "verifier": "etat_attendu",
        "attendu": {"pose_sous": [["sk066", "01112"]], "attributs_carte": [["sk066", "attack", 1], ["sk066", "scheme", 1]]},
    },
    {
        "nom": "[lyja] sk066 Paibok — deux traitrises attachees : +2 SCH et +2 ATK ; un evenement TREACHERY joueur compte aussi",
        "pourquoi": "01112 + sk039 (evenement TREACHERY de Lyja, defausse depuis la main) : +2/+2",
        **HEROS,
        "mise_en_place": ["Puzzle.PutIntoPlay('sk066')", "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01112')",
                          "Puzzle.CreateHandCards('sk039')"],
        "declencher": ["Puzzle.Discard('01112')", "Puzzle.Discard('sk039')"],
        "verifier": "etat_attendu",
        "attendu": {"taille_pose_sous": [["sk066", 2]], "attributs_carte": [["sk066", "attack", 2], ["sk066", "scheme", 2]]},
    },
    {
        "nom": "[lyja] sk066 Paibok — CONTRE-CAS : un sbire (non traitrise) defausse n'est pas attache (+0/+0)",
        "pourquoi": "01101 Hydra Mercenary defausse : il va en defausse rencontre, Paibok garde ses stats imprimees",
        **HEROS,
        "mise_en_place": ["Puzzle.PutIntoPlay('sk066')", "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01103', '01101')"],
        "declencher": ["Puzzle.Discard('01101')"],
        "verifier": "etat_attendu",
        "attendu": {"defausse_rencontre": ["01101"], "attributs_carte": [["sk066", "attack", 0], ["sk066", "scheme", 0]]},
    },
    # ===================================================================== sk067
    {
        "nom": "[lyja] sk067 Punish the Defector — When Revealed : une traitrise du deck rencontre est defaussee",
        "pourquoi": "« search the encounter deck for a TREACHERY card and discard it » : 01112 cherchee et defaussee, le sbire 01101 reste",
        **HEROS,
        "mise_en_place": ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01101', '01112')"],
        "declencher": ["Puzzle.Reveal('sk067')"],
        "verifier": "etat_attendu",
        "attendu": {"defausse_rencontre": ["01112"], "dans_deck_rencontre": ["01101"], "en_jeu": ["sk067"]},
    },
    {
        "nom": "[lyja] sk067 Punish the Defector — TEMOIN : aucune traitrise dans le deck, rien n'est defausse",
        "pourquoi": "le deck ne contient que 01101 : il reste ; la manigance entre quand meme en jeu",
        **HEROS,
        "mise_en_place": ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01101')"],
        "declencher": ["Puzzle.Reveal('sk067')"],
        "verifier": "etat_attendu",
        "attendu": {"dans_deck_rencontre": ["01101"], "en_jeu": ["sk067"]},
    },
    # ===================================================================== sk068
    {
        "nom": "[lyja] sk068 \"It's a Stinkin' Skrull!\" — defausse une traitrise du deck : pas de surge",
        "pourquoi": "01112 trouvee et defaussee ; le sbire 01101 reste dans le deck (aucune carte supplementaire revelee)",
        **HEROS,
        "mise_en_place": ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01101', '01112')"],
        "declencher": ["Puzzle.Reveal('sk068')"],
        "verifier": "etat_attendu",
        "attendu": {"defausse_rencontre": ["01112", "sk068"], "dans_deck_rencontre": ["01101"]},
    },
    {
        "nom": "[lyja] sk068 \"It's a Stinkin' Skrull!\" — aucune traitrise a defausser : la carte gagne surge",
        "pourquoi": "« if no TREACHERY card was discarded this way, this card gains surge » : la carte suivante (01101) est revelee et entre en jeu",
        **HEROS,
        "mise_en_place": ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01101')"],
        "declencher": ["Puzzle.Reveal('sk068')"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["01101"]},
    },
    # ===================================================================== sk069
    {
        "nom": "[lyja] sk069 Truth Revealed — les cartes propres a l'identite vont sous le deck",
        "pourquoi": ("« search your deck for all identity-specific cards, shuffle, place on the bottom in any order » : deck "
                     "[01090 dessus, sk039, 01088, sk038, 01089] -> sk038 et sk039 (signatures, Class Hero) sont les 2 dernieres"),
        **HEROS,
        "mise_en_place": ["Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01089', 'sk038', '01088', 'sk039', '01090')"],
        "declencher": ["Puzzle.Reveal('sk069')"],
        "verifier": "lyja_dessus_deck_joueur",
        "attendu": {"dessous_parmi": ["sk038", "sk039"], "taille": 5},
    },
    {
        "nom": "[lyja] sk069 Truth Revealed — TEMOIN : sans carte propre a l'identite dans le deck, il est juste melange",
        "pourquoi": "deck [01090, 01088, 01089] : rien a deplacer, 3 cartes",
        **HEROS,
        "mise_en_place": ["Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01089', '01088', '01090')"],
        "declencher": ["Puzzle.Reveal('sk069')"],
        "verifier": "lyja_dessus_deck_joueur",
        "attendu": {"taille": 3},
    },
]

VERIFICATIONS = r'''
def lyja_jouable(monde, aides):
    """`attendu` = {"carte": id, "jouable": bool} : la carte EN MAIN est-elle jouable (`CanPlayBy`) ?"""
    attendu = aides["cas"]["attendu"]
    joueur = monde.players[0]
    main = [f for f in joueur.hand_cards.GetAll() if getattr(f.paper, "card_id", None) == attendu["carte"]]
    if not main:
        return False, f"{attendu['carte']} absente de la main"
    jouable = bool(main[0].CanPlayBy(joueur))
    if jouable != attendu["jouable"]:
        return False, f"{attendu['carte']} jouable={jouable} (attendu {attendu['jouable']})"
    return True, f"{attendu['carte']} jouable={jouable}"


def lyja_untrust(monde, aides):
    """sk065 : `attendu` = {"menace": n (sur 01097b), "cartes_distribuees": n (cartes rencontre
    face cachee chez le joueur), "dans_deck_rencontre": [ids], "degats_rhino": n}."""
    from game.operate.worlds import Worlds
    attendu = aides["cas"].get("attendu") or {}
    soucis = []
    if "menace" in attendu:
        scheme = aides["par_id"](monde, "01097b")
        if scheme is None or scheme.threat != attendu["menace"]:
            soucis.append(f"menace = {None if scheme is None else scheme.threat} (attendu {attendu['menace']})")
    if "cartes_distribuees" in attendu:
        n = len(list(monde.players[0].dealt_encounter_cards.Get(True)))
        if n != attendu["cartes_distribuees"]:
            soucis.append(f"cartes rencontre distribuees = {n} (attendu {attendu['cartes_distribuees']})")
    if "dans_deck_rencontre" in attendu:
        ids = {getattr(f.paper, "card_id", None) for f in Worlds.GetEncounterDeckCards(monde)}
        for cid in attendu["dans_deck_rencontre"]:
            if cid not in ids:
                soucis.append(f"{cid} absent du deck rencontre ({sorted(ids)})")
    if "degats_rhino" in attendu:
        rhino = aides["par_id"](monde, "01094")
        subis = rhino.max_health - rhino.health
        if subis != attendu["degats_rhino"]:
            soucis.append(f"degats sur Rhino = {subis} (attendu {attendu['degats_rhino']})")
    if soucis:
        return False, " ; ".join(soucis)
    return True, "etat conforme"
'''
VERIFICATIONS_SUITE = r'''
def _lyja_est_traitrise(face):
    return type(face).__name__ == "Treachery" or face.HasTrait("TREACHERY")


def lyja_dessus_rencontre(monde, aides):
    """Le dessus du deck rencontre. `attendu` = {
        "dessus": [ids exacts, du dessus vers le bas],
        "dessus_parmi": [[ids permis pour la 1re carte], [ids permis pour la 2e], ...],
        "taille": N (facultatif), "face_cachee": True (facultatif : toutes face cachee),
        "traitrises_dessus": N (facultatif : nombre de TRAITRISES consecutives tout en haut)}."""
    from game.operate.worlds import Worlds
    attendu = aides["cas"].get("attendu") or {}
    cartes = list(Worlds.GetEncounterDeckCards(monde))
    ids = [getattr(f.paper, "card_id", None) for f in cartes]
    if "taille" in attendu and len(ids) != attendu["taille"]:
        return False, f"deck rencontre = {len(ids)} cartes (attendu {attendu['taille']}) : {ids}"
    for i, voulu in enumerate(attendu.get("dessus") or []):
        if i >= len(ids) or ids[i] != voulu:
            return False, f"carte n°{i + 1} du dessus = {ids[i] if i < len(ids) else None} (attendu {voulu}) : {ids[:6]}"
    for i, permis in enumerate(attendu.get("dessus_parmi") or []):
        if i >= len(ids) or ids[i] not in permis:
            return False, f"carte n°{i + 1} du dessus = {ids[i] if i < len(ids) else None} (permis {permis}) : {ids[:6]}"
    if "traitrises_dessus" in attendu:
        n = 0
        for f in cartes:
            if _lyja_est_traitrise(f):
                n += 1
            else:
                break
        if n != attendu["traitrises_dessus"]:
            return False, f"{n} traitrise(s) tout en haut (attendu {attendu['traitrises_dessus']}) : {ids[:6]}"
    if attendu.get("face_cachee"):
        visibles = [getattr(f.paper, "card_id", None) for f in cartes if f.IsFaceUp()]
        if visibles:
            return False, f"cartes du deck rencontre face visible : {visibles}"
    return True, f"dessus du deck rencontre = {ids[:6]}"


def lyja_dessus_deck_joueur(monde, aides):
    """Le dessus du deck du joueur 1. `attendu` = {"dessus": [ids], "taille": N,
    "dessus_non_traitrise": True (la 1re carte n'est NI de type Treachery NI TREACHERY)}."""
    attendu = aides["cas"].get("attendu") or {}
    cartes = list(monde.players[0].player_deck.Get(True))
    ids = [getattr(f.paper, "card_id", None) for f in cartes]
    if "taille" in attendu and len(ids) != attendu["taille"]:
        return False, f"deck joueur = {len(ids)} cartes (attendu {attendu['taille']}) : {ids}"
    for i, voulu in enumerate(attendu.get("dessus") or []):
        if i >= len(ids) or ids[i] != voulu:
            return False, f"carte n°{i + 1} du dessus = {ids[i] if i < len(ids) else None} (attendu {voulu}) : {ids[:6]}"
    if attendu.get("dessus_non_traitrise"):
        if cartes and _lyja_est_traitrise(cartes[0]):
            return False, f"le dessus du deck est une traitrise ({ids[0]}) : {ids[:6]}"
    if attendu.get("dessous_parmi"):
        voulues = sorted(attendu["dessous_parmi"])
        n = len(voulues)
        if sorted(ids[-n:]) != voulues:
            return False, f"les {n} dernieres cartes du deck = {sorted(ids[-n:])} (attendu {voulues}) : {ids}"
    return True, f"dessus du deck joueur = {ids[:6]}"
'''
VERIFICATIONS = VERIFICATIONS + VERIFICATIONS_SUITE
