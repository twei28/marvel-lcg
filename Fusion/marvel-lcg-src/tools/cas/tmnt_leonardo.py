# Cas test_capacites du heros Leonardo (TMNT, Inkwire) : prefixe « [leonardo] ».
# Un cas par capacite, sujet = le card_id dans le nom. Decisions : .planning/tmnt/decisions-phase-b.md.
#
# Rappels de montage : Leonardo demarre en ALTER EGO (tl001b) ;
# `Puzzle.ChangeToFace('tl001b', 'tl001a')` le passe en forme HEROS. Scenario Rhino :
# vilain 01094, complot principal 01097b (menace posee par SetThreat), sbire 01101
# (Hydra Mercenary, PV 3, 1 icone de boost). Cartes carburant (une carte = 2 icones) :
# 01088 Energy = YY (energie), 01089 Genius = BB (mental), 01090 Strength = RR (physique).
# `main_exclusive` vide la main d'abord : sans lui le pilote paie avec la main de depart.
# Les upgrades du heros s'ATTACHENT a lui (« s'equipe de ») et sont en jeu sous son controle.

HEROS = {
    "scenario": "rhino",
    "heros": "leonardo",
}
FORME_HEROS = "Puzzle.ChangeToFace('tl001b', 'tl001a')"
KATANAS = ["Puzzle.PutIntoPlay('tl011', under_control=True)",
           "Puzzle.PutIntoPlay('tl012', under_control=True)"]

CAS = [
    # ===================================================================== tl011 / tl012 Katana
    {
        "nom": "[leonardo] tl011 Katana — l'octroi donne la ressource wild AUX DEUX katanas (tl011 + tl012 paient Nukitsuke cout 2)",
        "pourquoi": ("« Each KATANA upgrade you control gains Hero Resource » (vrai octroi) : deux katanas en jeu, "
                     "Nukitsuke (tl010, cout 2) est payee uniquement par eux (main vide hors la carte jouee) ; "
                     "meme instance d'Ability enregistree chez deux porteurs (Ability.Initialize is_initialized)"),
        **HEROS,
        "mise_en_place": [FORME_HEROS, *KATANAS],
        "main_exclusive": ["tl010"],
        "payer_avec": ["tl011", "tl012"],
        "jouer": ["tl010"],
        "declencher": [],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["tl010"], "exhausted": ["tl011", "tl012"]},
    },
    {
        "nom": "[leonardo] tl011 Katana — UNE seule katana en jeu (tl011) : sa ressource wild paie Leo's Greenhouse (cout 1)",
        "pourquoi": "tl011 porte l'aptitude qu'elle octroie a elle-meme : seule en jeu, elle fonctionne",
        **HEROS,
        "mise_en_place": [FORME_HEROS, KATANAS[0]],
        "main_exclusive": ["tl007"],
        "payer_avec": ["tl011"],
        "jouer": ["tl007"],
        "declencher": [],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["tl007"], "exhausted": ["tl011"]},
    },
    {
        "nom": "[leonardo] tl011 Katana — l'octroi cesse quand tl011 quitte le jeu : tl012 reste en jeu SANS ressource",
        "pourquoi": ("« gains » : l'aptitude n'existe que tant que la donneuse est en jeu. Avant : 1 ressource sur "
                     "chaque katana (compte des capacites CanGenerateResources) ; apres defausse de tl011 : tl012 = 0"),
        **HEROS,
        "mise_en_place": [FORME_HEROS, *KATANAS],
        "declencher": ["Puzzle.Discard('tl011')"],
        "verifier": "katana_ressources",
        "attendu": {"tl012": 0, "tl011": None},
    },
    {
        "nom": "[leonardo] tl011 Katana — TEMOIN : tl012 SEULE en jeu (sans tl011) n'a aucune ressource",
        "pourquoi": ("contre-cas de l'octroi : sans la donneuse, tl012 ne genere rien (decision utilisateur : "
                     "vrai octroi, plus de ressource propre a tl012)"),
        **HEROS,
        "mise_en_place": [FORME_HEROS, KATANAS[1]],
        "declencher": [],
        "verifier": "katana_ressources",
        "attendu": {"tl012": 0},
    },
    {
        "nom": "[leonardo] tl011 Katana — TEMOIN POSITIF : deux katanas en jeu, chacune porte exactement UNE ressource octroyee",
        "pourquoi": ("meme instance d'Ability enregistree chez deux porteurs : chaque katana doit avoir SA propre "
                     "capacite (effets distincts), une seule chacune"),
        **HEROS,
        "mise_en_place": [FORME_HEROS, *KATANAS],
        "declencher": [],
        "verifier": "katana_ressources",
        "attendu": {"tl011": 1, "tl012": 1, "effets_distincts": True},
    },
    {
        "nom": "[leonardo] tl011 Katana — « you control » : la katana d'un AUTRE joueur ne recoit pas la ressource",
        "pourquoi": ("2 joueurs : tl011 chez le joueur 1, tl012 chez le joueur 2 -> `control_by=\"You\"` : "
                     "tl012 n'est pas controlee par le controleur de tl011, elle n'a pas la ressource"),
        **HEROS,
        "heros2": "spider_man",
        "mise_en_place": [FORME_HEROS, KATANAS[0],
                          "Puzzle.PutIntoPlay('tl012', under_control=True, player=1)"],
        "declencher": [],
        "verifier": "katana_ressources",
        "attendu": {"tl011": 1, "tl012": 0},
    },
    {
        "nom": "[leonardo] tl011 Katana — Hero Resource : INUTILISABLE en forme d'alter ego (Leo's Greenhouse reste en main)",
        "pourquoi": "« Hero Resource » : la forme de heros seulement ; en alter ego la katana ne paie rien",
        **HEROS,
        "mise_en_place": [KATANAS[0]],
        "main_exclusive": ["tl007"],
        "payer_avec": ["tl011"],
        "jouer": ["tl007"],
        "declencher": [],
        "verifier": "etat_attendu",
        "attendu": {"en_main": ["tl007"], "pret": ["tl011"]},
    },
    {
        "nom": "[leonardo] tl011 Katana — « for an identity-specific card » : la ressource ne paie PAS une carte d'aspect (01063)",
        "pourquoi": ("la ressource wild n'est utilisable que pour une carte specifique a l'identite ; "
                     "01063 Interrogation Room (Justice, cout 1) ne peut pas etre payee par la katana"),
        **HEROS,
        "mise_en_place": [FORME_HEROS, KATANAS[0]],
        "main_exclusive": ["01063"],
        "payer_avec": ["tl011"],
        "jouer": ["01063"],
        "declencher": [],
        "verifier": "etat_attendu",
        "attendu": {"en_main": ["01063"], "pret": ["tl011"]},
    },
    # ===================================================================== tl001a Kenjutsu
    {
        "nom": "[leonardo] tl001a Kenjutsu — Action : redresse une arme WEAPON inclinee que tu controles",
        "pourquoi": "« Ready a WEAPON upgrade you control » : tl011 (KATANA/WEAPON) inclinee -> prete",
        **HEROS,
        "mise_en_place": [FORME_HEROS, KATANAS[0], "Puzzle.Exhaust('tl011')"],
        "declencher": ["Puzzle.Action('tl001a', 'Action', 0)"],
        "cibles": ["tl011"],
        "verifier": "etat_attendu",
        "attendu": {"pret": ["tl011"]},
    },
    {
        "nom": "[leonardo] tl001a Kenjutsu — TEMOIN D'EPUISEMENT : 2e usage du round refuse (une katana reste inclinee)",
        "pourquoi": ("« Limit once per round » : deux katanas inclinees, deux Actions dans le meme round ; "
                     "la 1re redresse tl011, la 2e (cible forcee : la seule restante, tl012) est refusee -> tl012 inclinee"),
        **HEROS,
        "mise_en_place": [FORME_HEROS, *KATANAS, "Puzzle.Exhaust('tl011')", "Puzzle.Exhaust('tl012')"],
        "declencher": ["Puzzle.Action('tl001a', 'Action', 0)"],
        "declencher_tolerant": ["Puzzle.Action('tl001a', 'Action', 0)"],
        "cibles": ["tl011"],
        "verifier": "etat_attendu",
        "attendu": {"pret": ["tl011"], "exhausted": ["tl012"]},
    },
    {
        "nom": "[leonardo] tl001a Kenjutsu — contre-cas : arme DEJA prete, l'Action n'est pas proposee",
        "pourquoi": "`canbe_ready=True` : aucune cible legale -> aucune action disponible",
        **HEROS,
        "mise_en_place": [FORME_HEROS, KATANAS[0]],
        "declencher": [],
        "verifier": "actions_disponibles",
        "attendu": {"carte": "tl001a", "type": "Action", "nombre": 0},
    },
    {
        "nom": "[leonardo] tl001a Kenjutsu — « you control » et WEAPON : la katana d'un AUTRE joueur, ou une amelioration non-WEAPON inclinee, ne comptent pas",
        "pourquoi": ("2 joueurs : tl011 inclinee chez le joueur 2, et Nukitsuke tl010 (STANCE, pas WEAPON) inclinee chez "
                     "le joueur 1 : aucune cible legale -> Kenjutsu indisponible"),
        **HEROS,
        "heros2": "spider_man",
        "mise_en_place": [FORME_HEROS, "Puzzle.PutIntoPlay('tl010', under_control=True)", "Puzzle.Exhaust('tl010')",
                          "Puzzle.PutIntoPlay('tl011', under_control=True, player=1)", "Puzzle.Exhaust('tl011')"],
        "declencher": [],
        "verifier": "actions_disponibles",
        "attendu": {"carte": "tl001a", "type": "Action", "nombre": 0},
    },
    # ===================================================================== tl001b Leo
    {
        "nom": "[leonardo] tl001b Leo — Action : defausse 1 carte, met en jeu 2 katanas (deck + defausse), inclinees",
        "pourquoi": ("« Discard 1 card from your hand -> search deck and discard pile for up to 2 KATANA upgrades, "
                     "put them into play exhausted » : tl011 dans le deck, tl012 dans la defausse, main = 01088"),
        **HEROS,
        "mise_en_place": ["Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01073', 'tl011', '01074')",
                          "Puzzle.CreatePlayerDiscardPile('tl012')"],
        "main_exclusive": ["01088"],
        "accepter_choix": True,
        "declencher": ["Puzzle.Action('tl001b', 'Action', 0)"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["tl011", "tl012"], "exhausted": ["tl011", "tl012"], "defausse": ["01088"],
                    "taille_deck_joueur": 2},
    },
    {
        "nom": "[leonardo] tl001b Leo — « up to 2 » : UNE seule katana disponible (deck), une seule mise en jeu",
        "pourquoi": "jusqu'a 2 : une seule katana trouvee, l'autre absente ; le cout (defausse) est paye quand meme",
        **HEROS,
        "mise_en_place": ["Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01073', 'tl011', '01074')"],
        "main_exclusive": ["01088"],
        "accepter_choix": True,
        "declencher": ["Puzzle.Action('tl001b', 'Action', 0)"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["tl011"], "hors_jeu": ["tl012"], "exhausted": ["tl011"], "defausse": ["01088"]},
    },
    {
        "nom": "[leonardo] tl001b Leo — aucune katana a trouver : rien en jeu, mais la carte est bien defaussee",
        "pourquoi": "0 katana dans le deck et la defausse : la recherche ne ramene rien",
        **HEROS,
        "mise_en_place": ["Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01073', '01074')"],
        "main_exclusive": ["01088"],
        "accepter_choix": True,
        "declencher": ["Puzzle.Action('tl001b', 'Action', 0)"],
        "verifier": "etat_attendu",
        "attendu": {"hors_jeu": ["tl011", "tl012"], "defausse": ["01088"], "taille_deck_joueur": 2},
    },
    {
        "nom": "[leonardo] tl001b Leo — TEMOIN : main vide, l'Action n'est pas proposee (le cout de defausse est impayable)",
        "pourquoi": "« Discard 1 card from your hand -> » : sans carte en main, aucune action disponible",
        **HEROS,
        "mise_en_place": ["Puzzle.EmptyHand()", "Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01073', 'tl011', '01074')"],
        "declencher": [],
        "verifier": "actions_disponibles",
        "attendu": {"carte": "tl001b", "type": "Action", "nombre": 0},
    },
    # ===================================================================== tl002 Splinter
    {
        "nom": "[leonardo] tl002 Splinter — Response a l'entree : une carte specifique a l'identite de la defausse va SUR LE DESSUS du deck",
        "pourquoi": ("« choose an identity-specific card in your discard pile and put it on top of your deck » : "
                     "Splinter jouee (cout 3 paye par Energy + Strength), defausse = tl003 (specifique) ; "
                     "le dessus du deck doit etre tl003"),
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01073', '01074')",
                          "Puzzle.CreatePlayerDiscardPile('tl003')"],
        "main_exclusive": ["tl002", "01088", "01090"],
        "payer_avec": ["01088", "01090"],
        "jouer": ["tl002"],
        "cibles": ["tl003"],
        "declencher": [],
        "verifier": "dessus_deck",
        "attendu": {"dessus": "tl003", "taille": 3, "en_jeu": ["tl002"]},
    },
    {
        "nom": "[leonardo] tl002 Splinter — Response, TEMOIN : une carte de BASE en defausse (Energy) n'est pas une cible legale, elle ne monte pas",
        "pourquoi": ("« an identity-specific card » : on force le choix sur 01088 Energy (classe Basic, depensee pour payer Splinter) : "
                     "si le filtre manquait, elle monterait sur le dessus ; avec lui, une carte Hero monte a la place et "
                     "Energy reste en defausse"),
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01073', '01074')"],
        "main_exclusive": ["tl002", "01088", "01090"],
        "payer_avec": ["01088", "01090"],
        "jouer": ["tl002"],
        "cibles": ["01088"],
        "declencher": [],
        "verifier": "dessus_deck",
        "attendu": {"dessus_pas": "01088", "dessus_classe": "Hero", "defausse": ["01088"], "en_jeu": ["tl002"]},
    },
    {
        "nom": "[leonardo] tl002 Splinter — ATQ 2* / CTR 2* : 1 degat consecutif (attaque ET contre), et 3 PV",
        "pourquoi": "« 2* » : desc.ATK/THW lus par can_attack.py:47-52 -> consequential damage 1 sur les deux pouvoirs",
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.PutIntoPlay('tl002', under_control=True)"],
        "declencher": [],
        "verifier": "allie_consecutif",
        "attendu": {"carte": "tl002", "atq": 2, "ctr": 2, "cons_atq": 1, "cons_ctr": 1, "pv": 3},
    },
    # ===================================================================== tl003 Uke Nagashi
    {
        "nom": "[leonardo] tl003 Uke Nagashi — +2 DEF a la defense de Leonardo, payee en physique : plus aucun degat ET Leonardo redresse",
        "pourquoi": ("Rhino ATK 2 + boost 1 (Hydra Mercenary) = 3 contre DEF 2 : 1 degat. Avec +2 DEF : 0. "
                     "Payee par Strength (RR, physique) -> « ready Leonardo » (il s'etait incline en defendant)"),
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01101')"],
        "main_exclusive": ["tl003", "01090"],
        "payer_avec": ["01090"],
        "declencher": ["Puzzle.Defend('tl001a', '01094')"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 0, "defausse": ["tl003"], "pret": ["tl001a"]},
    },
    {
        "nom": "[leonardo] tl003 Uke Nagashi — payee SANS physique (Energy YY) : +2 DEF mais Leonardo reste incline",
        "pourquoi": "la condition « paid with a [physical] resource » : sans R, pas de redressement",
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01101')"],
        "main_exclusive": ["tl003", "01088"],
        "payer_avec": ["01088"],
        "declencher": ["Puzzle.Defend('tl001a', '01094')"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 0, "defausse": ["tl003"], "exhausted": ["tl001a"]},
    },
    {
        "nom": "[leonardo] tl003 Uke Nagashi — TEMOIN de ligne de base : sans Uke Nagashi, la meme attaque fait 1 degat",
        "pourquoi": "ligne de base de la mesure : DEF 2 contre 3 = 1 degat (sinon les cas precedents ne prouvent rien)",
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01101')"],
        "main_exclusive": ["01090"],
        "declencher": ["Puzzle.Defend('tl001a', '01094')"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 1},
    },
    {
        "nom": "[leonardo] tl003 Uke Nagashi — « When LEONARDO defends » : quand un ALLIE defend, la carte n'est pas jouee",
        "pourquoi": "`YourHero` : Splinter (allie) defend, Uke Nagashi reste en main",
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01101')",
                          "Puzzle.PutIntoPlay('tl002', under_control=True)"],
        "main_exclusive": ["tl003", "01090"],
        "payer_avec": ["01090"],
        "declencher": ["Puzzle.Defend('tl002', '01094')"],
        "verifier": "etat_attendu",
        "attendu": {"en_main": ["tl003"]},
    },
    # ===================================================================== tl004 Vigilant
    {
        "nom": "[leonardo] tl004 Vigilant — retire 3 menaces (payee en physique) ; aucune katana redressee",
        "pourquoi": ("« Remove 3 threat from a scheme » : menace 6 -> 3. Payee par Strength (RR, physique, pas de mental) : "
                     "la katana inclinee reste inclinee"),
        **HEROS,
        "mise_en_place": [FORME_HEROS, KATANAS[0], "Puzzle.Exhaust('tl011')", "Puzzle.SetThreat('01097b', 6)"],
        "main_exclusive": ["tl004", "01090"],
        "payer_avec": ["01090"],
        "jouer": ["tl004"],
        "declencher": [],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["01097b", 3]], "defausse": ["tl004"], "exhausted": ["tl011"]},
    },
    {
        "nom": "[leonardo] tl004 Vigilant — payee avec une ressource MENTALE (Genius BB) : la katana inclinee est redressee",
        "pourquoi": "« If you paid ... with a [mental] resource, ready a KATANA upgrade you control »",
        **HEROS,
        "mise_en_place": [FORME_HEROS, KATANAS[0], "Puzzle.Exhaust('tl011')", "Puzzle.SetThreat('01097b', 6)"],
        "main_exclusive": ["tl004", "01089"],
        "payer_avec": ["01089"],
        "jouer": ["tl004"],
        "cibles": ["tl011"],
        "declencher": [],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["01097b", 3]], "defausse": ["tl004"], "pret": ["tl011"]},
    },
    {
        "nom": "[leonardo] tl004 Vigilant — payee en mental mais AUCUNE katana inclinee : aucune question de redressement",
        "pourquoi": "`canbe_ready=True` : pas de cible legale, la menace est tout de meme retiree",
        **HEROS,
        "mise_en_place": [FORME_HEROS, KATANAS[0], "Puzzle.SetThreat('01097b', 6)"],
        "main_exclusive": ["tl004", "01089"],
        "payer_avec": ["01089"],
        "jouer": ["tl004"],
        "declencher": [],
        "questions_absentes": ["Ready a KATANA"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["01097b", 3]], "defausse": ["tl004"]},
    },
    # ===================================================================== tl005 Stoicism
    {
        "nom": "[leonardo] tl005 Stoicism — redresse Leonardo ; payee en mental (pas d'energie) : la katana reste inclinee",
        "pourquoi": "« Ready Leonardo. If paid with [energy], ready a KATANA » : Genius BB -> Leonardo seul",
        **HEROS,
        "mise_en_place": [FORME_HEROS, KATANAS[0], "Puzzle.Exhaust('tl011')", "Puzzle.Exhaust('tl001a')"],
        "main_exclusive": ["tl005", "01089"],
        "payer_avec": ["01089"],
        "jouer": ["tl005"],
        "declencher": [],
        "verifier": "etat_attendu",
        "attendu": {"pret": ["tl001a"], "exhausted": ["tl011"], "defausse": ["tl005"]},
    },
    {
        "nom": "[leonardo] tl005 Stoicism — payee avec une ressource ENERGIE (Energy YY) : Leonardo ET la katana sont redresses",
        "pourquoi": "la condition « paid with an [energy] resource »",
        **HEROS,
        "mise_en_place": [FORME_HEROS, KATANAS[0], "Puzzle.Exhaust('tl011')", "Puzzle.Exhaust('tl001a')"],
        "main_exclusive": ["tl005", "01088"],
        "payer_avec": ["01088"],
        "jouer": ["tl005"],
        "cibles": ["tl011"],
        "declencher": [],
        "verifier": "etat_attendu",
        "attendu": {"pret": ["tl001a", "tl011"], "defausse": ["tl005"]},
    },
    # ===================================================================== tl006 Yo Ko Giri
    {
        "nom": "[leonardo] tl006 Yo Ko Giri — 5 degats PERCANTS : Rhino Tenace prend 5 et perd son statut",
        "pourquoi": ("« Deal 5 damage to an enemy. This attack gains piercing » : sans piercing, Tenace absorberait "
                     "les degats (0). Payee Energy + Strength (YR : pas de mental, donc aucune question de retour)"),
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.Tough('01094')"],
        "main_exclusive": ["tl006", "01088", "01090"],
        "payer_avec": ["01088", "01090"],
        "jouer": ["tl006"],
        "cibles": ["01094"],
        "declencher": [],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 5]], "statuts_absents": [["01094", "Tough"]], "defausse": ["tl006"]},
    },
    {
        "nom": "[leonardo] tl006 Yo Ko Giri — payee energie + mental + physique : elle revient en main",
        "pourquoi": "« If paid with [energy][mental][physical] resources, you may return this card to your hand »",
        **HEROS,
        "mise_en_place": [FORME_HEROS],
        "main_exclusive": ["tl006", "01088", "01089", "01090"],
        "payer_avec": ["01088", "01089", "01090"],
        "payer_tout": True,
        "jouer": ["tl006"],
        "cibles": ["01094"],
        "declencher": [],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 5]], "en_main": ["tl006"]},
    },
    {
        "nom": "[leonardo] tl006 Yo Ko Giri — « you MAY return » : refus (Decline), la carte va en defausse",
        "pourquoi": "optionnel : meme paiement, le joueur choisit Decline",
        **HEROS,
        "mise_en_place": [FORME_HEROS],
        "main_exclusive": ["tl006", "01088", "01089", "01090"],
        "payer_avec": ["01088", "01089", "01090"],
        "payer_tout": True,
        "jouer": ["tl006"],
        "cibles": ["01094"],
        "choisir_option": ["Decline"],
        "declencher": [],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 5]], "absent_main": ["tl006"], "defausse": ["tl006"]},
    },
    {
        "nom": "[leonardo] tl006 Yo Ko Giri — TEMOIN : payee en energie + mental seulement (pas de physique), aucun retour en main",
        "pourquoi": "il manque une couleur : aucune question « Return this card », la carte part en defausse",
        **HEROS,
        "mise_en_place": [FORME_HEROS],
        "main_exclusive": ["tl006", "01088", "01089"],
        "payer_avec": ["01088", "01089"],
        "jouer": ["tl006"],
        "cibles": ["01094"],
        "declencher": [],
        "questions_absentes": ["Return this card"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 5]], "absent_main": ["tl006"], "defausse": ["tl006"]},
    },
    # ===================================================================== tl007 Leo's Greenhouse
    {
        "nom": "[leonardo] tl007 Leo's Greenhouse — Action d'alter ego : incline + defausse 1 carte -> pioche 2 et soigne 2",
        "pourquoi": ("« Exhaust and discard 1 card -> draw 2 cards and heal 2 damage from your identity » : "
                     "3 degats -> 1, main 2 -> 1 (defausse) -> 3 (pioche 2), soutien incline"),
        **HEROS,
        "mise_en_place": ["Puzzle.PutIntoPlay('tl007', under_control=True)", "Puzzle.Damage('tl001b', 3)"],
        "main_exclusive": ["01088", "01089"],
        "declencher": ["Puzzle.Action('tl007', 'AlterEgoAction', 0)"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 1, "taille_main": 3, "exhausted": ["tl007"]},
    },
    {
        "nom": "[leonardo] tl007 Leo's Greenhouse — TEMOIN : en forme de HEROS l'Action d'alter ego n'est pas proposee",
        "pourquoi": "« Alter-Ego Action » : alter ego seulement",
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.PutIntoPlay('tl007', under_control=True)"],
        "main_exclusive": ["01088", "01089"],
        "declencher": [],
        "verifier": "actions_disponibles",
        "attendu": {"carte": "tl007", "type": "AlterEgoAction", "nombre": 0},
    },
    {
        "nom": "[leonardo] tl007 Leo's Greenhouse — TEMOIN : main vide, l'Action n'est pas proposee (cout de defausse impayable)",
        "pourquoi": "deux parties de cout (inclinaison ET defausse) : sans carte en main, rien",
        **HEROS,
        "mise_en_place": ["Puzzle.EmptyHand()", "Puzzle.PutIntoPlay('tl007', under_control=True)"],
        "declencher": [],
        "verifier": "actions_disponibles",
        "attendu": {"carte": "tl007", "type": "AlterEgoAction", "nombre": 0},
    },
    {
        "nom": "[leonardo] tl007 Leo's Greenhouse — TEMOIN : soutien deja incline, l'Action n'est pas proposee",
        "pourquoi": "la partie « Exhaust Leo's Greenhouse » du cout",
        **HEROS,
        "mise_en_place": ["Puzzle.PutIntoPlay('tl007', under_control=True)", "Puzzle.Exhaust('tl007')"],
        "main_exclusive": ["01088", "01089"],
        "declencher": [],
        "verifier": "actions_disponibles",
        "attendu": {"carte": "tl007", "type": "AlterEgoAction", "nombre": 0},
    },
    # ===================================================================== tl008 Iaijutsu
    {
        "nom": "[leonardo] tl008 Iaijutsu — un SBIRE attaque : on joue Yo Ko Giri depuis la main, elle VAINC le sbire -> pioche 1",
        "pourquoi": ("Hero Interrupt « when an enemy initiates an attack, exhaust a KATANA -> play an ATTACK event with a "
                     "Hero Action from your hand (paying its cost). If this attack defeats an enemy, draw 1 card ». "
                     "Hydra Mercenary (PV 3) attaque ; Yo Ko Giri (5 degats, payee Energy + Strength) le vainc ; "
                     "main : 0 + 1 pioche = 1 ; katana inclinee, Iaijutsu elle-meme PRETE (l'insert)"),
        **HEROS,
        "mise_en_place": [FORME_HEROS, KATANAS[0], "Puzzle.PutIntoPlay('tl008', under_control=True)",
                          "Puzzle.PutIntoPlay('01101')"],
        "main_exclusive": ["tl006", "01088", "01090"],
        "payer_avec": ["01088", "01090"],
        "cibles": ["01101"],
        "declencher": ["Puzzle.Attack('01101')"],
        "verifier": "etat_attendu",
        "attendu": {"hors_jeu": ["01101"], "defausse": ["tl006"], "taille_main": 1,
                    "exhausted": ["tl011"], "pret": ["tl008"]},
    },
    {
        "nom": "[leonardo] tl008 Iaijutsu — le VILAIN attaque : Yo Ko Giri ne vainc pas Rhino -> AUCUNE pioche",
        "pourquoi": ("TEMOIN du « if this attack defeats » : meme montage, cible Rhino (PV 14) : pas de defaite, "
                     "main = 0. Prouve aussi que le declencheur vaut pour le vilain, pas seulement un sbire"),
        **HEROS,
        "mise_en_place": [FORME_HEROS, KATANAS[0], "Puzzle.PutIntoPlay('tl008', under_control=True)",
                          "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01101')"],
        "main_exclusive": ["tl006", "01088", "01090"],
        "payer_avec": ["01088", "01090"],
        "cibles": ["01094"],
        "declencher": ["Puzzle.Attack('01094')"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 5]], "defausse": ["tl006"], "taille_main": 0, "exhausted": ["tl011"]},
    },
    {
        "nom": "[leonardo] tl008 Iaijutsu — TEMOIN : aucune katana prete, l'Interrupt n'est pas proposee (Yo Ko Giri reste en main)",
        "pourquoi": "le cout est l'inclinaison d'une KATANA prete (pas Iaijutsu) : katana inclinee -> impossible",
        **HEROS,
        "mise_en_place": [FORME_HEROS, KATANAS[0], "Puzzle.Exhaust('tl011')",
                          "Puzzle.PutIntoPlay('tl008', under_control=True)", "Puzzle.PutIntoPlay('01101')"],
        "main_exclusive": ["tl006", "01088", "01090"],
        "payer_avec": ["01088", "01090"],
        "cibles": ["01101"],
        "declencher": ["Puzzle.Attack('01101')"],
        "verifier": "etat_attendu",
        "attendu": {"en_main": ["tl006"], "en_jeu": ["01101"], "pret": ["tl008"]},
    },
    {
        "nom": "[leonardo] tl008 Iaijutsu — TEMOIN : seul un evenement NON-ATTACK en main (Stoicism), rien n'est joue ni incline",
        "pourquoi": "« an ATTACK event with a Hero Action » : Stoicism (HeroAction mais pas ATTACK) n'est pas eligible",
        **HEROS,
        "mise_en_place": [FORME_HEROS, KATANAS[0], "Puzzle.PutIntoPlay('tl008', under_control=True)",
                          "Puzzle.PutIntoPlay('01101')"],
        "main_exclusive": ["tl005", "01089"],
        "declencher": ["Puzzle.Attack('01101')"],
        "verifier": "etat_attendu",
        "attendu": {"en_main": ["tl005"], "pret": ["tl011"]},
    },
    # ===================================================================== tl009 Taicho
    {
        "nom": "[leonardo] tl009 Taicho — Hero Action : incline une katana -> Taicho (inclinee) se redresse",
        "pourquoi": "« Exhaust a KATANA upgrade you control -> ready this card » : la carte elle-meme n'est PAS le cout",
        **HEROS,
        "mise_en_place": [FORME_HEROS, KATANAS[0], "Puzzle.PutIntoPlay('tl009', under_control=True)",
                          "Puzzle.Exhaust('tl009')"],
        "declencher": ["Puzzle.Action('tl009', 'HeroAction', 0)"],
        "verifier": "etat_attendu",
        "attendu": {"pret": ["tl009"], "exhausted": ["tl011"]},
    },
    {
        "nom": "[leonardo] tl009 Taicho — TEMOIN : Taicho DEJA prete, la Hero Action n'est pas proposee",
        "pourquoi": "« ready this card » sans effet sur une carte prete : l'action ne se propose pas",
        **HEROS,
        "mise_en_place": [FORME_HEROS, KATANAS[0], "Puzzle.PutIntoPlay('tl009', under_control=True)"],
        "declencher": [],
        "verifier": "actions_disponibles",
        "attendu": {"carte": "tl009", "type": "HeroAction", "nombre": 0},
    },
    {
        "nom": "[leonardo] tl009 Taicho — TEMOIN : aucune katana prete, la Hero Action n'est pas proposee (cout impayable)",
        "pourquoi": "Taicho inclinee mais la seule katana l'est aussi",
        **HEROS,
        "mise_en_place": [FORME_HEROS, KATANAS[0], "Puzzle.PutIntoPlay('tl009', under_control=True)",
                          "Puzzle.Exhaust('tl009')", "Puzzle.Exhaust('tl011')"],
        "declencher": [],
        "verifier": "actions_disponibles",
        "attendu": {"carte": "tl009", "type": "HeroAction", "nombre": 0},
    },
    {
        "nom": "[leonardo] tl009 Taicho — Hero Response : un allie subit un degat consecutif -> Taicho s'incline, l'allie se redresse",
        "pourquoi": ("Splinter (ATQ 2*) attaque, s'incline, subit 1 degat consecutif : Reponse de Taicho "
                     "(exhaust this card -> ready that ally) : Splinter prete, Taicho inclinee, 1 degat sur Splinter"),
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.PutIntoPlay('tl009', under_control=True)",
                          "Puzzle.PutIntoPlay('tl002', under_control=True)"],
        "declencher": ["Puzzle.Attack('tl002')"],
        "verifier": "etat_attendu",
        "attendu": {"pret": ["tl002"], "exhausted": ["tl009"], "degats": [["tl002", 1]]},
    },
    {
        "nom": "[leonardo] tl009 Taicho — Hero Response, TEMOIN : Taicho deja inclinee, la Reponse n'est pas proposee",
        "pourquoi": "le cout « exhaust this card » : Splinter reste inclinee apres son attaque",
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.PutIntoPlay('tl009', under_control=True)", "Puzzle.Exhaust('tl009')",
                          "Puzzle.PutIntoPlay('tl002', under_control=True)"],
        "declencher": ["Puzzle.Attack('tl002')"],
        "verifier": "etat_attendu",
        "attendu": {"exhausted": ["tl002", "tl009"], "degats": [["tl002", 1]]},
    },
    {
        "nom": "[leonardo] tl009 Taicho — l'allie est VAINCU par les degats consecutifs : pas d'erreur, Taicho reste prete",
        "pourquoi": "Splinter a deja 2 degats (PV 3) : le degat consecutif la vainc ; la Reponse ne vise plus rien",
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.PutIntoPlay('tl009', under_control=True)",
                          "Puzzle.PutIntoPlay('tl002', under_control=True)", "Puzzle.Damage('tl002', 2)"],
        "declencher": ["Puzzle.Attack('tl002')"],
        "verifier": "etat_attendu",
        "attendu": {"hors_jeu": ["tl002"], "pret": ["tl009"]},
    },
    {
        "nom": "[leonardo] tl009 Taicho — allie Tenace : degats consecutifs empeches, la Reponse ne se declenche pas",
        "pourquoi": "« takes consequential damage » : Tough empeche les degats, Splinter reste inclinee, Taicho prete",
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.PutIntoPlay('tl009', under_control=True)",
                          "Puzzle.PutIntoPlay('tl002', under_control=True)", "Puzzle.Tough('tl002')"],
        "declencher": ["Puzzle.Attack('tl002')"],
        "verifier": "etat_attendu",
        "attendu": {"exhausted": ["tl002"], "pret": ["tl009"], "degats": [["tl002", 0]]},
    },
    # ===================================================================== tl010 Nukitsuke
    {
        "nom": "[leonardo] tl010 Nukitsuke — Hero Action : s'incline -> redresse une katana inclinee",
        "pourquoi": "« Exhaust Nukitsuke -> ready a KATANA upgrade you control »",
        **HEROS,
        "mise_en_place": [FORME_HEROS, KATANAS[0], "Puzzle.PutIntoPlay('tl010', under_control=True)",
                          "Puzzle.Exhaust('tl011')"],
        "declencher": ["Puzzle.Action('tl010', 'HeroAction', 0)"],
        "cibles": ["tl011"],
        "verifier": "etat_attendu",
        "attendu": {"pret": ["tl011"], "exhausted": ["tl010"]},
    },
    {
        "nom": "[leonardo] tl010 Nukitsuke — TEMOIN : aucune katana inclinee, l'action n'est pas proposee",
        "pourquoi": "`canbe_ready=True` : pas de cible legale",
        **HEROS,
        "mise_en_place": [FORME_HEROS, KATANAS[0], "Puzzle.PutIntoPlay('tl010', under_control=True)"],
        "declencher": [],
        "verifier": "actions_disponibles",
        "attendu": {"carte": "tl010", "type": "HeroAction", "nombre": 0},
    },
    {
        "nom": "[leonardo] tl010 Nukitsuke — TEMOIN : Nukitsuke deja inclinee, l'action n'est pas proposee (cout)",
        "pourquoi": "« Exhaust Nukitsuke » : cout impayable",
        **HEROS,
        "mise_en_place": [FORME_HEROS, KATANAS[0], "Puzzle.PutIntoPlay('tl010', under_control=True)",
                          "Puzzle.Exhaust('tl011')", "Puzzle.Exhaust('tl010')"],
        "declencher": [],
        "verifier": "actions_disponibles",
        "attendu": {"carte": "tl010", "type": "HeroAction", "nombre": 0},
    },
    # ===================================================================== tl012 Other Katana
    {
        "nom": "[leonardo] tl012 Other Katana — Hero Action : incline 2 katanas -> Leonardo gagne +1 ATQ/CTR/DEF/REC",
        "pourquoi": "« exhaust 2 KATANA -> that character gets +1 to each of their basic powers until the end of the round »",
        **HEROS,
        "mise_en_place": [FORME_HEROS, *KATANAS],
        "declencher": ["Puzzle.Action('tl012', 'HeroAction', 0)"],
        "cibles": ["tl001a"],
        "verifier": "etat_attendu",
        "attendu": {"exhausted": ["tl011", "tl012"],
                    "attributs": {"attack": 1, "thwart": 1, "defense": 1}},
    },
    {
        "nom": "[leonardo] tl012 Other Katana — « a friendly character » : un ALLIE (Splinter) gagne +1 ATQ et +1 CTR",
        "pourquoi": "toute identite ou tout allie ami : on vise Splinter, le heros reste a l'imprime",
        **HEROS,
        "mise_en_place": [FORME_HEROS, *KATANAS, "Puzzle.PutIntoPlay('tl002', under_control=True)"],
        "declencher": ["Puzzle.Action('tl012', 'HeroAction', 0)"],
        "cibles": ["tl002"],
        "verifier": "etat_attendu",
        "attendu": {"exhausted": ["tl011", "tl012"],
                    "attributs_carte": [["tl002", "attack", 1], ["tl002", "thwart", 1]],
                    "attributs": {"attack": 0, "thwart": 0, "defense": 0}},
    },
    {
        "nom": "[leonardo] tl012 Other Katana — « until the END OF THE ROUND » : le bonus a disparu apres la fin du round",
        "pourquoi": "meme action, puis WhenRoundEnd + fin de round : les 4 attributs reviennent a l'imprime",
        **HEROS,
        "mise_en_place": [FORME_HEROS, *KATANAS],
        "declencher": ["Puzzle.Action('tl012', 'HeroAction', 0)"],
        "cibles": ["tl001a"],
        "verifier": "apres_fin_de_round",
        "attendu": {"attributs": {"attack": 0, "thwart": 0, "defense": 0}},
    },
    {
        "nom": "[leonardo] tl012 Other Katana — TEMOIN : une seule katana prete (l'autre inclinee), l'action n'est pas proposee",
        "pourquoi": "« exhaust 2 KATANA » : range (2, 2), les deux doivent etre pretes",
        **HEROS,
        "mise_en_place": [FORME_HEROS, *KATANAS, "Puzzle.Exhaust('tl011')"],
        "declencher": [],
        "verifier": "actions_disponibles",
        "attendu": {"carte": "tl012", "type": "HeroAction", "nombre": 0},
    },
    {
        "nom": "[leonardo] tl012 Other Katana — TEMOIN : tl012 SEULE en jeu, une seule katana, l'action n'est pas proposee",
        "pourquoi": "2 katanas requises : sans tl011 le cout est impayable",
        **HEROS,
        "mise_en_place": [FORME_HEROS, KATANAS[1]],
        "declencher": [],
        "verifier": "actions_disponibles",
        "attendu": {"carte": "tl012", "type": "HeroAction", "nombre": 0},
    },
    # ===================================================================== tl013 Brainwashed Betrayal
    {
        "nom": "[leonardo] tl013 Brainwashed Betrayal — donnee a Leo : bascule OBLIGATOIRE en heros et defausse l'allie unique",
        "pourquoi": ("« Flip to hero form and discard an ally you control » : Leo (alter ego) avec Splinter en jeu -> "
                     "forme Hero, Splinter defaussee, l'obligation reste en jeu"),
        **HEROS,
        "mise_en_place": ["Puzzle.PutIntoPlay('tl002', under_control=True)"],
        "declencher": ["Puzzle.Reveal('tl013')"],
        "verifier": "etat_attendu",
        "attendu": {"forme": "Hero", "hors_jeu": ["tl002"], "en_jeu": ["tl013"]},
    },
    {
        "nom": "[leonardo] tl013 Brainwashed Betrayal — aucun allie : bascule en heros quand meme, aucune erreur",
        "pourquoi": "« discard an ally you control » sans allie : rien a defausser, le flip reste obligatoire",
        **HEROS,
        "mise_en_place": [],
        "declencher": ["Puzzle.Reveal('tl013')"],
        "verifier": "etat_attendu",
        "attendu": {"forme": "Hero", "en_jeu": ["tl013"]},
    },
    {
        "nom": "[leonardo] tl013 Brainwashed Betrayal — DEUX allies : le joueur choisit lequel defausser (Splinter), l'autre reste",
        "pourquoi": "« an ally you control » : un seul, au choix ; Hellcat (01020) reste en jeu",
        **HEROS,
        "mise_en_place": ["Puzzle.PutIntoPlay('tl002', under_control=True)",
                          "Puzzle.PutIntoPlay('01020', under_control=True)"],
        "declencher": ["Puzzle.Reveal('tl013')"],
        "cibles": ["tl002"],
        "verifier": "etat_attendu",
        "attendu": {"forme": "Hero", "hors_jeu": ["tl002"], "en_jeu": ["01020"]},
    },
    {
        "nom": "[leonardo] tl013 Brainwashed Betrayal — « cannot attack the villain » : l'attaque va sur le SBIRE, Rhino intact",
        "pourquoi": ("obligation en jeu, forme heros : Leonardo (ATQ 2) attaque, cible preferee Rhino mais illegale -> "
                     "Hydra Mercenary (sbire attaquable) prend 2 ; Rhino 0 degat"),
        **HEROS,
        "mise_en_place": ["Puzzle.Reveal('tl013')", "Puzzle.PutIntoPlay('01103')"],
        "declencher": ["Puzzle.Attack('tl001a')"],
        "cibles": ["01094"],
        "verifier": "etat_attendu",
        "attendu": {"forme": "Hero", "degats": [["01094", 0], ["01103", 2]]},
    },
    {
        "nom": "[leonardo] tl013 Brainwashed Betrayal — TEMOIN : SANS l'obligation, la meme attaque frappe Rhino (2 degats)",
        "pourquoi": "ligne de base de la mesure precedente",
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.PutIntoPlay('01103')"],
        "declencher": ["Puzzle.Attack('tl001a')"],
        "cibles": ["01094"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 2], ["01103", 0]]},
    },
    {
        "nom": "[leonardo] tl013 Brainwashed Betrayal — Forced Response apres le debut du tour : 3 degats a l'allie d'un AUTRE joueur (au choix)",
        "pourquoi": ("« deal 3 damage to AN ally » (decision : n'importe quel allie, au choix) : Splinter chez Leo, War Machine "
                     "(PV 4) chez le joueur 2 ; on designe War Machine -> 3 degats ; Splinter intacte"),
        **HEROS,
        "heros2": "spider_man",
        "mise_en_place": ["Puzzle.Reveal('tl013')", "Puzzle.PutIntoPlay('tl002', under_control=True)",
                          "Puzzle.PutIntoPlay('01030', under_control=True, player=1)"],
        "declencher": [],
        "cibles": ["01030"],
        "verifier": "debut_de_tour_puis_etat",
        "attendu": {"degats": [["01030", 3], ["tl002", 0]]},
    },
    {
        "nom": "[leonardo] tl013 Brainwashed Betrayal — Forced Response : l'allie designe est celui qui encaisse (Splinter chez Leo, PV 3 -> vaincue)",
        "pourquoi": "meme montage, cible Splinter (PV 3) : 3 degats la vainquent ; War Machine intacte",
        **HEROS,
        "heros2": "spider_man",
        "mise_en_place": ["Puzzle.Reveal('tl013')", "Puzzle.PutIntoPlay('tl002', under_control=True)",
                          "Puzzle.PutIntoPlay('01030', under_control=True, player=1)"],
        "declencher": [],
        "cibles": ["tl002"],
        "verifier": "debut_de_tour_puis_etat",
        "attendu": {"hors_jeu": ["tl002"], "degats": [["01030", 0]]},
    },
    {
        "nom": "[leonardo] tl013 Brainwashed Betrayal — Alter-Ego Action : incline Leo + 2 degats -> l'obligation est RETIREE DU JEU",
        "pourquoi": ("l'obligation force le heros ; Leo repasse en alter ego (Change Form), puis l'Action "
                     "(exhaust Leo + take 2 damage) retire la carte de la partie"),
        **HEROS,
        "mise_en_place": ["Puzzle.Reveal('tl013')", "Puzzle.ChangeForm('tl001a')"],
        "declencher": ["Puzzle.Action('tl013', 'AlterEgoAction', 0)"],
        "verifier": "retiree_du_jeu",
        "attendu": {"carte": "tl013", "degats_identite": 2, "exhausted": ["tl001b"]},
    },
    # ===================================================================== tl014 Foot Patrol
    {
        "nom": "[leonardo] tl014 Foot Patrol — menace de depart 2 PAR JOUEUR : 2 en solo",
        "pourquoi": "desc.StartingThreat = « 2* » (par joueur)",
        **HEROS,
        "mise_en_place": [],
        "declencher": ["Puzzle.Reveal('tl014')"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["tl014", 2]]},
    },
    {
        "nom": "[leonardo] tl014 Foot Patrol — menace de depart 2 PAR JOUEUR : 4 a deux joueurs",
        "pourquoi": "meme carte, 2 heros -> 4",
        **HEROS,
        "heros2": "spider_man",
        "mise_en_place": [],
        "declencher": ["Puzzle.Reveal('tl014')"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["tl014", 4]]},
    },
    {
        "nom": "[leonardo] tl014 Foot Patrol — Crisis : la menace du complot PRINCIPAL ne peut pas etre retiree tant qu'elle est en jeu",
        "pourquoi": ("Leonardo contre : le principal n'est pas une cible legale (Crisis 1), le contre va sur Foot Patrol ; "
                     "menace principale inchangee (6)"),
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.SetThreat('01097b', 6)"],
        "declencher": ["Puzzle.Reveal('tl014')", "Puzzle.Thwart('tl001a')"],
        "cibles": ["01097b"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["01097b", 6]]},
    },
    {
        "nom": "[leonardo] tl014 Foot Patrol — Crisis, TEMOIN : sans Foot Patrol, le meme contre retire 2 menaces du principal (6 -> 4)",
        "pourquoi": "ligne de base de la mesure precedente",
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.SetThreat('01097b', 6)"],
        "declencher": ["Puzzle.Thwart('tl001a')"],
        "cibles": ["01097b"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["01097b", 4]]},
    },
    {
        "nom": "[leonardo] tl014 Foot Patrol — When Defeated : un sbire FOOT CLAN du DECK rencontre est mis en jeu, engage avec le premier joueur",
        "pourquoi": ("Foot Patrol (menace 2) vaincue par un contre de Leonardo (CTR 2) : Foot Soldiers (tl016) du deck "
                     "rencontre entre en jeu engage ; Hydra Mercenary (pas FOOT CLAN) reste dans le deck"),
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01101', 'tl016')"],
        "declencher": ["Puzzle.Reveal('tl014')", "Puzzle.Thwart('tl001a')"],
        "accepter_choix": True,
        "verifier": "sbire_engage",
        "attendu": {"carte": "tl016", "joueur": 0, "hors_jeu": ["01101", "tl014"], "dans_deck_rencontre": ["01101"]},
    },
    {
        "nom": "[leonardo] tl014 Foot Patrol — When Defeated : le sbire FOOT CLAN est cherche aussi dans la DEFAUSSE de rencontre",
        "pourquoi": "« search the encounter deck AND discard pile » : tl016 seulement dans la defausse de rencontre",
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01101')",
                          "Puzzle.CreateEncounterDiscardPile('tl016')"],
        "declencher": ["Puzzle.Reveal('tl014')", "Puzzle.Thwart('tl001a')"],
        "accepter_choix": True,
        "verifier": "sbire_engage",
        "attendu": {"carte": "tl016", "joueur": 0, "hors_jeu": ["tl014"]},
    },
    {
        "nom": "[leonardo] tl014 Foot Patrol — When Defeated, aucun FOOT CLAN : rien ne se passe (decision utilisateur)",
        "pourquoi": "ni le deck ni la defausse de rencontre n'ont de sbire FOOT CLAN : aucun sbire en jeu, deck intact",
        **HEROS,
        "mise_en_place": [FORME_HEROS, "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01101')"],
        "declencher": ["Puzzle.Reveal('tl014')", "Puzzle.Thwart('tl001a')"],
        "accepter_choix": True,
        "verifier": "etat_attendu",
        "attendu": {"hors_jeu": ["tl014", "tl016", "01101"], "dans_deck_rencontre": ["01101"]},
    },
    {
        "nom": "[leonardo] tl014 Foot Patrol — When Defeated a 2 joueurs : le sbire s'engage avec le PREMIER joueur, pas avec celui qui a vaincu",
        "pourquoi": ("2 joueurs : le jeton de premier joueur passe au joueur 2 (EndRound) ; Leo (joueur 1) vainc Foot Patrol "
                     "(menace reglee a 2, CTR 2) ; le sbire doit s'engager avec le PREMIER joueur (joueur 2), pas avec Leo"),
        **HEROS,
        "heros2": "spider_man",
        "mise_en_place": [FORME_HEROS, "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('tl016')",
                          "Puzzle.EndRound()"],
        "declencher": ["Puzzle.Reveal('tl014')", "Puzzle.SetThreat('tl014', 2)", "Puzzle.Thwart('tl001a')"],
        "accepter_choix": True,
        "verifier": "sbire_engage",
        "attendu": {"carte": "tl016", "joueur": "premier", "pas_vainqueur": True, "hors_jeu": ["tl014"]},
    },
]

VERIFICATIONS = r'''
def _nb_effets(face, nom_fonction):
    return [e for e in face.effect.GetAll() if nom_fonction in e.ability.func_names]


def katana_ressources(monde, aides):
    """`attendu` : {card_id: nombre de capacites CanGenerateResources portees, ou None = attendu hors jeu},
    `effets_distincts` : les deux katanas ont des effets (objets) distincts."""
    attendu = aides["cas"]["attendu"]
    soucis = []
    effets = []
    for cid, voulu in attendu.items():
        if cid == "effets_distincts":
            continue
        face = aides["par_id"](monde, cid)
        if voulu is None:
            if face is not None:
                soucis.append(f"{cid} est encore en jeu")
            continue
        if face is None:
            soucis.append(f"{cid} introuvable en jeu")
            continue
        lst = _nb_effets(face, "CanGenerateResources")
        effets += [id(e) for e in lst]
        if len(lst) != voulu:
            soucis.append(f"{cid} porte {len(lst)} ressource(s) octroyee(s) (attendu {voulu})")
    if attendu.get("effets_distincts") and len(set(effets)) != len(effets):
        soucis.append("des effets de ressource sont partages entre porteurs")
    if soucis:
        return False, " ; ".join(soucis)
    return True, f"ressources octroyees conformes : {attendu}"


def actions_disponibles(monde, aides):
    """Nombre d'actions REELLEMENT disponibles sur `carte` (type `type`), comme Puzzle.Action les numerote."""
    from game.ability.ability import AbilityType
    from game.event.manager import EventManager
    from game.message import Message
    from game.effect.rule import GameRule
    attendu = aides["cas"]["attendu"]
    face = aides["par_id"](monde, attendu["carte"])
    if face is None:
        return False, f"{attendu['carte']} introuvable en jeu"
    joueur = monde.GetCurrentPlayer()
    type_capacite = getattr(AbilityType, attendu["type"]) if attendu.get("type") else None
    candidats = [x for x in face.effect.Find(when=Message.WhenPlayerInTurn, type=type_capacite)
                 if not x.ability.is_play]
    message = Message.WhenPlayerLikeInTurn(joueur, GameRule(joueur.GetIdentity()))
    message.Send()
    dispo = EventManager.FilterAvailableEffects(message, candidats, joueur, monde, None)
    n = len(dispo)
    if n != attendu["nombre"]:
        return False, f"{attendu['carte']} offre {n} action(s) {attendu.get('type')} (attendu {attendu['nombre']})"
    return True, f"{attendu['carte']} : {n} action(s) {attendu.get('type')} disponible(s), comme attendu"


def dessus_deck(monde, aides):
    """`attendu` : dessus (card_id de la carte du dessus du deck joueur), taille, en_jeu (liste)."""
    attendu = aides["cas"]["attendu"]
    deck = monde.players[0].player_deck
    haut = deck.GetTop()
    vu = getattr(getattr(haut, "paper", None), "card_id", None)
    taille = len(list(deck.Get(True)))
    soucis = []
    if "dessus" in attendu and vu != attendu["dessus"]:
        soucis.append(f"dessus du deck = {vu} (attendu {attendu['dessus']})")
    if "dessus_pas" in attendu and vu == attendu["dessus_pas"]:
        soucis.append(f"le dessus du deck est {vu}, qui ne devait pas monter")
    if "dessus_classe" in attendu:
        classe = (getattr(getattr(haut, "paper", None), "desc", None) or {}).get("Class")
        if classe != attendu["dessus_classe"]:
            soucis.append(f"classe du dessus = {classe} (attendu {attendu['dessus_classe']})")
    if "defausse" in attendu:
        pile = [getattr(f.paper, "card_id", None) for f in monde.players[0].discard_pile.GetAll()]
        for cid in attendu["defausse"]:
            if cid not in pile:
                soucis.append(f"{cid} n'est pas dans la defausse (defausse = {pile})")
    if "taille" in attendu and taille != attendu["taille"]:
        soucis.append(f"taille du deck = {taille} (attendu {attendu['taille']})")
    for cid in attendu.get("en_jeu") or []:
        if aides["par_id"](monde, cid) is None:
            soucis.append(f"{cid} n'est pas en jeu")
    if soucis:
        return False, " ; ".join(soucis)
    return True, f"dessus du deck = {vu}, taille {taille}"


def allie_consecutif(monde, aides):
    attendu = aides["cas"]["attendu"]
    face = aides["par_id"](monde, attendu["carte"])
    if face is None:
        return False, f"{attendu['carte']} introuvable en jeu"
    lu = {"atq": face.attack, "ctr": face.thwart,
          "cons_atq": face.attack_consequential_damage, "cons_ctr": face.thwart_consequential_damage,
          "pv": face.max_health}
    ecarts = {k: (lu[k], v) for k, v in attendu.items() if k != "carte" and lu[k] != v}
    if ecarts:
        return False, f"ecarts (lu, attendu) : {ecarts}"
    return True, f"{attendu['carte']} : {lu}"


def apres_fin_de_round(monde, aides):
    """Envoie la fin de round (WhenRoundEnd + buff_manager.OnRoundEnd, comme world.end_round) puis delegue a etat_attendu."""
    from game.message import Message
    Message.WhenRoundEnd(monde).Send()
    monde.buff_manager.OnRoundEnd()
    return etat_attendu(monde, aides)


def debut_de_tour_puis_etat(monde, aides):
    """Envoie WhenPlayerTurnBegin + AfterPlayerTurnBegin (player_phase.PlayerTurn) puis delegue a etat_attendu."""
    from game.message import Message
    joueur = monde.players[0]
    debut = Message.WhenPlayerTurnBegin(joueur)
    debut.Send()
    Message.AfterPlayerTurnBegin(joueur, debut).Send()
    return etat_attendu(monde, aides)


def retiree_du_jeu(monde, aides):
    """`attendu.carte` doit etre dans la zone `area_removed` (retiree DE LA PARTIE, pas defaussee) ;
    delegue le reste (degats_identite, exhausted...) a etat_attendu."""
    attendu = aides["cas"]["attendu"]
    cid = attendu["carte"]
    retirees = [getattr(f.paper, "card_id", None) for f in monde.area_removed.GetAll()]
    defausse = [getattr(f.paper, "card_id", None) for f in monde.players[0].discard_pile.GetAll()]
    soucis = []
    if cid not in retirees:
        soucis.append(f"{cid} n'est pas retiree du jeu (retirees = {retirees}, defausse = {defausse})")
    if aides["par_id"](monde, cid) is not None:
        soucis.append(f"{cid} est encore en jeu")
    ok, msg = etat_attendu(monde, aides)
    if not ok:
        soucis.append(msg)
    if soucis:
        return False, " ; ".join(soucis)
    return True, f"{cid} retiree du jeu ; {msg}"


def sbire_engage(monde, aides):
    """`attendu.carte` : sbire en jeu ET engage avec le joueur `attendu.joueur` (rang dans monde.players) ;
    delegue le reste (hors_jeu, dans_deck_rencontre) a etat_attendu."""
    attendu = aides["cas"]["attendu"]
    cid = attendu["carte"]
    face = aides["par_id"](monde, cid)
    soucis = []
    if face is None:
        soucis.append(f"{cid} n'est pas en jeu")
    else:
        engage = face.engaged_player
        if attendu["joueur"] == "premier":
            voulu = monde.GetFirstPlayer()
            if engage is not voulu:
                soucis.append(f"{cid} n'est pas engage avec le premier joueur")
        else:
            voulu = monde.players[attendu["joueur"]]
            if engage is not voulu:
                soucis.append(f"{cid} n'est pas engage avec le joueur de rang {attendu['joueur']}")
        if attendu.get("pas_vainqueur"):
            vainqueur = monde.const_seat_order_players[0]
            if engage is vainqueur:
                soucis.append(f"{cid} est engage avec le joueur qui a vaincu Foot Patrol (siege 0)")
            if monde.GetFirstPlayer() is vainqueur:
                soucis.append("montage invalide : le premier joueur est le vainqueur")
    ok, msg = etat_attendu(monde, aides)
    if not ok:
        soucis.append(msg)
    if soucis:
        return False, " ; ".join(soucis)
    return True, f"{cid} engage avec le joueur {attendu['joueur']} ; {msg}"
'''
