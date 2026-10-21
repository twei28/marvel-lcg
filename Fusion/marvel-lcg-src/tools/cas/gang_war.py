# Cas test_capacites des TROIS COMPLOTS et de Gunrunner du scenario 1 « The Big Apple » (pu001a-pu004), PU-7. Prefixe `[gang]`.
# Deux montages : (1) la VRAIE mise en place (`scenario: the_big_apple`) pour Gang War 1A et les passages d'etape ; les 3 CAPO sont tires au
# hasard, donc les mesures sont independantes de leur identite ; (2) un montage DETERMINISTE (scenario `rhino`, CAPO pu055a Diamondback mis
# en jeu) pour les interruptions de 1B / 2B.
SC = "the_big_apple"
FORME_HEROS = "Puzzle.ChangeForm('01001b')"
RIEN = ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01105', '01105', '01105')"]
LIEUX = ["pu030", "pu031", "pu032", "pu033", "pu034", "pu035", "pu036", "pu037", "pu038"]


def _g(nom, pourquoi, scenario, mise, declencher, attendu, **cle):
    cas = {"nom": "[gang] " + nom, "pourquoi": pourquoi, "scenario": scenario, "heros": "spider_man",
           "mise_en_place": mise, "declencher": declencher, "verifier": "gang_etat", "attendu": attendu}
    cas.update(cle)
    return cas


def _d(nom, pourquoi, mise, declencher, attendu, **cle):
    """Montage deterministe : Rhino retire, le complot teste en jeu, Diamondback (13 PV) en jeu."""
    cle.setdefault("main_exclusive", ["01088"])   # sans cela le pilote joue Great Responsibility (01061) et annule la menace
    return _g(nom, pourquoi, "rhino", [*RIEN, FORME_HEROS, *mise], declencher, attendu, **cle)


CAS = [
    # ------------------------------------------------------------------------------------------------ pu001a : la mise en place
    _g("pu001a mise en place reelle : 3 CAPO en jeu, UN par zone de rangee, 5 dans le deck de mechants",
       "« Place one chosen CAPO villain next to each row » : trois tires au hasard, les cinq autres restent de cote",
       SC, [], [], {"vilains": 3, "deck_de_mechants": 5, "capos_par_zone": [[2, 1], [3, 1], [4, 1]]}),
    _g("pu001a mise en place reelle : les 9 lieux, The City et Never Sleeps sont en jeu ; le complot est 1B",
       "« Place the 9 locations ... Reveal The City and Never Sleeps environments »",
       SC, [], [], {"en_jeu": [*LIEUX, "pu005", "pu006", "pu001b"]}),
    _g("pu001a mise en place reelle : le joueur est a Midtown (case (1,1)), dans la zone de la rangee 1 (zone 3) ; 5 zones en tout",
       "R1 : tous les joueurs partent de Midtown ; indices : 0 = depart, 1 = commune, 2 a 4 = rangees",
       SC, [], [], {"case_de": [[0, [1, 1]]], "zone_de": [["01001b", 3]], "zones": 5}),
    _g("pu001a mise en place reelle : le joueur a revele UNE piste (dans son aire), il en reste 8 dans le paquet LEADS",
       "« Create the 9-card LEADS deck ... Each player reveals a card from the LEADS deck »",
       SC, [], [], {"pistes_chez_les_joueurs": 1, "paquet_pistes": 8}),
    _g("pu001a mise en place reelle : le complot principal est dans la zone COMMUNE (vu depuis toutes les zones)",
       "les manigances n'appartiennent a aucun territoire", SC, [], [], {"zone_de": [["pu001b", 1]], "schemes_vus": [[2, 1], [3, 1], [4, 1]]}),
    # ------------------------------------------------------------------------------------------------ pu001b : interruption et passage
    _d("pu001b Forced Interrupt : un CAPO (13 PV) subit 13 degats -> il n'est PAS vaincu, ses PV sont remis, 5 menaces retirees (8 -> 3)",
       "« When a villain would be defeated, instead reset their hit points and remove 5 threat from here »",
       ["Puzzle.PutIntoPlay('pu001b')", "Puzzle.PutIntoPlay('pu055a')"], ["Puzzle.SetThreat('pu001b', 8)", "Puzzle.Damage('pu055a', 13)"],
       {"en_jeu": ["pu055a"], "degats": [["pu055a", 0]], "menace": [["pu001b", 3]]}),
    _d("pu001b Forced Interrupt, TEMOIN : 12 degats (13 PV) -> pas vaincu, PAS de reinitialisation ni de menace retiree (8)",
       "l'interruption ne joue qu'a la defaite", ["Puzzle.PutIntoPlay('pu001b')", "Puzzle.PutIntoPlay('pu055a')"],
       ["Puzzle.SetThreat('pu001b', 8)", "Puzzle.Damage('pu055a', 12)"], {"en_jeu": ["pu055a"], "degats": [["pu055a", 12]], "menace": [["pu001b", 8]]}),
    _d("pu001b Forced Interrupt : seulement 3 menaces (< 5) -> la menace tombe a 0, jamais sous 0", "« remove 5 threat » : au mieux ce qu'il y a",
       ["Puzzle.PutIntoPlay('pu001b')", "Puzzle.PutIntoPlay('pu055a')"], ["Puzzle.SetThreat('pu001b', 3)", "Puzzle.Damage('pu055a', 13)"],
       {"en_jeu": ["pu055a"], "menace": [["pu001b", 0]]}),
    _g("pu001b Forced Response : UNE piste en victoire (1 joueur : seuil 2) -> on n'avance PAS",
       "« if there are 2[per hero] LEAD cards there » : 2 x 1 joueur", SC, [], ["Puzzle.AddToVictoryDisplay('pu041')"],
       {"en_jeu": ["pu001b"], "hors_jeu": ["pu002b"]}),
    _g("pu001b Forced Response : DEUX pistes en victoire -> le complot avance a 2A (2A se revele puis se retourne sur 2B)",
       "« advance to stage 2A »", SC, [], ["Puzzle.AddToVictoryDisplay('pu041')", "Puzzle.AddToVictoryDisplay('pu042')"],
       {"en_jeu": ["pu002b"], "hors_jeu": ["pu001b"]}),
    # ------------------------------------------------------------------------------------------------ pu002b : quell et passage
    _d("pu002b Forced Interrupt : un CAPO subit 13 degats -> PV remis, 1 compteur quell sur lui, 2 menaces de depart intactes",
       "« instead reset their hit points and place 1 quell counter on them »",
       ["Puzzle.PutIntoPlay('pu002b')", "Puzzle.PutIntoPlay('pu055a')"], ["Puzzle.Damage('pu055a', 13)"],
       {"en_jeu": ["pu055a"], "degats": [["pu055a", 0]], "compteurs": [["pu055a", "quell", 1]]}),
    _g("pu002b Forced Response : les 3 CAPO ont 1 quell a la fin de la phase des joueurs -> avance a 3A (3B apres retournement)",
       "« if each villain has at least 1 quell counter, advance to stage 3A » (vraie mise en place, 3 CAPO tires au hasard)",
       SC, [], ["Puzzle.AdvanceMainScheme(1)", "Puzzle.PlaceCountersOnVillains('quell', 1)", "Puzzle.EndPlayerPhase()"],
       {"en_jeu": ["pu003b"], "hors_jeu": ["pu002b"]}),
    _g("pu002b Forced Response, TEMOIN : 2 CAPO sur 3 ont un quell -> on n'avance pas",
       "« EACH villain » : il suffit qu'un seul n'en ait pas", SC,
       [], ["Puzzle.AdvanceMainScheme(1)", "Puzzle.PlaceCountersOnVillains('quell', 1, skip=1)", "Puzzle.EndPlayerPhase()"],
       {"en_jeu": ["pu002b"], "hors_jeu": ["pu003b"]}),
    _g("pu002a When Revealed : une carte de rencontre est DONNEE a chaque joueur (2 joueurs : 2 cartes)",
       "« Deal each player an encounter card » : chacun des joueurs, pas le seul premier ; deck de rencontre fixe (01105 x2)",
       SC, ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01105', '01105', '01105')"], ["Puzzle.AdvanceMainScheme(1)"],
       {"cartes_donnees": 2}, heros2="spider_man"),
    _g("pu002a When Revealed : 1 joueur -> 1 carte donnee", "idem, 1 joueur", SC,
       ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01105', '01105', '01105')"], ["Puzzle.AdvanceMainScheme(1)"], {"cartes_donnees": 1}),
    # ------------------------------------------------------------------------------------------------ pu003a : l'entrepot
    _g("pu003a When Revealed : Gunrunner est en jeu, il reste UN seul CAPO, les 9 lieux sont de cote, le joueur est dans la zone du CAPO",
       "« Set all locations aside. Reveal a random CAPO villain ... reveal Gunrunner, and attach it to them. Set all other CAPOS aside. »",
       SC, [], ["Puzzle.AdvanceMainScheme(1)", "Puzzle.AdvanceMainScheme(1)"],
       {"vilains": 1, "en_jeu": ["pu004", "pu003b"], "hors_jeu": LIEUX, "capo_avec_gunrunner": True}),
    # ------------------------------------------------------------------------------------------------ pu004 : Gunrunner
    _g("pu004 Gunrunner : le CAPO porteur a +7 PV par joueur, SCH +1, ATQ +1 et Steady (3A revelee, 1 joueur)",
       "« gets +7[per hero] hit points » ; icones SCH +1 / ATK +1 ; « gains steady »",
       SC, [], ["Puzzle.AdvanceMainScheme(1)", "Puzzle.AdvanceMainScheme(1)"], {"capo_avec_gunrunner": True, "gunrunner_stats": 1}),
    _g("pu004 Gunrunner : 2 joueurs -> +14 PV (7 x 2)", "« +7 PAR joueur »",
       SC, [], ["Puzzle.AdvanceMainScheme(1)", "Puzzle.AdvanceMainScheme(1)"], {"capo_avec_gunrunner": True, "gunrunner_stats": 2}, heros2="spider_man"),
    _g("pu004 Gunrunner : le CAPO porteur est vaincu (la 1re vague de degats est absorbee par sa carte Tough) -> les joueurs GAGNENT", "« When attached villain is defeated, the players win the game »",
       SC, [], ["Puzzle.AdvanceMainScheme(1)", "Puzzle.AdvanceMainScheme(1)", "Puzzle.DamageAllVillains(100)", "Puzzle.DamageAllVillains(100)"], {"partie": "gagnee"}),
    _g("pu004 TEMOIN : un CAPO vaincu AVANT 3A (Gang War reinitialise ses PV) -> la partie continue", "pas de Gunrunner, pas de victoire",
       SC, [], ["Puzzle.DamageAllVillains(100)"], {"partie": "en_cours"}),
]

VERIFICATIONS = r'''
def gang_etat(monde, aides):
    """Cles propres : `vilains` (nombre de CAPO en jeu, toutes zones), `deck_de_mechants`, `capos_par_zone` [[zone, n]], `pistes_chez_les_joueurs`,
    `paquet_pistes`, `capo_avec_gunrunner` ; le reste va a `big_etat` (ville + etat_attendu)."""
    from game.operate.villains import Villains
    from game.operate.worlds import Worlds
    cas = aides["cas"]
    attendu = cas.get("attendu") or {}
    propres = ("partie", "cartes_donnees", "gunrunner_stats", "vilains", "deck_de_mechants", "capos_par_zone", "pistes_chez_les_joueurs", "paquet_pistes", "capo_avec_gunrunner")
    soucis = []
    capos = [v for v in Worlds.GetAllVillains(monde) if v.HasTrait("CAPO")]
    if "vilains" in attendu and len(capos) != attendu["vilains"]:
        soucis.append(f"{len(capos)} CAPO en jeu (attendu {attendu['vilains']})")
    if "deck_de_mechants" in attendu:
        paquet = getattr(monde.GetScenario(), "deck_de_mechants", None)
        n = paquet.GetSize() if paquet is not None else 0
        if n != attendu["deck_de_mechants"]:
            soucis.append(f"deck de mechants = {n} (attendu {attendu['deck_de_mechants']})")
    for z, n in attendu.get("capos_par_zone") or []:
        vus = len([v for v in capos if v.card.GetGameArea() is monde.game_areas[z]])
        if vus != n:
            soucis.append(f"{vus} CAPO dans la zone {z} (attendu {n})")
    if "pistes_chez_les_joueurs" in attendu:
        n = sum(1 for j in monde.const_players for f in j.obligations_area.Get() if f.HasTrait("LEAD"))
        if n != attendu["pistes_chez_les_joueurs"]:
            soucis.append(f"{n} piste(s) chez les joueurs (attendu {attendu['pistes_chez_les_joueurs']})")
    if "paquet_pistes" in attendu:
        paquet = monde.scenario_decks["LeadsDeck"]
        n = paquet.deck.GetSize() if paquet.initialize else 0
        if n != attendu["paquet_pistes"]:
            soucis.append(f"paquet LEADS = {n} (attendu {attendu['paquet_pistes']})")
    if "partie" in attendu:
        go = monde.game_over
        etat = "en_cours" if not monde.is_game_over else ("gagnee" if go.players_won else "perdue")
        if etat != attendu["partie"]:
            soucis.append(f"partie {etat} (attendu {attendu['partie']})")
    if "cartes_donnees" in attendu:
        n = sum(len(j.dealt_encounter_cards.Get()) for j in monde.const_players)
        if n != attendu["cartes_donnees"]:
            soucis.append(f"{n} carte(s) donnee(s) aux joueurs (attendu {attendu['cartes_donnees']})")
    if attendu.get("gunrunner_stats"):
        porteur = aides["par_id"](monde, "pu004")
        hote = getattr(porteur, "bind_face", None) if porteur is not None else None
        if hote is not None:
            joueurs = attendu["gunrunner_stats"]
            if hote.max_health != hote.printed_health + 7 * joueurs:
                soucis.append(f"PV max {hote.max_health} (imprime {hote.printed_health} + {7 * joueurs} attendu)")
            if hote.attack != hote.printed_attack + 1 or hote.scheme != hote.printed_scheme + 1:
                soucis.append(f"ATQ {hote.attack}/SCH {hote.scheme} (imprimes {hote.printed_attack}/{hote.printed_scheme}, +1 attendu)")
            if not hote.IsSteady():
                soucis.append("le CAPO porteur n'est pas Steady")
    if attendu.get("capo_avec_gunrunner"):
        porteur = aides["par_id"](monde, "pu004")
        hote = getattr(porteur, "bind_face", None) if porteur is not None else None
        if hote is None or not hote.HasTrait("CAPO"):
            soucis.append("Gunrunner n'est attache a aucun CAPO")
        elif not hote.IsTough():
            soucis.append("le CAPO porteur n'a pas de carte Tough")
        else:
            zone = hote.card.GetGameArea()
            for j in monde.const_players:
                if j.GetIdentity().card.GetGameArea() is not zone:
                    soucis.append("un joueur n'est pas dans la zone du CAPO porteur")
    cas["attendu"] = {k: v for k, v in attendu.items() if k not in propres}
    try:
        if cas["attendu"]:
            ok, msg = big_etat(monde, aides)
            if not ok:
                soucis.append(msg)
    finally:
        cas["attendu"] = attendu
    return (False, " ; ".join(soucis)) if soucis else (True, "complot conforme")
'''
