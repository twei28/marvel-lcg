# Cas test_capacites de la carte d'etat maison « Cloaked » (pack TMNT, Shredder v3,
# scan Inkwire) : prefixe « [cloaked] ». Fiche : docs/reference/mots-cles/cloaked.md.
#
# Decision de l'utilisateur : UN SEUL effet, le premier qui arrive (+2 a la
# prochaine utilisation d'un pouvoir de base / activation d'ennemi, OU -2 aux
# prochains degats subis, minimum 0), puis la carte est defaussee.
#
# Montage : Spider-Man (01001a ATQ 2 / CTR 1) en forme heros contre Rhino 01094
# (ATQ 2 / MNG 1, PV 14). Le deck rencontre ne contient que 01105 « I'm Tough »
# (0 icone de boost) pour que l'attaque/la manigance de Rhino n'ait AUCUNE boost.
# Heros incline + main videe quand Rhino frappe : le pilote ne defend pas.

FORME_HEROS = "Puzzle.ChangeForm('01001b')"
RIEN_A_BOOSTER = "Puzzle.CreateEncounterDeck('01105', '01105', '01105')"

CAS = [
    # ------------------------------------------------------------ +2, pouvoir de base du heros
    {
        "nom": "[cloaked] attaque de base du heros : +2 ATQ, carte defaussee",
        "pourquoi": "« uses a basic power » : ATQ 2 + 2 = 4 degats sur Rhino, et Cloaked part (statuts_absents)",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [FORME_HEROS, "Puzzle.Cloak('01001a')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Attack('01001a')"],
        "cibles": ["01094"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 4]], "statuts_absents": [["01001a", "Cloaked"]]},
    },
    {
        "nom": "[cloaked] TEMOIN : attaque de base sans Cloaked = ATQ imprimee seule (2 degats)",
        "pourquoi": "contre-cas : prouve que les 4 degats du cas precedent viennent de la carte",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [FORME_HEROS],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Attack('01001a')"],
        "cibles": ["01094"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 2]]},
    },
    {
        "nom": "[cloaked] contre de base du heros : +2 CTR, carte defaussee",
        "pourquoi": "« a basic power » couvre aussi le contre : CTR 1 + 2 = 3 menaces retirees (5 -> 2)",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [FORME_HEROS, "Puzzle.Cloak('01001a')"],
        "main_exclusive": ["01088"],
        # SetThreat APRES le vidage de la main : sinon 01061 Great Responsibility
        # (deja en main) intercepte la pose de menace et la convertit en degats.
        "declencher": ["Puzzle.SetThreat('01097b', 5)", "Puzzle.Thwart('01001a')"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["01097b", 2]], "statuts_absents": [["01001a", "Cloaked"]]},
    },
    # ------------------------------------------------------------ +2, activation d'ennemi
    {
        "nom": "[cloaked] activation d'ennemi (attaque) : +2 ATQ, carte defaussee",
        "pourquoi": "Rhino porteur frappe : ATQ 2 + 2 = 4 degats a l'identite, sans boost ; Cloaked part",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [FORME_HEROS, "Puzzle.Exhaust('01001a')", RIEN_A_BOOSTER, "Puzzle.Cloak('01094')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Attack('01094')"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 4, "statuts_absents": [["01094", "Cloaked"]]},
    },
    {
        "nom": "[cloaked] TEMOIN : activation d'ennemi sans Cloaked = ATQ imprimee seule (2 degats)",
        "pourquoi": "contre-cas du cas precedent",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [FORME_HEROS, "Puzzle.Exhaust('01001a')", RIEN_A_BOOSTER],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Attack('01094')"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 2},
    },
    {
        "nom": "[cloaked] activation d'ennemi (manigance) : +2 MNG, carte defaussee",
        "pourquoi": "« or activates » vaut aussi pour la manigance : MNG 1 + 2 = 3 menaces (0 -> 3)",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [FORME_HEROS, RIEN_A_BOOSTER, "Puzzle.Cloak('01094')"],
        "main_exclusive": ["01088"],  # sans cela 01061 Great Responsibility convertit la menace en degats
        "declencher": ["Puzzle.Scheme('01094')"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["01097b", 3]], "statuts_absents": [["01094", "Cloaked"]]},
    },
    {
        "nom": "[cloaked] TEMOIN : manigance d'ennemi sans Cloaked = MNG imprimee seule (1 menace)",
        "pourquoi": "contre-cas du cas precedent",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [FORME_HEROS, RIEN_A_BOOSTER],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Scheme('01094')"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["01097b", 1]]},
    },
    # ------------------------------------------------------------ -2 degats
    {
        "nom": "[cloaked] degats subis : -2, carte defaussee",
        "pourquoi": "3 degats directs au heros : 3 - 2 = 1 subi, et Cloaked part",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [FORME_HEROS, "Puzzle.Cloak('01001a')"],
        "declencher": ["Puzzle.Damage('01001a', 3)"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 1, "statuts_absents": [["01001a", "Cloaked"]]},
    },
    {
        "nom": "[cloaked] degats subis : minimum 0 (1 degat -> 0, carte quand meme defaussee)",
        "pourquoi": "« decrease that value by 2 » ne descend pas sous 0 ; l'effet a eu lieu, la carte est consommee",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [FORME_HEROS, "Puzzle.Cloak('01001a')"],
        "declencher": ["Puzzle.Damage('01001a', 1)"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 0, "statuts_absents": [["01001a", "Cloaked"]]},
    },
    {
        "nom": "[cloaked] TEMOIN : 3 degats sans Cloaked = 3 subis",
        "pourquoi": "contre-cas des deux cas precedents",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [FORME_HEROS],
        "declencher": ["Puzzle.Damage('01001a', 3)"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 3},
    },
    # ------------------------------------------------------------ UN SEUL effet
    {
        "nom": "[cloaked] un seul effet : le pouvoir de base arrive d'abord (+2), les degats suivants ne sont PAS reduits",
        "pourquoi": "attaque de base (+2, carte consommee) puis 3 degats au heros : 3 subis, pas 1",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [FORME_HEROS, "Puzzle.Cloak('01001a')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Attack('01001a')", "Puzzle.Damage('01001a', 3)"],
        "cibles": ["01094"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 4]], "degats_identite": 3, "statuts_absents": [["01001a", "Cloaked"]]},
    },
    {
        "nom": "[cloaked] un seul effet : les degats arrivent d'abord (-2), l'attaque suivante n'a PAS +2",
        "pourquoi": "3 degats (1 subi, carte consommee) puis attaque de base : 2 degats, pas 4",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [FORME_HEROS, "Puzzle.Cloak('01001a')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Damage('01001a', 3)", "Puzzle.Attack('01001a')"],
        "cibles": ["01094"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 2]], "degats_identite": 1, "statuts_absents": [["01001a", "Cloaked"]]},
    },
    {
        "nom": "[cloaked] la carte d'etat est bien posee puis reconnue (HasStatus Cloaked)",
        "pourquoi": "Puzzle.Cloak pose une vraie carte d'etat comptee par HasStatus",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [FORME_HEROS, "Puzzle.Cloak('01001a')"],
        "declencher": [],
        "verifier": "etat_attendu",
        "attendu": {"statuts": [["01001a", "Cloaked"]]},
    },
]
