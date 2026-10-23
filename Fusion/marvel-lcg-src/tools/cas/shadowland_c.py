# Cas test_capacites du scenario 3 de Shadowland, « Heart of Shadow » (sl057-sl071, Krahllak), agent c. Prefixe de nom `[slc]`.
# Les cas tournent sur le scenario REEL `heart_of_shadow` (standard) ou `heart_of_shadow_expert` : la mise en place (sl060a) met une Creeping Corruption en jeu pour chaque joueur.
# ⚠ MONTAGE DE TEST MINIMAL : la Creeping Corruption sl072a/b appartient au set BLACK FLOWER (agent d, autre branche) ; elle n'a ICI aucun script (pas de retournement a 5 jetons, pas d'action).
#   Elle n'est qu'une carte portant des jetons `corruption`, mise en jeu par le Setup de sl060a. Le retournement / la defaite a 5 jetons ne sont PAS testes ici.
# Seed 42 : voir `Worlds.FindVillain` -> Krahllak (I) sl057 en standard, Krahllak (II) sl058 en expert.
HEROS = "spider_man"
FORME_HEROS = "Puzzle.ChangeForm('01001b')"
# Deck de rencontre sans boost (3 x 01105) : les degats mesures sont ceux de l'ATQ imprimee, sans icone de boost ; l'identite est INCLINEE pour ne pas defendre.
RIEN = ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01105', '01105', '01105')"]
# Pour une PHASE DU MECHANT complete : 3 x 01105 (le Surge reboucle des que le vilain a deja un Tough) feraient planter le harnais (`AssertionError is_revealing` dans can_surge), et un deck vide
# fige l'activation du vilain. Une seule 01112 False Alarm (boost 1, « you are confused », surge seulement si DEJA confus) : elle est le boost de l'activation (+1), puis la carte donnee et revelee.
VIDE = ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01112')"]
INCLINEE = "Puzzle.Exhaust('01001a')"


def _h(nom, pourquoi, mise, declencher, attendu, forme_heros=True, scenario="heart_of_shadow", **cle):
    cas = {"nom": "[slc] " + nom, "pourquoi": pourquoi, "scenario": scenario, "heros": HEROS,
           "mise_en_place": [*([FORME_HEROS] if forme_heros else []), *mise], "declencher": declencher, "verifier": "slc_etat", "attendu": attendu,
           "main_exclusive": cle.pop("main_exclusive", ["01088"])}
    cas.update(cle)
    return cas


def _r(nom, pourquoi, mise, declencher, attendu, forme_heros=True, **cle):
    """Cas SANS Creeping Corruption : le scenario `rhino` ne la met pas en jeu (temoin « le joueur n'en a pas »)."""
    return _h(nom, pourquoi, [*RIEN, *mise], declencher, attendu, forme_heros=forme_heros, scenario="rhino", **cle)


def _cc(n):
    """Pose `n` jetons corruption sur la Creeping Corruption du premier joueur (etat de depart du cas)."""
    return f"Puzzle.PlaceCounters('sl072a', 'corruption', {n})"


ATTAQUE = "Puzzle.EnemyAttacks('{}', '01001a')"
OPT_PLACER = "Place_1_corruption_counter_on_your_Creeping_Corruption"

CAS = [
    # ------------------------------------------------------------------------------------------------------ sl060a : mise en place
    _h("sl060a Setup : chaque joueur a SA Creeping Corruption en jeu (solo : 1)", "« Each player puts a Creeping Corruption upgrade into play »",
       [], [], {"corruption": [0]}, forme_heros=False),
    _h("sl060a Setup a DEUX joueurs : chacun a sa Creeping Corruption (2 cartes distinctes), les deux autres exemplaires restent de cote", "UNE par joueur, pas deux pour le premier",
       [], [], {"corruption": [0, 0], "cc_en_jeu": 2, "cc_de_cote": 2}, forme_heros=False, heros2="spider_man", main_exclusive=["01088", "01089"]),
    _h("sl060a Setup : le vilain en jeu est Krahllak (I) sl057 en standard, 18 PV par joueur", "« Contents : Krahllak (I) and Krahllak (II) »",
       [], [], {"en_jeu": ["sl057", "sl060b"], "pv_max": [["sl057", 18]]}, forme_heros=False),
    _h("sl060a Setup en EXPERT : le vilain en jeu est Krahllak (II) sl058 (21 PV par joueur)", "« (Krahllak (II) and Krahllak (III) instead for expert mode.) »",
       [], [], {"en_jeu": ["sl058", "sl060b"], "pv_max": [["sl058", 21]]}, forme_heros=False, scenario="heart_of_shadow_expert"),
    # ------------------------------------------------------------------------------------------------------ sl057 : Krahllak (I)
    _h("sl057 attaque le joueur, il accepte : 1 jeton pose, ATQ 3 - 3 = 0 degat", "« you may place 1 corruption counter ... If you do, Krahllak gets -3 ATK for this attack »",
       [*RIEN, INCLINEE], [ATTAQUE.format("sl057")], {"corruption": [1], "degats_identite": 0}, questions_presentes=["Interrupt"]),
    _h("sl057 attaque le joueur, il REFUSE : aucun jeton, 3 degats", "« you MAY » : facultatif",
       [*RIEN, INCLINEE], [ATTAQUE.format("sl057")], {"corruption": [0], "degats_identite": 3}, passer_sur_option="Interrupt"),
    _r("sl057 sans Creeping Corruption : rien a proposer, 3 degats (temoin)", "pas de Creeping Corruption -> pas d'Interruption possible",
       ["Puzzle.PutIntoPlay('sl057')", INCLINEE], [ATTAQUE.format("sl057")], {"degats_identite": 3}, questions_absentes=["Interrupt"]),
    _h("sl057 attaque un ALLIE : c'est une attaque contre le joueur (RR 1.8 p.10), l'Interruption part : jeton, ATQ 3 - 3 = 0, l'allie ne subit rien", "« When Krahllak attacks you » : le controleur de l'allie est le joueur attaque (decision du moteur, voir DECISIONS-c.md)",
       [*RIEN, INCLINEE, "Puzzle.PutIntoPlay('01075', under_control=True)"], ["Puzzle.EnemyAttacks('sl057', '01075')"], {"corruption": [1], "degats": [["01075", 0]], "degats_identite": 0}),
    _h("sl057 : SCH 2 / ATQ 3 / 18 PV par joueur et 36 PV a deux joueurs", "valeurs imprimees (cards.json) : Steady lu dans desc",
       [], [], {"pv_max": [["sl057", 36]]}, forme_heros=False, heros2="spider_man", main_exclusive=["01088", "01089"]),
    # ------------------------------------------------------------------------------------------------------ sl058 : Krahllak (II)
    _h("sl058 (expert) attaque l'identite, il accepte : jeton + ATQ 4 - 3 = 1 degat", "l'Interruption est la meme que sl057",
       [*RIEN, INCLINEE], [ATTAQUE.format("sl058")], {"corruption": [1], "degats_identite": 1}, scenario="heart_of_shadow_expert"),
    _h("sl058 (expert) attaque l'identite, il refuse : ATQ 4 = 4 degats", "ATQ 4 imprimee",
       [*RIEN, INCLINEE], [ATTAQUE.format("sl058")], {"corruption": [0], "degats_identite": 4}, scenario="heart_of_shadow_expert", passer_sur_option="Interrupt"),
    _h("sl058 (expert) : ses attaques ont OVERKILL (4 degats sur Black Widow a 2 PV : l'excedent de 2 passe a l'identite)", "« [star] Krahllak's attacks gain overkill »",
       [*RIEN, INCLINEE, "Puzzle.PutIntoPlay('01075', under_control=True)"], ["Puzzle.EnemyAttacks('sl058', '01075')"],
       {"defausse": ["01075"], "degats_identite": 2}, scenario="heart_of_shadow_expert", passer_sur_option="Interrupt"),
    _h("sl058 (expert) : Toughness (carte Tough a l'entree) et Steady (cards.json)", "« Steady. Toughness. »",
       [], [], {"statuts": [["sl058", "Tough"]], "pv_max": [["sl058", 21]]}, forme_heros=False, scenario="heart_of_shadow_expert"),
    # ------------------------------------------------------------------------------------------------------ sl059 : Krahllak (III)
    _r("sl059 : Tough a l'entree, ATQ 4 PERCANT : il defausse le Tough de l'identite et inflige 4", "« Krahllak's attacks gain overkill and piercing »",
       ["Puzzle.PutIntoPlay('sl059')", INCLINEE, "Puzzle.Tough('01001a')"], [ATTAQUE.format("sl059")], {"degats_identite": 4, "statuts_absents": [["01001a", "Tough"]], "statuts": [["sl059", "Tough"]]}),
    _r("sl059, TEMOIN : un autre ennemi sans Percant (Rhino ATQ 3) est bloque par le Tough de l'identite", "le temoin prouve que c'est bien sl059 qui perce",
       [INCLINEE, "Puzzle.Tough('01001a')"], ["Puzzle.EnemyAttacks('01094', '01001a')"], {"degats_identite": 0}),
    _r("sl059 : OVERKILL aussi (4 sur Black Widow a 2 PV : 2 a l'identite)", "les deux mots-cles",
       ["Puzzle.PutIntoPlay('sl059')", INCLINEE, "Puzzle.PutIntoPlay('01075', under_control=True)"], ["Puzzle.EnemyAttacks('sl059', '01075')"], {"defausse": ["01075"], "degats_identite": 2}),
    _r("sl059 : RETALIATE 1, le heros qui l'attaque (ATQ 2, le Tough absorbe) subit 1 degat", "« Retaliate 1 » lu dans desc",
       ["Puzzle.PutIntoPlay('sl059')"], ["Puzzle.Attack('01001a')"], {"degats_identite": 1}, cibles=["sl059"]),
    _h("sl059 attaque l'identite, il accepte l'Interruption : jeton + ATQ 4 - 3 = 1 degat", "meme Interruption que sl057 et sl058",
       [*RIEN, INCLINEE, "Puzzle.AdvanceVillain()"], [ATTAQUE.format("sl059")], {"corruption": [1], "degats_identite": 1}, scenario="heart_of_shadow_expert"),

    # ------------------------------------------------------------------------------------------------------ sl060b : le stade ne s'accomplit jamais, il se vide ; Krahllak vaincu -> stade 2
    _h("sl060b, menace 6/6 : le stade n'est PAS accompli, toute la menace est retiree et le joueur choisit : 2 jetons (branche 1)", "« instead remove all threat from here and each player chooses »",
       [], ["Puzzle.SetThreat('sl060b', 5)", "Puzzle.PlaceThreat('sl060b', 1)"], {"menace": [["sl060b", 0]], "corruption": [2], "en_jeu": ["sl060b"], "partie_finie": False, "degats_identite": 0, "cartes_donnees": [0]}),
    _h("sl060b, branche 2 : 3 degats a l'identite ET 1 carte rencontre donnee face cachee, aucun jeton", "« Take 3 damage and deal themself 1 facedown encounter card »",
       [], ["Puzzle.SetThreat('sl060b', 5)", "Puzzle.PlaceThreat('sl060b', 1)"], {"menace": [["sl060b", 0]], "corruption": [0], "degats_identite": 3, "cartes_donnees": [1]},
       choisir_option="Take_3_damage_and_deal_yourself_1_facedown_encounter_card"),
    _h("sl060b, TEMOIN : 5 menaces sur 6, rien ne se passe (ni jeton, ni degats)", "le choix ne part qu'a l'accomplissement",
       [], ["Puzzle.SetThreat('sl060b', 4)", "Puzzle.PlaceThreat('sl060b', 1)"], {"menace": [["sl060b", 5]], "corruption": [0], "degats_identite": 0, "cartes_donnees": [0]}),
    _h("sl060b a DEUX joueurs : menace 12, CHACUN choisit (les deux prennent la branche 1 : 2 jetons chacun)", "« EACH player chooses »",
       [], ["Puzzle.SetThreat('sl060b', 11)", "Puzzle.PlaceThreat('sl060b', 1)"], {"menace": [["sl060b", 0]], "corruption": [2, 2]}, heros2="spider_man", main_exclusive=["01088", "01089"]),
    _h("sl060b a DEUX joueurs, branche 2 : chacun prend 3 degats et se donne UNE carte (pas deux pour le premier)", "« THEMSELF »",
       [], ["Puzzle.SetThreat('sl060b', 11)", "Puzzle.PlaceThreat('sl060b', 1)"], {"menace": [["sl060b", 0]], "corruption": [0, 0], "cartes_donnees": [1, 1], "degats_identite": 3}, heros2="spider_man", main_exclusive=["01088", "01089"],
       choisir_option="Take_3_damage_and_deal_yourself_1_facedown_encounter_card"),
    _h("sl060b : Krahllak (I) vaincu -> Krahllak (II) entre en jeu ET le complot passe au stade 2 (Beast Be Praised 2B)", "« After Krahllak is defeated, advance this scheme to stage 2A »",
       [], ["Puzzle.Damage('sl057', 999)"], {"en_jeu": ["sl058", "sl061b"], "hors_jeu": ["sl057", "sl060b"], "partie_finie": False}),
    _h("sl060b, TEMOIN : Krahllak (I) blesse mais pas vaincu, le complot reste au stade 1", "la reponse ne part qu'a la defaite",
       [], ["Puzzle.Damage('sl057', 17)"], {"en_jeu": ["sl057", "sl060b"], "hors_jeu": ["sl061b"], "partie_finie": False}),
    _h("sl060b : Krahllak (II) vaincu a son tour (standard : stade FINAL) -> les joueurs GAGNENT (le complot est deja au stade 2)", "pas de seconde avancee du complot ; le dernier stade du vilain tombe",
       [], ["Puzzle.Damage('sl057', 999)", "Puzzle.Damage('sl058', 999)", "Puzzle.Damage('sl058', 999)"], {"partie_finie": True}),
    _h("sl060b (expert) : Krahllak (II) vaincu -> Krahllak (III) entre, le complot passe a 2B (et, en expert, chaque joueur recoit 1 carte face cachee de 2A)", "« In expert mode, deal each player 1 facedown encounter card » de sl061a",
       [], ["Puzzle.Damage('sl058', 999)", "Puzzle.Damage('sl058', 999)"], {"en_jeu": ["sl059", "sl061b"], "hors_jeu": ["sl058"], "cartes_donnees": [1], "partie_finie": False}, scenario="heart_of_shadow_expert"),
    _h("sl060b (expert) : Krahllak (III), dernier stade, vaincu -> victoire", "Toughness : un 1er coup retire le Tough",
       [], ["Puzzle.Damage('sl058', 999)", "Puzzle.Damage('sl058', 999)", "Puzzle.Damage('sl059', 999)", "Puzzle.Damage('sl059', 999)"], {"partie_finie": True}, scenario="heart_of_shadow_expert"),
    # ------------------------------------------------------------------------------------------------------ sl061a : When Revealed
    _h("sl061a revelee, Creeping Corruption SANS Overpowering : le joueur defausse une carte qu'il controle (son allie) ; sa main et sa Creeping Corruption ne bougent pas", "« Each other player discards a card they control from play »",
       ["Puzzle.PutIntoPlay('01075', under_control=True)"], ["Puzzle.AdvanceMainScheme(1)"], {"defausse": ["01075"], "mains": [2], "cc_en_jeu": 1, "cartes_donnees": [0]}, main_exclusive=["01088", "01090"]),
    _h("sl061a revelee, Creeping Corruption OVERPOWERING (face b) : defausse d'UNE carte AU HASARD de la main ; l'allie reste", "« whose Creeping Corruption has the OVERPOWERING trait discards 1 random card from their hand »",
       ["Puzzle.PutIntoPlay('01075', under_control=True)", "Puzzle.Flip('sl072a')"], ["Puzzle.AdvanceMainScheme(1)"], {"mains": [1], "en_jeu": ["01075"], "cc_face": ["b"]}, main_exclusive=["01088", "01090"]),
    _h("sl061a revelee, sans Overpowering et RIEN a defausser en jeu : aucune erreur, la Creeping Corruption (Permanent) n'est pas proposee a la defausse", "« discards a card they control from play » : la Creeping Corruption est Permanent",
       [], ["Puzzle.AdvanceMainScheme(1)"], {"mains": [2], "cc_en_jeu": 1, "en_jeu": ["sl061b"]}, main_exclusive=["01088", "01090"]),
    _h("sl061a (EXPERT) : de plus, chaque joueur recoit 1 carte rencontre face cachee", "« In expert mode, deal each player 1 facedown encounter card »",
       [], ["Puzzle.AdvanceMainScheme(1)"], {"cartes_donnees": [1], "en_jeu": ["sl061b"]}, scenario="heart_of_shadow_expert"),
    _h("sl061a a DEUX joueurs : le 2e est Overpowering (perd une carte au hasard de sa main de 6, garde son allie), le 1er non (defausse son allie, garde sa main de 2)", "chaque joueur est traite selon SA Creeping Corruption",
       ["Puzzle.PutIntoPlay('01075', under_control=True)", "Puzzle.PutIntoPlay('01051', under_control=True, player=1)", "Puzzle.Flip('sl072a')"], ["Puzzle.AdvanceMainScheme(1)"],
       {"cc_face": ["a", "b"], "mains": [2, 5], "allies_en_jeu": [0, 1], "defausse": ["01075"]}, heros2="spider_man", main_exclusive=["01088", "01090"]),
    # ------------------------------------------------------------------------------------------------------ sl061b : apres l'etape 1 de la phase du mechant
    _h("sl061b, apres l'etape 1 : le joueur place 1 jeton (branche 1) : 1 jeton ; menace = 1 (escalade) + 3 (manigance de Krahllak : SCH 2 + boost 1) = 4", "« After resolving step one of the villain phase, each player chooses »",
       ["Puzzle.AdvanceMainScheme(1)", "Puzzle.SetThreat('sl061b', 0)", *VIDE], ["Puzzle.RunVillainPhase()"], {"corruption": [1], "menace": [["sl061b", 4]]}, forme_heros=False),
    _h("sl061b, branche 2 : 3 menaces SUR le complot (4 + 3 = 7), aucun jeton", "« Place 3 threat here »",
       ["Puzzle.AdvanceMainScheme(1)", "Puzzle.SetThreat('sl061b', 0)", *VIDE], ["Puzzle.RunVillainPhase()"], {"corruption": [0], "menace": [["sl061b", 7]]}, forme_heros=False, choisir_option="Place_3_threat_here"),
    _h("sl061b : accomplie (9 menaces par joueur) -> les joueurs PERDENT", "« If this stage is completed, the players lose the game »",
       ["Puzzle.AdvanceMainScheme(1)"], ["Puzzle.SetThreat('sl061b', 8)", "Puzzle.PlaceThreat('sl061b', 1)"], {"partie_finie": True}),
    _h("sl061b a DEUX joueurs : chacun choisit apres l'etape 1 (les deux prennent un jeton)", "« each player chooses »",
       ["Puzzle.AdvanceMainScheme(1)", *VIDE], ["Puzzle.RunVillainPhase()"], {"corruption": [1, 1]}, forme_heros=False, heros2="spider_man", main_exclusive=["01088", "01089"]),

    # ------------------------------------------------------------------------------------------------------ sl062 : Dark Shroud
    _h("sl062 Dark Shroud : Swinging Web Kick (8 degats d'attaque) sur Krahllak -> TOUS les degats sont empeches, 1 jeton, Dark Shroud defaussee", "« would deal 4 or more damage ... with an attack, instead prevent all of that damage, place 1 corruption counter ..., and discard this card »",
       ["Puzzle.PutIntoPlay('sl062')"], [], {"degats": [["sl057", 0]], "corruption": [1], "defausse_rencontre": ["sl062"]}, jouer=["01005"], cibles=["sl057"], main_exclusive=["01088", "01089"]),
    _h("sl062, TEMOIN : sans Dark Shroud le meme Web Kick inflige 8 degats a Krahllak", "la prevention vient bien de la carte",
       [], [], {"degats": [["sl057", 8]], "corruption": [0]}, jouer=["01005"], cibles=["sl057"], main_exclusive=["01088", "01089"]),
    _h("sl062, REFUS : l'Interruption est facultative (le joueur passe) -> Krahllak subit les 8 degats, aucun jeton, Dark Shroud reste attachee", "« Interrupt » non forcee : le joueur choisit de s'en servir",
       ["Puzzle.PutIntoPlay('sl062')"], [], {"degats": [["sl057", 8]], "corruption": [0], "attaches": [["sl057", "sl062"]]}, jouer=["01005"], cibles=["sl057"], main_exclusive=["01088", "01089"], passer_sur_option="Interrupt"),
    _h("sl062, SEUIL : une attaque de base a 2 degats (< 4) n'est pas empechee ; Dark Shroud reste attachee, aucun jeton", "« 4 or more damage »",
       ["Puzzle.PutIntoPlay('sl062')"], ["Puzzle.Attack('01001a')"], {"degats": [["sl057", 2]], "corruption": [0], "attaches": [["sl057", "sl062"]]}, cibles=["sl057"]),
    _h("sl062 : ATQ +1 pour Krahllak (3 + 1 = 4 degats a l'identite, il refuse l'Interruption de Krahllak)", "ATK+ 1 lu dans desc",
       [*RIEN, INCLINEE, "Puzzle.PutIntoPlay('sl062')"], [ATTAQUE.format("sl057")], {"degats_identite": 4, "corruption": [0]}, passer_sur_option="Interrupt"),
    # ------------------------------------------------------------------------------------------------------ sl063 : Fear Projection
    _h("sl063 Fear Projection : Krahllak gagne RETALIATE 1 (le heros qui l'attaque, ATQ 2, subit 1 degat)", "« Krahllak gains retaliate 1 »",
       ["Puzzle.PutIntoPlay('sl063')"], ["Puzzle.Attack('01001a')"], {"degats_identite": 1, "degats": [["sl057", 2]]}, cibles=["sl057"]),
    _h("sl063, TEMOIN : sans Fear Projection le meme heros n'encaisse aucune riposte", "Krahllak (I) n'a pas Retaliate lui-meme",
       [], ["Puzzle.Attack('01001a')"], {"degats_identite": 0, "degats": [["sl057", 2]]}, cibles=["sl057"]),
    _h("sl063 Hero Action : 2 jetons sur la Creeping Corruption (cout) -> Fear Projection defaussee", "« Place 2 corruption counters on your Creeping Corruption → discard this card »",
       ["Puzzle.PutIntoPlay('sl063')"], ["Puzzle.Action('sl063', 'HeroAction')"], {"corruption": [2], "defausse_rencontre": ["sl063"], "taille_attaches": [["sl057", 0]]}),
    _r("sl063 Hero Action SANS Creeping Corruption : l'action n'est pas offerte (cout impayable), la carte reste attachee", "le cout est un jeton : pas de Creeping Corruption, pas d'action",
       ["Puzzle.PutIntoPlay('sl057')", "Puzzle.PutIntoPlay('sl063')"], [], {"attaches": [["sl057", "sl063"]]}, declencher_tolerant=["Puzzle.Action('sl063', 'HeroAction')"]),
    _h("sl063 Alter-Ego Action : depenser [mental][mental][mental] -> defaussee ET 1 jeton RETIRE (2 -> 1)", "« Spend [mental][mental][mental] resources → discard this card. Remove 1 corruption counter from your Creeping Corruption. »",
       ["Puzzle.PutIntoPlay('sl063')", _cc(2)], ["Puzzle.Action('sl063', 'AlterEgoAction')"], {"corruption": [1], "defausse_rencontre": ["sl063"], "defausse": ["01089"]},
       forme_heros=False, main_exclusive=["01089", "01089"], payer_avec=["01089", "01089"]),
    _h("sl063 Alter-Ego Action, TEMOIN : ressources INSUFFISANTES ([energy] seulement) -> rien n'est depense, la carte reste, le jeton aussi", "BBB exige trois ressources mentales",
       ["Puzzle.PutIntoPlay('sl063')", _cc(2)], [], {"corruption": [2], "attaches": [["sl057", "sl063"]]},
       forme_heros=False, main_exclusive=["01088", "01088"], declencher_tolerant=["Puzzle.Action('sl063', 'AlterEgoAction')"]),
    # ------------------------------------------------------------------------------------------------------ sl064 : Mark of the Wicked
    _h("sl064 revelee, le joueur l'ATTACHE : ATQ +2 (4 degats a Krahllak) ET, apres son attaque de base, 1 jeton", "« You may attach this card to your identity » ; « [star] Forced Response : After attached hero makes a basic attack, place 1 corruption counter »",
       [], ["Puzzle.Reveal('sl064')", "Puzzle.Attack('01001a')"], {"attaches": [["01001a", "sl064"]], "degats": [["sl057", 4]], "corruption": [1]}, cibles=["sl057"]),
    _h("sl064 revelee, il REFUSE : 4 degats, identite ETOURDIE, 1 jeton RETIRE (2 -> 1), carte defaussee", "« If you do not, take 4 damage, stun your identity, remove 1 corruption counter ..., and discard this card »",
       [_cc(2)], ["Puzzle.Reveal('sl064')"], {"degats_identite": 4, "statuts": [["01001a", "Stunned"]], "corruption": [1], "defausse_rencontre": ["sl064"]}, choisir_option="Cancel"),
    _h("sl064 attachee, TEMOIN : un contre de base (pas une attaque) ne pose AUCUN jeton", "« basic ATTACK »",
       [], ["Puzzle.Reveal('sl064')", "Puzzle.Thwart('01001a')"], {"attaches": [["01001a", "sl064"]], "corruption": [0]}),
    _h("sl064 attachee, TEMOIN : l'attaque d'un ALLIE (pas « attached hero ») ne pose aucun jeton", "« attached HERO »",
       ["Puzzle.PutIntoPlay('01075', under_control=True)"], ["Puzzle.Reveal('sl064')", "Puzzle.Attack('01075')"], {"attaches": [["01001a", "sl064"]], "corruption": [0]}, cibles=["sl057"]),
    _r("sl064 revelee SANS Creeping Corruption, refus : 4 degats, etourdi, defaussee (aucun jeton a retirer, aucune erreur)", "le retrait de jeton est sans objet",
       [], ["Puzzle.Reveal('sl064')"], {"degats_identite": 4, "statuts": [["01001a", "Stunned"]], "defausse_rencontre": ["sl064"]}, choisir_option="Cancel"),
    # ------------------------------------------------------------------------------------------------------ sl065 : Pull of Power
    _h("sl065 revelee, attachee : CTR +2 (1 + 2 = 3 menaces retirees, 5 -> 2) ET, apres le contre de base, 1 jeton", "« [star] Forced Response : After attached hero makes a basic thwart, place 1 corruption counter »",
       [], ["Puzzle.SetThreat('sl060b', 5)", "Puzzle.Reveal('sl065')", "Puzzle.Thwart('01001a')"], {"attaches": [["01001a", "sl065"]], "menace": [["sl060b", 2]], "corruption": [1]}),
    _h("sl065 revelee, il REFUSE : 4 degats, identite CONFUSE, 1 jeton RETIRE (2 -> 1), carte defaussee", "« If you do not, take 4 damage, confuse your identity, remove 1 corruption counter ..., and discard this card »",
       [_cc(2)], ["Puzzle.Reveal('sl065')"], {"degats_identite": 4, "statuts": [["01001a", "Confused"]], "corruption": [1], "defausse_rencontre": ["sl065"]}, choisir_option="Cancel"),
    _h("sl065 attachee, TEMOIN : une attaque de base (pas un contre) ne pose AUCUN jeton", "« basic THWART »",
       [], ["Puzzle.Reveal('sl065')", "Puzzle.Attack('01001a')"], {"attaches": [["01001a", "sl065"]], "corruption": [0]}, cibles=["sl057"]),

    # ------------------------------------------------------------------------------------------------------ sl066 : Fist
    _h("sl066 Fist, Hero Action : 1 jeton (cout) -> 4 degats a Fist (6 PV)", "« Place 1 corruption counter on your Creeping Corruption → deal 4 damage to Fist »",
       ["Puzzle.PutIntoPlay('sl066')"], ["Puzzle.Action('sl066', 'HeroAction')"], {"corruption": [1], "degats": [["sl066", 4]]}),
    _h("sl066, deux fois : 8 degats (> 6 PV), Fist est vaincu, 2 jetons en tout", "l'action reste offerte tant que Fist est en jeu",
       ["Puzzle.PutIntoPlay('sl066')"], ["Puzzle.Action('sl066', 'HeroAction')", "Puzzle.Action('sl066', 'HeroAction')"], {"corruption": [2], "hors_jeu": ["sl066"]}),
    _r("sl066 SANS Creeping Corruption : l'action n'est pas offerte (cout impayable), Fist reste intact", "le cout est un jeton",
       ["Puzzle.PutIntoPlay('sl066')"], [], {"degats": [["sl066", 0]], "en_jeu": ["sl066"]}, declencher_tolerant=["Puzzle.Action('sl066', 'HeroAction')"]),
    _h("sl066 : RETALIATE 2 (le heros qui l'attaque, ATQ 2, subit 2 degats ; Fist en recoit 2)", "« Retaliate 2 » (cards.json corrige : 1 -> 2)",
       ["Puzzle.PutIntoPlay('sl066')"], ["Puzzle.Attack('01001a')"], {"degats_identite": 2, "degats": [["sl066", 2]]}, cibles=["sl066"]),
    _h("sl066 : PATROL, le heros engage avec Fist ne peut pas contrecarrer le complot principal (menace 2 inchangee)", "« Patrol »",
       ["Puzzle.PutIntoPlay('sl066')"], ["Puzzle.Thwart('01001a')"], {"menace": [["sl060b", 2]]}),
    _h("sl066, TEMOIN : sans Fist le meme contre retire 1 menace (2 -> 1)", "le blocage vient de Fist",
       [], ["Puzzle.Thwart('01001a')"], {"menace": [["sl060b", 1]]}),
    # ------------------------------------------------------------------------------------------------------ sl067 : Hellbride
    _h("sl067 Hellbride vaincue par le heros : 2 jetons PUIS soin de 6 (identite a 8 degats -> 2)", "« The defeating player places 2 corruption counters ..., then heals 6 damage from their identity »",
       ["Puzzle.PutIntoPlay('sl067')", "Puzzle.Damage('sl067', 5)", "Puzzle.Damage('01001a', 8)"], ["Puzzle.Attack('01001a')"], {"corruption": [2], "degats_identite": 2, "hors_jeu": ["sl067"]}, cibles=["sl067"]),
    _r("sl067 vaincue SANS Creeping Corruption : aucun jeton, le soin de 6 a quand meme lieu (aucune erreur)", "« places 2 counters » est sans objet",
       ["Puzzle.PutIntoPlay('sl067')", "Puzzle.Damage('sl067', 5)", "Puzzle.Damage('01001a', 8)"], ["Puzzle.Attack('01001a')"], {"degats_identite": 2, "hors_jeu": ["sl067"]}, cibles=["sl067"]),
    _h("sl067 vaincue par le SECOND joueur (Iron Man) : c'est LUI qui pose les 2 jetons et se soigne de 6 (le premier ne bouge pas)", "« THE DEFEATING player »",
       ["Puzzle.ChangeForm('01029b')", "Puzzle.PutIntoPlay('sl067')", "Puzzle.Damage('sl067', 6)", "Puzzle.Damage('01029a', 7)", "Puzzle.Damage('01001a', 3)"], ["Puzzle.Attack('01029a')"],
       {"corruption": [0, 2], "degats_identites": [3, 1], "hors_jeu": ["sl067"]}, heros2="iron_man", main_exclusive=["01088", "01089"], cibles=["sl067"]),
    _h("sl067 Hero Action : a 2 PV restants (5 degats sur 7), epuiser le heros -> Hellbride DEFAUSSEE (pas vaincue) ET 1 jeton RETIRE (2 -> 1)", "« If Hellbride has 2 or fewer remaining hit points, exhaust your hero → discard Hellbride. Remove 1 corruption counter »",
       ["Puzzle.PutIntoPlay('sl067')", "Puzzle.Damage('sl067', 5)", _cc(2)], ["Puzzle.Action('sl067', 'HeroAction')"], {"hors_jeu": ["sl067"], "exhausted": ["01001a"], "corruption": [1], "degats_identite": 0}),
    _h("sl067 Hero Action, TEMOIN : 3 PV restants (4 degats) -> l'action n'est PAS offerte, rien ne bouge", "« 2 or fewer remaining hit points » (restants, pas subis)",
       ["Puzzle.PutIntoPlay('sl067')", "Puzzle.Damage('sl067', 4)", _cc(2)], [], {"en_jeu": ["sl067"], "corruption": [2], "pret": ["01001a"]}, declencher_tolerant=["Puzzle.Action('sl067', 'HeroAction')"]),
    _h("sl067 Hero Action, SEUIL : 1 seul PV restant (6 degats sur 7) : offerte aussi (« 2 or FEWER »)", "« 2 or FEWER remaining hit points »",
       ["Puzzle.PutIntoPlay('sl067')", "Puzzle.Damage('sl067', 6)"], ["Puzzle.Action('sl067', 'HeroAction')"], {"hors_jeu": ["sl067"], "exhausted": ["01001a"]}),
    # ------------------------------------------------------------------------------------------------------ sl068 : Retainer
    _h("sl068 Retainer attaque l'identite, il accepte : 1 jeton, ATQ 4 - 3 = 1 degat", "meme Interruption que Krahllak",
       [*RIEN, INCLINEE, "Puzzle.PutIntoPlay('sl068')"], [ATTAQUE.format("sl068")], {"corruption": [1], "degats_identite": 1}),
    _h("sl068 Retainer attaque, il REFUSE : ATQ 4 = 4 degats, aucun jeton", "« you may »",
       [*RIEN, INCLINEE, "Puzzle.PutIntoPlay('sl068')"], [ATTAQUE.format("sl068")], {"corruption": [0], "degats_identite": 4}, passer_sur_option="Interrupt"),
    _h("sl068 : ses attaques ont OVERKILL (4 sur Black Widow a 2 PV : l'excedent de 2 passe a l'identite)", "« [star] Retainer's attacks gain overkill »",
       [*RIEN, INCLINEE, "Puzzle.PutIntoPlay('sl068')", "Puzzle.PutIntoPlay('01075', under_control=True)"], ["Puzzle.EnemyAttacks('sl068', '01075')"], {"defausse": ["01075"], "degats_identite": 2}, passer_sur_option="Interrupt"),
    _r("sl068 SANS Creeping Corruption : aucune Interruption, 4 degats", "rien a proposer",
       ["Puzzle.PutIntoPlay('sl068')", INCLINEE], [ATTAQUE.format("sl068")], {"degats_identite": 4}, questions_absentes=["Interrupt"]),
    # ------------------------------------------------------------------------------------------------------ sl069 : Snakeroot Elders
    _h("sl069 revelee, le joueur place le jeton sur SA Creeping Corruption : aucun jeton sur le sbire, ni guard ni patrol", "« You may place 1 corruption counter on your Creeping Corruption »",
       [], ["Puzzle.Reveal('sl069')"], {"corruption": [1], "compteurs": [["sl069", "corruption", 0]], "mots_cles": [["sl069", "Guard", 0], ["sl069", "Patrol", 0]]}),
    _h("sl069 revelee, il REFUSE : 1 jeton SUR le sbire, qui gagne GUARD et PATROL ; rien sur la Creeping Corruption", "« If you do not, place 1 corruption counter here »",
       [], ["Puzzle.Reveal('sl069')"], {"corruption": [0], "compteurs": [["sl069", "corruption", 1]], "mots_cles": [["sl069", "Guard", 1], ["sl069", "Patrol", 1]]}, choisir_option="Cancel"),
    _r("sl069 revelee SANS Creeping Corruption : 1 jeton sur le sbire (guard + patrol)", "impossible de placer = « if you do not »",
       [], ["Puzzle.Reveal('sl069')"], {"compteurs": [["sl069", "corruption", 1]], "mots_cles": [["sl069", "Guard", 1], ["sl069", "Patrol", 1]]}, questions_absentes=["Place 1 corruption counter"]),
    _h("sl069 avec un jeton : GUARD, le heros engage ne peut pas attaquer Krahllak (le sbire encaisse l'attaque)", "« gains guard »",
       [], ["Puzzle.Reveal('sl069')", "Puzzle.Attack('01001a')"], {"degats": [["sl057", 0], ["sl069", 2]]}, choisir_option="Cancel"),
    _h("sl069 sans jeton, TEMOIN : pas de guard, l'attaque de base va sur Krahllak (2 degats)", "le garde ne tient qu'avec un jeton",
       [], ["Puzzle.Reveal('sl069')", "Puzzle.Attack('01001a')"], {"degats": [["sl057", 2], ["sl069", 0]]}, cibles=["sl057"]),
    _h("sl069 avec un jeton : PATROL, le heros engage ne peut pas contrecarrer le complot principal (menace 2 inchangee)", "« gains ... patrol »",
       [], ["Puzzle.Reveal('sl069')", "Puzzle.Thwart('01001a')"], {"menace": [["sl060b", 2]]}, choisir_option="Cancel"),
    _h("sl069 sans jeton, TEMOIN : le contre retire 1 menace (2 -> 1)", "le patrol ne tient qu'avec un jeton",
       [], ["Puzzle.Reveal('sl069')", "Puzzle.Thwart('01001a')"], {"menace": [["sl060b", 1]]}),
    _h("sl069 : un jeton qui apparait apres coup (pose a la main) donne guard et patrol", "la valeur est relue a chaque mouvement de jeton",
       ["Puzzle.PutIntoPlay('sl069')"], ["Puzzle.PlaceCounters('sl069', 'corruption', 1)"], {"mots_cles": [["sl069", "Guard", 1], ["sl069", "Patrol", 1]]}),
    # ------------------------------------------------------------------------------------------------------ sl070 : Veil of Nightmares
    _h("sl070 revelee : menace de depart 5 par joueur (5 en solo), icone HAZARD, boost 2", "Hazard et menace lus dans desc",
       [], ["Puzzle.Reveal('sl070')"], {"menace": [["sl070", 5]], "icones": [["Hazard", 1]], "icones_boost": [["sl070", 2]]}),
    _h("sl070 revelee a DEUX joueurs : 10 menaces (5 par joueur)", "« 5[per_hero] »",
       [], ["Puzzle.Reveal('sl070')"], {"menace": [["sl070", 10]]}, heros2="spider_man", main_exclusive=["01088", "01089"]),
    _h("sl070 Hero Action : 1 jeton (cout) -> 5 menaces retirees de CETTE manigance (7 -> 2)", "« Place 1 corruption counter ... → remove 5 threat from this scheme »",
       [*RIEN, "Puzzle.PutIntoPlay('sl070')"], ["Puzzle.SetThreat('sl070', 7)", "Puzzle.Action('sl070', 'HeroAction')"], {"menace": [["sl070", 2], ["sl060b", 2]], "corruption": [1]}),
    _h("sl070 Hero Action avec 3 menaces seulement : toutes retirees (3 -> 0), la manigance est vaincue", "au plus 5",
       [*RIEN, "Puzzle.PutIntoPlay('sl070')"], ["Puzzle.SetThreat('sl070', 3)", "Puzzle.Action('sl070', 'HeroAction')"], {"corruption": [1], "hors_jeu": ["sl070"]}),
    _r("sl070 SANS Creeping Corruption : l'action n'est pas offerte (cout impayable), la menace reste a 7", "le cout est un jeton",
       ["Puzzle.PutIntoPlay('sl070')"], ["Puzzle.SetThreat('sl070', 7)"], {"menace": [["sl070", 7]]}, declencher_tolerant=["Puzzle.Action('sl070', 'HeroAction')"]),
    # ------------------------------------------------------------------------------------------------------ sl071 : Submit or Suffer
    _h("sl071 revelee, branche 1 : 1 jeton sur la Creeping Corruption, rien d'autre", "« Choose: Either place 1 corruption counter on your Creeping Corruption »",
       [*RIEN, INCLINEE], ["Puzzle.Reveal('sl071')"], {"corruption": [1], "degats_identite": 0}),
    _h("sl071 revelee, branche 2 : 1 jeton RETIRE (2 -> 1) ET Krahllak attaque (3 degats ; il refuse l'Interruption de Krahllak)", "« or remove 1 corruption counter ... and Krahllak attacks you »",
       [*RIEN, INCLINEE, _cc(2)], ["Puzzle.Reveal('sl071')"], {"corruption": [1], "degats_identite": 3},
       choisir_option="Remove_1_corruption_counter_from_your_Creeping_Corruption_and_Krahllak_attacks_you", passer_sur_option="Interrupt"),
    _r("sl071 revelee SANS Creeping Corruption : la branche « place » n'est pas offerte, Krahllak attaque (3 degats)", "branche 1 impossible",
       ["Puzzle.PutIntoPlay('sl057')", INCLINEE], ["Puzzle.Reveal('sl071')"], {"degats_identite": 3}, questions_absentes=["Place 1 corruption counter"]),
    _h("sl071 en BOOST, branche 1 : 1 jeton", "« [star] Boost : Choose: Either place 1 corruption counter ... » (le boost revele par une attaque de Krahllak : on refuse son Interruption pour ne mesurer que le boost)",
       [*RIEN, INCLINEE], ["Puzzle.Boost('sl071')"], {"corruption": [1], "statuts_absents": [["01001a", "Stunned"]]}, passer_sur_option="Interrupt"),
    _h("sl071 en BOOST, branche 2 : l'identite est ETOURDIE, aucun jeton", "« or stun your identity »",
       [*RIEN, INCLINEE], ["Puzzle.Boost('sl071')"], {"corruption": [0], "statuts": [["01001a", "Stunned"]]}, choisir_option="Stun_your_identity", passer_sur_option="Interrupt"),
    _r("sl071 en BOOST SANS Creeping Corruption : seule la branche « stun » existe, l'identite est etourdie", "branche 1 impossible",
       [INCLINEE], ["Puzzle.Boost('sl071')"], {"statuts": [["01001a", "Stunned"]]}, questions_absentes=["Place 1 corruption counter"]),
]


VERIFICATIONS = r'''
def slc_etat(monde, aides):
    """etat_attendu + cles propres au scenario Heart of Shadow :
    `corruption` : [n par joueur] = jetons `corruption` sur la Creeping Corruption de chaque joueur (dans l'ordre des joueurs) ;
    `cc_en_jeu` / `cc_de_cote` : nombre de Creeping Corruption en jeu / mises de cote ;
    `cc_face` : ["a"|"b" par joueur] = face visible de sa Creeping Corruption ; `mains` : [taille de la main par joueur] ; `cartes_donnees` : [cartes rencontre face cachee par joueur] ;
    `allies_en_jeu` : [nombre d'allies controles par joueur] ; `degats_identites` : [degats subis par l'identite de chaque joueur] ; `partie_finie` : bool ; `mots_cles` : [[card_id, mot-cle, valeur]]."""
    cas = aides["cas"]
    attendu = cas.get("attendu") or {}
    soucis = []
    ids_cc = ("sl072a", "sl072b")
    en_jeu = []
    for objet in monde.object_manager.card_dict.values():
        face = getattr(objet, "face", None)
        if face is not None and face.IsInPlay() and str(getattr(face.paper, "card_id", "")) in ids_cc:
            en_jeu.append(face)
    if "cc_en_jeu" in attendu and len(en_jeu) != attendu["cc_en_jeu"]:
        soucis.append(f"{len(en_jeu)} Creeping Corruption en jeu (attendu {attendu['cc_en_jeu']})")
    if "cc_de_cote" in attendu:
        cote = [f for f in monde.aside_deck.Get(True) if str(f.paper.card_id) in ids_cc]
        if len(cote) != attendu["cc_de_cote"]:
            soucis.append(f"{len(cote)} Creeping Corruption de cote (attendu {attendu['cc_de_cote']})")
    if "corruption" in attendu:
        vus = []
        for joueur in monde.const_players:
            cc = [f for f in en_jeu if f.card.GetOwner() == joueur]
            vus.append(cc[0].GetCounters("corruption") if len(cc) == 1 else f"{len(cc)} cartes")
        if vus != attendu["corruption"]:
            soucis.append(f"jetons corruption par joueur {vus} (attendu {attendu['corruption']})")
    if "cc_face" in attendu:
        vus = []
        for joueur in monde.const_players:
            cc = [f for f in en_jeu if f.card.GetOwner() == joueur]
            vus.append(str(cc[0].paper.card_id)[-1] if len(cc) == 1 else f"{len(cc)} cartes")
        if vus != attendu["cc_face"]:
            soucis.append(f"face de la Creeping Corruption par joueur {vus} (attendu {attendu['cc_face']})")
    if "mains" in attendu:
        vus = [j.hand_cards.GetSize() for j in monde.const_players]
        if vus != attendu["mains"]:
            soucis.append(f"taille des mains {vus} (attendu {attendu['mains']})")
    if "cartes_donnees" in attendu:
        vus = [len(j.dealt_encounter_cards.Get(True)) for j in monde.const_players]
        if vus != attendu["cartes_donnees"]:
            soucis.append(f"cartes rencontre donnees face cachee {vus} (attendu {attendu['cartes_donnees']})")
    if "allies_en_jeu" in attendu:
        from game.card.face.card_type import Ally as _Ally
        vus = [len([c for c in j.GetControlCharacters() if _Ally.IsType(c)]) for j in monde.const_players]
        if vus != attendu["allies_en_jeu"]:
            soucis.append(f"allies controles par joueur {vus} (attendu {attendu['allies_en_jeu']})")
    if "degats_identites" in attendu:
        vus = [j.GetIdentity().max_health - j.GetIdentity().health for j in monde.const_players]
        if vus != attendu["degats_identites"]:
            soucis.append(f"degats subis par l'identite de chaque joueur {vus} (attendu {attendu['degats_identites']})")
    if "partie_finie" in attendu and bool(monde.is_game_over) != attendu["partie_finie"]:
        soucis.append(f"partie finie = {bool(monde.is_game_over)} (attendu {attendu['partie_finie']})")
    for card_id, mot, valeur in attendu.get("mots_cles") or []:
        face = aides["par_id"](monde, card_id)
        if face is None:
            soucis.append(f"{card_id} introuvable en jeu (mots_cles)")
        elif face.GetKeyword(mot) != valeur:
            soucis.append(f"{card_id} {mot} = {face.GetKeyword(mot)} (attendu {valeur})")
    reste = {k: v for k, v in attendu.items() if k not in ("corruption", "cc_en_jeu", "cc_de_cote", "cc_face", "mains", "cartes_donnees", "allies_en_jeu", "partie_finie", "mots_cles", "degats_identites")}
    cas["attendu"] = reste
    try:
        ok, msg = etat_attendu(monde, aides)
    finally:
        cas["attendu"] = attendu
    if not ok:
        soucis.append(msg)
    return (False, " ; ".join(soucis)) if soucis else (True, "etat conforme")
'''
