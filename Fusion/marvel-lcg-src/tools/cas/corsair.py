# Cas test_capacites du heros CORSAIR (Christopher Summers, Starjammers, prefixe `cr`) :
# noms prefixes « [cr] » puis le card_id (substituer_pack.py filtre dessus).
#
# Rappels de montage :
#  - le deck `corsair` demarre en ALTER EGO (cr001b) ; `Puzzle.ChangeToFace('cr001b', 'cr001a')` la passe en HEROS sans rien
#    declencher ; la Setup de cr001b a DEJA mis cr003 Corsair's Rapier en main au montage ;
#  - « glisser sous Corsair » : `Puzzle.PlaceUnder(carte, 'cr001a')` (face cachee) ; la zone est celle de L'IDENTITE (les deux
#    faces la partagent) ;
#  - Rhino 01094 est le vilain, 01097b son complot principal (menace 0 au depart), 01101 Hydra Mercenary un sbire (3 PV, Guard) ;
#  - ressources : 01088 Energy = YY, 01089 Genius = BB, 01090 Strength = RR ; 01083 Mockingbird (cout 3) est un allie ordinaire ;
#  - 49015 Cyclops et 36014 Havok : allies Leadership (« Cyclops or Havok » de l'obligation Irresponsible Cad) ;
#  - 08023 Quincarrier : soutien VEHICLE (Ace Pilot) ; 01023 Legal Practice : cout « defausser jusqu'a 5 cartes de la main ».
SC = "rhino"
HEROS = "Puzzle.ChangeToFace('cr001b', 'cr001a')"
CIVIL = "Puzzle.ChangeToFace('cr001a', 'cr001b')"
VILAIN = "01094"
COMPLOT = "01097b"
SBIRE = "01101"
SANS_BOOST = ["Puzzle.EmptyEncounterDeck()",
              "Puzzle.CreateEncounterDeck('01098', '01098', '01098', '01098', '01098', '01098', '01098', '01098')"]


def en_jeu(*ids):
    return [f"Puzzle.PutIntoPlay('{i}', under_control=True)" for i in ids]


def sous_corsair(*ids):
    return [f"Puzzle.PlaceUnder('{i}', 'cr001a')" for i in ids]


def _c(nom, pourquoi, mise, declencher, attendu, **cle):
    mise = SANS_BOOST + list(mise)
    cas = {"nom": "[cr] " + nom, "pourquoi": pourquoi, "scenario": cle.pop("scenario", SC),
           "heros": cle.pop("heros", "corsair"), "mise_en_place": mise, "declencher": declencher,
           "verifier": cle.pop("verifier", "cr_etat"), "attendu": attendu}
    cas.setdefault("regles", ["v16_all", "v18_all"])
    cas.update(cle)
    return cas


CAS = [
    # ============================================================ cr001a / cr001b : identite
    _c("cr001a Corsair : valeurs imprimees PV 10, ATK 1, THW 2, DEF 2, HS 5, STARJAMMER",
       "nombres texte <-> code (scan) : HAND SIZE 5 / HIT POINTS 10, THW 2 ATK 1 DEF 2",
       [HEROS], [], {"pv_max": [["cr001a", 10]], "traits": ["STARJAMMER"],
                     "cr_stats": {"attack": 1, "thwart": 2, "defense": 2, "hand_size": 5}}),
    _c("cr001b Christopher Summers : valeurs imprimees PV 10, REC 3, HS 6, OUTLAW",
       "nombres texte <-> code (scan) : HAND SIZE 6 / HIT POINTS 10 / REC 3",
       [], [], {"pv_max": [["cr001b", 10]], "traits": ["OUTLAW"], "cr_stats": {"recover": 3, "hand_size": 6}}),
    _c("cr001b Setup : Corsair's Rapier est en main des le montage",
       "« Setup: Find Corsair's Rapier and add it to your hand » : cr003 est dans le deck de heros, la Setup la met en main",
       [], [], {"cr_main": ["cr003"]}),

    # ============================================================ cr001a : jouer comme en main
    _c("cr001a Corsair : une carte glissee se JOUE comme si elle etait en main (Ace Pilot, cout 2)",
       "« You may play cards tucked under here as if they were in your hand » : cr006 glissee, payee par 01088 (YY) ; la ressource "
       "DEPENSEE de la main est a son tour glissee par les Gemmes (premier paiement du round)",
       [HEROS] + sous_corsair("cr006"), [],
       {"en_jeu": ["cr006"], "cr_glissees": ["01088"]},
       main_exclusive=["01088"], payer_avec=["01088"], jouer_glissee=["cr006"], accepter_choix=True),

    # ============================================================ cr001a : Pocket Universe Gems
    _c("cr001a Pocket Universe Gems : une carte DEPENSEE en ressource est rangee sous Corsair",
       "« After a card in your hand is discarded to pay for a cost, tuck that card under Corsair » : cr006 (cout 2) payee par "
       "01088 (YY) : 01088 est glissee, et non defaussee",
       [HEROS], [],
       {"en_jeu": ["cr006"], "cr_glissees": ["01088"]},
       main_exclusive=["cr006", "01088"], payer_avec=["01088"], jouer=["cr006"], accepter_choix=True),
    _c("cr001a Pocket Universe Gems : une carte SKILL depensee en ressource n'est glissee QU'UNE fois (Gems et Rapier)",
       "CORRECTIF 26/10/2026 : la carte depensee est DEFAUSSEE puis glissee ; Corsair's Rapier (cr003, « after you discard a SKILL "
       "card ») la voit aussi, mais une seule des deux Reponses peut la glisser : cr007 Parry (SKILL, physique) paie cr009 Remise "
       "(cout 1), elle finit sous Corsair, une seule fois",
       [HEROS], en_jeu("cr003"),
       {"cr_glissees": ["cr007"], "en_jeu": ["cr003"]},
       main_exclusive=["cr009", "cr007"], payer_avec=["cr007"], jouer=["cr009"], cibles=[VILAIN], accepter_choix=True),
    _c("cr001a Pocket Universe Gems : TEMOIN D'EPUISEMENT, deux cartes jouees dans le round -> UNE seule glissee",
       "« (Limit once per round.) » : 1 + 0 = 1 carte sous Corsair apres deux paiements (01088 puis 01089)",
       [HEROS], [],
       {"en_jeu": ["cr006", "cr003"], "cr_nb_glissees": 1},
       main_exclusive=["cr006", "cr003", "01088", "01089"], payer_avec=["01088", "01089"], jouer=["cr006"],
       jouer_apres=["cr003"], accepter_choix=True),
    _c("cr001a Pocket Universe Gems : Gemmes EPUISEES (1re carte glissee), une carte SKILL depensee ensuite est glissee par RAPIER",
       "CORRECTIF 26/10/2026 (cas ajoute pour DISTINGUER l'ancien du nouveau comportement) : la carte depensee est defaussee (zone de "
       "ressources -> defausse) et chaque Reponse « after you discard » la voit. cr006 (cout 2) est payee par 01088 : Gemmes la glisse "
       "(limite d'une fois par round atteinte) ; puis cr009 Remise (cout 1) est payee par cr007 Parry (SKILL) : Gemmes est epuisee, "
       "seule Corsair's Rapier (cr003, s'incline) peut la glisser. Sans la defausse prealable, Rapier ne la voyait pas",
       [HEROS], en_jeu("cr003"),
       {"cr_glissees": ["01088", "cr007"], "exhausted": ["cr003"]},
       main_exclusive=["cr006", "cr009", "01088", "cr007"], payer_avec=["01088", "cr007"], jouer=["cr006"], jouer_apres=["cr009"],
       cibles=[VILAIN], accepter_choix=True),
    _c("cr001a Pocket Universe Gems : defausse en COUT d'une carte (Plan B 27024) -> la carte defaussee est glissee",
       "« a cost is anything before the arrow » : 27024 Plan B, « Hero Action: exhaust Plan B and discard 1 random card from your "
       "hand -> deal 2 damage » ; la seule carte de la main (01090) est defaussee en cout puis glissee sous Corsair",
       [HEROS], en_jeu("27024") + ["Puzzle.Action('27024', 'HeroAction')"],
       {"cr_glissees": ["01090"], "degats": [[VILAIN, 2]]},
       main_exclusive=["01090"], cibles=[VILAIN], accepter_choix=True),
    _c("cr001a Pocket Universe Gems : CONTRE-CAS, une carte defaussee SANS payer de cout (DiscardAtRandom) n'est pas glissee",
       "« to pay for a cost » : une defausse d'effet (Puzzle.Discard) ne declenche pas la Reponse de Corsair",
       [HEROS], ["Puzzle.DiscardAtRandom(1)"],
       {"cr_nb_glissees": 0, "cr_defausse": ["01090"]},
       main_exclusive=["01090"], accepter_choix=True),

    # ============================================================ cr002 Hepzibah
    _c("cr002 Hepzibah : une carte glissee defaussee -> +3 ATQ (2 + 3 = 5 degats a Rhino)",
       "« When Hepzibah uses a basic power, discard a card tucked under Corsair -> +3 to that power for this use »",
       [HEROS] + en_jeu("cr002") + sous_corsair("cr006"), ["Puzzle.Attack('cr002')"],
       {"degats": [[VILAIN, 5]], "cr_glissees": [], "cr_defausse": ["cr006"]},
       main_exclusive=["01090"], cibles=[VILAIN], accepter_choix=True),
    _c("cr002 Hepzibah : +3 aussi a la MENEE (THW 0 + 3 = 3 menaces retirees)",
       "« uses a basic power » : l'Interruption vaut pour toute puissance de base",
       [HEROS] + en_jeu("cr002") + sous_corsair("cr006") + [f"Puzzle.SetThreat('{COMPLOT}', 5)"], ["Puzzle.Thwart('cr002')"],
       {"menace": [[COMPLOT, 2]], "cr_glissees": []},
       main_exclusive=["01090"], cibles=[COMPLOT], accepter_choix=True),
    _c("cr002 Hepzibah : CONTRE-CAS, aucune carte glissee -> ATQ imprimee seule (2 degats)",
       "la Reponse n'est pas offerte sans carte glissee",
       [HEROS] + en_jeu("cr002"), ["Puzzle.Attack('cr002')"],
       {"degats": [[VILAIN, 2]], "cr_glissees": []},
       main_exclusive=["01090"], cibles=[VILAIN], accepter_choix=True),
    _c("cr002 Hepzibah : valeurs imprimees cout 3, PV 3 (ATQ 2*, THW 0*)",
       "nombres texte <-> code (scan)",
       [HEROS] + en_jeu("cr002"), [],
       {"pv_max": [["cr002", 3]], "attributs_carte": [["cr002", "attack", 0], ["cr002", "thwart", 0]]},
       main_exclusive=["01090"]),

    # ============================================================ cr003 Corsair's Rapier
    _c("cr003 Corsair's Rapier : +1 ATQ au heros (ATQ 2)",
       "« Corsair gets +1 ATK »", [HEROS] + en_jeu("cr003"), [],
       {"attributs": {"attack": +1}}, main_exclusive=["01090"]),
    _c("cr003 Corsair's Rapier : CONTRE-CAS, le bonus ne vaut qu'en forme heros (alter ego : pas de bonus)",
       "bonus continu d'identite : contre-cas dans l'AUTRE forme (RECETTES §3)",
       en_jeu("cr003"), [], {"cr_stats": {"recover": 3}}, main_exclusive=["01090"]),
    _c("cr003 Corsair's Rapier : apres avoir defausse une carte SKILL de la main, elle s'incline et la glisse",
       "« After you discard a SKILL card from your hand, exhaust Rapier -> tuck that card under Corsair » : cr006 Ace Pilot (SKILL, "
       "seule carte en main, defaussee par `Puzzle.DiscardAtRandom` : `Puzzle.Discard` fabrique une copie HORS de la main)",
       [HEROS], en_jeu("cr003") + ["Puzzle.DiscardAtRandom(1)"],
       {"cr_glissees": ["cr006"], "exhausted": ["cr003"]},
       main_exclusive=["cr006"], accepter_choix=True),
    _c("cr003 Corsair's Rapier : CONTRE-CAS, une carte non SKILL defaussee (01090 Strength) n'est pas glissee",
       "« a SKILL card » : une ressource basique ne declenche rien",
       [HEROS], en_jeu("cr003") + ["Puzzle.DiscardAtRandom(1)"],
       {"cr_glissees": [], "pret": ["cr003"], "cr_defausse": ["01090"]},
       main_exclusive=["01090"], accepter_choix=True),

    # ============================================================ cr004 Pulse Blaster
    _c("cr004 Pulse Blaster : entre en jeu avec 3 compteurs de charge",
       "« Uses (3 charge counters) » (compteurs poses a la main : la cle `Uses` defausserait la carte au dernier compteur)",
       [HEROS] + en_jeu("cr004"), [], {"compteurs": [["cr004", "charge", 3]]}, main_exclusive=["01090"]),
    _c("cr004 Pulse Blaster : apres une attaque, -1 compteur et 1 degat de plus (1 + 1 = 2 a Rhino)",
       "« After you attack an enemy, remove 1 charge counter -> deal 1 damage to an enemy »",
       [HEROS] + en_jeu("cr004"), ["Puzzle.Attack('cr001a')"],
       {"degats": [[VILAIN, 2]], "compteurs": [["cr004", "charge", 2]]},
       main_exclusive=["01090"], cibles=[VILAIN, VILAIN], accepter_choix=True),
    _c("cr004 Pulse Blaster : le DERNIER compteur retire -> la carte est glissee sous Corsair (et non defaussee)",
       "« If you removed the last charge counter from Pulse Blaster this way, tuck it under Corsair »",
       [HEROS] + en_jeu("cr004") + ["Puzzle.Counter('cr004', 'charge', -2)"], ["Puzzle.Attack('cr001a')"],
       {"cr_glissees": ["cr004"], "hors_jeu": ["cr004"]},
       main_exclusive=["01090"], cibles=[VILAIN, VILAIN], accepter_choix=True),

    # ============================================================ cr005 Corsair's Gloves
    _c("cr005 Corsair's Gloves : paient la carte GLISSEE jouee (Rapier, cout 1) : les gants s'inclinent",
       "« generate a [wild] resource for a card tucked under Corsair » : main vide, cr003 glissee, 1 ressource suffit",
       [HEROS, "Puzzle.EmptyHand()"] + en_jeu("cr005") + sous_corsair("cr003"), [],
       {"en_jeu": ["cr003"], "exhausted": ["cr005"]},
       jouer_glissee=["cr003"], accepter_choix=True),
    _c("cr005 Corsair's Gloves : CONTRE-CAS, ne paient PAS une carte de la main (cr003 en main, aucune ressource)",
       "« for a card tucked under Corsair » seulement : cr003 reste injouable en main",
       [HEROS] + en_jeu("cr005"), [], {"pret": ["cr005"]},
       main_exclusive=["cr003"], jouer=["cr003"], accepter_choix=True,
       verifier="hellcat_carte_restee_en_main", restee="cr003"),

    # ============================================================ cr006 Ace Pilot
    _c("cr006 Ace Pilot : apres un evenement THWART (Trick up my Sleeve), l'identite se redresse",
       "« After you play an ATTACK or THWART event, exhaust Ace Pilot -> ready your identity » : le heros etait incline",
       [HEROS] + en_jeu("cr006") + ["Puzzle.Exhaust('cr001a')", f"Puzzle.SetThreat('{COMPLOT}', 5)"], [],
       {"pret": ["cr001a"], "exhausted": ["cr006"]},
       main_exclusive=["cr010", "01090", "01089"], payer_avec=["01090", "01089"], jouer=["cr010"], cibles=[COMPLOT], accepter_choix=True),
    _c("cr006 Ace Pilot : redresse AUSSI un VEHICLE que l'on controle (Quincarrier)",
       "« ready your identity and a VEHICLE you control » : 08023 inclinee, redressee",
       [HEROS] + en_jeu("cr006", "08023") + ["Puzzle.Exhaust('cr001a')", "Puzzle.Exhaust('08023')", f"Puzzle.SetThreat('{COMPLOT}', 5)"], [],
       {"pret": ["cr001a", "08023"], "exhausted": ["cr006"]},
       main_exclusive=["cr010", "01090", "01089"], payer_avec=["01090", "01089"], jouer=["cr010"], cibles=[COMPLOT], accepter_choix=True),

    # ============================================================ cr007 Parry
    _c("cr007 Parry : defense +3 DEF et pioche 1 carte (Rhino attaque)",
       "« he gets +3 DEF for that attack. Draw 1 card » : la main passe de 0 a 1 carte apres le jeu de Parry",
       [HEROS, "Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01073', '01074', '01073')"], ["Puzzle.Attack('01094')"],
       {"taille_main": 1, "defausse": ["cr007"], "degats_identite": 0},
       main_exclusive=["cr007"], accepter_choix=True),
    _c("cr007 Parry : +3 DEF MESURE, attaque boostee (2 + 2 = 4 contre DEF 2) -> 0 degat avec Parry",
       "« he gets +3 DEF for that attack » : Rhino (ATK 2) + une carte boost a 2 icones (01103 Shocker) = 4 contre DEF 2 : 2 degats SANS Parry "
       "(contre-cas ci-dessous), 0 avec Parry (DEF 5). La carte est bien JOUEE (defausse), la main n'est pas Parry elle-meme (taille 1 = la pioche)",
       [HEROS, "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01103', '01103', '01103', '01103')",
        "Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01073', '01074', '01073')"], ["Puzzle.Attack('01094')"],
       {"taille_main": 1, "defausse": ["cr007"], "degats_identite": 0},
       main_exclusive=["cr007"], accepter_choix=True),
    _c("cr007 Parry : CONTRE-CAS sans Parry, meme attaque boostee -> 2 degats a l'identite (la mesure DEF est donc discriminante)",
       "meme montage, Parry absente de la main : 4 - DEF 2 = 2 degats",
       [HEROS, "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01103', '01103', '01103', '01103')"],
       ["Puzzle.Attack('01094')"], {"degats_identite": 2}, main_exclusive=["01090"], accepter_choix=True),
    _c("cr007 Parry : apres REMISE (derniere carte jouee), la pioche passe a 3 cartes",
       "« If the last card you played was Remise, draw 3 cards instead » : Remise (cout 1, 01090) puis, quand Rhino attaque, Parry "
       "(cout 0) : la main (vide) se remplit de 3 cartes",
       [HEROS, "Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01073', '01074', '01073', '01074', '01073')"], [],
       {"taille_main": 3},
       main_exclusive=["cr009", "cr007", "01090"], payer_avec=["01090"], jouer=["cr009"], cibles=[VILAIN], accepter_choix=True,
       declencher_apres=["Puzzle.Attack('01094')"]),
    _c("cr007 Parry : Remise jouee au round PRECEDENT compte encore comme « la derniere carte jouee » (pioche 3)",
       "CORRECTIF 26/10/2026 : « the last card you played » n'est pas borne au round (RR : aucune borne) ; Remise jouee, le round "
       "change (`Puzzle.PlayersNewRound`), puis Rhino attaque et Parry est jouee : la main (vide) se remplit de 3 cartes",
       [HEROS, "Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01073', '01074', '01073', '01074', '01073')"], [],
       {"taille_main": 3},
       main_exclusive=["cr009", "cr007", "01090"], payer_avec=["01090"], jouer=["cr009"], cibles=[VILAIN], accepter_choix=True,
       declencher_apres=["Puzzle.PlayersNewRound()", "Puzzle.Attack('01094')"]),
    _c("cr007 Parry : valeurs imprimees cout 0, traits DEFENSE SKILL",
       "nombres texte <-> code (scan)", [HEROS], [],
       {"cr_traits_main": [["cr007", ["DEFENSE", "SKILL"]]]}, main_exclusive=["cr007"]),

    # ============================================================ cr008 Riposte
    _c("cr008 Riposte : apres l'attaque d'un ennemi, 4 degats a CET ennemi (Rhino)",
       "« After an enemy attacks you, deal 4 damage to that enemy » : cout 1 (01090 RR)",
       [HEROS], ["Puzzle.Attack('01094')"],
       {"degats": [[VILAIN, 4]], "statuts_absents": [[VILAIN, "Stunned"]]},
       main_exclusive=["cr008", "01090"], payer_avec=["01090"], accepter_choix=True),
    _c("cr008 Riposte : apres PARRY (jouee pendant la meme attaque), l'ennemi est aussi sonne",
       "« If the last card you played was Parry, stun that enemy » : Parry (cout 0) en defense, puis Riposte (cout 1)",
       [HEROS], ["Puzzle.Attack('01094')"],
       {"degats": [[VILAIN, 4]], "statuts": [[VILAIN, "Stunned"]]},
       main_exclusive=["cr007", "cr008", "01090"], payer_avec=["01090"], accepter_choix=True),
    _c("cr008 Riposte : Parry jouee au round PRECEDENT compte encore (l'ennemi est sonne)",
       "CORRECTIF 26/10/2026 : « the last card you played » n'est pas borne au round : Parry (cout 0) en defense au round 1, le round "
       "change, puis Rhino attaque encore et Riposte (cout 1, 01090) est jouee : 4 degats ET l'ennemi sonne",
       [HEROS, "Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01073', '01074', '01073')"], ["Puzzle.Attack('01094')"],
       {"degats": [[VILAIN, 4]], "statuts": [[VILAIN, "Stunned"]]},
       main_exclusive=["cr007"], payer_avec=["01090"], accepter_choix=True,
       declencher_apres=["Puzzle.PlayersNewRound()", "Puzzle.EmptyHand()", "Puzzle.Gain('cr008')", "Puzzle.Gain('01090')",
                         "Puzzle.Attack('01094')"]),
    _c("cr008 Riposte : valeurs imprimees cout 1, traits ATTACK SKILL",
       "nombres texte <-> code (scan)", [HEROS], [],
       {"cr_traits_main": [["cr008", ["ATTACK", "SKILL"]]]}, main_exclusive=["cr008"]),

    # ============================================================ cr009 Remise
    _c("cr009 Remise : 3 degats a Rhino",
       "« Deal 3 damage to an enemy »", [HEROS], [],
       {"degats": [[VILAIN, 3]], "defausse": ["cr009"]},
       main_exclusive=["cr009", "01090"], payer_avec=["01090"], jouer=["cr009"], cibles=[VILAIN], accepter_choix=True),
    _c("cr009 Remise : apres Riposte, Corsair se redresse (le heros etait incline)",
       "« If the last card you played was Riposte, ready Corsair » : Rhino attaque, Riposte (cout 1, 01090) en Reponse, puis "
       "Remise (cout 1, 01089) : 4 + 3 = 7 degats, heros redresse",
       [HEROS, "Puzzle.Exhaust('cr001a')"], ["Puzzle.Attack('01094')"],
       {"degats": [[VILAIN, 7]], "pret": ["cr001a"]},
       main_exclusive=["cr008", "cr009", "01090", "01089"], payer_avec=["01090", "01089"],
       jouer_apres=["cr009"], cibles=[VILAIN, VILAIN], accepter_choix=True),
    _c("cr009 Remise : Riposte jouee au round PRECEDENT compte encore, Corsair se redresse",
       "CORRECTIF 26/10/2026 : « the last card you played » n'est pas borne au round : Riposte jouee pendant la phase du vilain "
       "(Rhino attaque), le round change, puis Remise au tour suivant : 4 + 3 = 7 degats, heros redresse",
       [HEROS, "Puzzle.Exhaust('cr001a')"], ["Puzzle.Attack('01094')"],
       {"degats": [[VILAIN, 7]], "pret": ["cr001a"]},
       main_exclusive=["cr008", "01090"], payer_avec=["01090", "01089"], jouer_apres=["cr009"], cibles=[VILAIN, VILAIN],
       accepter_choix=True,
       declencher_apres=["Puzzle.PlayersNewRound()", "Puzzle.EmptyHand()", "Puzzle.Gain('cr009')", "Puzzle.Gain('01089')"]),
    _c("cr009 Remise : CONTRE-CAS, la derniere carte jouee n'est pas Riposte -> le heros reste incline",
       "seule Riposte compte : Remise jouee seule, le heros incline le reste",
       [HEROS, "Puzzle.Exhaust('cr001a')"], [],
       {"degats": [[VILAIN, 3]], "exhausted": ["cr001a"]},
       main_exclusive=["cr009", "01090"], payer_avec=["01090"], jouer=["cr009"], cibles=[VILAIN], accepter_choix=True),

    # ============================================================ cr010 Trick up my Sleeve
    _c("cr010 Trick up my Sleeve : 4 menaces retirees (6 -> 2)",
       "« Remove 4 threat from a scheme »", [HEROS, f"Puzzle.SetThreat('{COMPLOT}', 6)"], [],
       {"menace": [[COMPLOT, 2]]},
       main_exclusive=["cr010", "01090", "01089"], payer_avec=["01090", "01089"], jouer=["cr010"], cibles=[COMPLOT], accepter_choix=True),
    _c("cr010 Trick up my Sleeve : une carte glissee defaussee -> un ennemi est desoriente",
       "« You may discard a card tucked under Corsair to confuse an enemy »",
       [HEROS, f"Puzzle.SetThreat('{COMPLOT}', 6)"] + sous_corsair("cr006"), [],
       {"menace": [[COMPLOT, 2]], "statuts": [[VILAIN, "Confused"]], "cr_nb_glissees": 1},
       main_exclusive=["cr010", "01090", "01089"], payer_avec=["01090", "01089"], jouer=["cr010"], cibles=[COMPLOT, VILAIN],
       accepter_choix=True),

    # ============================================================ cr011 Irresponsible Cad
    _c("cr011 Irresponsible Cad : Cyclops defausse -> l'obligation quitte la partie",
       "« If the discarded card was Cyclops or Havok, remove this card from the game »",
       [HEROS] + en_jeu("49015", "01083"), ["Puzzle.Reveal('cr011')"],
       {"retirees": ["cr011"], "defausse": ["49015"]},
       cibles=["49015"], accepter_choix=True),
    _c("cr011 Irresponsible Cad : un autre allie (Mockingbird) defausse -> surge, l'obligation est defaussee",
       "« Otherwise, this card gains surge, then discard this obligation » : retiree de la partie : NON",
       [HEROS] + en_jeu("01083"), ["Puzzle.Reveal('cr011')"],
       {"defausse": ["01083"], "hors_jeu": ["cr011"]},
       cibles=["01083"], accepter_choix=True),

    # ============================================================ cr012 Making Amends
    _c("cr012 Making Amends : alter ego, 1re branche -> Christopher s'incline et l'obligation quitte la partie",
       "« Exhaust Christopher Summers ... -> remove Making Amends from the game »",
       [], ["Puzzle.Reveal('cr012')"],
       {"retirees": ["cr012"], "exhausted": ["cr001b"]},
       heros="corsair_making_amends", accepter_choix=True),
    _c("cr012 Making Amends : 2e branche -> une carte controlee defaussee, surge, l'obligation defaussee",
       "« Discard a card you control. This card gains surge. Discard this obligation » : l'alter ego est DEJA incline, la 1re branche "
       "(inclinaison) est impayable : le pilote prend la 2e",
       ["Puzzle.Exhaust('cr001b')"] + en_jeu("01083"), ["Puzzle.Reveal('cr012')"],
       {"defausse": ["01083"], "hors_jeu": ["cr012"]},
       heros="corsair_making_amends", cibles=["01083"]),

    # ============================================================ cr013 D'Ken
    _c("cr013 D'Ken : attaquer D'Ken coute une carte de la main (4 -> 3 cartes... ici 1 -> 0)",
       "« As an additional cost to attack D'Ken, you must discard a card from your hand »",
       [HEROS] + en_jeu("cr013"), ["Puzzle.Attack('cr001a')"],
       {"taille_main": 0, "degats": [["cr013", 1]]},
       main_exclusive=["01090"], cibles=["cr013", "cr013"], accepter_choix=True),
    _c("cr013 D'Ken : main vide -> l'attaque est impossible (aucun degat)",
       "pas de carte a defausser : l'attaque n'a pas lieu",
       [HEROS, "Puzzle.EmptyHand()"] + en_jeu("cr013"), ["Puzzle.Attack('cr001a')"],
       {"degats": [["cr013", 0]]},
       cibles=["cr013", "cr013"], accepter_choix=True),
    _c("cr013 D'Ken : valeurs imprimees PV 5, ATQ 1, SCH 1, ELITE KING SHI'AR",
       "nombres texte <-> code (scan)", [HEROS] + en_jeu("cr013"), [],
       {"pv_max": [["cr013", 5]], "attributs_carte": [["cr013", "attack", 0], ["cr013", "scheme", 0]],
        "traits_de": [["cr013", "ELITE"], ["cr013", "KING"], ["cr013", "SHI'AR"]]}, main_exclusive=["01090"]),

    # ============================================================ cr014 Slave Pits of Chandilar
    _c("cr014 Slave Pits : revelee, un allie controle est glisse sous la manigance (face cachee)",
       "« Each player places an ally or PERSONA support they control facedown under here »",
       [HEROS] + en_jeu("01083"), ["Puzzle.Reveal('cr014')"],
       {"hors_jeu": ["01083"], "cr_sous": [["cr014", ["01083"]]]},
       cibles=["01083"], accepter_choix=True),
    _c("cr014 Slave Pits : sans allie ni soutien PERSONA, le joueur defausse 1 carte de sa main",
       "« Each player who cannot discards 1 card from their hand »",
       [HEROS], ["Puzzle.Reveal('cr014')"],
       {"taille_main": 1, "cr_sous": [["cr014", []]]},
       main_exclusive=["01090", "01089"], cibles=["01090"], accepter_choix=True),
    _c("cr014 Slave Pits : vaincue (menace retiree), l'allie revient en jeu sous le controle de son proprietaire",
       "« When Defeated: Return each facedown card here to play under its owner's control »",
       [HEROS] + en_jeu("01083") + ["Puzzle.Damage('01083', 1)"], ["Puzzle.Reveal('cr014')", "Puzzle.Thwart('cr001a')"],
       {"en_jeu": ["01083"], "hors_jeu": ["cr014"], "degats": [["01083", 0]]},
       cibles=["01083", "cr014"], accepter_choix=True),
    _c("cr014 Slave Pits : valeurs imprimees menace 2 par joueur, 1 icone Acceleration",
       "nombres texte <-> code (scan) : une partie solo => 2 menaces",
       [HEROS], ["Puzzle.Reveal('cr014')"],
       {"menace": [["cr014", 2]]}, main_exclusive=["01090"]),

    # ============================================================ cr015 Shi'ar Bodyguard
    _c("cr015 Shi'ar Bodyguard : « Players cannot attack ELITE minions » (D'Ken, ELITE, ne peut pas etre attaque)",
       "le heros attaque D'Ken pendant que le garde du corps est en jeu : aucun degat sur D'Ken",
       [HEROS] + en_jeu("cr015", "cr013"), ["Puzzle.Attack('cr001a')"],
       {"degats": [["cr013", 0]]},
       main_exclusive=["01090"], cibles=["cr013"], accepter_choix=True),
    _c("cr015 Shi'ar Bodyguard : valeurs imprimees PV 4, ATQ 2, SCH 1, SHI'AR",
       "nombres texte <-> code (scan)", [HEROS] + en_jeu("cr015"), [],
       {"pv_max": [["cr015", 4]], "traits_de": [["cr015", "SHI'AR"]],
        "attributs_carte": [["cr015", "attack", 0], ["cr015", "scheme", 0]]}, main_exclusive=["01090"]),

    # ============================================================ cr016 Shi'ar Battle Cruiser
    _c("cr016 Shi'ar Battle Cruiser : fin de la phase vilain -> 1 degat indirect a chaque joueur",
       "« When the villain phase ends, deal 1 indirect damage to each player »",
       [HEROS] + en_jeu("cr016"), ["Puzzle.EndVillainPhase()"],
       {"degats_identite": 1}, main_exclusive=["01090"], accepter_choix=True),
    _c("cr016 Shi'ar Battle Cruiser : Hero Action, incliner l'identite et depenser YY -> defausser la carte",
       "« Exhaust your identity and spend [energy][energy] -> discard this card » : 01088 (YY)",
       [HEROS] + en_jeu("cr016"), ["Puzzle.Action('cr016', 'HeroAction')"],
       {"hors_jeu": ["cr016"], "exhausted": ["cr001a"]},
       main_exclusive=["01088"], payer_avec=["01088"], accepter_choix=True),
    _c("cr016 Shi'ar Battle Cruiser : ALLIANCE (2 joueurs), l'AUTRE joueur paie les YY de la Hero Action",
       "CORRECTIF 26/10/2026 (RR « Alliance » : « While paying costs for this card, any player may contribute ») : la main de Corsair "
       "(01090, physique) ne couvre pas YY ; le joueur 2 a 01088 (YY) en main : la carte est defaussee, l'identite s'incline",
       [HEROS] + en_jeu("cr016") + ["Puzzle.EmptyHand(siege=1)", "Puzzle.Gain('01088', siege=1)"],
       ["Puzzle.Action('cr016', 'HeroAction')"],
       {"hors_jeu": ["cr016"], "exhausted": ["cr001a"]},
       main_exclusive=["01090"], payer_avec=["01088"], accepter_choix=True, heros2="spider_man"),
]


VERIFICATIONS = r'''
def cr_etat(monde, aides):
    """Cles propres : `cr_glissees` (card_id EXACTS sous Corsair, ordre libre), `cr_nb_glissees`, `cr_main` / `cr_defausse`
    (presents), `cr_defausse_absente`, `cr_sous` ([[hote, [ids]]]), `retirees` / `retirees_absentes` (zone retiree du jeu),
    `cr_stats` ({attribut: valeur} de l'identite), `cr_traits_main` ([[card_id, [traits]]]) ; le reste va a etat_attendu."""
    cas = aides["cas"]
    attendu = cas.get("attendu") or {}
    soucis = []
    joueur = monde.players[0]
    identite = aides["identite"](monde)
    ids = lambda faces: [getattr(f.paper, "card_id", None) for f in faces]
    if "cr_glissees" in attendu or "cr_nb_glissees" in attendu:
        glissees = ids(identite.GetPlacedCardArea().Get(True))
        glissees = [g for g in glissees if g is not None]
        if "cr_glissees" in attendu and sorted(glissees) != sorted(attendu["cr_glissees"]):
            soucis.append(f"cartes sous Corsair = {sorted(glissees)} (attendu {sorted(attendu['cr_glissees'])})")
        if "cr_nb_glissees" in attendu and len(glissees) != attendu["cr_nb_glissees"]:
            soucis.append(f"{len(glissees)} carte(s) sous Corsair (attendu {attendu['cr_nb_glissees']}) : {sorted(glissees)}")
    main = ids(joueur.hand_cards.Get())
    for c in attendu.get("cr_main") or []:
        if c not in main:
            soucis.append(f"{c} absente de la main {sorted(main)}")
    defausse = ids(joueur.discard_pile.Get())
    for c in attendu.get("cr_defausse") or []:
        if c not in defausse:
            soucis.append(f"{c} absente de la defausse {sorted(defausse)}")
    for c in attendu.get("cr_defausse_absente") or []:
        if c in defausse:
            soucis.append(f"{c} est dans la defausse (elle devait etre glissee)")
    retirees = ids(monde.area_removed.Get(True))
    for c in attendu.get("retirees") or []:
        if c not in retirees:
            soucis.append(f"{c} pas retiree du jeu (retirees = {retirees})")
    for c in attendu.get("retirees_absentes") or []:
        if c in retirees:
            soucis.append(f"{c} retiree du jeu (elle ne devait pas l'etre)")
    for hote_id, voulus in attendu.get("cr_sous") or []:
        hote = aides["par_id"](monde, hote_id)
        if hote is None:
            soucis.append(f"{hote_id} introuvable en jeu (cr_sous)")
            continue
        dessous = sorted(x for x in ids(hote.GetPlacedCardArea().Get(True)) if x is not None)
        if dessous != sorted(voulus):
            soucis.append(f"sous {hote_id} : {dessous} (attendu {sorted(voulus)})")
    for nom, valeur in (attendu.get("cr_stats") or {}).items():
        courant = getattr(identite, nom, None)
        if courant != valeur:
            soucis.append(f"{nom} = {courant} (attendu {valeur})")
    cartes_main = {getattr(f.paper, "card_id", None): f for f in joueur.hand_cards.Get()}
    for card_id, traits in attendu.get("cr_traits_main") or []:
        face = cartes_main.get(card_id)
        if face is None:
            soucis.append(f"{card_id} absente de la main (cr_traits_main)")
            continue
        for t in ("SKILL", "THWART", "ATTACK", "DEFENSE", "TACTIC"):
            if face.HasTrait(t) != (t in traits):
                soucis.append(f"{card_id} : trait {t} {'present' if face.HasTrait(t) else 'absent'} (attendu {traits})")
    propres = ("cr_glissees", "cr_nb_glissees", "cr_main", "cr_defausse", "cr_defausse_absente", "cr_sous", "retirees",
               "retirees_absentes", "cr_stats", "cr_traits_main")
    reste = {k: v for k, v in attendu.items() if k not in propres}
    copie = dict(aides); copie["cas"] = dict(cas); copie["cas"]["attendu"] = reste
    ok, message = etat_attendu(monde, copie)
    if not ok:
        soucis.append(message)
    if soucis:
        return False, " ; ".join(soucis)
    return True, message
'''
