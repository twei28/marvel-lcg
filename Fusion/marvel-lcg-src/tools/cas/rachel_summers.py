# Cas test_capacites du heros RACHEL SUMMERS / MARVEL GIRL (Dipsome, campagne Hellfire Hunt, prefixe `rm`) :
# noms prefixes « [rm] » puis le card_id (substituer_pack.py filtre dessus, avec un ESPACE apres le card_id).
#
# Rappels de montage :
#  - le deck `rachel_summers` demarre en ALTER EGO (rm001b) ; `Puzzle.ChangeToFace('rm001b', 'rm001a')` la passe en HEROS sans rien
#    declencher ;
#  - « After your turn begins » : la mise en place se joue DANS le tour deja ouvert : `Puzzle.BeginPlayerTurn()` (ajout du
#    26/10/2026) envoie WhenPlayerTurnBegin + AfterPlayerTurnBegin ; il PART AVANT `jouer` (`declencher` d'abord) ;
#  - Rhino 01094 est le vilain, 01097b son complot principal, 01101 Hydra Mercenary un sbire (3 PV) ;
#  - ressources : 01088 Energy = YY, 01089 Genius = BB, 01090 Strength = RR ; rm002 (alliee, cout 2) imprime UNE ressource wild ;
#  - `Puzzle.CreatePlayerDiscardPile(a, b, c)` : `a` est le FOND de la defausse ; `Puzzle.CreatePlayerDeck(...)` : la derniere est le DESSUS.
SC = "rhino"
HEROS = "Puzzle.ChangeToFace('rm001b', 'rm001a')"
VILAIN = "01094"
COMPLOT = "01097b"
SBIRE = "01101"
SANS_BOOST = ["Puzzle.EmptyEncounterDeck()",
              "Puzzle.CreateEncounterDeck('01098', '01098', '01098', '01098', '01098', '01098', '01098', '01098')"]
DEBUT = "Puzzle.BeginPlayerTurn()"


def en_jeu(*ids):
    return [f"Puzzle.PutIntoPlay('{i}', under_control=True)" for i in ids]


def sous(hote, *ids):
    return [f"Puzzle.PlaceUnder('{i}', '{hote}')" for i in ids]


def deck(*ids):
    return ["Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck(" + ", ".join(f"'{i}'" for i in ids) + ")"]


def _c(nom, pourquoi, mise, declencher, attendu, **cle):
    mise = SANS_BOOST + list(mise)
    cas = {"nom": "[rm] " + nom, "pourquoi": pourquoi, "scenario": cle.pop("scenario", SC),
           "heros": cle.pop("heros", "rachel_summers"), "mise_en_place": mise, "declencher": declencher,
           "verifier": cle.pop("verifier", "rm_etat"), "attendu": attendu}
    cas.setdefault("regles", ["v16_all", "v18_all"])
    cas.update(cle)
    return cas


CAS = [
    # ============================================================ rm001a / rm001b : identite
    _c("rm001a Marvel Girl : valeurs imprimees PV 10, THW 3, ATK 1, DEF 2, HS 4, PSIONIC, X-FORCE",
       "nombres texte <-> code (scan) : HAND SIZE 4 / HIT POINTS 10, THW 3 ATK 1 DEF 2",
       [HEROS], [], {"pv_max": [["rm001a", 10]], "traits": ["PSIONIC", "X-FORCE"],
                     "rm_stats": {"attack": 1, "thwart": 3, "defense": 2, "hand_size": 4}}),
    _c("rm001b Rachel Summers : valeurs imprimees PV 10, REC 4, HS 5, MUTANT, PSIONIC",
       "nombres texte <-> code (scan) : HAND SIZE 5 / HIT POINTS 10 / REC 4",
       [], [], {"pv_max": [["rm001b", 10]], "traits": ["MUTANT", "PSIONIC"], "rm_stats": {"recover": 4, "hand_size": 5}}),

    # ============================================================ rm001a : Chronoskimming
    _c("rm001a Chronoskimming : la main est remelangee dans le deck puis une NOUVELLE main est piochee (4 cartes)",
       "« shuffle your hand into your deck -> draw a new hand » : main 01090 + deck de 6 rm002 : 7 cartes, 4 en main, 3 au deck",
       [HEROS] + deck(*["rm002"] * 6), [DEBUT],
       {"taille_main": 4, "taille_deck_joueur": 3}, main_exclusive=["01090"], accepter_choix=True),
    _c("rm001a Chronoskimming : le cout de la PROCHAINE carte jouee ce tour baisse de 1 (rm002, cout 2, payee par UNE carte : main 4 -> 2)",
       "« Reduce the cost of the next card you play this turn by 1 » : main de 4 rm002 piochee par la Reponse ; rm002 jouee en "
       "depensant UNE seule carte (1 ressource wild) : 4 - 1 jouee - 1 depensee = 2 en main",
       [HEROS, "Puzzle.EmptyHand()"] + deck(*["rm002"] * 6), [DEBUT],
       {"en_jeu": ["rm002"], "taille_main": 2}, jouer=["rm002"], payer_avec=["rm002"], accepter_choix=True),
    _c("rm001a Chronoskimming : CONTRE-CAS, sans la Reponse la meme carte coute 2 cartes depensees (main 4 -> 1)",
       "temoin de la reduction : meme main de 4 rm002 posee a la main, sans `BeginPlayerTurn` : cout 2 -> 2 cartes depensees + 1 jouee",
       [HEROS, "Puzzle.EmptyHand()", "Puzzle.CreateHandCards('rm002', 'rm002', 'rm002', 'rm002')"], [],
       {"en_jeu": ["rm002"], "taille_main": 1}, jouer=["rm002"], payer_avec=["rm002", "rm002"], accepter_choix=True),
    _c("rm001a Chronoskimming : CONTRE-CAS, en forme ALTER EGO la Reponse (face heros) ne part pas : la main reste",
       "la capacite est imprimee sur la face HEROS",
       ["Puzzle.EmptyHand()"] + deck(*["rm002"] * 6), [DEBUT],
       {"taille_main": 1, "taille_deck_joueur": 6}, main_exclusive=["01090"], accepter_choix=True),

    # ============================================================ rm001b : Telepathic Trickery
    _c("rm001b Telepathic Trickery : cherche Temporal Reversal dans le deck, l'ajoute en main, s'incline",
       "« Exhaust Rachel Summers -> search your deck for a copy of Temporal Reversal and add it to your hand »",
       ["Puzzle.EmptyHand()"] + deck("01090", "rm007", "01090"), ["Puzzle.Action('rm001b', 'Action')"],
       {"en_main": ["rm007"], "taille_main": 1, "taille_deck_joueur": 2, "exhausted": ["rm001b"]}, accepter_choix=True),
    _c("rm001b Telepathic Trickery : CONTRE-CAS, sans copie dans le deck rien n'est ajoute (le cout est paye)",
       "« a copy of Temporal Reversal » : le deck n'en contient pas -> main vide",
       ["Puzzle.EmptyHand()"] + deck("01090", "01090", "01090"), ["Puzzle.Action('rm001b', 'Action')"],
       {"taille_main": 0, "exhausted": ["rm001b"]}, accepter_choix=True),

    # ============================================================ rm002 Captain Britain
    _c("rm002 Captain Britain : valeurs imprimees PV 3, ATK 1, THW 1",
       "nombres texte <-> code (scan) : cout 2, HP 3, ATK 1*, THW 1*", [HEROS] + en_jeu("rm002"), [],
       {"pv_max": [["rm002", 3]], "attributs_carte": [["rm002", "attack", 0], ["rm002", "thwart", 0]]}),
    _c("rm002 Captain Britain : apres le debut du tour +1 ATQ et +1 MEN jusqu'a la fin de la phase",
       "« After your turn begins, Captain Britain gets +1 ATK and +1 THW until the end of the phase »",
       [HEROS] + en_jeu("rm002"), [DEBUT],
       {"attributs_carte": [["rm002", "attack", 1], ["rm002", "thwart", 1]]}, accepter_choix=True),
    _c("rm002 Captain Britain : CONTRE-CAS, sans debut de tour pas de bonus",
       "la Reponse ne part que sur le debut du tour", [HEROS] + en_jeu("rm002"), [],
       {"attributs_carte": [["rm002", "attack", 0], ["rm002", "thwart", 0]]}, accepter_choix=True),

    # ============================================================ rm003 Askani's Prophecies
    _c("rm003 Askani's Prophecies : redresse, soigne 1, change de forme (alter ego -> heros)",
       "« Alter-Ego Action: Ready Rachel Summers. Heal 1 damage from Rachel Summers. Change your form » : 3 degats, incline -> "
       "2 degats, pret, face heros",
       ["Puzzle.Damage('rm001b', 3)", "Puzzle.Exhaust('rm001b')"], [],
       {"en_jeu": ["rm001a"], "degats": [["rm001a", 2]], "pret": ["rm001a"]},
       main_exclusive=["rm003", "01088"], jouer=["rm003"], payer_avec=["01088"], accepter_choix=True),
    _c("rm003 Askani's Prophecies : CONTRE-CAS, en forme HEROS l'Action d'alter ego n'est pas jouable (la carte reste en main)",
       "« Alter-Ego Action » : injouable face heros", [HEROS], [], {},
       main_exclusive=["rm003", "01088"], jouer=["rm003"], payer_avec=["01088"], accepter_choix=True,
       verifier="hellcat_carte_restee_en_main", restee="rm003"),

    # ============================================================ rm004 Black Hole
    _c("rm004 Black Hole : etourdit ET desoriente un sbire et le vilain, 1 degat a chacun",
       "« Stun and confuse a minion and a villain. Deal 1 damage to the villain and each minion engaged with you »",
       [HEROS, f"Puzzle.Reveal('{SBIRE}')"], [],
       {"statuts": [[SBIRE, "Stunned"], [SBIRE, "Confused"], [VILAIN, "Stunned"], [VILAIN, "Confused"]],
        "degats": [[VILAIN, 1], [SBIRE, 1]]},
       main_exclusive=["rm004", "01088", "01089"], jouer=["rm004"], payer_avec=["01088", "01089"],
       cibles=[SBIRE, VILAIN], accepter_choix=True),
    _c("rm004 Black Hole : sans sbire en jeu la carte reste jouable et agit sur le vilain seul (choix provisoire, question en attente)",
       "« a minion and a villain » : le moteur laisse jouer la carte quand un seul des deux ciblages existe ; le vilain est sonne, "
       "desoriente et blesse",
       [HEROS], [],
       {"statuts": [[VILAIN, "Stunned"], [VILAIN, "Confused"]], "degats": [[VILAIN, 1]]},
       main_exclusive=["rm004", "01088", "01089"], jouer=["rm004"], payer_avec=["01088", "01089"],
       cibles=[VILAIN], accepter_choix=True),

    # ============================================================ rm005 Psionic Blasts
    _c("rm005 Psionic Blasts : 3 degats a l'ennemi, 3 menaces retirees, aucune pioche (ni defaite, ni derniere menace)",
       "« Deal 3 damage to the enemy... Remove 3 threat from a scheme » : Rhino 3 degats, menace 5 -> 2, main vide",
       [HEROS, f"Puzzle.SetThreat('{COMPLOT}', 5)"], [],
       {"degats": [[VILAIN, 3]], "menace": [[COMPLOT, 2]], "taille_main": 0},
       main_exclusive=["rm005", "01088"], jouer=["rm005"], payer_avec=["01088"], cibles=[VILAIN, COMPLOT],
       accepter_choix=True),
    _c("rm005 Psionic Blasts : l'attaque VAINC l'ennemi -> pioche 1 carte",
       "« If this attack defeats an enemy, draw 1 card » : Hydra Mercenary (3 PV) vaincu, menace 5 -> 2 : une seule pioche",
       [HEROS, f"Puzzle.Reveal('{SBIRE}')", f"Puzzle.SetThreat('{COMPLOT}', 5)"], [],
       {"hors_jeu": [SBIRE], "menace": [[COMPLOT, 2]], "taille_main": 1},
       main_exclusive=["rm005", "01088"], jouer=["rm005"], payer_avec=["01088"], cibles=[SBIRE, COMPLOT],
       accepter_choix=True),
    _c("rm005 Psionic Blasts : la DERNIERE menace est retiree -> pioche 1 carte",
       "« If this removes the last threat on that scheme, draw 1 card » : menace 3 -> 0, Rhino survit : une seule pioche",
       [HEROS, f"Puzzle.SetThreat('{COMPLOT}', 3)"], [],
       {"degats": [[VILAIN, 3]], "menace": [[COMPLOT, 0]], "taille_main": 1},
       main_exclusive=["rm005", "01088"], jouer=["rm005"], payer_avec=["01088"], cibles=[VILAIN, COMPLOT],
       accepter_choix=True),
    _c("rm005 Psionic Blasts : les DEUX conditions -> pioche 2 cartes",
       "ennemi vaincu ET derniere menace : deux pioches distinctes",
       [HEROS, f"Puzzle.Reveal('{SBIRE}')", f"Puzzle.SetThreat('{COMPLOT}', 3)"], [],
       {"hors_jeu": [SBIRE], "menace": [[COMPLOT, 0]], "taille_main": 2},
       main_exclusive=["rm005", "01088"], jouer=["rm005"], payer_avec=["01088"], cibles=[SBIRE, COMPLOT],
       accepter_choix=True),

    # ============================================================ rm006 Telekinetic Counterblast
    _c("rm006 Telekinetic Counterblast : apres l'attaque de Rhino, attaque de base +3 ATQ (1 + 3 = 4 degats) sans s'incliner",
       "« After an enemy attacks you, make a basic attack against that enemy without exhausting. Your hero gets +3 ATK » : "
       "heros incline pour ne pas defendre, Rhino attaque, la carte (cout 1, 01090) part en Reponse",
       [HEROS, "Puzzle.Exhaust('rm001a')"], ["Puzzle.Attack('01094')"],
       {"degats": [[VILAIN, 4]]},
       main_exclusive=["rm006", "01090"], payer_avec=["01090"], cibles=[VILAIN], accepter_choix=True),

    # ============================================================ rm007 Temporal Reversal
    _c("rm007 Temporal Reversal : jouee, elle pose UN tour supplementaire (drapeau du moteur) et va a la defausse",
       "« Take an additional turn after this one » : cout 0",
       [HEROS], [], {"rm_flag": {"RM_TOUR_SUPPLEMENTAIRE": 1}, "defausse": ["rm007"]},
       main_exclusive=["rm007"], jouer=["rm007"], accepter_choix=True),
    _c("rm007 Temporal Reversal : TEMOIN D'EPUISEMENT, « Max 1 per round » : la seconde copie ne se joue pas (1 + 0 = 1 tour)",
       "deux copies en main, une seule jouable dans le round : le drapeau reste a 1 et l'autre copie reste en main",
       [HEROS], [], {"rm_flag": {"RM_TOUR_SUPPLEMENTAIRE": 1}, "en_main": ["rm007"], "taille_main": 1},
       main_exclusive=["rm007", "rm007"], jouer=["rm007"], jouer_apres=["rm007"], accepter_choix=True),
    _c("rm007 Temporal Reversal : « Max 1 per round » vaut pour TOUS les joueurs (la copie du joueur 2 est bloquee)",
       "CORRECTIF 26/10/2026 (RR « Max » : « across all copies of a card (by title) for all players ») : le joueur 1 joue sa "
       "Temporal Reversal ; la limite du round est consommee pour la copie que le joueur 2 tient en main",
       [HEROS, "Puzzle.EmptyHand(siege=1)", "Puzzle.Gain('rm007', siege=1)"], [],
       {"rm_flag": {"RM_TOUR_SUPPLEMENTAIRE": 1}, "rm_limite_round": [["rm007", 1, False]]},
       main_exclusive=["rm007"], jouer=["rm007"], accepter_choix=True, heros2="spider_man"),
    _c("rm007 Temporal Reversal : TEMOIN de la mesure, personne n'a joue la carte -> la limite du round est LIBRE pour la copie du joueur 2",
       "ligne de base de `rm_limite_round` : sans premiere resolution la limite n'est pas consommee (la mesure distingue bien les deux etats)",
       [HEROS, "Puzzle.EmptyHand(siege=1)", "Puzzle.Gain('rm007', siege=1)"], [],
       {"rm_limite_round": [["rm007", 1, True]]},
       main_exclusive=["rm007"], accepter_choix=True, heros2="spider_man"),
    _c("rm007 Temporal Reversal : etapes de fin de tour (main de 2 -> 4, tout se redresse)",
       "« discard any number... draw up to your hand size... ready all of your cards » : HS 4, 2 cartes en main -> 4 ; heros et alliee "
       "inclines -> prets",
       [HEROS] + en_jeu("rm002") + deck(*["01090"] * 8) + ["Puzzle.Exhaust('rm001a')", "Puzzle.Exhaust('rm002')"],
       ["Puzzle.FinDeTourSupplementaire()"],
       {"taille_main": 4, "pret": ["rm001a", "rm002"]}, main_exclusive=["01088", "01089"], accepter_choix=True),
    _c("rm007 Temporal Reversal : etapes de fin de tour, main TROP PLEINE (6 -> 4 cartes)",
       "« discard down to your hand size » : 6 cartes en main, taille de main 4",
       [HEROS] + deck(*["01090"] * 8), ["Puzzle.FinDeTourSupplementaire()"],
       {"taille_main": 4}, main_exclusive=["01088", "01089", "01090", "01088", "01089", "01090"], accepter_choix=True),

    # ============================================================ rm008 Askani
    _c("rm008 Askani : Action d'alter ego, s'incline et remelange les TROIS cartes du dessus de la defausse dans le deck",
       "« Exhaust Askani -> shuffle the top three cards from your discard pile into your deck » : defausse (fond -> dessus) "
       "01088, 01089, 01090, rm002 : le fond reste, les trois du dessus rejoignent le deck",
       deck("rm009") + ["Puzzle.EmptyPlayerDiscardPile()", "Puzzle.CreatePlayerDiscardPile('01088', '01089', '01090', 'rm002')"]
       + en_jeu("rm008"), ["Puzzle.Action('rm008', 'AlterEgoAction')"],
       {"exhausted": ["rm008"], "dans_deck_joueur": ["01089", "01090", "rm002"], "taille_deck_joueur": 4,
        "rm_defausse_exacte": ["01088"]}, accepter_choix=True),
    _c("rm008 Askani : Interruption, vaincue par Rhino -> PV a 1 a la place, puis Askani est defaussee",
       "« When you would be defeated, set your hit point dial to 1 instead. Then, discard this card » : 9 degats, heros incline, "
       "Rhino attaque (ATQ 2)",
       [HEROS, "Puzzle.Damage('rm001a', 9)", "Puzzle.Exhaust('rm001a')"] + en_jeu("rm008"), ["Puzzle.Attack('01094')"],
       {"en_jeu": ["rm001a"], "degats": [["rm001a", 9]], "hors_jeu": ["rm008"], "defausse": ["rm008"]},
       main_exclusive=["01090"], accepter_choix=True),
    _c("rm008 Askani : CONTRE-CAS, un coup NON mortel : Askani reste en jeu",
       "2 degats subis seulement : pas de vaincu, l'Interruption ne part pas",
       [HEROS, "Puzzle.Damage('rm001a', 2)", "Puzzle.Exhaust('rm001a')"] + en_jeu("rm008"), ["Puzzle.Attack('01094')"],
       {"degats": [["rm001a", 4]], "en_jeu": ["rm008"]}, main_exclusive=["01090"], accepter_choix=True),

    # ============================================================ rm009 Psionic Shield
    _c("rm009 Psionic Shield : +2 DEF au heros",
       "« Marvel Girl gets +2 DEF »", [HEROS] + en_jeu("rm009"), [], {"attributs": {"defense": 2}}, main_exclusive=["01090"]),
    _c("rm009 Psionic Shield : Marvel Girl defend sans degat -> Rhino est desoriente, le bouclier s'incline",
       "« After Marvel Girl defends... and take no damage, exhaust Psionic Shield -> confuse that enemy » : DEF 4 contre ATQ 2",
       [HEROS] + en_jeu("rm009"), ["Puzzle.Attack('01094')"],
       {"degats_identite": 0, "statuts": [[VILAIN, "Confused"]], "exhausted": ["rm009"]},
       main_exclusive=["01090"], accepter_choix=True),
    _c("rm009 Psionic Shield : CONTRE-CAS, heros incline (il ne defend pas) : 2 degats subis, Rhino n'est pas desoriente",
       "« defends against an enemy attack » : sans defense, pas de Reponse",
       [HEROS, "Puzzle.Exhaust('rm001a')"] + en_jeu("rm009"), ["Puzzle.Attack('01094')"],
       {"degats_identite": 2, "statuts_absents": [[VILAIN, "Confused"]], "pret": ["rm009"]},
       main_exclusive=["01090"], accepter_choix=True),

    # ============================================================ rm010 Temporal Retrieval
    _c("rm010 Temporal Retrieval : Action, s'incline et attache une carte de la main FACE CACHEE",
       "« Exhaust Temporal Retrieval -> attach 1 card from your hand facedown here (to a maximum of 3) »",
       [HEROS] + en_jeu("rm010"), ["Puzzle.Action('rm010', 'Action')"],
       {"pose_sous": [["rm010", "01088"]], "taille_main": 0, "exhausted": ["rm010"]},
       main_exclusive=["01088"], cibles=["01088"], accepter_choix=True),
    _c("rm010 Temporal Retrieval : TEMOIN D'EPUISEMENT, avec 2 cartes attachees l'Action est encore offerte",
       "« to a maximum of 3 » : 2 attachees -> offerte", [HEROS] + en_jeu("rm010") + sous("rm010", "01088", "01089"), [],
       {"rm_action_offerte": [["rm010", "Action", True]], "taille_pose_sous": [["rm010", 2]]}, main_exclusive=["01090"]),
    _c("rm010 Temporal Retrieval : TEMOIN D'EPUISEMENT, avec 3 cartes attachees l'Action n'est PLUS offerte",
       "« to a maximum of 3 » : 3 attachees -> plus d'Action", [HEROS] + en_jeu("rm010") + sous("rm010", "01088", "01089", "01090"), [],
       {"rm_action_offerte": [["rm010", "Action", False]], "taille_pose_sous": [["rm010", 3]]}, main_exclusive=["01090"]),
    _c("rm010 Temporal Retrieval : Response apres Chronoskimming, les cartes attachees reviennent en main et la carte est defaussee",
       "« After you use your Chronoskimming ability... discard this card -> put each card attached into your hand »",
       [HEROS] + en_jeu("rm010") + sous("rm010", "01088", "01089") + deck(*["rm002"] * 6), [DEBUT],
       {"en_main": ["01088", "01089"], "defausse": ["rm010"], "hors_jeu": ["rm010"]}, main_exclusive=["01090"],
       accepter_choix=True),
    _c("rm010 Temporal Retrieval : Response apres avoir JOUE une carte TEMPORAL (Askani's Prophecies)",
       "« ... or play a TEMPORAL card » : alter ego, rm003 jouee (cout 2, 01088) -> la carte attachee (01089) revient en main",
       en_jeu("rm010") + sous("rm010", "01089"), [],
       {"en_main": ["01089"], "defausse": ["rm010"]},
       main_exclusive=["rm003", "01088"], jouer=["rm003"], payer_avec=["01088"], accepter_choix=True),
    _c("rm010 Temporal Retrieval : CONTRE-CAS, une carte NON TEMPORAL jouee (rm002) : la carte reste attachee",
       "« play a TEMPORAL card » : l'alliee n'a pas le trait", [HEROS] + en_jeu("rm010") + sous("rm010", "01089"), [],
       {"taille_pose_sous": [["rm010", 1]], "absent_main": ["01089"], "en_jeu": ["rm010", "rm002"]},
       main_exclusive=["rm002", "01088"], jouer=["rm002"], payer_avec=["01088"], accepter_choix=True),

    # ============================================================ rm011 Telekinetic Axe
    _c("rm011 Telekinetic Axe : +1 ATQ au heros", "« Marvel Girl gets +1 ATK »", [HEROS] + en_jeu("rm011"), [],
       {"attributs": {"attack": 1}}, main_exclusive=["01090"]),
    _c("rm011 Telekinetic Axe : attaque de base -> overkill (1 PV restant, 2 degats : 1 va au vilain), l'ennemi est etourdi, la hache s'incline",
       "« When Marvel Girl makes a basic attack, exhaust this card -> that attack gains overkill and stun the attacked enemy » : "
       "Hydra Mercenary a 1 PV restant",
       [HEROS, f"Puzzle.Reveal('{SBIRE}')", f"Puzzle.Damage('{SBIRE}', 2)"] + en_jeu("rm011"), [f"Puzzle.Attack('rm001a')"],
       {"hors_jeu": [SBIRE], "degats": [[VILAIN, 1]], "exhausted": ["rm011"]},
       main_exclusive=["01090"], cibles=[SBIRE], accepter_choix=True),
    _c("rm011 Telekinetic Axe : l'ennemi attaque est ETOURDI (Rhino)",
       "« stun the attacked enemy »", [HEROS] + en_jeu("rm011"), ["Puzzle.Attack('rm001a')"],
       {"statuts": [[VILAIN, "Stunned"]], "degats": [[VILAIN, 2]]}, main_exclusive=["01090"], cibles=[VILAIN],
       accepter_choix=True),
    _c("rm011 Telekinetic Axe : CONTRE-CAS, hache incline : pas d'overkill, pas d'etourdissement",
       "l'Interruption exige d'incliner la carte", [HEROS, f"Puzzle.Reveal('{SBIRE}')", f"Puzzle.Damage('{SBIRE}', 2)"]
       + en_jeu("rm011") + ["Puzzle.Exhaust('rm011')"], ["Puzzle.Attack('rm001a')"],
       {"hors_jeu": [SBIRE], "degats": [[VILAIN, 0]]}, main_exclusive=["01090"], cibles=[SBIRE], accepter_choix=True),

    # ============================================================ rm012 Telekinetic Sword
    _c("rm012 Telekinetic Sword : +3 PV", "« You get +3 hit points »", [HEROS] + en_jeu("rm012"), [],
       {"pv_max": [["rm001a", 13]]}, main_exclusive=["01090"]),
    _c("rm012 Telekinetic Sword : les attaques PERCENT (la robustesse du sbire est ignoree : 1 degat passe)",
       "« Marvel Girl attacks gain piercing » : Hydra Mercenary robuste, ATQ 1", [HEROS, f"Puzzle.Reveal('{SBIRE}')", f"Puzzle.Tough('{SBIRE}')"]
       + en_jeu("rm012"), ["Puzzle.Attack('rm001a')"],
       {"degats": [[SBIRE, 1]], "statuts_absents": [[SBIRE, "Tough"]]}, main_exclusive=["01090"], cibles=[SBIRE],
       accepter_choix=True),
    _c("rm012 Telekinetic Sword : CONTRE-CAS, sans epee la robustesse absorbe l'attaque (0 degat)",
       "temoin du piercing", [HEROS, f"Puzzle.Reveal('{SBIRE}')", f"Puzzle.Tough('{SBIRE}')"], ["Puzzle.Attack('rm001a')"],
       {"degats": [[SBIRE, 0]], "statuts_absents": [[SBIRE, "Tough"]]}, main_exclusive=["01090"], cibles=[SBIRE],
       accepter_choix=True),
    _c("rm012 Telekinetic Sword : apres une attaque, s'incline et pioche 1 carte",
       "« After you attack, exhaust Telekinetic Sword -> draw 1 card »", [HEROS] + en_jeu("rm012") + ["Puzzle.EmptyHand()"],
       ["Puzzle.Attack('rm001a')"], {"taille_main": 1, "exhausted": ["rm012"]}, cibles=[VILAIN], accepter_choix=True),

    # ============================================================ rm013 Memory From The Future
    _c("rm013 Memory From The Future : -1 taille de main (HS 5 -> 4)", "« You get -1 hand size »", ["Puzzle.Reveal('rm013')"], [],
       {"attributs": {"hand_size": -1}}),
    _c("rm013 Memory From The Future : Action d'alter ego, incline Rachel, defausse l'obligation et FINIT LE TOUR",
       "« Alter-Ego Action: Exhaust Rachel Summers -> discard this obligation and end this turn »",
       ["Puzzle.Reveal('rm013')"], ["Puzzle.Action('rm013', 'AlterEgoAction')"],
       {"defausse_rencontre": ["rm013"], "exhausted": ["rm001b"], "rm_flag": {"RM_FIN_DE_TOUR": 1}}, accepter_choix=True),
    _c("rm013 Memory From The Future : la boucle d'actions du tour LIT le drapeau et s'arrete (plus aucune carte n'est proposee)",
       "le harnais joue le cas DANS une question du pilote : on rejoue ici la boucle d'actions du tour (`WhenPlayerInTurn`), drapeau "
       "pose. Sans lecture du drapeau le pilote joue rm002 (carte en main, cout 0 impossible : on observe la main) ; avec, rien ne part",
       ["Puzzle.Reveal('rm013')"], ["Puzzle.Action('rm013', 'AlterEgoAction')"],
       {"rm_tour_fini": True, "en_main": ["01088"], "taille_main": 1}, main_exclusive=["01088"], accepter_choix=True),
    _c("rm013 Memory From The Future : CONTRE-CAS, face HEROS l'Action d'alter ego n'est pas offerte",
       "« Alter-Ego Action »", [HEROS, "Puzzle.Reveal('rm013')"], [],
       {"rm_action_offerte": [["rm013", "AlterEgoAction", False]]}),

    # ============================================================ rm014 Hound Program
    _c("rm014 Hound Program : valeurs imprimees (menace de depart 1, permanente)",
       "nombres texte <-> code (scan) : menace 1, boost 3", ["Puzzle.Reveal('rm014')"], [], {"menace": [["rm014", 1]]}),
    _c("rm014 Hound Program : au debut du tour de Marvel Girl, +1 menace (1 -> 2)",
       "« After Marvel Girl's turn begins, place 1 threat here »", [HEROS, "Puzzle.Reveal('rm014')"], [DEBUT],
       {"menace": [["rm014", 2]], "rm_partie_perdue": False}, accepter_choix=True),
    _c("rm014 Hound Program : CONTRE-CAS, en forme ALTER EGO le debut du tour ne pose rien",
       "« Marvel Girl's turn » : face heros seulement", ["Puzzle.Reveal('rm014')"], [DEBUT],
       {"menace": [["rm014", 1]], "rm_partie_perdue": False}, accepter_choix=True),
    _c("rm014 Hound Program : TEMOIN, a 4 menaces -> 5 : les joueurs PERDENT la partie",
       "« If there is at least 5 threat here, the players lose the game »", [HEROS, "Puzzle.Reveal('rm014')", "Puzzle.SetThreat('rm014', 4)"],
       [DEBUT], {"rm_partie_perdue": True}, accepter_choix=True),
    _c("rm014 Hound Program : TEMOIN, a 3 menaces -> 4 : la partie continue",
       "seuil >= 5", [HEROS, "Puzzle.Reveal('rm014')", "Puzzle.SetThreat('rm014', 3)"], [DEBUT],
       {"menace": [["rm014", 4]], "rm_partie_perdue": False}, accepter_choix=True),

    # ============================================================ rm015 Ahab
    _c("rm015 Ahab : valeurs imprimees PV 5, ATQ 3, SCH 2, ELITE CYBORG HOUNDS, Robuste a l'entree en jeu",
       "nombres texte <-> code (scan) ; « Toughness. Villainous. »", ["Puzzle.Reveal('rm015')"], [],
       {"pv_max": [["rm015", 5]], "traits_de": [["rm015", "ELITE"], ["rm015", "CYBORG"], ["rm015", "HOUNDS"]],
        "rm_stats_de": [["rm015", {"attack": 3, "scheme": 2, "villainous": 1}]], "statuts": [["rm015", "Tough"]]}),

    # ============================================================ rm016 Hound Clothes
    _c("rm016 Hound Clothes : s'attache a l'identite, -1 taille de main (HS 4 -> 3)",
       "« Attach to your identity... You get -1 hand size »", [HEROS, "Puzzle.Reveal('rm016')"], [],
       {"attaches": [["rm001a", "rm016"]], "attributs": {"hand_size": -1}}),
    _c("rm016 Hound Clothes : « Max 1 per identity » : la SECONDE copie ne s'attache pas",
       "deux copies revelees : une seule attachee", [HEROS, "Puzzle.Reveal('rm016')", "Puzzle.Reveal('rm016')"], [],
       {"taille_attaches": [["rm001a", 1]], "attributs": {"hand_size": -1}}),
    _c("rm016 Hound Clothes : Hero Action, incline l'identite et defausse la carte (la taille de main revient)",
       "« Hero Action: Exhaust your identity -> discard this card »", [HEROS, "Puzzle.Reveal('rm016')"],
       ["Puzzle.Action('rm016', 'HeroAction')"],
       {"defausse_rencontre": ["rm016"], "exhausted": ["rm001a"], "attributs": {"hand_size": 0}}, accepter_choix=True),
    _c("rm016 Hound Clothes : CONTRE-CAS, face ALTER EGO la Hero Action n'est pas offerte",
       "« Hero Action »", ["Puzzle.Reveal('rm016')"], [],
       {"rm_action_offerte": [["rm016", "HeroAction", False]]}),
    _c("rm016 Hound Clothes : ★ Boost, defausse 1 carte au hasard de la main (2 -> 1)",
       "« [star] Boost: Discard 1 card at random from your hand » : Rhino attaque, la carte est retournee en boost",
       [HEROS, "Puzzle.GiveFacedownBoost('01094', 'rm016')"], ["Puzzle.Attack('01094')"],
       {"taille_main": 1}, main_exclusive=["01088", "01089"], accepter_choix=True),
]


VERIFICATIONS = r'''
def rm_etat(monde, aides):
    """Cles propres : `rm_stats` ({attribut: valeur} de l'identite), `rm_stats_de` ([[card_id, {attribut: valeur}]]), `rm_flag`
    ({drapeau: valeur} du joueur), `rm_defausse_exacte` (card_id EXACTS de la defausse du joueur, ordre libre), `rm_partie_perdue`
    (la partie est finie sur une DEFAITE des joueurs), `rm_tour_fini` (on rejoue la boucle d'actions du tour : elle lit
    `RM_FIN_DE_TOUR` et s'arrete), `rm_action_offerte` ([[card_id, type, offerte]]) ; le reste va a etat_attendu."""
    cas = aides["cas"]
    attendu = cas.get("attendu") or {}
    soucis = []
    joueur = monde.players[0]
    identite = aides["identite"](monde)
    ids = lambda faces: [getattr(f.paper, "card_id", None) for f in faces]
    for nom, valeur in (attendu.get("rm_stats") or {}).items():
        courant = getattr(identite, nom, None)
        if courant != valeur:
            soucis.append(f"{nom} = {courant} (attendu {valeur})")
    for card_id, stats in attendu.get("rm_stats_de") or []:
        face = aides["par_id"](monde, card_id)
        if face is None:
            soucis.append(f"{card_id} introuvable en jeu (rm_stats_de)")
            continue
        for nom, valeur in stats.items():
            courant = getattr(face, nom, None)
            if courant != valeur:
                soucis.append(f"{card_id}.{nom} = {courant} (attendu {valeur})")
    for drapeau, valeur in (attendu.get("rm_flag") or {}).items():
        courant = joueur.flag.Get(drapeau)
        if courant != valeur:
            soucis.append(f"drapeau {drapeau} = {courant} (attendu {valeur})")
    if "rm_defausse_exacte" in attendu:
        defausse = sorted(x for x in ids(joueur.discard_pile.Get()) if x is not None)
        if defausse != sorted(attendu["rm_defausse_exacte"]):
            soucis.append(f"defausse = {defausse} (attendu {sorted(attendu['rm_defausse_exacte'])})")
    if "rm_partie_perdue" in attendu:
        perdue = bool(monde.is_game_over)
        if perdue != attendu["rm_partie_perdue"]:
            soucis.append(f"partie finie = {perdue} (attendu {attendu['rm_partie_perdue']})")
    if attendu.get("rm_zones"):
        soucis.append("ZONES main=%s deck=%s defausse=%s retirees=%s" % (
            ids(joueur.hand_cards.Get()), ids(joueur.player_deck.GetAll()), ids(joueur.discard_pile.Get()),
            ids(monde.area_removed.Get(True))))
    if attendu.get("rm_tour_fini"):
        # Le harnais joue le cas DANS une question du pilote : la boucle d'actions du tour (`EventManager`, message
        # `WhenPlayerInTurn`) n'a pas tourne depuis que la carte a pose `RM_FIN_DE_TOUR`. On la rejoue : si elle lit le drapeau,
        # elle s'arrete avant toute question et le remet a zero ; sinon le pilote (phase « cas ») jouerait ce qu'on lui propose.
        from game.message import Message
        if joueur.flag.Get("RM_FIN_DE_TOUR") != 1:
            soucis.append(f"RM_FIN_DE_TOUR = {joueur.flag.Get('RM_FIN_DE_TOUR')} avant la boucle (attendu 1)")
        Message.WhenPlayerInTurn(joueur, monde.round_id).Send()
        if joueur.flag.Get("RM_FIN_DE_TOUR") != 0:
            soucis.append("la boucle d'actions du tour n'a pas lu RM_FIN_DE_TOUR (drapeau toujours a 1)")
    for card_id, siege, libre in attendu.get("rm_limite_round") or []:
        # « Max 1 per round » : la limite du round est-elle encore LIBRE pour la copie de cette carte tenue en main par le joueur `siege` ?
        from game.ability.ability import AbilityType
        copie = [f for f in monde.players[siege].hand_cards.Get() if getattr(f.paper, "card_id", None) == card_id]
        if not copie:
            soucis.append(f"{card_id} absente de la main du joueur {siege} (rm_limite_round)")
            continue
        capacites = [a for a in copie[0].ability.Find(type=AbilityType.Action) if a.is_play]
        if not capacites:
            soucis.append(f"{card_id} : aucune capacite de jeu trouvee sur la copie du joueur {siege}")
            continue
        etat = all(monde.stat.IsOncePerRound(a) for a in capacites)
        if etat != libre:
            soucis.append(f"{card_id} (joueur {siege}) : limite du round {'libre' if etat else 'consommee'} (attendu {'libre' if libre else 'consommee'})")
    if attendu.get("rm_action_offerte"):
        from game.ability.ability import AbilityType
        from game.event.manager import EventManager
        from game.message import Message
        from game.effect.rule import GameRule
        for card_id, type_, voulue in attendu["rm_action_offerte"]:
            face = aides["par_id"](monde, card_id)
            if face is None:
                soucis.append(f"{card_id} introuvable en jeu (rm_action_offerte)")
                continue
            candidats = [x for x in face.effect.Find(when=Message.WhenPlayerInTurn, type=getattr(AbilityType, type_))
                         if not x.ability.is_play]
            message = Message.WhenPlayerLikeInTurn(joueur, GameRule(joueur.GetIdentity()))
            message.Send()
            offertes = EventManager.FilterAvailableEffects(message, candidats, joueur, monde, None) if candidats else []
            if bool(offertes) != voulue:
                soucis.append(f"{card_id} {type_} offerte = {bool(offertes)} (attendu {voulue})")
    propres = ("rm_stats", "rm_stats_de", "rm_flag", "rm_defausse_exacte", "rm_partie_perdue", "rm_tour_fini", "rm_action_offerte", "rm_zones", "rm_limite_round")
    reste = {k: v for k, v in attendu.items() if k not in propres}
    copie = dict(aides); copie["cas"] = dict(cas); copie["cas"]["attendu"] = reste
    ok, message = etat_attendu(monde, copie)
    if not ok:
        soucis.append(message)
    if soucis:
        return False, " ; ".join(soucis)
    return True, message
'''
