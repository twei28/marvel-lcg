# Cas test_capacites du heros QUASAR (Galactic Storm, Kajislav, lot GS-2) : noms prefixes « [quasar] ».
# Un cas par capacite, sujet = le card_id dans le nom (substituer_pack.py filtre dessus). Gabarits
# PROCESSUS-CARTE : .planning/galactic-storm/QUASAR-GABARITS.md. Questions : .planning/todos/2026-10-20-gs2-questions.md.
#
# Rappels de montage :
#  - Quasar demarre en ALTER EGO (gs300b Wendell Vaughn), Quantum Bands (gs301) deja en jeu (Setup) ;
#    `HEROS` le passe en forme heros ;
#  - le deck de depart est la decklist de l'auteur (officielles) : `main_exclusive` dit avec QUOI on paie
#    (01088 Energy = YY, 01089 Genius = BB, 01090 Strength = RR ; gs311 Quantum Energy = 1 joker,
#    gs309 Unbreakable Guard = 1 [mental]) ; les Bandes (pretes) sont un moyen de paiement de plus :
#    `BANDES_INCLINEES` les retire du paiement ;
#  - Rhino 01094 (14 PV), 01097b son complot (seuil 7 : ne jamais y poser 7), 01103 Shocker (3 PV),
#    01102 Sandman (4 PV, Tenace a l'entree), 01108 Crowd Control (Crise), 01109 Bomb Scare (manigance
#    annexe sans crise), 16119 Badoon Lieutenant (Patrouille) ;
#  - `SANS_BOOST` remplit le deck rencontre de « I'm Tough » 01105 (aucune icone de boost).
SC = "rhino"
HEROS = "Puzzle.ChangeToFace('gs300b', 'gs300a')"
BANDES_INCLINEES = "Puzzle.Exhaust('gs301')"
QUASAR_INCLINE = "Puzzle.Exhaust('gs300a')"
SANS_BOOST = ["Puzzle.EmptyEncounterDeck()",
              "Puzzle.CreateEncounterDeck('01105', '01105', '01105', '01105', '01105', '01105')"]
COMPLOT = "01097b"


def menace(n, sur=COMPLOT):
    return f"Puzzle.SetThreat('{sur}', {n})"


def en_jeu(*ids):
    return [f"Puzzle.PutIntoPlay('{i}', under_control=True)" for i in ids]


def _c(nom, pourquoi, mise, declencher, attendu, **cle):
    if not cle.pop("avec_boost", False):
        mise = SANS_BOOST + list(mise)
    cas = {"nom": "[quasar] " + nom, "pourquoi": pourquoi, "scenario": cle.pop("scenario", SC),
           "heros": cle.pop("heros", "quasar"), "mise_en_place": mise, "declencher": declencher,
           "verifier": cle.pop("verifier", "qz_etat"), "attendu": attendu}
    cas.update(cle)
    return cas


CAS = [
    # ================================================================== gs300a Quasar (face heros)
    _c("gs300a Quasar : valeurs imprimees PV 11, ATQ 2, CTR 2, DEF 2, main 5, trait GUARDIAN",
       "nombres texte <-> code (scan 1A) : THW 2, ATK 2, DEF 2, HAND SIZE 5 / HIT POINTS 11",
       [HEROS], [],
       {"attrs": [["gs300a", "max_health", 11], ["gs300a", "attack", 2], ["gs300a", "thwart", 2],
                  ["gs300a", "defense", 2], ["gs300a", "hand_size", 5]],
        "traits": ["GUARDIAN"]}, main_exclusive=["01090"]),
    _c("gs300a Channel the Bands : Bandes inclinees -> l'Action incline Quasar et redresse les Bandes",
       "« Action: Exhaust Quasar → ready Quantum Bands »",
       [HEROS, BANDES_INCLINEES], ["Puzzle.Action('gs300a', 'Action')"],
       {"pret": ["gs301"], "exhausted": ["gs300a"]}, main_exclusive=["01090"]),
    _c("gs300a Channel the Bands : Bandes deja pretes -> Action non offerte, Quasar reste pret",
       "condition : l'effet ne changerait rien (contre-cas d'absence, vert aussi sans module)",
       [HEROS], [], {"pret": ["gs301", "gs300a"]}, main_exclusive=["01090"],
       declencher_tolerant=["Puzzle.Action('gs300a', 'Action')"]),
    _c("gs300a Channel the Bands : absente en ALTER EGO (Wendell ne redresse pas les Bandes)",
       "contre-cas : l'Action est imprimee sur la face heros",
       [BANDES_INCLINEES], [], {"exhausted": ["gs301"], "forme": "AlterEgo"}, main_exclusive=["01090"],
       declencher_tolerant=["Puzzle.Action('gs300b', 'Action')"]),
    # ================================================================== gs300b Wendell Vaughn
    _c("gs300b Wendell Vaughn : valeurs imprimees PV 11, REC 3, main 6, trait S.H.I.E.L.D",
       "nombres texte <-> code (scan 1B) : REC 3, HAND SIZE 6 / HIT POINTS 11",
       [], [], {"attrs": [["gs300b", "max_health", 11], ["gs300b", "recover", 3], ["gs300b", "hand_size", 6]],
                "traits": ["S.H.I.E.L.D"]}, main_exclusive=["01090"]),
    _c("gs300b Chosen as the Protector : Setup, Quantum Bands en jeu des le debut, sous le controle du joueur",
       "« Setup: Put Quantum Bands into play » (la 16e carte, absente des 15 du deck de heros)",
       [], [], {"en_jeu": ["gs301"], "bandes_controlees": True}, main_exclusive=["01090"]),
    # ================================================================== gs301 Quantum Bands
    _c("gs301 Quantum Bands : Quasar gagne AERIAL en forme heros",
       "« Quasar gains the [[AERIAL]] trait »",
       [HEROS], [], {"traits": ["AERIAL", "GUARDIAN"]}, main_exclusive=["01090"]),
    _c("gs301 Quantum Bands : Wendell Vaughn (alter ego) n'est PAS AERIAL",
       "contre-cas dans l'AUTRE forme (piege an002, RECETTES §3) ; absence : vert aussi sans module",
       [], [], {"traits_absents": ["AERIAL"]}, main_exclusive=["01090"]),
    _c("gs301 Quantum Bands : Hero Resource, paie seule Quantum Absorption (cout 1) et s'incline",
       "« Hero Resource: Exhaust Quantum Bands → generate a [wild] resource » : main sans autre ressource",
       [HEROS], [], {"en_jeu": ["gs313"], "exhausted": ["gs301"]}, main_exclusive=["gs313"], jouer=["gs313"]),
    _c("gs301 Quantum Bands : pas de ressource en ALTER EGO (Quantum Absorption reste en main)",
       "« HERO Resource » : contre-cas d'absence (vert aussi sans module)",
       [], [], {"en_main": ["gs313"], "pret": ["gs301"]}, main_exclusive=["gs313"], jouer=["gs313"]),
    _c("gs301 Quantum Bands : Permanent lu dans desc (attribut permanent vrai)",
       "« Permanent » : base automatique (desc.Permanent, has_permanent.py)",
       [HEROS], [], {"attrs": [["gs301", "permanent", True]]}, main_exclusive=["01090"]),
    # ================================================================== gs302 Epoch
    _c("gs302 Epoch : valeurs imprimees PV 4, ATQ 3, CTR 1, trait COSMIC ENTITY",
       "nombres texte <-> code : cout 4, THW 1, ATK 3, pastille 4",
       [HEROS, *en_jeu("gs302")], [],
       {"attrs": [["gs302", "max_health", 4], ["gs302", "attack", 3], ["gs302", "thwart", 1]],
        "traits_de": [["gs302", "COSMIC ENTITY"]]}, main_exclusive=["01090"]),
    _c("gs302 Epoch : apres son CONTRE de base, les Bandes se redressent (et 1 degat consecutif)",
       "« ★ Response: After Epoch uses one of her basic powers, ready Quantum Bands » ; CTR 1, une etoile creuse",
       [HEROS, *en_jeu("gs302"), BANDES_INCLINEES, menace(3)], ["Puzzle.Thwart('gs302')"],
       {"pret": ["gs301"], "menace": [[COMPLOT, 2]], "degats": [["gs302", 1]]}, main_exclusive=["01090"]),
    _c("gs302 Epoch : apres son ATTAQUE de base, les Bandes se redressent (et 3 degats consecutifs)",
       "meme Reponse, l'autre pouvoir ; ATQ 3, trois etoiles creuses sous ATK",
       [HEROS, *en_jeu("gs302"), BANDES_INCLINEES], ["Puzzle.Attack('gs302')"],
       {"pret": ["gs301"], "degats": [["01094", 3], ["gs302", 3]]}, main_exclusive=["01090"], cibles=["01094"]),
    # ================================================================== gs303 Flight of Light
    _c("gs303 Flight of Light : 3 sur une annexe a 2 (vidée) -> 2 de plus sur le complot (5 -> 3)",
       "« If this removes the last threat from that scheme, remove 2 threat from a scheme »",
       [HEROS, *en_jeu("01109"), menace(2, "01109"), menace(5), BANDES_INCLINEES], [],
       {"hors_jeu": ["01109"], "menace": [[COMPLOT, 3]], "defausse": ["gs303"]},
       main_exclusive=["gs303", "01090"], jouer=["gs303"], cibles=["01109", COMPLOT]),
    _c("gs303 Flight of Light : annexe a 5 (pas videe) -> rien de plus (complot reste a 5)",
       "contre-cas : la menace restante (2) n'est pas la derniere",
       [HEROS, *en_jeu("01109"), menace(5, "01109"), menace(5), BANDES_INCLINEES], [],
       {"menace": [["01109", 2], [COMPLOT, 5]], "defausse": ["gs303"]},
       main_exclusive=["gs303", "01090"], jouer=["gs303"], cibles=["01109", COMPLOT]),
    # ================================================================== gs305 No Holding Back
    _c("gs305 No Holding Back : paye RR (Strength) -> 6 degats a Rhino, aucune menace retiree",
       "« 3 damage for each [physical] » ; aucune [mental] : pas de contre",
       [HEROS, menace(5), BANDES_INCLINEES], [], {"degats": [["01094", 6]], "menace": [[COMPLOT, 5]]},
       main_exclusive=["gs305", "01090"], jouer=["gs305"], cibles=["01094"]),
    _c("gs305 No Holding Back : paye BB (Genius) -> 4 menaces retirees, aucun degat",
       "« Remove 2 threat for each [mental] »",
       [HEROS, menace(5), BANDES_INCLINEES], [], {"degats": [["01094", 0]], "menace": [[COMPLOT, 1]]},
       main_exclusive=["gs305", "01089"], jouer=["gs305"], cibles=[COMPLOT]),
    _c("gs305 No Holding Back : Bandes (joker compte [physical]) + Unbreakable Guard [mental] -> 3 degats ET 2 menaces",
       "le joker vaut la couleur que le joueur lui donne (FAQ p.22 : « two P resources, one generated by Quantum Bands »)",
       [HEROS, menace(5)], [], {"degats": [["01094", 3]], "menace": [[COMPLOT, 3]]},
       main_exclusive=["gs305", "gs309"], jouer=["gs305"], cibles=["01094", COMPLOT], choisir_option=["R"]),
    # ================================================================== gs307 Righteous Fury
    _c("gs307 Righteous Fury : 6 degats a Rhino (14 PV) -> pas vaincu, Quasar reste incline",
       "« If this attack defeats that enemy, ready Quasar » : contre-cas, Rhino survit",
       [HEROS, BANDES_INCLINEES, QUASAR_INCLINE], [], {"degats": [["01094", 6]], "exhausted": ["gs300a"]},
       main_exclusive=["gs307", "01090", "01090"], jouer=["gs307"], cibles=["01094"]),
    _c("gs307 Righteous Fury : Shocker (3 PV) vaincu -> Quasar se redresse",
       "« Deal 6 damage to an enemy. If this attack defeats that enemy, ready Quasar »",
       [HEROS, *en_jeu("01103"), BANDES_INCLINEES, QUASAR_INCLINE], [], {"hors_jeu": ["01103"], "pret": ["gs300a"]},
       main_exclusive=["gs307", "01090", "01090"], jouer=["gs307"], cibles=["01103"]),
    # ================================================================== gs309 Unbreakable Guard
    _c("gs309 Unbreakable Guard : Rhino attaque Quasar incline, payee avec Genius -> 0 degat, PAS de Tenace",
       "« prevent all of that damage » ; payee sans les Bandes : pas de carte d'etat",
       [HEROS, BANDES_INCLINEES, QUASAR_INCLINE], ["Puzzle.Attack('01094')"],
       {"degats_identite": 0, "statuts_absents": [["gs300a", "Tough"]], "defausse": ["gs309"]},
       main_exclusive=["gs309", "01089"]),
    _c("gs309 Unbreakable Guard : payee avec les Bandes -> 0 degat ET Quasar Tenace",
       "« If you paid for this card with Quantum Bands give that friendly character a tough status card »",
       [HEROS, QUASAR_INCLINE], ["Puzzle.Attack('01094')"],
       {"degats_identite": 0, "statuts": [["gs300a", "Tough"]], "defausse": ["gs309"]},
       main_exclusive=["gs309"]),
    # ================================================================== gs311 Quantum Energy
    _c("gs311 Quantum Energy : depensee pour Quantum Absorption -> les Bandes inclinees se redressent",
       "« Response: After you spend this card, ready Quantum Bands »",
       [HEROS, BANDES_INCLINEES], [], {"en_jeu": ["gs313"], "pret": ["gs301"], "defausse": ["gs311"]},
       main_exclusive=["gs313", "gs311"], jouer=["gs313"]),
    _c("gs311 Quantum Energy : valeur imprimee, une icone joker (paie seule un cout 1 sans les Bandes)",
       "nombres texte <-> code : case verte a etoile = RES G",
       [HEROS, BANDES_INCLINEES], [], {"en_jeu": ["gs313"], "defausse": ["gs311"]},
       main_exclusive=["gs313", "gs311"], jouer=["gs313"]),
    # ================================================================== gs313 Quantum Absorption
    _c("gs313 Quantum Absorption : Unbreakable Guard payee par les Bandes -> 2 degats soignes sur Quasar (5 -> 3)",
       "« Hero Interrupt: When you pay for a DEFENSE event with Quantum Bands, heal 2 damage from Quasar »",
       [HEROS, *en_jeu("gs313"), QUASAR_INCLINE, "Puzzle.EmptyHand()", "Puzzle.Damage('gs300a', 5)"],
       ["Puzzle.Attack('01094')"],
       {"degats_identite": 3, "defausse": ["gs309"]}, main_exclusive=["gs309"]),
    _c("gs313 Quantum Absorption : Unbreakable Guard payee SANS les Bandes -> aucun soin (5 degats)",
       "contre-cas « with Quantum Bands » (absence : vert aussi sans module)",
       [HEROS, *en_jeu("gs313"), QUASAR_INCLINE, BANDES_INCLINEES, "Puzzle.EmptyHand()", "Puzzle.Damage('gs300a', 5)"],
       ["Puzzle.Attack('01094')"], {"degats_identite": 5, "defausse": ["gs309"]}, main_exclusive=["gs309", "01089"]),
    _c("gs313 Quantum Absorption : evenement NON DEFENSE (Righteous Fury) paye par les Bandes -> aucun soin",
       "« a DEFENSE event » : un ATTACK ne declenche pas",
       [HEROS, *en_jeu("gs313")], ["Puzzle.Damage('gs300a', 5)"], {"degats_identite": 5, "degats": [["01094", 6]]},
       main_exclusive=["gs307", "01090"], jouer=["gs307"], cibles=["01094"]),
    # ================================================================== gs315 Quantum Jump
    _c("gs315 Quantum Jump : Flight of Light payee par les Bandes -> 3 + 2 menaces (6 -> 1)",
       "« that thwart removes 2 additional threat »",
       [HEROS, *en_jeu("gs315"), menace(6)], [], {"menace": [[COMPLOT, 1]], "defausse": ["gs303"]},
       main_exclusive=["gs303", "gs311"], jouer=["gs303"], cibles=[COMPLOT]),
    _c("gs315 Quantum Jump : Flight of Light payee SANS les Bandes -> 3 menaces seulement (6 -> 3)",
       "contre-cas « with Quantum Bands » (absence : vert aussi sans module)",
       [HEROS, *en_jeu("gs315"), menace(6), BANDES_INCLINEES], [], {"menace": [[COMPLOT, 3]], "defausse": ["gs303"]},
       main_exclusive=["gs303", "01090"], jouer=["gs303"], cibles=[COMPLOT]),
    _c("gs315 Quantum Jump : sous CRISE (Crowd Control), payee par les Bandes -> le complot principal perd 5 (6 -> 1)",
       "« ignores the crisis icon » : ciblable (Bandes pretes) ET retrait accepte a la resolution",
       [HEROS, *en_jeu("gs315", "01108"), menace(6)], [], {"menace": [[COMPLOT, 1]], "defausse": ["gs303"]},
       main_exclusive=["gs303", "gs311"], jouer=["gs303"], cibles=[COMPLOT]),
    _c("gs315 Quantum Jump : sous CRISE, Bandes inclinees -> le complot principal n'est pas ciblable (Crowd Control vise)",
       "sans Bandes pour payer, rien n'ignore la crise : 1re cible = Crowd Control (videe), puis 2 sur le complot (6 -> 4)",
       [HEROS, *en_jeu("gs315", "01108"), menace(6), BANDES_INCLINEES], [], {"menace": [[COMPLOT, 4]], "hors_jeu": ["01108"]},
       main_exclusive=["gs303", "01090"], jouer=["gs303"], cibles=[COMPLOT]),
    _c("gs315 Quantum Jump : sous PATROUILLE (Badoon Lieutenant engage), payee par les Bandes -> 6 -> 1",
       "« and the patrol keyword »",
       [HEROS, *en_jeu("gs315", "16119"), menace(6)], [], {"menace": [[COMPLOT, 1]], "defausse": ["gs303"]},
       main_exclusive=["gs303", "gs311"], jouer=["gs303"], cibles=[COMPLOT]),
    _c("gs315 Quantum Jump : sous PATROUILLE, Bandes pretes mais payee avec Genius -> rien retire (CORRECTIF scheme_main)",
       "ciblage offert avant le paiement, Patrouille REVERIFIEE a la resolution (sans le correctif : 6 -> 3)",
       [HEROS, *en_jeu("gs315", "16119"), menace(6)], [], {"menace": [[COMPLOT, 6]], "defausse": ["gs303"]},
       main_exclusive=["gs303", "01089"], jouer=["gs303"], cibles=[COMPLOT], payer_avec=["01089"],
       ne_pas_depenser=["gs301"]),
    # ================================================================== gs316 Quantum Weapon
    _c("gs316 Quantum Weapon : Righteous Fury payee par les Bandes -> 6 + 1 = 7 degats a Rhino",
       "« that attack deals 1 additional damage »",
       [HEROS, *en_jeu("gs316")], [], {"degats": [["01094", 7]], "defausse": ["gs307"]},
       main_exclusive=["gs307", "01090"], jouer=["gs307"], cibles=["01094"]),
    _c("gs316 Quantum Weapon : Righteous Fury payee SANS les Bandes -> 6 degats seulement",
       "contre-cas « with Quantum Bands » (absence : vert aussi sans module)",
       [HEROS, *en_jeu("gs316"), BANDES_INCLINEES], [], {"degats": [["01094", 6]], "defausse": ["gs307"]},
       main_exclusive=["gs307", "01090", "01090"], jouer=["gs307"], cibles=["01094"]),
    _c("gs316 Quantum Weapon : percant ET deferlement : Sandman Tenace (4 PV) vaincu, 3 en exces sur Rhino",
       "« gains piercing and overkill » : la Tenace saute, 7 - 4 = 3 degats d'exces au vilain",
       [HEROS, *en_jeu("gs316", "01102")], [], {"hors_jeu": ["01102"], "degats": [["01094", 3]]},
       main_exclusive=["gs307", "01090"], jouer=["gs307"], cibles=["01102"]),
    # ================================================================== gs349 Quantum Bubble
    _c("gs349 Quantum Bubble : Martinex paye par les Bandes -> Martinex Tenace",
       "« Hero Response: After you pay for an ally with Quantum Bands, give that ally a tough status card »",
       [HEROS, *en_jeu("gs349")], [], {"en_jeu": ["21065"], "statuts": [["21065", "Tough"]]},
       main_exclusive=["21065", "gs311"], jouer=["21065"]),
    _c("gs349 Quantum Bubble : Martinex paye SANS les Bandes -> pas de Tenace",
       "contre-cas « with Quantum Bands » (absence : vert aussi sans module)",
       [HEROS, *en_jeu("gs349"), BANDES_INCLINEES], [], {"en_jeu": ["21065"], "statuts_absents": [["21065", "Tough"]]},
       main_exclusive=["21065", "01089"], jouer=["21065"]),
    # ================================================================== gs065 Protector of the Universe
    _c("gs065 Protector of the Universe : en jeu avec 3 pions duty ; Quasar ne peut plus passer en alter ego",
       "« Uses (3 duty counters). You cannot flip to alter-ego form »",
       [HEROS, "Puzzle.Reveal('gs065')"], ["Puzzle.ChangeForm('gs300a')"],
       {"compteurs": [["gs065", "duty", 3]], "forme": "Hero"}, main_exclusive=["01090"]),
    _c("gs065 Protector of the Universe : defendre sans subir de degat -> 1 pion duty retire (3 -> 2)",
       "« or defend against an attack and take no damage » : ATQ 2 de Rhino contre DEF 2",
       [HEROS, "Puzzle.Reveal('gs065')"], ["Puzzle.Attack('01094')"],
       {"compteurs": [["gs065", "duty", 2]], "degats_identite": 0}, main_exclusive=["01090"]),
    _c("gs065 Protector of the Universe : vaincre un ennemi (Shocker) -> 1 pion duty retire",
       "« After you defeat an enemy »",
       [HEROS, "Puzzle.Reveal('gs065')", *en_jeu("01103"), "Puzzle.Damage('01103', 1)"], ["Puzzle.Attack('gs300a')"],
       {"compteurs": [["gs065", "duty", 2]], "hors_jeu": ["01103"]}, main_exclusive=["01090"], cibles=["01103"]),
    _c("gs065 Protector of the Universe : vaincre une manigance (Bomb Scare a 2) -> 1 pion duty retire",
       "« or a scheme » : contre de base CTR 2",
       [HEROS, "Puzzle.Reveal('gs065')", *en_jeu("01109"), menace(2, "01109")], ["Puzzle.Thwart('gs300a')"],
       {"compteurs": [["gs065", "duty", 2]], "hors_jeu": ["01109"]}, main_exclusive=["01090"], cibles=["01109"]),
    _c("gs065 Protector of the Universe : le DERNIER pion retire fait partir l'obligation (Uses)",
       "regle du mot-cle Uses : 1 pion restant, une defense sans degat le retire, la carte quitte le jeu",
       [HEROS, "Puzzle.Reveal('gs065')", "Puzzle.Counter('gs065', 'duty', -2)"], ["Puzzle.Attack('01094')"],
       {"hors_jeu": ["gs065"]}, main_exclusive=["01090"]),
    # ================================================================== gs099q Maelstrom
    _c("gs099q Maelstrom : valeurs imprimees PV 5, ATQ 2, MNG 1, traits DEVIANT INHUMAN",
       "nombres texte <-> code (pastille 5, SCH 1, ATK 2)",
       [HEROS, "Puzzle.Reveal('gs099q')"], [],
       {"attrs": [["gs099q", "max_health", 5], ["gs099q", "attack", 2], ["gs099q", "scheme", 1]],
        "traits_de": [["gs099q", "DEVIANT"], ["gs099q", "INHUMAN"]]}, main_exclusive=["01090"]),
    _c("gs099q Maelstrom : revele -> Quantum Bands glissees sous lui (hors jeu, Quasar perd AERIAL)",
       "« When Revealed: Tuck Quantum Bands under Maelstrom » (Bandes PERMANENTES : exception moteur)",
       [HEROS, "Puzzle.Reveal('gs099q')"], [],
       {"pose_sous": [["gs099q", "gs301"]], "hors_jeu": ["gs301"], "traits_absents": ["AERIAL"]},
       main_exclusive=["01090"]),
    _c("gs099q Maelstrom : vaincu -> Quantum Bands reviennent en jeu sous le controle du joueur Quasar",
       "« Forced Response: After Maelstrom leaves play, put Quantum Bands into play under the Quasar player's control »",
       [HEROS, "Puzzle.Reveal('gs099q')"], ["Puzzle.Damage('gs099q', 5)"],
       {"hors_jeu": ["gs099q"], "en_jeu": ["gs301"], "bandes_controlees": True, "traits": ["AERIAL"]},
       main_exclusive=["01090"]),
    # ================================================================== gs239q Entropy Ascendant
    _c("gs239q Entropy Ascendant : menace de depart 3 + Entrave 1 (un joueur) = 4",
       "nombres texte <-> code : case 3, « Hinder 1 [per_player] »",
       [HEROS, "Puzzle.Reveal('gs239q')"], [], {"menace": [["gs239q", 4]]}, main_exclusive=["01090"]),
    _c("gs239q Entropy Ascendant : un evenement exige une [energy] : Flight of Light payee RR reste en main",
       "« Each event card gains requirement ([energy]) »",
       [HEROS, "Puzzle.Reveal('gs239q')", BANDES_INCLINEES, menace(5)], [],
       {"en_main": ["gs303"], "menace": [[COMPLOT, 5]]}, main_exclusive=["gs303", "01090"], jouer=["gs303"],
       cibles=[COMPLOT]),
    _c("gs239q Entropy Ascendant : payee YY (Energy) -> Flight of Light jouee (5 -> 2)",
       "requirement = pas un cout en plus : 2 ressources dont une [energy] suffisent",
       [HEROS, "Puzzle.Reveal('gs239q')", BANDES_INCLINEES, menace(5)], [],
       {"defausse": ["gs303"], "menace": [[COMPLOT, 2]]}, main_exclusive=["gs303", "01088"], jouer=["gs303"],
       cibles=[COMPLOT]),
    _c("gs239q Entropy Ascendant : une AMELIORATION n'est pas touchee (Quantum Absorption payee RR)",
       "« EACH EVENT card » : seulement les evenements",
       [HEROS, "Puzzle.Reveal('gs239q')", BANDES_INCLINEES], [], {"en_jeu": ["gs313"]},
       main_exclusive=["gs313", "01090"], jouer=["gs313"]),
    # ================================================================== gs237q Avatar of Oblivion
    _c("gs237q Avatar of Oblivion : attache au sbire de plus forte ATQ (Shocker), ELITE et ATQ +1",
       "« Attach to the minion with the highest ATK. Attached minion gains the ELITE trait » ; +1 ATK imprime",
       [HEROS, *en_jeu("01103"), "Puzzle.Reveal('gs237q')"], [],
       {"attaches": [["01103", "gs237q"]], "traits_de": [["01103", "ELITE"]], "attributs_carte": [["01103", "attack", 1]]},
       main_exclusive=["01090"]),
    _c("gs237q Avatar of Oblivion : le sbire censé etre vaincu est soigne et reste ; l'attachement part",
       "« When attached minion would be defeated, heal all damage from it instead, then discard this card »",
       [HEROS, *en_jeu("01103"), "Puzzle.Reveal('gs237q')"], ["Puzzle.Damage('01103', 3)"],
       {"en_jeu": ["01103"], "degats": [["01103", 0]], "hors_jeu": ["gs237q"]}, main_exclusive=["01090"]),
    _c("gs237q Avatar of Oblivion : aucun sbire en jeu -> Renfort (la carte suivante du deck rencontre part)",
       "« If you cannot, this card gains surge »",
       ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01109', '01105')", HEROS,
        "Puzzle.RemoveMinionsInPlay()", "Puzzle.Reveal('gs237q')"], [],
       {"carte_du_surge": "01105"}, main_exclusive=["01090"], avec_boost=True),
    # ================================================================== gs240q Distant Manipulation
    _c("gs240q Distant Manipulation : choix « incliner » -> les Bandes s'inclinent, l'Energy reste en main",
       "« Choose to either exhaust each card with a 'Resource' ability you control or discard each resource card »",
       [HEROS], ["Puzzle.Reveal('gs240q')"], {"exhausted": ["gs301"], "en_main": ["01088"]},
       main_exclusive=["01088"]),
    _c("gs240q Distant Manipulation : Bandes deja inclinees -> seule option, defausser l'Energy de la main",
       "l'option impossible n'est pas offerte",
       [HEROS, BANDES_INCLINEES], ["Puzzle.Reveal('gs240q')"], {"defausse": ["01088"], "absent_main": ["01088"]},
       main_exclusive=["01088"]),
    _c("gs240q Distant Manipulation : ni carte Resource prete ni ressource en main -> Renfort",
       "« If you cannot, this card gains surge »",
       ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01109', '01105')", HEROS, BANDES_INCLINEES,
        ], ["Puzzle.Reveal('gs240q')"], {"carte_du_surge": "01105"}, main_exclusive=["gs303"], avec_boost=True),
    # ================================================================== etape 8 bis : ce que le plateau DESSINE
    _c("gs099q gs065 gs237q gs239q gs349 plateau : fixture du descripteur (Bandes glissees, duty, Avatar, Entropy, Tenace)",
       "PROCESSUS-CARTE 8 bis : le descripteur PRODUIT PAR LE MOTEUR, relu par ui-app/src/board/quasar-plateau.test.ts",
       [HEROS, "Puzzle.Reveal('gs065')", *en_jeu("21065"), "Puzzle.Tough('21065')", "Puzzle.Reveal('gs099q')",
        "Puzzle.Reveal('gs239q')", *en_jeu("01103"), "Puzzle.Reveal('gs237q')"], [],
       {"pose_sous": [["gs099q", "gs301"]], "fixture": "quasar-maelstrom.json"},
       main_exclusive=["01090"], verifier="qz_fixture_plateau"),
    _c("gs099q gs301 plateau : fixture apres la defaite de Maelstrom (Bandes revenues sur Quasar)",
       "PROCESSUS-CARTE 8 bis : la carte revient en jeu, dessinee sur l'identite",
       [HEROS, "Puzzle.Reveal('gs099q')"], ["Puzzle.Damage('gs099q', 5)"],
       {"en_jeu": ["gs301"], "fixture": "quasar-bandes-revenues.json"},
       main_exclusive=["01090"], verifier="qz_fixture_plateau"),
]


VERIFICATIONS = r'''
CLES_QUASAR = {'attrs', 'bandes_controlees'}


def qz_etat(monde, aides):
    """etat_attendu + cles propres : attrs [[card_id, attribut, valeur]] (valeur COURANTE d'une carte en
    jeu), bandes_controlees (Quantum Bands en jeu sous le controle du joueur 1)."""
    cas = aides["cas"]
    attendu = dict(cas.get("attendu") or {})
    propres = {k: attendu.pop(k) for k in list(attendu) if k in CLES_QUASAR}
    soucis = []
    for cid, attr, voulu in propres.get("attrs") or []:
        face = aides["par_id"](monde, cid)
        if face is None:
            soucis.append(f"{cid} introuvable en jeu (attrs)")
        elif getattr(face, attr) != voulu:
            soucis.append(f"{cid}.{attr} = {getattr(face, attr)} (attendu {voulu})")
    if propres.get("bandes_controlees"):
        bandes = aides["par_id"](monde, "gs301")
        joueur = monde.players[0]
        if bandes is None:
            soucis.append("Quantum Bands (gs301) pas en jeu")
        elif bandes.GetControlByOrOwner() != joueur:
            soucis.append(f"Quantum Bands controlees par {bandes.GetControlByOrOwner()} (attendu {joueur})")
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


def qz_fixture_plateau(monde, aides):
    """Etape 8 bis : qz_etat (sans la cle `fixture`), puis ecrit le descripteur du monde
    (`ToDescriptor.World`, ce que sert /get_world, sans les decks) dans QUASAR_FIXTURE_DIR/<fixture>."""
    import json, os
    from dataclasses import asdict, is_dataclass
    from game.render.to_descriptor import ToDescriptor
    cas = aides["cas"]
    attendu = dict(cas.get("attendu") or {})
    nom = attendu.pop("fixture", None)
    sauvegarde = cas["attendu"]
    cas["attendu"] = attendu
    try:
        ok, msg = qz_etat(monde, aides)
    finally:
        cas["attendu"] = sauvegarde
    descripteur = ToDescriptor.World(monde, "", "")
    brut = json.loads(json.dumps(asdict(descripteur) if is_dataclass(descripteur) else descripteur,
                                 default=lambda o: asdict(o) if is_dataclass(o) else str(o)))
    siege = brut["players"][0]
    for cle in ("player_deck", "player_discard_pile", "additional_deck", "hand_cards"):
        if cle in siege:
            siege[cle] = []
    dossier = os.environ.get("QUASAR_FIXTURE_DIR")
    if dossier and nom:
        communes = {k: v for k, v in brut.items() if k.startswith("area_")}
        fixture = {"monde": {"render_id": 1, "players": [siege], **communes},
                   "identite": monde.players[0].GetIdentity().card.object_id}
        with open(os.path.join(dossier, nom), "w", encoding="utf-8") as f:
            json.dump(fixture, f, ensure_ascii=False, indent=1, sort_keys=True)
    return ok, msg
'''
