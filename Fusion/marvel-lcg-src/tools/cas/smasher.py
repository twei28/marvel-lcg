# Cas test_capacites du heros SMASHER (Starjammers, Phenexian, prefixe `sz`) :
# noms prefixes « [sz] » puis le card_id (substituer_pack.py filtre dessus).
#
# Rappels de montage :
#  - le deck `smasher` demarre en ALTER EGO (sz001b) ; `Puzzle.ChangeToFace('sz001b', 'sz001a')` la passe en HEROS ;
#  - Rhino 01094 est le vilain (ATQ 2, 14 PV), 01097b son complot principal (menace 0 au depart), 01101 Hydra Mercenary un sbire
#    (3 PV, ATQ 1, boost 1, Guard), 01172 Whiplash un sbire a Retaliate 1 (4 PV, ATQ 3), 01098 Armored Rhino Suit n'a AUCUNE icone de boost ;
#  - ⚠ `defausse: [id]` lit la DEFAUSSE ENTIERE : le harnais y jette la main de depart (`main_exclusive`), qui contient d'autres exemplaires de la
#    meme carte (les ameliorations du deck de heros). Pour prouver que l'exemplaire EN JEU est parti, ecrire `hors_jeu: [id]` (vu rouge a la
#    substitution du 26/10/2026 : `sz001a` restait verte 5/5 sans son module) ;
#  - ressources : 01088 Energy = YY, 01089 Genius = BB, 01090 Strength = RR ; 01002 Black Cat (2 PV) est un allie neutre
#    (n'a aucun effet a l'entree en jeu, contrairement a 01083 Mockingbird qui sonne un ennemi).
SC = "rhino"
HEROS = "Puzzle.ChangeToFace('sz001b', 'sz001a')"
CIVIL = "Puzzle.ChangeToFace('sz001a', 'sz001b')"
VILAIN = "01094"
COMPLOT = "01097b"
SBIRE = "01101"
RETALIATE = "01172"
SANS_BOOST = ["Puzzle.EmptyEncounterDeck()",
              "Puzzle.CreateEncounterDeck('01098', '01098', '01098', '01098', '01098', '01098', '01098', '01098')"]


def en_jeu(*ids):
    return [f"Puzzle.PutIntoPlay('{i}', under_control=True)" for i in ids]


def _c(nom, pourquoi, mise, declencher, attendu, **cle):
    base = [] if cle.pop("sans_deck_neutre", False) else SANS_BOOST
    mise = base + list(mise)
    cas = {"nom": "[sz] " + nom, "pourquoi": pourquoi, "scenario": cle.pop("scenario", SC),
           "heros": cle.pop("heros", "smasher"), "mise_en_place": mise, "declencher": declencher,
           "verifier": cle.pop("verifier", "sz_etat"), "attendu": attendu}
    cas.setdefault("regles", ["v16_all", "v18_all"])
    cas.update(cle)
    return cas


def joue(carte, ressource="01088", cibles=None, **cle):
    """Cles communes pour JOUER `carte` de la main en la payant avec `ressource`."""
    base = {"main_exclusive": [carte, ressource], "payer_avec": [ressource], "jouer": [carte], "accepter_choix": True}
    if cibles is not None:
        base["cibles"] = cibles
    base.update(cle)
    return base


CAS = [
    # ============================================================ sz001a / sz001b : identite
    _c("sz001a Smasher : valeurs imprimees PV 12, ATK 1, THW 1, DEF 1, HS 5, AVENGER IMPERIAL GUARD",
       "nombres texte <-> code (scan) : HAND SIZE 5 / HIT POINTS 12, THW 1 ATK 1 DEF 1",
       [HEROS], [], {"pv_max": [["sz001a", 12]], "traits": ["AVENGER", "IMPERIAL GUARD"],
                     "sz_stats": {"attack": 1, "thwart": 1, "defense": 1, "hand_size": 5}}, main_exclusive=["01090"]),
    _c("sz001b Izzy Kane : valeurs imprimees PV 12, REC 3, HS 6, SOLDIER",
       "nombres texte <-> code (scan) : HAND SIZE 6 / HIT POINTS 12 / REC 3",
       [], [], {"pv_max": [["sz001b", 12]], "traits": ["SOLDIER"], "sz_stats": {"recover": 3, "hand_size": 6}}, main_exclusive=["01090"]),
    _c("sz001a Forced Response : on joue Hyper-Speed, Penta-Vision (autre EXOSPEX en jeu) est defaussee et Hyper-Speed reste",
       "« After you play an EXOSPEX upgrade, discard all other EXOSPEX upgrades you control »",
       [HEROS] + en_jeu("sz005"), [], {"en_jeu": ["sz007"], "hors_jeu": ["sz005"]}, **joue("sz007")),
    _c("sz001a Forced Response : TROIS EXOSPEX en jeu -> les deux AUTRES partent, la carte jouee reste",
       "« discard ALL other EXOSPEX upgrades » : Penta-Vision et Hyper-Strength posees, Hyper-Speed jouee",
       [HEROS] + en_jeu("sz005", "sz006"), [], {"en_jeu": ["sz007"], "hors_jeu": ["sz005", "sz006"]}, **joue("sz007")),
    _c("sz001a Forced Response : CONTRE-CAS, on joue un soutien (Home on Chandilar) : Penta-Vision reste en jeu",
       "seule une amelioration EXOSPEX declenche la defausse", [HEROS] + en_jeu("sz005"), [],
       {"en_jeu": ["sz005", "sz003"]}, **joue("sz003", ressource="01090")),
    _c("sz001a Forced Response : CONTRE-CAS, une amelioration SANS le trait EXOSPEX (01027 Focused Rage) ne chasse pas Penta-Vision",
       "le declencheur est le TRAIT EXOSPEX de la carte jouee", [HEROS] + en_jeu("sz005"), [],
       {"en_jeu": ["sz005", "01027"]}, **joue("01027", ressource="01090", main_exclusive=["01027", "01090", "01088"], payer_avec=["01090", "01088"])),
    _c("sz001b Izzy Kane : en ALTER EGO, une 2e amelioration EXOSPEX n'est PAS jouable (Penta-Vision en jeu, Hyper-Speed reste en main)",
       "« You cannot have more than 1 EXOSPEX upgrade in play » : la carte jouee ne se pose pas",
       en_jeu("sz005"), [], {"en_jeu": ["sz005"], "sz_main": ["sz007"]}, **joue("sz007")),
    _c("sz001b Izzy Kane : CONTRE-CAS, sans EXOSPEX en jeu l'amelioration se joue (alter ego)",
       "la restriction ne vaut que s'il y en a deja une", [], [], {"en_jeu": ["sz007"]}, **joue("sz007")),
    _c("sz001b Battle Ready : Action, une EXOSPEX du DECK (Hyper-Strength) passe en main",
       "« Search your deck and discard pile for an EXOSPEX upgrade and add it to your hand »",
       ["Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01073', 'sz006', '01074')"],
       ["Puzzle.Action('sz001b', 'Action')"], {"sz_main": ["sz006"]}, main_exclusive=["01090"], cibles=["sz006"], accepter_choix=True),
    _c("sz001b Battle Ready : une EXOSPEX de la DEFAUSSE (Exo-Flight) passe en main",
       "la defausse est aussi fouillee",
       ["Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01073', '01074')", "Puzzle.EmptyPlayerDiscardPile()",
        "Puzzle.CreatePlayerDiscardPile('sz009', '01090')"],
       ["Puzzle.Action('sz001b', 'Action')"], {"sz_main": ["sz009"]}, main_exclusive=["01090"], cibles=["sz009"], accepter_choix=True),
    _c("sz001b Battle Ready : TEMOIN D'EPUISEMENT, une seule fois par tour (la 2e Action est refusee, une seule EXOSPEX en main)",
       "« (Limit once per turn.) » : deux declenchements dans le meme round (le 2e dans `declencher_tolerant`), deux EXOSPEX dans le deck, une seule arrive en main (+ la Strength de depart = 2 cartes)",
       ["Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01073', 'sz006', 'sz007', '01074')"],
       ["Puzzle.Action('sz001b', 'Action')"], {"taille_main": 2, "sz_main": ["sz006"]},
       main_exclusive=["01090"], cibles=["sz006"], accepter_choix=True, declencher_tolerant=["Puzzle.Action('sz001b', 'Action')"]),
    _c("sz001b Battle Ready : « once per TURN » et non « per round » : au TOUR SUIVANT du meme joueur (tour de plus), l'Action repart (2 EXOSPEX en main)",
       "RR « Action » ; la limite se compte par tour : un tour de plus dans le meme round (rm007) rouvre la capacite. Montage : 1re Action, "
       "fin du tour (compteurs « ce tour » remis a zero), 2e Action : sz006 ET sz007 arrivent en main (+ la Strength de depart = 3 cartes)",
       ["Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01073', 'sz006', 'sz007', '01074')"],
       ["Puzzle.Action('sz001b', 'Action')", "Puzzle.NewPlayerTurnStat()", "Puzzle.Action('sz001b', 'Action')"],
       {"taille_main": 3, "sz_main": ["sz006", "sz007"]},
       main_exclusive=["01090"], cibles=["sz006", "sz007"], accepter_choix=True),

    # ============================================================ sz002 Cannonball
    _c("sz002 Cannonball : valeurs imprimees PV 3, AERIAL X-MEN",
       "nombres texte <-> code (scan) : cout 3, HP 3, ATK 2 THW 2 (deux icones de degats consequents chacun)",
       [HEROS] + en_jeu("sz002"), [], {"pv_max": [["sz002", 3]], "traits_de": [["sz002", "AERIAL"], ["sz002", "X-MEN"]]},
       main_exclusive=["01090"]),
    _c("sz002 Cannonball : identite AERIAL (Exo-Flight en jeu) -> il entre en jeu avec une carte Tough",
       "« Cannonball has toughness if your identity has the AERIAL trait »", [HEROS] + en_jeu("sz009"), [],
       {"en_jeu": ["sz002"], "statuts": [["sz002", "Tough"]]}, **joue("sz002", ressource="01090", main_exclusive=["sz002", "01090", "01088"], payer_avec=["01090", "01088"])),
    _c("sz002 Cannonball : CONTRE-CAS, identite NON aerienne, mis en jeu sans etre JOUE -> aucune carte Tough",
       "sans le trait AERIAL pas de Toughness (PutIntoPlay ne declenche aucune Response « after you play »)", [HEROS] + en_jeu("sz002"), [],
       {"en_jeu": ["sz002"], "statuts_absents": [["sz002", "Tough"]]}, main_exclusive=["01090"]),
    _c("sz002 Cannonball : jouer Cannonball LUI-MEME (carte AERIAL) lui donne une carte Tough par sa Response (comportement du moteur, question en attente)",
       "« After you play an AERIAL card » : Cannonball est lui-meme AERIAL, et il est en jeu quand la Response part",
       [HEROS], [], {"en_jeu": ["sz002"], "statuts": [["sz002", "Tough"]]},
       **joue("sz002", ressource="01090", main_exclusive=["sz002", "01090", "01088"], payer_avec=["01090", "01088"])),
    _c("sz002 Cannonball : Response, on joue une carte AERIAL (Power Couple) -> Cannonball recoit une carte Tough",
       "« After you play an AERIAL card, give Cannonball a tough status card »",
       [HEROS] + en_jeu("sz002"), [], {"statuts": [["sz002", "Tough"]]}, **joue("sz015", ressource="01088", main_exclusive=["sz015", "01088", "01089"], payer_avec=["01088"])),
    _c("sz002 Cannonball : CONTRE-CAS, on joue une carte NON aerienne (Home on Chandilar) -> pas de carte Tough",
       "le declencheur est le trait AERIAL de la carte jouee", [HEROS] + en_jeu("sz002"), [],
       {"statuts_absents": [["sz002", "Tough"]]}, **joue("sz003", ressource="01090")),

    # ============================================================ sz003 Home on Chandilar
    _c("sz003 Home on Chandilar : Action d'alter ego, s'incline et pioche 2 cartes",
       "« Alter-Ego Action: Exhaust Home on Chandilar -> draw 2 cards »",
       en_jeu("sz003") + ["Puzzle.EmptyHand()"], ["Puzzle.Action('sz003', 'AlterEgoAction')"],
       {"exhausted": ["sz003"], "taille_main": 2}),
    _c("sz003 Home on Chandilar : valeurs imprimees LOCATION, SHI'AR",
       "nombres texte <-> code (scan)", en_jeu("sz003"), [], {"traits_de": [["sz003", "LOCATION"], ["sz003", "SHI'AR"]]}, main_exclusive=["01090"]),

    # ============================================================ sz004 Accessing
    _c("sz004 Accessing : Penta-Vision -> sa Hero Response (3 degats a un ennemi) puis elle est defaussee",
       "« Resolve the Hero Response ability on an EXOSPEX upgrade you control. Then discard that upgrade »",
       [HEROS] + en_jeu("sz005"), [], {"degats": [[VILAIN, 3]], "hors_jeu": ["sz005"]},
       main_exclusive=["sz004"], jouer=["sz004"], cibles=["sz005", VILAIN], accepter_choix=True),
    _c("sz004 Accessing : la Response (attack) de Penta-Vision resolue par Accessing EST une attaque : Smasher SONNEE -> le Sonne part, 0 degat a Rhino",
       "RR « Labeled Ability » : resoudre une capacite etiquetee (attack) = une attaque de l'identite ; une attaque d'un personnage sonne "
       "retire le Sonne a la place (et ne frappe pas). Avant le 26/10/2026 : 3 degats directs, le Sonne restait",
       [HEROS, "Puzzle.Stun('sz001a')"] + en_jeu("sz005"), [],
       {"degats": [[VILAIN, 0]], "statuts_absents": [["sz001a", "Stunned"]], "hors_jeu": ["sz005"]},
       main_exclusive=["sz004"], jouer=["sz004"], cibles=["sz005", VILAIN], accepter_choix=True),
    _c("sz004 Accessing : TEMOIN, la meme resolution sans Sonne -> 3 degats a Rhino (l'attaque passe)",
       "meme montage sans statut : l'attaque etiquetee frappe pour 3", [HEROS] + en_jeu("sz005"), [],
       {"degats": [[VILAIN, 3]], "hors_jeu": ["sz005"]},
       main_exclusive=["sz004"], jouer=["sz004"], cibles=["sz005", VILAIN], accepter_choix=True),
    _c("sz005 Penta-Vision : TEMOIN de l'etiquette (attack) : jouee de la main, Smasher SONNEE -> le Sonne part, 0 degat a Rhino",
       "montre que le moteur traite bien une capacite (attack) comme une attaque (le Sonne d'une identite s'y applique)",
       [HEROS, "Puzzle.Stun('sz001a')"], [], {"degats": [[VILAIN, 0]], "statuts_absents": [["sz001a", "Stunned"]], "en_jeu": ["sz005"]},
       **joue("sz005", cibles=[VILAIN])),
    _c("sz004 Accessing : Hyper-Strength -> un ennemi est sonne, puis defaussee",
       "la Response de Hyper-Strength : stun an enemy", [HEROS] + en_jeu("sz006"), [],
       {"statuts": [[VILAIN, "Stunned"]], "hors_jeu": ["sz006"]},
       main_exclusive=["sz004"], jouer=["sz004"], cibles=["sz006", VILAIN], accepter_choix=True),
    _c("sz004 Accessing : Hyper-Speed -> le heros INCLINE se redresse, puis defaussee",
       "la Response de Hyper-Speed : ready Smasher", [HEROS] + en_jeu("sz007") + ["Puzzle.Exhaust('sz001a')"], [],
       {"pret": ["sz001a"], "hors_jeu": ["sz007"]},
       main_exclusive=["sz004"], jouer=["sz004"], cibles=["sz007"], accepter_choix=True),
    _c("sz004 Accessing : Super-Resistance -> Smasher recoit une carte Tough, puis defaussee",
       "la Response de Super-Resistance : give Smasher a tough status card", [HEROS] + en_jeu("sz008"), [],
       {"statuts": [["sz001a", "Tough"]], "hors_jeu": ["sz008"]},
       main_exclusive=["sz004"], jouer=["sz004"], cibles=["sz008"], accepter_choix=True),
    _c("sz004 Accessing : Exo-Flight -> 3 menaces retirees (5 -> 2), puis defaussee",
       "la Response de Exo-Flight : remove 3 threat from a scheme", [HEROS, f"Puzzle.SetThreat('{COMPLOT}', 5)"] + en_jeu("sz009"), [],
       {"menace": [[COMPLOT, 2]], "hors_jeu": ["sz009"]},
       main_exclusive=["sz004"], jouer=["sz004"], cibles=["sz009", COMPLOT], accepter_choix=True),
    _c("sz004 Accessing : CONTRE-CAS, aucune amelioration EXOSPEX en jeu -> Accessing n'est pas jouable (reste en main)",
       "« on an EXOSPEX upgrade you control » : sans cible legale la carte n'est pas proposee",
       [HEROS], [], {"sz_main": ["sz004"]}, main_exclusive=["sz004"], jouer=["sz004"], accepter_choix=True),

    # ============================================================ sz005 Penta-Vision
    _c("sz005 Penta-Vision : Smasher gagne +1 ATK et +1 THW (ATK 2, THW 2)",
       "« Smasher gets +1 ATK and +1 THW »", [HEROS] + en_jeu("sz005"), [], {"sz_stats": {"attack": 2, "thwart": 2, "defense": 1}},
       main_exclusive=["01090"]),
    _c("sz005 Penta-Vision : Hero Response (attack), jouee de la main -> 3 degats a Rhino",
       "« After you play Penta-Vision, deal 3 damage to an enemy »", [HEROS], [], {"degats": [[VILAIN, 3]], "en_jeu": ["sz005"]},
       **joue("sz005", cibles=[VILAIN])),
    _c("sz005 Penta-Vision : l'attaque de Smasher est A DISTANCE (Whiplash, Retaliate 1, ne riposte pas : 0 degat au heros)",
       "« Smasher's attacks gain ranged » : ranged ignore la Riposte",
       [HEROS, f"Puzzle.PutIntoPlay('{RETALIATE}', under_control=False)"] + en_jeu("sz005"), ["Puzzle.Attack('sz001a')"],
       {"degats": [[RETALIATE, 2]], "degats_identite": 0}, main_exclusive=["01090"], cibles=[RETALIATE], accepter_choix=True),
    _c("sz005 Penta-Vision : TEMOIN de la Riposte, meme attaque avec Hyper-Speed (sans ranged) -> Whiplash riposte (1 degat au heros)",
       "meme montage sans le mot-clE ranged : la Riposte s'applique",
       [HEROS, f"Puzzle.PutIntoPlay('{RETALIATE}', under_control=False)"] + en_jeu("sz007"), ["Puzzle.Attack('sz001a')"],
       {"degats": [[RETALIATE, 2]], "degats_identite": 1}, main_exclusive=["01090"], cibles=[RETALIATE], accepter_choix=True),
    _c("sz005 Penta-Vision : valeurs imprimees EXOSPEX SUPERPOWER",
       "nombres texte <-> code (scan)", [HEROS] + en_jeu("sz005"), [], {"traits_de": [["sz005", "EXOSPEX"], ["sz005", "SUPERPOWER"]]},
       main_exclusive=["01090"]),

    # ============================================================ sz006 Hyper-Strength
    _c("sz006 Hyper-Strength : Smasher gagne +2 ATK (ATK 3)",
       "« Smasher gets +2 ATK »", [HEROS] + en_jeu("sz006"), [], {"sz_stats": {"attack": 3, "thwart": 1, "defense": 1}},
       main_exclusive=["01090"]),
    _c("sz006 Hyper-Strength : Hero Response, jouee de la main -> un ennemi est sonne",
       "« After you play Hyper-Strength, stun an enemy »", [HEROS], [], {"statuts": [[VILAIN, "Stunned"]], "en_jeu": ["sz006"]},
       **joue("sz006", ressource="01090", cibles=[VILAIN])),
    _c("sz006 Hyper-Strength : l'attaque a OVERKILL (sbire a 1 PV restant, ATK 3 : 2 degats d'exces a Rhino)",
       "« Smasher's attacks gain overkill » : exces = 3 - 1 = 2 vers le vilain",
       [HEROS, f"Puzzle.PutIntoPlay('{SBIRE}', under_control=False)", f"Puzzle.Damage('{SBIRE}', 2)"] + en_jeu("sz006"),
       ["Puzzle.Attack('sz001a')"], {"hors_jeu": [SBIRE], "degats": [[VILAIN, 2]]},
       main_exclusive=["01090"], cibles=[SBIRE], accepter_choix=True),
    _c("sz006 Hyper-Strength : TEMOIN d'overkill, meme montage avec Hyper-Speed (ATK 2, sans overkill) -> exces perdu (0 degat a Rhino)",
       "meme attaque sans le mot-cle overkill : l'exces n'est pas reporte",
       [HEROS, f"Puzzle.PutIntoPlay('{SBIRE}', under_control=False)", f"Puzzle.Damage('{SBIRE}', 2)"] + en_jeu("sz007"),
       ["Puzzle.Attack('sz001a')"], {"hors_jeu": [SBIRE], "degats": [[VILAIN, 0]]},
       main_exclusive=["01090"], cibles=[SBIRE], accepter_choix=True),

    # ============================================================ sz007 Hyper-Speed
    _c("sz007 Hyper-Speed : Smasher gagne +1 ATK, +1 THW et +1 DEF (2, 2, 2)",
       "« Smasher gets +1 ATK, +1 THW and +1 DEF »", [HEROS] + en_jeu("sz007"), [], {"sz_stats": {"attack": 2, "thwart": 2, "defense": 2}},
       main_exclusive=["01090"]),
    _c("sz007 Hyper-Speed : Hero Response, jouee de la main -> Smasher INCLINEE se redresse",
       "« After you play Hyper-Speed, ready Smasher »", [HEROS, "Puzzle.Exhaust('sz001a')"], [], {"pret": ["sz001a"], "en_jeu": ["sz007"]},
       **joue("sz007")),

    # ============================================================ sz008 Super-Resistance
    _c("sz008 Super-Resistance : Smasher gagne +2 DEF (3) et STALWART",
       "« Smasher gets +2 DEF and gains Stalwart »", [HEROS] + en_jeu("sz008"), [],
       {"sz_stats": {"attack": 1, "thwart": 1, "defense": 3, "stalwart": 1}}, main_exclusive=["01090"]),
    _c("sz008 Super-Resistance : Hero Response, jouee de la main -> Smasher recoit une carte Tough",
       "« After you play Super-Resistance, give Smasher a tough status card »", [HEROS], [],
       {"statuts": [["sz001a", "Tough"]], "en_jeu": ["sz008"]}, **joue("sz008", ressource="01090")),
    _c("sz008 Super-Resistance : STALWART, Smasher ne peut pas etre sonnee (Puzzle.Stun ne pose aucune carte)",
       "Stalwart : le statut Sonne n'est pas pose", [HEROS] + en_jeu("sz008") + ["Puzzle.Stun('sz001a')"], [],
       {"statuts_absents": [["sz001a", "Stunned"]]}, main_exclusive=["01090"]),

    # ============================================================ sz009 Exo-Flight
    _c("sz009 Exo-Flight : Smasher gagne +1 THW et +1 DEF (2, 2) et le trait AERIAL",
       "« Smasher gets +1 THW, +1 DEF and gains the AERIAL trait »", [HEROS] + en_jeu("sz009"), [],
       {"sz_stats": {"attack": 1, "thwart": 2, "defense": 2}, "traits": ["AVENGER", "IMPERIAL GUARD", "AERIAL"]}, main_exclusive=["01090"]),
    _c("sz009 Exo-Flight : Hero Response (thwart), jouee de la main -> 3 menaces retirees (5 -> 2)",
       "« After you play Exo-Flight, remove 3 threat from a scheme »", [HEROS, f"Puzzle.SetThreat('{COMPLOT}', 5)"], [],
       {"menace": [[COMPLOT, 2]], "en_jeu": ["sz009"]}, **joue("sz009", cibles=[COMPLOT])),
    _c("sz009 Exo-Flight : valeurs imprimees AERIAL EXOSPEX SUPERPOWER",
       "nombres texte <-> code (scan)", [HEROS] + en_jeu("sz009"), [],
       {"traits_de": [["sz009", "AERIAL"], ["sz009", "EXOSPEX"], ["sz009", "SUPERPOWER"]]}, main_exclusive=["01090"]),

    # ============================================================ sz010 Family Matters
    _c("sz010 Family Matters : « Your hand size is reduced by 3 » (alter ego : 6 -> 3)",
       "obligation donnee a Izzy Kane, hand size 6 - 3", ["Puzzle.Reveal('sz010')"], [], {"sz_stats": {"hand_size": 3}}, main_exclusive=["01090"]),
    _c("sz010 Family Matters : Alter-Ego Action, Izzy Kane s'incline -> l'obligation est defaussee (defausse rencontre)",
       "« Exhaust Izzy Kane or Cannonball -> discard Family Matters » : premiere branche",
       ["Puzzle.Reveal('sz010')"], ["Puzzle.Action('sz010', 'AlterEgoAction', index=0)"],
       {"defausse_rencontre": ["sz010"], "exhausted": ["sz001b"]}, main_exclusive=["01090"], accepter_choix=True),
    _c("sz010 Family Matters : Alter-Ego Action, Cannonball s'incline -> l'obligation est defaussee, Izzy Kane reste prete",
       "seconde branche (l'allie paie a la place de l'identite)",
       en_jeu("sz002") + ["Puzzle.Reveal('sz010')"], ["Puzzle.Action('sz010', 'AlterEgoAction', index=1)"],
       {"defausse_rencontre": ["sz010"], "exhausted": ["sz002"], "pret": ["sz001b"]}, main_exclusive=["01090"], accepter_choix=True),

    # ============================================================ sz011 Scientist Supreme
    _c("sz011 Scientist Supreme : valeurs imprimees PV 4, A.I.M ELITE GENIUS",
       "nombres texte <-> code (scan) : HP 4, SCH 2, ATK 1",
       ["Puzzle.PutIntoPlay('sz011', under_control=False)"], [], {"pv_max": [["sz011", 4]], "traits_de": [["sz011", "A.I.M"], ["sz011", "ELITE"], ["sz011", "GENIUS"]]},
       main_exclusive=["01090"]),
    _c("sz011 Scientist Supreme : When Revealed, le joueur est sonne ET desoriente",
       "« You are stunned and confused » : alter ego du joueur", [], ["Puzzle.Reveal('sz011')"],
       {"statuts": [["sz001b", "Stunned"], ["sz001b", "Confused"]]}, main_exclusive=["01090"]),
    _c("sz011 Scientist Supreme : VILLAINOUS, son attaque pioche une carte de boost (deck rencontre 8 -> 7)",
       "mot-cle automatique : une carte de boost par activation (desc.Villainous)",
       [HEROS, "Puzzle.PutIntoPlay('sz011', under_control=False)", "Puzzle.Exhaust('sz001a')"], ["Puzzle.EnemyAttacks('sz011', 'sz001a')"],
       {"sz_deck_rencontre": 7}, main_exclusive=["01090"], accepter_choix=True),
    _c("sz011 Scientist Supreme : TEMOIN, un sbire non Villainous (Hydra Mercenary) attaque sans boost (deck rencontre 8)",
       "meme attaque par un sbire ordinaire : aucune carte de boost",
       [HEROS, f"Puzzle.PutIntoPlay('{SBIRE}', under_control=False)", "Puzzle.Exhaust('sz001a')"], [f"Puzzle.EnemyAttacks('{SBIRE}', 'sz001a')"],
       {"sz_deck_rencontre": 8}, main_exclusive=["01090"], accepter_choix=True),
    _c("sz011 Scientist Supreme : ses attaques sont PERFORANTES (la carte Tough du heros est defaussee, 1 degat passe)",
       "« [star] Scientist Supreme's attacks gain piercing and ranged » : piercing contourne Tough",
       [HEROS, "Puzzle.PutIntoPlay('sz011', under_control=False)", "Puzzle.Tough('sz001a')", "Puzzle.Exhaust('sz001a')"],
       ["Puzzle.EnemyAttacks('sz011', 'sz001a')"], {"degats_identite": 1, "statuts_absents": [["sz001a", "Tough"]]},
       sans_deck_neutre=False, main_exclusive=["01090"], accepter_choix=True),
    _c("sz011 Scientist Supreme : TEMOIN de la perforation, un sbire ordinaire contre Tough : 0 degat et la carte Tough est consommee",
       "sans piercing, Tough absorbe l'attaque (Hydra Mercenary ATK 1)",
       [HEROS, f"Puzzle.PutIntoPlay('{SBIRE}', under_control=False)", "Puzzle.Tough('sz001a')", "Puzzle.Exhaust('sz001a')"],
       [f"Puzzle.EnemyAttacks('{SBIRE}', 'sz001a')"], {"degats_identite": 0, "statuts_absents": [["sz001a", "Tough"]]},
       main_exclusive=["01090"], accepter_choix=True),

    # ============================================================ sz012 Entropic Subversion
    _c("sz012 Entropic Subversion : menace de depart 3 (un heros)",
       "nombres texte <-> code (scan) : 3 par heros", ["Puzzle.Reveal('sz012')"], [], {"menace": [["sz012", 3]]}, main_exclusive=["01090"]),
    _c("sz012 Entropic Subversion : une carte SONNE defaussee d'un personnage ami -> 2 degats a un personnage ami (le heros)",
       "« After a status card is discarded from a friendly character, if that status was Stunned - Deal 2 damage to a friendly character »",
       [HEROS, "Puzzle.Reveal('sz012')", "Puzzle.Stun('sz001a')"], ["Puzzle.Stun('sz001a')"],
       {"degats_identite": 2}, main_exclusive=["01090"], cibles=["sz001a"], accepter_choix=True),
    _c("sz012 Entropic Subversion : une carte DESORIENTE defaussee d'un personnage ami -> 2 menaces sur le complot principal",
       "« Confused - Place 2 threat on the main scheme »",
       [HEROS, "Puzzle.Reveal('sz012')", "Puzzle.Confuse('sz001a')"], ["Puzzle.Confuse('sz001a')"],
       {"menace": [[COMPLOT, 2]], "degats_identite": 0}, main_exclusive=["01090"], accepter_choix=True),
    _c("sz012 Entropic Subversion : CONTRE-CAS, la carte Sonne d'un ENNEMI (Rhino) defaussee ne declenche rien",
       "« from a FRIENDLY character » : un ennemi n'est pas un personnage ami",
       [HEROS, "Puzzle.Reveal('sz012')", f"Puzzle.Stun('{VILAIN}')"], [f"Puzzle.Stun('{VILAIN}')"],
       {"degats_identite": 0, "menace": [[COMPLOT, 0]]}, main_exclusive=["01090"], accepter_choix=True),
    _c("sz012 Entropic Subversion : CONTRE-CAS, une carte TOUGH defaussee d'un personnage ami ne declenche rien",
       "seuls les statuts Sonne et Desoriente sont vises",
       [HEROS, "Puzzle.Reveal('sz012')", "Puzzle.Tough('sz001a')"], ["Puzzle.Tough('sz001a')"],
       {"degats_identite": 0, "menace": [[COMPLOT, 0]]}, main_exclusive=["01090"], accepter_choix=True),

    # ============================================================ sz013 Biosynthetic Sting
    _c("sz013 Biosynthetic Sting : When Revealed, 1 degat au joueur et il est sonne",
       "« Take 1 damage. You are stunned »", [HEROS], ["Puzzle.Reveal('sz013')"],
       {"degats_identite": 1, "statuts": [["sz001a", "Stunned"]]}, main_exclusive=["01090"]),
    _c("sz013 Biosynthetic Sting : Boost, la carte est REVELEE pendant l'attaque (1 degat + sonne en plus des 2 de Rhino)",
       "« [star] Boost: Reveal this card » : Rhino (ATQ 2) attaque le heros incline, la carte de boost se revele",
       [HEROS, "Puzzle.Exhaust('sz001a')", "Puzzle.GiveFacedownBoost('01094', 'sz013')"], ["Puzzle.EnemyAttacks('01094', 'sz001a')"],
       {"degats_identite": 3, "statuts": [["sz001a", "Stunned"]]}, main_exclusive=["01090"], accepter_choix=True),
    _c("sz013 Biosynthetic Sting : TEMOIN du Boost, meme attaque avec une carte sans effet de boost (Armored Rhino Suit) -> 2 degats, pas sonne",
       "sans la carte, aucun degat supplementaire ni statut",
       [HEROS, "Puzzle.Exhaust('sz001a')", "Puzzle.GiveFacedownBoost('01094', '01098')"], ["Puzzle.EnemyAttacks('01094', 'sz001a')"],
       {"degats_identite": 2, "statuts_absents": [["sz001a", "Stunned"]]}, main_exclusive=["01090"], accepter_choix=True),

    # ============================================================ sz014 Corrupting Revelation
    _c("sz014 Corrupting Revelation : When Revealed, le joueur est desoriente et Entropic Subversion est trouvee puis revelee",
       "« You are confused. Find Entropic Subversion and reveal it » : la manigance est dans le deck rencontre",
       [HEROS, "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01098', 'sz012', '01098')"], ["Puzzle.Reveal('sz014')"],
       {"statuts": [["sz001a", "Confused"]], "en_jeu": ["sz012"], "menace": [["sz012", 3]]}, sans_deck_neutre=True, main_exclusive=["01090"], accepter_choix=True),
    _c("sz014 Corrupting Revelation : Entropic Subversion DEJA en jeu -> 3 menaces posees dessus (3 + 3 = 6), personne n'est cherche",
       "« If Entropic Subversion is already in play, place 3 threat on it »",
       [HEROS, "Puzzle.Reveal('sz012')"], ["Puzzle.Reveal('sz014')"],
       {"statuts": [["sz001a", "Confused"]], "menace": [["sz012", 6]]}, main_exclusive=["01090"], accepter_choix=True),

    # ============================================================ sz015 Power Couple
    _c("sz015 Power Couple : Team-Up, Smasher et Cannonball INCLINES se redressent",
       "« Ready Smasher and Cannonball »", [HEROS, "Puzzle.Exhaust('sz001a')"] + en_jeu("sz002") + ["Puzzle.Exhaust('sz002')"], [],
       {"pret": ["sz001a", "sz002"], "defausse": ["sz015"]}, **joue("sz015", ressource="01088", main_exclusive=["sz015", "01088", "01089"])),
    _c("sz015 Power Couple : Smasher ne peut plus prendre de degats jusqu'a la fin du round (3 degats directs APRES la carte : 0)",
       "« They cannot take damage until the end of the round » : `declencher_apres` (les degats arrivent une fois la carte jouee)",
       [HEROS] + en_jeu("sz002"), [],
       {"degats_identite": 0}, declencher_apres=["Puzzle.Damage('sz001a', 3)"], **joue("sz015", ressource="01088", main_exclusive=["sz015", "01088", "01089"])),
    _c("sz015 Power Couple : Cannonball non plus (2 degats directs APRES la carte : 0)",
       "les DEUX personnages sont protegees", [HEROS] + en_jeu("sz002"), [],
       {"degats": [["sz002", 0]]}, declencher_apres=["Puzzle.Damage('sz002', 2)"], **joue("sz015", ressource="01088", main_exclusive=["sz015", "01088", "01089"])),
    _c("sz015 Power Couple : CONTRE-CAS, un AUTRE allie (Black Cat) prend ses degats (1 degat : 1)",
       "la protection ne vaut que pour les deux cibles du Team-Up", [HEROS] + en_jeu("sz002", "01002"), [],
       {"degats": [["01002", 1]]}, declencher_apres=["Puzzle.Damage('01002', 1)"], **joue("sz015", ressource="01088", main_exclusive=["sz015", "01088", "01089"])),
    _c("sz015 Power Couple : TEMOIN, sans la carte Smasher prend ses 3 degats",
       "meme montage sans Power Couple", [HEROS] + en_jeu("sz002"), ["Puzzle.Damage('sz001a', 3)"],
       {"degats_identite": 3}, main_exclusive=["01090"]),
    _c("sz015 Power Couple : CONTRE-CAS, sans Cannonball en jeu le Team-Up n'est pas jouable (la carte reste en main)",
       "« Team-Up (Cannonball and Smasher) » : les deux personnages doivent etre en jeu", [HEROS], [],
       {"sz_main": ["sz015"]}, **joue("sz015", ressource="01088", main_exclusive=["sz015", "01088", "01089"])),
]


VERIFICATIONS = r'''
def sz_etat(monde, aides):
    """Cles propres : `sz_stats` ({attribut: valeur} de l'identite), `sz_main` (card_id presents en main), `sz_deck_rencontre`
    (taille exacte du deck rencontre) ; le reste va a etat_attendu."""
    from game.operate.worlds import Worlds
    cas = aides["cas"]
    attendu = cas.get("attendu") or {}
    soucis = []
    joueur = monde.players[0]
    identite = aides["identite"](monde)
    ids = lambda faces: [getattr(f.paper, "card_id", None) for f in faces]
    for nom, valeur in (attendu.get("sz_stats") or {}).items():
        courant = getattr(identite, nom, None)
        if courant != valeur:
            soucis.append(f"{nom} = {courant} (attendu {valeur})")
    if "sz_deck_rencontre" in attendu:
        taille = len(Worlds.GetEncounterDeckCards(monde))
        if taille != attendu["sz_deck_rencontre"]:
            soucis.append(f"deck rencontre = {taille} carte(s) (attendu {attendu['sz_deck_rencontre']})")
    main = ids(joueur.hand_cards.Get())
    for c in attendu.get("sz_main") or []:
        if c not in main:
            soucis.append(f"{c} absente de la main {sorted(main)}")
    propres = ("sz_stats", "sz_deck_rencontre", "sz_main")
    reste = {k: v for k, v in attendu.items() if k not in propres}
    copie = dict(aides); copie["cas"] = dict(cas); copie["cas"]["attendu"] = reste
    ok, message = etat_attendu(monde, copie)
    if not ok:
        soucis.append(message)
    if soucis:
        try:
            vus = []
            for objet in monde.object_manager.card_dict.values():
                face = getattr(objet, "face", None) or objet
                if getattr(face, "IsInPlay", None) and face.IsInPlay():
                    vus.append(f"{getattr(face.paper, 'card_id', '?')}({getattr(face, 'sustained', '')})")
            soucis.append("[en jeu : " + " ".join(vus) + "]")
        except Exception as e:
            soucis.append(f"[dump impossible : {e}]")
        return False, " ; ".join(soucis)
    return True, message
'''
