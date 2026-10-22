# Cas test_capacites de la CAMPAGNE « La ville ne dort jamais », combat 1 (pu140 Big Apple Gang War!, pu141 Seized Tech Crates, et les deux
# ecritures du carnet : stade 2A de pu002a et releve de fin de partie de `punisher_mcdc_2026/campaign.py`). Prefixe `[camp]`.
# Deux montages : (1) la VRAIE mise en place (`scenario: the_big_apple`, `campagne: True`) pour la mise en jeu de pu140 et le carnet SORTANT
# (relu dans `campaign_log_last_file`, comme `fnefin_carnet_sortant`) ; (2) `rhino` pour pu141 (Spider-Man, main reduite a UNE carte).
# ⚠ `Puzzle.SendGameWouldBegin()` : le Setup de pu141 (`AfterGameSetup`) part une fois, AVANT le montage d'un cas : on le renvoie a la main.
SC = "the_big_apple"
FORME_HEROS = "Puzzle.ChangeForm('01001b')"
RIEN = ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01105', '01105', '01105')"]
DEUX_PISTES = ["Puzzle.AddToVictoryDisplay('pu041')", "Puzzle.AddToVictoryDisplay('pu042')"]   # pu041 = piste 3 (Upper East Side), pu042 = piste 4 (West Village)
GUNRUNNER = ["Puzzle.AdvanceMainScheme(1)", "Puzzle.AdvanceMainScheme(1)"]                      # 1B -> 2A -> 3A (Gunrunner attache a un CAPO)


def _c(nom, pourquoi, mise, declencher, attendu, **cle):
    cas = {"nom": "[camp] " + nom, "pourquoi": pourquoi, "scenario": cle.pop("scenario", SC), "heros": "spider_man",
           "mise_en_place": mise, "declencher": declencher, "verifier": cle.pop("verifier", "camp_etat"), "attendu": attendu,
           "main_exclusive": cle.pop("main_exclusive", ["01088"])}
    cas.update(cle)
    return cas


def _caisses(nom, pourquoi, mise, declencher, attendu, carnet=None, **cle):
    """pu141 : `rhino`, Spider-Man, la carte en jeu SOUS LE CONTROLE du premier joueur (`under_control`)."""
    cle.setdefault("carnet", carnet if carnet is not None else {"Player 1 Identity": "Spider-Man"})
    return _c(nom, pourquoi, [*RIEN, FORME_HEROS, *mise], declencher, attendu, scenario="rhino", campagne=True, **cle)


CAS = [
    # ---------------------------------------------------------------------------------------------------------- pu140
    _c("pu140 mise en place (campagne) : l'environnement Big Apple Gang War! entre en jeu avec la ville",
       "Battle Setup / Setup : `CampaignSetup()` de pu001a met pu140 en jeu (WhenCampaignSetup)", [], [],
       {"en_jeu": ["pu140", "pu005", "pu006", "pu001b"]}, campagne=True, verifier="camp_etat"),
    _c("pu140, TEMOIN : hors campagne (partie ordinaire de The Big Apple), l'environnement n'entre PAS en jeu", "WhenCampaignSetup ne part qu'en campagne",
       [], [], {"hors_jeu": ["pu140"], "en_jeu": ["pu005"]}),
    # ---------------------------------------------------------------------------------------------------------- pu002a : le lieu
    _c("pu002a (campagne) : 2 pistes en victoire (pu041 puis pu042) -> le carnet note le lieu de la DERNIERE : West Village",
       "« record the location where the final LEAD card was added to the victory display » : la derniere ajoutee, pas la premiere",
       [], [*DEUX_PISTES, "Puzzle.Win()"],
       {"carnet_cles": {"Final LEAD Location": "West Village"}}, campagne=True),
    _c("pu002a (campagne) : l'ordre inverse (pu042 puis pu041) -> Upper East Side (la derniere, quelle que soit la carte)",
       "TEMOIN de l'ordre : le lieu suit la derniere piste ajoutee", [], ["Puzzle.AddToVictoryDisplay('pu042')", "Puzzle.AddToVictoryDisplay('pu041')", "Puzzle.Win()"],
       {"carnet_cles": {"Final LEAD Location": "Upper East Side"}}, campagne=True),
    _c("pu002a, TEMOIN : hors campagne, 2A se revele sans rien ecrire au carnet (le magasin n'a pas la cle)",
       "« In campaign mode » seulement", [], DEUX_PISTES, {"store_sans": ["Final LEAD Location"], "en_jeu": ["pu002b"]}),
    # ---------------------------------------------------------------------------------------------------------- releve
    _c("Releve (campagne, victoire par Gunrunner) : environnement retourne, Caisses gagnees, Trafiquant d'armes = le CAPO porteur",
       "Victory de pu140 : « Flip this card and put Seized Tech Crates into play for battles 2 and 3 » + CAPO Trafiquant d'armes",
       [], [*GUNRUNNER, "Puzzle.DamageAllVillains(100)", "Puzzle.DamageAllVillains(100)"],
       {"partie": "gagnee", "carnet_cles": {"Big Apple Gang War!": "Flipped", "Seized Tech Crates": "1"}, "trafiquant_egal_porteur": True,
        "carnet_gagnee": True}, campagne=True),
    _c("Releve (campagne, victoire forcee AVANT 3A) : environnement retourne et Caisses gagnees, mais PAS de Trafiquant d'armes",
       "Gunrunner n'est pas en jeu : rien a noter pour lui", [], ["Puzzle.Win()"],
       {"carnet_cles": {"Big Apple Gang War!": "Flipped", "Seized Tech Crates": "1"}, "carnet_cles_absentes": ["Gunrunner"], "carnet_gagnee": True}, campagne=True),
    _c("Releve (campagne, DEFAITE) : rien n'est coche (ni environnement, ni Caisses, ni Trafiquant) ; les PV restants restent",
       "« Defaite : on reinitialise le scenario et on reessaie sans penalite »", [], [*GUNRUNNER, "Puzzle.Lose()"],
       {"carnet_cles_absentes": ["Big Apple Gang War!", "Seized Tech Crates", "Gunrunner"], "carnet_cles_presentes": ["Player 1 Remaining hit points"],
        "carnet_gagnee": False}, campagne=True),
    _c("Releve : l'estampille du carnet est l'id du scenario de la campagne (the_big_apple)", "le panneau ignore tout releve dont l'estampille differe",
       [], ["Puzzle.Win()"], {"carnet_scenario": "the_big_apple"}, campagne=True),
    # ---------------------------------------------------------------------------------------------------------- pu141 : Setup
    _caisses("pu141 Setup : le seul joueur etait dans la partie precedente (carnet : Spider-Man) -> 1 compteur",
             "« Place 1 counter here, plus 1 more for each player who did not play the last game together »",
             ["Puzzle.PutIntoPlay('pu141', under_control=True)"], ["Puzzle.SendGameWouldBegin()"], {"compteurs": [["pu141", "counter", 1]]}),
    _caisses("pu141 Setup : un 2e joueur (Iron Man) n'etait PAS dans la partie precedente -> 2 compteurs",
             "« plus 1 more for each player who did not play the last game together » : un heros absent du carnet",
             ["Puzzle.PutIntoPlay('pu141', under_control=True)"], ["Puzzle.SendGameWouldBegin()"], {"compteurs": [["pu141", "counter", 2]]},
             heros2="iron_man"),
    _caisses("pu141 Setup : DEUX joueurs, tous deux dans la partie precedente (carnet : Spider-Man x2) -> 1 compteur (temoin)",
             "personne de nouveau : seulement le compteur de base",
             ["Puzzle.PutIntoPlay('pu141', under_control=True)"], ["Puzzle.SendGameWouldBegin()"], {"compteurs": [["pu141", "counter", 1]]},
             heros2="spider_man", carnet={"Player 1 Identity": "Spider-Man", "Player 2 Identity": "Spider-Man"}),
    _caisses("pu141 Setup : aucun carnet de la partie precedente -> 1 compteur (on ne sait pas qui est nouveau)",
             "decision documentee dans le script : sans carnet, aucun joueur en plus",
             ["Puzzle.PutIntoPlay('pu141', under_control=True)"], ["Puzzle.SendGameWouldBegin()"], {"compteurs": [["pu141", "counter", 1]]}, carnet={"Autre": "1"}),
    # ---------------------------------------------------------------------------------------------------------- pu141 : Action
    _caisses("pu141 Action, 1er choix : la carte suivante coute 1 de moins -> Aunt May (cout 1), seule carte de la main, est jouee sans ressource ; 1 compteur retire",
             "« Remove 1 counter -> reduce the cost of the next card you play this phase by 1 »",
             ["Puzzle.PutIntoPlay('pu141', under_control=True)", "Puzzle.PlaceCounters('pu141', 'counter', 2)"],
             ["Puzzle.Action('pu141', 'Action')"],
             {"compteurs": [["pu141", "counter", 1]], "en_jeu": ["01006"]}, main_exclusive=["01006"], jouer=["01006"],
             choisir_option="Reduce_the_cost_of_the_next_card_you_play_this_phase_by_1"),
    _caisses("pu141 Action, TEMOIN : sans l'Action, Aunt May (cout 1, rien pour le payer) reste en main",
             "preuve par insuffisance : sans reduction la carte est impayable",
             ["Puzzle.PutIntoPlay('pu141', under_control=True)", "Puzzle.PlaceCounters('pu141', 'counter', 2)"], [],
             {"compteurs": [["pu141", "counter", 2]], "en_main": ["01006"]}, main_exclusive=["01006"], jouer=["01006"]),
    _caisses("pu141 Action, 2e choix : chercher un soutien/une amelioration de cout <= 2 -> UNE carte de ce type rejoint la main ; 1 compteur retire",
             "« Find a support or upgrade with a cost of 2 or less and add it to your hand »",
             ["Puzzle.PutIntoPlay('pu141', under_control=True)", "Puzzle.PlaceCounters('pu141', 'counter', 2)"],
             ["Puzzle.Action('pu141', 'Action')"],
             {"compteurs": [["pu141", "counter", 1]], "main_ok": {"taille": 2, "types": ["Support", "Upgrade"], "cout_max": 2}},
             choisir_option="Find_a_support_or_upgrade_with_a_cost_of_2_or_less_and_add_it_to_your_hand"),
    _caisses("pu141 Action : sans compteur, l'Action n'est pas offerte (rien ne change)",
             "« Remove 1 counter -> » : le retrait est le cout",
             ["Puzzle.PutIntoPlay('pu141', under_control=True)"], [],
             {"compteurs": [["pu141", "counter", 0]]}, declencher_tolerant=["Puzzle.Action('pu141', 'Action')"]),
    _caisses("pu141 Action : limite UNE fois par joueur et par round -> la 2e Action du meme joueur n'est pas offerte (2 compteurs -> 1)",
             "« limit once per player per round »",
             ["Puzzle.PutIntoPlay('pu141', under_control=True)", "Puzzle.PlaceCounters('pu141', 'counter', 2)"],
             ["Puzzle.Action('pu141', 'Action')"],
             {"compteurs": [["pu141", "counter", 1]]}, main_exclusive=["01006"], declencher_tolerant=["Puzzle.Action('pu141', 'Action')"]),
    _caisses("pu141 Action : N'IMPORTE QUEL joueur peut la declencher, une fois chacun -> joueur 1 puis joueur 2 : 3 compteurs -> 1",
             "« any player may trigger this ability, limit once per player per round » : la limite est PAR JOUEUR",
             ["Puzzle.PutIntoPlay('pu141', under_control=True)", "Puzzle.PlaceCounters('pu141', 'counter', 3)"],
             ["Puzzle.Action('pu141', 'Action')", "Puzzle.Action('pu141', 'Action', siege=1)"],
             {"compteurs": [["pu141", "counter", 1]]}, heros2="spider_man", carnet={"Player 1 Identity": "Spider-Man", "Player 2 Identity": "Spider-Man"}),
    _caisses("pu141 Action, TEMOIN : le joueur 1 declenche deux fois, le joueur 2 une fois -> seulement 2 retraits (3 compteurs -> 1), pas 3",
             "la limite par joueur bloque la 2e Action du joueur 1 meme quand un autre joueur a joue entre-temps",
             ["Puzzle.PutIntoPlay('pu141', under_control=True)", "Puzzle.PlaceCounters('pu141', 'counter', 3)"],
             ["Puzzle.Action('pu141', 'Action')", "Puzzle.Action('pu141', 'Action', siege=1)"],
             {"compteurs": [["pu141", "counter", 1]]}, heros2="spider_man", carnet={"Player 1 Identity": "Spider-Man", "Player 2 Identity": "Spider-Man"},
             declencher_tolerant=["Puzzle.Action('pu141', 'Action')"]),
]

VERIFICATIONS = r'''
def camp_etat(monde, aides):
    """Cles propres : `partie`, `store_sans` [cles absentes du magasin], `carnet_*` (le carnet SORTANT ecrit a la fin de la partie, comme
    `fnefin_carnet_sortant`), `trafiquant_egal_porteur`, `main_ok` {taille, types, cout_max} ; le reste va a `etat_attendu`."""
    import json, os
    from engine.config import ConfigVariables
    cas = aides["cas"]
    attendu = cas.get("attendu") or {}
    propres = ("partie", "store_sans", "carnet_cles", "carnet_cles_absentes", "carnet_cles_presentes", "carnet_gagnee", "carnet_scenario",
               "trafiquant_egal_porteur", "main_ok")
    soucis = []
    if "partie" in attendu:
        etat = "en_cours" if not monde.is_game_over else ("gagnee" if monde.game_over.players_won else "perdue")
        if etat != attendu["partie"]:
            soucis.append(f"partie {etat} (attendu {attendu['partie']})")
    for cle in attendu.get("store_sans") or []:
        if monde.store.dic.get(cle):
            soucis.append(f"le magasin contient {cle} = {monde.store.dic.get(cle)!r}")
    if any(k.startswith("carnet_") or k == "trafiquant_egal_porteur" for k in attendu):
        chemin = ConfigVariables.File('campaign_log_last_file', './campaign_log_last.json').value
        if not os.path.exists(chemin):
            soucis.append(f"aucun carnet sortant ecrit ({chemin})")
        else:
            carnet = json.load(open(chemin, encoding="utf-8"))
            sug = carnet.get("suggestions") or {}
            if "carnet_gagnee" in attendu and bool(carnet.get("players_won")) != attendu["carnet_gagnee"]:
                soucis.append(f"players_won = {carnet.get('players_won')}")
            if "carnet_scenario" in attendu and carnet.get("scenario") != attendu["carnet_scenario"]:
                soucis.append(f"estampille = {carnet.get('scenario')!r}")
            for cle, valeur in (attendu.get("carnet_cles") or {}).items():
                if sug.get(cle) != valeur:
                    soucis.append(f"{cle} = {sug.get(cle)!r} (attendu {valeur!r})")
            for cle in attendu.get("carnet_cles_presentes") or []:
                if cle not in sug:
                    soucis.append(f"{cle} manque au carnet")
            for cle in attendu.get("carnet_cles_absentes") or []:
                if cle in sug:
                    soucis.append(f"{cle} = {sug[cle]!r} alors qu'il ne devrait pas y etre")
            if attendu.get("trafiquant_egal_porteur"):
                porteur = aides["par_id"](monde, "pu004")
                hote = getattr(porteur, "bind_face", None) if porteur is not None else None
                nom = hote.paper.name.lstrip("* ") if hote is not None else None
                if nom is None:
                    soucis.append("Gunrunner (pu004) n'est attache a aucun CAPO en fin de partie")
                elif sug.get("Gunrunner") != nom:
                    soucis.append(f"Gunrunner = {sug.get('Gunrunner')!r} (CAPO porteur : {nom!r})")
    if "main_ok" in attendu:
        voulu = attendu["main_ok"]
        main = monde.players[0].hand_cards.GetAll()
        if len(main) != voulu["taille"]:
            soucis.append(f"{len(main)} carte(s) en main (attendu {voulu['taille']}) : {[f.paper.card_id for f in main]}")
        nouvelles = [f for f in main if f.paper.card_id != "01088"]
        if len(nouvelles) != voulu["taille"] - 1:
            soucis.append(f"cartes trouvees = {[f.paper.card_id for f in nouvelles]}")
        for f in nouvelles:
            if type(f).__name__ not in voulu["types"]:
                soucis.append(f"{f.paper.card_id} est un {type(f).__name__} (attendu {voulu['types']})")
            cout = f.printed_cost.val
            if cout > voulu["cout_max"]:
                soucis.append(f"{f.paper.card_id} coute {cout} (> {voulu['cout_max']})")
    cas["attendu"] = {k: v for k, v in attendu.items() if k not in propres}
    try:
        if cas["attendu"]:
            ok, msg = etat_attendu(monde, aides)
            if not ok:
                soucis.append(msg)
    finally:
        cas["attendu"] = attendu
    return (False, " ; ".join(soucis)) if soucis else (True, "campagne conforme")
'''
