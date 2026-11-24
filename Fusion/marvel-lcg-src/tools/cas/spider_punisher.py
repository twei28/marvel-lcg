# Cas test_capacites du pack SPIDER-PUNISHER (T-Wrecks, prefixe `sq`) : noms prefixes « [sq] » puis le card_id
# (substituer_pack.py filtre dessus).
#
# Rappels de montage :
#  - le deck spider_punisher demarre en ALTER EGO (sq001b Peter Parker) ; `Puzzle.ChangeToFace('sq001b', 'sq001a')`
#    passe en HEROS sans declencher de capacite ;
#  - Rhino 01094 est le vilain (14 PV), 01097b son complot principal ; 01110 Hydra Bomber (2 PV, sans Guard) est le sbire
#    des cas ; Klaw (scenario `klaw`, 01113, 12 PV) + 01119 Solid-Sound Body donnent un ennemi RETALIATE 1 ;
#  - ressources : 01088 Energy = YY, 01089 Genius = BB, 01090 Strength = RR ;
#  - `Puzzle.Action(carte, 'HeroAction')` PAIE le cout de la capacite avec la main : les couts « Spend a [x] resource »
#    exigent donc la bonne ressource en main (01089 = BB, 01088 = YY, 01090 = RR) et `payer_avec` ;
#  - Web-Sling lit la fin de phase JOUEUR : `Puzzle.ReadyAtEndOfPlayerPhase()` (nouveau) rejoue l'etape « ready » ;
#  - fillers de deck : 01088 (aucun cout), 01022 (2), 01025 (3).
SC = "rhino"
HEROS = "Puzzle.ChangeToFace('sq001b', 'sq001a')"
CIVIL = "Puzzle.ChangeToFace('sq001a', 'sq001b')"
SANS_BOOST = ["Puzzle.EmptyEncounterDeck()",
              "Puzzle.CreateEncounterDeck('01098', '01098', '01098', '01098', '01098', '01098', '01098', '01098')"]
COMPLOT = "01097b"
VILAIN = "01094"
SBIRE = "01110"
WEBS = ["sq008", "sq009", "sq010", "sq011"]          # les quatre WEB-SHOOTER (TECH, WEAPON)


def en_jeu(*ids):
    return [f"Puzzle.PutIntoPlay('{i}', under_control=True)" for i in ids]


def _c(nom, pourquoi, mise, declencher, attendu, **cle):
    mise = SANS_BOOST + list(mise)
    cas = {"nom": "[sq] " + nom, "pourquoi": pourquoi, "scenario": cle.pop("scenario", SC),
           "heros": cle.pop("heros", "spider_punisher"), "mise_en_place": mise, "declencher": declencher,
           "verifier": cle.pop("verifier", "sq_etat"), "attendu": attendu}
    cas.setdefault("regles", ["v16_all", "v18_all"])
    cas.update(cle)
    return cas


CAS = [
    # ============================================================ sq001a Spider-Punisher : valeurs imprimees
    _c("sq001a Spider-Punisher : valeurs imprimees PV 11, THW 2, ATK 2, DEF 2, main 5, EARTH-71928 WEB-WARRIOR",
       "nombres texte <-> code (scan) : HAND SIZE 5 / HIT POINTS 11",
       [HEROS], [], {"pv_max": [["sq001a", 11]], "traits": ["EARTH-71928", "WEB-WARRIOR"],
                     "sq_stats": {"attack": 2, "thwart": 2, "defense": 2, "hand_size": 5}}, main_exclusive=["01088"]),
    _c("sq001b Peter Parker : valeurs imprimees PV 11, REC 3, main 6, GENIUS",
       "nombres texte <-> code (scan) : HAND SIZE 6 / HIT POINTS 11 / REC 3",
       [], [], {"pv_max": [["sq001b", 11]], "traits": ["GENIUS"], "sq_stats": {"recover": 3, "hand_size": 6}},
       main_exclusive=["01088"]),

    # ============================================================ sq001a Web-Sling
    _c("sq001a Web-Sling : 2 ameliorations redressees en fin de phase -> 1 degat a Rhino",
       "« for each 2 upgrades you readied this way, deal 1 damage to an enemy »",
       [HEROS] + en_jeu("sq008", "sq009") + ["Puzzle.Exhaust('sq008', 'sq009')"], ["Puzzle.ReadyAtEndOfPlayerPhase()"],
       {"degats": [[VILAIN, 1]], "pret": ["sq008", "sq009"]}, main_exclusive=["01088"], cibles=[VILAIN],
       preferer_option="Deal 1 damage"),
    _c("sq001a Web-Sling : 4 ameliorations redressees -> 2 degats (une fois par paire)",
       "« for each 2 upgrades » : 4 -> deux fois",
       [HEROS] + en_jeu(*WEBS) + [f"Puzzle.Exhaust('{i}')" for i in WEBS], ["Puzzle.ReadyAtEndOfPlayerPhase()"],
       {"degats": [[VILAIN, 2]]}, main_exclusive=["01088"], cibles=[VILAIN], preferer_option="Deal 1 damage"),
    _c("sq001a Web-Sling : CONTRE-CAS une seule amelioration redressee -> aucun degat",
       "1 amelioration ne fait pas une paire",
       [HEROS] + en_jeu("sq008") + ["Puzzle.Exhaust('sq008')"], ["Puzzle.ReadyAtEndOfPlayerPhase()"],
       {"degats": [[VILAIN, 0]]}, main_exclusive=["01088"], cibles=[VILAIN], preferer_option="Deal 1 damage"),
    _c("sq001a Web-Sling : branche « remove 1 threat from a scheme » (3 -> 2)",
       "« or remove 1 threat from a scheme »",
       [HEROS, f"Puzzle.SetThreat('{COMPLOT}', 3)"] + en_jeu("sq008", "sq009") + ["Puzzle.Exhaust('sq008', 'sq009')"],
       ["Puzzle.ReadyAtEndOfPlayerPhase()"], {"menace": [[COMPLOT, 2]]}, main_exclusive=["01088"],
       cibles=[COMPLOT], preferer_option="Remove 1 threat"),
    _c("sq001a Web-Sling : TEMOIN D'EPUISEMENT, 8 ameliorations redressees (4 paires) -> 3 fois seulement",
       "« (Limit 3 times per round.) » : 4 paires, 3 degats a Rhino",
       [HEROS] + en_jeu("sq005", "sq006", "sq008", "sq009", "sq010", "sq011", "sq012", "01027")
       + [f"Puzzle.Exhaust('{i}')" for i in ("sq005", "sq006", "sq008", "sq009", "sq010", "sq011", "sq012", "01027")],
       ["Puzzle.ReadyAtEndOfPlayerPhase()"], {"degats": [[VILAIN, 3]]}, main_exclusive=["01088"], cibles=[VILAIN],
       preferer_option="Deal 1 damage"),
    _c("sq001a Web-Sling : CONTRE-CAS en ALTER EGO, rien ne part",
       "capacite imprimee sur la face HEROS seulement",
       en_jeu("sq008", "sq009") + ["Puzzle.Exhaust('sq008', 'sq009')"], ["Puzzle.ReadyAtEndOfPlayerPhase()"],
       {"degats": [[VILAIN, 0]]}, main_exclusive=["01088"], cibles=[VILAIN], preferer_option="Deal 1 damage"),
    _c("sq001a Web-Sling : CONTRE-CAS une redressement HORS fin de phase (Swing and Reload) ne compte pas",
       "« After you ready your cards at the end of the player phase » : seul le redressement de fin de phase compte",
       [HEROS] + en_jeu("sq012", "sq008", "sq009") + ["Puzzle.Exhaust('sq008', 'sq009')", "Puzzle.Ready('sq008')", "Puzzle.Ready('sq009')"],
       [], {"degats": [[VILAIN, 0]]}, main_exclusive=["01088"], cibles=[VILAIN], preferer_option="Deal 1 damage"),

    # ============================================================ sq001a : ranged des attaques WEB-SHOOTER
    _c("sq001a [star] ranged : attaque de High Explosive Rounds contre un ennemi RETALIATE -> aucune riposte",
       "« Spider-Punisher's attacks from WEB-SHOOTER upgrades gain ranged » : Klaw avec Solid-Sound Body (retaliate 1)",
       [HEROS, "Puzzle.PutIntoPlay('01119')"] + en_jeu("sq010"), ["Puzzle.Action('sq010', 'HeroAction')"],
       {"degats_identite": 0}, main_exclusive=["01090"], payer_avec=["01090"], cibles=["01113"], scenario="klaw"),
    _c("sq001a [star] ranged : TEMOIN, attaque de BASE contre le meme ennemi RETALIATE -> 1 degat de riposte",
       "l'attaque de base ne vient pas d'une amelioration WEB-SHOOTER : elle n'est pas a portee",
       [HEROS, "Puzzle.PutIntoPlay('01119')"], ["Puzzle.Attack('sq001a')"],
       {"degats_identite": 1}, main_exclusive=["01088"], cibles=["01113"], scenario="klaw"),

    # ============================================================ sq001b Vengeance
    _c("sq001b Vengeance : cherche Armor-Piercing Rounds (WEB-SHOOTER) dans le deck -> en main",
       "« Search your deck and discard pile for a WEB-SHOOTER upgrade and add it to your hand »",
       ["Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01088', 'sq008')"], ["Puzzle.Action('sq001b', 'Action')"],
       {"en_main": ["sq008"]}, main_exclusive=["01088"], accepter_choix=True),
    _c("sq001b Vengeance : cherche aussi dans la DEFAUSSE (EMP Rounds)",
       "« deck AND discard pile »",
       ["Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01088')", "Puzzle.CreatePlayerDiscardPile('sq009')"], ["Puzzle.Action('sq001b', 'Action')"],
       {"en_main": ["sq009"]}, main_exclusive=["01088"], accepter_choix=True),
    _c("sq001b Vengeance : CONTRE-CAS une amelioration qui n'est PAS WEB-SHOOTER (Neighborhood Watch) n'est pas cherchee",
       "le filtre est le trait WEB-SHOOTER",
       ["Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01088', 'sq005')"], ["Puzzle.Action('sq001b', 'Action')"],
       {"absent_main": ["sq005"]}, main_exclusive=["01088"], accepter_choix=True),
    _c("sq001b Vengeance : TEMOIN D'EPUISEMENT, apres UNE Action la capacite n'est plus offerte (nombre = 0)",
       "« (Limit once per phase.) » : deux WEB-SHOOTER dans le deck, mais la seconde Action n'est plus proposee",
       ["Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01088', 'sq009', 'sq008')"], ["Puzzle.Action('sq001b', 'Action')"],
       {"carte": "sq001b", "type": "Action", "nombre": 0}, main_exclusive=["01088"], accepter_choix=True,
       verifier="actions_disponibles"),
    _c("sq001b Vengeance : TEMOIN, avant toute Action la capacite est offerte (nombre = 1)",
       "contre-temoin du precedent : sans limite atteinte, l'Action est proposee",
       ["Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01088', 'sq009', 'sq008')"], [],
       {"carte": "sq001b", "type": "Action", "nombre": 1}, main_exclusive=["01088"], verifier="actions_disponibles"),

    # ============================================================ sq002 Enhanced Combat Sense
    _c("sq002 Enhanced Combat Sense : revelation d'une carte rencontre -> elle est defaussee (payee avec 3 ressources)",
       "« Hero Interrupt: When an encounter card is revealed from the encounter deck, discard it »",
       [HEROS], ["Puzzle.Reveal('01103')"],
       {"defausse_rencontre": ["01103"]}, main_exclusive=["sq002", "01090", "01088"], jouer=["sq002"],
       payer_avec=["01090", "01088"], cibles=[VILAIN]),
    _c("sq002 Enhanced Combat Sense : [star] 3 ameliorations inclinees pour la payer -> 3 resources, puis 3 degats/menace",
       "« exhaust any number of WEAPON or TECH upgrades ... to generate that many resources » ; « for each upgrade you exhausted »",
       [HEROS] + en_jeu("sq008", "sq009", "sq010"), ["Puzzle.Reveal('01103')"],
       {"defausse_rencontre": ["01103"], "exhausted": ["sq008", "sq009", "sq010"], "degats": [[VILAIN, 3]]},
       main_exclusive=["sq002"], jouer=["sq002"], surpayer=True, cibles=[VILAIN], preferer_option="Deal 1 damage"),

    # ============================================================ sq003 Point Blank
    _c("sq003 Point Blank : sans arme -> 3 degats a Rhino",
       "« Deal 3 damage to an enemy »",
       [HEROS], [], {"degats": [[VILAIN, 3]]}, main_exclusive=["sq003", "01090", "01088"], jouer=["sq003"],
       payer_avec=["01090", "01088"], cibles=[VILAIN]),
    _c("sq003 Point Blank : 2 armes inclinees -> 3 + 3 + 3 = 9 degats",
       "« You may exhaust up to 2 WEAPON upgrades ... For each exhausted this way, deal 3 damage to that enemy »",
       [HEROS] + en_jeu("sq008", "sq009"), [], {"degats": [[VILAIN, 9]], "exhausted": ["sq008", "sq009"]},
       main_exclusive=["sq003", "01090", "01088"], jouer=["sq003"], payer_avec=["01090", "01088"], cibles=[VILAIN]),
    _c("sq003 Point Blank : 3 armes -> au plus 2 inclinees (9 degats, une arme reste prete)",
       "« up to 2 »",
       [HEROS] + en_jeu("sq008", "sq009", "sq010"), [], {"degats": [[VILAIN, 9]]},
       main_exclusive=["sq003", "01090", "01088"], jouer=["sq003"], payer_avec=["01090", "01088"], cibles=[VILAIN]),
    _c("sq003 Point Blank : valeurs imprimees cout 3, trait ATTACK",
       "nombres texte <-> code (scan) : cout 3",
       [HEROS], [], {"traits_main": [["sq003", ["ATTACK"]]]}, main_exclusive=["sq003"]),

    # ============================================================ sq004 Web Snatch
    _c("sq004 Web Snatch : etourdit Rhino, cherche Neighborhood Watch dans le deck -> en main",
       "« Stun an enemy -> search your deck and discard pile for an upgrade and add it to your hand »",
       [HEROS, "Puzzle.CreatePlayerDeck('01088', 'sq005')"], [], {"statuts": [[VILAIN, "Stunned"]], "en_main": ["sq005"]},
       main_exclusive=["sq004", "01088"], jouer=["sq004"], payer_avec=["01088"], cibles=[VILAIN], accepter_choix=True,
       preferer_option="Search your deck"),
    _c("sq004 Web Snatch : variante « discard an attachment from the villain's play area instead »",
       "« You may choose to discard an attachment from the villain's play area instead » (Armored Rhino Suit 01098)",
       [HEROS, "Puzzle.CreatePlayerDeck('01088', 'sq005')"] + ["Puzzle.PutIntoPlay('01098')"],
       [], {"statuts": [[VILAIN, "Stunned"]], "absent_main": ["sq005"], "defausse_rencontre": ["01098"]},
       main_exclusive=["sq004", "01088"], jouer=["sq004"], payer_avec=["01088"], cibles=[VILAIN, "01098"],
       accepter_choix=True, preferer_option="Discard an attachment"),

    # ============================================================ sq005 Neighborhood Watch
    _c("sq005 Neighborhood Watch : 2 ameliorations inclinees -> AERIAL -> redresse Spider-Punisher",
       "« You gain the AERIAL trait when 2 or more upgrades you control are exhausted. Hero Action: If you have the AERIAL trait, exhaust this card -> ready Spider-Punisher »",
       [HEROS] + en_jeu("sq005", "sq008", "sq009") + ["Puzzle.Exhaust('sq008', 'sq009', 'sq001a')"], ["Puzzle.Action('sq005', 'HeroAction')"],
       {"pret": ["sq001a"], "exhausted": ["sq005"]}, main_exclusive=["01088"], accepter_choix=True),
    _c("sq005 Neighborhood Watch : CONTRE-CAS une seule amelioration inclinee (hors Watch) -> pas AERIAL, l'Action n'est pas offerte",
       "seuil « 2 or more » : 1 amelioration inclinee ne donne pas AERIAL",
       [HEROS] + en_jeu("sq005", "sq008") + ["Puzzle.Exhaust('sq008')"], [],
       {"carte": "sq005", "type": "HeroAction", "nombre": 0}, main_exclusive=["01088"], verifier="actions_disponibles"),
    _c("sq005 Neighborhood Watch : AERIAL est un VRAI trait de l'identite quand 2 ameliorations sont inclinees (lu par n'importe quelle carte)",
       "« You gain the AERIAL trait when 2 or more upgrades you control are exhausted » : le trait est pose sur l'identite (arbitrage du 26/10/2026), "
       "pas un raccourci reserve a sq005 / sq012 ; une carte d'un autre pack qui teste AERIAL le voit",
       [HEROS] + en_jeu("sq005", "sq008", "sq009") + ["Puzzle.Exhaust('sq008', 'sq009')"], [],
       {"traits": ["AERIAL"]}, main_exclusive=["01088"]),
    _c("sq005 Neighborhood Watch : TEMOIN, une seule amelioration inclinee (hors Watch) -> l'identite n'a PAS le trait AERIAL",
       "seuil « 2 or more »", [HEROS] + en_jeu("sq005", "sq008") + ["Puzzle.Exhaust('sq008')"], [],
       {"traits_absents": ["AERIAL"]}, main_exclusive=["01088"]),
    _c("sq005 Neighborhood Watch : le trait AERIAL se PERD quand une amelioration est redressee (2 inclinees -> 1)",
       "« when 2 or more upgrades you control are EXHAUSTED » : le trait suit l'etat, il n'est pas definitif",
       [HEROS] + en_jeu("sq005", "sq008", "sq009") + ["Puzzle.Exhaust('sq008', 'sq009')"], ["Puzzle.Ready('sq008')"],
       {"traits_absents": ["AERIAL"]}, main_exclusive=["01088"]),
    _c("sq005 Neighborhood Watch : valeurs imprimees cout 1, trait CONDITION",
       "nombres texte <-> code (scan) : cout 1",
       [HEROS] + en_jeu("sq005"), [], {"traits_de": [["sq005", "CONDITION"]]}, main_exclusive=["01088"]),

    # ============================================================ sq006 With Great Firepower
    _c("sq006 With Great Firepower : Alter-Ego Action, joue Armor-Piercing Rounds (cout 2) pour 0",
       "« Exhaust this card -> play a WEAPON or TECH upgrade from your hand, reducing its cost by 2 »",
       en_jeu("sq006"), ["Puzzle.Action('sq006', 'AlterEgoAction')"], {"en_jeu": ["sq008"], "exhausted": ["sq006"]},
       main_exclusive=["sq008", "01088"], cibles=["sq008"], accepter_choix=True),
    _c("sq006 With Great Firepower : CONTRE-CAS seule une amelioration ni WEAPON ni TECH (Neighborhood Watch) en main -> l'Action n'est pas offerte",
       "le filtre est WEAPON ou TECH : aucune cible jouable, aucune action disponible",
       en_jeu("sq006"), [], {"carte": "sq006", "type": "AlterEgoAction", "nombre": 0},
       main_exclusive=["sq005", "01088"], verifier="actions_disponibles"),
    _c("sq006 With Great Firepower : valeurs imprimees cout 2",
       "nombres texte <-> code (scan)", [HEROS] + en_jeu("sq006"), [], {"en_jeu": ["sq006"]}, main_exclusive=["01088"]),

    # ============================================================ sq007 Concrete Perch
    _c("sq007 Concrete Perch : 2 ameliorations inclinees -> regarde les 2 premieres cartes rencontre et les remet",
       "« look at the top X cards of the encounter deck, and return them to the top ... in any order »",
       [HEROS, "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01098', '01110', '01103')"] + en_jeu("sq007", "sq008", "sq009"),
       ["Puzzle.Action('sq007', 'HeroAction')"], {"exhausted": ["sq007", "sq008", "sq009"], },
       main_exclusive=["01088"], accepter_choix=True),
    _c("sq007 Concrete Perch : valeurs imprimees cout 1, trait LOCATION", "nombres texte <-> code (scan)",
       [HEROS] + en_jeu("sq007"), [], {"traits_de": [["sq007", "LOCATION"]]}, main_exclusive=["01088"]),

    # ============================================================ sq008 Armor-Piercing Rounds
    _c("sq008 Armor-Piercing Rounds : 2 degats a Rhino, l'amelioration s'incline",
       "« deal 2 damage to an enemy »",
       [HEROS] + en_jeu("sq008"), ["Puzzle.Action('sq008', 'HeroAction')"], {"degats": [[VILAIN, 2]]},
       main_exclusive=["01089"], payer_avec=["01089"], cibles=[VILAIN]),
    _c("sq008 Armor-Piercing Rounds : ennemi ROBUSTE (Shocker 3 PV) -> 5 degats : il est vaincu malgre Robuste",
       "« If that enemy has a tough status card, deal 5 damage instead. This attack gains piercing »",
       [HEROS, "Puzzle.PutIntoPlay('01103')", "Puzzle.Tough('01103')"] + en_jeu("sq008"),
       ["Puzzle.Action('sq008', 'HeroAction')"], {"absent_en_jeu": ["01103"]}, main_exclusive=["01089"], payer_avec=["01089"], cibles=["01103"]),
    _c("sq008 Armor-Piercing Rounds : CONTRE-CAS sans Robuste -> 2 degats seulement (Shocker 3 PV survit avec 1)",
       "la clause des 5 degats est conditionnee a Robuste",
       [HEROS, "Puzzle.PutIntoPlay('01103')"] + en_jeu("sq008"),
       ["Puzzle.Action('sq008', 'HeroAction')"], {"degats": [["01103", 2]]}, main_exclusive=["01089"], payer_avec=["01089"], cibles=["01103"]),

    # ============================================================ sq009 EMP Rounds
    _c("sq009 EMP Rounds : etourdit un sbire (Hydra Bomber)",
       "« stun or confuse a minion »",
       [HEROS, "Puzzle.PutIntoPlay('01110')"] + en_jeu("sq009"), ["Puzzle.Action('sq009', 'HeroAction')"],
       {"statuts": [["01110", "Stunned"]], "exhausted": ["sq009"]}, main_exclusive=["01088"], cibles=["01110"],
       preferer_option="Stun a minion"),
    _c("sq009 EMP Rounds : desoriente un sbire",
       "« stun or confuse a minion »",
       [HEROS, "Puzzle.PutIntoPlay('01110')"] + en_jeu("sq009"), ["Puzzle.Action('sq009', 'HeroAction')"],
       {"statuts": [["01110", "Confused"]]}, main_exclusive=["01088"], cibles=["01110"], preferer_option="Confuse a minion"),
    _c("sq009 EMP Rounds : « shuffle this card into your deck » -> etourdit le MECHANT, la carte retourne dans le deck",
       "« You may shuffle this card into your deck to stun or confuse the villain instead »",
       [HEROS] + en_jeu("sq009"), ["Puzzle.Action('sq009', 'HeroAction')"],
       {"statuts": [[VILAIN, "Stunned"]], "absent_en_jeu": ["sq009"]}, main_exclusive=["01088"], cibles=[VILAIN],
       preferer_option="Shuffle this card into your deck → stun"),

    # ============================================================ sq010 High Explosive Rounds
    _c("sq010 High Explosive Rounds : 3 degats a Rhino",
       "« deal 3 damage to an enemy »",
       [HEROS] + en_jeu("sq010"), ["Puzzle.Action('sq010', 'HeroAction')"], {"degats": [[VILAIN, 3]]},
       main_exclusive=["01090"], payer_avec=["01090"], cibles=[VILAIN]),
    _c("sq010 High Explosive Rounds : vainc un sbire (Hydra Bomber 2 PV) -> overkill sur le mechant + pioche 1",
       "« This attack gains overkill. If this attack defeats an enemy, draw 1 card »",
       [HEROS, "Puzzle.PutIntoPlay('01110')"] + en_jeu("sq010"), ["Puzzle.Action('sq010', 'HeroAction')"],
       {"absent_en_jeu": ["01110"], "taille_main": 1, "degats": [[VILAIN, 1]]}, main_exclusive=["01090"], payer_avec=["01090"], cibles=["01110"]),
    _c("sq010 High Explosive Rounds : CONTRE-CAS ne vainc pas -> pas de pioche",
       "la pioche est conditionnee a la defaite",
       [HEROS] + en_jeu("sq010"), ["Puzzle.Action('sq010', 'HeroAction')"], {"taille_main": 0}, main_exclusive=["01090"], payer_avec=["01090"], cibles=[VILAIN]),

    # ============================================================ sq011 Incendiary Rounds
    _c("sq011 Incendiary Rounds : seul ennemi en jeu -> 3 degats",
       "« deal 3 damage to an enemy. Reduce this damage by 1 for each other enemy in play »",
       [HEROS] + en_jeu("sq011"), ["Puzzle.Action('sq011', 'HeroAction')"], {"degats": [[VILAIN, 3]]},
       main_exclusive=["01088"], cibles=[VILAIN]),
    _c("sq011 Incendiary Rounds : 1 autre ennemi -> 2 a Rhino, puis 1 a l'autre",
       "reduction de 1 puis « deal 1 damage to that many other enemies »",
       [HEROS, "Puzzle.PutIntoPlay('01110')"] + en_jeu("sq011"), ["Puzzle.Action('sq011', 'HeroAction')"],
       {"degats": [[VILAIN, 2], ["01110", 1]]}, main_exclusive=["01088"], cibles=[VILAIN]),
    _c("sq011 Incendiary Rounds : 2 autres ennemis -> 1 a Rhino, puis 1 a chacun",
       "reduction plafonnee a 2",
       [HEROS, "Puzzle.PutIntoPlay('01101')", "Puzzle.PutIntoPlay('01110')"] + en_jeu("sq011"), ["Puzzle.Action('sq011', 'HeroAction')"],
       {"degats": [[VILAIN, 1], ["01101", 1], ["01110", 1]]}, main_exclusive=["01088"], cibles=[VILAIN]),
    _c("sq011 Incendiary Rounds : 3 autres ennemis -> 1 a Rhino, 1 a DEUX des trois seulement (plafond 2)",
       "« to a maximum of 2 » : la reduction et le nombre d'autres ennemis touches",
       [HEROS, "Puzzle.PutIntoPlay('01101')", "Puzzle.PutIntoPlay('01110')", "Puzzle.PutIntoPlay('01103')"] + en_jeu("sq011"),
       ["Puzzle.Action('sq011', 'HeroAction')"], {"degats": [[VILAIN, 1]], "sq_degats_total": [["01101", "01110", "01103"], 2]},
       main_exclusive=["01088"], cibles=[VILAIN]),

    # ============================================================ sq008-sq011 : action offerte SANS RESSOURCE EN MAIN (blocage d'autoplay)
    _c("sq011 Incendiary Rounds : SANS RESSOURCE EN MAIN la Hero Action n'est PAS offerte (nombre = 0)",
       "cout « Spend 1 resource of any type » impayable : une action offerte mais impayable fait boucler le pilote d'autoplay (4 parties sur 8 bloquees)",
       [HEROS, "Puzzle.EmptyHand()"] + en_jeu("sq011"), [], {"carte": "sq011", "type": "HeroAction", "nombre": 0},
       main_exclusive=[], verifier="actions_disponibles"),
    _c("sq008 Armor-Piercing Rounds : SANS RESSOURCE [mental] EN MAIN la Hero Action n'est PAS offerte (nombre = 0)",
       "meme controle pour le cout [mental]",
       [HEROS, "Puzzle.EmptyHand()"] + en_jeu("sq008"), [], {"carte": "sq008", "type": "HeroAction", "nombre": 0},
       main_exclusive=[], verifier="actions_disponibles"),
    _c("sq011 Incendiary Rounds : TEMOIN, AVEC une ressource en main la Hero Action est offerte (nombre = 1)",
       "contre-temoin des deux precedents",
       [HEROS] + en_jeu("sq011"), [], {"carte": "sq011", "type": "HeroAction", "nombre": 1},
       main_exclusive=["01088"], verifier="actions_disponibles"),

    _c("sq011 Incendiary Rounds : main VIDE mais With Great Firepower PRETE -> la Hero Action est offerte (nombre = 1)",
       "With Great Firepower genere une ressource [wild] pour une capacite d'amelioration : l'action reste payable",
       [HEROS, "Puzzle.EmptyHand()"] + en_jeu("sq011", "sq006"), [], {"carte": "sq011", "type": "HeroAction", "nombre": 1},
       main_exclusive=[], verifier="actions_disponibles"),
    _c("sq008 Armor-Piercing Rounds : main avec seulement [energy] (01088) -> la Hero Action [mental] n'est PAS offerte (nombre = 0)",
       "la couleur compte : YY ne paie pas B (blocage d'autoplay : le pilote repetait l'action impayable)",
       [HEROS] + en_jeu("sq008"), [], {"carte": "sq008", "type": "HeroAction", "nombre": 0},
       main_exclusive=["01088"], verifier="actions_disponibles"),
    # ============================================================ sq012 Swing and Reload
    _c("sq012 Swing and Reload : AERIAL (2 ameliorations inclinees avec Watch) -> redresse une autre amelioration",
       "« If you have the AERIAL trait, exhaust this card -> ready another upgrade you control »",
       [HEROS] + en_jeu("sq012", "sq005", "sq008", "sq009") + ["Puzzle.Exhaust('sq008', 'sq009')"],
       ["Puzzle.Action('sq012', 'HeroAction')"], {"exhausted": ["sq012"]}, main_exclusive=["01088"], cibles=["sq008"],
       accepter_choix=True),
    _c("sq012 Swing and Reload : Interruption, 1 degat qui menace -> prevenu, la carte est defaussee",
       "« When you would take any amount of damage, discard this card -> prevent that damage »",
       [HEROS] + en_jeu("sq012"), ["Puzzle.Damage('sq001a', 2)"], {"degats_identite": 0, "defausse": ["sq012"]},
       main_exclusive=["01088"], accepter_choix=True),
    _c("sq012 Swing and Reload : valeurs imprimees cout 1, trait SKILL",
       "nombres texte <-> code (scan)", [HEROS] + en_jeu("sq012"), [], {"traits_de": [["sq012", "SKILL"]]}, main_exclusive=["01088"]),

    # ============================================================ sq013 Punisher No More (obligation)
    _c("sq013 Punisher No More : branche « exhaust Peter Parker -> discard this obligation »",
       "« You may flip to alter-ego form. Choose: ... Exhaust Peter Parker -> discard this obligation »",
       [], ["Puzzle.Reveal('sq013')"], {"exhausted": ["sq001b"], "defausse_rencontre": ["sq013"]}, main_exclusive=["01088"],
       accepter_choix=True, preferer_option="Exhaust Peter Parker"),
    _c("sq013 Punisher No More : branche « discard 2 Web-Shooter upgrades -> remove from the game »",
       "« Discard 2 WEB-SHOOTER upgrades from play. Remove Punisher No More from the game »",
       en_jeu("sq008", "sq009"), ["Puzzle.Reveal('sq013')"], {"defausse": ["sq008", "sq009"], "hors_jeu": ["sq013"]},
       main_exclusive=["01088"], accepter_choix=True, preferer_option="Discard 2 Web-Shooter"),

    _c("sq013 Punisher No More : a DEUX joueurs, un WEB-SHOOTER chez chacun -> les deux sont defausses (« from play », pas « you control »)",
       "« Discard 2 WEB-SHOOTER upgrades FROM PLAY » (RR : pas de « you control », et pas un cout) : toute amelioration WEB-SHOOTER en jeu, "
       "tous joueurs (arbitrage du 26/10/2026) ; avant, seules celles du joueur Peter Parker comptaient et la branche etait indisponible",
       en_jeu("sq008") + ["Puzzle.PutIntoPlay('sq009', under_control=True, player=1)"], ["Puzzle.Reveal('sq013')"],
       {"defausse": ["sq008", "sq009"], "hors_jeu": ["sq013"]},
       main_exclusive=["01088"], accepter_choix=True, preferer_option="Discard 2 Web-Shooter", heros2="spider_man"),

    # ============================================================ sq014 Green Goblin
    _c("sq014 Green Goblin : attaque un allie du joueur au lieu du joueur (Hellcat 01020)",
       "« When Green Goblin attacks you, he attacks an ally you control instead (if able) »",
       [HEROS, "Puzzle.PutIntoPlay('01020', under_control=True)", "Puzzle.PutIntoPlay('sq014')"],
       ["Puzzle.EnemyAttacks('sq014', 'sq001a')"], {"degats_identite": 0}, main_exclusive=["01088"], passer_sur_option="Defense"),
    _c("sq014 Green Goblin : a DEUX joueurs, le joueur attaque (2) a deux allies -> c'est le PREMIER joueur (Spider-Punisher) qui choisit lequel (RR First Player)",
       "« he attacks an ally you control instead » : plusieurs cibles admissibles pour une carte de rencontre -> le premier joueur choisit (RR First Player, "
       "arbitrage du 26/10/2026) ; avant, le joueur attaque choisissait lui-meme",
       [HEROS, "Puzzle.PutIntoPlay('01020', under_control=True, player=1)", "Puzzle.PutIntoPlay('01083', under_control=True, player=1)",
        "Puzzle.PutIntoPlay('sq014')"],
       [], {"choisit": 0},
       main_exclusive=["01088"], heros2="spider_man", verifier="sq_qui_choisit"),
    _c("sq014 Green Goblin : CONTRE-CAS sans allie, il attaque le joueur (2 degats)",
       "« (if able) »",
       [HEROS, "Puzzle.PutIntoPlay('sq014')"], ["Puzzle.EnemyAttacks('sq014', 'sq001a')"], {"degats_identite": 2},
       main_exclusive=["01088"], passer_sur_option="Defense"),
    _c("sq014 Green Goblin : valeurs imprimees PV 6, ATK 2, SCH 2, ELITE GOBLIN, Toughness",
       "nombres texte <-> code (scan)", [HEROS, "Puzzle.PutIntoPlay('sq014')"], [],
       {"pv_max": [["sq014", 6]], "traits_de": [["sq014", "ELITE"], ["sq014", "GOBLIN"]], "statuts": [["sq014", "Tough"]]},
       main_exclusive=["01088"]),

    # ============================================================ sq015 The Goblin's Ultimatum
    _c("sq015 The Goblin's Ultimatum : entre en jeu avec 2 de menace",
       "menace de depart 2 (fixe)",
       [HEROS], ["Puzzle.Reveal('sq015')"], {"menace": [["sq015", 2]]}, main_exclusive=["01088"]),
    _c("sq015 The Goblin's Ultimatum : un heros ne peut PAS retirer sa menace en thwart",
       "« Threat cannot be removed from this scheme except from its own abilities »",
       [HEROS, "Puzzle.Reveal('sq015')"], ["Puzzle.Thwart('sq001a')"], {"menace": [["sq015", 2]]}, main_exclusive=["01088"],
       cibles=["sq015"]),
    _c("sq015 The Goblin's Ultimatum : Hero Action « take 2 damage -> remove 1 threat from this scheme »",
       "« Exhaust your hero, discard 1 upgrade you control, or take 2 damage -> remove 1 threat from this scheme »",
       [HEROS, "Puzzle.Reveal('sq015')"], ["Puzzle.Action('sq015', 'HeroAction')"], {"menace": [["sq015", 1]], "degats_identite": 2},
       main_exclusive=["01088"], accepter_choix=True, preferer_option="Take 2 damage"),
    _c("sq015 The Goblin's Ultimatum : Hero Action « exhaust your hero »",
       "branche « Exhaust your hero »",
       [HEROS, "Puzzle.Reveal('sq015')"], ["Puzzle.Action('sq015', 'HeroAction')"], {"menace": [["sq015", 1]], "exhausted": ["sq001a"]},
       main_exclusive=["01088"], accepter_choix=True, preferer_option="Exhaust your hero"),
    _c("sq015 The Goblin's Ultimatum : Hero Action « discard 1 upgrade you control »",
       "branche « discard 1 upgrade »",
       [HEROS, "Puzzle.Reveal('sq015')"] + en_jeu("sq008"), ["Puzzle.Action('sq015', 'HeroAction')"],
       {"menace": [["sq015", 1]], "defausse": ["sq008"]}, main_exclusive=["01088"], accepter_choix=True, preferer_option="Discard 1 upgrade"),
    _c("sq015 The Goblin's Ultimatum : fin de la phase joueur -> devoile l'obligation Punisher No More et se defausse",
       "« At the end of the next player phase, if this card is still in play, find the Spider-Punisher obligation and reveal it. Discard this card »",
       [HEROS, "Puzzle.CreateEncounterDeck('sq013')", "Puzzle.Reveal('sq015')"], ["Puzzle.EndPlayerPhase()"], {"defausse_rencontre": ["sq015"]},
       main_exclusive=["01088"], accepter_choix=True),

    # ============================================================ sq016 Reorganized Crime
    _c("sq016 Reorganized Crime : sbire non ELITE (Hydra Bomber) dans la defausse rencontre -> en jeu, ROBUSTE",
       "« Search the encounter discard pile for a non-ELITE minion and put it into play engaged with you. Give that minion a tough status card »",
       [HEROS, "Puzzle.CreateEncounterDiscardPile('01110')"], ["Puzzle.Reveal('sq016')"],
       {"en_jeu": ["01110"], "statuts": [["01110", "Tough"]]}, main_exclusive=["01088"], accepter_choix=True),
    _c("sq016 Reorganized Crime : CONTRE-CAS un sbire ELITE (Green Goblin) n'est pas cherche",
       "« non-ELITE »",
       [HEROS, "Puzzle.CreateEncounterDiscardPile('sq014')"], ["Puzzle.Reveal('sq016')"],
       {"absent_en_jeu": ["sq014"]}, main_exclusive=["01088"], accepter_choix=True),
    _c("sq016 Reorganized Crime : aucune cible -> la carte gagne Renfort",
       "« If you cannot, this card gains surge »", [HEROS], ["Puzzle.Reveal('sq016')"], {"carte_du_surge": True},
       main_exclusive=["01088"], accepter_choix=True),

    # ============================================================ sq017 Revealed Identity
    _c("sq017 Revealed Identity : le mechant manigance contre le joueur -> il l'ATTAQUE (2 degats), puis 2 menaces",
       "« When the villain would scheme against you, it attacks you instead. Place 2 threat on the main scheme after that attack »",
       [HEROS, "Puzzle.Reveal('sq017')"], [f"Puzzle.Scheme('{VILAIN}')"], {"degats_identite": 2, "menace": [[COMPLOT, 2]]},
       main_exclusive=["01088"], passer_sur_option="Defense"),
    _c("sq017 Revealed Identity : Hero Action « spend 2 resources -> discard this card »",
       "cout 2 ressources (paye par le montage)",
       [HEROS, "Puzzle.Reveal('sq017')"], ["Puzzle.Action('sq017', 'HeroAction')"], {"defausse_rencontre": ["sq017"]},
       main_exclusive=["01088"]),
]


VERIFICATIONS = r'''

def sq_qui_choisit(monde, aides):
    """RR First Player : qui est interroge par `AskChooseFace` quand Green Goblin redirige son attaque vers l'un de PLUSIEURS allies ?
    Le choix est intercepte (le premier allie est pris), et l'attaque est jouee ICI, apres la mise en place, sous interception.
    Cle `attendu` : `choisit` = indice du joueur interroge."""
    from game.puzzle import RunPuzzle
    attendu = aides["cas"]["attendu"]
    interroges = []
    classe = type(monde.players[0])
    origine = classe.__dict__.get("AskChooseFace")

    def intercepte(self, faces, by_effect, **kwargs):
        interroges.append(self.player_id)
        return faces[0] if faces else None

    classe.AskChooseFace = intercepte
    try:
        RunPuzzle(monde).EnemyAttacks('sq014', '01001b', joueur=1, players_may_defend=False)
    finally:
        if origine is None:
            del classe.AskChooseFace
        else:
            classe.AskChooseFace = origine
    if interroges != [attendu["choisit"]]:
        return False, f"joueur(s) interroge(s) : {interroges}, attendu [{attendu['choisit']}]"
    return True, f"le joueur {interroges[0]} choisit l'allie"


def sq_etat(monde, aides):
    """Cles propres : `sq_stats` ({attribut: valeur} lus sur l'identite), `traits_main` ([[card_id, [traits exacts]]] d'une carte
    EN MAIN), `absent_en_jeu` ([card_id] absents du jeu), `taille_deck_rencontre` ; le reste va a etat_attendu."""
    cas = aides["cas"]
    attendu = cas.get("attendu") or {}
    soucis = []
    identite = aides["identite"](monde)
    for nom, valeur in (attendu.get("sq_stats") or {}).items():
        courant = getattr(identite, nom, None)
        if courant != valeur:
            soucis.append(f"{nom} = {courant} (attendu {valeur})")
    main = {getattr(f.paper, "card_id", None): f for f in monde.players[0].hand_cards.Get()}
    for card_id, traits in attendu.get("traits_main") or []:
        face = main.get(card_id)
        if face is None:
            soucis.append(f"{card_id} absente de la main (traits_main)")
            continue
        for t in ("ATTACK", "SKILL", "TACTIC", "CONDITION", "LOCATION"):
            if face.HasTrait(t) != (t in traits):
                soucis.append(f"{card_id} : trait {t} {'present' if face.HasTrait(t) else 'absent'} (attendu {traits})")
    if attendu.get("sq_degats_total"):
        ids, total = attendu["sq_degats_total"]
        somme = 0
        for card_id in ids:
            face = aides["par_id"](monde, card_id)
            somme += getattr(face, "sustained", 0) if face is not None else 0
        if somme != total:
            soucis.append(f"degats totaux sur {ids} = {somme} (attendu {total})")
    if attendu.get("absent_en_jeu"):
        for card_id in attendu["absent_en_jeu"]:
            if aides["par_id"](monde, card_id) is not None:
                soucis.append(f"{card_id} est encore en jeu (absent_en_jeu)")
    reste = {k: v for k, v in attendu.items() if k not in ("sq_stats", "traits_main", "absent_en_jeu", "taille_deck_rencontre", "sq_degats_total")}
    copie = dict(aides); copie["cas"] = dict(cas); copie["cas"]["attendu"] = reste
    ok, message = etat_attendu(monde, copie)
    if not ok:
        soucis.append(message)
    if soucis:
        return False, " ; ".join(soucis)
    return True, message
'''
