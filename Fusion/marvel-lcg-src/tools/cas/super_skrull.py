# Cas test_capacites du scenario SUPER-SKRULL (sk117-135) et du set Kree-Skrull War (sk136-140).
# Prefixe des cas : [super_skrull] ; filtre : `super_skrull`.
#
# Le heros de test (Spider-Man 01001) demarre en alter ego (01001b) ; `Puzzle.ChangeForm('01001b')` le
# passe en heros. A la mise en place, la graine du harnais attache `sk122` Flexibility au Super-Skrull
# (complot sk120b) : `RAZ` le retire du jeu pour partir d'un plateau connu (paquet SUPERPOWER de 3 cartes,
# aucun pouvoir attache). `NEUTRE` remplace le deck rencontre par trois cartes sans icone de boost.

RAZ = "Puzzle.Remove('sk122')"
RAZ_EXPERT = "Puzzle.Remove('sk125')"   # mode expert : la graine attache sk125 a la mise en place
NEUTRE = ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('sk101', 'sk101', 'sk101')"]
SANS_EARTH = "Puzzle.Remove('sk138')"   # Earth Involvement (crise) bloquerait le contre du complot principal

CAS = [
    # ===================================================================
    # Mise en place, mechants, complots principaux
    # ===================================================================
    {
        "nom": "[super_skrull] sk120a Setup : paquet SUPERPOWER cree, sk120b revele, UN pouvoir attache au Super-Skrull",
        "pourquoi": ("Livret p. 10 : les 4 attachements SUPERPOWER forment un paquet a cote du complot ; sk120b (When "
                     "Revealed) revele la carte du dessus, qui s'attache au Super-Skrull : reste 3 cartes dans le paquet. "
                     "Earth Involvement (Setup) commence la partie en jeu"),
        "scenario": "sk_super_skrull",
        "heros": "spider_man",
        "mise_en_place": [],
        "declencher": [],
        "verifier": "ss_etat",
        "attendu": {"en_jeu": ["sk117", "sk120b", "sk138"], "hors_jeu": ["sk118", "sk119", "sk121a"],
                    "paquet": 3, "pouvoirs_sur_mechant": 1, "menace": [["sk138", 1]], "pv_max": [["sk117", 14]]},
    },
    {
        "nom": "[super_skrull] Setup EXPERT : on commence au stade II (sk118), un pouvoir attache, paquet de 3",
        "pourquoi": "Insert p. 10 : mode expert = Super-Skrull (II) puis (III) ; meme paquet SUPERPOWER",
        "scenario": "sk_super_skrull_expert",
        "heros": "spider_man",
        "mise_en_place": [],
        "declencher": [],
        "verifier": "ss_etat",
        "attendu": {"en_jeu": ["sk118", "sk120b", "sk138"], "hors_jeu": ["sk117", "sk119"],
                    "paquet": 3, "pouvoirs_sur_mechant": 1, "pv_max": [["sk118", 16]]},
    },
    {
        "nom": "[super_skrull] sk117 Super-Skrull I — Reponse obligatoire apres l'etape 2 : tout revient au paquet, UNE carte revelee",
        "pourquoi": ("Deux pouvoirs attaches (sk124, sk125), paquet {sk123} ; on joue la phase du mechant : les deux retournent "
                     "dans le paquet, qui est melange, puis une seule carte est revelee (stade I) : 1 pouvoir, paquet de 2. "
                     "Sans le module, les deux restent attaches"),
        "scenario": "sk_super_skrull",
        "heros": "spider_man",
        "mise_en_place": [RAZ, "Puzzle.Reveal('sk124')", "Puzzle.Reveal('sk125')", *NEUTRE],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.RunVillainPhase()"],
        "verifier": "ss_etat",
        "attendu": {"en_jeu": ["sk117"], "pouvoirs_sur_mechant": 1, "paquet": 2},
    },
    {
        "nom": "[super_skrull] sk118 Super-Skrull II — Reponse obligatoire : DEUX cartes revelees (stade II)",
        "pourquoi": ("Expert, stade II. Un pouvoir attache (sk124), paquet {sk123, sk125} ; apres la phase : tout est remelange "
                     "puis 2 cartes sont revelees : 2 pouvoirs, paquet de 1. Sans le module : 1 pouvoir, paquet de 2"),
        "scenario": "sk_super_skrull_expert",
        "heros": "spider_man",
        "mise_en_place": [RAZ_EXPERT, "Puzzle.Reveal('sk124')", *NEUTRE],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.RunVillainPhase()"],
        "verifier": "ss_etat",
        "attendu": {"en_jeu": ["sk118"], "pouvoirs_sur_mechant": 2, "paquet": 1},
    },
    {
        "nom": "[super_skrull] sk117 Super-Skrull I — vaincu : le stade II herite des pouvoirs attaches (les attachements restent au mechant)",
        "pourquoi": ("Regle native du moteur : quand le mechant avance de stade, ses attachements restent (le stade II porte encore Pyrokinesis) ; "
                     "le paquet SUPERPOWER n'est pas touche (2 cartes)"),
        "scenario": "sk_super_skrull",
        "heros": "spider_man",
        "mise_en_place": [RAZ, "Puzzle.Reveal('sk124')", "Puzzle.Damage('sk117', 14)", *NEUTRE],
        "main_exclusive": ["01088"],
        "declencher": [],
        "verifier": "ss_etat",
        "attendu": {"en_jeu": ["sk118"], "hors_jeu": ["sk117"], "attaches": [["sk118", "sk124"]], "paquet": 2, "defausse_paquet": 0},
    },
    {
        "nom": "[super_skrull] sk119 Super-Skrull III — stade III (expert) : deux cartes, et la defausse du paquet revient au paquet",
        "pourquoi": ("Expert, stade III (AdvanceVillain). Pyrokinesis est defaussee par un effet : elle va dans la defausse du paquet SUPERPOWER ; la "
                     "Reponse obligatoire remelange paquet ET defausse (choix Q1, defs/super_skrull_questions.md) puis revele 2 cartes : "
                     "2 pouvoirs, paquet de 1, defausse vide"),
        "scenario": "sk_super_skrull_expert",
        "heros": "spider_man",
        "mise_en_place": [RAZ_EXPERT, "Puzzle.Reveal('sk124')", "Puzzle.AdvanceVillain()", "Puzzle.Discard('sk124')", *NEUTRE],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.RunVillainPhase()"],
        "verifier": "ss_etat",
        "attendu": {"en_jeu": ["sk119"], "hors_jeu": ["sk118"], "pouvoirs_sur_mechant": 2, "paquet": 1, "defausse_paquet": 0},
    },
    {
        "nom": "[super_skrull] sk119 Super-Skrull III — PV 19 par joueur, SCH 2 (les trois stades ont leurs chiffres)",
        "pourquoi": "Valeurs imprimees : HP 19*, ATK 2, SCH 2 (le stade II : 16, 2, 1 ; le stade I : 14, 2, 1)",
        "scenario": "sk_super_skrull_expert",
        "heros": "spider_man",
        "mise_en_place": [RAZ_EXPERT, "Puzzle.AdvanceVillain()"],
        "declencher": [],
        "verifier": "ss_etat",
        "attendu": {"en_jeu": ["sk119"], "pv_max": [["sk119", 19]], "attributs_carte": [["sk119", "scheme", 0], ["sk119", "attack", 0]]},
    },
    {
        "nom": "[super_skrull] sk121a Heir to the Throne 2A — Lord Kl'rt absent : il est cherche et attache au Super-Skrull",
        "pourquoi": ("2A : « search the encounter deck and discard pile for Lord Kl'rt and attach it to Super-Skrull ». "
                     "Deck : sk127 sous deux autres cartes ; on avance le complot (1B -> 2A -> 2B)"),
        "scenario": "sk_super_skrull",
        "heros": "spider_man",
        "mise_en_place": [RAZ, "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('sk127', 'sk101', 'sk101')"],
        "declencher": ["Puzzle.AdvanceMainScheme()"],
        "verifier": "ss_etat",
        "attendu": {"en_jeu": ["sk121b", "sk127"], "attaches": [["sk117", "sk127"]]},
    },
    {
        "nom": "[super_skrull] sk121a Heir to the Throne 2A — Lord Kl'rt deja en jeu : une carte rencontre face cachee a chaque joueur",
        "pourquoi": "« If Lord Kl'rt is in play, deal each player a facedown encounter card » ; une seule copie reste en jeu",
        "scenario": "sk_super_skrull",
        "heros": "spider_man",
        "mise_en_place": [RAZ, "Puzzle.PutIntoPlay('sk127')", "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('sk127', 'sk101', 'sk101')"],
        "declencher": ["Puzzle.AdvanceMainScheme()"],
        "verifier": "ss_etat",
        "attendu": {"en_jeu": ["sk121b", "sk127"], "cartes_distribuees": 1, "dans_deck_rencontre": ["sk127"]},
    },
    {
        "nom": "[super_skrull] sk121b Heir to the Throne 2B — revelee : un pouvoir de plus est revele",
        "pourquoi": "2B : « Reveal the top card of the SUPERPOWER deck » : le pouvoir de la mise en place + un deuxieme ; paquet de 2",
        "scenario": "sk_super_skrull",
        "heros": "spider_man",
        "mise_en_place": ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('sk127', 'sk101', 'sk101')"],
        "declencher": ["Puzzle.AdvanceMainScheme()"],
        "verifier": "ss_etat",
        "attendu": {"en_jeu": ["sk121b"], "pouvoirs_sur_mechant": 2, "paquet": 2},
    },

    {
        "nom": "[super_skrull] sk117 Super-Skrull I — a DEUX joueurs : 28 PV (14 par joueur), Earth Involvement a 2 menaces, 2 joueurs dans la partie",
        "pourquoi": "Valeurs « par joueur » (HP 14*, StartingThreat 1*) multipliees par le nombre de joueurs",
        "scenario": "sk_super_skrull",
        "heros": "spider_man",
        "heros2": "hawkeye",
        "mise_en_place": [],
        "declencher": [],
        "verifier": "ss_etat",
        "attendu": {"en_jeu": ["sk117", "sk138"], "pv_max": [["sk117", 28]], "menace": [["sk138", 2]]},
    },
    # ===================================================================
    # Paquet SUPERPOWER : les quatre attachements
    # ===================================================================
    {
        "nom": "[super_skrull] sk122 Flexibility — +1 SCH et le Super-Skrull gagne stalwart (il ne peut plus etre etourdi)",
        "pourquoi": "`GiveKeywordToAttached(stalwart=1)` + cle desc SCH+ : SCH 1 -> 2 ; `Puzzle.Stun` est refuse (Stalwart natif)",
        "scenario": "sk_super_skrull",
        "heros": "spider_man",
        "mise_en_place": [RAZ, "Puzzle.Reveal('sk122')", "Puzzle.Stun('sk117')"],
        "declencher": [],
        "verifier": "ss_etat",
        "attendu": {"attaches": [["sk117", "sk122"]], "attributs_carte": [["sk117", "scheme", 1]], "statuts_absents": [["sk117", "Stunned"]]},
    },
    {
        "nom": "[super_skrull] sk122 Flexibility — TEMOIN sans pouvoir : le Super-Skrull est bien etourdi, SCH imprime",
        "pourquoi": "Meme montage sans l'attachement : Stunned pose, SCH 1",
        "scenario": "sk_super_skrull",
        "heros": "spider_man",
        "mise_en_place": [RAZ, "Puzzle.Stun('sk117')"],
        "declencher": [],
        "verifier": "ss_etat",
        "attendu": {"statuts": [["sk117", "Stunned"]], "attributs_carte": [["sk117", "scheme", 0]]},
    },
    {
        "nom": "[super_skrull] sk122 Flexibility — ses attaques gagnent Distance : la Riposte de l'allie defenseur est ignoree",
        "pourquoi": "`UnitAttackGainKeyword(mechant, ranged=True)` : U.S. Agent (Riposte 1) defend, le Super-Skrull ne prend rien",
        "scenario": "sk_super_skrull",
        "heros": "spider_man",
        "mise_en_place": [RAZ, "Puzzle.Reveal('sk122')", "Puzzle.ChangeForm('01001b')", "Puzzle.PutIntoPlay('04014')", *NEUTRE],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Attack('sk117', '04014')"],
        "verifier": "ss_etat",
        "attendu": {"degats": [["sk117", 0]]},
    },
    {
        "nom": "[super_skrull] sk122 Flexibility — TEMOIN Riposte : sans Distance, le Super-Skrull encaisse la Riposte (1 degat)",
        "pourquoi": "Meme montage sans l'attachement",
        "scenario": "sk_super_skrull",
        "heros": "spider_man",
        "mise_en_place": [RAZ, "Puzzle.ChangeForm('01001b')", "Puzzle.PutIntoPlay('04014')", *NEUTRE],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Attack('sk117', '04014')"],
        "verifier": "ss_etat",
        "attendu": {"degats": [["sk117", 1]]},
    },
    {
        "nom": "[super_skrull] sk123 Invisibility — +1 SCH",
        "pourquoi": "Cle desc SCH+ (HasModify) : SCH 1 -> 2",
        "scenario": "sk_super_skrull",
        "heros": "spider_man",
        "mise_en_place": [RAZ, "Puzzle.Reveal('sk123')"],
        "declencher": [],
        "verifier": "ss_etat",
        "attendu": {"attaches": [["sk117", "sk123"]], "attributs_carte": [["sk117", "scheme", 1]]},
    },
    {
        "nom": "[super_skrull] sk123 Invisibility — attaquer le Super-Skrull coute 1 ressource : l'attaque part, une carte est depensee",
        "pourquoi": ("« As an additional cost to attack Super-Skrull, you must spend 1 resource of any type ». Spider-Man (ATK 2) "
                     "attaque avec 2 cartes en main : le cout est paye (1 carte) et l'attaque blesse le mechant (2)"),
        "scenario": "sk_super_skrull",
        "heros": "spider_man",
        "mise_en_place": [RAZ, "Puzzle.Reveal('sk123')", "Puzzle.ChangeForm('01001b')", *NEUTRE],
        "main_exclusive": ["01088", "01089"],
        "cibles": ["sk117"],
        "declencher": ["Puzzle.Attack('01001a')"],
        "verifier": "ss_etat",
        "attendu": {"degats": [["sk117", 2]], "taille_main": 1},
    },
    {
        "nom": "[super_skrull] sk123 Invisibility — main vide : le cout ne peut pas etre paye, l'attaque est annulee",
        "pourquoi": "Aucune ressource a depenser : `SetBeInstead`, le Super-Skrull ne subit rien",
        "scenario": "sk_super_skrull",
        "heros": "spider_man",
        "mise_en_place": [RAZ, "Puzzle.Reveal('sk123')", "Puzzle.ChangeForm('01001b')", "Puzzle.EmptyHand()", *NEUTRE],
        "cibles": ["sk117"],
        "declencher": ["Puzzle.Attack('01001a')"],
        "verifier": "ss_etat",
        "attendu": {"degats": [["sk117", 0]], "taille_main": 0},
    },
    {
        "nom": "[super_skrull] sk123 Invisibility — TEMOIN sans pouvoir : l'attaque ne coute rien (2 degats, main intacte)",
        "pourquoi": "Meme montage sans l'attachement",
        "scenario": "sk_super_skrull",
        "heros": "spider_man",
        "mise_en_place": [RAZ, "Puzzle.ChangeForm('01001b')", *NEUTRE],
        "main_exclusive": ["01088", "01089"],
        "cibles": ["sk117"],
        "declencher": ["Puzzle.Attack('01001a')"],
        "verifier": "ss_etat",
        "attendu": {"degats": [["sk117", 2]], "taille_main": 2},
    },
    {
        "nom": "[super_skrull] sk124 Pyrokinesis — +1 ATK (le Super-Skrull passe de 2 a 3)",
        "pourquoi": "Cle desc ATK+ : ATK 2 -> 3 (le ★ du badge renvoie au texte, sans valeur de plus)",
        "scenario": "sk_super_skrull",
        "heros": "spider_man",
        "mise_en_place": [RAZ, "Puzzle.Reveal('sk124')"],
        "declencher": [],
        "verifier": "ss_etat",
        "attendu": {"attaches": [["sk117", "sk124"]], "attributs_carte": [["sk117", "attack", 1]]},
    },
    {
        "nom": "[super_skrull] sk124 Pyrokinesis — un personnage ami contre le complot principal : il prend 1 degat",
        "pourquoi": ("`AfterUnitThwartScheme(ForcedResponse, ..., MainScheme)` : Spider-Man (hero) contre le complot principal "
                     "(menace posee a 5, Earth Involvement retire pour lever la Crise) et recoit 1 degat"),
        "scenario": "sk_super_skrull",
        "heros": "spider_man",
        "mise_en_place": [RAZ, SANS_EARTH, "Puzzle.Reveal('sk124')", "Puzzle.SetThreat('sk120b', 5)", "Puzzle.ChangeForm('01001b')", *NEUTRE],
        "main_exclusive": ["01088"],
        "cibles": ["sk120b"],
        "declencher": ["Puzzle.Thwart('01001a')"],
        "verifier": "ss_etat",
        "attendu": {"menace": [["sk120b", 4]], "degats_identite": 1},
    },
    {
        "nom": "[super_skrull] sk124 Pyrokinesis — CONTRE-CAS complot ANNEXE contre : aucun degat",
        "pourquoi": "« thwarts the MAIN scheme » : le contre d'un complot annexe (sk101) ne declenche rien",
        "scenario": "sk_super_skrull",
        "heros": "spider_man",
        "mise_en_place": [RAZ, SANS_EARTH, "Puzzle.Reveal('sk124')", "Puzzle.PutIntoPlay('sk101')", "Puzzle.ChangeForm('01001b')", *NEUTRE],
        "main_exclusive": ["01088"],
        "cibles": ["sk101"],
        "declencher": ["Puzzle.Thwart('01001a')"],
        "verifier": "ss_etat",
        "attendu": {"menace": [["sk101", 2]], "degats_identite": 0},
    },
    {
        "nom": "[super_skrull] sk124 Pyrokinesis — ses attaques gagnent Perforant : la carte Tough du heros est defaussee ET il subit les degats",
        "pourquoi": ("`UnitAttackGainKeyword(mechant, piercing=True)` : Spider-Man (Tough) attaque non defendu par le Super-Skrull "
                     "(ATK 2 + 1 = 3) : la carte Tough part et les 3 degats passent. Sans Perforant, Tough absorberait tout"),
        "scenario": "sk_super_skrull",
        "heros": "spider_man",
        "mise_en_place": [RAZ, "Puzzle.Reveal('sk124')", "Puzzle.ChangeForm('01001b')", "Puzzle.Tough('01001a')", *NEUTRE],
        "main_exclusive": ["01088"],
        "passer_sur_option": "Defense",
        "declencher": ["Puzzle.Attack('sk117')"],
        "verifier": "ss_etat",
        "attendu": {"degats_identite": 3, "statuts_absents": [["01001a", "Tough"]]},
    },
    {
        "nom": "[super_skrull] sk124 Pyrokinesis — TEMOIN Tough : sans Perforant, la carte Tough absorbe l'attaque (0 degat)",
        "pourquoi": "Meme montage sans l'attachement",
        "scenario": "sk_super_skrull",
        "heros": "spider_man",
        "mise_en_place": [RAZ, "Puzzle.ChangeForm('01001b')", "Puzzle.Tough('01001a')", *NEUTRE],
        "main_exclusive": ["01088"],
        "passer_sur_option": "Defense",
        "declencher": ["Puzzle.Attack('sk117')"],
        "verifier": "ss_etat",
        "attendu": {"degats_identite": 0, "statuts_absents": [["01001a", "Tough"]]},
    },
    {
        "nom": "[super_skrull] sk125 Rock Mimicry — le Super-Skrull attaque avec UNE carte boost de plus (2 icones au lieu de 1)",
        "pourquoi": ("Forced Interrupt « When Super-Skrull attacks, give him 1 additional boost card for this activation » : deck "
                     "rencontre de trois Hypnotic Gaze (1 icone chacun) ; ATK 2 + 2 boosts = 4 degats (sans le pouvoir : 3)"),
        "scenario": "sk_super_skrull",
        "heros": "spider_man",
        "mise_en_place": [RAZ, "Puzzle.Reveal('sk125')", "Puzzle.ChangeForm('01001b')",
                          "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('sk133', 'sk133', 'sk133')"],
        "main_exclusive": ["01088"],
        "passer_sur_option": "Defense",
        "declencher": ["Puzzle.Attack('sk117')"],
        "verifier": "ss_etat",
        "attendu": {"attaches": [["sk117", "sk125"]], "degats_identite": 4},
    },
    {
        "nom": "[super_skrull] sk125 Rock Mimicry — TEMOIN : sans le pouvoir, une seule carte boost (3 degats)",
        "pourquoi": "Meme montage sans l'attachement",
        "scenario": "sk_super_skrull",
        "heros": "spider_man",
        "mise_en_place": [RAZ, "Puzzle.ChangeForm('01001b')",
                          "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('sk133', 'sk133', 'sk133')"],
        "main_exclusive": ["01088"],
        "passer_sur_option": "Defense",
        "declencher": ["Puzzle.Attack('sk117')"],
        "verifier": "ss_etat",
        "attendu": {"degats_identite": 3},
    },
    {
        "nom": "[super_skrull] sk125 Rock Mimicry — ses attaques gagnent Dechainement : l'exces sur un allie vaincu va a l'identite",
        "pourquoi": ("`UnitAttackGainKeyword(mechant, overkill=True)` : Black Cat (2 PV, 1 degat deja) est vaincue par ATK 2 : "
                     "1 degat d'exces sur Spider-Man. (Deck neutre : aucune carte boost ne change le total.)"),
        "scenario": "sk_super_skrull",
        "heros": "spider_man",
        "mise_en_place": [RAZ, "Puzzle.Reveal('sk125')", "Puzzle.ChangeForm('01001b')", "Puzzle.PutIntoPlay('01002')", "Puzzle.Damage('01002', 1)", *NEUTRE],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Attack('sk117', '01002')"],
        "verifier": "ss_etat",
        "attendu": {"hors_jeu": ["01002"], "degats_identite": 1},
    },

    # ===================================================================
    # Cartes de rencontre du scenario
    # ===================================================================
    {
        "nom": "[super_skrull] sk126 Invisible Forcefield — revelee : s'attache a l'ennemi aux PV imprimes les plus eleves (le mechant)",
        "pourquoi": "`AttachToFaceWhenPutIntoPlay(Enemy, highest_printed_hp=True)` ; Praxagora (5 PV) est en jeu : le mechant (14) gagne",
        "scenario": "sk_super_skrull",
        "heros": "spider_man",
        "mise_en_place": [RAZ, "Puzzle.PutIntoPlay('sk129')", "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('sk126', 'sk101')"],
        "declencher": ["Puzzle.Reveal('sk126')"],
        "verifier": "ss_etat",
        "attendu": {"attaches": [["sk117", "sk126"]]},
    },
    {
        "nom": "[super_skrull] sk126 Invisible Forcefield — la 2e copie saute le mechant (deja protege) et va sur l'ennemi suivant",
        "pourquoi": "« without another Invisible Forcefield attached » : deux copies en deck, Praxagora (5 PV) en jeu ; la 2e s'attache a Praxagora",
        "scenario": "sk_super_skrull",
        "heros": "spider_man",
        "mise_en_place": [RAZ, "Puzzle.PutIntoPlay('sk129')", "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('sk101', 'sk126', 'sk126')"],
        "declencher": ["Puzzle.Reveal('sk126')", "Puzzle.Reveal('sk126')"],
        "verifier": "ss_etat",
        "attendu": {"attaches": [["sk117", "sk126"], ["sk129", "sk126"]]},
    },
    {
        "nom": "[super_skrull] sk126 Invisible Forcefield — aucun ennemi libre : elle gagne surge (la carte suivante est revelee)",
        "pourquoi": "Le mechant est deja protege et il n'y a pas d'autre ennemi : `if_cannot_gain_surge` : la carte du dessus (sk101) est revelee dans la foulee",
        "scenario": "sk_super_skrull",
        "heros": "spider_man",
        "mise_en_place": [RAZ, "Puzzle.Reveal('sk126')", "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('sk101', 'sk101', 'sk126')"],
        "surge_hors_phase": 1,
        "declencher": ["Puzzle.Reveal('sk126')"],
        "verifier": "ss_etat",
        "attendu": {"attaches": [["sk117", "sk126"]], "taille_attaches": [["sk117", 1]], "defausse_rencontre": ["sk126"], "en_jeu": ["sk101"]},
    },
    {
        "nom": "[super_skrull] sk126 Invisible Forcefield — les degats vont sur la carte : le Super-Skrull ne perd rien, 2 jetons de degat ici",
        "pourquoi": "Forced Interrupt « place it here instead » : Spider-Man (ATK 2) frappe le mechant protege",
        "scenario": "sk_super_skrull",
        "heros": "spider_man",
        "mise_en_place": [RAZ, "Puzzle.Reveal('sk126')", "Puzzle.ChangeForm('01001b')", *NEUTRE],
        "main_exclusive": ["01088"],
        "cibles": ["sk117"],
        "declencher": ["Puzzle.Attack('01001a')"],
        "verifier": "ss_etat",
        "attendu": {"degats": [["sk117", 0]], "compteurs": [["sk126", "damage", 2]], "en_jeu": ["sk126"]},
    },
    {
        "nom": "[super_skrull] sk126 Invisible Forcefield — a 5 degats ici ou plus : la carte est defaussee (3 puis 2 degats)",
        "pourquoi": "Deja 3 degats (Puzzle.Damage) ; l'attaque (2) en ajoute : 5 >= 5 -> defaussee ; le mechant n'a toujours rien subi",
        "scenario": "sk_super_skrull",
        "heros": "spider_man",
        "mise_en_place": [RAZ, "Puzzle.Reveal('sk126')", "Puzzle.Damage('sk117', 3)", "Puzzle.ChangeForm('01001b')", *NEUTRE],
        "main_exclusive": ["01088"],
        "cibles": ["sk117"],
        "declencher": ["Puzzle.Attack('01001a')"],
        "verifier": "ss_etat",
        "attendu": {"degats": [["sk117", 0]], "hors_jeu": ["sk126"], "defausse_rencontre": ["sk126"]},
    },
    {
        "nom": "[super_skrull] sk126 Invisible Forcefield — TEMOIN : sans la carte, le Super-Skrull encaisse les 2 degats",
        "pourquoi": "Meme attaque, aucun champ de force",
        "scenario": "sk_super_skrull",
        "heros": "spider_man",
        "mise_en_place": [RAZ, "Puzzle.ChangeForm('01001b')", *NEUTRE],
        "main_exclusive": ["01088"],
        "cibles": ["sk117"],
        "declencher": ["Puzzle.Attack('01001a')"],
        "verifier": "ss_etat",
        "attendu": {"degats": [["sk117", 2]]},
    },
    {
        "nom": "[super_skrull] sk127 Lord Kl'rt — revele : s'attache au Super-Skrull ; porte l'icone d'amplification",
        "pourquoi": "`AttachToFaceWhenPutIntoPlay(Super-Skrull)` ; cle desc Amplify 1 (croix + avion, convention du 15/10/2026)",
        "scenario": "sk_super_skrull",
        "heros": "spider_man",
        "mise_en_place": [RAZ, "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('sk127')"],
        "declencher": ["Puzzle.Reveal('sk127')"],
        "verifier": "ss_etat",
        "attendu": {"attaches": [["sk117", "sk127"]], "icones": [["Amplify", 1]]},
    },
    {
        "nom": "[super_skrull] sk127 Lord Kl'rt — Action de heros : le cout revele un pouvoir, l'effet defausse Lord Kl'rt",
        "pourquoi": "`PlayerActionToDiscardThis(HeroAction)` + `CostFunc.Custom` (reveler le dessus du paquet SUPERPOWER) : un pouvoir de plus, Kl'rt part",
        "scenario": "sk_super_skrull",
        "heros": "spider_man",
        "mise_en_place": [RAZ, "Puzzle.Reveal('sk127')", "Puzzle.ChangeForm('01001b')", *NEUTRE],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Action('sk127', 'HeroAction')"],
        "verifier": "ss_etat",
        "attendu": {"hors_jeu": ["sk127"], "pouvoirs_sur_mechant": 1, "paquet": 2, "defausse_rencontre": ["sk127"]},
    },
    {
        "nom": "[super_skrull] sk127 Lord Kl'rt — Boost : « Reveal this card » : revele pendant l'activation du mechant, il s'attache",
        "pourquoi": "`WhenCardBecomeBoost('This', RevealThisCard)` : `Puzzle.Boost` fait activer le mechant avec sk127 en boost",
        "scenario": "sk_super_skrull",
        "heros": "spider_man",
        "mise_en_place": [RAZ, "Puzzle.ChangeForm('01001b')", *NEUTRE],
        "main_exclusive": ["01088"],
        "passer_sur_option": "Defense",
        "declencher": ["Puzzle.Boost('sk127')"],
        "verifier": "ss_etat",
        "attendu": {"attaches": [["sk117", "sk127"]]},
    },
    {
        "nom": "[super_skrull] sk128 Mt'nox — attaque non defendue, carte physique (Strength) : le mechant recoit Tough",
        "pourquoi": ("`AfterUnitAttackUnit(ForcedResponse, 'This', 'You', is_undefended_attack=True)` : deck du joueur = Strength "
                     "(RR, physique) ; la carte est defaussee, Tough sur le Super-Skrull, rien d'autre"),
        "scenario": "sk_super_skrull",
        "heros": "spider_man",
        "mise_en_place": [RAZ, "Puzzle.PutIntoPlay('sk128')", "Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01091', '01090')", *NEUTRE],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Attack('sk128')"],
        "verifier": "ss_etat",
        "attendu": {"statuts": [["sk117", "Tough"]], "statuts_absents": [["01001b", "Stunned"], ["01001b", "Confused"]], "defausse_ids": ["01090"]},
    },
    {
        "nom": "[super_skrull] sk128 Mt'nox — attaque non defendue, carte energie (Energy) : le joueur est etourdi",
        "pourquoi": "Deck du joueur = Energy (YY, energie) : Stunned sur l'identite, pas de Tough ni de Confused",
        "scenario": "sk_super_skrull",
        "heros": "spider_man",
        "mise_en_place": [RAZ, "Puzzle.PutIntoPlay('sk128')", "Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01091', '01088')", *NEUTRE],
        "main_exclusive": ["01090"],
        "declencher": ["Puzzle.Attack('sk128')"],
        "verifier": "ss_etat",
        "attendu": {"statuts": [["01001b", "Stunned"]], "statuts_absents": [["sk117", "Tough"], ["01001b", "Confused"]], "defausse_ids": ["01088"]},
    },
    {
        "nom": "[super_skrull] sk128 Mt'nox — attaque non defendue, carte mentale (Genius) : le joueur est desoriente",
        "pourquoi": "Deck du joueur = Genius (BB, mental) : Confused sur l'identite, pas de Tough ni de Stunned",
        "scenario": "sk_super_skrull",
        "heros": "spider_man",
        "mise_en_place": [RAZ, "Puzzle.PutIntoPlay('sk128')", "Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01091', '01089')", *NEUTRE],
        "main_exclusive": ["01090"],
        "declencher": ["Puzzle.Attack('sk128')"],
        "verifier": "ss_etat",
        "attendu": {"statuts": [["01001b", "Confused"]], "statuts_absents": [["sk117", "Tough"], ["01001b", "Stunned"]], "defausse_ids": ["01089"]},
    },
    {
        "nom": "[super_skrull] sk128 Mt'nox — attaque non defendue, carte wild (Power of Justice) : TOUT (Tough, etourdi, desoriente)",
        "pourquoi": "Deck du joueur = The Power of Justice (G, wild) : les trois lignes s'appliquent",
        "scenario": "sk_super_skrull",
        "heros": "spider_man",
        "mise_en_place": [RAZ, "Puzzle.PutIntoPlay('sk128')", "Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01091', '01062')", *NEUTRE],
        "main_exclusive": ["01090"],
        "declencher": ["Puzzle.Attack('sk128')"],
        "verifier": "ss_etat",
        "attendu": {"statuts": [["sk117", "Tough"], ["01001b", "Stunned"], ["01001b", "Confused"]], "defausse_ids": ["01062"]},
    },
    {
        "nom": "[super_skrull] sk128 Mt'nox — CONTRE-CAS attaque DEFENDUE par un allie : rien n'est defausse, aucun statut",
        "pourquoi": "« undefended attack » : Black Cat defend ; le deck du joueur (Strength) reste intact",
        "scenario": "sk_super_skrull",
        "heros": "spider_man",
        "mise_en_place": [RAZ, "Puzzle.PutIntoPlay('sk128')", "Puzzle.PutIntoPlay('01002')", "Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01091', '01090')", *NEUTRE],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Attack('sk128', '01002')"],
        "verifier": "ss_etat",
        "attendu": {"statuts_absents": [["sk117", "Tough"], ["01001b", "Stunned"], ["01001b", "Confused"]], "taille_deck_joueur": 2},
    },
    {
        "nom": "[super_skrull] sk129 Praxagora — ses attaques gagnent Dechainement : l'exces (2) sur Black Cat vaincue va a l'identite",
        "pourquoi": "`UnitAttackGainKeyword('This', overkill=True)` : Praxagora ATK 3 contre Black Cat (1 PV restant) : 2 d'exces",
        "scenario": "sk_super_skrull",
        "heros": "spider_man",
        "mise_en_place": [RAZ, "Puzzle.PutIntoPlay('sk129')", "Puzzle.PutIntoPlay('01002')", "Puzzle.Damage('01002', 1)", *NEUTRE],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Attack('sk129', '01002')"],
        "verifier": "ss_etat",
        "attendu": {"hors_jeu": ["01002"], "degats_identite": 2},
    },
    {
        "nom": "[super_skrull] sk130 R'kin — vaincu : on defausse jusqu'a un attachement, qui est revele (ici un Invisible Forcefield)",
        "pourquoi": ("`WhenUnitBeDefeated(WhenDefeated)` + `Worlds.DiscardEncounterCardsUntil(Attachment)` + `Reveal` : deck [sk101, sk126, sk101] ; "
                     "sk101 defaussee, sk126 defaussee puis revelee, elle s'attache au mechant"),
        "scenario": "sk_super_skrull",
        "heros": "spider_man",
        "mise_en_place": [RAZ, "Puzzle.PutIntoPlay('sk130')", "Puzzle.ChangeForm('01001b')",
                          "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('sk101', 'sk126', 'sk101')"],
        "main_exclusive": ["01088"],
        "cibles": ["sk130"],
        "declencher": ["Puzzle.Attack('01001a')"],
        "verifier": "ss_etat",
        "attendu": {"hors_jeu": ["sk130"], "attaches": [["sk117", "sk126"]], "defausse_rencontre": ["sk101"]},
    },
    {
        "nom": "[super_skrull] sk131 Galactic Council Membership — un joueur attaque le Super-Skrull : 1 menace sur le complot principal",
        "pourquoi": "`AfterUnitAttackEnd(ForcedResponse, Hero|Ally, against_who=Super-Skrull)` : Spider-Man frappe le mechant, sk120b passe de 0 a 1",
        "scenario": "sk_super_skrull",
        "heros": "spider_man",
        "mise_en_place": [RAZ, "Puzzle.PutIntoPlay('sk131')", "Puzzle.ChangeForm('01001b')", *NEUTRE],
        "main_exclusive": ["01088"],
        "cibles": ["sk117"],
        "declencher": ["Puzzle.Attack('01001a')"],
        "verifier": "ss_etat",
        "attendu": {"menace": [["sk120b", 1]], "degats": [["sk117", 2]]},
    },
    {
        "nom": "[super_skrull] sk131 Galactic Council Membership — CONTRE-CAS : l'attaque vise un sbire, pas le Super-Skrull : aucune menace",
        "pourquoi": "« attacks Super-Skrull » : Spider-Man attaque Praxagora",
        "scenario": "sk_super_skrull",
        "heros": "spider_man",
        "mise_en_place": [RAZ, "Puzzle.PutIntoPlay('sk131')", "Puzzle.PutIntoPlay('sk129')", "Puzzle.ChangeForm('01001b')", *NEUTRE],
        "main_exclusive": ["01088"],
        "cibles": ["sk129"],
        "declencher": ["Puzzle.Attack('01001a')"],
        "verifier": "ss_etat",
        "attendu": {"menace": [["sk120b", 0]], "degats": [["sk129", 2]]},
    },
    {
        "nom": "[super_skrull] sk132 Skrull Warlords — un allie entre en jeu sous le controle du joueur : le mechant recoit une carte boost face cachee",
        "pourquoi": "`AfterCardEnterPlay(ForcedResponse, CardFinder(), ...)` + `Faces.GiveFacedownBoostCards` : Black Cat jouee",
        "scenario": "sk_super_skrull",
        "heros": "spider_man",
        "mise_en_place": [RAZ, "Puzzle.PutIntoPlay('sk132')", *NEUTRE],
        "main_exclusive": ["01002", "01088", "01089"],
        "jouer": ["01002"],
        "declencher": [],
        "verifier": "ss_etat",
        "attendu": {"en_jeu": ["01002"], "boost_du_mechant": 1},
    },
    {
        "nom": "[super_skrull] sk132 Skrull Warlords — TEMOIN : une carte de RENCONTRE qui entre en jeu ne donne aucune carte boost",
        "pourquoi": "« under any player's control » : Praxagora (ennemi) arrive, pas de boost",
        "scenario": "sk_super_skrull",
        "heros": "spider_man",
        "mise_en_place": [RAZ, "Puzzle.PutIntoPlay('sk132')", *NEUTRE],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.PutIntoPlay('sk129')"],
        "verifier": "ss_etat",
        "attendu": {"en_jeu": ["sk129"], "boost_du_mechant": 0},
    },
    {
        "nom": "[super_skrull] sk133 Hypnotic Gaze — 2 icones physiques defaussees : un personnage est etourdi par ressource (heros et allie)",
        "pourquoi": ("Deck du joueur = Strength (RR) + Energy (YY) : 2 ressources physiques -> `AskChooseFace` deux fois, "
                     "Spider-Man (identite) et Black Cat sont tous deux etourdis ; Energy ne compte pas"),
        "scenario": "sk_super_skrull",
        "heros": "spider_man",
        "mise_en_place": [RAZ, "Puzzle.PutIntoPlay('01002')", "Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01091', '01091', '01088', '01090')", *NEUTRE],
        "main_exclusive": ["01093"],
        "declencher": ["Puzzle.Reveal('sk133')"],
        "verifier": "ss_etat",
        "attendu": {"statuts": [["01001b", "Stunned"], ["01002", "Stunned"]], "statuts_absents": [["01001b", "Confused"], ["01002", "Confused"]],
                    "defausse_ids": ["01088", "01090"]},
    },
    {
        "nom": "[super_skrull] sk133 Hypnotic Gaze — 2 icones mentales defaussees : un personnage est desoriente par ressource",
        "pourquoi": "Deck du joueur = Genius (BB) + Energy (YY) : 2 ressources mentales -> Spider-Man et Black Cat desorientes, personne d'etourdi",
        "scenario": "sk_super_skrull",
        "heros": "spider_man",
        "mise_en_place": [RAZ, "Puzzle.PutIntoPlay('01002')", "Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01091', '01091', '01088', '01089')", *NEUTRE],
        "main_exclusive": ["01093"],
        "declencher": ["Puzzle.Reveal('sk133')"],
        "verifier": "ss_etat",
        "attendu": {"statuts": [["01001b", "Confused"], ["01002", "Confused"]], "statuts_absents": [["01001b", "Stunned"], ["01002", "Stunned"]]},
    },
    {
        "nom": "[super_skrull] sk133 Hypnotic Gaze — CONTRE-CAS energie + wild : aucune ressource physique ni mentale, aucun effet",
        "pourquoi": "Deck du joueur = Energy (YY) + Power of Justice (G) : le wild n'est ni physique ni mental (lecture litterale, voir questions)",
        "scenario": "sk_super_skrull",
        "heros": "spider_man",
        "mise_en_place": [RAZ, "Puzzle.PutIntoPlay('01002')", "Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01091', '01091', '01062', '01088')", *NEUTRE],
        "main_exclusive": ["01093"],
        "declencher": ["Puzzle.Reveal('sk133')"],
        "verifier": "ss_etat",
        "attendu": {"statuts_absents": [["01001b", "Stunned"], ["01001b", "Confused"], ["01002", "Stunned"], ["01002", "Confused"]],
                    "defausse_ids": ["01088", "01062"]},
    },
    {
        "nom": "[super_skrull] sk134 Power Multiplying — revelee : un pouvoir de plus est revele (pas de surge)",
        "pourquoi": "`RevelerSuperpouvoir` : paquet de 3 -> 2 ; 1 pouvoir attache",
        "scenario": "sk_super_skrull",
        "heros": "spider_man",
        "mise_en_place": [RAZ, *NEUTRE],
        "declencher": ["Puzzle.Reveal('sk134')"],
        "verifier": "ss_etat",
        "attendu": {"pouvoirs_sur_mechant": 1, "paquet": 2, "cartes_distribuees": 0},
    },
    {
        "nom": "[super_skrull] sk134 Power Multiplying — paquet SUPERPOWER vide : « If you cannot, this card gains surge »",
        "pourquoi": "Les trois pouvoirs restants sont deja attaches : rien a reveler, surge : la carte du dessus (sk101) est revelee dans la foulee",
        "scenario": "sk_super_skrull",
        "heros": "spider_man",
        "mise_en_place": [RAZ, "Puzzle.Reveal('sk123')", "Puzzle.Reveal('sk124')", "Puzzle.Reveal('sk125')", *NEUTRE],
        "surge_hors_phase": 1,
        "declencher": ["Puzzle.Reveal('sk134')"],
        "verifier": "ss_etat",
        "attendu": {"pouvoirs_sur_mechant": 3, "paquet": 0, "en_jeu": ["sk101"]},
    },
    {
        "nom": "[super_skrull] sk134 Power Multiplying — Boost : +1 icone par pouvoir attache (2 pouvoirs : ATK 2 + 2 icones = 4 degats)",
        "pourquoi": ("`message.GainBoostIcon(n)` dans `WhenCardBecomeBoost` : Flexibility et Invisibility attachees (ni l'un ni l'autre ne change l'ATK) ; "
                     "le Super-Skrull attaque Spider-Man (heros) avec sk134 en boost"),
        "scenario": "sk_super_skrull",
        "heros": "spider_man",
        "mise_en_place": [RAZ, "Puzzle.Reveal('sk122')", "Puzzle.Reveal('sk123')", "Puzzle.ChangeForm('01001b')", *NEUTRE],
        "main_exclusive": ["01088"],
        "passer_sur_option": "Defense",
        "declencher": ["Puzzle.Boost('sk134')"],
        "verifier": "ss_etat",
        "attendu": {"degats_identite": 4},
    },
    {
        "nom": "[super_skrull] sk134 Power Multiplying — Boost TEMOIN sans pouvoir attache : aucune icone (ATK 2 = 2 degats)",
        "pourquoi": "Meme boost, aucun pouvoir attache : « for each SUPERPOWER attachment attached to Super-Skrull » = 0",
        "scenario": "sk_super_skrull",
        "heros": "spider_man",
        "mise_en_place": [RAZ, "Puzzle.ChangeForm('01001b')", *NEUTRE],
        "main_exclusive": ["01088"],
        "passer_sur_option": "Defense",
        "declencher": ["Puzzle.Boost('sk134')"],
        "verifier": "ss_etat",
        "attendu": {"degats_identite": 2},
    },
    {
        "nom": "[super_skrull] sk135 Villain's Versatility — Pyrokinesis attache : 3 degats indirects au joueur",
        "pourquoi": "Une branche par pouvoir attache ; Pyrokinesis -> `TakeIndirectDamage(3)` sur l'identite (alter ego Peter Parker)",
        "scenario": "sk_super_skrull",
        "heros": "spider_man",
        "mise_en_place": [RAZ, "Puzzle.Reveal('sk124')", *NEUTRE],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Reveal('sk135')"],
        "verifier": "ss_etat",
        "attendu": {"degats_identite": 3, "statuts_absents": [["sk117", "Tough"]], "menace": [["sk120b", 0]]},
    },
    {
        "nom": "[super_skrull] sk135 Villain's Versatility — Rock Mimicry attache : le Super-Skrull recoit une carte Tough",
        "pourquoi": "Rock Mimicry -> `Faces.GiveStatus([mechant], 'Tough')` ; aucun autre pouvoir, aucun autre effet",
        "scenario": "sk_super_skrull",
        "heros": "spider_man",
        "mise_en_place": [RAZ, "Puzzle.Reveal('sk125')", *NEUTRE],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Reveal('sk135')"],
        "verifier": "ss_etat",
        "attendu": {"statuts": [["sk117", "Tough"]], "degats_identite": 0, "menace": [["sk120b", 0]]},
    },
    {
        "nom": "[super_skrull] sk135 Villain's Versatility — Flexibility attache : le joueur defausse 1 carte de sa main",
        "pourquoi": "Flexibility -> `DiscardHandCards((1, 1))` : main de 3 cartes, il en reste 2",
        "scenario": "sk_super_skrull",
        "heros": "spider_man",
        "mise_en_place": [RAZ, "Puzzle.Reveal('sk122')", *NEUTRE],
        "main_exclusive": ["01088", "01089", "01090"],
        "declencher": ["Puzzle.Reveal('sk135')"],
        "verifier": "ss_etat",
        "attendu": {"taille_main": 2, "statuts_absents": [["sk117", "Tough"]], "degats_identite": 0, "menace": [["sk120b", 0]]},
    },
    {
        "nom": "[super_skrull] sk135 Villain's Versatility — Invisibility attache : 2 menaces sur le complot principal",
        "pourquoi": "Invisibility -> `PlaceThreatOnSchemes('MainScheme', 2)` : sk120b passe de 0 a 2",
        "scenario": "sk_super_skrull",
        "heros": "spider_man",
        "mise_en_place": [RAZ, "Puzzle.Reveal('sk123')", *NEUTRE],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Reveal('sk135')"],
        "verifier": "ss_etat",
        "attendu": {"menace": [["sk120b", 2]], "degats_identite": 0, "statuts_absents": [["sk117", "Tough"]]},
    },
    {
        "nom": "[super_skrull] sk135 Villain's Versatility — deux pouvoirs (Pyrokinesis + Invisibility) : les deux lignes s'appliquent",
        "pourquoi": "Chaque ligne est independante : 3 degats indirects ET 2 menaces",
        "scenario": "sk_super_skrull",
        "heros": "spider_man",
        "mise_en_place": [RAZ, "Puzzle.Reveal('sk124')", "Puzzle.Reveal('sk123')", *NEUTRE],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Reveal('sk135')"],
        "verifier": "ss_etat",
        "attendu": {"degats_identite": 3, "menace": [["sk120b", 2]]},
    },
    {
        "nom": "[super_skrull] sk135 Villain's Versatility — CONTRE-CAS aucun pouvoir attache : la carte ne fait rien",
        "pourquoi": "Aucune ligne de la liste ne s'applique",
        "scenario": "sk_super_skrull",
        "heros": "spider_man",
        "mise_en_place": [RAZ, *NEUTRE],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Reveal('sk135')"],
        "verifier": "ss_etat",
        "attendu": {"degats_identite": 0, "menace": [["sk120b", 0]], "statuts_absents": [["sk117", "Tough"]], "taille_main": 1},
    },

    # ===================================================================
    # Set modulaire Kree-Skrull War (sk136-140)
    # ===================================================================
    {
        "nom": "[super_skrull] sk136 Bel-Dann — revele : Raksor est cherche dans le deck et mis en jeu engage avec le joueur",
        "pourquoi": "`Search.EncounterCard(include_discard_pile=True, name='Raksor')` + `PutIntoPlay(joueur)` ; Raksor n'est pas REVELE (pas de boucle)",
        "scenario": "sk_super_skrull",
        "heros": "spider_man",
        "mise_en_place": [RAZ, "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('sk137', 'sk101', 'sk136')"],
        "declencher": ["Puzzle.Reveal('sk136')"],
        "verifier": "ss_etat",
        "attendu": {"en_jeu": ["sk136", "sk137"], "engages": [["sk137", 0]], "menace": [["sk138", 3]]},
    },
    {
        "nom": "[super_skrull] sk136 Bel-Dann — Raksor est cherche aussi dans la DEFAUSSE rencontre",
        "pourquoi": "« search the encounter deck AND discard pile » : sk137 est dans la defausse, pas dans le deck",
        "scenario": "sk_super_skrull",
        "heros": "spider_man",
        "mise_en_place": [RAZ, "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('sk101', 'sk136')", "Puzzle.CreateEncounterDiscardPile('sk137')"],
        "declencher": ["Puzzle.Reveal('sk136')"],
        "verifier": "ss_etat",
        "attendu": {"en_jeu": ["sk136", "sk137"], "engages": [["sk137", 0]]},
    },
    {
        "nom": "[super_skrull] sk137 Raksor — revele : Bel-Dann est cherche et mis en jeu engage avec le joueur",
        "pourquoi": "Miroir de sk136 : `MettreEnJeuEngage(joueur, 'Bel-Dann')`",
        "scenario": "sk_super_skrull",
        "heros": "spider_man",
        "mise_en_place": [RAZ, "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('sk136', 'sk101', 'sk137')"],
        "declencher": ["Puzzle.Reveal('sk137')"],
        "verifier": "ss_etat",
        "attendu": {"en_jeu": ["sk137", "sk136"], "engages": [["sk136", 0]], "menace": [["sk138", 3]]},
    },
    {
        "nom": "[super_skrull] sk138 Earth Involvement — Permanent + Setup : en jeu des la mise en place, menace 1 par joueur, crise tant qu'il y a de la menace",
        "pourquoi": "Insert p. 10 : « it always begins the game in play and cannot leave play » ; crise conditionnelle (ThisGainKeyword + OnEvent.Threat)",
        "scenario": "sk_super_skrull",
        "heros": "spider_man",
        "mise_en_place": [],
        "declencher": [],
        "verifier": "ss_etat",
        "attendu": {"en_jeu": ["sk138"], "menace": [["sk138", 1]], "attributs_carte": [["sk138", "crisis", 1]]},
    },
    {
        "nom": "[super_skrull] sk138 Earth Involvement — menace contree jusqu'a 0 : elle RESTE en jeu (Permanent) et perd la crise",
        "pourquoi": "Spider-Man (THW 1) contre sa derniere menace : pas de defausse (Permanent), plus d'icone de crise",
        "scenario": "sk_super_skrull",
        "heros": "spider_man",
        "mise_en_place": [RAZ, "Puzzle.ChangeForm('01001b')", *NEUTRE],
        "main_exclusive": ["01088"],
        "cibles": ["sk138"],
        "declencher": ["Puzzle.Thwart('01001a')"],
        "verifier": "ss_etat",
        "attendu": {"en_jeu": ["sk138"], "menace": [["sk138", 0]], "attributs_carte": [["sk138", "crisis", 0]]},
    },
    {
        "nom": "[super_skrull] sk138 Earth Involvement — Reponse obligatoire : une carte du set Kree-Skrull War revelee : +2 menaces ici",
        "pourquoi": "`AfterPlayerRevealCard(ForcedResponse, 'AnyPlayer', set == Kree-Skrull War)` : Imperial Kree Army (carte de dessus sans icone Y) revelee : 1 + 2",
        "scenario": "sk_super_skrull",
        "heros": "spider_man",
        "mise_en_place": [RAZ, *NEUTRE],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Reveal('sk139')"],
        "verifier": "ss_etat",
        "attendu": {"menace": [["sk138", 3]]},
    },
    {
        "nom": "[super_skrull] sk138 Earth Involvement — CONTRE-CAS une carte d'un AUTRE set (Super-Skrull) revelee : pas de menace",
        "pourquoi": "« belongs to the Kree-Skrull War encounter set » : Villain's Versatility (sk135) ne declenche rien",
        "scenario": "sk_super_skrull",
        "heros": "spider_man",
        "mise_en_place": [RAZ, *NEUTRE],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Reveal('sk135')"],
        "verifier": "ss_etat",
        "attendu": {"menace": [["sk138", 1]]},
    },
    {
        "nom": "[super_skrull] sk139 Imperial Kree Army — revelee : defausse le dessus (1 icone Y) : 1 degat a chaque personnage controle",
        "pourquoi": "`CountTotalBoostIcons` sur la carte defaussee (Hypnotic Gaze, 1 icone) : Spider-Man (identite) et Black Cat prennent 1",
        "scenario": "sk_super_skrull",
        "heros": "spider_man",
        "mise_en_place": [RAZ, "Puzzle.PutIntoPlay('01002', under_control=True)", "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('sk101', 'sk133')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Reveal('sk139')"],
        "verifier": "ss_etat",
        "attendu": {"degats_identite": 1, "degats": [["01002", 1]], "defausse_rencontre": ["sk133"]},
    },
    {
        "nom": "[super_skrull] sk139 Imperial Kree Army — 2 icones Y defaussees : 2 degats a chaque personnage (pas 2 repartis)",
        "pourquoi": "Bel-Dann (2 icones) defausse : « 1 damage to EACH character FOR EACH icon » = 2 chacun ; identite seule",
        "scenario": "sk_super_skrull",
        "heros": "spider_man",
        "mise_en_place": [RAZ, "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('sk101', 'sk136')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Reveal('sk139')"],
        "verifier": "ss_etat",
        "attendu": {"degats_identite": 2, "defausse_rencontre": ["sk136"]},
    },
    {
        "nom": "[super_skrull] sk139 Imperial Kree Army — CONTRE-CAS dessus sans icone Y : aucun degat",
        "pourquoi": "Seeking a Suitable World (sk101, aucune icone) defaussee",
        "scenario": "sk_super_skrull",
        "heros": "spider_man",
        "mise_en_place": [RAZ, "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('sk101', 'sk101')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Reveal('sk139')"],
        "verifier": "ss_etat",
        "attendu": {"degats_identite": 0},
    },
    {
        "nom": "[super_skrull] sk139 Imperial Kree Army — Boost : +2 menaces sur Earth Involvement (sans etre « revelee »)",
        "pourquoi": "`Puzzle.Boost` : la carte est retournee en boost : sk138 passe de 1 a 3 (pas 5 : le boost n'est pas une revelation)",
        "scenario": "sk_super_skrull",
        "heros": "spider_man",
        "mise_en_place": [RAZ, "Puzzle.ChangeForm('01001b')", *NEUTRE],
        "main_exclusive": ["01088"],
        "passer_sur_option": "Defense",
        "declencher": ["Puzzle.Boost('sk139')"],
        "verifier": "ss_etat",
        "attendu": {"menace": [["sk138", 3]]},
    },
    {
        "nom": "[super_skrull] sk140 Skrull Imperial Fleet — revelee : 1 menace par icone Y defaussee sur CHAQUE complot (principal et annexes)",
        "pourquoi": "Dessus = Hypnotic Gaze (1 icone) : sk120b +1, sk101 (3) +1, Earth Involvement 1 +1 (+2 de sa Reponse obligatoire)",
        "scenario": "sk_super_skrull",
        "heros": "spider_man",
        "mise_en_place": [RAZ, "Puzzle.PutIntoPlay('sk101')", "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('sk101', 'sk133')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Reveal('sk140')"],
        "verifier": "ss_etat",
        "attendu": {"menace": [["sk120b", 1], ["sk101", 4], ["sk138", 4]], "defausse_rencontre": ["sk133"]},
    },
    {
        "nom": "[super_skrull] sk140 Skrull Imperial Fleet — Boost : +2 menaces sur Earth Involvement",
        "pourquoi": "Meme boost que sk139 : sk138 de 1 a 3",
        "scenario": "sk_super_skrull",
        "heros": "spider_man",
        "mise_en_place": [RAZ, "Puzzle.ChangeForm('01001b')", *NEUTRE],
        "main_exclusive": ["01088"],
        "passer_sur_option": "Defense",
        "declencher": ["Puzzle.Boost('sk140')"],
        "verifier": "ss_etat",
        "attendu": {"menace": [["sk138", 3]]},
    },
]

VERIFICATIONS = r'''
def _ss_paquet(monde):
    return monde.scenario_decks.get("SuperpowerDeck")

def _ss_ids(faces):
    return [getattr(f.paper, "card_id", None) for f in faces]

def _ss_pouvoirs_sur_mechant(monde):
    from game.operate.worlds import Worlds
    mechant = Worlds.GetAllVillains(monde)[0]
    return [a for a in mechant.GetAttachedAttachments() if a.HasTrait("SUPERPOWER")]

_SS_PROPRES = {"defausse_ids", "paquet", "defausse_paquet", "dans_paquet", "dans_defausse_paquet", "pouvoirs_sur_mechant",
               "pouvoirs_ids", "cartes_distribuees", "boost_du_mechant", "engages", "pv_max_mechant"}

def ss_etat(monde, aides):
    """Etat du paquet SUPERPOWER et des pouvoirs attaches au Super-Skrull, puis delegation a etat_attendu.
    Cles propres : paquet / defausse_paquet (tailles), dans_paquet / dans_defausse_paquet (ids), pouvoirs_sur_mechant
    (nombre), pouvoirs_ids (liste exacte sans ordre), cartes_distribuees (face cachee au joueur 0),
    boost_du_mechant (nombre de cartes boost du mechant), engages ([[card_id, rang du joueur]])."""
    attendu = aides["cas"].get("attendu") or {}
    soucis = []
    paquet = _ss_paquet(monde)
    if any(k in attendu for k in ("paquet", "defausse_paquet", "dans_paquet", "dans_defausse_paquet")):
        if paquet is None or not paquet.initialize:
            soucis.append("le paquet SUPERPOWER n'existe pas")
        else:
            if "paquet" in attendu and paquet.deck.GetSize() != attendu["paquet"]:
                soucis.append(f"paquet = {paquet.deck.GetSize()} carte(s) {_ss_ids(paquet.deck.GetAll())} (attendu {attendu['paquet']})")
            if "defausse_paquet" in attendu and paquet.discard_pile.GetSize() != attendu["defausse_paquet"]:
                soucis.append(f"defausse du paquet = {paquet.discard_pile.GetSize()} {_ss_ids(paquet.discard_pile.GetAll())} (attendu {attendu['defausse_paquet']})")
            for i in attendu.get("dans_paquet") or []:
                if i not in _ss_ids(paquet.deck.GetAll()):
                    soucis.append(f"{i} absent du paquet {_ss_ids(paquet.deck.GetAll())}")
            for i in attendu.get("dans_defausse_paquet") or []:
                if i not in _ss_ids(paquet.discard_pile.GetAll()):
                    soucis.append(f"{i} absent de la defausse du paquet {_ss_ids(paquet.discard_pile.GetAll())}")
    portes = _ss_ids(_ss_pouvoirs_sur_mechant(monde))
    if "pouvoirs_sur_mechant" in attendu and len(portes) != attendu["pouvoirs_sur_mechant"]:
        soucis.append(f"{len(portes)} pouvoir(s) sur le Super-Skrull {portes} (attendu {attendu['pouvoirs_sur_mechant']})")
    if "pouvoirs_ids" in attendu and sorted(portes) != sorted(attendu["pouvoirs_ids"]):
        soucis.append(f"pouvoirs sur le Super-Skrull {sorted(portes)} (attendu {sorted(attendu['pouvoirs_ids'])})")
    if "defausse_ids" in attendu:
        # `Get()` n'enumere pas les cartes FACE CACHEE : une carte defaussee du dessus du deck y reste cachee.
        vues = _ss_ids(monde.players[0].discard_pile.GetAll())
        for i in attendu["defausse_ids"]:
            if i not in vues:
                ou = [str(getattr(o.face.card, "area", None)) for o in monde.object_manager.card_dict.values()
                      if o.face is not None and getattr(o.face.paper, "card_id", None) == i]
                soucis.append(f"{i} n'est pas dans la defausse du joueur {vues} (la carte est en : {ou} ; deck = {_ss_ids(monde.players[0].player_deck.GetAll())} ; main = {_ss_ids(monde.players[0].hand_cards.GetAll())})")
    if "cartes_distribuees" in attendu:
        n = len(list(monde.players[0].dealt_encounter_cards.Get(True)))
        if n != attendu["cartes_distribuees"]:
            soucis.append(f"{n} carte(s) rencontre distribuee(s) face cachee au joueur (attendu {attendu['cartes_distribuees']})")
    if "boost_du_mechant" in attendu:
        from game.operate.worlds import Worlds
        mechant = Worlds.GetAllVillains(monde)[0]
        pile = [getattr(f.paper, "card_id", "?") for f in mechant.components.boostable.GetDeck().Get(True)]
        if len(pile) != attendu["boost_du_mechant"]:
            soucis.append(f"pile de boost du mechant = {pile} (attendu {attendu['boost_du_mechant']} carte(s))")
    for card_id, rang in attendu.get("engages") or []:
        face = aides["par_id"](monde, card_id)
        if face is None:
            soucis.append(f"{card_id} introuvable en jeu (engage)")
        elif getattr(face, "engaged_player", None) is not monde.players[rang]:
            soucis.append(f"{card_id} n'est pas engage avec le joueur {rang} (engage avec {getattr(face, 'engaged_player', None)})")
    reste = {k: v for k, v in attendu.items() if k not in _SS_PROPRES}
    if reste:
        inconnues = sorted(set(reste) - CLES_ETAT_ATTENDU)
        if inconnues:
            return False, f"cle(s) inconnue(s) : {inconnues}"
        sauve = aides["cas"]["attendu"]
        aides["cas"]["attendu"] = reste
        try:
            ok, msg = etat_attendu(monde, aides)
        finally:
            aides["cas"]["attendu"] = sauve
        if not ok:
            soucis.append(msg)
    if soucis:
        return False, " ; ".join(soucis)
    return True, f"etat conforme (pouvoirs sur le mechant : {portes})"
'''
