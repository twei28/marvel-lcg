# Cas test_capacites : une carte defaussee que le Collectionneur range dans LA COLLECTION garde ses compteurs.
# Rapport de bug 125 (10/11/2026) : Energy Channel (01018) infligeait 0 degat au Collectionneur. Sa Hero Action
# defausse la carte (cout) PUIS lit ses compteurs ; la defausse redirigee vers la Collection (AsideDeck, pas
# `is_discards`) remettait la carte a zero (card.py, « Fix surge »), contrairement a une vraie defausse.
# Montage : scenario infiltrate_the_museum, le Collectionneur est le vilain (16070) ; Captain Marvel en forme heros.
HEROS = "Puzzle.ChangeForm('01010a')"
COLLECTIONNEUR = "16070"

CAS = [
    {
        "nom": "[collector] 01018 Energy Channel : 5 compteurs -> 10 degats meme quand la Collection ramasse la carte",
        "pourquoi": "rapport 125 : la defausse redirigee vers La Collection effacait les compteurs avant que l'effet les lise (0 degat)",
        "scenario": "infiltrate_the_museum", "heros": "captain_marvel",
        "mise_en_place": [HEROS, "Puzzle.PutIntoPlay('01018')", "Puzzle.PlaceCounters('01018', 'energy', 5)"],
        "declencher": ["Puzzle.Action('01018', 'HeroAction')"],
        "cibles": [COLLECTIONNEUR],
        "verifier": "etat_attendu", "attendu": {"degats": [[COLLECTIONNEUR, 10]]},
    },
    {
        "nom": "[collector] 01018 Energy Channel : CONTRE-CAS vilain ordinaire (Rhino), 5 compteurs -> 10 degats",
        "pourquoi": "le comportement hors Collector ne doit pas bouger",
        "scenario": "rhino", "heros": "captain_marvel",
        "mise_en_place": [HEROS, "Puzzle.PutIntoPlay('01018')", "Puzzle.PlaceCounters('01018', 'energy', 5)"],
        "declencher": ["Puzzle.Action('01018', 'HeroAction')"],
        "cibles": ["01094"],
        "verifier": "etat_attendu", "attendu": {"degats": [["01094", 10]]},
    },
    {
        "nom": "[collector] sv004 Energy Manipulation : 3 compteurs -> 3 cartes meme quand la Collection ramasse la carte",
        "pourquoi": "meme defaut que 01018 (cout « Discard This » puis lecture des compteurs) : balayage des cartes de ce type, cote Silver Surfer",
        "scenario": "infiltrate_the_museum", "heros": "silver_surfer",
        "mise_en_place": ["Puzzle.ChangeToFace('sv001b', 'sv001a')", "Puzzle.PutIntoPlay('sv004', under_control=True)",
                          "Puzzle.PlaceCounters('sv004', 'energy', 3)", "Puzzle.EmptyPlayerDeck()",
                          "Puzzle.CreatePlayerDeck('01089', '01089', '01089', '01089', '01089', '01089')"],
        "declencher": ["Puzzle.Action('sv004', 'HeroAction')"],
        "main_exclusive": ["01090"],
        "verifier": "etat_attendu", "attendu": {"taille_main": 4},
    },
]
