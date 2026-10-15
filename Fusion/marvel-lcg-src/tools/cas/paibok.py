# Cas test_capacites du bloc PAIBOK (sk141-160) et du set modulaire NEW REVENGERS (sk161-169).
# Format identique a tools/test_capacites.py ; noms prefixes `[paibok]` (filtre : `[paibok]`).
#
# Conventions de ce fichier :
#  - le heros de test (Spider-Man, 01001) demarre en ALTER EGO ; `Puzzle.ChangeForm('01001b')` le met
#    en forme HEROS.
#  - `SANS_POUVOIR` vide les quatre attachements POWER SKRULL : celui que 1B revele a la mise en place
#    (au hasard) et ceux restes dans le deck ; chaque mesure part d'un plateau connu (Paibok I, 1 jeton).
#  - `payer_avec` + `payer_tout` imposent QUELLES cartes de la main financent un cout colore :
#    01088 Energy = YY, 01089 Genius = BB, 01090 Strength = RR.
SC = "sk_paibok"
SCE = "sk_paibok_expert"
SANS_POUVOIR = "Puzzle.Remove('sk148', 'sk150', 'sk151', 'sk152')"
HEROS = "Puzzle.ChangeForm('01001b')"


def _c(nom, pourquoi, mise, declencher, attendu, **cle):
    cas = {"nom": "[paibok] " + nom, "pourquoi": pourquoi, "scenario": cle.pop("scenario", SC),
           "heros": cle.pop("heros", "spider_man"), "mise_en_place": mise, "declencher": declencher,
           "verifier": cle.pop("verifier", "paibok_etat"), "attendu": attendu}
    cas.update(cle)
    return cas


CAS = [
    # ===================================================================== mise en place
    _c("sk144a Setup (puis 1B sk144b) : Paibok I en jeu, 1 jeton de maitrise, complot 1B, UN attachement POWER SKRULL",
       "1A pose le jeton ('mastery') sur Paibok ; 1B revele un POWER SKRULL qui s'attache a Paibok",
       [], [], {"en_jeu": ["sk141", "sk144b"], "maitrise": 1, "nb_pouvoirs": 1, "mechant_id": "sk141"}),
    _c("sk144b Revelation a la mise en place : la defausse rencontre est REMELANGEE dans le deck (defausse vide)",
       "« Shuffle the encounter discard pile into the encounter deck » : les cartes defaussees par la recherche reviennent dans le deck ; "
       "mesure faite a la mise en place (le nombre de cartes defaussees avant le POWER SKRULL depend de l'ordre du deck)",
       [], [], {"nb_pouvoirs": 1, "defausse_rencontre_taille": 0}),
    _c("sk142 Setup EXPERT : Paibok II, 1 jeton, DEUX POWER SKRULL (1B + « When Revealed » de Paibok II)",
       "mode expert : villain sk142, sk143 ; le When Revealed du stade II revele un second pouvoir",
       [], [], {"mechant_id": "sk142", "maitrise": 1, "nb_pouvoirs": 2}, scenario=SCE),
    # ===================================================================== sk141-143 : la regle des pouvoirs
    _c("sk141 pouvoirs VERROUILLES : 1 POWER SKRULL, 1 jeton -> impossible de le defausser",
       "« While attachements <= jetons de maitrise, POWER SKRULL cards cannot be discarded » : `WhenCardWouldDiscard` + SetBeInstead",
       [SANS_POUVOIR, "Puzzle.PutIntoPlay('sk148')"], ["Puzzle.Discard('sk148')"],
       {"pouvoirs": ["sk148"], "accroche_a": [["sk148", "sk141"]]}),
    _c("sk141 pouvoirs verrouilles, TEMOIN : 2 POWER SKRULL pour 1 jeton -> on peut en defausser un",
       "attachements (2) > jetons (1) : la regle ne s'applique plus ; la defausse part",
       [SANS_POUVOIR, "Puzzle.PutIntoPlay('sk148')", "Puzzle.PutIntoPlay('sk151')"], ["Puzzle.Discard('sk148')"],
       {"pouvoirs": ["sk151"], "hors_jeu": ["sk148"]}),
    _c("sk141 pouvoirs verrouilles, TEMOIN : 0 jeton -> le POWER SKRULL se defausse",
       "attachements (1) > jetons (0) : defausse permise (ligne de base sans le verrou)",
       [SANS_POUVOIR, "Puzzle.PutIntoPlay('sk148')", "Puzzle.Counter('sk141', 'mastery', -1)"], ["Puzzle.Discard('sk148')"],
       {"nb_pouvoirs": 0, "maitrise": 0, "hors_jeu": ["sk148"]}),
    _c("sk141 la regle ne vise QUE les POWER SKRULL : Captain Paibok (TITLE) se defausse malgre le verrou",
       "« POWER SKRULL cards cannot be discarded » : un autre attachement du set reste defaussable",
       [SANS_POUVOIR, "Puzzle.PutIntoPlay('sk148')", "Puzzle.PutIntoPlay('sk146')"], ["Puzzle.Discard('sk146')"],
       {"pouvoirs": ["sk148"], "hors_jeu": ["sk146"]}),
    # ===================================================================== sk144b / sk145a / sk145b
    _c("sk145b Forced Interrupt : le complot « serait accompli » -> jeton +1, menace remise a 0, un POWER SKRULL revele du deck",
       "(jetons : 1 de depart + 1 de 2A + 1 de 2B = 3) `WhenMainSchemeStageWouldBeCompleted` + SetBeInstead : 5 menaces (cible 5[per_hero], 1 joueur) = accompli ; il reste en jeu, a 0",
       [SANS_POUVOIR, "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01101', 'sk148')", "Puzzle.AdvanceMainScheme(1)"],
       ["Puzzle.SetThreat('sk145b', 5)"],
       {"en_jeu": ["sk145b"], "menace": [["sk145b", 0]], "maitrise": 3, "pouvoirs": ["sk148"]}),
    _c("sk145b « discard until POWER SKRULL », bord du deck : le POWER SKRULL est la DERNIERE carte du deck",
       "`Deck.DiscardUntil` rend None quand il vide le deck, meme si la derniere carte est celle qu'on cherche ; le helper `RevelerPouvoirDuDeck` doit quand meme la reveler",
       [SANS_POUVOIR, "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('sk148', '01101')", "Puzzle.AdvanceMainScheme(1)"],
       ["Puzzle.SetThreat('sk145b', 5)"],
       {"en_jeu": ["sk145b"], "menace": [["sk145b", 0]], "maitrise": 3, "pouvoirs": ["sk148"]}),
    _c("sk145a Revelation : jeton de maitrise +1 ET Captain Paibok (du deck) s'attache a Paibok",
       "« Place 1 mastery counter... Otherwise search the encounter deck and discard pile for Captain Paibok and attach it to Paibok »",
       [SANS_POUVOIR, "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('sk146', '01101')"],
       ["Puzzle.AdvanceMainScheme(1)"],
       {"maitrise": 2, "accroche_a": [["sk146", "sk141"]], "en_jeu": ["sk145b"]}),
    _c("sk145a Revelation, branche « Captain Paibok est en jeu » : son Boost soigne 2 degats de Paibok",
       "« if Captain Paibok is in play, resolve its Boost ability » = Heal 2 damage from Paibok (3 degats poses -> 1)",
       [SANS_POUVOIR, "Puzzle.PutIntoPlay('sk146')", "Puzzle.Tough('sk141')", "Puzzle.Damage('sk141', 3)"],
       ["Puzzle.AdvanceMainScheme(1)"],
       {"maitrise": 2, "degats": [["sk141", 1]], "accroche_a": [["sk146", "sk141"]]}),
    # ===================================================================== sk145b : la defaite
    _c("sk145b « when the player phase ends, if all 4 POWER SKRULL are attached to Paibok, the players lose »",
       "2B en jeu + les quatre attachements sur Paibok + fin de la phase des joueurs = defaite",
       [SANS_POUVOIR, "Puzzle.AdvanceMainScheme(1)", "Puzzle.PutIntoPlay('sk148')", "Puzzle.PutIntoPlay('sk150')",
        "Puzzle.PutIntoPlay('sk151')", "Puzzle.PutIntoPlay('sk152')"],
       ["Puzzle.EndPlayerPhase()"], {"defaite": True, "nb_pouvoirs": 4}),
    _c("sk145b defaite, TEMOIN : seulement 3 POWER SKRULL -> pas de defaite",
       "« if ALL 4 » : trois attachements ne suffisent pas",
       [SANS_POUVOIR, "Puzzle.AdvanceMainScheme(1)", "Puzzle.PutIntoPlay('sk148')", "Puzzle.PutIntoPlay('sk150')",
        "Puzzle.PutIntoPlay('sk151')"],
       ["Puzzle.EndPlayerPhase()"], {"defaite": False, "nb_pouvoirs": 3}),
    _c("sk145b defaite, TEMOIN : quatre POWER SKRULL mais le complot 1B (pas 2B) est en jeu -> pas de defaite",
       "« if the Mastering Powers main scheme is in play » : la capacite vit sur la face 2B",
       [SANS_POUVOIR, "Puzzle.PutIntoPlay('sk148')", "Puzzle.PutIntoPlay('sk150')",
        "Puzzle.PutIntoPlay('sk151')", "Puzzle.PutIntoPlay('sk152')"],
       ["Puzzle.EndPlayerPhase()"], {"defaite": False, "nb_pouvoirs": 4, "en_jeu": ["sk144b"]}),
    # ===================================================================== sk148 Electricity Projection
    _c("sk148 Electricity Projection : Paibok gagne Riposte 1 et +1 ATQ",
       "`GiveKeywordToAttached(retaliate=1)` ; `ATK+` natif (desc)",
       [SANS_POUVOIR, "Puzzle.PutIntoPlay('sk148')"], [],
       {"pouvoirs": ["sk148"], "attributs_carte": [["sk141", "retaliate", 1], ["sk141", "attack", 1]]}),
    _c("sk148 Electricity Projection : Boost -> un personnage qu'on controle est etourdi",
       "`WhenCardBecomeBoost` : le joueur choisit parmi SES personnages (canbe_stunned) ; Paibok manigance (alter ego)",
       [SANS_POUVOIR], ["Puzzle.Boost('sk148')"], {"statuts": [["01001b", "Stunned"]]}, main_exclusive=["01088"]),
    _c("sk148 Electricity Projection : Action de heros [mental][physical] -> la carte est defaussee (2 POWER SKRULL, 1 jeton)",
       "Cout `BR` paye par Genius (BB) et Strength (RR) ; `PlayerActionToDiscardThis`",
       [SANS_POUVOIR, "Puzzle.PutIntoPlay('sk148')", "Puzzle.PutIntoPlay('sk151')", HEROS],
       ["Puzzle.Action('sk148', 'HeroAction')"], {"hors_jeu": ["sk148"], "pouvoirs": ["sk151"], "taille_main": 0},
       main_exclusive=["01089", "01090"], payer_avec=["01089", "01090"], payer_tout=True),
    _c("sk148 Action de heros NON OFFERTE quand les pouvoirs sont verrouilles (1 POWER SKRULL, 1 jeton)",
       "`ActionDefausserPouvoir` : la defausse est interdite par le texte de Paibok, le cout ne doit pas etre offert",
       [SANS_POUVOIR, "Puzzle.PutIntoPlay('sk148')", HEROS], [], {"action_offerte": [["sk148", 0]]},
       main_exclusive=["01089", "01090"]),
    _c("sk148 Action de heros OFFERTE des qu'il y a plus d'attachements que de jetons (TEMOIN)",
       "meme position avec un second POWER SKRULL : 2 > 1",
       [SANS_POUVOIR, "Puzzle.PutIntoPlay('sk148')", "Puzzle.PutIntoPlay('sk151')", HEROS], [],
       {"action_offerte": [["sk148", 1]]}, main_exclusive=["01089", "01090"]),
    # ===================================================================== sk150 Ice Control
    _c("sk150 Ice Control : Paibok gagne +1 MNG (le badge ATQ a etoile n'a pas de valeur)",
       "`SCH+ 1` natif ; decision utilisateur du 15/10/2026 : etoile seule = « voir le texte »",
       [SANS_POUVOIR, "Puzzle.PutIntoPlay('sk150')"], [],
       {"pouvoirs": ["sk150"], "attributs_carte": [["sk141", "scheme", 1], ["sk141", "attack", 0]]}),
    _c("sk150 Ice Control : Reponse forcee -> apres que Paibok l'attaque, un de ses personnages s'incline",
       "`AfterUnitAttackYou(ForcedResponse, 'AttachedEnemy')` ; attaque laissee sans defense (defendre inclinerait le heros)",
       [SANS_POUVOIR, "Puzzle.PutIntoPlay('sk150')", HEROS], ["Puzzle.Attack('sk141')"],
       {"exhausted": ["01001a"]}, main_exclusive=["01088"], passer_sur_option="Defense"),
    _c("sk150 Ice Control, TEMOIN : sans l'attachement, le heros attaque sans defense reste pret",
       "ligne de base du precedent : rien ne s'incline",
       [SANS_POUVOIR, HEROS], ["Puzzle.Attack('sk141')"], {"pret": ["01001a"]},
       main_exclusive=["01088"], passer_sur_option="Defense"),
    _c("sk150 Ice Control : Boost -> un personnage qu'on controle s'incline",
       "`WhenCardBecomeBoost` + `canbe_exhaust` (modele 32073)",
       [SANS_POUVOIR], ["Puzzle.Boost('sk150')"], {"exhausted": ["01001b"]}, main_exclusive=["01088"]),
    _c("sk150 Ice Control : Action de heros « 3 ressources de n'importe quel type » -> defaussee (2 POWER SKRULL, 1 jeton)",
       "Cout `Cost('3')` paye par Energy (YY) + Strength (RR)",
       [SANS_POUVOIR, "Puzzle.PutIntoPlay('sk150')", "Puzzle.PutIntoPlay('sk148')", HEROS],
       ["Puzzle.Action('sk150', 'HeroAction')"], {"hors_jeu": ["sk150"], "pouvoirs": ["sk148"], "taille_main": 0},
       main_exclusive=["01088", "01090"], payer_avec=["01088", "01090"], payer_tout=True),
    # ===================================================================== sk151 Metallic Skin
    _c("sk151 Metallic Skin : Paibok gagne +1 ATQ",
       "`ATK+ 1` natif (desc)",
       [SANS_POUVOIR, "Puzzle.PutIntoPlay('sk151')"], [],
       {"pouvoirs": ["sk151"], "attributs_carte": [["sk141", "attack", 1]]}),
    _c("sk151 Metallic Skin : Reponse forcee -> apres des degats, Paibok recoit une carte Robuste",
       "`AfterUnitTookDamage(ForcedResponse, 'AttachedEnemy')` ; on retire d'abord le Robuste d'entree de Paibok (Toughness)",
       [SANS_POUVOIR, "Puzzle.PutIntoPlay('sk151')", "Puzzle.Tough('sk141')"], ["Puzzle.Damage('sk141', 1)"],
       {"statuts": [["sk141", "Tough"]], "degats": [["sk141", 1]]}),
    _c("sk151 Metallic Skin, TEMOIN : sans l'attachement, apres des degats Paibok n'est PAS Robuste",
       "ligne de base du precedent",
       [SANS_POUVOIR, "Puzzle.Tough('sk141')"], ["Puzzle.Damage('sk141', 1)"],
       {"statuts_absents": [["sk141", "Tough"]], "degats": [["sk141", 1]]}),
    _c("sk151 Metallic Skin : Boost -> Paibok recoit une carte Robuste",
       "Paibok a perdu son Robuste d'entree ; le Boost le lui redonne",
       [SANS_POUVOIR, "Puzzle.Tough('sk141')"], ["Puzzle.Boost('sk151')"],
       {"statuts": [["sk141", "Tough"]]}, main_exclusive=["01088"]),
    _c("sk151 Metallic Skin : Action de heros [energy][mental] -> defaussee (2 POWER SKRULL, 1 jeton)",
       "Cout `YB` paye par Energy (YY) et Genius (BB)",
       [SANS_POUVOIR, "Puzzle.PutIntoPlay('sk151')", "Puzzle.PutIntoPlay('sk148')", HEROS],
       ["Puzzle.Action('sk151', 'HeroAction')"], {"hors_jeu": ["sk151"], "pouvoirs": ["sk148"], "taille_main": 0},
       main_exclusive=["01088", "01089"], payer_avec=["01088", "01089"], payer_tout=True),
    # ===================================================================== sk152 Shapeshifting
    _c("sk152 Shapeshifting : Paibok gagne Solide, le trait AERIAL et +1 MNG",
       "`GiveKeywordToAttached(stalwart=1, trait='AERIAL')` ; `SCH+ 1` natif",
       [SANS_POUVOIR, "Puzzle.PutIntoPlay('sk152')"], [],
       {"pouvoirs": ["sk152"], "stalwart": True, "traits_mechant": [["AERIAL", True]],
        "attributs_carte": [["sk141", "scheme", 1]]}),
    _c("sk152 Shapeshifting, TEMOIN : sans l'attachement, Paibok n'est ni Solide ni AERIAL",
       "ligne de base du precedent",
       [SANS_POUVOIR], [], {"nb_pouvoirs": 0, "stalwart": False, "traits_mechant": [["AERIAL", False]]}),
    _c("sk152 Shapeshifting : Boost -> un personnage qu'on controle est desoriente",
       "`WhenCardBecomeBoost` + `canbe_confused`",
       [SANS_POUVOIR], ["Puzzle.Boost('sk152')"], {"statuts": [["01001b", "Confused"]]}, main_exclusive=["01088"]),
    _c("sk152 Shapeshifting : Action de heros [energy][physical] -> defaussee (2 POWER SKRULL, 1 jeton)",
       "Cout `YR` paye par Energy (YY) et Strength (RR)",
       [SANS_POUVOIR, "Puzzle.PutIntoPlay('sk152')", "Puzzle.PutIntoPlay('sk148')", HEROS],
       ["Puzzle.Action('sk152', 'HeroAction')"], {"hors_jeu": ["sk152"], "pouvoirs": ["sk148"], "taille_main": 0},
       main_exclusive=["01088", "01090"], payer_avec=["01088", "01090"], payer_tout=True),
    # ===================================================================== sk146 Captain Paibok
    _c("sk146 Captain Paibok : s'attache a Paibok et porte une icone HAZARD",
       "`AttachToFaceWhenPutIntoPlay(CardFinder(name='Paibok', card_type=Villain))` ; `desc.Hazard 1` (icone lue sur le scan)",
       [SANS_POUVOIR, "Puzzle.PutIntoPlay('sk146')"], [],
       {"accroche_a": [["sk146", "sk141"]], "icones": [["Hazard", 1]]}),
    _c("sk146 Captain Paibok : Boost -> Paibok soigne 2 degats",
       "`WhenCardBecomeBoost('This', ...)` + `HealHealth(2)` ; 3 degats poses (Robuste d'entree retire d'abord) -> 1",
       [SANS_POUVOIR, "Puzzle.Tough('sk141')", "Puzzle.Damage('sk141', 3)"], ["Puzzle.Boost('sk146')"],
       {"degats": [["sk141", 1]]}, main_exclusive=["01088"]),
    _c("sk146 Captain Paibok : Action de heros -> resout le Boost de CHAQUE attachement du set (cout), puis se defausse",
       "Distracted (sur l'identite) : +1 menace sur le complot principal ; Captain Paibok lui-meme : soigne 2 (3 -> 1)",
       [SANS_POUVOIR, "Puzzle.Tough('sk141')", "Puzzle.Damage('sk141', 3)", HEROS, "Puzzle.PutIntoPlay('sk146')",
        "Puzzle.PutIntoPlay('sk147')"],
       ["Puzzle.Action('sk146', 'HeroAction')"],
       {"hors_jeu": ["sk146"], "menace": [["sk144b", 2]], "degats": [["sk141", 1]], "en_jeu": ["sk147"]},
       main_exclusive=["01088"]),
    # ===================================================================== sk147 Distracted
    _c("sk147 Distracted : s'attache a l'identite",
       "`AttachToFaceWhenPutIntoPlay('YourIdentity')`",
       [HEROS, "Puzzle.PutIntoPlay('sk147')"], [], {"accroche_a": [["sk147", "01001a"]]}),
    _c("sk147 Distracted : Interruption forcee -> un contre retire 1 menace de MOINS (4 -> 4 au lieu de 3)",
       "`WhenUnitWouldThwart` + `RemoveAdditionalThreat(-1)` ; THW 1 de Spider-Man - 1 = 0",
       [HEROS, "Puzzle.EmptyHand()", "Puzzle.SetThreat('sk144b', 4)", "Puzzle.PutIntoPlay('sk147')"], ["Puzzle.Thwart('01001a')"],
       {"menace": [["sk144b", 4]]}, main_exclusive=["01088"], cibles=["sk144b"]),
    _c("sk147 Distracted, TEMOIN : sans l'attachement le meme contre retire 1 menace (4 -> 3)",
       "ligne de base du precedent",
       [HEROS, "Puzzle.EmptyHand()", "Puzzle.SetThreat('sk144b', 4)"], ["Puzzle.Thwart('01001a')"],
       {"menace": [["sk144b", 3]]}, main_exclusive=["01088"], cibles=["sk144b"]),
    _c("sk147 Distracted : Boost -> 1 menace sur le complot principal (en plus de la manigance de Paibok)",
       "menace de depart 1 + manigance SCH 1 + Boost 1 = 3 ; temoin = meme carte de boost sans effet",
       [SANS_POUVOIR], ["Puzzle.Boost('sk147')"], {"menace": [["sk144b", 3]]}, main_exclusive=["01088"]),
    _c("sk147 Distracted, TEMOIN : une carte de boost sans effet ne pose que la manigance (1 + 1 = 2)",
       "ligne de base du precedent (01104 Hard to Keep Down, sans icone de boost)",
       [SANS_POUVOIR], ["Puzzle.Boost('01104')"], {"menace": [["sk144b", 2]]}, main_exclusive=["01088"]),
    _c("sk147 Distracted : Action de heros [mental][mental] -> defaussee",
       "Cout `BB` paye par Genius",
       [HEROS, "Puzzle.PutIntoPlay('sk147')"], ["Puzzle.Action('sk147', 'HeroAction')"],
       {"hors_jeu": ["sk147"], "taille_main": 0}, main_exclusive=["01089"], payer_avec=["01089"]),
    # ===================================================================== sk149 Hypnotized
    _c("sk149 Hypnotized : changer de forme coute 1 ressource de plus (Energy depensee, heros en forme heros)",
       "`AdditionalCostToChangeForm('AttachedIdentity', Spend(Cost('1')))` : la main perd sa carte",
       ["Puzzle.PutIntoPlay('sk149')"], ["Puzzle.ChangeForm('01001b')"],
       {"forme": "Hero", "taille_main": 0}, main_exclusive=["01088"], payer_avec=["01088"]),
    _c("sk149 Hypnotized, TEMOIN : sans l'attachement le changement de forme ne coute rien",
       "ligne de base du precedent : la main reste pleine",
       [], ["Puzzle.ChangeForm('01001b')"], {"forme": "Hero", "taille_main": 1}, main_exclusive=["01088"]),
    _c("sk149 Hypnotized : sans ressource a depenser, le changement de forme est REFUSE",
       "main vide et alter ego (T'Challa) sans pouvoir de ressource : le cout supplementaire ne peut pas etre paye, `SetBeInstead` annule le changement",
       ["Puzzle.EmptyHand()", "Puzzle.PutIntoPlay('sk149')"], ["Puzzle.ChangeForm('01040b')"],
       {"forme": "AlterEgo", "taille_main": 0}, heros="black_panther"),
    _c("sk149 Hypnotized : Boost -> defausse 1 carte de la main",
       "le joueur choisit la carte (57062)",
       [], ["Puzzle.Boost('sk149')"], {"taille_main": 1}, main_exclusive=["01088", "01089"]),
    _c("sk149 Hypnotized : Action de heros [energy][energy] -> defaussee",
       "Cout `YY` paye par Energy",
       [HEROS, "Puzzle.PutIntoPlay('sk149')"], ["Puzzle.Action('sk149', 'HeroAction')"],
       {"hors_jeu": ["sk149"], "taille_main": 0}, main_exclusive=["01088"], payer_avec=["01088"]),
    # ===================================================================== sk153 Trapped in Ice
    _c("sk153 Trapped in Ice : Interruption forcee -> l'attaque de Spider-Man inflige 1 degat de moins (2 -> 1)",
       "`WhenUnitWouldAttack` + `GainATKForThisAttack(-1)` ; cible : Hydra Mercenary (PV 3)",
       [HEROS, "Puzzle.PutIntoPlay('01101')", "Puzzle.PutIntoPlay('sk153')"], ["Puzzle.Attack('01001a')"],
       {"degats": [["01101", 1]]}, main_exclusive=["01088"], cibles=["01101"]),
    _c("sk153 Trapped in Ice, TEMOIN : sans l'attachement la meme attaque inflige 2 degats",
       "ligne de base du precedent",
       [HEROS, "Puzzle.PutIntoPlay('01101')"], ["Puzzle.Attack('01001a')"],
       {"degats": [["01101", 2]]}, main_exclusive=["01088"], cibles=["01101"]),
    _c("sk153 Trapped in Ice : Boost -> le joueur subit 1 degat",
       "`identity.TakeDamage(this, 1, effect)` ; Paibok manigance (alter ego) : aucun autre degat",
       [SANS_POUVOIR], ["Puzzle.Boost('sk153')"], {"degats_identite": 1}, main_exclusive=["01088"]),
    _c("sk153 Trapped in Ice : Action de heros [physical][physical] -> defaussee",
       "Cout `RR` paye par Strength",
       [HEROS, "Puzzle.PutIntoPlay('sk153')"], ["Puzzle.Action('sk153', 'HeroAction')"],
       {"hors_jeu": ["sk153"], "taille_main": 0}, main_exclusive=["01090"], payer_avec=["01090"]),
    # ===================================================================== sk154 Devos / sk155 Kalamari
    _c("sk154 Devos : un statut sur un personnage AMI -> Devos s'active contre son joueur (attaque ATQ 4)",
       "`AfterStatusCardPlaceOn(ForcedResponse, 'Character')` + `DoActivate` ; attaque laissee sans defense, deck rencontre sans boost",
       [SANS_POUVOIR, HEROS, "Puzzle.PutIntoPlay('sk154')", "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01104')"],
       ["Puzzle.Stun('01001a')"], {"degats_identite": 4}, main_exclusive=["01088"], passer_sur_option="Defense"),
    _c("sk154 Devos, TEMOIN : un statut sur un ENNEMI (Paibok) ne le declenche pas",
       "« friendly character » : les statuts des ennemis sont hors sujet",
       [SANS_POUVOIR, HEROS, "Puzzle.PutIntoPlay('sk154')", "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01104')"],
       ["Puzzle.Stun('sk141')"], {"degats_identite": 0}, main_exclusive=["01088"]),
    _c("sk154 Devos : le joueur est en alter ego -> Devos MANIGANCE (menace +1 sur le complot principal)",
       "« activates » : attaque en heros, manigance en alter ego (regle native de `DoActivate`)",
       [SANS_POUVOIR, "Puzzle.PutIntoPlay('sk154')", "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01104')"],
       ["Puzzle.Confuse('01001b')"], {"menace": [["sk144b", 2]]}, main_exclusive=["01088"]),
    _c("sk155 General Kalamari : vaincu -> le joueur resout le Boost de chaque attachement du set (Distracted : +1 menace)",
       "`WhenUnitBeDefeated(WhenDefeated)` + `ResoudreLesBoosts` ; PV 4 : 2 degats poses puis l'attaque de Spider-Man",
       [SANS_POUVOIR, HEROS, "Puzzle.PutIntoPlay('sk155')", "Puzzle.Damage('sk155', 2)", "Puzzle.PutIntoPlay('sk147')"],
       ["Puzzle.Attack('01001a')"], {"hors_jeu": ["sk155"], "menace": [["sk144b", 2]]},
       main_exclusive=["01088"], cibles=["sk155"]),
    _c("sk155 General Kalamari, TEMOIN : sans attachement du set, sa defaite ne change pas la menace",
       "ligne de base du precedent",
       [SANS_POUVOIR, HEROS, "Puzzle.PutIntoPlay('sk155')", "Puzzle.Damage('sk155', 2)"],
       ["Puzzle.Attack('01001a')"], {"hors_jeu": ["sk155"], "menace": [["sk144b", 1]]},
       main_exclusive=["01088"], cibles=["sk155"]),
    # ===================================================================== sk156 Galactic Ambassador / sk157 Settling Scores
    _c("sk156 Galactic Ambassador : AUCUN personnage avec un statut -> menace de depart seule (2), icone Acceleration",
       "`desc.Acceleration 1` natif ; StartingThreat 2[per_hero]",
       [SANS_POUVOIR], ["Puzzle.Reveal('sk156')"], {"menace": [["sk156", 2]], "icones": [["Acceleration", 1]]}),
    _c("sk156 Galactic Ambassador : 2 personnages avec un statut (l'un en a deux) -> +2 par personnage = 2 + 4",
       "« for each friendly character WITH A STATUS CARD » : un personnage compte UNE fois (Sonne + Desoriente = 1)",
       [SANS_POUVOIR, "Puzzle.PutIntoPlay('01002', under_control=True)", "Puzzle.Stun('01001b')", "Puzzle.Stun('01002')",
        "Puzzle.Confuse('01002')"],
       ["Puzzle.Reveal('sk156')"], {"menace": [["sk156", 6]]}),
    _c("sk157 Settling Scores : Hinder 2[per_hero] natif -> 2 + 2 = 4 menaces",
       "`desc.Hinder 2*` lu par le moteur (fiche mots-cles/hinder.md)",
       [SANS_POUVOIR], ["Puzzle.Reveal('sk157')"], {"menace": [["sk157", 4]]}),
    _c("sk157 Settling Scores : revelee -> seuls les POWER SKRULL de la DEFAUSSE rencontre retournent dans le deck",
       "`Faces.ShuffleAllTo(POWER SKRULL, 'EncounterDeck')` ; Hydra Mercenary reste en defausse",
       [SANS_POUVOIR, "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01104')",
        "Puzzle.CreateEncounterDiscardPile('sk148', '01101')"],
       ["Puzzle.Reveal('sk157')"], {"dans_deck_rencontre": ["sk148"], "defausse_rencontre": ["01101"],
        "pas_dans_deck_rencontre": ["01101"]}),
    _c("sk157 Settling Scores : chaque Boost est resolu UNE FOIS DE PLUS (Distracted : 1 + 2 = 3 menaces ajoutees)",
       "`AfterCardBecomeBoost` + `ResolveAbility(Boost, ref_message=...)` ; menace de depart 1 + manigance 1 + Boost x2 = 4",
       [SANS_POUVOIR, "Puzzle.PutIntoPlay('sk157')", "Puzzle.SetThreat('sk157', 0)"], ["Puzzle.Boost('sk147')"],
       {"menace": [["sk144b", 4]]}, main_exclusive=["01088"]),
    # ===================================================================== sk158 / sk159 / sk160 traitrises
    _c("sk158 Council Manipulation : Paibok manigance (1 + 1 = 2) ; joueur ni sonne ni desoriente -> PAS de surge",
       "`DoSchemes` ; la carte du dessus du deck rencontre reste dans le deck",
       [SANS_POUVOIR, "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01101', '01104')"],
       ["Puzzle.Reveal('sk158')"], {"menace": [["sk144b", 2]], "dans_deck_rencontre": ["01101"]}),
    _c("sk158 Council Manipulation : joueur SONNE -> la carte gagne surge (le sbire du dessus est revele)",
       "`ThisCardGainSurge` si `IsStunned() or IsConfused()`",
       [SANS_POUVOIR, "Puzzle.Stun('01001b')", "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01101', '01104')"],
       ["Puzzle.Reveal('sk158')"], {"menace": [["sk144b", 2]], "en_jeu": ["01101"]}),
    _c("sk158 Council Manipulation : joueur DESORIENTE -> surge aussi",
       "« stunned OR confused » : l'un ou l'autre",
       [SANS_POUVOIR, "Puzzle.Confuse('01001b')", "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01101', '01104')"],
       ["Puzzle.Reveal('sk158')"], {"en_jeu": ["01101"]}),
    _c("sk159 Getting Ruthless (alter ego) : resout le Boost de chaque attachement du set (Distracted : +1 menace)",
       "`WhenThisRevealed('Alter-Ego', ...)` + `ResoudreLesBoosts`",
       [SANS_POUVOIR, "Puzzle.PutIntoPlay('sk147')"], ["Puzzle.Reveal('sk159')"], {"menace": [["sk144b", 2]]}),
    _c("sk159 Getting Ruthless (heros) : Paibok attaque le joueur (ATQ 2 + 1 carte de boost de 1 icone = 3)",
       "`DoAttackYou` ; deck rencontre : Hydra Mercenary (1 icone) ; attaque laissee sans defense",
       [SANS_POUVOIR, HEROS, "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01101', '01101')"],
       ["Puzzle.Reveal('sk159')"], {"degats_identite": 3}, main_exclusive=["01088"], passer_sur_option="Defense"),
    _c("sk159 Getting Ruthless (heros) : joueur SONNE -> UNE carte de boost de plus (ATQ 2 + 2 icones = 4)",
       "`GiveAdditionalBoostCardForThisActivation(1)` seulement si le joueur est sonne ou desoriente",
       [SANS_POUVOIR, HEROS, "Puzzle.Stun('01001a')", "Puzzle.EmptyEncounterDeck()",
        "Puzzle.CreateEncounterDeck('01101', '01101')"],
       ["Puzzle.Reveal('sk159')"], {"degats_identite": 4}, main_exclusive=["01088"], passer_sur_option="Defense"),
    _c("sk160 Power Demonstration : resout le Boost de chaque attachement du set (Distracted : +1 menace)",
       "`ResoudreLesBoosts` pour le joueur qui revele",
       [SANS_POUVOIR, "Puzzle.PutIntoPlay('sk147')"], ["Puzzle.Reveal('sk160')"], {"menace": [["sk144b", 2]]}),
    _c("sk160 Power Demonstration : plusieurs attachements -> tous resolus (Distracted +1 menace ET Captain Paibok soigne 2)",
       "deux Boost distincts d'un coup (l'ordre est au choix du joueur)",
       [SANS_POUVOIR, "Puzzle.Tough('sk141')", "Puzzle.Damage('sk141', 3)", "Puzzle.PutIntoPlay('sk146')",
        "Puzzle.PutIntoPlay('sk147')"],
       ["Puzzle.Reveal('sk160')"], {"menace": [["sk144b", 2]], "degats": [["sk141", 1]]}),
    # ===================================================================== NEW REVENGERS (set modulaire, sk161-169)
    _c("sk161 O.M.N.I.T.R.O.N.I.C.U.S. : chaque sbire REVENGER gagne villainous",
       "`GiveKeywordToInPlayWhenApplyThis(CardFinder2('REVENGER', Minion), villainous=1)` (modele 30037)",
       [SANS_POUVOIR, "Puzzle.PutIntoPlay('sk161')", "Puzzle.PutIntoPlay('sk162')"], [],
       {"attributs_carte": [["sk162", "villainous", 1]]}),
    _c("sk161 O.M.N.I.T.R.O.N.I.C.U.S., TEMOIN : sans l'environnement, Angar n'est pas villainous",
       "ligne de base du precedent",
       [SANS_POUVOIR, "Puzzle.PutIntoPlay('sk162')"], [], {"attributs_carte": [["sk162", "villainous", 0]]}),
    _c("sk161 O.M.N.I.T.R.O.N.I.C.U.S. : un sbire qui n'est PAS REVENGER n'est pas villainous",
       "Hydra Mercenary (01101) reste sans villainous",
       [SANS_POUVOIR, "Puzzle.PutIntoPlay('sk161')", "Puzzle.PutIntoPlay('01101')"], [],
       {"attributs_carte": [["01101", "villainous", 0]]}),
    _c("sk161 O.M.N.I.T.R.O.N.I.C.U.S. : Action de heros [energy][energy] -> defaussee quand AUCUN ennemi REVENGER n'est en jeu",
       "`PlayerActionToDiscardThis(HeroAction, conditions=[aucun_revenger])` ; cout `YY` paye par Energy",
       [SANS_POUVOIR, HEROS, "Puzzle.PutIntoPlay('sk161')"], ["Puzzle.Action('sk161', 'HeroAction')"],
       {"hors_jeu": ["sk161"], "taille_main": 0}, main_exclusive=["01088"], payer_avec=["01088"]),
    _c("sk161 O.M.N.I.T.R.O.N.I.C.U.S. : Action de heros NON OFFERTE tant qu'un ennemi REVENGER est en jeu",
       "« If there is no REVENGER enemy in play » : Asti (REVENGER) est en jeu",
       [SANS_POUVOIR, HEROS, "Puzzle.PutIntoPlay('sk161')", "Puzzle.PutIntoPlay('sk163')"], [],
       {"action_offerte": [["sk161", 0]]}, main_exclusive=["01088"]),
    _c("sk162 Angar the Screamer : ses attaques gagnent RANGED -> la Riposte du heros (Black Panther) ne le touche pas",
       "`UnitAttackGainKeyword('This', ranged=True)` ; Black Panther a Riposte 1 nativement (01040a) ; attaque laissee sans defense",
       [HEROS.replace("01001b", "01040b"), "Puzzle.PutIntoPlay('sk162')"], ["Puzzle.Attack('sk162')"],
       {"degats": [["sk162", 0]]}, heros="black_panther", main_exclusive=["01088"], passer_sur_option="Defense"),
    _c("sk162 Angar, TEMOIN : un sbire SANS ranged (Hydra Mercenary) subit la Riposte 1 de Black Panther",
       "ligne de base du precedent : la Riposte marche bien",
       [HEROS.replace("01001b", "01040b"), "Puzzle.PutIntoPlay('01101')"], ["Puzzle.Attack('01101')"],
       {"degats": [["01101", 1]]}, heros="black_panther", main_exclusive=["01088"], passer_sur_option="Defense"),
    _c("sk162 Angar : quand il attaque un heros, son attaque est AUSSI resolue contre l'autre heros (2 joueurs)",
       "`WhenUnitAttackYou(ForcedInterrupt) + AlsoResolveThisAttackTo(heros)` (modele 01130 Whirlwind) ; ATQ 2 chacun, sans defense",
       ["Puzzle.ChangeForm('01001b')", "Puzzle.ChangeForm('01010b')", "Puzzle.PutIntoPlay('sk162')"],
       ["Puzzle.Attack('sk162')"], {"degats_identite": 2, "degats": [["01010a", 2]]},
       heros2="captain_marvel", main_exclusive=["01088"], passer_sur_option="Defense"),
    _c("sk163 Asti the All-Seeing : chaque coup pose 1 jeton d'absorption (2 coups = 2 jetons)",
       "`WhenUnitWouldTakeDamage(ForcedInterrupt, 'This')` + compteur maison 'absorption' (card_face.py)",
       [SANS_POUVOIR, "Puzzle.PutIntoPlay('sk163')", "Puzzle.Damage('sk163', 1)"], ["Puzzle.Damage('sk163', 1)"],
       {"compteurs": [["sk163", "absorption", 2]], "degats": [["sk163", 2]]}),
    _c("sk163 Asti : vaincu avec 1 jeton -> 2 degats INDIRECTS repartis entre les joueurs (1 joueur : 2)",
       "`WhenUnitBeDefeated(WhenDefeated)` + `first_player.AssignDamage(unites, this, 2 x jetons)` ; un seul coup mortel (PV 4) = 1 jeton",
       [HEROS, "Puzzle.PutIntoPlay('sk163')"], ["Puzzle.Damage('sk163', 4)"],
       {"hors_jeu": ["sk163"], "degats_identite": 2}, cibles=["01001a", "01001a"], main_exclusive=["01088"]),
    _c("sk163 Asti : vaincu avec 3 jetons -> 6 degats indirects (2 par jeton)",
       "trois coups (1, 1, 2) : le coup mortel pose aussi son jeton (Interruption forcee AVANT les degats)",
       [HEROS, "Puzzle.PutIntoPlay('sk163')", "Puzzle.Damage('sk163', 1)", "Puzzle.Damage('sk163', 1)"],
       ["Puzzle.Damage('sk163', 2)"],
       {"hors_jeu": ["sk163"], "degats_identite": 6}, cibles=["01001a"] * 6, main_exclusive=["01088"]),
    _c("sk164 Skar : ses attaques gagnent OVERKILL -> l'exces sur l'allie vaincu passe au heros (3 - 1 PV = 2)",
       "`UnitAttackGainKeyword('This', overkill=True)` (modele nv001) ; Daredevil (3 PV) deja a 1 PV",
       ["Puzzle.ChangeForm('01001b')", "Puzzle.Exhaust('01001a')", "Puzzle.PutIntoPlay('sk164')",
        "Puzzle.PutIntoPlay('01058', under_control=True)", "Puzzle.Damage('01058', 2)"],
       ["Puzzle.Attack('sk164', '01058')"], {"hors_jeu": ["01058"], "degats_identite": 2}, main_exclusive=["01088"]),
    _c("sk164 Skar, TEMOIN : Shocker (ATQ 2, sans overkill) vainc l'allie sans rien deverser sur le heros",
       "ligne de base du precedent",
       ["Puzzle.ChangeForm('01001b')", "Puzzle.Exhaust('01001a')", "Puzzle.PutIntoPlay('01103')",
        "Puzzle.PutIntoPlay('01058', under_control=True)", "Puzzle.Damage('01058', 2)"],
       ["Puzzle.Attack('01103', '01058')"], {"hors_jeu": ["01058"], "degats_identite": 0}, main_exclusive=["01088"]),
    _c("sk164 Skar : revele (heros) -> un personnage qu'on controle s'incline",
       "`WhenThisRevealed` + `ForChoiceAbility(...).SetTarget('YouControlUnit', canbe_exhaust=True)` (modele 04136)",
       [HEROS], ["Puzzle.Reveal('sk164')"], {"exhausted": ["01001a"]}, main_exclusive=["01088"]),
    _c("sk165 The Maker : ne subit AUCUN degat tant qu'un AUTRE ennemi REVENGER est en jeu",
       "`ThisCannotTakeDamageWhile(conditions=[AutreEnnemiRevenger])` (modele 05027) ; Asti est le second Revenger",
       [SANS_POUVOIR, "Puzzle.PutIntoPlay('sk165')", "Puzzle.PutIntoPlay('sk163')"], ["Puzzle.Damage('sk165', 2)"],
       {"degats": [["sk165", 0]]}),
    _c("sk165 The Maker, TEMOIN : seul Revenger en jeu, il subit les degats",
       "« ANOTHER REVENGER enemy » : il ne se compte pas lui-meme",
       [SANS_POUVOIR, "Puzzle.PutIntoPlay('sk165')"], ["Puzzle.Damage('sk165', 2)"], {"degats": [["sk165", 2]]}),
    _c("sk165 The Maker : le MECHANT devenu REVENGER (The Revenge Time) suffit a le rendre invulnerable",
       "« enemy » : le mechant compte des qu'il porte le trait (sk168 le lui donne)",
       [SANS_POUVOIR, "Puzzle.PutIntoPlay('sk165')", "Puzzle.PutIntoPlay('sk168')"], ["Puzzle.Damage('sk165', 2)"],
       {"degats": [["sk165", 0]]}),
    _c("sk165 The Maker : revele -> cherche The Revenge Time dans le deck et la defausse et la revele",
       "`Search.EncounterCard(include_discard_pile=True, name=..., card_type=SchemeSide2)` + `Reveal` (modele 01136)",
       [SANS_POUVOIR, "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('sk168', '01101')"],
       ["Puzzle.Reveal('sk165')"], {"en_jeu": ["sk165", "sk168"]}),
    _c("sk165 The Maker : The Revenge Time dans la DEFAUSSE rencontre est trouvee aussi",
       "« Search the encounter deck AND discard pile »",
       [SANS_POUVOIR, "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDiscardPile('sk168')"],
       ["Puzzle.Reveal('sk165')"], {"en_jeu": ["sk165", "sk168"]}),
    _c("sk166 Vermin : ses attaques sont INDIRECTES -> le joueur REPARTIT les degats : l'allie (Black Cat) les encaisse, le heros non",
       "`UnitAttackGainKeyword('This', indirect_damage=True)` ; ATQ 2 sur Black Cat (2 PV) : vaincu ; Spider-Man intact",
       [HEROS, "Puzzle.PutIntoPlay('01002', under_control=True)", "Puzzle.PutIntoPlay('sk166')"], ["Puzzle.Attack('sk166')"],
       {"degats_identite": 0, "hors_jeu": ["01002"]}, cibles=["01002", "01002"], main_exclusive=["01088"],
       passer_sur_option="Defense"),
    _c("sk166 Vermin, TEMOIN : Shocker (ATQ 2, direct) frappe le HEROS, l'allie est intact",
       "ligne de base du precedent : une attaque directe ne se repartit pas",
       [HEROS, "Puzzle.PutIntoPlay('01002', under_control=True)", "Puzzle.PutIntoPlay('01103')"], ["Puzzle.Attack('01103')"],
       {"degats_identite": 2, "en_jeu": ["01002"]}, main_exclusive=["01088"], passer_sur_option="Defense"),
    _c("sk166 Vermin : Boost -> l'attaque de Paibok (ATQ 2 + 1 icone = 3) devient INDIRECTE : l'allie encaisse, le heros non",
       "`WhenCardBecomeBoost('This', ..., during_attack=True)` + `would_atk_message.SetDealIndirectDamage` (modele 27122)",
       [SANS_POUVOIR, HEROS, "Puzzle.PutIntoPlay('01002', under_control=True)"], ["Puzzle.Boost('sk166')"],
       {"degats_identite": 0, "hors_jeu": ["01002"]}, cibles=["01002"] * 3, main_exclusive=["01088"],
       passer_sur_option="Defense"),
    _c("sk166 Vermin, TEMOIN : une carte de boost de 1 icone sans effet -> attaque DIRECTE : le heros encaisse 3, l'allie est intact",
       "ligne de base du precedent (01101 Hydra Mercenary, 1 icone)",
       [SANS_POUVOIR, HEROS, "Puzzle.PutIntoPlay('01002', under_control=True)"], ["Puzzle.Boost('01101')"],
       {"degats_identite": 3, "en_jeu": ["01002"]}, main_exclusive=["01088"], passer_sur_option="Defense"),
    _c("sk167 White Tiger : Quickstrike (natif) -> elle attaque des son engagement avec le heros (ATQ 2)",
       "`desc.Quickstrike 1` : aucun module pour ce mot-cle ; attaque laissee sans defense",
       [HEROS], ["Puzzle.PutIntoPlay('sk167')"], {"degats_identite": 2}, main_exclusive=["01088"], passer_sur_option="Defense"),
    _c("sk167 White Tiger : vaincue -> le mechant recoit 1 carte de boost face cachee",
       "`WhenUnitBeDefeated(WhenDefeated)` + `Faces.GiveFacedownBoostCards([villain], 1, effect)`",
       [SANS_POUVOIR, "Puzzle.PutIntoPlay('sk167')"], ["Puzzle.Damage('sk167', 3)"],
       {"hors_jeu": ["sk167"], "boosts_mechant": 1}),
    _c("sk167 White Tiger, TEMOIN : un autre sbire vaincu ne donne aucune carte de boost au mechant",
       "ligne de base du precedent (Hydra Mercenary, 3 PV)",
       [SANS_POUVOIR, "Puzzle.PutIntoPlay('01101')"], ["Puzzle.Damage('01101', 3)"],
       {"hors_jeu": ["01101"], "boosts_mechant": 0}),
    _c("sk168 The Revenge Time : le MECHANT gagne le trait REVENGER ; icone Acceleration",
       "`GiveKeywordToInPlayWhenApplyThis(Villain, trait='REVENGER')` ; `desc.Acceleration 1`",
       [SANS_POUVOIR], ["Puzzle.Reveal('sk168')"],
       {"traits_mechant": [["REVENGER", True]], "icones": [["Acceleration", 1]]}),
    _c("sk168 The Revenge Time, TEMOIN : sans la carte le mechant n'est pas REVENGER",
       "ligne de base du precedent",
       [SANS_POUVOIR], [], {"traits_mechant": [["REVENGER", False]]}),
    _c("sk168 The Revenge Time : revelee -> +1 menace par ennemi REVENGER en jeu (2 sbires + le mechant = 3 : 2 + 3)",
       "« for each REVENGER enemy in play » : le mechant, devenu Revenger, compte ; menace de depart 2[per_hero]",
       [SANS_POUVOIR, "Puzzle.PutIntoPlay('sk162')", "Puzzle.PutIntoPlay('sk163')"], ["Puzzle.Reveal('sk168')"],
       {"menace": [["sk168", 5]]}),
    _c("sk168 The Revenge Time : aucun sbire REVENGER -> seul le mechant compte (2 + 1)",
       "ligne de base du precedent",
       [SANS_POUVOIR], ["Puzzle.Reveal('sk168')"], {"menace": [["sk168", 3]]}),
    _c("sk169 Forming the Revengers : defausse jusqu'a une carte REVENGER (un sbire) et la revele",
       "`Worlds.DiscardEncounterCardsUntil(trait='REVENGER')` + `Reveal` ; Hydra Mercenary au-dessus est defausse",
       [SANS_POUVOIR, "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01104', 'sk162', '01101')"],
       ["Puzzle.Reveal('sk169')"], {"en_jeu": ["sk162"], "defausse_rencontre": ["01101"]}),
    _c("sk169 Forming the Revengers : « a card WITH the REVENGER trait » : l'ENVIRONNEMENT O.M.N.I.T.R.O.N.I.C.U.S. convient",
       "tout type de carte porteuse du trait",
       [SANS_POUVOIR, "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01104', 'sk161', '01101')"],
       ["Puzzle.Reveal('sk169')"], {"en_jeu": ["sk161"], "defausse_rencontre": ["01101"]}),
    # ===================================================================== stades du mechant (jetons et attachements)
    _c("sk142 Changement de stade : Paibok II garde ses jetons de maitrise ET ses attachements",
       "`AdvanceVillain` : la meme carte prend la face du stade II ; les compteurs et attachements restent attaches a la carte",
       [SANS_POUVOIR, "Puzzle.PutIntoPlay('sk148')", "Puzzle.Counter('sk141', 'mastery', 1)"],
       ["Puzzle.AdvanceVillain()"], {"mechant_id": "sk142", "maitrise": 2, "pouvoirs": ["sk148"]}),
    _c("sk142 Paibok II revele : cherche un POWER SKRULL dans le DECK rencontre et le revele (il s'attache)",
       "`WhenThisRevealed` + `Search.EncounterCard(include_discard_pile=True, trait='POWER SKRULL')`",
       [SANS_POUVOIR, "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('sk150', '01101')"],
       ["Puzzle.AdvanceVillain()"], {"mechant_id": "sk142", "pouvoirs": ["sk150"]}),
    _c("sk142 Paibok II revele : un POWER SKRULL dans la DEFAUSSE rencontre est trouve aussi",
       "« Search the encounter deck AND discard pile »",
       [SANS_POUVOIR, "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01104')",
        "Puzzle.CreateEncounterDiscardPile('sk151')"],
       ["Puzzle.AdvanceVillain()"], {"mechant_id": "sk142", "pouvoirs": ["sk151"]}),
    _c("sk142 Paibok II revele, TEMOIN : aucun POWER SKRULL dans le deck ni la defausse -> rien n'est attache",
       "la fouille ne trouve rien (pas de boucle, pas d'erreur)",
       [SANS_POUVOIR, "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01101')"],
       ["Puzzle.AdvanceVillain()"], {"mechant_id": "sk142", "nb_pouvoirs": 0}),
    _c("sk143 Paibok III (expert) revele : cherche un POWER SKRULL et le revele (stade II -> stade III)",
       "meme texte que sk142 ; scenario EXPERT (villain: sk142, sk143)",
       [SANS_POUVOIR, "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('sk152', '01101')"],
       ["Puzzle.AdvanceVillain()"], {"mechant_id": "sk143", "pouvoirs": ["sk152"]}, scenario=SCE),
    _c("sk143 Paibok III : la regle des pouvoirs s'applique aussi au stade III (1 pouvoir, jetons >= 1 -> verrouille)",
       "`RegleDesPouvoirs()` presente sur les trois stades",
       [SANS_POUVOIR, "Puzzle.AdvanceVillain()", "Puzzle.PutIntoPlay('sk148')"], ["Puzzle.Discard('sk148')"],
       {"mechant_id": "sk143", "pouvoirs": ["sk148"]}, scenario=SCE),
    # ===================================================================== evenements : portee de Distracted / Trapped in Ice
    _c("sk153 Trapped in Ice : un EVENEMENT d'attaque (Swinging Web Kick, 8 degats) est reduit lui aussi (7)",
       "`WhenUnitWouldAttack` couvre les attaques que le moteur declare comme telles ; 8 - 1 sur Paibok (Robuste d'entree retire)",
       [SANS_POUVOIR, HEROS, "Puzzle.Tough('sk141')", "Puzzle.PutIntoPlay('sk153')"], [],
       {"degats": [["sk141", 7]]}, main_exclusive=["01005", "01088", "01089"], jouer=["01005"], cibles=["sk141"],
       payer_avec=["01088", "01089"]),
    _c("sk153 Trapped in Ice, TEMOIN : sans l'attachement Swinging Web Kick inflige 8",
       "ligne de base du precedent",
       [SANS_POUVOIR, HEROS, "Puzzle.Tough('sk141')"], [],
       {"degats": [["sk141", 8]]}, main_exclusive=["01005", "01088", "01089"], jouer=["01005"], cibles=["sk141"],
       payer_avec=["01088", "01089"]),
    _c("sk147 Distracted : un EVENEMENT de contre (Crisis Interdiction, 2 menaces) retire 1 menace de moins",
       "evenement `(thwart)` : 4 - (2 - 1) = 3",
       [HEROS, "Puzzle.EmptyHand()", "Puzzle.SetThreat('sk144b', 4)", "Puzzle.PutIntoPlay('sk147')"], [],
       {"menace": [["sk144b", 3]]}, main_exclusive=["01012", "01088"], jouer=["01012"], cibles=["sk144b"],
       payer_avec=["01088"]),
    _c("sk147 Distracted, TEMOIN : sans l'attachement Crisis Interdiction retire 2 menaces (4 -> 2)",
       "ligne de base du precedent",
       [HEROS, "Puzzle.EmptyHand()", "Puzzle.SetThreat('sk144b', 4)"], [],
       {"menace": [["sk144b", 2]]}, main_exclusive=["01012", "01088"], jouer=["01012"], cibles=["sk144b"],
       payer_avec=["01088"]),
    # ===================================================================== New Revengers hors Paibok (set modulaire)
    _c("sk168 The Revenge Time dans un AUTRE scenario (Rhino) : le mechant Rhino devient REVENGER (menace 2 + 1)",
       "le set est retirable du scenario Paibok et ajoutable ailleurs (insert p.12) : aucun texte ne suppose Paibok",
       [], ["Puzzle.Reveal('sk168')"], {"traits_mechant": [["REVENGER", True]], "menace": [["sk168", 3]]}, scenario="rhino"),
    _c("sk165 The Maker dans le scenario Rhino : revele, il trouve The Revenge Time ; Rhino devenu REVENGER le rend invulnerable",
       "chaine complete du set hors Paibok : fouille -> revelation -> trait donne au mechant -> « another REVENGER enemy »",
       ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('sk168', '01101')"],
       ["Puzzle.Reveal('sk165')", "Puzzle.Damage('sk165', 2)"],
       {"en_jeu": ["sk165", "sk168"], "traits_mechant": [["REVENGER", True]], "degats": [["sk165", 0]]}, scenario="rhino"),
]

VERIFICATIONS = r'''
def paibok_dump(monde, aides):
    """SONDE de mise au point (jamais dans la batterie finale) : decrit l'etat, rend toujours False."""
    lignes = []
    identite = aides["identite"](monde)
    lignes.append(f"identite={identite.paper.card_id} forme={'Hero' if monde.players[0].IsHero() else 'AlterEgo'} main={len(list(monde.players[0].hand_cards.Get()))}")
    lignes.append("attaches identite=" + str([a.paper.card_id for a in identite.GetAttachedAttachments()]))
    for objet in monde.object_manager.card_dict.values():
        f = objet.face
        if f is not None and f.IsInPlay() and getattr(f.paper, "card_id", "").startswith("sk"):
            ab = [str(e.ability.type) for e in f.effects][:8]
            lignes.append(f"{f.paper.card_id} menace={getattr(f, 'threat', None)} abilities={ab}")
    return False, " | ".join(lignes)


def _paibok_villain(monde):
    from game.operate.worlds import Worlds
    vilains = Worlds.GetAllVillains(monde)
    return vilains[0] if vilains else None


def _pouvoirs(villain):
    return [a for a in villain.GetAttachedAttachments() if a.HasTrait("POWER SKRULL")]


def paibok_etat(monde, aides):
    """etat_attendu (cles communes) + les cles propres au scenario Paibok :
    maitrise, nb_pouvoirs, pouvoirs, mechant_id, stalwart, traits_mechant, defaite,
    action_offerte [[card_id, n]]."""
    attendu = aides["cas"].get("attendu") or {}
    # Une cle INCONNUE etait ignoree en silence (verifier != "etat_attendu") : on la refuse ici.
    connues = set(CLES_ETAT_ATTENDU) | {"maitrise", "nb_pouvoirs", "pouvoirs", "mechant_id", "stalwart",
                                        "traits_mechant", "defaite", "action_offerte", "pas_dans_deck_rencontre",
                                        "boosts_mechant", "defausse_rencontre_taille"}
    inconnues = sorted(set(attendu) - connues)
    if inconnues:
        return False, f"cle(s) attendu INCONNUE(S) de paibok_etat : {inconnues}"
    ok, message = etat_attendu(monde, aides)
    soucis = [] if ok else [message]
    v = _paibok_villain(monde)
    if v is None:
        return False, "aucun mechant en jeu"
    if "maitrise" in attendu and v.GetCounters("mastery") != attendu["maitrise"]:
        soucis.append(f"jetons de maitrise = {v.GetCounters('mastery')} (attendu {attendu['maitrise']})")
    if "mechant_id" in attendu and v.paper.card_id != attendu["mechant_id"]:
        soucis.append(f"mechant = {v.paper.card_id} (attendu {attendu['mechant_id']})")
    ids = sorted(a.paper.card_id for a in _pouvoirs(v))
    if "nb_pouvoirs" in attendu and len(ids) != attendu["nb_pouvoirs"]:
        soucis.append(f"POWER SKRULL attaches = {ids} (attendu {attendu['nb_pouvoirs']})")
    if "pouvoirs" in attendu and ids != sorted(attendu["pouvoirs"]):
        soucis.append(f"POWER SKRULL attaches = {ids} (attendu {sorted(attendu['pouvoirs'])})")
    if "stalwart" in attendu and bool(v.IsStalwart()) != attendu["stalwart"]:
        soucis.append(f"stalwart = {v.IsStalwart()} (attendu {attendu['stalwart']})")
    for trait, present in attendu.get("traits_mechant") or []:
        if bool(v.HasTrait(trait)) != present:
            soucis.append(f"trait {trait} sur le mechant = {v.HasTrait(trait)} (attendu {present})")
    if attendu.get("pas_dans_deck_rencontre"):
        from game.operate.worlds import Worlds
        ids = {getattr(f.paper, "card_id", None) for f in Worlds.GetEncounterDeckCards(monde)}
        for card_id in attendu["pas_dans_deck_rencontre"]:
            if card_id in ids:
                soucis.append(f"{card_id} est dans le deck rencontre (attendu : absent)")
    if "defausse_rencontre_taille" in attendu:
        from game.operate.worlds import Worlds
        n = len(Worlds.GetEncounterDiscardPileCards(monde))
        if n != attendu["defausse_rencontre_taille"]:
            soucis.append(f"defausse rencontre = {n} carte(s) (attendu {attendu['defausse_rencontre_taille']})")
    if "boosts_mechant" in attendu:
        n = v.components.boostable.GetDeck().GetSize()
        if n != attendu["boosts_mechant"]:
            soucis.append(f"cartes de boost face cachee du mechant = {n} (attendu {attendu['boosts_mechant']})")
    if "defaite" in attendu:
        perdu = bool(monde.is_game_over) and not monde.game_over.players_won
        if perdu != attendu["defaite"]:
            soucis.append(f"defaite = {perdu} (attendu {attendu['defaite']}, partie terminee = {monde.is_game_over})")
    for card_id, n in attendu.get("action_offerte") or []:
        from game.ability.ability import AbilityType
        from game.event.manager import EventManager
        from game.message import Message
        from game.effect.rule import GameRule
        face = aides["par_id"](monde, card_id)
        if face is None:
            soucis.append(f"{card_id} introuvable en jeu (action_offerte)")
            continue
        joueur = monde.GetCurrentPlayer()
        candidats = [x for x in face.effect.Find(when=Message.WhenPlayerInTurn, type=AbilityType.HeroAction)
                     if not x.ability.is_play]
        msg = Message.WhenPlayerLikeInTurn(joueur, GameRule(joueur.GetIdentity()))
        msg.Send()
        offertes = EventManager.FilterAvailableEffects(msg, candidats, joueur, monde, None)
        if len(offertes) != n:
            soucis.append(f"{card_id} offre {len(offertes)} Action(s) de heros (attendu {n})")
    if soucis:
        return False, " ; ".join(soucis)
    return True, "etat Paibok conforme"
'''
