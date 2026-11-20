# Cas test_capacites PREDATOR, partie 4 : set nemesis ALTERNATIF (Dutch, Dillon, M134, Get To The..., Chopper). Deck de depart
# `predator_dutch` (meme heros, autre set nemesis mis de cote). Rappels de montage : voir predator.py et predator_c.py.
SC = "rhino"
HEROS = "Puzzle.ChangeToFace('pd001b', 'pd001a')"
SANS_BOOST = ["Puzzle.EmptyEncounterDeck()",
              "Puzzle.CreateEncounterDeck('01105', '01105', '01105', '01105', '01105', '01105', '01105', '01105')"]
COMPLOT = "01097b"
VILAIN = "01094"
CHOPPER = "pd026"
DUTCH = "pd027"
DILLON = "pd028"


def _c(nom, pourquoi, mise, declencher, attendu, **cle):
    if not cle.pop("avec_boost", False):
        mise = SANS_BOOST + list(mise)
    cas = {"nom": "[pd] " + nom, "pourquoi": pourquoi, "scenario": cle.pop("scenario", SC),
           "heros": cle.pop("heros", "predator_dutch"), "mise_en_place": mise, "declencher": declencher,
           "verifier": cle.pop("verifier", "pd_etat"), "attendu": attendu}
    cas.update(cle)
    return cas


CAS = [
    # ============================================================ pd026 Chopper
    _c("pd026 Chopper : revelee, 3 menaces (fixes) et l'icone Hazard",
       "StartingThreat 3 sans icone par joueur ; Hazard imprime",
       [HEROS], ["Puzzle.Reveal('pd026')"], {"menace": [[CHOPPER, 3]], "icones": [["Hazard", 1]]}, main_exclusive=["01090"]),
    _c("pd026 Chopper : « While there is no threat here, this scheme loses the hazard icon » -> a 0 menace, plus d'icone",
       "bonus -1 Hazard dynamique tant que la menace est nulle",
       [HEROS, "Puzzle.Reveal('pd026')"], [f"Puzzle.SetThreat('{CHOPPER}', 0)"], {"menace": [[CHOPPER, 0]], "icones": [["Hazard", 0]]},
       main_exclusive=["01090"]),
    _c("pd026 Chopper : la menace REVIENT -> l'icone Hazard aussi",
       "contre-cas : la perte n'est pas definitive",
       [HEROS, "Puzzle.Reveal('pd026')", f"Puzzle.SetThreat('{CHOPPER}', 0)"], [f"Puzzle.PlaceThreat('{CHOPPER}', 1)"],
       {"menace": [[CHOPPER, 1]], "icones": [["Hazard", 1]]}, main_exclusive=["01090"]),
    _c("pd026 Chopper : 8 menaces -> les joueurs PERDENT la partie",
       "« After threat is placed here, if there is at least 8 threat here, the players lose the game »",
       [HEROS, "Puzzle.Reveal('pd026')"], [f"Puzzle.PlaceThreat('{CHOPPER}', 5)"], {"menace": [[CHOPPER, 8]], "defaite": True},
       main_exclusive=["01090"]),
    _c("pd026 Chopper : 7 menaces -> la partie continue",
       "contre-cas : « at least 8 »",
       [HEROS, "Puzzle.Reveal('pd026')"], [f"Puzzle.PlaceThreat('{CHOPPER}', 4)"], {"menace": [[CHOPPER, 7]], "defaite": False},
       main_exclusive=["01090"]),
    _c("pd026 Chopper : Permanent -> un effet d'un AUTRE set ne peut pas la defausser",
       "« Permanent. »",
       [HEROS, "Puzzle.Reveal('pd026')"], [], {"en_jeu": [CHOPPER]}, main_exclusive=["01090"],
       declencher_tolerant=[f"Puzzle.Discard('{CHOPPER}')"]),
    # ============================================================ pd027 Dutch Schaefer
    _c("pd027 Dutch Schaefer : Toughness -> entre en jeu avec une carte Tough ; valeurs imprimees PV 6, ELITE SOLDIER",
       "« Toughness. » ; nombres texte <-> code (scan) : SCH 2 / ATK 2 / PV 6",
       [HEROS, f"Puzzle.PutIntoPlay('{DUTCH}')"], [],
       {"statuts": [[DUTCH, "Tough"]], "pv_max": [[DUTCH, 6]], "traits_de": [[DUTCH, "ELITE"], [DUTCH, "SOLDIER"]]},
       main_exclusive=["01090"]),
    _c("pd027 Dutch Schaefer : apres son activation, 1 menace sur CHAQUE manigance (complot principal 4 -> 5, Chopper 3 -> 4)",
       "« After Dutch Schaefer activates, place 1 threat on each scheme »",
       [HEROS, f"Puzzle.SetThreat('{COMPLOT}', 4)", "Puzzle.Reveal('pd026')", f"Puzzle.PutIntoPlay('{DUTCH}')"],
       [f"Puzzle.Attack('{DUTCH}')"], {"menace": [[COMPLOT, 5], [CHOPPER, 4]]}, main_exclusive=["01090"]),
    # ============================================================ pd028 Colonel Dillon
    _c("pd028 Colonel Dillon : une ATTAQUE contre le joueur -> 1 menace sur chaque manigance",
       "« After Colonel Dillon attacks you, place 1 threat on each scheme »",
       [HEROS, f"Puzzle.SetThreat('{COMPLOT}', 4)", "Puzzle.Reveal('pd026')", f"Puzzle.PutIntoPlay('{DILLON}')"],
       [f"Puzzle.Attack('{DILLON}')"], {"menace": [[COMPLOT, 5], [CHOPPER, 4]]}, main_exclusive=["01090"]),
    _c("pd028 Colonel Dillon : Teamwork (SOLDIER) -> avec Dutch deja en jeu il s'active a son arrivee (Predator se defend : incline)",
       "« Teamwork (SOLDIER) » natif : un autre sbire SOLDIER en jeu",
       [HEROS, f"Puzzle.PutIntoPlay('{DUTCH}')"], [f"Puzzle.PutIntoPlay('{DILLON}')"], {"exhausted": ["pd001a"]},
       main_exclusive=["01090"]),
    _c("pd028 Colonel Dillon : valeurs imprimees PV 4, SOLDIER, Patrol",
       "nombres texte <-> code (scan) : SCH 1 / ATK 2 / PV 4",
       [HEROS, f"Puzzle.PutIntoPlay('{DILLON}')"], [], {"pv_max": [[DILLON, 4]], "traits_de": [[DILLON, "SOLDIER"]]},
       main_exclusive=["01090"]),
    # ============================================================ pd029 M134 Minigun
    _c("pd029 M134 Minigun : Dutch en jeu -> l'arme s'attache a lui",
       "« Attach to Dutch Schaefer »",
       [HEROS, f"Puzzle.PutIntoPlay('{DUTCH}')"], ["Puzzle.Reveal('pd029')"], {"accroche_a": [["pd029", DUTCH]]},
       main_exclusive=["01090"]),
    _c("pd029 M134 Minigun : Dutch ABSENT (mis de cote) -> il est cherche, revele et l'arme s'attache a lui",
       "« If he is not in play, search the encounter deck and discard pile for him, reveal him and attach this card to him »",
       [HEROS], ["Puzzle.Reveal('pd029')"], {"accroche_a": [["pd029", DUTCH]], "en_jeu": [DUTCH]}, main_exclusive=["01090"]),
    _c("pd029 M134 Minigun : « +1 ATK » -> Dutch frappe a 3 (ATQ 2 + 1 - DEF 2 = 1 degat)",
       "bonus d'ATQ imprime (icone) pour l'hote",
       [HEROS, f"Puzzle.PutIntoPlay('{DUTCH}')", "Puzzle.Reveal('pd029')"], [f"Puzzle.Attack('{DUTCH}')"],
       {"degats_identite": 1}, main_exclusive=["01090"]),
    _c("pd029 M134 Minigun : apres l'attaque de Dutch contre le joueur -> 1 menace sur Chopper",
       "« After Dutch Schaefer attacks you, place 1 threat on the Chopper side scheme »",
       [HEROS, "Puzzle.Reveal('pd026')", f"Puzzle.PutIntoPlay('{DUTCH}')", "Puzzle.Reveal('pd029')"], [f"Puzzle.Attack('{DUTCH}')"],
       {"menace": [[CHOPPER, 5]]}, main_exclusive=["01090"]),
    # ============================================================ pd030 Get To The...
    _c("pd030 Get To The... : le vilain MANIGANCE et Chopper recoit 2 menaces (3 -> 5)",
       "« The villain schemes. Place 2 threat on The Chopper side scheme »",
       [HEROS, f"Puzzle.SetThreat('{COMPLOT}', 4)", "Puzzle.Reveal('pd026')"], ["Puzzle.Reveal('pd030')"],
       {"menace": [[CHOPPER, 5]], "menace_min": [[COMPLOT, 5]]}, main_exclusive=["01090"]),
    _c("pd030 Get To The... : SANS Chopper en jeu -> le vilain manigance, aucune menace ailleurs",
       "contre-cas : « the Chopper side scheme » absent",
       [HEROS, f"Puzzle.SetThreat('{COMPLOT}', 4)"], ["Puzzle.Reveal('pd030')"], {"menace_min": [[COMPLOT, 5]]},
       main_exclusive=["01090"]),
]

VERIFICATIONS = r'''
def pd_etat(monde, aides):
    """`defaite` (booleen) : la partie est perdue (pd026 Chopper) ; le reste par etat_attendu."""
    cas = aides["cas"]
    if "defaite" in (cas.get("attendu") or {}):
        voulue = bool(cas["attendu"]["defaite"])
        perdue = bool(monde.is_game_over and not monde.game_over.players_won)
        if perdue != voulue:
            return False, f"partie perdue = {perdue} (attendu {voulue})"
        reste = dict(cas["attendu"])
        reste.pop("defaite")
        cas = dict(cas, attendu=reste)
        aides = dict(aides, cas=cas)
    return etat_attendu(monde, aides)
'''
