# Cas test_capacites du set HOBGOBLIN (pack MC×DC 2026 « La ville ne dort jamais »), PU-2. Prefixe `[hob]`.
# Montage : scenario d'essai `protection_racket_hobgoblin` (Hobgoblin I pu071a puis pu072a), Spider-Man en HEROS.
# Le deck rencontre est REMPLACE par les cartes voulues : la DERNIERE de la liste est le DESSUS (mesure du 21/10).
SC = "protection_racket_hobgoblin"
SCE = "protection_racket_hobgoblin_expert"
HEROS = "Puzzle.ChangeForm('01001b')"
SANS_DEFENSE = {"passer_sur_option": "Defense"}


def _h(nom, pourquoi, deck, mise, declencher, attendu, **cle):
    cas = {"nom": "[hob] " + nom, "pourquoi": pourquoi, "scenario": cle.pop("scenario", SC), "heros": "spider_man",
           "mise_en_place": ["Puzzle.EmptyEncounterDeck()",
                             "Puzzle.CreateEncounterDeck(%s)" % ", ".join(repr(x) for x in deck), HEROS, *mise],
           "declencher": declencher, "verifier": "etat_attendu", "attendu": attendu}
    cas.update(cle)
    return cas


# Cartes officielles utilisees : 01105 traitrise (I'm Tough, 0 icone de boost), 01103 sbire (Shocker), 01160 obligation
# (Enhanced Ivory Horn). ⚠ Protection Racket (60134b) pose DEJA 1 menace quand le vilain attaque le heros (Battle in
# the Bodega) : les attendus de menace comptent ce 1 de base. La carte de BOOST de l'attaque (le dessus du deck) est
# defaussee AVANT la Reponse forcee ; la Pumpkin Bomb defausse la carte d'en dessous.
CAS = [
    _h("pu071a Forced Response : Pumpkin Bomb, carte defaussee = TRAITRISE -> 1 menace de plus (1 de base + 1)",
       "Pumpkin Bomb : « If that card is a Treachery, place 1 threat on the main scheme »",
       ["01105", "01105", "01105"], [], ["Puzzle.EnemyAttacks('pu071a', '01001a')"], {"menace": [["60134b", 2]]},
       main_exclusive=["01088"], **SANS_DEFENSE),
    _h("pu071a Pumpkin Bomb : carte defaussee = SBIRE -> 1 degat indirect sur le heros (1 de l'attaque + 1)",
       "« Minion or side scheme: Take 1 indirect damage »",
       ["01103", "01105"], [], ["Puzzle.EnemyAttacks('pu071a', '01001a')"],
       {"degats_identite": 2, "menace": [["60134b", 1]]}, main_exclusive=["01088"], **SANS_DEFENSE),
    _h("pu071a Pumpkin Bomb : carte defaussee = AUTRE (obligation) -> 3 cartes defaussees de plus, ni menace ni indirect",
       "« Other: Discard 3 cards from the encounter deck »",
       ["01103", "01108", "01107", "01106", "01160", "01105"], [], ["Puzzle.EnemyAttacks('pu071a', '01001a')"],
       {"defausse_rencontre": ["01105", "01160", "01106", "01107", "01108"], "degats_identite": 1, "menace": [["60134b", 1]]},
       main_exclusive=["01088"], **SANS_DEFENSE),
    _h("pu071b Forced Response (2 fois) : deux traitrises defaussees -> 2 menaces (complot du joueur tire au sort : pas de Battle in the Bodega)",
       "« resolve the Pumpkin Bomb ability twice » (expert : pu071b)",
       ["01105", "01105", "01105", "01105"], ["Puzzle.PutIntoPlay('pu071b')"], ["Puzzle.EnemyAttacks('pu071b', '01001a')"],
       {"menace_joueur": 2}, main_exclusive=["01088"], verifier="fne3p_racket", **SANS_DEFENSE, scenario=SCE),
]

CAS += [
    _h("pu073 Hobgoblin's Glider : attache a Hobgoblin (Setup, Permanent natifs)",
       "« Attach to Hobgoblin » ; Setup : le Glider est en jeu des la mise en place (modele Paibok)",
       ["01105"], [], [], {"accroche_a": [["pu073", "pu071a"]]}, main_exclusive=["01088"]),
    _h("pu071a « attacks gain ranged » : Hobgoblin attaque le Jailor (gs131, Riposte 1) -> aucune riposte (autre manigance : Battle in the Bodega blesserait le vilain)",
       "ranged ignore Retaliate (modele gs083)",
       ["01105"], ["Puzzle.PutIntoPlay('gs131')"], ["Puzzle.EnemyAttacks('pu071a', 'gs131')"],
       {"degats": [["pu071a", 0], ["gs131", 1]]}, main_exclusive=["01088"],
       scenario="art_museum_heist_hobgoblin"),
]
