# Cas test_capacites du heros WASP (Hank Pym) (JackHKP, prefixe `hp`) : noms prefixes « [hp] » puis le card_id
# (substituer_pack.py filtre dessus).
#
# Rappels de montage :
#  - le deck wasp_hank_pym demarre en ALTER EGO (hp001b Hank Pym). `Puzzle.ChangeToFace('hp001b', 'hp001a')` -> Wasp
#    MINUSCULE ; `('hp001b', 'hp001c')` -> Wasp GEANT. Chaque changement de forme est COMPTE (« formes changees ce tour ») ;
#  - Rhino 01094 est le vilain, 01097b son complot principal, 01101 Hydra Mercenary un sbire (3 PV, Guard) ;
#  - ressources : 01088 Energy = YY, 01089 Genius = BB, 01090 Strength = RR. ⚠ La main des cas est faite de 01088 (YY) :
#    avec RR (01090) en main le pilote paierait la branche « stun the villain instead » de Man-Mountain PENDANT la mise en place
#    (le paiement y echoue, UndoRequest, la forme GEANTE est annulee) ; idem BB (01089) pour Bumble Bee. On ne met RR / BB en main
#    que dans les cas qui PAIENT cette branche.
SC = "rhino"
VILAIN = "01094"
COMPLOT = "01097b"
SBIRE = "01101"
TINY = "Puzzle.ChangeToFace('hp001b', 'hp001a')"
GIANT = "Puzzle.ChangeToFace('hp001b', 'hp001c')"
# Aucun « Change Form » en alter ego (« only by card abilities ») : le tour est atteint des que l'une de ces options est offerte.
NOMS_TOUR = ["Scientist_Supreme", "Scientist Supreme", "Recover"]
SANS_BOOST = ["Puzzle.EmptyEncounterDeck()",
              "Puzzle.CreateEncounterDeck('01098', '01098', '01098', '01098', '01098', '01098', '01098', '01098')"]


# Passer en GEANT pendant la MISE EN PLACE declenche « Man-Mountain » : sans sbire en jeu, le pilote prend la branche payante
# (la main de depart est tiree au hasard, elle peut offrir des [physical] imprimes que `payer_avec` ne designe pas) et le
# paiement echoue, ce qui annule tout le changement de forme. Un sbire en jeu donne a la premiere branche une cible.
SBIRE_PUIS_GEANT = [f"Puzzle.PutIntoPlay('{SBIRE}', under_control=True)", GIANT]


def en_jeu(*ids):
    return [f"Puzzle.PutIntoPlay('{i}', under_control=True)" for i in ids]


def _c(nom, pourquoi, mise, declencher, attendu, **cle):
    mise = SANS_BOOST + list(mise)
    cas = {"nom": "[hp] " + nom, "pourquoi": pourquoi, "scenario": cle.pop("scenario", SC),
           "heros": cle.pop("heros", "wasp_hank_pym"), "mise_en_place": mise, "declencher": declencher,
           "verifier": cle.pop("verifier", "hp_etat"), "attendu": attendu}
    cas.setdefault("regles", ["v16_all", "v18_all"])
    cas.setdefault("noms_tour", NOMS_TOUR)
    cas.update(cle)
    return cas


CAS = [
    # ============================================================ hp001a Wasp minuscule : Bumble Bee
    _c("hp001a Bumble Bee : passage en TINY -> un sbire est desoriente",
       "« After you change to this form, confuse a minion »",
       en_jeu(SBIRE), [TINY],
       {"hp_face": "hp001a", "statuts": [[SBIRE, "Confused"]], "statuts_absents": [[VILAIN, "Confused"]]},
       main_exclusive=["01088"], cibles=[SBIRE], accepter_choix=True, preferer_option="Confuse_a_minion"),
    _c("hp001a Bumble Bee : en payant [mental][mental] le VILAIN est desoriente A LA PLACE du sbire",
       "« You may spend [mental][mental] resource to confuse the villain instead »",
       en_jeu(SBIRE), [TINY],
       {"hp_face": "hp001a", "statuts": [[VILAIN, "Confused"]], "statuts_absents": [[SBIRE, "Confused"]]},
       main_exclusive=["01089"], payer_avec=["01089"], cibles=[VILAIN], accepter_choix=True,
       preferer_option="Confuse_the_villain_instead"),
    _c("hp001a Wasp minuscule : valeurs imprimees PV 12, THW 2, ATK 1, DEF 2, taille de main 5, AVENGER TINY",
       "nombres texte <-> code (scan) : HAND SIZE 5 / HIT POINTS 12",
       [TINY], [], {"hp_face": "hp001a", "pv_max": [["hp001a", 12]], "traits": ["AVENGER", "TINY"],
                    "hp_stats": {"attack": 1, "thwart": 2, "defense": 2, "hand_size": 5}}, main_exclusive=["01088"]),

    # ============================================================ hp001c Wasp geant : Man-Mountain
    _c("hp001c Man-Mountain : passage en GIANT -> un sbire est etourdi",
       "« After you change to this form, stun a minion »",
       en_jeu(SBIRE), [GIANT],
       {"hp_face": "hp001c", "statuts": [[SBIRE, "Stunned"]], "statuts_absents": [[VILAIN, "Stunned"]]},
       main_exclusive=["01088"], cibles=[SBIRE], accepter_choix=True, preferer_option="Stun_a_minion"),
    _c("hp001c Man-Mountain : en payant [physical][physical] le VILAIN est etourdi A LA PLACE du sbire",
       "« You may spend [physical][physical] resource to stun the villain instead »",
       en_jeu(SBIRE), [GIANT],
       {"hp_face": "hp001c", "statuts": [[VILAIN, "Stunned"]], "statuts_absents": [[SBIRE, "Stunned"]]},
       main_exclusive=["01090"], payer_avec=["01090"], cibles=[VILAIN], accepter_choix=True,
       preferer_option="Stun_the_villain_instead"),
    _c("hp001c Wasp geant : valeurs imprimees PV 12, THW 1, ATK 3, DEF 3, taille de main 4, AVENGER GIANT",
       "nombres texte <-> code (scan) : HAND SIZE 4 / HIT POINTS 12",
       SBIRE_PUIS_GEANT, [], {"hp_face": "hp001c", "pv_max": [["hp001c", 12]], "traits": ["AVENGER", "GIANT"],
                    "hp_stats": {"attack": 3, "thwart": 1, "defense": 3, "hand_size": 4}}, main_exclusive=["01088"]),

    # ============================================================ hp001b Hank Pym : Scientist Supreme
    _c("hp001b Scientist Supreme : un Size Manipulation en jeu (2 compteurs) -> 3 compteurs pym",
       "« Spend 1 [mental] resource -> place 1 pym counter on a Size Manipulation upgrade »",
       en_jeu("hp011"), ["Puzzle.Action('hp001b', 'Action')"],
       {"hp_face": "hp001b", "compteurs": [["hp011", "pym", 3]]},
       main_exclusive=["01089"], payer_avec=["01089"], accepter_choix=True),
    _c("hp001b Scientist Supreme : AUCUN Size Manipulation en jeu -> cherche un exemplaire dans le deck et le met en jeu",
       "« If you cannot, search your deck for a copy of Size Manipulation and put it into play »",
       [], ["Puzzle.Action('hp001b', 'Action')"],
       {"hp_face": "hp001b", "en_jeu": ["hp011"], "compteurs": [["hp011", "pym", 2]]},
       main_exclusive=["01089"], payer_avec=["01089"], accepter_choix=True),
    _c("hp001b Hank Pym : valeurs imprimees PV 12, REC 3, taille de main 6, GENIUS",
       "nombres texte <-> code (scan) : HAND SIZE 6 / HIT POINTS 12 / REC 3",
       [], [], {"hp_face": "hp001b", "pv_max": [["hp001b", 12]], "traits": ["GENIUS"],
                "hp_stats": {"recover": 3, "hand_size": 6}}, main_exclusive=["01088"]),
    _c("hp001b TEMOIN : pas de changement de forme LIBRE offert (« only by card abilities »)",
       "« You can only change form by card abilities » : aucune option « Change To » offerte en alter ego",
       [], [], {"hp_face": "hp001b", "hp_pas_de_changement_libre": True}, main_exclusive=["01088"],
       options_attendues_mise_en_place=["Scientist Supreme"]),

    # ============================================================ hp002 Ant-Man
    _c("hp002 Ant-Man : incline un Size Manipulation -> 1 compteur pym passe sur Ant-Man (+1 THW +1 ATK)",
       "« Exhaust a Size Manipulation -> move 1 pym counter from it to here » ; « +1 THW and +1 ATK for each pym counter »",
       en_jeu("hp011", "hp002"), ["Puzzle.Action('hp002', 'Action', 0)"],
       {"compteurs": [["hp011", "pym", 1], ["hp002", "pym", 1]], "exhausted": ["hp011"],
        "hp_attr": [["hp002", "attack", 3], ["hp002", "thwart", 3]]},
       main_exclusive=["01088"], accepter_choix=True),
    _c("hp002 Ant-Man : TEMOIN sans compteur -> ses valeurs imprimees (ATK 2, THW 2)",
       "les valeurs imprimees 2* / 2* valent 2 sans compteur",
       en_jeu("hp002"), [], {"hp_attr": [["hp002", "attack", 2], ["hp002", "thwart", 2]]}, main_exclusive=["01088"]),
    _c("hp002 Ant-Man : se defausse -> change de forme (TINY vers alter ego ou GIANT)",
       "« Discard this card -> change form »",
       [TINY] + en_jeu("hp002"), ["Puzzle.Action('hp002', 'Action', 0)"],
       {"hors_jeu": ["hp002"], "hp_formes": 2},
       main_exclusive=["01088"], accepter_choix=True),

    # ============================================================ hp003 Gigantification
    _c("hp003 Gigantification : TINY -> GIANT et 4 degats au vilain malgre le Guard du sbire",
       "« Change to GIANT hero form. Deal 4 damage to an enemy, ignoring any guard keyword »",
       [TINY] + en_jeu(SBIRE), [],
       {"hp_face": "hp001c", "degats": [[VILAIN, 4]]},
       main_exclusive=["hp003", "01088"], jouer=["hp003"], payer_avec=["01088"], cibles=[VILAIN], accepter_choix=True),
    _c("hp003 Gigantification : TEMOIN en forme GEANTE -> injouable",
       "« Play only if you are in TINY hero form »",
       [GIANT], [], {}, main_exclusive=["hp003", "01088"], jouer=["hp003"], accepter_choix=True,
       verifier="hellcat_carte_restee_en_main", restee="hp003"),
    _c("hp003 Gigantification (defense) : un ennemi attaque -> passe en GIANT et recoit un statut Tough",
       "« Hero Interrupt (defense): When an enemy attacks, change to GIANT hero form. Give your hero a tough status card »",
       [TINY], [f"Puzzle.EnemyAttacks('{VILAIN}', 'hp001a')"],
       {"hp_face": "hp001c", "statuts": [["hp001c", "Tough"]]},
       main_exclusive=["hp003", "01088"], jouer=["hp003"], payer_avec=["01088"], accepter_choix=True),

    # ============================================================ hp004 Resize at Will
    _c("hp004 Resize at Will : en alter ego -> change de forme puis (heros) fait une attaque de base sans incliner",
       "« Change form. Then, if you are in GIANT hero form, make a basic attack without exhausting »",
       [], [],
       {"hp_formes": 1, "degats_min": [[VILAIN, 1]]},
       main_exclusive=["hp004", "01088"], jouer=["hp004"], payer_avec=["01088"], cibles=[VILAIN], accepter_choix=True,
       preferer_option="GIANT"),

    # ============================================================ hp005 Self-Shrinking
    _c("hp005 Self-Shrinking : GIANT -> TINY et 3 menaces retirees",
       "« Change to TINY hero form. Remove 3 threat from a scheme »",
       SBIRE_PUIS_GEANT + [f"Puzzle.SetThreat('{COMPLOT}', 5)"], [],
       {"hp_face": "hp001a", "menace": [[COMPLOT, 2]]},
       main_exclusive=["hp005", "01088"], jouer=["hp005"], payer_avec=["01088"], cibles=[COMPLOT], accepter_choix=True),
    _c("hp005 Self-Shrinking : TEMOIN en forme MINUSCULE -> injouable",
       "« Play only if you are in GIANT hero form »",
       [TINY], [], {}, main_exclusive=["hp005", "01088"], jouer=["hp005"], accepter_choix=True,
       verifier="hellcat_carte_restee_en_main", restee="hp005"),
    _c("hp005 Self-Shrinking (defense) : l'ennemi declare une attaque -> passe en TINY et l'attaque est ANNULEE",
       "« When an enemy initiates an attack against you, change to TINY hero form and cancel that attack »",
       SBIRE_PUIS_GEANT, [f"Puzzle.EnemyAttacks('{VILAIN}', 'hp001c')"],
       {"hp_face": "hp001a", "degats_identite": 0},
       main_exclusive=["hp005", "01088"], jouer=["hp005"], payer_avec=["01088"], accepter_choix=True),

    # ============================================================ hp006 Pym Particles
    _c("hp006 Pym Particles : depensee, redresse le Size Manipulation et y pose 2 compteurs",
       "« Ready each Size Manipulation upgrade you control and place a total of 2 pym counters on them »",
       en_jeu("hp011") + ["Puzzle.Exhaust('hp011')"], [],
       {"pret": ["hp011"], "compteurs": [["hp011", "pym", 4]], "hp_formes": 0},
       main_exclusive=["hp006", "hp008", "01088"], jouer=["hp008"], payer_avec=["hp006", "01088"], accepter_choix=True),

    # ============================================================ hp007 Infinite Avengers Mansion
    _c("hp007 Infinite Avengers Mansion : en alter ego -> 1 compteur pym sur une carte et une carte « identity-specific » remelangee",
       "« place 1 pym counter on a card you control and shuffle 1 identity-specific card from your discard pile into your deck »",
       en_jeu("hp007", "hp011") + ["Puzzle.Discard('hp003')"], ["Puzzle.Action('hp007', 'AlterEgoAction')"],
       {"exhausted": ["hp007"], "compteurs": [["hp011", "pym", 3]], "dans_deck_joueur": ["hp003"]},
       main_exclusive=["01088"], accepter_choix=True),

    # ============================================================ hp008 Jocasta
    _c("hp008 Jocasta : en forme GEANTE Wasp gagne +1 THW (1 -> 2)",
       "« Wasp gets +1 THW »",
       SBIRE_PUIS_GEANT + en_jeu("hp008"), [], {"hp_attr": [["hp001c", "thwart", 2]]}, main_exclusive=["01088"]),
    _c("hp008 Jocasta : TEMOIN en alter ego, aucun THW donne a Hank Pym (lecon an002 : « Wasp » = les formes heros)",
       "le NOM Wasp ne designe pas l'alter ego : pas de bonus",
       en_jeu("hp008"), [], {"hp_face": "hp001b", "hp_attr": [["hp001b", "thwart", None]]}, main_exclusive=["01088"]),
    _c("hp008 Jocasta : apres le passage en alter ego, incline Jocasta -> redresse l'identite",
       "« Alter-Ego Response: After you change to alter-ego form, exhaust this card -> ready your identity »",
       [TINY, "Puzzle.Exhaust('hp001a')"] + en_jeu("hp008"), ["Puzzle.ChangeToFace('hp001a', 'hp001b')"],
       {"hp_face": "hp001b", "pret": ["hp001b"], "exhausted": ["hp008"]},
       main_exclusive=["01088"], accepter_choix=True),

    # ============================================================ hp009 Bio-Synthetic Wings
    _c("hp009 Bio-Synthetic Wings : en forme MINUSCULE le heros gagne le trait AERIAL",
       "« While Wasp is in TINY hero form, he gains the AERIAL trait »",
       [TINY] + en_jeu("hp009"), [], {"hp_face": "hp001a", "traits": ["AERIAL"]}, main_exclusive=["01088"]),
    _c("hp009 Bio-Synthetic Wings : TEMOIN en forme GEANTE, pas de trait AERIAL",
       "le trait n'est donne qu'en forme minuscule",
       SBIRE_PUIS_GEANT + en_jeu("hp009"), [], {"hp_face": "hp001c", "traits_absents": ["AERIAL"]}, main_exclusive=["01088"]),
    _c("hp009 Bio-Synthetic Wings : thwart X = formes changees ce tour",
       "« Exhaust this card -> remove X threat ... where X is the number of times you have changed form this turn »",
       [f"Puzzle.SetThreat('{COMPLOT}', 6)", TINY] + en_jeu("hp009"), ["Puzzle.Action('hp009', 'HeroAction')"],
       {"exhausted": ["hp009"], "hp_formes_menace": COMPLOT},
       main_exclusive=["01088"], cibles=[COMPLOT], accepter_choix=True),

    # ============================================================ hp010 Huge Surprise
    _c("hp010 Huge Surprise : s'attache au vilain ; etourdi, il subit 4 degats",
       "« Attach this card to an enemy -> ... takes 4 damage after it is stunned or confused »",
       [TINY] + en_jeu("hp010"), ["Puzzle.Action('hp010', 'HeroAction')", f"Puzzle.Stun('{VILAIN}')"],
       {"hotes": [["hp010", VILAIN]], "degats": [[VILAIN, 4]]},
       main_exclusive=["01088"], cibles=[VILAIN], accepter_choix=True),

    # ============================================================ hp011 Size Manipulation
    _c("hp011 Size Manipulation : entre en jeu avec 2 compteurs pym",
       "« Enters play with 2 pym counters on it »",
       en_jeu("hp011"), [], {"compteurs": [["hp011", "pym", 2]]}, main_exclusive=["01088"]),
    _c("hp011 Size Manipulation : Action -> incline, retire 1 compteur, change de forme",
       "« Exhaust this card and remove 1 pym counter from here -> change form »",
       en_jeu("hp011"), ["Puzzle.Action('hp011', 'Action', 0)"],
       {"exhausted": ["hp011"], "compteurs": [["hp011", "pym", 1]], "hp_formes": 1},
       main_exclusive=["01088"], accepter_choix=True),
    _c("hp011 Size Manipulation : Resource -> paie une carte de cout 1 avec [wild] et perd 1 compteur",
       "« Resource: Exhaust this card and remove 1 pym counter from here -> generate a [wild] resource »",
       en_jeu("hp011"), [],
       {"exhausted": ["hp011"], "compteurs": [["hp011", "pym", 1]], "en_jeu": ["hp008"]},
       main_exclusive=["hp008", "01088"], jouer=["hp008"], payer_avec=["hp011", "01088"], accepter_choix=True),

    # ============================================================ hp012 The Stinger
    _c("hp012 The Stinger : X degats = formes changees ce tour (1 changement -> 1 degat)",
       "« Exhaust this card -> deal X damage divided among enemies you choose, X = times you have changed form this turn »",
       [TINY] + en_jeu("hp012"), ["Puzzle.Action('hp012', 'HeroAction')"],
       {"exhausted": ["hp012"], "hp_formes_degats": VILAIN},
       main_exclusive=["01088"], cibles=[VILAIN], accepter_choix=True),

    # ============================================================ hp013 Identity Crisis
    _c("hp013 Identity Crisis : un changement de forme -> 1 compteur crisis",
       "« Forced Response: After you change form, place 1 crisis counter here »",
       en_jeu("hp013"), [TINY], {"hp_face": "hp001a", "compteurs": [["hp013", "crisis", 1]]}, main_exclusive=["01088"]),
    # ============================================================ hp002 Ant-Man : plafond +3
    _c("hp002 Ant-Man : 5 compteurs pym -> bonus plafonne a +3 (ATK 5, THW 5)",
       "« to a maximum of +3 THW and +3 ATK » : 2 + 3 = 5 malgre 5 compteurs",
       en_jeu("hp002") + ["Puzzle.Counter('hp002', 'pym', 5)"], [],
       {"hp_attr": [["hp002", "attack", 5], ["hp002", "thwart", 5]]}, main_exclusive=["01088"]),

    # ============================================================ hp013 Identity Crisis : sortie
    _c("hp013 Identity Crisis : 2 compteurs crisis, Action d'alter ego -> 2 degats, Hank Pym s'incline et l'obligation est defaussee",
       "« Choose to take 1 damage ... for each crisis counter here. Then, exhaust Hank Pym -> discard this obligation »",
       en_jeu("hp013") + ["Puzzle.Counter('hp013', 'crisis', 2)"], ["Puzzle.Action('hp013', 'AlterEgoAction')"],
       {"degats_identite": 2, "exhausted": ["hp001b"], "hors_jeu": ["hp013"]},
       main_exclusive=["01088"], accepter_choix=True, preferer_option="Take_1_damage"),

    # ============================================================ hp014 Return of the Prodigal Son
    _c("hp014 Prodigal Son : apres la phase joueur, 1 compteur seize",
       "« After the player phase ends, place 1 seize counter here »",
       ["Puzzle.PutIntoPlay('hp014')"], ["Puzzle.EndPlayerPhase()"],
       {"compteurs": [["hp014", "seize", 1]]}, main_exclusive=["01088"]),
    _c("hp014 Prodigal Son : au 2e compteur, retire les compteurs et glisse sous la carte le soutien/l'amelioration au cout le plus eleve",
       "« if there are 2 or more seize counters here, remove all seize counters and place the upgrade or support with the highest cost facedown under here »",
       ["Puzzle.PutIntoPlay('hp014')"] + en_jeu("hp008", "hp009"), ["Puzzle.EndPlayerPhase()", "Puzzle.EndPlayerPhase()"],
       {"compteurs": [["hp014", "seize", 0]], "en_jeu": ["hp009"], "hors_jeu": ["hp008"]}, main_exclusive=["01088"]),

    # ============================================================ hp015 Ultron + hp016 Seized Control
    _c("hp015 Ultron : revele -> trouve Seized Control mis de cote, qui s'attache a Ultron et glisse sous lui la carte au cout le plus bas",
       "« Find the set-aside Seized Control attachment and reveal it » ; hp016 « Tuck the card you control with the lowest cost under here »",
       en_jeu("hp008"), ["Puzzle.Reveal('hp015')"],
       {"en_jeu": ["hp015", "hp016"], "hotes": [["hp016", "hp015"]], "hors_jeu": ["hp008"], "pv_max": [["hp015", 5]]},
       main_exclusive=["01088"]),
    _c("hp016 Seized Control : les degats subis par Ultron sont places SUR la carte (X = cout de la carte glissee = 3)",
       "« When the attached character would take any amount of damage, place it here instead »",
       en_jeu("hp008"), ["Puzzle.Reveal('hp015')", "Puzzle.Damage('hp015', 2)"],
       {"compteurs": [["hp016", "damage", 2]], "degats": [["hp015", 0]]},
       main_exclusive=["01088"]),

    # ============================================================ hp017 Take Over Signal
    _c("hp017 Take Over Signal : revelee -> s'attache a l'allie au cout le plus eleve (Ant-Man, 3)",
       "« Attach to the ally you control with the highest cost »",
       en_jeu("hp002"), ["Puzzle.Reveal('hp017')"],
       {"hotes": [["hp017", "minion"]]}, main_exclusive=["01088"]),

    # ============================================================ hp018 Submit or Perish
    _c("hp018 Submit or Perish : UNE amelioration inclinee (< 2) -> Ultron entre en jeu, engage avec toi",
       "« If fewer than 2 upgrades were exhausted this way, search ... for the Ultron minion and put it into play »",
       [TINY] + en_jeu("hp009") + ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('hp015', '01098', '01098')"],
       ["Puzzle.Reveal('hp018')"],
       {"exhausted": ["hp009"], "en_jeu": ["hp015"]}, main_exclusive=["01088"]),
    _c("hp018 Submit or Perish : DEUX ameliorations inclinees -> la carte gagne surge, pas d'Ultron",
       "« Otherwise, this card gains surge »",
       [TINY] + en_jeu("hp009", "hp011"), ["Puzzle.Reveal('hp018')"],
       {"exhausted": ["hp009", "hp011"], "hp_ultron_absent": True}, main_exclusive=["01088"]),
    # ============================================================ CORRECTIFS DU 26/10/2026 (arbitrages relus contre le RR v1.8 et les scans)
    # hp007 : « a card you control » inclut l'IDENTITE et le Mansion lui-meme (OWNERSHIP AND CONTROL).
    _c("hp007 Infinite Avengers Mansion : seule carte en jeu avec l'identite -> le compteur pym est pose quand meme (identite ou Mansion)",
       "« place 1 pym counter on a card you control » : l'identite et le Mansion sont des cartes que l'on controle (RR OWNERSHIP AND CONTROL)",
       en_jeu("hp007"), ["Puzzle.Action('hp007', 'AlterEgoAction')"],
       {"exhausted": ["hp007"], "compteurs_total": [["pym", 1]]},
       main_exclusive=["01088"], accepter_choix=True),
    _c("hp007 Infinite Avengers Mansion : le joueur designe l'IDENTITE (Hank Pym) -> elle porte le compteur pym",
       "« a card you control » : l'identite est une carte que l'on controle (RR OWNERSHIP AND CONTROL)",
       en_jeu("hp007", "hp011"), ["Puzzle.Action('hp007', 'AlterEgoAction')"],
       {"exhausted": ["hp007"], "compteurs_identite": [["pym", 1]], "compteurs": [["hp011", "pym", 2]]},
       main_exclusive=["01088"], accepter_choix=True, cibles=["hp001b"]),
    # hp009 : « remove X threat from AMONG schemes » = repartition entre manigances (17029, 36010).
    _c("hp009 Bio-Synthetic Wings : X = 2, deux manigances a 1 menace -> 1 menace retiree a CHACUNE (repartition entre manigances)",
       "« remove X threat from among schemes » : la formule officielle de repartition (17029 Agile Flight)",
       en_jeu(SBIRE) + [f"Puzzle.SetThreat('{COMPLOT}', 1)", "Puzzle.PutIntoPlay('01109')", "Puzzle.SetThreat('01109', 1)",
                        TINY, "Puzzle.ChangeToFace('hp001a', 'hp001c')"] + en_jeu("hp009"),
       ["Puzzle.Action('hp009', 'HeroAction')"],
       {"exhausted": ["hp009"], "hp_formes": 2, "menace": [[COMPLOT, 0]], "hp_menace_nulle_ou_absente": ["01109"]},
       main_exclusive=["01088"], accepter_choix=True),
    # hp012 : « deal X damage divided among enemies » = X degats a inflige, jamais moins.
    _c("hp012 The Stinger : X = 2, le joueur ne designe que le MINIMUM exige -> les 2 degats sont quand meme infliges",
       "« deal X damage divided among enemies you choose » : l'action oblige a repartir les X (RR DEAL DAMAGE), pas a en perdre",
       en_jeu(SBIRE) + [TINY, "Puzzle.ChangeToFace('hp001a', 'hp001c')"] + en_jeu("hp012"), ["Puzzle.Action('hp012', 'HeroAction')"],
       {"exhausted": ["hp012"], "hp_formes": 2, "hp_degats_somme": [[VILAIN, SBIRE], 2]},
       main_exclusive=["01088"]),
    _c("hp012 The Stinger : TEMOIN X = 0 (forme prise au tour precedent : compteur remis a zero par `NewTurnWorldStat`) -> l'Action se resout sans erreur, aucun degat",
       "« X = formes changees CE tour » : 0 au tour suivant ; la plage de cibles (0 a 0) ne doit ni bloquer ni planter",
       [TINY, "Puzzle.NewTurnWorldStat()"] + en_jeu("hp012"), ["Puzzle.Action('hp012', 'HeroAction')"],
       {"exhausted": ["hp012"], "hp_formes": 0, "hp_degats_somme": [[VILAIN], 0]},
       main_exclusive=["01088"], accepter_choix=True),
    _c("hp009 Bio-Synthetic Wings : TEMOIN X = 0 (forme prise au tour precedent : compteur remis a zero par `NewTurnWorldStat`) -> l'Action se resout sans erreur, aucune menace retiree",
       "« X = formes changees CE tour » : 0 au tour suivant ; la plage de cibles (0 a 0) ne doit ni bloquer ni planter",
       [f"Puzzle.SetThreat('{COMPLOT}', 6)", TINY, "Puzzle.NewTurnWorldStat()"] + en_jeu("hp009"), ["Puzzle.Action('hp009', 'HeroAction')"],
       {"exhausted": ["hp009"], "hp_formes": 0, "menace_min": [[COMPLOT, 6]]},
       main_exclusive=["01088"], accepter_choix=True),
    # hp013 : tout ce qui precede la fleche est le COUT (COST ARROW ICON) ; a 5 compteurs, « find Shadow of the Past ».
    _c("hp013 Identity Crisis : TEMOIN Hank Pym deja incline -> le cout n'est pas payable, l'Action n'est pas offerte (aucun degat, l'obligation reste)",
       "« Then, exhaust Hank Pym -> discard this obligation » : tout le texte avant la fleche est le cout (RR COST ARROW ICON)",
       en_jeu("hp013") + ["Puzzle.Counter('hp013', 'crisis', 2)", "Puzzle.Exhaust('hp001b')"], [],
       {"degats_identite": 0, "exhausted": ["hp001b"], "en_jeu": ["hp013"]},
       main_exclusive=["01088"], declencher_tolerant=["Puzzle.Action('hp013', 'AlterEgoAction')"]),
    _c("hp013 Identity Crisis : 2 compteurs crisis, branche MENACE -> 2 menaces sur le complot principal, aucun degat, Hank Pym incline, obligation defaussee",
       "« Choose to take 1 damage OR place 1 threat on the main scheme for each crisis counter here » : le choix fait partie du cout",
       en_jeu("hp013") + ["Puzzle.Counter('hp013', 'crisis', 2)"], ["Puzzle.Action('hp013', 'AlterEgoAction')"],
       {"degats_identite": 0, "menace": [[COMPLOT, 2]], "exhausted": ["hp001b"], "hors_jeu": ["hp013"]},
       main_exclusive=["01088"], accepter_choix=True, preferer_option="Place_1_threat"),
    _c("hp013 Identity Crisis : 5e compteur crisis, Shadow of the Past (01190) dans le deck rencontre -> elle est revelee et Ultron entre en jeu",
       "« if there are 5 or more crisis counters here, find Shadow of the Past and reveal it » (RR FIND)",
       en_jeu("hp013") + ["Puzzle.Counter('hp013', 'crisis', 4)", "Puzzle.EmptyEncounterDeck()",
                          "Puzzle.CreateEncounterDeck('01190', '01098', '01098')"], [TINY],
       {"hp_face": "hp001a", "compteurs": [["hp013", "crisis", 5]], "en_jeu": ["hp015"]},
       main_exclusive=["01088"], accepter_choix=True),
    _c("hp013 Identity Crisis : TEMOIN 4 compteurs seulement -> Shadow of the Past n'est pas cherchee",
       "« if there are 5 or more crisis counters » : a 4, rien",
       en_jeu("hp013") + ["Puzzle.Counter('hp013', 'crisis', 3)", "Puzzle.EmptyEncounterDeck()",
                          "Puzzle.CreateEncounterDeck('01190', '01098', '01098')"], [TINY],
       {"hp_face": "hp001a", "compteurs": [["hp013", "crisis", 4]], "hors_jeu": ["hp015"], "dans_deck_rencontre": ["01190"]},
       main_exclusive=["01088"], accepter_choix=True),
    _c("hp013 Identity Crisis : 5e compteur, AUCUNE Shadow of the Past, Pursued by the Past (45075a) en jeu -> 7 compteurs pursuit lui sont poses (il se retourne, revele Ultron, se retourne de nouveau)",
       "« If you cannot, place 7 pursuit counters on Pursued by the Past » : 7 >= 3 + nombre de joueurs, 45075a se retourne",
       en_jeu("hp013") + ["Puzzle.PutIntoPlay('45075a,45075b', under_control=True)", "Puzzle.Counter('hp013', 'crisis', 4)",
                          "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01098', '01098', '01098')"], [TINY],
       {"hp_face": "hp001a", "compteurs": [["hp013", "crisis", 5], ["45075a", "pursuit", 0]], "en_jeu": ["hp015"]},
       main_exclusive=["01088"], accepter_choix=True),
    _c("hp013 Identity Crisis : 5e compteur, ni Shadow of the Past ni Pursued by the Past -> rien ne se passe, aucune erreur",
       "« find ... If you cannot, place 7 pursuit counters on Pursued by the Past » : sans cette carte en jeu, rien a poser",
       en_jeu("hp013") + ["Puzzle.Counter('hp013', 'crisis', 4)", "Puzzle.EmptyEncounterDeck()",
                          "Puzzle.CreateEncounterDeck('01098', '01098', '01098')"], [TINY],
       {"hp_face": "hp001a", "compteurs": [["hp013", "crisis", 5]], "hors_jeu": ["hp015"]},
       main_exclusive=["01088"], accepter_choix=True),
    # hp016 : UNE seule copie de Seized Control dans la partie (set nemesis + BeginGameWithSetAside).
    _c("hp016 Seized Control : une seule copie existe dans la partie au demarrage (pas de doublon set nemesis / mis de cote)",
       "« Seized Control est mis de cote au Setup » : ni dans le set nemesis, ni en double",
       [], [], {"hp_exemplaires": [["hp016", 1], ["hp015", 1]]}, main_exclusive=["01088"]),
    # hp017 : « HACKED minion » ; le surge n'est PAS imprime sur la carte.
    _c("hp017 Take Over Signal : l'allie traite en sbire porte le trait HACKED",
       "« Treat attached ally as a HACKED minion with a blank text box »",
       en_jeu("hp002"), ["Puzzle.Reveal('hp017')"],
       {"hotes": [["hp017", "minion"]], "hp_hote_trait": [["hp017", "HACKED"]]}, main_exclusive=["01088"]),
    _c("hp017 Take Over Signal : aucun allie en jeu ni dans le deck -> PAS de surge (non imprime), la carte est defaussee",
       "le texte imprime n'a aucun surge : « Otherwise, seek an ally from your deck. Put that ally into play ... »",
       ["Puzzle.EmptyPlayerDeck()"], ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01103')", "Puzzle.Reveal('hp017')"],
       {"dans_deck_rencontre": ["01103"], "hors_jeu": ["hp017"], "aucune_en_resolution": True}, main_exclusive=["01088"]),
    _c("hp017 Take Over Signal : aucun allie en jeu, un allie (Ant-Man) dans le deck -> il entre en jeu, la carte s'y attache, il porte HACKED",
       "« Otherwise, seek an ally from your deck. Put that ally into play engaged with you with Take Over Signal attached to it »",
       ["Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('hp002', '01088', '01088')"], ["Puzzle.Reveal('hp017')"],
       {"en_jeu": ["hp017"], "hotes": [["hp017", "minion"]], "hp_hote_trait": [["hp017", "HACKED"]]}, main_exclusive=["01088"]),
]


VERIFICATIONS = r'''
def hp_etat(monde, aides):
    """Cles propres : `hp_face` (card_id de la face courante de l'identite), `hp_formes` (formes changees CE tour),
    `hp_attr` ([[card_id, attribut, valeur]] lus en jeu), `hp_stats` ({attribut: valeur} de l'identite),
    `hp_pas_de_changement_libre` (aucune option « Change To » offerte), `hp_formes_menace` / `hp_formes_degats`
    (menace retiree / degats infliges == formes changees ce tour), `hp_hote_trait` ([[carte, TRAIT]] porte par l'hote
    d'une carte attachee), `hp_exemplaires` ([[card_id, n]] exemplaires dans la partie, toutes zones), `hp_degats_somme`
    ([[card_id...], n] degats cumules), `hp_menace_nulle_ou_absente` ([card_id...] manigance annexe a 0 menace OU deja defaussee) ; le reste va a etat_attendu."""
    cas = aides["cas"]
    attendu = cas.get("attendu") or {}
    soucis = []
    identite = aides["identite"](monde)
    if attendu.get("hp_face") and identite.paper.card_id != attendu["hp_face"]:
        soucis.append(f"face courante {identite.paper.card_id} (attendu {attendu['hp_face']})")
    joueur = monde.players[0]
    formes = monde.stat.CountFormChanges(joueur)
    if "hp_formes" in attendu and formes != attendu["hp_formes"]:
        soucis.append(f"{formes} changement(s) de forme ce tour (attendu {attendu['hp_formes']})")
    for card_id, nom, valeur in attendu.get("hp_attr") or []:
        face = aides["par_id"](monde, card_id)
        if face is None:
            soucis.append(f"{card_id} introuvable en jeu (hp_attr)")
        else:
            courant = getattr(face, nom, None)
            if courant != valeur:
                soucis.append(f"{card_id}.{nom} = {courant} (attendu {valeur})")
    for nom, valeur in (attendu.get("hp_stats") or {}).items():
        courant = getattr(identite, nom, None)
        if courant != valeur:
            soucis.append(f"{nom} = {courant} (attendu {valeur})")
    if attendu.get("hp_pas_de_changement_libre"):
        vues = [str(n) for n in aides["etat"].get("options_vues_mise_en_place", []) if n]
        libres = [n for n in vues if n.startswith("Change")]
        if not vues:
            soucis.append("aucune option vue avant le tour (options_attendues_mise_en_place)")
        if libres:
            soucis.append(f"changement de forme libre offert : {libres}")
    if attendu.get("hp_formes_menace"):
        from game.operate.worlds import Worlds
        complot = aides["par_id"](monde, attendu["hp_formes_menace"])
        reste = 6 - complot.threat
        if reste != formes:
            soucis.append(f"menace retiree {reste} (attendu {formes} = formes changees)")
    for carte_id, trait in attendu.get("hp_hote_trait") or []:
        carte = aides["par_id"](monde, carte_id)
        hote = getattr(carte, "bind_face", None)
        if carte is None or hote is None:
            soucis.append(f"{carte_id} n'est accrochee a aucun hote (hp_hote_trait)")
        elif not hote.HasTrait(trait):
            soucis.append(f"l'hote de {carte_id} n'a pas le trait {trait} (traits : {list(hote.traits)})")
    for card_id, n_voulu in attendu.get("hp_exemplaires") or []:
        n = sum(1 for objet in monde.object_manager.card_dict.values()
                if objet.face is not None and getattr(objet.face.paper, "card_id", None) == card_id)
        if n != n_voulu:
            soucis.append(f"{n} exemplaire(s) de {card_id} dans la partie (attendu {n_voulu})")
    if attendu.get("hp_degats_somme"):
        ids, total_voulu = attendu["hp_degats_somme"]
        total = 0
        for card_id in ids:
            face = aides["par_id"](monde, card_id)
            if face is not None:
                total += face.max_health - face.health
        if total != total_voulu:
            soucis.append(f"{total} degat(s) au total sur {ids} (attendu {total_voulu})")
    for card_id in attendu.get("hp_menace_nulle_ou_absente") or []:
        face = aides["par_id"](monde, card_id)
        if face is not None and face.threat != 0:
            soucis.append(f"{card_id} porte encore {face.threat} menace(s) (attendu 0 ou carte defaussee)")
    if attendu.get("hp_ultron_absent") and aides["par_id"](monde, "hp015") is not None:
        soucis.append("Ultron est en jeu alors que la carte devait gagner surge")
    reste = {k: v for k, v in attendu.items() if not k.startswith("hp_")}
    if attendu.get("hp_formes_degats"):
        reste["degats"] = [[attendu["hp_formes_degats"], formes]]
    copie = dict(aides); copie["cas"] = dict(cas); copie["cas"]["attendu"] = reste
    ok, message = etat_attendu(monde, copie)
    if not ok:
        soucis.append(message)
    if soucis:
        return False, " ; ".join(soucis)
    return True, message
'''
