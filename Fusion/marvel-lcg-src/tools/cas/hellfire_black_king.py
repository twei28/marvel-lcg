# Cas test_capacites du scenario 2 « BLACK KING » (Sebastian Shaw) de la campagne Hellfire Hunt (Dipsome), prefixe `hf`, pack
# hellfire_hunt_black_king (set 242) + module « Sebastian Shaw » (hf331-hf338). Noms prefixes « [hf] » puis le card_id (substituer_pack.py filtre dessus).
#
# Rappels de montage (voir aussi docs/packs/hellfire-hunt-black-king/GABARITS.md, « pieges de harnais ») :
#  - `spider_man` demarre en ALTER-EGO : `Puzzle.ChangeForm('01001a')` le passe en HEROS (le vilain ATTAQUE un heros, MANIGANCE contre un alter ego) ;
#  - le vilain et le complot sont ceux du scenario : Sebastian Shaw I (hf201) et Jailbreak at the Hellfire Club (hf204b, menace 0, cible 5 par heros) ;
#  - `Puzzle.CreateEncounterDeck(a, b, c)` pose `a` en DERNIER : la derniere carte creee est le DESSUS du deck ; `deck()` inverse la liste ;
#  - 01105 = « Bomb Scare » (aucune capacite de boost), remplissage inoffensif.
SC = "hellfire_black_king"
SCX = "hellfire_black_king_expert"
HEROS = "Puzzle.ChangeForm('01001a')"   # spider_man demarre en ALTER-EGO
REMPLI = "'01105'"


def deck(*cartes, remplissage=6):
    """Deck de rencontre de test, les cartes voulues listees DU DESSUS vers le dessous, puis du remplissage inoffensif."""
    ids = list(cartes) + ["01105"] * remplissage
    return ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck(%s)" % ", ".join("'%s'" % c for c in reversed(ids))]


STADE2 = deck("01105", "01105", "01105") + ["Puzzle.AdvanceMainScheme()"]     # stade 2 : menace de depart 4 par joueur, Black King retourne (hf207b)


def _c(nom, pourquoi, mise, declencher, attendu, **cle):
    cas = {"nom": "[hf] " + nom, "pourquoi": pourquoi, "scenario": cle.pop("scenario", SC),
           "heros": cle.pop("heros", "spider_man"), "mise_en_place": ["Puzzle.EmptyHand()"] + list(mise), "declencher": declencher,
           "verifier": cle.pop("verifier", "hfk_etat"), "attendu": attendu}
    cas.update(cle)
    cas.setdefault("main_exclusive", ["01090"])
    return cas


CAS = [
    # ===================================================================== le scenario se monte : Setup de 1A (hf204a)
    _c("hf204a mise en place : Sebastian Shaw I en jeu (PV 13, ATK 0, SCH 2), complot 1B a 0 menace",
       "le scenario `hellfire_black_king` se charge : vilain hf201, complot hf204b, nombres imprimes (texte <-> code)",
       deck("01105"), [],
       {"en_jeu": ["hf201", "hf204b"], "vie": [["hf201", 13]], "attaque": [["hf201", 0]], "menace_de": [["hf204b", 0]],
        "trait_de": [["hf201", "HELLFIRE", True]]}),
    _c("hf204a Setup : Captured by Hellfire! revelee (menace 5), un captif cache dessous (1 par joueur), 3 captifs restent de cote, Black King attache a Shaw",
       "« Set each CAPTIVE ally aside. Reveal the Captured by Hellfire! side scheme. Attach Black King to Sebastian Shaw » : 4 captifs de cote, 1 (par joueur) glisse sous la manigance",
       [], [],
       {"en_jeu": ["hf206", "hf207a", "hf201"], "menace_de": [["hf206", 5]], "attache": [["hf207a", "hf201"]], "taille_pose_sous": [["hf206", 1]],
        "aside_nb_captifs": 3, "aside_absents": ["hf207a"]}),
    _c("hf204a Setup : le sbire Sebastian Shaw (hf331) du module n'est PAS dans le deck de rencontre au depart (le reste du module y est)",
       "« Remove each minion named Sebastian Shaw from the game » (montage natif du scenario, sans `deck()`) : le VILAIN du meme nom reste en jeu",
       [], [], {"en_jeu": ["hf201"], "dans_deck_rencontre": ["hf332", "hf338"], "hors_deck_rencontre": ["hf331"], "absents": ["hf331"]}),
    _c("hf204a Setup a DEUX joueurs : deux captifs caches sous Captured by Hellfire! (1 par joueur), deux de cote",
       "« Place 1[per player] random set-aside CAPTIVE allies facedown beneath this scheme »",
       [], [],
       {"en_jeu": ["hf206"], "taille_pose_sous": [["hf206", 2]], "aside_nb_captifs": 2}, heros2="spider_man"),
    # ===================================================================== hf201-hf203 : Shaw, Absorb et attaque
    _c("hf201 Absorb : le heros inflige 2 degats -> 2 compteurs d'energie sur Shaw",
       "Absorb - Forced Response : « After Sebastian Shaw takes damage from an attack, place energy counters on him equal to the damage taken »",
       [HEROS] + deck("01105"), ["Puzzle.Attack('01001a')"],
       {"degats_de": [["hf201", 2]], "compteurs_sur": [["hf201", "energy", 2]]}, cibles=["hf201"], accepter_choix=True),
    _c("hf201 Absorb : TEMOIN, des degats qui ne viennent PAS d'une attaque (Puzzle.Damage) ne placent aucun compteur",
       "« damage from an attack » : un degat d'effet n'est pas absorbe",
       deck("01105"), ["Puzzle.Damage('hf201', 3)"],
       {"degats_de": [["hf201", 3]], "compteurs_sur": [["hf201", "energy", 0]]}),
    _c("hf201 Interruption forcee : Shaw (2 compteurs) attaque le heros -> +2 ATK pour cette activation (2 degats) et les 2 compteurs sont retires",
       "« When Sebastian Shaw attacks, remove all energy counters here to a maximum of 3. For each removed, +1 ATK for this activation » : ATK imprimee 0, +2 = 2 degats ; le heros est incline (il ne defend pas)",
       [HEROS, "Puzzle.Exhaust('01001a')", "Puzzle.PlaceCounters('hf201', 'energy', 2)"] + deck("01105"), ["Puzzle.Attack('hf201')"],
       {"degats_identite": 2, "compteurs_sur": [["hf201", "energy", 0]]}),
    _c("hf201 Interruption forcee : au plus 3 compteurs retires -> 5 compteurs : 3 retires (+3 ATK = 3 degats), 2 restent",
       "« to a maximum of 3 » : la limite compte ; mesure du reste (2) ET des degats (3)",
       [HEROS, "Puzzle.Exhaust('01001a')", "Puzzle.PlaceCounters('hf201', 'energy', 5)"] + deck("01105"), ["Puzzle.Attack('hf201')"],
       {"degats_identite": 3, "compteurs_sur": [["hf201", "energy", 2]]}),
    _c("hf201 Interruption forcee : TEMOIN, Shaw sans compteur attaque avec son ATK imprimee 0 -> aucun degat",
       "contre-cas : sans compteur, pas de bonus", [HEROS, "Puzzle.Exhaust('01001a')"] + deck("01105"), ["Puzzle.Attack('hf201')"],
       {"degats_identite": 0}),
    _c("hf202 stade II : PV 15, ATK 1, SCH 3 ; Absorb et interruption identiques (le heros inflige 2 -> 2 compteurs)",
       "nombres texte <-> code du stade II ; meme texte que le stade I",
       ["Puzzle.Damage('hf201', 13)"] + deck("01105"), [],
       {"en_jeu": ["hf202"], "absents": ["hf201"], "vie": [["hf202", 15]], "attaque": [["hf202", 1]]}),
    _c("hf202 Absorb : stade II, le heros inflige 2 degats -> 2 compteurs",
       "Absorb du stade II", ["Puzzle.Damage('hf201', 13)", HEROS] + deck("01105"), ["Puzzle.Attack('01001a')"],
       {"degats_de": [["hf202", 2]], "compteurs_sur": [["hf202", "energy", 2]]}, cibles=["hf202"], accepter_choix=True),
    _c("hf202 Interruption forcee : stade II, 2 compteurs -> ATK 1 + 2 = 3 degats",
       "« remove ... +1 ATK for this activation » sur le stade II (ATK imprimee 1)",
       ["Puzzle.Damage('hf201', 13)", HEROS, "Puzzle.Exhaust('01001a')", "Puzzle.PlaceCounters('hf202', 'energy', 2)"] + deck("01105"), ["Puzzle.Attack('hf202')"],
       {"degats_identite": 3, "compteurs_sur": [["hf202", "energy", 0]]}),
    _c("hf203 mode expert : la partie commence au stade II (PV 15), le stade I est retire",
       "livret p. 10 : « Remove Sebastian Shaw (I) and add Sebastian Shaw (III) for expert mode » : villains hf202 puis hf203",
       deck("01105"), [], {"en_jeu": ["hf202"], "absents": ["hf201", "hf203"], "vie": [["hf202", 15]]}, scenario=SCX),
    _c("hf203 Absorb : stade III, 2 degats d'attaque -> 3 compteurs (2 + 1 supplementaire)",
       "stade III apres defaite du stade II (expert : II puis III)",
       ["Puzzle.Damage('hf202', 15)", HEROS] + deck("01105"), ["Puzzle.Attack('01001a')"],
       {"en_jeu": ["hf203"], "vie": [["hf203", 17]], "attaque": [["hf203", 1]], "degats_de": [["hf203", 2]], "compteurs_sur": [["hf203", "energy", 3]]},
       scenario=SCX, cibles=["hf203"], accepter_choix=True),
    _c("hf203 Absorb : TEMOIN, au stade II (expert aussi) la meme attaque ne donne que 2 compteurs",
       "contre-cas : le compteur supplementaire est propre au stade III",
       [HEROS] + deck("01105"), ["Puzzle.Attack('01001a')"],
       {"compteurs_sur": [["hf202", "energy", 2]]}, scenario=SCX, cibles=["hf202"], accepter_choix=True),
    _c("hf201 stade vaincu : Black King (Permanent) reste attache a Shaw (II)",
       "le stade suivant est revele : l'attachement Permanent ne quitte pas le jeu",
       ["Puzzle.Damage('hf201', 13)"] + deck("01105"), [],
       {"en_jeu": ["hf202", "hf207a"], "attache": [["hf207a", "hf202"]]}),

    # ===================================================================== hf207a Black King : King's Tactic (face A, sans limite)
    _c("hf207a King's Tactic : Shaw a 3 compteurs et absorbe 2 degats -> les 3 sont retires AVANT l'Absorb et deviennent 3 menaces ; l'Absorb en pose 2 neufs",
       "« Forced Interrupt : When Sebastian Shaw's Absorb triggers while there is an energy counter on him, remove each energy counter from him, place that much threat on the main scheme » : "
       "interruption forcee AVANT la reponse forcee (energie finale 2, pas 5 ; menace 3)",
       [HEROS, "Puzzle.PlaceCounters('hf201', 'energy', 3)"] + deck("01105"), ["Puzzle.Attack('01001a')"],
       {"compteurs_sur": [["hf201", "energy", 2]], "menace_de": [["hf204b", 3]]}, cibles=["hf201"], accepter_choix=True),
    _c("hf207a King's Tactic : TEMOIN, Shaw sans compteur -> aucune conversion (2 compteurs poses par l'Absorb, menace 0)",
       "« while there is an energy counter on him » : la condition est evaluee AVANT l'Absorb",
       [HEROS] + deck("01105"), ["Puzzle.Attack('01001a')"],
       {"compteurs_sur": [["hf201", "energy", 2]], "menace_de": [["hf204b", 0]]}, cibles=["hf201"], accepter_choix=True),
    _c("hf207a King's Tactic : face A sans limite -> DEUX Absorb dans le round convertissent tous les deux (menace 3 puis 5, a DEUX joueurs : cible 10)",
       "FAQ du livret : la limite « Max 1 par joueur » ne compte pas les instances de la face Black King",
       [HEROS, "Puzzle.PlaceCounters('hf201', 'energy', 3)"] + deck("01105"), ["Puzzle.Attack('01001a')", "Puzzle.Ready('01001a')", "Puzzle.Attack('01001a')"],
       {"en_jeu": ["hf207a"], "compteurs_sur": [["hf201", "energy", 2]], "menace_de": [["hf204b", 5]]}, cibles=["hf201"], accepter_choix=True, heros2="spider_man"),
    # ===================================================================== hf207b : face B, limitee + stalwart
    _c("hf207b King's Tactic : face B, premiere instance du round -> conversion (3 compteurs -> 3 menaces : 4 + 3 = 7, Absorb : 2 compteurs)",
       "la face B converts comme la A tant que la limite « Max 1 par joueur par round » n'est pas atteinte",
       STADE2 + [HEROS, "Puzzle.PlaceCounters('hf201', 'energy', 3)"], ["Puzzle.Attack('01001a')"],
       {"en_jeu": ["hf207b"], "absents": ["hf207a"], "compteurs_sur": [["hf201", "energy", 2]], "menace_de": [["hf205b", 7]]}, cibles=["hf201"], accepter_choix=True),
    _c("hf207b King's Tactic : TEMOIN D'EPUISEMENT, 2e Absorb du MEME round (1 joueur) -> pas de conversion : les 2 compteurs restent et 2 s'ajoutent (4), menace inchangee (7)",
       "FAQ du livret : « beyond this limit, it will not activate King's Tactic, and the energy counter will instead be stacked on Sebastian Shaw » ; chiffres mesures au SECOND declenchement",
       STADE2 + [HEROS, "Puzzle.PlaceCounters('hf201', 'energy', 3)"], ["Puzzle.Attack('01001a')", "Puzzle.Ready('01001a')", "Puzzle.Attack('01001a')"],
       {"compteurs_sur": [["hf201", "energy", 4]], "menace_de": [["hf205b", 7]]}, cibles=["hf201"], accepter_choix=True),
    _c("hf207b King's Tactic : la limite se renouvelle au round suivant -> 2e conversion (2 compteurs -> 2 menaces : 4 + 3 + 2 = 9, Absorb : 2)",
       "la limite est PAR ROUND : `ResetRoundStats` entre les deux attaques",
       STADE2 + [HEROS, "Puzzle.PlaceCounters('hf201', 'energy', 3)"],
       ["Puzzle.Attack('01001a')", "Puzzle.ResetRoundStats()", "Puzzle.Ready('01001a')", "Puzzle.Attack('01001a')"],
       {"compteurs_sur": [["hf201", "energy", 2]], "menace_de": [["hf205b", 9]]}, cibles=["hf201"], accepter_choix=True),
    _c("hf207b King's Tactic : a DEUX joueurs la limite est de 2 par round -> 2 conversions possibles (menace 8 + 3 = 11 puis 13 : 2 joueurs, depart 8), une 3e non",
       "« Max 1[per player] times per round » : 2 joueurs = 2 instances ; la 3e s'empile",
       STADE2 + [HEROS, "Puzzle.PlaceCounters('hf201', 'energy', 3)"],
       ["Puzzle.Attack('01001a')", "Puzzle.Ready('01001a')", "Puzzle.Attack('01001a')", "Puzzle.Ready('01001a')", "Puzzle.Attack('01001a')"],
       {"compteurs_sur": [["hf201", "energy", 4]], "menace_de": [["hf205b", 13]]}, cibles=["hf201"], accepter_choix=True, heros2="spider_man"),
    _c("hf207b Stalwart : Shaw a 6 compteurs (plus de 5) -> stalwart ; avec 5 -> pas stalwart",
       "« Sebastian Shaw gains stalwart while there is more than 5 energy counters on him »",
       ["Puzzle.Flip('hf207a')", "Puzzle.PlaceCounters('hf201', 'energy', 6)"] + deck("01105"), [],
       {"en_jeu": ["hf207b"], "stalwart": [["hf201", True]]}),
    _c("hf207b Stalwart : TEMOIN, 5 compteurs exactement -> pas de stalwart",
       "« more than 5 » : strictement", ["Puzzle.Flip('hf207a')", "Puzzle.PlaceCounters('hf201', 'energy', 5)"] + deck("01105"), [],
       {"en_jeu": ["hf207b"], "stalwart": [["hf201", False]]}),
    _c("hf207b Stalwart : TEMOIN, face A avec 6 compteurs -> pas de stalwart (propre a la face B)",
       "la face A n'a pas ce texte", ["Puzzle.PlaceCounters('hf201', 'energy', 6)"] + deck("01105"), [],
       {"en_jeu": ["hf207a"], "stalwart": [["hf201", False]]}),
    _c("hf207b Stalwart : les compteurs retires (Hero Action de 2B, 6 -> 4) font perdre le stalwart",
       "le bonus suit le nombre de compteurs en temps reel (`ex_change_on_event=OnEvent.Counter`)",
       [HEROS, "Puzzle.AdvanceMainScheme()", "Puzzle.PutIntoPlay('hf209', under_control=True)", "Puzzle.PlaceCounters('hf201', 'energy', 6)"] + deck("01105", "01105"),
       ["Puzzle.Action('hf205b', 'HeroAction')"],
       {"en_jeu": ["hf207b"], "compteurs_sur": [["hf201", "energy", 4]], "stalwart": [["hf201", False]]}),
    # ===================================================================== hf204b : menace inamovible, complot remplace, defaite
    _c("hf204b Threat cannot be removed : une attaque de menace du heros (THW 1) laisse les 3 menaces du complot ; TEMOIN : une side scheme a 3 menaces perd 1",
       "« Threat cannot be removed from this scheme » ; temoin Mutant Experimentation (hf226, 3 menaces pour 1 joueur) : le meme geste y retire 1",
       [HEROS, "Puzzle.PlaceThreat('hf204b', 3)"] + deck("01105"), ["Puzzle.Thwart('01001a')"],
       {"menace_de": [["hf204b", 3]]}, cibles=["hf204b"], accepter_choix=True),
    _c("hf204b Threat cannot be removed : TEMOIN, la meme action contre une side scheme (hf226 : 3 menaces) retire bien 1 menace",
       "contre-cas : l'interdiction ne vise que CE complot", [HEROS, "Puzzle.PutIntoPlay('hf226')"] + deck("01105"), ["Puzzle.Thwart('01001a')"],
       {"menace_de": [["hf226", 2]]}, cibles=["hf226"], accepter_choix=True),
    _c("hf204b Interruption forcee : contre un ALTER-EGO, Shaw (I) ne manigance pas : le joueur recoit 1 carte de rencontre face cachee a la place, menace du complot inchangee",
       "« When Sebastian Shaw would scheme against you, deal you 1 facedown encounter card instead »",
       deck("01105", "01105"), ["Puzzle.Scheme('hf201')"],
       {"distribuees": 1, "menace_de": [["hf204b", 0]]}),
    _c("hf204b stade 1 complete : « the players lose the game »",
       "« If this stage is completed, the players lose the game » : texte imprime lu par le moteur (cible 5 pour 1 joueur)",
       deck("01105"), ["Puzzle.PlaceThreat('hf204b', 5)"], {"gagnee": False, "partie_finie": True}),
    # ===================================================================== hf205a / hf205b : stade 2
    _c("hf205a When Revealed : chaque joueur recoit 1 carte face cachee et Black King se RETOURNE (hf207b)",
       "« Deal each player a facedown encounter card. Flip Black King attachment. »",
       deck("01105", "01105"), ["Puzzle.AdvanceMainScheme()"],
       {"en_jeu": ["hf205b", "hf207b"], "absents": ["hf204b", "hf207a"], "attache": [["hf207b", "hf201"]], "distribuees": 1}),
    _c("hf205a When Revealed : a DEUX joueurs chacun recoit sa carte (le joueur 1 en recoit 1)",
       "« each player »", deck("01105", "01105", "01105"), ["Puzzle.AdvanceMainScheme()"],
       {"en_jeu": ["hf207b"], "distribuees": 1}, heros2="spider_man"),
    _c("hf205b nombres : menace de depart 4 pour 1 joueur, cible 13 ; complete -> les joueurs perdent",
       "StartingThreat 4[par joueur], TargetThreat 13[par joueur], « If this stage is completed, the players lose the game »",
       deck("01105", "01105"), ["Puzzle.AdvanceMainScheme()", "Puzzle.PlaceThreat('hf205b', 9)"], {"gagnee": False, "partie_finie": True}),
    _c("hf205b menace de depart : 4",
       "nombres imprimes", deck("01105", "01105"), ["Puzzle.AdvanceMainScheme()"], {"menace_de": [["hf205b", 4]]}),
    _c("hf205b Hero Action : exhaust a CAPTIVE ally -> 2 compteurs d'energie retires de Shaw (5 -> 3), l'allie s'incline",
       "« Exhaust a CAPTIVE ally you control -> remove 2 energy counters from Sebastian Shaw »",
       [HEROS, "Puzzle.AdvanceMainScheme()", "Puzzle.PutIntoPlay('hf209', under_control=True)", "Puzzle.PlaceCounters('hf201', 'energy', 5)"] + deck("01105"),
       ["Puzzle.Action('hf205b', 'HeroAction')"],
       {"compteurs_sur": [["hf201", "energy", 3]], "exhausted": ["hf209"]}),
    _c("hf205b Hero Action : TEMOIN D'EPUISEMENT, DEUX captifs prets mais une seule Action par round et par joueur -> 5 -> 3 (pas 1), un seul captif incline",
       "« (Limit once per round per player.) » ; FAQ : meme avec plusieurs captifs on ne peut pas la declencher deux fois",
       [HEROS, "Puzzle.AdvanceMainScheme()", "Puzzle.PutIntoPlay('hf209', under_control=True)", "Puzzle.PutIntoPlay('hf211', under_control=True)",
        "Puzzle.PlaceCounters('hf201', 'energy', 5)"] + deck("01105"),
       ["Puzzle.Action('hf205b', 'HeroAction')"],
       {"compteurs_sur": [["hf201", "energy", 3]]}, declencher_tolerant=["Puzzle.Action('hf205b', 'HeroAction')"]),
    _c("hf205b Hero Action : la limite se renouvelle au round suivant -> 5 -> 3 -> 1",
       "limite PAR ROUND", [HEROS, "Puzzle.AdvanceMainScheme()", "Puzzle.PutIntoPlay('hf209', under_control=True)", "Puzzle.PutIntoPlay('hf211', under_control=True)",
        "Puzzle.PlaceCounters('hf201', 'energy', 5)"] + deck("01105"),
       ["Puzzle.Action('hf205b', 'HeroAction')", "Puzzle.ResetRoundStats()", "Puzzle.Action('hf205b', 'HeroAction')"],
       {"compteurs_sur": [["hf201", "energy", 1]]}),
    _c("hf205b stade 2 : Shaw manigane normalement (plus de remplacement par une carte face cachee) : SCH 2 -> menace 4 + 2 = 6, une seule carte distribuee (celle de 2A)",
       "le remplacement « deal you 1 facedown encounter card instead » est propre a 1B",
       deck("01105", "01105", "01105"), ["Puzzle.AdvanceMainScheme()", "Puzzle.Scheme('hf201')"],
       {"menace_de": [["hf205b", 6]], "distribuees": 1}),

    # ===================================================================== hf206 Captured by Hellfire!
    _c("hf206 When Defeated (1 joueur, 1 captif dessous) : le joueur qui la defait prend le captif en MAIN, la manigance va a la zone de victoire et le complot AVANCE a 2A (hf205b)",
       "« takes a random card from beneath here, and add it to their hand ... Otherwise, advance to main scheme 2A and add this card to the victory display »",
       [HEROS, "Puzzle.SetThreat('hf206', 1)"] + deck("01105", "01105", "01105"), ["Puzzle.Thwart('01001a')"],
       {"taille_main": 2, "victoire": ["hf206"], "absents": ["hf206", "hf204b"], "en_jeu": ["hf205b", "hf207b"]}, cibles=["hf206"], accepter_choix=True),
    _c("hf206 When Defeated : le captif libere est bien un des quatre allies CAPTIVE (jamais une autre carte)",
       "la carte prise est celle de DESSOUS", [HEROS, "Puzzle.SetThreat('hf206', 1)"] + deck("01105", "01105", "01105"), ["Puzzle.Thwart('01001a')"],
       {"hfk_main_captif": True}, cibles=["hf206"], accepter_choix=True),
    _c("hf206 When Defeated (2 joueurs, 2 captifs dessous) : 1er captif pris, il en reste 1 -> 5 menaces reposees, la manigance RESTE en jeu (Permanent), le complot n'avance PAS",
       "« After that, if there still has card under this scheme, place 5 threat here »",
       [HEROS, "Puzzle.SetThreat('hf206', 1)"] + deck("01105", "01105", "01105"), ["Puzzle.Thwart('01001a')"],
       {"taille_main": 2, "menace_de": [["hf206", 5]], "taille_pose_sous": [["hf206", 1]], "en_jeu": ["hf206", "hf204b"], "absents": ["hf205b"]},
       cibles=["hf206"], accepter_choix=True, heros2="spider_man"),
    _c("hf206 When Defeated (2 joueurs) : la 2e defaite prend le dernier captif -> victoire + complot 2A",
       "boucle complete : 2 captifs, 2 defaites",
       [HEROS, "Puzzle.SetThreat('hf206', 1)"] + deck("01105", "01105", "01105", "01105"),
       ["Puzzle.Thwart('01001a')", "Puzzle.Ready('01001a')", "Puzzle.SetThreat('hf206', 1)", "Puzzle.Thwart('01001a')"],
       {"taille_main": 3, "victoire": ["hf206"], "absents": ["hf206", "hf204b"], "en_jeu": ["hf205b"]},
       cibles=["hf206"], accepter_choix=True, heros2="spider_man"),
    _c("hf206 Permanent : tant qu'il reste un captif la manigance ne quitte pas le jeu apres sa defaite (pas de zone de victoire)",
       "mot-cle Permanent : le moteur envoie « When Defeated » sans defausser la carte", [HEROS, "Puzzle.SetThreat('hf206', 1)"] + deck("01105", "01105", "01105"),
       ["Puzzle.Thwart('01001a')"], {"en_jeu": ["hf206"], "hors_victoire": ["hf206"]}, cibles=["hf206"], accepter_choix=True, heros2="spider_man"),
    # ===================================================================== les quatre captifs
    _c("hf208 Dust : l'attaque vise un sbire engage (Tiger Shark) ET le vilain : 2 degats a chacun (Absorb : 2 compteurs sur Shaw)",
       "« Interrupt : When Dust attacks, resolve this attack against the villain and each minion engaged with you »",
       [HEROS, "Puzzle.PutIntoPlay('hf208', under_control=True)", "Puzzle.PutIntoPlay('01131')"] + deck("01105"), ["Puzzle.Attack('hf208')"],
       {"degats_de": [["01131", 2], ["hf201", 2]], "compteurs_sur": [["hf201", "energy", 2]]}, cibles=["01131"], accepter_choix=True),
    _c("hf208 Dust : TEMOIN, un sbire engage avec un AUTRE joueur n'est pas touche (2 joueurs)",
       "« each minion engaged with YOU » : seulement les sbires engages avec le controleur de Dust",
       [HEROS, "Puzzle.PutIntoPlay('hf208', under_control=True)", "Puzzle.PutIntoPlay('01131')", "Puzzle.PutIntoPlay('01110')", "Puzzle.Engage('01110', 1)"] + deck("01105"),
       ["Puzzle.Attack('hf208')"],
       {"degats_de": [["01131", 2], ["hf201", 2], ["01110", 0]]}, cibles=["01131"], accepter_choix=True, heros2="spider_man"),
    _c("hf208 Dust : l'attaque vise le VILAIN : le sbire engage est touche aussi (pas de doublon sur le vilain : 2 degats, pas 4)",
       "`AlsoResolveThisAttackTo` ne duplique jamais la cible deja visee",
       [HEROS, "Puzzle.PutIntoPlay('hf208', under_control=True)", "Puzzle.PutIntoPlay('01131')"] + deck("01105"), ["Puzzle.Attack('hf208')"],
       {"degats_de": [["01131", 2], ["hf201", 2]]}, cibles=["hf201"], accepter_choix=True),
    _c("hf209 Mercury : valeurs imprimees (PV 5, Toughness : arrive avec un statut Robuste)",
       "nombres texte <-> code ; Toughness natif (desc)",
       [HEROS, "Puzzle.PutIntoPlay('hf209', under_control=True)"] + deck("01105"), [],
       {"en_jeu": ["hf209"], "vie": [["hf209", 5]], "statuts": [["hf209", "Tough"]]}),
    _c("hf210 Surge : elle attaque le vilain -> Shaw est ETOURDI (Interruption)",
       "« Interrupt : When Surge attacks an enemy, that enemy get stunned »",
       [HEROS, "Puzzle.PutIntoPlay('hf210', under_control=True)"] + deck("01105"), ["Puzzle.Attack('hf210')"],
       {"statuts": [["hf201", "Stunned"]]}, cibles=["hf201"], accepter_choix=True),
    _c("hf210 Surge : TEMOIN, Mercury (sans texte) attaque le vilain -> pas d'etourdissement",
       "contre-cas : l'effet est propre a Surge", [HEROS, "Puzzle.PutIntoPlay('hf209', under_control=True)"] + deck("01105"), ["Puzzle.Attack('hf209')"],
       {"statuts_absents": [["hf201", "Stunned"]]}, cibles=["hf201"], accepter_choix=True),
    _c("hf211 Prodigy : jouee DEPUIS LA MAIN -> pioche 1 carte (main 1 : la carte piochee)",
       "« Response : After you play Prodigy from hand, draw 1 card »",
       [HEROS] + deck("01105"), [], {"en_jeu": ["hf211"], "taille_main": 1}, main_exclusive=["hf211", "01090"], payer_avec=["01090"], jouer=["hf211"]),
    _c("hf211 Prodigy : TEMOIN, mise en jeu autrement que depuis la main -> pas de pioche (la main reste a la seule carte de depart, 01090)",
       "« from hand » : une mise en jeu par un effet ne pioche pas", [HEROS, "Puzzle.PutIntoPlay('hf211', under_control=True)"] + deck("01105"), [],
       {"en_jeu": ["hf211"], "taille_main": 1}),
    _c("hf208 RECRUITED : un captif note « Recruited » au carnet porte le trait RECRUITED (scenarios suivants)",
       "livret p. 10 : « These allies can be used for the rest of the campaign as have the RECRUITED trait » ; ici le carnet le note",
       [HEROS, "Puzzle.EmptyHand()"], ["Puzzle.HellfireCampagne(3, {'Recruited Allies': 'hf208'})", "Puzzle.PutIntoPlay('hf208', under_control=True)"],
       {"en_jeu": ["hf208"], "trait_de": [["hf208", "RECRUITED", True], ["hf208", "CAPTIVE", True]]}),
    _c("hf209 RECRUITED : Mercury note « Recruited » au carnet porte le trait RECRUITED (scenarios suivants)",
       "livret p. 10 : « can be used for the rest of the campaign as have the RECRUITED trait »",
       [HEROS, "Puzzle.EmptyHand()"], ["Puzzle.HellfireCampagne(3, {'Recruited Allies': 'hf209'})", "Puzzle.PutIntoPlay('hf209', under_control=True)"],
       {"en_jeu": ["hf209"], "trait_de": [["hf209", "RECRUITED", True], ["hf209", "CAPTIVE", True]]}),
    _c("hf210 RECRUITED : Surge note « Recruited » au carnet porte le trait RECRUITED (scenarios suivants)",
       "livret p. 10 : « can be used for the rest of the campaign as have the RECRUITED trait »",
       [HEROS, "Puzzle.EmptyHand()"], ["Puzzle.HellfireCampagne(3, {'Recruited Allies': 'hf210'})", "Puzzle.PutIntoPlay('hf210', under_control=True)"],
       {"en_jeu": ["hf210"], "trait_de": [["hf210", "RECRUITED", True], ["hf210", "CAPTIVE", True]]}),
    _c("hf211 RECRUITED : Prodigy note « Recruited » au carnet porte le trait RECRUITED (scenarios suivants)",
       "livret p. 10 : « can be used for the rest of the campaign as have the RECRUITED trait »",
       [HEROS, "Puzzle.EmptyHand()"], ["Puzzle.HellfireCampagne(3, {'Recruited Allies': 'hf211'})", "Puzzle.PutIntoPlay('hf211', under_control=True)"],
       {"en_jeu": ["hf211"], "trait_de": [["hf211", "RECRUITED", True], ["hf211", "CAPTIVE", True]]}),
    _c("hf208 RECRUITED : TEMOIN, dans le scenario 2 lui-meme (carnet sans lui) il n'est PAS Recruited",
       "la libération n'est notée qu'à la victoire", [HEROS, "Puzzle.PutIntoPlay('hf208', under_control=True)"] + deck("01105"), [],
       {"en_jeu": ["hf208"], "trait_de": [["hf208", "RECRUITED", False]]}),
    # ===================================================================== campagne : mise en place et releve
    _c("campagne scenario 2 : Emma Frost's Redemption revelee et Xavier's Institute en jeu ; les 16 allies de cote",
       "livret p. 10, Setup de campagne : « Reveal the Emma Frost's Redemption side scheme. Put Xavier's Institute into play. Create a Recruited Mutants Deck »",
       [HEROS, "Puzzle.EmptyHand()"], ["Puzzle.HellfireCampagne(2)"],
       {"en_jeu": ["hf042", "hf048"], "hfk_recrutes_deck": []}),
    _c("campagne scenario 2 : un captif deja note Recruited (Dust) rejoint le deck Recruited Mutants des le debut",
       "le carnet note hf208 ; `_allies_recrutes` l'accepte (CAPTIFS)", [HEROS, "Puzzle.EmptyHand()"],
       ["Puzzle.HellfireCampagne(2, {'Recruited Allies': 'hf208;hf013'})"],
       {"hfk_recrutes_deck": ["hf013", "hf208"]}),
    _c("campagne releve : un captif LIBERE (en main) est note « Recruited » au carnet, un captif encore de cote ou cache sous la manigance non",
       "livret p. 10 : « Record the name of each CAPTIVE ally ... as Recruited »",
       [HEROS, "Puzzle.EmptyHand()", "Puzzle.Gain('hf209')"], ["Puzzle.HellfireReleve(2, True)"],
       {"hfk_releve": {"Recruited Allies": "hf209"}}, main_exclusive=["hf209"]),
    _c("campagne releve : un captif de la DEFAUSSE du joueur est lui aussi note ; le captif cache sous Captured by Hellfire! non",
       "« in each player's deck and discard pile »", [HEROS, "Puzzle.EmptyHand()", "Puzzle.CreatePlayerDiscardPile('hf210')"], ["Puzzle.HellfireReleve(2, True)"],
       {"hfk_releve": {"Recruited Allies": "hf210"}}),
    _c("campagne releve : a la DEFAITE rien n'est note",
       "livret p.5 : « defeat : replay without penalty »", [HEROS, "Puzzle.EmptyHand()", "Puzzle.Gain('hf209')"], ["Puzzle.HellfireReleve(2, False)"],
       {"hfk_releve": {}}, main_exclusive=["hf209"]),

    # ===================================================================== hf212-hf215 Ebon Knight
    _c("hf212 Ebon Knight : valeurs imprimees (PV 2, ATK 2, SCH 2), Guard + Patrol + Quickstrike (desc) ; Quickstrike : il attaque a l'engagement (heros incline : 2 degats)",
       "nombres texte <-> code ; mots-cles natifs ; « Quickstrike » : le sbire attaque des qu'il s'engage avec un HEROS",
       [HEROS, "Puzzle.Exhaust('01001a')"] + deck("hf212", "01105"), ["Puzzle.Reveal('hf212')"],
       {"en_jeu": ["hf212"], "vie": [["hf212", 2]], "attaque": [["hf212", 2]], "mots": [["hf212", "Guard", 1], ["hf212", "Patrol", 1], ["hf212", "Quickstrike", 1]],
        "degats_identite": 2, "trait_de": [["hf212", "HELLFIRE", True]]}),
    _c("hf212 Boost : Shaw attaque avec Ebon Knight en boost (1 icone : 0 + 1 = 1 degat) -> APRES l'activation Ebon Knight est distribue au joueur face cachee",
       "« [star] Boost : After this activation, deal Ebon Knight to you as a facedown encounter card »",
       [HEROS, "Puzzle.Exhaust('01001a')"] + deck("hf212", "01105", "01105"), ["Puzzle.Attack('hf201')"],
       {"degats_identite": 1, "distribuee_id": "hf212", "distribuees": 1}),
    _c("hf212 Boost : TEMOIN, une carte de boost sans effet (Bomb Scare) -> rien n'est distribue",
       "contre-cas", [HEROS, "Puzzle.Exhaust('01001a')"] + deck("01105", "01105"), ["Puzzle.Attack('hf201')"],
       {"distribuees": 0}),
    _c("hf213 Ebon Knight (2e exemplaire) : meme carte, meme boost",
       "chacun des 4 exemplaires (hf212-hf215) porte le script", [HEROS, "Puzzle.Exhaust('01001a')"] + deck("hf213", "01105", "01105"), ["Puzzle.Attack('hf201')"],
       {"distribuee_id": "hf213", "distribuees": 1}),
    _c("hf214 Ebon Knight (3e exemplaire) : meme boost", "3e exemplaire", [HEROS, "Puzzle.Exhaust('01001a')"] + deck("hf214", "01105", "01105"), ["Puzzle.Attack('hf201')"],
       {"distribuee_id": "hf214", "distribuees": 1}),
    _c("hf215 Ebon Knight (4e exemplaire) : meme boost", "4e exemplaire", [HEROS, "Puzzle.Exhaust('01001a')"] + deck("hf215", "01105", "01105"), ["Puzzle.Attack('hf201')"],
       {"distribuee_id": "hf215", "distribuees": 1}),
    # ===================================================================== hf216-hf217 Inhibitor Collar
    _c("hf216 Inhibitor Collar : revele, s'attache a l'IDENTITE du joueur et son texte imprime devient blanc",
       "« Attach to your identity. Treat your identity's printed text box as blank (except for TRAITS) »",
       deck("hf216", "01105"), ["Puzzle.Reveal('hf216')"],
       {"en_jeu": ["hf216"], "attache": [["hf216", "01001b"]], "texte_blanc": [["01001b", True]]}),
    _c("hf216 Inhibitor Collar : TEMOIN, sans collier le texte de l'identite n'est pas blanc",
       "contre-cas", deck("01105"), [], {"texte_blanc": [["01001b", False]]}),
    _c("hf216 Alter-Ego Action : depenser [physical][physical] (2 Strength) defausse le collier",
       "« Spend [physical][physical] resources -> discard this card » : Strength (01090) vaut RR a elle seule",
       deck("hf216", "01105"), ["Puzzle.Reveal('hf216')", "Puzzle.Action('hf216', 'AlterEgoAction')"],
       {"absents": ["hf216"], "defausse_rencontre": ["hf216"], "texte_blanc": [["01001b", False]]}, main_exclusive=["01090"], payer_avec=["01090"], accepter_choix=True),
    _c("hf216 Alter-Ego Action : TEMOIN, une seule ressource ne suffit pas -> le collier reste",
       "cout = DEUX ressources physiques ; Helicarrier (01092) n'en offre qu'UNE", deck("hf216", "01105"), ["Puzzle.Reveal('hf216')", "Puzzle.Action('hf216', 'AlterEgoAction')"],
       {"en_jeu": ["hf216"]}, main_exclusive=["01092"]),
    _c("hf216 Alter-Ego Action : ANY PLAYER, le 2e joueur defausse le collier du 1er avec SES deux ressources",
       "« Any player may trigger this ability » : collier sur l'identite du joueur 1, action declenchee par le joueur 2 (siege 1) ; le collier est defausse",
       deck("hf216", "01105"), ["Puzzle.Reveal('hf216')", "Puzzle.Action('hf216', 'AlterEgoAction', siege=1)"],
       {"absents": ["hf216"]}, main_exclusive=["01090", "01090"], payer_avec=["01090", "01090"], payer_tout=True, accepter_choix=True, heros2="spider_man"),
    _c("hf216 Boost : Shaw (1 compteur : ATK 1 + 2 icones = 3) attaque, Black Cat (PV 2) defend : avec OVERKILL l'exces (1) passe au heros",
       "« [star] Boost : If this activation is an attack, this attack gains overkill »",
       [HEROS, "Puzzle.PutIntoPlay('01002', under_control=True)", "Puzzle.PlaceCounters('hf201', 'energy', 1)"] + deck("hf216", "01105", "01105"),
       ["Puzzle.Attack('hf201', defender='01002')"],
       {"degats_identite": 1, "defausse": ["01002"]}),
    _c("hf216 Boost : TEMOIN, sans le collier (Bomb Scare en boost : 0 icone, ATK 1) Black Cat (PV 2) encaisse et ne passe rien au heros",
       "contre-cas : pas d'overkill", [HEROS, "Puzzle.PutIntoPlay('01002', under_control=True)", "Puzzle.PlaceCounters('hf201', 'energy', 3)"] + deck("01105", "01105", "01105"),
       ["Puzzle.Attack('hf201', defender='01002')"], {"degats_identite": 0}),
    _c("hf217 Inhibitor Collar (2e exemplaire) : s'attache a l'identite, texte blanc",
       "2e exemplaire", deck("hf217", "01105"), ["Puzzle.Reveal('hf217')"],
       {"en_jeu": ["hf217"], "attache": [["hf217", "01001b"]], "texte_blanc": [["01001b", True]]}),
    # ===================================================================== hf218-hf219 Targeted by Hellfire
    _c("hf218 Targeted by Hellfire : revelee, s'attache a l'identite (alter-ego)",
       "« Attach to your identity if a copy of Targeted by Hellfire is not attached to you »",
       deck("hf218", "01105"), ["Puzzle.Reveal('hf218')"], {"en_jeu": ["hf218"], "attache": [["hf218", "01001b"]]}),
    _c("hf218 Targeted by Hellfire : Reponse forcee, le joueur passe en forme HEROS -> Shaw (+2 compteurs d'ATK : consommes) et chaque sbire HELLFIRE engage (Ebon Knight) attaquent, la carte est defaussee ; le sbire non-HELLFIRE (Tiger Shark) n'attaque pas",
       "« After you change to hero form, Sebastian Shaw and each HELLFIRE minion engaged with you attacks you. Discard this card » : le heros defend contre la 1re attaque (Shaw : 2) et, incline, subit la 2e (Ebon Knight : 2) ; Tiger Shark (ATK 3) n'attaque pas : total 2",
       ["Puzzle.PlaceCounters('hf201', 'energy', 2)"] + deck("hf218", "01105"),
       ["Puzzle.Reveal('hf218')", "Puzzle.PutIntoPlay('hf212')", "Puzzle.PutIntoPlay('01131')", "Puzzle.ChangeForm('01001a')"],
       {"absents": ["hf218"], "compteurs_sur": [["hf201", "energy", 0]], "degats_identite": 2}),
    _c("hf218 Targeted by Hellfire : TEMOIN, un changement de forme vers l'ALTER-EGO ne declenche rien (la carte reste attachee)",
       "« change to HERO form »", [HEROS] + deck("hf218", "01105"), ["Puzzle.Reveal('hf218')", "Puzzle.ChangeForm('01001b')"],
       {"en_jeu": ["hf218"], "attache": [["hf218", "01001b"]]}),
    _c("hf218 Targeted by Hellfire : un 2e exemplaire (hf219) ne s'attache pas a un joueur qui en porte deja un : il gagne surge (la carte suivante, Mutant Experimentation, est revelee)",
       "« Otherwise, this card gains surge »",
       ["Puzzle.PutIntoPlay('hf218', under_control=True)"] + deck("hf219", "hf226", "01105"), ["Puzzle.Reveal('hf219')"],
       {"nb_en_jeu": [["hf218", 1], ["hf219", 0]], "en_jeu": ["hf226"]}),
    _c("hf219 Targeted by Hellfire (2e exemplaire) : s'attache et fonctionne comme hf218",
       "2e exemplaire", deck("hf219", "01105"), ["Puzzle.Reveal('hf219')"], {"en_jeu": ["hf219"], "attache": [["hf219", "01001b"]]}),
    # ===================================================================== hf220-hf221 Mutant Suppression
    _c("hf220 Mutant Suppression : When Revealed, l'identite ET chaque allie du joueur sont incline",
       "« Exhaust your identity and each ally you control »", ["Puzzle.PutIntoPlay('01002', under_control=True)"] + deck("hf220", "01105"), ["Puzzle.Reveal('hf220')"],
       {"exhausted": ["01001b", "01002"]}),
    _c("hf220 Mutant Suppression : Boost, apres l'activation de Shaw (stade 2, contre l'alter-ego) l'identite est inclinee et Shaw gagne 1 compteur",
       "« [star] Boost : After this activation, exhaust your identity and place 1 energy counter on Sebastian Shaw »",
       deck("01105", "hf220", "01105", "01105") + ["Puzzle.AdvanceMainScheme()"], ["Puzzle.Scheme('hf201')"],
       {"exhausted": ["01001b"], "compteurs_sur": [["hf201", "energy", 1]]}),
    _c("hf220 Mutant Suppression : TEMOIN, boost sans effet -> identite prete, aucun compteur",
       "contre-cas", deck("01105", "01105", "01105") + ["Puzzle.AdvanceMainScheme()"], ["Puzzle.Scheme('hf201')"], {"pret": ["01001b"], "compteurs_sur": [["hf201", "energy", 0]]}),
    _c("hf221 Mutant Suppression (2e exemplaire) : identite et allie incline",
       "2e exemplaire", ["Puzzle.PutIntoPlay('01002', under_control=True)"] + deck("hf221", "01105"), ["Puzzle.Reveal('hf221')"], {"exhausted": ["01001b", "01002"]}),
    # ===================================================================== hf222-hf223 Hellfire Indoctrination
    _c("hf222 Hellfire Indoctrination : un captif ET un allie ordinaire sont desorientes, la carte NE gagne PAS surge (Mutant Experimentation reste dans le deck)",
       "« Confuse each ally you control. If there is no CAPTIVE ally is confused in this way, this gains surge »",
       ["Puzzle.PutIntoPlay('hf209', under_control=True)", "Puzzle.PutIntoPlay('01002', under_control=True)"] + deck("hf222", "hf226", "01105"), ["Puzzle.Reveal('hf222')"],
       {"statuts": [["hf209", "Confused"], ["01002", "Confused"]], "absents": ["hf226"]}),
    _c("hf222 Hellfire Indoctrination : AUCUN captif (allie ordinaire seul) -> desoriente, et la carte gagne surge (Mutant Experimentation revelee)",
       "« If there is no CAPTIVE ally is confused in this way, this gains surge »",
       ["Puzzle.PutIntoPlay('01002', under_control=True)"] + deck("hf222", "hf226", "01105"), ["Puzzle.Reveal('hf222')"],
       {"statuts": [["01002", "Confused"]], "en_jeu": ["hf226"]}),
    _c("hf222 Hellfire Indoctrination : sans aucun allie -> surge",
       "aucun captif desoriente", deck("hf222", "hf226", "01105"), ["Puzzle.Reveal('hf222')"], {"en_jeu": ["hf226"]}),
    _c("hf222 Hellfire Indoctrination : le captif etait DEJA desoriente -> pas desoriente « de cette facon » -> surge",
       "« confused IN THIS WAY » : un captif deja desoriente ne compte pas",
       ["Puzzle.PutIntoPlay('hf209', under_control=True)", "Puzzle.Confuse('hf209')"] + deck("hf222", "hf226", "01105"), ["Puzzle.Reveal('hf222')"],
       {"en_jeu": ["hf226"]}),
    _c("hf222 Hellfire Indoctrination : Boost, apres l'activation de Shaw -> 2 compteurs d'energie",
       "« [star] Boost : After this activation, place 2 energy counters on Sebastian Shaw »", [HEROS, "Puzzle.Exhaust('01001a')"] + deck("hf222", "01105", "01105"), ["Puzzle.Attack('hf201')"],
       {"compteurs_sur": [["hf201", "energy", 2]]}),
    _c("hf223 Hellfire Indoctrination (2e exemplaire) : captif desoriente, pas de surge",
       "2e exemplaire", ["Puzzle.PutIntoPlay('hf209', under_control=True)"] + deck("hf223", "hf226", "01105"), ["Puzzle.Reveal('hf223')"],
       {"statuts": [["hf209", "Confused"]], "absents": ["hf226"]}),
    # ===================================================================== hf224-hf225 Energic Backlash
    _c("hf224 Energic Backlash : When Revealed (ALTER-EGO) -> 4 compteurs d'energie sur Shaw",
       "« When Revealed (Alter-Ego) : Place 4 energy counters on Sebastian Shaw »", deck("hf224", "01105"), ["Puzzle.Reveal('hf224')"],
       {"compteurs_sur": [["hf201", "energy", 4]], "degats_identite": 0}),
    _c("hf224 Energic Backlash : When Revealed (HERO) -> 2 compteurs, puis Shaw attaque : ses 2 compteurs deviennent +2 ATK (2 degats, heros incline)",
       "« When Revealed (Hero) : Place 2 energy counters on Sebastian Shaw. Sebastian Shaw attacks you »",
       [HEROS, "Puzzle.Exhaust('01001a')"] + deck("hf224", "01105"), ["Puzzle.Reveal('hf224')"],
       {"compteurs_sur": [["hf201", "energy", 0]], "degats_identite": 2}),
    _c("hf224 Energic Backlash : Boost, apres l'activation de Shaw -> 3 compteurs d'energie",
       "« [star] Boost : After this activation, place 3 energy counters on Sebastian Shaw »", [HEROS, "Puzzle.Exhaust('01001a')"] + deck("hf224", "01105", "01105"), ["Puzzle.Attack('hf201')"],
       {"compteurs_sur": [["hf201", "energy", 3]]}),
    _c("hf225 Energic Backlash (2e exemplaire) : alter-ego -> 4 compteurs", "2e exemplaire", deck("hf225", "01105"), ["Puzzle.Reveal('hf225')"],
       {"compteurs_sur": [["hf201", "energy", 4]]}),
    # ===================================================================== hf226 Mutant Experimentation, hf227 Rage of Black King
    _c("hf226 Mutant Experimentation : menace de depart 3 (1 joueur), icone HAZARD 1, boost 2 (desc)",
       "nombres texte <-> code ; l'icone est HAZARD (carte penchee sans barre, comparee a hf318/hf039 (Hazard) et a l'Acceleration de hf035)",
       deck("hf226", "01105"), ["Puzzle.Reveal('hf226')"], {"menace_de": [["hf226", 3]], "mots": [["hf226", "Hazard", 1]]}),
    _c("hf226 When Defeated : le joueur doit choisir et defausser 1 carte de sa main (main 2 -> 1)",
       "« Each player must choose and discard 1 card from their hand »",
       [HEROS, "Puzzle.PutIntoPlay('hf226')", "Puzzle.SetThreat('hf226', 1)"] + deck("01105"), ["Puzzle.Thwart('01001a')"],
       {"absents": ["hf226"], "taille_main": 1}, main_exclusive=["01090", "01089"], cibles=["hf226"], accepter_choix=True),
    _c("hf226 When Defeated : A DEUX joueurs chacun defausse 1 carte (la main du joueur 1 : 2 -> 1)",
       "« Each player »", [HEROS, "Puzzle.PutIntoPlay('hf226')", "Puzzle.SetThreat('hf226', 1)"] + deck("01105"), ["Puzzle.Thwart('01001a')"],
       {"absents": ["hf226"], "taille_main": 1}, main_exclusive=["01090", "01089"], cibles=["hf226"], accepter_choix=True, heros2="spider_man"),
    _c("hf227 Rage of Black King : menace 2 + Hinder 1[par joueur] a l'entree en jeu = 3 (1 joueur)",
       "nombres texte <-> code ; Hinder natif", deck("hf227", "01105"), ["Puzzle.Reveal('hf227')"], {"menace_de": [["hf227", 3]], "mots": [["hf227", "Hinder", 1]]}),
    _c("hf227 Forced Response : apres l'activation de Shaw -> Shaw gagne un statut Robuste",
       "« After Sebastian Shaw activates, he gains a tough status card »", [HEROS, "Puzzle.Exhaust('01001a')", "Puzzle.PutIntoPlay('hf227')"] + deck("01105", "01105"), ["Puzzle.Attack('hf201')"],
       {"statuts": [["hf201", "Tough"]]}),
    _c("hf227 Forced Response : TEMOIN, sans la manigance Shaw n'a pas de statut Robuste", "contre-cas", [HEROS, "Puzzle.Exhaust('01001a')"] + deck("01105", "01105"), ["Puzzle.Attack('hf201')"],
       {"statuts_absents": [["hf201", "Tough"]]}),
    _c("hf227 When Defeated : le joueur choisit de placer 2 compteurs d'energie sur Shaw",
       "« Each player chooses to either place 2 energy counters on Sebastian Shaw or deal themselves 1 facedown encounter card »",
       [HEROS, "Puzzle.PutIntoPlay('hf227')", "Puzzle.SetThreat('hf227', 1)"] + deck("01105"), ["Puzzle.Thwart('01001a')"],
       {"absents": ["hf227"], "compteurs_sur": [["hf201", "energy", 2]], "distribuees": 0}, cibles=["hf227"], accepter_choix=True, preferer_option="Place 2 energy counters on Sebastian Shaw"),
    _c("hf227 When Defeated : l'autre branche, le joueur se distribue 1 carte face cachee (Shaw sans compteur)",
       "second choix", [HEROS, "Puzzle.PutIntoPlay('hf227')", "Puzzle.SetThreat('hf227', 1)"] + deck("01105"), ["Puzzle.Thwart('01001a')"],
       {"absents": ["hf227"], "compteurs_sur": [["hf201", "energy", 0]], "distribuees": 1}, cibles=["hf227"], accepter_choix=True, preferer_option="Deal yourself 1 facedown encounter card"),
    # ===================================================================== MODULE « Sebastian Shaw » : hf331-hf338
    _c("hf331 Sebastian Shaw (sbire) : valeurs imprimees (PV 6, ATK 2, SCH 1), ELITE HELLFIRE, Villainous ; Reponse forcee : degats subis -> autant de menace sur le complot (autre scenario : White Queen, car le vilain Shaw bloque le nom unique)",
       "« After Sebastian Shaw takes any amount of damage, place that amount of threat on the main scheme » : 1 degat -> 1 menace sur Infiltrating the Mansion (hf104b)",
       deck("hf331", "01105"), ["Puzzle.Reveal('hf331')", "Puzzle.Damage('hf331', 1)"],
       {"en_jeu": ["hf331"], "vie": [["hf331", 6]], "attaque": [["hf331", 2]], "menace_de": [["hf104b", 1]], "trait_de": [["hf331", "ELITE", True], ["hf331", "HELLFIRE", True]], "mots": [["hf331", "Villainous", 1]]}, scenario="hellfire_white_queen"),
    _c("hf331 Boost : Shaw (sbire) en boost de l'attaque de Shaw (vilain) -> le VILAIN recoit une carte de boost de plus (Hellfire Domination, 3 icones) : ATK 0 + 1 + 3 = 4 degats",
       "« [star] Boost : Give the villain a facedown boost card » : la carte supplementaire est retournee dans la MEME activation",
       [HEROS, "Puzzle.Exhaust('01001a')"] + deck("hf331", "hf338", "01105"), ["Puzzle.Attack('hf201')"],
       {"degats_identite": 4}),
    _c("hf331 Boost : TEMOIN, une carte de boost sans effet -> aucune carte de boost donnee au vilain",
       "contre-cas : meme pile, sans Shaw en boost (la 2e carte ne sert pas) : 0 degat", [HEROS, "Puzzle.Exhaust('01001a')"] + deck("01105", "hf338", "01105"), ["Puzzle.Attack('hf201')"],
       {"degats_identite": 0}),
    _c("hf332 Energy Absorption : revelee, s'attache a Sebastian Shaw ; il est blesse (3) : l'attaque du heros (2) est REMPLACEE par un soin de 2 (degats 3 -> 1), pas de statut Robuste, aucun compteur, la carte est mise de cote",
       "« heal that character for that amount instead of dealing damage ... Set aside this card »",
       [HEROS, "Puzzle.Damage('hf201', 3)"] + deck("hf332", "01105"), ["Puzzle.Reveal('hf332')", "Puzzle.Attack('01001a')"],
       {"degats_de": [["hf201", 1]], "compteurs_sur": [["hf201", "energy", 0]], "statuts_absents": [["hf201", "Tough"]], "absents": ["hf332"]}, cibles=["hf201"], accepter_choix=True),
    _c("hf332 Energy Absorption : Shaw intact -> rien a soigner : statut Robuste, aucun degat, carte mise de cote",
       "« If no damage was healed this way, give that character a tough status card »",
       [HEROS] + deck("hf332", "01105"), ["Puzzle.Reveal('hf332')", "Puzzle.Attack('01001a')"],
       {"degats_de": [["hf201", 0]], "statuts": [["hf201", "Tough"]], "absents": ["hf332"]}, cibles=["hf201"], accepter_choix=True),
    _c("hf332 Energy Absorption : revelee, elle est attachee a Shaw (mode scenario)",
       "« Attach to Sebastian Shaw »", deck("hf332", "01105"), ["Puzzle.Reveal('hf332')"], {"en_jeu": ["hf332"], "attache": [["hf332", "hf201"]]}),
    _c("hf332 Energy Absorption : dans un AUTRE scenario (vilain White Queen), elle s'attache au SBIRE Sebastian Shaw s'il est en jeu",
       "« Attach to Sebastian Shaw. Otherwise, attach to the villain » : la carte nommee est preferee", ["Puzzle.PutIntoPlay('hf331')"] + deck("hf332", "01105"), ["Puzzle.Reveal('hf332')"],
       {"en_jeu": ["hf332", "hf331"], "attache": [["hf332", "hf331"]]}, scenario="hellfire_white_queen"),
    _c("hf332 Energy Absorption : dans un AUTRE scenario sans Shaw (White Queen seule) -> elle s'attache au VILAIN",
       "« Otherwise, attach to the villain »", deck("hf332", "01105"), ["Puzzle.Reveal('hf332')"],
       {"en_jeu": ["hf332"], "attache": [["hf332", "hf101a"]]}, scenario="hellfire_white_queen"),
    _c("hf332 Energy Absorption : Max 1 par personnage, un 2e exemplaire (hf333) ne s'ajoute pas a Shaw",
       "« Max 1 per character »", ["Puzzle.PutIntoPlay('hf332')"] + deck("hf333", "01105"), ["Puzzle.Reveal('hf333')"],
       {"en_jeu": ["hf332"], "nb_en_jeu": [["hf332", 1], ["hf333", 0]]}),
    _c("hf333 Energy Absorption (2e exemplaire) : meme effet (soin 2 sur 3 degats)",
       "2e exemplaire", [HEROS, "Puzzle.Damage('hf201', 3)"] + deck("hf333", "01105"), ["Puzzle.Reveal('hf333')", "Puzzle.Attack('01001a')"],
       {"degats_de": [["hf201", 1]], "absents": ["hf333"]}, cibles=["hf201"], accepter_choix=True),
    _c("hf334 Energy Counterattack : revelee, attachee a Shaw ; le heros l'attaque -> Shaw (2 compteurs : 2 degats) contre-attaque D'ABORD le heros incline, puis l'attaque du heros passe (Shaw : 2) ; la carte est mise de cote",
       "« When a character attacks the attached character, the attached character attacks that character. (Resolve the attached character's attack first). Set aside this card »",
       [HEROS, "Puzzle.PlaceCounters('hf201', 'energy', 2)"] + deck("hf334", "01105", "01105"), ["Puzzle.Reveal('hf334')", "Puzzle.Attack('01001a')"],
       {"degats_identite": 2, "degats_de": [["hf201", 2]], "absents": ["hf334"]}, cibles=["hf201"], accepter_choix=True),
    _c("hf334 Energy Counterattack : attachee a Shaw -> attache (hf201)", "« Attach to Sebastian Shaw »", deck("hf334", "01105"), ["Puzzle.Reveal('hf334')"],
       {"en_jeu": ["hf334"], "attache": [["hf334", "hf201"]]}),
    _c("hf334 Energy Counterattack : TEMOIN, un SBIRE (pas un personnage) n'attaque pas Shaw -> la carte reste attachee (rien ne se declenche) : Shaw ne contre-attaque pas",
       "« When a CHARACTER attacks » : heros / allies seulement", [HEROS, "Puzzle.Exhaust('01001a')", "Puzzle.PutIntoPlay('01131')"] + deck("hf334", "01105"), ["Puzzle.Reveal('hf334')"],
       {"en_jeu": ["hf334"], "degats_identite": 0}),
    _c("hf335 Energy Counterattack (2e exemplaire) : meme effet", "2e exemplaire", [HEROS, "Puzzle.PlaceCounters('hf201', 'energy', 2)"] + deck("hf335", "01105", "01105"),
       ["Puzzle.Reveal('hf335')", "Puzzle.Attack('01001a')"], {"degats_identite": 2, "absents": ["hf335"]}, cibles=["hf201"], accepter_choix=True),
    _c("hf336 Ambient Energy Absorption : un attachement Shaw de COTE (Energy Absorption) est revele, s'attache a Shaw ; la carte devient une carte de boost de Shaw (1 boost face cachee)",
       "« Choose a set-aside Sebastian Shaw attachment and reveal it. Give this card to the enemy who attached that attachment as a facedown boost card »",
       ["Puzzle.MoveTo('hf332', 'AsideScenario')"] + deck("hf336", "01105"), ["Puzzle.Reveal('hf336')"],
       {"en_jeu": ["hf332"], "attache": [["hf332", "hf201"]], "boosts_de": [["hf201", 1]]}),
    _c("hf336 Ambient Energy Absorption : aucun attachement Shaw de cote -> la carte gagne surge (Mutant Experimentation revelee)",
       "« Otherwise, this card gains surge »", deck("hf336", "hf226", "01105"), ["Puzzle.Reveal('hf336')"], {"en_jeu": ["hf226"], "boosts_de": [["hf201", 0]]}),
    _c("hf336 Ambient Energy Absorption : Boost, Shaw recoit 1 carte de boost de PLUS pour cette activation (2 boosts : Bomb Scare + le boost supplementaire = ATK 0 + 0)",
       "« [star] Boost : Give this enemy 1 additional boost card for this activation » : la 2e carte (Hellfire Hunt hf338, 3 icones) ajoute +3 ATK",
       [HEROS, "Puzzle.Exhaust('01001a')"] + deck("hf336", "hf338", "01105"), ["Puzzle.Attack('hf201')"],
       {"degats_identite": 4}),
    _c("hf337 Ambient Energy Absorption (2e exemplaire) : meme effet", "2e exemplaire", ["Puzzle.MoveTo('hf334', 'AsideScenario')"] + deck("hf337", "01105"), ["Puzzle.Reveal('hf337')"],
       {"en_jeu": ["hf334"], "attache": [["hf334", "hf201"]], "boosts_de": [["hf201", 1]]}),
    _c("hf338 Hellfire Domination : menace de depart 3 (1 joueur), icone AMPLIFY 1, boost 3 (desc)",
       "nombres texte <-> code ; icone = AMPLIFY (avion + croix, comparee a hf029/hf042 et a l'Amplify 16054 ; ni l'Acceleration (barre dessous) ni le Hazard)", deck("hf338", "01105"), ["Puzzle.Reveal('hf338')"],
       {"menace_de": [["hf338", 3]], "mots": [["hf338", "Amplify", 1]]}),
    _c("hf338 When Defeated : tous les attachements Shaw mis de cote retournent dans le deck de rencontre",
       "« Shuffle each set-aside Sebastian Shaw encounter card into the encounter deck »",
       [HEROS, "Puzzle.PutIntoPlay('hf338')", "Puzzle.SetThreat('hf338', 1)", "Puzzle.MoveTo('hf332', 'AsideScenario')", "Puzzle.MoveTo('hf334', 'AsideScenario')"] + deck("01105"),
       ["Puzzle.Thwart('01001a')"], {"absents": ["hf338"], "dans_deck_rencontre": ["hf332", "hf334"]}, cibles=["hf338"], accepter_choix=True),
    _c("hf338 When Defeated : TEMOIN, une carte de COTE d'un autre set (Black King hf207) n'est pas melangee",
       "« each set-aside SEBASTIAN SHAW encounter card »",
       [HEROS, "Puzzle.PutIntoPlay('hf338')", "Puzzle.SetThreat('hf338', 1)", "Puzzle.MoveTo('hf332', 'AsideScenario')", "Puzzle.MoveTo('hf216', 'AsideScenario')"] + deck("01105"),
       ["Puzzle.Thwart('01001a')"], {"dans_deck_rencontre": ["hf332"], "hors_deck_rencontre": ["hf216"]}, cibles=["hf338"], accepter_choix=True),
]

VERIFICATIONS = r'''
def hfk_etat(monde, aides):
    """Extensions de `etat_attendu` (meme famille que bb_etat) : compteurs_sur [[id, nom, n]], menace_de [[id, n]], attaque [[id, n]], vie [[id, pv_max]],
    degats_de [[id, n]], statuts_sur [[id, 'stunned'|'tough'|'confused', n]], absents [ids hors jeu], trait_de [[id, TRAIT, bool]],
    attache [[carte, hote]], boosts_de [[id, n]] (cartes de boost face cachee sur la carte), le reste va a etat_attendu."""
    attendu = aides["cas"].get("attendu") or {}
    # FILET (26/10/2026) : le moteur AVALE les exceptions des scripts de cartes (PROCESSUS-CARTE etape 7, point 6) ; un cas ne doit donc JAMAIS passer
    # au vert si le journal contient une trace d'exception.
    try:
        import os as _os
        _journal = open(f"/tmp/capacites_{_os.environ.get('CAS_PREFIX', '')}{aides['index']}.log", encoding="utf-8", errors="replace").read()
        _trace = [l for l in _journal.splitlines() if "Traceback" in l]
    except Exception:
        _trace = []
    propres = ("texte_blanc", "mots", "distribuee_id", "hors_victoire", "hfk_main_captif", "victoire", "hfk_recrutes_deck", "hfk_releve", "stalwart", "aside_nb_captifs", "aside_absents", "compteurs_sur", "menace_de", "attaque", "vie", "degats_de", "statuts_sur", "absents", "trait_de", "attache", "boosts_de", "steady", "acceleration", "gagnee", "partie_finie", "nb_en_jeu", "distribuees", "hors_deck_rencontre", "peut_defendre", "hote_pic")
    reste = {k: v for k, v in attendu.items() if k not in propres}
    copie = dict(aides); copie["cas"] = dict(aides["cas"]); copie["cas"]["attendu"] = reste
    ok, msg = etat_attendu(monde, copie)
    soucis = [] if ok else [msg]
    if _trace:
        soucis.append("le journal contient une exception avalee par le moteur (Traceback)")
    par_id = aides["par_id"]
    def face(cid):
        f = par_id(monde, cid)
        if f is None:
            soucis.append(f"{cid} n'est pas en jeu")
        return f
    if "aside_nb_captifs" in attendu:
        vus = [getattr(f.paper, "card_id", None) for f in monde.aside_deck.GetAll() if getattr(f.paper, "card_id", None) in ("hf208", "hf209", "hf210", "hf211")]
        if len(vus) != attendu["aside_nb_captifs"]:
            soucis.append(f"{len(vus)} captif(s) de cote (attendu {attendu['aside_nb_captifs']}) : {vus}")
    for cid, voulu in attendu.get("texte_blanc", []):
        f = face(cid)
        if f is not None and bool(f.is_treat_as_if_blank) != voulu:
            soucis.append(f"{cid} texte blanc = {f.is_treat_as_if_blank} (attendu {voulu})")
    for cid, mot, voulu in attendu.get("mots", []):
        f = face(cid)
        if f is not None and f.GetKeyword(mot) != voulu:
            soucis.append(f"{cid} mot-cle {mot} = {f.GetKeyword(mot)} (attendu {voulu})")
    if "distribuee_id" in attendu:
        ids = [getattr(f.paper, "card_id", None) for f in monde.players[0].dealt_encounter_cards.Get(True)]
        if attendu["distribuee_id"] not in ids:
            soucis.append(f"{attendu['distribuee_id']} n'est pas dans les cartes distribuees ({ids})")
    for cid in attendu.get("hors_victoire", []):
        if cid in [getattr(f.paper, "card_id", None) for f in monde.victory_display.GetAll()]:
            soucis.append(f"{cid} est deja dans la zone de victoire")
    if attendu.get("hfk_main_captif"):
        ids = [getattr(f.paper, "card_id", None) for f in monde.players[0].hand_cards.GetAll() if getattr(f.paper, "card_id", None) != "01090"]
        if len(ids) != 1 or ids[0] not in ("hf208", "hf209", "hf210", "hf211"):
            soucis.append(f"la main ne contient pas un captif : {ids}")
    for cid in attendu.get("victoire", []):
        if cid not in [getattr(f.paper, "card_id", None) for f in monde.victory_display.GetAll()]:
            soucis.append(f"{cid} n'est pas dans la zone de victoire")
    if "hfk_recrutes_deck" in attendu:
        etat = getattr(monde, "hf_recruited", None)
        deck_ids = sorted(getattr(f.paper, "card_id", None) for f in etat[0].Get(True)) if etat else []
        if deck_ids != sorted(attendu["hfk_recrutes_deck"]):
            soucis.append(f"deck Recruited Mutants = {deck_ids} (attendu {sorted(attendu['hfk_recrutes_deck'])})")
    if "hfk_releve" in attendu:
        releve = getattr(monde, "hf_releve", None)
        if releve is None:
            soucis.append("aucun releve de campagne calcule")
        else:
            for cle, valeur in attendu["hfk_releve"].items():
                if releve.get(cle) != valeur:
                    soucis.append(f"releve[{cle!r}] = {releve.get(cle)!r} (attendu {valeur!r})")
    for cid, voulu in attendu.get("stalwart", []):
        f = face(cid)
        if f is not None and bool(f.IsStalwart()) != voulu:
            soucis.append(f"{cid} stalwart = {f.IsStalwart()} (attendu {voulu})")
    for cid in attendu.get("aside_absents", []):
        if cid in [getattr(f.paper, "card_id", None) for f in monde.aside_deck.GetAll()]:
            soucis.append(f"{cid} est encore dans la zone mise de cote du scenario")
    for cid, hote in attendu.get("attache", []):
        f = face(cid)
        if f is not None:
            b = f.bind_face
            got = getattr(getattr(b, "paper", None), "card_id", None) if b else None
            if got != hote:
                soucis.append(f"{cid} attache a {got} (attendu {hote})")
    for cid, nom, n in attendu.get("compteurs_sur", []):
        f = face(cid)
        if f is not None and f.GetCounters(nom) != n:
            soucis.append(f"{cid} compteurs {nom} = {f.GetCounters(nom)} (attendu {n})")
    for cid, n in attendu.get("menace_de", []):
        f = face(cid)
        if f is not None and f.threat != n:
            soucis.append(f"{cid} menace = {f.threat} (attendu {n})")
    for cid, n in attendu.get("attaque", []):
        f = face(cid)
        if f is not None and f.attack != n:
            soucis.append(f"{cid} ATK = {f.attack} (attendu {n})")
    for cid, n in attendu.get("vie", []):
        f = face(cid)
        if f is not None and f.max_health != n:
            soucis.append(f"{cid} PV max = {f.max_health} (attendu {n})")
    for cid, n in attendu.get("degats_de", []):
        f = face(cid)
        if f is not None and (f.max_health - f.health) != n:
            soucis.append(f"{cid} degats = {f.max_health - f.health} (attendu {n})")
    for cid, st, n in attendu.get("statuts_sur", []):
        f = face(cid)
        if f is not None and getattr(f, st) != n:
            soucis.append(f"{cid} statut {st} = {getattr(f, st)} (attendu {n})")
    for cid in attendu.get("absents", []):
        if par_id(monde, cid) is not None:
            soucis.append(f"{cid} est encore en jeu")
    for cid, tr, b in attendu.get("trait_de", []):
        f = face(cid)
        if f is not None and bool(f.HasTrait(tr)) != b:
            soucis.append(f"{cid} trait {tr} = {f.HasTrait(tr)} (attendu {b})")
    for cid, n in attendu.get("boosts_de", []):
        f = face(cid)
        if f is not None:
            vus = f.components.boostable.GetDeck().GetSize()
            if vus != n:
                soucis.append(f"{cid} cartes de boost = {vus} (attendu {n})")
    for cid, n in attendu.get("acceleration", []):
        f = face(cid)
        if f is not None and f.acceleration_token != n:
            soucis.append(f"{cid} jetons d'acceleration = {f.acceleration_token} (attendu {n})")
    if "partie_finie" in attendu and bool(getattr(monde, "is_game_over", False)) != attendu["partie_finie"]:
        soucis.append(f"partie finie = {getattr(monde, 'is_game_over', False)} (attendu {attendu['partie_finie']})")
    if "gagnee" in attendu:
        fini = bool(getattr(monde, "is_game_over", False))
        gagne = fini and bool(monde.game_over.players_won)
        if gagne != attendu["gagnee"]:
            soucis.append(f"partie gagnee = {gagne} (attendu {attendu['gagnee']})")
    for cid, voulu in attendu.get("nb_en_jeu", []):
        total = 0
        for objet in monde.object_manager.card_dict.values():
            f = getattr(objet, "face", None) or objet
            if getattr(getattr(f, "paper", None), "card_id", None) == cid and f.IsInPlay():
                total += 1
        if total != voulu:
            soucis.append(f"{total} exemplaire(s) de {cid} en jeu (attendu {voulu})")
    if "distribuees" in attendu:
        n = len(list(monde.players[0].dealt_encounter_cards.Get(True)))
        if n != attendu["distribuees"]:
            soucis.append(f"cartes rencontre distribuees = {n} (attendu {attendu['distribuees']})")
    if attendu.get("hors_deck_rencontre"):
        from game.operate.worlds import Worlds
        ids = {getattr(f.paper, "card_id", None) for f in Worlds.GetEncounterDeckCards(monde)}
        for cid in attendu["hors_deck_rencontre"]:
            if cid in ids:
                soucis.append(f"{cid} est dans le deck de rencontre (il devait en etre retire)")
    for ally, attaquant, voulu in attendu.get("peut_defendre", []):
        f, a = face(ally), face(attaquant)
        if f is not None and a is not None and bool(f.IsCanDefense(a)) != voulu:
            soucis.append(f"{ally} peut defendre contre {attaquant} = {f.IsCanDefense(a)} (attendu {voulu})")
    for cid, pic in attendu.get("hote_pic", []):
        f = face(cid)
        if f is not None:
            hote = f.bind_face
            vu = getattr(hote, "pic_id", None) if hote else None
            if vu != pic:
                soucis.append(f"{cid} est attache a une carte d'image {vu} (attendu {pic})")
    for cid in attendu.get("steady", []):
        f = face(cid)
        if f is not None and not f.IsSteady():
            soucis.append(f"{cid} n'est pas Steady")
    if soucis:
        return False, " ; ".join(soucis)
    return True, "etat conforme"
'''
