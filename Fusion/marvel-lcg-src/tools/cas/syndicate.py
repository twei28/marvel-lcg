# Cas test_capacites du set THE SYNDICATE (pack MC×DC 2026 « La ville ne dort jamais »), PU-3. Prefixe `[syn]`.
# Montage : scenario d'essai `protection_racket_jigsaw` (Jigsaw), Spider-Man (01001) en HEROS, deck rencontre remplace par des
# 01105 (traitrise sans icone de boost). Les sbires entrent par `Puzzle.PutIntoPlay` (engages avec le heros).
SC = "protection_racket_jigsaw"
HEROS = "Puzzle.ChangeForm('01001b')"
SANS_DEFENSE = {"passer_sur_option": "Defense"}


def _s(nom, pourquoi, mise, declencher, attendu, **cle):
    cas = {"nom": "[syn] " + nom, "pourquoi": pourquoi, "scenario": cle.pop("scenario", SC), "heros": "spider_man",
           "mise_en_place": ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01105', '01105', '01105', '01105')",
                             HEROS, *mise],
           "declencher": declencher, "verifier": "etat_attendu", "attendu": attendu, "main_exclusive": cle.pop("main_exclusive", ["01088"])}
    cas.update(cle)
    return cas


CAS = [
    # ---- pu125 Beetle
    _s("pu125 Beetle : l'attaque de base du heros (ATQ 2, non AERIAL) ne fait que 1 degat (-1)",
       "« Reduce the amount of damage Beetle takes from non-AERIAL attacks by 1 »",
       ["Puzzle.PutIntoPlay('pu125')"], ["Puzzle.Attack('01001a')"], {"degats": [["pu125", 1]]}, cibles=["pu125"]),
    _s("pu125 TEMOIN : Shocker (sans la reduction) prend les 2 degats de la meme attaque",
       "contre-cas", ["Puzzle.PutIntoPlay('01103')"], ["Puzzle.Attack('01001a')"], {"degats": [["01103", 2]]}, cibles=["01103"]),
    # ---- pu126 White Rabbit
    _s("pu126 White Rabbit : elle blesse le heros -> un soutien qu'on controle (Aunt May) est defausse",
       "« After White Rabbit attacks and damages you, discard a card you control from play »",
       ["Puzzle.PutIntoPlay('01006', under_control=True)", "Puzzle.PutIntoPlay('pu126')"], ["Puzzle.Attack('pu126')"],
       {"hors_jeu": ["01006"]}, **SANS_DEFENSE),
    _s("pu126 TEMOIN : Shocker blesse le heros, Aunt May reste en jeu",
       "contre-cas", ["Puzzle.PutIntoPlay('01006', under_control=True)", "Puzzle.PutIntoPlay('01103')"], ["Puzzle.Attack('01103')"],
       {"en_jeu": ["01006"]}, **SANS_DEFENSE),
    # ---- pu127 Electro
    _s("pu127 Electro : ses attaques font des degats INDIRECTS (un allie defenseur n'en prend pas, l'identite si)",
       "« Electro's attacks deal indirect damage »",
       ["Puzzle.PutIntoPlay('01075', under_control=True)", "Puzzle.PutIntoPlay('pu127')"],
       ["Puzzle.Attack('pu127', defender='01075')"], {"degats_identite": 1}),
    _s("pu127 TEMOIN : Shocker attaque, l'allie defenseur encaisse normalement",
       "contre-cas", ["Puzzle.PutIntoPlay('01075', under_control=True)", "Puzzle.PutIntoPlay('01103')"],
       ["Puzzle.Attack('01103', defender='01075')"], {"degats_identite": 0}),
    # ---- pu128 Lady Octopus
    _s("pu128 Lady Octopus : apres son attaque, 2 menaces sur la principale (3 = 1 de base de Protection Racket + 2)",
       "« After Lady Octopus attacks, place 2 threat on the main scheme »",
       ["Puzzle.PutIntoPlay('pu128')"], ["Puzzle.Attack('pu128')"], {"menace": [["60134b", 3]]}, **SANS_DEFENSE),
    _s("pu128 TEMOIN : Shocker attaque, seulement la menace de base (1)",
       "contre-cas", ["Puzzle.PutIntoPlay('01103')"], ["Puzzle.Attack('01103')"], {"menace": [["60134b", 1]]}, **SANS_DEFENSE),
    # ---- pu129 Scorpia
    _s("pu129 Scorpia : ses attaques gagnent piercing (allie Tenace : la Tenace saute, il meurt)",
       "« Scorpia's attacks gain piercing »",
       ["Puzzle.PutIntoPlay('pu129')", "Puzzle.PutIntoPlay('01075', under_control=True)", "Puzzle.Tough('01075')"],
       ["Puzzle.EnemyAttacks('pu129', '01075')"], {"hors_jeu": ["01075"]}, **SANS_DEFENSE),
    _s("pu129 TEMOIN : Shocker, sans piercing, la Tenace absorbe",
       "contre-cas", ["Puzzle.PutIntoPlay('01103')", "Puzzle.PutIntoPlay('01075', under_control=True)", "Puzzle.Tough('01075')"],
       ["Puzzle.EnemyAttacks('01103', '01075')"], {"degats": [["01075", 0]], "statuts_absents": [["01075", "Tough"]]}, **SANS_DEFENSE),
    # ---- pu130 Trapstr
    _s("pu130 Trapstr : Quickstrike, et quand elle t'attaque tu etourdis un personnage que tu controles (le heros)",
       "« Forced Interrupt: When Trapstr attacks you, stun a character you control »",
       [], ["Puzzle.PutIntoPlay('pu130')"], {"statuts": [["01001a", "Stunned"]]}, **SANS_DEFENSE),
    _s("pu130 TEMOIN : un sbire Quickstrike ordinaire (Vulture 01167) n'etourdit personne",
       "contre-cas", [], ["Puzzle.PutIntoPlay('01167')"], {"statuts_absents": [["01001a", "Stunned"]]}, **SANS_DEFENSE),
    # ---- pu131 The Syndicate
    _s("pu131 When Revealed : le joueur trouve un sbire SYNDICATE hors jeu (Beetle dans le deck) et le revele",
       "« each player finds and reveals a SYNDICATE minion that is not in play »",
       ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('pu125', '01105')"], ["Puzzle.Reveal('pu131')"],
       {"en_jeu": ["pu125"], "menace": [["pu131", 3]]}),
    # ---- When Defeated commun
    _s("When Defeated : Scorpia vaincue -> le Maggia Thug (CRIMINAL engage, pu060) s'active contre le joueur (2 degats)",
       "« Choose a CRIMINAL minion. That minion activates against the player it is engaged with »",
       ["Puzzle.PutIntoPlay('pu060')", "Puzzle.PutIntoPlay('pu129')"], ["Puzzle.Damage('pu129', 6)"],
       {"hors_jeu": ["pu129"], "degats_identite": 2}, **SANS_DEFENSE),
    _s("When Defeated, TEMOIN : un sbire sans l'aptitude (Shocker) vaincu n'active personne",
       "contre-cas", ["Puzzle.PutIntoPlay('pu060')", "Puzzle.PutIntoPlay('01103')"], ["Puzzle.Damage('01103', 3)"],
       {"hors_jeu": ["01103"], "degats_identite": 0}),
]
