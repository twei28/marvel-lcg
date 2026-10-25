# Cas test_capacites PREDATOR, partie 3 : alter-ego, obligation, set nemesis, ressources, Team-Up, set nemesis alternatif.
# Rappels de montage : voir predator.py. Un deck (CreateEncounterDeck / CreatePlayerDeck) liste ses cartes du DESSOUS vers le DESSUS :
# la derniere carte citee est celle du dessus.
SC = "rhino"
HEROS = "Puzzle.ChangeToFace('pd001b', 'pd001a')"
SANS_DECK = "Puzzle.EmptyPlayerDeck()"
SANS_BOOST = ["Puzzle.EmptyEncounterDeck()",
              "Puzzle.CreateEncounterDeck('01105', '01105', '01105', '01105', '01105', '01105', '01105', '01105')"]
COMPLOT = "01097b"
VILAIN = "01094"
INFRA = "pd002"
SHOCKER = "01103"
RUNNER = "01121"
REINE = "pd017"
WOLVERINE = "32041"
SPIDER = "13019"


def en_jeu(*ids):
    return [f"Puzzle.PutIntoPlay('{i}', under_control=True)" for i in ids]


def _c(nom, pourquoi, mise, declencher, attendu, **cle):
    if not cle.pop("avec_boost", False):
        mise = SANS_BOOST + list(mise)
    cas = {"nom": "[pd] " + nom, "pourquoi": pourquoi, "scenario": cle.pop("scenario", SC),
           "heros": cle.pop("heros", "predator"), "mise_en_place": mise, "declencher": declencher,
           "verifier": cle.pop("verifier", "etat_attendu"), "attendu": attendu}
    cas.update(cle)
    return cas


CAS = [
    # ============================================================ pd001b Yd'Nar : Future Trophy
    _c("pd001b Future Trophy : defausse du deck jusqu'a une AMELIORATION, qui revient en main (Wrist Blades sous 2 Genius) ; 1 carte de fond reste",
       "« Discard cards from the top of your deck until you discard an upgrade, then add that card to your hand »",
       ["Puzzle.EmptyHand()", SANS_DECK, "Puzzle.CreatePlayerDeck('01090', 'pd012', '01089', '01089')"],
       ["Puzzle.Action('pd001b', 'AlterEgoAction')"],
       {"en_main": ["pd012"], "taille_main": 1, "taille_deck_joueur": 1}),
    _c("pd001b Future Trophy : « Limit once per round » -> une SECONDE Action dans le round ne fait rien (une seule amelioration en main)",
       "temoin d'epuisement : deux declenchements, la 2e amelioration reste dans le deck",
       ["Puzzle.EmptyHand()", SANS_DECK, "Puzzle.CreatePlayerDeck('01090', 'pd013', '01089', 'pd012', '01089')"], [],
       {"taille_main": 1, "taille_deck_joueur": 3},
       declencher_tolerant=["Puzzle.Action('pd001b', 'AlterEgoAction')", "Puzzle.Action('pd001b', 'AlterEgoAction')"]),
    _c("pd001b Future Trophy : « Action » d'ALTER-EGO -> absente en forme HEROS (aucune carte en main)",
       "contre-cas : seule la face alter-ego offre l'Action",
       [HEROS, "Puzzle.EmptyHand()", SANS_DECK, "Puzzle.CreatePlayerDeck('01090', 'pd012', '01089')"], [],
       {"taille_main": 0},
       declencher_tolerant=["Puzzle.Action('pd001a', 'AlterEgoAction')"]),
    # ============================================================ pd015 Exposed Target
    _c("pd015 Exposed Target : forme alter-ego, branche 1 -> Yd'Nar s'incline et l'obligation est RETIREE de la partie",
       "« Exhaust Yd'Nar -> remove Exposed Target from the game »",
       [], ["Puzzle.Reveal('pd015')"], {"exhausted": ["pd001b"], "hors_jeu": ["pd015"]},
       main_exclusive=["01090"], preferer_option="Exhaust Yd'Nar"),
    _c("pd015 Exposed Target : branche 2 -> la carte Cloaked ET une amelioration TECH (Wrist Blades) sont defaussees, l'obligation aussi (pas de surge)",
       "« Discard each cloaked status card from your identity and 1 TECH upgrade you control »",
       [HEROS, "Puzzle.Cloak('pd001a')", "Puzzle.PutIntoPlay('pd012', under_control=True)",
        "Puzzle.EmptyEncounterDeck()", f"Puzzle.CreateEncounterDeck('01105', '{SHOCKER}')"], ["Puzzle.Reveal('pd015')"],
       {"statuts_absents": [["pd001b", "Cloaked"]], "hors_jeu": ["pd015", "pd012"], "dans_deck_rencontre": [SHOCKER]},
       main_exclusive=["01090"], avec_boost=True, preferer_option="Discard each cloaked"),
    _c("pd015 Exposed Target : branche 2 SANS Cloaked ni TECH -> « this card gains surge » : la carte du dessus (Shocker) est revelee, l'obligation defaussee",
       "« If no cards were discarded this way, this card gains surge. Discard this obligation »",
       [HEROS, "Puzzle.EmptyEncounterDeck()", f"Puzzle.CreateEncounterDeck('01105', '{SHOCKER}')"], ["Puzzle.Reveal('pd015')"],
       {"carte_du_surge": SHOCKER, "en_jeu": [SHOCKER], "hors_jeu": ["pd015"]},
       main_exclusive=["01090"], avec_boost=True, preferer_option="Discard each cloaked"),
    # ============================================================ pd016 Xenomorph's Prey
    _c("pd016 Xenomorph's Prey : revelee, elle porte 3 menaces (3 par joueur, 1 joueur) et aucune de plus sans carte d'etat",
       "StartingThreat « 3 par joueur » ; When Revealed : +1 par carte d'etat en jeu (zero ici)",
       [HEROS], ["Puzzle.Reveal('pd016')"], {"menace": [["pd016", 3]]}, main_exclusive=["01090"]),
    _c("pd016 Xenomorph's Prey : tant qu'elle est en jeu, Predator ne peut PAS recevoir de carte Cloaked",
       "« While this card is in play, Predator cannot gain cloaked status cards »",
       [HEROS, "Puzzle.PutIntoPlay('pd016')"], ["Puzzle.Cloak('pd001a')"], {"statuts_absents": [["pd001a", "Cloaked"]]},
       main_exclusive=["01090"]),
    _c("pd016 Xenomorph's Prey : une carte Cloaked DEJA posee RESTE quand la manigance arrive (« cannot gain », pas « loses »)",
       "contre-cas : la regle empeche de GAGNER, elle ne retire rien",
       [HEROS, "Puzzle.Cloak('pd001a')"], ["Puzzle.PutIntoPlay('pd016')"], {"statuts": [["pd001a", "Cloaked"]]},
       main_exclusive=["01090"]),
    _c("pd016 Xenomorph's Prey : SANS la manigance en jeu, Predator recoit bien sa carte Cloaked (temoin de la regle)",
       "contre-cas : la regle ne vaut que tant que la carte est en jeu",
       [HEROS], ["Puzzle.Cloak('pd001a')"], {"statuts": [["pd001a", "Cloaked"]]}, main_exclusive=["01090"]),
    _c("pd016 Xenomorph's Prey : When Revealed -> 1 menace de plus par carte d'etat EN JEU (Stunned sur le vilain + Tough sur un sbire = 2) : 3 + 2 = 5",
       "« Place 1 additional threat here for each status card in play »",
       [HEROS, f"Puzzle.PutIntoPlay('{SHOCKER}')", f"Puzzle.Tough('{SHOCKER}')", f"Puzzle.Stun('{VILAIN}')"],
       ["Puzzle.Reveal('pd016')"], {"menace": [["pd016", 5]]}, main_exclusive=["01090"]),
    # ============================================================ pd017 Xenomorph Queen
    _c("pd017 Xenomorph Queen : Toughness -> entre en jeu avec une carte Tough",
       "« Toughness. »",
       [HEROS, f"Puzzle.PutIntoPlay('{REINE}')"], [], {"statuts": [[REINE, "Tough"]]}, main_exclusive=["01090"]),
    _c("pd017 Xenomorph Queen : valeurs imprimees PV 9, ELITE XENOMORPH",
       "nombres texte <-> code (scan) : SCH 1 / ATK 3 / PV 9",
       [HEROS, f"Puzzle.PutIntoPlay('{REINE}')"], [], {"pv_max": [[REINE, 9]], "traits_de": [[REINE, "ELITE"], [REINE, "XENOMORPH"]]},
       main_exclusive=["01090"]),
    _c("pd017 Xenomorph Queen : ses attaques sont PERFORANTES -> elles defaussent la carte Tough de Predator ET le blessent (ATQ 3 - DEF 2 = 1)",
       "« Xenomorph Queen's attacks gain piercing and overkill »",
       [HEROS, "Puzzle.Tough('pd001a')", f"Puzzle.PutIntoPlay('{REINE}')"], [f"Puzzle.Attack('{REINE}')"],
       {"degats_identite": 1, "statuts_absents": [["pd001a", "Tough"]]}, main_exclusive=["01090"]),
    _c("pd017 Xenomorph Queen : ses attaques ont l'OUTREPASSEMENT -> contre un sbire de 2 PV (Weapons Runner), l'exces de 1 va a Predator",
       "« ... gain piercing and OVERKILL » : brique `Enemy.AttackCharacter` (un ennemi attaque un ennemi), exces designe par `overkill_to`",
       [HEROS, f"Puzzle.PutIntoPlay('{RUNNER}')", f"Puzzle.PutIntoPlay('{REINE}')"],
       [f"Puzzle.EnemyAttacks('{REINE}', '{RUNNER}', overkill_to='pd001a')"], {"hors_jeu": [RUNNER], "degats_identite": 1},
       main_exclusive=["01090"]),
    # ============================================================ pd018 Xenomorph Drone
    _c("pd018 Xenomorph Drone : valeurs imprimees PV 3, XENOMORPH, Guard",
       "nombres texte <-> code (scan) : SCH 1 / ATK 2 / PV 3",
       [HEROS, "Puzzle.PutIntoPlay('pd018')"], [], {"pv_max": [["pd018", 3]], "traits_de": [["pd018", "XENOMORPH"]]},
       main_exclusive=["01090"]),
    _c("pd018 Xenomorph Drone : Forced Response, SEUL sbire engage -> 1 carte rencontre face cachee (revelee ensuite : le Shocker du dessus arrive)",
       "« After Drone engages you, if there are no other minions engaged with you, deal yourself 1 facedown encounter card »",
       [HEROS, "Puzzle.EmptyEncounterDeck()", f"Puzzle.CreateEncounterDeck('01105', '{SHOCKER}')"],
       ["Puzzle.PutIntoPlay('pd018')", "Puzzle.RevealDealtCards()"], {"en_jeu": [SHOCKER]},
       main_exclusive=["01090"], avec_boost=True),
    _c("pd018 Xenomorph Drone : un AUTRE sbire est deja engage -> aucune carte distribuee (le Shocker reste dans le deck)",
       "contre-cas : « if there are no OTHER minions engaged with you »",
       [HEROS, f"Puzzle.PutIntoPlay('{RUNNER}')", "Puzzle.EmptyEncounterDeck()", f"Puzzle.CreateEncounterDeck('01105', '{SHOCKER}')"],
       ["Puzzle.PutIntoPlay('pd018')", "Puzzle.RevealDealtCards()"], {"dans_deck_rencontre": [SHOCKER]},
       main_exclusive=["01090"], avec_boost=True),
    _c("pd018 Xenomorph Drone : [star] Boost -> il entre en jeu engage avec le joueur",
       "« [star] Boost: Put Xenomorph Drone into play engaged with you »",
       [HEROS], ["Puzzle.Boost('pd018')"], {"en_jeu": ["pd018"]}, main_exclusive=["01090"]),
    # ============================================================ pd019 Hunted By the Hive
    _c("pd019 Hunted By the Hive : Reine ABSENTE (mise de cote) -> trouvee et mise en jeu engagee, SANS attaquer (Predator reste pret)",
       "« Xenomorph Queen attacks you. If it's not in play, find Xenomorph Queen and put it into play engaged with you » (DECISION UTILISATEUR 25/10 : elle n'attaque pas apres son arrivee)",
       [HEROS], ["Puzzle.Reveal('pd019')"], {"en_jeu": [REINE], "pret": ["pd001a"]}, main_exclusive=["01090"]),
    _c("pd019 Hunted By the Hive : Reine DEJA en jeu -> elle attaque (elle ne revient pas)",
       "« Xenomorph Queen attacks you »",
       [HEROS, f"Puzzle.PutIntoPlay('{REINE}')"], ["Puzzle.Reveal('pd019')"], {"en_jeu": [REINE], "exhausted": ["pd001a"]},
       main_exclusive=["01090"]),
    _c("pd019 Hunted By the Hive : Reine INTROUVABLE -> rien ne se passe (Predator reste pret)",
       "contre-cas : ni en jeu, ni a trouver",
       [HEROS, "Puzzle.RemoveNemesisAside()"], ["Puzzle.Reveal('pd019')"], {"pret": ["pd001a"]}, main_exclusive=["01090"]),
    # ============================================================ pd020 Acid Blood
    _c("pd020 Acid Blood : When Revealed -> la Reine est trouvee, mise en jeu engagee et l'attachement s'accroche a elle",
       "« Find the Xenomorph Queen and put it into play engaged with you and attach this card to it »",
       [HEROS], ["Puzzle.Reveal('pd020')"], {"accroche_a": [["pd020", REINE]], "en_jeu": [REINE]}, main_exclusive=["01090"]),
    _c("pd020 Acid Blood : la Reine est DEJA en jeu -> l'attachement s'accroche a elle",
       "la carte ne peut pas la remettre en jeu mais doit quand meme s'attacher",
       [HEROS, f"Puzzle.PutIntoPlay('{REINE}')"], ["Puzzle.Reveal('pd020')"], {"accroche_a": [["pd020", REINE]]},
       main_exclusive=["01090"]),
    _c("pd020 Acid Blood : « +1 ATK » -> la Reine frappe a 4 (ATQ 3 + 1 - DEF 2 = 2 degats)",
       "bonus d'ATQ imprime (icone) : +1 pour le porteur",
       [HEROS, "Puzzle.Reveal('pd020')"], [f"Puzzle.Attack('{REINE}')"], {"degats_identite": 2}, main_exclusive=["01090"]),
    _c("pd020 Acid Blood : « retaliate 1 » -> Predator attaque la Reine et subit 1 degat de riposte",
       "« Attached minion gains retaliate 1 »",
       [HEROS, "Puzzle.Reveal('pd020')"], ["Puzzle.Attack('pd001a')"], {"degats_identite": 1},
       main_exclusive=["01090"], cibles=[REINE]),
    # ============================================================ pd021-pd023 ressources de base
    _c("pd021 Energy : deux ressources energie (YY) paient Ghost Protocol (cout 1) -- Max 1 par deck",
       "ressource de base a l'art de Predator",
       [HEROS, f"Puzzle.SetThreat('{COMPLOT}', 6)"], [], {"menace": [[COMPLOT, 4]]},
       main_exclusive=["pd004", "pd021"], jouer=["pd004"], payer_avec=["pd021"], cibles=[COMPLOT]),
    _c("pd022 Genius : deux ressources mentales (BB) paient Shadow Counter (cout 1)",
       "ressource de base a l'art de Predator",
       [HEROS], ["Puzzle.Damage('pd001a', 5)"], {"degats_identite": 2, "statuts": [["pd001a", "Cloaked"]]},
       main_exclusive=["pd006", "pd022"], payer_avec=["pd022"]),
    _c("pd023 Strength : deux ressources physiques (RR) paient Spine Rip (cout 3) avec une Energy",
       "ressource de base a l'art de Predator",
       [HEROS], [], {"degats": [[VILAIN, 7]]},
       main_exclusive=["pd005", "pd023", "01088"], jouer=["pd005"], payer_avec=["pd023", "01088"], cibles=[VILAIN]),
    # ============================================================ pd024 Razor Hunt
    _c("pd024 Razor Hunt : Team-Up (Wolverine et Predator en jeu) -> 1 degat a CHACUN d'eux et 3 + 3 degats a l'ennemi",
       "« Deal 1 damage each to Wolverine and Predator. Deal 3 damage to an enemy. Deal 3 damage to an enemy. »",
       [HEROS, *en_jeu(WOLVERINE)], [], {"degats": [[VILAIN, 6], [WOLVERINE, 1]], "degats_identite": 1},
       main_exclusive=["pd024", "01090"], jouer=["pd024"], payer_avec=["01090"], cibles=[VILAIN, VILAIN]),
    _c("pd024 Razor Hunt : SANS Wolverine en jeu -> la carte n'est pas jouable (reste en main, rien ne bouge)",
       "Team-Up : les DEUX personnages doivent etre en jeu",
       [HEROS], [], {"en_main": ["pd024"], "degats": [[VILAIN, 0]]},
       main_exclusive=["pd024", "01090"], jouer=["pd024"], payer_avec=["01090"], cibles=[VILAIN, VILAIN]),
    # ============================================================ pd025 Infrared Web
    _c("pd025 Infrared Web : Team-Up (Spider-Man et Predator) -> evite 3 degats d'une attaque et inflige 3 degats a un ennemi",
       "« When an enemy attack would deal damage to you, prevent 3 of that damage. Deal 3 damage to an enemy »",
       [HEROS, *en_jeu(SPIDER), "Puzzle.PutIntoPlay('01102')"], ["Puzzle.Attack('01102')"],
       {"degats_identite": 0, "degats": [[VILAIN, 3]]},
       main_exclusive=["pd025", "01088"], payer_avec=["01088"], cibles=[VILAIN]),
    _c("pd025 Infrared Web : SANS Spider-Man en jeu -> la carte n'est pas jouee (Predator encaisse l'attaque, le vilain n'est pas touche)",
       "Team-Up : les DEUX personnages doivent etre en jeu",
       [HEROS, "Puzzle.PutIntoPlay('01102')"], ["Puzzle.Attack('01102')"],
       {"degats_identite": 1, "degats": [[VILAIN, 0]], "en_main": ["pd025"]},
       main_exclusive=["pd025", "01088"], payer_avec=["01088"], cibles=[VILAIN]),
]
