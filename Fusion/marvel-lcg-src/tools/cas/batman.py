# Cas test_capacites du heros BATMAN (Bruce Wayne, ES, prefixe `bm`) : noms prefixes « [bm] » puis le card_id (substituer_pack.py filtre dessus).
#
# Rappels de montage :
#  - le deck `batman` demarre en ALTER EGO (bm001b) ; `Puzzle.ChangeToFace('bm001b', 'bm001a')` la passe en HEROS ;
#  - le deck de dissuasion est `additional_deck` du joueur : `Puzzle.SetDeterrenceDeck(...)` le remplace par EXACTEMENT les cartes voulues (le pilote
#    ne peut pas choisir lesquelles des 15 il retient au Setup) ; sa defausse est `additional_discard_pile` ;
#  - Rhino 01094 est le vilain, 01097b son complot principal, 01101 Hydra Mercenary un sbire (3 PV, Guard), 01121 Weapons Runner un sbire
#    neutre (2 PV) ; 01098 : remplissage neutre du deck rencontre (aucun boost, aucun surge) ;
#  - ressources : 01088 Energy = YY, 01089 Genius = BB, 01090 Strength = RR.
SC = "rhino"
HEROS = "Puzzle.ChangeToFace('bm001b', 'bm001a')"
CIVIL = "Puzzle.ChangeToFace('bm001a', 'bm001b')"
VILAIN = "01094"
COMPLOT = "01097b"
SBIRE = "01101"
SBIRE_NEUTRE = "01121"
SANS_BOOST = ["Puzzle.EmptyEncounterDeck()",
              "Puzzle.CreateEncounterDeck('01098', '01098', '01098', '01098', '01098', '01098', '01098', '01098')"]


def en_jeu(*ids):
    return [f"Puzzle.PutIntoPlay('{i}', under_control=True)" for i in ids]


def dissuasion(*ids):
    return [f"Puzzle.SetDeterrenceDeck({', '.join(repr(i) for i in ids)})"]


def reveler(carte):
    """Le montage pour reveler la VRAIE carte de dissuasion : dans le deck de dissuasion, puis dans le deck de rencontre."""
    return [f"Puzzle.SetDeterrenceDeck('{carte}')", f"Puzzle.ShuffleDeterrence('{carte}')"]


def _c(nom, pourquoi, mise, declencher, attendu, **cle):
    mise = cle.pop("remplissage", SANS_BOOST) + list(mise)
    cas = {"nom": "[bm] " + nom, "pourquoi": pourquoi, "scenario": cle.pop("scenario", SC),
           "heros": cle.pop("heros", "batman"), "mise_en_place": mise, "declencher": declencher,
           "verifier": cle.pop("verifier", "bm_etat"), "attendu": attendu}
    cas.setdefault("regles", ["v16_all", "v18_all"])
    cas.update(cle)
    return cas


CAS = [
    # ============================================================ bm001a / bm001b : identite
    _c("bm001a Batman : valeurs imprimees PV 11, ATK 2, THW 2, DEF 2, HS 5, BAT FAMILY JUSTICE LEAGUE",
       "nombres texte <-> code (scan) : HAND SIZE 5 / HIT POINTS 11, THW 2 ATK 2 DEF 2",
       [HEROS], [], {"pv_max": [["bm001a", 11]], "traits": ["BAT FAMILY", "JUSTICE LEAGUE"],
                     "bm_stats": {"attack": 2, "thwart": 2, "defense": 2, "hand_size": 5}}),
    _c("bm001b Bruce Wayne : valeurs imprimees PV 11, REC 3, HS 6, BILLIONAIRE GENIUS",
       "nombres texte <-> code (scan) : HAND SIZE 6 / HIT POINTS 11 / REC 3",
       [], [], {"pv_max": [["bm001b", 11]], "traits": ["BILLIONAIRE", "GENIUS"], "bm_stats": {"recover": 3, "hand_size": 6}}),
    _c("bm001b Setup : le deck de dissuasion compte 8 cartes de dissuasion, la defausse de dissuasion est vide",
       "« the player selects 8 of the 15 deterrence cards to form the deterrence deck » : 15 mises de cote, 8 retenues, 7 retirees du jeu",
       [], [], {"bm_taille_deck": 8, "bm_defausse": [], "bm_nb_dissuasion_total": 8}),

    # ============================================================ bm001a : melanger une dissuasion
    _c("bm001a Hero Response : apres une attaque, une carte de dissuasion CHOISIE passe du deck de dissuasion au deck de rencontre",
       "« After Batman attacks or thwarts, choose a deterrence card and shuffle it into the encounter deck »",
       [HEROS, *en_jeu(SBIRE_NEUTRE), *dissuasion("bm018", "bm019")], ["Puzzle.Attack('bm001a')"],
       {"bm_taille_deck": 1, "bm_rencontre_nb": 1}, accepter_choix=True),
    _c("bm001a Hero Response : apres un contre, une carte de dissuasion est melangee dans le deck de rencontre",
       "« ... attacks or thwarts »",
       [HEROS, "Puzzle.SetThreat('01097b', 3)", *dissuasion("bm018", "bm019")], ["Puzzle.Thwart('bm001a')"],
       {"bm_taille_deck": 1, "bm_rencontre_nb": 1}, accepter_choix=True),
    _c("bm001a Hero Response : au plus 3 melanges par round (3 attaques, 4e sans effet)",
       "« You are allowed to shuffle a maximum of 3 deterrence cards into the encounter deck in a round »",
       [HEROS, *dissuasion("bm018", "bm018", "bm019", "bm019", "bm020")],
       ["Puzzle.Attack('bm001a')", "Puzzle.Ready('bm001a')", "Puzzle.Attack('bm001a')", "Puzzle.Ready('bm001a')",
        "Puzzle.Attack('bm001a')", "Puzzle.Ready('bm001a')", "Puzzle.Attack('bm001a')"],
       {"bm_taille_deck": 2, "bm_rencontre_nb": 3}, accepter_choix=True),

    # ============================================================ cartes de dissuasion : When Revealed
    _c("bm018 Sudden Strike : Batman en jeu, 3 degats a un ennemi, surge, retour dans la defausse de dissuasion",
       "« If Batman is in play, Batman deals 3 damage to an enemy of your choice. This card gains surge. » Carte RESOLUE : defausse de dissuasion",
       [HEROS, *reveler("bm018")], ["Puzzle.Reveal('bm018')"],
       {"degats": [[VILAIN, 3]], "bm_defausse": ["bm018"], "bm_taille_deck": 0}, accepter_choix=True, cibles=[VILAIN]),
    _c("bm018 Sudden Strike : Bruce Wayne (alter ego) ne frappe pas (« if Batman is in play »)",
       "Batman n'est pas en jeu en forme alter ego",
       [*reveler("bm018")], ["Puzzle.Reveal('bm018')"],
       {"degats": [[VILAIN, 0]], "bm_defausse": ["bm018"]}, accepter_choix=True),
    _c("bm019 Smoke Cloud : When Revealed, desoriente un ennemi",
       "« Confuse an enemy. This card gains surge. »",
       [HEROS, *en_jeu(SBIRE_NEUTRE), *reveler("bm019")], ["Puzzle.Reveal('bm019')"],
       {"statuts": [[SBIRE_NEUTRE, "Confused"]], "bm_defausse": ["bm019"]}, accepter_choix=True, cibles=[SBIRE_NEUTRE]),
    _c("bm021 Vigilantism : When Revealed, Batman retire 2 menaces au total",
       "« Batman removes 2 threat among schemes, divided as you choose »",
       [HEROS, "Puzzle.SetThreat('01097b', 5)", *reveler("bm021")], ["Puzzle.Reveal('bm021')"],
       {"menace": [["01097b", 3]], "bm_defausse": ["bm021"]}, accepter_choix=True),
    _c("bm022 Shadow of the Bat : When Revealed, pioche une carte (Batman en jeu)",
       "« choose one: draw a card or ready a card »",
       [HEROS, *reveler("bm022")], ["Puzzle.Reveal('bm022')"],
       {"bm_defausse": ["bm022"], "taille_main": 2}, accepter_choix=True, main_exclusive=["01090"]),
    _c("bm001b Actually... a Trillionaire : Grapple Gun (ITEM TECH, cout 3) se paie avec UNE ressource YY (cout reduit a 2)",
       "« Reduce the cost of the next ... [[VEHICLE]] ... card played this round by 1 »",
       [], ["Puzzle.Action('bm001b', 'Action')"], {"en_jeu": ["bm010"]},
       main_exclusive=["bm010", "01088"], payer_avec=["01088"], jouer=["bm010"]),
    _c("bm001b Actually... a Trillionaire : TEMOIN D'EPUISEMENT, une 2e Action dans le round est refusee (limite une fois par round)",
       "« (Limit once per round.) » : `declencher_tolerant` autorise la tentative ; la reduction reste de 1 (Grapple Gun payee par UNE YY)",
       [], ["Puzzle.Action('bm001b', 'Action')"], {"en_jeu": ["bm010"]},
       main_exclusive=["bm010", "01088"], payer_avec=["01088"], jouer=["bm010"],
       declencher_tolerant=["Puzzle.Action('bm001b', 'Action')"]),
    _c("bm001b Actually... a Trillionaire : TEMOIN sans l'Action, Grapple Gun (cout 3) ne se paie PAS avec une seule YY",
       "contre-temoin : sans reduction la carte reste en main",
       [], [], {"en_main": ["bm010"]}, main_exclusive=["bm010", "01088"], payer_avec=["01088"], jouer=["bm010"]),

    # 26/10/2026 (verdict regles bm001b) : le filtre de Trillionaire est un TRAIT (LOCATION, VEHICLE...), pas un type : un SOUTIEN en profite aussi.
    _c("bm001b Actually... a Trillionaire : un SOUTIEN a trait LOCATION (The Batcave, cout 2) se paie avec UNE seule ressource (cout reduit a 1)",
       "« Reduce the cost of the next ARMOR, ITEM, LOCATION, TECH, VEHICLE, or WEAPON card played this round by 1 » : le filtre est par trait, soutiens compris",
       [], ["Puzzle.Action('bm001b', 'Action')"], {"en_jeu": ["bm006"]},
       main_exclusive=["bm006", "01057"], payer_avec=["01057"], jouer=["bm006"]),
    _c("bm001b Actually... a Trillionaire : TEMOIN sans l'Action, The Batcave (cout 2) ne se paie PAS avec une seule ressource",
       "contre-temoin : sans reduction la carte reste en main",
       [], [], {"en_main": ["bm006"]}, main_exclusive=["bm006", "01057"], payer_avec=["01057"], jouer=["bm006"]),

    # ============================================================ bm002 Robin
    _c("bm002 Robin : apres avoir vaincu un ennemi, defausse une des 3 cartes du dessus du deck rencontre",
       "« After Robin defeats an enemy, look at the top 3 cards of the encounter deck. You may discard one »",
       [HEROS, *en_jeu("bm002", SBIRE_NEUTRE), "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01098', '01098', '01098')"],
       ["Puzzle.Attack('bm002')"], {"defausse_rencontre": ["01098"], "hors_jeu": [SBIRE_NEUTRE]}, remplissage=[], cibles=[SBIRE_NEUTRE, "01098"]),
    _c("bm002 Robin : apres avoir retire la DERNIERE menace d'une manigance, meme regard",
       "« ... or removes the last threat from a scheme »",
       [HEROS, *en_jeu("bm002"), "Puzzle.SetThreat('01097b', 1)", "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01098', '01098', '01098')"],
       ["Puzzle.Thwart('bm002')"], {"defausse_rencontre": ["01098"], "menace": [["01097b", 0]]}, remplissage=[], cibles=["01098"]),
    _c("bm002 Robin : une carte de dissuasion defaussee ainsi n'est pas resolue, elle est remelangee dans le deck rencontre",
       "livret : defaussee sans etre resolue -> defausse auxiliaire, puis remelange a la fin de l'effet",
       [HEROS, *en_jeu("bm002", SBIRE_NEUTRE), *reveler("bm018")], ["Puzzle.Attack('bm002')"],
       {"bm_rencontre_nb": 1, "bm_defausse": [], "bm_defausse_rencontre_nb": 0, "bm_remelanges": 1}, remplissage=[], cibles=[SBIRE_NEUTRE, "bm018"]),

    # ============================================================ bm003 / bm004 evenements
    _c("bm003 Violent Means : deux fois 2 degats, deux cibles choisies",
       "« Deal 2 damage to an enemy. Deal 2 damage to an enemy. »",
       [HEROS], [], {"degats": [[VILAIN, 4]]}, main_exclusive=["bm003", "01090"], payer_avec=["01090"], jouer=["bm003"],
       cibles=[VILAIN, VILAIN]),
    _c("bm004 I Am the Night : X = 1 (une carte a UNE ressource imprimee), retire 2 menaces d'une manigance",
       "« Resolve this action X times (max 3) : remove up to 2 threat » : 01057 Combat Training (RES R, 1 icone) paie X = 1",
       [HEROS, "Puzzle.SetThreat('01097b', 5)"], [], {"menace": [["01097b", 3]]},
       main_exclusive=["bm004", "01057"], payer_avec=["01057"], jouer=["bm004"], surpayer=True, cibles=[COMPLOT]),
    _c("bm004 I Am the Night : X = 2 (une carte YY), retire 4 menaces au total",
       "le cout X compte les RESSOURCES depensees (YY = 2) : 2 repetitions",
       [HEROS, "Puzzle.SetThreat('01097b', 5)"], [], {"menace": [["01097b", 1]]},
       main_exclusive=["bm004", "01088"], payer_avec=["01088"], jouer=["bm004"], surpayer=True, cibles=[COMPLOT, COMPLOT]),
    _c("bm004 I Am the Night : retirer la DERNIERE menace inflige 1 degat a un sbire",
       "« If this removes the last threat on that scheme, deal 1 damage to a minion »",
       [HEROS, "Puzzle.SetThreat('01097b', 2)", *en_jeu(SBIRE)], [], {"menace": [["01097b", 0]], "degats": [[SBIRE, 1]]},
       main_exclusive=["bm004", "01088"], payer_avec=["01088"], jouer=["bm004"], surpayer=True, cibles=[COMPLOT, SBIRE]),

    # ============================================================ bm005 Intimidate
    _c("bm005 Intimidate : la carte de dissuasion revelee ne gagne PAS Renfort (le carte du dessus du deck rencontre n'est pas revelee)",
       "« cancel its surge effect » : bm019 revelee, surge annule, la carte semee en dessous reste dans le deck",
       [HEROS, *en_jeu(SBIRE_NEUTRE), *reveler("bm019"), "Puzzle.MoveTo('01098', 'EncounterDeck')"], ["Puzzle.Reveal('bm019')"],
       {"bm_surge": [["bm019", 0]], "statuts": [[SBIRE_NEUTRE, "Confused"]]},
       main_exclusive=["bm005", "01088"], payer_avec=["01088"], cibles=[SBIRE_NEUTRE], accepter_choix=True, remplissage=[]),

    _c("bm005 Intimidate : TEMOIN sans Intimidate, la meme carte gagne Renfort (la carte du dessus est revelee)",
       "contre-temoin du precedent : sans l'Interruption, le surge de bm019 revele la carte semee au sommet",
       [HEROS, *en_jeu(SBIRE_NEUTRE), *reveler("bm019"), "Puzzle.MoveTo('01098', 'EncounterDeck')"], ["Puzzle.Reveal('bm019')"],
       {"bm_surge": [["bm019", 1]]}, remplissage=[], cibles=[SBIRE_NEUTRE], accepter_choix=True, main_exclusive=["01090"]),

    # ============================================================ bm006 / bm007 soutiens
    _c("bm006 The Batcave : Bruce Wayne gagne +2 REC (3 -> 5)",
       "« Bruce Wayne gets +2 REC »",
       [*en_jeu("bm006")], [], {"bm_stats": {"recover": 5}}),
    _c("bm006 The Batcave : Action d'alter ego, une des 5 cartes du dessus rejoint la main, le reste est melange",
       "« look at the top 5 cards of your deck. Choose one and add it to your hand. Shuffle the remaining cards »",
       [*en_jeu("bm006"), "Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01088', '01089', '01090', '01057', '01083')"],
       ["Puzzle.Action('bm006', 'AlterEgoAction')"], {"en_main": ["01083"], "exhausted": ["bm006"]},
       main_exclusive=["01090"], cibles=["01083"]),
    _c("bm007 Oracle : cherche une carte de dissuasion dans le deck rencontre, la REVELE (When Revealed) et melange",
       "« search the encounter deck for a deterrence card. Then reveal the chosen card and shuffle the encounter deck »",
       [HEROS, *en_jeu("bm007", SBIRE_NEUTRE), *reveler("bm019"), "Puzzle.MoveTo('01098', 'EncounterDeck')"], ["Puzzle.Action('bm007', 'Action')"],
       {"bm_defausse": ["bm019"], "statuts": [[SBIRE_NEUTRE, "Confused"]], "exhausted": ["bm007"]}, remplissage=[], cibles=["bm019", SBIRE_NEUTRE],
       accepter_choix=True),

    # ============================================================ bm008-bm012 ameliorations
    _c("bm008 Contingency Plan : retire 2 menaces ignorant les icones de crise, la carte est defaussee",
       "« remove up to 2 threat from a scheme, ignoring any crisis icons in play »",
       [HEROS, "Puzzle.SetThreat('01097b', 4)", *en_jeu("bm008")], ["Puzzle.Action('bm008', 'HeroAction')"],
       {"menace": [["01097b", 2]], "defausse_joueur": 1}, cibles=[COMPLOT], accepter_choix=True),
    # 26/10/2026 (verdict regles bm008) : « basic power » = ATK, THW ou DEF (RR p.10 : cinq pouvoirs de base) : la DEF doit etre proposee.
    _c("bm008 Contingency Plan : choix DEF, +2 DEF pour la prochaine defense du round (attaque de Rhino 2+4 : 2 degats au lieu de 4)",
       "« Choose a basic power, Batman gets +2 for his next use of the chosen basic power this round » : la DEF est un pouvoir de base",
       [HEROS, "Puzzle.SetThreat('01097b', 4)", *en_jeu("bm008")],
       ["Puzzle.Action('bm008', 'HeroAction')", f"Puzzle.EnemyAttacks('{VILAIN}', 'bm001a', additional_attack=4)"],
       {"degats_identite": 2}, cibles=[COMPLOT], accepter_choix=True,
       choisir_option="Batman_gets_+2_for_his_next_basic_defense_this_round"),
    _c("bm008 Contingency Plan : TEMOIN sans la carte, la meme attaque (2+4) contre DEF 2 inflige 4 degats",
       "temoin : le gain de 2 DEF vient bien de la carte",
       [HEROS], [f"Puzzle.EnemyAttacks('{VILAIN}', 'bm001a', additional_attack=4)"], {"degats_identite": 4}, accepter_choix=True),
    _c("bm009 Batsuit : +3 PV et +1 DEF (PV max 14, DEF 3)",
       "« You get +3 hit points. Batman gets +1 DEF »",
       [HEROS, *en_jeu("bm009")], [], {"pv_max": [["bm001a", 14]], "bm_stats": {"defense": 3}}),
    _c("bm010 Grapple Gun : Batman ignore Guard (Hydra Mercenary ne protege plus le vilain)",
       "« Batman ignores the guard keyword and the patrol keyword »",
       [HEROS, *en_jeu("bm010", SBIRE)], ["Puzzle.Attack('bm001a')"], {"degats": [[VILAIN, 2]]}, cibles=[VILAIN]),
    _c("bm010 Grapple Gun : Interruption, incliner -> changer de forme quand un ennemi s'active",
       "« When an enemy activates, exhaust Grapple Gun -> change your form »",
       [HEROS, *en_jeu("bm010")], ["Puzzle.Boost('01098')"], {"forme": "AlterEgo", "exhausted": ["bm010"]}, accepter_choix=True),
    _c("bm011 Batarangs : apres le When Revealed d'une dissuasion, 1 degat a un ennemi",
       "« After resolving the When Revealed ... of a deterrence card, deal 1 damage to an enemy » : Smoke Cloud desoriente Rhino puis Batarangs le blesse",
       [HEROS, *en_jeu("bm011"), *reveler("bm019")], ["Puzzle.Reveal('bm019')"],
       {"degats": [[VILAIN, 1]]}, accepter_choix=True),
    _c("bm012 Utility Belt : apres le When Revealed, incliner -> le resoudre une fois de plus (Sudden Strike : 3 + 3 degats), sans Renfort",
       "« resolve that card's When Revealed effect 1 additional time and cancel its surge effect » : Rhino 6 degats, le dessus du deck rencontre n'est pas revele",
       [HEROS, *en_jeu("bm012"), *reveler("bm018"), "Puzzle.MoveTo('01099', 'EncounterDeck')"], ["Puzzle.Reveal('bm018')"],
       {"degats": [[VILAIN, 6]], "exhausted": ["bm012"], "bm_surge": [["bm018", 0]]}, accepter_choix=True),
    # ============================================================ bm013 Ghosts of the Past
    _c("bm013 Ghosts of the Past : branche 2, les cartes de dissuasion du deck rencontre rejoignent le deck de dissuasion",
       "« Search and remove all of the deterrence cards from the encounter deck. Add these cards to your deterrence deck. »",
       [*reveler("bm018"), "Puzzle.ShuffleDeterrence('bm018')"], ["Puzzle.Reveal('bm013')"],
       {"bm_rencontre_nb": 0, "bm_taille_deck": 1}, accepter_choix=True,
       choisir_option="Add_the_deterrence_cards_of_the_encounter_deck_to_your_deterrence_deck._Discard_this_obligation"),

    # ============================================================ nemesis
    _c("bm015 Two-Face : apres un melange de dissuasion, +1 MNG et +1 ATQ",
       "« After a deterrence card is shuffled into the encounter deck, Two-Face gets +1 SCH and +1 ATK until the end of the round »",
       [HEROS, *en_jeu("bm015"), *dissuasion("bm018", "bm019")], ["Puzzle.Attack('bm001a')"],
       {"attributs_carte": [["bm015", "scheme", 1], ["bm015", "attack", 1]]}, accepter_choix=True, cibles=[VILAIN]),
    _c("bm015 Two-Face : TEMOIN D'EPUISEMENT, 3 melanges dans le round -> +2 seulement (« max twice per round »)",
       "trois attaques (Batman redresse entre deux) : la 3e ne donne plus de bonus",
       [HEROS, *en_jeu("bm015"), *dissuasion("bm018", "bm019", "bm020")],
       ["Puzzle.Attack('bm001a')", "Puzzle.Ready('bm001a')", "Puzzle.Attack('bm001a')", "Puzzle.Ready('bm001a')", "Puzzle.Attack('bm001a')"],
       {"attributs_carte": [["bm015", "scheme", 2], ["bm015", "attack", 2]]}, accepter_choix=True, cibles=[VILAIN]),
    _c("bm015 Two-Face : le REMELANGE du livret (dissuasion defaussee sans etre resolue) reveille aussi Two-Face, +1 MNG et +1 ATQ",
       "livret : « shuffle the deterrence card/s back into the encounter deck » = « a deterrence card is shuffled into the encounter deck » : Heads I Win defausse bm018, qui revient dans le deck",
       [HEROS, *en_jeu("bm015"), *reveler("bm018"), "Puzzle.MoveTo('01101', 'EncounterDeck')"], ["Puzzle.Reveal('bm016')"],
       {"attributs_carte": [["bm015", "scheme", 1], ["bm015", "attack", 1]]}, accepter_choix=True),
    _c("bm015 Two-Face : DEUX dissuasions defaussees puis remelangees par le meme effet -> +2 (une fois par carte remelangee, dans la limite de « max twice »)",
       "Heads I Win defausse bm018 et bm019 ; chacune revient dans le deck rencontre : Two-Face recoit +1 MNG / +1 ATQ pour chacune",
       [HEROS, *en_jeu("bm015"), *dissuasion("bm018", "bm019"), "Puzzle.ShuffleDeterrence('bm019')", "Puzzle.ShuffleDeterrence('bm018')"],
       ["Puzzle.Reveal('bm016')"],
       {"attributs_carte": [["bm015", "scheme", 2], ["bm015", "attack", 2]]}, accepter_choix=True),
    _c("bm016 Heads I Win : defausse 2 cartes, degats indirects = icones de boost, surge si une dissuasion est defaussee",
       "dessus du deck : bm018 (deviee, defausse rencontre vide : on defausse UNE AUTRE carte, 01098 sans icone) + 01101 (1 icone) -> 1 degat indirect (avant le 26/10 : 2)",
       [HEROS, *reveler("bm018"), "Puzzle.MoveTo('01101', 'EncounterDeck')"], ["Puzzle.Reveal('bm016')"],
       {"degats_identite": 1}, accepter_choix=True),
    _c("bm017 Tails You Lose : nombre impair d'icones, le premier joueur defausse 2 cartes au hasard",
       "dessus : 01101 (1 icone) + une carte sans icone (01098) -> total impair",
       [HEROS, "Puzzle.MoveTo('01101', 'EncounterDeck')", "Puzzle.MoveTo('01098', 'EncounterDeck')"], ["Puzzle.Reveal('bm017')"],
       {"taille_main": 3}, accepter_choix=True, main_exclusive=["01088", "01089", "01090", "01057", "01083"]),
    _c("bm017 Tails You Lose : une des deux cartes est une DISSUASION -> ses icones sont lues sur le dessus de la defausse (01101, 1 icone) : impair",
       "livret : la dissuasion deviee est remplacee par le dessus de la defausse rencontre ; 0 + 1 = impair -> la main tombe a 3",
       [HEROS, *reveler("bm018"), "Puzzle.MoveTo('01098', 'EncounterDeck')", "Puzzle.MoveTo('01101', 'EncounterDiscardPile')"], ["Puzzle.Reveal('bm017')"],
       {"taille_main": 3}, accepter_choix=True, main_exclusive=["01088", "01089", "01090", "01057", "01083"]),
    _c("bm017 Tails You Lose : TEMOIN, dissuasion + carte sans icone, defausse rencontre vide -> 0 icone (carte de remplacement 01098) : la main reste a 5",
       "meme montage sans carte a 1 icone dans la defausse : pair, personne ne defausse",
       [HEROS, *reveler("bm018"), "Puzzle.MoveTo('01098', 'EncounterDeck')"], ["Puzzle.Reveal('bm017')"],
       {"taille_main": 5}, accepter_choix=True, main_exclusive=["01088", "01089", "01090", "01057", "01083"]),
    _c("bm014 Split Decision : quand une dissuasion est revelee, defausse le dessus du deck ; nombre impair d'icones -> +2 menaces",
       "dessus du deck : 01101 (1 icone, impair) ; la dissuasion revelee est bm019",
       [HEROS, *en_jeu("bm014"), *reveler("bm019"), "Puzzle.MoveTo('01101', 'EncounterDeck')"], ["Puzzle.Reveal('bm019')"],
       {"menace": [["01097b", 2]], "defausse_rencontre": ["01101"]}, accepter_choix=True),

    _c("bm014 Split Decision : porte UNE icone Danger (Hazard), comme 01107 Breakin' & Takin' (+1 carte de rencontre en phase du mechant)",
       "pictogramme « carte + » imprime sous le texte, identique a 01107 (RR HAZARD ICON) : donnee `desc.Hazard` = 1",
       [HEROS], ["Puzzle.PutIntoPlay('bm014')"], {"icones": [["Hazard", 1]]}, accepter_choix=True),
    # 26/10/2026 (verdict regles, livret de l'auteur) : « If an effect references icons on a deterrence card that would have ended up in the discard pile,
    # use the top card of the discard pile instead, otherwise discard another card for the purposes of that effect. »
    _c("bm014 Split Decision : la carte defaussee est une DISSUASION -> on lit la carte du dessus de la defausse rencontre (0 icone : pas de menace)",
       "dessus du deck : bm018 (1 icone, mais deviee vers la defausse auxiliaire) ; dessus de la defausse : 01098 (0 icone) -> pair, aucune menace ; bm018 est remelangee",
       [HEROS, *en_jeu("bm014"), *dissuasion("bm018", "bm019"), "Puzzle.ShuffleDeterrence('bm019')", "Puzzle.ShuffleDeterrence('bm018')",
        "Puzzle.MoveTo('01098', 'EncounterDiscardPile')"], ["Puzzle.Reveal('bm019')"],
       {"menace": [["01097b", 0]]}, accepter_choix=True),
    _c("bm014 Split Decision : TEMOIN, dessus de la defausse a 1 icone (01101) -> impair, +2 menaces",
       "meme montage, la carte lue est celle du dessus de la defausse (1 icone) et non la dissuasion",
       [HEROS, *en_jeu("bm014"), *dissuasion("bm018", "bm019"), "Puzzle.ShuffleDeterrence('bm019')", "Puzzle.ShuffleDeterrence('bm018')",
        "Puzzle.MoveTo('01101', 'EncounterDiscardPile')"], ["Puzzle.Reveal('bm019')"],
       {"menace": [["01097b", 2]]}, accepter_choix=True),
    _c("bm014 Split Decision : defausse rencontre VIDE -> on defausse UNE AUTRE carte pour cet effet (01101, 1 icone) : +2 menaces",
       "« otherwise discard another card for the purposes of that effect » : la dissuasion est deviee, la carte suivante du deck (01101) est defaussee et lue",
       [HEROS, *en_jeu("bm014"), *dissuasion("bm018", "bm019"), "Puzzle.MoveTo('01101', 'EncounterDeck')",
        "Puzzle.ShuffleDeterrence('bm019')", "Puzzle.ShuffleDeterrence('bm018')"], ["Puzzle.Reveal('bm019')"],
       {"menace": [["01097b", 2]], "defausse_rencontre": ["01101"]}, accepter_choix=True),
    _c("bm016 Heads I Win : une des deux cartes defaussees est une DISSUASION -> ses icones sont lues sur le dessus de la defausse (01099 : 2 icones)",
       "dessus du deck : bm018 (deviee) + 01101 (1 icone) ; dessus de la defausse : 01099 (2 icones) -> 3 degats indirects (et non 1 + 1)",
       [HEROS, *dissuasion("bm018"), "Puzzle.MoveTo('01101', 'EncounterDeck')", "Puzzle.ShuffleDeterrence('bm018')",
        "Puzzle.MoveTo('01099', 'EncounterDiscardPile')"], ["Puzzle.Reveal('bm016')"],
       {"degats_identite": 3}, accepter_choix=True),
    _c("bm016 Heads I Win : EGALITE de PV restants a deux joueurs -> le PREMIER JOUEUR choisit la cible (ici Peter Parker, pas Batman)",
       "« The player with the most remaining hit points » + egalite : RR FIRST PLAYER (le premier joueur choisit parmi les cibles admissibles)",
       [HEROS, "Puzzle.Damage('bm001a', 1)", *dissuasion("bm018"), "Puzzle.MoveTo('01101', 'EncounterDeck')", "Puzzle.MoveTo('01099', 'EncounterDeck')"],
       ["Puzzle.Reveal('bm016')"],
       {"degats": [["01001b", 3], ["bm001a", 1]]}, accepter_choix=True, cibles=["01001b"], heros2="spider_man"),

    # ============================================================ bm018-bm022 : boost et defausse non resolue
    _c("bm018 Sudden Strike : en BOOST, resolue -> defausse de dissuasion ; 2 degats a l'ennemi qui s'active (Batman en jeu)",
       "« [star] Boost: ... If Batman is in play, Batman deals the activating enemy 2 damage »",
       [HEROS, *reveler("bm018")], ["Puzzle.Boost('bm018')"], {"degats": [[VILAIN, 2]], "bm_defausse": ["bm018"]}, remplissage=[], accepter_choix=True),
    _c("bm019 Smoke Cloud : en BOOST contre une attaque, reduit de 2 les degats de l'activation",
       "« If the enemy is attacking, reduce the damage dealt by this activation by 2 » : Rhino ATK 2 + 0 = 2 degats normaux -> 0",
       [HEROS, "Puzzle.Exhaust('bm001a')", *reveler("bm019")], ["Puzzle.Boost('bm019')"], {"degats_identite": 0, "bm_defausse": ["bm019"]},
       remplissage=[], accepter_choix=True, ),
    _c("bm022 Shadow of the Bat : en BOOST, prevent all damage de l'activation (Batman en jeu)",
       "« prevent all threat and damage from this activation »",
       [HEROS, "Puzzle.Exhaust('bm001a')", *reveler("bm022")], ["Puzzle.Boost('bm022')"], {"degats_identite": 0, "bm_defausse": ["bm022"]}, remplissage=[], accepter_choix=True),
    _c("bm020 Detective Work : When Revealed, deux cartes de la defausse sous le deck",
       "« That player chooses two cards in their discard pile and either puts them on the bottom of their deck or shuffles them into their deck »",
       [HEROS, "Puzzle.CreatePlayerDiscardPile('01088', '01089')", *reveler("bm020")], ["Puzzle.Reveal('bm020')"],
       {"bm_defausse": ["bm020"], "defausse_joueur": 1}, remplissage=[], accepter_choix=True),

]


VERIFICATIONS = r'''
def bm_etat(monde, aides):
    """Cles propres : `bm_taille_deck` (cartes du deck de dissuasion), `bm_deck` / `bm_defausse` (card_id exacts, ordre libre), `bm_rencontre_nb` (cartes
    DETERRENCE dans le deck de rencontre), `bm_defausse_rencontre_nb`, `bm_nb_dissuasion_total` (deck + defausse de dissuasion), `bm_stats`
    ({attribut: valeur} de l'identite) ; le reste va a etat_attendu."""
    from game.operate.worlds import Worlds
    cas = aides["cas"]
    attendu = cas.get("attendu") or {}
    soucis = []
    joueur = monde.players[0]
    identite = aides["identite"](monde)
    ids = lambda faces: [getattr(f.paper, "card_id", None) for f in faces if f is not None]
    deck = ids(joueur.additional_deck.Get())
    defausse = ids(joueur.additional_discard_pile.Get(True))
    if "bm_taille_deck" in attendu and len(deck) != attendu["bm_taille_deck"]:
        soucis.append(f"deck de dissuasion = {sorted(deck)} (attendu {attendu['bm_taille_deck']} carte(s))")
    if "bm_deck" in attendu and sorted(deck) != sorted(attendu["bm_deck"]):
        soucis.append(f"deck de dissuasion = {sorted(deck)} (attendu {sorted(attendu['bm_deck'])})")
    if "bm_defausse" in attendu and sorted(defausse) != sorted(attendu["bm_defausse"]):
        soucis.append(f"defausse de dissuasion = {sorted(defausse)} (attendu {sorted(attendu['bm_defausse'])})")
    if "bm_nb_dissuasion_total" in attendu and len(deck) + len(defausse) != attendu["bm_nb_dissuasion_total"]:
        soucis.append(f"{len(deck) + len(defausse)} carte(s) de dissuasion (deck {sorted(deck)} + defausse {sorted(defausse)})")
    rencontre = [f for f in Worlds.GetEncounterDeckCards(monde) if f.HasTrait("DETERRENCE")]
    if "bm_rencontre_nb" in attendu and len(rencontre) != attendu["bm_rencontre_nb"]:
        soucis.append(f"{len(rencontre)} carte(s) de dissuasion dans le deck rencontre : {sorted(ids(rencontre))} (attendu {attendu['bm_rencontre_nb']})")
    if "bm_defausse_rencontre_nb" in attendu:
        dr = [f for f in Worlds.GetEncounterDiscardPileCards(monde) if f.HasTrait("DETERRENCE")]
        if len(dr) != attendu["bm_defausse_rencontre_nb"]:
            soucis.append(f"{len(dr)} carte(s) de dissuasion dans la defausse rencontre (attendu {attendu['bm_defausse_rencontre_nb']})")
    for card_id, voulu in attendu.get("bm_surge") or []:
        faces = [f for f in joueur.additional_discard_pile.Get(True) if getattr(f.paper, "card_id", None) == card_id]
        valeurs = sorted({getattr(f, "surge", None) for f in faces})
        if valeurs != [voulu]:
            soucis.append(f"surge de {card_id} resolue (defausse de dissuasion) = {valeurs} (attendu {voulu})")
    if "bm_remelanges" in attendu and getattr(joueur, "bm_remelanges", 0) != attendu["bm_remelanges"]:
        soucis.append(f"{getattr(joueur, 'bm_remelanges', 0)} remelange(s) de la defausse auxiliaire (attendu {attendu['bm_remelanges']})")
    for nom, valeur in (attendu.get("bm_stats") or {}).items():
        courant = getattr(identite, nom, None)
        if courant != valeur:
            soucis.append(f"{nom} = {courant} (attendu {valeur})")
    propres = ("bm_taille_deck", "bm_deck", "bm_defausse", "bm_nb_dissuasion_total", "bm_rencontre_nb", "bm_defausse_rencontre_nb", "bm_stats", "bm_surge", "bm_remelanges")
    reste = {k: v for k, v in attendu.items() if k not in propres}
    copie = dict(aides); copie["cas"] = dict(cas); copie["cas"]["attendu"] = reste
    ok, message = etat_attendu(monde, copie)
    if not ok:
        soucis.append(message)
    if soucis:
        return False, " ; ".join(soucis)
    return True, message
'''
