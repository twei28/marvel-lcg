# Cas test_capacites du set PUNISHER'S HIT LIST (pack MC×DC 2026), PU-3/PU-4. Prefixe `[hit]`.
# Montage : scenario `protection_racket_jigsaw` (Jigsaw vilain), Spider-Man (01001) en HEROS, deck rencontre remplace.
# Sbires de test (core) : 01103 Shocker (PV 3), 01110 Hydra Bomber (PV 2), 01101 Hydra Mercenary (PV 3). Punisher (pu107) : ATQ 1 + 2
# (Punishment) = 3 degats.
SC = "protection_racket_jigsaw"
HEROS = "Puzzle.ChangeForm('01001b')"
SANS_DEFENSE = {"passer_sur_option": "Defense"}


def _p(nom, pourquoi, mise, declencher, attendu, **cle):
    deck = cle.pop("deck", ["01105"] * 4)
    cas = {"nom": "[hit] " + nom, "pourquoi": pourquoi, "scenario": SC, "heros": "spider_man",
           "mise_en_place": ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck(%s)" % ", ".join(repr(x) for x in deck), HEROS, *mise],
           "declencher": declencher, "verifier": "etat_attendu", "attendu": attendu, "main_exclusive": cle.pop("main_exclusive", ["01088"])}
    cas.update(cle)
    return cas


PUN = ["Puzzle.PutIntoPlay('pu107')"]
CAS = [
    _p("pu108 When Revealed : Punishment (Punisher attaque le sbire aux PV les plus bas, Shocker) -> Shocker abattu, Rachel n'attaque pas",
       "« Resolve Punisher's Punishment ability. Otherwise, Rachel attacks you »",
       [*PUN, "Puzzle.PutIntoPlay('01103')"], ["Puzzle.Reveal('pu108')"], {"hors_jeu": ["01103"], "degats_identite": 0}),
    _p("pu108 When Revealed, SANS Punisher : Punishment impossible -> Rachel attaque le joueur (ATQ 2 = 2 degats)",
       "« Otherwise, Rachel Cole-Alves attacks you »", [], ["Puzzle.Reveal('pu108')"], {"degats_identite": 2}, **SANS_DEFENSE),
    _p("pu107 Punishment, repetition : deux sbires (Bomber 2 PV, Shocker 3 PV) -> les deux sont abattus, le plus faible d'abord",
       "« If the attack defeats that minion, repeat this ability » (ATQ 1 + 2 = 3)",
       [*PUN, "Puzzle.PutIntoPlay('01110')", "Puzzle.PutIntoPlay('01103')"], ["Puzzle.Reveal('pu108')"],
       {"hors_jeu": ["01110", "01103"]}),
    _p("pu107 Punishment, Rachel n'est JAMAIS une cible : seule Rachel en jeu -> aucune attaque (et Rachel attaque le joueur)",
       "« Punisher cannot attack this minion »", [*PUN], ["Puzzle.Reveal('pu108')"], {"en_jeu": ["pu108"], "degats_identite": 2}, **SANS_DEFENSE),
    _p("pu106a Forced Response : Punisher abat un sbire -> 1 compteur sur la liste",
       "« After Punisher defeats a character, add 1 counter here »",
       ["Puzzle.PutIntoPlay('pu106a,pu106b')", *PUN, "Puzzle.PutIntoPlay('01103')"], ["Puzzle.Reveal('pu108')"],
       {"compteurs": [["pu106a", "counter", 1]]}),
    _p("pu106a fin de la phase des joueurs : Punishment (Shocker abattu)",
       "« After the player phase ends, resolve Punisher's Punishment ability, if able »",
       ["Puzzle.PutIntoPlay('pu106a,pu106b')", *PUN, "Puzzle.PutIntoPlay('01103')"], ["Puzzle.EndPlayerPhase()"],
       {"hors_jeu": ["01103"]}),
    _p("pu106a : 3 compteurs (2+1 joueur) -> retournee en Satchel Charge : 2 degats au vilain, 3 indirects au heros, Punisher melange dans le deck, retour en 1A",
       "« remove all counters and flip this card » puis pu106b",
       ["Puzzle.PutIntoPlay('pu106a,pu106b')", *PUN, "Puzzle.PutIntoPlay('01110')", "Puzzle.PutIntoPlay('01103')", "Puzzle.PutIntoPlay('01101')"],
       ["Puzzle.Reveal('pu108')"],
       {"degats": [["pu056a", 2]], "degats_identite": 3, "dans_deck_rencontre": ["pu107"], "en_jeu": ["pu106a"],
        "compteurs": [["pu106a", "counter", 0]]}),
    _p("pu109 Katana : revele -> trouve Punisher (deck), le revele, s'attache a lui",
       "« Find Punisher, reveal him, and attach this to him »",
       [], ["Puzzle.Reveal('pu109')"], {"en_jeu": ["pu107"], "accroche_a": [["pu109", "pu107"]]}, deck=["pu107", "01105"]),
    _p("pu110 M1911 : revele -> Punisher trouve, arme attachee, il t'attaque SANS carte de boost (ATQ 1 + 1 = 2)",
       "« He attacks you. Do not give him a boost card for this attack »",
       [], ["Puzzle.Reveal('pu110')"], {"accroche_a": [["pu110", "pu107"]], "degats_identite": 2}, deck=["pu107", "01103", "01105"], **SANS_DEFENSE),
    _p("pu111 Dramatic Entrance : Punisher trouve, attaque le vilain (1 degat) puis te frappe (1 degat)",
       "« He attacks the villain and then attacks you »",
       [], ["Puzzle.Reveal('pu111')"], {"degats": [["pu056a", 1]], "degats_identite": 1}, deck=["pu107", "01105"], **SANS_DEFENSE),
    _p("pu113 Arsenal : When Revealed -> trouve une arme ARMAMENT hors jeu (Shotgun pu115) et la revele",
       "« Find an ARMAMENT attachment that is not in play and reveal it »",
       [], ["Puzzle.Reveal('pu113')"], {"en_jeu": ["pu115"]}, deck=["pu115", "01105"]),
    _p("pu113 Arsenal : When Defeated -> trouve et revele Punisher",
       "« Find Punisher and reveal him »",
       ["Puzzle.PutIntoPlay('pu113')", "Puzzle.SetThreat('pu113', 1)"], ["Puzzle.Thwart('01001a')"], {"en_jeu": ["pu107"]}, deck=["pu107", "01105"]),
]
