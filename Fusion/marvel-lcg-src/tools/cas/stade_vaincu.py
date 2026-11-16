# Cas test_capacites du CORRECTIF du 16/11/2026 (signalement de bug n°133, Excessive Force sur Rhino) : noms prefixes
# « [stade_vaincu] ». Un vilain a PLUSIEURS STADES (Rhino 01094 -> 01095) qui perd son dernier PV est bien VAINCU : le moteur
# l'annonce, puis le fait progresser (PV remis a fond, meme nom). Une carte qui relit `cible.IsDefeated()` APRES ses degats
# voyait donc le stade 2 en pleine forme et croyait la cible vivante : « si cet ennemi est vaincu, piochez X » ne partait pas.
# Montage : scenario Rhino (stade 1 : 14 PV en solo), Spider-Man, deck rencontre neutre (01105, aucun boost).
FORME_HEROS = "Puzzle.ChangeForm('01001b')"
RIEN_A_BOOSTER = ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01105', '01105', '01105')"]
VILAIN = "01094"


def _c(nom, pourquoi, mise, attendu, **cle):
    cas = {"nom": "[stade_vaincu] " + nom, "pourquoi": pourquoi, "scenario": "rhino", "heros": "spider_man",
           "mise_en_place": RIEN_A_BOOSTER + [FORME_HEROS] + list(mise), "declencher": [],
           "verifier": "etat_attendu", "attendu": attendu}
    cas.update(cle)
    return cas


CAS = [
    _c("dt083 Excessive Force : Rhino stade 1 achevé (2 PV restants) -> pioche X = 2",
       "« If that enemy is defeated by this attack, draw X cards » : le stade 1 vaincu compte, meme si le stade 2 repart a 15 PV",
       [f"Puzzle.Damage('{VILAIN}', 12)"], {"taille_main": 2},
       main_exclusive=["dt083", "01088"], payer_avec=["01088"], jouer=["dt083"], surpayer=True, cibles=[VILAIN]),
    _c("dt083 Excessive Force : Rhino a 3 PV, 2 degats -> PAS vaincu, aucune pioche",
       "contre-cas : la pioche ne vient que d'une VRAIE defaite",
       [f"Puzzle.Damage('{VILAIN}', 11)"], {"taille_main": 0},
       main_exclusive=["dt083", "01088"], payer_avec=["01088"], jouer=["dt083"], surpayer=True, cibles=[VILAIN]),
    _c("35018 Precision Strike : Rhino stade 1 acheve (2 PV restants) -> soigne 2 degats du heros",
       "carte OFFICIELLE de la meme famille (« if this attack defeats that enemy ») : meme defaut que dt083",
       [f"Puzzle.Damage('{VILAIN}', 12)", "Puzzle.Damage('01001a', 3)"], {"degats_identite": 1},
       main_exclusive=["35018", "01090"], payer_avec=["01090"], jouer=["35018"], cibles=[VILAIN]),
    _c("35018 Precision Strike : Rhino a 3 PV -> PAS vaincu, aucun soin",
       "contre-cas : le soin ne vient que d'une VRAIE defaite",
       [f"Puzzle.Damage('{VILAIN}', 11)", "Puzzle.Damage('01001a', 3)"], {"degats_identite": 3},
       main_exclusive=["35018", "01090"], payer_avec=["01090"], jouer=["35018"], cibles=[VILAIN]),
]
