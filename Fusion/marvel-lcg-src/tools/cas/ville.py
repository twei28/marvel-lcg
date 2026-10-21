# Cas test_capacites du BANC DE ZONES (PU-5, spec docs/rapports/spec-ville-m1-m2-2026-10-21.md, etape 1). Prefixe `[ville]`.
# Aucune carte de la campagne : scenario Rhino du jeu de base, Spider-Man, des zones creees par le harnais. Chaque cas mesure ce que
# le moteur FAIT AUJOURD'HUI quand un joueur change de zone (ecarts G1-G5 de la spec).
FORME_HEROS = "Puzzle.ChangeForm('01001b')"
GRILLE = [["01088", "01089", "01092"], ["01093", "01090", "01094"], ["01095", "01091", "01096"]]  # cartes de reference (lieux du banc)
G = repr(GRILLE)
RIEN = ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01105', '01105', '01105')"]


def _z(nom, pourquoi, mise, declencher, attendu, **cle):
    cas = {"nom": "[ville] " + nom, "pourquoi": pourquoi, "scenario": "rhino", "heros": "spider_man",
           "mise_en_place": [*RIEN, FORME_HEROS, *mise], "declencher": declencher, "verifier": "ville_etat",
           "attendu": attendu, "main_exclusive": ["01088"]}
    cas.update(cle)
    return cas


CAS = [
    _z("zones : un joueur change de zone (sans zone commune) -> il emmene ses sbires, ne voit plus ni le complot ni le vilain",
       "BASELINE du moteur avant PU-5 : ecart G1/G6",
       ["Puzzle.PutIntoPlay('01103')"], ["Puzzle.CreateGameArea()", "Puzzle.MovePlayerToGameArea(1)"],
       {"zones": 2, "zone_de": [["01001a", 1], ["01103", 1], ["01094", 0]], "schemes_vus": [[0, 1], [1, 0]],
        "mechant_vu": [[0, "01094"], [1, None]]}),
    _z("zone COMMUNE : le complot principal passe dans la zone commune -> il est vu depuis la zone 0 ET depuis la zone 2",
       "spec G1 : « toutes les manigances ne font partie d'aucun territoire »",
       [], ["Puzzle.CreateCommonGameArea()", "Puzzle.MoveCardToGameArea('01097b', 1)", "Puzzle.CreateGameArea()", "Puzzle.MovePlayerToGameArea(2)"],
       {"zones": 3, "zone_de": [["01097b", 1], ["01001a", 2]], "schemes_vus": [[0, 1], [1, 1], [2, 1]]}),
    _z("zone COMMUNE : une manigance annexe (SWAT) en zone commune reagit a un sbire vaincu dans une autre zone (1 + 1 = 2 menaces)",
       "les capacites d'une carte de la zone commune se declenchent depuis toutes les zones (`check_game_area`)",
       ["Puzzle.PutIntoPlay('pu119')", "Puzzle.PutIntoPlay('01103')"],
       ["Puzzle.CreateCommonGameArea()", "Puzzle.MoveCardToGameArea('pu119', 1)", "Puzzle.CreateGameArea()", "Puzzle.MovePlayerToGameArea(2)",
        "Puzzle.Damage('01103', 3)"],
       {"zone_de": [["pu119", 1], ["01001a", 2]], "menace": [["pu119", 2]]}),
    _z("SANS zone commune, TEMOIN : la meme manigance reste dans la zone 0, le joueur en zone 1 ne la voit pas et elle ne reagit pas (1 menace)",
       "contre-cas : prouve que le garde ne change rien hors scenario de ville",
       ["Puzzle.PutIntoPlay('pu119')", "Puzzle.PutIntoPlay('01103')"],
       ["Puzzle.CreateGameArea()", "Puzzle.MovePlayerToGameArea(1)", "Puzzle.Damage('01103', 3)"],
       {"zone_de": [["pu119", 0], ["01001a", 1]], "menace": [["pu119", 1]]}),
    # ---------------------------------------------------------------- etape 3 : la grille et le deplacement
    _z("ville : tous les joueurs partent de la case (1,1) (Midtown) dans la zone de la ligne 1 (zone 3)",
       "R1 : « tous les joueurs commencent a Midtown »",
       [], ["Puzzle.InstallerVille(%s)" % G], {"case_de": [[0, [1, 1]]], "zone_de": [["01001a", 3]]}),
    _z("ville : deplacement VERTICAL (1,1) -> (0,1) : le joueur change de zone (ligne 0 = zone 2) et emmene son sbire engage",
       "R2 : orthogonal ; R4 : changer de ligne = changer de territoire ; G5 : les sbires suivent le joueur",
       ["Puzzle.PutIntoPlay('01103')"], ["Puzzle.InstallerVille(%s)" % G, "Puzzle.DeplacerDansLaVille((0, 1))"],
       {"case_de": [[0, [0, 1]]], "zone_de": [["01001a", 2], ["01103", 2]]}),
    _z("ville : deplacement HORIZONTAL (1,1) -> (1,2) : meme ligne, meme zone",
       "R2 ; une ligne = un territoire",
       [], ["Puzzle.InstallerVille(%s)" % G, "Puzzle.DeplacerDansLaVille((1, 2))"],
       {"case_de": [[0, [1, 2]]], "zone_de": [["01001a", 3]]}),
    _z("ville : deplacement en DIAGONALE refuse ((1,1) -> (0,0)) : la position et la zone ne bougent pas",
       "R2 : nord/sud ou est/ouest seulement",
       [], ["Puzzle.InstallerVille(%s)" % G, "Puzzle.DeplacerDansLaVille((0, 0))"],
       {"case_de": [[0, [1, 1]]], "zone_de": [["01001a", 3]]}),
    _z("ville : deplacement HORS GRILLE refuse (depuis (0,1) vers (-1,1)) et saut de deux cases refuse ((0,1) -> (2,1))",
       "R2", [], ["Puzzle.InstallerVille(%s, (0, 1))" % G, "Puzzle.DeplacerDansLaVille((-1, 1))", "Puzzle.DeplacerDansLaVille((2, 1))"],
       {"case_de": [[0, [0, 1]]]}),
    _z("ville : deux deplacements d'affilee ((1,1) -> (0,1) -> (0,2)) puis retour ((0,1) -> (1,1)) : le joueur change de zone plusieurs fois",
       "G4 : le deplacement est repetable (Kang ne le permettait qu'une fois)",
       [], ["Puzzle.InstallerVille(%s)" % G, "Puzzle.DeplacerDansLaVille((0, 1))", "Puzzle.DeplacerDansLaVille((0, 2))",
            "Puzzle.DeplacerDansLaVille((0, 1))", "Puzzle.DeplacerDansLaVille((1, 1))"],
       {"case_de": [[0, [1, 1]]], "zone_de": [["01001a", 3]]}),
    _z("ville : le lieu (1,1) est occupe par le joueur, le lieu (0,0) est inoccupe",
       "FAQ : « lieu inoccupe = sans aucun joueur present »",
       [], ["Puzzle.InstallerVille(%s)" % G], {"occupe": [[[1, 1], True], [[0, 0], False]]}),
]

VERIFICATIONS = r'''
def ville_etat(monde, aides):
    """Mesures du banc de zones : `zones` (nombre), `zone_de` [[card_id, indice]], `schemes_vus` [[zone, nombre de complots
    principaux vus]], `mechant_vu` [[zone, card_id|None]]."""
    from game.operate.worlds import Worlds
    attendu = aides["cas"].get("attendu") or {}
    soucis = []
    reste = {k: v for k, v in attendu.items() if k in ("menace",)}
    if reste:
        aides["cas"]["attendu"] = reste
        ok, msg = etat_attendu(monde, aides)
        aides["cas"]["attendu"] = attendu
        if not ok:
            soucis.append(msg)
    zones = monde.game_areas
    if "zones" in attendu and len(zones) != attendu["zones"]:
        soucis.append(f"zones = {len(zones)} (attendu {attendu['zones']})")
    for card_id, indice in attendu.get("zone_de") or []:
        face = aides["par_id"](monde, card_id)
        if face is None:
            soucis.append(f"{card_id} introuvable")
            continue
        z = zones.index(face.card.GetGameArea()) if face.card.GetGameArea() in zones else -1
        if z != indice:
            soucis.append(f"{card_id} en zone {z} (attendu {indice})")
    for z, n in attendu.get("schemes_vus") or []:
        vus = len(Worlds.GetMainSchemes(zones[z]))
        if vus != n:
            soucis.append(f"complots principaux vus depuis la zone {z} = {vus} (attendu {n})")
    from game.operate.ville import Ville
    for indice, case in attendu.get("case_de") or []:
        vu = Ville.Case(monde, monde.const_players[indice])
        if list(vu or []) != list(case):
            soucis.append(f"joueur {indice} en case {vu} (attendu {tuple(case)})")
    for case, voulu in attendu.get("occupe") or []:
        lieu = Ville.Etat(monde).cases[tuple(case)]
        occupe = not Ville.Inoccupe(monde, lieu)
        if occupe != voulu:
            soucis.append(f"lieu {tuple(case)} occupe = {occupe} (attendu {voulu})")
    for z, cid in attendu.get("mechant_vu") or []:
        v = Worlds.FindVillainByGameArea(zones[z])
        vu = v.paper.card_id if v is not None else None
        if vu != cid:
            soucis.append(f"mechant vu depuis la zone {z} = {vu} (attendu {cid})")
    return (False, " ; ".join(soucis)) if soucis else (True, "banc de zones conforme")
'''
