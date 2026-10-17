# Cas test_capacites du pack tmnt_shinobi_paths (Inkwire, TMNT Shinobi, les 11 PATHS, prefixe `se`), 17/10/2026.
# Filtre : `[se]`. Gabarits : .planning/tmnt/shinobi-paths-gabarits.md. Questions : .planning/tmnt/shinobi-socle-questions.md.
#
# Conventions :
#  - Spider-Man (01001) demarre en ALTER EGO ; HEROS le met en forme heros ;
#  - le Path est mis en jeu par `Puzzle.PutIntoPlay('seNNN', under_control=True)` (aire de soutien, type Path) ;
#    le chemin REEL « Path du deck -> mis de cote -> en jeu au Setup » a ses propres cas (`deck_ajoute`) ;
#  - Rhino 01094 (vilain du scenario `rhino`) est la cible des attaques, 01101 Hydra Mercenary (3 PV) le sbire ;
#  - `main_exclusive` vide la main (APRES la mise en place) : chaque cas sait avec QUOI il paie
#    (01088 Energy = YY, 01089 Genius = BB, 01090 Strength = RR) ;
#  - deck rencontre bourre de « I'm Tough » (01105, sans icone de boost) : aucune carte rencontre ne vient
#    brouiller la mesure ;
#  - cartes Shinobi deja en base (jennika, `tj`) servant de matiere : tj004 Decisive Strike (Taijutsu, evenement
#    ATTACK, 2), tj005 Moonlighting (Ninjutsu, 0), tj003 Apparition (Kuji-Kiri), tj006 Fearless Resolve (Bushido, OATH,
#    Uses 2 samurai), tj008 Jennika's Bow (amelioration NON Oath, sans classe Shinobi).
SC = "rhino"
HEROS = "Puzzle.ChangeForm('01001b')"
COMPLOT = "01097b"
SANS_BOOST = ["Puzzle.EmptyEncounterDeck()",
              "Puzzle.CreateEncounterDeck('01105', '01105', '01105', '01105', '01105', '01105', '01105', '01105')"]
TOUS = [("se001", "Kagemusha"), ("se002", "Onmyodo"), ("se003", "Samurai"), ("se004", "Shihan"),
        ("se005", "The Last Ronin"), ("se006", "Yoshimitsu"), ("se007", "Yamabushi"), ("se008", "Onigari"),
        ("se009", "Ashigaru"), ("se010", "Onmitsu"), ("se011", "Yojimbo")]


def _voie(cid):
    return f"Puzzle.PutIntoPlay('{cid}', under_control=True)"


def _c(nom, pourquoi, mise, declencher, attendu, **cle):
    if not cle.pop("avec_boost", False):
        mise = SANS_BOOST + list(mise)
    cas = {"nom": "[se] " + nom, "pourquoi": pourquoi, "scenario": cle.pop("scenario", SC),
           "heros": cle.pop("heros", "spider_man"), "mise_en_place": list(mise), "declencher": list(declencher),
           "verifier": cle.pop("verifier", "etat_attendu"), "attendu": attendu}
    cas.update(cle)
    return cas


def _dispo(nom, pourquoi, mise, carte, type_, nombre, **cle):
    """Cas « l'action est (ou n'est pas) proposee » : `nombre` actions REELLEMENT disponibles."""
    return _c(nom, pourquoi, mise, cle.pop("declencher", []), {"carte": carte, "type": type_, "nombre": nombre},
              verifier="se_actions_disponibles", **cle)


CAS = [
    # ===================================================================== moteur : classes Shinobi, Dual
    _c("se006 Yoshimitsu (classe DUAL Bushido;Kuji-Kiri) : compte pour LES DEUX classes, ni aspect ni Basic",
       "une carte a deux classes Shinobi : `IsClass` et `CardFinder(card_class=...)` la reconnaissent pour CHACUNE (livret p.7 : "
       "« Dual Shinobi cards count as both types »), pas pour une troisieme ; les classes Shinobi ne sont NI un aspect NI Basic "
       "(livret p.8 : « Shinobi cards do not count as aspect or basic cards when triggering abilities »)",
       [_voie("se006")], [],
       {"carte": "se006", "oui": ["Bushido", "Kuji-Kiri"], "non": ["Ninjutsu", "Taijutsu", "Aspect", "Basic", "Aggression",
                                                                    "Justice", "Leadership", "Protection"]},
       verifier="se_classes"),
    _c("se005 The Last Ronin (QUATRE classes) : une carte portant les quatre types est Shinobi pour chacun",
       "Bushido, Ninjutsu, Kuji-Kiri et Taijutsu tous vrais ; `CarteShinobi()` (sans argument) la retient ; aucun aspect, pas Basic",
       [_voie("se005")], [],
       {"carte": "se005", "oui": ["Bushido", "Ninjutsu", "Kuji-Kiri", "Taijutsu"], "non": ["Aspect", "Basic", "Aggression"]},
       verifier="se_classes"),

    # ===================================================================== moteur : le Path du deck est mis en jeu au Setup
    _c("se001 Kagemusha choisi au deck-building : mis de cote, mis en jeu au Setup (hors du deck), pour un heros QUELCONQUE",
       "un Path place dans `player_deck` par le constructeur n'est jamais melange : `PlayerSetup.MettreLesPathsDeCoteEtEnJeuAuSetup` le "
       "fabrique de cote et le met en jeu sous le controle du joueur a l'etape « Set Up » ; un SEUL exemplaire, aucun dans le deck "
       "ni en main (Spider-Man, heros non TMNT)",
       [], [], {"carte": "se001", "total": 1, "en_jeu": 1, "dans_deck": 0, "en_main": 0},
       verifier="se_exemplaires", deck_ajoute=["se001"]),
    _c("se001 Kagemusha : TEMOIN, sans Path dans le deck, rien n'est mis en jeu",
       "contre-cas du precedent : aucune carte Path n'existe dans la partie",
       [], [], {"carte": "se001", "total": 0, "en_jeu": 0, "dans_deck": 0, "en_main": 0},
       verifier="se_exemplaires"),
    _c("se001 Kagemusha : la main de DEPART tient deja compte de « -1 hand size » (Peter Parker 6 -> 5)",
       "le Path est mis en jeu AVANT la pioche de depart (etape 11 de la mise en place, pioche a l'etape 14)",
       [], [], {"taille_main": 5, "en_jeu": ["se001"]}, deck_ajoute=["se001"], avec_boost=True),
    _c("se001 Kagemusha : TEMOIN, sans Path la main de depart est complete (6)",
       "meme position sans Path : 6 cartes (taille de main de Peter Parker)",
       [], [], {"taille_main": 6, "hors_jeu": ["se001"]}, avec_boost=True),
    _c("se005 The Last Ronin choisi au deck-building : un Path HYBRIDE suit le meme chemin (mis en jeu au Setup)",
       "meme mecanisme pour les onze Paths ; le hybride unique est en jeu, hors du deck",
       [], [], {"carte": "se005", "total": 1, "en_jeu": 1, "dans_deck": 0, "en_main": 0},
       verifier="se_exemplaires", deck_ajoute=["se005"]),
]

# ========================================================================= « You get -1 hand size » (les onze)
for _cid, _nom in TOUS:
    CAS.append(_c(f"{_cid} {_nom} : « You get -1 hand size », forme HEROS (Spider-Man 5 -> 4)",
                  "taille de main imprimee moins 1 ; Permanent, aucun script de plus que `GiveKeywordToInPlayWhenApplyThis(\"You\", hand_size=-1)`",
                  [HEROS, _voie(_cid)], [], {"attributs": {"hand_size": -1}, "en_jeu": [_cid]}))
    CAS.append(_c(f"{_cid} {_nom} : « You get -1 hand size » vaut aussi en forme ALTER-EGO (Peter Parker 6 -> 5)",
                  "« You » = les deux formes de l'identite (contrairement a « your hero »)",
                  [_voie(_cid)], [], {"attributs": {"hand_size": -1}}))

CAS += [
    # ===================================================================== se001 Kagemusha
    _c("se001 Kagemusha Shadow Stride : Hero Action, la Voie s'incline et le HEROS est camoufle (Cloaked)",
       "« Hero Action: Exhaust this card -> cloak your hero » : carte d'etat Cloaked sur le heros, Voie inclinee",
       [HEROS, _voie("se001")], ["Puzzle.Action('se001', 'HeroAction', 0)"],
       {"statuts": [["01001a", "Cloaked"]], "exhausted": ["se001"]}),
    _dispo("se001 Kagemusha : TEMOIN D'EPUISEMENT, la Voie inclinee ne propose plus Shadow Stride dans le meme round",
           "« Exhaust this card » est le cout : une fois utilisee, plus aucune Hero Action disponible (le livret dit « once per round »)",
           [HEROS, _voie("se001")], "se001", "HeroAction", 0, declencher=["Puzzle.Action('se001', 'HeroAction', 0)"]),
    _dispo("se001 Kagemusha : Hero Action NON proposee en forme alter-ego",
           "« Hero Action » : seulement quand l'identite est en forme heros",
           [_voie("se001")], "se001", "HeroAction", 0),
    _dispo("se001 Kagemusha : Hero Action proposee en forme heros (avant usage)",
           "temoin positif des deux cas precedents : 1 action disponible",
           [HEROS, _voie("se001")], "se001", "HeroAction", 1),
    _c("se001 Kagemusha : le HEROS gagne le trait NINJA (« Your hero gains the NINJA trait »)",
       "forme heros : NINJA present",
       [HEROS, _voie("se001")], [], {"traits": ["NINJA"]}),
    _c("se001 Kagemusha : « Your HERO gains » : l'ALTER-EGO ne gagne PAS NINJA",
       "contre-cas : forme alter-ego, trait absent (contraste avec « You gain the MYSTIC trait » d'Onmyodo)",
       [_voie("se001")], [], {"traits_absents": ["NINJA"]}),
    _c("se001 Kagemusha : TEMOIN, sans Path le heros n'a pas NINJA",
       "pas de Path, pas de trait (Spider-Man n'est pas NINJA)",
       [HEROS], [], {"traits_absents": ["NINJA"]}),
    _c("se001 Kagemusha : un heros DEJA camoufle ne recoit pas une seconde carte Cloaked",
       "« Unless otherwise specified, a character can only have one Cloaked status card » : le heros est deja camoufle, "
       "Shadow Stride incline quand meme la Voie sans en empiler une seconde",
       [HEROS, _voie("se001"), "Puzzle.Cloak('01001a')"], ["Puzzle.Action('se001', 'HeroAction', 0)"],
       {"statuts": [["01001a", "Cloaked"]], "exhausted": ["se001"]}, verifier="se_un_seul_cloaked"),

    # ===================================================================== se002 Onmyodo
    _c("se002 Onmyodo Insight : regarde les 2 cartes du dessus du deck RENCONTRE, sans rien deplacer",
       "« look at the top 2 cards of any deck and put them back in the same order » : les 2 premieres cartes deviennent visibles du "
       "joueur, la 3e non, le deck garde sa taille et son ordre ; Voie inclinee",
       [HEROS, _voie("se002")], ["Puzzle.Action('se002', 'HeroAction', 0)"],
       {"deck": "rencontre", "vus": 2, "taille": 8, "exhausted": ["se002"]}, verifier="se_a_regarde",
       preferer_option="encounter deck"),
    _c("se002 Onmyodo Insight : regarde les 2 cartes du dessus de SON deck",
       "meme capacite, autre deck : les 2 du dessus du deck du joueur, ordre intact",
       [HEROS, _voie("se002"), "Puzzle.EmptyPlayerDeck()",
        "Puzzle.CreatePlayerDeck('01073', '01074', '01075', '01076', '01077')"],
       ["Puzzle.Action('se002', 'HeroAction', 0)"],
       {"deck": "joueur", "vus": 2, "taille": 5, "exhausted": ["se002"]}, verifier="se_a_regarde",
       preferer_option="your deck"),
    _c("se002 Onmyodo Insight : « ANY deck » comprend le deck d'un AUTRE joueur (partie a deux)",
       "2 joueurs : l'option du deck du second joueur est proposee et regarde SES 2 cartes du dessus",
       [HEROS, _voie("se002")], ["Puzzle.Action('se002', 'HeroAction', 0)"],
       {"deck": "autre", "vus": 2}, verifier="se_a_regarde", heros2="iron_man", preferer_option="'s deck"),
    _dispo("se002 Onmyodo : TEMOIN D'EPUISEMENT, plus d'Insight apres usage dans le meme round",
           "cout = incliner la Voie", [HEROS, _voie("se002")], "se002", "HeroAction", 0,
           declencher=["Puzzle.Action('se002', 'HeroAction', 0)"]),
    _dispo("se002 Onmyodo : Insight (Hero Action) NON proposee en alter-ego",
           "forme heros uniquement", [_voie("se002")], "se002", "HeroAction", 0),
    _c("se002 Onmyodo : « You gain the MYSTIC trait » : l'identite l'a dans les DEUX formes",
       "forme alter-ego : MYSTIC present (« You », pas « your hero »)",
       [_voie("se002")], [], {"traits": ["MYSTIC"]}),
    _c("se002 Onmyodo : TEMOIN, sans Path, pas de trait MYSTIC",
       "Peter Parker n'est pas MYSTIC", [], [], {"traits_absents": ["MYSTIC"]}),

    # ===================================================================== se003 Samurai
    _c("se003 Samurai Way of the Warrior : 2 compteurs samurai retires d'une amelioration OATH -> heros redresse + 1 carte",
       "tj006 Fearless Resolve (OATH, Uses 2 samurai) : « remove a total of 2 samurai counters from among OATH upgrades you control -> "
       "ready your hero and draw 1 card » ; la Voie s'incline, tj006 perd ses 2 compteurs (defaussee, Uses), le heros est pret, main +1",
       [HEROS, _voie("se003"), _voie("tj006"), "Puzzle.Exhaust('01001a')", "Puzzle.EmptyHand()",
        "Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01073', '01074')"],
       ["Puzzle.Action('se003', 'HeroAction', 0)"],
       {"exhausted": ["se003"], "pret": ["01001a"], "taille_main": 1, "defausse": ["tj006"], "hors_jeu": ["tj006"]},
       accepter_choix=True),
    _c("se003 Samurai : la repartition est LIBRE, 2 compteurs pris entre DEUX ameliorations OATH (2+1 -> 1 restant au total)",
       "tj006 (2 compteurs) et une seconde tj006 reduite a 1 compteur : 3 au total, 2 retires, 1 reste ; le choix du joueur est libre",
       [HEROS, _voie("se003"), _voie("tj006"), "Puzzle.PutIntoPlay(Puzzle.CreateCard('tj006'), under_control=True)",
        "Puzzle.Counter('tj006', 'samurai', -1)"],
       ["Puzzle.Action('se003', 'HeroAction', 0)"],
       {"total_restant": 1, "exhausted": ["se003"]}, verifier="se_samurai_total", accepter_choix=True),
    _dispo("se003 Samurai : un SEUL compteur samurai au total -> l'action n'est PAS proposee (cout impayable)",
           "« a total of 2 » : 1 compteur ne suffit pas, meme repartis sur plusieurs cartes",
           [HEROS, _voie("se003"), _voie("tj006"), "Puzzle.Counter('tj006', 'samurai', -1)"],
           "se003", "HeroAction", 0),
    _dispo("se003 Samurai : 1 compteur sur chacune de DEUX ameliorations OATH = 2 au total -> l'action est proposee",
           "le total se compte entre toutes les OATH sous controle (contre-cas du precedent)",
           [HEROS, _voie("se003"), _voie("tj006"), "Puzzle.PutIntoPlay(Puzzle.CreateCard('tj006'), under_control=True)",
            "Puzzle.Counter('tj006', 'samurai', -1)"],
           "se003", "HeroAction", 1),
    _dispo("se003 Samurai : des compteurs samurai sur une amelioration NON OATH ne comptent pas",
           "« among OATH upgrades » : tj008 (Bow, pas OATH) portant 2 compteurs samurai ne paie rien",
           [HEROS, _voie("se003"), _voie("tj008"), "Puzzle.Counter('tj008', 'samurai', 2)"],
           "se003", "HeroAction", 0),
    _dispo("se003 Samurai : TEMOIN D'EPUISEMENT, la Voie inclinee ne propose plus Way of the Warrior",
           "deux ameliorations OATH de 2 compteurs ; apres un usage la Voie est inclinee : plus d'action, malgre les compteurs restants",
           [HEROS, _voie("se003"), _voie("tj006"), "Puzzle.PutIntoPlay(Puzzle.CreateCard('tj006'), under_control=True)"],
           "se003", "HeroAction", 0, declencher=["Puzzle.Action('se003', 'HeroAction', 0)"], accepter_choix=True),
    _dispo("se003 Samurai : Way of the Warrior (Hero Action) NON proposee en alter-ego",
           "forme heros uniquement", [_voie("se003"), _voie("tj006")], "se003", "HeroAction", 0),

    # ===================================================================== se004 Shihan
    _c("se004 Shihan Recenter : a la fin de la phase joueur, 2 cartes du deck defaussees -> 1 Taijutsu de la defausse revient en main",
       "« When the player phase ends, discard the top 2 cards of your deck -> return 1 Taijutsu card from your discard pile to your hand » : "
       "tj004 (Taijutsu) dans la defausse revient, 01090 (non Taijutsu) reste ; deck 4 -> 2",
       [HEROS, _voie("se004"), "Puzzle.EmptyHand()", "Puzzle.EmptyPlayerDeck()",
        "Puzzle.CreatePlayerDeck('01073', '01074', '01075', '01076')",
        "Puzzle.CreatePlayerDiscardPile('01090', 'tj004')"],
       ["Puzzle.EndPlayerPhase()"],
       {"en_main": ["tj004"], "taille_main": 1, "defausse": ["01090", "01076", "01075"], "taille_deck_joueur": 2},
       accepter_choix=True),
    _c("se004 Shihan Recenter : une Taijutsu qui vient d'etre DEFAUSSEE par le cout peut etre rendue (choix APRES le cout)",
       "le dessus du deck est tj004 (la DERNIERE carte de `CreatePlayerDeck`) : le cout la defausse, elle est alors la seule Taijutsu de "
       "la defausse et revient en main",
       [HEROS, _voie("se004"), "Puzzle.EmptyHand()", "Puzzle.EmptyPlayerDeck()",
        "Puzzle.CreatePlayerDeck('01074', '01075', '01076', 'tj004')", "Puzzle.EmptyPlayerDiscardPile()"],
       ["Puzzle.EndPlayerPhase()"],
       {"en_main": ["tj004"], "taille_main": 1, "defausse": ["01076"], "taille_deck_joueur": 2},
       accepter_choix=True),
    _c("se004 Shihan Recenter : aucune Taijutsu a rendre, le cout est paye quand meme et rien ne revient",
       "defausse sans Taijutsu et deck sans Taijutsu : 2 cartes defaussees, main vide",
       [HEROS, _voie("se004"), "Puzzle.EmptyHand()", "Puzzle.EmptyPlayerDeck()",
        "Puzzle.CreatePlayerDeck('01073', '01074', '01075', '01076')", "Puzzle.CreatePlayerDiscardPile('01090')"],
       ["Puzzle.EndPlayerPhase()"],
       {"taille_main": 0, "taille_deck_joueur": 2, "defausse": ["01076", "01075", "01090"]},
       accepter_choix=True),
    _c("se004 Shihan Recenter : TEMOIN, une carte Ninjutsu de la defausse ne revient PAS (seulement Taijutsu)",
       "tj005 (Ninjutsu) dans la defausse : « 1 TAIJUTSU card » exclut les autres types Shinobi",
       [HEROS, _voie("se004"), "Puzzle.EmptyHand()", "Puzzle.EmptyPlayerDeck()",
        "Puzzle.CreatePlayerDeck('01073', '01074', '01075', '01076')", "Puzzle.CreatePlayerDiscardPile('tj005')"],
       ["Puzzle.EndPlayerPhase()"],
       {"absent_main": ["tj005"], "taille_main": 0, "defausse": ["tj005"]},
       accepter_choix=True),
    _c("se004 Shihan Recenter : Hero Interrupt NON disponible en forme alter-ego (le deck n'est pas touche)",
       "« Hero Interrupt » : forme heros seulement ; deck inchange (4)",
       [_voie("se004"), "Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01073', '01074', '01075', '01076')",
        "Puzzle.CreatePlayerDiscardPile('tj004')"],
       ["Puzzle.EndPlayerPhase()"],
       {"taille_deck_joueur": 4, "absent_main": ["tj004"]}, accepter_choix=True),

    # ===================================================================== se005 The Last Ronin
    _c("se005 The Last Ronin Kanpeki : incline la Voie, glisse 1 carte Shinobi de la main DESSOUS, pioche 1",
       "« Action: Exhaust this card and tuck 1 Shinobi card from your hand under here -> draw 1 card » : tj005 (Ninjutsu) glissee sous la "
       "Voie (hors de la main), 1 carte piochee : main 1 (la carte piochee)",
       [HEROS, _voie("se005"), "Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01073', '01074')"],
       ["Puzzle.Action('se005', 'Action', 0)"],
       {"exhausted": ["se005"], "pose_sous": [["se005", "tj005"]], "absent_main": ["tj005"], "taille_main": 1},
       main_exclusive=["tj005"], accepter_choix=True),
    _c("se005 The Last Ronin Kanpeki : seule une carte SHINOBI peut etre glissee (une Dual/classe ; ici Taijutsu, pas 01090)",
       "main = 01090 (Basic) + tj004 (Taijutsu) : c'est tj004 qui part sous la Voie, 01090 reste en main",
       [HEROS, _voie("se005"), "Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01073', '01074')"],
       ["Puzzle.Action('se005', 'Action', 0)"],
       {"pose_sous": [["se005", "tj004"]], "en_main": ["01090"], "taille_main": 2},
       main_exclusive=["01090", "tj004"], accepter_choix=True),
    _dispo("se005 The Last Ronin : aucune carte Shinobi en main -> Kanpeki NON proposee",
           "cout impayable : « tuck 1 SHINOBI card from your hand »", [HEROS, _voie("se005")], "se005", "Action", 0,
           main_exclusive=["01090", "01089"]),
    _dispo("se005 The Last Ronin : « (Max 2 tucked cards) » -> avec 2 cartes deja rangees, Kanpeki NON proposee",
           "plafond de cartes glissees : 2",
           [HEROS, _voie("se005"), "Puzzle.PlaceUnder('tj005', 'se005')", "Puzzle.PlaceUnder('tj005', 'se005')"],
           "se005", "Action", 0, main_exclusive=["tj004"]),
    _dispo("se005 The Last Ronin : avec UNE seule carte rangee, Kanpeki reste proposee (la limite est 2, pas 1)",
           "contre-cas du plafond : 1 < 2",
           [HEROS, _voie("se005"), "Puzzle.PlaceUnder('tj005', 'se005')"],
           "se005", "Action", 1, main_exclusive=["tj004"]),
    _dispo("se005 The Last Ronin : Kanpeki est une ACTION, proposee aussi en forme alter-ego",
           "« Action » (sans Hero) : les deux formes", [_voie("se005")], "se005", "Action", 1,
           main_exclusive=["tj004"]),
    _c("se005 The Last Ronin : une carte glissee sous la Voie se JOUE comme si elle etait en main",
       "« You may play cards tucked here as if they were in your hand » : tj005 Moonlighting (cout 0) glissee sous la Voie, main VIDE, "
       "elle est jouee depuis le dessous de la Voie et finit dans la defausse",
       [HEROS, _voie("se005"), "Puzzle.PlaceUnder('tj005', 'se005')", "Puzzle.EmptyHand()"], [],
       {"defausse": ["tj005"]}, jouer=["tj005"], accepter_choix=True),
    _c("se005 The Last Ronin : TEMOIN, sans la Voie une carte glissee ailleurs ne se joue pas (reste hors de la main)",
       "tj005 glissee sous un autre hote (Spider-Man) : non jouable, elle ne passe pas en defausse",
       [HEROS, "Puzzle.PlaceUnder('tj005', '01001a')", "Puzzle.EmptyHand()"], [],
       {"hors_jeu": ["tj005"]}, jouer=["tj005"], accepter_choix=True),

    # ===================================================================== se006 Yoshimitsu
    _c("se006 Yoshimitsu : « You get +2 hit points » (forme heros, 10 -> 12)",
       "PV max imprimes + 2", [HEROS, _voie("se006")], [], {"attributs": {"health": 2}}),
    _c("se006 Yoshimitsu : +2 PV aussi en forme alter-ego",
       "« You » : les deux formes", [_voie("se006")], [], {"attributs": {"health": 2}}),
    _c("se006 Yoshimitsu Magnificence : 1 degat subi + Voie inclinee -> +1 THW, +1 ATK, +1 DEF",
       "« Take 1 damage and exhaust this card -> you get +1 THW, +1 ATK, and +1 DEF until the end of the round »",
       [HEROS, _voie("se006")], ["Puzzle.Action('se006', 'HeroAction', 0)"],
       {"attributs": {"hand_size": -1, "thwart": 1, "attack": 1, "defense": 1}, "degats_identite": 1, "exhausted": ["se006"]}),
    _c("se006 Yoshimitsu Magnificence : les bonus disparaissent a la FIN DU ROUND (le degat reste)",
       "apres WhenRoundEnd + buff_manager : THW/ATK/DEF a l'imprime ; 1 degat toujours la",
       [HEROS, _voie("se006")], ["Puzzle.Action('se006', 'HeroAction', 0)"],
       {"attributs": {"hand_size": -1, "thwart": 0, "attack": 0, "defense": 0}, "degats_identite": 1},
       verifier="se_apres_fin_de_round"),
    _dispo("se006 Yoshimitsu : TEMOIN D'EPUISEMENT, plus de Magnificence apres usage",
           "cout = incliner la Voie", [HEROS, _voie("se006")], "se006", "HeroAction", 0,
           declencher=["Puzzle.Action('se006', 'HeroAction', 0)"]),
    _dispo("se006 Yoshimitsu : Magnificence (Hero Action) NON proposee en alter-ego",
           "forme heros uniquement", [_voie("se006")], "se006", "HeroAction", 0),

    # ===================================================================== se007 Yamabushi
    _c("se007 Yamabushi Meditate : incline la Voie ET le heros -> pioche 3, defausse 1 carte de la main",
       "« Exhaust this card and your hero -> draw 3 cards. Choose and discard 1 card from your hand » : main 1 + 3 - 1 = 3, 1 carte "
       "defaussee, Voie et heros inclines",
       [HEROS, _voie("se007"), "Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01073', '01074', '01075', '01076')"],
       ["Puzzle.Action('se007', 'HeroAction', 0)"],
       {"exhausted": ["se007", "01001a"], "taille_main": 3, "taille_deck_joueur": 1},
       main_exclusive=["01088"], accepter_choix=True),
    _dispo("se007 Yamabushi : le HEROS deja incline -> Meditate NON proposee (deuxieme cout impayable)",
           "« Exhaust this card AND your hero » : deux couts", [HEROS, _voie("se007"), "Puzzle.Exhaust('01001a')"],
           "se007", "HeroAction", 0),
    _dispo("se007 Yamabushi : heros pret -> Meditate proposee (temoin du cas precedent)",
           "meme position, heros redresse", [HEROS, _voie("se007")], "se007", "HeroAction", 1),
    _dispo("se007 Yamabushi : TEMOIN D'EPUISEMENT, plus de Meditate apres usage",
           "la Voie et le heros sont inclines", [HEROS, _voie("se007"), "Puzzle.EmptyPlayerDeck()",
                                                  "Puzzle.CreatePlayerDeck('01073', '01074', '01075', '01076')"],
           "se007", "HeroAction", 0, declencher=["Puzzle.Action('se007', 'HeroAction', 0)"], accepter_choix=True),
    _c("se007 Yamabushi : « You gain the TEMPORAL trait » (les deux formes)",
       "trait TEMPORAL en alter-ego", [_voie("se007")], [], {"traits": ["TEMPORAL"]}),

    # ===================================================================== se008 Onigari
    _c("se008 Onigari Dark Visions : apres avoir VAINCU un sbire -> Voie inclinee, heros camoufle, 1 carte piochee",
       "« After you defeat a minion or side scheme, exhaust this card -> cloak your hero and draw 1 card » : Hydra Mercenary (1 PV) "
       "vaincu par l'attaque de base du heros",
       [HEROS, _voie("se008"), "Puzzle.PutIntoPlay('01101')", "Puzzle.Damage('01101', 2)", "Puzzle.EmptyHand()",
        "Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01073', '01074')"],
       ["Puzzle.Attack('01001a')"],
       {"hors_jeu": ["01101"], "statuts": [["01001a", "Cloaked"]], "exhausted": ["se008"], "taille_main": 1},
       cibles=["01101"], accepter_choix=True),
    _c("se008 Onigari Dark Visions : apres avoir vaincu un complot ANNEXE -> meme effet",
       "side scheme (1 menace) retire par l'attaque de... un contre du heros : le complot annexe est vaincu",
       [HEROS, _voie("se008"), "Puzzle.EmptyHand()", "Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01073', '01074')",
        "Puzzle.PutIntoPlay('01107')", "Puzzle.SetThreat('01107', 1)"],
       ["Puzzle.Thwart('01001a')"],
       {"hors_jeu": ["01107"], "statuts": [["01001a", "Cloaked"]], "exhausted": ["se008"], "taille_main": 1},
       cibles=["01107"], accepter_choix=True),
    _c("se008 Onigari : TEMOIN, un sbire attaque SANS etre vaincu ne declenche rien",
       "Hydra Mercenary (3 PV) survit a l'attaque de base (1 degat) : pas de camouflage, Voie prete",
       [HEROS, _voie("se008"), "Puzzle.PutIntoPlay('01101')"], ["Puzzle.Attack('01001a')"],
       {"en_jeu": ["01101"], "statuts_absents": [["01001a", "Cloaked"]], "pret": ["se008"]},
       cibles=["01101"], accepter_choix=True),
    _c("se008 Onigari : You gain the PSIONIC trait (les deux formes)",
       "alter-ego : PSIONIC", [_voie("se008")], [], {"traits": ["PSIONIC"]}),

    # ===================================================================== se009 Ashigaru
    _c("se009 Ashigaru Light of Foot : une ressource WILD payant une carte SHINOBI pioche 1 carte",
       "« Hero Resource: Exhaust this card -> generate a [wild] resource. If you paid for a Shinobi card with this resource, draw 1 "
       "card » : tj005 Moonlighting (cout 0 : pas de ressource) ne convient pas ; tj006 Fearless Resolve (cout 1, Bushido) payee par la "
       "Voie : la Voie s'incline et une carte est piochee (main : 0 apres jeu + 1 pioche)",
       [HEROS, _voie("se009"), "Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01073', '01074')"],
       [], {"exhausted": ["se009"], "en_jeu": ["tj006"], "taille_main": 1},
       main_exclusive=["tj006"], jouer=["tj006"], accepter_choix=True),
    _c("se009 Ashigaru : TEMOIN, la ressource de la Voie paye une carte NON Shinobi (Mockingbird, cout 3) : aucune pioche",
       "01083 n'est pas Shinobi : payee par la Voie (1 wild) + 01088 Energy (YY), elle entre en jeu mais aucune carte n'est piochee (main 0)",
       [HEROS, _voie("se009"), "Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01073', '01074')"],
       [], {"exhausted": ["se009"], "en_jeu": ["01083"], "taille_main": 0},
       main_exclusive=["01083", "01088"], jouer=["01083"], accepter_choix=True),
    _c("se009 Ashigaru : TEMOIN, une carte Shinobi payee SANS la Voie (Voie deja inclinee) ne pioche pas",
       "tj006 payee par 01090 Strength (RR) alors que la Voie est inclinee : aucune pioche (main 0), la Voie reste inclinee",
       [HEROS, _voie("se009"), "Puzzle.Exhaust('se009')", "Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01073', '01074')"],
       [], {"exhausted": ["se009"], "en_jeu": ["tj006"], "taille_main": 0},
       main_exclusive=["tj006", "01090"], payer_avec=["01090"], jouer=["tj006"], accepter_choix=True),
    _c("se009 Ashigaru : « You gain the SOLDIER trait » (les deux formes)",
       "alter-ego : SOLDIER", [_voie("se009")], [], {"traits": ["SOLDIER"]}),

    # ===================================================================== se010 Onmitsu
    _c("se010 Onmitsu Gardener : apres un evenement ATTACK, 1 degat subi -> un ennemi est hebete (Dazed)",
       "« After you play an ATTACK or DEFENSE event, take 1 damage -> daze an enemy » : tj004 Decisive Strike (ATTACK) contre Rhino",
       [HEROS, _voie("se010")], [],
       {"statuts": [["01094", "Dazed"]], "degats_identite": 1},
       main_exclusive=["tj004", "01088"], payer_avec=["01088"], jouer=["tj004"], cibles=["01094", "01094"], accepter_choix=True),
    _c("se010 Onmitsu Gardener : apres un evenement DEFENSE (Backflip), 1 degat subi -> un ennemi est hebete",
       "01003 Backflip (DEFENSE, Hero Interrupt) jouee quand Rhino attaque : l'attaque est prevenue, puis la Reponse de la Voie : "
       "1 degat (le cout) et Rhino hebete",
       [HEROS, _voie("se010"), "Puzzle.Exhaust('01001a')"], ["Puzzle.Attack('01094')"],
       {"statuts": [["01094", "Dazed"]], "degats_identite": 1, "defausse": ["01003"]},
       main_exclusive=["01003"], accepter_choix=True),
    _c("se010 Onmitsu : TEMOIN, un evenement ni ATTACK ni DEFENSE ne declenche rien",
       "01089 Genius n'est pas un evenement : aucun degat subi, aucun Dazed",
       [HEROS, _voie("se010")], [],
       {"statuts_absents": [["01094", "Dazed"]], "degats_identite": 0},
       main_exclusive=["01089"], jouer=["01089"], accepter_choix=True),
    _c("se010 Onmitsu : un ennemi deja hebete n'en recoit pas une seconde carte (une seule Dazed)",
       "Rhino deja Dazed : le degat est subi, pas de second Dazed (verifie par le nombre de statuts)",
       [HEROS, _voie("se010"), "Puzzle.Daze('01094')"], [],
       {"statuts": [["01094", "Dazed"]], "degats_identite": 1},
       main_exclusive=["tj004", "01088"], payer_avec=["01088"], jouer=["tj004"], cibles=["01094", "01094"], accepter_choix=True,
       verifier="se_un_seul_dazed"),

    # ===================================================================== se011 Yojimbo
    _c("se011 Yojimbo Bodyguard : Rhino attaque, le HEROS est declare defenseur SANS s'incliner (reste pret), la Voie s'incline",
       "« Hero Interrupt: When an enemy attacks, exhaust this card -> declare your hero as the defender without exhausting them »",
       [HEROS, _voie("se011")], ["Puzzle.Attack('01094')"],
       {"pret": ["01001a"], "exhausted": ["se011"]}, accepter_choix=True),
    _c("se011 Yojimbo : TEMOIN, sans Bodyguard un heros qui defend normalement S'INCLINE",
       "contre-cas du precedent : `Puzzle.Defend` (defense de base) incline le heros ; la Voie est absente",
       [HEROS], ["Puzzle.Defend('01001a', '01094')"],
       {"exhausted": ["01001a"]}),
    _c("se011 Yojimbo : Hero Interrupt NON disponible en forme alter-ego (la Voie reste prete)",
       "« Hero Interrupt » : l'alter-ego encaisse l'attaque sans Bodyguard",
       [_voie("se011")], ["Puzzle.Attack('01094')"],
       {"pret": ["se011"]}, accepter_choix=True),
    _c("se011 Yojimbo : TEMOIN D'EPUISEMENT, une Voie deja inclinee ne declare rien : le heros n'est pas defenseur",
       "Voie inclinee avant l'attaque : pas de Bodyguard ; le heros defend normalement (le pilote declare la defense de base), donc "
       "S'INCLINE (contraste avec le premier cas, ou il reste pret)",
       [HEROS, _voie("se011"), "Puzzle.Exhaust('se011')"], ["Puzzle.Attack('01094')"],
       {"exhausted": ["se011", "01001a"]}, accepter_choix=True),
]

VERIFICATIONS = r'''
def se_classes(monde, aides):
    """`attendu` : carte (en jeu), `oui` (classes que `IsClass` ET `CardFinder(card_class=...)` doivent reconnaitre),
    `non` (classes refusees). Verifie aussi que `CarteShinobi()`-equivalent (4 classes, OU) la retient."""
    from game.card.card_finder import CardFinder
    attendu = aides["cas"]["attendu"]
    face = aides["par_id"](monde, attendu["carte"])
    if face is None:
        return False, f"{attendu['carte']} introuvable en jeu"
    soucis = []
    for classe in attendu["oui"]:
        if not face.IsClass(classe):
            soucis.append(f"IsClass({classe}) devrait etre vrai")
        if not CardFinder(card_class=classe).Check(face):
            soucis.append(f"CardFinder(card_class={classe}) devrait retenir la carte")
        if not CardFinder(card_classes=[classe]).Check(face):
            soucis.append(f"CardFinder(card_classes=[{classe}]) devrait retenir la carte")
    for classe in attendu["non"]:
        if face.IsClass(classe):
            soucis.append(f"IsClass({classe}) devrait etre faux")
        if CardFinder(card_class=classe).Check(face):
            soucis.append(f"CardFinder(card_class={classe}) ne devrait PAS retenir la carte")
    toutes = ["Bushido", "Ninjutsu", "Kuji-Kiri", "Taijutsu"]
    if not CardFinder(card_classes=toutes).Check(face):
        soucis.append("CardFinder(card_classes=<les 4 Shinobi>) devrait retenir la carte (une carte Shinobi)")
    if soucis:
        return False, " ; ".join(soucis)
    return True, f"{attendu['carte']} : classes {attendu['oui']} reconnues, {len(attendu['non'])} classes refusees"


def se_exemplaires(monde, aides):
    """`attendu` : carte, total (exemplaires dans toute la partie), en_jeu, dans_deck (deck du joueur), en_main."""
    attendu = aides["cas"]["attendu"]
    joueur = monde.players[0]
    total = en_jeu = dans_deck = en_main = 0
    for objet in monde.object_manager.card_dict.values():
        face = getattr(objet, "face", None) or objet
        if getattr(getattr(face, "paper", None), "card_id", None) != attendu["carte"]:
            continue
        total += 1
        if face.IsInPlay():
            en_jeu += 1
        if face.card.area is joueur.player_deck:
            dans_deck += 1
        if face.card.area is joueur.hand_cards:
            en_main += 1
    obtenu = {"total": total, "en_jeu": en_jeu, "dans_deck": dans_deck, "en_main": en_main}
    ecarts = [f"{k}={obtenu[k]} (attendu {attendu[k]})" for k in obtenu if k in attendu and obtenu[k] != attendu[k]]
    if ecarts:
        return False, f"{attendu['carte']} : " + ", ".join(ecarts)
    return True, f"{attendu['carte']} : {obtenu}"


def se_actions_disponibles(monde, aides):
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


def se_a_regarde(monde, aides):
    """`attendu` : deck (rencontre|joueur|autre), vus (nombre de cartes du dessus devenues visibles du joueur),
    taille (facultatif), exhausted (Voie). Les `vus` premieres cartes sont visibles, la suivante non, l'ordre est intact."""
    from game.operate.worlds import Worlds
    attendu = aides["cas"]["attendu"]
    joueur = monde.players[0]
    if attendu["deck"] == "rencontre":
        cartes = list(Worlds.GetEncounterDeckCards(monde))
    elif attendu["deck"] == "joueur":
        cartes = list(joueur.player_deck.Get(True))
    else:
        cartes = list(monde.players[1].player_deck.Get(True))
    n = attendu["vus"]
    visibles = [f.card.visible.IsVisible(joueur) for f in cartes]
    if len(cartes) < n + 1:
        return False, f"deck trop court pour la mesure ({len(cartes)} cartes)"
    if not all(visibles[:n]):
        return False, f"les {n} cartes du dessus devraient etre visibles : {visibles[:n + 1]}"
    if visibles[n]:
        return False, f"la carte {n + 1} ne devrait PAS etre visible : {visibles[:n + 1]}"
    if "taille" in attendu and len(cartes) != attendu["taille"]:
        return False, f"le deck a {len(cartes)} cartes (attendu {attendu['taille']}) : une carte a bouge"
    for card_id in attendu.get("exhausted") or []:
        face = aides["par_id"](monde, card_id)
        if face is None or not face.card.IsExhaust():
            return False, f"{card_id} devrait etre inclinee"
    return True, f"deck {attendu['deck']} : {n} cartes du dessus regardees, la suivante non, ordre et taille intacts"


def se_samurai_total(monde, aides):
    """`attendu` : total_restant (compteurs samurai restant sur les ameliorations en jeu), exhausted."""
    attendu = aides["cas"]["attendu"]
    total = 0
    for objet in monde.object_manager.card_dict.values():
        face = getattr(objet, "face", None) or objet
        if face.IsInPlay() and hasattr(face, "GetCounters"):
            try:
                total += face.GetCounters("samurai")
            except Exception:
                pass
    if total != attendu["total_restant"]:
        return False, f"il reste {total} compteur(s) samurai (attendu {attendu['total_restant']})"
    for card_id in attendu.get("exhausted") or []:
        face = aides["par_id"](monde, card_id)
        if face is None or not face.card.IsExhaust():
            return False, f"{card_id} devrait etre inclinee"
    return True, f"{total} compteur(s) samurai restant(s), comme attendu"


def se_apres_fin_de_round(monde, aides):
    """Envoie la fin de round (WhenRoundEnd + buff_manager.OnRoundEnd, comme world.end_round) puis delegue a
    etat_attendu : `attendu` decrit l'etat APRES la fin de round ; on exige AVANT elle un bonus +1/+1/+1 visible."""
    from game.message import Message
    identite = aides["identite"](monde)
    avant = (identite.attack, identite.thwart, identite.defense)
    base = (identite.printed_attack, identite.printed_thwart, identite.printed_defense)
    if avant != tuple(b + 1 for b in base):
        return False, f"avant la fin de round le bonus +1/+1/+1 devrait etre la : {avant} (imprime {base})"
    Message.WhenRoundEnd(monde).Send()
    monde.stat.OnRoundEnd()
    monde.buff_manager.OnRoundEnd()
    ok, msg = etat_attendu(monde, aides)
    return ok, f"bonus avant la fin du round {avant} ; apres : {msg}"


def se_un_seul_cloaked(monde, aides):
    """Le heros porte EXACTEMENT une carte Cloaked (jamais deux) et la Voie est inclinee."""
    attendu = aides["cas"]["attendu"]
    identite = aides["identite"](monde)
    n = identite.cloaked
    if n != 1:
        return False, f"le heros porte {n} carte(s) Cloaked (attendu exactement 1)"
    return etat_attendu(monde, aides)


def se_un_seul_dazed(monde, aides):
    """Rhino porte EXACTEMENT une carte Dazed (jamais deux) ; le reste est delegue a etat_attendu."""
    attendu = aides["cas"]["attendu"]
    rhino = aides["par_id"](monde, "01094")
    n = rhino.dazed
    if n != 1:
        return False, f"Rhino porte {n} carte(s) Dazed (attendu exactement 1)"
    return etat_attendu(monde, aides)
'''
