# Cas test_capacites du heros CH'OD (Starjammers, Phenexian et Mysteltainn, prefixe `co`) : noms prefixes « [co] » puis le card_id
# (substituer_pack.py filtre dessus).
#
# Rappels de montage :
#  - le deck `chod` demarre en ALTER EGO (co001b) ; `Puzzle.ChangeToFace('co001b', 'co001a')` le passe en HEROS ;
#  - taille de main : Ch'od HEROS 4, ALTER EGO 5 ; ressources : 01088 Energy = YY, 01089 Genius = BB, 01090 Strength = RR ;
#    01020 Hellcat (cout 3, ressource WILD imprimee) ; 01083 Mockingbird (ressource physique) est un allie ordinaire ;
#  - Rhino 01094 est le vilain, 01097b son complot principal (menace 0 au depart), 01101 Hydra Mercenary un sbire (3 PV) ;
#  - « payer avec » une carte de la main : `payer_avec=[...]` ; la main de depart est REMPLACEE par `main_exclusive`.
SC = "rhino"
HEROS = "Puzzle.ChangeToFace('co001b', 'co001a')"
VILAIN = "01094"
COMPLOT = "01097b"
SBIRE = "01101"
SANS_BOOST = ["Puzzle.EmptyEncounterDeck()",
              "Puzzle.CreateEncounterDeck('01098', '01098', '01098', '01098', '01098', '01098', '01098', '01098')"]
DECK = lambda *ids: ["Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck(" + ", ".join(f"'{i}'" for i in ids) + ")"]


def en_jeu(*ids):
    return [f"Puzzle.PutIntoPlay('{i}', under_control=True)" for i in ids]


def _c(nom, pourquoi, mise, declencher, attendu, **cle):
    mise = SANS_BOOST + list(mise)
    cas = {"nom": "[co] " + nom, "pourquoi": pourquoi, "scenario": cle.pop("scenario", SC),
           "heros": cle.pop("heros", "chod"), "mise_en_place": mise, "declencher": declencher,
           "verifier": cle.pop("verifier", "co_etat"), "attendu": attendu}
    cas.setdefault("regles", ["v16_all", "v18_all"])
    cas.update(cle)
    return cas


CAS = [
    # ============================================================ co001a / co001b : identite
    _c("co001a Ch'od : valeurs imprimees PV 14, ATK 3, THW 2, DEF 3, HS 4, STARJAMMER",
       "nombres texte <-> code (scan) : HAND SIZE 4 / HIT POINTS 14, THW 2 ATK 3 DEF 3",
       [HEROS], [], {"pv_max": [["co001a", 14]], "traits": ["STARJAMMER"],
                     "co_stats": {"attack": 3, "thwart": 2, "defense": 3, "hand_size": 4}}),
    _c("co001b Ch'od : valeurs imprimees PV 14, REC 4, HS 5, GENIUS, OUTLAW",
       "nombres texte <-> code (scan) : HAND SIZE 5 / HIT POINTS 14 / REC 4",
       [], [], {"pv_max": [["co001b", 14]], "traits": ["GENIUS", "OUTLAW"], "co_stats": {"recover": 4, "hand_size": 5}}),
    _c("co001a Master of All Trades : jouer une carte a Requirement -> +1 taille de main (Raw Physicality = 4 + 1 = 5 degats)",
       "« When you play a card with the requirement keyword, Ch'od gets +1 hand size until the end of the player phase » : l'Interruption "
       "part AVANT la resolution de l'evenement, qui lit la taille de main augmentee",
       [HEROS], [], {"degats": [[VILAIN, 5]], "co_stats": {"hand_size": 5}},
       main_exclusive=["co003", "01090"], payer_avec=["01090"], jouer=["co003"], cibles=[VILAIN], accepter_choix=True),
    _c("co001a Master of All Trades : CONTRE-CAS, une carte SANS Requirement (Polymath payee en energie) ne donne rien",
       "« a card with the requirement keyword » : Polymath n'en a pas ; payee en [energy], seule sa ligne « Ready Ch'od » joue (heros incline -> pret)",
       [HEROS, "Puzzle.Exhaust('co001a')"], [], {"co_stats": {"hand_size": 4}, "pret": ["co001a"]},
       main_exclusive=["co005", "01088"], payer_avec=["01088"], jouer=["co005"], accepter_choix=True),
    _c("co001a Master of All Trades : TEMOIN D'EPUISEMENT, deux cartes a Requirement dans la phase -> UN seul +1 (menace 6 - 5 = 1)",
       "« (Limit once per phase.) » : Raw Physicality (+1 -> HS 5) puis Raw Intellect (limite atteinte : HS reste 5) retire 5 menaces, et non 6 (menace 6 -> 1, et non 0)",
       [HEROS, f"Puzzle.SetThreat('{COMPLOT}', 6)"], [], {"menace": [[COMPLOT, 1]], "co_stats": {"hand_size": 5}},
       main_exclusive=["co003", "co004", "01090", "01089"], payer_avec=["01090", "01089"], jouer=["co003", "co004"],
       cibles=[VILAIN, COMPLOT], accepter_choix=True),
    _c("co001b Forever Friends : defausse une carte -> Cr'reee (du deck) en main",
       "« Action: discard a card from your hand -> search your deck and discard pile for Cr'reee and add it to your hand »",
       DECK("co002", "01090", "01090"), ["Puzzle.Action('co001b', 'Action')"],
       {"co_main": ["co002"], "co_defausse": ["01090"]}, main_exclusive=["01090"], accepter_choix=True),
    _c("co001b Forever Friends : Cr'reee se trouve aussi dans la DEFAUSSE",
       "« search your deck and discard pile »",
       ["Puzzle.EmptyPlayerDeck()", "Puzzle.EmptyPlayerDiscardPile()", "Puzzle.CreatePlayerDiscardPile('co002')"],
       ["Puzzle.Action('co001b', 'Action')"], {"co_main": ["co002"]}, main_exclusive=["01090"], accepter_choix=True),
    _c("co001b Forever Friends : TEMOIN D'EPUISEMENT, deux Actions dans la phase -> UNE seule Cr'reee en main",
       "« (Limit once per phase.) » : deux Cr'reee dans le deck, deux Actions : la seconde est refusee",
       DECK("co002", "co002", "01090"), ["Puzzle.Action('co001b', 'Action')"],
       {"co_nb_main": [["co002", 1]]}, main_exclusive=["01090", "01090"], declencher_tolerant=["Puzzle.Action('co001b', 'Action')"], accepter_choix=True),

    # ============================================================ co002 Cr'reee
    _c("co002 Cr'reee : valeurs imprimees cout 2, PV 3, ATQ 1*, THW 1*",
       "nombres texte <-> code (scan)", [HEROS] + en_jeu("co002"), [],
       {"pv_max": [["co002", 3]], "attributs_carte": [["co002", "attack", 0], ["co002", "thwart", 0]]}, main_exclusive=["01090"]),
    _c("co002 Cr'reee : INCLINEE, Ch'od a +1 taille de main (4 -> 5)",
       "« While Cr'reee is exhausted, Ch'od gets +1 hand size »", [HEROS] + en_jeu("co002") + ["Puzzle.Exhaust('co002')"], [],
       {"co_stats": {"hand_size": 5}}, main_exclusive=["01090"]),
    _c("co002 Cr'reee : CONTRE-CAS, PRETE, aucun bonus (taille de main 4)",
       "la condition suit l'etat de l'allie", [HEROS] + en_jeu("co002"), [], {"co_stats": {"hand_size": 4}}, main_exclusive=["01090"]),

    # ============================================================ co003 Raw Physicality
    _c("co003 Raw Physicality : degats = taille de main (Cr'reee inclinee : 5, +1 Master of All Trades = 6)",
       "« Hero Action: deal damage to an enemy equal to your hand size » : la valeur suit la taille de main courante",
       [HEROS] + en_jeu("co002") + ["Puzzle.Exhaust('co002')"], [], {"degats": [[VILAIN, 6]]},
       main_exclusive=["co003", "01090"], payer_avec=["01090"], jouer=["co003"], cibles=[VILAIN], accepter_choix=True),
    _c("co003 Raw Physicality : CONTRE-CAS, Requirement ([physical][physical]) non satisfait (payee en [mental]) -> injouable",
       "« Requirement (RR) » : lu nativement par le moteur (desc.Requirement), la carte reste en main",
       [HEROS], [], {"degats": [[VILAIN, 0]], "en_main": ["co003"]},
       main_exclusive=["co003", "01089"], payer_avec=["01089"], jouer=["co003"], cibles=[VILAIN], accepter_choix=True),

    # ============================================================ co004 Raw Intellect
    _c("co004 Raw Intellect : retire des menaces = taille de main (4 + 1 Master = 5 : 6 -> 1)",
       "« Hero Action: remove threat from a scheme equal to your hand size »",
       [HEROS, f"Puzzle.SetThreat('{COMPLOT}', 6)"], [], {"menace": [[COMPLOT, 1]]},
       main_exclusive=["co004", "01089"], payer_avec=["01089"], jouer=["co004"], cibles=[COMPLOT], accepter_choix=True),
    _c("co004 Raw Intellect : CONTRE-CAS, Requirement ([mental][mental]) non satisfait (payee en [physical]) -> injouable",
       "« Requirement (BB) »", [HEROS, f"Puzzle.SetThreat('{COMPLOT}', 6)"], [], {"menace": [[COMPLOT, 6]], "en_main": ["co004"]},
       main_exclusive=["co004", "01090"], payer_avec=["01090"], jouer=["co004"], cibles=[COMPLOT], accepter_choix=True),

    # ============================================================ co005 Polymath
    _c("co005 Polymath : payee en [physical] -> Ch'od recoit une carte Robuste (et rien d'autre)",
       "« If you paid with a [physical]: give Ch'od a tough status card »", [HEROS, "Puzzle.Exhaust('co001a')"], [],
       {"statuts": [["co001a", "Tough"]], "exhausted": ["co001a"], "co_stats": {"hand_size": 4}},
       main_exclusive=["co005", "01090"], payer_avec=["01090"], jouer=["co005"], accepter_choix=True),
    _c("co005 Polymath : payee en [energy] -> Ch'od se redresse (pas de statut)",
       "« [energy] - Ready Ch'od »", [HEROS, "Puzzle.Exhaust('co001a')"], [],
       {"pret": ["co001a"], "statuts_absents": [["co001a", "Tough"]]},
       main_exclusive=["co005", "01088"], payer_avec=["01088"], jouer=["co005"], accepter_choix=True),
    _c("co005 Polymath : payee en [mental] -> pioche 1 carte et +1 taille de main (main 1 -> 2, HS 5)",
       "« [mental] - Draw a card. Ch'od gets +1 hand size until the end of the phase »",
       [HEROS, "Puzzle.Exhaust('co001a')"] + DECK("01090", "01090", "01090"), [],
       {"taille_main": 2, "co_stats": {"hand_size": 5}, "exhausted": ["co001a"]},
       main_exclusive=["co005", "01089", "01090"], payer_avec=["01089"], jouer=["co005"], accepter_choix=True),
    # RR « Wild Resource » : un wild depense compte pour UN type, celui que le joueur declare au paiement (26/10/2026).
    _c("co005 Polymath : payee avec un WILD (Hellcat) declare [energy] -> Ch'od se redresse, rien d'autre",
       "RR Wild Resource : le wild compte pour UN seul type, choisi par le joueur (pas les trois lignes)",
       [HEROS, "Puzzle.Exhaust('co001a')"] + DECK("01090", "01090", "01090"), [],
       {"pret": ["co001a"], "statuts_absents": [["co001a", "Tough"]], "taille_main": 0, "co_stats": {"hand_size": 4}},
       main_exclusive=["co005", "01020"], payer_avec=["01020"], jouer=["co005"], accepter_choix=True, preferer_option="Y"),
    _c("co005 Polymath : payee avec un WILD (Hellcat) declare [physical] -> carte Robuste, rien d'autre",
       "RR Wild Resource : un seul type",
       [HEROS, "Puzzle.Exhaust('co001a')"] + DECK("01090", "01090", "01090"), [],
       {"statuts": [["co001a", "Tough"]], "exhausted": ["co001a"], "taille_main": 0, "co_stats": {"hand_size": 4}},
       main_exclusive=["co005", "01020"], payer_avec=["01020"], jouer=["co005"], accepter_choix=True, preferer_option="R"),
    _c("co005 Polymath : payee avec un WILD (Hellcat) declare [mental] -> pioche 1 carte et +1 taille de main, rien d'autre",
       "RR Wild Resource : un seul type",
       [HEROS, "Puzzle.Exhaust('co001a')"] + DECK("01090", "01090", "01090"), [],
       {"taille_main": 1, "co_stats": {"hand_size": 5}, "exhausted": ["co001a"], "statuts_absents": [["co001a", "Tough"]]},
       main_exclusive=["co005", "01020"], payer_avec=["01020"], jouer=["co005"], accepter_choix=True, preferer_option="B"),

    # ============================================================ co006 Saurian Physique
    _c("co006 Saurian Physique : « Ch'od's attacks gain overkill » (sbire a 1 PV, ATQ 3 : 2 degats d'exces au vilain)",
       "overkill : l'exces d'une attaque qui abat un sbire va au vilain",
       [HEROS] + en_jeu("co006", SBIRE) + [f"Puzzle.Damage('{SBIRE}', 2)"], ["Puzzle.Attack('co001a')"],
       {"degats": [[VILAIN, 2]]}, main_exclusive=["01090"], cibles=[SBIRE], accepter_choix=True),
    _c("co006 Saurian Physique : CONTRE-CAS, sans la Condition l'exces est perdu (0 degat au vilain)",
       "temoin de l'overkill", [HEROS] + en_jeu(SBIRE) + [f"Puzzle.Damage('{SBIRE}', 2)"], ["Puzzle.Attack('co001a')"],
       {"degats": [[VILAIN, 0]]}, main_exclusive=["01090"], cibles=[SBIRE], accepter_choix=True),
    _c("co006 Saurian Physique : sbire vaincu -> elle s'incline et Ch'od a +1 taille de main (HS 5)",
       "« Hero Response: after you defeat a minion, exhaust Saurian Physique -> Ch'od gets +1 hand size until the end of the phase »",
       [HEROS] + en_jeu("co006", SBIRE) + [f"Puzzle.Damage('{SBIRE}', 2)"], ["Puzzle.Attack('co001a')"],
       {"exhausted": ["co006"], "co_stats": {"hand_size": 5}}, main_exclusive=["01090"], cibles=[SBIRE], accepter_choix=True),
    _c("co006 Saurian Physique : CONTRE-CAS, l'attaque ne vainc pas le sbire (3 PV, ATQ 3 -> vaincu) -> ici un vilain : rien",
       "« defeat a MINION » : abattre le vilain ne declenche pas la Reponse",
       [HEROS] + en_jeu("co006"), ["Puzzle.Attack('co001a')"], {"pret": ["co006"], "co_stats": {"hand_size": 4}},
       main_exclusive=["01090"], cibles=[VILAIN], accepter_choix=True),

    # ============================================================ co007 Philosopher Scientist
    _c("co007 Philosopher Scientist : Ch'od a +1 taille de main (4 -> 5)", "« Ch'od gets +1 hand size »", [HEROS] + en_jeu("co007"), [],
       {"co_stats": {"hand_size": 5}}, main_exclusive=["01090"]),

    # ============================================================ co008-co010 : ressource imprimee en main
    _c("co008 Engineer : une carte a ressource [energy] imprimee en main -> +1 taille de main (5)",
       "« While you have a card with a printed [energy] resource in your hand, Ch'od gets +1 hand size »", [HEROS] + en_jeu("co008"), [],
       {"co_stats": {"hand_size": 5}}, main_exclusive=["01088"]),
    _c("co008 Engineer : CONTRE-CAS, seulement une carte [mental] en main -> pas de bonus (4)", "la couleur compte",
       [HEROS] + en_jeu("co008"), [], {"co_stats": {"hand_size": 4}}, main_exclusive=["01089"]),
    _c("co008 Engineer : CONTRE-CAS, une ressource WILD imprimee (Hellcat) en main ne compte pour AUCUNE couleur -> 4",
       "RR Wild Resource : hors paiement, un wild n'est que « wild » et ne se lit pas comme [energy]", [HEROS] + en_jeu("co008"), [],
       {"co_stats": {"hand_size": 4}}, main_exclusive=["01020"]),
    _c("co009 Teacher : une carte a ressource [mental] imprimee en main -> +1 taille de main (5)",
       "« printed [mental] resource in your hand »", [HEROS] + en_jeu("co009"), [], {"co_stats": {"hand_size": 5}}, main_exclusive=["01089"]),
    _c("co009 Teacher : CONTRE-CAS, seulement une carte [physical] en main -> 4", "la couleur compte",
       [HEROS] + en_jeu("co009"), [], {"co_stats": {"hand_size": 4}}, main_exclusive=["01090"]),
    _c("co009 Teacher : CONTRE-CAS, une ressource WILD imprimee (Hellcat) en main ne compte pas comme [mental] -> 4",
       "RR Wild Resource : hors paiement, un wild n'est que « wild »", [HEROS] + en_jeu("co009"), [], {"co_stats": {"hand_size": 4}},
       main_exclusive=["01020"]),
    _c("co010 Warrior : CONTRE-CAS, une ressource WILD imprimee (Hellcat) en main ne compte pas comme [physical] -> 4",
       "RR Wild Resource : hors paiement, un wild n'est que « wild »", [HEROS] + en_jeu("co010"), [], {"co_stats": {"hand_size": 4}},
       main_exclusive=["01020"]),
    _c("co010 Warrior : une carte a ressource [physical] imprimee en main -> +1 taille de main (5)",
       "« printed [physical] resource in your hand »", [HEROS] + en_jeu("co010"), [], {"co_stats": {"hand_size": 5}}, main_exclusive=["01090"]),
    _c("co010 Warrior : CONTRE-CAS, seulement une carte [energy] en main -> 4", "la couleur compte",
       [HEROS] + en_jeu("co010"), [], {"co_stats": {"hand_size": 4}}, main_exclusive=["01088"]),

    # ============================================================ co011 Cr'reee Captured
    _c("co011 Cr'reee Captured : revelee, Cr'reee (du deck) est glissee dessous et 2 compteurs de recherche sont poses",
       "« When Revealed: find Cr'reee and tuck them under this card, then place 2 search counters here »",
       DECK("co002", "01090"), ["Puzzle.Reveal('co011')"],
       {"co_sous": [["co011", ["co002"]]], "compteurs": [["co011", "search", 2]]}, main_exclusive=["01090"], accepter_choix=True),
    _c("co011 Cr'reee Captured : CONTRE-CAS, Cr'reee introuvable -> les 2 compteurs sont quand meme poses, rien dessous",
       "« Find » sans cible : seule la 2e moitie de la phrase joue", DECK("01090", "01090"), ["Puzzle.Reveal('co011')"],
       {"co_sous": [["co011", []]], "compteurs": [["co011", "search", 2]]}, main_exclusive=["01090"], accepter_choix=True),
    _c("co011 Cr'reee Captured : Action d'alter ego -> Ch'od s'incline, 1 compteur retire (2 -> 1), l'obligation reste",
       "« Alter-Ego Action: exhaust Ch'od -> remove a search counter from here »",
       DECK("co002", "01090"), ["Puzzle.Reveal('co011')", "Puzzle.Action('co011', 'AlterEgoAction')"],
       {"exhausted": ["co001b"], "compteurs": [["co011", "search", 1]]}, main_exclusive=["01090"], accepter_choix=True),
    _c("co011 Cr'reee Captured : plus de compteur -> l'obligation quitte la partie",
       "« Then, if there are no search counters here, remove this obligation from the game »",
       DECK("co002", "01090"),
       ["Puzzle.Reveal('co011')", "Puzzle.Action('co011', 'AlterEgoAction')", "Puzzle.Ready('co001b')", "Puzzle.Action('co011', 'AlterEgoAction')"],
       {"retirees": ["co011"]}, main_exclusive=["01090"], accepter_choix=True),

    _c("co011 Cr'reee Captured : MESURE, ou est Cr'reee (glissee dessous) quand l'obligation quitte la partie ?",
       "le texte imprime ne le dit pas : le moteur defausse les cartes glissees sous une carte qui quitte le jeu (a verifier : defausse du joueur)",
       DECK("co002", "01090"),
       ["Puzzle.Reveal('co011')", "Puzzle.Action('co011', 'AlterEgoAction')", "Puzzle.Ready('co001b')", "Puzzle.Action('co011', 'AlterEgoAction')"],
       {"retirees": ["co011"], "co_defausse": ["co002"]}, main_exclusive=["01090"], accepter_choix=True),

    # ============================================================ co012 Mentor
    _c("co012 Mentor : engage, la taille de main du joueur baisse de 1 (4 -> 3)",
       "« While Mentor is engaged with you, your hand size is reduced by 1 »", [HEROS] + en_jeu("co012"), [],
       {"co_stats": {"hand_size": 3}}, main_exclusive=["01090"]),
    _c("co012 Mentor : valeurs imprimees PV 5, ATQ 1, SCH 3, ELITE, IMPERIAL GUARD", "nombres texte <-> code (scan)",
       [HEROS] + en_jeu("co012"), [], {"pv_max": [["co012", 5]], "attributs_carte": [["co012", "attack", 0], ["co012", "scheme", 0]]},
       main_exclusive=["01090"]),
    _c("co012 Mentor : vaincu, defausse 2 cartes du deck (R + B) -> 2 menaces sur le complot principal",
       "« When Defeated: discard the top 2 cards of your deck. Place threat on the main scheme equal to the number of different printed resources »",
       [HEROS] + en_jeu("co012") + ["Puzzle.Damage('co012', 4)"] + DECK("01090", "01089"), ["Puzzle.Attack('co001a')"],
       {"menace": [[COMPLOT, 2]]}, main_exclusive=["01083"], cibles=["co012"], accepter_choix=True),
    _c("co012 Mentor : CONTRE-CAS, deux cartes de la MEME couleur -> 1 seule menace (ressources DIFFERENTES)",
       "« different printed resources »", [HEROS] + en_jeu("co012") + ["Puzzle.Damage('co012', 4)"] + DECK("01090", "01090"),
       ["Puzzle.Attack('co001a')"], {"menace": [[COMPLOT, 1]]}, main_exclusive=["01083"], cibles=["co012"], accepter_choix=True),

    _c("co012 Mentor : vaincu, deck = WILD (Hellcat) + [physical] -> 2 ressources imprimees DIFFERENTES (wild + physique) -> 2 menaces",
       "RR Wild Resource : hors paiement un wild est un type a part (le 4e), pas trois couleurs",
       [HEROS] + en_jeu("co012") + ["Puzzle.Damage('co012', 4)"] + DECK("01020", "01090"), ["Puzzle.Attack('co001a')"],
       {"menace": [[COMPLOT, 2]]}, main_exclusive=["01083"], cibles=["co012"], accepter_choix=True),
    _c("co012 Mentor : vaincu, deck = deux WILD (Hellcat x2) -> UNE seule ressource differente -> 1 menace",
       "RR Wild Resource : le wild ne compte pas comme R + B + Y (ancien code : 3 menaces)",
       [HEROS] + en_jeu("co012") + ["Puzzle.Damage('co012', 4)"] + DECK("01020", "01020"), ["Puzzle.Attack('co001a')"],
       {"menace": [[COMPLOT, 1]]}, main_exclusive=["01083"], cibles=["co012"], accepter_choix=True),

    # Arbitrage utilisateur du 26/10/2026 (multijoueur) : « When Defeated: Discard the top 2 cards of YOUR deck » = le joueur qui a VAINCU Mentor
    # (precedent FFG : errata de Mystique's Manipulations « the defeating player »), pas le joueur engage avec lui.
    _c("co012 Mentor (arbitrage 26/10) : engage avec le JOUEUR 2, vaincu par Ch'od (joueur 1) : c'est le deck de Ch'od (R + B) qui est defausse -> 2 menaces",
       "le joueur qui a vaincu Mentor, pas le joueur engage (dont le deck, R + R, ne donnerait qu'une menace)",
       [HEROS] + en_jeu("co012") + ["Puzzle.Engage('co012', 1)", "Puzzle.Damage('co012', 4)"] + DECK("01090", "01089")
       + ["Puzzle.EmptyPlayerDeck(siege=1)", "Puzzle.CreatePlayerDeck('01090', '01090', siege=1)"], ["Puzzle.Attack('co001a')"],
       {"menace": [[COMPLOT, 2]]}, heros2="spider_man", main_exclusive=["01083"], cibles=["co012"], accepter_choix=True),
    _c("co012 Mentor (arbitrage 26/10) : CONTRE-CAS, vaincu sans vainqueur (degats directs), c'est le deck du joueur ENGAGE (joueur 2, R + R) -> 1 menace",
       "pas de joueur vainqueur : repli sur le joueur engage",
       [HEROS] + en_jeu("co012") + ["Puzzle.Engage('co012', 1)"] + DECK("01090", "01089")
       + ["Puzzle.EmptyPlayerDeck(siege=1)", "Puzzle.CreatePlayerDeck('01090', '01090', siege=1)"], ["Puzzle.Damage('co012', 5)"],
       {"menace": [[COMPLOT, 1]]}, heros2="spider_man", main_exclusive=["01083"]),

    # ============================================================ co013 Duel of Wits
    _c("co013 Duel of Wits : revelee, une carte de la main est glissee dessous ; menace 3 (une partie solo)",
       "« When Revealed: tuck a card from your hand under here » ; menace de depart 3 par joueur",
       [HEROS], ["Puzzle.Reveal('co013')"], {"co_sous": [["co013", ["01090"]]], "menace": [["co013", 3]]},
       main_exclusive=["01090"], accepter_choix=True),
    _c("co013 Duel of Wits : une carte de MEME ressource imprimee ne peut pas y retirer de menace (Raw Intellect [physical] contre 01090 [physical])",
       "« Threat cannot be removed from here by cards with a printed resource that matches the printed resource on the card tucked under here »",
       [HEROS] + en_jeu("co013") + ["Puzzle.PlaceUnder('01090', 'co013')"], [], {"menace": [["co013", 3]]},
       main_exclusive=["co004", "01089"], payer_avec=["01089"], jouer=["co004"], cibles=["co013"], accepter_choix=True),
    _c("co013 Duel of Wits : CONTRE-CAS, ressource DIFFERENTE sous la manigance ([mental]) -> la menace est retiree",
       "meme carte, mais la carte glissee est [mental] : Raw Intellect ([physical]) retire 5 menaces (menace 3 -> 0)",
       [HEROS] + en_jeu("co013") + ["Puzzle.PlaceUnder('01089', 'co013')"], [], {"hors_jeu": ["co013"]},
       main_exclusive=["co004", "01089"], payer_avec=["01089"], jouer=["co004"], cibles=["co013"], accepter_choix=True),

    _c("co013 Duel of Wits : une carte WILD glissee dessous ne correspond PAS a une carte [physical] -> la menace est retiree",
       "RR Wild Resource : hors paiement un wild ne correspond qu'a un autre wild ; Raw Intellect ([physical]) retire 5 menaces (menace 3 -> 0)",
       [HEROS] + en_jeu("co013") + ["Puzzle.PlaceUnder('01020', 'co013')"], [], {"hors_jeu": ["co013"]},
       main_exclusive=["co004", "01089"], payer_avec=["01089"], jouer=["co004"], cibles=["co013"], accepter_choix=True),

    # ============================================================ co014 Plutonia
    _c("co014 Plutonia : revelee, defausse une amelioration controlee (Philosopher Scientist)",
       "« When Revealed: discard an upgrade you control »", [HEROS] + en_jeu("co007"), ["Puzzle.Reveal('co014')"],
       {"defausse": ["co007"]}, main_exclusive=["01090"], accepter_choix=True),
    _c("co014 Plutonia : sans amelioration, defausse 1 carte AU HASARD de la main",
       "« If you cannot, discard 1 random card from your hand »", [HEROS], ["Puzzle.Reveal('co014')"],
       {"taille_main": 0, "co_defausse": ["01090"]}, main_exclusive=["01090"], accepter_choix=True),
    _c("co014 Plutonia : ses attaques ont piercing (Tough defaussee, 2 degats passent sur l'alter ego)",
       "« [star] Plutonia's attacks gain piercing »", ["Puzzle.Tough('co001b')"] + en_jeu("co014"), ["Puzzle.EnemyAttacks('co014', 'co001b')"],
       {"degats": [["co001b", 2]], "statuts_absents": [["co001b", "Tough"]]}, main_exclusive=["01090"], accepter_choix=True),
    _c("co014 Plutonia : valeurs imprimees PV 4, ATQ 2*, SCH 1", "nombres texte <-> code (scan)", [HEROS] + en_jeu("co014"), [],
       {"pv_max": [["co014", 4]], "attributs_carte": [["co014", "attack", 0], ["co014", "scheme", 0]]}, main_exclusive=["01090"]),

    # ============================================================ co015 Strike and Phase
    _c("co015 Strike and Phase : defausse le dessus du deck ([physical]) puis chaque carte de la main de meme ressource",
       "« Discard the top card of your deck, then discard each card from your hand with a resource symbol that matches that card »",
       DECK("01090"), ["Puzzle.Reveal('co015')"], {"taille_main": 2, "co_defausse": ["01090"]},
       main_exclusive=["01090", "01089", "01088"], accepter_choix=True),

    _c("co015 Strike and Phase : dessus du deck = WILD (Hellcat) -> aucune carte de la main (R, B, Y) ne correspond",
       "RR Wild Resource : un wild ne correspond qu'a un autre wild (ancien code : tout partait)",
       DECK("01020"), ["Puzzle.Reveal('co015')"], {"taille_main": 3, "co_main": ["01090", "01089", "01088"]},
       main_exclusive=["01090", "01089", "01088"], accepter_choix=True),
    _c("co015 Strike and Phase : dessus du deck = WILD, la main a un WILD et une carte [physical] -> seul le wild part",
       "RR Wild Resource : le wild defausse correspond au wild de la main, pas a la carte [physical]",
       DECK("01020", "01020"), ["Puzzle.Reveal('co015')"], {"taille_main": 1, "co_main": ["01090"], "co_defausse": ["01020"]},
       main_exclusive=["01020", "01090"], accepter_choix=True),

    # ============================================================ co016 Utter Contempt
    _c("co016 Utter Contempt : 1re branche, 2 cartes rencontre defaussees (2 + 2 icones boost) -> 4 degats indirects",
       "« Discard the top 2 cards of the encounter deck. Take indirect damage equal to the number of boost icons discarded »",
       ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01098', '01098', 'co012', 'co014')", HEROS],
       ["Puzzle.Reveal('co016')"], {"degats": [["co001a", 4]]}, main_exclusive=["01090"], preferer_option="encounter deck", accepter_choix=True),
    _c("co016 Utter Contempt : 2e branche, 2 cartes du deck (RR + YY = 4 icones) -> 4 menaces sur le complot principal",
       "« Discard the top 2 cards of your deck. Place threat on the main scheme equal to the number of printed resources discarded »",
       [HEROS] + DECK("01090", "01088"), ["Puzzle.Reveal('co016')"], {"menace": [[COMPLOT, 4]]},
       main_exclusive=["01089"], preferer_option="your deck", accepter_choix=True),
]

# ----------------------------------------------------- verifications propres au pack --
VERIFICATIONS = r'''
def co_etat(monde, aides):
    """Cles propres : `co_glissees` (card_id EXACTS sous l'identite, ordre libre), `co_nb_glissees`, `co_main` / `co_defausse`
    (presents), `co_defausse_absente`, `co_sous` ([[hote, [ids]]]), `retirees` / `retirees_absentes` (zone retiree du jeu),
    `co_stats` ({attribut: valeur} de l'identite), `co_traits_main` ([[card_id, [traits]]]) ; le reste va a etat_attendu."""
    cas = aides["cas"]
    attendu = cas.get("attendu") or {}
    soucis = []
    joueur = monde.players[0]
    identite = aides["identite"](monde)
    ids = lambda faces: [getattr(f.paper, "card_id", None) for f in faces]
    if "co_glissees" in attendu or "co_nb_glissees" in attendu:
        glissees = ids(identite.GetPlacedCardArea().Get(True))
        glissees = [g for g in glissees if g is not None]
        if "co_glissees" in attendu and sorted(glissees) != sorted(attendu["co_glissees"]):
            soucis.append(f"cartes sous l'identite = {sorted(glissees)} (attendu {sorted(attendu['co_glissees'])})")
        if "co_nb_glissees" in attendu and len(glissees) != attendu["co_nb_glissees"]:
            soucis.append(f"{len(glissees)} carte(s) sous l'identite (attendu {attendu['co_nb_glissees']}) : {sorted(glissees)}")
    main = ids(joueur.hand_cards.Get())
    for c in attendu.get("co_main") or []:
        if c not in main:
            soucis.append(f"{c} absente de la main {sorted(main)}")
    defausse = ids(joueur.discard_pile.Get())
    for c in attendu.get("co_defausse") or []:
        if c not in defausse:
            soucis.append(f"{c} absente de la defausse {sorted(defausse)}")
    for c in attendu.get("co_defausse_absente") or []:
        if c in defausse:
            soucis.append(f"{c} est dans la defausse (elle devait etre glissee)")
    retirees = ids(monde.area_removed.Get(True))
    for c in attendu.get("retirees") or []:
        if c not in retirees:
            soucis.append(f"{c} pas retiree du jeu (retirees = {retirees})")
    for c in attendu.get("retirees_absentes") or []:
        if c in retirees:
            soucis.append(f"{c} retiree du jeu (elle ne devait pas l'etre)")
    for hote_id, voulus in attendu.get("co_sous") or []:
        hote = aides["par_id"](monde, hote_id)
        if hote is None:
            soucis.append(f"{hote_id} introuvable en jeu (co_sous)")
            continue
        dessous = sorted(x for x in ids(hote.GetPlacedCardArea().Get(True)) if x is not None)
        if dessous != sorted(voulus):
            soucis.append(f"sous {hote_id} : {dessous} (attendu {sorted(voulus)})")
    for nom, valeur in (attendu.get("co_stats") or {}).items():
        courant = getattr(identite, nom, None)
        if courant != valeur:
            soucis.append(f"{nom} = {courant} (attendu {valeur})")
    cartes_main = {getattr(f.paper, "card_id", None): f for f in joueur.hand_cards.Get()}
    for card_id, traits in attendu.get("co_traits_main") or []:
        face = cartes_main.get(card_id)
        if face is None:
            soucis.append(f"{card_id} absente de la main (co_traits_main)")
            continue
        for t in ("SKILL", "THWART", "ATTACK", "DEFENSE", "TACTIC"):
            if face.HasTrait(t) != (t in traits):
                soucis.append(f"{card_id} : trait {t} {'present' if face.HasTrait(t) else 'absent'} (attendu {traits})")
    for card_id, n in attendu.get("co_nb_main") or []:
        nb = len([x for x in main if x == card_id])
        if nb != n:
            soucis.append(f"{card_id} en main : {nb} (attendu {n})")
    propres = ("co_nb_main", "co_glissees", "co_nb_glissees", "co_main", "co_defausse", "co_defausse_absente", "co_sous", "retirees",
               "retirees_absentes", "co_stats", "co_traits_main")
    reste = {k: v for k, v in attendu.items() if k not in propres}
    copie = dict(aides); copie["cas"] = dict(cas); copie["cas"]["attendu"] = reste
    ok, message = etat_attendu(monde, copie)
    if not ok:
        soucis.append(message)
    if soucis:
        return False, " ; ".join(soucis)
    return True, message
'''
