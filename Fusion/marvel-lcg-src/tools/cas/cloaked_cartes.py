# Cas des CARTES qui posent Cloaked (pack TMNT) : prefixe « [cloaked-cartes] ».
# Fiche : docs/reference/mots-cles/cloak.md. Les cas de la carte d'etat elle-meme
# sont dans cloaked.py.
#
#  - tl015 * Karai : « When Revealed: Cloak Karai. » / « When Defeated: Cloak the
#    villain. » (Rhino 01094 est le vilain du scenario `rhino`).
#  - tl016 Foot Soldiers : « When Revealed: Cloak Foot Soldiers. »
#  - td005 Improvised Tactics : « Cloak two friendly characters » (option 1 de
#    « choose two », que le pilote prend d'office comme premiere option).

CAS = [
    {
        "nom": "[cloaked-cartes] tl015 Karai — When Revealed : Karai elle-meme devient Cloaked",
        "pourquoi": "« Cloak Karai » = la carte, pas le vilain : Karai porte Cloaked, Rhino non",
        "scenario": "rhino", "heros": "leonardo",
        "mise_en_place": [],
        "declencher": ["Puzzle.Reveal('tl015')"],
        "verifier": "etat_attendu",
        "attendu": {"statuts": [["tl015", "Cloaked"]], "statuts_absents": [["01094", "Cloaked"]]},
    },
    {
        "nom": "[cloaked-cartes] tl015 Karai — When Defeated : le VILAIN devient Cloaked",
        "pourquoi": "« Cloak the villain » : Rhino recoit Cloaked quand Karai est vaincue",
        "scenario": "rhino", "heros": "leonardo",
        "mise_en_place": ["Puzzle.PutIntoPlay('tl015')"],
        "declencher": ["Puzzle.Damage('tl015', 9)"],
        "verifier": "etat_attendu",
        "attendu": {"statuts": [["01094", "Cloaked"]], "hors_jeu": ["tl015"]},
    },
    {
        "nom": "[cloaked-cartes] tl016 Foot Soldiers — When Revealed : la carte elle-meme devient Cloaked",
        "pourquoi": "« Cloak Foot Soldiers » : le sbire porte Cloaked, le vilain non",
        "scenario": "rhino", "heros": "leonardo",
        "mise_en_place": [],
        "declencher": ["Puzzle.Reveal('tl016')"],
        "verifier": "etat_attendu",
        "attendu": {"statuts": [["tl016", "Cloaked"]], "statuts_absents": [["01094", "Cloaked"]]},
    },
    {
        "nom": "[cloaked-cartes] td005 Improvised Tactics — « Cloak two friendly characters » : deux amis Cloaked",
        "pourquoi": "option 1 de « choose two » ; amis = identite + allies. Le pilote prend la 1re option puis la 2e jouable",
        "scenario": "rhino", "heros": "donatello",
        "mise_en_place": ["Puzzle.ChangeForm('td001b')", "Puzzle.PutIntoPlay('td002', under_control=True)",
                          "Puzzle.PutIntoPlay('td009')"],
        "main_exclusive": ["td005", "td007"],
        "declencher": [],
        "jouer": ["td005"],
        "payer_avec": ["td007"],
        "verifier": "etat_attendu",
        "attendu": {"statuts": [["td001a", "Cloaked"], ["td002", "Cloaked"]]},
    },
]
