# Cas test_capacites du pack NEW ULTIMATE WINTER SOLDIER (Dipsome, prefixe `uw`) :
# noms prefixes « [uw] » puis le card_id (substituer_pack.py filtre dessus).
#
# Rappels de montage :
#  - le deck new_ultimate_winter_soldier demarre en ALTER EGO (uw001b Logan), avec uw002 (Griffes) deja en jeu (Setup) ;
#    `Puzzle.ChangeToFace('uw001b', 'uw001a')` passe en HEROS sans declencher de capacite ;
#  - Rhino 01094 est le vilain (14 PV), 01097b son complot principal ; 01110 Hydra Bomber (2 PV, sans Guard) est le sbire
#    des cas ; (01101 Hydra Mercenary porte GUARD : il interdirait d'attaquer Rhino) ;
#  - X = « the numeral in the printed resource cost » de la carte tiree : fillers 01088 (aucun cout, X=0), 01024 (1),
#    01022 (2), 01025 (3), 01021 (4) ; la main est fixee par `main_exclusive` (la defausse au hasard n'a alors qu'UNE carte) ;
#  - ressources : 01089 Genius = BB, 01090 Strength = RR, 01088 Energy = YY ; uw002 Griffes = 1 wild pour un evenement ATTACK.
SC = "rhino"
HEROS = "Puzzle.ChangeToFace('uw001b', 'uw001a')"
CIVIL = "Puzzle.ChangeToFace('uw001a', 'uw001b')"
SANS_BOOST = ["Puzzle.EmptyEncounterDeck()",
              "Puzzle.CreateEncounterDeck('01098', '01098', '01098', '01098', '01098', '01098', '01098', '01098')"]
COMPLOT = "01097b"
VILAIN = "01094"
SBIRE = "01110"


def en_jeu(*ids):
    return [f"Puzzle.PutIntoPlay('{i}', under_control=True)" for i in ids]


def _c(nom, pourquoi, mise, declencher, attendu, **cle):
    mise = SANS_BOOST + list(mise)
    cas = {"nom": "[uw] " + nom, "pourquoi": pourquoi, "scenario": cle.pop("scenario", SC),
           "heros": cle.pop("heros", "new_ultimate_winter_soldier"), "mise_en_place": mise, "declencher": declencher,
           "verifier": cle.pop("verifier", "etat_attendu"), "attendu": attendu}
    cas.setdefault("regles", ["v16_all", "v18_all"])
    cas.update(cle)
    return cas


CAS = [
    # ============================================================ uw001a Winter Soldier (face heros) : Healing Factor
    _c("uw001a Healing Factor : debut de la phase du mechant -> soigne 2 (3 degats -> 1)",
       "« Response: After the villain phase begins, heal 2 damage » (35001a : la phase des JOUEURS ; ici la phase du MECHANT)",
       [HEROS, "Puzzle.Damage('uw001a', 3)"], ["Puzzle.BeginVillainPhase()"],
       {"degats_identite": 1}, main_exclusive=["01088"], accepter_choix=True),
    _c("uw001a Healing Factor : CONTRE-CAS en ALTER EGO, rien n'est soigne",
       "la capacite est imprimee sur la face HEROS seulement (Logan n'a que « Shuck! »)",
       ["Puzzle.Damage('uw001b', 3)"], ["Puzzle.BeginVillainPhase()"],
       {"degats_identite": 3}, main_exclusive=["01088"], accepter_choix=True),
    _c("uw001a Winter Soldier : valeurs imprimees PV 10, THW 2, ATK 2, DEF 2, main 5, EARTH-6160 OPPOSITION SOLDIER",
       "nombres texte <-> code (scan) : HAND SIZE 5 / HIT POINTS 10",
       [HEROS], [], {"pv_max": [["uw001a", 10]], "traits": ["EARTH-6160", "OPPOSITION", "SOLDIER"],
                     "uw_stats": {"attack": 2, "thwart": 2, "defense": 2, "hand_size": 5}}, main_exclusive=["01088"],
       verifier="uw_etat"),

    # ============================================================ uw001b Logan : Setup
    _c("uw001b Logan : Setup, Wolverine's Claws entre en jeu au depart (mise de cote), pas dans la main",
       "« Shuck! - Setup: Search your deck and discard pile for the Wolverine's Claws upgrade and put it into play »",
       [], [], {"en_jeu": ["uw002"], "forme": "AlterEgo"}),
    _c("uw001b Logan : valeurs imprimees PV 10, REC 6, main 6, EARTH-6160 MUTANT SOLDIER",
       "nombres texte <-> code (scan) : HAND SIZE 6 / HIT POINTS 10 / REC 6",
       [], [], {"pv_max": [["uw001b", 10]], "traits": ["EARTH-6160", "MUTANT", "SOLDIER"],
                "uw_stats": {"recover": 6, "hand_size": 6}}, verifier="uw_etat"),

    # ============================================================ uw002 Wolverine's Claws
    _c("uw002 Griffes : payent Berserker Fury (2 + X(2) + 1 defausse au hasard ce round = 5 degats a Rhino)",
       "« generate a [wild] resource for an ATTACK event. That event deals 1 additional damage for each card you discarded "
       "from your hand at random this round » : la defausse qui PAIE l'evenement compte",
       [HEROS], [], {"degats": [[VILAIN, 5]], "exhausted": ["uw002"]},
       main_exclusive=["uw006", "01022"], jouer=["uw006"], payer_avec=["uw002"], cibles=[VILAIN], accepter_choix=True),
    _c("uw002 Griffes : PLAFOND de 3 (4 defausses au hasard + celle du cout = 5 -> +3) : 2 + 2 + 3 = 7",
       "« (to a maximum of 3) »",
       [HEROS, "Puzzle.EmptyHand()", "Puzzle.Gain('01088', '01089', '01090', '01024')", "Puzzle.DiscardAtRandom(4)",
        "Puzzle.Gain('uw006', '01022')"], [],
       {"degats": [[VILAIN, 7]], "exhausted": ["uw002"]},
       jouer=["uw006"], payer_avec=["uw002"], cibles=[VILAIN], accepter_choix=True),
    _c("uw002 Griffes : 2 defausses au hasard deja faites ce round + celle du cout = 3 -> +3 : 2 + 2 + 3 = 7",
       "chaque carte defaussee AU HASARD ce round compte, aussi celles d'une autre carte",
       [HEROS, "Puzzle.EmptyHand()", "Puzzle.Gain('01088', '01089')", "Puzzle.DiscardAtRandom(2)",
        "Puzzle.Gain('uw006', '01022')"], [],
       {"degats": [[VILAIN, 7]], "exhausted": ["uw002"]},
       jouer=["uw006"], payer_avec=["uw002"], cibles=[VILAIN], accepter_choix=True),
    _c("uw002 Griffes : TEMOIN, des defausses CHOISIES (plus de main) ne comptent pas : 2 + 2 + 1 = 5",
       "« discarded from your hand AT RANDOM » : `Puzzle.EmptyHand()` est une defausse ordinaire",
       [HEROS, "Puzzle.EmptyHand()", "Puzzle.Gain('01088', '01089', '01090')", "Puzzle.EmptyHand()",
        "Puzzle.Gain('uw006', '01022')"], [],
       {"degats": [[VILAIN, 5]], "exhausted": ["uw002"]},
       jouer=["uw006"], payer_avec=["uw002"], cibles=[VILAIN], accepter_choix=True),
    _c("uw002 Griffes : le compteur repart a zero au round suivant",
       "« THIS round » : 2 defausses au hasard, fin de round, puis Berserker Fury payee par les Griffes : 2 + 2 + 1 = 5",
       [HEROS, "Puzzle.EmptyHand()", "Puzzle.Gain('01088', '01089')", "Puzzle.DiscardAtRandom(2)", "Puzzle.SendRoundEnd()", "Puzzle.ResetRoundStats()",
        "Puzzle.EmptyHand()", "Puzzle.Gain('uw006', '01022')"], [],
       {"degats": [[VILAIN, 5]]},
       jouer=["uw006"], payer_avec=["uw002"], cibles=[VILAIN], accepter_choix=True),
    _c("uw002 Griffes : TEMOIN, ne paient pas un evenement qui n'est pas ATTACK (Last Resort, cout 1) : reste en main",
       "« for an ATTACK event »",
       [HEROS], [], {}, main_exclusive=["uw007", "01022"], jouer=["uw007"], payer_avec=["uw002"], cibles=[COMPLOT],
       accepter_choix=True, verifier="hellcat_carte_restee_en_main", restee="uw007"),

    # ============================================================ uw003 Phoenix
    _c("uw003 Phoenix : tiree AU HASARD par le cout de Berserker Fury -> entre en jeu, pas defaussee (2 + 3 = 5, sans bonus des Griffes)",
       "« When Phoenix is discarded from your hand at random, put her into play under your control » ; son cout imprime (3) "
       "fait quand meme le X de la carte qui l'a tiree ; elle n'est pas DEFAUSSEE (remplacee), donc ne compte pas pour les Griffes",
       [HEROS], [], {"en_jeu": ["uw003"], "degats": [[VILAIN, 5]], "uw_pas_en_defausse": ["uw003"]},
       main_exclusive=["uw006", "uw003"], jouer=["uw006"], payer_avec=["uw002"], cibles=[VILAIN], accepter_choix=True,
       verifier="uw_etat"),
    _c("uw003 Phoenix : defaussee au hasard hors d'un cout (forme heros) -> entre en jeu",
       "meme interruption, sans carte qui la tire pour son cout",
       [HEROS, "Puzzle.EmptyHand()", "Puzzle.Gain('uw003')", "Puzzle.DiscardAtRandom(1)"], [],
       {"en_jeu": ["uw003"], "taille_main": 0, "uw_pas_en_defausse": ["uw003"]}, verifier="uw_etat"),
    _c("uw003 Phoenix : TEMOIN, defaussee CHOISIE (pas au hasard) -> reste dans la defausse",
       "« AT RANDOM » : une defausse ordinaire ne declenche rien",
       [HEROS, "Puzzle.EmptyHand()", "Puzzle.Gain('uw003')", "Puzzle.EmptyHand()"], [],
       {"defausse": ["uw003"], "hors_jeu": ["uw003"]}),
    _c("uw003 Phoenix : TEMOIN, en forme ALTER EGO (Hero Interrupt) -> reste dans la defausse",
       "« Hero Interrupt » : forme heros seulement",
       ["Puzzle.EmptyHand()", "Puzzle.Gain('uw003')", "Puzzle.DiscardAtRandom(1)"], [],
       {"defausse": ["uw003"], "hors_jeu": ["uw003"]}),
    _c("uw003 Phoenix : valeurs imprimees PV 3 (en jeu), cout 3, trait EARTH-6160",
       "nombres texte <-> code (scan) : cout 3, PV 3, THW 2*, ATK 1*",
       [HEROS] + en_jeu("uw003"), [], {"pv_max": [["uw003", 3]], "traits_de": [["uw003", "EARTH-6160"]]}, main_exclusive=["01088"]),

    # ============================================================ uw004 Deranged Burst
    _c("uw004 Deranged Burst : 6 + X(2) = 8 degats, payee par 01090 (RR)",
       "« discard 1 card at random -> deal 6 damage, X additional (cout imprime de la carte defaussee) »",
       [HEROS], [], {"degats": [[VILAIN, 8]], "defausse": ["01022"]},
       main_exclusive=["uw004", "01022", "01090"], jouer=["uw004"], payer_avec=["01090"], cibles=[VILAIN], accepter_choix=True),
    _c("uw004 Deranged Burst : X = cout 4 (Gamma Slam) -> 6 + 4 = 10",
       "X vient de la carte DEFAUSSEE",
       [HEROS], [], {"degats": [[VILAIN, 10]]},
       main_exclusive=["uw004", "01021", "01090"], jouer=["uw004"], payer_avec=["01090"], cibles=[VILAIN], accepter_choix=True),
    _c("uw004 Deranged Burst : X = 0 (carte sans cout imprime : Energy) -> 6",
       "« the numeral in the printed resource cost » : une ressource n'en a pas",
       [HEROS], [], {"degats": [[VILAIN, 6]]},
       main_exclusive=["uw004", "01088", "01090"], jouer=["uw004"], payer_avec=["01090"], cibles=[VILAIN], accepter_choix=True),
    _c("uw004 Deranged Burst : payee par les Griffes + Cybernetic Arm : PERFORANT, traverse Tough (6 + 0 + 1 + 1 = 8)",
       "« If you exhausted Wolverine's Claws to play this card, this attack gains piercing »",
       [HEROS, "Puzzle.Tough('01094')"] + en_jeu("54002"), [],
       {"degats": [[VILAIN, 8]], "statuts_absents": [[VILAIN, "Tough"]]},
       main_exclusive=["uw004", "01088"], jouer=["uw004"], payer_avec=["uw002", "54002"], cibles=[VILAIN], accepter_choix=True),
    _c("uw004 Deranged Burst : TEMOIN, payee SANS les Griffes : Tough absorbe, 0 degat (la carte Tough est defaussee)",
       "pas de piercing hors des Griffes",
       [HEROS, "Puzzle.Tough('01094')"], [],
       {"degats": [[VILAIN, 0]], "statuts_absents": [[VILAIN, "Tough"]]},
       main_exclusive=["uw004", "01088", "01090"], jouer=["uw004"], payer_avec=["01090"], cibles=[VILAIN], accepter_choix=True),

    # ============================================================ uw005 Wild Slash
    _c("uw005 Wild Slash : X = 2 -> deux attaques de 3 (6 a Rhino), 2 degats subis",
       "« up to X times: Take 1 damage -> deal 3 damage to an enemy »",
       [HEROS], [], {"degats": [[VILAIN, 6]], "degats_identite": 2, "defausse": ["01022"]},
       main_exclusive=["uw005", "01022"], jouer=["uw005"], cibles=[VILAIN, VILAIN], accepter_choix=True),
    _c("uw005 Wild Slash : X = 0 (Energy) -> aucune attaque",
       "« up to 0 times »",
       [HEROS], [], {"degats": [[VILAIN, 0]], "degats_identite": 0},
       main_exclusive=["uw005", "01088"], jouer=["uw005"], cibles=[VILAIN], accepter_choix=True),
    _c("uw005 Wild Slash : TEMOIN « up to » : le joueur s'arrete tout de suite (Cancel) -> 0 degat, aucun degat subi",
       "chaque attaque est facultative",
       [HEROS], [], {"degats": [[VILAIN, 0]], "degats_identite": 0},
       main_exclusive=["uw005", "01022"], jouer=["uw005"], cibles=[VILAIN], preferer_option="Cancel"),
    _c("uw005 Wild Slash : X = 4 -> 4 attaques possibles, 12 degats a Rhino, 4 degats subis",
       "« up to X times » avec X = 4 (Gamma Slam) : le joueur peut faire les 4 attaques",
       [HEROS], [], {"degats": [[VILAIN, 12]], "degats_identite": 4},
       main_exclusive=["uw005", "01021"], jouer=["uw005"], cibles=[VILAIN, VILAIN, VILAIN, VILAIN], accepter_choix=True),

    # ============================================================ uw006 Berserker Fury
    _c("uw006 Berserker Fury : sans Griffes, payee par 01090 (RR) : 2 + X(2) = 4",
       "« deal 2 damage ... X additional »",
       [HEROS], [], {"degats": [[VILAIN, 4]]},
       main_exclusive=["uw006", "01022", "01090"], jouer=["uw006"], payer_avec=["01090"], cibles=[VILAIN], accepter_choix=True),
    _c("uw006 Berserker Fury : l'attaque VAINC le sbire, main VIDE apres le paiement -> repetition IMPOSSIBLE (le cout ne peut pas etre repaye)",
       "FAQ RR v1.8 (Across the Spider-Verse) : repeter la capacite = tout rejouer, cout compris ; sans carte a defausser au hasard, rien n'est propose "
       "(arbitrage du 26/10/2026 ; avant, la repetition etait offerte et coutait 2 degats)",
       [HEROS, f"Puzzle.PutIntoPlay('{SBIRE}')"], [],
       {"hors_jeu": [SBIRE], "degats": [[VILAIN, 0]], "degats_identite": 0},
       main_exclusive=["uw006", "01022", "01090"], jouer=["uw006"], payer_avec=["01090"], cibles=[SBIRE, VILAIN],
       accepter_choix=True),
    _c("uw006 Berserker Fury : l'attaque VAINC le sbire, une 2e carte en main -> on paie 2 degats, on defausse UNE NOUVELLE carte au hasard (nouveau X) et on repete",
       "FAQ RR v1.8 : repeter inclut le cout. Mains 01022 (X = 2) et 01021 (X = 4) : la repetition defausse la carte RESTANTE, donc son X, pas celui de la 1re",
       [HEROS, f"Puzzle.PutIntoPlay('{SBIRE}')"], [],
       {"hors_jeu": [SBIRE], "degats": [[VILAIN, 6]], "degats_identite": 2, "defausse": ["01022", "01021"]},
       main_exclusive=["uw006", "01022", "01021", "01090"], jouer=["uw006"], payer_avec=["01090"], cibles=[SBIRE, VILAIN],
       accepter_choix=True),
    _c("uw006 Berserker Fury : TEMOIN, sans victoire pas de repetition (4 degats, aucun degat subi)",
       "la repetition exige qu'un ennemi soit vaincu",
       [HEROS], [], {"degats": [[VILAIN, 4]], "degats_identite": 0},
       main_exclusive=["uw006", "01022", "01090"], jouer=["uw006"], payer_avec=["01090"], cibles=[VILAIN], accepter_choix=True),
    _c("uw006 Berserker Fury : TEMOIN, victoire mais repetition declinee (Cancel) : Rhino intact, aucun degat subi",
       "« you MAY »",
       [HEROS, f"Puzzle.PutIntoPlay('{SBIRE}')"], [],
       {"hors_jeu": [SBIRE], "degats": [[VILAIN, 0]], "degats_identite": 0},
       main_exclusive=["uw006", "01022", "01090"], jouer=["uw006"], payer_avec=["01090"], cibles=[SBIRE, VILAIN],
       preferer_option="Cancel"),

    # ============================================================ uw007 Last Resort
    _c("uw007 Last Resort : 1 + X(2) = 3 menaces retirees d'un complot (6 -> 3), pas de pioche",
       "« remove 1 threat ... remove X additional threat from that scheme »",
       [HEROS, f"Puzzle.SetThreat('{COMPLOT}', 6)"], [], {"menace": [[COMPLOT, 3]]},
       main_exclusive=["uw007", "01022", "01089"], jouer=["uw007"], payer_avec=["01089"], cibles=[COMPLOT], accepter_choix=True),
    _c("uw007 Last Resort : retire la DERNIERE menace du complot -> pioche 2 cartes",
       "« If this removes the last threat from that scheme, draw 2 cards »",
       [HEROS, f"Puzzle.SetThreat('{COMPLOT}', 3)"], [], {"menace": [[COMPLOT, 0]], "taille_main": 2},
       main_exclusive=["uw007", "01022", "01089"], jouer=["uw007"], payer_avec=["01089"], cibles=[COMPLOT], accepter_choix=True),
    _c("uw007 Last Resort : TEMOIN, il reste de la menace -> pas de pioche (menace 5 -> 2, main vide)",
       "pas de pioche tant que le complot n'est pas vide",
       [HEROS, f"Puzzle.SetThreat('{COMPLOT}', 5)"], [], {"menace": [[COMPLOT, 2]], "taille_main": 0},
       main_exclusive=["uw007", "01022", "01089"], jouer=["uw007"], payer_avec=["01089"], cibles=[COMPLOT], accepter_choix=True),

    # ============================================================ uw008 Desperate Regenerate
    _c("uw008 Desperate Regenerate : pioche 2, defausse 1 au hasard, soigne 3 (5 degats -> 2) ; main : 1 + 2 - 1 = 2",
       "« Draw 2 cards. Discard 1 card at random. Choose: Heal 3 damage from your identity »",
       [HEROS, "Puzzle.Damage('uw001a', 5)"], [], {"degats_identite": 2, "taille_main": 2},
       main_exclusive=["uw008", "01022", "01088"], jouer=["uw008"], payer_avec=["01088"], accepter_choix=True),
    _c("uw008 Desperate Regenerate : identite etourdie sans degat -> seule l'option « Discard each stunned ... » reste",
       "second choix : « Discard each stunned and confused status card from your identity »",
       [HEROS, "Puzzle.Stun('uw001a')"], [], {"statuts_absents": [["uw001a", "Stunned"]], "taille_main": 2},
       main_exclusive=["uw008", "01022", "01088"], jouer=["uw008"], payer_avec=["01088"], accepter_choix=True),
    _c("uw008 Desperate Regenerate : sans degat ni statut elle pioche et defausse quand meme (main 2)",
       "pas de condition d'identite, contrairement a 35012",
       [HEROS], [], {"taille_main": 2},
       main_exclusive=["uw008", "01022", "01088"], jouer=["uw008"], payer_avec=["01088"], accepter_choix=True),

    # ============================================================ uw009 Winter Mask
    _c("uw009 Winter Mask : apres une defausse AU HASARD, 1 degat -> pioche 1 (main 1, 1 degat)",
       "« After you discard a card from your hand at random, take 1 damage -> draw 1 card »",
       [HEROS, "Puzzle.EmptyHand()", "Puzzle.Gain('01022')"] + en_jeu("uw009") + ["Puzzle.DiscardAtRandom(1)"], [],
       {"degats_identite": 1, "taille_main": 1}, accepter_choix=True),
    _c("uw009 Winter Mask : TEMOIN, une defausse CHOISIE ne la declenche pas (aucun degat)",
       "« AT RANDOM »",
       [HEROS, "Puzzle.EmptyHand()", "Puzzle.Gain('01022')"] + en_jeu("uw009") + ["Puzzle.EmptyHand()"], [],
       {"degats_identite": 0, "taille_main": 0}, accepter_choix=True),
    _c("uw009 Winter Mask : TEMOIN, en ALTER EGO (Hero Response) : aucun degat, aucune pioche",
       "« Hero Response »",
       ["Puzzle.EmptyHand()", "Puzzle.Gain('01022')"] + en_jeu("uw009") + ["Puzzle.DiscardAtRandom(1)"], [],
       {"degats_identite": 0, "taille_main": 0}, accepter_choix=True),

    # ============================================================ uw010 Adamantium Skeleton
    _c("uw010 Adamantium Skeleton : +4 PV et +1 ATQ en forme heros (PV 14, ATQ 3)",
       "« You get +4 hit points. Winter Soldier gets +1 ATK »",
       [HEROS] + en_jeu("uw010"), [], {"attributs": {"health": 4, "attack": 1}}, main_exclusive=["01088"]),
    _c("uw010 Adamantium Skeleton : CONTRE-CAS ALTER EGO : +4 PV, la capacite « Winter Soldier gets +1 ATK » ne vaut pas pour Logan",
       "« You » = identite (les deux faces) ; « Winter Soldier » = la face heros seulement",
       en_jeu("uw010"), [], {"attributs": {"health": 4}}, main_exclusive=["01088"]),
    _c("uw010 Adamantium Skeleton : l'attaque de base est PERFORANTE (Tough traverse : 2 + 1 = 3 degats)",
       "« his basic attacks gain piercing »",
       [HEROS, "Puzzle.Tough('01094')"] + en_jeu("uw010"), ["Puzzle.Attack('uw001a')"],
       {"degats": [[VILAIN, 3]], "statuts_absents": [[VILAIN, "Tough"]]}, main_exclusive=["01088"], cibles=[VILAIN]),
    _c("uw010 Adamantium Skeleton : TEMOIN, sans la carte l'attaque de base est absorbee par Tough (0 degat)",
       "pas de piercing d'origine",
       [HEROS, "Puzzle.Tough('01094')"], ["Puzzle.Attack('uw001a')"],
       {"degats": [[VILAIN, 0]], "statuts_absents": [[VILAIN, "Tough"]]}, main_exclusive=["01088"], cibles=[VILAIN]),

    # ============================================================ uw011 Mission Objective
    _c("uw011 Mission Objective : jouee (forme heros) sur un sbire -> attachee a lui",
       "« Hero form only. Attach to a minion »",
       [HEROS, f"Puzzle.PutIntoPlay('{SBIRE}')"], [], {"accroche_a": [["uw011", SBIRE]]},
       main_exclusive=["uw011", "01089"], jouer=["uw011"], payer_avec=["01089"], cibles=[SBIRE], accepter_choix=True),
    _c("uw011 Mission Objective : TEMOIN, en ALTER EGO elle n'est pas jouable (reste en main)",
       "« Hero form only »",
       [f"Puzzle.PutIntoPlay('{SBIRE}')"], [], {},
       main_exclusive=["uw011", "01089"], jouer=["uw011"], payer_avec=["01089"], cibles=[SBIRE], accepter_choix=True,
       verifier="hellcat_carte_restee_en_main", restee="uw011"),
    _c("uw011 Mission Objective : le sbire est vaincu PAR le heros -> 3 menaces retirees (5 -> 2)",
       "« After the attached minion is defeated by Winter Soldier, remove 3 threat from a scheme »",
       [HEROS, f"Puzzle.SetThreat('{COMPLOT}', 5)", f"Puzzle.PutIntoPlay('{SBIRE}')", "Puzzle.PutIntoPlay('uw011', under_control=True)",
        f"Puzzle.Attach('uw011', '{SBIRE}')"], ["Puzzle.Attack('uw001a')"],
       {"hors_jeu": [SBIRE], "menace": [[COMPLOT, 2]]}, main_exclusive=["01088"], cibles=[SBIRE, COMPLOT], accepter_choix=True),
    _c("uw011 Mission Objective : un AUTRE sbire en jeu -> 1 degat pour y rattacher la carte (accroche_a, 1 degat subi)",
       "« Winter Soldier may take 1 damage to attach this card to another minion »",
       [HEROS, f"Puzzle.SetThreat('{COMPLOT}', 5)", f"Puzzle.PutIntoPlay('{SBIRE}')", "Puzzle.PutIntoPlay('01103')",
        "Puzzle.PutIntoPlay('uw011', under_control=True)", f"Puzzle.Attach('uw011', '{SBIRE}')"], ["Puzzle.Attack('uw001a')"],
       {"hors_jeu": [SBIRE], "menace": [[COMPLOT, 2]], "accroche_a": [["uw011", "01103"]], "degats_identite": 1},
       main_exclusive=["01088"], cibles=[SBIRE, COMPLOT, "01103"], accepter_choix=True),
    _c("uw011 Mission Objective : TEMOIN, le sbire meurt d'autre chose que du heros (Puzzle.Damage) -> aucune menace retiree",
       "« defeated BY Winter Soldier »",
       [HEROS, f"Puzzle.SetThreat('{COMPLOT}', 5)", f"Puzzle.PutIntoPlay('{SBIRE}')", "Puzzle.PutIntoPlay('uw011', under_control=True)",
        f"Puzzle.Attach('uw011', '{SBIRE}')", f"Puzzle.Damage('{SBIRE}', 2)"], [],
       {"hors_jeu": [SBIRE], "menace": [[COMPLOT, 5]]}, main_exclusive=["01088"], cibles=[COMPLOT], accepter_choix=True),

    # ============================================================ uw012 "This is Your Enemy"
    _c("uw012 This is Your Enemy : jouee sur un sbire (forme heros) -> attachee",
       "« Hero form only. Attach to a minion »",
       [HEROS, f"Puzzle.PutIntoPlay('{SBIRE}')"], [], {"accroche_a": [["uw012", SBIRE]]},
       main_exclusive=["uw012", "01089"], jouer=["uw012"], payer_avec=["01089"], cibles=[SBIRE], accepter_choix=True),
    _c("uw012 This is Your Enemy : le sbire est vaincu PAR le heros -> pioche 3, defausse 1 au hasard (main 1 -> 3)",
       "« Winter Soldier draws 3 cards and discards 1 card from his hand at random »",
       [HEROS, f"Puzzle.PutIntoPlay('{SBIRE}')", "Puzzle.PutIntoPlay('uw012', under_control=True)",
        f"Puzzle.Attach('uw012', '{SBIRE}')"], ["Puzzle.Attack('uw001a')"],
       {"hors_jeu": [SBIRE], "taille_main": 3}, main_exclusive=["01022"], cibles=[SBIRE], accepter_choix=True),
    _c("uw012 This is Your Enemy : TEMOIN, sbire vaincu par autre chose que le heros -> rien (main 1)",
       "« defeated BY Winter Soldier »",
       [HEROS, f"Puzzle.PutIntoPlay('{SBIRE}')", "Puzzle.PutIntoPlay('uw012', under_control=True)",
        f"Puzzle.Attach('uw012', '{SBIRE}')", f"Puzzle.Damage('{SBIRE}', 2)"], [],
       {"hors_jeu": [SBIRE], "taille_main": 1}, main_exclusive=["01022"], accepter_choix=True),

    # ============================================================ uw013 Live with the Burden
    _c("uw013 Live with the Burden : carte tiree cout 3 -> 3 degats, on incline l'identite pour en empecher 2 (1 degat)",
       "« Take X damage ... You may exhaust your identity to prevent 2 of that damage »",
       [], ["Puzzle.Reveal('uw013')"], {"degats_identite": 1, "exhausted": ["uw001b"], "hors_jeu": ["uw013"]},
       main_exclusive=["01025"], accepter_choix=True),
    _c("uw013 Live with the Burden : TEMOIN, facultatif decline (Cancel) : 3 degats, identite prete",
       "« You MAY exhaust your identity »",
       [], ["Puzzle.Reveal('uw013')"], {"degats_identite": 3, "hors_jeu": ["uw013"]}, main_exclusive=["01025"],
       preferer_option="Cancel"),
    _c("uw013 Live with the Burden : X = 0 (Energy) -> aucun degat",
       "« the numeral in the printed resource cost » : aucun",
       [], ["Puzzle.Reveal('uw013')"], {"degats_identite": 0, "hors_jeu": ["uw013"]}, main_exclusive=["01088"], accepter_choix=True),
]


# ================================================================== le set nemesis (uw014-uw018)
CAS += [
    _c("uw015 Alonya Prostovich : s'active en ALTER EGO (manigance) -> 2 menaces sur CHAQUE complot a la place (principal + annexe)",
       "« When Alonya Prostovich activates, place 2 threat on each scheme instead »",
       ["Puzzle.PutIntoPlay('01109')", "Puzzle.PutIntoPlay('uw015')"], ["Puzzle.Activate('uw015')"],
       {"menace": [[COMPLOT, 2], ["01109", 4]], "degats_identite": 0}, main_exclusive=["01088"]),
    _c("uw015 Alonya Prostovich : s'active en forme HEROS (attaque) -> aucune attaque, 2 menaces sur chaque complot",
       "« instead » : elle ne fait ni l'un ni l'autre",
       [HEROS, "Puzzle.PutIntoPlay('01109')", "Puzzle.PutIntoPlay('uw015')"], ["Puzzle.Activate('uw015')"],
       {"menace": [[COMPLOT, 2], ["01109", 4]], "degats_identite": 0}, main_exclusive=["01088"]),
    _c("uw015 Alonya Prostovich : « [star] Boost: Reveal this card » -> donnee en boost au mechant, elle est REVELEE (en jeu)",
       "boost : `WhenCardBecomeBoost(\"This\", RevealThisCard)`",
       [HEROS, "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01098', 'uw015')"],
       [f"Puzzle.EnemyAttacks('{VILAIN}', 'uw001a')"], {"en_jeu": ["uw015"]}, main_exclusive=["01088"],
       passer_sur_option="Defense"),
    _c("uw015 Alonya Prostovich : valeurs imprimees PV 3 ; trait EARTH-6160 DIRECTORATE X",
       "nombres texte <-> code (scan) : HP 3, ATK ★, SCH ★ (0 dans desc, valeur donnee par le texte)",
       ["Puzzle.PutIntoPlay('uw015')"], [],
       {"pv_max": [["uw015", 3]], "traits_de": [["uw015", "EARTH-6160"], ["uw015", "DIRECTORATE X"]]}, main_exclusive=["01088"]),
    _c("uw014 Directorate X : fin de la phase du mechant, Alonya ABSENTE -> le premier joueur la trouve et la revele",
       "« If it is not in play, the first player finds it and reveals it » (lecture retenue : « it » = Alonya)",
       ["Puzzle.PutIntoPlay('uw014')", "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01098', '01098', 'uw015', '01098')"],
       ["Puzzle.EndVillainPhase()"], {"en_jeu": ["uw014", "uw015"]}, main_exclusive=["01088"]),
    _c("uw014 Directorate X : Alonya EN JEU -> defausse du deck rencontre jusqu'a un sbire, qu'on revele",
       "« the engaged player discards cards from the encounter deck until a minion is discarded and reveal it »",
       ["Puzzle.PutIntoPlay('uw014')", "Puzzle.PutIntoPlay('uw015')", "Puzzle.EmptyEncounterDeck()",
        "Puzzle.CreateEncounterDeck('01098', '01103', '01098', '01098')"],
       ["Puzzle.EndVillainPhase()"], {"en_jeu": ["uw014", "uw015", "01103"], "defausse_rencontre": ["01098"]},
       main_exclusive=["01088"]),
    _c("uw014 Directorate X : valeurs imprimees (menace de depart 2 par joueur : 2 en solo)",
       "nombres texte <-> code (scan) : « 2 [per_hero] »",
       ["Puzzle.Reveal('uw014')"], [], {"menace": [["uw014", 2]]}, main_exclusive=["01088"]),
    _c("uw016 Phoenix Specimen Brainwashing : fin de la phase du mechant -> defausse au hasard (cout 3) et 3 menaces sur un complot",
       "« discard 1 card from your hand at random, place X threat on a scheme, where X = printed cost »",
       ["Puzzle.Reveal('uw016')"], ["Puzzle.EndVillainPhase()"], {"menace": [[COMPLOT, 3]], "defausse": ["01025"]},
       main_exclusive=["01025"], cibles=[COMPLOT], accepter_choix=True),
    _c("uw016 Phoenix Specimen Brainwashing : main sans cout imprime (Energy) -> X = 0, aucune menace",
       "X = 0",
       ["Puzzle.Reveal('uw016')"], ["Puzzle.EndVillainPhase()"], {"menace": [[COMPLOT, 0]], "defausse": ["01088"]},
       main_exclusive=["01088"], cibles=[COMPLOT], accepter_choix=True),
    _c("uw016 Phoenix Specimen Brainwashing : « Hero Action: Spend a [mental] resource -> discard this card »",
       "la carte se defausse en payant une ressource mentale (Genius BB)",
       [HEROS, "Puzzle.Reveal('uw016')"], ["Puzzle.Action('uw016', 'HeroAction')"], {"hors_jeu": ["uw016"]},
       main_exclusive=["01089"], payer_avec=["01089"], accepter_choix=True),
    _c("uw017 X-S Sentinel I : son attaque est PERFORANTE, elle traverse Tough (3 degats, Tough defaussee)",
       "« [star] X-S Sentinel I's attack gains ranged, overkill and piercing »",
       [HEROS, "Puzzle.Tough('uw001a')", "Puzzle.PutIntoPlay('uw017')"], ["Puzzle.EnemyAttacks('uw017', 'uw001a')"],
       {"degats_identite_min": 3, "statuts_absents": [["uw001a", "Tough"]]}, main_exclusive=["01088"], passer_sur_option="Defense"),
    _c("uw017 X-S Sentinel I : TEMOIN, un sbire ordinaire (Shocker) est arrete par Tough (aucun degat)",
       "pas de piercing d'origine",
       [HEROS, "Puzzle.Tough('uw001a')", "Puzzle.PutIntoPlay('01103')"], ["Puzzle.EnemyAttacks('01103', 'uw001a')"],
       {"degats_identite": 0, "statuts_absents": [["uw001a", "Tough"]]}, main_exclusive=["01088"], passer_sur_option="Defense"),
    _c("uw017 X-S Sentinel I : « [star] Boost: This attack gains ranged, overkill and piercing » : donnee en boost a Rhino, l'attaque traverse Tough",
       "boost : `would_atk_message.GainRanged/GainOverKill/GainPiercing`",
       [HEROS, "Puzzle.Tough('uw001a')", "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('uw017')"],
       [f"Puzzle.EnemyAttacks('{VILAIN}', 'uw001a')"], {"degats_identite_min": 3, "statuts_absents": [["uw001a", "Tough"]]},
       main_exclusive=["01088"], passer_sur_option="Defense"),
    _c("uw017 X-S Sentinel I : valeurs imprimees PV 8 ; trait EARTH-6160 SENTINEL",
       "nombres texte <-> code (scan) : HP 8, ATK 3, SCH 1",
       ["Puzzle.PutIntoPlay('uw017')"], [], {"pv_max": [["uw017", 8]], "traits_de": [["uw017", "EARTH-6160"], ["uw017", "SENTINEL"]]},
       main_exclusive=["01088"]),
    _c("uw018 X-S Sentinel II : QUICKSTRIKE, il attaque des qu'il s'engage (forme heros, 1 degat)",
       "« Quickstrike. Villainous. » natifs ; ATK 1",
       [HEROS], ["Puzzle.PutIntoPlay('uw018')"], {"degats_identite": 1}, main_exclusive=["01088"], passer_sur_option="Defense"),
    _c("uw018 X-S Sentinel II : apres son activation il se soigne de 3 (4 degats -> 1)",
       "« [star] Forced Response: After X-S Sentinel II activates, heal 3 damage from X-S Sentinel II »",
       [HEROS, "Puzzle.PutIntoPlay('uw018')", "Puzzle.Damage('uw018', 4)"], ["Puzzle.EnemyAttacks('uw018', 'uw001a')"],
       {"degats": [["uw018", 1]]}, main_exclusive=["01088"], passer_sur_option="Defense"),
    _c("uw018 X-S Sentinel II : valeurs imprimees PV 7 ; trait EARTH-6160 SENTINEL",
       "nombres texte <-> code (scan) : HP 7, ATK 1, SCH 1",
       [HEROS, "Puzzle.PutIntoPlay('uw018')"], [], {"pv_max": [["uw018", 7]], "traits_de": [["uw018", "EARTH-6160"], ["uw018", "SENTINEL"]]},
       main_exclusive=["01088"]),
]

# ================================================================== interactions du moteur de defausse au hasard
CAS += [
    _c("uw009 + uw006 : la defausse qui PAIE Berserker Fury declenche Winter Mask (1 degat, 1 carte piochee) ; 2 + X(2) = 4",
       "le cout « discard 1 card at random » est une defausse au hasard comme une autre : la Response de Winter Mask est offerte",
       [HEROS] + en_jeu("uw009"), [], {"degats": [[VILAIN, 4]], "degats_identite": 1, "taille_main": 1},
       main_exclusive=["uw006", "01022", "01090"], jouer=["uw006"], payer_avec=["01090"], cibles=[VILAIN], accepter_choix=True),
    _c("uw004 Deranged Burst : TEMOIN, payee avec la SEULE autre carte de la main (01090) -> plus rien a defausser",
       "cas limite : la condition `UneCarteADefausser` voit 01090 au moment de jouer, le paiement la depense AVANT la defausse au hasard",
       [HEROS], [], {},
       main_exclusive=["uw004", "01090"], jouer=["uw004"], payer_avec=["01090"], cibles=[VILAIN], accepter_choix=True,
       verifier="hellcat_carte_restee_en_main", restee="uw004"),
    _c("uw009 + uw003 : Phoenix tiree au hasard entre en jeu, elle n'est PAS defaussee : Winter Mask ne se declenche pas",
       "« After you DISCARD a card from your hand at random » : une carte remplacee par l'interruption n'est pas defaussee",
       [HEROS, "Puzzle.EmptyHand()", "Puzzle.Gain('uw003')"] + en_jeu("uw009") + ["Puzzle.DiscardAtRandom(1)"], [],
       {"en_jeu": ["uw003"], "degats_identite": 0, "taille_main": 0}, accepter_choix=True),
]


VERIFICATIONS = r'''

def uw_etat(monde, aides):
    """Cles propres : `uw_stats` ({attribut: valeur} lus sur l'identite), `uw_pas_en_defausse` ([card_id] absents de la
    defausse du joueur) ; le reste va a etat_attendu."""
    cas = aides["cas"]
    attendu = cas.get("attendu") or {}
    soucis = []
    identite = aides["identite"](monde)
    for nom, valeur in (attendu.get("uw_stats") or {}).items():
        courant = getattr(identite, nom, None)
        if courant != valeur:
            soucis.append(f"{nom} = {courant} (attendu {valeur})")
    defausse = [getattr(f.paper, "card_id", None) for f in monde.players[0].discard_pile.Get()]
    for card_id in attendu.get("uw_pas_en_defausse") or []:
        if card_id in defausse:
            soucis.append(f"{card_id} est dans la defausse ({defausse})")
    reste = {k: v for k, v in attendu.items() if k not in ("uw_stats", "uw_pas_en_defausse")}
    copie = dict(aides); copie["cas"] = dict(cas); copie["cas"]["attendu"] = reste
    ok, message = etat_attendu(monde, copie)
    if not ok:
        soucis.append(message)
    if soucis:
        return False, " ; ".join(soucis)
    return True, message
'''
