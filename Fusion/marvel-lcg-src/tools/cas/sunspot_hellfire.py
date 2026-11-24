# Cas test_capacites du pack SUNSPOT (Dipsome, campagne Hellfire Hunt, prefixe `so`) : noms prefixes « [so] » puis le card_id
# (substituer_pack.py filtre dessus).
#
# Rappels de montage :
#  - le deck `sunspot_hellfire` demarre en ALTER EGO (so001b Roberto) avec 5 compteurs `solar` poses a la mise en place (Setup) ;
#    `Puzzle.ChangeToFace('so001b', 'so001a')` passe en HEROS SANS declencher de capacite et GARDE le stock (meme identite) ;
#  - Rhino 01094 est le vilain (ATK 2, 14 PV), 01097b son complot principal (menace 0 au depart), 01103 Shocker un sbire (3 PV, ATK 2),
#    01110 Hydra Bomber un sbire de 2 PV sans Guard ;
#  - ressources : 01088 Energy = YY, 01089 Genius = BB, 01090 Strength = RR, 01085 Emergency = 1 ressource [energy] ;
#  - `accepter_choix=True` repond « oui » a l'interruption ET prend le PREMIER item d'une saisie de nombre (le maximum : X = le stock) ;
#  - les cas qui mesurent une defense comptent les degats de l'identite (Rhino : ATK 2).
SC = "rhino"
HEROS = "Puzzle.ChangeToFace('so001b', 'so001a')"
CIVIL = "Puzzle.ChangeToFace('so001a', 'so001b')"
VILAIN = "01094"
COMPLOT = "01097b"
SBIRE = "01103"
SBIRE_2PV = "01110"
SANS_BOOST = ["Puzzle.EmptyEncounterDeck()",
              "Puzzle.CreateEncounterDeck('01098', '01098', '01098', '01098', '01098', '01098', '01098', '01098')"]


def en_jeu(*ids):
    return [f"Puzzle.PutIntoPlay('{i}', under_control=True)" for i in ids]


def solaires(n):
    """Ramene le stock de l'identite a EXACTEMENT n (il part de 5 apres le Setup)."""
    ecart = n - 5
    return [f"Puzzle.PlaceCounters('so001a', 'solar', {ecart})"] if ecart else []


def _c(nom, pourquoi, mise, declencher, attendu, **cle):
    # La main de DEPART contient des cartes du pack : on la vide AVANT la mise en place des cartes du cas (sauf `garder_main`).
    debut = [] if cle.pop("garder_main", False) else ["Puzzle.EmptyHand()"]
    mise = debut + list(cle.pop("sans", SANS_BOOST)) + list(mise)
    cas = {"nom": "[so] " + nom, "pourquoi": pourquoi, "scenario": cle.pop("scenario", SC),
           "heros": cle.pop("heros", "sunspot_hellfire"), "mise_en_place": mise, "declencher": declencher,
           "verifier": cle.pop("verifier", "so_etat"), "attendu": attendu}
    cas.setdefault("regles", ["v16_all", "v18_all"])
    cas.update(cle)
    return cas


CAS = [
    # ============================================================ so001b Roberto Da Costa : Setup, Energy Absorption
    _c("so001b Roberto : Setup, 5 compteurs solaires sur l'identite",
       "« Setup: Place 5 solar counters here. » : le stock de tout le pack",
       [], ["Puzzle.Draw(0)"], {"compteurs": [["so001b", "solar", 5]]}),
    _c("so001b Roberto : valeurs imprimees PV 10, REC 3, main 6, MUTANT",
       "nombres texte <-> code (scan) : HAND SIZE 6 / HIT POINTS 10 / REC 3",
       [], [], {"pv_max": [["so001b", 10]], "traits": ["MUTANT"], "so_stats": {"recover": 3, "hand_size": 6}}),
    _c("so001b Energy Absorption : Energy (YY) + Genius (BB) defaussees = 4 icones, 5 + 4 = 9 compteurs",
       "« Discard up to 3 cards from your hand. For each resource icon discarded, place 1 solar counter here. »",
       [], ["Puzzle.Action('so001b', 'Action')"], {"compteurs": [["so001b", "solar", 9]]},
       main_exclusive=["01088", "01089"], cibles=["01088", "01089"], accepter_choix=True),
    _c("so001b Energy Absorption : UNE carte (Energy, YY) -> 5 + 2 = 7 compteurs",
       "« up to 3 » : on peut defausser moins ; chaque ICONE compte (YY = 2)",
       [], ["Puzzle.Action('so001b', 'Action')"], {"compteurs": [["so001b", "solar", 7]]},
       main_exclusive=["01088", "01089"], cibles=["01088"], accepter_choix=True),
    _c("so001b Energy Absorption : trois cartes (YY + BB + RR) = 6 icones, 5 + 6 = 11 compteurs",
       "plafond de 3 cartes ; aucun plafond sur le stock",
       [], ["Puzzle.Action('so001b', 'Action')"], {"compteurs": [["so001b", "solar", 11]]},
       main_exclusive=["01088", "01089", "01090"], cibles=["01088", "01089", "01090"], accepter_choix=True),

    # ============================================================ so001a Sunspot : valeurs, Solar Rechanneling, reflux
    _c("so001a Sunspot : valeurs imprimees PV 10, THW 0, ATK 0, DEF 0, main 5, X-FORCE",
       "nombres texte <-> code (scan) : HAND SIZE 5 / HIT POINTS 10 / 0-0-0",
       [HEROS], [], {"pv_max": [["so001a", 10]], "traits": ["X-FORCE"],
                     "so_stats": {"attack": 0, "thwart": 0, "defense": 0, "hand_size": 5}}),
    _c("so001a Solar Rechanneling ATK : X = 5 compteurs -> attaque de base 0 + 5 = 5 degats a Rhino",
       "« remove X solar counters -> Sunspot gets +X to that chosen power for this use »",
       [HEROS], ["Puzzle.Attack('so001a')"], {"degats": [[VILAIN, 5]], "compteurs": [["so001a", "solar", 0]]},
       accepter_choix=True),
    _c("so001a Solar Rechanneling ATK : TEMOIN, stock vide, l'attaque de base vaut 0",
       "sans compteur, l'interruption n'a rien a depenser",
       [HEROS] + solaires(0), ["Puzzle.Attack('so001a')"], {"degats": [[VILAIN, 0]], "compteurs": [["so001a", "solar", 0]]},
       accepter_choix=True),
    _c("so001a Solar Rechanneling THW : X = 5 -> 5 menaces retirees (menace 6 -> 1)",
       "le bonus vaut pour le pouvoir CHOISI : ici contrer",
       [HEROS, f"Puzzle.SetThreat('{COMPLOT}', 6)"], ["Puzzle.Thwart('so001a')"],
       {"menace": [[COMPLOT, 1]], "compteurs": [["so001a", "solar", 0]]}, accepter_choix=True),
    _c("so001a Solar Rechanneling DEF : X = 5 -> DEF 5, Rhino (ATK 2) ne fait aucun degat",
       "le bonus vaut aussi pour se DEFENDRE",
       [HEROS], ["Puzzle.Defend('so001a', '01094')"], {"degats_identite": 0, "compteurs": [["so001a", "solar", 0]]},
       accepter_choix=True),
    _c("so001a Solar Rechanneling DEF : TEMOIN, stock vide, DEF 0, Rhino fait 2 degats",
       "sans compteur, rien n'absorbe l'attaque",
       [HEROS] + solaires(0), ["Puzzle.Defend('so001a', '01094')"], {"degats_identite": 2}, accepter_choix=True),
    _c("so001a Solar Rechanneling : au moins la moitie retiree (5 sur 5) -> Sunspot est REDRESSE",
       "« If you removed at least half of the counters, ready Sunspot. »",
       [HEROS], ["Puzzle.Attack('so001a')"], {"pret": ["so001a"]}, accepter_choix=True),
    _c("so001a Forced Response : stock vide a la fin de la phase -> inclinee et retournee en ALTER EGO",
       "« At the end of each phase, if Sunspot has no solar counters, exhaust Sunspot and flip him into his alter-ego form »",
       [HEROS] + solaires(0), ["Puzzle.EndPlayerPhase()"], {"forme": "AlterEgo", "exhausted": ["so001b"]}),
    _c("so001a Forced Response : TEMOIN, il reste des compteurs -> reste HEROS",
       "la condition est « no solar counters »",
       [HEROS], ["Puzzle.EndPlayerPhase()"], {"forme": "Hero"}),
    _c("so001a Forced Response : la phase du MECHANT compte aussi (« each phase »)",
       "chaque phase, pas seulement celle des joueurs",
       [HEROS] + solaires(0), ["Puzzle.BeginVillainPhase()", "Puzzle.EndPlayerPhase()"], {"forme": "AlterEgo"}),

    # ============================================================ so002 Cannonball
    _c("so002 Cannonball : valeurs imprimees cout 3, PV 3, ATK 2, THW 2, X-FORCE",
       "nombres texte <-> code (scan)",
       [HEROS] + en_jeu("so002"), [], {"traits_de": [["so002", "X-FORCE"]], "pv_max": [["so002", 3]]}),
    _c("so002 Cannonball : apres son attaque (2 degats), la PROCHAINE carte coute 1 de moins (Blazing Strike 2 -> 1, payee par UNE ressource : 2 + 6 = 8)",
       "« After Cannonball attacks, reduce the cost of the next card you play this phase by 1. »",
       [HEROS] + en_jeu("so002"), ["Puzzle.Attack('so002')"], {"degats": [[VILAIN, 8]]},
       main_exclusive=["so003", "01085"], jouer=["so003"], payer_avec=["01085"], cibles=[VILAIN], accepter_choix=True),
    _c("so002 Cannonball : TEMOIN, sans son attaque la carte coute 2, une seule ressource ne suffit pas",
       "la reduction ne vient que de l'attaque de Cannonball",
       [HEROS] + en_jeu("so002"), [], {"degats": [[VILAIN, 0]]},
       main_exclusive=["so003", "01085"], jouer=["so003"], payer_avec=["01085"], cibles=[VILAIN], accepter_choix=True),

    # ============================================================ so003 Blazing Strike
    _c("so003 Blazing Strike : 6 degats a Rhino, 1 compteur depense (5 -> 4)",
       "« Remove 1 solar counter from Sunspot -> deal 6 damage to an enemy »",
       [HEROS], [], {"degats": [[VILAIN, 6]], "compteurs": [["so001a", "solar", 4]]},
       main_exclusive=["so003", "01090"], jouer=["so003"], payer_avec=["01090"], cibles=[VILAIN], accepter_choix=True),
    _c("so003 Blazing Strike : avec le trait AERIAL (Solar Soar), l'ennemi est SONNE",
       "« If Sunspot has the AERIAL trait, stun that enemy. »",
       [HEROS] + en_jeu("so011"), [], {"degats": [[VILAIN, 6]], "statuts": [[VILAIN, "Stunned"]]},
       main_exclusive=["so003", "01090"], jouer=["so003"], payer_avec=["01090"], cibles=[VILAIN], accepter_choix=True),
    _c("so003 Blazing Strike : TEMOIN, sans le trait AERIAL, pas de statut Sonne",
       "le statut ne vient que du trait",
       [HEROS], [], {"degats": [[VILAIN, 6]], "statuts_absents": [[VILAIN, "Stunned"]]},
       main_exclusive=["so003", "01090"], jouer=["so003"], payer_avec=["01090"], cibles=[VILAIN], accepter_choix=True),
    _c("so003 Blazing Strike : stock VIDE, la carte n'est pas jouable (le compteur est un COUT)",
       "« Remove 1 solar counter -> » : sans compteur, aucun degat",
       [HEROS] + solaires(0), [], {"degats": [[VILAIN, 0]]},
       main_exclusive=["so003", "01090"], jouer=["so003"], payer_avec=["01090"], cibles=[VILAIN], accepter_choix=True),

    # ============================================================ so004 Blessings of the Sun
    _c("so004 Blessings of the Sun : stock 1 -> +1 compteur (2) -> +2 DEF, puis Solar Rechanneling retire les 2 (+2) : Tiger Shark (ATK 3) ne fait aucun degat",
       "« for each solar counter on Sunspot, +1 DEF » : sans la carte, DEF 1 seulement (Rechanneling X = 1) et Tiger Shark fait 2 degats",
       [HEROS] + solaires(1) + ["Puzzle.PutIntoPlay('01131')"], ["Puzzle.Defend('so001a', '01131')"],
       {"degats_identite": 0, "compteurs": [["so001a", "solar", 0]]},
       main_exclusive=["so004"], accepter_choix=True),
    _c("so004 Blessings of the Sun : stock vide -> 1 compteur pose -> +1 DEF, puis Solar Rechanneling en retire 1 (+1) : Tiger Shark (ATK 3) fait 1 degat",
       "le compteur POSE compte dans le « for each » (DEF 1) ; l'interruption du heros, acceptee ensuite, ajoute +1 : 3 - 2 = 1",
       [HEROS] + solaires(0) + ["Puzzle.PutIntoPlay('01131')"], ["Puzzle.Defend('so001a', '01131')"],
       {"degats_identite": 1, "compteurs": [["so001a", "solar", 0]]},
       main_exclusive=["so004"], accepter_choix=True),
    _c("so004 Blessings of the Sun : TEMOIN, sans l'evenement, stock vide, Tiger Shark (ATK 3) fait 3 degats",
       "la difference avec le cas precedent (3 -> 1) est la DEF de l'evenement + de Solar Rechanneling",
       [HEROS] + solaires(0) + ["Puzzle.PutIntoPlay('01131')"], ["Puzzle.Defend('so001a', '01131')"],
       {"degats_identite": 3}, accepter_choix=True),

    # ============================================================ so005 Radiant Disruption
    _c("so005 Radiant Disruption : X = 5 -> 5 menaces retirees (6 -> 1), stock 0",
       "« Remove X solar counters. Remove X threat from a scheme. »",
       [HEROS, f"Puzzle.SetThreat('{COMPLOT}', 6)"], [], {"menace": [[COMPLOT, 1]], "compteurs": [["so001a", "solar", 0]]},
       main_exclusive=["so005", "01090"], jouer=["so005"], payer_avec=["01090"], cibles=[COMPLOT], accepter_choix=True),
    _c("so005 Radiant Disruption : avec AERIAL, X menaces retirees d'une AUTRE manigance aussi",
       "« If Sunspot has the AERIAL trait, remove X threat from another scheme. »",
       [HEROS, f"Puzzle.SetThreat('{COMPLOT}', 6)"] + en_jeu("so011", "so013"), [],
       {"menace": [[COMPLOT, 1], ["so013", 1]]},
       main_exclusive=["so005", "01090"], jouer=["so005"], payer_avec=["01090"], cibles=[COMPLOT], accepter_choix=True),
    _c("so005 Radiant Disruption : avec AERIAL, la seconde manigance est OBLIGATOIRE (le joueur qui voudrait « Cancel » n'en a pas la possibilite)",
       "RR « May » : seul « may » donne une option ; « If Sunspot has the AERIAL trait, remove X threat from another scheme » n'en porte pas. "
       "Le pilote cherche l'option « Cancel » : elle n'existe plus, la 2e manigance perd ses 5 menaces (6 -> 1) quand meme",
       [HEROS, f"Puzzle.SetThreat('{COMPLOT}', 6)"] + en_jeu("so011", "so013"), [],
       {"menace": [[COMPLOT, 1], ["so013", 1]]},
       main_exclusive=["so005", "01090"], jouer=["so005"], payer_avec=["01090"], cibles=[COMPLOT], accepter_choix=True,
       preferer_option="Cancel"),
    _c("so005 Radiant Disruption : CONTRE-CAS, AERIAL mais AUCUNE autre manigance -> une seule retire (6 -> 1), rien ne plante, rien n'est force",
       "« another scheme » sans autre manigance : la seconde partie n'a pas de cible, la carte se resout quand meme",
       [HEROS, f"Puzzle.SetThreat('{COMPLOT}', 6)"] + en_jeu("so011"), [], {"menace": [[COMPLOT, 1]], "compteurs": [["so001a", "solar", 0]]},
       main_exclusive=["so005", "01090"], jouer=["so005"], payer_avec=["01090"], cibles=[COMPLOT], accepter_choix=True),

    # ============================================================ so006 Soak Up the Sun
    _c("so006 Soak Up the Sun : Action d'ALTER EGO, +5 compteurs (5 -> 10)",
       "« Alter-Ego Action: Place 5 solar counters on your identity card. »",
       [], [], {"compteurs": [["so001b", "solar", 10]]},
       main_exclusive=["so006", "01090"], jouer=["so006"], payer_avec=["01090"], accepter_choix=True),
    _c("so006 Soak Up the Sun : Action de HEROS avec AERIAL, +3 compteurs (5 -> 8)",
       "« Hero Action: If you have the AERIAL trait, place 3 solar counters on Sunspot. »",
       [HEROS] + en_jeu("so011"), [], {"compteurs": [["so001a", "solar", 8]]},
       main_exclusive=["so006", "01090"], jouer=["so006"], payer_avec=["01090"], accepter_choix=True),
    _c("so006 Soak Up the Sun : TEMOIN, forme heros SANS AERIAL, aucun compteur",
       "la Hero Action est conditionnee au trait",
       [HEROS], [], {"compteurs": [["so001a", "solar", 5]]},
       main_exclusive=["so006", "01090"], jouer=["so006"], payer_avec=["01090"], accepter_choix=True),

    # ============================================================ so007 Solar Flare
    _c("so007 Solar Flare : X = 5 -> 10 degats a Rhino ET au sbire engage (Shocker, 3 PV), Rhino desoriente",
       "« Confuse an enemy. Remove any number of solar counters -> deal 2 damage to that enemy and each minion engaged with you for each counter removed »",
       [HEROS] + en_jeu(SBIRE), [], {"degats": [[VILAIN, 10]], "statuts": [[VILAIN, "Confused"]], "compteurs": [["so001a", "solar", 0]]},
       main_exclusive=["so007", "01090", "01088"], jouer=["so007"], payer_avec=["01090", "01088"], cibles=[VILAIN], accepter_choix=True),
    _c("so007 Solar Flare : stock vide, l'ennemi est desoriente quand meme, aucun degat",
       "« Confuse an enemy » ne coute rien ; X = 0",
       [HEROS] + solaires(0), [], {"degats": [[VILAIN, 0]], "statuts": [[VILAIN, "Confused"]]},
       main_exclusive=["so007", "01090", "01088"], jouer=["so007"], payer_avec=["01090", "01088"], cibles=[VILAIN], accepter_choix=True),

    # ============================================================ so008 Solar Surge
    _c("so008 Solar Surge : stock 5 (> 4) -> TRIPLE : paye un evenement de cout 3 avec UNE carte",
       "« triple the resources instead if Sunspot has more than 4 solar counters »",
       [HEROS], [], {"degats": [[VILAIN, 6]]},
       main_exclusive=["so003", "so008"], jouer=["so003"], payer_avec=["so008"], cibles=[VILAIN], accepter_choix=True),
    _c("so008 Solar Surge : stock 3 (> 2) -> DOUBLE : paye Blazing Strike (cout 2) avec UNE carte",
       "« Double the number of resources this card generates if Sunspot has more than 2 solar counters »",
       [HEROS] + solaires(3), [], {"degats": [[VILAIN, 6]]},
       main_exclusive=["so003", "so008"], jouer=["so003"], payer_avec=["so008"], cibles=[VILAIN], accepter_choix=True),
    _c("so008 Solar Surge : TEMOIN, stock 2 (pas plus de 2) -> 1 seule ressource, ne paie pas un cout 2",
       "« MORE than 2 » : 2 ne suffit pas",
       [HEROS] + solaires(2), [], {"degats": [[VILAIN, 0]]},
       main_exclusive=["so003", "so008"], jouer=["so003"], payer_avec=["so008"], cibles=[VILAIN], accepter_choix=True),

    # ============================================================ so009 Da Costa International
    _c("so009 Da Costa International : apres Energy Absorption, +1 compteur (5 + 2 + 1 = 8)",
       "« After you resolve your Energy Absorption ability, place 1 solar counter on your identity. »",
       [] + en_jeu("so009"), ["Puzzle.Action('so001b', 'Action')"], {"compteurs": [["so001b", "solar", 8]]},
       main_exclusive=["01088"], cibles=["01088"], accepter_choix=True),
    _c("so009 Da Costa International : TEMOIN, sans le soutien, 5 + 2 = 7",
       "le compteur en plus ne vient que de la Response",
       [], ["Puzzle.Action('so001b', 'Action')"], {"compteurs": [["so001b", "solar", 7]]},
       main_exclusive=["01088"], cibles=["01088"], accepter_choix=True),

    # ============================================================ so010 Radiant Avenger
    _c("so010 Radiant Avenger : Sunspot gagne le trait AVENGER",
       "« Sunspot gains the AVENGER trait. »",
       [HEROS] + en_jeu("so010"), [], {"traits": ["X-FORCE", "AVENGER"]}),
    _c("so010 Radiant Avenger : Hero Action, incline + 1 compteur -> +1 ATK ce round (attaque de base 1)",
       "« Exhaust this card and remove 1 solar counter -> Sunspot gains +1 ATK until the end of the round »",
       [HEROS] + en_jeu("so010"), ["Puzzle.Action('so010', 'HeroAction')"], {"so_stats": {"attack": 1}, "exhausted": ["so010"],
                                                                         "compteurs": [["so001a", "solar", 4]]}),
    _c("so010 Radiant Avenger : Action, incline -> +1 compteur (5 -> 6)",
       "« Exhaust this card -> place 1 solar counter on Sunspot. »",
       [HEROS] + en_jeu("so010"), ["Puzzle.Action('so010', 'Action')"], {"exhausted": ["so010"], "compteurs": [["so001a", "solar", 6]]}),

    # ============================================================ so011 Solar Soar
    _c("so011 Solar Soar : Sunspot gagne le trait AERIAL",
       "« Sunspot gains the AERIAL trait. »",
       [HEROS] + en_jeu("so011"), [], {"traits": ["X-FORCE", "AERIAL"]}),
    _c("so011 Solar Soar : a la fin du tour, +1 compteur (5 -> 6)",
       "« Hero Response: At the end of your turn, place 1 solar counter on Sunspot. »",
       [HEROS] + en_jeu("so011"), ["Puzzle.EndPlayerTurn()"], {"compteurs": [["so001a", "solar", 6]]}, accepter_choix=True),

    # ============================================================ so012 M-Pox Sickness
    _c("so012 M-Pox Sickness : la PREMIERE carte du round coute 1 de plus (Blazing Strike 2 -> 3, payee par RR + 1 : refusee avec RR seul)",
       "« Increase the resource cost of the first card you play each round by 1. »",
       [HEROS] + en_jeu("so012"), [], {"degats": [[VILAIN, 0]]},
       main_exclusive=["so003", "01090"], jouer=["so003"], payer_avec=["01090"], cibles=[VILAIN], accepter_choix=True),
    _c("so012 M-Pox Sickness : payee par RR + YY (4 ressources), la premiere carte passe",
       "le surcout est de 1 exactement",
       [HEROS] + en_jeu("so012"), [], {"degats": [[VILAIN, 6]]},
       main_exclusive=["so003", "01090", "01088"], jouer=["so003"], payer_avec=["01090", "01088"], cibles=[VILAIN], accepter_choix=True),
    _c("so012 M-Pox Sickness : TEMOIN, sans l'obligation, RR suffit",
       "le surcout vient de l'obligation",
       [HEROS], [], {"degats": [[VILAIN, 6]]},
       main_exclusive=["so003", "01090"], jouer=["so003"], payer_avec=["01090"], cibles=[VILAIN], accepter_choix=True),
    _c("so012 M-Pox Sickness : Action d'alter ego, 3 compteurs retires -> l'obligation quitte la partie",
       "« Alter-Ego Action: Remove 3 solar counters from your identity -> remove M-Pox Sickness from the game. »",
       en_jeu("so012"), ["Puzzle.Action('so012', 'AlterEgoAction')"], {"hors_jeu": ["so012"], "compteurs": [["so001b", "solar", 2]]}),
]


# =============================================================== nemesis
CAS += [
    _c("so014 Donald Pierce : valeurs imprimees PV 6, ATK 3, SCH 1, CYBORG ELITE HELLFIRE",
       "nombres texte <-> code (scan)",
       en_jeu("so014"), [], {"traits_de": [["so014", "CYBORG"], ["so014", "ELITE"], ["so014", "HELLFIRE"]], "pv_max": [["so014", 6]]}),
    _c("so015 Cybernetic Assault : Pierce EN JEU -> il attaque (Rhino est le vilain, Pierce ATK 3 : 3 degats a l'identite)",
       "« When Revealed: Donald Pierce attacks you. »",
       [HEROS] + en_jeu("so014"), ["Puzzle.Reveal('so015')"], {"degats_identite": 3}),
    _c("so015 Cybernetic Assault : Pierce ABSENT (dans le deck rencontre) -> mis en jeu engage avec vous",
       "« If he is not in play, search the encounter deck and discard pile for Donald Pierce and put him into play engaged with you. »",
       ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('so014', '01098', '01098', '01098')"], ["Puzzle.Reveal('so015')"],
       {"en_jeu": ["so014"]}, sans=[]),
    _c("so016 Political Persecution : la manigance annexe n'est PAS en jeu -> 2 menaces sur la manigance principale",
       "« If it is not in play, place 2 threats to the main scheme. »",
       [], ["Puzzle.Reveal('so016')"], {"menace": [[COMPLOT, 2]]}),
    _c("so016 Political Persecution : Superhuman Mutants Murdering en jeu -> 2 menaces SUR ELLE, aucune sur la principale",
       "« If the Superhuman Mutants Murdering scheme is in play, place 2 threats to that scheme. »",
       en_jeu("so013"), ["Puzzle.Reveal('so016')"], {"menace": [["so013", 8], [COMPLOT, 0]]}),
    _c("so013 Superhuman Mutants Murdering : menace de depart 6 (fixe), Hazard",
       "nombres texte <-> code (scan) : 6 au coin ; icone [hazard] verifiee contre 01180 Legions of Hydra",
       en_jeu("so013"), [], {"menace": [["so013", 6]]}),
    _c("so013 Superhuman Mutants Murdering : chaque activation de Pierce en declenche UNE de plus, sans rebond (>= 2 attaques : 6 degats)",
       "« After Donald Pierce activates against you, it activates against you again. » Le banc enchaine plusieurs activations : on mesure "
       "l'invariant (autant d'activations supplementaires que de Responses ignorees, au moins une) et au moins 6 degats",
       [HEROS, "Puzzle.PutIntoPlay('so013')", "Puzzle.PutIntoPlay('so014')"], ["Puzzle.Activate('so014')"],
       {"degats_identite_min": 6, "so013_journal": True}),
    _c("so013 Superhuman Mutants Murdering : TEMOIN, sans la manigance, Pierce n'attaque qu'une fois (3 degats)",
       "la seconde activation vient de la manigance",
       [HEROS, "Puzzle.PutIntoPlay('so014')"], ["Puzzle.Activate('so014')"], {"degats_identite": 3}),
]


VERIFICATIONS = r'''

def so_etat(monde, aides):
    """Cles propres : `so_stats` ({attribut: valeur} lus sur l'identite), le reste va a etat_attendu."""
    cas = aides["cas"]
    attendu = cas.get("attendu") or {}
    soucis = []
    identite = aides["identite"](monde)
    for nom, valeur in (attendu.get("so_stats") or {}).items():
        courant = getattr(identite, nom, None)
        if courant != valeur:
            soucis.append(f"{nom} = {courant} (attendu {valeur})")
    if attendu.get("so013_journal"):
        import sys
        module = sys.modules.get("cards.pack.sunspot_hellfire.sunspot_hellfire_hunt_nemesis.so013")
        journal = list(getattr(module, "JOURNAL_ACTIVATIONS", [])) if module else []
        extras, ignores = journal.count("extra"), journal.count("ignore")
        if extras < 1 or extras != ignores:
            soucis.append(f"journal so013 : {extras} activation(s) supplementaire(s), {ignores} ignoree(s) (attendu : egaux, au moins 1) {journal}")
    reste = {k: v for k, v in attendu.items() if k not in ("so_stats", "so013_journal")}
    copie = dict(aides); copie["cas"] = dict(cas); copie["cas"]["attendu"] = reste
    ok, message = etat_attendu(monde, copie)
    if not ok:
        soucis.append(message)
    if soucis:
        return False, " ; ".join(soucis)
    return True, message
'''
