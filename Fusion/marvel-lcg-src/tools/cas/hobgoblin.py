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

# ============================================================== pu074 .. pu084
ALTER_EGO = "Puzzle.ChangeForm('01001a')"
T5 = ["01105"] * 5
CAS += [
    # ---- pu074 Flaming Sword
    _h("pu074 Flaming Sword : attache a Hobgoblin ; ses attaques gagnent piercing (allie Tenace : la Tenace saute, il meurt)",
       "« Attach to Hobgoblin » + piercing (modele gs083)", ["01105"],
       ["Puzzle.PutIntoPlay('pu074')", "Puzzle.PutIntoPlay('01075', under_control=True)", "Puzzle.Tough('01075')"],
       ["Puzzle.EnemyAttacks('pu071a', '01075')"], {"accroche_a": [["pu074", "pu071a"]], "hors_jeu": ["01075"]},
       main_exclusive=["01088"], **SANS_DEFENSE),
    _h("pu074 piercing, TEMOIN : sans l'epee la Tenace absorbe l'attaque",
       "contre-cas", ["01105"], ["Puzzle.PutIntoPlay('01075', under_control=True)", "Puzzle.Tough('01075')"],
       ["Puzzle.EnemyAttacks('pu071a', '01075')"], {"degats": [["01075", 0]]}, main_exclusive=["01088"], **SANS_DEFENSE),
    _h("pu074 Hero Action : epuiser le heros, 2 Pumpkin Bomb (2 traitrises -> 2 menaces) puis defausser l'epee",
       "« Exhaust your hero and resolve the Pumpkin Bomb ability twice → discard this card »",
       ["01105", "01105"], ["Puzzle.PutIntoPlay('pu074')"], ["Puzzle.Action('pu074', 'HeroAction')"],
       {"hors_jeu": ["pu074"], "exhausted": ["01001a"], "menace": [["60134b", 2]]}, main_exclusive=["01088"]),
    # ---- pu075 Prowler
    _h("pu075 Forced Response : Prowler blesse le heros (Quickstrike) -> 2 cartes defaussees ; une traitrise -> le soutien (Aunt May) est defausse",
       "« discard 2 cards ... If a treachery was discarded this way, discard an upgrade or support you control »",
       ["01105", "01105", "01105"], ["Puzzle.PutIntoPlay('01006', under_control=True)"],
       ["Puzzle.PutIntoPlay('pu075')"], {"hors_jeu": ["01006"]}, main_exclusive=["01088"], **SANS_DEFENSE),
    _h("pu075 Forced Response, TEMOIN : 2 cartes sans traitrise (sbires) -> le soutien reste",
       "contre-cas", ["01103"] * 4, ["Puzzle.PutIntoPlay('01006', under_control=True)"],
       ["Puzzle.PutIntoPlay('pu075')"], {"en_jeu": ["01006"]}, main_exclusive=["01088"], **SANS_DEFENSE),
    # ---- pu076 Rabble
    _h("pu076 Rabble entre en jeu avec 2 compteurs drone",
       "ThisEnterPlayWithCounters(2, 'drone')", ["01105"], ["Puzzle.PutIntoPlay('pu076')"], [],
       {"compteurs": [["pu076", "drone", 2]]}, main_exclusive=["01088"]),
    _h("pu076 Forced Interrupt : 2 degats sur Rabble -> 1 compteur retire, degats empeches, 2 cartes defaussees",
       "« remove 1 drone counter → prevent that damage and discard 2 cards from the encounter deck instead »",
       ["01108", "01107", "01106"], ["Puzzle.PutIntoPlay('pu076')"], ["Puzzle.Damage('pu076', 2)"],
       {"degats": [["pu076", 0]], "compteurs": [["pu076", "drone", 1]], "defausse_rencontre": ["01106", "01107"]},
       main_exclusive=["01088"]),
    _h("pu076 sans compteur : le troisieme coup passe (2 compteurs -> 0, puis 1 degat subi)",
       "le cout est le compteur", ["01105"] * 6, ["Puzzle.PutIntoPlay('pu076')"],
       ["Puzzle.Damage('pu076', 1)", "Puzzle.Damage('pu076', 1)", "Puzzle.Damage('pu076', 1)"],
       {"degats": [["pu076", 1]], "compteurs": [["pu076", "drone", 0]]}, main_exclusive=["01088"]),
    # ---- pu077 The Enforcers
    _h("pu077 Forced Response : apres l'activation, 3 cartes defaussees (3 traitrises) -> 3 degats indirects (+ 3 de l'attaque)",
       "« Take 1 indirect damage for each treachery discarded this way »",
       ["01105"] * 4, ["Puzzle.PutIntoPlay('pu077')"], ["Puzzle.Attack('pu077')"], {"degats_identite": 6},
       main_exclusive=["01088"], **SANS_DEFENSE),
    _h("pu077 Forced Response, TEMOIN : 3 sbires defausses -> aucun degat indirect (3 de l'attaque)",
       "contre-cas", ["01103"] * 4, ["Puzzle.PutIntoPlay('pu077')"], ["Puzzle.Attack('pu077')"],
       {"degats_identite": 3}, main_exclusive=["01088"], **SANS_DEFENSE),
    # ---- pu078 Torn to Pieces
    _h("pu078 Forced Response : le heros utilise un pouvoir de base (attaque) -> Pumpkin Bomb : 1 carte defaussee",
       "« After your hero uses a basic power, resolve the Pumpkin Bomb ability »",
       ["01105", "01105"], ["Puzzle.Reveal('pu078')"], ["Puzzle.Attack('01001a')"],
       {"defausse_rencontre": ["01105"]}, main_exclusive=["01088"], cibles=["pu071a"]),
    _h("pu078 Alter-Ego Action : epuiser l'identite, 3 cartes defaussees, l'obligation est defaussee",
       "« Exhaust your identity and discard 3 cards from the encounter deck → discard this card »",
       ["01108", "01107", "01106", "01105"], [ALTER_EGO, "Puzzle.Reveal('pu078')"],
       ["Puzzle.Action('pu078', 'AlterEgoAction')"],
       {"exhausted": ["01001b"], "defausse_rencontre": ["01105", "01106", "01107"], "hors_jeu": ["pu078"]},
       main_exclusive=["01088"]),
    # ---- pu079 Designs on Crimes
    _h("pu079 When Revealed : 3 cartes defaussees par joueur (solo : 3) ; menace de depart 3",
       "« Discard 3[per hero] cards »", ["01108", "01107", "01106", "01105"], [], ["Puzzle.Reveal('pu079')"],
       {"defausse_rencontre": ["01105", "01106", "01107"], "menace": [["pu079", 3]]}, main_exclusive=["01088"]),
    _h("pu079 When Defeated : le joueur resout la Pumpkin Bomb (traitrise -> 1 menace sur la principale)",
       "« each player resolves the Pumpkin Bomb ability »",
       ["01105", "01105"], ["Puzzle.PutIntoPlay('pu079')", "Puzzle.SetThreat('pu079', 1)"], ["Puzzle.Thwart('01001a')"],
       {"menace": [["60134b", 1]]}, main_exclusive=["01088"]),
    # ---- pu080 Guise to Terrorize
    _h("pu080 When Revealed : la carte defaussee est une TRAITRISE -> Pumpkin Bomb (une autre traitrise -> 1 menace)",
       "« If the discarded card is a treachery, resolve the Pumpkin Bomb ability »",
       ["01105", "01105", "01105"], [], ["Puzzle.Reveal('pu080')"], {"menace": [["60134b", 1]]}, main_exclusive=["01088"]),
    _h("pu080 When Revealed : la carte defaussee est un SBIRE -> elle est revelee (entre en jeu), pas de Pumpkin Bomb",
       "« Otherwise, reveal that card »", ["01105", "01103"], [], ["Puzzle.Reveal('pu080')"],
       {"en_jeu": ["01103"], "menace": [["60134b", 0]]}, main_exclusive=["01088"]),
    # ---- pu082 Smashing Pumpkins
    _h("pu082 When Revealed : 3 Pumpkin Bomb (3 traitrises) -> 3 menaces",
       "« Resolve the Pumpkin Bomb ability three times »", ["01105"] * 4, [], ["Puzzle.Reveal('pu082')"],
       {"menace": [["60134b", 3]]}, main_exclusive=["01088"]),
    _h("pu082 Boost : une Pumpkin Bomb de plus pendant l'activation (3 menaces : Battle in the Bodega + bombe de Hobgoblin + bombe du boost)",
       "« ★ Boost: Resolve the Pumpkin Bomb ability »", ["01105"] * 5, [], ["Puzzle.Boost('pu082')"],
       {"menace": [["60134b", 3]]}, main_exclusive=["01088"], **SANS_DEFENSE),
    _h("pu082 Boost, TEMOIN : avec une carte quelconque (01105), 2 menaces seulement",
       "contre-cas", ["01105"] * 5, [], ["Puzzle.Boost('01105')"], {"menace": [["60134b", 2]]},
       main_exclusive=["01088"], **SANS_DEFENSE),
    # ---- pu084 Wrath of the Hobgoblin
    _h("pu084 When Revealed : Hobgoblin attaque (ATQ 1 + 2 jetons d'acceleration = 3 degats sur l'identite)",
       "« +1 SCH and +1 ATK for each acceleration token on the main scheme »",
       ["01105"] * 4, ["Puzzle.Token('60134b', 'acceleration_token', 2)"], ["Puzzle.Reveal('pu084')"],
       {"degats_identite": 3}, main_exclusive=["01088"], **SANS_DEFENSE),
    _h("pu084 When Revealed, TEMOIN : sans jeton d'acceleration, ATQ 1 = 1 degat",
       "contre-cas", ["01105"] * 4, [], ["Puzzle.Reveal('pu084')"], {"degats_identite": 1}, main_exclusive=["01088"], **SANS_DEFENSE),
]
CAS.append(_h("Stades expert : pu071b vaincu -> pu072b prend la releve (pas de victoire)", "expert = deux stades (II puis III), comme Hammerhead expert", ["01105"], [], ["Puzzle.Damage('pu071b', 17)"], {"en_jeu": ["pu072b"]}, main_exclusive=["01088"], scenario=SCE))
CAS.append(_h("Stades standard : pu071a vaincu -> pu072a prend la releve", "standard = deux stades (I puis II)", ["01105"], [], ["Puzzle.Damage('pu071a', 15)"], {"en_jeu": ["pu072a"]}, main_exclusive=["01088"]))
CAS.append(_h("Stades expert : pu071b vaincu PAR UNE ATTAQUE du heros -> pu072b", "meme chemin que la defaite par degats", ["01105"], ["Puzzle.Damage('pu071b', 16)"], ["Puzzle.Attack('01001a')"], {"en_jeu": ["pu072b"]}, main_exclusive=["01088"], scenario=SCE, cibles=["pu071b"]))
