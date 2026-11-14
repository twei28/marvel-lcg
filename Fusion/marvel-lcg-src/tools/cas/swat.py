# Cas test_capacites du set SWAT TEAM (pack MC×DC 2026), PU-3. Prefixe `[swat]`.
# Montage : scenario `protection_racket_jigsaw`, Spider-Man en HEROS (sauf mention), deck rencontre remplace. SWAT (pu119) mis en jeu
# par `Puzzle.PutIntoPlay` : menace de depart 1.
SC = "protection_racket_jigsaw"
HEROS = "Puzzle.ChangeForm('01001b')"
ALTER_EGO = "Puzzle.ChangeForm('01001a')"
SANS_DEFENSE = {"passer_sur_option": "Defense"}


def _w(nom, pourquoi, mise, declencher, attendu, **cle):
    deck = cle.pop("deck", ["01105"] * 4)
    cas = {"nom": "[swat] " + nom, "pourquoi": pourquoi, "scenario": cle.pop("scenario", SC), "heros": "spider_man",
           "mise_en_place": ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck(%s)" % ", ".join(repr(x) for x in deck), HEROS, *mise],
           "declencher": declencher, "verifier": cle.pop("verifier", "swat_etat"), "attendu": attendu,
           "main_exclusive": cle.pop("main_exclusive", ["01088"])}
    cas.update(cle)
    return cas


SW = ["Puzzle.PutIntoPlay('pu119')"]
CAS = [
    _w("pu119 SWAT : menace de depart 1 (fixe)", "StartingThreat 1", SW, [], {"menace": [["pu119", 1]]}),
    _w("pu119 Forced Response : un sbire non POLICE (Shocker) abattu -> 1 menace de plus (1 + 1 = 2)",
       "« After an enemy is defeated, place 1 threat here »", [*SW, "Puzzle.PutIntoPlay('01103')"], ["Puzzle.Damage('01103', 3)"],
       {"menace": [["pu119", 2]]}),
    _w("pu119 un sbire POLICE (Riot Police) abattu -> 3 menaces, total 4 -> tout retire, 1 compteur wanted, SWAT reste en jeu",
       "« 3 threat instead if it had the POLICE trait. Then, if there is 4+ threat here, remove all threat and place 1 wanted counter »",
       [*SW, "Puzzle.PutIntoPlay('pu121')"], ["Puzzle.Damage('pu121', 6)", "Puzzle.Damage('pu121', 6)"],
       {"menace": [["pu119", 0]], "compteurs": [["pu119", "wanted", 1]], "en_jeu": ["pu119"]}),
    _w("pu119 : 5 compteurs wanted -> les joueurs perdent",
       "« If there are 5 or more wanted counters here, the players lose the game »",
       [*SW, "Puzzle.PlaceCounters('pu119', 'wanted', 4)", "Puzzle.PutIntoPlay('pu121')"], ["Puzzle.Damage('pu121', 6)", "Puzzle.Damage('pu121', 6)"],
       {"defaite": True}),
    _w("pu119 : 4 compteurs seulement -> pas de defaite", "temoin",
       [*SW, "Puzzle.PlaceCounters('pu119', 'wanted', 3)", "Puzzle.PutIntoPlay('pu121')"], ["Puzzle.Damage('pu121', 6)", "Puzzle.Damage('pu121', 6)"],
       {"defaite": False, "compteurs": [["pu119", "wanted", 4]]}),
    _w("pu119 : les joueurs ne peuvent pas contrer SWAT (Spider-Man contre : aucune menace retiree)",
       "« Players cannot thwart this scheme »", SW, ["Puzzle.PlaceThreat('pu119', 2)", "Puzzle.Thwart('01001a')"],
       {"menace": [["pu119", 3]]}, cibles=["pu119"]),
    # ---- redirections de menace (alter ego : les sbires manigancent)
    _w("pu120 Cole North manigance (SCH 2) : la menace va sur SWAT (1 + 2 = 3), pas sur le complot",
       "« When Cole North schemes, place that threat on SWAT, if able »",
       [ALTER_EGO, *SW, "Puzzle.PutIntoPlay('pu120')"], ["Puzzle.Scheme('pu120')"], {"menace": [["pu119", 3], ["60134b", 0]]}),
    _w("pu120 TEMOIN : sans SWAT en jeu, la menace va au complot (« if able »)",
       "contre-cas", [ALTER_EGO, "Puzzle.PutIntoPlay('pu120')"], ["Puzzle.Scheme('pu120')"], {"menace": [["60134b", 2]]}),
    _w("pu121 Riot Police manigance (SCH 1★ = 1) : menace sur SWAT (1 + 1 = 2)",
       "« When Riot Police schemes, place that threat on SWAT »",
       [ALTER_EGO, *SW, "Puzzle.PutIntoPlay('pu121')"], ["Puzzle.Scheme('pu121')"], {"menace": [["pu119", 2]]}),
    _w("pu123 Tactical Sniper manigance (SCH 1) : menace sur SWAT",
       "« When Tactical Sniper schemes, place that threat on SWAT »",
       [ALTER_EGO, *SW, "Puzzle.PutIntoPlay('pu123')"], ["Puzzle.Scheme('pu123')"], {"menace": [["pu119", 2]]}),
    # ---- attaques remplacees
    _w("pu120 Cole North va attaquer, moins de 3 wanted -> a la place 2 menaces retirees de la principale (1 + 3 = 4 -> 2), aucun degat",
       "« remove 2 threat from the main scheme instead »",
       [*SW, "Puzzle.PutIntoPlay('pu120')"], ["Puzzle.PlaceThreat('60121b', 3)", "Puzzle.Attack('pu120')"],
       {"menace": [["60121b", 2]], "degats_identite": 0}, scenario="art_museum_heist_jigsaw"),
    _w("pu120 TEMOIN : 3 wanted -> il attaque normalement (2 degats), la principale ne bouge pas",
       "« if there are fewer than 3 wanted counters »",
       [*SW, "Puzzle.PlaceCounters('pu119', 'wanted', 3)", "Puzzle.PutIntoPlay('pu120')"],
       ["Puzzle.PlaceThreat('60121b', 3)", "Puzzle.Attack('pu120')"], {"menace": [["60121b", 4]], "degats_identite": 2}, scenario="art_museum_heist_jigsaw", **SANS_DEFENSE),
    _w("pu123 Tactical Sniper va attaquer, moins de 3 wanted -> il attaque l'ennemi non POLICE aux PV les plus bas (Jigsaw : 3 degats), le heros indemne",
       "« it attacks the enemy with the fewest remaining hit points without the POLICE trait instead »",
       [*SW, "Puzzle.PutIntoPlay('pu123')"], ["Puzzle.Attack('pu123')"], {"degats": [["pu056a", 3]], "degats_identite": 0}),
    _w("pu123 TEMOIN : 3 wanted -> il attaque le heros (3 degats)",
       "contre-cas", [*SW, "Puzzle.PlaceCounters('pu119', 'wanted', 3)", "Puzzle.PutIntoPlay('pu123')"], ["Puzzle.Attack('pu123')"],
       {"degats": [["pu056a", 0]], "degats_identite": 3}, **SANS_DEFENSE),
    # ---- Riot Police : action de heros
    _w("pu121 Hero Action : 1 ressource + defausser un allie -> Riot Police defaussee, 2 menaces retirees de SWAT (4 -> 2)",
       "« Spend 1 resource of any type and discard an ally you control → discard Riot Police and remove 2 threat from SWAT »",
       [*SW, "Puzzle.PutIntoPlay('pu121')", "Puzzle.PutIntoPlay('01075', under_control=True)"],
       ["Puzzle.PlaceThreat('pu119', 3)", "Puzzle.Action('pu121', 'HeroAction')"], {"hors_jeu": ["pu121", "01075"], "menace": [["pu119", 2]]},
       main_exclusive=["01089", "01090"], payer_avec=["01089", "01090"], payer_tout=True),
]

VERIFICATIONS = r'''
def swat_etat(monde, aides):
    """etat_attendu + `defaite` (les joueurs ont perdu)."""
    attendu = aides["cas"].get("attendu") or {}
    inconnues = sorted(set(attendu) - set(CLES_ETAT_ATTENDU) - {"defaite"})
    if inconnues:
        return False, f"cle(s) attendu INCONNUE(S) de swat_etat : {inconnues}"
    reste = {k: v for k, v in attendu.items() if k != "defaite"}
    aides["cas"]["attendu"] = reste
    ok, message = etat_attendu(monde, aides)
    aides["cas"]["attendu"] = attendu
    soucis = [] if ok else [message]
    if "defaite" in attendu:
        perdu = bool(monde.is_game_over) and not monde.game_over.players_won
        if perdu != attendu["defaite"]:
            soucis.append(f"defaite = {perdu} (attendu {attendu['defaite']})")
    return (False, " ; ".join(soucis)) if soucis else (True, "etat SWAT conforme")
'''
