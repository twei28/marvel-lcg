# Cas test_capacites du heros HEPZIBAH (Starjammers, Phenexian et Mysteltainn, prefixe `hz`) :
# noms prefixes « [hz] » puis le card_id (substituer_pack.py filtre dessus).
#
# Rappels de montage :
#  - le deck `hepzibah` demarre en ALTER EGO (hz001b) ; `Puzzle.ChangeToFace('hz001b', 'hz001a')` la passe en HEROS sans rien
#    declencher ; `Puzzle.ChangeForm('hz001a')` fait un VRAI changement de forme (messages envoyes) ;
#  - Rhino 01094 est le vilain, 01097b son complot principal (menace 0 au depart), 01101 Hydra Mercenary un sbire (3 PV, Guard) ;
#  - ressources : 01088 Energy = YY, 01089 Genius = BB, 01090 Strength = RR ; 01083 Mockingbird (cout 3) est un allie ordinaire ;
#  - « resolve the Special ability on a card in your hand » : les evenements hz007-hz010 portent un Special ; le pilote choisit
#    la PREMIERE carte candidate de la main (ordre de `main_exclusive`) ;
#  - ⚠ `main_exclusive` DEFAUSSE la main de depart apres la mise en place ; `Puzzle.EmptyHand()` vide la main (liste vide ignoree).
SC = "rhino"
HEROS = "Puzzle.ChangeToFace('hz001b', 'hz001a')"
VILAIN = "01094"
COMPLOT = "01097b"
SBIRE = "01101"
SANS_BOOST = ["Puzzle.EmptyEncounterDeck()",
              "Puzzle.CreateEncounterDeck('01098', '01098', '01098', '01098', '01098', '01098', '01098', '01098')"]


def en_jeu(*ids):
    return [f"Puzzle.PutIntoPlay('{i}', under_control=True)" for i in ids]


def _c(nom, pourquoi, mise, declencher, attendu, **cle):
    mise = SANS_BOOST + list(mise)
    cas = {"nom": "[hz] " + nom, "pourquoi": pourquoi, "scenario": cle.pop("scenario", SC),
           "heros": cle.pop("heros", "hepzibah"), "mise_en_place": mise, "declencher": declencher,
           "verifier": cle.pop("verifier", "hz_etat"), "attendu": attendu}
    cas.setdefault("regles", ["v16_all", "v18_all"])
    cas.update(cle)
    return cas


CAS = [
    # ============================================================ hz001a / hz001b : identite
    _c("hz001a Hepzibah : valeurs imprimees PV 10, STARJAMMER ; ATQ 2 (2 degats a Rhino)",
       "nombres texte <-> code (scan) : HAND SIZE 5 / HIT POINTS 10, THW 1 ATK 2 DEF 2",
       [HEROS], ["Puzzle.Attack('hz001a')"], {"pv_max": [["hz001a", 10]], "traits": ["STARJAMMER"], "degats": [[VILAIN, 2]]},
       main_exclusive=["01090"], cibles=[VILAIN], accepter_choix=True),
    _c("hz001a Hepzibah : valeurs imprimees CTR 1 (1 menace retiree)",
       "nombres texte <-> code (scan) : THW 1", [HEROS, f"Puzzle.SetThreat('{COMPLOT}', 4)"], ["Puzzle.Thwart('hz001a')"],
       {"menace": [[COMPLOT, 3]]}, main_exclusive=["01090"], cibles=[COMPLOT], accepter_choix=True),
    _c("hz001b Hepzibah : valeurs imprimees PV 10, OUTLAW",
       "nombres texte <-> code (scan) : HAND SIZE 6 / HIT POINTS 10 / REC 3", [], [],
       {"pv_max": [["hz001b", 10]], "traits": ["OUTLAW"]}, main_exclusive=["01090"]),

    # ============================================================ hz001a : Response (apres un evenement)
    _c("hz001a Response : apres un evenement joue, le Special de Feral Rage en main -> +1 ATQ",
       "« After you play an event, resolve the Special ability on a card in your hand » : Keen Senses (cout 1, 01089 BB) puis le Special de "
       "Feral Rage (hz007, en main) : Hepzibah gagne +1 ATQ jusqu'a la fin de la phase ; la menace passe de 5 a 3",
       [HEROS, f"Puzzle.SetThreat('{COMPLOT}', 5)"], [],
       {"menace": [[COMPLOT, 3]], "attributs": {"attack": 1}, "en_main": ["hz007"]},
       main_exclusive=["hz008", "hz007", "01089"], payer_avec=["01089"], jouer=["hz008"], cibles=[COMPLOT], accepter_choix=True),
    _c("hz001a Response : CONTRE-CAS, aucun Special en main -> pas de bonus (ATQ imprimee)",
       "la Response n'est pas offerte sans carte a Special en main",
       [HEROS, f"Puzzle.SetThreat('{COMPLOT}', 5)"], [],
       {"menace": [[COMPLOT, 3]], "attributs": {"attack": 0}},
       main_exclusive=["hz008", "01089"], payer_avec=["01089"], jouer=["hz008"], cibles=[COMPLOT], accepter_choix=True),

    # ============================================================ hz001b : Response (passage en alter ego)
    _c("hz001b Response : apres le passage en alter ego, 2 evenements de la defausse vont sous le deck",
       "« place 2 events in your discard pile on the bottom of your deck » : deck de 2 cartes -> 4, les deux evenements dedans",
       [HEROS, "Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01073', '01074')"],
       ["Puzzle.EmptyPlayerDiscardPile()", "Puzzle.CreatePlayerDiscardPile('hz007', 'hz008')", "Puzzle.ChangeForm('hz001a')"],
       {"dans_deck_joueur": ["hz007", "hz008"], "taille_deck_joueur": 4, "en_jeu": ["hz001b"]},
       main_exclusive=["01090"], accepter_choix=True),
    _c("hz001b Response : un seul evenement dans la defausse -> seul celui-la est place (la carte non evenement reste)",
       "« 2 events » : on place ce qu'il y a (1 evenement), la defausse garde l'autre carte",
       [HEROS, "Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01073', '01074')"],
       ["Puzzle.EmptyPlayerDiscardPile()", "Puzzle.CreatePlayerDiscardPile('hz007', '01090')", "Puzzle.ChangeForm('hz001a')"],
       {"dans_deck_joueur": ["hz007"], "taille_deck_joueur": 3, "defausse": ["01090"]},
       main_exclusive=["01089"], accepter_choix=True),
    _c("hz001b Response : CONTRE-CAS, aucun evenement dans la defausse -> le deck ne change pas",
       "rien a placer", [HEROS, "Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01073', '01074')"],
       ["Puzzle.EmptyPlayerDiscardPile()", "Puzzle.CreatePlayerDiscardPile('01090')", "Puzzle.ChangeForm('hz001a')"],
       {"taille_deck_joueur": 2, "defausse": ["01090"]}, main_exclusive=["01089"], accepter_choix=True),

    # ============================================================ hz002 Corsair (allie)
    _c("hz002 Corsair : apres un pouvoir de base, le Special de Feral Rage en main -> +1 ATQ",
       "« After Corsair uses a basic power, resolve the Special ability on a card in your hand » : Corsair attaque, 2 degats a Rhino",
       [HEROS] + en_jeu("hz002"), ["Puzzle.Attack('hz002')"],
       {"degats": [[VILAIN, 2]], "attributs": {"attack": 1}},
       main_exclusive=["hz007"], cibles=[VILAIN], accepter_choix=True),
    _c("hz002 Corsair : le Special de Feline Grace redresse Hepzibah (heros incline)",
       "meme Reponse, autre Special : Hepzibah etait inclinee, elle se redresse",
       [HEROS, "Puzzle.Exhaust('hz001a')"] + en_jeu("hz002"), ["Puzzle.Attack('hz002')"],
       {"pret": ["hz001a"], "degats": [[VILAIN, 2]]},
       main_exclusive=["hz009"], cibles=[VILAIN], accepter_choix=True),
    _c("hz002 Corsair : CONTRE-CAS, en forme alter ego la Hero Response n'est pas offerte",
       "« Hero Response » : l'identite reste inclinee",
       ["Puzzle.Exhaust('hz001b')"] + en_jeu("hz002") + [f"Puzzle.SetThreat('{COMPLOT}', 3)"], ["Puzzle.Thwart('hz002')"],
       {"exhausted": ["hz001b"], "menace": [[COMPLOT, 1]]},
       main_exclusive=["hz009"], cibles=[COMPLOT], accepter_choix=True),
    _c("hz002 Corsair : valeurs imprimees cout 3, PV 3, STARJAMMER",
       "nombres texte <-> code (scan)", [HEROS] + en_jeu("hz002"), [],
       {"pv_max": [["hz002", 3]], "traits_de": [["hz002", "STARJAMMER"]]}, main_exclusive=["01090"]),

    # ============================================================ hz003 Targeting Goggles
    _c("hz003 Targeting Goggles : cherche un evenement dans le deck, l'ajoute, puis remet 1 carte sur le dessus",
       "« search your deck for an event and add it to your hand. Then place 1 card from your hand on top of your deck » : main vide -> "
       "Feral Rage ajoutee puis remise sur le dessus ; Goggles inclinees",
       [HEROS, "Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('hz007', '01073', '01074')", "Puzzle.EmptyHand()"] + en_jeu("hz003"),
       ["Puzzle.Action('hz003', 'HeroAction')"],
       {"exhausted": ["hz003"], "taille_main": 0, "dans_deck_joueur": ["hz007"], "taille_deck_joueur": 3},
       accepter_choix=True),
    _c("hz003 Targeting Goggles : 2 cartes en main apres la recherche -> la main finit a 1 carte de plus que le depart",
       "la recherche ajoute 1 carte, le placement en retire 1 : main 1 -> 1, deck inchange en taille",
       [HEROS, "Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('hz007', '01073', '01074')"] + en_jeu("hz003"),
       ["Puzzle.Action('hz003', 'HeroAction')"],
       {"exhausted": ["hz003"], "taille_main": 1, "taille_deck_joueur": 3},
       main_exclusive=["01090"], accepter_choix=True),

    _c("hz003 Targeting Goggles : « Then » : aucun evenement dans le deck -> RIEN n'est remis sur le dessus (main 1, deck 3 inchanges)",
       "RR « Then » : si le texte avant « then » ne se resout pas entierement, celui d'apres n'est pas tente ; le deck n'a que des ressources "
       "(01088), la main garde Strength (01090) au lieu de la perdre sur le deck",
       [HEROS, "Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01088', '01088', '01088')"] + en_jeu("hz003"),
       ["Puzzle.Action('hz003', 'HeroAction')"],
       {"exhausted": ["hz003"], "taille_main": 1, "taille_deck_joueur": 3, "en_main": ["01090"],
        "hz_avis": "No event in your deck: no card is placed on top of your deck."},
       main_exclusive=["01090"], accepter_choix=True),

    # ============================================================ hz004 Hepzibah's Spacesuit
    _c("hz004 Spacesuit : Hero Resource -> paie un evenement (Keen Senses) et s'incline",
       "« Exhaust Hepzibah's Spacesuit -> generate a [wild] resource for an event » : Keen Senses (cout 1) payee par la combinaison seule",
       [HEROS, f"Puzzle.SetThreat('{COMPLOT}', 5)"] + en_jeu("hz004"), [],
       {"menace": [[COMPLOT, 3]], "exhausted": ["hz004"]},
       main_exclusive=["hz008"], jouer=["hz008"], cibles=[COMPLOT], accepter_choix=True),
    _c("hz004 Spacesuit : CONTRE-CAS, ne paie PAS une amelioration (Targeting Goggles reste en main)",
       "« for an event » seulement", [HEROS] + en_jeu("hz004"), [],
       {"en_main": ["hz003"], "pret": ["hz004"]},
       main_exclusive=["hz003"], jouer=["hz003"], accepter_choix=True),
    _c("hz004 Spacesuit : un 3e amelioration Restricted est permise (hz005 + hz006 + Pulse Blaster cr004)",
       "« You can control 1 additional upgrade that has the restricted keyword » : trois ameliorations Restricted en jeu",
       [HEROS] + en_jeu("hz004", "hz005", "hz006"), [],
       {"en_jeu": ["hz004", "hz005", "hz006", "cr004"]},
       main_exclusive=["cr004", "01088"], payer_avec=["01088"], jouer=["cr004"], accepter_choix=True),
    _c("hz004 Spacesuit : CONTRE-CAS, sans la combinaison le 3e Restricted ne rentre pas (une des trois sort du jeu)",
       "limite de 2 Restricted par defaut", [HEROS] + en_jeu("hz005", "hz006"), [],
       {"hors_jeu": ["hz005"], "en_jeu": ["hz006", "cr004"]},
       main_exclusive=["cr004", "01088"], payer_avec=["01088"], jouer=["cr004"], accepter_choix=True),

    # ============================================================ hz005 Energy Blaster
    _c("hz005 Energy Blaster : 1 degat, un compteur de charge en moins, incline",
       "« Exhaust and remove 1 charge counter -> deal 1 damage to an enemy » : 3 compteurs -> 2",
       [HEROS] + en_jeu("hz005"), ["Puzzle.Action('hz005', 'HeroAction')"],
       {"degats": [[VILAIN, 1]], "compteurs": [["hz005", "charge", 2]], "exhausted": ["hz005"]},
       main_exclusive=["01090"], cibles=[VILAIN], accepter_choix=True),
    _c("hz005 Energy Blaster : si l'action vainc l'ennemi, le Special de Feral Rage en main -> +1 ATQ",
       "« If this action defeats that enemy, resolve the Special ability on a card in your hand » : Hydra Mercenary (3 PV) a 2 degats",
       [HEROS] + en_jeu("hz005", SBIRE) + [f"Puzzle.Damage('{SBIRE}', 2)"], ["Puzzle.Action('hz005', 'HeroAction')"],
       {"hors_jeu": [SBIRE], "attributs": {"attack": 1}, "compteurs": [["hz005", "charge", 2]]},
       main_exclusive=["hz007"], cibles=[SBIRE], accepter_choix=True),
    _c("hz005 Energy Blaster : si l'action vainc le MECHANT (derniere PV d'une etape), le Special de Feral Rage en main -> +1 ATQ",
       "RR « Villain Defeat » : si le cadran de PV du mechant tombe a zero, les joueurs ont vaincu CETTE etape : « defeats that enemy » vaut aussi "
       "pour un mechant (comportement sur le mechant non mesure avant le 26/10/2026)",
       [HEROS, "Puzzle.SetHealth('01094', 1)"] + en_jeu("hz005"), ["Puzzle.Action('hz005', 'HeroAction')"],
       {"attributs": {"attack": 1}, "compteurs": [["hz005", "charge", 2]]},
       main_exclusive=["hz007"], cibles=[VILAIN], accepter_choix=True),
    _c("hz005 Energy Blaster : CONTRE-CAS, le mechant a 2 PV n'est pas vaincu par 1 degat -> pas de Special (ATQ imprimee)",
       "meme montage que le cas « vainc le MECHANT », avec 1 PV de trop : le Special ne part pas",
       [HEROS, "Puzzle.SetHealth('01094', 2)"] + en_jeu("hz005"), ["Puzzle.Action('hz005', 'HeroAction')"],
       {"attributs": {"attack": 0}, "compteurs": [["hz005", "charge", 2]]},
       main_exclusive=["hz007"], cibles=[VILAIN], accepter_choix=True),
    _c("hz005 Energy Blaster : CONTRE-CAS, l'ennemi n'est pas vaincu -> pas de Special",
       "Hydra Mercenary (3 PV) n'a pas assez de degats : l'ATQ reste imprimee", [HEROS] + en_jeu("hz005", SBIRE),
       ["Puzzle.Action('hz005', 'HeroAction')"],
       {"degats": [[SBIRE, 1]], "attributs": {"attack": 0}},
       main_exclusive=["hz007"], cibles=[SBIRE], accepter_choix=True),
    _c("hz005 Energy Blaster : TEMOIN D'EPUISEMENT, le dernier compteur retire -> la carte est defaussee (Uses)",
       "« Uses (3 charge counters) » : il en reste 1 (3 + (-2)) ; apres l'action la carte quitte le jeu",
       [HEROS] + en_jeu("hz005") + ["Puzzle.Counter('hz005', 'charge', -2)"], ["Puzzle.Action('hz005', 'HeroAction')"],
       {"hors_jeu": ["hz005"], "defausse": ["hz005"], "degats": [[VILAIN, 1]]},
       main_exclusive=["01090"], cibles=[VILAIN], accepter_choix=True),

    # ============================================================ hz006 Heavy Machine Gun
    _c("hz006 Heavy Machine Gun : 1 degat a CHAQUE ennemi, un compteur de munitions en moins",
       "« deal 1 damage to each enemy » : Rhino et Hydra Mercenary ; 2 compteurs -> 1",
       [HEROS] + en_jeu("hz006", SBIRE), ["Puzzle.Action('hz006', 'HeroAction')"],
       {"degats": [[VILAIN, 1], [SBIRE, 1]], "compteurs": [["hz006", "ammo", 1]], "exhausted": ["hz006"]},
       main_exclusive=["01090"], accepter_choix=True),
    _c("hz006 Heavy Machine Gun : TEMOIN D'EPUISEMENT, le dernier compteur -> la carte est defaussee",
       "« Uses (2 ammo counters) » : il en reste 1 ; apres l'action la carte quitte le jeu",
       [HEROS] + en_jeu("hz006") + ["Puzzle.Counter('hz006', 'ammo', -1)"], ["Puzzle.Action('hz006', 'HeroAction')"],
       {"hors_jeu": ["hz006"], "defausse": ["hz006"], "degats": [[VILAIN, 1]]},
       main_exclusive=["01090"], accepter_choix=True),

    # ============================================================ hz007 Feral Rage
    _c("hz007 Feral Rage : degats egaux a l'ATQ (2 a Rhino)",
       "« Deal damage to an enemy equal to your ATK » : cout 1 (01090 RR)", [HEROS], [],
       {"degats": [[VILAIN, 2]], "defausse": ["hz007"]},
       main_exclusive=["hz007", "01090"], payer_avec=["01090"], jouer=["hz007"], cibles=[VILAIN], accepter_choix=True),
    _c("hz007 Feral Rage : le Special (depuis la main, via Keen Senses) donne +1 ATQ",
       "voir hz001a : le Special de la carte en MAIN est resolu apres un autre evenement", [HEROS, f"Puzzle.SetThreat('{COMPLOT}', 5)"], [],
       {"attributs": {"attack": 1}, "menace": [[COMPLOT, 3]]},
       main_exclusive=["hz008", "hz007", "01089"], payer_avec=["01089"], jouer=["hz008"], cibles=[COMPLOT], accepter_choix=True),

    _c("hz007 Feral Rage : le Special resolu en PHASE DU MECHANT donne +1 ATQ qui TIENT apres cette phase (jusqu'a la fin de la phase des joueurs SUIVANTE)",
       "RR « Lasting Effects » : « until the end of the player phase » = la fin de la phase des joueurs, meme si le Special se resout pendant "
       "la phase du mechant (avant : le bonus s'arretait a la fin de la phase du mechant)",
       [HEROS] + en_jeu("hz007"), ["Puzzle.BeginVillainPhase()", "Puzzle.ResolveSpecial('hz007')", "Puzzle.EndVillainPhase()"],
       {"attributs": {"attack": 1}}),
    _c("hz007 Feral Rage : TEMOIN, ce meme +1 ATQ tombe a la fin de la phase des joueurs suivante (la duree MORD)",
       "meme montage, puis la phase des joueurs suivante se termine : l'ATQ revient a l'imprimee",
       [HEROS] + en_jeu("hz007"),
       ["Puzzle.BeginVillainPhase()", "Puzzle.ResolveSpecial('hz007')", "Puzzle.EndVillainPhase()", "Puzzle.EndPlayerPhase()"],
       {"attributs": {"attack": 0}}),

    # ============================================================ hz008 Keen Senses
    _c("hz008 Keen Senses : retire 2 menaces (5 -> 3), le heros incline reste incline",
       "« Remove 2 threat from a scheme » : la derniere menace n'est pas retiree", [HEROS, f"Puzzle.SetThreat('{COMPLOT}', 5)", "Puzzle.Exhaust('hz001a')"], [],
       {"menace": [[COMPLOT, 3]], "exhausted": ["hz001a"]},
       main_exclusive=["hz008", "01089"], payer_avec=["01089"], jouer=["hz008"], cibles=[COMPLOT], accepter_choix=True),
    _c("hz008 Keen Senses : la DERNIERE menace retiree -> Hepzibah se redresse",
       "« If this removes the last threat on that scheme, ready Hepzibah » : menace 2 -> 0", [HEROS, f"Puzzle.SetThreat('{COMPLOT}', 2)", "Puzzle.Exhaust('hz001a')"], [],
       {"menace": [[COMPLOT, 0]], "pret": ["hz001a"]},
       main_exclusive=["hz008", "01089"], payer_avec=["01089"], jouer=["hz008"], cibles=[COMPLOT], accepter_choix=True),
    _c("hz008 Keen Senses : le Special (depuis la main, via Feral Rage) retire 1 menace",
       "« Special: Remove 1 threat from a scheme » : Feral Rage (2 degats), puis le Special de Keen Senses en main : 5 -> 4",
       [HEROS, f"Puzzle.SetThreat('{COMPLOT}', 5)"], [],
       {"degats": [[VILAIN, 2]], "menace": [[COMPLOT, 4]]},
       main_exclusive=["hz007", "hz008", "01090"], payer_avec=["01090"], jouer=["hz007"], cibles=[VILAIN, COMPLOT], accepter_choix=True),

    # ============================================================ hz009 Feline Grace
    _c("hz009 Feline Grace : Rhino attaque, 4 degats evites",
       "« When you would take any amount of damage from an attack, prevent 4 of that damage » : cout 0 ; le heros est incline (sinon il defend lui-meme, "
       "DEF 2 contre ATQ 2, et la mesure ne prouverait rien)",
       [HEROS, "Puzzle.Exhaust('hz001a')"], ["Puzzle.Attack('01094')"],
       {"degats_identite": 0, "defausse": ["hz009"]},
       main_exclusive=["hz009"], accepter_choix=True),
    _c("hz009 Feline Grace : CONTRE-CAS, sans la carte Rhino blesse Hepzibah",
       "temoin : la meme attaque sans Feline Grace, heros incline", [HEROS, "Puzzle.Exhaust('hz001a')"], ["Puzzle.Attack('01094')"],
       {"degats_identite_min": 1}, main_exclusive=["01090"], accepter_choix=True),
    _c("hz009 Feline Grace : le Special redresse Hepzibah (heros incline)",
       "« Special: Ready Hepzibah » : Feral Rage jouee, puis le Special de Feline Grace en main",
       [HEROS, "Puzzle.Exhaust('hz001a')"], [],
       {"pret": ["hz001a"], "degats": [[VILAIN, 2]]},
       main_exclusive=["hz007", "hz009", "01090"], payer_avec=["01090"], jouer=["hz007"], cibles=[VILAIN], accepter_choix=True),
    _c("hz009 Feline Grace : TEMOIN D'EPUISEMENT, (Limit once per phase) -> le 2e Special de la phase ne redresse pas",
       "deux Keen Senses jouees dans la meme phase, le heros est re-incline entre les deux : il reste incline au 2e Special de la carte",
       [HEROS, "Puzzle.Exhaust('hz001a')", f"Puzzle.SetThreat('{COMPLOT}', 6)"], [],
       {"exhausted": ["hz001a"], "menace": [[COMPLOT, 2]]},
       main_exclusive=["hz009", "hz008", "hz008", "01089", "01088"], payer_avec=["01089", "01088"], jouer=["hz008"],
       declencher_apres=["Puzzle.Exhaust('hz001a')"], jouer_apres=["hz008"], cibles=[COMPLOT, COMPLOT], accepter_choix=True),

    # ============================================================ hz010 Armed to the Teeth
    _c("hz010 Armed to the Teeth : 1re branche, chaque arme controlee se redresse",
       "« Ready each WEAPON you control » : Energy Blaster et Heavy Machine Gun inclinees",
       [HEROS] + en_jeu("hz005", "hz006") + ["Puzzle.Exhaust('hz005', 'hz006')"], [],
       {"pret": ["hz005", "hz006"], "defausse": ["hz010"]},
       main_exclusive=["hz010"], jouer=["hz010"], preferer_option="Ready each WEAPON", accepter_choix=True),
    _c("hz010 Armed to the Teeth : 2e branche, cherche une arme dans le deck et l'ajoute a la main",
       "« Search your deck and discard pile for a WEAPON and add it to your hand » : Heavy Machine Gun est dans le deck",
       [HEROS, "Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('hz006', '01073', '01074')"], [],
       {"en_main": ["hz006"], "defausse": ["hz010"]},
       main_exclusive=["hz010"], jouer=["hz010"], preferer_option="Search your deck", accepter_choix=True),
    _c("hz010 Armed to the Teeth : le Special (via Feral Rage) place 1 compteur polyvalent sur une arme",
       "« Place 1 all-purpose counter on a WEAPON you control » : Energy Blaster en jeu ; un compteur polyvalent compte comme N'IMPORTE quel "
       "compteur (regle) : `GetCounters('charge')` et `GetCounters('all-purpose')` rendent le TOTAL (3 charge + 1 polyvalent = 4 ; sans le "
       "Special : 3, voir le temoin)",
       [HEROS] + en_jeu("hz005"), [],
       {"compteurs": [["hz005", "charge", 4], ["hz005", "all-purpose", 4]], "degats": [[VILAIN, 2]]},
       main_exclusive=["hz007", "hz010", "01090"], payer_avec=["01090"], jouer=["hz007"], cibles=[VILAIN], accepter_choix=True),

    _c("hz010 Armed to the Teeth : CONTRE-CAS, sans le Special le total reste 3 (les 3 compteurs de charge)",
       "temoin de la lecture « total des compteurs » : Feral Rage jouee SANS Armed to the Teeth en main", [HEROS] + en_jeu("hz005"), [],
       {"compteurs": [["hz005", "charge", 3], ["hz005", "all-purpose", 3]]},
       main_exclusive=["hz007", "01090"], payer_avec=["01090"], jouer=["hz007"], cibles=[VILAIN], accepter_choix=True),

    # ============================================================ hz011 Vendetta
    _c("hz011 Vendetta : Forced Interrupt, un sbire entre en jeu -> engage et Hepzibah passe en forme heros",
       "« When a minion enters play, engage it and flip to hero form » : alter ego au depart, Hydra Mercenary est revele",
       [], ["Puzzle.Reveal('hz011')", f"Puzzle.Reveal('{SBIRE}')"],
       {"en_jeu": ["hz001a", SBIRE]}, main_exclusive=["01090"], accepter_choix=True),
    _c("hz011 Vendetta : tant qu'un sbire est engage, impossible de passer en alter ego",
       "« You cannot flip to alter-ego while a minion is engaged with you » : le sbire est REVELE (donc engage par le moteur, `en_jeu` + `Puzzle.Engage` "
       "ne le rangeait pas dans la zone des sbires engages), puis Vendetta",
       [HEROS, f"Puzzle.Reveal('{SBIRE}')", "Puzzle.Reveal('hz011')"], ["Puzzle.ChangeForm('hz001a')"],
       {"en_jeu": ["hz001a"]}, main_exclusive=["01090"], accepter_choix=True),
    _c("hz011 Vendetta : CONTRE-CAS, aucun sbire engage -> le passage en alter ego est possible",
       "meme obligation sans sbire", [HEROS, "Puzzle.Reveal('hz011')"], ["Puzzle.ChangeForm('hz001a')"],
       {"en_jeu": ["hz001b"]}, main_exclusive=["01090"], accepter_choix=True),
    _c("hz011 Vendetta : Action, defausser un allie -> l'obligation est retiree de la partie",
       "« Discard an ally you control -> remove this card from the game »", [HEROS] + en_jeu("01083"),
       ["Puzzle.Reveal('hz011')", "Puzzle.Action('hz011', 'Action')"],
       {"hz_retirees": ["hz011"], "defausse": ["01083"]}, main_exclusive=["01090"], cibles=["01083"], accepter_choix=True),

    # ============================================================ hz012 Minister T'Cahr
    _c("hz012 Minister T'Cahr : apres son activation contre vous, une carte SHI'AR du deck rencontre est revelee",
       "« After T'Cahr activates against you, search the encounter deck and discard pile for a SHI'AR card and reveal it » : Shi'ar Infantry "
       "(revelee, puis son « When Revealed » met l'autre copie en jeu : 2 en jeu)",
       [HEROS] + en_jeu("hz012") + ["Puzzle.EmptyEncounterDeck()",
        "Puzzle.CreateEncounterDeck('hz015', 'hz015', '01098', '01098', '01098', '01098')"], ["Puzzle.Activate('hz012')"],
       {"hz_nb_en_jeu": [["hz015", 2]]}, main_exclusive=["01090"], accepter_choix=True),
    _c("hz012 Minister T'Cahr : CONTRE-CAS, aucune carte SHI'AR dans le deck -> rien n'est revele",
       "recherche vide", [HEROS] + en_jeu("hz012"), ["Puzzle.Activate('hz012')"],
       {"hz_nb_en_jeu": [["hz015", 0]]}, main_exclusive=["01090"], accepter_choix=True),
    _c("hz012 Minister T'Cahr : valeurs imprimees PV 5, SHI'AR",
       "nombres texte <-> code (scan)", [HEROS] + en_jeu("hz012"), [],
       {"pv_max": [["hz012", 5]], "traits_de": [["hz012", "SHI'AR"]]}, main_exclusive=["01090"]),

    # ============================================================ hz013 Kill Order
    _c("hz013 Kill Order : revelee, menace 3 (une partie solo)",
       "nombres texte <-> code (scan) : menace de depart 3 par heros", [HEROS], ["Puzzle.Reveal('hz013')"],
       {"menace": [["hz013", 3]]}, main_exclusive=["01090"], accepter_choix=True),
    _c("hz013 Kill Order : « Each minion gains quickstrike », le sbire attaque des qu'il s'engage",
       "Hydra Mercenary revele pendant Kill Order : il s'engage et frappe aussitot (Hepzibah, inclinee donc sans defense, subit des degats)",
       [HEROS, "Puzzle.Exhaust('hz001a')"], ["Puzzle.Reveal('hz013')", f"Puzzle.Reveal('{SBIRE}')"],
       {"degats_identite_min": 1}, main_exclusive=["01090"], accepter_choix=True),
    _c("hz013 Kill Order : CONTRE-CAS, sans Kill Order le sbire revele ne frappe pas aussitot",
       "temoin, heros incline : aucun degat puisque aucune attaque", [HEROS, "Puzzle.Exhaust('hz001a')"], [f"Puzzle.Reveal('{SBIRE}')"],
       {"degats_identite": 0}, main_exclusive=["01090"], accepter_choix=True),

    # ============================================================ hz014 The Vengeful Wing
    _c("hz014 The Vengeful Wing : ses attaques infligent des degats INDIRECTS (le joueur les repartit : 2 sur son allie)",
       "« [star] The Vengeful Wing's attacks deal indirect damage » : heros ET allie inclines (sans defense) ; une attaque DIRECTE de 3 tomberait en entier "
       "sur Hepzibah (le moteur demande « Assign 3 damage » seulement pour l'indirect). Le joueur assigne les points : 2 a l'allie (Mockingbird), 1 a Hepzibah",
       [HEROS, "Puzzle.Exhaust('hz001a')"] + en_jeu("hz014", "01083") + ["Puzzle.Exhaust('01083')"], ["Puzzle.Attack('hz014')"],
       {"degats": [["01083", 2]], "degats_identite": 1}, main_exclusive=["01090"], cibles=["01083", "01083", "hz001a"], accepter_choix=True),
    _c("hz014 The Vengeful Wing : valeurs imprimees PV 6, ELITE SHI'AR VEHICLE",
       "nombres texte <-> code (scan)", [HEROS] + en_jeu("hz014"), [],
       {"pv_max": [["hz014", 6]], "traits_de": [["hz014", "ELITE"], ["hz014", "SHI'AR"], ["hz014", "VEHICLE"]]}, main_exclusive=["01090"]),

    # ============================================================ hz015 Shi'ar Infantry
    _c("hz015 Shi'ar Infantry : « When Revealed », l'autre copie du deck rencontre entre en jeu",
       "revelee + autre copie mise en jeu (non revelee) = 2 Shi'ar Infantry en jeu",
       [HEROS, "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('hz015', 'hz015', '01098', '01098', '01098')"],
       ["Puzzle.Reveal('hz015')"],
       {"hz_nb_en_jeu": [["hz015", 2]]}, main_exclusive=["01090"], accepter_choix=True),
    _c("hz015 Shi'ar Infantry : en Boost (attaque de Rhino), la carte est mise en jeu",
       "« [star] Boost: Put this card into play » : hz015 donnee face cachee en boost a Rhino, qui attaque",
       [HEROS, "Puzzle.GiveFacedownBoost('01094', 'hz015')"],
       ["Puzzle.Attack('01094')"],
       {"hz_nb_en_jeu": [["hz015", 1]]}, main_exclusive=["01090"], accepter_choix=True),
    _c("hz015 Shi'ar Infantry : valeurs imprimees PV 2, SHI'AR SOLDIER",
       "nombres texte <-> code (scan)", [HEROS] + en_jeu("hz015"), [],
       {"pv_max": [["hz015", 2]], "traits_de": [["hz015", "SHI'AR"], ["hz015", "SOLDIER"]]}, main_exclusive=["01090"]),
]


VERIFICATIONS = r'''
def hz_etat(monde, aides):
    """Cles propres : `hz_retirees` / `hz_retirees_absentes` (zone retiree du jeu), `hz_nb_en_jeu` ([[card_id, n]] : combien
    d'exemplaires en jeu), `hz_total_degats` ([[[card_id, ...], total]] : degats cumules sur ces cartes) ; le reste va a
    etat_attendu."""
    cas = aides["cas"]
    attendu = cas.get("attendu") or {}
    soucis = []
    ids = lambda faces: [getattr(f.paper, "card_id", None) for f in faces]
    retirees = ids(monde.area_removed.Get(True))
    for c in attendu.get("hz_retirees") or []:
        if c not in retirees:
            soucis.append(f"{c} pas retiree du jeu (retirees = {retirees})")
    for c in attendu.get("hz_retirees_absentes") or []:
        if c in retirees:
            soucis.append(f"{c} retiree du jeu (elle ne devait pas l'etre)")
    for card_id, voulu in attendu.get("hz_nb_en_jeu") or []:
        total = 0
        for objet in monde.object_manager.card_dict.values():
            face = getattr(objet, "face", None) or objet
            if getattr(getattr(face, "paper", None), "card_id", None) == card_id and face.IsInPlay():
                total += 1
        if total != voulu:
            soucis.append(f"{total} exemplaire(s) de {card_id} en jeu (attendu {voulu})")
    for cartes, voulu in attendu.get("hz_total_degats") or []:
        total = 0
        for card_id in cartes:
            face = aides["par_id"](monde, card_id)
            if face is None:
                soucis.append(f"{card_id} introuvable en jeu (hz_total_degats)")
                continue
            total += face.max_health - face.health
        if total != voulu:
            soucis.append(f"degats cumules sur {cartes} = {total} (attendu {voulu})")
    avis = [c.get("texte") for c in getattr(monde.stat, "choix_uniques", []) if c.get("texte")]
    if attendu.get("hz_avis") and attendu["hz_avis"] not in avis:
        soucis.append(f"l'avis « {attendu['hz_avis']} » n'a pas ete publie (avis : {avis})")
    propres = ("hz_retirees", "hz_retirees_absentes", "hz_nb_en_jeu", "hz_total_degats", "hz_avis")
    reste = {k: v for k, v in attendu.items() if k not in propres}
    copie = dict(aides); copie["cas"] = dict(cas); copie["cas"]["attendu"] = reste
    ok, message = etat_attendu(monde, copie)
    if not ok:
        soucis.append(message)
    if soucis:
        return False, " ; ".join(soucis)
    return True, message
'''
