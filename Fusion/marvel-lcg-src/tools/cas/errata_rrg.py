# Cas test_capacites des CORRECTIONS DE COMPORTEMENT dues aux errata officiels (Rules Reference 1.8, Annexe V) : noms commencant par le card_id
# (pas de prefixe commun : la substitution se fait carte par carte, `tools/substituer_pack.py <game_dir> <port> <card_id>`, ou en remettant l'ANCIEN script).
# Source du comportement voulu : `ui-app/src/board/errata-rrg.ts` (texte EN corrige) ; audit : `A creer/errata-rrg/AUDIT-ERRATA.md`.
#
# Rappels de montage (spider_man, scenario rhino) :
#  - `Puzzle.CreatePlayerDeck(...)` dans `declencher` AVANT `jouer` fixe le deck ; `main_exclusive` fixe la main ; `jouer` joue la carte ;
#  - 01067 Maria Hill (allie, pas signature), 01002 Black Cat (allie SIGNATURE de Spider-Man : classe Hero = « identity-specific ») ;
#  - `Puzzle.ChangeToFace('01001b', '01001a')` : Spider-Man en HEROS (trait AVENGER) ; `Puzzle.ChangeToFace('50001b', '50001a')` : Maria Hill en HEROS (trait S.H.I.E.L.D),
#    deck `maria_hill` ; `Puzzle.Attach(<carte>, <cible>)` attache une carte deja en jeu ; cle `taille_attaches` [[hote, n]] = nombre EXACT d'attaches de l'hote.
HEROS_SM = "Puzzle.ChangeToFace('01001b', '01001a')"
HEROS_MH = "Puzzle.ChangeToFace('50001b', '50001a')"


def _c(nom, pourquoi, mise, declencher, attendu, **cle):
    cas = {'nom': nom, 'pourquoi': pourquoi, 'scenario': cle.pop('scenario', 'rhino'), 'heros': cle.pop('heros', 'spider_man'),
           'mise_en_place': list(mise), 'declencher': list(declencher), 'verifier': cle.pop('verifier', 'etat_attendu'), 'attendu': attendu}
    cas.update(cle)
    return cas


CAS = [
    # ============================================================ 45017 Suit Up (errata 1.7/1.8 : « to THAT ally » -> « to AN ally »)
    _c("45017 Suit Up — errata : Sidekick (45015) est proposee avec un allie NON signature (Maria Hill) quand un allie signature est en jeu",
       "« an upgrade that can be attached to AN ally » : l'amelioration se cherche independamment de l'allie pris ; Sidekick (« identity-specific ally ») "
       "est attachable a Black Cat EN JEU, meme si l'allie pris est Maria Hill. Avec l'ANCIEN script (« that ally ») Sidekick n'etait pas proposee",
       ["Puzzle.PutIntoPlay('01002', under_control=True)"],
       ["Puzzle.CreatePlayerDeck('01067', '45015')"],
       {'en_main': ['01067', '45015'], 'taille_main': 2},
       main_exclusive=['45017', '01088'], jouer=['45017'], accepter_choix=True),
    _c("45017 Suit Up — errata, TEMOIN : Sidekick n'est PAS proposee quand aucun allie signature n'existe nulle part (seul l'allie est pris)",
       "« can be attached to an ally » reste une vraie restriction : sans allie signature (deck VIDE d'abord : le deck de Spider-Man contient Black Cat, deck, defausse, main, jeu) Sidekick n'est attachable a aucun allie ; "
       "RRG 1.8 (Search) : chaque recherche est INDEPENDANTE, l'allie (Maria Hill) est pris meme si aucune amelioration n'est attachable (decision du 04/11 : on suit les regles)",
       ["Puzzle.EmptyPlayerDeck()"],
       ["Puzzle.CreatePlayerDeck('01067', '45015')"],
       {'en_main': ['01067'], 'taille_main': 1},
       main_exclusive=['45017', '01088'], jouer=['45017'], accepter_choix=True),
    _c("45017 Suit Up — errata, TEMOIN : Danger Room Training (33015, « X-MEN ally ») n'est pas proposee quand aucun allie X-Men n'existe (seul l'allie est pris)",
       "l'amelioration d'allie specifique reste ecartee quand aucun allie compatible n'existe, mais l'allie (Maria Hill) est pris : chaque recherche est independante (RRG 1.8, Search)",
       ["Puzzle.EmptyPlayerDeck()"],
       ["Puzzle.CreatePlayerDeck('01067', '33015')"],
       {'en_main': ['01067'], 'taille_main': 1},
       main_exclusive=['45017', '01088'], jouer=['45017'], accepter_choix=True),

    # ============================================================ 03025 Honorary Avenger et 54033 S.H.I.E.L.D. Deputy (errata 1.7/1.8 : ajout de « Max 1 per character »)
    # Le moteur applique deja le maximum : `MaxPerUnit: 1` est dans `desc` (play.py `max_per_unit`) ; le texte affiche n'avait simplement pas la ligne. Ces cas le PROUVENT.
    # ⚠ Deux copies de la MEME carte : `Puzzle.CreatePlayerDeck('X', 'X')` cree DEUX cartes neuves (un `Puzzle.Attach`/`Gain` par id retombe sinon sur la meme) ;
    # `Puzzle.Attach` attache la 1re (trouvee dans le deck), `Puzzle.Gain` met la 2e en main.
    _c("03025 Honorary Avenger — errata « Max 1 per character » : une 2e copie ne s'attache pas au personnage qui en porte deja une (aucune cible legale)",
       "une copie est attachee a Spider-Man (seul personnage ami en jeu) : la 2e copie, en main, n'a aucune cible legale et reste en main",
       [HEROS_SM, "Puzzle.EmptyHand()", "Puzzle.CreatePlayerDeck('03025', '03025')", "Puzzle.Attach('03025', '01001a')", "Puzzle.Gain('03025')"], [],
       {'taille_attaches': [['01001a', 1]], 'en_main': ['03025']}),
    _c("03025 Honorary Avenger — errata, TEMOIN : la 2e copie se pose sur un AUTRE personnage ami (Black Cat), Spider-Man garde la sienne",
       "« Max 1 PER CHARACTER » et pas « per player » : Black Cat n'en porte pas encore, elle est la seule cible legale",
       [HEROS_SM, "Puzzle.EmptyHand()", "Puzzle.PutIntoPlay('01002', under_control=True)", "Puzzle.CreatePlayerDeck('03025', '03025')", "Puzzle.Attach('03025', '01001a')", "Puzzle.Gain('03025')"], [],
       {'taille_attaches': [['01001a', 1], ['01002', 1]]}, jouer=['03025'], accepter_choix=True),
    _c("54033 S.H.I.E.L.D. Deputy — errata « Max 1 per character » : une 2e copie ne s'attache pas au personnage qui en porte deja une (aucune cible legale)",
       "Maria Hill (trait S.H.I.E.L.D) porte deja un Deputy : la 2e copie, en main, n'a aucune cible legale",
       [HEROS_MH, "Puzzle.EmptyHand()", "Puzzle.CreatePlayerDeck('54033', '54033')", "Puzzle.Attach('54033', '50001a')", "Puzzle.Gain('54033')"], [],
       {'taille_attaches': [['50001a', 1]], 'en_main': ['54033']}, heros='maria_hill'),
    _c("54033 S.H.I.E.L.D. Deputy — errata, TEMOIN : la 2e copie se pose sur un AUTRE personnage ami (Black Cat)",
       "« Max 1 per CHARACTER » : Black Cat n'en porte pas encore, elle est la seule cible legale",
       [HEROS_MH, "Puzzle.EmptyHand()", "Puzzle.PutIntoPlay('01002', under_control=True)", "Puzzle.CreatePlayerDeck('54033', '54033')", "Puzzle.Attach('54033', '50001a')", "Puzzle.Gain('54033')"], [],
       {'taille_attaches': [['50001a', 1], ['01002', 1]]}, heros='maria_hill', jouer=['54033'], accepter_choix=True),
    # ============================================================ 39016 The Search for Spiral (errata 1.8 : « Take 2 damage → remove 3 threat » : les degats sont un COUT)
    _c("39016 The Search for Spiral — Hero Action : 2 degats a l'identite (cout) ET 3 menaces retirees de la manigance (3 de depart + 5 posees = 8 -> 5)",
       "modele `16123` (`CostFunc.TakeDamage`) : le cout est paye, puis l'effet retire 3 menaces",
       [HEROS_SM, "Puzzle.EmptyHand()", "Puzzle.PutIntoPlay('39016')", "Puzzle.PlaceThreat('39016', 5)"],
       ["Puzzle.Action('39016', 'HeroAction')"],
       {'degats_identite': 2, 'menace': [['39016', 5]]}, accepter_choix=True),
    _c("39016 The Search for Spiral — errata : le COUT n'est pas paye si les degats sont empeches (Tenace) : AUCUNE menace retiree (8 reste 8)",
       "« Take 2 damage → remove 3 threat » : si tous les degats ne sont pas subis, le cout n'est pas paye (regle officielle, `TakeDamageOnCall`) ; "
       "avec l'ANCIEN script la menace etait retiree quand meme (8 -> 5). La carte Tenace est consommee, l'identite ne subit rien",
       [HEROS_SM, "Puzzle.EmptyHand()", "Puzzle.PutIntoPlay('39016')", "Puzzle.PlaceThreat('39016', 5)", "Puzzle.Tough('01001a')"],
       ["Puzzle.Action('39016', 'HeroAction')"],
       {'degats_identite': 0, 'menace': [['39016', 8]]}, accepter_choix=True),
    _c("39016 The Search for Spiral — TEMOIN : sous forme ALTER-EGO la Hero Action n'est pas offerte (menace 8, aucun degat)",
       "« Hero Action » : uniquement en forme heros",
       ["Puzzle.EmptyHand()", "Puzzle.PutIntoPlay('39016')", "Puzzle.PlaceThreat('39016', 5)"],
       [],
       {'degats_identite': 0, 'menace': [['39016', 8]]}, declencher_tolerant=["Puzzle.Action('39016', 'HeroAction')"]),

    # ============================================================ 31001b SP//dr Suit (errata 1.8 : « Return to Base » : jetons et attachements vont VERS Peni Parker)
    # Montage : deck `sp_dr`, identite de depart = Peni Parker (31002a, alter-ego) ; `Puzzle.ChangeForm('31002a')` -> armure SP//dr Suit (31001a, heros) ;
    # `Puzzle.ChangeForm('31001a')` -> retour a Peni Parker (« Return to Base », 31001b). L'armure et Peni ne sont jamais en jeu en meme temps comme identite.
    _c("31001b SP//dr Suit — errata « Return to Base » : au retour sous forme Peni Parker, les 3 compteurs de l'armure passent a PENI (31002a) ; l'armure est retournee sur sa face inactive (31001b)",
       "texte corrige : « moving all counters on THIS card ... to HER » (de l'armure vers Peni) ; `Spdr()` deplace de l'identite sortante vers l'identite entrante dans les deux sens",
       ["Puzzle.EmptyHand()"],
       ["Puzzle.ChangeForm('31002a')", "Puzzle.PlaceCounters('31001a', 'counter', 3)", "Puzzle.ChangeForm('31001a')"],
       {'compteurs': [['31002a', 'counter', 3]], 'hors_jeu': ['31001a']}, heros='sp_dr'),
    _c("31001b SP//dr Suit — errata « Return to Base » : une amelioration attachee a l'armure (31011 Psychic Link) suit a PENI PARKER au retour",
       "« ... and cards attached to this card to her »",
       ["Puzzle.EmptyHand()"],
       ["Puzzle.ChangeForm('31002a')", "Puzzle.Attach('31011', '31001a')", "Puzzle.ChangeForm('31001a')"],
       {'attaches': [['31002a', '31011']]}, heros='sp_dr'),
    _c("31001b SP//dr Suit — TEMOIN, sens inverse (« Suit Up! » 31002b, inchange) : les 2 compteurs de Peni passent a l'ARMURE (31001a) quand on revêt le costume",
       "« moving all counters on this card ... to SP//dr Suit » : le sens du texte de 31002b n'est PAS celui de l'errata de 31001b",
       ["Puzzle.EmptyHand()", "Puzzle.PlaceCounters('31002a', 'counter', 2)"],
       ["Puzzle.ChangeForm('31002a')"],
       {'compteurs': [['31001a', 'counter', 2]], 'hors_jeu': ['31002a']}, heros='sp_dr'),

    # ============================================================ 32141b / 32142b / 32143b Asteroid M, Factory Online, The Rule of Magnus (errata 1.8 : 3 compteurs RETIRES AVANT la revelation)
    # Scenario `magneto` (complot principal Asteroid M B 32141b en jeu au depart). 32142b et 32143b ont `ability_link: 32141b` : ils executent le script de 32141b (leur preuve par substitution est celle de 32141b).
    # 32147 Magneto's Helmet : attachement MAGNETIC « Attach to Magneto » : sa revelation prouve que la carte Magnetic a ete defaussee puis revelee.
    _c("32141b Asteroid M B — errata : au 3e compteur magnet, 3 compteurs sont retires (3 -> 0) PUIS la carte Magnetic defaussee est revelee (32147 en jeu)",
       "« remove 3 of them and discard cards from the encounter deck until a Magnetic card is discarded. Reveal that card. » : le deck est vide sauf 32147",
       ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('32147')"],
       ["Puzzle.PlaceCounters('32141b', 'magnet', 3)"],
       {'compteurs': [['32141b', 'magnet', 0]], 'en_jeu': ['32147']}, scenario='magneto'),
    _c("32141b Asteroid M B — TEMOIN : sous le seuil (2 compteurs), rien n'est retire ni revele",
       "« if there are at least 3 magnet counters here »",
       ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('32147')"],
       ["Puzzle.PlaceCounters('32141b', 'magnet', 2)"],
       {'compteurs': [['32141b', 'magnet', 2]], 'hors_jeu': ['32147']}, scenario='magneto'),
    _c("32142b Factory Online B — errata : au 3e compteur magnet, 3 compteurs retires PUIS la carte Magnetic revelee (via ability_link vers le script de 32141b)",
       "meme texte que 32141b ; stade 2 mis en jeu a la main",
       ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('32147')", "Puzzle.PutIntoPlay('32142b')"],
       ["Puzzle.PlaceCounters('32142b', 'magnet', 3)"],
       {'compteurs': [['32142b', 'magnet', 0]], 'en_jeu': ['32147']}, scenario='magneto'),
    _c("32143b The Rule of Magnus B — errata : au 3e compteur magnet, 3 compteurs retires PUIS la carte Magnetic revelee (via ability_link vers le script de 32141b)",
       "meme texte que 32141b ; stade 3 mis en jeu a la main",
       ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('32147')", "Puzzle.PutIntoPlay('32143b')"],
       ["Puzzle.PlaceCounters('32143b', 'magnet', 3)"],
       {'compteurs': [['32143b', 'magnet', 0]], 'en_jeu': ['32147']}, scenario='magneto'),

    # ============================================================ 32008 Steel Fist (errata 1.8 : « discard a tough status card ... TO stun and confuse » : la fleche de cout devient « to »)
    # Le script suivait deja « to » : le choix facultatif est tire APRES les 5 degats, la carte Tenace est defaussee puis les deux statuts sont poses (aucun cout).
    # Montage : deck `colossus` (alter-ego 32001b, heros 32001a), Strength (01090, RR) paie le cout 2.
    _c("32008 Steel Fist — 5 degats a Rhino ; on defausse la carte Tenace de Colossus (Steel Skin la donne au passage en heros) : l'ennemi est ETOURDI et DESORIENTE, la Tenace est consommee",
       "« You may discard a tough status card from your hero to stun and confuse that enemy » ; ⚠ pas de `Puzzle.Tough` : 32001a « Steel Skin » donne deja une Tenace et en permet 2 (le cas a montre qu'une 2e etait defaussee par le montage)",
       ["Puzzle.EmptyHand()", "Puzzle.ChangeForm('32001b')"], [],
       {'degats': [['01094', 5]], 'statuts': [['01094', 'Stunned'], ['01094', 'Confused']]},
       heros='colossus', main_exclusive=['32008', '01090'], jouer=['32008'], payer_avec=['01090'], cibles=['01094'], accepter_choix=True),
    # ============================================================ 35008 Berserker Barrage (errata 1.8 : « you may take 2 damage TO repeat this ability » : plus un cout)
    # Le script suivait deja « to » (`TakeDamage` puis `action`, pas de `CostFunc`). Montage : deck `wolverine` (alter-ego 35001b, heros 35001a) ;
    # Hydra Mercenary (01101, 3 PV, Garde) est engage : la 1re attaque doit le viser, 4 degats le vainquent -> on peut en prendre 2 pour recommencer sur Rhino.
    _c("35008 Berserker Barrage — l'attaque (4) vainc Hydra Mercenary ; on prend 2 degats pour la REPETER : Rhino subit 4 et Wolverine 2",
       "« If this attack defeats an enemy, you may take 2 damage to repeat this ability »",
       ["Puzzle.EmptyHand()", "Puzzle.ChangeForm('35001b')", "Puzzle.PutIntoPlay('01101')"], [],
       {'degats_identite': 2, 'degats': [['01094', 4]], 'hors_jeu': ['01101']},
       heros='wolverine', main_exclusive=['35008', '01090'], jouer=['35008'], payer_avec=['01090'], cibles=['01101', '01094'], accepter_choix=True),
    _c("35008 Berserker Barrage — TEMOIN : l'attaque ne vainc personne (Rhino, 4 degats) : pas de repetition, Wolverine ne subit rien",
       "« If this attack DEFEATS an enemy »",
       ["Puzzle.EmptyHand()", "Puzzle.ChangeForm('35001b')"], [],
       {'degats_identite': 0, 'degats': [['01094', 4]]},
       heros='wolverine', main_exclusive=['35008', '01090'], jouer=['35008'], payer_avec=['01090'], cibles=['01094'], accepter_choix=True),
    # ============================================================ 36030 Claustrophobia (errata 1.8 : « You cannot change to HERO form » : equivalent en pratique)
    # `PlayersCannotChangeForms` interdit tout changement ; le joueur est deja force en alter-ego a la revelation, donc seul le passage au heros est possible : meme resultat.
    _c("36030 Claustrophobia — revelee, elle fait passer Storm sous forme d'ALTER-EGO (Ororo Munroe 36001b)",
       "« Flip to alter-ego form »",
       ["Puzzle.EmptyHand()", "Puzzle.ChangeForm('36001b')"], ["Puzzle.Reveal('36030')"],
       {'en_jeu': ['36001b', '36030'], 'hors_jeu': ['36001a']}, heros='storm'),
    _c("36030 Claustrophobia — errata : tant qu'elle est en jeu, on NE PEUT PAS repasser sous forme de heros (le changement est refuse, Ororo reste alter-ego)",
       "« You cannot change to hero form »",
       ["Puzzle.EmptyHand()", "Puzzle.Reveal('36030')"], [],
       {'en_jeu': ['36001b', '36030'], 'hors_jeu': ['36001a']}, heros='storm', declencher_tolerant=["Puzzle.ChangeForm('36001b')"]),
]
