# Cas test_capacites du scenario 3 « BLACK QUEEN » (Selene) de la campagne Hellfire Hunt (Dipsome), prefixe `hf`, pack hellfire_hunt_black_queen (set 243),
# + le module DARKHOLD (hf361-hf366, porte par ce pack) : noms prefixes « [hf] » puis le card_id (le nom du cas contient le card_id).
# Filtre de passe : `"[hf] hf4|[hf] hf36"`.
#
# Rappels de montage (voir aussi tools/cas/hellfire_white_queen.py, dont les pieges de harnais valent ici) :
#  - `spider_man` demarre en ALTER-EGO : `Puzzle.ChangeForm('01001a')` le passe en HEROS (le vilain ATTAQUE un heros, MANIGANCE contre un alter ego) ;
#  - le scenario monte : Selene I (hf401), « Throne of the Hellfire Club » (hf404b, menace 1, cible 5), l'environnement NUIT (hf407a, 3 compteurs
#    `time` par joueur), le module Darkhold MIS DE COTE (hf362-hf366), le Darkhold Dwarf (hf361) dans le deck de rencontre ;
#  - `Puzzle.BeginVillainPhase()` ne fait pas activer le vilain : `Puzzle.Attack('hf401')` / `Puzzle.Scheme('hf401')` ;
#  - la NUIT donne 1 carte de boost de plus a Selene : le deck de rencontre de test est refait avec du remplissage inoffensif (01105 Bomb Scare) ;
#  - pour mesurer des degats, le heros est INCLINE (`Puzzle.Exhaust('01001a')`) : sinon le pilote defend ;
#  - chaque activation d'un ennemi et chaque pouvoir de base RETIRE un compteur de l'environnement : les cas qui mesurent les compteurs le disent.
SC = "hellfire_black_queen"
SCX = "hellfire_black_queen_expert"
HEROS = "Puzzle.ChangeForm('01001a')"   # spider_man demarre en ALTER-EGO
PRET_EXH = "Puzzle.Exhaust('01001a')"
LC = "Puzzle.PutIntoPlay('01076', under_control=True)"   # Luke Cage (allie, 5 PV, ATK 2)
BC = "Puzzle.PutIntoPlay('01002', under_control=True)"   # Black Cat (allie, 2 PV)
MB = "Puzzle.PutIntoPlay('01083', under_control=True)"   # Mockingbird (allie, 3 PV)
HU = "Puzzle.PutIntoPlay('01050', under_control=True)"   # Hulk (allie, 5 PV, ATK 3)


def deck(*cartes, remplissage=8):
    """Deck de rencontre de test, les cartes voulues listees DU DESSUS vers le dessous, puis du remplissage inoffensif.
    ⚠ `Puzzle.CreateEncounterDeck(a, b, c)` pose `a` en DERNIER : la derniere carte creee est le DESSUS du deck ; on inverse donc la liste."""
    ids = list(cartes) + ["01105"] * remplissage
    return ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck(%s)" % ", ".join("'%s'" % c for c in reversed(ids))]


def _c(nom, pourquoi, mise, declencher, attendu, **cle):
    cas = {"nom": "[hf] " + nom, "pourquoi": pourquoi, "scenario": cle.pop("scenario", SC),
           "heros": cle.pop("heros", "spider_man"), "mise_en_place": ["Puzzle.EmptyHand()"] + list(mise), "declencher": declencher,
           "verifier": cle.pop("verifier", "hfq_etat"), "attendu": attendu}
    cas.update(cle)
    cas.setdefault("main_exclusive", ["01090"])
    return cas


CAS = [
    # ===================================================================== mise en place (hf404a)
    _c("hf404a mise en place : Selene I, Throne of the Hellfire Club (menace 1), la NUIT en jeu avec 3 compteurs, Darkhold mis de cote sauf le Dwarf",
       "« Setup : Put Under the Moonlight environment into the play. Set the Darkhold module aside. Shuffle the set-aside Darkhold Dwarf into the encounter deck. »",
       [], [],
       {"en_jeu": ["hf401", "hf404b", "hf407a"], "absents": ["hf407b"], "vie": [["hf401", 12]], "attaque": [["hf401", 1]], "menace_de": [["hf404b", 1]],
        "compteurs_sur": [["hf407a", "time", 3]],
        "mis_de_cote": ["hf362", "hf363", "hf364", "hf365", "hf366"], "dans_deck_rencontre_nb": [["hf361", 1], ["hf362", 0], ["hf408", 1], ["hf422", 1]]}),
    _c("hf404a mise en place EXPERT : Selene II (PV 14, ATK 2, Toughness) puis la meme installation",
       "scenario expert : Selene (II) et Selene (III)", [], [],
       {"en_jeu": ["hf402", "hf404b", "hf407a"], "vie": [["hf402", 14]], "attaque": [["hf402", 2]], "statuts": [["hf402", "Tough"]],
        "mis_de_cote": ["hf362"]}, scenario=SCX),
    # ===================================================================== Selene : vol de vie (hf401)
    _c("hf401 Reponse forcee : Selene (3 degats) attaque le heros incline (1 degat non excedentaire) -> elle se soigne de 1 (3 -> 2)",
       "« After Selene attacks, heal damage from her equal to the amount of non-excess damage characters the defending player controlled took from this attack »",
       [HEROS, PRET_EXH, "Puzzle.Damage('hf401', 3)"] + deck("01105"), ["Puzzle.Attack('hf401')"],
       {"degats_de": [["hf401", 2]], "degats_identite": 1}),
    _c("hf401 Reponse forcee : TEMOIN, le heros DEFEND (0 degat) -> Selene ne se soigne pas",
       "contre-cas : aucun degat subi, aucun soin", [HEROS, "Puzzle.Damage('hf401', 3)"] + deck("01105"), ["Puzzle.Attack('hf401')"],
       {"degats_de": [["hf401", 3]], "degats_identite": 0}),

    # ===================================================================== l'environnement jour / nuit (hf407a / hf407b)
    _c("hf407a entre en jeu avec 3 compteurs time PAR JOUEUR : deux joueurs -> 6",
       "« Under the Moonlight enters play with 3[per_hero] time counters »", [], [],
       {"compteurs_sur": [["hf407a", "time", 6]]}, heros2="black_widow"),
    _c("hf407a Reponse forcee : un ennemi s'active (Selene attaque) -> 1 compteur retire (3 -> 2)",
       "« After ... an enemy activates, remove 1 time counter here »",
       [HEROS, PRET_EXH] + deck("01105"), ["Puzzle.Activate('hf401')"],
       {"compteurs_sur": [["hf407a", "time", 2]], "en_jeu": ["hf407a"]}),
    _c("hf407a Reponse forcee : un personnage ami utilise un pouvoir de base (le heros attaque) -> 1 compteur retire (3 -> 2)",
       "« After a character uses a basic power ... remove 1 time counter here »",
       [HEROS] + deck("01105"), ["Puzzle.Attack('01001a')"],
       {"compteurs_sur": [["hf407a", "time", 2]]}, cibles=["hf401"], accepter_choix=True),
    _c("hf407a Reponse forcee : le heros THWART la manigance -> 1 compteur retire",
       "meme Reponse, pouvoir de base = thwart", [HEROS, "Puzzle.PlaceThreat('hf404b', 2)"] + deck("01105"), ["Puzzle.Thwart('01001a')"],
       {"compteurs_sur": [["hf407a", "time", 2]]}, cibles=["hf404b"], accepter_choix=True),
    _c("hf407a Reponse forcee : l'alter-ego RECUPERE (pouvoir de base REC) -> 1 compteur retire",
       "meme Reponse, pouvoir de base = recover", ["Puzzle.Damage('01001b', 3)"] + deck("01105"), ["Puzzle.Recover('01001b')"],
       {"compteurs_sur": [["hf407a", "time", 2]]}),
    _c("hf407a Reponse forcee : le heros DEFEND contre Selene -> 2 compteurs retires (la defense + l'activation de Selene : 3 -> 1)",
       "la defense est un pouvoir de base ; l'activation de l'ennemi en est un autre : les deux moities de la phrase",
       [HEROS] + deck("01105"), ["Puzzle.Activate('hf401')"],
       {"compteurs_sur": [["hf407a", "time", 1]]}),
    _c("hf407a Reponse forcee : TEMOIN, rien ne se passe -> 3 compteurs",
       "contre-cas : sans pouvoir de base ni activation, aucun compteur ne bouge", [HEROS] + deck("01105"), [],
       {"compteurs_sur": [["hf407a", "time", 3]]}),
    _c("hf407a sans compteur : l'environnement se RETOURNE (Beneath the Sun, hf407b) et entre en jeu avec 3 compteurs",
       "« If there are no time counters here, flip this card » + « Beneath the Sun enters play with 3[per_hero] time counters »",
       [HEROS, PRET_EXH, "Puzzle.Counter('hf407a', 'time', -2)"] + deck("01105"),
       ["Puzzle.Activate('hf401')"],
       {"en_jeu": ["hf407b"], "absents": ["hf407a"], "compteurs_sur": [["hf407b", "time", 3]]}),
    _c("hf407b sans compteur : il se retourne sur la NUIT (hf407a) avec 3 compteurs",
       "l'alternance fonctionne dans les DEUX sens", [HEROS, PRET_EXH, "Puzzle.Flip('hf407a')", "Puzzle.Counter('hf407b', 'time', -2)"] + deck("01105"),
       ["Puzzle.Activate('hf401')"],
       {"en_jeu": ["hf407a"], "absents": ["hf407b"], "compteurs_sur": [["hf407a", "time", 3]]}),
    _c("hf407a Interruption forcee : la NUIT donne 1 carte de boost de plus a Selene (2 cartes de 2 icones : 1 + 4 = 5 degats)",
       "« When Black Queen would activate, give her 1 more boost card » : Little Demon (2 icones) x2 en boost",
       [HEROS, PRET_EXH] + deck("hf409", "hf409"), ["Puzzle.Activate('hf401')"],
       {"degats_identite": 5}),
    _c("hf407b TEMOIN : le JOUR ne donne PAS de carte de boost de plus (1 carte de 2 icones : 1 + 2 = 3 degats)",
       "contre-cas de la nuit : la face jour n'a pas l'Interruption", [HEROS, PRET_EXH, "Puzzle.Flip('hf407a')"] + deck("hf409", "hf409"),
       ["Puzzle.Activate('hf401')"], {"degats_identite": 3}),
    _c("hf407b le JOUR : chaque identite a +1 a chaque pouvoir de base (l'attaque du heros passe de 2 a 3)",
       "« Each identity gets +1 to each of its basic powers »", [HEROS, "Puzzle.Flip('hf407a')"] + deck("01105"), ["Puzzle.Attack('01001a')"],
       {"degats_de": [["hf401", 3]]}, cibles=["hf401"], accepter_choix=True),
    _c("hf407a TEMOIN : la nuit, l'attaque du heros reste a 2",
       "contre-cas : sans le jour, 2 degats", [HEROS] + deck("01105"), ["Puzzle.Attack('01001a')"],
       {"degats_de": [["hf401", 2]]}, cibles=["hf401"], accepter_choix=True),
    _c("hf407b le JOUR : le THW du heros passe de 1 a 2",
       "+1 a CHAQUE pouvoir de base : la contre-manigance retire 2 menaces au lieu de 1",
       [HEROS, "Puzzle.Flip('hf407a')", "Puzzle.PlaceThreat('hf404b', 3)"] + deck("01105"), ["Puzzle.Thwart('01001a')"],
       {"menace_de": [["hf404b", 2]]}, cibles=["hf404b"], accepter_choix=True),
    _c("hf407b le JOUR : la RECUPERATION de l'alter-ego gagne +1 (3 -> 4)",
       "REC est un pouvoir de base de l'identite", ["Puzzle.Flip('hf407a')", "Puzzle.Damage('01001b', 5)"] + deck("01105"), ["Puzzle.Recover('01001b')"],
       {"degats_identite": 1}),

    # ===================================================================== les complots
    _c("hf404b Interruption forcee : le Darkhold Dwarf est vaincu (va a la defausse) -> avance au stade 2 ; hf405a melange le module Darkhold au deck",
       "« When Darkhold Dwarf enters the discard pile, advance to stage 2A » + 2A « Shuffle the set-aside Darkhold modular set into the encounter deck »",
       ["Puzzle.PutIntoPlay('hf361')"], ["Puzzle.Damage('hf361', 3)"],
       {"en_jeu": ["hf405b"], "absents": ["hf404b"], "pas_mis_de_cote": ["hf362", "hf363", "hf364", "hf365", "hf366"],
        "dans_deck_rencontre_nb": [["hf362", 1], ["hf363", 1], ["hf364", 1], ["hf365", 1], ["hf366", 1]]}),
    _c("hf404b Interruption forcee : TEMOIN, un AUTRE sbire defausse (Little Demon) -> le stade 1 reste",
       "contre-cas : seul le Darkhold Dwarf fait avancer le complot", ["Puzzle.PutIntoPlay('hf409')"], ["Puzzle.Damage('hf409', 3)"],
       {"en_jeu": ["hf404b"], "absents": ["hf405b"], "mis_de_cote": ["hf362"]}),
    _c("hf404b When Completed (la NUIT) : Selene recoit une carte Tough ; les compteurs de la nuit ne bougent pas",
       "« Give Selene a tough status card. If Beneath the Sun environment is in play, remove 2[per_hero] time counters from it » : la nuit est visible",
       deck("01105"), ["Puzzle.PlaceThreat('hf404b', 4)"],
       {"en_jeu": ["hf405b"], "statuts": [["hf401", "Tough"]], "compteurs_sur": [["hf407a", "time", 3]]}),
    _c("hf404b When Completed (le JOUR) : Selene recoit une carte Tough ET le jour perd 2 compteurs par joueur (3 -> 1)",
       "la branche « If Beneath the Sun environment is in play »", ["Puzzle.Flip('hf407a')"] + deck("01105"), ["Puzzle.PlaceThreat('hf404b', 4)"],
       {"en_jeu": ["hf405b", "hf407b"], "statuts": [["hf401", "Tough"]], "compteurs_sur": [["hf407b", "time", 1]]}),
    _c("hf405b When Completed : Selene recoit une carte Tough et le Darkhold est cherche puis ATTACHE a Selene",
       "« Give Selene a tough status card. Find Darkhold and attach it to Selene » ; le complot passe au stade 3 (hf406a revele)",
       ["Puzzle.AdvanceMainScheme()", "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01105', '01105', 'hf408', 'hf422', 'hf362')"],
       ["Puzzle.PlaceThreat('hf405b', 5)"],
       {"en_jeu": ["hf406b", "hf362"], "absents": ["hf405b"], "attache": [["hf362", "hf401"]], "statuts": [["hf401", "Tough"]]}),
    _c("hf406a When Revealed : Immortal Moon Goddess est cherchee et revelee, Blackheart mis en jeu engage avec le premier joueur",
       "« Find the Immortal Moon Goddess side scheme and reveal it. Find Blackheart and put it into play engaged with the first player. (Shuffle.) »",
       ["Puzzle.AdvanceMainScheme()", "Puzzle.AdvanceMainScheme()", "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01105', '01105', 'hf408', 'hf422')"], [],
       {"en_jeu": ["hf406b", "hf422", "hf408"], "vie": [["hf408", 9]], "attaque": [["hf408", 3]], "steady": ["hf408"]}),
    _c("hf406b Reponse forcee : apres l'etape 1 de la phase du mechant, 1 menace par compteur time (3) + l'escalade imprimee (2) + la manigance de Selene a l'etape 3 (2) = 7",
       "« After step one of the villain phase, place 1 threat here for each time counter on Under the Moonlight or Beneath the Sun » ; le deck ne contient ni Goddess ni Blackheart (pas d'icone d'acceleration) ; Selene (stun sans effet ici) complote encore : +2 a l'etape 3, que le cas compte",
       deck("01105") + ["Puzzle.AdvanceMainScheme()", "Puzzle.AdvanceMainScheme()", "Puzzle.Stun('hf401')"], ["Puzzle.RunVillainPhase()"],
       {"menace_de": [["hf406b", 7]]}),
    _c("hf406b Reponse forcee : le JOUR visible avec 1 compteur -> 1 + escalade 2 + manigance 2 = 5 menaces",
       "la regle lit l'environnement visible quel qu'il soit",
       deck("01105") + ["Puzzle.AdvanceMainScheme()", "Puzzle.AdvanceMainScheme()", "Puzzle.Stun('hf401')", "Puzzle.Flip('hf407a')", "Puzzle.Counter('hf407b', 'time', -2)"],
       ["Puzzle.RunVillainPhase()"], {"menace_de": [["hf406b", 5]]}),
    _c("hf403 stade III (expert) : PV 17, ATK 3, Steady + Toughness (carte Tough)",
       "nombres texte <-> code (scan) : Selene (III) ; l'expert part de Selene (II) et avance a (III)", ["Puzzle.AdvanceVillain()"] + deck("01105"), [],
       {"en_jeu": ["hf403"], "absents": ["hf402"], "vie": [["hf403", 17]], "attaque": [["hf403", 3]], "steady": ["hf403"], "statuts": [["hf403", "Tough"]]}, scenario=SCX),
    _c("hf401 Reponse forcee : l'EXCES n'est pas soigne (Black Cat 2 PV defend, subit 5 : 2 non excedentaires -> Selene 4 -> 2 degats)",
       "« non-excess damage characters the defending player controlled took » : 1 ATK + 2 cartes de boost de 2 icones = 5 degats sur une alliee a 2 PV",
       [HEROS, PRET_EXH, BC, "Puzzle.Damage('hf401', 4)"] + deck("hf409", "hf409"), ["Puzzle.Attack('hf401', defender='01002')"],
       {"absents": ["01002"], "degats_de": [["hf401", 2]], "degats_identite": 0}),
    _c("hf401 Reponse forcee : TEMOIN, sa manigance (alter-ego) ne la soigne pas",
       "la Reponse n'existe qu'apres une ATTAQUE", ["Puzzle.Damage('hf401', 3)"] + deck("01105"), ["Puzzle.Scheme('hf401')"],
       {"degats_de": [["hf401", 3]], "menace_de": [["hf404b", 3]]}),
    # ===================================================================== hf408 Blackheart
    _c("hf408 Boost : l'attaque de Selene gagne PERCANT : la carte Tough du heros est defaussee ET les 4 degats passent (1 + 3 icones)",
       "« If this activation is an attack, this attack gains overkill, piercing, and ranged »",
       [HEROS, PRET_EXH, "Puzzle.Tough('01001a')"] + deck("hf408"), ["Puzzle.Attack('hf401')"],
       {"degats_identite": 4, "statuts_absents": [["01001a", "Tough"]]}),
    _c("hf408 Boost : TEMOIN, une carte de boost sans effet (Little Demon, 2 icones) : la carte Tough absorbe TOUTE l'attaque (0 degat)",
       "contre-cas du percant", [HEROS, PRET_EXH, "Puzzle.Tough('01001a')"] + deck("hf409"), ["Puzzle.Attack('hf401')"],
       {"degats_identite": 0, "statuts_absents": [["01001a", "Tough"]]}),
    _c("hf408 Boost : l'attaque gagne OVERKILL : l'allie Black Cat (2 PV) defend, 4 degats -> l'exces (2) passe au heros",
       "overkill : l'exces de degats est inflige a l'identite", [HEROS, PRET_EXH, BC] + deck("hf408"), ["Puzzle.Attack('hf401', defender='01002')"],
       {"absents": ["01002"], "degats_identite": 2}),
    _c("hf408 Boost : TEMOIN, sans overkill (Little Demon, 3 degats) : l'exces (1) est perdu, le heros ne subit rien",
       "contre-cas de l'overkill", [HEROS, PRET_EXH, BC] + deck("hf409"), ["Puzzle.Attack('hf401', defender='01002')"],
       {"absents": ["01002"], "degats_identite": 0}),
    _c("hf408 Blackheart en jeu : Guard (desc) : le heros ne peut pas attaquer Selene tant qu'il est la",
       "Guard + Patrol + Steady lus dans `desc` ; le sbire s'engage avec le joueur", [HEROS, "Puzzle.PutIntoPlay('hf408')"] + deck("01105"), ["Puzzle.Attack('01001a')"],
       {"vie": [["hf408", 9]], "attaque": [["hf408", 3]], "steady": ["hf408"], "degats_de": [["hf401", 0]]}, cibles=["hf401"], accepter_choix=True),
    # ===================================================================== hf409-hf412 Little Demon
    _c("hf409 Reponse forcee : Little Demon attaque le heros incline (2 degats) -> le heros est desoriente",
       "« After Little Demon attacks and damages you, you are confused »", [HEROS, PRET_EXH, "Puzzle.PutIntoPlay('hf409')"] + deck("01105"), ["Puzzle.Attack('hf409')"],
       {"degats_identite": 2, "statuts": [["01001a", "Confused"]], "vie": [["hf409", 3]], "attaque": [["hf409", 2]]}),
    _c("hf409 Reponse forcee : TEMOIN, l'allie (Luke Cage) DEFEND : les degats vont a l'allie, le heros n'est PAS desoriente",
       "« damages YOU » : un allie qui encaisse ne desoriente pas l'identite", [HEROS, PRET_EXH, LC, "Puzzle.PutIntoPlay('hf409')"] + deck("01105"),
       ["Puzzle.Attack('hf409', defender='01076')"], {"statuts_absents": [["01001a", "Confused"]], "degats_identite": 0}),
    _c("hf409 Teamwork (DEMON, natif) : un 2e Little Demon entre en jeu -> il s'active tout de suite (2 degats au heros incline, desoriente)",
       "`desc.Teamwork` : « After a minion with Teamwork enters play, if another DEMON minion is in play, it activates » (regles v16/v18 du lanceur)",
       [HEROS, PRET_EXH, "Puzzle.PutIntoPlay('hf409')"] + deck("01105"), ["Puzzle.PutIntoPlay('hf410')"],
       {"degats_identite": 2, "statuts": [["01001a", "Confused"]], "en_jeu": ["hf409", "hf410"]}, regles=["v16_all", "v18_all"]),
    _c("hf409 Patrol (natif) : tant que Little Demon est la, le heros ne peut pas attaquer Selene sans Guard... TEMOIN de Patrol : Selene reste attaquable",
       "Patrol n'empeche rien cote joueur (il s'applique aux ennemis qui complotent) : l'attaque du heros touche Selene (2 degats)",
       [HEROS, "Puzzle.PutIntoPlay('hf409')"] + deck("01105"), ["Puzzle.Attack('01001a')"],
       {"degats_de": [["hf401", 2]]}, cibles=["hf401"], accepter_choix=True),
    _c("hf410 Little Demon (illustration 2) : meme Reponse forcee (desoriente apres avoir attaque et blesse)",
       "les quatre exemplaires portent le meme texte", [HEROS, PRET_EXH, "Puzzle.PutIntoPlay('hf410')"] + deck("01105"), ["Puzzle.Attack('hf410')"],
       {"degats_identite": 2, "statuts": [["01001a", "Confused"]]}),
    _c("hf411 Little Demon (illustration 3) : meme Reponse forcee (desoriente apres avoir attaque et blesse)",
       "les quatre exemplaires portent le meme texte", [HEROS, PRET_EXH, "Puzzle.PutIntoPlay('hf411')"] + deck("01105"), ["Puzzle.Attack('hf411')"],
       {"degats_identite": 2, "statuts": [["01001a", "Confused"]]}),
    _c("hf412 Little Demon (illustration 4) : meme Reponse forcee (desoriente apres avoir attaque et blesse)",
       "les quatre exemplaires portent le meme texte", [HEROS, PRET_EXH, "Puzzle.PutIntoPlay('hf412')"] + deck("01105"), ["Puzzle.Attack('hf412')"],
       {"degats_identite": 2, "statuts": [["01001a", "Confused"]]}),

    # ===================================================================== hf413-hf415 Hyponotic Trance
    _c("hf413 revelee : s'attache a l'allie qui a le plus de PV RESTANTS (Mockingbird 3 PV intacts, pas Hulk 5 PV a 4 degats) ; THW -1",
       "« Attach to the ally with the highest remaining hit-point without Hyponotic Trance attached » ; -1 THW imprime (Hulk 5 PV a 4 degats : 1 restant ; Luke Cage aurait la carte Tough et ne se prete pas a la mesure)",
       [HEROS, HU, MB, "Puzzle.Damage('01050', 4)"] + deck("hf413"), ["Puzzle.Reveal('hf413')"],
       {"attache": [["hf413", "01083"]], "prop_de": [["01083", "thwart", 0]]}),
    _c("hf414 revelee apres hf413 : l'allie qui a deja une Trance est exclu, la 2e va a l'AUTRE allie (Hulk)",
       "« ... without Hyponotic Trance attached »", [HEROS, HU, MB, "Puzzle.Damage('01050', 4)"] + deck("hf413", "hf414"), ["Puzzle.Reveal('hf413')", "Puzzle.Reveal('hf414')"],
       {"attache": [["hf413", "01083"], ["hf414", "01050"]]}),
    _c("hf415 revelee quand le seul allie porte deja une Trance : « Otherwise, this card gains surge » (la carte suivante, Little Demon, est revelee)",
       "pas d'hote legal -> surge", [HEROS, MB] + deck("hf413", "hf415", "hf409"), ["Puzzle.Reveal('hf413')", "Puzzle.Reveal('hf415')"],
       {"attache": [["hf413", "01083"]], "en_jeu": ["hf409"], "absents": ["hf415"]}),
    _c("hf413 revelee sans aucun allie : elle gagne surge (la carte suivante est revelee)",
       "« Otherwise, this card gains surge »", [HEROS] + deck("hf413", "hf409"), ["Puzzle.Reveal('hf413')"],
       {"en_jeu": ["hf409"], "absents": ["hf413"]}),
    _c("hf413 : l'allie hypnotise ne peut PAS attaquer Selene (Luke Cage ATK 2 : 0 degat)",
       "« Attached character cannot attack Selene »", [HEROS, LC] + deck("hf413"), ["Puzzle.Reveal('hf413')", "Puzzle.Attack('01076')"],
       {"degats_de": [["hf401", 0]]}, cibles=["hf401"], accepter_choix=True),
    _c("hf413 TEMOIN : sans Trance, Luke Cage attaque Selene (2 degats)",
       "contre-cas de la ligne du dessus", [HEROS, LC] + deck("01105"), ["Puzzle.Attack('01076')"],
       {"degats_de": [["hf401", 2]]}, cibles=["hf401"], accepter_choix=True),
    _c("hf413 : l'allie hypnotise ne peut PAS defendre contre Selene, mais defend contre un autre ennemi (Little Demon)",
       "« cannot defend against Selene's attacks » seulement", [HEROS, LC, "Puzzle.PutIntoPlay('hf409')"] + deck("hf413"), ["Puzzle.Reveal('hf413')"],
       {"peut_defendre": [["01076", "hf401", False], ["01076", "hf409", True]]}),
    _c("hf413 Action de heros : le JOUR visible, depenser [mental][mental] (Genius) et retirer 1 compteur du jour -> la Trance est defaussee (compteurs 3 -> 2)",
       "« Hero Action : Spend [mental][mental] resources and remove 1 time counter from Beneath the Sun -> discard this card » (cout = les deux)",
       [HEROS, LC, "Puzzle.Flip('hf407a')"] + deck("hf413"), ["Puzzle.Reveal('hf413')", "Puzzle.Action('hf413', 'HeroAction')"],
       {"absents": ["hf413"], "compteurs_sur": [["hf407b", "time", 2]]}, main_exclusive=["01089"], payer_avec=["01089"], payer_tout=True, accepter_choix=True),
    _c("hf413 Action de heros : TEMOIN, la NUIT (pas de jour a entamer) -> l'action n'est pas payable, la Trance reste",
       "le cout « remove 1 time counter from Beneath the Sun » exige le JOUR", [HEROS, LC] + deck("hf413"), ["Puzzle.Reveal('hf413')"],
       {"en_jeu": ["hf413"], "compteurs_sur": [["hf407a", "time", 3]]}, main_exclusive=["01089"]),
    # ===================================================================== hf416-hf417 Shining Shield
    _c("hf416 revele : s'attache a Selene",
       "« Attach to Selene »", deck("hf416"), ["Puzzle.Reveal('hf416')"], {"attache": [["hf416", "hf401"]]}),
    _c("hf416 : Selene ne peut pas subir plus de 2 degats d'UNE attaque (le JOUR, le heros attaque avec 3 -> 2 degats)",
       "« Selene cannot take more than 2 damage from a single attack »", [HEROS, "Puzzle.Flip('hf407a')"] + deck("hf416"), ["Puzzle.Reveal('hf416')", "Puzzle.Attack('01001a')"],
       {"degats_de": [["hf401", 2]]}, cibles=["hf401"], accepter_choix=True),
    _c("hf416 TEMOIN : sans Shining Shield, le heros fait ses 3 degats le jour",
       "contre-cas du plafond", [HEROS, "Puzzle.Flip('hf407a')"] + deck("01105"), ["Puzzle.Attack('01001a')"], {"degats_de": [["hf401", 3]]}, cibles=["hf401"], accepter_choix=True),
    _c("hf416 Action de heros : le JOUR visible, depenser [energy] (Energy) et retirer 1 compteur du jour -> le bouclier est defausse (compteurs 3 -> 2)",
       "« Hero Action : Spend a [energy] resource and remove 1 time counter from Beneath the Sun -> discard this card »",
       [HEROS, "Puzzle.Flip('hf407a')"] + deck("hf416"), ["Puzzle.Reveal('hf416')", "Puzzle.Action('hf416', 'HeroAction')"],
       {"absents": ["hf416"], "compteurs_sur": [["hf407b", "time", 2]]}, main_exclusive=["01088"], payer_avec=["01088"], payer_tout=True, accepter_choix=True),
    _c("hf417 Boost : Selene active avec Shining Shield en boost -> la carte s'attache a Selene",
       "« [star] Boost : Attach this card to Selene »", [HEROS, PRET_EXH] + deck("hf417", "01105"), ["Puzzle.Attack('hf401')"],
       {"attache": [["hf417", "hf401"]]}),
    # ===================================================================== hf418 Relentless Pursuit
    _c("hf418 revelee : s'attache a l'identite ; Selene qui allait MANIGANCER ATTAQUE a la place (1 degat a l'alter-ego, menace inchangee a 1)",
       "« When Selene would scheme against you, she attacks you instead »", deck("hf418"), ["Puzzle.Reveal('hf418')", "Puzzle.Scheme('hf401')"],
       {"attache": [["hf418", "01001b"]], "menace_de": [["hf404b", 1]], "degats_identite": 1}),
    _c("hf418 TEMOIN : sans Pursuit, Selene manigance (+2 menace : 1 -> 3)",
       "contre-cas", deck("01105"), ["Puzzle.Scheme('hf401')"], {"menace_de": [["hf404b", 3]], "degats_identite": 0}),
    _c("hf418 Action de heros : le JOUR visible, depenser [physical] (Strength) et retirer 1 compteur du jour -> la carte est defaussee",
       "« Hero Action : Spend a [physical] resource and remove 1 time counter from Beneath the Sun -> discard this card »",
       [HEROS, "Puzzle.Flip('hf407a')"] + deck("hf418"), ["Puzzle.Reveal('hf418')", "Puzzle.Action('hf418', 'HeroAction')"],
       {"absents": ["hf418"], "compteurs_sur": [["hf407b", "time", 2]]}, main_exclusive=["01090"], payer_avec=["01090"], payer_tout=True, accepter_choix=True),
    # ===================================================================== hf419 Dark Temptation
    _c("hf419 revelee : Selene attaque le joueur (heros incline : 1 degat)",
       "« When Revealed : Selene attacks you »", [HEROS, PRET_EXH] + deck("hf419"), ["Puzzle.Reveal('hf419')"], {"degats_identite": 1}),
    _c("hf419 Boost : l'attaque DEFAIT une alliee (Black Cat 2 PV, 1 ATK + 1 icone = 2) -> 2 menaces sur le complot (1 -> 3)",
       "« [star] Boost : If this attack defeats an ally, place 2 threat on the main scheme »", [HEROS, PRET_EXH, BC] + deck("hf419"),
       ["Puzzle.Attack('hf401', defender='01002')"], {"absents": ["01002"], "menace_de": [["hf404b", 3]]}),
    _c("hf419 Boost : TEMOIN, l'alliee (Mockingbird 3 PV) survit -> pas de menace (reste 1)",
       "contre-cas", [HEROS, PRET_EXH, MB] + deck("hf419"), ["Puzzle.Attack('hf401', defender='01083')"], {"en_jeu": ["01083"], "menace_de": [["hf404b", 1]]}),
    # ===================================================================== hf420 Lunar Eclipse
    _c("hf420 revelee (JOUR) : retire 1 compteur du jour (3 -> 2)",
       "« Remove 1[per_hero] time counter from Beneath the Sun »", ["Puzzle.Flip('hf407a')"] + deck("hf420"), ["Puzzle.Reveal('hf420')"],
       {"compteurs_sur": [["hf407b", "time", 2]]}),
    _c("hf420 revelee (JOUR, 1 compteur) : le dernier est retire -> l'environnement se retourne sur la NUIT (3 compteurs)",
       "retrait du dernier compteur -> « flip this card »", ["Puzzle.Flip('hf407a')", "Puzzle.Counter('hf407b', 'time', -2)"] + deck("hf420"), ["Puzzle.Reveal('hf420')"],
       {"en_jeu": ["hf407a"], "absents": ["hf407b"], "compteurs_sur": [["hf407a", "time", 3]]}),
    _c("hf420 revelee (NUIT) : « If you cannot, place 1[per_hero] time counter on Under the Moonlight » (3 -> 4)",
       "pas de jour a entamer", deck("hf420"), ["Puzzle.Reveal('hf420')"], {"compteurs_sur": [["hf407a", "time", 4]]}),
    _c("hf420 Boost : Selene active avec Lunar Eclipse en boost -> la carte est REVELEE (+1 compteur la nuit, -1 pour l'activation : 3 -> 3)",
       "« [star] Boost : Reveal this card »", [HEROS, PRET_EXH] + deck("hf420"), ["Puzzle.Activate('hf401')"], {"compteurs_sur": [["hf407a", "time", 3]]}),
    _c("hf420 Boost : TEMOIN, meme activation avec une carte sans effet -> 3 -> 2",
       "contre-cas de la ligne du dessus", [HEROS, PRET_EXH] + deck("01105"), ["Puzzle.Activate('hf401')"], {"compteurs_sur": [["hf407a", "time", 2]]}),
    # ===================================================================== hf421 Eternal Night
    _c("hf421 revelee quand le JOUR est visible : « Flip Beneath the Sun » -> la NUIT revient avec 3 compteurs",
       "When Revealed : Flip Beneath the Sun", ["Puzzle.Flip('hf407a')", "Puzzle.Counter('hf407b', 'time', -2)"] + deck("hf421"), ["Puzzle.Reveal('hf421')"],
       {"en_jeu": ["hf407a", "hf421"], "absents": ["hf407b"], "compteurs_sur": [["hf407a", "time", 3]]}),
    _c("hf421 revelee quand c'est deja la NUIT : rien ne se retourne (3 compteurs)",
       "contre-cas", deck("hf421"), ["Puzzle.Reveal('hf421')"], {"en_jeu": ["hf407a", "hf421"], "compteurs_sur": [["hf407a", "time", 3]]}),
    _c("hf421 : les compteurs de la NUIT ne peuvent pas etre retires (Selene s'active : 3 -> 3)",
       "« Time counter on Under the Moonlight environment could not be removed »", [HEROS, PRET_EXH] + deck("hf421", "01105"),
       ["Puzzle.Reveal('hf421')", "Puzzle.Activate('hf401')"], {"compteurs_sur": [["hf407a", "time", 3]]}),
    _c("hf421 TEMOIN : meme manigance en jeu, mais le JOUR est visible -> ses compteurs se retirent normalement (3 -> 2)",
       "Eternal Night ne protege que la nuit", [HEROS, PRET_EXH] + deck("hf421", "01105"),
       ["Puzzle.Reveal('hf421')", "Puzzle.Flip('hf407a')", "Puzzle.Activate('hf401')"], {"compteurs_sur": [["hf407b", "time", 2]]}),
    # ===================================================================== hf422 Immortal Moon Goddess
    _c("hf422 revelee : menace 7 + Hinder 2 par joueur = 9 ; Victory 1 (desc)",
       "nombres texte <-> code (scan)", deck("hf422"), ["Puzzle.Reveal('hf422')"], {"menace_de": [["hf422", 9]], "en_jeu": ["hf422"]}),
    _c("hf422 : la NUIT, Selene a 12 degats (mortels) mais n'est PAS vaincue (elle reste le stade I)",
       "« While Under the Moonlight is in play, Black Queen cannot be defeated »", deck("hf422"), ["Puzzle.Reveal('hf422')", "Puzzle.Damage('hf401', 12)"],
       {"en_jeu": ["hf401"], "absents": ["hf402"]}),
    _c("hf422 : le JOUR venu (retournement), Selene a 12 degats est vaincue -> le stade II prend sa place",
       "la protection tombe avec la nuit : la defaite differee est relancee", deck("hf422"),
       ["Puzzle.Reveal('hf422')", "Puzzle.Damage('hf401', 12)", "Puzzle.Flip('hf407a')"], {"en_jeu": ["hf402"], "absents": ["hf401"]}),
    _c("hf422 : la manigance quitte le jeu -> Selene (a 12 degats) est vaincue aussi",
       "la protection tombe avec la carte : la defaite differee est relancee", deck("hf422"),
       ["Puzzle.Reveal('hf422')", "Puzzle.Damage('hf401', 12)", "Puzzle.Discard('hf422')"], {"en_jeu": ["hf402"], "absents": ["hf401"]}),
    _c("hf422 TEMOIN : sans la manigance, 12 degats vainquent Selene I (stade II)",
       "contre-cas", deck("01105"), ["Puzzle.Damage('hf401', 12)"], {"en_jeu": ["hf402"], "absents": ["hf401"]}),
    # ===================================================================== MODULE DARKHOLD
    _c("hf362 Darkhold revele : s'attache au vilain, +1 ATK (Selene 2), 2 compteurs darkspell",
       "« Attach to the villain. Uses (2 Darkspell counters) » ; +1 ATK imprime", deck("hf362"), ["Puzzle.Reveal('hf362')"],
       {"attache": [["hf362", "hf401"]], "attaque": [["hf401", 2]], "compteurs_sur": [["hf362", "darkspell", 2]]}),
    _c("hf362 Interruption forcee : Selene ATTAQUE -> -1 compteur darkspell et 1 carte de boost de plus (nuit + Darkhold = 3 cartes de 2 icones : 2 + 6 = 8 degats)",
       "« When the villain attacks, remove 1 Darkspell counter from here -> give the attached character 1 additional boost card »",
       [HEROS, PRET_EXH] + deck("hf362", "hf409", "hf409", "hf409"), ["Puzzle.Reveal('hf362')", "Puzzle.Attack('hf401')"],
       {"degats_identite": 8, "compteurs_sur": [["hf362", "darkspell", 1]]}),
    _c("hf362 Uses : le DERNIER compteur retire fait quitter le Darkhold",
       "mot-cle Uses natif : la carte part avec son dernier pion, donc sans son +1 ATK (1 + 3 cartes de 2 icones = 7 degats)", [HEROS, PRET_EXH] + deck("hf362", "hf409", "hf409", "hf409"), ["Puzzle.Reveal('hf362')", "Puzzle.Counter('hf362', 'darkspell', -1)", "Puzzle.Attack('hf401')"],
       {"absents": ["hf362"], "degats_identite": 7}),
    _c("hf362 TEMOIN : une MANIGANCE de Selene ne consomme pas de compteur",
       "« When the villain attacks » seulement", deck("hf362", "01105"), ["Puzzle.Reveal('hf362')", "Puzzle.Scheme('hf401')"],
       {"compteurs_sur": [["hf362", "darkspell", 2]], "en_jeu": ["hf362"]}),
    _c("hf363 Eternal Manipulation, Darkhold sur le vilain : s'attache a l'allie qui a le plus de PV restants (Mockingbird), -1 darkspell ; l'allie devient un sbire (SCH = son THW imprime 1, ATK +1)",
       "« attach this to your ally with highest hit-point, remove 1 darkspell counter from Darkhold »",
       [HU, MB, "Puzzle.Damage('01050', 4)"] + deck("hf362", "hf363"), ["Puzzle.Reveal('hf362')", "Puzzle.Reveal('hf363')"],
       {"hote_pic": [["hf363", "01083"]], "compteurs_sur": [["hf362", "darkspell", 1]], "hote_sbire": [["hf363", 1, 2]]}),
    _c("hf363 Eternal Manipulation, SANS Darkhold sur le vilain : le Darkhold est cherche et revele (il s'attache a Selene), l'allie n'est pas touche",
       "« Otherwise, find Darkhold attachment and reveal it »", [MB] + deck("hf363", "hf362"), ["Puzzle.Reveal('hf363')"],
       {"attache": [["hf362", "hf401"]], "compteurs_sur": [["hf362", "darkspell", 2]], "absents": ["hf363"]}),
    _c("hf364 Hellfire Conjuration, Darkhold sur le vilain : 3 degats indirects au joueur (heros seul : 3) et -1 darkspell",
       "« take 3 indirect damages, remove 1 darkspell counter from Darkhold »", [HEROS] + deck("hf362", "hf364"), ["Puzzle.Reveal('hf362')", "Puzzle.Reveal('hf364')"],
       {"degats_identite": 3, "compteurs_sur": [["hf362", "darkspell", 1]]}),
    _c("hf364 Hellfire Conjuration, SANS Darkhold : il est cherche et revele (aucun degat)",
       "« Otherwise, find Darkhold attachment and reveal it »", [HEROS] + deck("hf364", "hf362"), ["Puzzle.Reveal('hf364')"],
       {"attache": [["hf362", "hf401"]], "degats_identite": 0, "compteurs_sur": [["hf362", "darkspell", 2]]}),
    _c("hf364 Hellfire Conjuration : le Darkhold est cherche aussi dans la DEFAUSSE de rencontre",
       "« find » : deck, defausse, zone mise de cote", [HEROS] + deck("hf364") + ["Puzzle.CreateEncounterDiscardPile('hf362')"], ["Puzzle.Reveal('hf364')"],
       {"attache": [["hf362", "hf401"]], "degats_identite": 0}),
    _c("hf365 Soul Siphon, Darkhold sur le vilain : le joueur est etourdi ET desoriente, -1 darkspell",
       "« you are stunned and confused, remove 1 darkspell counter from Darkhold »", [HEROS] + deck("hf362", "hf365"), ["Puzzle.Reveal('hf362')", "Puzzle.Reveal('hf365')"],
       {"statuts": [["01001a", "Stunned"], ["01001a", "Confused"]], "compteurs_sur": [["hf362", "darkspell", 1]]}),
    _c("hf365 Soul Siphon, SANS Darkhold : il est cherche et revele, aucun statut",
       "« Otherwise, find Darkhold and reveal it »", [HEROS] + deck("hf365", "hf362"), ["Puzzle.Reveal('hf365')"],
       {"attache": [["hf362", "hf401"]], "statuts_absents": [["01001a", "Stunned"], ["01001a", "Confused"]]}),
    _c("hf365 Boost : Selene active avec Soul Siphon en boost -> la carte est revelee (Darkhold cherche et attache)",
       "« [star] Boost : Reveal this card »", [HEROS, PRET_EXH] + deck("hf365", "hf362"), ["Puzzle.Attack('hf401')"],
       {"attache": [["hf362", "hf401"]]}),
    _c("hf366 Dimensional Portal, Darkhold sur le vilain : defausse jusqu'a un sbire (2 cartes defaussees), le REVELE (Little Demon en jeu), -1 darkspell",
       "« discard cards from the top of the encounter deck until a minion, reveal that minion, and remove 1 darkspell counter from Darkhold »",
       [HEROS] + deck("hf362", "hf366", "01105", "01105", "hf409"), ["Puzzle.Reveal('hf362')", "Puzzle.Reveal('hf366')"],
       {"en_jeu": ["hf409"], "defausse_rencontre_nb": [["01105", 2]], "compteurs_sur": [["hf362", "darkspell", 1]]}),
    _c("hf366 Dimensional Portal, SANS Darkhold : il est cherche et revele (rien n'est defausse)",
       "« Otherwise, find Darkhold and reveal it »", [HEROS] + deck("hf366", "hf362", "01105", "hf409"), ["Puzzle.Reveal('hf366')"],
       {"attache": [["hf362", "hf401"]], "absents": ["hf409"], "defausse_rencontre_nb": [["01105", 0]]}),
    _c("hf361 Darkhold Dwarf revele : glisse sous lui le Spell of Darkhold du DESSUS de la defausse (Soul Siphon, pose en dernier)",
       "« Tuck the topmost Spell of Darkhold encounter card from the encounter discard pile under here »",
       deck("hf361") + ["Puzzle.CreateEncounterDiscardPile('hf364', '01105', 'hf365')"], ["Puzzle.Reveal('hf361')"],
       {"en_jeu": ["hf361"], "glisse_sous": [["hf361", "hf365"]]}),
    _c("hf361 Darkhold Dwarf revele : ordre inverse (Hellfire Conjuration au-dessus) -> c'est elle qui est glissee",
       "le « topmost » depend de l'ordre de la defausse", deck("hf361") + ["Puzzle.CreateEncounterDiscardPile('hf365', '01105', 'hf364')"], ["Puzzle.Reveal('hf361')"],
       {"en_jeu": ["hf361"], "glisse_sous": [["hf361", "hf364"]]}),
    _c("hf361 Darkhold Dwarf revele SANS Spell of Darkhold dans la defausse : rien n'est glisse",
       "contre-cas", deck("hf361") + ["Puzzle.CreateEncounterDiscardPile('01105')"], ["Puzzle.Reveal('hf361')"], {"en_jeu": ["hf361"]}),
    _c("hf361 Darkhold Dwarf vaincu : « Reveal the card tucked here » (Hellfire Conjuration, Darkhold sur le vilain : 3 degats indirects)",
       "« When Defeated : Reveal the card tucked here »", [HEROS] + deck("hf362", "hf361") + ["Puzzle.CreateEncounterDiscardPile('hf364')"],
       ["Puzzle.Reveal('hf362')", "Puzzle.Reveal('hf361')", "Puzzle.Damage('hf361', 3)"], {"degats_identite": 3, "compteurs_sur": [["hf362", "darkspell", 1]]}),
    # ===================================================================== campagne
    _c("campagne scenario 3 (carnet vierge) : Emma Frost's Redemption est revelee, Xavier's Institute en jeu, la nuit en jeu",
       "livret : « if Emma Frost's Redemption is not checked, reveal it » (hf404a appelle `CampaignSetup(3)`)", [], [],
       {"en_jeu": ["hf042", "hf048", "hf407a"], "absents": ["hf043"], "recrutes_deck": []}, campagne=True),
    _c("campagne scenario 3 (Emma's Redemption cochee) : Emma Frost rejoint le deck Recruited Mutants et Cryptic Threatening Message est revelee",
       "« otherwise shuffle Emma Frost into the Recruited Mutants deck and reveal Cryptic Threatening Message »", [], [],
       {"en_jeu": ["hf043", "hf048"], "absents": ["hf042"], "recrutes_deck": ["hf025"]}, campagne=True, carnet={"Emma Frost's Redemption: Defeated": "1"}),
    _c("campagne scenario 3 : TEMOIN, hors campagne aucune carte de campagne n'entre en jeu",
       "`WhenCampaignSetup` ne part qu'en campagne", [], [], {"absents": ["hf042", "hf043", "hf048"], "en_jeu": ["hf407a"]}),
    _c("campagne scenario 3 : victoire avec Emma Frost's Redemption vaincue -> le carnet sortant la coche et porte l'estampille du scenario",
       "releve de fin de partie (`Releve`) : « Emma Frost's Redemption: Defeated »", [], ["Puzzle.AddToVictoryDisplay('hf042')", "Puzzle.Win()"],
       {"carnet_cles": {"Emma Frost's Redemption: Defeated": "1"}, "carnet_scenario": "hellfire_black_queen", "carnet_gagnee": True}, campagne=True),

    # ===================================================================== compléments (limites, témoins, chemins alternatifs)
    _c("hf407a Reponse forcee : un ALLIE (Luke Cage) attaque Selene -> 1 compteur retire (3 -> 2)",
       "« After a character uses a basic power » : un allie compte aussi (pouvoir de base ATK)", [HEROS, LC] + deck("01105"), ["Puzzle.Attack('01076')"],
       {"compteurs_sur": [["hf407a", "time", 2]]}, cibles=["hf401"], accepter_choix=True),
    _c("hf362 Uses : TEMOIN D'EPUISEMENT, DEUX attaques de Selene (2 compteurs) -> le Darkhold quitte le jeu a la 2e ; ATK 2 (avec le livre) puis 1 (sans) = 3 degats",
       "limite imprimee « Uses (2 Darkspell counters) » : apres la 1re attaque 1 compteur restait (cas plus haut), la 2e est la derniere",
       [HEROS, PRET_EXH] + deck("hf362"), ["Puzzle.Reveal('hf362')", "Puzzle.Attack('hf401')", "Puzzle.Attack('hf401')"],
       {"absents": ["hf362"], "degats_identite": 3}),
    _c("hf404b Interruption forcee : le Darkhold Dwarf est defausse du DESSUS du deck de rencontre (pas vaincu) -> le complot avance quand meme",
       "« When Darkhold Dwarf enters the discard pile » : quelle que soit la route", deck("hf361"), ["Puzzle.Discard('hf361')"],
       {"en_jeu": ["hf405b"], "absents": ["hf404b"]}),
    _c("hf405b When Completed : le Darkhold est DEJA attache a Selene (revele pendant le stade 2) -> il y reste, un seul exemplaire, la carte Tough est donnee",
       "« Find Darkhold and attach it to Selene » : rien a chercher",
       ["Puzzle.AdvanceMainScheme()", "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01105', '01105', 'hf408', 'hf422', 'hf362')", "Puzzle.Reveal('hf362')"],
       ["Puzzle.PlaceThreat('hf405b', 5)"],
       {"en_jeu": ["hf406b"], "attache": [["hf362", "hf401"]], "nb_en_jeu": [["hf362", 1]], "statuts": [["hf401", "Tough"]]}),
    _c("hf402 EXPERT : Selene (II) vaincue -> Selene (III), PV 17, Steady, Toughness ; ses attachements ne sont pas necessaires a la mesure",
       "expert : villain [hf402, hf403] ; le 1er degat est absorbe par la carte Tough de la Toughness (1 degat pour la retirer, puis 14 pour vaincre)", ["Puzzle.Damage('hf402', 1)", "Puzzle.Damage('hf402', 14)"] + deck("01105"), [],
       {"en_jeu": ["hf403"], "absents": ["hf402"], "vie": [["hf403", 17]], "steady": ["hf403"]}, scenario=SCX),

    _c("hf402 Reponse forcee (EXPERT, Selene II) : elle se soigne des degats non excedentaires (3 degats, 2 de plus au heros incline : 3 -> 1)",
       "meme Reponse forcee que hf401, sur la carte du stade II ; ATK 2 : le heros incline subit 2 + 0 icone ; la carte Tough de la Toughness est retiree d'abord",
       [HEROS, PRET_EXH, "Puzzle.Damage('hf402', 1)", "Puzzle.Damage('hf402', 3)"] + deck("01105"), ["Puzzle.Attack('hf402')"],
       {"degats_de": [["hf402", 1]], "degats_identite": 2}, scenario=SCX),
    _c("hf403 Reponse forcee (EXPERT, Selene III) : meme vol de vie (ATK 3 : 3 degats au heros incline, 5 -> 2)",
       "meme Reponse forcee sur la carte du stade III", ["Puzzle.AdvanceVillain()", HEROS, PRET_EXH, "Puzzle.Damage('hf403', 1)", "Puzzle.Damage('hf403', 5)"] + deck("01105"), ["Puzzle.Attack('hf403')"],
       {"degats_de": [["hf403", 2]], "degats_identite": 3}, scenario=SCX),
    _c("hf405a When Revealed : le module Darkhold mis de cote est melange au deck de rencontre (le complot avance au stade 2)",
       "« Shuffle the set-aside Darkhold modular set into the encounter deck »", ["Puzzle.AdvanceMainScheme()"], [],
       {"en_jeu": ["hf405b"], "pas_mis_de_cote": ["hf362", "hf363", "hf364", "hf365", "hf366"],
        "dans_deck_rencontre_nb": [["hf362", 1], ["hf363", 1], ["hf364", 1], ["hf365", 1], ["hf366", 1]]}),
]


VERIFICATIONS = r'''
def hfq_etat(monde, aides):
    """Copie de `hf_etat` (White Queen) + cles du scenario Black Queen : mis_de_cote [ids dans la zone mise de cote], glisse_sous [[hote, carte]], attache_a_vide [ids sans hote], deck_rencontre_nb [[nom_set, n]], defausse_rencontre_nb [[id, n]] : compteurs_sur [[id, nom, n]], menace_de [[id, n]], attaque [[id, n]], vie [[id, pv_max]],
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
    propres = ("prop_de", "hote_sbire", "victoire", "recrutes_deck", "carnet_cles", "carnet_cles_absentes", "carnet_gagnee", "carnet_scenario", "mis_de_cote", "pas_mis_de_cote", "glisse_sous", "dans_deck_rencontre_nb", "defausse_rencontre_nb", "compteurs_total_sur", "compteurs_sur", "menace_de", "attaque", "vie", "degats_de", "statuts_sur", "absents", "trait_de", "attache", "boosts_de", "steady", "acceleration", "gagnee", "partie_finie", "nb_en_jeu", "distribuees", "hors_deck_rencontre", "peut_defendre", "hote_pic")
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
    from game.operate.worlds import Worlds
    def _a_cote(m):
        return list(m.aside_deck.Get(True)) + [x for p in m.const_players for x in p.set_aside_deck.Get(True)]
    for cid in attendu.get("mis_de_cote", []):
        ids = {getattr(f.paper, "card_id", None) for f in _a_cote(monde)}
        if cid not in ids:
            soucis.append(f"{cid} n'est pas dans la zone mise de cote")
    for cid in attendu.get("pas_mis_de_cote", []):
        ids = {getattr(f.paper, "card_id", None) for f in _a_cote(monde)}
        if cid in ids:
            soucis.append(f"{cid} est dans la zone mise de cote")
    for hote, cid in attendu.get("glisse_sous", []):
        h = face(hote)
        if h is not None:
            vus = [getattr(f.paper, "card_id", None) for f in h.GetPlacedCardArea().Get(True)]
            if cid not in vus:
                soucis.append(f"{cid} n'est pas glissee sous {hote} (vu : {vus})")
    for cid, n in attendu.get("dans_deck_rencontre_nb", []):
        vus = [getattr(f.paper, "card_id", None) for f in Worlds.GetEncounterDeckCards(monde)].count(cid)
        if vus != n:
            soucis.append(f"{vus} exemplaire(s) de {cid} dans le deck de rencontre (attendu {n})")
    for cid, n in attendu.get("defausse_rencontre_nb", []):
        vus = [getattr(f.paper, "card_id", None) for f in Worlds.GetEncounterDiscardPileCards(monde)].count(cid)
        if vus != n:
            soucis.append(f"{vus} exemplaire(s) de {cid} dans la defausse de rencontre (attendu {n})")
    for cid, n in attendu.get("compteurs_total_sur", []):
        f = face(cid)
        if f is not None and sum(f.GetCounters(k) for k in ("time", "darkspell", "illusion")) != n:
            soucis.append(f"{cid} compteurs (tous) = {sum(f.GetCounters(k) for k in ('time', 'darkspell', 'illusion'))} (attendu {n})")
    for cid, attr, voulu in attendu.get("prop_de", []):
        f = face(cid)
        if f is not None and getattr(f, attr) != voulu:
            soucis.append(f"{cid}.{attr} = {getattr(f, attr)} (attendu {voulu})")
    for cid, sch, atk in attendu.get("hote_sbire", []):
        f = face(cid)
        hote = getattr(f, "bind_face", None) if f is not None else None
        from game.card.face.card_type import Minion as _Minion
        if f is not None and (hote is None or not _Minion.IsType(hote)):
            soucis.append(f"{cid} n'est pas attache a un SBIRE (hote = {hote})")
        elif hote is not None and (hote.scheme != sch or hote.attack != atk):
            soucis.append(f"hote de {cid} : SCH {hote.scheme} ATK {hote.attack} (attendu SCH {sch} ATK {atk})")
    if "victoire" in attendu:
        vus = {getattr(f.paper, "card_id", None) for f in monde.victory_display.Get(True)}
        for cid in attendu["victoire"]:
            if cid not in vus:
                soucis.append(f"{cid} n'est pas dans la pile de victoire")
    if "recrutes_deck" in attendu:
        etat = getattr(monde, "hf_recruited", None)
        ids = sorted(getattr(f.paper, "card_id", None) for f in etat[0].Get(True)) if etat else []
        if ids != sorted(attendu["recrutes_deck"]):
            soucis.append(f"deck Recruited Mutants = {ids} (attendu {sorted(attendu['recrutes_deck'])})")
    if any(k.startswith("carnet_") for k in attendu):
        import json as _json, os as _os
        from engine.config import ConfigVariables
        chemin = ConfigVariables.File('campaign_log_last_file', './campaign_log_last.json').value
        if not _os.path.exists(chemin):
            soucis.append(f"aucun carnet sortant ecrit ({chemin})")
        else:
            carnet = _json.load(open(chemin, encoding="utf-8"))
            sug = carnet.get("suggestions") or {}
            if "carnet_gagnee" in attendu and bool(carnet.get("players_won")) != attendu["carnet_gagnee"]:
                soucis.append(f"players_won = {carnet.get('players_won')}")
            if "carnet_scenario" in attendu and carnet.get("scenario") != attendu["carnet_scenario"]:
                soucis.append(f"estampille = {carnet.get('scenario')!r}")
            for cle, valeur in (attendu.get("carnet_cles") or {}).items():
                if sug.get(cle) != valeur:
                    soucis.append(f"{cle} = {sug.get(cle)!r} (attendu {valeur!r})")
            for cle in attendu.get("carnet_cles_absentes") or []:
                if cle in sug:
                    soucis.append(f"{cle} = {sug[cle]!r} alors qu'il ne devrait pas y etre")
    if soucis:
        return False, " ; ".join(soucis)
    return True, "etat conforme"
'''
