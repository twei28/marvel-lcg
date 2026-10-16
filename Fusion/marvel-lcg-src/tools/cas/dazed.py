# Cas test_capacites de la carte d'etat maison « Dazed » (pack TMNT, Baxter Stockman v3,
# scan Inkwire, insert « Dazed Rules ») : prefixe « [dazed] ». Fiche : docs/reference/mots-cles/dazed.md.
#
# Regle : « The next time this character uses a basic power or activates, DECREASE that
# value by 2, then discard this status card. The next time this character would take any
# amount of damage, INCREASE that value by 2, then discard this status card. »
# L'insert tranche : UN SEUL effet (le premier qui arrive), UN seul Dazed par personnage,
# Steady/Stalwart n'y changent rien, Tough resout avant, Cloaked et Dazed « en meme temps ».
#
# Montage (calque de cloaked.py) : Spider-Man (01001a ATQ 2 / CTR 1) en forme heros contre
# Rhino 01094 (ATQ 2 / MNG 1, PV 14). Le deck rencontre ne contient que 01105 « I'm Tough »
# (0 icone de boost) pour que l'attaque/la manigance de Rhino n'ait AUCUNE boost.

FORME_HEROS = "Puzzle.ChangeForm('01001b')"
RIEN_A_BOOSTER = "Puzzle.CreateEncounterDeck('01105', '01105', '01105')"

CAS = [
    # ------------------------------------------------------------ -2, pouvoir de base du heros
    {
        "nom": "[dazed] attaque de base du heros : -2 ATQ (2 -> 0 degat), carte defaussee",
        "pourquoi": "« uses a basic power » : ATQ 2 - 2 = 0 degat sur Rhino, et Dazed part (statuts_absents)",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [FORME_HEROS, "Puzzle.Daze('01001a')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Attack('01001a')"],
        "cibles": ["01094"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 0]], "statuts_absents": [["01001a", "Dazed"]]},
    },
    {
        "nom": "[dazed] TEMOIN : attaque de base sans Dazed = ATQ imprimee seule (2 degats)",
        "pourquoi": "contre-cas : prouve que les 0 degat du cas precedent viennent de la carte",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [FORME_HEROS],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Attack('01001a')"],
        "cibles": ["01094"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 2]]},
    },
    {
        "nom": "[dazed] contre de base du heros : -2 CTR (1 -> 0 menace retiree), carte defaussee",
        "pourquoi": "« a basic power » couvre aussi le contre : CTR 1 - 2 = 0 menace retiree (5 reste 5)",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [FORME_HEROS, "Puzzle.Daze('01001a')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.SetThreat('01097b', 5)", "Puzzle.Thwart('01001a')"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["01097b", 5]], "statuts_absents": [["01001a", "Dazed"]]},
    },
    # ------------------------------------------------------------ -2, activation d'ennemi
    {
        "nom": "[dazed] activation d'ennemi (attaque) : -2 ATQ (2 -> 0 degat), carte defaussee",
        "pourquoi": "Rhino porteur frappe : ATQ 2 - 2 = 0 degat a l'identite, sans boost ; Dazed part",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [FORME_HEROS, "Puzzle.Exhaust('01001a')", RIEN_A_BOOSTER, "Puzzle.Daze('01094')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Attack('01094')"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 0, "statuts_absents": [["01094", "Dazed"]]},
    },
    {
        "nom": "[dazed] activation d'ennemi (manigance) : -2 MNG (1 -> 0 menace), carte defaussee",
        "pourquoi": "« or activates » vaut aussi pour la manigance : MNG 1 - 2 = 0 menace posee",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [FORME_HEROS, RIEN_A_BOOSTER, "Puzzle.Daze('01094')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Scheme('01094')"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["01097b", 0]], "statuts_absents": [["01094", "Dazed"]]},
    },
    # ------------------------------------------------------------ +2 degats
    {
        "nom": "[dazed] degats subis : +2, carte defaussee",
        "pourquoi": "3 degats directs au heros : 3 + 2 = 5 subis, et Dazed part",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [FORME_HEROS, "Puzzle.Daze('01001a')"],
        "declencher": ["Puzzle.Damage('01001a', 3)"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 5, "statuts_absents": [["01001a", "Dazed"]]},
    },
    {
        "nom": "[dazed] TEMOIN : 3 degats sans Dazed = 3 subis",
        "pourquoi": "contre-cas du cas precedent",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [FORME_HEROS],
        "declencher": ["Puzzle.Damage('01001a', 3)"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 3},
    },
    {
        "nom": "[dazed] degats d'une attaque d'ennemi : +2 (Rhino ATQ 2 sur un heros Dazed qui ne se defend pas : 4 subis)",
        "pourquoi": "« would take ANY AMOUNT of damage » : l'attaque de Rhino (2) devient 4 ; ce n'est pas l'activation de Rhino",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [FORME_HEROS, "Puzzle.Exhaust('01001a')", RIEN_A_BOOSTER, "Puzzle.Daze('01001a')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Attack('01094')"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 4, "statuts_absents": [["01001a", "Dazed"]]},
    },
    # ------------------------------------------------------------ UN SEUL effet
    {
        "nom": "[dazed] un seul effet : le pouvoir de base arrive d'abord (-2), les degats suivants ne sont PAS augmentes",
        "pourquoi": "attaque de base (-2, carte consommee) puis 3 degats au heros : 3 subis, pas 5",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [FORME_HEROS, "Puzzle.Daze('01001a')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Attack('01001a')", "Puzzle.Damage('01001a', 3)"],
        "cibles": ["01094"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 0]], "degats_identite": 3, "statuts_absents": [["01001a", "Dazed"]]},
    },
    {
        "nom": "[dazed] un seul effet : les degats arrivent d'abord (+2), l'attaque suivante n'a PAS -2",
        "pourquoi": "3 degats (5 subis, carte consommee) puis attaque de base : 2 degats, pas 0",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [FORME_HEROS, "Puzzle.Daze('01001a')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Damage('01001a', 3)", "Puzzle.Attack('01001a')"],
        "cibles": ["01094"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 2]], "degats_identite": 5, "statuts_absents": [["01001a", "Dazed"]]},
    },
    # ------------------------------------------------------------ UNE seule carte par personnage
    {
        "nom": "[dazed] une seule carte Dazed par personnage : la seconde pose est refusee (Faces.GiveStatus rend 0, 1 carte)",
        "pourquoi": "« a character can only have one Dazed status card » : le verificateur tente une SECONDE pose et compte les cartes",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [FORME_HEROS, "Puzzle.Daze('01001a')"],
        "declencher": [],
        "verifier": "dazed_unique",
        "attendu": {"cartes": 1},
    },
    # ------------------------------------------------------------ Steady / Stalwart n'y changent rien
    {
        "nom": "[dazed] un personnage Stalwart peut etre Dazed (Kree Lieutenant 16133 Stalwart : la pose reussit)",
        "pourquoi": "insert : « Can I Daze a steady/stalwart character? Yes. » Stalwart interdit Sonne/Desoriente, pas Dazed",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [FORME_HEROS, "Puzzle.PutIntoPlay('16133')", "Puzzle.Daze('16133')"],
        "declencher": [],
        "verifier": "etat_attendu",
        "attendu": {"statuts": [["16133", "Dazed"]]},
    },
    {
        "nom": "[dazed] TEMOIN : Stalwart refuse bien Sonne (Kree Lieutenant 16133 : Puzzle.Stun ne pose rien)",
        "pourquoi": "contre-cas : prouve que le cas precedent teste bien un personnage Stalwart (Sonne refuse, Dazed accepte)",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [FORME_HEROS, "Puzzle.PutIntoPlay('16133')", "Puzzle.Stun('16133')"],
        "declencher": [],
        "verifier": "etat_attendu",
        "attendu": {"statuts_absents": [["16133", "Stunned"]]},
    },
    # ------------------------------------------------------------ Tough d'abord
    {
        "nom": "[dazed] Tough resout d'abord : un Tough + un Dazed, 3 degats -> 0 subi et Dazed RESTE",
        "pourquoi": "insert : « Tough always resolves before Cloaked, and Cloaked and Dazed ... » ; Tough previent tout, Dazed ne se declenche pas",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [FORME_HEROS, "Puzzle.Tough('01001a')", "Puzzle.Daze('01001a')"],
        "declencher": ["Puzzle.Damage('01001a', 3)"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 0, "statuts": [["01001a", "Dazed"]], "statuts_absents": [["01001a", "Tough"]]},
    },
    {
        "nom": "[dazed] Tough d'abord, PUIS Dazed : 3 degats (prevenus par Tough) puis 3 degats (+2 = 5 subis), Dazed consommee",
        "pourquoi": "preuve positive de l'ordre : le premier coup est absorbe par Tough (Dazed intacte), le second declenche Dazed ; rouge sans module",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [FORME_HEROS, "Puzzle.Tough('01001a')", "Puzzle.Daze('01001a')"],
        "declencher": ["Puzzle.Damage('01001a', 3)", "Puzzle.Damage('01001a', 3)"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 5, "statuts_absents": [["01001a", "Dazed"], ["01001a", "Tough"]]},
    },
    # ------------------------------------------------------------ Cloaked et Dazed en meme temps
    {
        "nom": "[dazed] Cloaked + Dazed, pouvoir de base : +2 -2 = ATQ imprimee (2 degats), les DEUX cartes partent",
        "pourquoi": "insert : « Cloaked and Dazed status cards always resolve simultaneously » ; +2 et -2 s'annulent sur une attaque",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [FORME_HEROS, "Puzzle.Daze('01001a')", "Puzzle.Cloak('01001a')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Attack('01001a')"],
        "cibles": ["01094"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 2]], "statuts_absents": [["01001a", "Dazed"], ["01001a", "Cloaked"]]},
    },
    {
        "nom": "[dazed] Cloaked + Dazed, degats : +2 -2 = degats imprimes (1 degat -> 1 subi), les DEUX cartes partent",
        "pourquoi": "simultane : 1 + 2 - 2 = 1 (et non 2 si Cloaked retirait d'abord 1 puis Dazed ajoutait 2)",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [FORME_HEROS, "Puzzle.Daze('01001a')", "Puzzle.Cloak('01001a')"],
        "declencher": ["Puzzle.Damage('01001a', 1)"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 1, "statuts_absents": [["01001a", "Dazed"], ["01001a", "Cloaked"]]},
    },
    {
        "nom": "[dazed] la carte d'etat est bien posee puis reconnue (HasStatus Dazed)",
        "pourquoi": "Puzzle.Daze pose une vraie carte d'etat comptee par HasStatus",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [FORME_HEROS, "Puzzle.Daze('01001a')"],
        "declencher": [],
        "verifier": "etat_attendu",
        "attendu": {"statuts": [["01001a", "Dazed"]]},
    },
]


VERIFICATIONS = r'''
def dazed_unique(monde, aides):
    """Tente une SECONDE pose de Dazed sur l'identite deja Dazed ; `attendu.cartes` = nombre de cartes Dazed apres."""
    from game.operate.faces import Faces
    from game.effect.rule import GameRule
    identite = aides["identite"](monde)
    avant = identite.dazed
    Faces.GiveStatus([identite], "Dazed", GameRule(identite))
    apres = identite.dazed
    voulu = aides["cas"]["attendu"]["cartes"]
    if avant != 1:
        return False, f"montage : {avant} carte(s) Dazed avant la seconde pose (attendu 1)"
    if apres != voulu:
        return False, f"{apres} carte(s) Dazed apres une seconde pose (attendu {voulu})"
    return True, f"une seule carte Dazed apres deux poses ({apres})"
'''
