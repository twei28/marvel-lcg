# Cas test_capacites du heros officiel IRON FIST (Hero Pack MC64EN, set « Iron Fist », 64001a-64012) :
# noms prefixes « [iron_fist] ». Un cas par capacite, sujet = le card_id dans le nom (substituer_pack.py
# filtre dessus). Gabarits PROCESSUS-CARTE : docs/packs/iron_fist_cartes.md. Decisions de l'utilisateur :
# .planning/iron-fist-officiel/lecture-reponses.md.
#
# Rappels de montage :
#  - Iron Fist demarre en ALTER EGO (64001b Danny Rand) ; `Puzzle.ChangeToFace('64001b', '64001a')` le passe
#    en forme HEROS ;
#  - le deck de depart a un `player_deck` VIDE : le harnais le complete (remplir_les_decks_vides) ;
#    `main_exclusive` dit avec QUOI on paie (01088 Energy = YY, 01089 Genius = BB, 01090 Strength = RR) ;
#  - ⚠ en forme heros, la Reponse de 64001a (« After you play a card, place 1 chi counter here ») part a
#    CHAQUE carte jouee par le cas : les comptes de chi l'incluent (« +1 de la Reponse ») ;
#  - Rhino 01094 (14 PV) est le vilain, 01097b son complot principal, 01101 Hydra Mercenary le sbire ;
#  - `choisir_option: ["N"]` force la reponse N a `DeclareNumber` ; `"Cancel"` passe un choix facultatif.
SC = "rhino"
HEROS = "Puzzle.ChangeToFace('64001b', '64001a')"
CIVIL = "Puzzle.ChangeToFace('64001a', '64001b')"
SANS_DECK = "Puzzle.EmptyPlayerDeck()"
SANS_BOOST = ["Puzzle.EmptyEncounterDeck()",
              "Puzzle.CreateEncounterDeck('01105', '01105', '01105', '01105', '01105', '01105', '01105', '01105')"]
COMPLOT = "01097b"
FIN_DE_PHASE = "Puzzle.EndPlayerPhase()"
# ⚠ `main_exclusive` DEFAUSSE la main de depart (pleine de cartes signature, Techniques comprises) APRES
# `mise_en_place` : une defausse construite pour un cas se fait donc dans `declencher`, apres ce vidage.
VIDER_DEFAUSSE = "Puzzle.EmptyPlayerDiscardPile()"


def chi(face, n):
    return f"Puzzle.Counter('{face}', 'chi', {n})"


def en_jeu(*ids):
    return [f"Puzzle.PutIntoPlay('{i}', under_control=True)" for i in ids]


def _c(nom, pourquoi, mise, declencher, attendu, **cle):
    if not cle.pop("avec_boost", False):
        mise = SANS_BOOST + list(mise)
    cas = {"nom": "[iron_fist] " + nom, "pourquoi": pourquoi, "scenario": cle.pop("scenario", SC),
           "heros": cle.pop("heros", "iron_fist"), "mise_en_place": mise, "declencher": declencher,
           "verifier": cle.pop("verifier", "if_etat"), "attendu": attendu}
    cas.update(cle)
    return cas


CAS = [
    # ============================================================ 64001a Iron Fist : Response (Martial Arts Master)
    _c("64001a Iron Fist : Response, jouer une carte pose 1 chi sur l'identite (Feel the Flow jouee -> 1)",
       "« Martial Arts Master — Response: After you play a card, place 1 chi counter here »",
       [HEROS], [], {"en_jeu": ["64010"], "compteurs_identite": [["chi", 1]]},
       main_exclusive=["64010", "01090"], jouer=["64010"]),
    _c("64001a Iron Fist : Response, deux cartes jouees -> 2 chi (une par carte, evenement compris)",
       "« After you play A card » : chaque carte jouee, tout type (amelioration puis evenement Fists of Fury)",
       [HEROS], [], {"compteurs_identite": [["chi", 2]], "degats": [["01094", 3]]},
       main_exclusive=["64010", "64004", "01090"], jouer=["64010", "64004"]),
    _c("64001a Iron Fist : Response ABSENTE en alter ego (Danny joue une carte : 0 chi)",
       "contre-cas dans l'AUTRE forme : la Reponse est imprimee sur la face heros seulement",
       [], [], {"en_jeu": ["64010"], "compteurs_identite": [["chi", 0]]},
       main_exclusive=["64010", "01090"], jouer=["64010"]),
    _c("64001a Iron Fist : une carte MISE en jeu (pas jouee) ne pose pas de chi",
       "« play a card » ≠ « put into play » : PutIntoPlay de Feel the Flow, 0 chi",
       [HEROS, *en_jeu("64010")], [], {"en_jeu": ["64010"], "compteurs_identite": [["chi", 0]]},
       main_exclusive=["01090"]),
    # ============================================================ 64001a : Forced Response (fin de la phase des joueurs)
    _c("64001a Iron Fist : fin de phase des joueurs, 7 chi -> 4, et 3 degats soignes (5 -> 2)",
       "« remove all but 4 chi counters from here and heal 1 damage for each chi counter removed this way »",
       [HEROS, chi("64001a", 7), "Puzzle.Damage('64001a', 5)"], [FIN_DE_PHASE],
       {"compteurs_identite": [["chi", 4]], "degats_identite": 2}, main_exclusive=["01090"]),
    _c("64001a Iron Fist : fin de phase, 3 chi -> rien ne change (3 chi, degats intacts)",
       "« all BUT 4 » : sous 4, rien a retirer, rien a soigner",
       [HEROS, chi("64001a", 3), "Puzzle.Damage('64001a', 5)"], [FIN_DE_PHASE],
       {"compteurs_identite": [["chi", 3]], "degats_identite": 5}, main_exclusive=["01090"]),
    _c("64001a Iron Fist : fin de phase en ALTER EGO, 7 chi restent 7 (capacite de la face heros)",
       "contre-cas dans l'AUTRE forme : Danny Rand ne porte pas la Reponse forcee",
       [chi("64001b", 7), "Puzzle.Damage('64001b', 5)"], [FIN_DE_PHASE],
       {"compteurs_identite": [["chi", 7]], "degats_identite": 5}, main_exclusive=["01090"]),
    _c("64001a Iron Fist : les chi RESTENT sur l'identite au retournement (3 chi en heros -> 3 en Danny)",
       "decision utilisateur n°5 (Rules Reference : le personnage garde ses jetons au changement de forme)",
       [HEROS, chi("64001a", 3), CIVIL], [], {"compteurs_identite": [["chi", 3]], "forme": "AlterEgo"},
       main_exclusive=["01090"]),
    _c("64001a Iron Fist : valeurs imprimees PV 10, ATQ 2, CTR 1, DEF 2, main 5, traits",
       "nombres texte <-> code (scan 1A) : HAND SIZE 5 / HIT POINTS 10, THW 1, ATK 2, DEF 2",
       [HEROS], [],
       {"attrs": [["64001a", "max_health", 10], ["64001a", "attack", 2], ["64001a", "thwart", 1],
                  ["64001a", "defense", 2], ["64001a", "hand_size", 5]],
        "traits": ["DEFENDER", "K'UN-LUN", "MARTIAL ARTIST"]}, main_exclusive=["01090"]),
    # ============================================================ 64001b Danny Rand : « Your Technique cards lose temporary »
    _c("64001b Danny Rand : une Technique en jeu sous Danny n'est PAS defaussee a la fin du round",
       "« Your Technique cards lose temporary » : ProcessTemporary (fin de round) laisse Feel the Flow en jeu",
       [*en_jeu("64010")], [], {"en_jeu": ["64010"]}, main_exclusive=["01090"], verifier="if_fin_de_round"),
    _c("64001b Danny Rand : en forme HEROS, la Technique redevient Temporary et part a la fin du round",
       "contre-cas dans l'AUTRE forme : la capacite continue est sur la face Danny Rand seulement",
       [HEROS, *en_jeu("64010")], [], {"hors_jeu": ["64010"]}, main_exclusive=["01090"],
       verifier="if_fin_de_round"),
    _c("64001b Danny Rand : Technique posee sous Danny puis retournement en heros -> defaussee a la fin du round",
       "decision utilisateur n°2 : au retournement, les Techniques redeviennent Temporary (lecture litterale)",
       [*en_jeu("64010"), HEROS], [], {"hors_jeu": ["64010"], "forme": "Hero"}, main_exclusive=["01090"],
       verifier="if_fin_de_round"),
    _c("64001b Danny Rand : une carte Temporary SANS le trait Technique part quand meme (Move in Shadow 60027)",
       "« YOUR TECHNIQUE cards » : seul le trait compte ; 60027 (Temporary, SKILL) est defaussee sous Danny",
       [*en_jeu("60027", "64010")], [], {"hors_jeu": ["60027"], "en_jeu": ["64010"]}, main_exclusive=["01090"],
       verifier="if_fin_de_round"),
    _c("64001b Danny Rand : les cinq Techniques en jeu sous Danny restent toutes a la fin du round",
       "chaque Technique du pack (64008-64012) porte le trait TECHNIQUE et Temporary",
       [*en_jeu("64008", "64009", "64010", "64011", "64012")], [],
       {"en_jeu": ["64008", "64009", "64010", "64011", "64012"]}, main_exclusive=["01090"],
       verifier="if_fin_de_round"),
    # ============================================================ 64001b : Meditation
    _c("64001b Meditation : trouve une Technique dans le DECK et la met en jeu, attachee a l'identite",
       "« Search your deck and discard pile for a Technique card. Put that card into play » (decision n°1 : identite)",
       [SANS_DECK, "Puzzle.CreatePlayerDeck('01090', '64011', '01088')"], [VIDER_DEFAUSSE, "Puzzle.Action('64001b', 'Action')"],
       {"en_jeu": ["64011"], "accroche_a": [["64011", "64001b"]], "dans_deck_joueur": ["01090", "01088"]},
       main_exclusive=["01089"]),
    _c("64001b Meditation : trouve une Technique dans la DEFAUSSE (deck sans Technique)",
       "« deck AND discard pile » : 64009 est dans la defausse, rien dans le deck",
       [SANS_DECK, "Puzzle.CreatePlayerDeck('01090', '01088')"],
       [VIDER_DEFAUSSE, "Puzzle.CreatePlayerDiscardPile('64009')", "Puzzle.Action('64001b', 'Action')"],
       {"en_jeu": ["64009"], "accroche_a": [["64009", "64001b"]]},
       main_exclusive=["01089"]),
    _c("64001b Meditation : une amelioration SANS le trait Technique n'est pas trouvee (Book of the Iron Fist)",
       "« a TECHNIQUE card » : le Livre (ITEM) reste dans le deck",
       [SANS_DECK, "Puzzle.CreatePlayerDeck('01090', '64007')"], [VIDER_DEFAUSSE, "Puzzle.Action('64001b', 'Action')"],
       {"hors_jeu": ["64007"], "dans_deck_joueur": ["64007"]}, main_exclusive=["01089"]),
    _c("64001b Meditation : limite 1 par phase (TEMOIN D'EPUISEMENT) : deux Techniques disponibles, une seule en jeu",
       "« (Limit once per phase.) » : 1re Action = 1 Technique ; la 2e est refusee : 1 Technique en jeu et non 2",
       [SANS_DECK, "Puzzle.CreatePlayerDeck('64010', '64011')"], [VIDER_DEFAUSSE, "Puzzle.Action('64001b', 'Action')"],
       {"techniques_en_jeu": 1}, main_exclusive=["01089"],
       declencher_tolerant=["Puzzle.Action('64001b', 'Action')"]),
    _c("64001b Meditation : absente en forme HEROS (aucune Technique mise en jeu)",
       "contre-cas : l'Action est imprimee sur la face Danny Rand",
       [HEROS, SANS_DECK, "Puzzle.CreatePlayerDeck('64010')"], [], {"techniques_en_jeu": 0}, main_exclusive=["01089"],
       declencher_tolerant=["Puzzle.Action('64001a', 'Action')"]),
    _c("64001b Danny Rand : valeurs imprimees PV 10, REC 4, main 6, trait CIVILIAN",
       "nombres texte <-> code (scan 1B) : HAND SIZE 6 / HIT POINTS 10, REC 4",
       [], [], {"attrs": [["64001b", "max_health", 10], ["64001b", "recover", 4], ["64001b", "hand_size", 6]],
                "traits": ["CIVILIAN"]}, main_exclusive=["01090"]),
    # ============================================================ 64002 Deep Breathing
    _c("64002 Deep Breathing : defausse jusqu'a une carte Iron Fist et l'ajoute a la main",
       "deck (dessus -> bas) : 01089, 01088, 64010 : 01089 et 01088 defaussees, 64010 (set Iron Fist) en main",
       [HEROS, SANS_DECK, "Puzzle.CreatePlayerDeck('01090', '64010', '01088', '01089')"], [],
       {"main_ids": ["64010"], "defausse_avec": ["01089", "01088", "64002"], "dans_deck_joueur": ["01090"]},
       main_exclusive=["64002"], jouer=["64002"]),
    _c("64002 Deep Breathing : une carte signature d'un AUTRE heros ne l'arrete pas (62004 Knuckle Sandwich)",
       "« an IRON FIST card » = le set Iron Fist (bandeau IRON FIST), pas « une carte de heros » : 62004 est traversee",
       [HEROS, SANS_DECK, "Puzzle.CreatePlayerDeck('01090', '64011', '62004')"], [],
       {"main_ids": ["64011"], "defausse_avec": ["62004", "64002"], "dans_deck_joueur": ["01090"]},
       main_exclusive=["64002"], jouer=["64002"]),
    _c("64002 Deep Breathing : aucune carte Iron Fist -> tout le deck est defausse, rien en main",
       "decision utilisateur n°4 (« until » au pied de la lettre) ; deck epuise : regle du moteur (remelange)",
       [HEROS, SANS_DECK, "Puzzle.CreatePlayerDeck('01090', '01088', '01089')"], [],
       {"main_ids": []}, main_exclusive=["64002"], jouer=["64002"]),
    _c("64002 Deep Breathing : la carte Iron Fist est la DERNIERE du deck -> en main quand meme",
       "piege DiscardUntil (venus) : le deck epuise remelange la defausse, la carte trouvee est rendue",
       [HEROS, SANS_DECK, "Puzzle.CreatePlayerDeck('64012', '01088')"], [],
       {"main_ids": ["64012"]}, main_exclusive=["64002"], jouer=["64002"]),
    _c("64002 Deep Breathing : Hero Action, injouable en alter ego",
       "contre-cas dans l'AUTRE forme",
       [], [], {"jouable": [["64002", False]]}, main_exclusive=["64002"], verifier="if_jouable"),
    # ============================================================ 64003 Dragon Punch
    _c("64003 Dragon Punch : X = 0 -> 2 degats, chi intacts (4 ; +1 de la Reponse = 5), pas sonne",
       "« Deal 2 damage to an enemy. You MAY remove up to 5 » : rien retire",
       [HEROS, chi("64001a", 4)], [],
       {"degats": [["01094", 2]], "compteurs_identite": [["chi", 5]], "statuts_absents": [["01094", "Stunned"]]},
       main_exclusive=["64003", "01088"], jouer=["64003"], choisir_option=["0"]),
    _c("64003 Dragon Punch : X = 2 -> 6 degats, 2 chi retires (4 -> 2, +1 = 3), PAS sonne (< 3)",
       "« 2 additional damage for each » ; « at least 3 » non atteint",
       [HEROS, chi("64001a", 4)], [],
       {"degats": [["01094", 6]], "compteurs_identite": [["chi", 3]], "statuts_absents": [["01094", "Stunned"]]},
       main_exclusive=["64003", "01088"], jouer=["64003"], choisir_option=["2"]),
    _c("64003 Dragon Punch : X = 3 -> 8 degats ET sonne (« at least 3 », 3 compris)",
       "seuil inclusif : 3 compteurs retires suffisent",
       [HEROS, chi("64001a", 4)], [],
       {"degats": [["01094", 8]], "compteurs_identite": [["chi", 2]], "statuts": [["01094", "Stunned"]]},
       main_exclusive=["64003", "01088"], jouer=["64003"], choisir_option=["3"]),
    _c("64003 Dragon Punch : 7 chi, X plafonne a 5 -> 12 degats, 2 chi restent (+1 = 3), sonne",
       "« UP TO 5 » : on retire 5 au plus ; 6 n'est pas propose (le pilote prend 5, le maximum offert)",
       [HEROS, chi("64001a", 7)], [],
       {"degats": [["01094", 12]], "compteurs_identite": [["chi", 3]], "statuts": [["01094", "Stunned"]]},
       main_exclusive=["64003", "01088"], jouer=["64003"], choisir_option=["5"]),
    _c("64003 Dragon Punch : sans chi -> 2 degats (aucun choix)",
       "0 compteur : X ne peut valoir que 0",
       [HEROS], [], {"degats": [["01094", 2]], "compteurs_identite": [["chi", 1]]},
       main_exclusive=["64003", "01088"], jouer=["64003"]),
    # ============================================================ 64004 Fists of Fury
    _c("64004 Fists of Fury : trois fois 1 degat -> 3 degats sur Rhino (seul ennemi)",
       "trois « Deal 1 damage to an enemy » : 1 + 1 + 1",
       [HEROS], [], {"degats": [["01094", 3]]}, main_exclusive=["64004", "01090"], jouer=["64004"]),
    _c("64004 Fists of Fury : cibles independantes : Tiger Shark a 1 PV tombe au 1er coup, Rhino prend les deux autres",
       "trois choix de cible independants (le pilote vise Tiger Shark tant qu'il est la) : 1er coup sur 01131 (vaincu), "
       "2e et 3e sur Rhino ; un sbire a Garde (01101) interdirait Rhino",
       [HEROS, "Puzzle.PutIntoPlay('01131')", "Puzzle.Damage('01131', 5)"], [],
       {"hors_jeu": ["01131"], "degats": [["01094", 2]]},
       main_exclusive=["64004", "01090"], jouer=["64004"], cibles=["01131", "01094"]),
    # ============================================================ 64005 The Way of Things
    _c("64005 The Way of Things : 2 menaces retirees, choix facultatif refuse (chi intacts : 2, +1 = 3)",
       "« Remove 2 threat from a scheme. You MAY ... »",
       [HEROS, f"Puzzle.SetThreat('{COMPLOT}', 6)", chi("64001a", 2)], [],
       {"menace": [[COMPLOT, 4]], "compteurs_identite": [["chi", 3]]},
       main_exclusive=["64005", "01089"], jouer=["64005"], cibles=[COMPLOT], choisir_option=["Cancel"]),
    _c("64005 The Way of Things : choix accepte : 2 chi retires -> 2 menaces de plus (meme manigance 6 -> 2)",
       "decision n°3 : la seconde « a scheme » peut etre la meme ; 2 chi depenses (2 -> 0, +1 = 1)",
       [HEROS, f"Puzzle.SetThreat('{COMPLOT}', 6)", chi("64001a", 2)], [],
       {"menace": [[COMPLOT, 2]], "compteurs_identite": [["chi", 1]]},
       main_exclusive=["64005", "01089"], jouer=["64005"], cibles=[COMPLOT, COMPLOT], accepter_choix=True),
    _c("64005 The Way of Things : 1 seul chi -> la branche n'est pas offerte (4 menaces, chi 1, +1 = 2)",
       "le retrait des 2 compteurs est le prix de la seconde menace : impayable a 1",
       [HEROS, f"Puzzle.SetThreat('{COMPLOT}', 6)", chi("64001a", 1)], [],
       {"menace": [[COMPLOT, 4]], "compteurs_identite": [["chi", 2]]},
       main_exclusive=["64005", "01089"], jouer=["64005"], cibles=[COMPLOT, COMPLOT], accepter_choix=True),
    # ============================================================ 64006 Lei Kung
    _c("64006 Lei Kung : incline + 1 chi -> pioche 1 carte (main 1 -> 2, chi 1 -> 0)",
       "« Exhaust Lei Kung AND remove 1 chi counter from your identity → draw 1 card »",
       [HEROS, chi("64001a", 1), *en_jeu("64006")], ["Puzzle.Action('64006', 'Action')"],
       {"taille_main": 2, "compteurs_identite": [["chi", 0]], "exhausted": ["64006"]}, main_exclusive=["01090"]),
    _c("64006 Lei Kung : sans chi, l'Action est refusee (main 1, Lei Kung pret)",
       "cout a deux parties : sans compteur, rien",
       [HEROS, *en_jeu("64006")], [], {"taille_main": 1, "pret": ["64006"]}, main_exclusive=["01090"],
       declencher_tolerant=["Puzzle.Action('64006', 'Action')"]),
    _c("64006 Lei Kung : utilisable en ALTER EGO (« Action » nue, chi de l'identite Danny)",
       "« your identity » : Danny Rand porte le stock",
       [chi("64001b", 1), *en_jeu("64006")], ["Puzzle.Action('64006', 'Action')"],
       {"taille_main": 2, "compteurs_identite": [["chi", 0]]}, main_exclusive=["01090"]),
    # ============================================================ 64007 Book of the Iron Fist
    _c("64007 Book of the Iron Fist : Technique au sommet de la defausse -> mise en jeu sur l'identite, Livre incline",
       "« Exhaust this card → if the top card of your discard pile is a Technique, put it into play »",
       [HEROS, *en_jeu("64007")],
       [VIDER_DEFAUSSE, "Puzzle.CreatePlayerDiscardPile('01088', '64011')", "Puzzle.Action('64007', 'HeroAction')"],
       {"en_jeu": ["64011"], "accroche_a": [["64011", "64001a"]], "exhausted": ["64007"]}, main_exclusive=["01090"]),
    _c("64007 Book of the Iron Fist : la Technique n'est pas AU SOMMET -> rien (Livre incline quand meme)",
       "« the TOP card » seulement : 64011 sous 01088",
       [HEROS, *en_jeu("64007")],
       [VIDER_DEFAUSSE, "Puzzle.CreatePlayerDiscardPile('64011', '01088')", "Puzzle.Action('64007', 'HeroAction')"],
       {"hors_jeu": ["64011"], "exhausted": ["64007"]}, main_exclusive=["01090"]),
    _c("64007 Book of the Iron Fist : Hero Action, absente en alter ego (Technique au sommet, rien en jeu)",
       "contre-cas dans l'AUTRE forme",
       [*en_jeu("64007")], [VIDER_DEFAUSSE, "Puzzle.CreatePlayerDiscardPile('64011')"],
       {"hors_jeu": ["64011"], "pret": ["64007"]}, main_exclusive=["01090"],
       declencher_tolerant=["Puzzle.Action('64007', 'HeroAction')"]),
    # ============================================================ 64008 Channel the Iron Fist
    _c("64008 Channel the Iron Fist : attaque de BASE + 1 chi -> +2 (2 + 2 = 4 degats), chi 0",
       "« increase ... by 1 (by 2 INSTEAD if it is a basic attack) »",
       [HEROS, chi("64001a", 1), *en_jeu("64008")], ["Puzzle.Attack('64001a')"],
       {"degats": [["01094", 4]], "compteurs_identite": [["chi", 0]]}, main_exclusive=["01090"]),
    _c("64008 Channel the Iron Fist : evenement d'attaque (Haymaker 3) + 1 chi -> +1 (4 degats)",
       "attaque qui n'est PAS de base : +1 seulement",
       [HEROS, chi("64001a", 1), *en_jeu("64008")], [],
       {"degats": [["01094", 4]], "compteurs_identite": [["chi", 1]]},
       main_exclusive=["01087", "01088"], jouer=["01087"]),
    _c("64008 Channel the Iron Fist : Fists of Fury + 3 chi -> 3 declenchements, 3 chi, 6 degats (Q1 tranchee)",
       "decision utilisateur du 20/10/2026 (Q1) : chaque « Deal 1 damage » est une attaque distincte (ruling des "
       "cartes a phrases repetees, Dance of Death) : Channel part a chacune, 2 + 2 + 2 ; chi 3 -> 0, +1 Reponse = 1",
       [HEROS, chi("64001a", 3), *en_jeu("64008")], [],
       {"degats": [["01094", 6]], "compteurs_identite": [["chi", 1]]},
       main_exclusive=["64004", "01090"], jouer=["64004"]),
    _c("64008 Channel the Iron Fist : sans chi, rien (attaque de base : 2 degats)",
       "cout impayable : l'Interruption n'est pas offerte",
       [HEROS, *en_jeu("64008")], ["Puzzle.Attack('64001a')"], {"degats": [["01094", 2]]}, main_exclusive=["01090"]),
    # ============================================================ 64009 Embody the Dragon
    _c("64009 Embody the Dragon : 2 chi SUR LA CARTE -> Iron Fist a riposte 2",
       "« Iron Fist gains retaliate X, X = chi counters on this card »",
       [HEROS, *en_jeu("64009"), chi("64009", 2)], [], {"attrs": [["64001a", "retaliate", 2]]},
       main_exclusive=["01090"]),
    _c("64009 Embody the Dragon : Hero Action deplace 1 chi de l'identite vers la carte (2/0 -> 1/1, riposte 1)",
       "« MOVE 1 chi counter from Iron Fist to this card » : il part de l'identite ET arrive sur la carte",
       [HEROS, *en_jeu("64009"), chi("64001a", 2)], ["Puzzle.Action('64009', 'HeroAction')"],
       {"compteurs_identite": [["chi", 1]], "compteurs": [["64009", "chi", 1]], "attrs": [["64001a", "retaliate", 1]]},
       main_exclusive=["01090"]),
    _c("64009 Embody the Dragon : Rhino attaque Iron Fist (riposte 2) -> Rhino subit 2 degats",
       "la riposte mord vraiment : 2 chi sur la carte, attaque de Rhino",
       [HEROS, *en_jeu("64009"), chi("64009", 2)], ["Puzzle.Attack('01094')"],
       {"degats": [["01094", 2]]}, main_exclusive=["01090"]),
    _c("64009 Embody the Dragon : en ALTER EGO, Danny Rand n'a PAS de riposte (2 chi sur la carte)",
       "« IRON FIST gains » : le nom de la face heros, pas « you » (RECETTES §3, contre-cas dans l'autre forme)",
       [*en_jeu("64009"), chi("64009", 2)], [], {"attrs": [["64001b", "retaliate", 0]]}, main_exclusive=["01090"]),
    _c("64009 Embody the Dragon : sans chi sur l'identite, l'Action n'est pas offerte (0 sur la carte)",
       "rien a deplacer",
       [HEROS, *en_jeu("64009")], [], {"compteurs": [["64009", "chi", 0]], "attrs": [["64001a", "retaliate", 0]]},
       main_exclusive=["01090"], declencher_tolerant=["Puzzle.Action('64009', 'HeroAction')"]),
    # ============================================================ 64010 Feel the Flow
    _c("64010 Feel the Flow : 1 chi -> 1 menace retiree (5 -> 4), chi 0",
       "« Remove 1 chi counter from Iron Fist → remove 1 threat from a scheme »",
       [HEROS, f"Puzzle.SetThreat('{COMPLOT}', 5)", chi("64001a", 1), *en_jeu("64010")],
       ["Puzzle.Action('64010', 'HeroAction')"],
       {"menace": [[COMPLOT, 4]], "compteurs_identite": [["chi", 0]]}, main_exclusive=["01090"], cibles=[COMPLOT]),
    _c("64010 Feel the Flow : sans chi, refuse (menace 5)",
       "cout impayable",
       [HEROS, f"Puzzle.SetThreat('{COMPLOT}', 5)", *en_jeu("64010")], [],
       {"menace": [[COMPLOT, 5]]}, main_exclusive=["01090"],
       declencher_tolerant=["Puzzle.Action('64010', 'HeroAction')"]),
    # ============================================================ 64011 Keep 'Em Coming
    _c("64011 Keep 'Em Coming : 2 chi -> Iron Fist incline est redresse, chi 0",
       "« Remove 2 chi counters from Iron Fist → ready him »",
       [HEROS, chi("64001a", 2), *en_jeu("64011"), "Puzzle.Exhaust('64001a')"],
       ["Puzzle.Action('64011', 'HeroAction')"],
       {"pret": ["64001a"], "compteurs_identite": [["chi", 0]]}, main_exclusive=["01090"]),
    _c("64011 Keep 'Em Coming : 1 seul chi -> refuse, Iron Fist reste incline",
       "cout de 2 impayable a 1",
       [HEROS, chi("64001a", 1), *en_jeu("64011"), "Puzzle.Exhaust('64001a')"], [],
       {"exhausted": ["64001a"], "compteurs_identite": [["chi", 1]]}, main_exclusive=["01090"],
       declencher_tolerant=["Puzzle.Action('64011', 'HeroAction')"]),
    # ============================================================ 64012 Redirect Chi
    _c("64012 Redirect Chi : 2 chi paient Book of the Iron Fist (cout 2) a eux seuls (chi 0, +1 = 1)",
       "« Remove 2 chi counters from Iron Fist → generate [wild][wild] » : main = le Livre seul",
       [HEROS, chi("64001a", 2), *en_jeu("64012")], [],
       {"en_jeu": ["64007"], "compteurs_identite": [["chi", 1]]}, main_exclusive=["64007"], jouer=["64007"]),
    _c("64012 Redirect Chi : 1 seul chi -> pas de ressource, le Livre reste en main",
       "cout de 2 impayable : la ressource n'est pas offerte",
       [HEROS, chi("64001a", 1), *en_jeu("64012")], [],
       {"hors_jeu": ["64007"], "compteurs_identite": [["chi", 1]]}, main_exclusive=["64007"], jouer=["64007"]),
    _c("64012 Redirect Chi : Hero Resource, absente en alter ego (2 chi, le Livre reste en main)",
       "contre-cas dans l'AUTRE forme",
       [chi("64001b", 2), *en_jeu("64012")], [],
       {"hors_jeu": ["64007"], "compteurs_identite": [["chi", 2]]}, main_exclusive=["64007"], jouer=["64007"]),
]


VERIFICATIONS = r'''
CLES_IRON_FIST = {'main_ids', 'attrs', 'techniques_en_jeu', 'defausse_avec'}


def if_etat(monde, aides):
    """etat_attendu + cles propres : main_ids (ensemble exact de la main), attrs [[card_id, attribut, valeur]],
    techniques_en_jeu (nombre exact de cartes TECHNIQUE en jeu), defausse_avec (card_id presents dans la defausse)."""
    cas = aides["cas"]
    attendu = dict(cas.get("attendu") or {})
    propres = {k: attendu.pop(k) for k in list(attendu) if k in CLES_IRON_FIST}
    j = monde.players[0]
    soucis = []
    if "main_ids" in propres:
        vu = sorted(getattr(f.paper, "card_id", "?") for f in j.hand_cards.GetAll())
        if vu != sorted(propres["main_ids"]):
            soucis.append(f"main = {vu} (attendu {sorted(propres['main_ids'])})")
    if "defausse_avec" in propres:
        pile = [getattr(f.paper, "card_id", "?") for f in j.discard_pile.Get()]
        for cid in propres["defausse_avec"]:
            if cid not in pile:
                soucis.append(f"{cid} absent de la defausse (defausse = {pile})")
    for cid, attr, voulu in propres.get("attrs") or []:
        face = aides["par_id"](monde, cid)
        if face is None:
            soucis.append(f"{cid} introuvable en jeu (attrs)")
        elif getattr(face, attr) != voulu:
            soucis.append(f"{cid}.{attr} = {getattr(face, attr)} (attendu {voulu})")
    if "techniques_en_jeu" in propres:
        n = 0
        for objet in monde.object_manager.card_dict.values():
            face = objet.face
            if face is not None and face.IsInPlay() and face.HasTrait("TECHNIQUE"):
                n += 1
        if n != propres["techniques_en_jeu"]:
            soucis.append(f"{n} Technique(s) en jeu (attendu {propres['techniques_en_jeu']})")
    sauvegarde = cas["attendu"]
    cas["attendu"] = attendu
    try:
        ok, msg = etat_attendu(monde, aides)
    finally:
        cas["attendu"] = sauvegarde
    if not ok:
        soucis.append(msg)
    if soucis:
        return False, " ; ".join(soucis)
    return True, msg


def if_fin_de_round(monde, aides):
    """Joue la defausse de fin de round du moteur (`ProcessTemporary`, world.py) puis if_etat."""
    from game.effect.rule import GameRule
    monde.ProcessTemporary(GameRule(monde.const_players[0].GetIdentity()))
    return if_etat(monde, aides)


def if_jouable(monde, aides):
    """`attendu.jouable` = [[card_id, bool]] : la carte EN MAIN est-elle jouable (`CanPlayBy`) ?"""
    soucis = []
    j = monde.players[0]
    for cid, voulu in aides["cas"]["attendu"]["jouable"]:
        main = [f for f in j.hand_cards.GetAll() if getattr(f.paper, "card_id", None) == cid]
        if not main:
            soucis.append(f"{cid} absente de la main")
            continue
        vu = bool(main[0].CanPlayBy(j))
        if vu != voulu:
            soucis.append(f"{cid} jouable={vu} (attendu {voulu})")
    if soucis:
        return False, " ; ".join(soucis)
    return True, "jouabilite conforme"
'''
