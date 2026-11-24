# Cas test_capacites : un evenement joue QUITTE la zone de traitement et va a la defausse (26/10/2026).
#
# Rapport de l'utilisateur, partie reelle sur telephone : « j'ai joue un evenement, il est reste dans "Cards in play" comme un
# upgrade », avec PLUSIEURS heros (evenements officiels compris). Ce defaut a deja existe (signalement Aghenatak, 21/09/2026) :
# une carte coincee dans la zone de traitement n'est ni en jeu ni en defausse, et le plateau la montre posee sur la table.
# La verification `aucune_en_resolution` du banc le voit ; ces cas la font passer sur des evenements OFFICIELS de plusieurs heros.
#
# Montage : le pilote joue l'evenement depuis la main ; 01090 Strength (RR) / 01088 Energy (YY) / 01089 Genius (BB) paient.
VILAIN = "01094"   # Rhino
COMPLOT = "01097b"


IDENTITE = {"spider_man": "01001", "captain_america": "03001", "iron_man": "01029", "black_panther": "01040",
            "ms_marvel": "05001", "captain_marvel": "01010", "she_hulk": "01019"}


def _c(nom, heros, event, ressources, declencher_cible, attendu_extra=None, **cle):
    # les heros demarrent en ALTER EGO : « Hero Action » n'est jouable qu'en forme heros
    i = IDENTITE[heros]
    cas = {
        "nom": f"[ev] {event} {nom}",
        "pourquoi": "un evenement joue va a la defausse du joueur et ne reste dans aucune zone de traitement",
        "scenario": "rhino",
        "heros": heros,
        "mise_en_place": [f"Puzzle.ChangeToFace('{i}b', '{i}a')"] + cle.pop("mise_en_place", []),
        "main_exclusive": [event, *ressources],
        "jouer": [event],
        "declencher": [],
        "verifier": "etat_attendu",
        "attendu": {"defausse": [event], "aucune_en_resolution": True, **(attendu_extra or {})},
        "accepter_choix": True,
        "cibles": declencher_cible,
    }
    cas.update(cle)
    return cas


CAS = [
    _c("Haymaker (attack, Basic) avec Spider-Man", "spider_man", "01087", ["01090"], [VILAIN], {"degats": [[VILAIN, 3]]}),
    _c("Haymaker avec Captain America", "captain_america", "01087", ["01090"], [VILAIN], {"degats": [[VILAIN, 3]]}),
    _c("Haymaker avec Iron Man", "iron_man", "01087", ["01090"], [VILAIN]),
    _c("First Aid (Action) avec Spider-Man", "spider_man", "01086", ["01088"], ["01001a"],
       mise_en_place=["Puzzle.Damage('01001a', 3)"]),
    _c("For Justice! (thwart, Justice) avec Black Panther", "black_panther", "01060", ["01090"], [COMPLOT],
       mise_en_place=[f"Puzzle.SetThreat('{COMPLOT}', 6)"]),
    _c("Ground Stomp (attack toute la table) avec Ms. Marvel", "ms_marvel", "01022", ["01090"], []),
    _c("Repulsor Blast (attack) avec Iron Man", "iron_man", "01031", ["01088"], [VILAIN]),
    _c("Supersonic Punch (attack) avec Captain Marvel", "captain_marvel", "01032", ["01090"], [VILAIN]),
    _c("Crisis Interdiction (thwart) avec She-Hulk", "she_hulk", "01012", ["01090"], [COMPLOT],
       mise_en_place=[f"Puzzle.SetThreat('{COMPLOT}', 6)"]),
]
