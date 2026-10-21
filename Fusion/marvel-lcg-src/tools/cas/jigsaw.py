# Cas test_capacites du set JIGSAW (pack MC×DC 2026 « La ville ne dort jamais »), PU-2.
# Prefixe `[jig]` (filtre : `[jig]`, ou `[jig] pu056a ` pour une carte).
#
# Montage : scenario d'essai `protection_racket_jigsaw` (Jigsaw I pu056a, puis pu057a), Spider-Man (01001) en HEROS.
# Le deck rencontre est remplace par des 01105 (« I'm Tough », 0 icone de boost) pour que l'attaque ne recoive aucun
# bonus. Jigsaw attaque directement le heros (`Puzzle.EnemyAttacks`, brique commune) ; aucune defense proposee.
SC = "protection_racket_jigsaw"
SCE = "protection_racket_jigsaw_expert"
HEROS = "Puzzle.ChangeForm('01001b')"
SANS_DEFENSE = {"passer_sur_option": "Defense"}
RIEN = ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01105', '01105', '01105')", HEROS]


def _c(nom, pourquoi, mise, attendu, **cle):
    cas = {"nom": "[jig] " + nom, "pourquoi": pourquoi, "scenario": cle.pop("scenario", SC), "heros": "spider_man",
           "mise_en_place": RIEN + mise, "declencher": ["Puzzle.EnemyAttacks('pu056a', '01001a')"],
           "verifier": "etat_attendu", "attendu": attendu}
    cas.update(cle)
    return cas


# ⚠ La carte Boost de l'attaque est defaussee AVANT la Reponse forcee (« apres que Jigsaw vous a attaque ») : c'est donc
# elle qui est « le dessus de la defausse rencontre ». Le deck rencontre sert ici a choisir ce dessus.
BOOST_SBIRE = ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01103', '01105')"]


def _d(nom, pourquoi, deck, mise, attendu, attaquant="pu056a", **cle):
    avant = cle.pop("avant_attaque", None)
    cas = _c(nom, pourquoi, mise, attendu, **cle)
    cas["mise_en_place"] = [*RIEN[:1], f"Puzzle.CreateEncounterDeck({', '.join(repr(x) for x in deck)})", HEROS, *mise]
    cas["declencher"] = [*([avant] if avant else []), f"Puzzle.EnemyAttacks('{attaquant}', '01001a')"]
    return cas


CAS = [
    _d("pu056a Forced Response : la carte Boost (defaussee) est un SBIRE -> mis en jeu engage avec le heros, pas de menace",
       "« if the top of the encounter discard pile is a minion, put it into play engaged with you »",
       ["01105", "01103"], [], {"en_jeu": ["01103"], "menace": [["60134b", 0]]}, **SANS_DEFENSE),
    _d("pu056a Forced Response : la carte Boost est une TRAITRISE (sbire plus bas dans la defausse) -> 1 menace, aucun sbire",
       "seul le DESSUS compte ; « Otherwise, place 1 threat on the main scheme »",
       ["01105", "01105"], ["Puzzle.CreateEncounterDiscardPile('01103')"],
       {"hors_jeu": ["01103"], "menace": [["60134b", 1]]}, **SANS_DEFENSE),
    _d("pu057b Forced Response (expert final) : dessus = traitrise -> 2 menaces sur le complot du joueur",
       "« place 2 threat on the main scheme »",
       ["01105", "01105"], [],
       {"menace_joueur": 2}, attaquant="pu057b", scenario=SCE, avant_attaque="Puzzle.AdvanceVillain()",
       verifier="fne3p_racket", main_exclusive=["01088"], **SANS_DEFENSE),
]
