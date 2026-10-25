# Cas test_capacites de la variante SHE-HULK « WHY NOT » (Merlin, prefixe `wn`) :
# noms prefixes « [wn] » puis le card_id (substituer_pack.py filtre dessus).
#
# Rappels de montage :
#  - le deck she_hulk_why_not demarre en ALTER EGO (wn001b Jennifer Walters) ;
#    `Puzzle.ChangeToFace('wn001b', 'wn001a')` la passe en HEROS SANS declencher
#    « Do You Even Lift? » ; `Puzzle.ChangeForm('wn001b')` la declenche ;
#  - Rhino 01094 est le vilain, 01097b son complot principal (menace 0 au depart),
#    01101 Hydra Mercenary un sbire (3 PV, Guard), 01109 Bomb Scare une manigance
#    annexe a 1 icone Acceleration imprimee ;
#  - ressources : 01088 Energy = YY, 01089 Genius = BB, 01090 Strength = RR ;
#    01020 Hellcat (RES G) ne rapporte qu'UNE ressource : 01090 + 01020 = 3 pile ;
#  - allies des Team-Up : 40024 Deadpool, 01050 Hulk, 13019 Spider-Man.
SC = "rhino"
HEROS = "Puzzle.ChangeToFace('wn001b', 'wn001a')"
CIVIL = "Puzzle.ChangeToFace('wn001a', 'wn001b')"


def menace_de_depart(n):
    # ⚠ En ALTER EGO, « I Object! » (wn001b) previent 1 des menaces que pose la
    # mise en place elle-meme, et consomme sa limite de la phase (vu au journal :
    # SetThreat 5 -> « recoit 4 »). On pose donc la menace en forme HEROS, puis on
    # revient en alter ego par ChangeToFace (aucune capacite declenchee).
    return [HEROS, f"Puzzle.SetThreat('01097b', {n})", CIVIL]
SANS_BOOST = ["Puzzle.EmptyEncounterDeck()",
              "Puzzle.CreateEncounterDeck('01098', '01098', '01098', '01098', '01098', '01098', '01098', '01098')"]
COMPLOT = "01097b"
VILAIN = "01094"
SBIRE = "01101"


def en_jeu(*ids):
    return [f"Puzzle.PutIntoPlay('{i}', under_control=True)" for i in ids]


def _c(nom, pourquoi, mise, declencher, attendu, **cle):
    mise = SANS_BOOST + list(mise)
    cas = {"nom": "[wn] " + nom, "pourquoi": pourquoi, "scenario": cle.pop("scenario", SC),
           "heros": cle.pop("heros", "she_hulk_why_not"), "mise_en_place": mise, "declencher": declencher,
           "verifier": cle.pop("verifier", "wn_etat"), "attendu": attendu}
    cas.setdefault("regles", ["v16_all", "v18_all"])
    cas.update(cle)
    return cas


CAS = [
    # ============================================================ wn001a She-Hulk : Do You Even Lift?
    _c("wn001a Do You Even Lift? : 2 pions Acceleration sur le complot -> 2 degats a Rhino",
       "« deal 1 damage to an enemy for each [acceleration] icon in play » ; les pions comptent (decision du 25/10/2026)",
       [f"Puzzle.Token('{COMPLOT}', 'acceleration_token', 2)"], ["Puzzle.ChangeForm('wn001b')"],
       {"forme": "Hero", "degats": [[VILAIN, 2]]}, main_exclusive=["01090"], cibles=[VILAIN], accepter_choix=True),
    _c("wn001a Do You Even Lift? : une manigance a icone Acceleration imprimee (Bomb Scare) -> 1 degat",
       "les icones IMPRIMEES comptent aussi : Bomb Scare 01109 porte 1 [acceleration]",
       en_jeu("01109"), ["Puzzle.ChangeForm('wn001b')"],
       {"forme": "Hero", "degats": [[VILAIN, 1]]}, main_exclusive=["01090"], cibles=[VILAIN], accepter_choix=True),
    _c("wn001a Do You Even Lift? : icone imprimee + 2 pions -> 3 degats (les deux sources s'additionnent)",
       "chaque icone et chaque pion compte pour 1",
       en_jeu("01109") + [f"Puzzle.Token('{COMPLOT}', 'acceleration_token', 2)"], ["Puzzle.ChangeForm('wn001b')"],
       {"forme": "Hero", "degats": [[VILAIN, 3]]}, main_exclusive=["01090"], cibles=[VILAIN], accepter_choix=True),
    _c("wn001a Do You Even Lift? : CONTRE-CAS aucune icone en jeu -> aucun degat",
       "0 icone : rien a infliger (vert aussi sans module : contre-cas d'absence assume)",
       [], ["Puzzle.ChangeForm('wn001b')"],
       {"forme": "Hero", "degats": [[VILAIN, 0]]}, main_exclusive=["01090"], cibles=[VILAIN], accepter_choix=True),
    _c("wn001a She-Hulk : valeurs imprimees PV 15, ATK 3, THW 1, DEF 2, AVENGER GAMMA",
       "nombres texte <-> code (scan) : HAND SIZE 4 / HIT POINTS 15",
       [HEROS], [], {"pv_max": [["wn001a", 15]], "traits": ["AVENGER", "GAMMA"],
                     "wn_stats": {"attack": 3, "thwart": 1, "defense": 2, "hand_size": 4}},
       main_exclusive=["01090"]),

    # ============================================================ wn001b Jennifer Walters : I Object!
    _c("wn001b I Object! : Rhino manigance (1) -> la menace est prevenue",
       "« When threat would be placed on a scheme, prevent 1 of that threat »",
       menace_de_depart(1), [f"Puzzle.Scheme('{VILAIN}')"],
       {"forme": "AlterEgo", "menace": [[COMPLOT, 1]]}, main_exclusive=["01090"], accepter_choix=True),
    _c("wn001b I Object! : TEMOIN D'EPUISEMENT, deux manigances dans la meme phase -> la seconde passe",
       "« (Limit once per phase.) » : 1 + 0 + 1 = 2",
       menace_de_depart(1), [f"Puzzle.Scheme('{VILAIN}')", f"Puzzle.Scheme('{VILAIN}')"],
       {"forme": "AlterEgo", "menace": [[COMPLOT, 2]]}, main_exclusive=["01090"], accepter_choix=True),
    _c("wn001b Jennifer Walters : valeurs imprimees PV 15, REC 5, ATTORNEY GAMMA",
       "nombres texte <-> code (scan) : HAND SIZE 6 / HIT POINTS 15 / REC 5",
       [], [], {"pv_max": [["wn001b", 15]], "traits": ["ATTORNEY", "GAMMA"],
                "wn_stats": {"recover": 5, "hand_size": 6}},
       main_exclusive=["01090"]),

    # ============================================================ wn002 Gamma Slam
    _c("wn002 Gamma Slam : 5 degats subis -> 5 degats a Rhino, payee avec 3 ressources (cout 3)",
       "« Deal X damage to an enemy. X is the amount of damage you have sustained » ; cout 3 (4 sur l'officielle) : "
       "01090 (2) + 01020 Hellcat (1) = 3, insuffisant pour 4",
       [HEROS, "Puzzle.Damage('wn001a', 5)"], [],
       {"degats": [[VILAIN, 5]], "absent_main": ["wn002"]},
       main_exclusive=["wn002", "01090", "01020"], jouer=["wn002"], payer_avec=["01090", "01020"],
       cibles=[VILAIN], accepter_choix=True),

    # ============================================================ wn003 Ground Stomp
    _c("wn003 Ground Stomp : 2 degats a CHAQUE ennemi (Rhino et le sbire)",
       "« Deal 2 damage to each enemy » (1 sur l'officielle)",
       [HEROS, f"Puzzle.PutIntoPlay('{SBIRE}')"], [],
       {"degats": [[VILAIN, 2], [SBIRE, 2]]},
       main_exclusive=["wn003", "01090"], jouer=["wn003"], payer_avec=["01090"], accepter_choix=True),

    # ============================================================ wn004 Legal Practice
    _c("wn004 Legal Practice : 2 cartes defaussees -> 4 menaces retirees",
       "« remove 2 threat from a scheme for each card discarded this way » (1 sur l'officielle) : 6 - 4 = 2",
       menace_de_depart(6), [],
       {"menace": [[COMPLOT, 2]], "taille_main": 0},
       main_exclusive=["wn004", "01090", "01089"], jouer=["wn004"], cibles=[COMPLOT], accepter_choix=True),
    _c("wn004 Legal Practice : trait SKILL seul (THWART barre par l'auteur)",
       "« SKILL. ~~THWART~~ » : la carte n'est plus une carte [[THWART]] (lue EN MAIN : un evenement n'est jamais en jeu)",
       [], [],
       {"wn_traits_main": [["wn004", ["SKILL"]]]}, main_exclusive=["wn004", "01090"]),

    # ============================================================ wn005 Split Personality
    _c("wn005 Split Personality : change de forme, pioche jusqu'a 6, et REDRESSE l'identite",
       "« Change your form. Then, draw up to your printed hand size. Ready your identity. »",
       [HEROS, "Puzzle.Exhaust('wn001a')"], [],
       {"forme": "AlterEgo", "pret": ["wn001b"], "taille_main": 6},
       main_exclusive=["wn005", "01090", "01020"], jouer=["wn005"], payer_avec=["01090", "01020"], accepter_choix=True),

    # ============================================================ wn006 Superhuman Law Division
    _c("wn006 Superhuman Law Division : inclinee + [mental] -> 3 menaces retirees",
       "« Exhaust ... and spend a [mental] resource -> remove 3 threat from a scheme » (2 sur l'officielle) : 5 - 3 = 2",
       en_jeu("wn006") + menace_de_depart(5), ["Puzzle.Action('wn006', 'AlterEgoAction')"],
       {"menace": [[COMPLOT, 2]], "exhausted": ["wn006"]},
       main_exclusive=["01089"], payer_avec=["01089"], cibles=[COMPLOT], accepter_choix=True),

    # ============================================================ wn007 Focused Rage
    _c("wn007 Focused Rage : inclinee + 1 degat -> 1 carte piochee",
       "« Exhaust Focused Rage and take 1 damage -> draw 1 card »",
       [HEROS] + en_jeu("wn007"), ["Puzzle.Action('wn007', 'HeroAction')"],
       {"exhausted": ["wn007"], "degats_identite": 1, "taille_main": 2},
       main_exclusive=["01090"], accepter_choix=True),
    _c("wn007 Focused Rage : cout 2, jouable avec une seule carte double (01090 = 2)",
       "cout 2 (3 sur l'officielle) : 01090 seule suffit",
       [HEROS], [], {"en_jeu": ["wn007"]},
       main_exclusive=["wn007", "01090"], jouer=["wn007"], payer_avec=["01090"], accepter_choix=True),

    # ============================================================ wn008 Superhuman Strength
    _c("wn008 Superhuman Strength : +2 ATK, l'attaque sonne Rhino et la carte se defausse",
       "« She-Hulk gets +2 ATK. Forced Response: After She-Hulk attacks, discard ... -> stun the attacked enemy. » 3 + 2 = 5",
       [HEROS] + en_jeu("wn008"), ["Puzzle.Attack('wn001a')"],
       {"degats": [[VILAIN, 5]], "statuts": [[VILAIN, "Stunned"]], "hors_jeu": ["wn008"]},
       main_exclusive=["01090"], cibles=[VILAIN], accepter_choix=True),
    _c("wn008 Superhuman Strength : l'ennemi attaque est VAINCU -> personne a sonner, la carte RESTE",
       "note de l'auteur « If you have no one to stun, you cannot discard it » (decision du 25/10/2026) : "
       "le sbire (3 PV) meurt sous 5 degats",
       [HEROS, f"Puzzle.PutIntoPlay('{SBIRE}')"] + en_jeu("wn008"), ["Puzzle.Attack('wn001a')"],
       {"en_jeu": ["wn008"], "hors_jeu": [SBIRE]},
       main_exclusive=["01090"], cibles=[SBIRE], accepter_choix=True),

    # ============================================================ wn009 Hey you!
    _c("wn009 Hey you! : Deadpool en jeu -> Rhino sonne ET desoriente, la carte est retiree de la partie",
       "« Team-Up (Deadpool and She-Hulk). Action: Stun and confuse an enemy. Remove Hey you! from the game. »",
       [HEROS] + en_jeu("40024"), [],
       {"statuts": [[VILAIN, "Stunned"], [VILAIN, "Confused"]], "retirees": ["wn009"]},
       main_exclusive=["wn009", "01090"], jouer=["wn009"], cibles=[VILAIN], accepter_choix=True),
    _c("wn009 Hey you! : TEMOIN Team-Up, sans Deadpool en jeu -> injouable",
       "« Team-Up (Deadpool and She-Hulk) » : la carte reste en main",
       [HEROS], [], {}, main_exclusive=["wn009", "01090"], jouer=["wn009"], accepter_choix=True,
       verifier="hellcat_carte_restee_en_main", restee="wn009"),

    # ============================================================ wn010 Gamma Power
    _c("wn010 Gamma Power : Hulk en jeu, deux ennemis -> une carte Sonne chacun, carte retiree de la partie",
       "« Place a total of 2 stun status cards on up to 2 enemies. Remove Gamma Power from the game. »",
       [HEROS, f"Puzzle.PutIntoPlay('{SBIRE}')"] + en_jeu("01050"), [],
       {"statuts": [[VILAIN, "Stunned"], [SBIRE, "Stunned"]], "retirees": ["wn010"]},
       main_exclusive=["wn010", "01090"], jouer=["wn010"], cibles=[VILAIN, SBIRE], accepter_choix=True),
    _c("wn010 Gamma Power : TEMOIN Team-Up, sans Hulk en jeu -> injouable",
       "« Team-Up (Hulk and She-Hulk) » : la carte reste en main",
       [HEROS], [], {}, main_exclusive=["wn010", "01090"], jouer=["wn010"], accepter_choix=True,
       verifier="hellcat_carte_restee_en_main", restee="wn010"),

    # ============================================================ wn011 A Spider on the Wall
    _c("wn011 A Spider on the Wall : Spider-Man en jeu -> She-Hulk redressee, 3 cartes piochees, carte retiree",
       "« Ready She-Hulk and draw 3 cards. Remove A Spider on the Wall from the game. »",
       [HEROS, "Puzzle.Exhaust('wn001a')"] + en_jeu("13019"), [],
       {"pret": ["wn001a"], "taille_main": 4, "retirees": ["wn011"]},
       main_exclusive=["wn011", "01090"], jouer=["wn011"], accepter_choix=True),
    _c("wn011 A Spider on the Wall : TEMOIN Team-Up, sans Spider-Man en jeu -> injouable",
       "« Team-Up (She-Hulk and Spider-Man) » : la carte reste en main",
       [HEROS], [], {}, main_exclusive=["wn011", "01090"], jouer=["wn011"], accepter_choix=True,
       verifier="hellcat_carte_restee_en_main", restee="wn011"),
]


VERIFICATIONS = r'''
def wn_etat(monde, aides):
    """Cles propres : `retirees` (card_id dans la zone retiree du jeu), `wn_sans_trait` ([[card_id, trait]] :
    la carte en jeu ne porte PAS ce trait), `wn_stats` ({attribut: valeur} lus sur l'identite) ; le reste va a etat_attendu."""
    cas = aides["cas"]
    attendu = cas.get("attendu") or {}
    soucis = []
    ids = [getattr(f.paper, "card_id", None) for f in monde.area_removed.Get(True)]
    for c in attendu.get("retirees") or []:
        if c not in ids:
            soucis.append(f"{c} pas retiree du jeu (retirees = {ids})")
    for card_id, trait in attendu.get("wn_sans_trait") or []:
        face = aides["par_id"](monde, card_id)
        if face is None:
            soucis.append(f"{card_id} introuvable en jeu (wn_sans_trait)")
        elif face.HasTrait(trait):
            soucis.append(f"{card_id} porte encore le trait {trait}")
    identite = aides["identite"](monde)
    for nom, valeur in (attendu.get("wn_stats") or {}).items():
        courant = getattr(identite, nom, None)
        if courant != valeur:
            soucis.append(f"{nom} = {courant} (attendu {valeur})")
    # `wn_traits_main` : [[card_id, [traits exacts]]] d'une carte EN MAIN (un evenement n'est jamais en jeu).
    main = {getattr(f.paper, "card_id", None): f for f in monde.players[0].hand_cards.Get()}
    for card_id, traits in attendu.get("wn_traits_main") or []:
        face = main.get(card_id)
        if face is None:
            soucis.append(f"{card_id} absente de la main (wn_traits_main)")
            continue
        for t in ("SKILL", "THWART", "ATTACK", "SUPERPOWER", "GAMMA", "TACTIC"):
            if face.HasTrait(t) != (t in traits):
                soucis.append(f"{card_id} : trait {t} {'present' if face.HasTrait(t) else 'absent'} (attendu {traits})")
    reste = {k: v for k, v in attendu.items() if k not in ("retirees", "wn_sans_trait", "wn_stats", "wn_traits_main")}
    copie = dict(aides); copie["cas"] = dict(cas); copie["cas"]["attendu"] = reste
    ok, message = etat_attendu(monde, copie)
    if not ok:
        soucis.append(message)
    if soucis:
        return False, " ; ".join(soucis)
    return True, message
'''
